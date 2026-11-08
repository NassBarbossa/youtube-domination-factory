"""Composition du clip 1 « 5 000 €, 10 000 €… ou offerte ici » (Formation 3 « L'investissement on-chain », Nass seul), comp_lib thème ydf.

Il est temps de conduire la Formule 1 : une stratégie que très peu vulgarisent sur le marché français, ou qu'ils facturent 5 000 € en accompagnement et 10 000 € en mastermind. Ici, offerte.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 1, "« 5 000 €, 10 000 €… ou offerte ici »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 76
c.hook_html = '5 000 €, 10 000 €…<br><b>OU OFFERTE ICI</b>'
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_N+")]
t_peu, t_5000, t_10000 = find("s2", "très"), find("s3", "5"), find("s3", "10")
c.kwc("kw-peu", "TRÈS PEU<br>LA VULGARISENT", WHITE, t_peu - 0.2, t_5000 - 0.9, size=80)
c.kwc("kw-5000", "5 000 € L'ACCOMPAGNEMENT", MUTED, t_5000 - 0.2, c.END_T + 0.45, size=48, top=1266)
c.kwc("kw-10000", "10 000 € LE MASTERMIND", MUTED, t_10000 - 0.2, c.END_T + 0.45, size=48, top=1332, anim="rise")
c.kwc("kw-chute", "ICI : OFFERTE", ORANGE, t_10000 + 1.6, c.END_T + 0.45, size=80, top=1408)
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_peu - 0.18, 0.26), ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26),
       ("sfx-pop-2", "pop", t_5000 - 0.18, 0.26), ("sfx-pop-3", "pop", t_10000 - 0.18, 0.26), ("sfx-pop-4", "pop", t_10000 + 1.62, 0.32)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
