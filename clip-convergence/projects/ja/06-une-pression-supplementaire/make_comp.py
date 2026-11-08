"""Composition du clip 6 « Une pression supplémentaire » (J'abandonne mon challenge crypto, Nass seul), comp_lib thème ydf.

Il se forçait : pas envie, mais la pression d'avancer sur un challenge affiché publiquement. Des trades sans envie, « tout ça pour pouvoir avancer sur mon challenge » : une pression supplémentaire. La slide « Je sors de mon style de trading » sous lui.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 6, "« Une pression supplémentaire »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = "LA PRESSION<br><b>DE S'AFFICHER</b>"
c.moves = [(E[0], "SOLO_N+")]
t_pression, t_affiche, t_envie, t_supp = find("s1", "pression"), find("s1", "afficher"), find("s2", "envie"), find("s2", "supplémentaire.")
c.hook_fade = t_pression - 0.45
c.kwc("kw-pression", "JE ME METTAIS<br>LA PRESSION", WHITE, t_pression - 0.1, t_affiche - 0.9, size=72)
c.kwc("kw-affiche", "EN TRAIN<br>DE M'AFFICHER", MUTED, t_affiche - 0.2, E[0] - 0.3, size=72)
c.kwc("kw-envie", "DES TRADES<br>SANS ENVIE", MUTED, t_envie - 0.3, t_supp - 0.9, size=72)
c.kwc("kw-chute", "UNE PRESSION<br>SUPPLÉMENTAIRE", ORANGE, t_supp - 0.4, c.END_T + 0.45, size=70, anim="rise")
SFX = [("sfx-pop-1", "pop", t_pression - 0.08, 0.26), ("sfx-pop-2", "pop", t_affiche - 0.18, 0.26), ("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3),
       ("sfx-pop-3", "pop", t_envie - 0.28, 0.26), ("sfx-pop-4", "pop", t_supp - 0.38, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
