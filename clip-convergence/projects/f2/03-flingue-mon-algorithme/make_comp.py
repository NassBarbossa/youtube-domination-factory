"""Composition du clip 3 « Flingue-moi mon algorithme » (Formation 2 « Comment devenir riche », Nass seul), comp_lib thème ydf.

Va voir la vidéo 1 d'abord : « flingue-moi mon algorithme, ce n'est pas grave, c'est pour toi ». La slide « Flingue-moi mon algorithme » sous lui.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 3, "« Flingue-moi mon algorithme »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = 'FLINGUE-MOI<br><b>MON ALGORITHME</b>'
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_E"), (E[2], "SOLO_N+")]
c.screen_windows = [(E[1], E[2])]
t_i, t_toi, t_va = find("s2", "petit"), find("s3", "toi"), find("s4", "Va")
c.kwc("kw-i", "LE PETIT i", CYAN, t_i - 0.2, E[1] - 0.3, size=92, top=1270)
c.kwc("kw-chute", "VA VOIR<br>LA VIDÉO 1", ORANGE, t_va - 0.2, c.END_T + 0.45, size=92)
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_i - 0.18, 0.26), ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.3),
       ("sfx-whoosh-3", "whoosh", E[2] - 0.22, 0.26), ("sfx-pop-2", "pop", t_va - 0.18, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
