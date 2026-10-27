#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = ["playwright>=1.49"]
# ///
"""Lit les moments clés de la rétention dans YouTube Studio (onglet Engagement) : pourcentage encore là à 30 s,
moments forts, pics et creux. Aucune API Google ne les fournit.

Usage :
    uv run yt-analytics/studio_retention.py                 # les vidéos du dernier outputs/analytics-<date>.json
    uv run yt-analytics/studio_retention.py ID1 ID2 ...     # des vidéos précises
    uv run yt-analytics/studio_retention.py --period default  # 28 derniers jours au lieu de « depuis la mise en ligne »

Même profil Chrome que studio_ctr.py (yt-analytics/.studio-profile, connexion une fois).
Résultat : history/studio-retention.json (une entrée datée par vidéo, texte brut de la carte conservé)
+ capture et texte de la page dans outputs/studio-debug/<id>-retention.{png,txt}.
Studio affiche la carte « moments clés » quand la vidéo a au moins 100 vues et 60 s ; sinon « carte absente ».
"""
import argparse
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

SCRIPT_DIR = Path(__file__).resolve().parent
PROFILE_DIR = SCRIPT_DIR / ".studio-profile"
HISTORY = SCRIPT_DIR / "history" / "studio-retention.json"
OUTPUTS = SCRIPT_DIR / "outputs"
DEBUG = OUTPUTS / "studio-debug"
PERIODS = {"lifetime": "period-lifetime", "default": "period-default"}

CARD_TITLES = ["Key moments for audience retention", "Moments clés pour la fidélisation de l'audience",
               "Moments clés de la fidélisation", "Moments clés"]
SECTIONS = {  # libellés EN / FR des quatre types de moments
    "intro": ["Intro", "Introduction"],
    "top_moments": ["Top moments", "Moments forts", "Meilleurs moments"],
    "spikes": ["Spikes", "Pics"],
    "dips": ["Dips", "Creux", "Baisses"],
}
TS = re.compile(r"\b(\d{1,2}:\d{2}(?::\d{2})?)\b")
PCT = re.compile(r"(\d{1,3}(?:[.,]\d+)?)\s?%")


def to_seconds(ts: str) -> int:
    parts = [int(x) for x in ts.split(":")]
    return parts[0] * 60 + parts[1] if len(parts) == 2 else parts[0] * 3600 + parts[1] * 60 + parts[2]


def parse_card(text: str) -> dict:
    """Découpe le texte de la page : carte « Audience retention » (durée moyenne, % moyen) et carte « moments clés »."""
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    out = {"card_found": False}
    for i, l in enumerate(lines):
        if l in ("Average view duration", "Durée moyenne de visionnage") and i + 1 < len(lines) and TS.search(lines[i + 1]):
            out["avg_view_duration"] = TS.search(lines[i + 1]).group(1)
        if l in ("Average percentage viewed", "Pourcentage moyen visionné", "Pourcentage moyen de la vidéo visionné") and i + 1 < len(lines) and PCT.search(lines[i + 1]):
            out["avg_pct_viewed"] = float(PCT.search(lines[i + 1]).group(1).replace(",", "."))
    start = next((i for i, l in enumerate(lines) if any(l.startswith(t) for t in CARD_TITLES)), None)
    if start is None:
        return out
    end = next((j for j in range(start + 1, min(start + 60, len(lines))) if lines[j] in ("See more", "Afficher plus")), min(start + 60, len(lines)))
    block = lines[start:end]
    out.update({"card_found": True, "card_text": "\n".join(block)})
    out["tabs"] = [l for l in block[1:8] if re.match(r"^(\d+ )?(Intro|Introduction|dips?|creux|baisses?|spikes?|pics?|top moments?|moments forts)$", l, re.I)]
    for l in block:
        m = PCT.search(l)
        if m and ("0:30" in l or re.search(r"\b30\s?s", l)):
            out["intro_30s_pct"] = float(m.group(1).replace(",", "."))
            low = l.lower()
            out["intro_vs_typical"] = ("below" if "below" in low or "inférieur" in low else
                                       "above" if "above" in low or "supérieur" in low else
                                       "typical" if "typical" in low or "typique" in low else None)
            out["intro_sentence"] = l
            break
    return out


def read_tab(page, tab_label: str) -> dict:
    """Clique un onglet de la carte (« 2 dips », « 1 spike »…) et renvoie les horodatages qui apparaissent."""
    try:
        page.get_by_text(tab_label, exact=True).first.click(timeout=4000)
    except Exception:
        return {}
    time.sleep(2)
    text = page.evaluate("() => document.body.innerText")
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    start = next((i for i, l in enumerate(lines) if any(l.startswith(t) for t in CARD_TITLES)), None)
    if start is None:
        return {}
    end = next((j for j in range(start + 1, min(start + 60, len(lines))) if lines[j] in ("See more", "Afficher plus")), min(start + 60, len(lines)))
    block = lines[start:end]
    # Après le clic, le lecteur intégré se cale sur le moment sélectionné : la ligne « 01:48 / 11:10 »
    # donne sa position. Les graduations de l'axe (lignes « m:ss » seules) et la phrase « …0:30 mark… » ne comptent pas.
    axis = sorted({l for l in block if TS.fullmatch(l)}, key=to_seconds)
    stamps = []
    for l in block:
        if TS.fullmatch(l) or "0:30" in l:
            continue
        m = re.match(r"^(\d{1,2}:\d{2}(?::\d{2})?)\s*/\s*(\d{1,2}:\d{2}(?::\d{2})?)$", l)
        if m and to_seconds(m.group(1)) > 0:
            stamps.append(m.group(1))
    detected = next((int(m.group(1)) for m in [re.match(r"^(\d+) ", tab_label)] if m), 1)
    return {"text": "\n".join(block), "timestamps": [{"time": t, "sec": to_seconds(t)} for t in stamps], "detected": detected,
            "note": "position du lecteur après clic sur l'onglet ; les autres moments se lisent sur la capture outputs/studio-debug/<id>-retention.png",
            "axis": axis}


