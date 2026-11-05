"""Composition HyperFrames du clip 35 « La meilleure des positions » (Convergence EP.01).

Variante « écran + médaillons » de la DA « Les deux droites » : dans la scène « À L'ÉCRAN » de l'EP.01, les caméras
sont des ronds d'environ 330 px, trop petits pour remplir les cadres du pilote 08. Ici, l'écran réel de Nass occupe
la bande quand il explique, et les deux caméras rondes du live sont des médaillons (cercle vert = Nass, or = Sadek)
posés sur le papier, de part et d'autre des deux droites. Le reste est la grammaire commune au pilote 08 : droites,
bascules de 0,6 s aux coutures, sous-titres qui suivent la bande, mot clé, fin en V -> logo, 4 SFX, pas de musique.

Entrées : cut.json, timeline.json (build_media.py + face_track.py), assets/video/{nass,sadek,screen}_<seg>.mp4,
          assets/audio/voice.wav, assets/sfx/*.mp3, assets/fonts/, assets/convergence-logo-clair.svg.
Sorties : index.html, compositions/stage.html, compositions/captions.html, assets/sfx/*-n.wav.
Usage : python make_comp.py [dossier_projet]   (par défaut, le dossier de ce fichier)
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent
FF = shutil.which("ffmpeg") or sys.exit("ffmpeg introuvable dans le PATH")
LOGO = HERE / "assets/convergence-logo-clair.svg"
TL = json.loads((HERE / "timeline.json").read_text(encoding="utf-8"))
SEG = {s["id"]: s for s in TL["segments"]}
ORDER = [s["id"] for s in TL["segments"]]
K = TL["prescale"]
VOICE_END = TL["duration_voice"]
END_T = VOICE_END
D = round(END_T + 4.15, 2)   # le CTA reste >= 2 s ; pas de disclaimer à l'image (il va dans la légende)

INK, PAPER, GRID = "#0B0E11", "#F2EFE8", "#E6E1D6"
GOLD, GREEN, RED, GREY = "#C98A0B", "#0F8A5F", "#C8323F", "#565D6B"
GOLD_TXT = "#A07006"   # or foncé pour le TEXTE sur papier (contraste >= 3:1)
CUT = json.loads((HERE / "cut.json").read_text(encoding="utf-8"))
CROP = {cam: (c[2], c[3]) for cam, c in CUT["crops"].items()}
VW = {cam: round(CROP[cam][0] * K / 2) * 2 for cam in CROP}      # côté du médaillon vidéo (px) avant échelle CSS
SX, SY, SW_, SH_ = 34, 600, CUT["screen"]["size"][0], CUT["screen"]["size"][1]   # boîte de l'écran réel

# ---------- états ---------- PROPRE À LA MISE EN PAGE « écran + médaillons »
# g / o = droite verte / or (y à gauche, y à droite) ; nass / sadek = (cx, cy, diamètre) du médaillon à l'écran ;
# cap = y des sous-titres. Grossissement total (prescale × CSS) <= 1,6 : diamètre <= 1,6 × côté du crop.
STATES = {
    "H":  dict(g=(430, 470), o=(900, 840),   nass=(540, 225, 400), sadek=(540, 1160, 400), cap=660),                # accroche
    "E":  dict(g=(540, 580), o=(1340, 1300), nass=(260, 300, 400), sadek=(820, 1530, 300), cap=1218, screen=True),  # Nass explique à l'écran
    "E+": dict(g=(540, 580), o=(1340, 1300), nass=(260, 300, 430), sadek=(820, 1530, 320), cap=1218, screen=True),  # punch-in
    "N":  dict(g=(700, 760), o=(1010, 930),  nass=(540, 370, 460), sadek=(540, 1260, 360), cap=850),                # Nass parle
    "S":  dict(g=(560, 600), o=(860, 800),   nass=(540, 290, 360), sadek=(540, 1140, 470), cap=705),                # Sadek parle
}
for st, S in STATES.items():
    for cam in ("nass", "sadek"):
        assert S[cam][2] <= 1.6 * CROP[cam][0] + 1, f"{st} {cam} : médaillon trop grossi (flou)"


def med_tf(cam, st):
    """x, y, échelle CSS du médaillon (transform-origin 0 0) pour l'état st."""
    cx, cy, d = STATES[st][cam]
    s = d / VW[cam]
    return round(cx - d / 2, 1), round(cy - d / 2, 1), round(s, 4)


