#!/usr/bin/env python3
"""Génère bitcoin-piege-baissier-visual.html (version basique, sans animations) à partir des bougies Binance.
Usage : python3 yt-script/outputs/bitcoin-piege-baissier-build.py  (depuis la racine du repo)"""
import json, datetime as dt
from pathlib import Path
OUT = Path(__file__).resolve().parent; REPO = OUT.parent.parent; D = dt.date
def load(sym):
    return [(dt.datetime.fromtimestamp(k[0]/1000, dt.UTC).date(), float(k[2]), float(k[3]), float(k[4])) for k in json.load(open(OUT/f"bitcoin-piege-baissier-{sym}-1d-binance.json"))]
BTC, ETH, SOL = load("btc"), load("ETH"), load("SOL")
def sma200(rows):
    c = [r[3] for r in rows]; return {rows[i][0]: sum(c[i-199:i+1])/200 for i in range(199, len(rows))}
def fmt(v, unit="$"): return f"{v:,.0f}".replace(",", " ") + f" {unit}"
def chart(rows, a, b, labels, w=1100, h=440, line=None, sma=None, unit="$"):
    """labels : (date, valeur, texte[, 'up'|'down'])"""
    seg = [r for r in rows if a <= r[0] <= b]; xs = [r[0] for r in seg]; ys = [r[3] for r in seg]
    lo = min(min(r[2] for r in seg), *(l[1] for l in labels)) * 0.95; hi = max(max(r[1] for r in seg), *(l[1] for l in labels)) * 1.05
    if line: lo, hi = min(lo, line[0]*0.97), max(hi, line[0]*1.03)
    pl, pr, pt, pb = 90, 40, 30, 60
    X = lambda d: pl + (d - a).days / max(1, (b - a).days) * (w - pl - pr); Y = lambda v: pt + (hi - v) / (hi - lo) * (h - pt - pb)
    s = [f'<svg viewBox="0 0 {w} {h}" class="pb-chart" xmlns="http://www.w3.org/2000/svg">']
    for k in range(5):
        v = lo + (hi - lo) * k / 4; y = Y(v)
        s.append(f'<line x1="{pl}" y1="{y:.1f}" x2="{w-pr}" y2="{y:.1f}" stroke="rgba(244,239,231,0.12)"/><text x="{pl-10}" y="{y+5:.1f}" text-anchor="end" class="pb-ax">{fmt(v, unit)}</text>')
    m = a.replace(day=1)
    while m <= b:
        if m >= a: s.append(f'<text x="{X(m):.1f}" y="{h-pb+22}" text-anchor="middle" class="pb-ax">{m.strftime("%b %y")}</text>')
        m = (m.replace(day=28) + dt.timedelta(days=4)).replace(day=1)
    if sma:
        s.append('<polyline points="' + " ".join(f"{X(d):.1f},{Y(sma[d]):.1f}" for d in xs if d in sma) + '" fill="none" stroke="#648596" stroke-width="3" stroke-dasharray="8 6"/>')
        s.append(f'<text x="{w-pr}" y="{Y(sma[xs[-1]])-10:.1f}" text-anchor="end" class="pb-ax" fill="#648596">MM200</text>')
    if line:
        v, txt = line; s.append(f'<line x1="{pl}" y1="{Y(v):.1f}" x2="{w-pr}" y2="{Y(v):.1f}" stroke="#DBB17F" stroke-width="2" stroke-dasharray="4 6"/><text x="{pl+8}" y="{Y(v)-8:.1f}" class="pb-ax" fill="#DBB17F">{txt}</text>')
    s.append('<polyline points="' + " ".join(f"{X(d):.1f},{Y(v):.1f}" for d, v in zip(xs, ys)) + '" fill="none" stroke="#F4EFE7" stroke-width="2.5"/>')
    for l in labels:
        d, v, txt = l[:3]; pos = l[3] if len(l) > 3 else ("up" if v > (lo+hi)/2 else "down")
        x, y = X(d), Y(v); ty = y - 18 if pos == "up" else y + 30
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="#DBB17F" stroke="#0B0B0B" stroke-width="2"/><text x="{x:.1f}" y="{ty:.1f}" text-anchor="middle" class="pb-lab">{txt}</text><text x="{x:.1f}" y="{ty+16:.1f}" text-anchor="middle" class="pb-ax">{d.strftime("%d/%m/%y")}</text>')
    s.append("</svg>"); return "\n".join(s)
