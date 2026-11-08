"""Bibliothèque commune des `make_comp.py` des clips Convergence, variante « écran + médaillons » (v6, 2026-11-08).

Tout ce qui est commun aux clips vit ici : états de mise en page à écarts égaux (sym / sym_screen / solo / solo_screen),
bascules de 0,6 s aux coutures, médaillons, écran réel, sous-titres de ≤ 3 mots qui suivent la bande, fin V → logo → CTA,
normalisation des SFX. Le `make_comp.py` d'un clip ne garde que ce qui lui est propre : coupes de mise en page (MOVES),
accroche, mots clés, illustrations à l'encre dans la bande, SFX, corrections de sous-titres.

Usage dans un clip :
    sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
    from comp_lib import Comp, GREEN, GOLD, ...
    c = Comp(HERE, 21, "« Montrez-moi des preuves »")
    c.moves = [(c.seams[0], "SOLO_E"), ...]
    ...
    c.build()
"""
import json
import re
import shutil
import subprocess
from pathlib import Path

FF = shutil.which("ffmpeg") or exit("ffmpeg introuvable dans le PATH")

INK, PAPER, GRID = "#0B0E11", "#F2EFE8", "#E6E1D6"
GOLD, GREEN, RED, GREY = "#C98A0B", "#0F8A5F", "#C8323F", "#565D6B"
GOLD_TXT = "#A07006"   # or foncé pour le TEXTE sur papier (contraste >= 3:1)
FH = 1920
MOVE_DUR = 0.6
E = "power3.inOut"
ILL = dict(left=90, top=1180, w=900, h=300)   # zone des illustrations dans la bande des états solo sans écran

# SFX : nom -> (fichier source, durée gardée, filtre ffmpeg préalable)
SFX_KINDS = {
    "whoosh-short": ("whoosh-short", 0.55, ""),
    "whoosh": ("whoosh-short", 0.62, "asetrate=48000*0.86,aresample=48000,"),   # whoosh grave
    "pop": ("pop", 0.40, ""),
    "impact-bass-1": ("impact-bass-1", 1.00, ""),
}


# ---------- états ---------- mise en page symétrique (Nass, 2026-11-07) : le même écart e au-dessus de la caméra du haut,
# entre cette caméra et la droite verte, entre les deux droites (bande des sous-titres), entre la droite or et la caméra du
# bas, et sous la caméra du bas. Droites horizontales. 5e + d_haut + d_bas = 1920.
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
    """Monologue (Nass, 2026-11-07) : une seule caméra, grande, en haut ; la bande entre les droites porte les illustrations
    (zone ILL) et les sous-titres plus gros en dessous. L'autre caméra se range derrière, invisible."""
    g, o = e + d + e, FH - e
    other = "sadek" if cam == "nass" else "nass"
    return {cam: (540, round(e + d / 2), d), other: (540, round(e + d / 2), 400), "g": (g, g), "o": (o, o),
            "cap": g + 440, "e": e, "solo": cam, "capscale": 1.25}


def solo_screen(d, sw, sh, cap_h=110, cam="nass"):
    """Monologue avec l'écran : caméra seule en haut, écran puis sous-titres dans la bande, mêmes écarts e."""
    band = 14 + sh + 16 + cap_h + 14
    e = (FH - d - band) / 3
    g = e + d + e
    o = g + band
    other = "sadek" if cam == "nass" else "nass"
    return {"g": (round(g), round(g)), "o": (round(o), round(o)), cam: (540, round(e + d / 2), d), other: (540, round(e + d / 2), 400),
            "cap": round(g + 14 + sh + 16 + cap_h / 2), "e": round(e), "solo": cam, "capscale": 1.25,
            "screen": True, "sx": round((1080 - sw) / 2), "sy": round(g + 14), "sw": sw, "sh": sh}