def seg_at(t):
    cur = ORDER[0]
    for sid in ORDER:
        if t >= SEG[sid]["out_start"]:
            cur = sid
    return cur


def find(seg, text, nth=0):
    hits = [w for w in SEG[seg]["words"] if w["w"].strip().lower().lstrip("'").startswith(text.lower())]
    return hits[nth]["s"]


# ---------- calendrier ---------- PROPRE AU CLIP : une bascule par couture de parole
seams = [SEG[k]["out_start"] for k in ORDER[1:]]
MOVES = [
    (seams[0], "E"),    # s1 -> s2 : l'écran s'ouvre, Nass dessine break / retest
    (seams[1], "E+"),   # s2 -> s3 : punch-in, « giga résistance »
    (seams[2], "N"),    # s3 -> s4 : l'écran se referme, le philosophe
    (seams[3], "S"),    # s4 -> s5 : Sadek finit la phrase
    (seams[4], "N"),    # s5 -> s6 : « Exactement »
]
MOVE_DUR = 0.6
E = "power3.inOut"
t_screen_open, t_screen_close = seams[0], seams[2]
t_patienter = find("s3", "patienter")

# ---------- SFX ---------- 4 sons, chacun sur un vrai événement
SFX_SRC = [("whoosh-short", "whoosh-short", 0.55, ""), ("whoosh", "whoosh-short", 0.62, "asetrate=48000*0.86,aresample=48000,"),
           ("pop", "pop", 0.40, ""), ("impact-bass-1", "impact-bass-1", 1.00, "")]
for name, base, keep, var in SFX_SRC:
    src, out = HERE / f"assets/sfx/{base}.mp3", HERE / f"assets/sfx/{name}-n.wav"
    vd = subprocess.run([FF, "-hide_banner", "-i", str(src), "-af", f"{var}atrim=0:{keep},volumedetect", "-f", "null", "-"],
                        capture_output=True, text=True).stderr
    peak = float(vd.split("max_volume:")[1].split("dB")[0])
    subprocess.run([FF, "-v", "error", "-y", "-i", str(src), "-af",
                    f"{var}atrim=0:{keep},volume={-1 - peak:.2f}dB,afade=t=out:st={keep - 0.08:.2f}:d=0.08", "-ar", "48000",
                    str(out)], check=True)
SFX = [
    ("sfx-whoosh-1", "whoosh-short-n.wav", round(t_screen_open - 0.20, 3), 0.34),   # l'écran s'ouvre
    ("sfx-pop-1", "pop-n.wav", round(t_patienter + 0.02, 3), 0.30),                  # PATIENTER
    ("sfx-whoosh-2", "whoosh-n.wav", round(seams[3] - 0.22, 3), 0.30),               # la voix passe à Sadek
    ("sfx-impact", "impact-bass-1-n.wav", round(END_T + 0.70, 3), 0.40),             # les droites touchent le logo
]

# ---------- sous-titres ----------
FIX = {}   # PROPRE AU CLIP : rien à corriger à l'écoute (vérifié avec qa_voice_mlx.py)


def caption_words(seg):
    out = []
    for w in SEG[seg]["words"]:
        t = FIX.get((seg, w["w"].strip()), w["w"].strip())
        if not t:
            continue
        if out and (t.startswith("'") or t.startswith("-") or t == "%"):
            out[-1]["t"] += (" %" if t == "%" else t)
            out[-1]["e"] = w["e"]
            continue
        out.append({"t": t, "s": w["s"], "e": w["e"]})
    return out


SKIP_BEFORE = seams[0]   # l'accroche tient lieu de sous-titre pendant s1
groups = []
for seg in ORDER:
    cur = []
    for w in caption_words(seg):
        if w["s"] < SKIP_BEFORE:
            continue
        if cur and (len(cur) >= 3 or len(" ".join(x["t"] for x in cur + [w])) > 17 or w["s"] - cur[-1]["e"] > 0.15):
            groups.append((seg, cur))
            cur = []
        cur.append(w)
    if cur:
        groups.append((seg, cur))
