"""Composition du clip 17 « Pas pour gagner de l'argent » (Formation 1 « Pourquoi investir en 2026 », Nass seul), comp_lib thème ydf.

On investit pour contrer l'inflation : pas pour gagner de l'argent, pour ne pas en perdre. Et la liberté géographique vaut mille fois la liberté financière.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402

c = Comp(HERE, 17, "« Pas pour gagner de l'argent »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = "PAS POUR GAGNER<br><b>DE L'ARGENT</b>"
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_N+"), (E[2], "SOLO_N")]
t_perdre, t_com, t_geo, t_fin = find("s2", "perdre"), find("s3", "commentaires"), find("s4", "géographique"), find("s4", "financière")
c.kwc("kw-perdre", "POUR NE PAS<br>EN PERDRE", RED_Y, t_perdre - 0.6, t_com - 0.85, size=88)
c.kwc("kw-com", "DIS-LE MOI<br>EN COMMENTAIRE", WHITE, t_com - 0.4, t_geo - 0.85, size=76, anim="rise")
c.kwc("kw-geo", "LIBERTÉ GÉOGRAPHIQUE", CYAN, t_geo - 0.3, c.END_T + 0.45, size=56, top=1215)
c.kwc("kw-fin", "> LIBERTÉ FINANCIÈRE", MUTED, t_fin - 0.3, c.END_T + 0.45, size=50, top=1305, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_perdre - 0.58, 0.3), ("sfx-whoosh-2", "whoosh", E[2] - 0.22, 0.26),
       ("sfx-pop-2", "pop", t_geo - 0.28, 0.28), ("sfx-pop-3", "pop", t_fin - 0.28, 0.24)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
