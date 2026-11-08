"""Composition du clip 30 « La plus grande correction de l'or depuis 2000 » (Convergence EP.01, Sadek), comp_lib v6.

Accroche « LA PLUS GRANDE / CORRECTION DE L'OR », puis Sadek seul avec l'écran de Nass (le graphique de l'or) pendant « vous
pouvez aller vérifier les datas », puis Sadek seul pour « du haut de la mèche ». Les pourcentages (18 %, 30 %) restent dans la
voix et les sous-titres : non vérifiés, pas affichés en mot clé. Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, GOLD_TXT, INK, solo_screen  # noqa: E402

c = Comp(HERE, 30, "« La plus grande correction de l'or depuis 2000 »")
seams, find = c.seams, c.find
S = c.STATES
S["SOLO_ES"] = solo_screen(860, 900, 491, cam="sadek")
S["SOLO_ES+"] = dict(S["SOLO_ES"], sadek=(540, S["SOLO_ES"]["sadek"][1] + 10, 880))
c.screen_state = "SOLO_ES"
c.moves = [
    (seams[0], "SOLO_ES"),    # s2 : « vous pouvez aller vérifier les datas » : le graphique de l'or
    (seams[1], "SOLO_ES+"),   # s3 : « on n'a jamais eu une correction aussi profonde »
    (seams[2], "SOLO_S"),     # s4 : « du haut de la mèche »
]
c.z_front = [(0, "sadek")]
c.screen_windows = [(seams[0], seams[2])]
c.hook_html = 'LA PLUS GRANDE<br><b class="or">CORRECTION DE L\'OR</b>'
c.hook_font = 88

t_meche = find("s4", "mèche")
c.kw("kw-meche", "DU HAUT<br>DE LA MÈCHE", f"left: 0; right: 0; top: 1200px; text-align: center; color: {GOLD_TXT}; font-size: 100px; line-height: 1;",
     t_meche - 0.7, c.END_T + 0.05)

c.sfx = [
    ("sfx-whoosh-1", "whoosh-short", seams[0] - 0.20, 0.34),
    ("sfx-whoosh-2", "whoosh", seams[2] - 0.22, 0.30),
    ("sfx-pop-1", "pop", t_meche - 0.68, 0.28),
    ("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40),
]
c.build()
print(f"écran {seams[0]}-{seams[2]} | mèche {t_meche}")
