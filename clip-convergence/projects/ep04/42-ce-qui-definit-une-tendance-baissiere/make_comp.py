"""Composition du clip 42 « Ce qui définit une tendance baissière » (Convergence EP.04, Nass seul), comp_lib v6, monologue.

Sur le BTC : un changement de structure potentiel, « sommet là, creux là, sommet là », début de tendance baissière en court terme. Et le rappel de la définition : des sommets de plus en plus bas et des points bas de plus en plus bas. Son écran TradingView sous lui quand il pointe.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, INK, GREEN, GOLD, GOLD_TXT, GREY, RED, solo, solo_screen  # noqa: E402

c = Comp(HERE, 42, "« Ce qui définit une tendance baissière »", cta="Épisode 4 complet sur la chaîne")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 72
c.hook_html = "UNE TENDANCE BAISSIÈRE,<br><b>C'EST QUOI ?</b>"
c.moves = [(E[0], "SOLO_E"), (E[1], "SOLO_N+")]
c.screen_windows = [(E[0], E[1])]
t_sommets, t_points = find("s3", "sommets"), find("s3", "points")
c.kwc("kw-sommets", "DES SOMMETS<br>DE PLUS EN PLUS BAS", INK, t_sommets - 0.1, t_points - 0.7, size=66)
c.kwc("kw-chute", "DES CREUX<br>DE PLUS EN PLUS BAS", GREEN, t_points - 0.3, c.END_T + 0.45, size=66, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh", E[0] - 0.22, 0.3), ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26), ("sfx-pop-1", "pop", t_sommets - 0.08, 0.26), ("sfx-pop-2", "pop", t_points - 0.28, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
