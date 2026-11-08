"""Composition du clip 12 « Les cracks, pas les tricheurs » (J'abandonne mon challenge crypto, Nass seul), comp_lib thème ydf.

Il ne parle pas des devs qui farment, des scams, des bundlers : il parle des vrais cracks. « Il y en a, et je n'en fais pas partie. Est-ce qu'un jour j'en ferai partie ? Je ne sais pas. »
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 12, "« Les cracks, pas les tricheurs »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 72
c.hook_html = 'LES CRACKS,<br><b>PAS LES TRICHEURS</b>'
c.moves = [(E[0], "SOLO_N+")]
t_scams, t_cracks, t_partie, t_sais = find("s1", "scams"), find("s2", "cracks"), find("s2", "partie"), find("s2", "sais")
c.hook_fade = t_scams - 0.45
c.kwc("kw-scams", "DEVS, SCAMS,<br>BUNDLERS : NON.", MUTED, t_scams - 0.1, E[0] - 0.3, size=68)
c.kwc("kw-cracks", "LES VRAIS CRACKS", CYAN, t_cracks - 0.2, t_partie - 0.9, size=76, top=1270)
c.kwc("kw-partie", "JE N'EN FAIS<br>PAS PARTIE", WHITE, t_partie - 0.2, t_sais - 0.9, size=76)
c.kwc("kw-chute", "UN JOUR ?<br>JE NE SAIS PAS.", ORANGE, t_sais - 0.3, c.END_T + 0.45, size=76, anim="rise")
SFX = [("sfx-pop-1", "pop", t_scams - 0.08, 0.26), ("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-2", "pop", t_cracks - 0.18, 0.26),
       ("sfx-pop-3", "pop", t_partie - 0.18, 0.26), ("sfx-pop-4", "pop", t_sais - 0.28, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
