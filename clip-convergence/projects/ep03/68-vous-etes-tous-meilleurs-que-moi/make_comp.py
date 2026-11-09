"""Composition du clip 68 « Vous êtes tous meilleurs que moi » (Convergence EP.03, replay YouTube 720p), comp_lib v6.

Sadek, dernière question : ça ne sert à rien de demander ce qu'on pense d'un tel ou un tel ; il ne répondra jamais, « vous êtes tous des bons et moi je suis là pour être le meilleur » ; « vous êtes tous meilleurs que moi, moi je suis là pour être meilleur que vous ». Sadek seul (Nass en punk).
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, INK, GREEN, GOLD, GOLD_TXT, GREY, RED, screen_only, solo, solo_screen, sym, sym_screen  # noqa: E402

c = Comp(HERE, 68, "« Vous êtes tous meilleurs que moi »", cta="Épisode 3 complet sur la chaîne")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("sadek", 760)
S["SOLO_E"] = solo_screen(860, 900, 506, cam="sadek")
c.hook_font = 80
c.hook_html = 'VOUS ÊTES TOUS<br><b>MEILLEURS QUE MOI</b>'
c.moves = [(E[0], "SOLO_S"), (E[1], "SOLO_S+")]
t_bons, t_meilleur, t_moi = find("s2", "bons"), find("s2", "meilleur"), find("s3", "moi")
c.kwc("kw-bons", "VOUS ÊTES<br>TOUS DES BONS", GREY, t_bons - 0.2, t_meilleur - 0.9, size=72)
c.kwc("kw-meilleur", "MOI, JE SUIS LÀ<br>POUR ÊTRE LE MEILLEUR", INK, t_meilleur - 0.2, E[1] - 0.3, size=58)
c.kwc("kw-chute", "MEILLEUR<br>QUE VOUS", GREEN, t_moi - 0.3, c.END_T + 0.45, size=84, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_bons - 0.18, 0.26), ("sfx-pop-2", "pop", t_meilleur - 0.18, 0.26),
       ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26), ("sfx-pop-3", "pop", t_moi - 0.28, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
