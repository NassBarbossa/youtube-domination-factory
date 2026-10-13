#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parse YouTube Studio CSV exports and convert to analytics JSON format.

Usage:
    python parse_youtube_csv.py "path/to/Informations relatives aux tableaux.csv"

Accepts the YouTube Studio export in French (default for Nass) or in English.
Required columns (FR / EN):
    Vues / Views · Impressions · Taux de clics par impression (%) / Impressions click-through rate (%)
    Pourcentage moyen de vidéo regardé (%) / Average percentage viewed (%)
    Durée moyenne d'une vue / Average view duration · Durée de visionnage (heures) / Watch time (hours)
Optional (0 if absent): Vues intentionnelles / Engaged views, Spectateurs uniques / Unique viewers,
    Nouveaux spectateurs / New viewers, Spectateurs réguliers / Returning viewers, Partages / Shares,
    Abonnés ou Nouveaux abonnés / Subscribers
"""

import csv
import json
import sys
import io
from pathlib import Path
from datetime import datetime

if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Nom interne → en-têtes acceptés (FR d'abord, puis EN). Le premier trouvé dans le CSV gagne.
COLUMNS = {
    "content": ["Contenu", "Content"],
    "views": ["Vues", "Views"],
    "impressions": ["Impressions"],
    "ctr": ["Taux de clics par impression (%)", "Impressions click-through rate (%)"],
    "avg_pct_watched": ["Pourcentage moyen de vidéo regardé (%)", "Average percentage viewed (%)"],
    "avg_view_duration": ["Durée moyenne d'une vue", "Average view duration"],
    "watch_time_hours": ["Durée de visionnage (heures)", "Watch time (hours)"],
    "engaged_views": ["Vues intentionnelles", "Engaged views"],
    "unique_viewers": ["Spectateurs uniques", "Unique viewers"],
    "new_viewers": ["Nouveaux spectateurs", "New viewers"],
    "returning_viewers": ["Spectateurs réguliers", "Returning viewers"],
    "shares": ["Partages", "Shares"],
    "subscribers": ["Abonnés", "Nouveaux abonnés", "Subscribers"],
}
REQUIRED = ["views", "impressions", "ctr", "avg_pct_watched", "avg_view_duration", "watch_time_hours"]


def resolve_columns(headers):
    """Map internal names to the CSV's actual headers (FR or EN). Exits if a required column is missing."""
    found = [h.strip() for h in headers]
    mapping = {}
    for key, names in COLUMNS.items():
        for name in names:
            if name in found:
                mapping[key] = name
                break
    missing = [k for k in REQUIRED if k not in mapping]
    if missing:
        print("❌ Colonnes obligatoires absentes du CSV :")
        for k in missing:
            print(f"   ✗ {' / '.join(COLUMNS[k])}")
        print("\n   Ré-exporte depuis YouTube Studio (Analytics → Télécharger → CSV) avec ces colonnes.")
        sys.exit(1)
    lang = "FR" if mapping["views"] == "Vues" else "EN"
    return mapping, lang


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

        mapping, lang = resolve_columns(headers)

        rows = list(reader)

    if not rows:
        print("❌ CSV has headers but no data rows.")
        sys.exit(1)

    # Ligne « Total » (export vidéo) en premier ; sinon première ligne de données.
    row = next((r for r in rows if (r.get(mapping.get("content", ""), "") or "").strip().lower() == "total"), rows[0])
    row = {k.strip(): v for k, v in row.items() if k}

    def col(key, default=""):
        name = mapping.get(key)
        return row.get(name, default) if name else default

    # --- Parse raw values ---
    views = safe_int(col("views"))
    engaged_views = safe_int(col("engaged_views"))
    impressions = safe_int(col("impressions"))
    ctr = safe_float(col("ctr"))
    avg_pct_watched = safe_float(col("avg_pct_watched"))
    avg_view_duration_raw = (col("avg_view_duration", "0:00") or "0:00").strip()
    avg_view_duration_sec = time_to_seconds(avg_view_duration_raw)
    watch_time_hours = safe_float(col("watch_time_hours"))
    unique_viewers = safe_int(col("unique_viewers"))
    new_viewers = safe_int(col("new_viewers"))
    returning_viewers = safe_int(col("returning_viewers"))
    shares = safe_int(col("shares"))
    subscribers = safe_int(col("subscribers"))

    # --- Derived metrics ---
    subscriber_conversion = round((subscribers / views) * 100, 2) if views > 0 else 0
    share_rate = round((shares / views) * 100, 2) if views > 0 else 0
    views_per_viewer = round(views / unique_viewers, 2) if unique_viewers > 0 else 0
    estimated_video_duration_sec = round(avg_view_duration_sec / (avg_pct_watched / 100)) if avg_pct_watched > 0 else 0

    # --- Build output ---
    data = {
        "metadata": {
            "source": f"YouTube Studio CSV ({lang})",
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
        print("\nExport YouTube Studio (FR ou EN). Colonnes obligatoires :")
        for k in REQUIRED:
            print(f"  - {' / '.join(COLUMNS[k])}")
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
