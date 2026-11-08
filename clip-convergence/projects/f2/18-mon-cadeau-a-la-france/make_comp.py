"""Composition du clip 18 « Mon cadeau à la France » (Formation 2 « Comment devenir riche », Nass seul), comp_lib thème ydf.

« Tu es parti à l'étranger, tu ne donnes rien à la France » : cette formation offerte, c'est son cadeau à la France. Partage, commente.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 18, "« Mon cadeau à la France »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = 'MON CADEAU<br><b>À LA FRANCE</b>'
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_N+"), (E[2], "SOLO_N")]
t_rien, t_voila, t_riches = find("s3", "donnes"), find("s3", "Voilà"), find("s4", "riches")
c.kwc("kw-parti", "« TOI, T'ES PARTI<br>À L'ÉTRANGER »", MUTED, E[0] + 0.3, t_rien - 1.0, size=64, extra="font-style: italic;")
c.kwc("kw-rien", "« TU NE DONNES RIEN<br>À LA FRANCE »", MUTED, t_rien - 0.4, t_voila - 0.6, size=68, extra="font-style: italic;")
c.kwc("kw-voila", "VOILÀ MON CADEAU<br>À LA FRANCE", ORANGE, t_voila - 0.2, t_riches - 0.9, size=76)
c.kwc("kw-chute", "VOUS RENDRE<br>TOUS RICHES", CYAN, t_riches - 0.6, c.END_T + 0.45, size=88, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-0", "pop", E[0] + 0.32, 0.24), ("sfx-pop-1", "pop", t_rien - 0.38, 0.24), ("sfx-whoosh-2", "whoosh", E[2] - 0.22, 0.26),
       ("sfx-pop-2", "pop", t_voila - 0.18, 0.3), ("sfx-pop-3", "pop", t_riches - 0.58, 0.28)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
