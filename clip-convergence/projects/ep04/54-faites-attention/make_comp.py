"""Composition du clip 54 « Faites attention » (Convergence EP.04, Nass seul), comp_lib v6, monologue.

La clôture : semaine difficile, trading très difficile, « faites attention si vous ne savez pas ce que vous faites, c'est très difficile de trader actuellement ». Investir : le gold est bien, il est déjà en train de repartir. Plein cadre.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, INK, GREEN, GOLD, GOLD_TXT, GREY, RED, solo, solo_screen  # noqa: E402

c = Comp(HERE, 54, "« Faites attention »", cta="Épisode 4 complet sur la chaîne")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 104
c.hook_html = 'FAITES<br><b>ATTENTION</b>'
c.fix = {("s1", "limité"): ""}
c.moves = [(E[0], "SOLO_N+")]
t_connaissez, t_investir, t_deja = find("s1", "connaissez"), find("s2", "investir"), find("s2", "déjà")
c.hook_fade = t_connaissez - 0.45
c.kwc("kw-savez", "SI VOUS NE SAVEZ PAS<br>CE QUE VOUS FAITES", RED, t_connaissez - 0.1, E[0] - 0.3, size=60)
c.kwc("kw-investir", "INVESTIR :", GREY, t_investir - 0.2, t_deja - 0.9, size=80, top=1270)
c.kwc("kw-chute", "LE GOLD EST DÉJÀ<br>EN TRAIN DE REPARTIR", GOLD_TXT, t_deja - 0.3, c.END_T + 0.45, size=62, anim="rise")
SFX = [("sfx-pop-1", "pop", t_connaissez - 0.08, 0.26), ("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-2", "pop", t_investir - 0.18, 0.26), ("sfx-pop-3", "pop", t_deja - 0.28, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