def mini(rows, sma, name, a=D(2026,6,1), b=D(2026,10,14)):
    seg = [r for r in rows if a <= r[0] <= b]; xs = [r[0] for r in seg]; ys = [r[3] for r in seg]
    lo, hi = min(ys + [sma[d] for d in xs]) * 0.95, max(ys + [sma[d] for d in xs]) * 1.05; w, h = 340, 220
    X = lambda d: 10 + (d - a).days / (b - a).days * (w - 20); Y = lambda v: 10 + (hi - v) / (hi - lo) * (h - 40); x19 = X(D(2026,8,19))
    return (f'<div class="pb-mini"><svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg"><line x1="{x19:.1f}" y1="0" x2="{x19:.1f}" y2="{h-30}" stroke="#DBB17F" stroke-width="2" stroke-dasharray="4 4"/>'
            '<polyline points="' + " ".join(f"{X(d):.1f},{Y(sma[d]):.1f}" for d in xs) + '" fill="none" stroke="#648596" stroke-width="2.5" stroke-dasharray="6 5"/>'
            '<polyline points="' + " ".join(f"{X(d):.1f},{Y(v):.1f}" for d, v in zip(xs, ys)) + f'" fill="none" stroke="#F4EFE7" stroke-width="2.5"/><text x="{x19:.1f}" y="{h-10}" text-anchor="middle" class="pb-ax" fill="#DBB17F">19 août 2026</text></svg><div class="pb-mini-t">{name}</div></div>')
