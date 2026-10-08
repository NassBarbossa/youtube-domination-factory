# Rebrand 100 % crypto — à valider par Nass (2026-10-07)

Branche `rebrand/crypto`, **rien n'est commité ni poussé**. Pour voir les changements : `git diff` sur cette branche.

## Ce qui a changé
- **CLAUDE.md, README, orchestrateur** : niche crypto on-chain (spot, zéro levier, wallet public), avatar recopié mot pour mot, ton direct/transparent/pédagogique, règle halal non négociable, garde-fou : le pipeline refuse un sujet levier/futures/short/lending/casino et propose un angle spot.
- **yt-script + templates de slides** : nouvelle charte (noir #0B0B0B, sable #DBB17F, crème #F4EFE7, bleu punk #648596, Archivo Black + Public Sans), règles de dictée/centrage/animation conservées, CTA par funnel (TOP → formation offerte, MIDDLE → challenge 10K → 100K, BOTTOM → communauté privée + Convergence), disclaimer obligatoire, 6 pistes « information gain » crypto.
- **Titres, descriptions, repurposing** : mots-clés crypto débutant, zéro promesse de gain, disclaimer, liens écosystème, thread X @punk6995, LinkedIn angle patrimoine.
- **Miniatures** : punk pixel + palette du site, chiffres réels et sourcés uniquement, aucun graphique généré par IA.
- **Calendrier / analytics** : mix proposé, benchmarks « à recalibrer », anciennes vidéos IA analysées à part.
- **Veille** : 40 chaînes crypto vérifiées (28 FR, 12 US), ancienne liste IA archivée, sujets non halal étiquetés, tests 58/58 OK.

## À trancher
1. **Mix de contenus** proposé : éducation débutant 35 %, suivi du challenge 25 %, on-chain/early 20 %, actu/Convergence 15 %, questions communauté 5 % ; rythme « 3 vidéos + 2 Shorts » par semaine ?
2. **Liens réels** à fournir : formation offerte, communauté privée, Convergence, X, Instagram, Twitch, YouTube.
3. **Couleurs hausse/baisse** dans les slides (pas de vert/rouge dans la charte) : sable = hausse, gris = baisse, OK ?
4. **Langue du thread X @punk6995** : français ou anglais ?
5. **LinkedIn** : on garde le canal ?
6. **Veille** : garder Finary / Matthieu Louvet (finance générale, mais pile l'avatar) ? Valider les 9 chaînes « à vérifier » et le classement en tiers.
7. **Assets manquants** : une image de référence du punk (`yt-miniature/references/punk/`), `neutral.jpg` (photo de secours citée mais absente).
8. **Live Convergence** : jour et heure fixes ?

## Pour mettre en ligne (après validation)
```bash
git add -A ':!shows' && git commit -m "rebrand: chaîne 100 % crypto" && git push -u origin rebrand/crypto
ssh root@72.62.253.227
cd /root/youtube-domination-factory && git fetch && git checkout rebrand/crypto && git pull
cd yt-veille/scripts && python3 -m pytest tests -q && python3 daily_monitor.py && python3 report.py
```
Les anciennes vidéos IA restent ~7 jours dans le top 25 de la veille (sauf purge de la base sur le VPS). Le filtre halal étiquette les sujets mais ne les retire pas encore du top 25 (modif de `report.py` à prévoir).
