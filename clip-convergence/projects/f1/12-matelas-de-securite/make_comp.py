"""Composition du clip 12 « 30 % d'épargne : le matelas de sécurité » (Formation 1 « Pourquoi investir en 2026 », Nass seul), comp_lib thème ydf.

30 % en épargne jusqu'à un matelas de 3 à 6 mois de coût de la vie, selon l'âge, la situation, les enfants : pour être tranquille. La slide du donut 30 % sous lui.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402

c = Comp(HERE, 12, "« 30 % d'épargne : le matelas de sécurité »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 76
c.hook_html = "30 % D'ÉPARGNE :<br>UN MATELAS<br><b>DE SÉCURITÉ</b>"
c.moves = [(E[0], "SOLO_E"), (E[1], "SOLO_N"), (E[2], "SOLO_N+"), (E[3], "SOLO_N")]
c.screen_windows = [(E[0], E[1])]
t_3, t_pepin, t_tranq = find("s3", "3"), find("s4", "pépin"), find("s5", "tranquille")
c.kwc("kw-3", "3 À 6 MOIS<br>DE COÛT DE LA VIE", CYAN, t_3 - 0.2, t_pepin - 0.6, size=72)
c.kwc("kw-pepin", "UN PÉPIN ?<br>VOUS ÊTES COUVERT", WHITE, t_pepin - 0.2, t_tranq - 0.9, size=72, anim="rise")
c.kwc("kw-chute", "POUR ÊTRE<br>TRANQUILLE", ORANGE, t_tranq - 0.5, c.END_T + 0.45, size=92)
c.cap_cuts = [("s5", t_tranq - 0.4, 1e9)]; c.cap_end_before = [t_tranq - 0.3]
SFX = [("sfx-whoosh-1", "whoosh", E[0] - 0.22, 0.3), ("sfx-whoosh-2", "whoosh-short", E[1] - 0.2, 0.3), ("sfx-pop-1", "pop", t_3 - 0.18, 0.26),
       ("sfx-whoosh-3", "whoosh", E[3] - 0.22, 0.26), ("sfx-pop-2", "pop", t_tranq - 0.48, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
