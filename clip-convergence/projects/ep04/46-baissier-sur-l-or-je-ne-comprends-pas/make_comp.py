"""Composition du clip 46 « Baissier sur l'or ? Je ne comprends pas » (Convergence EP.04, Nass seul), comp_lib v6, monologue.

Certains sont baissiers sur l'or : il ne comprend pas, personnellement, d'être baissier sur un support comme ça avec le contexte fondamental (guerre qui reprend, macro pas bien, la Russie). « Je ne vois pas pourquoi je serais baissier sur l'or à ce niveau-là. » Son écran or sous lui pendant le contexte. Partage 8 s avec le 45.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, INK, GREEN, GOLD, GOLD_TXT, GREY, RED, solo, solo_screen  # noqa: E402

c = Comp(HERE, 46, "« Baissier sur l'or ? Je ne comprends pas »", cta="Épisode 4 complet sur la chaîne")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 72
c.hook_html = "BAISSIER SUR L'OR ?<br><b>JE NE COMPRENDS PAS</b>"
c.fix = {("s1", "baissés"): "baissiers", ("s1", "goal"): "gold", ("s1", "baissé"): "baissier", ("s2", "bériche"): "baissier"}
t_support, t_pourquoi = find("s1", "support"), find("s2", "pourquoi")
c.moves = [(E[0], "SOLO_E"), (t_pourquoi - 0.7, "SOLO_N+")]
c.screen_windows = [(E[0], t_pourquoi - 0.7)]
c.hook_fade = t_support - 0.45
c.kwc("kw-support", "SUR UN SUPPORT ?", INK, t_support - 0.1, E[0] - 0.3, size=80, top=1270)
c.kwc("kw-chute", "PAS BAISSIER SUR L'OR<br>À CE NIVEAU-LÀ", GREEN, t_pourquoi - 0.1, c.END_T + 0.45, size=62, anim="rise")
SFX = [("sfx-pop-1", "pop", t_support - 0.08, 0.26), ("sfx-whoosh-1", "whoosh", E[0] - 0.22, 0.3), ("sfx-whoosh-2", "whoosh", t_pourquoi - 0.92, 0.26), ("sfx-pop-2", "pop", t_pourquoi - 0.08, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
