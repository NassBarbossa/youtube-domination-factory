"""Composition du clip 4 « Acheter avant les autres » (Formation 3 « L'investissement on-chain », Nass seul), comp_lib thème ydf.

Le bon sens appliqué : la façon la plus facile de faire de l'argent, c'est d'acheter avant les autres. « Tu ne seras peut-être pas ici, mais à partir d'ici. » La slide de la courbe sous lui.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 4, "« Acheter avant les autres »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = 'ACHETER<br><b>AVANT LES AUTRES</b>'
c.moves = [(E[0], "SOLO_E"), (E[1], "SOLO_N+")]
c.screen_windows = [(E[0], E[1])]
t_ici = find("s3", "ici")
c.kwc("kw-meth", "AVEC<br>UNE MÉTHODE", WHITE, E[1] + 0.3, t_ici - 0.9, size=80)
c.kwc("kw-chute", "PAS ICI,<br>MAIS À PARTIR D'ICI", ORANGE, t_ici - 0.3, c.END_T + 0.45, size=72)
SFX = [("sfx-whoosh-1", "whoosh", E[0] - 0.22, 0.3), ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26), ("sfx-pop-1", "pop", E[1] + 0.32, 0.26), ("sfx-pop-2", "pop", t_ici - 0.28, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