def screen_only(sw, sh, kw_h=300, cap_h=110, hook=180):
    """Écran seul (scène où l'invité partage son écran en plein cadre, aucune caméra exploitable) : zone des mots clés en
    haut (kw_h), puis la bande entre les droites avec l'écran et les sous-titres, mêmes écarts e. Les caméras sont
    cachées ("solo": "none") ; les coutures se marquent par un léger punch sur l'écran (Comp.punch)."""
    band = 14 + sh + 16 + cap_h * 1.25 + 14
    e = (FH - kw_h - band) / 3
    g = e + kw_h + e
    o = g + band
    return {"g": (round(g), round(g)), "o": (round(o), round(o)), "nass": (540, 300, 400), "sadek": (540, 300, 400),
            "cap": round(g + 14 + sh + 16 + cap_h * 1.25 / 2), "e": round(e), "solo": "none", "capscale": 1.25,
            "screen": True, "sx": round((1080 - sw) / 2), "sy": round(g + 14), "sw": sw, "sh": sh,
            "kw_top": round(e), "kw_h": kw_h, "hook": round(e + (kw_h - hook) / 2)}


def base_states():
    return {
        "H": sym("nass", 620, 620, band_mult=3, hook=200),   # accroche : les deux à 620, bande de 3e pour deux lignes de titre
        "E": sym_screen(480, 520, 900, 491),                   # Nass explique à l'écran, Sadek présent
        "E+": sym_screen(500, 520, 900, 491),
        "N": sym("nass", 740, 660),                            # Nass parle
        "N+": sym("nass", 760, 660),
        "S": sym("nass", 660, 740),                            # Sadek parle (Nass reste en haut, plus petit)
        "S+": sym("nass", 660, 760),
        "SOLO_E": solo_screen(860, 900, 491),                  # Nass seul avec son écran
        "SOLO_N": solo("nass", 900),                           # Nass seul
        "SOLO_N+": solo("nass", 940),
        "SOLO_S": solo("sadek", 900),                          # Sadek seul
        "SOLO_S+": solo("sadek", 940),
    }


