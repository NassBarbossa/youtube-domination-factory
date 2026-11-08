"""Composition du clip 56 « Un range bien dégoûtant » (Convergence EP.03, replay YouTube 720p), comp_lib v6.

Nass sur le graphique : depuis le 28 septembre, rien ne s'est passé, on est dans un range bien dégoûtant ; un peu de résilience acheteuse, on le casse peut-être aujourd'hui, mais « on n'est pas sorti de l'auberge ». Son écran TradingView sous lui.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, INK, GREEN, GOLD, GOLD_TXT, GREY, RED, screen_only, solo, solo_screen, sym, sym_screen  # noqa: E402

c = Comp(HERE, 56, "« Un range bien dégoûtant »", cta="Épisode 3 complet sur la chaîne")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["E"] = sym_screen(480, 520, 900, 506)
S["E+"] = sym_screen(500, 520, 900, 506)
S["SOLO_E"] = solo_screen(860, 900, 506)
S["SOLO_E+"] = solo_screen(880, 900, 506)
c.hook_font = 92
c.hook_html = 'UN RANGE<br><b>BIEN DÉGOÛTANT</b>'
SCR = screen_only(900, 506, kw_h=915)   # même boîte d'écran que SOLO_E (sy 1141) : Nass est hors de sa caméra sur s1-s2
S["H"] = SCR
c.screen_state = "H"
TOP = SCR["kw_top"]
c.fix = {("s2", "rennes"): "range"}
t_rien, t_auberge = find("s2", "grand"), find("s3", "auberge")
c.hook_fade = E[1] - 0.3
c.moves = [(E[1], "SOLO_E"), (t_auberge - 1.1, "H")]
c.screen_windows = [(0, c.END_T)]
c.punch([seams[0]])
c.kwc("kw-rien", "PAS GRAND-CHOSE", GREY, t_rien - 0.3, E[1] - 0.3, size=72, top=TOP + 700)
c.kwc("kw-chute", "PAS SORTI<br>DE L'AUBERGE", GREEN, t_auberge - 0.5, c.END_T + 0.45, size=84, top=TOP + 330, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh", E[1] - 0.22, 0.3), ("sfx-whoosh-2", "whoosh", t_auberge - 1.32, 0.26), ("sfx-pop-1", "pop", t_auberge - 0.48, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
