#!/usr/bin/env python3
"""
Feedback Analyzer — Connects analytics data to production choices and extracts lessons.

Usage:
    python3 feedback_analyzer.py

This script:
1. Reads video-context archives (past video productions)
2. Fetches analytics performance for each video
3. Updates each skill's memory/choices.json with performance data
4. Extracts patterns and writes lessons to memory/lessons.json

Run this after analytics data is available (48h+ after publication).
"""

import json
import os
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
TOKEN_PATH = SCRIPT_DIR / "token.json"

# Skill memory paths
SKILLS = {
    "titres_seo": PROJECT_ROOT / "yt-titres-seo" / "memory",
    "miniature": PROJECT_ROOT / "yt-miniature" / "memory",
    "script": PROJECT_ROOT / "yt-script" / "memory",
    "veille": PROJECT_ROOT / "yt-veille" / "memory",
}


def get_credentials():
    with open(TOKEN_PATH) as f:
        token_data = json.load(f)
    creds = Credentials(
        token=token_data["token"],
        refresh_token=token_data["refresh_token"],
        token_uri=token_data["token_uri"],
        client_id=token_data["client_id"],
        client_secret=token_data["client_secret"],
        scopes=token_data["scopes"],
    )
    if creds.expired:
        creds.refresh(Request())
        token_data["token"] = creds.token
        with open(TOKEN_PATH, "w") as f:
            json.dump(token_data, f, indent=2)
    return creds


def read_json(path, default=None):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default if default is not None else {}