def wait_for_login(page, timeout_s=300):
    if "studio.youtube.com" in page.url and "accounts.google" not in page.url:
        return
    print("→ Connecte-toi à ton compte YouTube dans la fenêtre Chrome qui vient de s'ouvrir (une seule fois).")
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        if page.url.startswith("https://studio.youtube.com") and "accounts.google" not in page.url:
            print("   Session OK."); return
        time.sleep(2)
    sys.exit("Pas connecté après 5 minutes. Relance le script.")


def read_video(page, video_id, period):
    url = f"https://studio.youtube.com/video/{video_id}/analytics/tab-interest_viewers/{PERIODS[period]}"
    page.goto(url, wait_until="domcontentloaded")
    wait_for_login(page)
    if not page.url.startswith(f"https://studio.youtube.com/video/{video_id}"):
        page.goto(url, wait_until="domcontentloaded")
    parsed, text = {"card_found": False}, ""
    for _ in range(40):  # Studio charge ses cartes en différé
        time.sleep(1)
        text = page.evaluate("() => document.body.innerText")
        parsed = parse_card(text)
        if parsed.get("card_found") and "intro_30s_pct" in parsed:
            break
        if "avg_pct_viewed" in parsed and _ > 15:  # vidéo sans carte « moments clés » (moins de 100 vues)
            break
    for tab in parsed.get("tabs", []):
        if re.match(r"^(Intro|Introduction)$", tab, re.I):
            continue
        key = "dips" if re.search(r"dip|creux|baisse", tab, re.I) else "spikes" if re.search(r"spike|pic", tab, re.I) else "top_moments"
        r = read_tab(page, tab)
        if r:
            parsed[key] = r["timestamps"]; parsed[key + "_detected"] = r["detected"]; parsed[key + "_note"] = r["note"]
    if parsed.get("dips"):
        parsed["first_dip_sec"] = min(d["sec"] for d in parsed["dips"])
    DEBUG.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(DEBUG / f"{video_id}-retention.png"), full_page=True)
    (DEBUG / f"{video_id}-retention.txt").write_text(text, encoding="utf-8")
    parsed.update({"period": period, "fetched_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")})
    return parsed


def latest_analytics_json():
    files = sorted(OUTPUTS.glob("analytics-????-??-??.json"))
    return files[-1] if files else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video_ids", nargs="*")
    ap.add_argument("--period", choices=list(PERIODS), default="lifetime")
    args = ap.parse_args()
    ids = args.video_ids
    if not ids:
        latest = latest_analytics_json()
        if not latest:
            sys.exit("Aucun ID donné et aucun outputs/analytics-<date>.json : passe des IDs.")
        ids = [v["id"] for v in json.loads(latest.read_text(encoding="utf-8"))["videos"]]
    print(f"Vidéos : {', '.join(ids)}  (période : {args.period})")
    history = json.loads(HISTORY.read_text(encoding="utf-8")) if HISTORY.exists() else {}
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            str(PROFILE_DIR), channel="chrome", headless=False, viewport={"width": 1400, "height": 1100},
            args=["--disable-blink-features=AutomationControlled"], locale="fr-FR",
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        for vid in ids:
            r = read_video(page, vid, args.period)
            history.setdefault(vid, []).append(r)
            if not r.get("card_found"):
                print(f"  {vid}: carte « moments clés » absente (moins de 100 vues ?) ; % moyen vu = {r.get('avg_pct_viewed', 'n/d')} ; "
                      f"durée moyenne = {r.get('avg_view_duration', 'n/d')} ; texte dans outputs/studio-debug/")
            else:
                dips = ", ".join(d["time"] for d in r.get("dips", [])) or "aucun"
                print(f"  {vid}: à 30 s = {r.get('intro_30s_pct', 'n/d')} % ({r.get('intro_vs_typical')}) ; "
                      f"% moyen vu = {r.get('avg_pct_viewed', 'n/d')} ; durée moyenne = {r.get('avg_view_duration', 'n/d')} ; "
                      f"onglets : {r.get('tabs')} ; creux : {dips}")
        ctx.close()
    HISTORY.parent.mkdir(parents=True, exist_ok=True)
    HISTORY.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"→ {HISTORY.relative_to(SCRIPT_DIR.parent)}")


if __name__ == "__main__":
    main()
