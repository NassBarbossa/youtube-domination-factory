#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = ["playwright>=1.49"]
# ///
"""Lit impressions et CTR des miniatures dans YouTube Studio (ils n'existent dans aucune API).

Usage :
    uv run yt-analytics/studio_ctr.py                 # les vidéos du dernier outputs/analytics-<date>.json
    uv run yt-analytics/studio_ctr.py ID1 ID2 ...     # des vidéos précises
    uv run yt-analytics/studio_ctr.py --period default  # 28 derniers jours au lieu de « depuis la mise en ligne »

Premier lancement : une fenêtre Chrome dédiée s'ouvre (profil dans yt-analytics/.studio-profile, hors git),
tu te connectes une fois avec ton compte YouTube habituel ; la session est conservée ensuite.
Résultat : history/studio-ctr.json (une entrée datée par vidéo) + mise à jour du ctr_official
du dernier outputs/analytics-<date>.json, relu par analyze.py.
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
HISTORY = SCRIPT_DIR / "history" / "studio-ctr.json"
OUTPUTS = SCRIPT_DIR / "outputs"
DEBUG = OUTPUTS / "studio-debug"

LABELS = {  # Studio en anglais ou en français
    "impressions": ["Thumbnail impressions", "Impressions des miniatures", "Impressions"],
    "ctr": ["Thumbnail click-through rate", "Taux de clics des miniatures", "Taux de clics par impression", "Impressions click-through rate"],
}
PERIODS = {"lifetime": "period-lifetime", "default": "period-default"}


def parse_number(text):
    """'12,3 k' / '1 234' / '4,5 %' / '12.3K' → float."""
    t = text.replace(" ", "").replace("\xa0", "").replace(" ", "").replace("%", "")
    mult = 1
    m = re.match(r"^([\d.,]+)([kKmM]?)$", t)
    if not m:
        return None
    num, suf = m.groups()
    if suf.lower() == "k":
        mult = 1_000
    elif suf.lower() == "m":
        mult = 1_000_000
    num = num.replace(",", ".") if num.count(",") == 1 and num.count(".") == 0 else num.replace(",", "")
    try:
        return float(num) * mult
    except ValueError:
        return None


JS_EXTRACT = """
(labels) => {
  // Cherche chaque libellé dans la page, puis remonte jusqu'à un bloc qui contient aussi un nombre.
  const out = {};
  const all = Array.from(document.querySelectorAll('body *'));
  for (const [key, names] of Object.entries(labels)) {
    for (const el of all) {
      if (el.children.length > 3) continue;
      const t = (el.innerText || '').trim();
      if (!names.some(n => t === n || t.startsWith(n + '\\n') || t === n + ' ')) continue;
      let node = el;
      for (let i = 0; i < 6 && node; i++) {
        const txt = (node.innerText || '').trim();
        const lines = txt.split('\\n').map(s => s.trim()).filter(Boolean);
        const val = lines.find(l => l !== t && /^[\\d\\s.,\\u202f\\u00a0]+[kKmM]?\\s?%?$/.test(l));
        if (val) { out[key] = {label: t, value: val, context: lines.slice(0, 6)}; break; }
        node = node.parentElement;
      }
      if (out[key]) break;
    }
  }
  return out;
}
"""


def wait_for_login(page, timeout_s=300):
    if "studio.youtube.com" in page.url and "accounts.google" not in page.url:
        return
    print("→ Connecte-toi à ton compte YouTube dans la fenêtre Chrome qui vient de s'ouvrir (une seule fois).")
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        if page.url.startswith("https://studio.youtube.com") and "accounts.google" not in page.url:
            print("   Session OK.")
            return
        time.sleep(2)
    sys.exit("Pas connecté après 5 minutes. Relance le script.")


def read_video(page, video_id, period):
    url = f"https://studio.youtube.com/video/{video_id}/analytics/tab-reach_viewers/{PERIODS[period]}"
    page.goto(url, wait_until="domcontentloaded")
    wait_for_login(page)
    if not page.url.startswith(f"https://studio.youtube.com/video/{video_id}"):
        page.goto(url, wait_until="domcontentloaded")
    # Studio charge ses cartes en différé : on attend que « Impressions » apparaisse avec un chiffre.
    found = {}
    for _ in range(30):
        time.sleep(1)
        found = page.evaluate(JS_EXTRACT, LABELS)
        if "impressions" in found and "ctr" in found:
            break
    DEBUG.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(DEBUG / f"{video_id}.png"), full_page=False)
    (DEBUG / f"{video_id}.txt").write_text(page.evaluate("() => document.body.innerText"), encoding="utf-8")
    imp = parse_number(found.get("impressions", {}).get("value", "")) if "impressions" in found else None
    ctr = parse_number(found.get("ctr", {}).get("value", "")) if "ctr" in found else None
    return {"impressions": int(imp) if imp is not None else None, "ctr": round(ctr, 2) if ctr is not None else None,
            "period": period, "fetched_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), "raw": found}


def latest_analytics_json():
    files = sorted(OUTPUTS.glob("analytics-????-??-??.json"))
    return files[-1] if files else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video_ids", nargs="*")
    ap.add_argument("--period", choices=list(PERIODS), default="lifetime", help="lifetime = depuis la mise en ligne (défaut)")
    args = ap.parse_args()

    ids = args.video_ids
    latest = latest_analytics_json()
    if not ids:
        if not latest:
            sys.exit("Aucun ID donné et aucun outputs/analytics-<date>.json : lance analyze.py d'abord, ou passe des IDs.")
        ids = [v["id"] for v in json.loads(latest.read_text(encoding="utf-8"))["videos"]]
    print(f"Vidéos : {', '.join(ids)}  (période : {args.period})")

    history = json.loads(HISTORY.read_text(encoding="utf-8")) if HISTORY.exists() else {}
    results = {}
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            str(PROFILE_DIR), channel="chrome", headless=False, viewport={"width": 1400, "height": 1000},
            args=["--disable-blink-features=AutomationControlled"], locale="fr-FR",
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        for vid in ids:
            r = read_video(page, vid, args.period)
            results[vid] = r
            ok = r["impressions"] is not None and r["ctr"] is not None
            print(f"  {vid} : impressions {r['impressions']}  CTR {r['ctr']}%" if ok else f"  {vid} : CTR introuvable (voir outputs/studio-debug/{vid}.png et .txt)")
            if ok:
                history.setdefault(vid, []).append({k: r[k] for k in ("fetched_at", "period", "impressions", "ctr")})
        ctx.close()

    HISTORY.parent.mkdir(exist_ok=True)
    HISTORY.write_text(json.dumps(history, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Historique : {HISTORY}")

    if latest:
        data = json.loads(latest.read_text(encoding="utf-8"))
        n = 0
        for v in data["videos"]:
            r = results.get(v["id"])
            if r and r["impressions"] is not None and r["ctr"] is not None:
                v["ctr_official"] = {"impressions": r["impressions"], "ctr": r["ctr"], "source": "YouTube Studio", "period": r["period"]}
                n += 1
        latest.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{n} CTR écrit(s) dans {latest.name}. Régénère le rapport : python3 yt-analytics/analyze.py --from-json [--notes <notes>]")


if __name__ == "__main__":
    main()
