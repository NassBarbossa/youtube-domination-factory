#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parse YouTube Studio CSV exports and convert to analytics JSON format.

Usage:
    python parse_youtube_csv.py "path/to/Informations relatives aux tableaux.csv"

Expects exactly these 13 columns (YouTube Studio EN export):
    Content, Unique viewers, New viewers, Returning viewers, Shares,
    Average percentage viewed (%), Engaged views, Views,
    Watch time (hours), Subscribers, Average view duration,
    Impressions, Impressions click-through rate (%)
"""

import csv
import json
import sys
import io
from pathlib import Path
from datetime import datetime

if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

EXPECTED_COLUMNS = {
    "Content",
    "Unique viewers",
    "New viewers",
    "Returning viewers",
    "Shares",
    "Average percentage viewed (%)",
    "Engaged views",
    "Views",
    "Watch time (hours)",
    "Subscribers",
    "Average view duration",
    "Impressions",
    "Impressions click-through rate (%)",
}


def validate_columns(headers):
    """Validate that the CSV has exactly the 13 expected columns."""
    found = set(h.strip() for h in headers)
    missing = EXPECTED_COLUMNS - found
    extra = found - EXPECTED_COLUMNS

    errors = []
    if missing:
        errors.append(f"Missing columns: {', '.join(sorted(missing))}")
    if extra:
        errors.append(f"Unexpected columns: {', '.join(sorted(extra))}")

    if errors:
        print("❌ CSV validation failed.\n")
        for e in errors:
            print(f"   {e}")
        print(f"\n   Expected exactly these 13 columns:")
        for col in sorted(EXPECTED_COLUMNS):
            status = "✓" if col in found else "✗"
            print(f"     {status} {col}")
        print("\n   Re-export from YouTube Studio with the correct columns selected.")
        sys.exit(1)


def time_to_seconds(time_str):
    """Convert H:MM:SS or M:SS to seconds."""
    if not time_str or time_str == "-":
        return 0
    parts = time_str.split(":")
    if len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    elif len(parts) == 2:
        return int(parts[0]) * 60 + int(parts[1])
    return 0


def seconds_to_hms(seconds):
    """Convert seconds to H:MM:SS or M:SS."""
    if seconds == 0:
        return "0:00"
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def safe_int(value, default=0):
    """Parse a string to int, return default if empty or invalid."""
    if not value or value.strip() in ("", "-"):
        return default
    try:
        return int(value.strip())
    except ValueError:
        return default


def safe_float(value, default=0.0):
    """Parse a string to float, return default if empty or invalid."""
    if not value or value.strip() in ("", "-"):
        return default
    try:
        return float(value.strip())
    except ValueError:
        return default


def parse_youtube_csv(csv_path):
    """Parse YouTube Studio CSV and return structured data."""

    csv_file = Path(csv_path)
    if not csv_file.exists():
        print(f"❌ File not found: {csv_path}")
        sys.exit(1)

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames

        if not headers:
            print("❌ CSV file is empty or has no header row.")
            sys.exit(1)

        validate_columns(headers)

        rows = list(reader)

    if not rows:
        print("❌ CSV has headers but no data rows.")
        sys.exit(1)

    row = rows[0]

    # --- Parse raw values ---
    views = safe_int(row["Views"])
    engaged_views = safe_int(row["Engaged views"])
    impressions = safe_int(row["Impressions"])
    ctr = safe_float(row["Impressions click-through rate (%)"])
    avg_pct_watched = safe_float(row["Average percentage viewed (%)"])
    avg_view_duration_raw = row.get("Average view duration", "0:00").strip()
    avg_view_duration_sec = time_to_seconds(avg_view_duration_raw)
    watch_time_hours = safe_float(row["Watch time (hours)"])
    unique_viewers = safe_int(row["Unique viewers"])
    new_viewers = safe_int(row["New viewers"])
    returning_viewers = safe_int(row["Returning viewers"])
    shares = safe_int(row["Shares"])
    subscribers = safe_int(row["Subscribers"])

    # --- Derived metrics ---
    subscriber_conversion = round((subscribers / views) * 100, 2) if views > 0 else 0
    share_rate = round((shares / views) * 100, 2) if views > 0 else 0
    views_per_viewer = round(views / unique_viewers, 2) if unique_viewers > 0 else 0
    estimated_video_duration_sec = round(avg_view_duration_sec / (avg_pct_watched / 100)) if avg_pct_watched > 0 else 0

    # --- Build output ---
    data = {
        "metadata": {
            "source": "YouTube Studio CSV (EN)",
            "parsed_at": datetime.now().isoformat(),
            "csv_file": csv_file.name
        },
        "video_metrics": {
            "views": views,
            "engaged_views": engaged_views,
            "impressions": impressions,
            "ctr": round(ctr, 2),
            "avg_percentage_viewed": round(avg_pct_watched, 2),
            "avg_view_duration": avg_view_duration_raw,
            "avg_view_duration_seconds": avg_view_duration_sec,
            "watch_time_hours": round(watch_time_hours, 2),
            "estimated_video_duration": seconds_to_hms(estimated_video_duration_sec),
            "estimated_video_duration_seconds": estimated_video_duration_sec
        },
        "audience": {
            "unique_viewers": unique_viewers,
            "new_viewers": new_viewers,
            "returning_viewers": returning_viewers,
            "views_per_viewer": views_per_viewer,
            "subscribers": subscribers,
            "subscriber_conversion_percent": subscriber_conversion,
            "shares": shares,
            "share_rate_percent": share_rate
        },
        "retention": {
            "avg_percentage_viewed": round(avg_pct_watched, 2),
            "status": "great" if avg_pct_watched >= 60
                else "good" if avg_pct_watched >= 45
                else "average" if avg_pct_watched >= 30
                else "bad"
        }
    }

    return data


def main():
    if len(sys.argv) < 2:
        print("Usage: python parse_youtube_csv.py 'path/to/Informations relatives aux tableaux.csv'")
        print("\nExpects a YouTube Studio CSV export (EN) with these 13 columns:")
        for col in sorted(EXPECTED_COLUMNS):
            print(f"  - {col}")
        sys.exit(1)

    csv_path = sys.argv[1]

    print(f"📊 Parsing: {csv_path}")
    data = parse_youtube_csv(csv_path)

    # Output to same directory as input
    input_file = Path(csv_path)
    output_file = input_file.parent / f"analytics_{input_file.stem}.json"

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    vm = data["video_metrics"]
    aud = data["audience"]
    ret = data["retention"]

    print(f"✅ Parsed successfully → {output_file}\n")
    print(f"   Views: {vm['views']}  |  CTR: {vm['ctr']}%  |  Retention: {vm['avg_percentage_viewed']}% ({ret['status']})")
    print(f"   Subscribers: +{aud['subscribers']}  |  Shares: {aud['shares']}  |  Unique viewers: {aud['unique_viewers']}")

    return output_file


if __name__ == "__main__":
    main()
