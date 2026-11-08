"""Composition du clip 27 « C'est or contre dollar » (Convergence EP.01, Sadek), comp_lib v6, écran seul.

L'or se cote contre le dollar : DXY qui monte, dollar fort, or en baisse ; la décorrélation (les deux montent ensemble)
annonce un retournement très violent. Coupé : « dans leur politique, c'est l'intérêt de le faire monter » (digression) et
« il va falloir se positionner à l'achat sur l'or » (appel à acheter, hors cadre) ; la conclusion « positive pour l'actif »
reste. Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, GOLD_TXT, INK, RED, screen_only  # noqa: E402

c = Comp(HERE, 27, "« C'est or contre dollar »")
seams, find = c.seams, c.find
SCR = screen_only(1000, 544)
c.STATES["H"] = SCR
c.screen_state = "H"
c.screen_windows = [(0, c.END_T)]
c.punch([seams[2], seams[4], seams[5]])
c.hook_html = 'C\'EST OR<br><b class="or">CONTRE DOLLAR</b>'
c.hook_font = 104
TOP = SCR["kw_top"]

t_dxy = find("s2", "dxy")
t_dollar = find("s3", "dollar")
t_baisse = find("s3", "baisse")
t_decor = find("s4", "décorrélation")
t_retour = find("s6", "retournement")
t_dxy2 = find("s7", "dxy")
t_or2 = find("s7", "or")
t_positive = find("s8", "positive")

c.kw("kw-dxy", "LE DXY MONTE", f"left: 0; right: 0; top: {TOP + 95}px; text-align: center; color: {INK}; font-size: 104px;",
     t_dxy - 0.1, t_dollar - 0.4)
c.kw("kw-dollar", "DOLLAR FORT", f"left: 0; width: 540px; top: {TOP + 105}px; text-align: center; color: {INK}; font-size: 80px;",
     t_dollar - 0.1, seams[2] - 0.3)
c.kw("kw-baisse", "OR EN BAISSE", f"left: 540px; width: 540px; top: {TOP + 105}px; text-align: center; color: {RED}; font-size: 80px;",
     t_baisse - 0.5, seams[2] - 0.3)
c.kw("kw-decor", "DÉCORRÉLATION", f"left: 0; right: 0; top: {TOP + 100}px; text-align: center; color: {GOLD_TXT}; font-size: 96px; letter-spacing: 0.04em;",
     t_decor - 0.1, seams[4] - 0.3)
c.kw("kw-retour", "RETOURNEMENT<br>TRÈS VIOLENT", f"left: 0; right: 0; top: {TOP + 50}px; text-align: center; color: {RED}; font-size: 92px; line-height: 1;",
     t_retour - 0.1, seams[5] - 0.3)
c.kw("kw-both", "DXY QUI MONTE<br>ET OR QUI MONTE", f"left: 0; right: 0; top: {TOP + 50}px; text-align: center; color: {INK}; font-size: 84px; line-height: 1;",
     t_dxy2 - 0.2, seams[6] - 0.3, anim="rise")
c.kw("kw-chute", "POSITIVE<br>POUR L'ACTIF", f"left: 0; right: 0; top: {TOP + 50}px; text-align: center; color: {GOLD_TXT}; font-size: 96px; line-height: 1;",
     t_positive - 0.1, c.END_T + 0.05)
c.cap_cuts = [("s8", t_positive - 0.05, 1e9)]
c.cap_end_before = [t_positive]
c.sfx = [
    ("sfx-whoosh-1", "whoosh-short", seams[0] - 0.20, 0.30),
    ("sfx-pop-1", "pop", t_dollar - 0.08, 0.26), ("sfx-pop-2", "pop", t_baisse - 0.48, 0.26),
    ("sfx-whoosh-2", "whoosh", seams[4] - 0.22, 0.26),
    ("sfx-pop-3", "pop", t_retour - 0.08, 0.30),
    ("sfx-pop-4", "pop", t_positive - 0.08, 0.28),
    ("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40),
]
c.build()
print(f"dxy {t_dxy} | dollar {t_dollar} baisse {t_baisse} | décor {t_decor} | retour {t_retour} | both {t_dxy2} | chute {t_positive}")
