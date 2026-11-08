"""Composition du clip 11 « La ligue que j'aspire à être » (J'abandonne mon challenge crypto, Nass seul), comp_lib thème ydf.

La ligue qu'il vise, et qu'il devrait avoir « si je faisais mieux les choses », au vu du temps et des années. Beaucoup y sont arrivés en août et septembre ; en octobre, ça va être plus difficile.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 11, "« La ligue que j'aspire à être »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = 'LA LIGUE QUE<br><b>JE VISE</b>'
c.fix = {("s1", "Six"): "six", ("s1", "Fix"): "figures"}
c.moves = [(E[0], "SOLO_N+")]
t_mieux, t_octobre, t_difficile = find("s1", "mieux"), find("s2", "octobre"), find("s2", "difficile")
c.hook_fade = t_mieux - 0.45
c.kwc("kw-mieux", "SI JE FAISAIS<br>MIEUX LES CHOSES", WHITE, t_mieux - 0.1, E[0] - 0.3, size=68)
c.kwc("kw-oct", "OCTOBRE :", MUTED, t_octobre - 0.2, t_difficile - 0.9, size=84, top=1270)
c.kwc("kw-chute", "PLUS DIFFICILE", ORANGE, t_difficile - 0.3, c.END_T + 0.45, size=92, top=1270, anim="rise")
SFX = [("sfx-pop-1", "pop", t_mieux - 0.08, 0.26), ("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-2", "pop", t_octobre - 0.18, 0.26), ("sfx-pop-3", "pop", t_difficile - 0.28, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
