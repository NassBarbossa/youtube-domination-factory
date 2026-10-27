#!/usr/bin/env python3
"""Génère ou édite une image via l'API Images d'OpenRouter (POST /api/v1/images). Stdlib seulement.

Deux modes :

  Génération (portrait ancre, fond, scène) :
    python3 yt-miniature/scripts/generate.py --prompt-file prompt.txt \
        --ref yt-miniature/references/nass/neutral-2-2026-10.jpg \
        --ref yt-miniature/references/nass/neutral-2026-10.jpg \
        --aspect 3:4 --quality high --out yt-miniature/outputs/slug-anchor.jpg

  Édition d'une ancre validée (une seule chose change, le visage est verrouillé) :
    python3 yt-miniature/scripts/generate.py \
        --base yt-miniature/outputs/convergence-ep03-cutout-nass-v3-2.jpg \
        --edit "replace the charcoal t-shirt with a plain white crewneck t-shirt under an open dark navy overshirt" \
        --out yt-miniature/outputs/slug-nass-outfit.jpg

  Le mode édition compose le prompt lui-même : image 1 = portrait approuvé, changement unique,
  liste de ce qui ne bouge pas (visage, traits, peau, expression, cheveux, angle, proportions, cadrage, lumière).
  --keep ajoute des éléments à cette liste (ex. --keep "the solid green background"), --edit-prompt-file
  remplace la composition automatique par un prompt complet.

Règles encodées :
  - --n plafonné à 2 (règle de Nass : deux tirages, pas quatre) ;
  - l'ordre des --ref compte : la première image est celle que le prompt appelle « image 1 » ;
  - chaque appel est journalisé dans yt-miniature/outputs/generation-log.jsonl (modèle, coût, fichiers) ;
  - --dry-run affiche le corps de la requête (sans les images) et ne dépense rien.

Modèles (voir references/generation-images.md) : openai/gpt-image-2 par défaut (portraits, éditions, 16 références),
google/gemini-3.1-flash-image (Nano Banana 2, 14 références), openai/gpt-image-2.5-flare (fond transparent).
La clé vient de OPENROUTER_API_KEY (env), puis du .env à la racine du repo, ./.env, ~/.zshrc, ~/.env.
"""
import argparse
import base64
import json
import mimetypes
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ENDPOINT = "https://openrouter.ai/api/v1/images"
DEFAULT_MODEL = "openai/gpt-image-2"
REPO_ROOT = Path(__file__).resolve().parents[2]
LOG_PATH = REPO_ROOT / "yt-miniature" / "outputs" / "generation-log.jsonl"
MAX_N = 2

KEEP_DEFAULT = (
    "the face, facial features, skin texture, expression, hairstyle, head angle, "
    "body proportions, framing and lighting"
)


def api_key(name: str = "OPENROUTER_API_KEY") -> str:
    key = os.environ.get(name)
    if key:
        return key
    for candidate in (REPO_ROOT / ".env", Path.cwd() / ".env", Path.home() / ".zshrc", Path.home() / ".env"):
        if candidate.exists():
            m = re.search(name + r'\s*=\s*["\']?([^"\'\s]+)', candidate.read_text())
            if m:
                return m.group(1)
    sys.exit(f"{name} introuvable (env, {REPO_ROOT / '.env'}, ./.env, ~/.zshrc, ~/.env)")


