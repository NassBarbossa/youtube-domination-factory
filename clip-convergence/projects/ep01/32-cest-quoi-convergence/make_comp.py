"""Composition du clip 32 « C'est quoi Convergence » (Convergence EP.01), comp_lib v6.

Accroche « DE QUOI / ON PARLERA » (les mots de la slide), la slide réelle du live (News, Tendances de marché, nos positions)
sous Nass pendant qu'il énumère, puis Nass seul avec des pastilles qui s'ajoutent (IA, INVESTISSEMENTS EXOTIQUES, CARTES ONE
PIECE, IMMOBILIER), NOS EXPERTISES / EN UN SEUL SHOW, et « ON LE DIT UNE FOIS ». Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, GREEN, INK, solo_screen  # noqa: E402

c = Comp(HERE, 32, "« C'est quoi Convergence »")
seams, find = c.seams, c.find
S = c.STATES
S["SOLO_E"] = solo_screen(860, 900, 496)
S["SOLO_E+"] = dict(S["SOLO_E"], nass=(540, S["SOLO_E"]["nass"][1] + 10, 880))

c.moves = [
    (seams[0], "SOLO_E"),    # s2 : « donc accès investissement, accès trading et un peu des news » : la slide
    (seams[1], "SOLO_E+"),   # s3 : « après, dans un volume un peu plus large »
    (seams[2], "SOLO_N"),    # s4 : « des liens avec l'IA, des investissements exotiques »
    (seams[3], "SOLO_N+"),   # s5 : « des petites cartes One Piece »
    (seams[4], "SOLO_N"),    # s6 : « pourquoi pas d'immobilier »
    (seams[5], "SOLO_N+"),   # s7 : « en gros Convergence, c'est nos expertises »
    (seams[6], "SOLO_N"),    # s8 : « on le dit une fois »
]
c.screen_windows = [(seams[0], seams[2])]
c.hook_html = "DE QUOI<br><b>ON PARLERA</b>"
c.fix = {("s7", "roi"): "rejoignent", ("s7", "-gènent"): ""}

t_ia = find("s4", "ia")
t_exo = find("s4", "exotiques")
t_cartes = find("s5", "cartes")
t_immo = find("s6", "immobilier")
t_conv = find("s7", "convergence")
t_expertises = find("s7", "expertises")
t_seul = find("s7", "seul")
t_dit = find("s8", "dit")

c.kw("kw-expertises", "NOS EXPERTISES", f"left: 0; right: 0; top: 1200px; text-align: center; color: {INK}; font-size: 100px;",
     t_expertises, seams[6] - 0.3)
c.kw("kw-show", "EN UN SEUL SHOW", f"left: 0; right: 0; top: 1322px; text-align: center; color: {GREEN}; font-size: 100px;",
     t_seul, seams[6] - 0.3)
c.kw("kw-fois", "ON LE DIT UNE FOIS", f"left: 0; right: 0; top: 1280px; text-align: center; color: {INK}; font-size: 96px;",
     t_dit, c.END_T + 0.05, anim="rise")

c.ill_css = f""".chip {{ position: absolute; padding: 14px 30px; border: 8px solid {INK}; border-radius: 60px; font: 800 42px/1 'Inter Tight';
            letter-spacing: -0.01em; color: {INK}; white-space: nowrap; }}"""
c.ill_html = """<div id="ill-chips" class="ill">
        <div id="ch-ia" class="chip" style="left:0px; top:30px; opacity:0">IA</div>
        <div id="ch-exo" class="chip" style="left:150px; top:30px; opacity:0">INVESTISSEMENTS EXOTIQUES</div>
        <div id="ch-op" class="chip" style="left:0px; top:160px; opacity:0">CARTES ONE PIECE</div>
        <div id="ch-immo" class="chip" style="left:540px; top:160px; opacity:0">IMMOBILIER</div>
      </div>"""
c.ill_js = [f'tl.fromTo("#ill-chips", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.1 }}, {round(t_ia - 0.1, 3)});']
for cid, t in (("ch-ia", t_ia), ("ch-exo", t_exo), ("ch-op", t_cartes), ("ch-immo", t_immo)):
    c.ill_js.append(f'tl.fromTo("#{cid}", {{ opacity: 0, scale: 0.6, transformOrigin: "50% 50%" }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }}, {round(t - 0.05, 3)});')
c.ill_js.append(f'tl.to("#ill-chips", {{ opacity: 0, duration: 0.25, ease: "power2.in" }}, {round(t_conv - 0.3, 3)});')

c.sfx = [
    ("sfx-whoosh-1", "whoosh-short", seams[0] - 0.20, 0.34),   # la slide
    ("sfx-whoosh-2", "whoosh", seams[2] - 0.22, 0.30),          # retour sur Nass
    ("sfx-pop-1", "pop", t_ia + 0.02, 0.26),
    ("sfx-pop-2", "pop", t_cartes + 0.02, 0.26),
    ("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40),
]
c.build()
print(f"slide {seams[0]}-{seams[2]} | ia {t_ia} exo {t_exo} op {t_cartes} immo {t_immo} | expertises {t_expertises} | fois {t_dit}")
