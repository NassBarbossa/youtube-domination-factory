"""Convergence — cours en direct pour le bandeau OBS.

Toutes les 60 secondes, récupère les cours sur Yahoo Finance et écrit obs/cours.js,
que les écrans OBS relisent chaque minute.
Lancer avant le live (double-clic sur « Lancer les cours en direct.bat ») et laisser la fenêtre ouverte.
"""
import json, os, time, urllib.parse, urllib.request
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "cours.js")
INTERVAL = 60  # secondes

# Nom affiché, symbole Yahoo, format du prix
ACTIFS = [
    ("OR",       "GC=F",     "{:,.0f} $"),
    ("ARGENT",   "SI=F",     "{:,.2f} $"),
    ("S&P 500",  "^GSPC",    "{:,.0f}"),
    ("CAC 40",   "^FCHI",    "{:,.0f}"),
    ("EUR/USD",  "EURUSD=X", "{:,.4f}"),
    ("PÉTROLE",  "CL=F",     "{:,.2f} $"),
    ("BTC",      "BTC-USD",  "{:,.0f} $"),
    ("ETH",      "ETH-USD",  "{:,.0f} $"),
    ("SOL",      "SOL-USD",  "{:,.2f} $"),
]
# Actifs du panneau « Cette semaine » (variation sur 5 séances)
SEMAINE = ["OR", "S&P 500", "BTC", "SOL"]

def fr(fmt, v):
    """Format français : espace pour les milliers, virgule pour les décimales."""
    s = fmt.format(v).replace(",", " ").replace(".", ",")
    return s.replace(" ", " ")

def pct(a, b):
    v = (a / b - 1) * 100
    return ("+" if v >= 0 else "−") + f"{abs(v):.1f}".replace(".", ",") + " %"

def quote(symbol):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(symbol)}?range=5d&interval=1d"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    r = json.load(urllib.request.urlopen(req, timeout=10))["chart"]["result"][0]
    m = r["meta"]
    closes = [c for c in r["indicators"]["quote"][0]["close"] if c]
    prix = m["regularMarketPrice"]
    veille = closes[-2] if len(closes) > 1 else m.get("chartPreviousClose", prix)
    semaine = m.get("chartPreviousClose") or closes[0]
    return prix, veille, semaine

def tour():
    ticker, semaine = [], []
    for nom, sym, fmt in ACTIFS:
        try:
            prix, veille, base = quote(sym)
        except Exception as e:
            print(f"  ! {nom} indisponible ({e.__class__.__name__})")
            continue
        ticker.append([nom, fr(fmt, prix), pct(prix, veille)])
        if nom in SEMAINE:
            semaine.append([nom, pct(prix, base)])
    semaine.sort(key=lambda x: SEMAINE.index(x[0]))
    data = {"maj": datetime.now().strftime("%H:%M"), "ticker": ticker, "semaine": semaine}
    tmp = OUT + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write("window.COURS_LIVE = " + json.dumps(data, ensure_ascii=False) + ";\n")
    os.replace(tmp, OUT)
    return data

if __name__ == "__main__":
    print("Convergence — cours en direct (Ctrl+C pour arrêter)")
    while True:
        try:
            d = tour()
            print(f"[{d['maj']}] {len(d['ticker'])} cours à jour")
        except Exception as e:
            print("Erreur :", e)
        time.sleep(INTERVAL)
