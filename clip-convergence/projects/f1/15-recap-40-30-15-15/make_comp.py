"""Composition du clip 15 « La règle 40 · 30 · 15 · 15 » (Formation 1 « Pourquoi investir en 2026 », Nass seul), comp_lib thème ydf.

Le récap : 40 % coût de la vie, 30 % d'épargne jusqu'à 6 mois, puis plus d'investissement ; chaque individu est différent, mais c'est comme ça qu'on gère son capital. Le donut complet sous lui.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402

c = Comp(HERE, 15, "« La règle 40 · 30 · 15 · 15 »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = 'LA RÈGLE<br><b>40 · 30 · 15 · 15</b>'
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_E"), (E[2], "SOLO_E+"), (E[3], "SOLO_E"), (E[4], "SOLO_N")]
c.screen_windows = [(E[1], E[4])]
t_ex, t_diff, t_capital = find("s2", "exercice"), find("s6", "différent"), find("s6", "capital")
c.kwc("kw-ex", "FAITES<br>CET EXERCICE", ORANGE, t_ex - 0.3, E[1] - 0.3, size=88)
c.kwc("kw-diff", "CHAQUE INDIVIDU<br>EST DIFFÉRENT", MUTED, t_diff - 0.8, t_capital - 1.2, size=64)
c.kwc("kw-chute", "COMMENT GÉRER<br>VOTRE CAPITAL", ORANGE, t_capital - 1.1, c.END_T + 0.45, size=84, anim="rise")
c.cap_cuts = [("s6", t_capital - 1.0, 1e9)]; c.cap_end_before = [t_capital - 0.9]
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_ex - 0.28, 0.26), ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.3),
       ("sfx-whoosh-3", "whoosh", E[4] - 0.22, 0.3), ("sfx-pop-2", "pop", t_capital - 1.08, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
