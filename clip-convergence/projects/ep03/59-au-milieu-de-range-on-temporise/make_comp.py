"""Composition du clip 59 « Au milieu de range, on temporise » (Convergence EP.03, replay YouTube 720p), comp_lib v6.

Sadek, côté investissement : acheter sur les supports, revendre sur les résistances ; au milieu de range, ça peut partir dans les deux sens, ce n'est pas une zone où se presser et cliquer partout : temporiser, analyser, attendre une direction claire et la suivre. Coupe de « ou alors shorter pour ceux qui shortent ». L'écran or de Nass pendant l'explication.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, INK, GREEN, GOLD, GOLD_TXT, GREY, RED, screen_only, solo, solo_screen, sym, sym_screen  # noqa: E402

c = Comp(HERE, 59, "« Au milieu de range, on temporise »", cta="Épisode 3 complet sur la chaîne")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["E"] = sym_screen(480, 520, 900, 506)
S["E+"] = sym_screen(500, 520, 900, 506)
S["SOLO_E"] = solo_screen(860, 900, 506)
S["SOLO_E+"] = solo_screen(880, 900, 506)
c.hook_font = 104
c.hook_html = 'AU MILIEU<br><b>DE RANGE</b>'
S["SOLO_ES"] = solo_screen(860, 900, 506, cam="sadek")   # Sadek seul avec l'écran de Nass (Nass ne parle pas dans ce clip)
c.screen_state = "SOLO_ES"
t_supports, t_temporiser, t_direction = find("s1", "supports"), find("s4", "temporiser"), find("s4", "direction")
c.moves = [(t_supports - 0.3, "SOLO_S"), (E[0], "SOLO_ES"), (E[2], "SOLO_S+")]
c.screen_windows = [(E[0], E[2])]
c.hook_fade = t_supports - 0.45
c.kwc("kw-supports", "ACHETER SUR LES SUPPORTS,<br>REVENDRE SUR LES RÉSISTANCES", INK, t_supports - 0.1, E[0] - 0.3, size=54)
c.kwc("kw-temporiser", "TEMPORISER,<br>ANALYSER", GREY, t_temporiser - 0.2, t_direction - 0.9, size=76)
c.kwc("kw-chute", "ATTENDRE UNE<br>DIRECTION CLAIRE", GREEN, t_direction - 0.3, c.END_T + 0.45, size=72, anim="rise")
SFX = [("sfx-pop-1", "pop", t_supports - 0.08, 0.26), ("sfx-whoosh-1", "whoosh", E[0] - 0.22, 0.3), ("sfx-whoosh-2", "whoosh", E[2] - 0.22, 0.26),
       ("sfx-pop-2", "pop", t_temporiser - 0.18, 0.26), ("sfx-pop-3", "pop", t_direction - 0.28, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
