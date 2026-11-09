"""Met à jour SPEC.md, REVIEW.md et la ligne EPISODE.md d'un clip Formation après le re-rendu avec l'outro (v2).
Usage : outro_docs.py <f1|f2|f3> <slug> --dur D --lufs L --peak P --mb M"""
import argparse, json, re
from pathlib import Path
ROOT = Path.home() / "youtube-domination-factory/clip-convergence"
ap = argparse.ArgumentParser(); ap.add_argument("fx"); ap.add_argument("slug")
for k in ("dur", "lufs", "peak", "mb"): ap.add_argument(f"--{k}", required=True)
a = ap.parse_args(); d = ROOT / "projects" / a.fx / a.slug
cut = json.loads((d / "cut.json").read_text()); voice = sum(s["b"] - s["a"] for s in cut["segments"]); dur = float(a.dur)
mc = (d / "make_comp.py").read_text(); nsfx = len(re.findall(r'\("sfx-', mc)) + 6
OUTRO = ("outro « formation offerte » de 3 s : caméras soufflées, FORMATION / OFFERTE qui claquent (flash orange, secousse), "
         "barre orange + cyan, « Retrouvez-la sur » puis badge NASSIN CRYPTO avec reflet")
spec = (d / "SPEC.md").read_text()
spec = re.sub(r"OUTPUT:  HyperFrames, 1080 × 1920, 60 i/s\. [\d.]+ s \([\d.]+ s de voix \+ [\d.]+ s de fin\)\.",
              f"OUTPUT:  HyperFrames, 1080 × 1920, 60 i/s. {dur:.2f} s ({voice:.2f} s de voix + {dur - voice:.2f} s d'outro).", spec)
if "fin barre orange + cyan → CTA « Les 3 vidéos sur la chaîne »" in spec:
    spec = spec.replace("fin barre orange + cyan → CTA « Les 3 vidéos sur la chaîne »", OUTRO)
elif "outro « formation offerte »" not in spec:
    spec = re.sub(r"(MOTION:  .*)", lambda m: m.group(1).rstrip() + f" Fin : {OUTRO}.", spec, count=1)
spec = re.sub(r"SOUND:   voix −14 LUFS ; \d+ SFX \(whoosh, pop, impact\)\.",
              f"SOUND:   voix −14 LUFS ; {nsfx} SFX dont les 6 de l'outro (souffle cinématique, basse, whoosh, pop, sparkle ; sons HyperFrames, licence Pixabay).", spec)
(d / "SPEC.md").write_text(spec)
rev = (d / "REVIEW.md").read_text()
rev = re.sub(r"\(Formation (\d), v1 du 2026-11-09\)", r"(Formation \1, v2 du 2026-11-09 : outro)", rev)
if "Outro v2" not in rev:
    rev = rev.replace("## Mesuré", "- Outro v2 (demande de Nass du 2026-11-09 : « outro ultra banger, 3 s, sons HyperFrames, formation offerte sur Nassin Crypto ») :\n"
                      "  la fin barre + CTA est remplacée par l'outro commune de comp_lib (`end=\"outro\"`), même chorégraphie sur F1, F2, F3.\n\n## Mesuré", 1)
rev = re.sub(r"- Rendu : [\d.]+ s, 1080 × 1920, 60 i/s, .+? LUFS, crête .+? dBTP, .+? Mo\.",
             f"- Rendu : {dur:.2f} s, 1080 × 1920, 60 i/s, {a.lufs} LUFS, crête {a.peak} dBTP, {a.mb} Mo.", rev)
(d / "REVIEW.md").write_text(rev)
ep = ROOT / "projects" / a.fx / "EPISODE.md"; t = ep.read_text(); lines = t.splitlines(keepends=True); hit = 0
for i, l in enumerate(lines):
    if f"/projects/{a.fx}/{a.slug}/" in l and "v1 rendue le 2026-11-09" in l:
        lines[i] = l.replace("**v1 rendue le 2026-11-09**", "**v2 (outro) rendue le 2026-11-09**"); hit += 1
ep.write_text("".join(lines)); print("docs ok", a.slug, f"{voice:.2f}s voix", "EPISODE changé" if hit else "EPISODE inchangé")
