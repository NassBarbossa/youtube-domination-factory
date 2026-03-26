"""Discover new YouTube creators in the AI/Claude Code niche."""
import logging
import os
import sys
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

from json_io import read_json, write_json
from youtube_api import YouTubeClient

SCRIPT_DIR = Path(__file__).parent
CONFIG_DIR = SCRIPT_DIR / "config"

logger = logging.getLogger("discover_creators")


def filter_known_channels(found: list[dict], known_ids: set) -> list[dict]:
    return [ch for ch in found if ch["channel_id"] not in known_ids]


def score_channel(channel: dict, keywords: list[str]) -> dict:
    text = (channel.get("title", "") + " " + channel.get("description", "")).lower()

    relevance = sum(1 for kw in keywords if kw.lower() in text)
    sub_count = channel.get("subscriber_count", 0)
    video_count = channel.get("video_count", 0)

    if sub_count >= 100000:
        size = 3
    elif sub_count >= 10000:
        size = 2
    elif sub_count >= 1000:
        size = 1
    else:
        size = 0

    if video_count >= 50:
        activity = 2
    elif video_count >= 10:
        activity = 1
    else:
        activity = 0

    return {
        "relevance": relevance,
        "size": size,
        "activity": activity,
        "total": relevance + size + activity,
    }


def main():
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
    load_dotenv(SCRIPT_DIR / ".env")

    api_key = os.environ.get("YOUTUBE_API_KEY")
    if not api_key:
        logger.error("YOUTUBE_API_KEY not set")
        sys.exit(1)

    client = YouTubeClient(api_key)
    channels_config = read_json(str(CONFIG_DIR / "channels.json"), default={"channels": []})
    keywords_config = read_json(str(CONFIG_DIR / "keywords.json"), default={"keywords": []})

    known_ids = {ch["channel_id"] for ch in channels_config.get("channels", [])}
    keywords = keywords_config.get("keywords", [])

    all_candidates = []

    for kw in keywords:
        logger.info("Searching for: %s", kw)
        found = client.search_channels(kw, max_results=10)
        new_channels = filter_known_channels(found, known_ids)

        for ch in new_channels:
            stats = client.get_channel_stats(ch["channel_id"])
            if stats is None:
                continue
            ch.update(stats)
            ch["scores"] = score_channel(ch, keywords)
            if ch["scores"]["relevance"] > 0:
                all_candidates.append(ch)
            known_ids.add(ch["channel_id"])

    all_candidates.sort(key=lambda c: c["scores"]["total"], reverse=True)

    if not all_candidates:
        print("\nNo new relevant creators found.")
        return

    print(f"\n{'='*60}")
    print(f" Found {len(all_candidates)} new creator(s)")
    print(f"{'='*60}\n")

    for i, ch in enumerate(all_candidates, 1):
        s = ch["scores"]
        print(f"{i}. {ch['title']}")
        print(f"   Channel ID: {ch['channel_id']}")
        print(f"   Subscribers: {ch.get('subscriber_count', '?'):,}")
        print(f"   Videos: {ch.get('video_count', '?')}")
        print(f"   Score: relevance={s['relevance']} size={s['size']} activity={s['activity']} total={s['total']}")
        print(f"   Description: {ch.get('description', '')[:100]}")
        print()

    print("Enter the numbers of channels to add (comma-separated), or 'q' to quit:")
    choice = input("> ").strip()
    if choice.lower() == "q":
        return

    indices = [int(x.strip()) - 1 for x in choice.split(",") if x.strip().isdigit()]
    added = 0
    for idx in indices:
        if 0 <= idx < len(all_candidates):
            ch = all_candidates[idx]
            channels_config["channels"].append({
                "handle": ch["title"],
                "channel_id": ch["channel_id"],
                "niche": "discovered",
                "added_at": date.today().isoformat(),
            })
            added += 1
            print(f"  Added: {ch['title']}")

    if added > 0:
        write_json(str(CONFIG_DIR / "channels.json"), channels_config)
        print(f"\n{added} channel(s) added to channels.json")


if __name__ == "__main__":
    main()
