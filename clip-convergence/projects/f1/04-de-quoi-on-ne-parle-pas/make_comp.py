"""Composition du clip 4 « De quoi on ne va pas parler » (Formation 1 « Pourquoi investir en 2026 », Nass seul), comp_lib thème ydf.

Pas de trading, pas de scalping, pas d'automatisation avec l'IA : ce dont on va parler, c'est l'investissement. Positionne la chaîne en 30 secondes.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402

c = Comp(HERE, 4, "« De quoi on ne va pas parler »", cta="Les 3 vidéos sont sur la chaîne", theme="ydf")
seams, find, S = c.seams, c.find, c.STATES
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 84
c.hook_html = 'DE QUOI ON NE VA<br><b>PAS PARLER</b>'
c.moves = [(seams[0], "SOLO_N"), (seams[1], "SOLO_N+"), (seams[2], "SOLO_N")]
t_trad, t_scalp, t_ia, t_inv = find("s2", "trading"), find("s2", "scalping"), find("s3", "IA"), find("s4", "investissement")
ROW = "left: 0; right: 0; text-align: center; color: %s; font-size: 72px; line-height: 1;"
for i, (t, w, k) in enumerate([(t_trad, "TRADING", "trad"), (t_scalp, "SCALPING", "scalp"), (t_ia, "L'IA", "ia")]):
    c.kw(f"kw-{k}", f'<span class="no">{w}</span>', (ROW % WHITE) + f" top: {1185 + i * 96}px;", t - 0.05, t_inv - 0.5)
c.ill_css = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 50%; height: 10px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"
c.kwc("kw-chute", "L'INVESTISSEMENT", ORANGE, t_inv - 0.2, c.END_T + 0.45, size=92, top=1270)
c.cap_cuts = [("s4", t_inv - 0.1, 1e9)]; c.cap_end_before = [t_inv - 0.05]
SFX = [("sfx-whoosh-1", "whoosh-short", seams[0] - 0.2, 0.3), ("sfx-pop-1", "pop", t_trad, 0.26), ("sfx-pop-2", "pop", t_scalp, 0.26), ("sfx-pop-3", "pop", t_ia, 0.26),
       ("sfx-whoosh-2", "whoosh", seams[2] - 0.22, 0.26), ("sfx-pop-4", "pop", t_inv - 0.18, 0.32)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
