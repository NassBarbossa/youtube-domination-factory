#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate individual and aggregated analytics reports from YouTube CSV data.

Usage:
    python generate_report.py "path/to/CSV" "video-slug"

This script:
1. Parses YouTube Studio CSV
2. Checks historical data for the video
3. Calculates deltas (changes from last analysis)
4. Generates individual HTML report with comparison
5. Updates historical database
6. (Future) Regenerates aggregated dashboard
"""

import csv
import json
import sys
import io
from pathlib import Path
from datetime import datetime

if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PROJECT_ROOT = Path(__file__).parent
HISTORY_DIR = PROJECT_ROOT / "history"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

HISTORY_DIR.mkdir(exist_ok=True)
OUTPUTS_DIR.mkdir(exist_ok=True)

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

def parse_youtube_csv(csv_path):
    """Parse YouTube Studio CSV and return metrics dictionary."""

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        print("Erreur: Fichier CSV vide")
        sys.exit(1)

    total_row = rows[0]

    def get_value(key, default=0):
        val = total_row.get(key, "").strip()
        if not val or val == "-":
            return default
        return val

    views = int(get_value("Vues", 0))
    impressions = int(get_value("Impressions", 0))
    ctr = float(get_value("Taux de clics par impression (%)", 0))
    avg_pct_watched = float(get_value("Pourcentage moyen de vidéo regardé (%)", 0))
    watch_time_hours = float(get_value("Durée de visionnage (heures)", 0))
    unique_viewers = int(get_value("Spectateurs uniques", 0))
    new_subscribers = int(get_value("Nouveaux abonnés", 0))
    shares = int(get_value("Partages", 0))
    average_view_duration = get_value("Durée moyenne d'une vue", "0:00")

    return {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "views": views,
        "impressions": impressions,
        "ctr": round(ctr, 2),
        "retention": round(avg_pct_watched, 2),
        "watch_time_hours": round(watch_time_hours, 2),
        "average_view_duration": average_view_duration,
        "unique_viewers": unique_viewers,
        "new_subscribers": new_subscribers,
        "shares": shares
    }

def calculate_delta(current, previous):
    """Calculate change (delta) between current and previous metrics."""
    if previous is None:
        return None

    if current == 0 and previous == 0:
        return {"value": 0, "percent": 0, "status": "stable"}

    if previous == 0:
        return {"value": current, "percent": float('inf'), "status": "new"}

    delta = current - previous
    percent = (delta / previous) * 100

    if abs(percent) < 0.5:
        status = "stable"
    elif percent > 0:
        status = "up"
    else:
        status = "down"

    return {
        "value": round(delta, 2),
        "percent": round(percent, 2),
        "previous": previous,
        "current": current,
        "status": status
    }

def load_history(video_slug):
    """Load historical data for a video."""
    history_file = HISTORY_DIR / f"{video_slug}.json"

    if history_file.exists():
        with open(history_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    return {
        "video_slug": video_slug,
        "analyses": []
    }

def save_history(video_slug, history_data):
    """Save historical data for a video."""
    history_file = HISTORY_DIR / f"{video_slug}.json"

    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(history_data, f, indent=2, ensure_ascii=False)

def get_previous_analysis(history_data):
    """Get the most recent previous analysis."""
    if len(history_data["analyses"]) == 0:
        return None
    return history_data["analyses"][-1]

def add_analysis(history_data, metrics):
    """Add new analysis to history."""
    history_data["analyses"].append(metrics)
    return history_data

def format_metric_badge(delta):
    """Format delta for HTML display."""
    if delta is None:
        return "Première analyse"

    status = delta["status"]
    percent = delta["percent"]
    value = delta["value"]

    if status == "new":
        return f'<span class="badge badge-new">NOUVEAU</span>'
    elif status == "up":
        return f'<span class="badge badge-up">↑ +{percent}%</span>'
    elif status == "down":
        return f'<span class="badge badge-down">↓ {percent}%</span>'
    else:
        return f'<span class="badge badge-stable">→ Stable</span>'

def generate_html_report(video_slug, metrics, delta_data):
    """Generate HTML report with comparison data."""

    # Format comparison section
    comparison_section = ""
    if delta_data["ctr"] is not None:
        comparison_section = f"""
  <!-- Comparison with previous analysis -->
  <div class="comparison-section">
    <h2>Progression depuis la dernière analyse</h2>
    <div class="comparison-grid">
      <div class="comparison-card">
        <div class="metric-name">CTR</div>
        <div class="current">{metrics['ctr']}%</div>
        <div class="delta">{delta_data['ctr']['previous']}% → {delta_data['ctr']['current']}%</div>
        <div class="badge {('badge-up' if delta_data['ctr']['status'] == 'up' else 'badge-down' if delta_data['ctr']['status'] == 'down' else 'badge-stable')}">
          {('↑ +' + str(delta_data['ctr']['percent']) + '%') if delta_data['ctr']['status'] == 'up' else ('↓ ' + str(delta_data['ctr']['percent']) + '%') if delta_data['ctr']['status'] == 'down' else '→ Stable'}
        </div>
      </div>
      <div class="comparison-card">
        <div class="metric-name">Rétention</div>
        <div class="current">{metrics['retention']}%</div>
        <div class="delta">{delta_data['retention']['previous']}% → {delta_data['retention']['current']}%</div>
        <div class="badge {('badge-up' if delta_data['retention']['status'] == 'up' else 'badge-down' if delta_data['retention']['status'] == 'down' else 'badge-stable')}">
          {('↑ +' + str(delta_data['retention']['percent']) + '%') if delta_data['retention']['status'] == 'up' else ('↓ ' + str(delta_data['retention']['percent']) + '%') if delta_data['retention']['status'] == 'down' else '→ Stable'}
        </div>
      </div>
      <div class="comparison-card">
        <div class="metric-name">Vues</div>
        <div class="current">{metrics['views']}</div>
        <div class="delta">{delta_data['views']['previous']} → {delta_data['views']['current']}</div>
        <div class="badge {('badge-up' if delta_data['views']['status'] == 'up' else 'badge-down' if delta_data['views']['status'] == 'down' else 'badge-stable')}">
          {('↑ +' + str(delta_data['views']['value'])) if delta_data['views']['status'] == 'up' else ('↓ ' + str(delta_data['views']['value'])) if delta_data['views']['status'] == 'down' else '→ Stable'}
        </div>
      </div>
      <div class="comparison-card">
        <div class="metric-name">Nouveaux abonnés</div>
        <div class="current">+{metrics['new_subscribers']}</div>
        <div class="delta">{delta_data['new_subscribers']['previous']} → {delta_data['new_subscribers']['current']}</div>
        <div class="badge {('badge-up' if delta_data['new_subscribers']['status'] == 'up' else 'badge-down' if delta_data['new_subscribers']['status'] == 'down' else 'badge-stable')}">
          {('↑ +' + str(delta_data['new_subscribers']['value'])) if delta_data['new_subscribers']['status'] == 'up' else ('↓ ' + str(delta_data['new_subscribers']['value'])) if delta_data['new_subscribers']['status'] == 'down' else '→ Stable'}
        </div>
      </div>
    </div>
  </div>
