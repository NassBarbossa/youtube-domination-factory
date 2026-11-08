"""Composition du clip 50 « Encore un lundi noir ? » (Convergence EP.04, Nass seul), comp_lib v6, monologue.

Le programme : revue de marché. On avait annoncé un lundi noir la semaine dernière, au final plutôt ok en début de semaine, puis ça s'est gâté en fin de semaine : « est-ce qu'on a encore un lundi noir ou pas ? » Teaser de l'épisode, plein cadre.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, INK, GREEN, GOLD, GOLD_TXT, GREY, RED, solo, solo_screen  # noqa: E402

c = Comp(HERE, 50, "« Encore un lundi noir ? »", cta="Épisode 4 complet sur la chaîne")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 92
c.hook_html = 'ENCORE<br><b>UN LUNDI NOIR ?</b>'
c.moves = [(E[0], "SOLO_N+")]
t_annonce, t_ok, t_gate, t_encore = find("s2", "annoncé"), find("s2", "ok"), find("s2", "gâté"), find("s2", "encore")
c.hook_fade = t_annonce - 0.45
c.kwc("kw-annonce", "UN LUNDI NOIR<br>ANNONCÉ", GREY, t_annonce - 0.1, t_ok - 0.9, size=72)
c.kwc("kw-ok", "PLUTÔT OK<br>EN DÉBUT DE SEMAINE", INK, t_ok - 0.2, t_gate - 0.9, size=62)
c.kwc("kw-gate", "ÇA S'EST GÂTÉ", RED, t_gate - 0.2, t_encore - 0.9, size=80, top=1270)  # 1,7 s à l'écran : trois mots
c.kwc("kw-chute", "ENCORE UN<br>LUNDI NOIR ?", GREEN, t_encore - 0.3, c.END_T + 0.45, size=84, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_annonce - 0.08, 0.26), ("sfx-pop-2", "pop", t_ok - 0.18, 0.26),
       ("sfx-pop-3", "pop", t_gate - 0.18, 0.26), ("sfx-pop-4", "pop", t_encore - 0.28, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
