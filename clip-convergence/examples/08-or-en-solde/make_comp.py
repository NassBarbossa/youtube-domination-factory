"""Exemple de référence : composition HyperFrames du clip 08 « L'or est en solde » (EP.03, « Les deux droites »), v2
validée par Nass le 2026-10-25.

Pour un nouveau clip : copier ce fichier dans le dossier du projet, puis adapter les blocs marqués « PROPRE AU CLIP »
(calendrier des bascules, données et graphique, SFX, corrections de sous-titres, mots clés, accroche, CTA).
Le reste (états, cadrage sans trou, sous-titres qui suivent la bande, fin en V -> logo) est la grammaire commune.

Entrées : timeline.json (build_media.py + face_track.py), assets/data/*.json (données réelles et sourcées),
          assets/convergence-logo-clair.svg (copie de {repo}/shows/emission-live/assets/logo/).
Sorties : index.html, compositions/stage.html, compositions/captions.html, assets/sfx/*-n.wav.
Usage : python make_comp.py [dossier_projet]   (par défaut, le dossier de ce fichier)
"""
import json
import math
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
FACES = TL["faces"]
K = TL["prescale"]
VOICE_END = TL["duration_voice"]
END_T = VOICE_END
D = round(END_T + 4.15, 2)   # le CTA reste >= 2 s ; pas de disclaimer à l'image (il va dans la légende)

INK, PAPER, GRID = "#0B0E11", "#F2EFE8", "#E6E1D6"
GOLD, GREEN, RED, GREY = "#C98A0B", "#0F8A5F", "#C8323F", "#565D6B"   # gris foncé : contraste AA sur le papier
GOLD_TXT = "#A07006"   # or foncé pour le TEXTE sur papier (contraste >= 3:1) ; les droites gardent l'or de la marque
MINUS = "\u2212"
CUT = json.loads((HERE / "cut.json").read_text(encoding="utf-8"))
CROP = {cam: (c[2], c[3]) for cam, c in CUT["crops"].items()}   # (largeur, hauteur) des recadrages caméra


def fr_int(v):
    return f"{round(v):,}".replace(",", "\u202f")


# ---------- états de mise en page ----------
# PROPRE À LA MISE EN PAGE : valeurs calées sur des crops de 1028 × ~515 (mise en page « trois bandes » de l'EP.03).
# Autres crops (« fullcam », plus hauts) : recaler échelles et droites sur snapshots. Un seul orateur sans écran :
# ajouter un état B+ (punch-in : Nass +0,10, Sadek +0,06, mêmes droites) et alterner B / B+ à chaque couture.
# g / o = droite verte / or (y à gauche, y à droite) ; nass / sadek = (échelle, y voulu du visage à l'écran)
STATES = {
    "H":   dict(g=(430, 470), o=(900, 840), nass=(1.30, 250), sadek=(1.60, 1190), cap=660),
    "CS":  dict(g=(8, 36), o=(1000, 940), nass=(1.30, -260), sadek=(1.60, 1240), cap=868, chart=(70, 150, 940, 560)),
    "A":   dict(g=(560, 600), o=(860, 800), nass=(1.30, 380), sadek=(1.60, 1166), cap=705),
    "B":   dict(g=(700, 760), o=(1010, 930), nass=(1.50, 420), sadek=(1.30, 1343), cap=850),
    "CN":  dict(g=(540, 580), o=(1340, 1300), nass=(1.30, 330), sadek=(1.30, 1640), cap=1218, chart=(70, 615, 940, 520)),
    "CN+": dict(g=(540, 580), o=(1340, 1300), nass=(1.44, 330), sadek=(1.36, 1640), cap=1218, chart=(70, 615, 940, 520)),  # Sadek bouge aussi : sa coupe tombe en plein mouvement
}


def seg_at(t):
    cur = ORDER[0]
    for sid in ORDER:
        if t >= SEG[sid]["out_start"]:
            cur = sid
    return cur


