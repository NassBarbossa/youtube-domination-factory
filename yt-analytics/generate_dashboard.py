#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate aggregated analytics dashboard comparing all videos.

Usage:
    python generate_dashboard.py

This script:
1. Reads all historical video data from yt-analytics/history/
2. Calculates global statistics (avg CTR, avg retention, etc.)
3. Compares videos against each other
4. Identifies top performers and bottom performers
5. Generates dashboard HTML with comparisons and trends
"""

import json
import sys
import io
from pathlib import Path
from datetime import datetime
from statistics import mean

if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PROJECT_ROOT = Path(__file__).parent
HISTORY_DIR = PROJECT_ROOT / "history"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

def load_all_videos():
    """Load historical data for all videos."""
    videos = {}

    if not HISTORY_DIR.exists():
        print("Aucun historique trouvé")
        return videos

    for history_file in HISTORY_DIR.glob("*.json"):
        with open(history_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            videos[data["video_slug"]] = data

    return videos

def get_latest_metrics(video_data):
    """Get the most recent analysis for a video."""
    if not video_data["analyses"]:
        return None
    return video_data["analyses"][-1]

def get_previous_metrics(video_data):
    """Get the second-to-last analysis for a video."""
    if len(video_data["analyses"]) < 2:
        return None
    return video_data["analyses"][-2]

def calculate_global_stats(videos):
    """Calculate global statistics across all videos."""

    latest_metrics = {}
    for slug, video_data in videos.items():
        latest = get_latest_metrics(video_data)
        if latest:
            latest_metrics[slug] = latest

    if not latest_metrics:
        return None

    stats = {
        "total_videos": len(latest_metrics),
        "total_views": sum(m["views"] for m in latest_metrics.values()),
        "avg_ctr": round(mean([m["ctr"] for m in latest_metrics.values()]), 2),
        "avg_retention": round(mean([m["retention"] for m in latest_metrics.values()]), 2),
        "total_impressions": sum(m["impressions"] for m in latest_metrics.values()),
        "total_subscribers": sum(m["new_subscribers"] for m in latest_metrics.values()),
        "total_shares": sum(m["shares"] for m in latest_metrics.values()),
        "avg_watch_time": round(mean([m["watch_time_hours"] for m in latest_metrics.values()]), 2),
    }

    return stats, latest_metrics

def rank_videos(latest_metrics, metric_name):
    """Rank videos by a specific metric."""
    sorted_videos = sorted(
        latest_metrics.items(),
        key=lambda x: x[1][metric_name],
        reverse=True
    )
    return sorted_videos

def generate_dashboard_html(videos, global_stats, latest_metrics):
    """Generate aggregated dashboard HTML."""

    if not global_stats:
        return "<h1>Pas de données disponibles</h1>"

    stats, _ = global_stats

    # Get top performers
    top_ctr = rank_videos(latest_metrics, "ctr")[:3]
    top_retention = rank_videos(latest_metrics, "retention")[:3]
    top_views = rank_videos(latest_metrics, "views")[:3]

    # Get bottom performers
    bottom_ctr = rank_videos(latest_metrics, "ctr")[-3:][::-1]
    bottom_retention = rank_videos(latest_metrics, "retention")[-3:][::-1]

    # Build comparison table
    comparison_rows = ""
    for slug, metrics in sorted(latest_metrics.items()):
        video_data = videos[slug]
        previous = get_previous_metrics(video_data)

        if previous:
            ctr_delta = metrics["ctr"] - previous["ctr"]
            retention_delta = metrics["retention"] - previous["retention"]
            views_delta = metrics["views"] - previous["views"]
        else:
            ctr_delta = retention_delta = views_delta = 0

        comparison_rows += f"""
    <tr>
      <td class="video-name">{slug}</td>
      <td>{metrics['views']}</td>
      <td><span class="metric-badge">Dernier: {metrics['ctr']}%</span> {f'<span class="delta-up">+{ctr_delta:.2f}%</span>' if ctr_delta > 0 else f'<span class="delta-down">{ctr_delta:.2f}%</span>' if ctr_delta < 0 else ''}</td>
      <td><span class="metric-badge">{metrics['retention']}%</span> {f'<span class="delta-up">+{retention_delta:.2f}%</span>' if retention_delta > 0 else f'<span class="delta-down">{retention_delta:.2f}%</span>' if retention_delta < 0 else ''}</td>
      <td>{metrics['impressions']}</td>
      <td>+{metrics['new_subscribers']}</td>
      <td>{metrics['shares']}</td>
    </tr>
