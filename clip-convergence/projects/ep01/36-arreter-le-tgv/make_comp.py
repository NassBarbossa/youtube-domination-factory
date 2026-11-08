"""Composition HyperFrames du clip 36 « Arrêter le TGV en pleine route » (Convergence EP.01).

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
HAS_SCREEN = "screen" in CUT
SX, SY, SW_, SH_ = 34, 600, 1012, 552   # boîte de l'écran réel (inutilisée ici : pas d'écran dans ce clip)

# ---------- états ---------- PROPRE À LA MISE EN PAGE « écran + médaillons »
# g / o = droite verte / or (y à gauche, y à droite) ; nass / sadek = (cx, cy, diamètre) du médaillon à l'écran ;
# cap = y des sous-titres. Grossissement total (prescale × CSS) <= 1,6 : diamètre <= 1,6 × côté du crop.
# Mise en page symétrique demandée par Nass (2026-11-07) : le même nombre de pixels e au-dessus de la caméra du haut, entre
# cette caméra et la droite verte, entre les deux droites (bande des sous-titres), entre la droite or et la caméra du bas, et
# sous la caméra du bas. Droites horizontales pour que ces écarts se lisent. 5e + d_haut + d_bas = 1920.
FH = 1920


def sym(top_cam, d_top, d_bot, band_mult=1, hook=None):
    """État symétrique : top_cam est la caméra du haut ("nass" ou "sadek"). band_mult = bande entre les droites en multiples de e."""
    e = (FH - d_top - d_bot) / (4 + band_mult)
    g = e + d_top + e
    o = g + band_mult * e
    cams = {top_cam: (540, round(e + d_top / 2), d_top),
            ("sadek" if top_cam == "nass" else "nass"): (540, round(o + e + d_bot / 2), d_bot)}
    st = dict(g=(round(g), round(g)), o=(round(o), round(o)), cap=round(g + band_mult * e / 2), e=round(e), **cams)
    if hook is not None:
        st["hook"] = round(g + (band_mult * e - hook) / 2)
    return st


def sym_screen(d_top, d_bot, sw, sh, cap_h=100):
    """État écran : Nass en haut à gauche, écran + sous-titres dans la bande, Sadek en bas à droite, mêmes écarts e."""
    band = 14 + sh + 16 + cap_h + 14
    e = (FH - d_top - d_bot - band) / 4
    g = e + d_top + e
    o = g + band
    return dict(g=(round(g), round(g)), o=(round(o), round(o)), nass=(300, round(e + d_top / 2), d_top),
                sadek=(780, round(o + e + d_bot / 2), d_bot), cap=round(g + 14 + sh + 16 + cap_h / 2), e=round(e),
                screen=True, sx=round((1080 - sw) / 2), sy=round(g + 14), sw=sw, sh=sh)


def solo(cam, d, e=130):
    """Monologue (demande de Nass, 2026-11-07) : une seule caméra, grande, en haut ; la bande entre les droites porte les
    illustrations (zone ILL) et les sous-titres plus gros en dessous. L'autre caméra se range derrière, invisible."""
    g, o = e + d + e, FH - e
    other = "sadek" if cam == "nass" else "nass"
    return {cam: (540, round(e + d / 2), d), other: (540, round(e + d / 2), 400), "g": (g, g), "o": (o, o),
            "cap": g + 440, "e": e, "solo": cam, "capscale": 1.25}


ILL = dict(left=90, top=1180, w=900, h=300)   # zone des illustrations dans la bande des états solo (g = 1160, o = 1790)

