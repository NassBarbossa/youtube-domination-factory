"""Composition du clip 13 « Vous êtes un kiffeur ? C'est OK » (Formation 3 « L'investissement on-chain », Nass seul), comp_lib thème ydf.

Si votre choix, c'est juste investir tous les mois parce que vous êtes un kiffeur : obligatoire, et dans 10 ou 20 ans vos enfants vous remercieront, ça a fait ses preuves depuis 70 ans. Choix 2 : affronter le far west bien entouré.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 13, "« Vous êtes un kiffeur ? C'est OK »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf", end="outro")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = "UN KIFFEUR ?<br><b>C'EST OK.</b>"
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_N+")]
t_oblig, t_enfants, t_70, t_choix2 = find("s1", "obligatoire"), find("s2", "enfants"), find("s2", "preuves"), find("s3", "Choix")
c.hook_fade = t_oblig - 0.45
c.kwc("kw-oblig", "OBLIGATOIRE :<br>TOUS LES MOIS", ORANGE, t_oblig - 0.1, t_enfants - 0.9, size=72)
c.kwc("kw-enfants", "VOS ENFANTS<br>VOUS REMERCIERONT", WHITE, t_enfants - 0.3, t_70 - 0.9, size=64)
c.kwc("kw-70", "70 ANS<br>DE PREUVES", CYAN, t_70 - 0.2, t_choix2 - 0.9, size=84)
c.kwc("kw-chute", "CHOIX 2 :<br>LE FAR WEST,<br>BIEN ENTOURÉ", ORANGE, t_choix2 - 0.2, c.END_T + 0.45, size=62, anim="rise")
SFX = [("sfx-pop-1", "pop", t_oblig - 0.08, 0.3), ("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-2", "pop", t_enfants - 0.28, 0.26),
       ("sfx-pop-3", "pop", t_70 - 0.28, 0.26), ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26), ("sfx-pop-4", "pop", t_choix2 - 0.18, 0.3)]
c.sfx = SFX   # la fin « outro » ajoute ses propres sons
c.build()
