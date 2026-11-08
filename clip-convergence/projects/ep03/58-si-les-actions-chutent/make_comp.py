"""Composition du clip 58 « Si les actions chutent ? » (Convergence EP.03, replay YouTube 720p), comp_lib v6.

Nass demande les corrélations ; Sadek : si les actions chutent, il voit l'or monter, le Bitcoin continuer une montée tranquille en escalier, une rotation de liquidités ; les actions ne chutent jamais vraiment, elles corrigent. Coupe avant « vous ne reverrez jamais le NAS100 à 16 000 » (certitude).
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, INK, GREEN, GOLD, GOLD_TXT, GREY, RED, screen_only, solo, solo_screen, sym, sym_screen  # noqa: E402

c = Comp(HERE, 58, "« Si les actions chutent ? »", cta="Épisode 3 complet sur la chaîne")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["E"] = sym_screen(480, 520, 900, 506)
S["E+"] = sym_screen(500, 520, 900, 506)
S["SOLO_E"] = solo_screen(860, 900, 506)
S["SOLO_E+"] = solo_screen(880, 900, 506)
c.hook_font = 92
c.hook_html = 'SI LES ACTIONS<br><b>CHUTENT ?</b>'
c.moves = [(E[0], "SOLO_S"), (E[1], "SOLO_S+")]   # Sadek seul dès sa réponse : les mots clés vivent dans la bande solo
t_or, t_bitcoin, t_rotation, t_corrigent = find("s2", "or"), find("s2", "bitcoin"), find("s3", "rotation"), find("s3", "corrigent")
c.kwc("kw-or", "L'OR MONTE", GOLD_TXT, t_or - 0.2, t_bitcoin - 0.9, size=84, top=1270)
c.kwc("kw-bitcoin", "LE BITCOIN<br>EN ESCALIER", INK, t_bitcoin - 0.2, E[1] - 0.3, size=72)
c.kwc("kw-rotation", "UNE ROTATION<br>DE LIQUIDITÉS", GREY, t_rotation - 0.2, t_corrigent - 0.9, size=70)
c.kwc("kw-chute", "LES ACTIONS NE CHUTENT PAS,<br>ELLES CORRIGENT", GREEN, t_corrigent - 0.3, c.END_T + 0.45, size=58, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_or - 0.18, 0.26), ("sfx-pop-2", "pop", t_bitcoin - 0.18, 0.26),
       ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26), ("sfx-pop-3", "pop", t_rotation - 0.18, 0.26), ("sfx-pop-4", "pop", t_corrigent - 0.28, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
