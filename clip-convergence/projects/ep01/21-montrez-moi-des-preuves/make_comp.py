"""Composition du clip 21 « Montrez-moi des preuves » (Convergence EP.01) sur comp_lib (DA « Les deux droites », v6).

Déroulé : accroche à deux caméras « LE BITCOIN, RÉSERVE DE VALEUR ? », puis Nass seul avec son écran (BTC + l'or en bleu
par-dessus) pendant qu'il compare, retour à Nass seul pour « quand on dit l'or, le bitcoin c'est une réserve de valeur »
(RÉSERVE DE VALEUR barré en rouge sur « pas de preuves »), MONTREZ-MOI DES PREUVES en mot clé, puis l'écran revient pour la
chute « l'or, le montait » (mot clé or sous l'écran). Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, GOLD_TXT, GREY, INK, RED  # noqa: E402

c = Comp(HERE, 21, "« Montrez-moi des preuves »")
seams, find = c.seams, c.find
S = c.STATES
S["SOLO_E+"] = dict(S["SOLO_E"], nass=(540, S["SOLO_E"]["nass"][1] + 10, 880))   # punch-in léger, l'écran ne bouge pas

# ---------- mise en page ----------
c.moves = [
    (seams[0], "SOLO_E"),    # s2 : « pendant tout ce temps là… on peut comparer » : l'écran s'ouvre
    (seams[1], "SOLO_E+"),   # s3 : « pendant toute cette phase là » (coupe du « donc »)
    (seams[2], "SOLO_N"),    # s4 : « pour moi quand on dit… » : Nass seul, l'illustration dans la bande
    (seams[3], "SOLO_N+"),   # s5 : « montrez-moi des preuves »
    (seams[4], "SOLO_E"),    # s6 : « pendant que BTC était en train de s'éclater… l'or, le montait » : l'écran revient
]
c.screen_windows = [(seams[0], seams[2]), (seams[4], c.END_T)]
c.hook_html = "LE BITCOIN,<br><b>RÉSERVE DE VALEUR ?</b>"
c.hook_font = 88

# ---------- instants ----------
t_reserve = find("s4", "réserve")      # « c'est une réserve de valeur »
t_pas = find("s4", "pas")              # « j'ai pas de preuves » : barré rouge
t_montrez = find("s5", "montrez")      # « montrez-moi des preuves »
t_pas2 = find("s5", "pas")             # « c'est pas une réserve de valeur » : pulse
t_chute = round(find("s6", "or") - 0.32, 3)   # « l'or, le montait » (le « l' » précède « or »)

# ---------- mots clés ----------
c.kw("kw-montrez", "MONTREZ-MOI<br>DES PREUVES",
     f"left: 0; right: 0; top: 1192px; text-align: center; color: {INK}; font-size: 112px; line-height: 1;",
     t_montrez, seams[4] - 0.4)
c.kw("kw-or", "<span>L'OR MONTAIT</span>",
     f"left: 0; right: 0; top: {S['SOLO_E']['cap'] - 38}px; text-align: center; color: {GOLD_TXT}; font-size: 68px;",
     t_chute, c.END_T + 0.05)
c.extra_js = [
    f'tl.to("#kw-montrez", {{ scale: 1.08, duration: 0.14, ease: "power2.out", yoyo: true, repeat: 1 }}, {round(t_pas2, 3)});',
]
c.cap_cuts = [("s6", t_chute, 1e9)]
c.cap_end_before = [t_chute]
c.fix = {("s2", "x"): "XAU/USD", ("s2", "à"): "", ("s2", "usd"): "", ("s6", "'achaufaient,"): "'échauffaient,"}

# ---------- illustration : RÉSERVE DE VALEUR barré ----------
c.ill_css = f"""#kw-or span {{ box-shadow: inset 0 -14px 0 {GOLD_TXT}; }}
    #ill-rdv {{ text-align: center; }}
    #rdv-txt {{ position: absolute; left: 0; right: 0; top: 70px; font: 800 96px/1 'Inter Tight'; letter-spacing: -0.03em; color: {GREY}; white-space: nowrap; }}
    #rdv-line {{ position: absolute; left: 30px; right: 30px; top: 112px; height: 16px; border-radius: 8px; background: {RED}; transform: rotate(-3deg); }}"""
c.ill_html = """<div id="ill-rdv" class="ill">
        <div id="rdv-txt" style="opacity:0">RÉSERVE DE VALEUR</div>
        <div id="rdv-line"></div>
      </div>"""
c.ill_js = [
    f'tl.fromTo("#ill-rdv", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.1 }}, {round(t_reserve - 0.1, 3)});',
    f'tl.fromTo("#rdv-txt", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }}, {round(t_reserve - 0.08, 3)});',
    f'tl.fromTo("#rdv-line", {{ scaleX: 0, transformOrigin: "0% 50%" }}, {{ scaleX: 1, duration: 0.3, ease: "power3.out" }}, {round(t_pas, 3)});',
    f'tl.to("#ill-rdv", {{ opacity: 0, duration: 0.25, ease: "power2.in" }}, {round(t_montrez - 0.3, 3)});',
]

# ---------- SFX ----------
c.sfx = [
    ("sfx-whoosh-1", "whoosh-short", seams[0] - 0.20, 0.34),   # l'écran s'ouvre
    ("sfx-pop-1", "pop", t_pas + 0.02, 0.30),                   # le barré rouge
    ("sfx-pop-2", "pop", t_montrez + 0.02, 0.30),               # MONTREZ-MOI DES PREUVES
    ("sfx-whoosh-2", "whoosh", seams[4] - 0.22, 0.30),          # l'écran revient
    ("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40),
]
c.build()
print(f"écran {seams[0]}-{seams[2]} et {seams[4]}-{c.END_T} | barré {t_pas} | montrez {t_montrez} | chute {t_chute}")
