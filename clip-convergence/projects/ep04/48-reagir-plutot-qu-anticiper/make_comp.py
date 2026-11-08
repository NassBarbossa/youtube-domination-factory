"""Composition du clip 48 « Réagir plutôt qu'anticiper » (Convergence EP.04, Nass seul), comp_lib v6, monologue.

Sa façon d'investir : ne pas anticiper, réagir ; viser l'entrée au meilleur prix pour pouvoir couper si ça s'invalide sans trop perdre. Si tu attends la confirmation, la zone est déjà là, dur de tenir, tu repasses vite en BE voire en perte. Son écran or sous lui pour la démonstration.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, INK, GREEN, GOLD, GOLD_TXT, GREY, RED, solo, solo_screen  # noqa: E402

c = Comp(HERE, 48, "« Réagir plutôt qu'anticiper »", cta="Épisode 4 complet sur la chaîne")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = "RÉAGIR<br><b>PLUTÔT QU'ANTICIPER</b>"
c.moves = [(E[0], "SOLO_N+"), (E[1], "SOLO_E")]
c.screen_windows = [(E[1], c.END_T)]
t_meilleur, t_couper = find("s2", "meilleur"), find("s2", "couper")
c.kwc("kw-entree", "L'ENTRÉE AU<br>MEILLEUR PRIX", INK, t_meilleur - 0.1, t_couper - 0.9, size=70)
c.kwc("kw-couper", "COUPER SI ÇA S'INVALIDE,<br>SANS TROP PERDRE", GREEN, t_couper - 0.2, E[1] - 0.3, size=56)
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_meilleur - 0.08, 0.26), ("sfx-pop-2", "pop", t_couper - 0.18, 0.3), ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
