"""Daily YouTube channel monitor — scrapes videos and stores in SQLite."""
import logging
import os
import sys
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler
from pathlib import Path

from dotenv import load_dotenv

from database import init_db, upsert_channel, upsert_video, insert_snapshot
from json_io import read_json
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
    """Scrape channels and store raw data in DB. No scoring."""
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
                duration_seconds=d["duration_seconds"],
                published_at=d["published_at"],
            )
            insert_snapshot(
                db_path, video_id=vid_id, scraped_at=today,
                views=d["views"], likes=d["likes"], comments=d["comments"],
            )

        logger.info("  Inserted %d videos for %s", len(details), ch["handle"])

    logger.info("Scrape complete: %d channels", len(channels))


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
