"""Composition du clip 10 « Imagine 200 € par mois » (Formation 2 « Comment devenir riche », Nass seul), comp_lib thème ydf.

Imagine 200 € par mois au lieu de 100 : 24 000 € investis, 54 000 € en bourse américaine, 55 000 € en or, 300 000 € en bitcoin. Les chiffres de sa slide.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 10, "« Imagine 200 € par mois »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf", end="outro")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = 'IMAGINE<br><b>200 € PAR MOIS</b>'
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_N+")]
t_500 = find("s1", "500")
c.hook_fade = t_500 - 0.45
c.kwc("kw-500", "200 € ? 500 € ?<br>1 000 € ?", WHITE, t_500 - 0.1, E[0] - 0.3, size=76)
t_200 = find("s2", "200")
t_24, t_54, t_55, t_300 = find("s3", "24"), find("s3", "54"), find("s3", "55"), find("s3", "300")
c.kwc("kw-200", "200 € / MOIS", WHITE, t_200 - 0.2, t_24 - 0.5, size=92, top=1270)
c.kwc("kw-24", "24 000 € INVESTIS", WHITE, t_24 - 0.1, c.END_T + 0.45, size=60, top=1228)
c.kwc("kw-54", "54 000 € BOURSE · 55 000 € OR", CYAN, t_54 - 0.1, c.END_T + 0.45, size=46, top=1306, anim="rise")
c.kwc("kw-300", "300 000 € BITCOIN", ORANGE, t_300 - 0.1, c.END_T + 0.45, size=68, top=1372)
SFX = [("sfx-pop-0", "pop", t_500 - 0.08, 0.26), ("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_200 - 0.18, 0.26), ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26),
       ("sfx-pop-2", "pop", t_24 - 0.08, 0.26), ("sfx-pop-3", "pop", t_54 - 0.08, 0.26), ("sfx-pop-4", "pop", t_300 - 0.08, 0.32)]
c.sfx = SFX   # la fin « outro » ajoute ses propres sons
c.build()
