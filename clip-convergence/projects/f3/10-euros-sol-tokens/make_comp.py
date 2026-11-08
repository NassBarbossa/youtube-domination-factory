"""Composition du clip 10 « Euros → SOL → tokens » (Formation 3 « L'investissement on-chain », Nass seul), comp_lib thème ydf.

Les trois étapes : tes euros, convertis en SOL sur un échange centralisé (OKX), puis mis dans d'autres tokens du monde décentralisé (Solana). « Reste concentré, ce n'est pas compliqué. » La slide « Les euros, on les convertit en SOL » sous lui.
Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, ORANGE, CYAN, WHITE, RED_Y, MUTED, solo, solo_screen  # noqa: E402
NO_CSS = ".no { position: relative; display: inline-block; padding: 0 10px; } .no::after { content: ''; position: absolute; left: 0; right: 0; top: 52%; height: 9px; background: " + RED_Y + "; border-radius: 5px; transform: translateY(-50%); box-shadow: 0 0 16px rgba(255,68,68,.6); }"

c = Comp(HERE, 10, "« Euros → SOL → tokens »", cta="Les 3 vidéos<br>sur la chaîne", theme="ydf")
seams, find, S = c.seams, c.find, c.STATES
E = seams + [c.END_T]  # E[i] = fin du morceau i+1
S["H"] = solo("nass", 760)
S["SOLO_E"] = solo_screen(820, 960, 540)
S["SOLO_E+"] = solo_screen(850, 960, 540)
c.hook_font = 80
c.hook_html = 'EUROS → SOL<br><b>→ TOKENS</b>'
c.fix = {("s1", "sexe."): "CEX.", ("s1", "sexe,"): "CEX,", ("s1", "sexe"): "CEX", ("s2", "sexe."): "CEX.", ("s2", "sexe,"): "CEX,", ("s2", "sexe"): "CEX", ("s3", "sexe."): "CEX.", ("s3", "sexe,"): "CEX,", ("s3", "sexe"): "CEX", ("s4", "sexe,"): "CEX,", ("s4", "sexe"): "CEX", ("s1", "OKEx"): "OKX", ("s2", "OKEx"): "OKX", ("s3", "sols,"): "SOL,", ("s3", "sols"): "SOL", ("s4", "sols"): "SOL", ("s2", "soldes."): "SOL.", ("s1", "fact"): "far", ("s1", "-well,"): "west,", ("s1", "Nas"): "Nass", ("s2", "Nas"): "Nass"}
c.moves = [(E[0], "SOLO_E"), (E[1], "SOLO_N"), (E[2], "SOLO_N+")]
c.screen_windows = [(E[0], E[1])]
t_tokens, t_solana = find("s3", "tokens"), find("s4", "Solana")
c.kwc("kw-tokens", "ÉTAPE 3 :<br>D'AUTRES TOKENS", WHITE, t_tokens - 0.4, t_solana - 0.9, size=72)
c.kwc("kw-chute", "SUR SOLANA,<br>IL TE FAUT DES SOL", ORANGE, t_solana - 0.3, c.END_T + 0.45, size=68, anim="rise")
SFX = [("sfx-whoosh-1", "whoosh", E[0] - 0.22, 0.3), ("sfx-whoosh-2", "whoosh", E[1] - 0.22, 0.3), ("sfx-pop-1", "pop", t_tokens - 0.38, 0.26),
       ("sfx-whoosh-3", "whoosh-short", E[2] - 0.2, 0.26), ("sfx-pop-2", "pop", t_solana - 0.28, 0.3)]
c.sfx = SFX + [("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40)]
c.build()
