"""Composition du clip 8 « Roberto Carlos a perdu 99 % » (Formation 1 « Pourquoi investir en 2026 », Nass seul), comp_lib thème ydf.

Roberto Carlos dit avoir perdu 99 % de sa fortune en gérant mal son argent ; en crypto, des gens montés à des centaines de millions ont tout perdu faute de cet exercice.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402

c = Comp(HERE, 8, "« Roberto Carlos a perdu 99 % »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf", end="outro")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = 'ROBERTO CARLOS :<br><b>« J\'AI PERDU 99 % »</b>'
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_N+"), (E[2], "SOLO_N"), (E[3], "SOLO_N+")]
t_rc = find("s1", "Roberto")
c.hook_fade = t_rc - 0.45
t_dizaines, t_perdu = find("s3", "dizaines"), find("s3", "perdu")
t_centaines = find("s4", "centaines")
t_tout = find("s5", "tout")
c.kwc("kw-rc", "ROBERTO CARLOS", ORANGE, t_rc - 0.1, E[0] - 0.3, size=80, top=1090)
c.kwc("kw-mal", "IL A MAL GÉRÉ<br>SON ARGENT", WHITE, find("s2", "mal") - 0.3, t_dizaines - 0.5, size=80)
c.kwc("kw-diz", "DES DIZAINES<br>DE MILLIONS", CYAN, t_dizaines - 0.2, t_perdu - 0.4, size=84)
c.kwc("kw-perdu", "TOUT PERDU", RED_Y, t_perdu - 0.1, E[2] - 0.3, size=104, top=1260)
c.kwc("kw-cent", "DES CENTAINES<br>DE MILLIONS", CYAN, t_centaines - 0.2, E[3] - 0.3, size=84)
c.kwc("kw-chute", "ET TOUT PERDRE", RED_Y, t_tout - 0.2, c.END_T + 0.45, size=96, top=1270)
SFX = [("sfx-pop-1", "pop", t_rc - 0.08, 0.26), ("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-2", "pop", t_perdu - 0.08, 0.32),
       ("sfx-whoosh-2", "whoosh", E[2] - 0.22, 0.26), ("sfx-pop-3", "pop", t_tout - 0.18, 0.32)]
c.sfx = SFX   # la fin « outro » ajoute ses propres sons
c.build()