"""
    else:
        comparison_section = """
  <!-- First analysis -->
  <div class="comparison-section first-analysis">
    <h2>Première analyse pour cette vidéo</h2>
    <p>Pas de données de comparaison disponibles. Les prochaines analyses afficheront la progression.</p>
  </div>
"""

    html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Analytics — {video_slug}</title>
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
    max-width: 1400px;
    margin: 0 auto;
  }}

  .header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 40px;
    padding-bottom: 30px;
    border-bottom: 1px solid #2a2a2a;
  }}

  .header-left h1 {{
    font-size: 36px;
    font-weight: 800;
    margin-bottom: 8px;
  }}

  .header-left h1 span {{ color: #4a90d9; }}

  .header-left .meta {{
    font-size: 14px;
    color: #888;
  }}

  .badge {{
    display: inline-block;
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
  }}

  .badge-up {{ background: #2eaa5e1a; color: #2eaa5e; }}
  .badge-down {{ background: #ff44441a; color: #ff4444; }}
  .badge-stable {{ background: #f5a6231a; color: #f5a623; }}
  .badge-new {{ background: #4a90d91a; color: #4a90d9; }}

  /* Comparison Section */
  .comparison-section {{
    background: #1a1a1a;
    border-radius: 16px;
    padding: 28px;
    border: 1px solid #2a2a2a;
    margin-bottom: 40px;
  }}

  .comparison-section h2 {{
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 20px;
  }}

  .comparison-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
  }}

  .comparison-card {{
    background: #252525;
    padding: 16px;
    border-radius: 12px;
    border-left: 3px solid #4a90d9;
  }}

  .comparison-card .metric-name {{
    font-size: 12px;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 8px;
  }}

  .comparison-card .current {{
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 8px;
  }}

  .comparison-card .delta {{
    font-size: 13px;
    color: #aaa;
    margin-bottom: 8px;
  }}

  .comparison-card .badge {{
    width: 100%;
    text-align: center;
  }}

  .first-analysis {{
    text-align: center;
    padding: 40px;
  }}

  .first-analysis p {{
    font-size: 16px;
    color: #aaa;
  }}

  .metrics-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin-bottom: 40px;
  }}

  .metric-card {{
    background: #1a1a1a;
    border-radius: 16px;
    padding: 24px;
    border: 1px solid #2a2a2a;
  }}

  .metric-card .label {{
    font-size: 13px;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 8px;
  }}

  .metric-card .value {{
    font-size: 36px;
    font-weight: 800;
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

  <div class="header">
    <div class="header-left">
      <h1>Analytics <span>— {video_slug}</span></h1>
      <div class="meta">Analysée le {metrics['date']}</div>
    </div>
  </div>

  {comparison_section}

  <div class="metrics-grid">
    <div class="metric-card">
      <div class="label">Vues</div>
      <div class="value">{metrics['views']}</div>
    </div>
    <div class="metric-card">
      <div class="label">CTR</div>
      <div class="value">{metrics['ctr']}%</div>
    </div>
    <div class="metric-card">
      <div class="label">Rétention</div>
      <div class="value">{metrics['retention']}%</div>
    </div>
    <div class="metric-card">
      <div class="label">Abonnés</div>
      <div class="value">+{metrics['new_subscribers']}</div>
    </div>
  </div>

  <div class="footer">
    Rapport généré par yt-analytics · {datetime.now().strftime('%d %B %Y')}
  </div>

</div>
</body>
</html>
"""

    return html_content

