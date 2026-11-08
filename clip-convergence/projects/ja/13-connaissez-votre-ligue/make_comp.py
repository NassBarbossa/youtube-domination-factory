"""Composition du clip 13 « Connaissez votre ligue » (J'abandonne mon challenge crypto, Nass seul), comp_lib thème ydf.

C'est vraiment important de connaître sa ligue : il connaît la sienne, le marché est difficile, donc il préfère se concentrer sur autre chose (du contenu) plutôt que forcer et brûler son capital. La slide « C'est important de connaître sa ligue » sous lui.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 13, "« Connaissez votre ligue »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = 'CONNAISSEZ<br><b>VOTRE LIGUE</b>'
c.moves = [(E[0], "SOLO_E")]
c.screen_windows = [(E[0], c.END_T)]
t_connais, t_difficile = find("s1", "connais"), find("s1", "difficile,")
c.hook_fade = t_connais - 0.45
c.kwc("kw-connais", "MOI, JE LA CONNAIS", CYAN, t_connais - 0.1, t_difficile - 0.9, size=72, top=1270)
c.kwc("kw-diff", "LE MARCHÉ EST<br>DIFFICILE", WHITE, t_difficile - 0.3, E[0] - 0.3, size=72)
SFX = [("sfx-pop-1", "pop", t_connais - 0.08, 0.26), ("sfx-pop-2", "pop", t_difficile - 0.28, 0.26), ("sfx-whoosh-1", "whoosh", E[0] - 0.22, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
