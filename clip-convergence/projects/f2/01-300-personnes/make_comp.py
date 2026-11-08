"""Composition du clip 1 « J'ai fait payer 300 personnes pour ça » (Formation 2 « Comment devenir riche », Nass seul), comp_lib thème ydf.

La méthode que Nass a fait payer à plus de 300 personnes en 2021-2022, donnée gratuitement aujourd'hui : il ne veut plus faire de formations. La slide « 2021 · 2022 · Payant » sous lui.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 1, "« J'ai fait payer 300 personnes pour ça »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 76
c.hook_html = "J'AI FAIT PAYER<br><b>300 PERSONNES POUR ÇA</b>"
c.moves = [(E[0], "SOLO_E"), (E[1], "SOLO_N"), (E[2], "SOLO_N+")]
c.screen_windows = [(E[0], E[1])]
t_gratuit, t_plus = find("s3", "gratuitement"), find("s4", "plus")
c.kwc("kw-gratuit", "AUJOURD'HUI,<br>GRATUITEMENT", ORANGE, t_gratuit - 0.4, t_plus - 0.6, size=84)
c.kwc("kw-chute", "JE NE VEUX PLUS<br>FAIRE DE FORMATIONS", WHITE, t_plus - 0.3, c.END_T + 0.45, size=72, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh", E[0] - 0.22, 0.3), ("sfx-whoosh-2", "whoosh-short", E[1] - 0.2, 0.3), ("sfx-pop-1", "pop", t_gratuit - 0.38, 0.3),
       ("sfx-whoosh-3", "whoosh", E[2] - 0.22, 0.26), ("sfx-pop-2", "pop", t_plus - 0.28, 0.26)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
