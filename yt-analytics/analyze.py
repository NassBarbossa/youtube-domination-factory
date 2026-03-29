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
import os
import sys
from datetime import datetime, timedelta
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

    if creds.expired:
        creds.refresh(Request())
        token_data["token"] = creds.token
        with open(TOKEN_PATH, "w") as f:
            json.dump(token_data, f, indent=2)

    return creds


def get_latest_videos(yt_data, count=4):
    """Get the latest uploaded videos with titles and publish dates."""
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
        })
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


def estimate_ctr(views, likes, comments, shares, retention_pct):
    """Estimate CTR preview based on engagement signals."""
    if views == 0:
        return None

    engagement_rate = (likes + comments * 3 + shares * 5) / views
    retention_factor = retention_pct / 30.0  # 30% = baseline

    # Estimated CTR between 2% and 12% based on engagement + retention
    base_ctr = 4.0  # Average YouTube CTR
    estimated = base_ctr * (0.5 + engagement_rate * 10) * retention_factor
    estimated = max(1.0, min(15.0, estimated))  # Clamp between 1-15%

    return round(estimated, 1)


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


def generate_html(videos_data, channel_traffic):
    """Generate the HTML analytics report."""
    now = datetime.now().strftime("%d/%m/%Y à %H:%M")

    # Find best/worst for highlighting
    if videos_data:
        max_views = max(v["metrics"]["views"] for v in videos_data if v["metrics"])
        max_retention = max(v["metrics"]["retention_pct"] for v in videos_data if v["metrics"])
        max_subs = max(v["metrics"]["subscribers_gained"] for v in videos_data if v["metrics"])

    video_cards = ""
    for v in videos_data:
        m = v["metrics"]
        if not m:
            continue

        # CTR display
        ctr_html = ""
        if v.get("ctr_official"):
            ctr_html = f"""
            <div class="metric">
              <div class="metric-label">CTR</div>
              <div class="metric-value">{v['ctr_official']['ctr']}%</div>
              <div class="metric-sub">{v['ctr_official']['impressions']:,} impressions</div>
            </div>"""
        elif v.get("ctr_preview"):
            ctr_html = f"""
            <div class="metric">
              <div class="metric-label">CTR <span class="preview-badge">estimé</span></div>
              <div class="metric-value preview">{v['ctr_preview']}%</div>
              <div class="metric-sub">basé sur l'engagement</div>
            </div>"""

        # Highlight best values
        views_class = " best" if m["views"] == max_views else ""
        retention_class = " best" if m["retention_pct"] == max_retention else ""
        subs_class = " best" if m["subscribers_gained"] == max_subs else ""

        # Traffic sources for this video
        traffic_bars = ""
        for src in v.get("traffic_sources", [])[:5]:
            traffic_bars += f"""
            <div class="traffic-row">
              <span class="traffic-name">{src['source']}</span>
              <div class="traffic-bar-container">
                <div class="traffic-bar" style="width: {src['percent']}%"></div>
              </div>
              <span class="traffic-pct">{src['percent']}%</span>
            </div>"""

        published = v["published_at"][:10]

        video_cards += f"""
    <div class="video-card">
      <div class="video-header">
        <img src="{v['thumbnail']}" alt="" class="video-thumb">
        <div class="video-info">
          <h2>{v['title']}</h2>
          <span class="video-date">Publiée le {published}</span>
        </div>
      </div>

      <div class="metrics-grid">
        <div class="metric{views_class}">
          <div class="metric-label">Vues</div>
          <div class="metric-value">{m['views']:,}</div>
        </div>
        {ctr_html}
        <div class="metric{retention_class}">
          <div class="metric-label">Rétention</div>
          <div class="metric-value">{m['retention_pct']}%</div>
        </div>
        <div class="metric">
          <div class="metric-label">Watch Time</div>
          <div class="metric-value">{m['watch_time_min']:,.0f} min</div>
        </div>
        <div class="metric">
          <div class="metric-label">Durée moy.</div>
          <div class="metric-value">{format_duration(m['avg_view_duration_sec'])}</div>
        </div>
        <div class="metric{subs_class}">
          <div class="metric-label">Abonnés</div>
          <div class="metric-value">+{m['subscribers_gained']}</div>
        </div>
        <div class="metric">
          <div class="metric-label">Engagement</div>
          <div class="metric-value">{m['likes']}👍 {m['comments']}💬 {m['shares']}🔗</div>
        </div>
      </div>

      <div class="traffic-section">
        <h3>Sources de trafic</h3>
        {traffic_bars}
      </div>
    </div>
"""

    # Channel-level traffic
    channel_traffic_html = ""
    for src in channel_traffic[:8]:
        channel_traffic_html += f"""
        <div class="traffic-row">
          <span class="traffic-name">{src['source']}</span>
          <div class="traffic-bar-container">
            <div class="traffic-bar channel" style="width: {src['percent']}%"></div>
          </div>
          <span class="traffic-pct">{src['views']} ({src['percent']}%)</span>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Analytics — NassRiviera — 4 dernières vidéos</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  body {{
    background: #0a0a0a;
    font-family: 'Inter', sans-serif;
    color: #e0e0e0;
    padding: 40px 20px;
    min-height: 100vh;
  }}

  .container {{
    max-width: 1200px;
    margin: 0 auto;
  }}

  .page-header {{
    text-align: center;
    margin-bottom: 48px;
    padding-bottom: 32px;
    border-bottom: 1px solid #1e1e1e;
  }}

  .page-header h1 {{
    font-size: 32px;
    font-weight: 800;
    margin-bottom: 8px;
  }}

  .page-header h1 span {{ color: #00E5FF; }}

  .page-header .date {{
    font-size: 14px;
    color: #666;
  }}

  .video-card {{
    background: #111;
    border: 1px solid #1e1e1e;
    border-radius: 16px;
    padding: 28px;
    margin-bottom: 24px;
  }}

  .video-header {{
    display: flex;
    gap: 20px;
    margin-bottom: 24px;
    align-items: center;
  }}

  .video-thumb {{
    width: 180px;
    height: 100px;
    object-fit: cover;
    border-radius: 8px;
  }}

  .video-info h2 {{
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 4px;
    line-height: 1.3;
  }}

  .video-date {{
    font-size: 13px;
    color: #666;
  }}

  .metrics-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 16px;
    margin-bottom: 24px;
  }}

  .metric {{
    background: #1a1a1a;
    border-radius: 12px;
    padding: 16px;
    text-align: center;
  }}

  .metric.best {{
    border: 1px solid #00E5FF33;
    background: #00E5FF08;
  }}

  .metric-label {{
    font-size: 11px;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 6px;
  }}

  .metric-value {{
    font-size: 24px;
    font-weight: 700;
  }}

  .metric-value.preview {{
    color: #f5a623;
  }}

  .metric-sub {{
    font-size: 11px;
    color: #666;
    margin-top: 4px;
  }}

  .preview-badge {{
    background: #f5a62333;
    color: #f5a623;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 9px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}

  .traffic-section {{
    border-top: 1px solid #1e1e1e;
    padding-top: 16px;
  }}

  .traffic-section h3 {{
    font-size: 13px;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 12px;
  }}

  .traffic-row {{
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 8px;
  }}

  .traffic-name {{
    font-size: 13px;
    width: 140px;
    flex-shrink: 0;
  }}

  .traffic-bar-container {{
    flex: 1;
    height: 8px;
    background: #1e1e1e;
    border-radius: 4px;
    overflow: hidden;
  }}

  .traffic-bar {{
    height: 100%;
    background: #00E5FF;
    border-radius: 4px;
    min-width: 2px;
  }}

  .traffic-bar.channel {{
    background: #4a90d9;
  }}

  .traffic-pct {{
    font-size: 13px;
    color: #888;
    width: 80px;
    text-align: right;
    flex-shrink: 0;
  }}

  .channel-section {{
    background: #111;
    border: 1px solid #1e1e1e;
    border-radius: 16px;
    padding: 28px;
    margin-top: 32px;
  }}

  .channel-section h2 {{
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 20px;
  }}

  .footer {{
    text-align: center;
    padding-top: 32px;
    margin-top: 32px;
    border-top: 1px solid #1e1e1e;
    font-size: 12px;
    color: #444;
  }}
</style>
</head>
<body>
<div class="container">

  <div class="page-header">
    <h1>Analytics <span>— NassRiviera</span></h1>
    <div class="date">4 dernières vidéos · Rapport généré le {now}</div>
  </div>

  {video_cards}

  <div class="channel-section">
    <h2>Sources de trafic — Chaîne (30 derniers jours)</h2>
    {channel_traffic_html}
  </div>

  <div class="footer">
    Rapport généré par yt-analytics · youtube-domination-factory
  </div>

</div>
</body>
</html>"""

    return html


def main():
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
    print("Récupération des 4 dernières vidéos...")
    videos = get_latest_videos(yt_data, count=4)
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
            "metrics": metrics,
            "traffic_sources": traffic,
            "ctr_official": ctr_data.get(v["id"]),
            "ctr_preview": None,
        }

        # Estimate CTR if no official data
        if metrics and not entry["ctr_official"]:
            entry["ctr_preview"] = estimate_ctr(
                metrics["views"], metrics["likes"], metrics["comments"],
                metrics["shares"], metrics["retention_pct"],
            )

        videos_data.append(entry)

    # Channel-level traffic sources
    print("Récupération des sources de trafic globales...")
    channel_start = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    channel_traffic = get_video_traffic_sources(yt_analytics, None, channel_start, end_date)

    # Generate HTML
    print("Génération du rapport HTML...")
    html = generate_html(videos_data, channel_traffic)
    output_file = OUTPUTS_DIR / f"analytics-{datetime.now().strftime('%Y-%m-%d')}.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\nRapport généré: {output_file}")
    print("Ouverture dans le navigateur...")
    os.system(f'open "{output_file}"')


if __name__ == "__main__":
    main()
