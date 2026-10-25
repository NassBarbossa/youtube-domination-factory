# « Les deux droites » : la DA des clips Convergence

Concept choisi par Nass le 2026-10-25, parmi trois (`{repo}/yt-shorts-montage/projects/recycles/STORYLINES.md`), puis validé sur le pilote 08 (v2). Tous les chiffres ci-dessous viennent de `examples/08-or-en-solde/make_comp.py`, qui les applique.

## L'idée

L'écran est coupé par deux droites qui reprennent les deux traits du V du logo :
- **verte `#0F8A5F` pour Nass**, cadre du haut ;
- **or `#C98A0B` pour Sadek**, cadre du bas.

Entre les deux, une bande de papier porte les sous-titres, les mots clés, le graphique ou l'écran de Nass. Celui qui parle prend la place : sa droite s'éloigne et son cadre grandit, l'autre reste visible et réagit. À la fin, les deux droites se rejoignent en V et glissent dans le V du vrai logo.

## Charte

| Élément | Valeur |
|---|---|
| Fond | papier `#F2EFE8` + grille `#E6E1D6` de 1 px tous les 96 px (décalée de −12 px) |
| Encre | `#0B0E11` |
| Droites | vert `#0F8A5F`, or `#C98A0B` ; trait de 12 px, bouts ronds, de x −30 à 1110 |
| Texte or | `#A07006`. L'or des droites n'a pas un contraste de 3:1 sur le papier |
| Rouge | `#C8323F`, seulement pour une baisse (−25 %) |
| Gris des étiquettes | `#565D6B` |
| Titres, sous-titres, mots clés | Inter Tight 800 (`InterTight-var.ttf`) |
| Étiquettes, dates, sources | IBM Plex Mono SemiBold, 32 à 34 px (le check refuse tout texte sous 28 px rendus) |
| Fichiers | polices dans `{repo}/shows/emission-live/assets/fonts/`, logo dans `{repo}/shows/emission-live/assets/logo/convergence-logo-clair.svg` |

**Zones :**
- on ne lit rien hors de la bande y 168 → 1330 ;
- rien d'important sous y ≈ 1670 ;
- rien d'important sur la colonne de boutons (x > 960, y > 900) ;
- jamais de texte sur un visage.

## États de la bande

Valeurs calées sur la mise en page « trois bandes » de l'EP.03 (crops caméra de 1028 × ~515). Avec d'autres crops, par exemple la « fullcam » (1028 × ~825), on recale échelles, droites et cibles des visages sur des snapshots : le visage doit garder la taille du pilote, et les cadres ne doivent montrer aucun trou.

Les ordonnées des droites sont données à gauche puis à droite. Pour chaque caméra : échelle, puis y voulu du visage à l'écran. `cap` est le y des sous-titres.

| État | Quand | Droite verte | Droite or | Nass | Sadek | cap | Contenu |
|---|---|---|---|---|---|---|---|
| H | accroche, image 0 | 430 → 470 | 900 → 840 | 1,30 / 250 | 1,60 / 1190 | 660 | accroche |
| CS | Sadek cite un chiffre | 8 → 36 (Nass replié) | 1000 → 940 | 1,30 / −260 | 1,60 / 1240 | 868 | graphique (70, 150, 940 × 560) |
| A | Sadek parle | 560 → 600 | 860 → 800 | 1,30 / 380 | 1,60 / 1166 | 705 | mots clés |
| B | Nass parle | 700 → 760 | 1010 → 930 | 1,50 / 420 | 1,30 / 1343 | 850 | mots clés |
| CN | Nass explique à l'écran | 540 → 580 | 1340 → 1300 | 1,30 / 330 | 1,30 / 1640 | 1218 | écran réel ou graphique (70, 615, 940 × 520) |
| CN+ | punch-in dans un long passage CN | idem | idem | 1,44 / 330 | 1,36 / 1640 | 1218 | idem |
| B+ | punch-in quand Nass parle seul, sans écran | comme B | comme B | B + 0,10 | B + 0,06 | 850 | mots clés |

