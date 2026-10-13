# Guide « Motion graphics with Claude Code » (Damiano Caudullo, @damianodesu) — adapté à Nass

Source : PDF « Motion Graphics with Claude Code » fourni par Nass le 2026-10-08 (14 prompts testés, même outil que nous : HyperFrames + Claude Code). Seul ce qui sert nos Shorts est repris ici.

## Règles Nass (priment sur le guide)
- **9:16 vertical, 1080×1920, rendu à 60 i/s.**
- **Jamais de musique, mais des sound effects** sur les animations (voir « Son »).
- **Rythme** : transitions fluides d'environ 0,6 s ; 1 plan par ~0,8 s max.
- Charte, règles de fond et chiffres réels : voir `_shared/cadre-nass.md`.

## 1. Principe : un prompt de base + un bloc STYLE interchangeable
Le prompt de base décrit le contenu (script, durée, format) ; le bloc STYLE, collé en dessous, décrit le look. On change de look sans toucher au contenu. **Notre bloc par défaut (validé par Nass le 2026-10-08 : « le même branding que les slides » + Editorial Grain) :**

```
STYLE: Nass Riviera (Editorial Grain) — mêmes tokens que les slides (yt-script/references/slide-template.html)
- It should feel like a printed dark editorial page, not a glossy screen.
- Background: near-black #0B0B0B (--bg) with visible animated film grain over everything
  (SVG feTurbulence noise layer, ~10-12% opacity, seed changes every 2-3 frames, driven by the
  timeline so it stays deterministic) and soft glows rgba(219,177,127,.12) / rgba(100,133,150,.12).
- Fonts: Archivo Black (--font-display, assets/fonts/ArchivoBlack-Regular.ttf) for headlines and
  labels, large, all caps; Public Sans 400/600/800 (--font-body, assets/fonts/PublicSans-var.ttf)
  for sentences. Small labels in Public Sans 600, uppercase, letter-spaced. No serif.
- Colours (slide tokens): sand #DBB17F primary accent (titles, dividers, key word on each screen),
  sand-light #F3D6A8, sand-dark #9C7748, cream #F4EFE7 text and card fill, punk blue #648596 /
  #4F6C7B for data and "online/tech" highlights, greys #3B3A37 / #9A968D, text-secondary
  rgba(244,239,231,.78), text-muted rgba(244,239,231,.45).
- Cards: cream fill, 3px solid #0B0B0B border, hard 8px 8px offset shadow in sand-dark #9C7748
  (no blur) — exactly like the slides' .card.
- Editorial details: cut-out paper shapes behind key words, slightly rotated (1 to 3 degrees),
  thin sand rules, small page / step numbers in the corners (e.g. 01 / 03).
- Signature: the pixel punk @punk6995 (assets/punk6995.jpg, image-rendering: pixelated) on the
  recap and the end card.
- Motion: hook and recap in Kinetic Type (words slam in one by one, power4.out, 0.25-0.4 s).
  Explanations unhurried and a bit imperfect: staggered timings that are not perfectly even,
  gentle slides and wipes, Rise / Blur-in; bounces only on the hook. Easing reference:
  cubic-bezier(0.16, 1, 0.3, 1) (--ease-out-expo).
- Keep all text inside the middle 80% of the width; nothing important in the bottom 250 px or the
  right-hand column.
- No music. Sound effects on the animations (see sound rule).
- Render with --crf 23 (grain makes big files).
```

## 2. Les mouvements nommés (vocabulaire commun script ↔ montage)
À utiliser tels quels dans les lignes `VISUEL` des scripts. Les 10 du guide, plus **Kinetic Type** (repris du bloc STYLE ci-dessus).

