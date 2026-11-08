"""Composition du clip 43 « Le bottom parfait, c'est par chance » (Convergence EP.04, Nass seul), comp_lib v6, monologue.

Acheter parfaitement au bottom : à posteriori c'est évident, dans l'action ça ne se passe pas comme ça. Revendre les parfaits sommets et acheter les parfaits bottoms, « quand vous êtes dans le feu de l'action, si vous arrivez à le faire, c'est uniquement par chance ». Coupe du « enlève-moi du replay » (04:03–04:11). Son écran SOL sous lui.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, INK, GREEN, GOLD, GOLD_TXT, GREY, RED, solo, solo_screen  # noqa: E402

c = Comp(HERE, 43, "« Le bottom parfait, c'est par chance »", cta="Épisode 4 complet sur la chaîne")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = 'ACHETER<br><b>LE BOTTOM PARFAIT ?</b>'
c.moves = [(E[0], "SOLO_E"), (E[1], "SOLO_N+")]
c.screen_windows = [(E[0], E[1])]
t_semaines, t_feu, t_chance = find("s3", "semaines"), find("s3", "feu"), find("s3", "chance")
c.kwc("kw-semaines", "ÉVIDENT…<br>DES SEMAINES APRÈS", GREY, t_semaines - 0.2, t_feu - 0.9, size=66)
c.kwc("kw-feu", "DANS LE FEU<br>DE L'ACTION", INK, t_feu - 0.2, t_chance - 0.9, size=70)
c.kwc("kw-chute", "UNIQUEMENT<br>PAR CHANCE", GREEN, t_chance - 0.3, c.END_T + 0.45, size=84, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh", E[0] - 0.22, 0.3), ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26), ("sfx-pop-1", "pop", t_semaines - 0.18, 0.26),
       ("sfx-pop-2", "pop", t_feu - 0.18, 0.26), ("sfx-pop-3", "pop", t_chance - 0.28, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
