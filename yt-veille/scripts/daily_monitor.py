"""Daily YouTube channel monitor — detects new videos and outliers."""
import logging
import os
import statistics
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from logging.handlers import RotatingFileHandler
from pathlib import Path

from dotenv import load_dotenv

from json_io import read_json, write_json
from youtube_api import YouTubeClient

SCRIPT_DIR = Path(__file__).parent
CONFIG_DIR = SCRIPT_DIR / "config"
DATA_DIR = SCRIPT_DIR / "data"
PROJECT_ROOT = SCRIPT_DIR.parent.parent
BACKLOG_PATH = PROJECT_ROOT / "context" / "backlog.json"

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


def detect_new_videos(uploads: list[dict], checked_ids: set) -> list[dict]:
    return [v for v in uploads if v["video_id"] not in checked_ids]


def compute_outliers(video_views: dict, history: list[int]) -> dict:
    result = {}
    if len(history) < 5:
        for vid, views in video_views.items():
            result[vid] = {"outlier": False, "median_views": None, "outlier_ratio": None}
        return result
    median = statistics.median(history)
    for vid, views in video_views.items():
        ratio = views / median if median > 0 else 0
        result[vid] = {
            "outlier": ratio > 3.0,
            "median_views": median,
            "outlier_ratio": ratio,
        }
    return result


def deduplicate_backlog(existing_items: list[dict], new_items: list[dict]) -> list[dict]:
    existing_ids = {item["id"] for item in existing_items}
    return [item for item in new_items if item["id"] not in existing_ids]


def prune_backlog(items: list[dict], max_age_days: int = 90) -> tuple[list[dict], list[dict]]:
    cutoff = datetime.now(timezone.utc) - timedelta(days=max_age_days)
    kept, archived = [], []
    for item in items:
        detected = datetime.fromisoformat(item["detected_at"].replace("Z", "+00:00"))
        if detected >= cutoff:
            kept.append(item)
        else:
            archived.append(item)
    return kept, archived


def save_archive(archived: list[dict], project_root: Path):
    if not archived:
        return
    archive_dir = project_root / "context" / "backlog-archive"
    by_month = {}
    for item in archived:
        month_key = item["detected_at"][:7]
        by_month.setdefault(month_key, []).append(item)
    for month_key, items in by_month.items():
        path = str(archive_dir / f"{month_key}.json")
        existing = read_json(path, default={"items": []})
        existing_ids = {i["id"] for i in existing["items"]}
        new_items = [i for i in items if i["id"] not in existing_ids]
        existing["items"].extend(new_items)
        write_json(path, existing)
    logger.info("Archived %d items across %d month(s)", len(archived), len(by_month))


def build_backlog_entry(
    video_id: str, title: str, channel_name: str, channel_id: str,
    published_at: str, views: int, likes: int, comments: int,
    subscribers: int, outlier: bool, median_views, outlier_ratio,
) -> dict:
    return {
        "id": video_id,
        "title": title,
        "channel": channel_name,
        "channel_id": channel_id,
        "published": published_at,
        "views": views,
        "likes": likes,
        "comments": comments,
        "channel_subscribers": subscribers,
        "thumbnail": f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg",
        "url": f"https://www.youtube.com/watch?v={video_id}",
        "outlier": outlier,
        "median_views": median_views,
        "outlier_ratio": outlier_ratio,
        "detected_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "daily_monitor",
    }


def git_push(project_root: Path):
    try:
        subprocess.run(
            ["git", "pull", "--rebase"],
            cwd=project_root, check=True, capture_output=True, text=True
        )
        subprocess.run(
            ["git", "add", "context/backlog.json", "context/backlog-archive/", "yt-veille/scripts/data/"],
            cwd=project_root, check=True, capture_output=True, text=True
        )
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=project_root, capture_output=True, text=True
        )
        if not result.stdout.strip():
            logger.info("No changes to commit")
            return
        subprocess.run(
            ["git", "commit", "-m", "chore(veille): daily monitor update"],
            cwd=project_root, check=True, capture_output=True, text=True
        )
        subprocess.run(
            ["git", "push"],
            cwd=project_root, check=True, capture_output=True, text=True
        )
        logger.info("Changes pushed to GitHub")
    except subprocess.CalledProcessError as e:
        logger.error("Git operation failed: %s\n%s", e, e.stderr)
        subprocess.run(["git", "rebase", "--abort"], cwd=project_root, capture_output=True)
        sys.exit(1)


