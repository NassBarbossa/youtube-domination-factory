#!/usr/bin/env python3
"""
YouTube Analytics — Analyze the 4 latest videos from NassRiviera channel.

Usage:
    python3 analyze.py

Generates an HTML report in outputs/ with:
- Per-video metrics: views, retention, watch time, engagement, subs, CTR
- Traffic sources breakdown
- Comparison between the 4 videos

Requires: OAuth token in token.json (run setup once to authorize)
"""

import json
import re
import sys
import webbrowser
import argparse
import statistics
from datetime import datetime, timedelta, timezone
from pathlib import Path

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCRIPT_DIR = Path(__file__).parent
TOKEN_PATH = SCRIPT_DIR / "token.json"
CLIENT_SECRET_PATH = SCRIPT_DIR / "client_secret.json"
OUTPUTS_DIR = SCRIPT_DIR / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True)


def get_credentials():
    """Load and refresh OAuth credentials."""
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

    # Le fichier n'a pas de date d'expiration : on rafraîchit toujours, et on explique quoi faire si le jeton est mort.
    try:
        creds.refresh(Request())
    except Exception as e:
        sys.exit(f"Jeton OAuth refusé ({e}).\nRelance l'autorisation : python3 yt-analytics/auth.py")
    token_data["token"] = creds.token
    with open(TOKEN_PATH, "w") as f:
        json.dump(token_data, f, indent=2)

    return creds


def parse_iso_duration(d):
    """PT9M29S → 569 s."""
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", d or "")
    if not m:
        return None
    h, mi, se = (int(x) if x else 0 for x in m.groups())
    return h * 3600 + mi * 60 + se


def get_latest_videos(yt_data, count=4):
    """Get the latest uploaded videos with titles, publish dates and durations."""
    channels = yt_data.channels().list(part="contentDetails", mine=True).execute()
    upload_playlist = channels["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    playlist_items = yt_data.playlistItems().list(
        part="snippet", playlistId=upload_playlist, maxResults=count
    ).execute()

    videos = []
    for item in playlist_items["items"]:
        snippet = item["snippet"]
        videos.append({
            "id": snippet["resourceId"]["videoId"],
            "title": snippet["title"],
            "published_at": snippet["publishedAt"],
            "thumbnail": snippet["thumbnails"].get("high", snippet["thumbnails"]["default"])["url"],
            "duration_sec": None,
        })
    if videos:
        details = yt_data.videos().list(part="contentDetails", id=",".join(v["id"] for v in videos)).execute()
        durations = {it["id"]: parse_iso_duration(it["contentDetails"].get("duration")) for it in details.get("items", [])}
        for v in videos:
            v["duration_sec"] = durations.get(v["id"])
    return videos


def get_video_analytics(yt_analytics, video_id, start_date, end_date):
    """Get analytics metrics for a single video."""
    resp = yt_analytics.reports().query(
        ids="channel==MINE",
        startDate=start_date,
        endDate=end_date,
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
    }


def get_video_traffic_sources(yt_analytics, video_id, start_date, end_date):
    """Get traffic source breakdown for a video or channel."""
    params = {
        "ids": "channel==MINE",
        "startDate": start_date,
        "endDate": end_date,
        "metrics": "views",
        "dimensions": "insightTrafficSourceType",
        "sort": "-views",
    }
    if video_id:
        params["filters"] = f"video=={video_id}"
    resp = yt_analytics.reports().query(**params).execute()

    sources = []
    total = sum(r[1] for r in resp.get("rows", []))
    for row in resp.get("rows", []):
        pct = (row[1] / total * 100) if total > 0 else 0
        sources.append({
            "source": format_traffic_source(row[0]),
            "views": int(row[1]),
            "percent": round(pct, 1),
        })
    return sources


def get_ctr_from_reporting(yt_reporting, video_ids):
    """Try to get CTR from Reporting API bulk reports."""
    ctr_data = {}
    try:
        jobs = yt_reporting.jobs().list().execute()
        reach_job = None
        for job in jobs.get("jobs", []):
            if "reach" in job.get("reportTypeId", "").lower():
                reach_job = job
                break

        if not reach_job:
            return ctr_data

        reports = yt_reporting.jobs().reports().list(jobId=reach_job["id"]).execute()
        if not reports.get("reports"):
            return ctr_data

        # Get the latest report
        latest = sorted(reports["reports"], key=lambda r: r.get("endTime", ""), reverse=True)[0]
        download_url = latest.get("downloadUrl")
        if not download_url:
            return ctr_data

        # Download and parse the CSV report
        import urllib.request
        from google.auth.transport.requests import AuthorizedSession
        creds = get_credentials()
        session = AuthorizedSession(creds)
        response = session.get(download_url)

        if response.status_code == 200:
            import csv
            import io
            reader = csv.DictReader(io.StringIO(response.text))
            for row in reader:
                vid = row.get("video_id", "")
                if vid in video_ids:
                    impressions = int(row.get("video_thumbnail_impressions", 0))
                    ctr = float(row.get("video_thumbnail_impressions_ctr", 0))
                    if vid not in ctr_data or impressions > ctr_data[vid].get("impressions", 0):
                        ctr_data[vid] = {
                            "impressions": impressions,
                            "ctr": round(ctr * 100, 2) if ctr < 1 else round(ctr, 2),
                        }
    except Exception as e:
        print(f"  Note: CTR Reporting API pas encore disponible ({e})")

    return ctr_data



