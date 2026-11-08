"""Composition du clip 1 « Pas une option, une obligation » (Formation 1 « Pourquoi investir en 2026 », Nass seul), comp_lib thème ydf.

Investir n'est pas une option, c'est une obligation : en 2027, 2028, 2029, 2030, jusqu'à la fin de votre vie, pour lutter contre l'inflation.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402

c = Comp(HERE, 1, "« Pas une option, une obligation »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf")
seams, find, S = c.seams, c.find, c.STATES
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = 'PAS UNE OPTION,<br><b>UNE OBLIGATION</b>'
c.moves = [(seams[0], "SOLO_N")]
t27, t28, t29, t30 = find("s2", "2027"), find("s2", "2028"), find("s2", "2029"), find("s2", "2030")
t_fin, t_lutter = find("s2", "fin"), find("s2", "lutter")
for i, (t, y) in enumerate([(t27, "2027"), (t28, "2028"), (t29, "2029"), (t30, "2030")]):
    c.kw(f"kw-y{i}", y, f"left: {44 + i * 252}px; width: 236px; top: 1230px; text-align: center; color: {ORANGE}; font-size: 66px; padding: 22px 0; "
         f"border: 5px solid rgba(255,107,53,0.6); border-radius: 22px; background: rgba(255,107,53,0.08);", t - 0.05, t_fin - 0.4)
c.kwc("kw-fin", "JUSQU'À LA FIN<br>DE VOTRE VIE", CYAN, t_fin - 0.3, t_lutter - 0.4, size=84, anim="rise")
c.kwc("kw-chute", "LUTTER CONTRE<br>L'INFLATION", ORANGE, t_lutter - 0.1, c.END_T + 0.45, size=84)
c.cap_cuts = [("s2", t_lutter - 0.05, 1e9)]; c.cap_end_before = [t_lutter]
SFX = [("sfx-whoosh-1", "whoosh-short", seams[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t27, 0.22), ("sfx-pop-2", "pop", t28, 0.22),
       ("sfx-pop-3", "pop", t29, 0.22), ("sfx-pop-4", "pop", t30, 0.22), ("sfx-pop-5", "pop", t_lutter - 0.08, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
