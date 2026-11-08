"""Composition du clip 3 « Le marché a changé » (J'abandonne mon challenge crypto, Nass seul), comp_lib thème ydf.

Pourquoi du surplace, pourquoi arrêter : deux grandes raisons, et la première, « le marché, il a changé, il faut se le dire ». La slide « Le marché a changé. Il faut s'adapter. » sous lui.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 3, "« Le marché a changé »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = 'LE MARCHÉ<br><b>A CHANGÉ</b>'
c.moves = [(E[0], "SOLO_E")]
c.screen_windows = [(E[0], c.END_T)]
t_pourquoi = find("s1", "pourquoi")
c.kwc("kw-pourquoi", "POURQUOI<br>DU SURPLACE ?", MUTED, t_pourquoi + 2.4, E[0] - 0.3, size=76)
c.hook_fade = t_pourquoi + 1.95
SFX = [("sfx-pop-1", "pop", t_pourquoi + 2.42, 0.26), ("sfx-whoosh-1", "whoosh", E[0] - 0.22, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