| Mouvement | Effet |
|---|---|
| **Kinetic Type** | les mots claquent un par un (hook et récap) |
| **Rise** | apparaît en fondu en montant un peu |
| **Pop** | grossit depuis petit avec un léger dépassement |
| **Count-up** | un nombre défile jusqu'à sa valeur (toute statistique) |
| **Checklist** | des lignes reçoivent une coche une par une |
| **Typewriter** | le texte se tape tout seul |
| **Slide-in** | arrive par le côté |
| **Blur-in** | passe du flou au net |
| **Punch-in** | toute l'image zoome vite : pour la phrase à retenir |
| **Reframe** | la vidéo rétrécit dans une carte et autre chose apparaît |
| **Bar fill** | une barre de progression se remplit |

## 3. Short 100 % texte (cas principal, adapté du prompt 08)
```
Make a [N]-second vertical video (1080x1920, 60 fps) with HyperFrames in this folder, made only of
animated text and simple icons. No footage. No music.
Script: [lignes ÉCRAN du script validé, dans l'ordre, avec leurs timecodes]
Use my exact words. Don't rewrite or shorten the script. Show one sentence per screen, big enough
to read on a phone. If a sentence is long, wrap it over two or three lines on the same screen.
Each screen stays up long enough to read. Keep all text inside the middle 80% of the width.
[STYLE: Nass Riviera]
```

## 4. Face cam IA : graphismes par-dessus la vidéo (adapté du prompt 11)
1. Analyser la vidéo d'abord : `npx hyperframes transcribe`, vérifier les timings des mots contre l'audio (la transcription peut être décalée jusqu'à ~1 s).
2. Ne jamais modifier la vidéo (taille, fps, audio, coupes) : on ajoute seulement par-dessus.
3. À chaque moment important, une animation faite pour ce qui est dit : un nombre → Count-up, une liste → Checklist, un avant/après → comparaison. Elle démarre sur le mot exact.
4. Un seul style sur toute la vidéo.
5. **Rien dans les 3 premières secondes** (c'est le hook).
6. Rien sur le visage, rien dans le tiers bas (sous-titres), rien dans les 10 % gauche et droite.

## 5. Méthode de retouche
- D'abord une **base** qui plaît, puis on change **un seul moment à la fois** (« Keep everything else the same and render again »).
- Désigner un moment **par la phrase** (« quand le texte dit FTX… »), pas par la seconde.
- Donner le vrai matériel (captures réelles, chiffres réels) et dire exactement quand le montrer.

## 6. Son (sans musique, avec sound effects)
**Règle Nass : pas de musique, mais des sound effects.** Le guide d'origine limite aux petits clics sans whoosh ; chez Nass, les whoosh / impacts de transition sont permis, tant que c'est équilibré et normalisé. Repères du guide : un *tick* quand un élément de liste / une coche apparaît, un *counter* pendant qu'un nombre défile, un *chime* sur la dernière carte. Environ **20 dB sous la voix** quand il y a une voix ; sans voix, rester discret (pics vers −20 dBFS). Sons générés en code (pas de licence) ou Freesound CC0 / Kenney.

## 7. Export et dépannage
- Rendu par défaut : `--fps 60`. Autres formats : `--resolution 4k`, `--format mov` (ProRes), `--format png-sequence`.
- Fichier trop lourd (grain, texture) : re-rendre avec `--crf 23`. **Testé sur le Short wallets/02 (grain)** : `--crf 28` = 1,6 Mo mais trop compressé, `--crf 20` = 70 Mo ; le bon compromis = rendu `--crf 20` puis ré-encodage ffmpeg `-c:v libx264 -preset slow -crf 25 -tune grain -movflags +faststart` (≈ 20 Mo pour 22 s).
- Export transparent pour Premiere / After Effects : retirer le fond, et utiliser une **carte pleine** (le verre dépoli perd son flou sans rien derrière).
- Police de remplacement à l'écran : mettre le fichier de police dans `assets/fonts` et le citer.
- Texte coupé sur téléphone : « garder tout le texte dans les 80 % centraux ».
- Une carte cache les sous-titres : « monter toutes les cartes au-dessus de la zone des sous-titres ».
- Une carte arrive un peu tôt / tard : la caler sur le mot (« quand le texte dit… »).
