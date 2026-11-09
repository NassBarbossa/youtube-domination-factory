"""Composition du clip 14 « 9 ans focus crypto » (Formation 2 « Comment devenir riche », Nass seul), comp_lib thème ydf.

Sa réponse à l'objet brillant : 9 ans focus crypto, avec des très hauts et des très bas, une seule chose. Deuxième raison : les réseaux ont rendu la génération incapable de faire les choses.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 14, "« 9 ans focus crypto »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf", end="outro")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 76
c.hook_html = '9 ANS FOCUS<br><b>CRYPTO, CRYPTO, CRYPTO</b>'
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_N+"), (E[2], "SOLO_N")]
t_hauts, t_une, t_bete, t_abrutie = find("s2", "hauts"), find("s2", "une"), find("s3", "bête"), find("s4", "abrutie")
c.kwc("kw-hauts", "DES TRÈS HAUTS,<br>DES TRÈS BAS", CYAN, t_hauts - 0.5, t_une - 0.6, size=80)
c.kwc("kw-une", "FOCUS SUR<br>UNE CHOSE", ORANGE, t_une - 0.3, t_bete - 0.9, size=92)
c.kwc("kw-bete", "ON VOUS A RENDU<br>INCAPABLES DE FAIRE", WHITE, t_bete - 0.6, t_abrutie - 0.8, size=68)
c.kwc("kw-chute", "ET DU COUP,<br>ON NE FAIT PAS", RED_Y, t_abrutie - 0.3, c.END_T + 0.45, size=84, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_hauts - 0.48, 0.26), ("sfx-pop-2", "pop", t_une - 0.28, 0.3),
       ("sfx-whoosh-2", "whoosh", E[2] - 0.22, 0.26), ("sfx-pop-3", "pop", t_bete - 0.58, 0.26), ("sfx-pop-4", "pop", t_abrutie - 0.28, 0.28)]
c.sfx = SFX   # la fin « outro » ajoute ses propres sons
c.build()
