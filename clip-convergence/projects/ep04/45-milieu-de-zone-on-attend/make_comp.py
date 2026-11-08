"""Composition du clip 45 « Milieu de zone ? On attend » (Convergence EP.04, Nass seul), comp_lib v6, monologue.

L'or en milieu de zone : c'est toujours plus difficile de prendre des positions, autant attendre les hauts ou les bas de zone. On se rapproche du bas du range. Il voit des gens baissiers, ni tort ni raison, mais il ne comprend pas d'être baissier sur un support comme ça. Son écran or sous lui.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, INK, GREEN, GOLD, GOLD_TXT, GREY, RED, solo, solo_screen  # noqa: E402

c = Comp(HERE, 45, "« Milieu de zone ? On attend »", cta="Épisode 4 complet sur la chaîne")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 92
c.hook_html = 'MILIEU DE ZONE ?<br><b>ON ATTEND.</b>'
c.fix = {("s3", "baissés"): "baissiers", ("s3", "goal"): "gold", ("s3", "baissé"): "baissier", ("s1", "hautes"): "hauts", ("s1", "zones"): "de zone"}
c.moves = [(E[0], "SOLO_E"), (E[1], "SOLO_N+")]
c.screen_windows = [(E[0], E[1])]
t_difficile, t_autant, t_tort, t_comprends = find("s1", "difficile"), find("s1", "autant"), find("s3", "tort"), find("s3", "comprends")
c.hook_fade = t_difficile - 0.45
c.kwc("kw-bords", "MILIEU DE ZONE : DIFFICILE.<br>LES HAUTS OU LES BAS", INK, t_difficile - 0.1, E[0] - 0.3, size=60)  # « difficile » et « autant » à 0,9 s : un seul mot clé
c.kwc("kw-tort", "NI TORT,<br>NI RAISON", GREY, t_tort - 0.2, t_comprends - 0.9, size=72)
c.kwc("kw-chute", "BAISSIER SUR UN SUPPORT ?<br>JE NE COMPRENDS PAS", GREEN, t_comprends - 0.3, c.END_T + 0.45, size=56, anim="rise")
SFX = [("sfx-pop-1", "pop", t_difficile - 0.08, 0.26), ("sfx-whoosh-1", "whoosh", E[0] - 0.22, 0.3),
       ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26), ("sfx-pop-3", "pop", t_tort - 0.18, 0.26), ("sfx-pop-4", "pop", t_comprends - 0.28, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
