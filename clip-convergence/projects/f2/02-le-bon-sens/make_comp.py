"""Composition du clip 2 « Le bon sens, il faut le savoir » (Formation 2 « Comment devenir riche », Nass seul), comp_lib thème ydf.

L'investissement, c'est du bon sens ; mais tant qu'on ne te l'a pas dit, tu ne sais pas que c'est du bon sens.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 2, "« Le bon sens, il faut le savoir »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf", end="outro")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = 'LE BON SENS,<br><b>IL FAUT LE SAVOIR</b>'
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_N+"), (E[2], "SOLO_N")]
t_savoir, t_debut, t_juste = find("s2", "savoir"), find("s3", "début"), find("s4", "juste")
c.kwc("kw-bonsens", "C'EST DU<br>BON SENS", WHITE, E[0] + 0.3, t_savoir - 0.9, size=88)
c.kwc("kw-savoir", "IL FAUT<br>LE SAVOIR", ORANGE, t_savoir - 0.4, t_juste - 0.9, size=92)
c.kwc("kw-chute", "JUSTE DU<br>BON SENS", CYAN, t_juste - 0.3, c.END_T + 0.45, size=92, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", E[0] + 0.32, 0.26), ("sfx-pop-2", "pop", t_savoir - 0.38, 0.3),
       ("sfx-whoosh-2", "whoosh", E[2] - 0.22, 0.26), ("sfx-pop-3", "pop", t_juste - 0.28, 0.28)]
c.sfx = SFX   # la fin « outro » ajoute ses propres sons
c.build()
