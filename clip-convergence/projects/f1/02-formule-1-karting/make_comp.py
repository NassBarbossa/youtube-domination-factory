"""Composition du clip 2 « La Formule 1 et le karting » (Formation 1 « Pourquoi investir en 2026 », Nass seul), comp_lib thème ydf.

La métaphore qui ouvre la formation : vous voulez tous conduire la Formule 1 et vous ne savez pas conduire un karting ; on passe le code ; ne banalisez pas l'information.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402

c = Comp(HERE, 2, "« La Formule 1 et le karting »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = 'VOUS VOULEZ TOUS<br>CONDUIRE <b>LA FORMULE 1</b>'
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_N+"), (E[2], "SOLO_N")]
t_kart, t_code, t_banal = find("s2", "karting"), find("s3", "code"), find("s4", "banalisez")
c.kwc("kw-kart", "VOUS NE SAVEZ PAS<br>CONDUIRE UN KARTING", CYAN, t_kart - 0.9, t_code - 0.9, size=64)
c.kwc("kw-code", "ON PASSE<br>LE CODE", ORANGE, t_code - 0.4, t_banal - 0.8, size=92)
c.kwc("kw-chute", "NE BANALISEZ PAS<br>L'INFORMATION", WHITE, t_banal - 0.3, c.END_T + 0.45, size=80, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_kart - 0.88, 0.28), ("sfx-whoosh-2", "whoosh", E[2] - 0.22, 0.26),
       ("sfx-pop-2", "pop", t_code - 0.38, 0.28), ("sfx-pop-3", "pop", t_banal - 0.28, 0.26)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
