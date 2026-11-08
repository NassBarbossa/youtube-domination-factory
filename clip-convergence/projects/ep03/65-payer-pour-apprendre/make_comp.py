"""Composition du clip 65 « Payer pour apprendre ? » (Convergence EP.03, replay YouTube 720p), comp_lib v6.

Sadek : you have to pay to learn, ça dépend avec qui ; ceux qui ne veulent pas payer paieront plus cher au final, en temps ; rien contre la gratuité, c'est votre argent, ça dépend si vous avez du capital. Puis : contre le copy trading, « ce n'est pas du tout ce que je veux pour vous, je veux transmettre et que vous soyez autonomes ». « J'en fournis parce que c'est un service qui vous intéresse » (37:41–37:47, son offre) reste hors clip.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, INK, GREEN, GOLD, GOLD_TXT, GREY, RED, screen_only, solo, solo_screen, sym, sym_screen  # noqa: E402

c = Comp(HERE, 65, "« Payer pour apprendre ? »", cta="Épisode 3 complet sur la chaîne")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["E"] = sym_screen(480, 520, 900, 506)
S["E+"] = sym_screen(500, 520, 900, 506)
S["SOLO_E"] = solo_screen(860, 900, 506)
S["SOLO_E+"] = solo_screen(880, 900, 506)
c.hook_font = 92
c.hook_html = 'PAYER<br><b>POUR APPRENDRE ?</b>'
c.moves = [(E[0], "SOLO_S+"), (E[2], "SOLO_S"), (E[3], "SOLO_S+")]
t_payer, t_gratuite, t_copy, t_autonome = find("s2", "payer"), find("s3", "gratuité"), find("s4", "copy"), find("s5", "autonome")
c.kwc("kw-payer", "VOUS PAIEREZ PLUS CHER :<br>EN TEMPS", RED, t_payer - 0.2, E[1] - 0.3, size=58)
c.kwc("kw-gratuite", "RIEN CONTRE<br>LA GRATUITÉ", GREY, t_gratuite - 0.2, E[2] - 0.3, size=72)
c.kwc("kw-copy", "CONTRE LE<br>COPY TRADING", INK, t_copy - 0.2, t_autonome - 1.5, size=72)
c.kwc("kw-chute", "JE VEUX QUE VOUS<br>SOYEZ AUTONOMES", GREEN, t_autonome - 1.3, c.END_T + 0.45, size=68, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_payer - 0.18, 0.26), ("sfx-whoosh-2", "whoosh", E[2] - 0.22, 0.26),
       ("sfx-pop-2", "pop", t_gratuite - 0.18, 0.26), ("sfx-whoosh-3", "whoosh", E[3] - 0.22, 0.26), ("sfx-pop-3", "pop", t_copy - 0.18, 0.26), ("sfx-pop-4", "pop", t_autonome - 0.28, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
