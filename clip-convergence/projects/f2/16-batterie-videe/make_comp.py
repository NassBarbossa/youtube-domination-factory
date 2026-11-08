"""Composition du clip 16 « Vous avez vidé ma batterie » (Formation 2 « Comment devenir riche », Nass seul), comp_lib thème ydf.

Quatrième raison : sur les réseaux on vous dit tout et n'importe quoi, scalping et compagnie, donc vous ne passez pas à l'action. Et la batterie de l'appareil photo lâche : « c'est pour votre bien, c'est pour vous réveiller ».
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 16, "« Vous avez vidé ma batterie »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = 'VOUS AVEZ VIDÉ<br><b>MA BATTERIE</b>'
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_N+"), (E[2], "SOLO_N")]
t_action = find("s2", "passez")
c.kwc("kw-scalp", "SUR LES RÉSEAUX :<br>TOUT ET N'IMPORTE QUOI", MUTED, E[0] + 0.3, t_action - 0.9, size=64)
c.kwc("kw-action", "VOUS NE PASSEZ PAS<br>À L'ACTION", WHITE, t_action - 0.4, E[1] - 0.3, size=72)
c.kwc("kw-batt", "BATTERIE VIDÉE.", CYAN, E[1] + 0.3, E[2] - 0.3, size=88)
c.kwc("kw-chute", "C'EST POUR VOTRE BIEN :<br>POUR VOUS RÉVEILLER", ORANGE, E[2] + 0.25, c.END_T + 0.45, size=56, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_action - 0.38, 0.26), ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26),
       ("sfx-pop-2", "pop", E[1] + 0.32, 0.26), ("sfx-whoosh-3", "whoosh", E[2] - 0.22, 0.26), ("sfx-pop-3", "pop", E[2] + 0.27, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
