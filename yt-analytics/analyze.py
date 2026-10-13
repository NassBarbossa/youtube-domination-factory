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


MIN_AGE_DAYS = 4  # retard de l'API YouTube Analytics : avant ça, une vidéo remonte 0 ou 1 vue
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


def age_days(published_at):
    return (datetime.now(timezone.utc) - datetime.fromisoformat(published_at.replace("Z", "+00:00"))).days


def bars_html(sources, limit, with_views=False):
    out = ""
    for src in sources[:limit]:
        label = f"{src['views']} · {src['percent']}%" if with_views else f"{src['percent']}%"
        out += f"""
        <div class="traffic-row">
          <span class="traffic-name">{src['source']}</span>
          <div class="traffic-bar-container"><div class="traffic-bar" style="width: {src['percent']}%"></div></div>
          <span class="traffic-pct">{label}</span>
        </div>"""
    return out


def generate_html(videos_data, channel_traffic, notes=None):
    """Rapport HTML à la charte du cadre. `notes` (optionnel) = analyse écrite par Claude, voir --notes."""
    notes = notes or {}
    now = datetime.now().strftime("%d/%m/%Y à %H:%M")
    reliable = [v for v in videos_data if v["metrics"] and age_days(v["published_at"]) >= MIN_AGE_DAYS]
    fresh = [v for v in videos_data if v["metrics"] and age_days(v["published_at"]) < MIN_AGE_DAYS]

    views_list = [v["metrics"]["views"] for v in reliable]
    median_views = statistics.median(views_list) if views_list else 0
    total_views = sum(views_list)
    total_subs = sum(v["metrics"]["subscribers_gained"] for v in reliable)
    avg_ret = round(statistics.mean(v["metrics"]["retention_pct"] for v in reliable), 1) if reliable else 0
    max_views = max(views_list) if views_list else 0
    max_ret = max((v["metrics"]["retention_pct"] for v in reliable), default=0)
    max_subs = max((v["metrics"]["subscribers_gained"] for v in reliable), default=0)
    max_ctr = max((v["ctr_official"]["ctr"] for v in reliable if v.get("ctr_official")), default=None)

    def verdict_badge(v):
        n = notes.get("videos", {}).get(v["id"], {})
        if n.get("verdict_label"):
            cls = {"réussite": "good", "moyenne": "mid", "échec": "bad"}.get(n.get("verdict_kind", ""), "mid")
            return f'<span class="badge {cls}">{n["verdict_label"]}</span>'
        return ""

    video_cards = ""
    for v in videos_data:
        m = v["metrics"]
        if not m:
            continue
        n = notes.get("videos", {}).get(v["id"], {})
        is_fresh = age_days(v["published_at"]) < MIN_AGE_DAYS
        idx = round(m["views"] / median_views, 2) if (median_views and not is_fresh) else None
        conv = round(m["subscribers_gained"] / m["views"] * 100, 1) if m["views"] else 0
        like_rate = round(m["likes"] / m["views"] * 100, 1) if m["views"] else 0
        c = v.get("ctr_official")
        ctr_html = (f"""<div class="metric{' best' if c['ctr'] == max_ctr else ''}"><div class="metric-label">CTR</div><div class="metric-value">{c['ctr']}%</div><div class="metric-sub">{c['impressions']:,} impressions · {PERIOD_LABEL.get(c.get('period'), '')}</div></div>"""
                    if c else
                    """<div class="metric"><div class="metric-label">CTR</div><div class="metric-value muted">n/d</div><div class="metric-sub">lance studio_ctr.py</div></div>""")
        if is_fresh:
            body = f"""
      <div class="fresh">Publiée il y a {age_days(v['published_at'])} jour(s) : l'API a 2 à 3 jours de retard, ces chiffres ne veulent encore rien dire. Hors moyennes.</div>"""
        else:
            analysis = ""
            if n:
                worked = "".join(f"<li>{x}</li>" for x in n.get("worked", []))
                failed = "".join(f"<li>{x}</li>" for x in n.get("failed", []))
                analysis = f"""
      <div class="two-col">
        <div class="col good-col"><h3>Ce qui a marché</h3><ul>{worked or '<li>Rien de net.</li>'}</ul></div>
        <div class="col bad-col"><h3>Ce qui n'a pas marché</h3><ul>{failed or '<li>Rien de net.</li>'}</ul></div>
      </div>
      {f'<div class="verdict"><strong>Verdict.</strong> {n["verdict"]}</div>' if n.get("verdict") else ''}"""
            body = f"""
      <div class="metrics-grid">
        <div class="metric{' best' if m['views'] == max_views else ''}"><div class="metric-label">Vues</div><div class="metric-value">{m['views']:,}</div><div class="metric-sub">{f'{idx}× la médiane' if idx else ''}</div></div>
        {ctr_html}
        <div class="metric{' best' if m['retention_pct'] == max_ret else ''}"><div class="metric-label">Rétention</div><div class="metric-value">{m['retention_pct']}%</div><div class="metric-sub">{format_duration(m['avg_view_duration_sec'])} par vue</div></div>
        <div class="metric{' best' if m['subscribers_gained'] == max_subs else ''}"><div class="metric-label">Abonnés</div><div class="metric-value">+{m['subscribers_gained']}</div><div class="metric-sub">{conv}% des vues</div></div>
        <div class="metric"><div class="metric-label">Likes</div><div class="metric-value">{m['likes']}</div><div class="metric-sub">{like_rate}% des vues</div></div>
        <div class="metric"><div class="metric-label">Commentaires</div><div class="metric-value">{m['comments']}</div><div class="metric-sub">{m['shares']} partage(s)</div></div>
        <div class="metric"><div class="metric-label">Temps regardé</div><div class="metric-value">{m['watch_time_min']:,.0f} min</div><div class="metric-sub">cumulé</div></div>
      </div>
      <div class="traffic-section"><h3>D'où viennent les vues</h3>{bars_html(v.get('traffic_sources', []), 5)}</div>
      {analysis}"""
        video_cards += f"""
    <section class="card video-card">
      <div class="video-header">
        <img src="{v['thumbnail']}" alt="" class="video-thumb">
        <div class="video-info">
          <h2>{v['title']}</h2>
          <div class="video-meta">Publiée le {v['published_at'][:10]} · <a href="https://www.youtube.com/watch?v={v['id']}">youtube.com/watch?v={v['id']}</a></div>
        </div>
        {verdict_badge(v)}
      </div>
      {body}
    </section>
"""

    recos_html = ""
    for i, r in enumerate(notes.get("recommendations", []), 1):
        recos_html += f"""
      <div class="reco">
        <div class="reco-num">{i}</div>
        <div>
          <h3>{r['title']}</h3>
          <p><strong>Basée sur :</strong> {r['based_on']}</p>
          <p><strong>Action :</strong> {r['action']}</p>
          <p><strong>Impact attendu :</strong> {r['impact']}</p>
        </div>
      </div>"""
    recos_section = f"""
    <section class="card">
      <h2 class="section-title">Recommandations</h2>
      {recos_html}
    </section>""" if recos_html else ""

    overview_note = notes.get("overview", "")
    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Nassin Crypto · analytics du {datetime.now().strftime('%d/%m/%Y')}</title>
