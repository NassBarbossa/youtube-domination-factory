# Convergence — Assets

Émission live hebdomadaire · Marchés · Or × Crypto · replay sur YouTube.
Référence visuelle complète : `brand-board-convergence.html` (à ouvrir dans le navigateur).

## logo/

| Fichier | Usage |
|---|---|
| `convergence-logo-clair.svg` / `.png` | Logo principal, sur fond clair. Fond transparent, 3000 px de large. |
| `convergence-logo-sombre.svg` / `.png` | Sur fond sombre (vidéo, photo). Or et vert plus lumineux. |
| `convergence-logo-mono-noir.svg` / `.png` | Une seule couleur, noir (impression, tampon). |
| `convergence-logo-mono-blanc.svg` / `.png` | Une seule couleur, blanc. |
| `convergence-icone-carre.svg` / `-1024.png` | Icône V, carré arrondi (favicon, app, réseaux). |
| `convergence-icone-rond.svg` / `-800.png` | Icône V ronde (avatar). |

Les SVG sont en vrais tracés : le texte est converti, ils s'ouvrent partout (Figma, Illustrator, Canva) sans police installée.

## youtube/

| Fichier | Usage |
|---|---|
| `avatar-800.png` | Photo de profil de la chaîne. |
| `banniere-2560x1440.png` | Bannière de chaîne. Logo et signature dans la zone visible partout (1546 × 423). |
| `miniature.html` | **Gabarit de miniature** modifiable (voir plus bas). |
| `miniature-exemple-1280x720.png` | Exemple rendu. |
| `miniatures/convergence-epNN-1280x720.jpg` | Miniatures publiées, une par épisode (ép. 01 validée le 2026-10-27, ép. 03 publiée le 2026-10-20). Produites avec `yt-miniature/scripts/compose_vs_brand.py` (face à face) ou `compose_podcast.py` (bustes). |

### Faire une miniature
1. Mettre les photos détourées (PNG transparent) dans `youtube/photos/`.
2. Ouvrir dans le navigateur :
   `miniature.html?l1=Or vs&l2=Bitcoin&chiffre1=+6 %&chiffre2=−2 %&ep=01&photo1=photos/cohost.png&photo2=photos/nass.png`
3. Capture en 1280 × 720 (ou demander à Claude de la rendre en PNG).
   Les chiffres qui commencent par « − » passent automatiquement en rouge, les autres en vert.

## obs/ — écrans du live (1920 × 1080)

À ajouter dans OBS en **Source navigateur**, en cochant « Fichier local », taille 1920 × 1080.
Les polices sont incluses dans `fonts/`, donc tout marche hors ligne. Garder le dossier `assets/` entier.

| Fichier | Rôle | Paramètres d'URL |
|---|---|---|
| `1-attente.html` | Avant le live : logo animé + compte à rebours | `?min=5` |
| `2-live.html` | Pendant le live : **fond percé de 2 fenêtres transparentes**, à placer au-dessus des caméras | `?ep=01&cohost=Prénom&nass=Nass` |
| `3-sujet.html` | Carte entre deux tendances | `?n=2&total=5&titre=L'or casse son record.&mot=or&tags=OR,BANQUES CENTRALES,BTC` |
| `4-fin.html` | Fin du live | — |

**Placement des caméras sous `2-live.html` :**
- Caméra co-host : x = 50, y = 108, 702 × 848 (cadre or)
- Caméra Nass : x = 784, y = 108, 702 × 848 (cadre vert)

**Bandeau de cours** (en bas de chaque écran) : les valeurs sont des **exemples**. À mettre à jour chaque semaine dans `obs/convergence.js` (tableau `COURS`), ou via l'URL :
`?cours=OR:4 321 $:+0,4 %|BTC:84 375 $:−2,4 %`

Le panneau « Cette semaine » de `2-live.html` se modifie directement dans le fichier.

Les `.png` du dossier sont des aperçus. `2-live.png` garde la transparence des fenêtres caméra.

## video/

