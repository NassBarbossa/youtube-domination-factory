"""Composition du clip 5 « Investir, la définition » (Formation 1 « Pourquoi investir en 2026 », Nass seul), comp_lib thème ydf.

Investir, c'est mettre son argent dans quelque chose qui prend de la valeur avec le temps. On revient aux bases, pendant longtemps.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402

c = Comp(HERE, 5, "« Investir, la définition »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf", end="outro")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = 'ON REVIENT<br><b>AUX BASES</b>'
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_N+"), (E[2], "SOLO_N"), (E[3], "SOLO_N+")]
t_mettre, t_valeur, t_temps2, t_long = find("s2", "mettre"), find("s2", "valeur"), find("s4", "temps"), find("s5", "longtemps")
c.kwc("kw-mettre", "METTRE<br>SON ARGENT", WHITE, t_mettre - 0.1, t_valeur - 0.5, size=88)
c.kwc("kw-valeur", "QUI PREND<br>DE LA VALEUR", CYAN, t_valeur - 0.4, E[2] - 0.3, size=84, anim="rise")
c.kwc("kw-temps", "AVEC LE TEMPS", ORANGE, t_temps2 - 0.3, min(t_long - 0.6, E[3] + 2.5), size=92, top=1270)
c.kwc("kw-chute", "PENDANT<br>LONGTEMPS", ORANGE, t_long - 0.3, c.END_T + 0.45, size=92)
c.cap_cuts = [("s5", t_long - 0.1, 1e9)]; c.cap_end_before = [t_long - 0.05]
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_mettre - 0.08, 0.26), ("sfx-whoosh-2", "whoosh", E[2] - 0.22, 0.26),
       ("sfx-pop-2", "pop", t_temps2 - 0.28, 0.28), ("sfx-pop-3", "pop", t_long - 0.28, 0.3)]
c.sfx = SFX   # la fin « outro » ajoute ses propres sons
c.build()
