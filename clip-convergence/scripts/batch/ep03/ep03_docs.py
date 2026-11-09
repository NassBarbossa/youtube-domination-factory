"""Écrit SPEC.md, REVIEW.md, la ligne EPISODE.md et le statut BATCH.md d'un clip EP.03.
Usage : ep03_docs.py <slug> --dur D --lufs L --peak P --mb M --frames "..." [--look "..."] [--motion "..."] [--data "..."] [--weak "..."] [--check "..."] [--choices "..."]"""
import argparse, json, re
from pathlib import Path
ROOT = Path.home() / "youtube-domination-factory/clip-convergence"
ap = argparse.ArgumentParser()
ap.add_argument("slug"); ap.add_argument("--dur", type=float, required=True); ap.add_argument("--lufs", required=True); ap.add_argument("--peak", required=True)
ap.add_argument("--mb", required=True); ap.add_argument("--frames", required=True); ap.add_argument("--look", default=""); ap.add_argument("--motion", default="")
ap.add_argument("--data", default="aucun chiffre affiché qui ne soit pas celui de Nass."); ap.add_argument("--weak", default=""); ap.add_argument("--check", default="0 erreur, 1 `nested_media_start_basis_ambiguous`.")
ap.add_argument("--choices", default="")
a = ap.parse_args()
d = ROOT / "projects/ep03" / a.slug
cut = json.loads((d / "cut.json").read_text()); mc = (d / "make_comp.py").read_text()
n = int(a.slug[:2]); title = re.search(r"\d\d — (.+?) \(Convergence EP\.03\)", cut["short"]).group(1)
doc = re.search(r'\n\n(.+?)\nUsage', mc, re.S).group(1).strip().replace("\n", "\n         ")
segs = cut["segments"]; voice = sum(s["b"] - s["a"] for s in segs)
def mmss(t): return f"{int(t // 60):02d}:{int(t % 60):02d}"
cutline = " + ".join(f"{mmss(s['a'])}–{mmss(s['b'])}" for s in segs)
sfx = len(re.findall(r'\("sfx-', mc)); screen = "screen" in cut; layout = "punk" if list(cut["crops"]) == ["sadek"] else ("full" if cut["prescale"] < 3 else "rond")
cams = ", ".join(f"{k} {'/'.join(map(str, v))}" for k, v in cut["crops"].items())
screen_kind = "" if not screen else ("son écran TradingView" if cut["screen"]["crop"][1] < 108 else "sa slide")
hook = re.search(r'c\.hook_html = (.+)', mc).group(1)
scene = f"{cut['scene']} (crops {cams}, prescale {str(cut['prescale']).replace('.', ',')}, sharpen)"
(d / "SPEC.md").write_text(f"""# SPEC — Short {n} « {title} » (Convergence EP.03, thème convergence)

GOAL:    {doc}
OUTPUT:  HyperFrames, 1080 × 1920, 60 i/s. {a.dur:.2f} s ({voice:.2f} s de voix + {a.dur - voice:.2f} s de fin).
SOURCE:  YouTube `PJaScgDfiMk` (replay 720p, 30 i/s, seule source sur ce Mac), scène {scene}.
CUT:     {len(segs)} morceau{'x' if len(segs) > 1 else ''}, {cutline}.
LOOK:    accroche {hook} ; DA « Les deux droites » (papier, encre, vert, or ; Inter Tight){' ; ' + screen_kind + ' (crop ' + '/'.join(map(str, cut['screen']['crop'])) + ', 900 × 506) entre les deux' if screen else ''}. {a.look}
MOTION:  {a.motion or ('moves solo Sadek (SOLO_S / SOLO_S+)' if layout == 'punk' else 'moves deux caméras (H / N / S' + (' / E' if screen else '') + ')') + ', mots clés pop/rise dans la bande, fin « v » → logo → CTA « Épisode 3 complet sur la chaîne ».'}
DATA:    {a.data}
SOUND:   voix −14 LUFS ; {sfx} SFX (whoosh, pop, impact).
""", encoding="utf-8")
(d / "REVIEW.md").write_text(f"""# REVIEW — Short {n} « {title} » (Convergence EP.03, v1 du 2026-11-09)

## Choix
- Série « tous les montages » du 2026-11-08, sans validation par clip : à revoir en lot.
- Source : replay YouTube 720p (les bruts OBS sont sur le PC Windows) ; les caméras sont des recadrages de la fenêtre OBS, agrandis.
{a.choices}
## Mesuré
- check : {a.check}
- Rendu : {a.dur:.2f} s, 1080 × 1920, 60 i/s, {a.lufs} LUFS, crête {a.peak} dBTP, {a.mb} Mo.

## Regardé seulement
- Images à {a.frames} s (accroche, mots clés, {'écran, ' if screen else ''}chute, fin).

## Plan le plus faible
- {a.weak or {'rond': 'Les caméras viennent de ronds de 210 px (720p) agrandis 4,4 × : doux, lisibles à taille de téléphone. Seule source disponible.', 'full': 'Les caméras sont des fenêtres de 464 px (720p) agrandies 2 × : correctes, pas la netteté d’un brut.', 'punk': 'La fenêtre de Nass montre son punk : Sadek seul à l’image, caméra de 468 px (720p) agrandie 2 ×.'}[layout]}

## Retours de Nass
- En attente.
""", encoding="utf-8")
ep = ROOT / "projects/ep03/EPISODE.md"; s = ep.read_text(); marker = "**Fin des clips rendus.**"
row = f"| {n} | « {title} » : {doc.splitlines()[0].strip()} | {cutline} | **v1 rendue le 2026-11-09** : projet `{{repo}}/clip-convergence/projects/ep03/{a.slug}/`, export `{{repo}}/clip-convergence/exports/ep03/{a.slug}.mp4` |\n"
if f"| {n} | « {title} »" not in s:
    s = s.replace(marker, row + marker); ep.write_text(s)
b = ROOT / "BATCH.md"; t = b.read_text()
t2 = re.sub(rf"(\| {n} \| [^|]+\| )(en cours|à faire)( \|)", r"\1fait (2026-11-09)\3", t, count=1)
b.write_text(t2); print("docs ok", title, f"{voice:.2f}s voix", "BATCH changé" if t2 != t else "BATCH inchangé")