def cam_tf(cam, st, seg):
    """x, y, échelle CSS du conteneur vidéo : visage cadré, mais le cadre est toujours couvert (pas de trou)"""
    S = STATES[st]
    s, fy_target = S[cam]
    fx, fy = FACES[cam].get(seg, [CROP[cam][0] / 2, CROP[cam][1] * 0.56])   # visage non trouvé : centre, un peu bas
    w, h = CROP[cam][0] * s, CROP[cam][1] * s
    x = min(0.0, max(1080 - w, 540 - fx * s))
    y = fy_target - fy * s
    if cam == "nass":
        y = min(0.0, y)
        y = max(max(S["g"]) + 4 - h, y)          # couvre jusqu'à la droite verte (si impossible, trou en haut, zone système)
    else:
        y = min(min(S["o"]) - 4, y)              # couvre depuis la droite or
    return round(x, 1), round(y, 1), round(s / K, 4)


def poly_nass(g):
    return f"polygon(0px 0px, 1080px 0px, 1080px {g[1]}px, 0px {g[0]}px)"


def poly_sadek(o):
    return f"polygon(0px {o[0]}px, 1080px {o[1]}px, 1080px 1920px, 0px 1920px)"


def find(seg, text, nth=0):
    hits = [w for w in SEG[seg]["words"] if w["w"].strip().lower().lstrip("'").startswith(text.lower())]
    return hits[nth]["s"]


# ---------- calendrier ---------- PROPRE AU CLIP : une bascule par couture de parole, plus l'ouverture du graphique
seams = [SEG[k]["out_start"] for k in ORDER[1:]]
t_chart_open = round(find("s1", "5600") - 0.30, 3)
MOVES = [
    (t_chart_open, "CS"),   # le graphique s'ouvre (Sadek parle)
    (seams[0], "A"),        # s1 -> s2 : le graphique se referme, coupe au milieu du mouvement
    (seams[1], "B"),        # s2 -> s3a : Nass prend l'écran
    (seams[2], "CN"),       # s3a -> s3b : le graphique revient
    (seams[3], "CN+"),      # s3b -> s4a : punch-in
    (seams[4], "CN"),       # s4a -> s4b
    (seams[5], "CN+"),      # s4b -> s5a
    (seams[6], "B"),        # s5a -> s5b : le graphique se referme
]
MOVE_DUR = 0.6


def state_at(t):
    st = "H"
    for tm, s in MOVES:
        if t >= tm:
            st = s
    return st


# ---------- données de l'or ---------- PROPRE AU CLIP : données réelles, source et dates à l'écran
G = json.loads((HERE / "assets/data/or-gcf.json").read_text(encoding="utf-8"))
closes = G["closes"]
ATH = G["ath_intraday"]["value"]
LIVE = 4180
DROP = round((LIVE / ATH - 1) * 100)
CW, CH = 940, 560
PAD_L, PAD_R, PAD_T, PAD_B = 10, 70, 130, 70
YMIN, YMAX = 2400, 5800
n = len(closes)


def cx(i):
    return PAD_L + (CW - PAD_L - PAD_R) * i / (n - 1)


def cy(v):
    return PAD_T + (CH - PAD_T - PAD_B) * (1 - (v - YMIN) / (YMAX - YMIN))


step = max(1, n // 260)
pts = [(cx(i), cy(v)) for i, (_, v) in enumerate(closes) if i % step == 0 or i == n - 1]
poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
plen = sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))
i_ath = [d for d, _ in closes].index(G["ath_intraday"]["date"])
ATH_X, ATH_Y = cx(i_ath), cy(ATH)
LIVE_X, LIVE_Y = cx(n - 1), cy(LIVE)


def chart_tf(st):
    x, y, w, h = STATES[st]["chart"]
    sc = min(1.0, w / CW, h / CH)
    return round(x + (w - CW * sc) / 2, 1), y, round(sc, 4)


# ---------- SFX ---------- PROPRE AU CLIP : 4-5 sons en tout, chacun sur un vrai événement
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

