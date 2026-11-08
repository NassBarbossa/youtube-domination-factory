"""Composition du clip 15 « Vous êtes des fainéants » (Formation 2 « Comment devenir riche », Nass seul), comp_lib thème ydf.

Troisième raison, dite les yeux dans la caméra : vous êtes des fainéants. L'imitation du spectateur (« ouais ouais t'as raison Nass, j'ai même pas fait ton exercice ») et vous n'allez pas passer à l'action.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 15, "« Vous êtes des fainéants »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 76
c.hook_html = 'JE TE LE DIS<br><b>À TOI PERSONNELLEMENT</b>'
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_N+"), (E[2], "SOLO_N"), (E[3], "SOLO_N+")]
t_fain = find("s1", "fainéants")
c.hook_fade = t_fain - 0.45
t_ouais, t_action, t_feignants = find("s3", "ouais"), find("s4", "passer"), find("s5", "feignants")
c.kwc("kw-fain", "VOUS ÊTES<br>DES FAINÉANTS", ORANGE, t_fain - 0.1, E[1] - 0.3, size=92)
c.kwc("kw-ouais", "« OUAIS OUAIS,<br>T'AS RAISON NASS »", MUTED, t_ouais - 0.2, t_action - 0.9, size=64, extra="font-style: italic;")
c.kwc("kw-action", "VOUS N'ALLEZ PAS<br>PASSER À L'ACTION", WHITE, t_action - 0.4, t_feignants - 0.8, size=72, anim="rise")
c.kwc("kw-chute", "DES FEIGNANTS.", ORANGE, t_feignants - 0.3, c.END_T + 0.45, size=78, top=1270)
SFX = [("sfx-pop-1", "pop", t_fain - 0.08, 0.32), ("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-whoosh-2", "whoosh", E[2] - 0.22, 0.26),
       ("sfx-pop-2", "pop", t_ouais - 0.18, 0.24), ("sfx-pop-3", "pop", t_action - 0.38, 0.26), ("sfx-pop-4", "pop", t_feignants - 0.28, 0.32)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
