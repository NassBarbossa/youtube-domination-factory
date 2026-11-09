"""Composition du clip 7 « Toutes les phases, je les ai vécues » (Formation 1 « Pourquoi investir en 2026 », Nass seul), comp_lib thème ydf.

Cryptos 2017, ICO, NFT, ordinals, memecoins, DeFi : Nass a tout vécu ; il a fait payer ce savoir en 2021-2022 et a encore des résultats. Deux passages cousus (03:00 et 04:05).
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402

c = Comp(HERE, 7, "« Toutes les phases, je les ai vécues »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf", end="outro")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 74
c.hook_html = 'TOUTES LES PHASES,<br><b>JE LES AI VÉCUES</b>'
c.moves = [(E[0], "SOLO_E"), (E[1], "SOLO_N")]
c.screen_windows = [(E[0], E[1])]
t_payer, t_res = find("s3", "payer"), find("s3", "résultats")
c.kwc("kw-payer", "J'AI FAIT PAYER<br>CE SAVOIR EN 2021", WHITE, t_payer - 0.3, t_res - 0.9, size=72)
c.kwc("kw-chute", "AUJOURD'HUI ENCORE,<br>J'AI DES RÉSULTATS", ORANGE, t_res - 0.8, c.END_T + 0.45, size=72, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh", E[0] - 0.22, 0.3), ("sfx-whoosh-2", "whoosh-short", E[1] - 0.2, 0.3), ("sfx-pop-1", "pop", t_payer - 0.28, 0.26),
       ("sfx-pop-2", "pop", t_res - 0.78, 0.28)]
c.sfx = SFX   # la fin « outro » ajoute ses propres sons
c.build()
