"""Composition du clip 11 « Déménage » (Formation 1 « Pourquoi investir en 2026 », Nass seul), comp_lib thème ydf.

« Je bosse à Paris, je ne suis pas assez payé » : déménage. 40 % max pour ne pas être endetté par les crédits.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402

c = Comp(HERE, 11, "« Déménage »", cta="Les 3 vidéos sont sur la chaîne", theme="ydf")
seams, find, S = c.seams, c.find, c.STATES
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 80
c.hook_html = '« OUAIS MAIS MOI,<br><b>JE BOSSE À PARIS »</b>'
c.moves = [(seams[0], "SOLO_N"), (seams[1], "SOLO_N+"), (seams[2], "SOLO_N")]
t_dem, t_40, t_credits = find("s3", "Déménage"), find("s4", "40"), find("s4", "crédits")
c.kwc("kw-dem", "DÉMÉNAGE.", ORANGE, t_dem - 0.05, seams[3] - 0.3, size=120, top=1250)
c.kwc("kw-40", "40 % MAX", WHITE, t_40 - 0.1, c.END_T + 0.45, size=92, top=1190)
c.kwc("kw-credits", "PAS ENDETTÉ<br>PAR LES CRÉDITS", CYAN, t_credits - 0.6, c.END_T + 0.45, size=64, top=1310, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh-short", seams[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_dem - 0.03, 0.34), ("sfx-whoosh-2", "whoosh", seams[2] - 0.22, 0.26),
       ("sfx-pop-2", "pop", t_40 - 0.08, 0.28)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
