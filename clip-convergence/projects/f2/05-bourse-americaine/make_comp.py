"""Composition du clip 5 « 100 € par mois dans la bourse américaine » (Formation 2 « Comment devenir riche », Nass seul), comp_lib thème ydf.

100 € par mois pendant 10 ans dans le S&P 500 : 27 261 € aujourd'hui, « tout est vérifiable ». Les chiffres sont ceux de sa slide (oct. 2016 → sept. 2026), la slide sous lui.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 5, "« 100 € par mois dans la bourse américaine »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf", end="outro")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 72
c.hook_html = '100 € PAR MOIS<br><b>DANS LA BOURSE AMÉRICAINE</b>'
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_E")]
c.screen_windows = [(E[1], c.END_T)]
t_verif = find("s2", "vérifiable")
t_x = find("s3", "multiplié")
c.kwc("kw-100", "100 € / MOIS<br>PENDANT 10 ANS", WHITE, E[0] + 0.3, t_verif - 1.7, size=80)
c.kwc("kw-verif", "TOUT EST<br>VÉRIFIABLE", CYAN, t_verif - 0.8, E[1] - 0.3, size=84)
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", E[0] + 0.32, 0.26), ("sfx-pop-2", "pop", t_verif - 0.78, 0.26),
       ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.3)]
c.sfx = SFX   # la fin « outro » ajoute ses propres sons
c.build()