def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_report.py 'path/to/CSV' 'video-slug'")
        print("Example: python generate_report.py 'inputs/vibecoding.csv' 'vibecoding'")
        sys.exit(1)

    csv_path = sys.argv[1]
    video_slug = sys.argv[2]

    if not Path(csv_path).exists():
        print(f"Erreur: Fichier CSV non trouvé: {csv_path}")
        sys.exit(1)

    print(f"📊 Parsing {video_slug}...")
    metrics = parse_youtube_csv(csv_path)

    print(f"📚 Chargement de l'historique...")
    history = load_history(video_slug)
    previous = get_previous_analysis(history)

    # Calculate deltas
    delta_data = {
        "ctr": calculate_delta(metrics["ctr"], previous["ctr"] if previous else None),
        "retention": calculate_delta(metrics["retention"], previous["retention"] if previous else None),
        "views": calculate_delta(metrics["views"], previous["views"] if previous else None),
        "new_subscribers": calculate_delta(metrics["new_subscribers"], previous["new_subscribers"] if previous else None),
    }

    # Display comparison
    print(f"\n📈 Comparaison:")
    if previous:
        print(f"  CTR: {previous['ctr']}% → {metrics['ctr']}% ({'+' if delta_data['ctr']['percent'] > 0 else ''}{delta_data['ctr']['percent']}%)")
        print(f"  Rétention: {previous['retention']}% → {metrics['retention']}% ({'+' if delta_data['retention']['percent'] > 0 else ''}{delta_data['retention']['percent']}%)")
        print(f"  Vues: {previous['views']} → {metrics['views']} ({'+' if delta_data['views']['value'] > 0 else ''}{delta_data['views']['value']})")
    else:
        print("  Première analyse pour cette vidéo")

    # Save to history
    history = add_analysis(history, metrics)
    save_history(video_slug, history)
    print(f"✅ Historique mis à jour")

    # Generate HTML
    html_content = generate_html_report(video_slug, metrics, delta_data)
    output_file = OUTPUTS_DIR / f"{video_slug}-analytics.html"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ Rapport généré: {output_file}")

    return output_file

if __name__ == "__main__":
    main()