t_5600, t_4180 = find("s1", "5600"), find("s1", "4080")
t_pop25 = round(find("s1", "30") + 0.05, 3)
SFX = [
    ("sfx-whoosh-1", "whoosh-short-n.wav", round(t_chart_open - 0.20, 3), 0.34),
    ("sfx-pop-1", "pop-n.wav", round(t_pop25 + 0.02, 3), 0.30),
    ("sfx-whoosh-2", "whoosh-n.wav", round(seams[1] - 0.22, 3), 0.30),
    ("sfx-impact", "impact-bass-1-n.wav", round(END_T + 0.70, 3), 0.40),
]

# ---------- sous-titres ----------
# PROPRE AU CLIP : erreurs de transcription relevées à l'écoute (chiffres, sigles, mots mal entendus)
FIX = {("s1", "th"): "ATH", ("s1", "4080"): "4 180", ("s1", "5600"): "5 600", ("s3b", "sols"): "soldes"}


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
        if out and out[-1]["t"].lower() == "la" and t == "ATH":
            out[-1]["t"], out[-1]["e"] = "l'ATH", w["e"]
            continue
        out.append({"t": t, "s": w["s"], "e": w["e"]})
    return out


# PROPRE AU CLIP : pas de sous-titres sous l'accroche, ni quand un mot clé porte déjà la phrase
SKIP_BEFORE = round(t_chart_open + 0.32, 3)          # l'accroche tient lieu de sous-titre au début
groups = []
for seg in ORDER:
    if seg == "s2":
        continue                                      # « le prix / le moment » portés par les mots clés
    cur = []
    for w in caption_words(seg):
        if w["s"] < SKIP_BEFORE or (seg == "s3a" and w["s"] < SEG["s3a"]["out_start"] + 0.62):
            continue
        if cur and (len(cur) >= 3 or len(" ".join(x["t"] for x in cur + [w])) > 17 or w["s"] - cur[-1]["e"] > 0.15):
            groups.append((seg, cur))
            cur = []
        cur.append(w)
    if cur:
        groups.append((seg, cur))
INV_T = None
if groups[-1][1][-1]["t"].lower().startswith("investisseur"):
    INV_T = groups[-1][1].pop()["s"]                 # porté par le mot clé final
    if not groups[-1][1]:
        groups.pop()

# ---------- timeline de la scène ----------
js = ["const tl = gsap.timeline({ paused: true });"]
H0 = STATES["H"]
for cam in ("nass", "sadek"):
    x, y, sc = cam_tf(cam, "H", ORDER[0])
    js.append(f'tl.fromTo("#wrap-{cam}", {{ x: {x}, y: {y}, scale: {sc} }}, {{ x: {x}, y: {y}, scale: {sc}, duration: 0.01 }}, 0);')
cs0 = chart_tf("CS")
js.append(f'tl.fromTo("#chart", {{ x: {cs0[0]}, y: {cs0[1]}, scale: {cs0[2]} }}, {{ x: {cs0[0]}, y: {cs0[1]}, scale: {cs0[2]}, duration: 0.01 }}, 0);')
E = "power3.inOut"
for tm, st in MOVES:
    S, t0, seg = STATES[st], round(tm - MOVE_DUR / 2, 3), seg_at(tm + 0.02)
    js += [
        f'tl.to("#stage-nass", {{ clipPath: "{poly_nass(S["g"])}", duration: {MOVE_DUR}, ease: "{E}" }}, {t0});',
        f'tl.to("#stage-sadek", {{ clipPath: "{poly_sadek(S["o"])}", duration: {MOVE_DUR}, ease: "{E}" }}, {t0});',
        f'tl.to("#line-g", {{ attr: {{ y1: {S["g"][0]}, y2: {S["g"][1]} }}, duration: {MOVE_DUR}, ease: "{E}" }}, {t0});',
        f'tl.to("#line-o", {{ attr: {{ y1: {S["o"][0]}, y2: {S["o"][1]} }}, duration: {MOVE_DUR}, ease: "{E}" }}, {t0});',
    ]
    for cam in ("nass", "sadek"):
        x, y, sc = cam_tf(cam, st, seg)
        js.append(f'tl.to("#wrap-{cam}", {{ x: {x}, y: {y}, scale: {sc}, duration: {MOVE_DUR}, ease: "{E}" }}, {t0});')
    if "chart" in S:
        x, y, sc = chart_tf(st)
        js.append(f'tl.to("#chart", {{ x: {x}, y: {y}, scale: {sc}, duration: {MOVE_DUR}, ease: "{E}" }}, {t0});')

