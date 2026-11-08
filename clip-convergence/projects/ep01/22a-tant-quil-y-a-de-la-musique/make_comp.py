"""Composition du clip 22a « Tant qu'il y a de la musique, il faut danser » (Convergence EP.01), comp_lib v6.

Déroulé : accroche à deux caméras « TANT QU'IL Y A / DE LA MUSIQUE… », Nass seul : notes de musique qui poppent sur « musique »
et IL FAUT DANSER sur « danser » ; « TOUT PEUT CHANGER / DU JOUR AU LENDEMAIN » ; JE GARDE MES POSITIONS ; courbe à l'encre
avec le TOP et le point vert « un peu plus bas » ; retour des deux caméras 1,3 s avant Sadek (« c'est très bien dit »), donc
« il y a de la musique, donc on danse » se dit à deux caméras, sous-titres seuls. Usage : python3 -I make_comp.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
from comp_lib import Comp, GOLD, GREEN, GREY, INK, RED  # noqa: E402

c = Comp(HERE, "22a", "« Tant qu'il y a de la musique, il faut danser »")
seams, find = c.seams, c.find
t_back = round(seams[4] - 1.3, 3)   # les deux caméras reviennent 1,3 s avant Sadek

c.moves = [
    (seams[0], "SOLO_N"),    # s2 : « que je me fie beaucoup… »
    (seams[1], "SOLO_N+"),   # s3 : « Et en fait, je trouve que c'est tellement difficile »
    (seams[2], "SOLO_N"),    # s4 : « que moi, j'ai mes positions »
    (seams[3], "SOLO_N+"),   # s5 : « Et après, si ça change »
    (t_back, "N"),           # les deux caméras, Nass parle encore
    (seams[4], "S"),         # s6 : Sadek, « c'est très bien dit »
]
c.hook_html = "TANT QU'IL Y A<br><b>DE LA MUSIQUE…</b>"

t_musique = find("s2", "musique")
t_danser = find("s2", "danser")
t_tout = find("s3", "tout")
t_lendemain = find("s3", "lendemain")
t_garde = find("s4", "garde")
t_top = find("s5", "top")
t_bas = find("s5", "bas")
t_musique2 = find("s5", "musique")
t_danse = find("s5", "danse")

# ---------- mots clés ----------
c.kw("kw-danser", "IL FAUT DANSER", f"left: 0; right: 0; top: 1330px; text-align: center; color: {INK}; font-size: 104px;",
     t_danser, seams[1] + 0.3)
c.kw("kw-tout", "TOUT PEUT CHANGER<br>DU JOUR AU LENDEMAIN",
     f"left: 0; right: 0; top: 1212px; text-align: center; color: {INK}; font-size: 78px; line-height: 1.05;",
     t_tout, seams[2] - 0.3, anim="rise")
c.kw("kw-garde", "JE GARDE<br>MES POSITIONS",
     f"left: 0; right: 0; top: 1200px; text-align: center; color: {GREEN}; font-size: 104px; line-height: 1;",
     t_garde, seams[3] - 0.3)

# ---------- illustrations ----------
c.ill_css = f""".note {{ position: absolute; font: 800 120px/1 'Inter Tight'; color: {INK}; }}
    #ill-top text {{ font: 700 44px 'Inter Tight'; fill: {GREY}; }}"""
c.ill_html = """<div id="ill-notes" class="ill">
        <div id="n0" class="note" data-layout-ignore style="left:60px; top:20px; opacity:0">♪</div>
        <div id="n1" class="note" data-layout-ignore style="left:250px; top:-20px; opacity:0">♫</div>
        <div id="n2" class="note" data-layout-ignore style="left:620px; top:10px; opacity:0">♪</div>
        <div id="n3" class="note" data-layout-ignore style="left:780px; top:-20px; opacity:0">♫</div>
      </div>
      <div id="ill-top" class="ill">
        <svg viewBox="0 0 900 300">
          <polyline id="curve" class="ink" points="20,270 120,230 200,245 300,170 380,190 450,60 520,120 600,110 680,200 760,180 860,250"/>
          <line id="top-line" x1="400" y1="60" x2="880" y2="60" stroke="#565D6B" stroke-width="6" stroke-dasharray="14 14"/>
          <text id="top-txt" x="880" y="40" text-anchor="end">TOP ABSOLU</text>
          <circle id="dot-bas" cx="600" cy="110" r="22" fill="#0F8A5F"/>
          <text id="bas-txt" x="640" y="140" fill="#0F8A5F" style="fill:#0F8A5F">un peu plus bas</text>
        </svg>
      </div>"""
js = [f'tl.fromTo("#ill-notes", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.1 }}, {round(t_musique - 0.06, 3)});']
for i in range(4):
    js.append(f'tl.fromTo("#n{i}", {{ opacity: 0, scale: 0.3, y: 40, transformOrigin: "50% 100%" }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.35, ease: "back.out(2)" }}, {round(t_musique - 0.04 + i * 0.09, 3)});')
js += [
    f'tl.to("#ill-notes", {{ opacity: 0, duration: 0.25, ease: "power2.in" }}, {round(seams[1] + 0.3, 3)});',
    # la courbe : le top, puis le point vert un peu plus bas
    f'tl.fromTo("#ill-top", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.1 }}, {round(t_top - 0.9, 3)});',
    f'tl.fromTo("#curve", {{ strokeDasharray: 1400, strokeDashoffset: 1400 }}, {{ strokeDashoffset: 0, duration: 0.9, ease: "power2.out" }}, {round(t_top - 0.9, 3)});',
    f'tl.fromTo(["#top-line", "#top-txt"], {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25 }}, {round(t_top - 0.05, 3)});',
    f'tl.fromTo("#dot-bas", {{ opacity: 0, scale: 0.2, transformOrigin: "600px 110px" }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2.5)" }}, {round(t_bas - 0.05, 3)});',
    f'tl.fromTo("#bas-txt", {{ opacity: 0, x: -20 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: "power2.out" }}, {round(t_bas + 0.05, 3)});',
    f'tl.to("#ill-top", {{ opacity: 0, duration: 0.25, ease: "power2.in" }}, {round(t_back - 0.35, 3)});',
]
c.ill_js = js

c.sfx = [
    ("sfx-whoosh-1", "whoosh-short", seams[0] - 0.20, 0.34),
    ("sfx-pop-1", "pop", t_danser + 0.02, 0.30),
    ("sfx-pop-2", "pop", t_bas + 0.02, 0.26),
    ("sfx-whoosh-2", "whoosh", t_back - 0.22, 0.30),
    ("sfx-impact", "impact-bass-1", c.END_T + 0.70, 0.40),
]
c.build()
print(f"retour deux caméras {t_back} | danser {t_danser} | top {t_top} | danse {t_danse}")
