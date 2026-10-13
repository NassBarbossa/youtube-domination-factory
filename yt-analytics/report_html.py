"""Rendu HTML du rapport analytics (charte du cadre). Utilisé par analyze.py.

Formes : stat tiles pour les totaux, tableau comparatif avec barres relatives (une teinte),
entonnoir impressions → vues → abonnés avec jauges, jauge de rétention, barres de trafic.
Couleurs des données : bleu punk foncé sur crème (contraste ≥ 4,5:1) ; accent « meilleur » en sable foncé.
"""
import statistics
from datetime import datetime, timezone

MIN_AGE_DAYS = 4  # retard de l'API YouTube Analytics : avant ça, une vidéo remonte 0 ou 1 vue
KIND_CLASS = {"réussite": "good", "moyenne": "mid", "échec": "bad"}


def age_days(published_at):
    return (datetime.now(timezone.utc) - datetime.fromisoformat(published_at.replace("Z", "+00:00"))).days


def format_duration(seconds):
    seconds = int(seconds or 0)
    if seconds < 3600:
        return f"{seconds // 60}:{seconds % 60:02d}"
    return f"{seconds // 3600}:{(seconds % 3600) // 60:02d}:{seconds % 60:02d}"


def fmt_int(n):
    return f"{int(n):,}".replace(",", " ")


def bar(value, vmax, title="", best=False):
    pct = (value / vmax * 100) if vmax else 0
    return f'<span class="bar{" best" if best else ""}" title="{title}"><span style="width:{pct:.1f}%"></span></span>'


def meter(pct, title=""):
    pct = max(0, min(100, pct or 0))
    return f'<span class="meter" title="{title}"><span style="width:{pct:.1f}%"></span></span>'


def traffic_html(sources, limit):
    if not sources:
        return '<p class="muted small">Pas de données.</p>'
    vmax = max(src["percent"] for src in sources[:limit]) or 1
    rows = []
    for src in sources[:limit]:
        rows.append(
            '<div class="trow"><span class="tname">%s</span>%s<span class="tval">%s%%</span></div>'
            % (src["source"], bar(src["percent"], vmax, f"{src['source']} : {src['views']} vues ({src['percent']}%)"), src["percent"])
        )
    return "".join(rows)


def badge(n, cls="badge"):
    if not n.get("verdict_label"):
        return ""
    return f'<span class="{cls} {KIND_CLASS.get(n.get("verdict_kind", ""), "mid")}">{n["verdict_label"]}</span>'