def data_url(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        sys.exit(f"Image introuvable : {p}")
    mt = mimetypes.guess_type(p.name)[0] or "image/jpeg"
    b64 = base64.b64encode(p.read_bytes()).decode()
    return {"type": "image_url", "image_url": {"url": f"data:{mt};base64,{b64}"}}


def edit_prompt(change: str, keep_extra: list[str]) -> str:
    keep = KEEP_DEFAULT
    if keep_extra:
        keep += ", " + ", ".join(keep_extra)
    change = change.strip().rstrip(".")
    return (
        "Image 1 is the approved portrait of this specific real person. Edit image 1: "
        f"{change}. Change only that. Keep everything else exactly the same as image 1: {keep} "
        "must remain identical, so that the person is still immediately recognisable as the same "
        "individual. Do not add text, props or new elements. Photorealistic, same sharpness as image 1."
    )


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--prompt", help="Prompt en anglais (génération)")
    ap.add_argument("--prompt-file", help="Fichier contenant le prompt (génération)")
    ap.add_argument("--base", help="Ancre validée à éditer : devient l'image 1 (mode édition)")
    ap.add_argument("--edit", help="Le seul changement demandé, en anglais (mode édition)")
    ap.add_argument("--edit-prompt-file", help="Prompt d'édition complet, à la place de la composition automatique")
    ap.add_argument("--keep", action="append", default=[], help="Élément supplémentaire à préserver (répétable)")
    ap.add_argument("--ref", action="append", default=[], help="Photo de référence d'identité (répétable, ordre conservé)")
    ap.add_argument("--aspect", default="3:4", help="1:1, 3:4, 16:9… (3:4 pour un portrait, 16:9 pour un fond)")
    ap.add_argument("--quality", default=None, help="OpenAI : auto|low|medium|high (xhigh|max sur gpt-image-2.5)")
    ap.add_argument("--resolution", default=None, help="Google / Sourceful : 512|1K|2K|4K")
    ap.add_argument("--background", default=None, help="transparent|opaque (modèles qui le supportent)")
    ap.add_argument("--output-format", default=None, help="png|jpeg|webp")
    ap.add_argument("--n", type=int, default=1, help=f"Nombre de tirages, {MAX_N} max")
    ap.add_argument("--out", required=True, help="Fichier de sortie (suffixes -1, -2 si --n 2)")
    ap.add_argument("--dry-run", action="store_true", help="Affiche la requête sans appeler l'API")
    ap.add_argument("--no-log", action="store_true", help="Ne pas journaliser dans outputs/generation-log.jsonl")
    a = ap.parse_args()

    if a.n < 1 or a.n > MAX_N:
        sys.exit(f"--n doit être entre 1 et {MAX_N} (deux tirages maximum, sur la scène, jamais sur le visage)")

    mode = "edit" if (a.base or a.edit or a.edit_prompt_file) else "generate"
    if mode == "edit":
        if not a.base:
            sys.exit("Mode édition : --base <ancre validée> est obligatoire")
        if a.edit_prompt_file:
            prompt = Path(a.edit_prompt_file).read_text(encoding="utf-8")
        elif a.edit:
            prompt = edit_prompt(a.edit, a.keep)
        else:
            sys.exit("Mode édition : donner --edit \"<un seul changement>\" ou --edit-prompt-file")
        refs = [a.base] + a.ref
    else:
        prompt = a.prompt or (Path(a.prompt_file).read_text(encoding="utf-8") if a.prompt_file else None)
        if not prompt:
            sys.exit("Mode génération : --prompt ou --prompt-file")
        refs = list(a.ref)

    body: dict = {"model": a.model, "prompt": prompt, "aspect_ratio": a.aspect, "n": a.n}
    if a.quality:
        body["quality"] = a.quality
    if a.resolution:
        body["resolution"] = a.resolution
    if a.background:
        body["background"] = a.background
    if a.output_format:
        body["output_format"] = a.output_format
    if refs:
        body["input_references"] = [data_url(r) for r in refs]

    if a.dry_run:
        shown = dict(body)
        if refs:
            shown["input_references"] = [f"<{Path(r).name}>" for r in refs]
        print(json.dumps(shown, ensure_ascii=False, indent=2))
        return

    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {api_key()}", "Content-Type": "application/json"},
    )
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=290) as r:
            d = json.load(r)
    except urllib.error.HTTPError as e:
        detail = e.read()[:600]
        if e.code == 402:
            sys.exit("OpenRouter 402 : solde insuffisant (il faut au moins 1 $ pour une sortie image). Recharger avant de relancer.")
        sys.exit(f"{a.model} HTTP {e.code}: {detail!r}")
    if "error" in d:
        sys.exit(f"{a.model} error: {d['error']}")

    items = d.get("data") or []
    if not items:
        sys.exit(f"Aucune image dans la réponse : {json.dumps(d)[:600]}")
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    written = []
    for i, item in enumerate(items):
        raw = base64.b64decode(item["b64_json"]) if item.get("b64_json") else urllib.request.urlopen(item["url"]).read()
        target = out if len(items) == 1 else out.with_name(f"{out.stem}-{i + 1}{out.suffix}")
        target.write_bytes(raw)
        written.append(str(target))
    cost = (d.get("usage") or {}).get("cost")
    print(f"{a.model} [{mode}] -> {', '.join(written)} cost={cost} USD ({time.time() - t0:.0f} s)")

    if not a.no_log:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "model": a.model,
            "mode": mode,
            "out": written,
            "cost_usd": cost,
            "aspect": a.aspect,
            "quality": a.quality,
            "resolution": a.resolution,
            "refs": [Path(r).name for r in refs],
            "edit": a.edit,
            "prompt_file": a.prompt_file or a.edit_prompt_file,
        }
        with LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
