"""Composition du clip 53 « Baissier ? Pas en investissement » (Convergence EP.04, Nass seul), comp_lib v6, monologue.

Il a du mal à comprendre ceux qui sont baissiers sur l'or : en time frame mineur, ok ; en investissement, non. Et le contexte : les cryptos sont fortement reliées au Nasdaq, avec la hausse des taux potentielle, la guerre et les mid-terms qui arrivent. Plein cadre.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, INK, GREEN, GOLD, GOLD_TXT, GREY, RED, solo, solo_screen  # noqa: E402

c = Comp(HERE, 53, "« Baissier ? Pas en investissement »", cta="Épisode 4 complet sur la chaîne")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 72
c.hook_html = "BAISSIER SUR L'OR ?<br><b>PAS EN INVESTISSEMENT</b>"
c.fix = {("s1", "baissés"): "baissiers"}
c.moves = [(E[0], "SOLO_N+")]
t_tu, t_invest, t_relies, t_taux = find("s1", "tu"), find("s1", "investissement"), find("s2", "reliés"), find("s2", "taux")
c.hook_fade = t_tu - 0.45
c.kwc("kw-mineur", "TIME FRAME MINEUR :<br>OK", GREY, t_tu - 0.1, t_invest - 0.9, size=66)
c.kwc("kw-invest", "EN INVESTISSEMENT :<br>J'AI DU MAL", INK, t_invest - 0.2, E[0] - 0.3, size=66)
c.kwc("kw-relies", "CRYPTO ET NASDAQ :<br>FORTEMENT RELIÉS", GREEN, t_relies - 0.2, t_taux - 0.9, size=60)
c.kwc("kw-chute", "TAUX, GUERRE,<br>MID-TERMS", GREY, t_taux - 0.3, c.END_T + 0.45, size=72, anim="rise")
SFX = [("sfx-pop-1", "pop", t_tu - 0.08, 0.26), ("sfx-pop-2", "pop", t_invest - 0.18, 0.26), ("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3),
       ("sfx-pop-3", "pop", t_relies - 0.18, 0.26), ("sfx-pop-4", "pop", t_taux - 0.28, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
