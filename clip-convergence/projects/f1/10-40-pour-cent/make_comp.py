"""Composition du clip 10 « 40 %, pas plus » (Formation 1 « Pourquoi investir en 2026 », Nass seul), comp_lib thème ydf.

La première règle du budget : 40 % du revenu mensuel pour le coût fixe de la vie (loyer, abonnements, le vital), pas 70 %. La slide du donut 40 % sous lui.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402

c = Comp(HERE, 10, "« 40 %, pas plus »", cta="Les 3 vidéos sont sur la chaîne", theme="ydf")
seams, find, S = c.seams, c.find, c.STATES
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = '40 % DU SALAIRE,<br><b>PAS PLUS</b>'
c.moves = [(seams[0], "SOLO_N"), (seams[1], "SOLO_E"), (seams[2], "SOLO_N+")]
c.screen_windows = [(seams[1], seams[2])]
t_sal = find("s2", "salaire")
t_40, t_70 = find("s4", "40"), find("s4", "70")
c.kwc("kw-sal", "TON SALAIRE<br>MENSUEL", WHITE, t_sal - 0.2, seams[1] - 0.3, size=84)
c.kwc("kw-40", "40 %", ORANGE, t_40 - 0.1, c.END_T + 0.45, size=150, top=1176)
c.kw("kw-70", '<span class="no">PAS 70 %</span>', f"left: 0; right: 0; top: 1360px; text-align: center; color: {MUTED}; font-size: 72px;", t_70 - 0.3, c.END_T + 0.45, anim="rise")
c.ill_css = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 54%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"
c.cap_cuts = [("s4", t_70 - 0.4, 1e9)]; c.cap_end_before = [t_70 - 0.3]
SFX = [("sfx-whoosh-1", "whoosh-short", seams[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_sal - 0.18, 0.26), ("sfx-whoosh-2", "whoosh", seams[1] - 0.22, 0.3),
       ("sfx-whoosh-3", "whoosh", seams[2] - 0.22, 0.26), ("sfx-pop-2", "pop", t_40 - 0.08, 0.32), ("sfx-pop-3", "pop", t_70 - 0.28, 0.28)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
