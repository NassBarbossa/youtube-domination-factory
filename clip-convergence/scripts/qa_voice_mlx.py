"""Contrôle de la voix montée sur Mac Apple Silicon : même rôle que qa_voice.py, avec mlx-whisper (GPU) au lieu de
faster-whisper. Re-transcrit assets/audio/voice.wav et compare chaque morceau à son champ "text" du cut.json.

Usage : uv run --python 3.12 --with mlx-whisper python qa_voice_mlx.py <dossier_projet>
Un mot coupé, avalé ou qui dépasse du morceau suivant se voit à la première ou à la dernière place : ajuster a / b
de 0,05 à 0,2 s dans cut.json, puis relancer build_media.py (et face_track.py, build_screen.py) et ce contrôle.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import mlx_whisper

proj = Path(sys.argv[1])
tl = json.loads((proj / "timeline.json").read_text(encoding="utf-8"))
with tempfile.TemporaryDirectory() as td:
    wav = Path(td) / "voice16.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(proj / "assets/audio/voice.wav"), "-ac", "1", "-ar", "16000",
                    str(wav)], check=True)
    r = mlx_whisper.transcribe(str(wav), path_or_hf_repo="mlx-community/whisper-large-v3-turbo", language="fr",
                               word_timestamps=True, condition_on_previous_text=False)
words = [w for s in r["segments"] for w in s.get("words", [])]
for seg in tl["segments"]:
    ws = [w["word"].strip() for w in words if seg["out_start"] - 0.05 <= w["start"] < seg["out_end"]]
    print(f"{seg['id']:5} {seg['out_start']:6.2f}-{seg['out_end']:6.2f} | {' '.join(ws)}")
    print(f"      attendu : {seg['text']}")
