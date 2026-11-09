"""Composition du clip 6 « 100 € par mois dans l'or » (Formation 2 « Comment devenir riche », Nass seul), comp_lib thème ydf.

100 € par mois pendant 10 ans dans l'or : 27 880 € aujourd'hui, et plus de 30 000 € au pic. Les chiffres de sa slide (source Yahoo Finance sur la slide), la slide sous lui.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 6, "« 100 € par mois dans l'or »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf", end="outro")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = "100 € PAR MOIS<br><b>DANS L'OR</b>"
c.moves = [(E[0], "SOLO_E"), (E[1], "SOLO_E+")]
c.screen_windows = [(E[0], c.END_T)]
t_or = find("s1", "or")
c.hook_fade = t_or - 0.45
c.kwc("kw-or", "PAREIL :<br>100 € / MOIS, 10 ANS", WHITE, t_or - 0.1, E[0] - 0.3, size=76)
SFX = [("sfx-pop-1", "pop", t_or - 0.08, 0.26), ("sfx-whoosh-1", "whoosh", E[0] - 0.22, 0.3), ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26)]
c.sfx = SFX   # la fin « outro » ajoute ses propres sons
c.build()
