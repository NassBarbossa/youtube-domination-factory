"""Composition du clip 22b « Mon activité ne repose pas sur Bitcoin » (Convergence EP.01), comp_lib v6.

Déroulé : accroche à deux caméras « ELLE NE REPOSE PAS / SUR BITCOIN », Nass seul : CONVERGENCE sur « dans Convergence »,
BITCOIN / ETHEREUM / SOLANA barrés un à un, ON-CHAIN en vert puis « AVANT QU'ELLES SE FASSENT LISTER », chute « EN DEHORS DES
ÉCHANGES ». Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, GREEN, GREY, INK, RED  # noqa: E402

c = Comp(HERE, "22b", "« Mon activité ne repose pas sur Bitcoin »")
seams, find = c.seams, c.find
c.moves = [
    (seams[0], "SOLO_N"),    # s2 : « Donc pour moi… dans Convergence »
    (seams[1], "SOLO_N+"),   # s3 : « mon activité principale en crypto »
    (seams[2], "SOLO_N"),    # s4 : « elle ne repose pas sur Ethereum »
    (seams[3], "SOLO_N+"),   # s5 : « elle repose sur le trading on-chain »
    (seams[4], "SOLO_N"),    # s6 : « Donc tant que BTC se comporte bien »
]
c.hook_html = "ELLE NE REPOSE PAS<br><b>SUR BITCOIN</b>"
c.hook_font = 96

t_conv = find("s2", "convergence")
t_btc = find("s3", "bitcoin")
t_eth = find("s4", "ethereum")
t_sol = find("s4", "solana")
t_repose = find("s5", "repose")
t_chain = find("s5", "on")           # « on-chain »
t_avant = find("s5", "avant")
t_dehors = find("s6", "dehors")

c.kw("kw-conv", "CONVERGENCE", f"left: 0; right: 0; top: 1270px; text-align: center; color: {INK}; font-size: 104px; letter-spacing: 0.18em;",
     t_conv, seams[1] - 0.3)
c.kw("kw-chain", "ON-CHAIN", f"left: 0; right: 0; top: 1192px; text-align: center; color: {GREEN}; font-size: 128px;",
     t_chain, seams[4] - 0.3)
c.kw("kw-avant", "AVANT QU'ELLES<br>SE FASSENT LISTER", f"left: 0; right: 0; top: 1340px; text-align: center; color: {INK}; font-size: 62px; line-height: 1.05;",
     t_avant, seams[4] - 0.3, anim="rise")
c.kw("kw-dehors", "EN DEHORS<br>DES ÉCHANGES", f"left: 0; right: 0; top: 1200px; text-align: center; color: {GREEN}; font-size: 104px; line-height: 1;",
     t_dehors, c.END_T + 0.05)

# trois noms barrés un à un (la bande n'est visible qu'une fois Nass seul : BITCOIN est déjà barré à l'arrivée)
c.ill_css = f""".row {{ position: absolute; left: 0; right: 0; text-align: center; }}
    .coin {{ position: relative; display: inline-block; font: 800 78px/1 'Inter Tight'; letter-spacing: -0.03em; color: {GREY}; white-space: nowrap; }}
    .coin i {{ position: absolute; left: -12px; right: -12px; top: 34px; height: 12px; border-radius: 6px; background: {RED}; transform: rotate(-4deg) scaleX(0); transform-origin: 0 50%; }}"""
c.ill_html = """<div id="ill-coins" class="ill">
        <div class="row" style="top:4px"><span id="coin-btc" class="coin">BITCOIN<i id="bar-btc"></i></span></div>
        <div class="row" style="top:106px"><span id="coin-eth" class="coin" style="opacity:0">ETHEREUM<i id="bar-eth"></i></span></div>
        <div class="row" style="top:208px"><span id="coin-sol" class="coin" style="opacity:0">SOLANA<i id="bar-sol"></i></span></div>
      </div>"""
c.ill_js = [
    f'tl.fromTo("#ill-coins", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.1 }}, {round(seams[1] - 0.2, 3)});',
    f'tl.fromTo("#bar-btc", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.3, ease: "power3.out" }}, {round(t_btc + 0.1, 3)});',
    f'tl.fromTo("#coin-eth", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.25, ease: "power2.out" }}, {round(t_eth - 0.5, 3)});',
    f'tl.fromTo("#bar-eth", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.3, ease: "power3.out" }}, {round(t_eth + 0.1, 3)});',
    f'tl.fromTo("#coin-sol", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.25, ease: "power2.out" }}, {round(t_sol - 0.5, 3)});',
    f'tl.fromTo("#bar-sol", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.3, ease: "power3.out" }}, {round(t_sol + 0.1, 3)});',
    f'tl.to("#ill-coins", {{ opacity: 0, duration: 0.25, ease: "power2.in" }}, {round(t_chain - 0.35, 3)});',
]
c.cap_cuts = [("s6", t_dehors, 1e9)]
c.cap_end_before = [t_dehors]

c.sfx = [
    ("sfx-whoosh-1", "whoosh-short", seams[0] - 0.20, 0.34),
    ("sfx-pop-1", "pop", t_eth + 0.12, 0.24),
    ("sfx-pop-2", "pop", t_sol + 0.12, 0.24),
    ("sfx-pop-3", "pop", t_chain + 0.02, 0.30),
    ("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40),
]
c.build()
print(f"conv {t_conv} | btc {t_btc} eth {t_eth} sol {t_sol} | chain {t_chain} | dehors {t_dehors}")
