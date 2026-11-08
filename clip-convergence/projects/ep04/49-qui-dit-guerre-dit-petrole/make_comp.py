"""Composition du clip 49 « Qui dit guerre dit pétrole » (Convergence EP.04, Nass seul), comp_lib v6, monologue.

Revue de marché : qui dit guerre dit reprise du pétrole ; les commodities, il a toujours refusé d'y toucher, mais c'est intéressant pour lire les tensions : depuis 20 jours le pétrole repart à la hausse. Pas d'avis sur l'or, juste le constat qu'il revient dans la zone du pic de la guerre, « ça se voyait graphiquement ». Son écran pétrole sous lui.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, INK, GREEN, GOLD, GOLD_TXT, GREY, RED, solo, solo_screen  # noqa: E402

c = Comp(HERE, 49, "« Qui dit guerre dit pétrole »", cta="Épisode 4 complet sur la chaîne")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 92
c.hook_html = 'QUI DIT GUERRE<br><b>DIT PÉTROLE</b>'
c.fix = {("s1", "l'oeil"): "l'oil,", ("s1", "'oeil"): "'oil,", ("s2", "traiter"): "trader", ("s4", "Gol,"): "gold,", ("s4", "Gol"): "gold"}
c.moves = [(E[0], "SOLO_N+"), (E[1], "SOLO_E"), (E[2], "SOLO_N+")]
c.screen_windows = [(E[1], E[2])]
t_refuse, t_avis, t_voyait = find("s2", "refusé"), find("s4", "avis"), find("s4", "voyait")
c.kwc("kw-refuse", "LES COMMODITIES ?<br>PAS MON TRUC", GREY, t_refuse - 0.2, E[1] - 0.3, size=66)
c.kwc("kw-avis", "PAS D'AVIS<br>SUR L'OR", GREY, t_avis - 0.2, t_voyait - 0.9, size=72)
c.kwc("kw-chute", "ÇA SE VOYAIT<br>GRAPHIQUEMENT", GREEN, t_voyait - 0.3, c.END_T + 0.45, size=72, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_refuse - 0.18, 0.26), ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.3),
       ("sfx-whoosh-3", "whoosh", E[2] - 0.22, 0.26), ("sfx-pop-2", "pop", t_avis - 0.18, 0.26), ("sfx-pop-3", "pop", t_voyait - 0.28, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