STATES = {
    "H":  sym("nass", 620, 620, band_mult=3, hook=200),   # accroche : les deux à 620, bande de 3e pour les deux lignes du titre
    "E":  sym_screen(480, 520, 900, 491),                   # Nass explique à l'écran
    "E+": sym_screen(500, 520, 900, 491),                   # punch-in
    "N":  sym("nass", 740, 660),                            # Nass parle
    "N+": sym("nass", 760, 660),                            # punch-in Nass
    "S":  sym("nass", 660, 740),                            # Sadek parle (Nass reste en haut, plus petit)
    "S+": sym("nass", 660, 760),                            # punch-in Sadek
    "SOLO_S": solo("sadek", 900), "SOLO_S+": solo("sadek", 940),   # monologue de Sadek
    "SOLO_N": solo("nass", 900), "SOLO_N+": solo("nass", 940),     # monologue de Nass
}


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
t_back = round(seams[2] - 1.3, 3)     # retour aux deux caméras 1 s avant que Nass parle (bascule comprise)
t_solo_n = round(seams[2] + 0.4, 3)   # puis Nass seul, une fois qu'il a la parole
MOVES = [
    (seams[0], "SOLO_S"),    # s1 -> s2 : Sadek seul (monologue)
    (t_back, "S"),           # les deux caméras reviennent avant la passe de parole
    (t_solo_n, "SOLO_N"),    # Nass seul (monologue)
    (seams[3], "SOLO_N+"),   # s4 -> s5 : punch-in sur Nass (« faire du contre-tendance »)
]
MOVE_DUR = 0.6
E = "power3.inOut"
t_first = seams[0]
t_tgv = find("s3", "tgv")
t_route = find("s3", "route")
t_casse = find("s2", "casse")
t_bougies = find("s2", "bougies")
t_tendance = find("s4", "tendance")
t_friend = find("s4", "friend")
t_contre = find("s5", "contre")
ws5 = SEG["s5"]["words"]
i_pire = next(i for i, w in enumerate(ws5) if w["w"].strip().lower().startswith("pire"))
t_chute = ws5[i_pire - 1]["s"]   # « la » pire chose à faire

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
    ("sfx-whoosh-1", "whoosh-short-n.wav", round(t_first - 0.20, 3), 0.34),      # première bascule : Sadek seul
    ("sfx-whoosh-2", "whoosh-n.wav", round(t_tgv - 0.05, 3), 0.34),               # le train entre
    ("sfx-pop-1", "pop-n.wav", round(t_friend + 0.02, 3), 0.30),                  # « friend » : la flèche pulse
    ("sfx-impact", "impact-bass-1-n.wav", round(END_T + 0.70, 3), 0.40),          # les droites touchent le logo
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


SKIP_BEFORE = t_first   # l'accroche tient lieu de sous-titre pendant s1
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
# « la pire chose à faire » est portée par le mot clé de chute, pas par les sous-titres
PAT_T, PAT_GI = t_chute, None
kept = []
for gi, (seg, ws) in enumerate(groups):
    if seg == "s5" and ws[0]["s"] >= t_chute - 0.01:
        continue                                  # groupes « la pire chose » / « à faire »
    ws[:] = [w for w in ws if not (seg == "s5" and w["s"] >= t_chute - 0.01)]
    if ws:
        kept.append((seg, ws))
groups = kept
PAT_GI = len(groups) - 1                          # le dernier groupe s'efface avant le mot clé

# ---------- timeline de la scène ----------
js = ["const tl = gsap.timeline({ paused: true });"]
H0 = STATES["H"]
for cam in ("nass", "sadek"):
    x, y, sc = med_tf(cam, "H")
    js.append(f'tl.fromTo("#wrap-{cam}", {{ x: {x}, y: {y}, scale: {sc} }}, {{ x: {x}, y: {y}, scale: {sc}, duration: 0.01 }}, 0);')
    js.append(f'tl.fromTo("#stage-{cam}", {{ opacity: 1 }}, {{ opacity: 1, duration: 0.01 }}, 0);')
for tm, st in MOVES:
    S, t0 = STATES[st], round(tm - MOVE_DUR / 2, 3)
    js += [
        f'tl.to("#line-g", {{ attr: {{ y1: {S["g"][0]}, y2: {S["g"][1]} }}, duration: {MOVE_DUR}, ease: "{E}" }}, {t0});',
        f'tl.to("#line-o", {{ attr: {{ y1: {S["o"][0]}, y2: {S["o"][1]} }}, duration: {MOVE_DUR}, ease: "{E}" }}, {t0});',
    ]
    for cam in ("nass", "sadek"):
        x, y, sc = med_tf(cam, st)
        vis = 0 if S.get("solo") not in (None, cam) else 1
        js.append(f'tl.to("#wrap-{cam}", {{ x: {x}, y: {y}, scale: {sc}, duration: {MOVE_DUR}, ease: "{E}" }}, {t0});')
        js.append(f'tl.to("#stage-{cam}", {{ opacity: {vis}, duration: {MOVE_DUR * 0.7:.2f}, ease: "power2.inOut" }}, {t0 if vis == 0 else round(t0 + MOVE_DUR * 0.3, 3)});')