class Comp:
    def __init__(self, here, n_short, title, cta="Épisode 1 complet sur la chaîne"):
        self.HERE = Path(here)
        self.n_short, self.title, self.cta = n_short, title, cta
        self.TL = TL = json.loads((self.HERE / "timeline.json").read_text(encoding="utf-8"))
        self.CUT = CUT = json.loads((self.HERE / "cut.json").read_text(encoding="utf-8"))
        self.SEG = {s["id"]: s for s in TL["segments"]}
        self.ORDER = [s["id"] for s in TL["segments"]]
        self.K = TL["prescale"]
        self.VOICE_END = TL["duration_voice"]
        self.END_T = self.VOICE_END
        self.D = round(self.END_T + 4.15, 2)   # le CTA reste >= 2 s ; pas de disclaimer à l'image (il va dans la légende)
        self.CROP = {cam: (c[2], c[3]) for cam, c in CUT["crops"].items()}
        self.VW = {cam: round(self.CROP[cam][0] * self.K / 2) * 2 for cam in self.CROP}   # côté du médaillon vidéo avant échelle CSS
        self.STATES = base_states()
        self.seams = [self.SEG[k]["out_start"] for k in self.ORDER[1:]]
        # ---- réglages propres au clip (valeurs par défaut) ----
        self.moves = []                 # [(t, état)]
        self.hook_html = ""             # contenu de #hook, leurs mots, pas de chiffre
        self.hook_font = 104
        self.hook_css = ""              # CSS supplémentaire
        self.hook_fade = None           # défaut : seams[0] − 0,32
        self.screen_state = "SOLO_E"    # état qui donne la boîte de l'écran réel
        self.screen_windows = []        # [(t_ouverture, t_fermeture)]
        self.kws = []                   # mots clés : dict(id, html, css, t_in, t_out, anim)
        self.ill_html, self.ill_css, self.ill_js = "", "", []
        self.extra_js = []              # JS libre ajouté à la timeline de la scène
        self.sfx = []                   # [(id, kind, t, volume)]
        self.fix = {}                   # (seg, mot) -> texte affiché ("" = retiré)
        self.skip_before = None         # pas de sous-titre avant (défaut : seams[0], l'accroche en tient lieu)
        self.cap_cuts = []              # [(seg, t_from, t_to)] mots retirés des sous-titres (portés par un mot clé)
        self.cap_end_before = []        # [t] : le groupe affiché s'efface à t − 0,08 (un mot clé le remplace)
        self.z_front = [(0, "nass")]    # [(t, cam)] : quelle caméra passe devant (quand les médaillons se croisent)
        self.cap_font = 66

    # ---------- outils ----------
    def find(self, seg, text, nth=0):
        hits = [w for w in self.SEG[seg]["words"] if w["w"].strip().lower().lstrip("'").startswith(text.lower())]
        return hits[nth]["s"]

    def find_end(self, seg, text, nth=0):
        hits = [w for w in self.SEG[seg]["words"] if w["w"].strip().lower().lstrip("'").startswith(text.lower())]
        return hits[nth]["e"]

    def med_tf(self, cam, st):
        cx, cy, d = self.STATES[st][cam]
        s = d / self.VW[cam]
        return round(cx - d / 2, 1), round(cy - d / 2, 1), round(s, 4)

    def kw(self, id_, html, css, t_in, t_out, anim="pop", attrs=""):
        """attrs : attributs HTML en plus (ex. 'data-layout-allow-overlap' quand deux mots clés partagent une zone sans être visibles ensemble)."""
        self.kws.append(dict(id=id_, html=html, css=css, t_in=t_in, t_out=t_out, anim=anim, attrs=attrs))

    def punch(self, times, amount=1.05):
        """Écran seul : à chaque instant donné, l'écran alterne entre 1 et `amount` d'échelle en 0,6 s (la couture se voit
        sans caméra à basculer)."""
        self.extra_js.append('tl.fromTo("#screen-body", { scale: 1, transformOrigin: "50% 50%" }, { scale: 1, duration: 0.01 }, 0);')
        for i, t in enumerate(times):
            sc = amount if i % 2 == 0 else 1
            self.extra_js.append(f'tl.to("#screen-body", {{ scale: {sc}, duration: {MOVE_DUR}, ease: "{E}" }}, {round(t - MOVE_DUR / 2, 3)});')

    # ---------- SFX ----------
    def _sfx_files(self):
        out = []
        for id_, kind, t, vol in self.sfx:
            base, keep, var = SFX_KINDS[kind]
            src, dst = self.HERE / f"assets/sfx/{base}.mp3", self.HERE / f"assets/sfx/{kind}-n.wav"
            if not dst.exists():
                vd = subprocess.run([FF, "-hide_banner", "-i", str(src), "-af", f"{var}atrim=0:{keep},volumedetect", "-f", "null", "-"],
                                    capture_output=True, text=True).stderr
                peak = float(vd.split("max_volume:")[1].split("dB")[0])
                subprocess.run([FF, "-v", "error", "-y", "-i", str(src), "-af",
                                f"{var}atrim=0:{keep},volume={-1 - peak:.2f}dB,afade=t=out:st={keep - 0.08:.2f}:d=0.08", "-ar", "48000",
                                str(dst)], check=True)
            out.append((id_, dst.name, round(t, 3), vol))
        return out

    # ---------- sous-titres ----------
    def _caption_words(self, seg):
        out = []
        for w in self.SEG[seg]["words"]:
            t = self.fix.get((seg, w["w"].strip()), w["w"].strip())
            if not t:
                continue
            if any(seg == cs and a - 0.01 <= w["s"] < b for cs, a, b in self.cap_cuts):
                continue
            if out and (t.startswith("'") or t.startswith("-") or t == "%"):
                out[-1]["t"] += (" %" if t == "%" else t)
                out[-1]["e"] = w["e"]
                continue
            out.append({"t": t, "s": w["s"], "e": w["e"]})
        return out

    def _groups(self):
        skip = self.seams[0] if self.skip_before is None else self.skip_before
        groups = []
        for seg in self.ORDER:
            cur = []
            for w in self._caption_words(seg):
                if w["s"] < skip:
                    continue
                if cur and (len(cur) >= 3 or len(" ".join(x["t"] for x in cur + [w])) > 17 or w["s"] - cur[-1]["e"] > 0.15):
                    groups.append((seg, cur))
                    cur = []
                cur.append(w)
            if cur:
                groups.append((seg, cur))
        return groups

    # ---------- construction ----------
    def build(self):
        HERE, STATES, SEG, TL = self.HERE, self.STATES, self.SEG, self.TL
        END_T, VOICE_END, D = self.END_T, self.VOICE_END, self.D
        seams = self.seams
        hook_fade = round(seams[0] - 0.32, 3) if self.hook_fade is None else round(self.hook_fade, 3)
        sfx = self._sfx_files()

        js = ["const tl = gsap.timeline({ paused: true });"]
        H0 = STATES["H"]
        for cam in ("nass", "sadek"):
            x, y, sc = self.med_tf(cam, "H")
            js.append(f'tl.fromTo("#wrap-{cam}", {{ x: {x}, y: {y}, scale: {sc} }}, {{ x: {x}, y: {y}, scale: {sc}, duration: 0.01 }}, 0);')
            v0 = 1 if H0.get("solo") in (None, cam) else 0
            js.append(f'tl.fromTo("#stage-{cam}", {{ opacity: {v0} }}, {{ opacity: {v0}, duration: 0.01 }}, 0);')
        for t, cam in self.z_front:
            other = "sadek" if cam == "nass" else "nass"
            if t == 0:
                js.append(f'tl.fromTo("#stage-{cam}", {{ zIndex: 2 }}, {{ zIndex: 2, duration: 0.01 }}, 0);')
                js.append(f'tl.fromTo("#stage-{other}", {{ zIndex: 0 }}, {{ zIndex: 0, duration: 0.01 }}, 0);')
            else:
                js.append(f'tl.set("#stage-{cam}", {{ zIndex: 2 }}, {round(t, 3)});')
                js.append(f'tl.set("#stage-{other}", {{ zIndex: 0 }}, {round(t, 3)});')
        for tm, st in self.moves:
            S, t0 = STATES[st], round(tm - MOVE_DUR / 2, 3)
            js += [
                f'tl.to("#line-g", {{ attr: {{ y1: {S["g"][0]}, y2: {S["g"][1]} }}, duration: {MOVE_DUR}, ease: "{E}" }}, {t0});',
                f'tl.to("#line-o", {{ attr: {{ y1: {S["o"][0]}, y2: {S["o"][1]} }}, duration: {MOVE_DUR}, ease: "{E}" }}, {t0});',
            ]
            for cam in ("nass", "sadek"):
                x, y, sc = self.med_tf(cam, st)
                vis = 0 if S.get("solo") not in (None, cam) else 1
                js.append(f'tl.to("#wrap-{cam}", {{ x: {x}, y: {y}, scale: {sc}, duration: {MOVE_DUR}, ease: "{E}" }}, {t0});')
                js.append(f'tl.to("#stage-{cam}", {{ opacity: {vis}, duration: {MOVE_DUR * 0.7:.2f}, ease: "power2.inOut" }}, '
                          f'{t0 if vis == 0 else round(t0 + MOVE_DUR * 0.3, 3)});')

        js += list(self.ill_js)
        js += [
            'tl.fromTo("#hook", { opacity: 1 }, { opacity: 1, duration: 0.01 }, 0);',
            f'tl.to("#hook", {{ opacity: 0, filter: "blur(8px)", duration: 0.2, ease: "power2.in" }}, {hook_fade});',
        ]
        if self.screen_windows:   # opacité sur un enfant, jamais sur un .clip ; une base à 0 puis des .to (seek-safe)
            js.append('tl.fromTo("#screen-body", { opacity: 0 }, { opacity: 0, duration: 0.01 }, 0);')
        for a, b in self.screen_windows:
            js.append(f'tl.to("#screen-body", {{ opacity: 1, duration: 0.25, ease: "power2.out" }}, {round(max(a - 0.05, 0.01), 3)});')
            js.append(f'tl.to("#screen-body", {{ opacity: 0, duration: 0.3, ease: "power2.in" }}, {round(b, 3)});')
        for k in self.kws:
            if k["anim"] == "pop":
                js.append(f'tl.fromTo("#{k["id"]}", {{ opacity: 0, scale: 1.3 }}, {{ opacity: 1, scale: 1, duration: 0.5, ease: "expo.out" }}, {round(k["t_in"] - 0.06, 3)});')
            elif k["anim"] == "rise":
                js.append(f'tl.fromTo("#{k["id"]}", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }}, {round(k["t_in"] - 0.06, 3)});')
            else:
                js.append(f'tl.fromTo("#{k["id"]}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, ease: "power2.out" }}, {round(k["t_in"] - 0.06, 3)});')
            if k["t_out"] is not None:
                js.append(f'tl.to("#{k["id"]}", {{ opacity: 0, duration: 0.25, ease: "power2.in" }}, {round(k["t_out"], 3)});')
        js += list(self.extra_js)

        # fin : les deux droites -> grand V -> le V du vrai logo
        LOGO = HERE / "assets/convergence-logo-clair.svg"
        LOGO_W, LX0, LY0 = 900, 90, 930
        ls = LOGO_W / 21736
        VG = [(90 + (6488.0 + 89) * ls, LY0 + (122.9 + 89) * ls), (90 + (7110.1 + 89) * ls, LY0 + (1367.1 + 89) * ls)]
        VV = [(90 + (7732.2 + 89) * ls, LY0 + (122.9 + 89) * ls), VG[1]]
        SW = round(245.9 * ls, 2)
        VX, VTOP, VBOT, VHALF = 540, 520, 820, 150
        js += [
            f'tl.to(["#stage-nass", "#stage-sadek", "#ill"], {{ opacity: 0, duration: 0.45, ease: "power2.in" }}, {END_T});',
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
            f'data-track-index="{1 if cam == "nass" else 2}"></video>' for s in TL["segments"]) for cam in self.CROP}
        screen_vids = "\n          ".join(
            f'<video id="screen-{s["id"]}" class="clip" src="assets/video/screen_{s["id"]}.mp4" muted playsinline '
            f'data-start="{s["out_start"]}" data-duration="{s["dur"]}" data-media-start="{TL["handle"]}" data-track-index="9"></video>'
            for s in TL["segments"] if (HERE / f'assets/video/screen_{s["id"]}.mp4').exists())
        logo_path = re.search(r"<path[^>]*/>", LOGO.read_text(encoding="utf-8")).group(0)
        SS = STATES[self.screen_state] if self.screen_state in STATES and STATES[self.screen_state].get("screen") else dict(sx=90, sy=1151, sw=900, sh=491)
        kw_css = "\n    ".join(f'#{k["id"]} {{ {k["css"]} }}' for k in self.kws)
        kw_html = "\n    ".join(f'<div id="{k["id"]}" class="kw" style="opacity:0" {k.get("attrs", "")}>{k["html"]}</div>' for k in self.kws)
        stage = f"""<template>
  <style>
    @font-face {{ font-family: 'Inter Tight'; src: url('assets/fonts/InterTight-var.ttf') format('truetype'); font-weight: 100 900; }}
    @font-face {{ font-family: 'Plex Mono C'; src: url('assets/fonts/IBMPlexMono-SemiBold.ttf') format('truetype'); font-weight: 600; }}
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
    .panel {{ position: absolute; inset: 0; overflow: hidden; }}
    .wrap {{ position: absolute; left: 0; top: 0; border-radius: 50%; overflow: hidden; transform-origin: 0 0; }}
    #wrap-nass {{ width: {self.VW["nass"]}px; height: {self.VW["nass"]}px; }}
    #wrap-sadek {{ width: {self.VW["sadek"]}px; height: {self.VW["sadek"]}px; }}
    .cam {{ position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: cover; }}
    .ring {{ position: absolute; inset: 0; border-radius: 50%; }}
    #ring-nass {{ box-shadow: inset 0 0 0 14px {GREEN}; }}
    #ring-sadek {{ box-shadow: inset 0 0 0 14px {GOLD}; }}
    #lines {{ position: absolute; inset: 0; width: 1080px; height: 1920px; overflow: visible; }}
    #lines line {{ stroke-width: 12; stroke-linecap: round; }}
    #hook {{ position: absolute; left: 0; right: 0; top: {STATES['H']['hook']}px; text-align: center; color: {INK}; }}
    #hook .h1 {{ font: 800 {self.hook_font}px/0.95 'Inter Tight'; letter-spacing: -0.02em; }}
    #hook .h1 b {{ color: {GREEN}; font-weight: 800; }}
    #hook .h1 b.or {{ color: {GOLD_TXT}; }}
    {self.hook_css}
    #screen {{ position: absolute; left: {SS['sx']}px; top: {SS['sy']}px; width: {SS['sw']}px; height: {SS['sh']}px; overflow: hidden; }}
    #screen-body {{ position: absolute; inset: 0; }}
    #screen video {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
    .kw {{ position: absolute; font: 800 104px/1 'Inter Tight'; letter-spacing: -0.03em; white-space: nowrap; }}
    {kw_css}
    #ill {{ position: absolute; left: {ILL["left"]}px; top: {ILL["top"]}px; width: {ILL["w"]}px; height: {ILL["h"]}px; }}
    .ill {{ position: absolute; inset: 0; opacity: 0; }}
    .ill svg {{ position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible; }}
    .ink {{ fill: none; stroke: {INK}; stroke-width: 10; stroke-linecap: round; stroke-linejoin: round; }}
    {self.ill_css}
    #logo {{ position: absolute; left: {LX0}px; top: {LY0}px; width: {LOGO_W}px; height: {1669 * ls:.1f}px; }}
    #cta {{ position: absolute; left: 0; right: 0; top: 1068px; text-align: center; font: 700 46px 'Inter Tight'; color: {INK}; }}
  </style>
  <div id="root" data-composition-id="stage" data-width="1080" data-height="1920">
    <div id="screen">
      <div id="screen-body" style="opacity:0" data-layout-allow-overflow>
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
      <div class="h1">{self.hook_html}</div>
    </div>

    {kw_html}

    <div id="ill">
      {self.ill_html}
    </div>

    <svg id="logo" viewBox="-89 -89 21736 1669" style="opacity:0">{logo_path}</svg>
    <svg id="lines" viewBox="0 0 1080 1920">
      <line id="line-g" x1="-30" y1="{H0["g"][0]}" x2="1110" y2="{H0["g"][1]}" stroke="{GREEN}"/>
      <line id="line-o" x1="-30" y1="{H0["o"][0]}" x2="1110" y2="{H0["o"][1]}" stroke="{GOLD}"/>
      <circle id="v-dot" cx="{VX}" cy="{VBOT}" r="34" fill="{INK}" opacity="0" style="transform-origin: {VX}px {VBOT}px"/>
    </svg>

    <div id="cta" style="opacity:0">{self.cta}</div>
  </div>
  <script>
    {(chr(10) + '    ').join(js)}
  </script>
</template>
"""
        (HERE / "compositions").mkdir(exist_ok=True)
        (HERE / "compositions/stage.html").write_text(stage, encoding="utf-8")

        # ---------- HTML : sous-titres ----------
        groups = self._groups()
        cap_html, cap_js = [], ["const tl = gsap.timeline({ paused: true });"]
        for gi, (seg, ws) in enumerate(groups):
            color = GREEN if SEG[seg]["speaker"] == "nass" else GOLD
            start = round(max(ws[0]["s"] - 0.05, 0), 3)
            nxt = groups[gi + 1][1][0]["s"] - 0.05 if gi + 1 < len(groups) else None
            end = round(min(ws[-1]["e"] + 0.18, nxt if nxt else 1e9, VOICE_END), 3)
            for t in self.cap_end_before:
                if start < t - 0.08 < end:
                    end = round(t - 0.08, 3)
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
        for tm, st in self.moves:
            cap_js.append(f'tl.to("#capwrap", {{ y: {STATES[st]["cap"]}, scale: {STATES[st].get("capscale", 1)}, duration: {MOVE_DUR}, ease: "{E}" }}, {round(tm - MOVE_DUR / 2, 3)});')
        cap_js.append('window.__timelines["captions"] = tl;')
        captions = f"""<template>
  <style>
    @font-face {{ font-family: 'Inter Tight'; src: url('assets/fonts/InterTight-var.ttf') format('truetype'); font-weight: 100 900; }}
    #root {{ position: absolute; inset: 0; }}
    #capwrap {{ position: absolute; left: 0; right: 0; top: 0; height: 0; overflow: visible; }}
    .grp {{ position: absolute; left: 130px; right: 130px; top: -36px; text-align: center; font: 800 {self.cap_font}px/1.08 'Inter Tight';
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
            for k, (i, f, t, v) in enumerate(sfx))
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
    <!-- Short {self.n_short} {self.title} — Convergence, DA « Les deux droites », variante écran + médaillons. Voix réelles, pas de musique. -->
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
        print(f"durée {D} s | groupes {len(groups)} | coutures {seams} | états {[s for _, s in self.moves]}")
        return D
