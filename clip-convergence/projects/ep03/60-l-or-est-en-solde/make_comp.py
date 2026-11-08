"""Composition du clip 60 « L'or est en solde » (Convergence EP.03, replay YouTube 720p), comp_lib v6.

Sadek : pas une question de zone, une question de moment ; en investissement, acheter de l'or à ce prix est un très bon prix, en trading avec peu de marge de manœuvre, attention. Nass sur son graphique : du point haut on est sur une correction de 30 %, « les soldes » entre guillemets ; en achat long terme, se positionner là n'est pas très risqué ; le prix d'entrée exact n'est pas le plus important quand vous êtes investisseur. Reprise en DA du pilote 08 (validé le 2026-10-25). « L'or n'ira pas à 2 100, c'est impossible » (24:51) et la guerre atomique restent hors clip.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, INK, GREEN, GOLD, GOLD_TXT, GREY, RED, screen_only, solo, solo_screen, sym, sym_screen  # noqa: E402

c = Comp(HERE, 60, "« L'or est en solde »", cta="Épisode 3 complet sur la chaîne")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["E"] = sym_screen(480, 520, 900, 506)
S["E+"] = sym_screen(500, 520, 900, 506)
S["SOLO_E"] = solo_screen(860, 900, 506)
S["SOLO_E+"] = solo_screen(880, 900, 506)
c.hook_font = 104
c.hook_html = "L'OR EST<br><b>EN SOLDE</b>"
SCR = screen_only(900, 506)   # Nass est hors de sa caméra sur s3-s4 : son écran seul, mots clés dans la zone haute
S["SCR"] = SCR
c.screen_state = "SCR"
TOP = SCR["kw_top"]
t_moment, t_trading, t_soldes, t_important = find("s1", "moment"), find("s2", "trading"), find("s3", "soldes"), find("s5", "important")
c.moves = [(t_moment - 0.3, "SOLO_S"), (E[0], "SOLO_S+"), (E[1], "SCR"), (E[3], "SOLO_N+")]
c.screen_windows = [(E[1], E[3])]
c.punch([seams[2]])
c.hook_fade = t_moment - 0.45
t_correction = find("s3", "correction")
c.kwc("kw-correction", "UNE CORRECTION", GREY, t_correction - 0.2, t_soldes - 0.9, size=92, top=TOP + 100)
c.kwc("kw-soldes", "« LES SOLDES »", GOLD_TXT, t_soldes - 0.2, E[3] - 0.3, size=100, top=TOP + 100)
c.kwc("kw-moment", "UNE QUESTION<br>DE MOMENT", INK, t_moment - 0.1, E[0] - 0.3, size=72)
c.kwc("kw-trading", "EN TRADING :<br>ATTENTION", RED, t_trading - 0.2, E[1] - 0.3, size=72)
c.kwc("kw-chute", "PAS LE PLUS IMPORTANT<br>QUAND VOUS INVESTISSEZ", GREEN, t_important - 0.3, c.END_T + 0.45, size=58, anim="rise")
SFX = [("sfx-pop-1", "pop", t_moment - 0.08, 0.26), ("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-2", "pop", t_trading - 0.18, 0.26),
       ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.3), ("sfx-whoosh-3", "whoosh", E[3] - 0.22, 0.26), ("sfx-pop-3", "pop", t_important - 0.28, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
