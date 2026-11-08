"""Composition du clip 34 « Le fameux 10-10 » (Convergence EP.01, Nass), comp_lib v6.

Accroche « LE FAMEUX / 10-10 », Nass seul : 10-10 en grand et « beaucoup de comptes ont sauté », puis son écran (le graphique
BTC : la correction, le range) pendant qu'il le montre, puis la chute « MÊME MOI, J'ÉTAIS BEARISH ». « Moins 50 % » et
« 200 jours » restent dans la voix et les sous-titres : non vérifiés, pas en mot clé. Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, INK, RED  # noqa: E402

c = Comp(HERE, 34, "« Le fameux 10-10 »")
seams, find = c.seams, c.find
S = c.STATES
S["SOLO_E+"] = dict(S["SOLO_E"], nass=(540, S["SOLO_E"]["nass"][1] + 10, 880))
c.moves = [
    (seams[0], "SOLO_N"),    # s2 : « Le fameux 10-10 »
    (seams[1], "SOLO_E"),    # s3 : « Énorme correction sur le BTC » : l'écran
    (seams[2], "SOLO_E+"),   # s4 : « cette phase de range »
    (seams[3], "SOLO_E"),    # s5 : « quasiment 200 jours »
    (seams[4], "SOLO_N+"),   # s6 : « même moi, j'étais plutôt bearish »
]
c.screen_windows = [(seams[1], seams[4])]
c.hook_html = "LE FAMEUX<br><b>10-10</b>"
c.fix = {("s6", "bearish"): "bearish"}

t_1010 = find("s2", "10")
t_comptes = find("s2", "comptes")
t_meme = find("s6", "même")

c.kw("kw-1010", "10-10", f"left: 0; right: 0; top: 1176px; text-align: center; color: {INK}; font-size: 170px;", t_1010, seams[1] - 0.3)
c.kw("kw-comptes", "BEAUCOUP DE COMPTES ONT SAUTÉ", f"left: 0; right: 0; top: 1368px; text-align: center; color: {RED}; font-size: 56px;",
     t_comptes - 0.4, seams[1] - 0.3, anim="rise")
c.kw("kw-chute", "MÊME MOI,<br>J'ÉTAIS BEARISH", f"left: 0; right: 0; top: 1240px; text-align: center; color: {INK}; font-size: 96px; line-height: 1;",
     t_meme, c.END_T + 0.05)
c.cap_cuts = [("s6", t_meme, 1e9)]
c.cap_end_before = [t_meme]

c.sfx = [
    ("sfx-whoosh-1", "whoosh-short", seams[0] - 0.20, 0.34),
    ("sfx-pop-1", "pop", t_1010 + 0.02, 0.30),
    ("sfx-whoosh-2", "whoosh", seams[1] - 0.22, 0.30),
    ("sfx-whoosh-3", "whoosh", seams[4] - 0.22, 0.26),
    ("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40),
]
c.build()
print(f"10-10 {t_1010} | écran {seams[1]}-{seams[4]} | chute {t_meme}")
