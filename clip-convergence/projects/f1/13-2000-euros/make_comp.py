"""Composition du clip 13 « 2 000 €, ça fait 800 € » (Formation 1 « Pourquoi investir en 2026 », Nass seul), comp_lib thème ydf.

« Moi je ne comprends pas les pourcents » : 2 000 € × 40 % = 800 € ; 15 % pour investir = 300 €, ou 150 € sur 1 000 €. Son exemple, de tête. La slide du donut 15 % sous lui.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402

c = Comp(HERE, 13, "« 2 000 €, ça fait 800 € »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf", end="outro")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 76
c.hook_html = '« JE NE COMPRENDS PAS<br><b>LES POURCENTS »</b>'
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_N+"), (E[2], "SOLO_E"), (E[3], "SOLO_E+")]
c.screen_windows = [(E[2], c.END_T)]
t_2000, t_800 = find("s2", "2000"), find("s2", "800")
t_tete = find("s3", "tête")
c.kwc("kw-2000", "2 000 € × 40 %", WHITE, t_2000 - 0.1, E[2] - 0.3, size=84, top=1190)
c.kwc("kw-800", "= 800 €", ORANGE, t_800 - 0.1, E[2] - 0.3, size=112, top=1300)
c.kwc("kw-tete", "DE TÊTE", CYAN, t_tete - 0.2, E[2] - 0.3, size=64, top=1440, anim="fade")
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_2000 - 0.08, 0.26), ("sfx-pop-2", "pop", t_800 - 0.08, 0.32),
       ("sfx-whoosh-2", "whoosh", E[2] - 0.22, 0.3), ("sfx-whoosh-3", "whoosh", E[3] - 0.22, 0.26)]
c.sfx = SFX   # la fin « outro » ajoute ses propres sons
c.build()
