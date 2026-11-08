"""Composition du clip 4 « La huitième merveille du monde » (Formation 2 « Comment devenir riche », Nass seul), comp_lib thème ydf.

Les intérêts composés, « la huitième merveille du monde » (citation attribuée à Einstein) ; le test : 100 € par mois pendant 10 ans, c'est déjà 12 000 € de côté.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 4, "« La huitième merveille du monde »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = 'LA HUITIÈME<br><b>MERVEILLE DU MONDE</b>'
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_N+"), (E[2], "SOLO_N"), (E[3], "SOLO_N+")]
t_einstein, t_100, t_12k, t_12k2 = find("s2", "Einstein"), find("s3", "100"), find("s4", "12"), find("s5", "12")
c.kwc("kw-einstein", "— EINSTEIN", MUTED, t_einstein - 0.2, E[1] - 0.3, size=64, top=1270, anim="rise")
c.kwc("kw-100", "100 € / MOIS<br>PENDANT 10 ANS", WHITE, t_100 - 0.2, t_12k - 0.6, size=80)
c.kwc("kw-12k", "= 12 000 €", ORANGE, t_12k - 0.2, t_12k2 - 0.9, size=112, top=1250)
c.kwc("kw-chute", "12 000 €<br>DE CÔTÉ", ORANGE, t_12k2 - 0.5, c.END_T + 0.45, size=96)
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_100 - 0.18, 0.26), ("sfx-whoosh-2", "whoosh", E[2] - 0.22, 0.26),
       ("sfx-pop-2", "pop", t_12k - 0.18, 0.32), ("sfx-pop-3", "pop", t_12k2 - 0.48, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