# « patienter » est porté par le mot clé, pas par le sous-titre
PAT_T, PAT_GI = None, None
for gi, (seg, ws) in enumerate(groups):
    if seg == "s3" and ws[-1]["t"].lower().startswith("patienter"):
        PAT_T = ws.pop()["s"]
        if ws:
            PAT_GI = gi          # ce groupe s'efface avant l'arrivée du mot clé (même place à l'écran)
        else:
            groups.pop(gi)
        break

# ---------- timeline de la scène ----------
js = ["const tl = gsap.timeline({ paused: true });"]
H0 = STATES["H"]
for cam in ("nass", "sadek"):
    x, y, sc = med_tf(cam, "H")
    js.append(f'tl.fromTo("#wrap-{cam}", {{ x: {x}, y: {y}, scale: {sc} }}, {{ x: {x}, y: {y}, scale: {sc}, duration: 0.01 }}, 0);')
for tm, st in MOVES:
    S, t0 = STATES[st], round(tm - MOVE_DUR / 2, 3)
    js += [
        f'tl.to("#line-g", {{ attr: {{ y1: {S["g"][0]}, y2: {S["g"][1]} }}, duration: {MOVE_DUR}, ease: "{E}" }}, {t0});',
        f'tl.to("#line-o", {{ attr: {{ y1: {S["o"][0]}, y2: {S["o"][1]} }}, duration: {MOVE_DUR}, ease: "{E}" }}, {t0});',
    ]
    for cam in ("nass", "sadek"):
        x, y, sc = med_tf(cam, st)
        js.append(f'tl.to("#wrap-{cam}", {{ x: {x}, y: {y}, scale: {sc}, duration: {MOVE_DUR}, ease: "{E}" }}, {t0});')

js += [
    # accroche
    'tl.fromTo("#hook", { opacity: 1 }, { opacity: 1, duration: 0.01 }, 0);',
    f'tl.to("#hook", {{ opacity: 0, filter: "blur(8px)", duration: 0.2, ease: "power2.in" }}, {round(t_screen_open - 0.32, 3)});',
    # écran réel de Nass (opacité sur un enfant, jamais sur un .clip)
    f'tl.fromTo("#screen-body", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25, ease: "power2.out" }}, {round(t_screen_open - 0.05, 3)});',
    f'tl.to("#screen-body", {{ opacity: 0, duration: 0.18, ease: "power2.in" }}, {round(t_screen_close - 0.25, 3)});',
]
if PAT_T:
    js += [f'tl.fromTo("#kw-pat", {{ opacity: 0, scale: 1.3 }}, {{ opacity: 1, scale: 1, duration: 0.5, ease: "expo.out" }}, {round(PAT_T - 0.06, 3)});',
           f'tl.to("#kw-pat", {{ opacity: 0, filter: "blur(8px)", duration: 0.2, ease: "power2.in" }}, {round(t_screen_close - 0.3, 3)});']

