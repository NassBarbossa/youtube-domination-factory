"""Crée le squelette d'un projet de clip à partir d'un projet existant (même épisode ou non).

Copie AGENTS.md, CLAUDE.md, hyperframes.json, package.json (nom remplacé), meta.json (id, nom, date), assets/fonts,
assets/sfx/*.mp3, le logo. Ne copie ni cut.json, ni make_comp.py, ni les médias construits.
Usage : python new_clip.py <projet_modèle> <nouveau_projet>
"""
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

src, dst = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
if dst.exists():
    sys.exit(f"{dst} existe déjà")
dst.mkdir(parents=True)
for f in ("AGENTS.md", "CLAUDE.md", "hyperframes.json"):
    shutil.copy(src / f, dst / f)
pkg = json.loads((src / "package.json").read_text(encoding="utf-8"))
pkg["name"] = dst.name
(dst / "package.json").write_text(json.dumps(pkg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
(dst / "meta.json").write_text(json.dumps({"id": dst.name, "name": dst.name, "createdAt": datetime.now(timezone.utc).isoformat()
                                           .replace("+00:00", "Z")}, indent=2) + "\n", encoding="utf-8")
(dst / "assets/video").mkdir(parents=True)
(dst / "assets/audio").mkdir(parents=True)
shutil.copytree(src / "assets/fonts", dst / "assets/fonts")
(dst / "assets/sfx").mkdir()
for f in (src / "assets/sfx").glob("*.mp3"):
    shutil.copy(f, dst / "assets/sfx" / f.name)
for f in (src / "assets").glob("*.svg"):
    shutil.copy(f, dst / "assets" / f.name)
print("créé", dst)
