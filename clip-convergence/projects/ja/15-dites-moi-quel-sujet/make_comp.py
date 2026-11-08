"""Composition du clip 15 « Dites-moi quel sujet, je vous tourne ça » (J'abandonne mon challenge crypto, Nass seul), comp_lib thème ydf.

La fin : petite transparence sur ce challenge, la formation offerte en bio, et il a du temps : dites-lui en commentaire quel sujet vous voulez, il vous tourne ça tout de suite. Que la paix soit sur vous.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 15, "« Dites-moi quel sujet, je vous tourne ça »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = 'VOUS VOULEZ<br><b>QUEL SUJET ?</b>'
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_N+")]
t_sujet, t_temps, t_contenu, t_tourne, t_paix = find("s2", "sujet"), find("s2", "temps"), find("s3", "contenu."), find("s3", "tourne"), find("s3", "paix")
c.kwc("kw-sujet", "QUEL SUJET<br>DE VIDÉO ?", WHITE, t_sujet - 0.3, t_temps - 0.9, size=76)
c.kwc("kw-temps", "J'AI DU TEMPS", CYAN, t_temps - 0.2, t_contenu - 0.9, size=84, top=1270)
c.kwc("kw-contenu", "FOCUS<br>SUR LE CONTENU", WHITE, t_contenu - 0.3, t_tourne - 0.9, size=72)
c.kwc("kw-chute", "JE VOUS TOURNE ÇA<br>TOUT DE SUITE", ORANGE, t_tourne - 0.3, c.END_T + 0.45, size=64, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_sujet - 0.28, 0.26), ("sfx-pop-2", "pop", t_temps - 0.18, 0.26),
       ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26), ("sfx-pop-3", "pop", t_contenu - 0.28, 0.26), ("sfx-pop-4", "pop", t_tourne - 0.28, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