| Fichier | Usage |
|---|---|
| `convergence-intro-clair-1920x1080.mp4` (+ `-1080x1920`, `-1080x1080`) | Intro de 6 s sur fond papier, en 16:9, 9:16 et 1:1 (le V se trace, le point s'allume, les lettres s'écartent, la signature apparaît). |
| `convergence-intro-transparent.mov` | La même en ProRes 4444 **avec transparence**, à incruster sur n'importe quel fond (OBS, Premiere, DaVinci, CapCut). |
| `intro.html` | Source de l'animation (`?t=1.2` pour figer un instant, `?bg=dark` pour la version sombre). |

## riverside/

Pack prêt pour Riverside (studio, Media Board, éditeur) : voir `riverside/README.md`.

## fonts/

Inter Tight (titres, logo) et IBM Plex Mono (chiffres). Licence SIL Open Font, utilisation libre.
`build_logo.py` régénère les SVG du logo.

## Couleurs

| Nom | Hex | Usage |
|---|---|---|
| Papier | #F2EFE8 | fond |
| Carte | #FBFAF6 | panneaux |
| Encre | #0B0E11 | texte, logo, bandeau de cours |
| Or | #C98A0B (#E2A93B sur fond sombre) | marchés traditionnels · or · co-host |
| Vert | #0F8A5F (#2BB37C sur fond sombre) | crypto · hausses · Nass |
| Rouge | #C8323F | baisses · badge LIVE uniquement |

## OBS — scènes déjà créées

Collection de scènes **« Convergence »** (menu Collection de scènes), créée par `obs/setup_obs.py` :

| Scène | Contenu |
|---|---|
| 1 · Attente | écran animé + compte à rebours 5 min (`?min=` dans l'URL de la source) |
| 2 · Intro | vidéo du V (6 s), se relance à chaque passage sur la scène |
| 3 · Live | fond papier → caméra co-host (VDO.Ninja) + caméra Nass → habillage percé par-dessus → micro Yeti X |
| 4 · Sujet | carte de tendance : modifier l'URL de la source « Carte sujet » (`?n=2&total=5&titre=…&mot=…&tags=…`) |
| 5 · Fin | écran de fin |

**Co-host à distance (gratuit, VDO.Ninja)** : il ouvre le lien `https://vdo.ninja/?push=convergence-6708c2&webcam&quality=1` dans Chrome, autorise caméra + micro, et sa vidéo arrive dans la source « Caméra co-host (VDO.Ninja) ». Son son passe par OBS (audio de la source navigateur).

**Caméra de Nass** : source « Caméra Nass » → double-clic → choisir le périphérique vidéo.

Le canvas OBS est en 2560 × 1440 : les écrans (dessinés en 1920 × 1080) sont mis à l'échelle automatiquement.

## Cours en direct (bandeau + panneau « Cette semaine »)

Avant le live : double-clic sur **`Lancer les cours en direct.bat`** et laisser la fenêtre ouverte.
Toutes les 60 s, le script récupère les cours (Yahoo Finance) et écrit `obs/cours.js` ; les écrans OBS le relisent chaque minute.
- Bandeau : prix + variation du jour (OR, ARGENT, S&P 500, CAC 40, EUR/USD, PÉTROLE, BTC, ETH, SOL).
- Panneau « Cette semaine » : variation sur 5 séances (OR, S&P 500, BTC, SOL).
- Changer la liste des actifs : tableaux `ACTIFS` et `SEMAINE` en haut de `obs/cours_live.py` (symboles Yahoo).
Sans le script, le bandeau garde les derniers cours enregistrés.

## Sujets de l'épisode

Remplir **`obs/sujets.js`** avant chaque live (un bloc par sujet, dans l'ordre).
Dans OBS : scène « 4 · Sujet 1 » = 1er sujet, « 4 · Sujet 2 » = 2e… (6 emplacements, les vides ne servent pas).
- `type: "TENDANCE"` → « TENDANCE N°x » numéroté automatiquement.
- Tout autre type s'affiche tel quel : « LE TRADE DE LA SEMAINE », « LA QUESTION DU CHAT »…
- `style: "trade"` + `trade: {actif, sens, entree, objectif, invalidation}` → carte spéciale avec les niveaux et la mention « Ceci n'est pas un conseil en investissement ».
Après modification, la carte se met à jour à chaque passage sur la scène.
