# Miniatures — « Pourquoi il faut obligatoirement investir son argent en 2026 » (formation offerte 1/3)

Date : 2026-10-04 · Statut : 3 concepts générés (Nano Banana 2 via OpenRouter, 4 appels, 0,27 $) + texte Syne appliqué

Fichiers finaux : `pourquoi-investir-2026-a-secret-final.jpg` (base v2, chart en bas à gauche, le modèle a ajouté les % malgré la consigne), `pourquoi-investir-2026-b-karting-final.jpg`, `pourquoi-investir-2026-c-coins-final.jpg` (texte passé de « COMMENCE ICI » à « LA BASE » : la ligne longue chevauchait le visage).

## Concept A — Le Secret (camembert)  ★ recommandé
- Layout : Nass à droite (45 % du cadre), donut 3D 40/30/15/15 à gauche, haut-gauche vide pour le texte
- Visage : `curious.jpg` — sourcil levé, demi-sourire fermé, « je vais te révéler un truc »
- Dominante : cyan `#00E5FF`, tranche 15 % orange tirée hors du cercle
- Texte (overlay) : `2026` orange + `LE SECRET` blanc
- Pourquoi : le titre dit POURQUOI, la miniature montre le COMMENT (la règle 40/30/15/15) → vraie complémentarité
- Scores : scroll-stop 4 · clarté 4 · synergie titre 5 · brand 5 → **18/20**

## Concept B — Karting vs F1
- Layout : Nass à droite, kart orange net à gauche, F1 floutée derrière
- Visage : `skeptical.jpg` — sourcil levé, smirk « t'as sauté les bases »
- Dominante : orange `#FF6B35`
- Texte : `ÉTAPE 1`
- Pourquoi : reprend la punchline du hook, très distinctif dans un feed finance
- Risque : peut se lire comme une vidéo auto/sport sans le titre
- Scores : scroll-stop 5 · clarté 3 · synergie 4 · brand 3 → **15/20**

## Concept C — L'escalier de pièces
- Layout : Nass à droite (sourire ouvert `confident.png`, préciser hoodie dans le prompt), 5 piles de pièces en escalier à gauche
- Dominante : cyan sur or
- Texte : `2026` orange + `LA BASE` blanc (« COMMENCE ICI » trop long, chevauche le visage à 1280 px)
- Pourquoi : lisible en 1 seconde, rassurant pour l'avatar débutant
- Risque : visuel le plus générique de la niche finance
- Scores : scroll-stop 3 · clarté 5 · synergie 4 · brand 4 → **16/20**

## Régénérer (dès qu'une clé est valide)
```bash
P=yt-miniature/outputs/prompts; R=yt-miniature/references/nass; O=yt-miniature/outputs
python3 yt-miniature/scripts/generate.py --prompt-file $P/pourquoi-investir-2026-a-secret.txt  --ref $R/curious.jpg   --out $O/pourquoi-investir-2026-a-secret.jpg
python3 yt-miniature/scripts/generate.py --prompt-file $P/pourquoi-investir-2026-b-karting.txt --ref $R/skeptical.jpg --out $O/pourquoi-investir-2026-b-karting.jpg
python3 yt-miniature/scripts/generate.py --prompt-file $P/pourquoi-investir-2026-c-coins.txt   --ref $R/confident.png --out $O/pourquoi-investir-2026-c-coins.jpg
# puis texte + preview mobile
python3 yt-miniature/scripts/overlay.py $O/pourquoi-investir-2026-a-secret.jpg $O/pourquoi-investir-2026-a-secret-final.jpg --line "2026" --line "LE SECRET" --colors "#FF6B35,#FFFFFF" --sizes 210,96
python3 yt-miniature/scripts/check.py $O/pourquoi-investir-2026-a-secret-final.jpg
```
Ajouter `--provider openai` pour passer par gpt-image si OpenRouter reste indisponible.

## Concept D — Billet déchiré (style demandé par Nass, référence identité `recent-2026-10.jpg`)
- Layout : Nass centré, buste, regard sérieux ; billet 100 € plein cadre déchiré en 4 bandes rouge 40 % / vert 30 % / jaune 15 % / bleu 15 %, labels blancs + pointillés en haut
- Texte (overlay bas, centré) : `AVANT D'INVESTIR`
- Luminosité 116 (dans la cible), 2 générations : `d-billet.jpg` (labels par le modèle, retenu) et `d-billet-clean.jpg` (sans labels, bandes moins proportionnelles)
- Fichier final : `pourquoi-investir-2026-d-billet-final.jpg`

### D v2 (retenue) — sourire, cadrage plus large, billets propres
- Référence : `smile-2026-10.jpg` (nouvelle série, barbe courte)
- 2 candidats générés (`d-billet-v2a.jpg`, `d-billet-v2b.jpg`), B retenu : billet plus net, labels mieux posés. A avait du lettrage brouillé sur la bande rouge.
- Texte (overlay bas, 2 lignes) : `FAIS ÇA` / `AVANT D'INVESTIR` (orthographe : impératif « fais »)
- Luminosité 134, fichier final : `pourquoi-investir-2026-d-billet-v2-final.jpg`

### D v3 (retenue) — yeux ouverts, visage naturel, barbe désaturée
- Retour Nass sur v2 : yeux pas assez ouverts, visage un peu étrange, barbe bien trop orange
- Correctifs prompt (`d-billet-v3.txt`) : « eyes FULLY OPEN, no squinting », « muted strawberry-blond beard, NOT orange », « neutral white balance on skin », « no beautification »
- Références : `soft-smile-2026-10.jpg` + `neutral-2026-10.jpg` (yeux ouverts) plutôt que `smile` (yeux plissés par le sourire)
- 2 candidats : A retenu (naturel, barbe juste) ; B avait les labels sur le texte du billet et une barbe plus chaude
- Fichier final : `pourquoi-investir-2026-d-billet-v3-final.jpg`

