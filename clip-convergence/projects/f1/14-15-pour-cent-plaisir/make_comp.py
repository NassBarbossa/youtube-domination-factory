"""Composition du clip 14 « 15 % pour le plaisir » (Formation 1 « Pourquoi investir en 2026 », Nass seul), comp_lib thème ydf.

« 100 € par mois, je ne peux pas » : ça ne représente que 15 %. Et 15 % pour le plaisir, sinon vous allez craquer.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402

c = Comp(HERE, 14, "« 15 % pour le plaisir »", cta="Les 3 vidéos sont sur la chaîne", theme="ydf")
seams, find, S = c.seams, c.find, c.STATES
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 80
c.hook_html = '« 100 € PAR MOIS,<br><b>JE NE PEUX PAS »</b>'
c.moves = [(seams[0], "SOLO_N"), (seams[1], "SOLO_N+"), (seams[2], "SOLO_N")]
t_15, t_plaisir, t_craquer = find("s2", "15"), find("s3", "plaisir"), find("s4", "craquer")
c.kwc("kw-15", "ÇA NE REPRÉSENTE<br>QUE 15 %", CYAN, t_15 - 0.8, seams[2] - 0.3, size=76)
c.kwc("kw-plaisir", "15 %<br>POUR LE PLAISIR", ORANGE, t_plaisir - 0.5, seams[3] - 0.3, size=84)
c.kwc("kw-chute", "SINON VOUS ALLEZ<br>CRAQUER", RED_Y, t_craquer - 0.4, c.END_T + 0.45, size=84, anim="rise")
c.cap_cuts = [("s4", t_craquer - 0.3, 1e9)]; c.cap_end_before = [t_craquer - 0.2]
SFX = [("sfx-whoosh-1", "whoosh-short", seams[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_15 - 0.78, 0.26), ("sfx-whoosh-2", "whoosh", seams[2] - 0.22, 0.26),
       ("sfx-pop-2", "pop", t_plaisir - 0.48, 0.28), ("sfx-pop-3", "pop", t_craquer - 0.38, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
