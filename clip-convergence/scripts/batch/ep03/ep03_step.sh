#!/bin/zsh
# f1_step.sh <slug> : qa voix + composition + check + instantanés aux moments clés
set -e
R=~/youtube-domination-factory/clip-convergence; P=$R/projects/ep03/$1; S=/private/tmp/claude-502/-Users-punk6995/04d8e694-c148-450d-98a7-77b6fdcfb548/scratchpad
cd $R
uv run --python 3.12 --with mlx-whisper python scripts/qa_voice_mlx.py projects/ep03/$1 2>&1 | grep -v "Fetching" | python3 -I -c "
import sys,re,difflib
lines=sys.stdin.read().splitlines()
for i,l in enumerate(lines):
    if l.strip().startswith('attendu'):
        got=re.sub(r\"\s+'\",\"'\",lines[i-1].split('|',1)[1].strip()).lower(); exp=l.split(':',1)[1].strip().lower()
        r=difflib.SequenceMatcher(None,got,exp).ratio()
        print(('OK ' if r>0.9 else 'DIFF %.2f '%r)+lines[i-1][:60])
"
cd $P
python3 -I make_comp.py | tail -1 | tee $S/last_build.txt
npx hyperframes check --json 2>/dev/null | python3 -I $S/chk.py
T=$(python3 -I -c "
import re;s=open('$S/last_build.txt').read()
d=float(re.search(r'durée ([\d.]+)',s).group(1)); seams=[float(x) for x in re.findall(r'[\d.]+',re.search(r'coutures \[(.*?)\]',s).group(1))]
end=d-4.15; pts=[0.8]; b=[0]+seams+[end]
for a,c in zip(b,b[1:]): pts.append(round((a+c)/2,2))
pts+= [round(end-0.6,2), round(d-0.4,2)]
print(','.join(str(p) for p in sorted(set(pts))))")
echo "instants $T"
npx hyperframes snapshot --at $T --json 2>/dev/null | python3 -I -c "import json,sys; print(json.load(sys.stdin)['contactSheets'][0])"
