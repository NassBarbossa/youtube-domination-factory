"""Composition du clip 44 « J'ai vendu à 115 et j'ai tenu » (Convergence EP.04, Nass seul), comp_lib v6, monologue.

Transparence : il avait partagé sur Telegram avoir vendu 70-80 % de ses SOL à 115 $. Ça a continué de monter, il n'a pas paniqué, il a tenu ; maintenant on est 15-20 % sous sa vente, et il pense re-rentrer une partie parce qu'il reste fondamentalement haussier à moyen terme. Son écran SOL sous lui. « Je vais attendre demain » laissé hors clip.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, INK, GREEN, GOLD, GOLD_TXT, GREY, RED, solo, solo_screen  # noqa: E402

c = Comp(HERE, 44, "« J'ai vendu à 115 et j'ai tenu »", cta="Épisode 4 complet sur la chaîne")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = "J'AI VENDU À 115.<br><b>ET J'AI TENU.</b>"
c.fix = {("s1", "soldes."): "SOL."}
c.moves = [(E[0], "SOLO_E"), (E[1], "SOLO_N+")]
c.screen_windows = [(E[0], E[1])]
t_partie, t_fond = find("s3", "partie"), find("s3", "fondamentalement")
c.kwc("kw-partie", "RE-RENTRER<br>UNE PARTIE", GREY, t_partie - 0.2, t_fond - 0.9, size=70)
c.kwc("kw-chute", "FONDAMENTALEMENT HAUSSIER<br>SUR LE MOYEN TERME", GREEN, t_fond - 0.3, c.END_T + 0.45, size=56, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh", E[0] - 0.22, 0.3), ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26), ("sfx-pop-1", "pop", t_partie - 0.18, 0.26), ("sfx-pop-2", "pop", t_fond - 0.28, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