# PROPRE AU CLIP : événements du graphique et de l'écran, calés sur les mots
open1, close1, open2, close2 = MOVES[0][0], MOVES[1][0], MOVES[3][0], MOVES[7][0]
js += [
    # accroche
    'tl.fromTo("#hook", { opacity: 1 }, { opacity: 1, duration: 0.01 }, 0);',
    f'tl.to("#hook", {{ opacity: 0, filter: "blur(8px)", duration: 0.2, ease: "power2.in" }}, {open1 - 0.32});',
    # graphique (opacité sur des enfants, jamais sur un .clip)
    f'tl.fromTo("#chart-body", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25, ease: "power2.out" }}, {open1 - 0.05});',
    f'tl.fromTo("#chart-line", {{ strokeDashoffset: {plen:.0f} }}, {{ strokeDashoffset: 0, duration: 0.9, ease: "power2.inOut" }}, {open1});',
    f'tl.fromTo(["#ath", "#ath-dot"], {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "expo.out" }}, {t_5600 - 0.05});',
    f'tl.fromTo(["#live", "#live-dot"], {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "expo.out" }}, {t_4180 - 0.05});',
    f'tl.fromTo("#bracket", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, ease: "power2.out" }}, {t_pop25 - 0.12});',
    f'tl.fromTo("#drop", {{ opacity: 0, scale: 1.25 }}, {{ opacity: 1, scale: 1, duration: 0.5, ease: "expo.out" }}, {t_pop25});',
    f'tl.to("#chart-body", {{ opacity: 0, duration: 0.18, ease: "power2.in" }}, {close1 - 0.25});',
    f'tl.fromTo("#screen", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25, ease: "power2.out" }}, {open2 - 0.05});',
    f'tl.to("#screen", {{ opacity: 0, duration: 0.18, ease: "power2.in" }}, {close2 - 0.25});',
]
# PROPRE AU CLIP — mots clés : « le prix » (or) et « le moment » (vert), empilés ; ils suivent la bande pendant la bascule vers Nass
t_prix, t_moment = find("s2", "prix"), find("s2", "moment")
DY = 155
js += [
    f'tl.fromTo("#kw-prix", {{ opacity: 0, scale: 1.25 }}, {{ opacity: 1, scale: 1, duration: 0.5, ease: "expo.out" }}, {t_prix - 0.08});',
    f'tl.fromTo("#kw-moment", {{ opacity: 0, scale: 1.25 }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "expo.out" }}, {t_moment - 0.08});',
    f'tl.to(["#kw-prix", "#kw-moment"], {{ y: {DY}, duration: {MOVE_DUR}, ease: "{E}" }}, {seams[1] - MOVE_DUR / 2});',
    f'tl.to(["#kw-prix", "#kw-moment"], {{ opacity: 0, filter: "blur(8px)", duration: 0.2, ease: "power2.in" }}, {seams[1] + 0.42});',
]
if INV_T:
    js += [f'tl.fromTo("#kw-inv", {{ opacity: 0, scale: 1.3 }}, {{ opacity: 1, scale: 1, duration: 0.5, ease: "expo.out" }}, {INV_T - 0.06});',
           f'tl.to("#kw-inv", {{ opacity: 0, duration: 0.25, ease: "power2.in" }}, {max(END_T + 0.05, INV_T + 0.46)});']

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
VW = round(CROP["nass"][0] * K / 2) * 2
VH = {cam: round(CROP[cam][1] * K / 2) * 2 for cam in CROP}
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
A, B = STATES["A"], STATES["B"]
# PROPRE AU CLIP dans le HTML : l'accroche (#hook, mots du passage + chiffre réel daté) et le CTA (#cta, numéro de l'épisode)
stage = f"""<template>
  <style>
    @font-face {{ font-family: 'Inter Tight'; src: url('assets/fonts/InterTight-var.ttf') format('truetype'); font-weight: 100 900; }}
    @font-face {{ font-family: 'Plex Mono C'; src: url('assets/fonts/IBMPlexMono-SemiBold.ttf') format('truetype'); font-weight: 600; }}
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
    .panel {{ position: absolute; inset: 0; overflow: hidden; }}
    #stage-nass {{ clip-path: {poly_nass(H0["g"])}; }}
    #stage-sadek {{ clip-path: {poly_sadek(H0["o"])}; }}
    .wrap {{ position: absolute; left: 0; top: 0; width: {VW}px; transform-origin: 0 0; }}
    #wrap-nass {{ height: {VH["nass"]}px; }}
    #wrap-sadek {{ height: {VH["sadek"]}px; }}
    .cam {{ position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: cover; }}
    #lines {{ position: absolute; inset: 0; width: 1080px; height: 1920px; overflow: visible; }}
    #lines line {{ stroke-width: 12; stroke-linecap: round; }}
    #hook {{ position: absolute; left: 0; right: 0; top: 532px; text-align: center; color: {INK}; }}
    #hook .h1 {{ font: 800 104px/0.95 'Inter Tight'; letter-spacing: -0.02em; }}
    #hook .h1 b {{ color: {GOLD_TXT}; font-weight: 800; }}
    #hook .h2 {{ margin-top: 22px; font: 600 32px 'Plex Mono C'; letter-spacing: .12em; color: {INK}; }}
    #chart {{ position: absolute; left: 0; top: 0; width: {CW}px; height: {CH}px; transform-origin: 0 0; }}
    #chart svg {{ position: absolute; left: 0; top: 0; overflow: visible; }}
    .lab {{ position: absolute; white-space: nowrap; color: {INK}; }}
    .lab .v {{ font: 800 60px/1 'Inter Tight'; letter-spacing: -0.01em; }}
    .lab .d {{ margin-top: 6px; font: 600 34px/1 'Plex Mono C'; letter-spacing: .04em; color: {GREY}; }}
    .lab.r {{ text-align: right; }}
    #drop {{ position: absolute; font: 800 76px/1 'Inter Tight'; color: {RED}; letter-spacing: -0.02em; transform-origin: 100% 50%; }}
    #src {{ position: absolute; left: {PAD_L}px; top: {CH - 36}px; font: 600 34px/1 'Plex Mono C'; letter-spacing: .04em; color: {GREY}; }}
    .kw {{ position: absolute; font: 800 96px/1 'Inter Tight'; letter-spacing: -0.03em; white-space: nowrap; }}
    #kw-inv {{ left: 0; right: 0; top: {B["cap"] - 56}px; text-align: center; font-size: 104px; color: {INK}; }}
    #kw-inv span {{ box-shadow: inset 0 -14px 0 {GREEN}; }}
    #screen {{ position: absolute; left: 34px; top: 598px; width: 1012px; height: 552px; overflow: hidden; }}
    #screen video {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
    #logo {{ position: absolute; left: {LX0}px; top: {LY0}px; width: {LOGO_W}px; height: {1669 * ls:.1f}px; }}
    #cta {{ position: absolute; left: 0; right: 0; top: 1068px; text-align: center; font: 700 46px 'Inter Tight'; color: {INK}; }}
  </style>
  <div id="root" data-composition-id="stage" data-width="1080" data-height="1920">
    <div id="stage-nass" class="panel">
      <div id="wrap-nass" class="wrap">
          {vids["nass"]}
      </div>
    </div>
    <div id="stage-sadek" class="panel">
      <div id="wrap-sadek" class="wrap">
          {vids["sadek"]}
      </div>
    </div>

    <div id="hook">
      <div class="h1">L'OR EST<br><b>EN SOLDE</b></div>
      <div class="h2">{MINUS}{abs(DROP)} % DEPUIS SON RECORD</div>
    </div>

    <div id="chart">
      <div id="chart-body" style="opacity:0">
        <svg width="{CW}" height="{CH}" viewBox="0 0 {CW} {CH}">
          <polyline id="chart-line" points="{poly}" fill="none" stroke="{GOLD}" stroke-width="6" stroke-linejoin="round"
                    stroke-linecap="round" stroke-dasharray="{plen:.0f}" stroke-dashoffset="{plen:.0f}"/>
          <g id="bracket" opacity="0"><line x1="{LIVE_X + 34:.1f}" y1="{ATH_Y:.1f}" x2="{LIVE_X + 34:.1f}" y2="{LIVE_Y:.1f}" stroke="{RED}" stroke-width="5" stroke-dasharray="10 8"/></g>
          <circle id="ath-dot" cx="{ATH_X:.1f}" cy="{ATH_Y:.1f}" r="11" fill="{INK}" opacity="0" style="transform-origin: {ATH_X:.1f}px {ATH_Y:.1f}px"/>
          <circle id="live-dot" cx="{LIVE_X:.1f}" cy="{LIVE_Y:.1f}" r="11" fill="{INK}" opacity="0" style="transform-origin: {LIVE_X:.1f}px {LIVE_Y:.1f}px"/>
        </svg>
        <div id="ath" class="lab" style="left:{ATH_X - 130:.0f}px; top:{ATH_Y - 120:.0f}px; transform-origin: 130px 120px; opacity:0">
          <div class="v">{fr_int(ATH)} $</div><div class="d">RECORD · 29 JANV. 2026</div>
        </div>
        <div id="live" class="lab r" style="left:{LIVE_X - 560:.0f}px; width:560px; top:{LIVE_Y + 40:.0f}px; transform-origin: 560px -40px; opacity:0">
          <div class="v">4 180 $</div><div class="d">19 OCT. 2026 · ÉMISSION</div>
        </div>
        <div id="drop" data-layout-allow-overlap style="left:{LIVE_X - 200:.0f}px; top:{ATH_Y + 2:.0f}px; opacity:0">{MINUS}{abs(DROP)} %</div>
        <div id="src">SOURCE : YAHOO FINANCE (GC=F)</div>
      </div>
    </div>

    <div id="screen" style="opacity:0">
          {screen_vids}
    </div>

    <div id="kw-moment" class="kw" style="right: 70px; top: {A["g"][1] + 16}px; color: {GREEN}; opacity:0">LE MOMENT</div>
    <div id="kw-prix" class="kw" style="left: 70px; top: {A["o"][0] - 124}px; color: {GOLD_TXT}; opacity:0">LE PRIX</div>
    <div id="kw-inv" class="kw" style="opacity:0"><span>INVESTISSEUR</span></div>

    <svg id="logo" viewBox="-89 -89 21736 1669" style="opacity:0">{logo_path}</svg>
    <svg id="lines" viewBox="0 0 1080 1920">
      <line id="line-g" x1="-30" y1="{H0["g"][0]}" x2="1110" y2="{H0["g"][1]}" stroke="{GREEN}"/>
      <line id="line-o" x1="-30" y1="{H0["o"][0]}" x2="1110" y2="{H0["o"][1]}" stroke="{GOLD}"/>
      <circle id="v-dot" cx="{VX}" cy="{VBOT}" r="34" fill="{INK}" opacity="0" style="transform-origin: {VX}px {VBOT}px"/>
    </svg>

    <div id="cta" style="opacity:0">Épisode 3 complet sur la chaîne</div>
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
    <!-- Short 08 « L'or est en solde » — Convergence EP.03, concept « Les deux droites ». Voix réelles de Sadek et Nass, pas de musique. -->
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
print(f"durée {D} s | groupes {len(groups)} | graphique {t_chart_open} | coutures {seams}")
