"""Composition du clip 57 « Pile ou face » (Convergence EP.03, replay YouTube 720p), comp_lib v6.

Sadek sur le range : « on s'est fait éclater » la semaine d'avant, trop d'indécision, à l'achat comme à la vente tu es touché, c'est pile ou face ; décision de se concentrer sur l'éducatif ; « j'ai pas envie de trader tant qu'on sort pas de cette zone, j'ai besoin d'une tendance ». Coupe de « je pourrais te montrer les retraits » (19:06–19:18).
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, INK, GREEN, GOLD, GOLD_TXT, GREY, RED, screen_only, solo, solo_screen, sym, sym_screen  # noqa: E402

c = Comp(HERE, 57, "« Pile ou face »", cta="Épisode 3 complet sur la chaîne")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["E"] = sym_screen(480, 520, 900, 506)
S["E+"] = sym_screen(500, 520, 900, 506)
S["SOLO_E"] = solo_screen(860, 900, 506)
S["SOLO_E+"] = solo_screen(880, 900, 506)
c.hook_font = 104
c.hook_html = 'PILE<br><b>OU FACE</b>'
S["H"] = solo("sadek", 760)   # Nass est penché hors de sa caméra sur tout le passage : Sadek seul
c.fix = {("s1", "?"): ""}
c.moves = [(E[0], "SOLO_S"), (E[1], "SOLO_S+"), (E[2], "SOLO_S")]
t_indecision, t_pile, t_educatif, t_besoin = find("s2", "indécision"), find("s2", "pile"), find("s3", "éducatif"), find("s4", "besoin")
c.kwc("kw-indecision", "TROP<br>D'INDÉCISION", GREY, t_indecision - 0.2, t_pile - 0.9, size=72)
c.kwc("kw-pile", "PILE OU FACE", RED, t_pile - 0.2, t_pile + 1.4, size=84, top=1270)
c.kwc("kw-educatif", "PLUS D'ÉDUCATIF", INK, t_educatif - 0.2, E[2] - 0.3, size=76, top=1270)
c.kwc("kw-chute", "J'AI BESOIN<br>D'UNE TENDANCE", GREEN, t_besoin - 0.3, c.END_T + 0.45, size=76, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_indecision - 0.18, 0.26), ("sfx-pop-2", "pop", t_pile - 0.18, 0.3),
       ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26), ("sfx-pop-3", "pop", t_educatif - 0.18, 0.26), ("sfx-whoosh-3", "whoosh", E[2] - 0.22, 0.26), ("sfx-pop-4", "pop", t_besoin - 0.28, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