def generate_html(videos_data, channel_traffic, notes=None):
    notes = notes or {}
    vnotes = notes.get("videos", {})
    now = datetime.now().strftime("%d/%m/%Y à %H:%M")
    with_metrics = [v for v in videos_data if v["metrics"]]
    reliable = [v for v in with_metrics if age_days(v["published_at"]) >= MIN_AGE_DAYS]
    fresh = [v for v in with_metrics if age_days(v["published_at"]) < MIN_AGE_DAYS]

    def m(v, k):
        return v["metrics"][k]

    def ctr(v):
        return v["ctr_official"]["ctr"] if v.get("ctr_official") else None

    def imp(v):
        return v["ctr_official"]["impressions"] if v.get("ctr_official") else None

    def conv(v):
        return round(m(v, "subscribers_gained") / m(v, "views") * 100, 1) if m(v, "views") else 0

    views_list = [m(v, "views") for v in reliable]
    median_views = statistics.median(views_list) if views_list else 0
    total_views = sum(views_list)
    total_subs = sum(m(v, "subscribers_gained") for v in reliable)
    total_imp = sum(imp(v) or 0 for v in reliable)
    ctrs = [ctr(v) for v in reliable if ctr(v) is not None]
    avg_ctr = round(statistics.mean(ctrs), 1) if ctrs else None
    avg_ret = round(statistics.mean(m(v, "retention_pct") for v in reliable), 1) if reliable else 0
    best = {
        "imp": max((imp(v) or 0 for v in reliable), default=0),
        "ctr": max(ctrs, default=None),
        "views": max(views_list, default=0),
        "ret": max((m(v, "retention_pct") for v in reliable), default=0),
        "subs": max((m(v, "subscribers_gained") for v in reliable), default=0),
        "conv": max((conv(v) for v in reliable), default=0),
    }

    # ---- comparatif
    def cell(val, vmax, text, title):
        is_best = val is not None and val == vmax and vmax not in (None, 0)
        return f'<td class="num{" is-best" if is_best else ""}"><span class="v">{text}</span>{bar(val or 0, vmax or 1, title, is_best)}</td>'

    rows = []
    for v in reliable:
        n = vnotes.get(v["id"], {})
        title_short = v["title"] if len(v["title"]) <= 48 else v["title"][:46] + "…"
        rows.append(
            "<tr>"
            f'<td class="vid"><img src="{v["thumbnail"]}" alt=""><div><a href="#v-{v["id"]}">{title_short}</a><div class="muted small">{v["published_at"][:10]}{badge(n, "pill")}</div></div></td>'
            + cell(imp(v), best["imp"], fmt_int(imp(v)) if imp(v) is not None else "n/d", "Impressions des miniatures, depuis la mise en ligne (YouTube Studio)")
            + cell(ctr(v), best["ctr"], f"{ctr(v)}%" if ctr(v) is not None else "n/d", "Clics ÷ impressions (YouTube Studio)")
            + cell(m(v, "views"), best["views"], fmt_int(m(v, "views")), "Vues (API YouTube Analytics)")
            + cell(m(v, "retention_pct"), best["ret"], f"{m(v, 'retention_pct')}%", "Part moyenne de la vidéo regardée")
            + cell(m(v, "subscribers_gained"), best["subs"], f"+{m(v, 'subscribers_gained')}", "Abonnés gagnés par cette vidéo")
            + cell(conv(v), best["conv"], f"{conv(v)}%", "Abonnés gagnés ÷ vues")
            + "</tr>"
        )
    for v in fresh:
        rows.append(
            '<tr class="fresh-row">'
            f'<td class="vid"><img src="{v["thumbnail"]}" alt=""><div>{v["title"]}<div class="muted small">{v["published_at"][:10]} · publiée il y a {age_days(v["published_at"])} j, hors comparatif (retard de l\'API)</div></div></td>'
            f'<td class="num muted">{fmt_int(imp(v)) if imp(v) is not None else "n/d"}</td><td class="num muted">{f"{ctr(v)}%" if ctr(v) is not None else "n/d"}</td>'
            '<td class="num muted">…</td><td class="num muted">…</td><td class="num muted">…</td><td class="num muted">…</td></tr>'
        )

    # ---- cartes vidéo
    cards = []
    for v in with_metrics:
        n = vnotes.get(v["id"], {})
        is_fresh = age_days(v["published_at"]) < MIN_AGE_DAYS
        dur = v.get("duration_sec")
        head = (
            '<div class="vhead">'
            f'<img src="{v["thumbnail"]}" alt="" class="vthumb">'
            f'<div class="vinfo"><h2>{v["title"]}</h2><div class="muted small">Publiée le {v["published_at"][:10]}'
            f'{f" · {format_duration(dur)}" if dur else ""} · <a href="https://www.youtube.com/watch?v={v["id"]}">youtube.com/watch?v={v["id"]}</a></div></div>'
            f"{badge(n)}</div>"
        )
        if is_fresh:
            body = (
                f'<div class="fresh">Publiée il y a {age_days(v["published_at"])} jour(s). L\'API a 2 à 3 jours de retard : '
                f'{fmt_int(imp(v)) if imp(v) is not None else "?"} impressions et {f"{ctr(v)}%" if ctr(v) is not None else "?"} de CTR selon Studio, '
                "le reste ne veut encore rien dire. Hors moyennes.</div>"
            )
        else:
            idx = round(m(v, "views") / median_views, 2) if median_views else None
            watched = m(v, "avg_view_duration_sec")
            ret_pct = m(v, "retention_pct")
            like_rate = round(m(v, "likes") / m(v, "views") * 100, 1) if m(v, "views") else 0
            funnel = (
                '<div class="funnel">'
                f'<div class="step"><div class="lbl">Impressions</div><div class="big">{fmt_int(imp(v)) if imp(v) is not None else "n/d"}</div><div class="muted small">miniature montrée (Studio)</div></div>'
                f'<div class="arrow"><div class="rate">{f"{ctr(v)}%" if ctr(v) is not None else "n/d"}</div>{meter(ctr(v) or 0, "CTR : clics ÷ impressions")}<div class="muted small">CTR</div></div>'
                f'<div class="step"><div class="lbl">Vues</div><div class="big">{fmt_int(m(v, "views"))}</div><div class="muted small">{f"{idx}× la médiane" if idx else ""}</div></div>'
                f'<div class="arrow"><div class="rate">{conv(v)}%</div>{meter(conv(v), "Abonnés ÷ vues")}<div class="muted small">conversion</div></div>'
                f'<div class="step"><div class="lbl">Abonnés</div><div class="big">+{m(v, "subscribers_gained")}</div><div class="muted small">gagnés</div></div>'
                "</div>"
            )
            retention = (
                '<div class="retention">'
                f'<div class="rlab"><strong>Rétention {ret_pct}%</strong> · {format_duration(watched)} regardées en moyenne{f" sur {format_duration(dur)}" if dur else ""}</div>'
                f'{meter(ret_pct, f"{format_duration(watched)} regardées sur {format_duration(dur) if dur else chr(63)}")}'
                "</div>"
            )
            engagement = (
                '<div class="mini-grid">'
                f'<div class="mini"><span class="k">Likes</span><span class="v">{m(v, "likes")}</span><span class="muted small">{like_rate}% des vues</span></div>'
                f'<div class="mini"><span class="k">Commentaires</span><span class="v">{m(v, "comments")}</span></div>'
                f'<div class="mini"><span class="k">Partages</span><span class="v">{m(v, "shares")}</span></div>'
                f'<div class="mini"><span class="k">Temps regardé</span><span class="v">{fmt_int(m(v, "watch_time_min"))} min</span></div>'
                "</div>"
            )
            analysis = ""
            if n:
                worked = "".join(f"<li>{x}</li>" for x in n.get("worked", [])) or "<li>Rien de net.</li>"
                failed = "".join(f"<li>{x}</li>" for x in n.get("failed", [])) or "<li>Rien de net.</li>"
                analysis = (
                    '<div class="two-col">'
                    f'<div class="col good-col"><h3>Ce qui a marché</h3><ul>{worked}</ul></div>'
                    f'<div class="col bad-col"><h3>Ce qui n\'a pas marché</h3><ul>{failed}</ul></div>'
                    "</div>"
                    + (f'<div class="verdict"><strong>Verdict.</strong> {n["verdict"]}</div>' if n.get("verdict") else "")
                )
            body = (
                funnel + retention
                + '<div class="split">'
                f'<div><h3 class="h-small">D\'où viennent les vues</h3>{traffic_html(v.get("traffic_sources", []), 5)}</div>'
                f'<div><h3 class="h-small">Engagement</h3>{engagement}</div></div>'
                + analysis
            )
        cards.append(f'<section class="card vcard" id="v-{v["id"]}">{head}{body}</section>')

    recos = []
    for i, r in enumerate(notes.get("recommendations", []), 1):
        recos.append(
            f'<div class="reco"><div class="reco-num">{i}</div><div><h3>{r["title"]}</h3>'
            f'<p><strong>Basée sur :</strong> {r["based_on"]}</p><p><strong>Action :</strong> {r["action"]}</p>'
            f'<p><strong>Impact attendu :</strong> {r["impact"]}</p></div></div>'
        )
    recos_section = f'<section class="card"><h2 class="section-title">Recommandations, par priorité</h2>{"".join(recos)}</section>' if recos else ""
    diagnostic = f'<div class="diag"><div class="diag-k">Diagnostic</div><p>{notes["overview"]}</p></div>' if notes.get("overview") else ""

    return TEMPLATE.format(
        date=datetime.now().strftime("%d/%m/%Y"), count=len(videos_data), now=now,
        n_reliable=len(reliable), n_fresh=len(fresh),
        total_imp=fmt_int(total_imp) if total_imp else "n/d",
        avg_ctr=f"{avg_ctr}%" if avg_ctr is not None else "n/d",
        total_views=fmt_int(total_views), median_views=f"{median_views:.0f}", avg_ret=avg_ret, total_subs=total_subs,
        diagnostic=diagnostic, rows="".join(rows), channel_traffic=traffic_html(channel_traffic, 8),
        cards="".join(cards), recos=recos_section,
    )


TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Nassin Crypto · analytics du {date}</title>
<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Public+Sans:wght@400;600;700&display=swap" rel="stylesheet">
<style>
  :root {{ --bg:#0B0B0B; --sand:#DBB17F; --sand-light:#F3D6A8; --sand-dark:#9C7748; --cream:#F4EFE7; --punk:#648596; --punk-dark:#4F6C7B; --punk-track:#D6DEE2; --ink:#0B0B0B; --ink-2:#3B3A37; --ink-3:#6E6A63; --good:#2E8B57; --bad:#B23A2E; --rule:#DED7CB; }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html {{ scroll-behavior:smooth; }}
  body {{ background:var(--bg); color:var(--cream); font-family:'Public Sans', Helvetica, Arial, sans-serif; padding:40px 20px 60px; line-height:1.45; }}
  .container {{ max-width:1400px; margin:0 auto; }}
  h1, h2, h3, .big, .reco-num, .stat .value {{ font-family:'Archivo Black', Impact, 'Arial Black', sans-serif; font-weight:400; }}
  a {{ color:var(--punk-dark); }}
  .muted {{ color:var(--ink-3); }} .small {{ font-size:12px; }}
  .page-header {{ display:flex; justify-content:space-between; align-items:flex-end; gap:24px; margin-bottom:28px; padding-bottom:18px; border-bottom:3px solid var(--sand); flex-wrap:wrap; }}
  .page-header h1 {{ font-size:34px; color:var(--sand); line-height:1.1; }}
  .page-header h1 small {{ display:block; font-family:'Public Sans', sans-serif; font-weight:700; font-size:13px; color:#9A968D; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:8px; }}
  .page-header .date {{ font-size:13px; color:#9A968D; text-align:right; line-height:1.5; }}
  .card {{ background:var(--cream); color:var(--ink); border:3px solid var(--bg); box-shadow:8px 8px 0 var(--sand-dark); padding:28px; margin-bottom:28px; }}
  .section-title {{ font-size:22px; margin-bottom:18px; }}
  .h-small {{ font-size:12px; letter-spacing:1.2px; text-transform:uppercase; margin-bottom:10px; color:var(--ink-2); font-family:'Public Sans', sans-serif; font-weight:700; }}
  .kpis {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(160px, 1fr)); gap:12px; margin-bottom:22px; }}
  .stat {{ background:var(--bg); color:var(--cream); padding:16px 18px; }}
  .stat .label {{ font-size:11px; letter-spacing:1px; text-transform:uppercase; color:#9A968D; font-weight:700; margin-bottom:6px; }}
  .stat .value {{ font-size:30px; color:var(--sand); line-height:1.1; }}
  .stat .sub {{ font-size:12px; color:#9A968D; margin-top:4px; }}
  .diag {{ display:grid; grid-template-columns:120px 1fr; gap:18px; align-items:start; background:#fff; border:2px solid var(--ink); padding:18px 20px; margin-bottom:22px; }}
  .diag-k {{ font-family:'Archivo Black', sans-serif; font-size:14px; letter-spacing:1px; text-transform:uppercase; color:var(--sand-dark); padding-top:3px; }}
  .diag p {{ font-size:15px; }}
  table.cmp {{ width:100%; border-collapse:collapse; font-size:14px; }}
  .cmp th {{ text-align:left; font-size:11px; letter-spacing:1px; text-transform:uppercase; color:var(--ink-2); padding:8px 10px; border-bottom:2px solid var(--ink); }}
  .cmp th.num {{ text-align:right; }}
  .cmp td {{ padding:12px 10px; border-bottom:1px solid var(--rule); vertical-align:middle; }}
  .cmp tr:last-child td {{ border-bottom:none; }}
  .cmp td.vid {{ display:flex; gap:12px; align-items:center; min-width:280px; }}
  .cmp td.vid img {{ width:72px; height:40px; object-fit:cover; border:2px solid var(--ink); flex-shrink:0; }}
  .cmp td.vid a {{ color:var(--ink); font-weight:700; text-decoration:none; }}
  .cmp td.num {{ text-align:right; width:11%; font-variant-numeric:tabular-nums; }}
  .cmp td.num .v {{ display:block; font-weight:700; margin-bottom:4px; }}
  .cmp td.is-best .v::after {{ content:""; display:inline-block; width:8px; height:8px; border-radius:50%; background:var(--sand-dark); margin-left:6px; vertical-align:middle; }}
  .cmp .fresh-row td {{ color:var(--ink-3); }}
  .legend {{ font-size:12px; color:var(--ink-3); margin-top:10px; }}
  .legend i {{ display:inline-block; width:8px; height:8px; border-radius:50%; background:var(--sand-dark); margin:0 4px 0 2px; vertical-align:middle; }}
  .bar {{ display:block; height:10px; }}
  .bar > span {{ display:block; height:10px; background:var(--punk-dark); border-radius:0 4px 4px 0; min-width:2px; }}
  .bar.best > span {{ background:var(--sand-dark); }}
  .meter {{ display:block; height:10px; background:var(--punk-track); border-radius:4px; overflow:hidden; }}
  .meter > span {{ display:block; height:10px; background:var(--punk-dark); border-radius:0 4px 4px 0; min-width:2px; }}
  .trow {{ display:grid; grid-template-columns:150px 1fr 56px; gap:10px; align-items:center; margin-bottom:8px; font-size:13px; }}
  .tname {{ font-weight:600; }} .tval {{ text-align:right; font-variant-numeric:tabular-nums; }}
  .vhead {{ display:flex; gap:18px; align-items:center; margin-bottom:22px; }}
  .vthumb {{ width:200px; height:112px; object-fit:cover; border:3px solid var(--ink); flex-shrink:0; }}
  .vinfo {{ flex:1; }} .vinfo h2 {{ font-size:20px; line-height:1.25; margin-bottom:6px; }}
  .badge, .pill {{ font-weight:700; font-size:11px; letter-spacing:1px; text-transform:uppercase; color:#fff; white-space:nowrap; }}
  .badge {{ padding:8px 12px; border:3px solid var(--ink); }} .pill {{ padding:2px 7px; margin-left:8px; font-size:10px; }}
  .good {{ background:var(--good); }} .mid {{ background:var(--sand-dark); }} .bad {{ background:var(--bad); }}
  .funnel {{ display:grid; grid-template-columns:1fr 1.2fr 1fr 1.2fr 1fr; gap:10px; align-items:center; background:#fff; border:2px solid var(--ink); padding:16px 18px; margin-bottom:14px; }}
  .step {{ text-align:center; }} .step .lbl {{ font-size:11px; letter-spacing:1px; text-transform:uppercase; color:var(--ink-2); font-weight:700; }} .step .big {{ font-size:30px; line-height:1.15; }}
  .arrow {{ text-align:center; padding:0 10px; }} .arrow .rate {{ font-weight:700; font-size:16px; margin-bottom:4px; font-variant-numeric:tabular-nums; }}
  .retention {{ background:#fff; border:2px solid var(--ink); padding:12px 18px; margin-bottom:18px; }} .rlab {{ font-size:14px; margin-bottom:8px; }}
  .split {{ display:grid; grid-template-columns:1.3fr 1fr; gap:24px; }}
  .mini-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:10px; }}
  .mini {{ background:#fff; border:2px solid var(--ink); padding:10px 12px; display:flex; flex-direction:column; }}
  .mini .k {{ font-size:11px; letter-spacing:1px; text-transform:uppercase; color:var(--ink-2); font-weight:700; }} .mini .v {{ font-size:22px; font-weight:700; }}
  .two-col {{ display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-top:22px; }}
  .col {{ background:#fff; border:2px solid var(--ink); padding:16px 18px; }}
  .col h3 {{ font-size:14px; margin-bottom:10px; }} .good-col h3 {{ color:var(--good); }} .bad-col h3 {{ color:var(--bad); }}
  .col ul {{ padding-left:18px; font-size:14px; }} .col li {{ margin-bottom:7px; }}
  .verdict {{ margin-top:16px; padding:14px 18px; background:var(--bg); color:var(--cream); font-size:15px; border-left:6px solid var(--sand); }}
  .fresh {{ padding:14px 18px; background:var(--sand-light); border:2px dashed var(--sand-dark); font-size:14px; }}
  .reco {{ display:flex; gap:18px; padding:18px 0; border-top:2px solid var(--ink); }} .reco:first-of-type {{ border-top:none; padding-top:0; }}
  .reco-num {{ font-size:30px; color:var(--punk-dark); width:44px; flex-shrink:0; line-height:1; }}
  .reco h3 {{ font-size:17px; margin-bottom:8px; }} .reco p {{ font-size:14px; margin-bottom:4px; }}
  .footer {{ text-align:center; padding-top:24px; font-size:12px; color:#9A968D; }}
  @media (max-width:900px) {{ .two-col, .split, .mini-grid, .funnel, .diag {{ grid-template-columns:1fr; }} .arrow {{ padding:6px 0; }} .vhead {{ flex-wrap:wrap; }} table.cmp {{ display:block; overflow-x:auto; }} }}
  @media print {{ body {{ background:#fff; color:var(--ink); padding:0; }} .card {{ box-shadow:none; break-inside:avoid; margin-bottom:18px; }} .page-header h1, .stat .value {{ color:var(--ink); }} .stat {{ background:#fff; color:var(--ink); border:2px solid var(--ink); }} .verdict {{ background:#fff; color:var(--ink); border:2px solid var(--ink); }} .page-header .date, .stat .sub, .stat .label {{ color:var(--ink-2); }} }}
</style>
</head>
<body>
<div class="container">
  <div class="page-header">
    <h1><small>Nassin Crypto · nouvelle chaîne</small>Analytics des {count} dernières vidéos</h1>
    <div class="date">Vues, rétention, abonnés : API YouTube Analytics (2 à 3 jours de retard)<br>Impressions et CTR : YouTube Studio, depuis la mise en ligne<br>Rapport généré le {now}</div>
  </div>

  <section class="card">
    <h2 class="section-title">La chaîne en un coup d'œil</h2>
    <div class="kpis">
      <div class="stat"><div class="label">Vidéos fiables</div><div class="value">{n_reliable}</div><div class="sub">{n_fresh} trop récente(s)</div></div>
      <div class="stat"><div class="label">Impressions</div><div class="value">{total_imp}</div><div class="sub">miniatures montrées</div></div>
      <div class="stat"><div class="label">CTR moyen</div><div class="value">{avg_ctr}</div><div class="sub">YouTube : la moitié des chaînes entre 2 et 10 %</div></div>
      <div class="stat"><div class="label">Vues</div><div class="value">{total_views}</div><div class="sub">médiane {median_views} par vidéo</div></div>
      <div class="stat"><div class="label">Rétention</div><div class="value">{avg_ret}%</div><div class="sub">de la vidéo regardée</div></div>
      <div class="stat"><div class="label">Abonnés gagnés</div><div class="value">+{total_subs}</div><div class="sub">par ces vidéos</div></div>
    </div>
    {diagnostic}
    <h3 class="h-small">Comparatif des vidéos fiables</h3>
    <table class="cmp">
      <thead><tr><th>Vidéo</th><th class="num">Impressions</th><th class="num">CTR</th><th class="num">Vues</th><th class="num">Rétention</th><th class="num">Abonnés</th><th class="num">Conversion</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
    <div class="legend">Barres : proportion du maximum de la colonne. <i></i>meilleure valeur de la colonne. Conversion = abonnés gagnés ÷ vues.</div>
  </section>

  <section class="card">
    <h2 class="section-title">D'où viennent les vues de la chaîne, 30 derniers jours</h2>
    {channel_traffic}
  </section>

  {cards}
  {recos}

  <div class="footer">yt-analytics · youtube-domination-factory · analyze.py + studio_ctr.py</div>
</div>
</body>
</html>
"""
