"""Composition du clip 14 « La formation la plus aboutie que j'ai faite » (Formation 3 « L'investissement on-chain », Nass seul), comp_lib thème ydf.

« C'est un peu prétentieux, mais je pense que c'est la formation la plus aboutie que j'ai faite » : trois vidéos de 10 minutes ultra condensées, et la peur qu'on banalise l'information. La slide « Fin de cette formation offerte » sous lui.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 14, "« La formation la plus aboutie que j'ai faite »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf", end="outro")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = 'LA FORMATION<br><b>LA PLUS ABOUTIE</b>'
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_N+")]
t_pret, t_about, t_trois, t_peur, t_pouvez = find("s2", "prétentieux"), find("s2", "formation"), find("s2", "trois"), find("s3", "peur"), find("s3", "pouvez")
c.kwc("kw-pret", "« UN PEU PRÉTENTIEUX,<br>MAIS… »", MUTED, t_pret - 0.2, t_about - 1.1, size=60, extra="font-style: italic;")
c.kwc("kw-about", "LA PLUS ABOUTIE", ORANGE, t_about - 0.2, t_trois - 0.9, size=84, top=1270)
c.kwc("kw-trois", "3 VIDÉOS × 10 MIN,<br>ULTRA CONDENSÉES", WHITE, t_trois - 0.3, t_peur - 0.9, size=64)
c.kwc("kw-peur", "NE BANALISEZ PAS<br>L'INFORMATION", RED_Y, t_peur - 0.2, t_pouvez - 1.0, size=72)
c.kwc("kw-chute", "VOUS POUVEZ ALLER<br>TELLEMENT LOIN", ORANGE, t_pouvez - 0.2, c.END_T + 0.45, size=72, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-0", "pop", t_about - 0.18, 0.26), ("sfx-pop-1", "pop", t_trois - 0.28, 0.26),
       ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26), ("sfx-pop-2", "pop", t_peur - 0.18, 0.26), ("sfx-pop-3", "pop", t_pouvez - 0.18, 0.3)]
c.sfx = SFX   # la fin « outro » ajoute ses propres sons
c.build()