"""

    # Build top performers
    top_ctr_html = "\n".join([
        f'<div class="rank-card rank-{i+1}"><div class="rank-number">{i+1}</div><div class="rank-name">{slug}</div><div class="rank-value">{metrics["ctr"]}% CTR</div></div>'
        for i, (slug, metrics) in enumerate(top_ctr)
    ])

    top_retention_html = "\n".join([
        f'<div class="rank-card rank-{i+1}"><div class="rank-number">{i+1}</div><div class="rank-name">{slug}</div><div class="rank-value">{metrics["retention"]}% Retention</div></div>'
        for i, (slug, metrics) in enumerate(top_retention)
    ])

    top_views_html = "\n".join([
        f'<div class="rank-card rank-{i+1}"><div class="rank-number">{i+1}</div><div class="rank-name">{slug}</div><div class="rank-value">{metrics["views"]} Views</div></div>'
        for i, (slug, metrics) in enumerate(top_views)
    ])

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>YouTube Analytics Dashboard</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  body {{
    background: #0f0f0f;
    font-family: 'Inter', sans-serif;
    color: #e8e8e8;
    padding: 40px;
    min-height: 100vh;
  }}

  .container {{
    max-width: 1600px;
    margin: 0 auto;
  }}

  .header {{
    margin-bottom: 40px;
    padding-bottom: 30px;
    border-bottom: 1px solid #2a2a2a;
  }}

  .header h1 {{
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 8px;
  }}

  .header h1 span {{ color: #4a90d9; }}

  .header .meta {{
    font-size: 14px;
    color: #888;
  }}

  /* Stats Grid */
  .stats-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin-bottom: 40px;
  }}

  .stat-card {{
    background: #1a1a1a;
    border-radius: 16px;
    padding: 24px;
    border: 1px solid #2a2a2a;
  }}

  .stat-card .label {{
    font-size: 13px;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 8px;
  }}

  .stat-card .value {{
    font-size: 36px;
    font-weight: 800;
  }}

  .stat-card .subtitle {{
    font-size: 12px;
    color: #555;
    margin-top: 8px;
  }}

  /* Ranking Section */
  .ranking-section {{
    margin-bottom: 40px;
  }}

  .ranking-section h2 {{
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 20px;
  }}

  .ranking-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
  }}

  .rank-container {{
    background: #1a1a1a;
    border-radius: 16px;
    padding: 28px;
    border: 1px solid #2a2a2a;
  }}

  .rank-container h3 {{
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 20px;
    text-align: center;
  }}

  .rank-cards {{
    display: flex;
    flex-direction: column;
    gap: 12px;
  }}

  .rank-card {{
    background: #252525;
    padding: 16px;
    border-radius: 12px;
    border-left: 4px solid;
    display: flex;
    align-items: center;
    gap: 12px;
  }}

  .rank-card.rank-1 {{ border-color: #ffd700; }}
  .rank-card.rank-2 {{ border-color: #c0c0c0; }}
  .rank-card.rank-3 {{ border-color: #cd7f32; }}

  .rank-number {{
    font-size: 24px;
    font-weight: 800;
    width: 40px;
    text-align: center;
  }}

  .rank-card.rank-1 .rank-number {{ color: #ffd700; }}
  .rank-card.rank-2 .rank-number {{ color: #c0c0c0; }}
  .rank-card.rank-3 .rank-number {{ color: #cd7f32; }}

  .rank-name {{
    flex: 1;
    font-weight: 600;
  }}

  .rank-value {{
    font-size: 12px;
    color: #888;
  }}

  /* Comparison Table */
  .comparison-section {{
    margin-bottom: 40px;
  }}

  .comparison-section h2 {{
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 20px;
  }}

  .comparison-table {{
    background: #1a1a1a;
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid #2a2a2a;
  }}

  .comparison-table table {{
    width: 100%;
    border-collapse: collapse;
  }}

  .comparison-table th {{
    background: #252525;
    padding: 16px;
    text-align: left;
    font-size: 13px;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 1px;
    border-bottom: 1px solid #2a2a2a;
    font-weight: 600;
  }}

  .comparison-table td {{
    padding: 16px;
    border-bottom: 1px solid #2a2a2a;
    font-size: 14px;
  }}

  .comparison-table tr:last-child td {{
    border-bottom: none;
  }}

  .video-name {{
    font-weight: 600;
  }}

  .metric-badge {{
    display: inline-block;
    padding: 4px 8px;
    background: #4a90d91a;
    border-radius: 6px;
    color: #4a90d9;
    font-size: 12px;
    margin-right: 8px;
  }}

  .delta-up {{
    color: #2eaa5e;
    font-weight: 600;
  }}

  .delta-down {{
    color: #ff4444;
    font-weight: 600;
  }}

  .footer {{
    text-align: center;
    padding-top: 30px;
    border-top: 1px solid #2a2a2a;
    font-size: 13px;
    color: #555;
  }}
</style>
</head>
<body>
<div class="container">

  <!-- Header -->
  <div class="header">
    <h1>YouTube <span>Analytics Dashboard</span></h1>
    <div class="meta">Généré le {datetime.now().strftime('%d %B %Y')} | {stats['total_videos']} vidéos analysées</div>
  </div>

  <!-- Global Stats -->
  <div class="stats-grid">
    <div class="stat-card">
      <div class="label">Total Vues</div>
      <div class="value">{stats['total_views']:,}</div>
      <div class="subtitle">Toutes les vidéos</div>
    </div>
    <div class="stat-card">
      <div class="label">CTR Moyen</div>
      <div class="value">{stats['avg_ctr']}%</div>
      <div class="subtitle">Click-through rate global</div>
    </div>
    <div class="stat-card">
      <div class="label">Rétention Moyenne</div>
      <div class="value">{stats['avg_retention']}%</div>
      <div class="subtitle">% vidéo regardée</div>
    </div>
    <div class="stat-card">
      <div class="label">Nouveaux Abonnés</div>
      <div class="value">+{stats['total_subscribers']}</div>
      <div class="subtitle">Croissance total</div>
    </div>
  </div>

  <!-- Rankings -->
  <div class="ranking-section">
    <h2>Top Performers</h2>
    <div class="ranking-grid">
      <div class="rank-container">
        <h3>🏆 Meilleur CTR</h3>
        <div class="rank-cards">
          {top_ctr_html}
        </div>
      </div>
      <div class="rank-container">
        <h3>📺 Meilleure Rétention</h3>
        <div class="rank-cards">
          {top_retention_html}
        </div>
      </div>
      <div class="rank-container">
        <h3>🚀 Plus Vues</h3>
        <div class="rank-cards">
          {top_views_html}
        </div>
      </div>
    </div>
  </div>

  <!-- Comparison Table -->
  <div class="comparison-section">
    <h2>Comparaison Complète</h2>
    <div class="comparison-table">
      <table>
        <thead>
          <tr>
            <th>Vidéo</th>
            <th>Vues</th>
            <th>CTR</th>
            <th>Rétention</th>
            <th>Impressions</th>
            <th>Abonnés</th>
            <th>Partages</th>
          </tr>
        </thead>
        <tbody>
          {comparison_rows}
        </tbody>
      </table>
    </div>
  </div>

  <!-- Footer -->
  <div class="footer">
    Dashboard généré par yt-analytics · Données historiques stockées dans yt-analytics/history/
  </div>

</div>
</body>
</html>
"""

    return html

def main():
    print("📊 Chargement de tous les historiques vidéo...")
    videos = load_all_videos()

    if not videos:
        print("Aucune vidéo analysée. Commencez par générer des rapports individuels.")
        sys.exit(1)

    print(f"✅ {len(videos)} vidéo(s) trouvée(s)")

    result = calculate_global_stats(videos)
    if not result:
        print("Aucune analyse disponible")
        sys.exit(1)

    global_stats, latest_metrics = result

    print(f"\n📈 Statistiques globales:")
    print(f"  Total vues: {global_stats['total_views']:,}")
    print(f"  CTR moyen: {global_stats['avg_ctr']}%")
    print(f"  Rétention moyenne: {global_stats['avg_retention']}%")
    print(f"  Nouveaux abonnés: +{global_stats['total_subscribers']}")

    # Generate dashboard
    html_content = generate_dashboard_html(videos, (global_stats, latest_metrics), latest_metrics)
    output_file = OUTPUTS_DIR / "dashboard.html"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"\n✅ Dashboard généré: {output_file}")

    return output_file

if __name__ == "__main__":
    main()