**Un seul orateur sans écran** (pas d'autre état possible) : alterner B et B+ à chaque couture. Chaque coupe tombe ainsi dans un mouvement ; enchaîner B → B, c'est une coupe sèche.

**Caméras :**
- Elles sont pré-agrandies ×1,45 (`prescale`) en lanczos. L'échelle CSS vaut échelle / 1,45.
- Ne pas dépasser 1,6 : au-delà, l'image devient floue.
- Recentrage sur le visage du morceau (`face_track.py`), avec `cam_tf()` : le cadre de Nass couvre toujours jusqu'à la droite verte, celui de Sadek depuis la droite or. Jamais de trou de papier dans un cadre.
- En CN+, Sadek bouge aussi (1,30 → 1,36). Ainsi sa propre coupe tombe en plein mouvement, pas en image fixe.

## Mouvement

- **Chaque coupe de parole tombe au milieu d'une bascule** de 0,6 s en `power3.inOut`. La bascule commence à couture − 0,3 s. Droites, découpes (`clip-path`), caméras, graphique et sous-titres bougent ensemble.
- Le graphique s'ouvre 0,30 s avant le mot du chiffre (état CS ou CN).
- Au plus un plan toutes les ~0,8 s. Deux coutures plus proches : fusionner les morceaux ou ne faire qu'une bascule.
- Un morceau long (plus de 8 s) tient par les événements du graphique ou de l'écran et par une alternance CN / CN+, pas par des coupes en plus.
- Le flou de bougé est actif au rendu (`data-motion-blur="on"` sur la racine) et coupé sur `#capwrap`.

## Accroche (état H)

- Deux lignes en Inter Tight 800 à 104 px (`#hook`, top 532).
- Le mot fort est dans la couleur de celui qui porte l'idée : vert pour Nass, or texte pour Sadek. Dans le pilote, c'est Sadek qui lance « l'or est en solde ».
- En dessous, éventuellement, une ligne en Plex Mono 32 px avec un chiffre réel et daté (« −25 % DEPUIS SON RECORD »).
- La ligne Plex Mono ne sert que **si le passage a un chiffre vérifiable**. Sans chiffre, pas de ligne ; jamais de chiffre ajouté pour remplir.
- Elle vient des mots du passage.
- Elle s'efface au début de la première bascule (centre de la bascule − 0,32 s) : flou de 8 px, 0,2 s, `power2.in`.
- Les sous-titres ne commencent qu'à centre + 0,32 s.

## Sous-titres (`compositions/captions.html`)

- **Groupes :** 3 mots et 17 caractères au plus. Un nouveau groupe commence après une pause de plus de 0,15 s. Inter Tight 800 à 70 px, marges latérales de 130 px.
- **Texte :** les apostrophes sont recollées (« l » + « 'or » → « l'or »). La table `FIX` corrige ce que la transcription a mal entendu, surtout les chiffres et les sigles : « 4080 » → « 4 180 », « th » → « ATH », « sols » → « soldes ». Chaque chiffre et chaque nom des sous-titres est vérifié à l'écoute.
- **Mot actif :** souligné de 9 px à la couleur de celui qui parle, vert pour Nass, or pour Sadek. Entrée en `clamp(écart − 0,01 ; 0,03 ; 0,12)` s, sortie en 0,06 s au mot suivant.
- **Suivi de la bande :** tous les groupes sont dans `#capwrap`, dont le y suit `cap` à chaque bascule.
- **Pas de sous-titres :** sous l'accroche, et quand un mot clé porte déjà la phrase (« le prix / le moment » dans le pilote).

## Mots clés

- Uniquement les mots du passage, en Inter Tight 800 à 96 px.
- Couleur de celui qui parle : vert, ou or texte `#A07006`.
- Entrée en `expo.out` 0,45 à 0,5 s (échelle 1,25 → 1). Sortie en 0,2 s avec un flou de 8 px.
- Deux mots clés à l'écran en même temps sont empilés, jamais superposés. Ils suivent la bande pendant une bascule (y + 155 dans le pilote).
- Un mot de chute (INVESTISSEUR) peut remplacer le dernier sous-titre : 104 px, encre, soulignement vert.

## Écran réel ou graphique redessiné

| Situation | Ce qu'on montre |
|---|---|
| **Nass montre son écran** : il dit « là », « ici », « ce niveau-là », ou dessine sur TradingView | **son écran réel** (`build_screen.py`) dans `#screen`, boîte fixe (34, 598, 1012 × 552) pendant les états CN / CN+. Fondu d'entrée de 0,25 s, fondu de sortie de 0,18 s |
| Un chiffre est dit sans écran (Sadek, ou Nass sans partage) | graphique redessiné dans la boîte de l'état (CS : 70, 150, 940 × 560 ; CN : 70, 615, 940 × 520). Données réelles (`assets/data/*.json`), points datés, ligne « SOURCE : … » à l'écran |
| Aucune donnée vérifiable | ni graphique ni chiffre à l'écran. Le chiffre reste dans la voix et les sous-titres |

**Graphique redessiné :**
- courbe or de 6 px, tracée en 0,9 s (`stroke-dashoffset`) ;
- points à l'encre (r 11) ;
- valeurs en 60 px, dates en Plex Mono 34 px gris ;
- baisse en rouge 76 px.

**Chiffres :** à l'écran, la valeur réelle et datée (−25 %). La voix garde ce qui a été dit (« presque 30 % ») : on ne reformule jamais une parole.

## Fin

| À partir de | Ce qui se passe |
|---|---|
| fin de la voix (`END_T`) | les cadres s'effacent en 0,45 s ; les deux droites forment un grand V en 0,7 s (centre x 540, haut 520, pointe 820, demi-largeur 150, trait de 46) |
| `END_T` + 0,68 | un point d'encre apparaît à la pointe |
| `END_T` + 1,1 | les droites glissent sur le V du logo en 0,5 s |
| `END_T` + 1,42 | le reste du logo apparaît (le `<path>` du SVG officiel, sans ses `<line>` : le V, ce sont nos droites) |
| `END_T` + 1,75 | CTA « Épisode N complet sur la chaîne » (Inter Tight 700, 46 px, top 1068) |
| `END_T` + 4,15 | durée totale `D` |

**Pas de disclaimer à l'image.** Il va dans la légende de publication.

## Son

- **Voix :** −14 LUFS, crête vraie −1,5 dBTP (`build_media.py`). **Pas de musique.**
- **4 à 5 SFX par clip,** pris dans le catalogue de `/media-use` (`audio/assets/sfx/`). Chacun est tronqué, normalisé à −1 dBFS en crête, avec un fondu de sortie de 80 ms. Puis on règle son volume :

| Son | Moment | Volume |
|---|---|---|
| `whoosh-short` (0,55 s) | 0,20 s avant l'ouverture du graphique | 0,34 |
| whoosh grave : `whoosh-short` en `asetrate=48000*0.86` (0,62 s) | la grande bascule entre les deux voix | 0,30 |
| `pop` (0,40 s) | le chiffre clé | 0,30 |
| `impact-bass-1` | `END_T` + 0,70, quand les droites touchent le logo | 0,40 |

- Sans graphique : le `whoosh-short` va sur la première bascule. Sans changement de voix : un seul whoosh. Le pop reste sur le mot clé le plus fort.
- Pas de son sur chaque bascule ni sur chaque mot clé. Deux whooshs identiques à la suite s'entendent : on utilise deux prises.

## Interdits

Fond sombre, halo, néon, dégradé, carte en verre, pastille, icône générique, logo collé dans un coin, B-roll, avatar ou voix IA, musique, coupe sèche, secousse d'une image, texte qui bouge pendant qu'on le lit, chiffre non sourcé, étiquettes du live gardées dans le cadre (NASS / SADEK / LIVE gravés, bordures).
