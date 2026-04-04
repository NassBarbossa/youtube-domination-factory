"""Daily YouTube channel monitor — scrapes to SQLite, scores, extracts topics."""
import json
import logging
import os
import sys
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler
from pathlib import Path

from dotenv import load_dotenv

from database import (
    init_db, upsert_channel, upsert_video, insert_snapshot,
    get_channel_median, get_channel_avg_velocity,
    get_video_snapshots, update_video_score, update_channel_stats,
    get_connection,
)
from json_io import read_json
from scoring import compute_video_metrics
from topic_extractor import extract_topic
from youtube_api import YouTubeClient

SCRIPT_DIR = Path(__file__).parent
CONFIG_DIR = SCRIPT_DIR / "config"
DB_PATH = str(SCRIPT_DIR / "data" / "veille.db")

logger = logging.getLogger("daily_monitor")


def setup_logging():
    handler = RotatingFileHandler(
        "/var/log/yt-veille.log", maxBytes=5 * 1024 * 1024, backupCount=3
    )
    handler.setFormatter(logging.Formatter(
        "[%(asctime)s] %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    ))
    logger.addHandler(handler)
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)


def run_monitor(*, db_path: str, client, channels: list[dict]):
    """Core monitor logic — testable without env/logging."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    for ch in channels:
        cid = ch["channel_id"]
        logger.info("Checking channel: %s (%s)", ch["handle"], cid)

        stats = client.get_channel_stats(cid)
        if stats is None:
            logger.warning("Skipping channel %s — could not fetch stats", ch["handle"])
            continue

        upsert_channel(
            db_path, channel_id=cid, handle=ch["handle"],
            subscribers=stats["subscriber_count"],
            niche=ch.get("niche", ""), added_at=ch.get("added_at", today),
        )

        max_vids = ch.get("max_videos", 5)
        uploads = client.get_latest_uploads(cid, max_results=max_vids)
        if not uploads:
            logger.info("  No uploads for %s", ch["handle"])
            continue

        video_ids = [v["video_id"] for v in uploads]
        details = client.get_video_details(video_ids)

        for vid_id, d in details.items():
            upsert_video(
                db_path, video_id=vid_id, channel_id=cid,
                title=d["title"], description=d["description"],
                tags=json.dumps(d["tags"]), duration_seconds=d["duration_seconds"],
                published_at=d["published_at"], thumbnail_url=d["thumbnail_url"],
                category_id=d["category_id"], detected_at=today,
            )
            insert_snapshot(
                db_path, video_id=vid_id, scraped_at=today,
                views=d["views"], likes=d["likes"], comments=d["comments"],
            )

        logger.info("  Inserted %d videos for %s", len(details), ch["handle"])

    logger.info("Running scoring pass...")
    _score_all_videos(db_path, channels)


def _score_all_videos(db_path: str, channels: list[dict]):
    """Score all videos and extract topics for those above threshold."""
    for ch in channels:
        cid = ch["channel_id"]
        median = get_channel_median(cid, db_path)
        avg_vel = get_channel_avg_velocity(cid, db_path)

        if median is None or median == 0:
            logger.info("  Not enough data for %s — skipping scoring", ch["handle"])
            continue

        if avg_vel is None:
            avg_vel = 0

        update_channel_stats(db_path, cid, median, avg_vel)

        conn = get_connection(db_path)
        ch_row = conn.execute(
            "SELECT subscribers FROM channels WHERE channel_id=?", (cid,)
        ).fetchone()
        subscribers = ch_row[0] if ch_row else 0

        videos = conn.execute(
            "SELECT video_id, title, description, published_at FROM videos WHERE channel_id=?", (cid,)
        ).fetchall()
        conn.close()

        for vid_row in videos:
            vid_id, title, description, published_at = vid_row[0], vid_row[1], vid_row[2], vid_row[3]
            snapshots = get_video_snapshots(vid_id, db_path)
            if not snapshots:
                continue

            metrics = compute_video_metrics(
                snapshots=snapshots,
                channel_median=median,
                channel_avg_velocity=avg_vel,
                channel_subscribers=subscribers,
                published_at=published_at,
            )

            topic = None
            if metrics["composite"] > 50:
                topic = extract_topic(title or "", description or "")

            update_video_score(db_path, vid_id, metrics["composite"], topic)

        logger.info("  Scored videos for %s (median=%.0f, avg_vel=%.0f)",
                     ch["handle"], median, avg_vel or 0)


def main():
    setup_logging()
    load_dotenv(SCRIPT_DIR / ".env")

    api_key = os.environ.get("YOUTUBE_API_KEY")
    if not api_key:
        logger.error("YOUTUBE_API_KEY not set")
        sys.exit(1)

    init_db(DB_PATH)
    client = YouTubeClient(api_key)
    channels_config = read_json(str(CONFIG_DIR / "channels.json"), default={"channels": []})
    channels = channels_config.get("channels", [])

    run_monitor(db_path=DB_PATH, client=client, channels=channels)
    logger.info("Daily monitor complete.")


if __name__ == "__main__":
    main()
