#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parse YouTube Studio CSV exports and convert to analytics JSON format.

Usage:
    python parse_youtube_csv.py "path/to/Informations relatives aux tableaux.csv"

Output:
    Creates a JSON file with structured analytics data ready for report generation.
"""

import csv
import json
import sys
import io
from pathlib import Path
from datetime import datetime

# Force UTF-8 output
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def time_to_seconds(time_str):
    """Convert HH:MM:SS or M:SS format to seconds."""
    if not time_str or time_str == "-":
        return 0
    parts = time_str.split(":")
    if len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    elif len(parts) == 2:
        return int(parts[0]) * 60 + int(parts[1])
    return 0

def seconds_to_hms(seconds):
    """Convert seconds back to HH:MM:SS format."""
    if seconds == 0:
        return "0:00"
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"

def parse_youtube_csv(csv_path):
    """Parse YouTube Studio CSV and return structured data."""

    csv_file = Path(csv_path)
    if not csv_file.exists():
        print(f"❌ File not found: {csv_path}")
        sys.exit(1)

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        print("❌ CSV file is empty")
        sys.exit(1)

    # Get the "Total" row (usually the first one)
    total_row = rows[0]

    # Extract metrics
    data = {
        "metadata": {
            "source": "YouTube Studio CSV",
            "parsed_at": datetime.now().isoformat(),
            "csv_file": csv_file.name
        },
        "video_metrics": {},
        "retention": {},
        "audience": {}
    }

    # Parse main metrics
    def get_value(key, default=0):
        val = total_row.get(key, "").strip()
        if not val or val == "-":
            return default
        return val

    # Video performance metrics
    average_view_duration = get_value("Durée moyenne d'une vue", "0:00")
    avg_view_duration_sec = time_to_seconds(average_view_duration)

    # Views and impressions
    views = int(get_value("Vues", 0))
    impressions = int(get_value("Impressions", 0))
    watch_time_hours = float(get_value("Durée de visionnage (heures)", 0))
    ctr = float(get_value("Taux de clics par impression (%)", 0))

    # Retention
    avg_pct_watched = float(get_value("Pourcentage moyen de vidéo regardé (%)", 0))

    # Audience metrics
    unique_viewers = int(get_value("Spectateurs uniques", 0))
    intentional_views = int(get_value("Vues intentionnelles", 0))
    new_subscribers = int(get_value("Nouveaux abonnés", 0))
    shares = int(get_value("Partages", 0))
    regular_viewers = int(get_value("Spectateurs réguliers", 0))
    casual_viewers = int(get_value("Spectateurs occasionnels", 0))

    # Calculate derived metrics
    if views > 0:
        revisit_rate = (views - intentional_views) / views * 100
    else:
        revisit_rate = 0

    if views > 0:
        subscriber_conversion = (new_subscribers / views) * 100
    else:
        subscriber_conversion = 0

    # Populate data
    data["video_metrics"] = {
        "views": views,
        "impressions": impressions,
        "ctr": round(ctr, 2),
        "watch_time_hours": round(watch_time_hours, 2),
        "average_view_duration": average_view_duration,
        "average_view_duration_seconds": avg_view_duration_sec,
        "avg_percent_watched": round(avg_pct_watched, 2)
    }

    data["audience"] = {
        "unique_viewers": unique_viewers,
        "intentional_views": intentional_views,
        "revisit_rate_percent": round(revisit_rate, 2),
        "new_subscribers": new_subscribers,
        "subscriber_conversion_percent": round(subscriber_conversion, 2),
        "shares": shares,
        "regular_viewers": regular_viewers,
        "casual_viewers": casual_viewers
    }

    data["retention"] = {
        "avg_percent_watched": round(avg_pct_watched, 2),
        "status": "good" if avg_pct_watched >= 30 else "bad" if avg_pct_watched < 20 else "average"
    }

    return data

def main():
    if len(sys.argv) < 2:
        print("Usage: python parse_youtube_csv.py 'path/to/Informations relatives aux tableaux.csv'")
        print("\nExample:")
        print("  python parse_youtube_csv.py 'YouTube Studio .csv/Informations relatives aux tableaux.csv'")
        sys.exit(1)

    csv_path = sys.argv[1]

    print(f"📊 Parsing YouTube CSV: {csv_path}")
    data = parse_youtube_csv(csv_path)

    # Generate output filename
    input_file = Path(csv_path)
    output_file = input_file.parent / f"analytics_{input_file.stem}.json"

    # Save JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Parsed successfully!")
    print(f"📄 Output: {output_file}")
    print(f"\n📈 Quick summary:")
    print(f"  Views: {data['video_metrics']['views']}")
    print(f"  CTR: {data['video_metrics']['ctr']}%")
    print(f"  Avg % watched: {data['retention']['avg_percent_watched']}%")
    print(f"  New subscribers: {data['audience']['new_subscribers']}")

    return output_file

if __name__ == "__main__":
    main()
