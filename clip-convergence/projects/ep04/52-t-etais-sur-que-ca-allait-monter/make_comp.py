"""Composition du clip 52 « T'étais sûr que ça allait monter ? » (Convergence EP.04, Nass seul), comp_lib v6, monologue.

Sa règle : se placer dans le support, revendre à la résistance, sans chercher plus loin ; des invalidations, « si ça casse, je coupe, j'ai perdu, c'est comme ça ». Aux débutants qui demandent « t'étais sûr que ça allait monter ? » : « non, je ne sais pas », plus de chances de monter que de descendre. Écran Axiom hors clip : caméra seule.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, INK, GREEN, GOLD, GOLD_TXT, GREY, RED, solo, solo_screen  # noqa: E402

c = Comp(HERE, 52, "« T'étais sûr que ça allait monter ? »", cta="Épisode 4 complet sur la chaîne")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 76
c.hook_html = "T'ÉTAIS SÛR QUE<br><b>ÇA ALLAIT MONTER ?</b>"
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_N+")]
t_casser, t_perdu, t_non, t_plus = find("s2", "casser"), find("s2", "perdu"), find("s3", "non"), find("s3", "plus")
c.kwc("kw-casser", "SI ÇA CASSE :<br>JE COUPE", RED, t_casser - 0.2, t_perdu - 0.9, size=72)
c.kwc("kw-perdu", "J'AI PERDU.<br>C'EST COMME ÇA.", GREY, t_perdu - 0.2, E[1] - 0.3, size=66)
c.kwc("kw-non", "NON.<br>JE NE SAIS PAS.", INK, t_non - 0.2, t_plus - 0.9, size=80)
c.kwc("kw-chute", "PLUS DE CHANCES DE MONTER<br>QUE DE DESCENDRE", GREEN, t_plus - 0.3, c.END_T + 0.45, size=56, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_casser - 0.18, 0.26), ("sfx-pop-2", "pop", t_perdu - 0.18, 0.26),
       ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26), ("sfx-pop-3", "pop", t_non - 0.18, 0.26), ("sfx-pop-4", "pop", t_plus - 0.28, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
