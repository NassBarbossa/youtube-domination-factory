"""Composition du clip 14 « Il faut survivre » (J'abandonne mon challenge crypto, Nass seul), comp_lib thème ydf.

Avec l'expérience, il est plus fort dans un marché facile que dans un marché difficile. Alors aujourd'hui, « on est dans une phase où il faut survivre, pour pouvoir être performant quand on redeviendra en mode easy ».
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 14, "« Il faut survivre »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = 'IL FAUT<br><b>SURVIVRE</b>'
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_N+")]
t_facile, t_difficile, t_performant = find("s2", "facile"), find("s2", "difficile"), find("s3", "performant")
c.kwc("kw-facile", "FORT DANS UN<br>MARCHÉ FACILE", CYAN, t_facile - 0.3, t_difficile - 0.9, size=68)
c.kwc("kw-difficile", "PAS DANS UN<br>MARCHÉ DIFFICILE", MUTED, t_difficile - 0.2, E[1] - 0.3, size=66)
c.kwc("kw-chute", "SURVIVRE, POUR ÊTRE<br>PERFORMANT APRÈS", ORANGE, t_performant - 0.8, c.END_T + 0.45, size=62, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_facile - 0.28, 0.26), ("sfx-pop-2", "pop", t_difficile - 0.18, 0.26),
       ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26), ("sfx-pop-3", "pop", t_performant - 0.78, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
