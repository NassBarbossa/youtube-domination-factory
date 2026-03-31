"""One-time script to discover AI/Claude Code channels."""
import os
from dotenv import load_dotenv
from youtube_api import YouTubeClient

load_dotenv(".env")
client = YouTubeClient(os.environ["YOUTUBE_API_KEY"])

keywords = [
    "Claude Code tutorial",
    "vibe coding AI",
    "vibecoding",
    "build app with AI",
    "Claude Code",
    "AI coding agent",
    "Cursor AI tutorial",
    "no code AI app",
    "AI tools for business",
    "AI automation tutorial",
    "Anthropic Claude",
    "AI agent workflow",
]

all_channels = {}
for kw in keywords:
    print(f"Searching: {kw}")
    results = client.search_channels(kw, max_results=15)
    for ch in results:
        cid = ch["channel_id"]
        if cid not in all_channels:
            stats = client.get_channel_stats(cid)
            if stats and stats["subscriber_count"] >= 5000:
                all_channels[cid] = {
                    "title": ch["title"],
                    "channel_id": cid,
                    "subscribers": stats["subscriber_count"],
                    "video_count": stats["video_count"],
                    "description": ch.get("description", "")[:100],
                    "found_via": kw,
                }

sorted_channels = sorted(all_channels.values(), key=lambda x: x["subscribers"], reverse=True)

print(f"\nFound {len(sorted_channels)} unique channels with 5k+ subs\n")
for i, ch in enumerate(sorted_channels, 1):
    print(f"{i:2d}. {ch['title'][:40]:40s} | {ch['subscribers']:>10,} subs | {ch['video_count']:>5} vids | via: {ch['found_via']}")