sB, sE, sS = sma200(BTC), sma200(ETH), sma200(SOL)
S = []
def sl(html, cls=""): S.append((html, cls))
sl(f'<h2>Le 19 août 2026, les trois majors repassent au-dessus de leur moyenne 200 jours</h2><div class="pb-minis">{mini(BTC,sB,"Bitcoin")}{mini(ETH,sE,"Ethereum")}{mini(SOL,sS,"Solana")}</div><p class="pb-src">Clôtures journalières Binance · ligne pointillée bleue = MM200</p>')
sl('<p class="key-statement">« Pour moi, la baisse est terminée. »</p>')
sl('<div class="divider divider-sand"></div><h2>Pourquoi je regarde les majors avant tout</h2><p>Ce sont eux qui décident si on peut acheter on-chain</p>', "transition")
sl('''<h2>Du record au creux, 2025-2026</h2><div class="pb-bars">
<div class="pb-bar"><img src="logos/bitcoin.png"><div class="pb-bar-fill" style="height:54%"><span>−54 %</span></div><b>Bitcoin</b><small>126 200 → 57 800 $</small></div>
<div class="pb-bar"><img src="logos/eth.png"><div class="pb-bar-fill" style="height:70%"><span>−70 %</span></div><b>Ethereum</b><small>4 957 → 1 506 $</small></div>
<div class="pb-bar"><img src="logos/sol.png"><div class="pb-bar-fill" style="height:76%"><span>−76 %</span></div><b>Solana</b><small>254 → 60 $</small></div></div>
<p class="pb-src">Binance, record → creux (oct. 2025 → juin / juillet 2026) · et les petits coins on-chain, encore pire</p>''')
sl('<div class="pb-light"><span class="pb-red"></span><span></span><span></span></div><p class="key-statement">Majors en baisse = pas d\'achat on-chain.</p>')
sl(f'''<h2>Bitcoin, du record à aujourd'hui : la structure baissière est cassée</h2>
{chart(BTC, D(2025,9,20), D(2026,10,14), [(D(2025,10,6),126200,"126 200 $ · record"),(D(2026,1,14),97924,"97 924 $","up"),(D(2026,5,6),82850,"82 850 $","up"),(D(2026,2,6),60000,"60 000 $","up"),(D(2026,7,1),57800,"57 800 $ · creux","down"),(D(2026,8,1),62275,"62 275 $ · creux plus haut","up"),(D(2026,9,21),86620,"86 620 $ · cassure","up"),(D(2026,10,8),80394,"80 394 $","down")], line=(82850,"82 850 $ · dernier sommet baissier (6 mai)"), sma=sB)}
<p class="pb-src">Binance BTC/USDT, clôtures journalières jusqu'au 14 octobre 2026 · sommets et creux de plus en plus bas jusqu'au 1er juillet, puis creux plus hauts et cassure le 21 septembre</p>''')
sl('<div class="pb-def"><div class="pb-term">Structure baissière</div><p>Des sommets de plus en plus bas et des creux de plus en plus bas. Tant que ça dure, le marché baisse.</p><div class="pb-stairs pb-down"><i></i><i></i><i></i><i></i></div></div>')
sl('<div class="pb-def"><div class="pb-term">Changement de structure</div><p>Un creux qui reste plus haut que le précédent, puis un sommet qui dépasse le précédent. Le marché arrête de baisser.</p><div class="pb-stairs pb-up"><i></i><i></i><i></i><i></i></div></div>')
sl('<div class="divider divider-sand"></div><h2>Ce qui a cassé, et quand</h2><p>Les dates, sur les trois majors</p>', "transition")
sl(f'''<h2>Bitcoin depuis le creux : creux plus hauts, puis cassure</h2>
{chart(BTC, D(2026,6,1), D(2026,10,14), [(D(2026,7,1),57800,"57 800 $ · creux","down"),(D(2026,8,1),62275,"62 275 $ · creux plus haut","up"),(D(2026,9,3),82300,"82 300 $ · sommet plus haut","down"),(D(2026,9,15),74968,"74 968 $ · creux plus haut","down"),(D(2026,9,21),86620,"86 620 $ · cassure","up"),(D(2026,10,8),80394,"80 394 $","down")], line=(82850,"82 850 $ · sommet du 6 mai"), sma=sB)}
<p class="pb-src">Binance BTC/USDT · clôture du 21 septembre 2026 au-dessus du sommet de mai : structure cassée</p>''')
sl(f'''<h2>Ethereum : même film, cassure le 21 août</h2>
{chart(ETH, D(2026,6,1), D(2026,10,14), [(D(2026,6,6),1506,"1 506 $ · creux","up"),(D(2026,8,21),2516,"2 516 $ · cassure","up"),(D(2026,9,21),2807,"2 807 $","up")], line=(2465,"2 465 $ · sommet du 17 avril"), sma=sE)}
<p class="pb-src">Binance ETH/USDT, clôtures journalières</p>''')
sl(f'''<h2>Solana : cassure le 24 août, creux plus hauts derrière</h2>
{chart(SOL, D(2026,6,1), D(2026,10,14), [(D(2026,6,6),60,"60 $ · creux","up"),(D(2026,8,1),71,"71 $ · creux plus haut","down"),(D(2026,8,24),99,"99 $ · cassure","up"),(D(2026,9,15),96,"96 $ · creux plus haut","down"),(D(2026,9,27),125,"125 $","up")], line=(98,"98 $ · sommet du 11 mai"), sma=sS)}
<p class="pb-src">Binance SOL/USDT, clôtures journalières</p>''')
sl('<div class="stat" style="color:var(--sand)">19 août 2026</div><p>Le jour où Bitcoin, Ethereum et Solana repassent durablement au-dessus de leur moyenne 200 jours.<br>Bitcoin : 289 jours en dessous avant ça.</p><div class="pb-logos"><img src="logos/bitcoin.png"><img src="logos/eth.png"><img src="logos/sol.png"></div><p class="pb-src">Binance, clôtures journalières</p>')
sl('<div class="divider divider-sand"></div><h2>Pourquoi ce n\'est pas un rebond-piège</h2><p>2018 et 2022 ont essayé, ça n\'a pas tenu</p>', "transition")
sl('''<h2>Les rebonds qui n'ont pas tenu, et celui-ci</h2><div class="pb-three">
<div class="card pb-grey"><h3>2018</h3><p>Rebond +67 %<br>6 000 → 10 020 $</p><p class="pb-no">sans dépasser 11 786 $</p><p><b>−84 % au final</b></p></div>
<div class="card pb-grey"><h3>2022</h3><p>Rebond +43 %<br>17 622 → 25 211 $</p><p class="pb-no">sans dépasser 32 399 $</p><p><b>−78 % au final</b></p></div>
<div class="card pb-gold"><h3>2026</h3><p>Rebond +44 %<br>57 800 → 83 420 $</p><p class="pb-yes">cassure de 82 850 $ le 21 sept.<br>creux plus hauts derrière</p><p><b>prochain niveau : 97 924 $</b></p></div></div>
<p class="pb-src">Binance, bougies hebdomadaires (2018, 2022) et journalières (2026)</p>''')
sl('''<h2>Ce qui me ferait changer d'avis</h2><div class="pb-three">
<div class="card" style="background:var(--sand-light)"><h3>Sous 74 968 $</h3><p>en clôture : je redeviens prudent</p></div>
<div class="card" style="background:var(--sand)"><h3>Sous 62 275 $</h3><p>en clôture : la thèse est morte</p></div>
<div class="card pb-grey"><h3>Sous la MM200</h3><p>les majors qui repassent dessous</p></div></div><p class="pb-src">[NASS] niveaux à confirmer</p>''')
sl('''<h2>Ce que ça change pour mes achats on-chain</h2><div class="two-col pb-wide">
<div class="card"><div class="pb-light pb-small"><span class="pb-red"></span><span></span><span></span></div><h3>Feu rouge</h3><p>Majors en structure baissière</p><p>Zéro achat on-chain. Le DCA mensuel continue, c'est tout.</p></div>
<div class="card"><div class="pb-light pb-small"><span></span><span></span><span class="pb-green"></span></div><h3>Feu vert</h3><p>Majors en structure haussière</p><p>Achats on-chain rares, sur de vraies opportunités, taille fixée d'avance. [NASS]</p></div></div>''')
sl('<div class="cta-box"><h2 style="margin-bottom:0.5em">La méthode complète, en trois vidéos</h2><p style="font-size:clamp(1rem,1.5vw,1.3rem)">Formation offerte : gérer son argent · investir chaque mois · acheter on-chain avant les autres</p><p style="margin-top:.6em;font-weight:600">youtube.com/playlist?list=PLH8HsDRAJ7R8</p></div><p class="disclaimer">Pas un conseil en investissement.</p>')
TOTAL = len(S)
tpl = (REPO/"yt-script/references/slide-template.html").read_text(encoding="utf-8")
head = tpl[:tpl.index("<!-- ====")].replace("{{TITLE}}", "Bitcoin et les majors : la baisse est terminée").replace(".reveal {", ".reveal-off {").replace(".visible .reveal", ".visible .reveal-off")
extra = (OUT/"bitcoin-piege-baissier-styles.css").read_text(encoding="utf-8")
body = "\n".join(f'<section class="slide center {cls}">\n<span class="slide-num">{i:02d} / {TOTAL}</span>\n<div class="slide-content center">\n{html}\n</div>\n</section>' for i, (html, cls) in enumerate(S, 1))
nav = tpl[tpl.index("<!-- ================================================================\n     NAVIGATION"):]
(OUT/"bitcoin-piege-baissier-visual.html").write_text(head + "<style>\n" + extra + "\n</style>\n<div class=\"watermark\">Nass Riviera</div>\n" + body + "\n" + nav, encoding="utf-8")
print("deck :", TOTAL, "slides")