def format_traffic_source(source):
    """Format traffic source names for display."""
    mapping = {
        "SUBSCRIBER": "Abonnés",
        "YT_SEARCH": "Recherche YouTube",
        "RELATED_VIDEO": "Vidéos suggérées",
        "EXT_URL": "Sites externes",
        "YT_CHANNEL": "Page chaîne",
        "NO_LINK_OTHER": "Autre",
        "YT_OTHER_PAGE": "Autre page YouTube",
        "NOTIFICATION": "Notifications",
        "PLAYLIST": "Playlists",
        "END_SCREEN": "Écran de fin",
        "ANNOTATION": "Annotations",
        "SHORTS": "Shorts",
    }
    return mapping.get(source, source)


def format_duration(seconds):
    """Format seconds to MM:SS or HH:MM:SS."""
    if seconds < 3600:
        return f"{seconds // 60}:{seconds % 60:02d}"
    return f"{seconds // 3600}:{(seconds % 3600) // 60:02d}:{seconds % 60:02d}"


from report_html import generate_html, age_days, MIN_AGE_DAYS  # noqa: E402

STUDIO_CTR = SCRIPT_DIR / "history" / "studio-ctr.json"  # écrit par studio_ctr.py (YouTube Studio, seule source du CTR)
PERIOD_LABEL = {"lifetime": "depuis la mise en ligne", "default": "28 derniers jours"}


def studio_ctr_for(video_id):
    """Dernière lecture Studio pour cette vidéo, ou None."""
    if not STUDIO_CTR.exists():
        return None
    entries = json.loads(STUDIO_CTR.read_text(encoding="utf-8")).get(video_id) or []
    if not entries:
        return None
    e = entries[-1]
    return {"impressions": e["impressions"], "ctr": e["ctr"], "source": "YouTube Studio", "period": e["period"], "fetched_at": e["fetched_at"]}



def main():
    ap = argparse.ArgumentParser(description="Rapport analytics des dernières vidéos (API YouTube Analytics).")
    ap.add_argument("--count", type=int, default=4, help="nombre de vidéos (défaut 4)")
    ap.add_argument("--notes", help="JSON d'analyse écrit par Claude : {overview, videos:{<id>:{worked[],failed[],verdict,verdict_label,verdict_kind}}, recommendations:[{title,based_on,action,impact}]}")
    ap.add_argument("--no-open", action="store_true", help="ne pas ouvrir le navigateur")
    ap.add_argument("--from-json", action="store_true", help="régénérer le rapport depuis le dernier outputs/analytics-<date>.json, sans appeler l'API")
    args = ap.parse_args()
    notes = json.loads(Path(args.notes).read_text(encoding="utf-8")) if args.notes else None

    if args.from_json:
        files = sorted(OUTPUTS_DIR.glob("analytics-????-??-??.json"))
        if not files:
            sys.exit("Aucun outputs/analytics-<date>.json à relire.")
        data = json.loads(files[-1].read_text(encoding="utf-8"))
        for v in data["videos"]:
            v["ctr_official"] = studio_ctr_for(v["id"]) or v.get("ctr_official")
        html = generate_html(data["videos"], data["channel_traffic"], notes)
        output_file = files[-1].with_suffix(".html")
        output_file.write_text(html, encoding="utf-8")
        print(f"Rapport régénéré depuis {files[-1].name} : {output_file}")
        if not args.no_open:
            webbrowser.open(output_file.resolve().as_uri())
        return

    if not TOKEN_PATH.exists():
        print("Erreur: token.json introuvable. Lance d'abord l'autorisation OAuth.")
        sys.exit(1)

    print("Connexion à YouTube Analytics...")
    creds = get_credentials()
    yt_data = build("youtube", "v3", credentials=creds)
    yt_analytics = build("youtubeAnalytics", "v2", credentials=creds)

    # Try Reporting API for CTR
    try:
        yt_reporting = build("youtubereporting", "v1", credentials=creds)
    except Exception:
        yt_reporting = None

    # Date range
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")

    # Get latest 4 videos
    print(f"Récupération des {args.count} dernières vidéos...")
    videos = get_latest_videos(yt_data, count=args.count)
    video_ids = [v["id"] for v in videos]

    # Get CTR from Reporting API
    ctr_data = {}
    if yt_reporting:
        print("Tentative de récupération du CTR (Reporting API)...")
        ctr_data = get_ctr_from_reporting(yt_reporting, set(video_ids))

    # Get analytics per video
    videos_data = []
    for v in videos:
        print(f"  Analyse: {v['title'][:50]}...")
        metrics = get_video_analytics(yt_analytics, v["id"], start_date, end_date)
        traffic = get_video_traffic_sources(yt_analytics, v["id"], start_date, end_date)

        entry = {
            "id": v["id"],
            "title": v["title"],
            "published_at": v["published_at"],
            "thumbnail": v["thumbnail"],
            "duration_sec": v.get("duration_sec"),
            "metrics": metrics,
            "traffic_sources": traffic,
            "ctr_official": studio_ctr_for(v["id"]) or ctr_data.get(v["id"]),
        }

        videos_data.append(entry)

    # Channel-level traffic sources
    print("Récupération des sources de trafic globales...")
    channel_start = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    channel_traffic = get_video_traffic_sources(yt_analytics, None, channel_start, end_date)

    # Generate HTML
    print("Génération du rapport HTML...")
    html = generate_html(videos_data, channel_traffic, notes)
    stamp = datetime.now().strftime('%Y-%m-%d')
    output_file = OUTPUTS_DIR / f"analytics-{stamp}.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    data_file = OUTPUTS_DIR / f"analytics-{stamp}.json"
    data_file.write_text(json.dumps({"generated_at": datetime.now().isoformat(), "videos": videos_data, "channel_traffic": channel_traffic}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"\nRapport généré: {output_file}")
    print(f"Données brutes: {data_file}")
    if not args.no_open:
        print("Ouverture dans le navigateur...")
        webbrowser.open(output_file.resolve().as_uri())


if __name__ == "__main__":
    main()
