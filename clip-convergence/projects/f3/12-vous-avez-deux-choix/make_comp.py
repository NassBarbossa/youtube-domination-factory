"""Composition du clip 12 « Vous avez deux choix » (Formation 3 « L'investissement on-chain », Nass seul), comp_lib thème ydf.

La fin de la formation offerte : vous avez deux choix. Choix 1, pas beaucoup de temps ni l'envie de prendre des risques : vous investissez tous les mois. « C'est mon cadeau à la France, mais c'est OK. »
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 12, "« Vous avez deux choix »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = 'VOUS AVEZ<br><b>DEUX CHOIX</b>'
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_N+")]
t_choix1, t_mois, t_ok = find("s2", "Choix"), find("s2", "tous"), find("s3", "OK")
c.kwc("kw-choix1", "CHOIX 1", CYAN, t_choix1 - 0.2, t_mois - 0.9, size=100, top=1270)
c.kwc("kw-mois", "INVESTIR<br>TOUS LES MOIS", WHITE, t_mois - 0.3, t_ok - 0.9, size=80)
c.kwc("kw-chute", "ET C'EST OK.", ORANGE, t_ok - 0.3, c.END_T + 0.45, size=96, top=1270, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_choix1 - 0.18, 0.3), ("sfx-pop-2", "pop", t_mois - 0.28, 0.26),
       ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26), ("sfx-pop-3", "pop", t_ok - 0.28, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