### D v4 → v5 (retenue) — visage réel composité
- Retour Nass sur v3 : tête trop modifiée, reculer bien plus, enlever le « 100 euros » en bas à gauche
- v4 (2 essais, régénération et édition) : le modèle a encore redessiné le visage et gardé le « 100 EURO »
- v5 = pipeline visage réel : fond généré seul (`d-billet-bg.jpg`, patch PIL sur le coin bas-gauche → `d-billet-bg-clean.jpg`) + détourage chroma de la vraie photo (`d-cutout-tall.jpg`, depuis IMG_6678) + `composite.py` (visage à 29 % de la hauteur) + titre
- Fichier final : `pourquoi-investir-2026-d-billet-v5-final.jpg` ; variante sourire : `d-billet-v5-smile-final.jpg` (depuis IMG_6676)

### D v6 (retenue) — détourage studio
- Retour Nass sur v5 : « catastrophe, remets le visage bien » → le collage du selfie brut (lumière plate, petit) ne passe pas
- v6 : même pipeline mais détourage avec relighting studio identité verrouillée (`d-cutout-studio-soft.jpg`, `d-cutout-studio-smile.jpg`), visage à 47 % de la hauteur, buste sous le titre
- Fichiers finaux : `pourquoi-investir-2026-d-billet-v6-soft-final.jpg` (sourire discret, yeux ouverts) et `…-v6-smile-final.jpg` (sourire franc)

### D v7 (retenue) — billet v2b + détourage studio affiné
- Retour Nass sur v6 : remettre le billet de la v2b (plus riche, « 100 EURO » en bas à gauche conservé), améliorer un peu la tête
- Fond : v2b avec le personnage effacé par le modèle (`d-billet-bg-v2b.jpg`, prompt `…-removeman.txt`)
- Visage : détourage studio v2 (`d-cutout-studio-smile2b.jpg`, yeux ouverts, barbe atténuée), visage à 45 %, bas du buste hors cadre (`--bottom 1.15`)
- Fichier final : `pourquoi-investir-2026-d-billet-v7-final.jpg`

### D v8 — retour à la tête v6 + fond v2b nettoyé
- Retour Nass sur v7 : « la tête va pas », « deux fois écrit 100 en haut » (le rebouchage avait complété le « 100 » de la bande verte)
- Fond : `d-billet-bg-v2b-clean.jpg` (édition : « 100 » vert effacé, prompt `…-remove100.txt`)
- Visage : retour au détourage v6 `d-cutout-studio-smile.jpg` (validé « ça va »), visage 47 %
- Fichier final : `pourquoi-investir-2026-d-billet-v8-final.jpg`

### D v9 — t-shirt blanc, bouche fermée, léger recul
- Retour Nass sur v8 : t-shirt blanc, pas de sourire avec les dents, reculer un peu
- Visage : nouveau détourage studio depuis `soft-smile-tall` (`d-cutout-studio-soft-white.jpg`, prompt `…-studio-white.txt`), visage 41 %
- Titre avec contour noir (`--stroke 5`, nouvelle option d'overlay.py) pour rester lisible sur le t-shirt blanc
- Fichier final : `pourquoi-investir-2026-d-billet-v9-final.jpg`

### E — variante CryptoPunk 6995
- Punk officiel 24×24 (larvalabs, alpha) → `references/punk/punk6995-24.png`, upscale NEAREST ×40 → `punk6995-960.png`
- `composite.py` accepte maintenant un PNG transparent (`--pixel-art` pour l'échelle sans lissage)
- Fichier : `pourquoi-investir-2026-e-punk-final.jpg`

### D v10 — t-shirt blanc, épaules et bras, un peu plus près
- Retour Nass sur v9 : avancer un peu, montrer les épaules et les bras
- Détourage large (`d-cutout-studio-soft-white-wide.jpg`, prompt `…-studio-white-wide.txt` : « keep the full framing, both shoulders and upper arms »), visage 46 %, bas du buste hors cadre (`--bottom 1.25`)
- Fichier final : `pourquoi-investir-2026-d-billet-v10-final.jpg`

### D v11 — visage v9 greffé sur le buste v10
- Retour Nass sur v10 : la tête de la v9 est meilleure, remettre le même visage
- Greffe PIL : visage de `d-cutout-studio-soft-white.jpg` mis à l'échelle (0,699) sur le corps de `…-soft-white-wide.jpg`, masque ellipse fondu 14 px → `d-cutout-hybrid-white.jpg`
- Même cadrage que v10 (visage 46 %, épaules et bras visibles)
- Fichier final : `pourquoi-investir-2026-d-billet-v11-final.jpg`

### D v12 → v17 (retenue, remplace v11 dans « Nassin Crypto »)
- Retours Nass : tête v11 « ça va vraiment pas » ; pas la même émotion que les vidéos 2 et 3 ; t-shirt blanc ; pose de référence poing sous le menton, centrée, bras et coudes non coupés ; corps plus bas ; texte plus haut ; remettre le « 100 » vert du billet
- Détourage : `cutout-chin-white-waist-a.jpg` (prompt `cutout-chin-white-waist.txt`, **1:1 plan taille avec marges** : seule façon d'avoir épaules + coudes entiers), depuis `thinking-tall-2026-10.jpg`
- Composite : `--face-frac 0.34 --bottom 1.25`, titre `--y 540`, fond `d-billet-bg-v2b.jpg` (non nettoyé)
- Fichier final : `pourquoi-investir-2026-d-billet-v17-final.jpg`
