# Générateur de la série EP.03 (2026-11-09)

`cat ep03_head.py ep03_clips.py ep03_tail.py > ep03_gen.py && python3 ep03_gen.py` (depuis `clip-convergence/`) crée les 15 projets `projects/ep03/56…70` (cut.json + make_comp.py) depuis le modèle `projects/ep01/21-montrez-moi-des-preuves`.
Puis `ep03_build_all.sh` (médias, visages, écrans), `ep03_step.sh <slug>` (voix, composition, check, planche), `ep03_finish.sh <slug> "<images>" --look … --motion … [--choices …]` (rendu 60 i/s, qa_render, SPEC/REVIEW/EPISODE/BATCH, commit).
Les chemins du scratchpad (`/private/tmp/claude-502/…`) dans les `.sh` sont à remplacer par ce dossier. Copie de travail, telle qu'utilisée ; les clips 56, 57, 60–62 ont ensuite été ajustés à la main (états écran seul / solo) et ces ajustements sont reportés dans `ep03_clips.py`.
