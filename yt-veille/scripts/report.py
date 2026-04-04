"""Generate top 15 report — Notion table + JSON for orchestrator."""
import json
import logging
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from database import get_video_snapshots, get_all_videos
from scoring import compute_score, compute_channel_stats, apply_tier_boost, apply_decay
from topic_extractor import extract_topic

SCRIPT_DIR = Path(__file__).parent
CONFIG_DIR = SCRIPT_DIR / "config"
OUTPUT_DIR = SCRIPT_DIR.parent.parent / "context"

logger = logging.getLogger("report")


def load_tier_map() -> dict:
    config_path = str(CONFIG_DIR / "channels.json")
    with open(config_path) as f:
        config = json.load(f)
    return {c["channel_id"]: c.get("tier", "Non classé") for c in config["channels"]}


def score_all_videos(db_path: str) -> list[dict]:
    """Score all videos and return sorted list with decay applied."""
    tier_map = load_tier_map()
    videos = get_all_videos(db_path)

    # Group videos by channel
    by_channel = {}
    for v in videos:
        by_channel.setdefault(v["channel_id"], []).append(v)

    results = []
    for ch_id, ch_videos in by_channel.items():
        # Build snapshots for channel stats
        vid_snapshots = {}
        for v in ch_videos:
            vid_snapshots[v["video_id"]] = get_video_snapshots(v["video_id"], db_path)

        ch_stats = compute_channel_stats(vid_snapshots)
        tier = tier_map.get(ch_id, "Non classé")
        subs = ch_videos[0]["channel_subscribers"]

        for v in ch_videos:
            snaps = vid_snapshots.get(v["video_id"], [])
            if not snaps:
                continue
            latest = snaps[-1]

            metrics = compute_score(
                views=latest["views"], likes=latest["likes"], comments=latest["comments"],
                channel_median=ch_stats["median_views"],
                channel_avg_velocity=ch_stats["avg_velocity"],
                channel_subscribers=subs, snapshots=snaps,
                published_at=v["published_at"],
            )

            boosted = apply_tier_boost(metrics["composite"], tier)
            decayed, anomaly = apply_decay(boosted, v["published_at"])

            if decayed > 0:
                topic = extract_topic(v["title"] or "", v["description"] or "")
                results.append({
                    "video_id": v["video_id"],
                    "title": v["title"],
                    "channel": v["channel_handle"],
                    "description": (v["description"] or "")[:500],
                    "published_at": v["published_at"],
                    "topic": topic,
                    "score": decayed,
                    "anomaly": anomaly,
                    "url": f"https://www.youtube.com/watch?v={v['video_id']}",
                })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results


def generate_json(top15: list[dict], output_path: str):
    """Write top 15 as JSON for orchestrator."""
    data = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "count": len(top15),
        "videos": [
            {
                "title": v["title"],
                "channel": v["channel"],
                "description": v["description"],
                "url": v["url"],
                "topic": v["topic"],
                "score": v["score"],
            }
            for v in top15
        ],
    }
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logger.info("JSON written to %s", output_path)


def push_to_notion(top15: list[dict], token: str, parent_page: str):
    """Create a dated Notion table with the top 15."""
    today = datetime.now().strftime("%Y-%m-%d")

    # Create database
    r = subprocess.run(
        ["curl", "-s", "-X", "POST", "https://api.notion.com/v1/databases",
         "-H", f"Authorization: Bearer {token}",
         "-H", "Notion-Version: 2022-06-28",
         "-H", "Content-Type: application/json",
         "-d", json.dumps({
             "parent": {"page_id": parent_page},
             "title": [{"type": "text", "text": {"content": f"Top 15 — {today}"}}],
             "properties": {
                 "Titre": {"title": {}},
                 "Chaîne": {"rich_text": {}},
                 "Description": {"rich_text": {}},
                 "Lien": {"url": {}},
                 "Topic": {"select": {}},
                 "Score": {"number": {}},
             }
         })],
        capture_output=True, text=True
    )
    db = json.loads(r.stdout)
    db_id = db.get("id")
    if not db_id:
        logger.error("Failed to create Notion table: %s", r.stdout)
        return

    logger.info("Notion table created: %s", db_id)

    import time
    for v in top15:
        payload = json.dumps({
            "parent": {"database_id": db_id},
            "properties": {
                "Titre": {"title": [{"text": {"content": v["title"][:100]}}]},
                "Chaîne": {"rich_text": [{"text": {"content": v["channel"]}}]},
                "Description": {"rich_text": [{"text": {"content": v["description"][:500]}}]} if v["description"] else {"rich_text": []},
                "Lien": {"url": v["url"]},
                "Topic": {"select": {"name": v["topic"]}},
                "Score": {"number": v["score"]},
            }
        })
        subprocess.run(
            ["curl", "-s", "-X", "POST", "https://api.notion.com/v1/pages",
             "-H", f"Authorization: Bearer {token}",
             "-H", "Notion-Version: 2022-06-28",
             "-H", "Content-Type: application/json",
             "-d", payload],
            capture_output=True, text=True
        )
        time.sleep(0.35)

    logger.info("Pushed %d videos to Notion", len(top15))


def main():
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")

    db_path = str(SCRIPT_DIR / "data" / "veille.db")
    json_path = str(OUTPUT_DIR / "veille-top15.json")

    notion_token = os.environ.get("NOTION_TOKEN", "")
    notion_page = os.environ.get("NOTION_VEILLE_PAGE", "")

    # Score and get top 15
    all_scored = score_all_videos(db_path)
    top15 = all_scored[:15]

    # Print
    print(f"\n{'='*70}")
    print(f" TOP 15 — {datetime.now().strftime('%Y-%m-%d')}")
    print(f"{'='*70}\n")
    for i, v in enumerate(top15, 1):
        print(f" {i:2d}. {v['score']:5.1f} | {v['channel'][:25]:25s} | {v['topic']:15s} | {v['title'][:45]}")
    print()

    # JSON
    generate_json(top15, json_path)

    # Notion
    if notion_token and notion_page:
        push_to_notion(top15, notion_token, notion_page)
    else:
        logger.info("Skipping Notion (NOTION_TOKEN or NOTION_VEILLE_PAGE not set)")


if __name__ == "__main__":
    main()
