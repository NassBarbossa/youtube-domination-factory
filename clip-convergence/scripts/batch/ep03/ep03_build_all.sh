#!/bin/zsh
cd ~/youtube-domination-factory/clip-convergence
for d in projects/ep03/*/; do
  p=${d%/}; echo "== $p"
  uv run --python 3.12 --with numpy,opencv-python,faster-whisper python scripts/build_media.py $p 2>&1 | tail -3
  uv run --python 3.12 --with numpy,opencv-python python scripts/face_track.py $p 2>&1 | tail -2
  if grep -q '"screen"' $p/cut.json; then uv run --python 3.12 --with numpy python scripts/build_screen.py $p 2>&1 | tail -2; fi
done
echo BUILD_ALL_DONE
