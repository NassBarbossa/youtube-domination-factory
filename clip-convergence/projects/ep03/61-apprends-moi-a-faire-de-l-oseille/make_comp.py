"""Composition du clip 61 « Apprends-moi à faire de l'oseille » (Convergence EP.03, replay YouTube 720p), comp_lib v6.

Question du chat lue par Nass : deux points de vue ; Sadek, focalisez-vous sur le trading ; Nass, développer des compétences monnayables, une activité digitale, et pendant que vous charbonnez, un pourcentage de vos rentrées dans les marchés : l'or, le Bitcoin, le S&P 500. Coupe de « partir de la France… en Asie avec 600–800 € » (30:04–30:33).
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, INK, GREEN, GOLD, GOLD_TXT, GREY, RED, screen_only, solo, solo_screen, sym, sym_screen  # noqa: E402

c = Comp(HERE, 61, "« Apprends-moi à faire de l'oseille »", cta="Épisode 3 complet sur la chaîne")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["E"] = sym_screen(480, 520, 900, 506)
S["E+"] = sym_screen(500, 520, 900, 506)
S["SOLO_E"] = solo_screen(860, 900, 506)
S["SOLO_E+"] = solo_screen(880, 900, 506)
c.hook_font = 72
c.hook_html = "APPRENDS-MOI À FAIRE<br><b>DE L'OSEILLE</b>"
c.fix = {("s4", "SP500"): "S&P 500"}
S["H"] = solo("nass", 760)   # fauteuil de Sadek vide sur ce passage (aucun visage détecté) : Nass seul
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_N+"), (E[2], "SOLO_N")]
t_deux, t_trading, t_competences, t_pourcentage, t_or = find("s1", "deux"), find("s2", "trading"), find("s3", "compétences"), find("s4", "pourcentage"), find("s4", "or,")
c.kwc("kw-deux", "DEUX POINTS DE VUE", GREY, t_deux - 0.2, E[0] - 0.3, size=76, top=1270)
c.kwc("kw-trading", "SADEK :<br>LE TRADING", INK, t_trading - 0.2, E[1] - 0.3, size=72)
c.kwc("kw-competences", "MOI : DES COMPÉTENCES<br>MONNAYABLES", INK, t_competences - 0.2, E[2] - 0.3, size=60)
c.kwc("kw-pourcentage", "UN POURCENTAGE<br>DANS LES MARCHÉS", GREY, t_pourcentage - 0.2, t_or - 0.9, size=66)
c.kwc("kw-chute", "L'OR, LE BITCOIN,<br>LE S&amp;P 500", GOLD_TXT, t_or - 0.3, c.END_T + 0.45, size=72, anim="rise")
SFX = [("sfx-pop-1", "pop", t_deux - 0.18, 0.26), ("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-2", "pop", t_trading - 0.18, 0.26),
       ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26), ("sfx-pop-3", "pop", t_competences - 0.18, 0.26), ("sfx-whoosh-3", "whoosh", E[2] - 0.22, 0.26),
       ("sfx-pop-4", "pop", t_pourcentage - 0.18, 0.26), ("sfx-pop-5", "pop", t_or - 0.28, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