def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def get_video_performance(yt_analytics, video_id):
    """Fetch key performance metrics for a video."""
    try:
        resp = yt_analytics.reports().query(
            ids="channel==MINE",
            startDate="2026-01-01",
            endDate=datetime.now().strftime("%Y-%m-%d"),
            metrics="views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained,likes,comments,shares",
            filters=f"video=={video_id}",
        ).execute()
        if not resp.get("rows"):
            return None
        r = resp["rows"][0]
        return {
            "views": int(r[0]),
            "watch_time_min": round(r[1], 1),
            "avg_view_duration_sec": int(r[2]),
            "retention_pct": round(r[3], 1),
            "subscribers_gained": int(r[4]),
            "likes": int(r[5]),
            "comments": int(r[6]),
            "shares": int(r[7]),
            "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
    except Exception as e:
        print(f"  Error fetching analytics for {video_id}: {e}")
        return None


def get_channel_averages(yt_analytics):
    """Get channel-level averages for comparison."""
    try:
        resp = yt_analytics.reports().query(
            ids="channel==MINE",
            startDate="2026-01-01",
            endDate=datetime.now().strftime("%Y-%m-%d"),
            metrics="views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained",
            dimensions="video",
            sort="-views",
            maxResults=20,
        ).execute()
        if not resp.get("rows"):
            return None
        views_list = [int(r[1]) for r in resp["rows"]]
        retention_list = [float(r[4]) for r in resp["rows"]]
        return {
            "avg_views": round(statistics.mean(views_list), 1),
            "median_views": statistics.median(views_list),
            "avg_retention": round(statistics.mean(retention_list), 1),
        }
    except Exception:
        return None


def update_skill_choices(skill_name, memory_path, yt_analytics, channel_avgs):
    """Update performance data in a skill's choices.json."""
    choices_path = memory_path / "choices.json"
    choices = read_json(str(choices_path), {"choices": []})

    updated = 0
    for choice in choices.get("choices", []):
        if choice.get("performance") is not None:
            continue  # Already has performance data

        video_slug = choice.get("video_slug")
        if not video_slug:
            continue

        # Find video ID from context archives
        video_id = find_video_id(video_slug)
        if not video_id:
            continue

        perf = get_video_performance(yt_analytics, video_id)
        if perf:
            perf["performance_index"] = round(perf["views"] / channel_avgs["median_views"], 2) if channel_avgs else None
            choice["performance"] = perf
            updated += 1
            print(f"  [{skill_name}] Updated: {video_slug} — {perf['views']} views, {perf['retention_pct']}% retention")

    if updated > 0:
        write_json(str(choices_path), choices)
    return updated


def find_video_id(video_slug):
    """Find video ID from context archives or video-context.json."""
    # Check current context
    ctx_path = PROJECT_ROOT / "context" / "video-context.json"
    ctx = read_json(str(ctx_path))
    if ctx.get("_meta", {}).get("slug") == video_slug:
        # Try to find video ID from YouTube Data API lookup
        return None  # Would need video ID stored in context

    # Check archives
    archive_dir = PROJECT_ROOT / "context" / "archive"
    if archive_dir.exists():
        for f in archive_dir.iterdir():
            if f.suffix == ".json" and video_slug in f.name:
                data = read_json(str(f))
                return data.get("video_id")
    return None


def extract_lessons_titres(memory_path):
    """Extract title-specific lessons from choices with performance data."""
    choices = read_json(str(memory_path / "choices.json"), {"choices": []})
    completed = [c for c in choices.get("choices", []) if c.get("performance")]

    if len(completed) < 3:
        return

    lessons = []
    style_perf = {}

    # Group by style
    for c in completed:
        style = c.get("style", "unknown")
        perf = c["performance"]
        if style not in style_perf:
            style_perf[style] = {"count": 0, "ctr_list": [], "views_list": []}
        style_perf[style]["count"] += 1
        style_perf[style]["views_list"].append(perf["views"])
        # CTR will be added when available

    # Analyze number usage
    with_number = [c for c in completed if c.get("has_number")]
    without_number = [c for c in completed if not c.get("has_number")]
    if len(with_number) >= 2 and len(without_number) >= 1:
        avg_views_number = statistics.mean([c["performance"]["views"] for c in with_number])
        avg_views_no_number = statistics.mean([c["performance"]["views"] for c in without_number])
        if avg_views_number > avg_views_no_number * 1.2:
            lessons.append({
                "rule": f"Les titres avec chiffres font en moyenne {avg_views_number:.0f} vues vs {avg_views_no_number:.0f} sans",
                "evidence": f"Basé sur {len(with_number)} titres avec chiffres vs {len(without_number)} sans",
                "sample_size": len(completed),
                "confidence": "medium" if len(completed) >= 5 else "low",
                "created_at": datetime.now().strftime("%Y-%m-%d"),
            })

    # Analyze char length
    short_titles = [c for c in completed if c.get("char_count", 100) <= 50]
    long_titles = [c for c in completed if c.get("char_count", 0) > 50]
    if len(short_titles) >= 2 and len(long_titles) >= 1:
        avg_short = statistics.mean([c["performance"]["views"] for c in short_titles])
        avg_long = statistics.mean([c["performance"]["views"] for c in long_titles])
        if avg_short > avg_long * 1.2:
            lessons.append({
                "rule": f"Les titres courts (≤50 chars) font {avg_short:.0f} vues vs {avg_long:.0f} pour les longs",
                "evidence": f"Basé sur {len(short_titles)} courts vs {len(long_titles)} longs",
                "sample_size": len(completed),
                "confidence": "medium" if len(completed) >= 5 else "low",
                "created_at": datetime.now().strftime("%Y-%m-%d"),
            })

    # Analyze framing
    negative = [c for c in completed if c.get("framing") == "negative"]
    positive = [c for c in completed if c.get("framing") == "positive"]
    if len(negative) >= 1 and len(positive) >= 1:
        avg_neg = statistics.mean([c["performance"]["views"] for c in negative])
        avg_pos = statistics.mean([c["performance"]["views"] for c in positive])
        better = "négatif" if avg_neg > avg_pos else "positif"
        lessons.append({
            "rule": f"Le framing {better} performe mieux ({max(avg_neg, avg_pos):.0f} vs {min(avg_neg, avg_pos):.0f} vues)",
            "evidence": f"Basé sur {len(negative)} négatifs vs {len(positive)} positifs",
            "sample_size": len(completed),
            "confidence": "low",
            "created_at": datetime.now().strftime("%Y-%m-%d"),
        })

    # Build style performance summary
    style_summary = {}
    for style, data in style_perf.items():
        if data["views_list"]:
            style_summary[style] = {
                "count": data["count"],
                "avg_views": round(statistics.mean(data["views_list"]), 0),
            }

    # Write lessons
    lessons_data = {
        "last_updated": datetime.now().strftime("%Y-%m-%d"),
        "sample_size": len(completed),
        "lessons": lessons,
        "style_performance": style_summary,
    }
    write_json(str(memory_path / "lessons.json"), lessons_data)
    print(f"  [titres_seo] {len(lessons)} leçons extraites de {len(completed)} vidéos")


def extract_lessons_miniature(memory_path):
    """Extract thumbnail-specific lessons."""
    choices = read_json(str(memory_path / "choices.json"), {"choices": []})
    completed = [c for c in choices.get("choices", []) if c.get("performance")]

    if len(completed) < 3:
        return

    lessons = []

    # Analyze face presence
    with_face = [c for c in completed if c.get("has_face")]
    without_face = [c for c in completed if not c.get("has_face")]
    if len(with_face) >= 1 and len(without_face) >= 1:
        avg_face = statistics.mean([c["performance"]["views"] for c in with_face])
        avg_no_face = statistics.mean([c["performance"]["views"] for c in without_face])
        if avg_face > avg_no_face * 1.15:
            lessons.append({
                "rule": f"Les miniatures avec visage font {avg_face:.0f} vues vs {avg_no_face:.0f} sans",
                "evidence": f"{len(with_face)} avec visage vs {len(without_face)} sans",
                "sample_size": len(completed),
                "confidence": "medium" if len(completed) >= 5 else "low",
                "created_at": datetime.now().strftime("%Y-%m-%d"),
            })

    # Analyze dominant color
    color_perf = {}
    for c in completed:
        color = c.get("color_name", "unknown")
        views = c["performance"]["views"]
        if color not in color_perf:
            color_perf[color] = []
        color_perf[color].append(views)

    if len(color_perf) >= 2:
        best_color = max(color_perf.items(), key=lambda x: statistics.mean(x[1]))
        lessons.append({
            "rule": f"La couleur dominante '{best_color[0]}' performe le mieux ({statistics.mean(best_color[1]):.0f} vues moy.)",
            "evidence": f"Basé sur {len(best_color[1])} miniatures en {best_color[0]}",
            "sample_size": len(completed),
            "confidence": "low",
            "created_at": datetime.now().strftime("%Y-%m-%d"),
        })

    # Build concept performance
    concept_perf = {}
    for c in completed:
        key = f"{c.get('color_name', 'unknown')}-{'face' if c.get('has_face') else 'noface'}-{c.get('background_style', 'unknown')}"
        if key not in concept_perf:
            concept_perf[key] = {"count": 0, "views_list": []}
        concept_perf[key]["count"] += 1
        concept_perf[key]["views_list"].append(c["performance"]["views"])

    concept_summary = {}
    for key, data in concept_perf.items():
        concept_summary[key] = {
            "count": data["count"],
            "avg_views": round(statistics.mean(data["views_list"]), 0),
        }

    lessons_data = {
        "last_updated": datetime.now().strftime("%Y-%m-%d"),
        "sample_size": len(completed),
        "lessons": lessons,
        "concept_performance": concept_summary,
    }
    write_json(str(memory_path / "lessons.json"), lessons_data)
    print(f"  [miniature] {len(lessons)} leçons extraites de {len(completed)} vidéos")


def extract_lessons_script(memory_path):
    """Extract script/retention-specific lessons."""
    choices = read_json(str(memory_path / "choices.json"), {"choices": []})
    completed = [c for c in choices.get("choices", []) if c.get("performance")]

    if len(completed) < 3:
        return

    lessons = []

    # Analyze hook type vs retention
    hook_perf = {}
    for c in completed:
        hook = c.get("hook_type", "unknown")
        retention = c["performance"]["retention_pct"]
        if hook not in hook_perf:
            hook_perf[hook] = []
        hook_perf[hook].append(retention)

    if len(hook_perf) >= 2:
        best_hook = max(hook_perf.items(), key=lambda x: statistics.mean(x[1]))
        worst_hook = min(hook_perf.items(), key=lambda x: statistics.mean(x[1]))
        lessons.append({
            "rule": f"Les hooks '{best_hook[0]}' retiennent {statistics.mean(best_hook[1]):.1f}% vs '{worst_hook[0]}' à {statistics.mean(worst_hook[1]):.1f}%",
            "evidence": f"Basé sur {sum(len(v) for v in hook_perf.values())} vidéos",
            "sample_size": len(completed),
            "confidence": "medium" if len(completed) >= 5 else "low",
            "created_at": datetime.now().strftime("%Y-%m-%d"),
        })

    # Analyze duration vs retention
    short_vids = [c for c in completed if c.get("estimated_duration_min", 0) <= 10]
    long_vids = [c for c in completed if c.get("estimated_duration_min", 0) > 10]
    if len(short_vids) >= 1 and len(long_vids) >= 1:
        avg_short_ret = statistics.mean([c["performance"]["retention_pct"] for c in short_vids])
        avg_long_ret = statistics.mean([c["performance"]["retention_pct"] for c in long_vids])
        lessons.append({
            "rule": f"Les vidéos ≤10 min retiennent {avg_short_ret:.1f}% vs {avg_long_ret:.1f}% pour les > 10 min",
            "evidence": f"{len(short_vids)} courtes vs {len(long_vids)} longues",
            "sample_size": len(completed),
            "confidence": "low",
            "created_at": datetime.now().strftime("%Y-%m-%d"),
        })

    # Analyze open loops impact
    with_loops = [c for c in completed if c.get("open_loops_count", 0) >= 2]
    without_loops = [c for c in completed if c.get("open_loops_count", 0) < 2]
    if len(with_loops) >= 1 and len(without_loops) >= 1:
        avg_loops_ret = statistics.mean([c["performance"]["retention_pct"] for c in with_loops])
        avg_no_loops_ret = statistics.mean([c["performance"]["retention_pct"] for c in without_loops])
        if avg_loops_ret > avg_no_loops_ret * 1.1:
            lessons.append({
                "rule": f"Les scripts avec 2+ open loops retiennent {avg_loops_ret:.1f}% vs {avg_no_loops_ret:.1f}%",
                "evidence": f"{len(with_loops)} avec loops vs {len(without_loops)} sans",
                "sample_size": len(completed),
                "confidence": "low",
                "created_at": datetime.now().strftime("%Y-%m-%d"),
            })

    # Build structure performance
    struct_perf = {}
    for c in completed:
        stype = c.get("structure_type", "unknown")
        if stype not in struct_perf:
            struct_perf[stype] = {"count": 0, "retention_list": [], "watch_time_list": []}
        struct_perf[stype]["count"] += 1
        struct_perf[stype]["retention_list"].append(c["performance"]["retention_pct"])
        struct_perf[stype]["watch_time_list"].append(c["performance"]["watch_time_min"])

    struct_summary = {}
    for stype, data in struct_perf.items():
        struct_summary[stype] = {
            "count": data["count"],
            "avg_retention": round(statistics.mean(data["retention_list"]), 1),
            "avg_watch_time": round(statistics.mean(data["watch_time_list"]), 0),
        }

    lessons_data = {
        "last_updated": datetime.now().strftime("%Y-%m-%d"),
        "sample_size": len(completed),
        "lessons": lessons,
        "structure_performance": struct_summary,
    }
    write_json(str(memory_path / "lessons.json"), lessons_data)
    print(f"  [script] {len(lessons)} leçons extraites de {len(completed)} vidéos")


def extract_lessons_veille(memory_path):
    """Extract veille/trend-specific lessons."""
    choices = read_json(str(memory_path / "choices.json"), {"choices": []})
    completed = [c for c in choices.get("choices", []) if c.get("performance") and c.get("decision") == "make_video"]

    if len(completed) < 3:
        return

    lessons = []

    # Calculate hit rate
    hits = [c for c in completed if c["performance"].get("performance_index", 0) > 1.5]
    hit_rate = len(hits) / len(completed) if completed else 0

    # Analyze by topic category
    topic_perf = {}
    for c in completed:
        cat = c.get("topic_category", "unknown")
        pi = c["performance"].get("performance_index", 1.0)
        if cat not in topic_perf:
            topic_perf[cat] = {"count": 0, "pi_list": [], "hits": 0}
        topic_perf[cat]["count"] += 1
        topic_perf[cat]["pi_list"].append(pi)
        if pi > 1.5:
            topic_perf[cat]["hits"] += 1

    # Best and worst categories
    if len(topic_perf) >= 2:
        best_cat = max(topic_perf.items(), key=lambda x: statistics.mean(x[1]["pi_list"]))
        worst_cat = min(topic_perf.items(), key=lambda x: statistics.mean(x[1]["pi_list"]))
        lessons.append({
            "rule": f"Les sujets '{best_cat[0]}' performent le mieux (index {statistics.mean(best_cat[1]['pi_list']):.1f}x)",
            "evidence": f"Hit rate {best_cat[1]['hits']}/{best_cat[1]['count']} pour {best_cat[0]} vs {worst_cat[1]['hits']}/{worst_cat[1]['count']} pour {worst_cat[0]}",
            "sample_size": len(completed),
            "confidence": "medium" if len(completed) >= 5 else "low",
            "created_at": datetime.now().strftime("%Y-%m-%d"),
        })

    # Analyze speed (days_lag)
    fast = [c for c in completed if c.get("days_lag_detect_to_publish", 99) <= 3]
    slow = [c for c in completed if c.get("days_lag_detect_to_publish", 0) > 3]
    if len(fast) >= 1 and len(slow) >= 1:
        avg_fast_pi = statistics.mean([c["performance"].get("performance_index", 1) for c in fast])
        avg_slow_pi = statistics.mean([c["performance"].get("performance_index", 1) for c in slow])
        if avg_fast_pi > avg_slow_pi * 1.2:
            lessons.append({
                "rule": f"Publier dans les 3 jours donne un index de {avg_fast_pi:.1f}x vs {avg_slow_pi:.1f}x après 3 jours",
                "evidence": f"{len(fast)} vidéos rapides vs {len(slow)} lentes",
                "sample_size": len(completed),
                "confidence": "medium" if len(completed) >= 5 else "low",
                "created_at": datetime.now().strftime("%Y-%m-%d"),
            })

    # TOAST score correlation
    toast_scores = [c.get("toast_score", {}).get("total", 0) for c in completed]
    perf_indices = [c["performance"].get("performance_index", 1) for c in completed]
    if len(toast_scores) >= 5 and any(t > 0 for t in toast_scores):
        # Simple correlation check
        high_toast = [c for c in completed if c.get("toast_score", {}).get("total", 0) >= 18]
        low_toast = [c for c in completed if c.get("toast_score", {}).get("total", 0) < 18 and c.get("toast_score", {}).get("total", 0) > 0]
        if high_toast and low_toast:
            avg_high = statistics.mean([c["performance"].get("performance_index", 1) for c in high_toast])
            avg_low = statistics.mean([c["performance"].get("performance_index", 1) for c in low_toast])
            lessons.append({
                "rule": f"Les sujets TOAST >= 18 performent {avg_high:.1f}x vs {avg_low:.1f}x pour les < 18",
                "evidence": f"{len(high_toast)} sujets >= 18 vs {len(low_toast)} < 18",
                "sample_size": len(completed),
                "confidence": "medium" if len(completed) >= 8 else "low",
                "created_at": datetime.now().strftime("%Y-%m-%d"),
            })

    # Build topic performance summary
    topic_summary = {}
    for cat, data in topic_perf.items():
        topic_summary[cat] = {
            "count": data["count"],
            "avg_performance_index": round(statistics.mean(data["pi_list"]), 2),
            "hit_rate": round(data["hits"] / data["count"], 2) if data["count"] > 0 else 0,
        }

    avg_lag = statistics.mean([c.get("days_lag_detect_to_publish", 0) for c in completed if c.get("days_lag_detect_to_publish")])

    lessons_data = {
        "last_updated": datetime.now().strftime("%Y-%m-%d"),
        "sample_size": len(completed),
        "lessons": lessons,
        "topic_performance": topic_summary,
        "hit_rate": round(hit_rate, 2),
        "avg_days_lag": round(avg_lag, 1) if avg_lag else None,
    }
    write_json(str(memory_path / "lessons.json"), lessons_data)
    print(f"  [veille] {len(lessons)} leçons extraites de {len(completed)} vidéos (hit rate: {hit_rate:.0%})")


def main():
    if not TOKEN_PATH.exists():
        print("Erreur: token.json introuvable.")
        sys.exit(1)

    print("=== Feedback Analyzer ===\n")
    print("Connexion à YouTube Analytics...")
    creds = get_credentials()
    yt_analytics = build("youtubeAnalytics", "v2", credentials=creds)

    # Get channel averages
    print("Calcul des moyennes de la chaîne...")
    channel_avgs = get_channel_averages(yt_analytics)
    if channel_avgs:
        print(f"  Moyenne: {channel_avgs['avg_views']:.0f} vues, {channel_avgs['avg_retention']:.1f}% rétention")
        print(f"  Médiane: {channel_avgs['median_views']:.0f} vues")

    # Update performance data in each skill's choices
    print("\nMise à jour des performances par skill...")
    for skill_name, memory_path in SKILLS.items():
        if (memory_path / "choices.json").exists():
            updated = update_skill_choices(skill_name, memory_path, yt_analytics, channel_avgs)
            if updated == 0:
                print(f"  [{skill_name}] Aucune nouvelle donnée à mettre à jour")

    # Extract lessons
    print("\nExtraction des leçons...")
    if (SKILLS["titres_seo"] / "choices.json").exists():
        extract_lessons_titres(SKILLS["titres_seo"])
    if (SKILLS["miniature"] / "choices.json").exists():
        extract_lessons_miniature(SKILLS["miniature"])
    if (SKILLS["script"] / "choices.json").exists():
        extract_lessons_script(SKILLS["script"])
    if (SKILLS["veille"] / "choices.json").exists():
        extract_lessons_veille(SKILLS["veille"])

    print("\n=== Feedback Analyzer terminé ===")


if __name__ == "__main__":
    main()
