"""Composition du clip 7 « Suis-je une fraude ? » (J'abandonne mon challenge crypto, Nass seul), comp_lib thème ydf.

Il pose lui-même la question : « est-ce que j'arrête parce que je suis une fraude, une arnaque ? » On reviendra sur « suis-je un trader rentable » au fil des années. Et l'important : savoir votre ligue, là où vous êtes placé. La slide « suis-je un trader rentable ? » sous lui.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 7, "« Suis-je une fraude ? »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = 'SUIS-JE<br><b>UNE FRAUDE ?</b>'
c.moves = [(E[0], "SOLO_E"), (E[1], "SOLO_N+")]
c.screen_windows = [(E[0], E[1])]
t_ligue = find("s3", "ligue")
c.kwc("kw-chute", "SAVOIR<br>VOTRE LIGUE", ORANGE, t_ligue - 0.4, c.END_T + 0.45, size=88, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh", E[0] - 0.22, 0.3), ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26), ("sfx-pop-1", "pop", t_ligue - 0.38, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
