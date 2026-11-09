#!/bin/zsh
# f1_finish.sh <slug> <frames> [args f3_docs…] : rendu, QA, docs, commit, quota
set -e
SLUG=$1; FRAMES=$2; shift 2
R=~/youtube-domination-factory/clip-convergence; P=$R/projects/ep03/$SLUG; S=/private/tmp/claude-502/-Users-punk6995/04d8e694-c148-450d-98a7-77b6fdcfb548/scratchpad
cd $P
DUR=$(python3 -I make_comp.py | tail -1 | sed -E 's/durée ([0-9.]+) s.*/\1/')
NODE_OPTIONS=--max-old-space-size=8192 npx hyperframes render --fps 60 --quality delivery --workers 4 --output $R/exports/ep03/$SLUG.mp4 > $S/render_$SLUG.log 2>&1 || { echo "RENDU KO"; tail -5 $S/render_$SLUG.log; exit 1; }
cd $R
Q=$(uv run --python 3.12 --with numpy python scripts/qa_render.py exports/ep03/$SLUG.mp4 --duration $DUR 2>&1 | tail -8)
echo "$Q"
echo "$Q" | grep -q "tout est bon" || { echo "QA KO"; exit 1; }
D=$(echo "$Q" | awk '/durée/{print $3}'); L=$(echo "$Q" | awk '/sonie/{print $3}'); PK=$(echo "$Q" | awk '/crête/{print $4}'); MB=$(echo "$Q" | awk '/Mo/{print $1}')
python3 -I $S/ep03_docs.py $SLUG --dur $D --lufs $L --peak $PK --mb $MB --frames "$FRAMES" "$@"
cd ~/youtube-domination-factory
N=${SLUG:0:2}; TITLE=$(python3 -I -c "import json,re;print(re.search(r'(\d\d) — (.+?) \(Convergence EP\.03\)',json.load(open('$P/cut.json'))['short']).group(2))")
git add clip-convergence/projects/ep03/$SLUG clip-convergence/projects/ep03/EPISODE.md clip-convergence/BATCH.md clip-convergence/scripts
git commit -q -m "clip-convergence: EP.03 clip $N « $TITLE »

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01Dvwzf4geW5RHh6Lx8hh65j"
git log --oneline -1
cd $P; npx hyperframes usage --json 2>/dev/null | python3 -I -c "import json,sys; d=json.load(sys.stdin); print('QUOTA session', d['session']['usedPercent'], '% utilisé, reset', d['session']['resetsAt'], '| semaine', d['weekly']['usedPercent'], '%')"