def main():
    setup_logging()
    load_dotenv(SCRIPT_DIR / ".env")

    api_key = os.environ.get("YOUTUBE_API_KEY")
    if not api_key:
        logger.error("YOUTUBE_API_KEY not set")
        sys.exit(1)

    client = YouTubeClient(api_key)
    channels = read_json(str(CONFIG_DIR / "channels.json"), default={"channels": []})
    last_check = read_json(str(DATA_DIR / "last_check.json"), default={"last_check_utc": None, "checked_video_ids": []})
    channel_stats = read_json(str(DATA_DIR / "channel_stats.json"), default={})
    backlog = read_json(str(BACKLOG_PATH), default={"last_updated": None, "items": []})

    checked_ids = set(last_check.get("checked_video_ids", []))
    all_new_checked_ids = set()
    new_entries = []
    total_new = 0
    total_outliers = 0

    for ch in channels.get("channels", []):
        cid = ch["channel_id"]
        logger.info("Checking channel: %s (%s)", ch["handle"], cid)

        stats = client.get_channel_stats(cid)
        if stats is None:
            logger.warning("Skipping channel %s — could not fetch stats", ch["handle"])
            continue

        uploads = client.get_latest_uploads(cid, max_results=10)
        new_videos = detect_new_videos(uploads, checked_ids)

        if not new_videos:
            logger.info("  No new videos for %s", ch["handle"])
            all_new_checked_ids.update(v["video_id"] for v in uploads)
            continue

        video_ids = [v["video_id"] for v in new_videos]
        video_stats = client.get_video_stats(video_ids)
        all_new_checked_ids.update(v["video_id"] for v in uploads)

        history = channel_stats.get(cid, {"views_history": []})
        views_history = history.get("views_history", [])

        video_views = {vid: video_stats.get(vid, {}).get("views", 0) for vid in video_ids}
        outlier_info = compute_outliers(video_views, views_history)

        for v in new_videos:
            vid = v["video_id"]
            vs = video_stats.get(vid, {"views": 0, "likes": 0, "comments": 0})
            oi = outlier_info.get(vid, {"outlier": False, "median_views": None, "outlier_ratio": None})

            entry = build_backlog_entry(
                video_id=vid,
                title=v["title"],
                channel_name=ch["handle"],
                channel_id=cid,
                published_at=v["published_at"],
                views=vs["views"],
                likes=vs["likes"],
                comments=vs["comments"],
                subscribers=stats["subscriber_count"],
                outlier=oi["outlier"],
                median_views=oi["median_views"],
                outlier_ratio=oi["outlier_ratio"],
            )
            new_entries.append(entry)
            views_history.append(vs["views"])
            if oi["outlier"]:
                total_outliers += 1

        channel_stats[cid] = {
            "handle": ch["handle"],
            "subscriber_count": stats["subscriber_count"],
            "views_history": views_history[-20:],
            "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        total_new += len(new_videos)

    deduped = deduplicate_backlog(backlog.get("items", []), new_entries)
    backlog["items"] = deduped + backlog.get("items", [])

    kept, archived = prune_backlog(backlog["items"])
    backlog["items"] = kept
    save_archive(archived, PROJECT_ROOT)

    backlog["last_updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    write_json(str(BACKLOG_PATH), backlog)
    write_json(str(DATA_DIR / "last_check.json"), {
        "last_check_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "checked_video_ids": list(checked_ids | all_new_checked_ids),
    })
    write_json(str(DATA_DIR / "channel_stats.json"), channel_stats)

    logger.info("Checked %d channels, %d new videos, %d outliers", len(channels.get("channels", [])), total_new, total_outliers)

    git_push(PROJECT_ROOT)


if __name__ == "__main__":
    main()
