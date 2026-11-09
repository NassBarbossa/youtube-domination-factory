"""Composition du clip 9 « Mets pause, prends un papier » (Formation 1 « Pourquoi investir en 2026 », Nass seul), comp_lib thème ydf.

L'exercice qui sert toute la vie : papier, crayon, tous les mois. Et les bases d'avant : travaille et gagne de l'argent.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402

c = Comp(HERE, 9, "« Mets pause, prends un papier »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf", end="outro")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = 'METS PAUSE,<br><b>PRENDS UN PAPIER</b>'
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_N+"), (E[2], "SOLO_N")]
t_vie, t_mois, t_bases, t_travail = find("s2", "vie"), find("s3", "mois"), find("s4", "bases", 1), find("s4", "travail")
c.kwc("kw-vie", "UN EXERCICE<br>POUR TOUTE LA VIE", CYAN, t_vie - 1.0, t_mois - 0.6, size=76)
c.kwc("kw-mois", "TOUS LES MOIS", ORANGE, t_mois - 0.3, t_bases - 0.5, size=92, top=1270)
c.kwc("kw-bases", "LES BASES D'AVANT :", MUTED, t_bases - 0.2, c.END_T + 0.45, size=52, top=1190)
c.kwc("kw-chute", "TRAVAILLE ET<br>GAGNE DE L'ARGENT", WHITE, t_travail - 0.3, c.END_T + 0.45, size=76, top=1270, anim="rise")
c.cap_cuts = [("s4", t_travail - 0.2, 1e9)]; c.cap_end_before = [t_travail - 0.1]
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_vie - 0.98, 0.26), ("sfx-whoosh-2", "whoosh", E[2] - 0.22, 0.26),
       ("sfx-pop-2", "pop", t_mois - 0.28, 0.28), ("sfx-pop-3", "pop", t_travail - 0.28, 0.3)]
c.sfx = SFX   # la fin « outro » ajoute ses propres sons
c.build()
