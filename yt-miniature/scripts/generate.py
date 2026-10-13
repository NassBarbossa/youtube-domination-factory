#!/usr/bin/env python3
"""Generate a YouTube thumbnail base image via OpenRouter (Nano Banana 2).

Usage:
  python3 yt-miniature/scripts/generate.py \
      --prompt-file prompt.txt \
      --ref yt-miniature/references/nass/curious.jpg \
      --out yt-miniature/outputs/slug-concept-a.jpg

The prompt MUST be in English. The reference photo is sent alongside the prompt
so the model keeps Nass's real face. The API key is read from the env var
OPENROUTER_API_KEY, or from ~/.zshrc as a fallback (macOS setup).
"""
import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

MODEL = "google/gemini-3.1-flash-image-preview"
ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"


def api_key(name: str = "OPENROUTER_API_KEY") -> str:
    key = os.environ.get(name)
    if key:
        return key
    repo_root = Path(__file__).resolve().parents[2]
    for candidate in (repo_root / ".env", Path.cwd() / ".env", Path.home() / ".zshrc", Path.home() / ".env"):
        if candidate.exists():
            m = re.search(name + r'\s*=\s*["\']?([^"\'\s]+)', candidate.read_text())
            if m:
                return m.group(1)
    sys.exit(f"{name} not found (env, {repo_root / '.env'}, ./.env, ~/.zshrc, ~/.env)")


def openai_edit(prompt: str, refs: list[str], model: str) -> bytes:
    """Fallback provider: OpenAI gpt-image edits (reference photo as input image)."""
    boundary = "----hfThumb" + os.urandom(8).hex()
    parts: list[bytes] = []

    def field(name: str, value: str) -> None:
        parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n'.encode())

    field("model", model)
    field("prompt", prompt)
    field("size", "1536x1024")
    field("quality", "high")
    field("n", "1")
    for ref in refs:
        p = Path(ref)
        parts.append(
            f'--{boundary}\r\nContent-Disposition: form-data; name="image[]"; filename="{p.name}"\r\n'
            f"Content-Type: {mime(p)}\r\n\r\n".encode() + p.read_bytes() + b"\r\n"
        )
    parts.append(f"--{boundary}--\r\n".encode())
    req = urllib.request.Request(
        "https://api.openai.com/v1/images/edits",
        data=b"".join(parts),
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Authorization": f"Bearer {api_key('OPENAI_API_KEY')}",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"OpenAI error {e.code}: {e.read()[:600]!r}")
    return base64.b64decode(data["data"][0]["b64_json"])


def mime(path: Path) -> str:
    return "image/png" if path.suffix.lower() == ".png" else "image/jpeg"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", help="English prompt text")
    ap.add_argument("--prompt-file", help="File containing the English prompt")
    ap.add_argument("--ref", action="append", default=[], help="Reference photo (repeatable)")
    ap.add_argument("--out", required=True, help="Output image path")
    ap.add_argument("--aspect", default="16:9")
    ap.add_argument("--provider", choices=["openrouter", "openai"], default="openrouter")
    ap.add_argument("--model", help="Override model id for the chosen provider")
    args = ap.parse_args()

    prompt = args.prompt or (Path(args.prompt_file).read_text() if args.prompt_file else None)
    if not prompt:
        sys.exit("Need --prompt or --prompt-file")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    if args.provider == "openai":
        raw = openai_edit(prompt, args.ref, args.model or "gpt-image-1.5")
        out.write_bytes(raw)
        print(f"Saved {out} ({len(raw)//1024} KB) via OpenAI")
        return

    content = [{"type": "text", "text": prompt}]
    for ref in args.ref:
        p = Path(ref)
        b64 = base64.b64encode(p.read_bytes()).decode()
        content.append({"type": "image_url", "image_url": {"url": f"data:{mime(p)};base64,{b64}"}})

    body = {
        "model": args.model or MODEL,
        "messages": [{"role": "user", "content": content}],
        "modalities": ["image", "text"],
        "image_config": {"aspect_ratio": args.aspect},
        "max_tokens": 4096,
    }
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key()}"},
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read())

    try:
        img = data["choices"][0]["message"]["images"][0]["image_url"]["url"]
    except (KeyError, IndexError, TypeError):
        sys.exit(f"No image in response: {json.dumps(data)[:800]}")

    raw = base64.b64decode(img.split(",", 1)[1])
    out.write_bytes(raw)
    cost = data.get("usage", {}).get("cost")
    print(f"Saved {out} ({len(raw)//1024} KB) cost={cost} USD")


if __name__ == "__main__":
    main()