# la caméra qui se range passe derrière celle qui parle
js.append('tl.fromTo("#stage-nass", { zIndex: 2 }, { zIndex: 2, duration: 0.01 }, 0);')
js.append(f'tl.set("#stage-nass", {{ zIndex: 0 }}, {round(seams[0] - MOVE_DUR / 2, 3)});')
js.append(f'tl.set("#stage-nass", {{ zIndex: 2 }}, {round(t_back - MOVE_DUR / 2, 3)});')

# ---------- illustrations de la bande (états solo) ---------- PROPRE AU CLIP
t_ill_candles_out = round(seams[1] - 0.12, 3)
t_train_out = round(t_back - 0.35, 3)
t_trend_out = round(find("s5", "trading") - 0.2, 3)
js += [
    # 1. « quand on casse un niveau … sur des bougies » : un niveau or, trois bougies dessous, la quatrième le casse
    f'tl.fromTo("#ill-candles", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.15 }}, {round(t_casse - 0.05, 3)});',
    f'tl.fromTo("#lvl", {{ strokeDashoffset: 900 }}, {{ strokeDashoffset: 0, duration: 0.45, ease: "power2.out" }}, {round(t_casse - 0.05, 3)});',
]
for i in range(3):
    js.append(f'tl.fromTo("#cd{i}", {{ scaleY: 0, transformOrigin: "50% 100%" }}, {{ scaleY: 1, duration: 0.28, ease: "power3.out" }}, {round(t_casse + 0.45 + i * 0.12, 3)});')
js += [
    f'tl.fromTo("#cd3", {{ scaleY: 0, transformOrigin: "50% 100%" }}, {{ scaleY: 1, duration: 0.4, ease: "expo.out" }}, {round(t_bougies - 0.02, 3)});',
    f'tl.to("#ill-candles", {{ opacity: 0, duration: 0.25, ease: "power2.in" }}, {t_ill_candles_out});',
    # 2. « arrêter le TGV en pleine route » : le train entre à toute vitesse et pile ; secousse sur « route »
    f'tl.fromTo("#ill-train", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.08 }}, {round(t_tgv - 0.1, 3)});',
    f'tl.fromTo("#rail", {{ strokeDashoffset: 900 }}, {{ strokeDashoffset: 0, duration: 0.35, ease: "power2.out" }}, {round(t_tgv - 0.1, 3)});',
    f'tl.fromTo("#train", {{ x: -1000 }}, {{ x: 0, duration: 0.7, ease: "power4.out" }}, {round(t_tgv - 0.05, 3)});',
    f'tl.fromTo("#speed", {{ opacity: 1, x: -300 }}, {{ opacity: 0, x: 0, duration: 0.6, ease: "power2.out" }}, {round(t_tgv + 0.05, 3)});',
    f'tl.to("#train", {{ x: 16, rotation: -1.2, transformOrigin: "50% 100%", duration: 0.1, ease: "power2.out" }}, {round(t_route - 0.02, 3)});',
    f'tl.to("#train", {{ x: 0, rotation: 0, duration: 0.35, ease: "elastic.out(1, 0.4)" }}, {round(t_route + 0.08, 3)});',
    f'tl.fromTo("#stop", {{ opacity: 0, scale: 0.4, transformOrigin: "50% 50%" }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, {round(t_route, 3)});',
    f'tl.to("#ill-train", {{ opacity: 0, duration: 0.25, ease: "power2.in" }}, {t_train_out});',
    # 3. « la tendance est votre ami, the trend is your friend » : la tendance verte se dessine ; « contre tendance » : la flèche rouge à rebours
    f'tl.fromTo("#ill-trend", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.12 }}, {round(t_tendance - 0.1, 3)});',
    f'tl.fromTo("#trend", {{ strokeDashoffset: 1200 }}, {{ strokeDashoffset: 0, duration: 1.1, ease: "power2.inOut" }}, {round(t_tendance - 0.05, 3)});',
    f'tl.fromTo("#head", {{ opacity: 0, scale: 0.3, transformOrigin: "50% 50%" }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }}, {round(t_tendance + 0.95, 3)});',
    f'tl.to("#head", {{ scale: 1.35, duration: 0.12, ease: "power2.out", yoyo: true, repeat: 1 }}, {round(t_friend, 3)});',
    f'tl.fromTo("#counter", {{ opacity: 0, strokeDashoffset: 300 }}, {{ opacity: 1, strokeDashoffset: 0, duration: 0.4, ease: "power3.out" }}, {round(t_contre - 0.02, 3)});',
    f'tl.fromTo("#counter-head", {{ opacity: 0, scale: 0.3, transformOrigin: "50% 50%" }}, {{ opacity: 1, scale: 1, duration: 0.2, ease: "back.out(2)" }}, {round(t_contre + 0.3, 3)});',
    f'tl.to("#ill-trend", {{ opacity: 0, duration: 0.25, ease: "power2.in" }}, {t_trend_out});',
    f'tl.to("#ill", {{ opacity: 0, duration: 0.3, ease: "power2.in" }}, {END_T});',
]

