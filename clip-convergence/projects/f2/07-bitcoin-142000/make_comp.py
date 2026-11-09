"""Composition du clip 7 « Est-ce que vous avez 142 000 € ? » (Formation 2 « Comment devenir riche », Nass seul), comp_lib thème ydf.

100 € par mois pendant 10 ans dans le bitcoin : 142 000 €. La question à sa communauté crypto : est-ce que vous les avez dans votre portefeuille ? Il suffisait de 100 € par mois. La slide sous lui.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 7, "« Est-ce que vous avez 142 000 € ? »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf", end="outro")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = 'VOUS AVEZ<br><b>142 000 € ?</b>'
c.moves = [(E[0], "SOLO_E"), (E[1], "SOLO_N"), (E[2], "SOLO_N+")]
c.screen_windows = [(E[0], E[1])]
t_q = find("s3", "posez")
t_suff = find("s4", "suffisait")
c.kwc("kw-q", "POSEZ-VOUS<br>LA QUESTION", WHITE, t_q - 0.2, E[2] - 0.3, size=80)
c.kwc("kw-chute", "100 € TOUS LES MOIS,<br>C'EST TOUT", ORANGE, t_suff - 0.3, c.END_T + 0.45, size=62)
SFX = [("sfx-whoosh-1", "whoosh", E[0] - 0.22, 0.3), ("sfx-whoosh-2", "whoosh-short", E[1] - 0.2, 0.3), ("sfx-pop-1", "pop", t_q - 0.18, 0.26),
       ("sfx-whoosh-3", "whoosh", E[2] - 0.22, 0.26), ("sfx-pop-2", "pop", t_suff - 0.28, 0.3)]
c.sfx = SFX   # la fin « outro » ajoute ses propres sons
c.build()
