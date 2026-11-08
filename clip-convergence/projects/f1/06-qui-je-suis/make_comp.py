"""Composition du clip 6 « Qui je suis pour vous dire ça ? » (Formation 1 « Pourquoi investir en 2026 », Nass seul), comp_lib thème ydf.

Dix ans d'investissement, premiers bitcoins en 2017 (3 000 $ à l'époque, ses mots), six ans sans emploi, 300 personnes formées. Les slides « 2017 » et « 300+ » sous lui.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402

c = Comp(HERE, 6, "« Qui je suis pour vous dire ça ? »", cta="Les 3 vidéos sont sur la chaîne", theme="ydf")
seams, find, S = c.seams, c.find, c.STATES
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = 'QUI JE SUIS<br><b>POUR VOUS DIRE ÇA ?</b>'
c.moves = [(seams[0], "SOLO_E"), (seams[1], "SOLO_N"), (seams[2], "SOLO_E+")]
c.screen_windows = [(seams[0], seams[1]), (seams[2], c.END_T)]
t_10 = find("s1", "10")
t_vis = find("s3", "vis")
c.kwc("kw-10", "10 ANS<br>INVESTISSEUR", ORANGE, t_10 - 0.1, seams[0] - 0.3, size=88, top=1080)
c.kwc("kw-vis", "JE VIS DE MES<br>INVESTISSEMENTS", CYAN, t_vis - 0.3, seams[2] - 0.3, size=76, anim="rise")
SFX = [("sfx-pop-1", "pop", t_10 - 0.08, 0.26), ("sfx-whoosh-1", "whoosh", seams[0] - 0.22, 0.3), ("sfx-whoosh-2", "whoosh-short", seams[1] - 0.2, 0.3),
       ("sfx-pop-2", "pop", t_vis - 0.28, 0.26), ("sfx-whoosh-3", "whoosh", seams[2] - 0.22, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
