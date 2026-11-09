"""Composition du clip 3 « Un secret depuis 2021 » (Formation 1 « Pourquoi investir en 2026 », Nass seul), comp_lib thème ydf.

Le secret que Nass partage depuis 2021 et qui change la vie : avant d'être un bon investisseur, il faut savoir gérer son capital. Deux passages (01:03 et 04:17) cousus.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402

c = Comp(HERE, 3, "« Un secret depuis 2021 »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf", end="outro")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = 'UN SECRET<br><b>DEPUIS 2021</b>'
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_N+")]
t_vie, t_avant, t_gerer = find("s2", "vie"), find("s3", "avant"), find("s3", "gérer")
c.kwc("kw-vie", "IL VA CHANGER<br>VOTRE VIE", CYAN, t_vie - 1.2, min(t_avant - 0.45, E[1] + 3.0), size=88)
c.kwc("kw-avant", "AVANT D'ÊTRE<br>UN BON INVESTISSEUR", WHITE, t_avant - 0.1, t_gerer - 0.5, size=72, anim="rise")
c.kwc("kw-chute", "SAVOIR GÉRER<br>SON CAPITAL", ORANGE, t_gerer - 0.4, c.END_T + 0.45, size=88)
c.cap_cuts = [("s3", t_gerer - 0.3, 1e9)]; c.cap_end_before = [t_gerer - 0.2]
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_vie - 0.88, 0.28), ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26),
       ("sfx-pop-2", "pop", t_gerer - 0.38, 0.3)]
c.sfx = SFX   # la fin « outro » ajoute ses propres sons
c.build()
