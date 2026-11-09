#!/bin/zsh
# Re-rend tous les clips Formation avec l'outro, un à la fois ; s'arrête à la première erreur.
R=~/youtube-domination-factory/clip-convergence; S=/private/tmp/claude-502/-Users-punk6995/04d8e694-c148-450d-98a7-77b6fdcfb548/scratchpad
for FX in f1 f2 f3; do
  for f in $R/exports/$FX/*.mp4; do
    SLUG=$(basename $f .mp4)
    [[ $FX == f1 && $SLUG == 01-pas-une-option ]] && continue
    grep -q "end=\"outro\"" $R/projects/$FX/$SLUG/make_comp.py || { echo "SKIP $FX/$SLUG (pas d'outro)"; continue; }
    echo "== $FX/$SLUG $(date +%H:%M:%S)"
    zsh $S/outro_finish.sh $FX $SLUG 2>&1 | tail -4 || { echo "STOP sur $FX/$SLUG"; exit 1; }
    # le pipe masque le code de retour : on vérifie le commit
    git -C ~/youtube-domination-factory log --oneline -1 | grep -q "$SLUG\|clip ${SLUG:0:2} " || { echo "STOP (pas de commit) sur $FX/$SLUG"; exit 1; }
  done
done
echo "TOUT RENDU $(date +%H:%M:%S)"
