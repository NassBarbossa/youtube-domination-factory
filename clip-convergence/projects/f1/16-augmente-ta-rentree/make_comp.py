"""Composition du clip 16 « Augmente ta rentrée mensuelle » (Formation 1 « Pourquoi investir en 2026 », Nass seul), comp_lib thème ydf.

Passe à l'action : avant de gagner de l'argent en investissement, occupe-toi du chiffre du haut, ta rentrée mensuelle, par ton travail et tes compétences.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402

c = Comp(HERE, 16, "« Augmente ta rentrée mensuelle »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf", end="outro")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = "PASSE<br><b>À L'ACTION</b>"
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_N+"), (E[2], "SOLO_N")]
t_avant, t_rentree, t_travail, t_aug = find("s2", "Avant"), find("s3", "rentrée"), find("s3", "travail"), find("s3", "augmenter")
t_aug4 = find("s4", "augmenter")
c.kwc("kw-avant", "AVANT DE GAGNER<br>EN INVESTISSEMENT", WHITE, t_avant - 0.1, t_rentree - 0.5, size=72)
c.kwc("kw-rentree", "TA RENTRÉE<br>MENSUELLE", ORANGE, t_rentree - 0.2, t_travail - 0.85, size=88)
c.kwc("kw-travail", "TON TRAVAIL,<br>TES COMPÉTENCES", CYAN, t_travail - 0.4, t_aug4 - 0.8, size=76, anim="rise")
c.kwc("kw-chute", "AUGMENTE<br>TA RENTRÉE", ORANGE, t_aug4 - 0.3, c.END_T + 0.45, size=92)
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_avant - 0.08, 0.26), ("sfx-whoosh-2", "whoosh", E[2] - 0.22, 0.26),
       ("sfx-pop-2", "pop", t_rentree - 0.18, 0.28), ("sfx-pop-3", "pop", t_aug4 - 0.28, 0.3)]
c.sfx = SFX   # la fin « outro » ajoute ses propres sons
c.build()
