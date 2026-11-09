"""Composition du clip 8 « Est-ce qu'il fallait un master ? » (Formation 2 « Comment devenir riche », Nass seul), comp_lib thème ydf.

Investir 100 € par mois, c'était difficile ? Il fallait un master, être trader, faire du scalping ? Non : 100 € tous les mois.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 8, "« Est-ce qu'il fallait un master ? »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf", end="outro")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = "EST-CE QU'IL FALLAIT<br><b>UN MASTER ?</b>"
c.moves = [(E[0], "SOLO_N"), (E[1], "SOLO_N+")]
t_master, t_trader, t_scalp, t_100 = find("s2", "master"), find("s2", "trader"), find("s2", "scalping"), find("s3", "100")
ROW = "left: 0; right: 0; text-align: center; color: %s; font-size: 72px; line-height: 1;"
for i, (t, w, k) in enumerate([(t_master, "UN MASTER ?", "master"), (t_trader, "ÊTRE TRADER ?", "trader"), (t_scalp, "DU SCALPING ?", "scalp")]):
    c.kw(f"kw-{k}", f'<span class="no">{w}</span>', (ROW % WHITE) + f" top: {1215 + i * 92}px;", t - 0.05, t_100 - 0.5)
c.ill_css = NO_CSS
c.kwc("kw-chute", "100 € TOUS LES MOIS.", ORANGE, t_100 - 0.2, c.END_T + 0.45, size=64, top=1280)
SFX = [("sfx-whoosh-1", "whoosh-short", E[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_master, 0.26), ("sfx-pop-2", "pop", t_trader, 0.26), ("sfx-pop-3", "pop", t_scalp, 0.26),
       ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.26), ("sfx-pop-4", "pop", t_100 - 0.18, 0.32)]
c.sfx = SFX   # la fin « outro » ajoute ses propres sons
c.build()