# ---------- fin : les deux droites -> grand V -> le V du vrai logo ----------
LOGO_W, LX0, LY0 = 900, 90, 930
ls = LOGO_W / 21736
VG = [(90 + (6488.0 + 89) * ls, LY0 + (122.9 + 89) * ls), (90 + (7110.1 + 89) * ls, LY0 + (1367.1 + 89) * ls)]
VV = [(90 + (7732.2 + 89) * ls, LY0 + (122.9 + 89) * ls), VG[1]]
SW = round(245.9 * ls, 2)
VX, VTOP, VBOT, VHALF = 540, 520, 820, 150
js += [
    f'tl.to(["#stage-nass", "#stage-sadek"], {{ opacity: 0, duration: 0.45, ease: "power2.in" }}, {END_T});',
    f'tl.to("#line-o", {{ attr: {{ x1: {VX - VHALF}, y1: {VTOP}, x2: {VX}, y2: {VBOT} }}, strokeWidth: 46, duration: 0.7, ease: "{E}" }}, {END_T});',
    f'tl.to("#line-g", {{ attr: {{ x1: {VX + VHALF}, y1: {VTOP}, x2: {VX}, y2: {VBOT} }}, strokeWidth: 46, duration: 0.7, ease: "{E}" }}, {END_T});',
    f'tl.fromTo("#v-dot", {{ opacity: 0, scale: 0.2 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "expo.out" }}, {END_T + 0.68});',
    f'tl.to("#line-o", {{ attr: {{ x1: {VG[0][0]:.1f}, y1: {VG[0][1]:.1f}, x2: {VG[1][0]:.1f}, y2: {VG[1][1]:.1f} }}, strokeWidth: {SW}, duration: 0.5, ease: "{E}" }}, {END_T + 1.1});',
    f'tl.to("#line-g", {{ attr: {{ x1: {VV[0][0]:.1f}, y1: {VV[0][1]:.1f}, x2: {VV[1][0]:.1f}, y2: {VV[1][1]:.1f} }}, strokeWidth: {SW}, duration: 0.5, ease: "{E}" }}, {END_T + 1.1});',
    f'tl.to("#v-dot", {{ opacity: 0, scale: 0.2, duration: 0.3, ease: "power2.in" }}, {END_T + 1.1});',
    f'tl.fromTo("#logo", {{ opacity: 0, filter: "blur(6px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.25, ease: "power2.out" }}, {END_T + 1.42});',
    f'tl.fromTo("#cta", {{ opacity: 0, filter: "blur(8px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power2.out" }}, {END_T + 1.75});',
    'window.__timelines["stage"] = tl;',
]

# ---------- HTML : scène ----------
vids = {cam: "\n          ".join(
    f'<video id="{cam}-{s["id"]}" class="clip cam" src="assets/video/{cam}_{s["id"]}.mp4" muted playsinline '
    f'data-start="{s["out_start"]}" data-duration="{s["dur"]}" data-media-start="{TL["handle"]}" '
    f'data-track-index="{1 if cam == "nass" else 2}"></video>' for s in TL["segments"]) for cam in CROP}
screen_vids = "\n          ".join(
    f'<video id="screen-{s["id"]}" class="clip" src="assets/video/screen_{s["id"]}.mp4" muted playsinline '
    f'data-start="{s["out_start"]}" data-duration="{s["dur"]}" data-media-start="{TL["handle"]}" data-track-index="9"></video>'
    for s in TL["segments"] if (HERE / f'assets/video/screen_{s["id"]}.mp4').exists())
