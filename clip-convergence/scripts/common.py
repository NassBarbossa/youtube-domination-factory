"""Outils partagés des scripts clip-convergence : ffmpeg, lecture audio, cut.json, sortie UTF-8."""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np

FF = shutil.which("ffmpeg")
FFPROBE = shutil.which("ffprobe")
if not FF or not FFPROBE:
    sys.exit("ffmpeg / ffprobe introuvables dans le PATH (Windows : winget install Gyan.FFmpeg ; Mac : brew install ffmpeg)")

SKILL = Path(__file__).resolve().parent.parent
YUNET = SKILL / "assets/models/face_detection_yunet_2023mar.onnx"

# console Windows en cp1252 : sans ça, les accents et les « » plantent les print
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def pcm(path, start=0.0, dur=None, sr=16000, ch=1):
    """Audio de [start, start + dur] en float32 (tout le fichier si dur est None) ; (n, ch) si ch > 1."""
    cmd = [FF, "-v", "error", "-ss", f"{max(start, 0):.3f}"]
    if dur is not None:
        cmd += ["-t", f"{dur:.3f}"]
    cmd += ["-i", str(path), "-vn", "-ac", str(ch), "-ar", str(sr), "-f", "f32le", "-"]
    a = np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, dtype=np.float32)
    return a.reshape(-1, ch) if ch > 1 else a


def seconds(t):
    """« 1690.5 », « 28:10.5 » ou « 1:28:10 » -> secondes."""
    s = 0.0
    for part in str(t).split(":"):
        s = s * 60 + float(part)
    return s


def load_cut(proj):
    """cut.json du projet, avec « ~ » développé dans les chemins."""
    cfg = json.loads((Path(proj) / "cut.json").read_text(encoding="utf-8"))
    for k in ("source", "transcript"):
        if k in cfg:
            cfg[k] = os.path.expanduser(cfg[k])
    return cfg
