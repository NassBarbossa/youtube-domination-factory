"""Composition du clip 64 « L'investissement c'est facile, le trading c'est dur » (Convergence EP.03, replay YouTube 720p), comp_lib v6.

Question du chat : est-ce que c'est dur le trading ? Nass : l'investissement c'est facile, le trading c'est dur. Sadek : totalement d'accord, très difficile, émotionnellement (« si des fois je suis un peu à cran, c'est que c'est très difficile »), jamais il dira que c'est facile ; par contre quand ça paye et que tu sais minimiser ton exposition, c'est génial. Son trade en lots (34:58) reste hors clip.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, INK, GREEN, GOLD, GOLD_TXT, GREY, RED, screen_only, solo, solo_screen, sym, sym_screen  # noqa: E402

c = Comp(HERE, 64, "« L'investissement c'est facile, le trading c'est dur »", cta="Épisode 3 complet sur la chaîne")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["E"] = sym_screen(480, 520, 900, 506)
S["E+"] = sym_screen(500, 520, 900, 506)
S["SOLO_E"] = solo_screen(860, 900, 506)
S["SOLO_E+"] = solo_screen(880, 900, 506)
c.hook_font = 60
c.hook_html = "L'INVESTISSEMENT C'EST FACILE,<br><b>LE TRADING C'EST DUR</b>"
c.moves = [(E[0], "SOLO_S"), (E[1], "SOLO_S+")]
t_emotion, t_jamais, t_genial = find("s2", "Émotionnellement"), find("s3", "Jamais"), find("s3", "génial")
c.kwc("kw-emotion", "ÉMOTIONNELLEMENT<br>TRÈS DIFFICILE", RED, t_emotion - 0.2, E[1] - 0.3, size=66)
c.kwc("kw-jamais", "JAMAIS JE NE DIRAI<br>QUE C'EST FACILE", INK, t_jamais - 0.2, t_genial - 1.3, size=60)
c.kwc("kw-chute", "QUAND ÇA PAYE :<br>C'EST GÉNIAL", GREEN, t_genial - 1.1, c.END_T + 0.45, size=76, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_emotion - 0.18, 0.26), ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26),
       ("sfx-pop-2", "pop", t_jamais - 0.18, 0.26), ("sfx-pop-3", "pop", t_genial - 0.28, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