logo_svg = LOGO.read_text(encoding="utf-8")
logo_path = re.search(r"<path[^>]*/>", logo_svg).group(0)
# PROPRE AU CLIP dans le HTML : l'accroche (#hook, leurs mots, pas de chiffre), le mot clé (#kw-pat) et le CTA (#cta)
stage = f"""<template>
  <style>
    @font-face {{ font-family: 'Inter Tight'; src: url('assets/fonts/InterTight-var.ttf') format('truetype'); font-weight: 100 900; }}
    @font-face {{ font-family: 'Plex Mono C'; src: url('assets/fonts/IBMPlexMono-SemiBold.ttf') format('truetype'); font-weight: 600; }}
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
    .panel {{ position: absolute; inset: 0; overflow: hidden; }}
    .wrap {{ position: absolute; left: 0; top: 0; border-radius: 50%; overflow: hidden; transform-origin: 0 0; }}
    #wrap-nass {{ width: {VW["nass"]}px; height: {VW["nass"]}px; }}
    #wrap-sadek {{ width: {VW["sadek"]}px; height: {VW["sadek"]}px; }}
    .cam {{ position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: cover; }}
    .ring {{ position: absolute; inset: 0; border-radius: 50%; }}
    #ring-nass {{ box-shadow: inset 0 0 0 14px {GREEN}; }}
    #ring-sadek {{ box-shadow: inset 0 0 0 14px {GOLD}; }}
    #lines {{ position: absolute; inset: 0; width: 1080px; height: 1920px; overflow: visible; }}
    #lines line {{ stroke-width: 12; stroke-linecap: round; }}
    #hook {{ position: absolute; left: 0; right: 0; top: 532px; text-align: center; color: {INK}; }}
    #hook .h1 {{ font: 800 104px/0.95 'Inter Tight'; letter-spacing: -0.02em; }}
    #hook .h1 b {{ color: {GOLD_TXT}; font-weight: 800; }}
    #screen {{ position: absolute; left: {SX}px; top: {SY}px; width: {SW_}px; height: {SH_}px; overflow: hidden; }}
    #screen-body {{ position: absolute; inset: 0; }}
    #screen video {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
    .kw {{ position: absolute; font: 800 104px/1 'Inter Tight'; letter-spacing: -0.03em; white-space: nowrap; }}
    #kw-pat {{ left: 0; right: 0; top: {STATES["E"]["cap"] - 56}px; text-align: center; color: {INK}; }}
    #kw-pat span {{ box-shadow: inset 0 -14px 0 {GREEN}; }}
    #logo {{ position: absolute; left: {LX0}px; top: {LY0}px; width: {LOGO_W}px; height: {1669 * ls:.1f}px; }}
    #cta {{ position: absolute; left: 0; right: 0; top: 1068px; text-align: center; font: 700 46px 'Inter Tight'; color: {INK}; }}
  </style>
  <div id="root" data-composition-id="stage" data-width="1080" data-height="1920">
    <div id="screen">
      <div id="screen-body" style="opacity:0">
          {screen_vids}
      </div>
    </div>
    <div id="stage-nass" class="panel">
      <div id="wrap-nass" class="wrap">
          {vids["nass"]}
          <div id="ring-nass" class="ring"></div>
      </div>
    </div>
    <div id="stage-sadek" class="panel">
      <div id="wrap-sadek" class="wrap">
          {vids["sadek"]}
          <div id="ring-sadek" class="ring"></div>
      </div>
    </div>

    <div id="hook">
      <div class="h1">LA MEILLEURE<br><b>DES POSITIONS</b></div>
    </div>

    <div id="kw-pat" class="kw" style="opacity:0"><span>PATIENTER</span></div>

    <svg id="logo" viewBox="-89 -89 21736 1669" style="opacity:0">{logo_path}</svg>
    <svg id="lines" viewBox="0 0 1080 1920">
      <line id="line-g" x1="-30" y1="{H0["g"][0]}" x2="1110" y2="{H0["g"][1]}" stroke="{GREEN}"/>
      <line id="line-o" x1="-30" y1="{H0["o"][0]}" x2="1110" y2="{H0["o"][1]}" stroke="{GOLD}"/>
      <circle id="v-dot" cx="{VX}" cy="{VBOT}" r="34" fill="{INK}" opacity="0" style="transform-origin: {VX}px {VBOT}px"/>
    </svg>

    <div id="cta" style="opacity:0">Épisode 1 complet sur la chaîne</div>
  </div>
  <script>
    {(chr(10) + '    ').join(js)}
  </script>
</template>
"""
(HERE / "compositions").mkdir(exist_ok=True)
(HERE / "compositions/stage.html").write_text(stage, encoding="utf-8")

# ---------- HTML : sous-titres ----------
cap_html, cap_js = [], ["const tl = gsap.timeline({ paused: true });"]
for gi, (seg, ws) in enumerate(groups):
    color = GREEN if SEG[seg]["speaker"] == "nass" else GOLD
    start = round(max(ws[0]["s"] - 0.05, 0), 3)
    nxt = groups[gi + 1][1][0]["s"] - 0.05 if gi + 1 < len(groups) else None
    end = round(min(ws[-1]["e"] + 0.18, nxt if nxt else 1e9, VOICE_END), 3)
    if gi == PAT_GI:
        end = round(min(end, PAT_T - 0.08), 3)
    spans = " ".join(f'<span class="w" id="c{gi}w{wi}">{w["t"]}<i style="background:{color}"></i></span>' for wi, w in enumerate(ws))
    cap_html.append(f'<div id="cg{gi}" class="clip grp" data-start="{start}" data-duration="{round(end - start, 3)}">{spans}</div>')
    cap_js.append(f'tl.fromTo("#cg{gi}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.08, ease: "power2.out" }}, {start});')
    for wi, w in enumerate(ws):
        gap = ws[wi + 1]["s"] - w["s"] if wi + 1 < len(ws) else 1.0
        d_in = round(max(0.03, min(0.12, gap - 0.01)), 3)
        cap_js.append(f'tl.fromTo("#c{gi}w{wi} i", {{ scaleX: 0 }}, {{ scaleX: 1, duration: {d_in}, ease: "power2.out" }}, {round(w["s"], 3)});')
        if wi + 1 < len(ws):
            off_at = max(ws[wi + 1]["s"], w["s"] + d_in + 0.002)
            cap_js.append(f'tl.to("#c{gi}w{wi} i", {{ scaleX: 0, duration: 0.06, ease: "power2.in" }}, {round(off_at, 3)});')
