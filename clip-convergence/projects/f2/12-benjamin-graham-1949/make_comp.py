"""Composition du clip 12 « On le sait depuis 1949 » (Formation 2 « Comment devenir riche », Nass seul), comp_lib thème ydf.

Le DCA est théorisé depuis 1949 par Benjamin Graham dans « L'investisseur intelligent », mentor de Warren Buffett, le meilleur investisseur de notre époque. La slide Buffett sous lui.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 12, "« On le sait depuis 1949 »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = 'ON LE SAIT<br><b>DEPUIS 1949</b>'
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_N+"), (E[2], "SOLO_E")]
c.screen_windows = [(E[2], c.END_T)]
t_80, t_mentor = find("s2", "80"), find("s3", "mentor")
t_bg = find("s1", "Benjamin")
c.hook_fade = t_bg - 0.45
c.kwc("kw-graham", "BENJAMIN GRAHAM<br>L'INVESTISSEUR INTELLIGENT", WHITE, t_bg - 0.1, t_80 - 0.6, size=60)
c.kwc("kw-80", "BIENTÔT 80 ANS<br>QUE ÇA MARCHE", ORANGE, t_80 - 0.3, t_mentor - 0.8, size=80)
c.kwc("kw-chute", "LE MENTOR DE<br>WARREN BUFFETT", CYAN, t_mentor - 0.3, E[2] - 0.3, size=76, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_bg - 0.08, 0.26), ("sfx-pop-2", "pop", t_80 - 0.28, 0.3),
       ("sfx-pop-3", "pop", t_mentor - 0.28, 0.26), ("sfx-whoosh-2", "whoosh", E[2] - 0.22, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
