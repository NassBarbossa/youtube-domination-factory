"""Composition du clip 8 « 97 % de perdants ? La vraie stat » (J'abandonne mon challenge crypto, Nass seul), comp_lib thème ydf.

On répète que 97 % des traders perdent. Vrai ou faux ? Il a trouvé un article (novembre 2025 → août 2026) : 74 % de perdants, 270 millions perdus. « On va dire la loi de Pareto : 80 / 20. » La slide 74 % avec sa source sous lui.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 8, "« 97 % de perdants ? La vraie stat »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 72
c.hook_html = '97 % DE PERDANTS ?<br><b>LA VRAIE STAT</b>'
c.moves = [(E[0], "SOLO_E"), (E[1], "SOLO_N+")]
c.screen_windows = [(E[0], E[1])]
t_97, t_74, t_pareto = find("s1", "97"), find("s3", "74"), find("s3", "Pareto")
c.hook_fade = t_97 - 0.45
c.kwc("kw-97", "« 97 % PERDANTS » ?", MUTED, t_97 - 0.1, E[0] - 0.3, size=68, top=1270)
c.kwc("kw-74", "74 % PERDANTS<br>(SA STAT)", CYAN, t_74 - 0.1, t_pareto - 0.5, size=68)
c.kwc("kw-chute", "LOI DE PARETO<br>80 % PERDANTS<br>20 % GAGNANTS", ORANGE, t_pareto - 0.25, c.END_T + 0.45, size=66, anim="rise")
SFX = [("sfx-pop-1", "pop", t_97 - 0.08, 0.26), ("sfx-whoosh-1", "whoosh", E[0] - 0.22, 0.3), ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26),
       ("sfx-pop-2", "pop", t_74 - 0.08, 0.26), ("sfx-pop-3", "pop", t_pareto - 0.23, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