cap_js.append(f'tl.fromTo("#capwrap", {{ y: {STATES["H"]["cap"]} }}, {{ y: {STATES["H"]["cap"]}, duration: 0.01 }}, 0);')
for tm, st in MOVES:
    cap_js.append(f'tl.to("#capwrap", {{ y: {STATES[st]["cap"]}, duration: {MOVE_DUR}, ease: "{E}" }}, {round(tm - MOVE_DUR / 2, 3)});')
cap_js.append('window.__timelines["captions"] = tl;')
captions = f"""<template>
  <style>
    @font-face {{ font-family: 'Inter Tight'; src: url('assets/fonts/InterTight-var.ttf') format('truetype'); font-weight: 100 900; }}
    #root {{ position: absolute; inset: 0; }}
    #capwrap {{ position: absolute; left: 0; right: 0; top: 0; height: 0; overflow: visible; }}
    .grp {{ position: absolute; left: 130px; right: 130px; top: -40px; text-align: center; font: 800 70px/1.08 'Inter Tight';
            letter-spacing: -0.01em; color: {INK}; overflow: visible; }}
    .w {{ position: relative; display: inline-block; }}
    .w i {{ position: absolute; left: 0; right: 0; bottom: -8px; height: 9px; border-radius: 5px; transform-origin: 0 50%; transform: scaleX(0); }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
    <div id="capwrap" data-motion-blur="off">
    {(chr(10) + '    ').join(cap_html)}
    </div>
  </div>
  <script>
    {(chr(10) + '    ').join(cap_js)}
  </script>
</template>
"""
(HERE / "compositions/captions.html").write_text(captions, encoding="utf-8")

# ---------- HTML : racine ----------
sfx_tags = "\n      ".join(
    f'<audio id="{i}" class="clip" src="assets/sfx/{f}" data-start="{t}" data-volume="{v}" data-track-index="{5 + k}"></audio>'
    for k, (i, f, t, v) in enumerate(SFX))
index = f"""<!doctype html>
<html lang="fr" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: {PAPER}; }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; }}
      #ground {{ position: absolute; inset: 0; background: {PAPER};
        background-image: linear-gradient({GRID} 1px, transparent 1px), linear-gradient(90deg, {GRID} 1px, transparent 1px);
        background-size: 96px 96px; background-position: -12px -12px; }}
    </style>
  </head>
  <body>
    <!-- Short 35 « La meilleure des positions » — Convergence EP.01, DA « Les deux droites », variante écran + médaillons. Voix réelles, pas de musique. -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1080" data-height="1920" data-fps="60" data-motion-blur="on">
      <div id="ground"></div>
      <div id="stage" data-composition-id="stage" data-composition-src="compositions/stage.html" data-start="0" data-duration="{D}"
           data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920"></div>
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0"
           data-duration="{VOICE_END}" data-track-index="3" data-track-kind="captions" data-width="1080" data-height="1920"></div>
      <audio id="voice" class="clip" src="assets/audio/voice.wav" data-start="0" data-volume="1" data-track-index="4"></audio>
      {sfx_tags}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
(HERE / "index.html").write_text(index, encoding="utf-8")
print(f"durée {D} s | groupes {len(groups)} | écran {t_screen_open}-{t_screen_close} | PATIENTER {PAT_T} | coutures {seams}")
