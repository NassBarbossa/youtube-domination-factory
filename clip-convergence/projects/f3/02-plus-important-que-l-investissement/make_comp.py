"""Composition du clip 2 « Plus important que l'investissement » (Formation 3 « L'investissement on-chain », Nass seul), comp_lib thème ydf.

Le récap des vidéos 1 et 2 : gérer son capital, « plus important que l'investissement, les fondations de toute votre carrière d'investisseur », puis investir intelligemment avec le DCA.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 2, "« Plus important que l'investissement »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 72
c.hook_html = "PLUS IMPORTANT<br><b>QUE L'INVESTISSEMENT</b>"
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_N+")]
t_fond, t_dca, t_facile = find("s1", "fondations"), find("s2", "DCA"), find("s3", "facile")
c.hook_fade = t_fond - 0.45
c.kwc("kw-fond", "LES FONDATIONS", ORANGE, t_fond - 0.1, E[0] - 0.3, size=88, top=1270)
c.kwc("kw-dca", "INVESTIR<br>INTELLIGEMMENT<br>= LE DCA", CYAN, E[0] + 0.3, t_facile - 0.9, size=60)
c.kwc("kw-chute", "FACILE À METTRE<br>EN PLACE", WHITE, t_facile - 0.3, c.END_T + 0.45, size=80, anim="rise")
SFX = [("sfx-pop-1", "pop", t_fond - 0.08, 0.3), ("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-2", "pop", E[0] + 0.32, 0.26),
       ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26), ("sfx-pop-3", "pop", t_facile - 0.28, 0.28)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