js += [
    # accroche
    'tl.fromTo("#hook", { opacity: 1 }, { opacity: 1, duration: 0.01 }, 0);',
    f'tl.to("#hook", {{ opacity: 0, filter: "blur(8px)", duration: 0.2, ease: "power2.in" }}, {round(t_first - 0.32, 3)});',
]
js += [f'tl.fromTo("#kw-pat", {{ opacity: 0, scale: 1.3 }}, {{ opacity: 1, scale: 1, duration: 0.5, ease: "expo.out" }}, {round(PAT_T - 0.06, 3)});',
       f'tl.to("#kw-pat", {{ opacity: 0, duration: 0.25, ease: "power2.in" }}, {round(END_T + 0.05, 3)});']

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
    #hook {{ position: absolute; left: 0; right: 0; top: {STATES['H']['hook']}px; text-align: center; color: {INK}; }}
    #hook .h1 {{ font: 800 104px/0.95 'Inter Tight'; letter-spacing: -0.02em; }}
    #hook .h1 b {{ color: {GOLD_TXT}; font-weight: 800; }}
    #screen {{ position: absolute; left: {STATES['E']['sx']}px; top: {STATES['E']['sy']}px; width: {STATES['E']['sw']}px; height: {STATES['E']['sh']}px; overflow: hidden; }}
    #screen-body {{ position: absolute; inset: 0; }}
    #screen video {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
    .kw {{ position: absolute; font: 800 104px/1 'Inter Tight'; letter-spacing: -0.03em; white-space: nowrap; }}
    #kw-pat {{ left: 0; right: 0; top: 1372px; text-align: center; color: {INK}; font-size: 104px; line-height: 0.98; white-space: normal; }}
    #kw-pat span {{ box-shadow: inset 0 -14px 0 {GREEN}; }}
    #ill {{ position: absolute; left: {ILL["left"]}px; top: {ILL["top"]}px; width: {ILL["w"]}px; height: {ILL["h"]}px; }}
    .ill {{ position: absolute; inset: 0; opacity: 0; }}
    .ill svg {{ position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible; }}
    .ink {{ fill: none; stroke: {INK}; stroke-width: 10; stroke-linecap: round; stroke-linejoin: round; }}
    #logo {{ position: absolute; left: {LX0}px; top: {LY0}px; width: {LOGO_W}px; height: {1669 * ls:.1f}px; }}
    #cta {{ position: absolute; left: 0; right: 0; top: 1068px; text-align: center; font: 700 46px 'Inter Tight'; color: {INK}; }}
  </style>
  <div id="root" data-composition-id="stage" data-width="1080" data-height="1920">
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
      <div class="h1">ARRÊTER <b>LE TGV</b><br>EN PLEINE ROUTE</div>
    </div>

    <div id="kw-pat" class="kw" style="opacity:0"><span>LA PIRE CHOSE</span><br><span>À FAIRE</span></div>

    <div id="ill">
      <div id="ill-candles" class="ill">
        <svg viewBox="0 0 900 300">
          <line id="lvl" x1="0" y1="96" x2="900" y2="96" stroke="{GOLD}" stroke-width="10" stroke-dasharray="900" stroke-dashoffset="900" stroke-linecap="round"/>
          <g id="cd0"><line class="ink" x1="200" y1="130" x2="200" y2="282"/><rect x="172" y="170" width="56" height="78" fill="{PAPER}" stroke="{INK}" stroke-width="10"/></g>
          <g id="cd1"><line class="ink" x1="350" y1="150" x2="350" y2="292"/><rect x="322" y="196" width="56" height="60" fill="{INK}"/></g>
          <g id="cd2"><line class="ink" x1="500" y1="120" x2="500" y2="280"/><rect x="472" y="150" width="56" height="94" fill="{PAPER}" stroke="{INK}" stroke-width="10"/></g>
          <g id="cd3"><line class="ink" x1="660" y1="10" x2="660" y2="272"/><rect x="624" y="30" width="72" height="200" fill="{GREEN}" stroke="{INK}" stroke-width="10"/></g>
        </svg>
      </div>
      <div id="ill-train" class="ill">
        <svg viewBox="0 0 900 300">
          <line id="rail" x1="0" y1="262" x2="900" y2="262" stroke="{INK}" stroke-width="10" stroke-dasharray="900" stroke-dashoffset="900" stroke-linecap="round"/>
          <g id="speed" opacity="0">
            <line class="ink" x1="20" y1="110" x2="150" y2="110" stroke="{GREY}"/><line class="ink" x1="50" y1="150" x2="170" y2="150" stroke="{GREY}"/><line class="ink" x1="20" y1="190" x2="130" y2="190" stroke="{GREY}"/>
          </g>
          <g id="train">
            <path class="ink" d="M 150 90 L 700 90 Q 830 90 870 208 L 150 208 Z" fill="{PAPER}"/>
            <path d="M 150 170 L 806 170 L 822 194 L 150 194 Z" fill="{GOLD}"/>
            <rect x="200" y="112" width="70" height="44" rx="6" fill="{INK}"/><rect x="300" y="112" width="70" height="44" rx="6" fill="{INK}"/>
            <rect x="400" y="112" width="70" height="44" rx="6" fill="{INK}"/><rect x="500" y="112" width="70" height="44" rx="6" fill="{INK}"/>
            <path d="M 620 112 L 712 112 Q 770 116 800 156 L 620 156 Z" rx="6" fill="{INK}"/>
            <circle cx="230" cy="236" r="22" fill="{PAPER}" stroke="{INK}" stroke-width="10"/><circle cx="310" cy="236" r="22" fill="{PAPER}" stroke="{INK}" stroke-width="10"/>
            <circle cx="690" cy="236" r="22" fill="{PAPER}" stroke="{INK}" stroke-width="10"/><circle cx="770" cy="236" r="22" fill="{PAPER}" stroke="{INK}" stroke-width="10"/>
          </g>
          <g id="stop" opacity="0">
            <circle cx="860" cy="60" r="44" fill="{RED}"/>
            <rect x="834" y="52" width="52" height="16" rx="4" fill="{PAPER}"/>
          </g>
        </svg>
      </div>
      <div id="ill-trend" class="ill">
        <svg viewBox="0 0 900 300">
          <polyline id="trend" points="40,270 210,160 330,215 520,96 640,150 820,36" fill="none" stroke="{GREEN}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="1200" stroke-dashoffset="1200"/>
          <path id="head" d="M 842 22 L 772 24 L 836 92 Z" fill="{GREEN}" opacity="0"/>
          <line id="counter" x1="760" y1="60" x2="560" y2="236" stroke="{RED}" stroke-width="12" stroke-linecap="round" stroke-dasharray="300" stroke-dashoffset="300" opacity="0"/>
          <path id="counter-head" d="M 548 246 L 600 236 L 560 194 Z" fill="{RED}" opacity="0"/>
        </svg>
      </div>
    </div>

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
cap_js.append(f'tl.fromTo("#capwrap", {{ y: {STATES["H"]["cap"]}, scale: 1, transformOrigin: "50% 0%" }}, {{ y: {STATES["H"]["cap"]}, scale: 1, duration: 0.01 }}, 0);')
for tm, st in MOVES:
    cap_js.append(f'tl.to("#capwrap", {{ y: {STATES[st]["cap"]}, scale: {STATES[st].get("capscale", 1)}, duration: {MOVE_DUR}, ease: "{E}" }}, {round(tm - MOVE_DUR / 2, 3)});')
cap_js.append('window.__timelines["captions"] = tl;')
captions = f"""<template>
  <style>
    @font-face {{ font-family: 'Inter Tight'; src: url('assets/fonts/InterTight-var.ttf') format('truetype'); font-weight: 100 900; }}
    #root {{ position: absolute; inset: 0; }}
    #capwrap {{ position: absolute; left: 0; right: 0; top: 0; height: 0; overflow: visible; }}
    .grp {{ position: absolute; left: 130px; right: 130px; top: -36px; text-align: center; font: 800 66px/1.08 'Inter Tight';
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
    <!-- Short 36 « Arrêter le TGV en pleine route » — Convergence EP.01, DA « Les deux droites », variante écran + médaillons. Voix réelles, pas de musique. -->
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
print(f"durée {D} s | groupes {len(groups)} | TGV {t_tgv} | retour 2 cams {t_back} | Nass seul {t_solo_n} | chute {PAT_T} | coutures {seams}")
