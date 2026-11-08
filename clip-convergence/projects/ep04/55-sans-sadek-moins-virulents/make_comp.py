"""Composition du clip 55 « Sans Sadek, vous êtes moins virulents » (Convergence EP.04, Nass seul), comp_lib v6, monologue.

Teaser : fin de la revue de marché, place au trade de la semaine ; « aujourd'hui on n'est pas sur TikTok avec Sadek, donc vous êtes un peu moins virulents et actifs dans vos questions », mais sur Twitch, allez-y. Caméra seule.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, INK, GREEN, GOLD, GOLD_TXT, GREY, RED, solo, solo_screen  # noqa: E402

c = Comp(HERE, 55, "« Sans Sadek, vous êtes moins virulents »", cta="Épisode 4 complet sur la chaîne")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = 'SANS SADEK,<br><b>MOINS VIRULENTS</b>'
c.moves = [(E[0], "SOLO_N+")]
t_virulent, t_twitch = find("s2", "virulent"), find("s2", "Twitch")
c.hook_fade = t_virulent - 0.45
c.kwc("kw-virulent", "MOINS VIRULENTS,<br>MOINS ACTIFS", GREY, t_virulent - 0.1, t_twitch - 0.9, size=66)
c.kwc("kw-chute", "VOS QUESTIONS<br>SUR TWITCH", GREEN, t_twitch - 0.2, c.END_T + 0.45, size=72, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_virulent - 0.08, 0.26), ("sfx-pop-2", "pop", t_twitch - 0.18, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
