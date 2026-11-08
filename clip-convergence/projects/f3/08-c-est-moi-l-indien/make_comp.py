"""Composition du clip 8 « « C'est moi l'indien » » (Formation 3 « L'investissement on-chain », Nass seul), comp_lib thème ydf.

Dans le far west, beaucoup perdent de l'argent, beaucoup d'arnaques : il faut venir équipé d'une méthode. Sinon, « c'est moi l'indien, qui peut m'aider ? », il y a de grandes chances que tu te fasses capturer.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 8, "« « C'est moi l'indien » »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = 'FAR WEST :<br><b>VIENS ÉQUIPÉ</b>'
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_N+")]
t_arn, t_meth, t_indien, t_capt = find("s1", "arnaques"), find("s2", "méthode"), find("s2", "indien"), find("s2", "capturer")
c.hook_fade = t_arn - 0.45
c.kwc("kw-arn", "BEAUCOUP<br>D'ARNAQUES", RED_Y, t_arn - 0.1, t_meth - 0.9, size=84)
c.kwc("kw-meth", "ÉQUIPÉ<br>D'UNE MÉTHODE", ORANGE, t_meth - 0.2, t_indien - 0.9, size=84)
c.kwc("kw-indien", "« C'EST MOI L'INDIEN,<br>QUI PEUT M'AIDER ? »", MUTED, t_indien - 0.3, t_capt - 0.8, size=60, extra="font-style: italic;")
c.kwc("kw-chute", "TU TE FAIS<br>CAPTURER", WHITE, t_capt - 0.3, c.END_T + 0.45, size=88, anim="rise")
SFX = [("sfx-pop-1", "pop", t_arn - 0.08, 0.26), ("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-2", "pop", t_meth - 0.18, 0.3),
       ("sfx-pop-3", "pop", t_indien - 0.28, 0.24), ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26), ("sfx-pop-4", "pop", t_capt - 0.28, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