<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Public+Sans:wght@400;600;700&display=swap" rel="stylesheet">
<style>
  :root {{ --bg:#0B0B0B; --sand:#DBB17F; --sand-light:#F3D6A8; --sand-dark:#9C7748; --cream:#F4EFE7; --punk:#648596; --punk-dark:#4F6C7B; --grey-dark:#3B3A37; --grey:#9A968D; --good:#2E8B57; --bad:#C0392B; }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ background:var(--bg); color:var(--cream); font-family:'Public Sans', Helvetica, Arial, sans-serif; padding:40px 20px; line-height:1.45; }}
  .container {{ max-width:1400px; margin:0 auto; }}
  h1, h2, h3, .metric-value, .reco-num {{ font-family:'Archivo Black', Impact, 'Arial Black', sans-serif; font-weight:400; }}
  .page-header {{ display:flex; justify-content:space-between; align-items:flex-end; gap:24px; margin-bottom:32px; padding-bottom:20px; border-bottom:3px solid var(--sand); flex-wrap:wrap; }}
  .page-header h1 {{ font-size:34px; color:var(--sand); line-height:1.1; }}
  .page-header h1 small {{ display:block; font-family:'Public Sans', sans-serif; font-weight:600; font-size:14px; color:var(--grey); letter-spacing:1px; text-transform:uppercase; margin-bottom:6px; }}
  .page-header .date {{ font-size:13px; color:var(--grey); text-align:right; }}
  .card {{ background:var(--cream); color:var(--bg); border:3px solid var(--bg); box-shadow:8px 8px 0 var(--sand-dark); padding:28px; margin-bottom:28px; }}
  .section-title {{ font-size:22px; margin-bottom:18px; }}
  .overview {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(170px, 1fr)); gap:14px; margin-bottom:18px; }}
  .stat {{ background:var(--bg); color:var(--cream); padding:16px; }}
  .stat .metric-label {{ color:var(--grey); }}
  .stat .metric-value {{ color:var(--sand); }}
  .overview-note {{ font-size:15px; margin-top:6px; }}
  .video-header {{ display:flex; gap:20px; align-items:center; margin-bottom:22px; }}
  .video-thumb {{ width:200px; height:112px; object-fit:cover; border:3px solid var(--bg); flex-shrink:0; }}
  .video-info {{ flex:1; }}
  .video-info h2 {{ font-size:20px; line-height:1.25; margin-bottom:6px; }}
  .video-meta {{ font-size:13px; color:var(--grey-dark); }}
  .video-meta a {{ color:var(--punk-dark); }}
  .badge {{ font-weight:700; font-size:12px; letter-spacing:1px; text-transform:uppercase; padding:8px 12px; border:3px solid var(--bg); white-space:nowrap; }}
  .badge.good {{ background:var(--good); color:#fff; }} .badge.mid {{ background:var(--sand-dark); color:#fff; }} .badge.bad {{ background:var(--bad); color:#fff; }}
  .metrics-grid {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(150px, 1fr)); gap:12px; margin-bottom:22px; }}
  .metric {{ background:#fff; border:2px solid var(--bg); padding:14px; text-align:center; }}
  .metric.best {{ background:var(--sand-light); }}
  .metric-label {{ font-size:11px; color:var(--grey-dark); text-transform:uppercase; letter-spacing:1px; margin-bottom:6px; font-weight:700; }}
  .metric-value {{ font-size:26px; }}
  .metric-value.muted {{ color:var(--grey); }}
  .metric-sub {{ font-size:11px; color:var(--grey-dark); margin-top:4px; }}
  .traffic-section h3 {{ font-size:13px; letter-spacing:1px; text-transform:uppercase; margin-bottom:10px; }}
  .traffic-row {{ display:flex; align-items:center; gap:12px; margin-bottom:7px; }}
  .traffic-name {{ font-size:13px; width:170px; flex-shrink:0; font-weight:600; }}
  .traffic-bar-container {{ flex:1; height:12px; background:#fff; border:2px solid var(--bg); overflow:hidden; }}
  .traffic-bar {{ height:100%; background:var(--punk); min-width:2px; }}
  .traffic-pct {{ font-size:13px; width:110px; text-align:right; flex-shrink:0; }}
  .two-col {{ display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-top:22px; }}
  .col {{ background:#fff; border:2px solid var(--bg); padding:16px 18px; }}
  .col h3 {{ font-size:14px; margin-bottom:10px; }}
  .good-col h3 {{ color:var(--good); }} .bad-col h3 {{ color:var(--bad); }}
  .col ul {{ padding-left:18px; font-size:14px; }} .col li {{ margin-bottom:6px; }}
  .verdict {{ margin-top:16px; padding:14px 18px; background:var(--bg); color:var(--cream); font-size:15px; border-left:6px solid var(--sand); }}
  .fresh {{ padding:14px 18px; background:var(--sand-light); border:2px dashed var(--sand-dark); font-size:14px; }}
  .reco {{ display:flex; gap:18px; padding:18px 0; border-top:2px solid var(--bg); }}
  .reco:first-of-type {{ border-top:none; padding-top:0; }}
  .reco-num {{ font-size:30px; color:var(--punk-dark); width:44px; flex-shrink:0; line-height:1; }}
  .reco h3 {{ font-size:17px; margin-bottom:8px; }} .reco p {{ font-size:14px; margin-bottom:4px; }}
  .footer {{ text-align:center; padding-top:24px; font-size:12px; color:var(--grey); }}
  @media (max-width:800px) {{ .two-col {{ grid-template-columns:1fr; }} .video-header {{ flex-wrap:wrap; }} }}
</style>
</head>
<body>
<div class="container">
  <div class="page-header">
    <h1><small>Nassin Crypto · nouvelle chaîne</small>Analytics des {len(videos_data)} dernières vidéos</h1>
    <div class="date">Données API YouTube Analytics (2 à 3 jours de retard)<br>Rapport généré le {now}</div>
  </div>

  <section class="card">
    <h2 class="section-title">La chaîne en un coup d'œil</h2>
    <div class="overview">
      <div class="stat"><div class="metric-label">Vidéos fiables</div><div class="metric-value">{len(reliable)}</div><div class="metric-sub">{len(fresh)} trop récente(s)</div></div>
      <div class="stat"><div class="metric-label">Vues cumulées</div><div class="metric-value">{total_views:,}</div><div class="metric-sub">médiane {median_views:.0f} par vidéo</div></div>
      <div class="stat"><div class="metric-label">Rétention moyenne</div><div class="metric-value">{avg_ret}%</div><div class="metric-sub">de la vidéo regardée</div></div>
      <div class="stat"><div class="metric-label">Abonnés gagnés</div><div class="metric-value">+{total_subs}</div><div class="metric-sub">par ces vidéos</div></div>
    </div>
    <div class="traffic-section"><h3>D'où viennent les vues de la chaîne (30 derniers jours)</h3>{bars_html(channel_traffic, 8, with_views=True)}</div>
    {f'<p class="overview-note">{overview_note}</p>' if overview_note else ''}
  </section>

  {video_cards}
  {recos_section}

  <div class="footer">yt-analytics · youtube-domination-factory · CTR absent de l'API : il vient de l'export CSV de YouTube Studio (parse_youtube_csv.py)</div>
</div>
</body>
</html>"""
    return html


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
