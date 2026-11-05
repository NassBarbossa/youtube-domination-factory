"""Transcription mot à mot sur Mac Apple Silicon avec mlx-whisper (GPU), même format de sortie que transcribe.py.

Usage : uv run --with mlx-whisper python transcribe_mlx.py <source> <sortie.json> [--model mlx-community/whisper-large-v3-turbo]
Sortie : [{start, end, text, words: [{w, s, e}]}] en temps de la source. Dix fois plus rapide que faster-whisper sur CPU.
"""
import argparse, json, subprocess, tempfile
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("source"); ap.add_argument("out")
ap.add_argument("--model", default="mlx-community/whisper-large-v3-turbo")
a = ap.parse_args()

import mlx_whisper  # noqa: E402

with tempfile.TemporaryDirectory() as td:
    wav = Path(td) / "audio.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.source, "-vn", "-ac", "1", "-ar", "16000", str(wav)], check=True)
    r = mlx_whisper.transcribe(str(wav), path_or_hf_repo=a.model, language="fr", word_timestamps=True,
                               condition_on_previous_text=False)
out = []
for s in r["segments"]:
    words = [{"w": w["word"], "s": round(w["start"], 2), "e": round(w["end"], 2)} for w in s.get("words", [])]
    out.append({"start": round(s["start"], 2), "end": round(s["end"], 2), "text": s["text"].strip(), "words": words})
Path(a.out).write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
print(f"{len(out)} phrases -> {a.out}")
