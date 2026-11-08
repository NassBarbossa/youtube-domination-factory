"""Composition du clip 10 « Arrêtez, allez travailler » (J'abandonne mon challenge crypto, Nass seul), comp_lib thème ydf.

Félicitations si vous êtes dans le top 20 %, plus fort que les 80 % qui perdent. Mais très honnêtement : 100 ou 200 dollars par mois en trading à plein temps, « arrêtez, allez travailler, c'est bien mieux pour vous ».
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 10, "« Arrêtez, allez travailler »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 76
c.hook_html = 'ARRÊTEZ,<br><b>ALLEZ TRAVAILLER</b>'
c.moves = [(E[0], "SOLO_N+")]
t_felic, t_fort, t_honn, t_arretez = find("s1", "félicitations"), find("s1", "fort"), find("s2", "honnêtement"), find("s2", "arrêtez")
c.hook_fade = t_fort - 0.45
c.kwc("kw-fort", "PLUS FORT QUE<br>LES 80 % QUI PERDENT", CYAN, t_fort - 0.1, t_honn - 0.9, size=60)
c.kwc("kw-honn", "TRÈS HONNÊTEMENT…", MUTED, t_honn - 0.2, t_arretez - 0.9, size=72, top=1270)
c.kwc("kw-chute", "ARRÊTEZ,<br>ALLEZ TRAVAILLER", ORANGE, t_arretez - 0.3, c.END_T + 0.45, size=80, anim="rise")
SFX = [("sfx-pop-1", "pop", t_fort - 0.08, 0.26), ("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-2", "pop", t_honn - 0.18, 0.26), ("sfx-pop-3", "pop", t_arretez - 0.28, 0.32)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
