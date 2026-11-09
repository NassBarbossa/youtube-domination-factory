#!/bin/zsh
# outro_finish.sh <f1|f2|f3> <slug> : composition, rendu, QA, docs v2, commit, quota
set -e
FX=$1; SLUG=$2; N=${SLUG:0:2}; FN=${FX:1:1}
R=~/youtube-domination-factory/clip-convergence; P=$R/projects/$FX/$SLUG; S=/private/tmp/claude-502/-Users-punk6995/04d8e694-c148-450d-98a7-77b6fdcfb548/scratchpad
cd $P
DUR=$(python3 -I make_comp.py | tail -1 | sed -E 's/durée ([0-9.]+) s.*/\1/')
npx hyperframes check --json 2>/dev/null | python3 -I $S/chk.py | tee $S/chk_$FX_$SLUG.txt | grep -q "'error'" && { echo "CHECK KO"; exit 1; }
NODE_OPTIONS=--max-old-space-size=8192 npx hyperframes render --fps 60 --quality delivery --workers 4 --output $R/exports/$FX/$SLUG.mp4 > $S/render_$SLUG.log 2>&1 || { echo "RENDU KO"; tail -5 $S/render_$SLUG.log; exit 1; }
cd $R
Q=$(uv run --python 3.12 --with numpy python scripts/qa_render.py exports/$FX/$SLUG.mp4 --duration $DUR 2>&1 | tail -8)
echo "$Q" | tail -1
echo "$Q" | grep -q "tout est bon" || { echo "$Q"; echo "QA KO"; exit 1; }
D=$(echo "$Q" | awk '/durée/{print $3}'); L=$(echo "$Q" | awk '/sonie/{print $3}'); PK=$(echo "$Q" | awk '/crête/{print $4}'); MB=$(echo "$Q" | awk '/Mo/{print $1}')
python3 -I $S/outro_docs.py $FX $SLUG --dur $D --lufs $L --peak $PK --mb $MB
cd ~/youtube-domination-factory
TITLE=$(python3 -I -c "import json,re;print(re.search(r'F$FN-\d\d — (.+?) \(Formation',json.load(open('$P/cut.json'))['short']).group(1))")
git add clip-convergence/projects/$FX/$SLUG clip-convergence/projects/$FX/EPISODE.md clip-convergence/scripts/comp_lib.py
git commit -q -m "clip-convergence: Formation $FN clip $N « $TITLE », outro formation offerte (v2)

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01Dvwzf4geW5RHh6Lx8hh65j"
git log --oneline -1
cd $P; npx hyperframes usage --json 2>/dev/null | python3 -I -c "import json,sys; d=json.load(sys.stdin); print('QUOTA session', d['session']['usedPercent'], '% utilisé | semaine', d['weekly']['usedPercent'], '%')"
