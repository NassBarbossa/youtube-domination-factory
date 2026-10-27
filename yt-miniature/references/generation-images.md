# Génération et édition d'images — API Images d'OpenRouter

Chargé par `yt-miniature/SKILL.md` dès qu'une miniature demande une image générée (portrait, fond, scène). Pas de génération en mode autonome (pipeline) : on livre le concept, Nass déclenche. Méthode révisée le 20 octobre 2026 après la comparaison sourcée `references/veille-visages-ia-2026-10-20.md` (OpenAI, Google, guides praticiens) : ce fichier en est l'application.

`{repo}` = racine du dépôt youtube-domination-factory (Mac : `~/youtube-domination-factory` · Windows : `C:\Users\User\youtube-domination-factory`) ; les chemins relatifs partent de là.

## 1. Les six règles

1. **Une ancre par personne, éditée, jamais régénérée.** Un portrait validé par Nass sert de base à tous les épisodes suivants. On l'envoie comme image 1 avec « change only X, keep everything else exactly the same » (OpenAI : « identify what should change and what must stay the same » ; Google : « Keep everything else in the image exactly the same »). Régénérer de zéro redonne un nouveau visage à chaque tir.
2. **Une variable par appel.** Tenue, puis fond, puis angle : jamais les quatre ensemble. La sortie validée devient l'entrée suivante ; la liste de ce qui ne bouge pas est répétée à chaque tour (« repeated edits can still change details you intended to preserve »).
3. **Deux tirages maximum**, et sur la scène (fond, cadrage), pas sur le visage. `generate.py` refuse `--n` au-delà de 2.
4. **Brouillon pas cher, final en qualité haute.** gpt-image-2 en `quality` par défaut coûte moins d'un centime (0,004 $ mesuré pour un fond 16:9 le 20 oct.) : on valide la composition avec ça, et on ne passe en `high` (≈ 0,22 $ en 3:4) que pour le tirage final.
5. **Vérifier à taille réelle avant de montrer.** `compare_ref.py` met la sortie à côté de la référence ; un trait protégé qui bouge (yeux, nez, mâchoire, barbe, cheveux) = tirage rejeté, sans le montrer. Puis `check.py` pour le test à 256 px.
6. **Assembler, puis harmoniser.** Fond et corps d'abord, visage validé en dernier ; un seul étalonnage sur tout (`--grade`), ombres de contact, lumière dans le même sens. Ce qui trahit un montage, c'est la lumière, pas les bords.

## 2. L'API

- Endpoint : `POST https://openrouter.ai/api/v1/images` (JSON), clé `OPENROUTER_API_KEY` dans le `.env` à la racine.
- Corps : `model`, `prompt` (anglais), `aspect_ratio`, `n`, `input_references` (liste d'objets `{"type":"image_url","image_url":{"url":"data:image/jpeg;base64,…"}}`, l'ordre compte : la première est « image 1 »), puis selon le modèle `quality` (OpenAI), `resolution` (Google, Sourceful), `background`, `output_format`.
- Réponse : `data[0].b64_json` (ou `url`), coût réel dans `usage.cost`. Facturation tout ou rien : une génération échouée ou annulée n'est pas facturée ; un solde sous 1 $ renvoie 402.
- Pas de masque sur cette API : l'édition passe par l'image 1 + le prompt « change only X ». Si une zone doit rester identique au pixel, on la recompose en PIL (`compose_podcast.py`, `composite.py`), on ne compte pas sur le prompt.
- Paramètres et limites réels (lus sur `/api/v1/images/models` le 20 oct. 2026) :

| Modèle | Rôle | Références max | Paramètres | Prix |
|---|---|---|---|---|
| `openai/gpt-image-2` (défaut) | portraits ancre de Nass, éditions d'ancre, fonds | 16 | `aspect_ratio`, `quality` auto/low/medium/high | au token : ≈ 0,22-0,23 $ un portrait 3:4 high, ≈ 0,004 $ un fond 16:9 auto |
| `google/gemini-3.1-flash-image` (Nano Banana 2) | portraits ancre de Sadek (jugé plus ressemblant pour lui le 20 oct.), éditions | 14 | `aspect_ratio`, `resolution` 512/1K/2K/4K | ≈ 0,07 $ l'image 1K |
| `google/gemini-nano-banana-2.1` | à tester : même famille, moitié prix au token, 14 références | 14 | `resolution` 1K/2K/4K | ≈ 0,03-0,04 $ l'image 1K (estimé) |
| `openai/gpt-image-2.5-flare` / `-sunburst` | à tester : `background: transparent` (plus de fond vert à détourer), `quality` jusqu'à max | 16 | comme gpt-image-2 + `background` | même tarif au token que gpt-image-2 |
| `sourceful/riverflow-v2.5-pro` | fonds, `background: transparent` ; aucun test indépendant sur le visage | 10 | `resolution`, `output_format`, `background` | 0,13 $ fixe (0,15 en 2K) |

`gpt-image-2` ne supporte pas `background: transparent` (seulement auto/opaque) : avec lui, les détourages se font sur fond chroma vert #00FF00 et `compose_podcast.py` ou `composite.py` fait la clé.

## 3. Les scripts

| Script | Rôle |
|---|---|
| `scripts/generate.py` | appel API : `--prompt-file` + `--ref` (génération) ou `--base` + `--edit` (édition d'ancre, prompt composé automatiquement avec le verrou d'identité) ; `--n` ≤ 2 ; `--dry-run` ; journal `outputs/generation-log.jsonl` |
| `scripts/compare_ref.py` | sortie à côté de la ou des références, à taille réelle, avant toute présentation |
| `scripts/compose_podcast.py` | deux bustes + texte central (Convergence) : `--lead`, `--grade`, ombres de contact, `--lines`, `--ep` |
| `scripts/composite.py` | une personne sur un fond (vidéos solo), mise à l'échelle par la hauteur du visage |
| `scripts/overlay.py`, `banner.py`, `pfp.py`, `bg_cream.py`, `check.py` | texte, bannière, avatar, fond crème à grille, contrôle 256 px |

Dépendances : Pillow et numpy (`scripts/requirements.txt`) ; `generate.py` n'utilise que la stdlib.

## 4. Références et ancres

**Photos d'identité** (`references/nass/`, 19 fichiers `*-2026-10.jpg`, ne pas modifier) : pour un portrait ancre, envoyer **2 ou 3** photos, pas plus (fidélité maximale à 6 références ou moins, et moins c'est mieux) : `neutral-2-2026-10.jpg` (frontale), `neutral-2026-10.jpg`, et l'expression visée (`thinking-`, `smirk-`, `serious`…). Ne pas envoyer `recent-2026-10.jpg` (piscine, plein soleil, main devant, contre-plongée : la contre-plongée exagère la mâchoire). Une photo dédiée serait mieux encore : face, lumière uniforme, fond uni, expression neutre, 1024 px ou plus, visage sur au moins un tiers du cadre.

**Sadek** (`references/sadek/`) : 5 photos réelles (`closeup-red`, `profile-denim`, `side-face`, `studio-black-wide`, `studio-leather-full`) et 5 modèles d'expression générés (`*-gen-2026-10.jpg`). Pour une ancre : `closeup-red` + `profile-denim` + `side-face`.

**Punk** (`references/punk/`) : `punk6995-960.png` comme référence, `punk6995-24.png` agrandi en NEAREST pour l'incrustation. Ne jamais laisser un modèle inventer un autre punk.

**Ancres validées** (à éditer, jamais à régénérer ; ajouter une ligne quand Nass en valide une nouvelle) :

| Personne | Fichier | Validée | Notes |
|---|---|---|---|
| Nass | `outputs/convergence-ep03-cutout-nass-v3-2.jpg` | 2026-10-20 (ép. 03) | gpt-image-2 high, 3:4, t-shirt anthracite, corps tourné vers la droite, sérieux calme, fond chroma vert |
| Sadek | `outputs/convergence-ep03-cutout-sadek-nb2-1.jpg` | 2026-10-20 (ép. 03) | Nano Banana 2, 3:4, t-shirt blanc + surchemise marine, lunettes transparentes, corps tourné vers la gauche |
| Nass (conversation) | `outputs/convergence-ep01-talk-nass2.jpg` | 2026-10-27 (ép. 01) | gpt-image-2 high, 3:4, t-shirt noir, épaules face caméra, tête tournée à gauche vers son interlocuteur, pas convaincu ; pour les miniatures « les deux se regardent » |
| Nass (ébloui, caméra) | `outputs/convergence-ep04-nass-dazzled-3.jpg` | 2026-10-27 (ép. 04) | gpt-image-2 high, édition de l'ancre ép. 03 : regard caméra, yeux grands ouverts, bouche fermée sans dents ; pupilles source (565,352) et (725,350), iris 26 px, pour `compose_solo_brand.py --pupils` |
| Sadek (conversation) | `outputs/convergence-ep01-talk-sadek.jpg` | 2026-10-27 (ép. 01) | Nano Banana 2 2K, 3:4, t-shirt noir + chaîne, penché vers la droite, doigt pointé, demi-sourire ; mène la miniature |

Pour l'autre position (Nass à droite), on **retourne l'ancre en miroir** dans `compose_podcast.py` (`--flip-left/--flip-right`), on ne régénère pas un portrait tourné de l'autre côté.

Règles Convergence validées le 2026-10-27 : les deux se regardent, jamais la caméra ; Sadek mène (posé devant, ou au moins à égalité) ; assemblage `compose_vs_brand.py` (papier crème à grille ou studio sombre, bloc or, pastille logo + ÉP.). Nass a choisi le studio sombre pour l'ép. 01.

## 5. Les quatre opérations

### A. Portrait ancre (une fois par personne, puis réutilisé)

`generate.py --model openai/gpt-image-2 --prompt-file … --ref <2-3 photos> --aspect 3:4 --quality high --out outputs/<personne>-anchor-<date>.jpg`

Prompt (celui qui a donné l'ancre de Nass, à adapter pour une autre personne) :

```
The attached photos all show the SAME specific real man (N). Reproduce HIS exact face with maximum fidelity: completely shaved head, round-ish full face, short ginger-blond beard and moustache, fair skin with freckles, blue-grey eyes, straight nose, strong jaw. Same eye shape, same nose, same beard colour as the photos. Waist-up studio photo of N for a podcast YouTube thumbnail: body turned about 30 degrees toward the RIGHT side of the frame, face toward the camera, calm serious expression, mouth closed, slight frown, direct eye contact, eyes open. Plain dark charcoal crewneck t-shirt. No microphone, no props, nothing in front of him. Both arms and elbows fully inside the frame with clear margin, hands relaxed, forearms resting on the table edge at the very bottom. Lighting: warm key light from the front-right, cool rim light on the shoulders. Background: SOLID FLAT CHROMA GREEN #00FF00, nothing else. Photorealistic, sharp, 85mm look, no text.
```

Toujours : description écrite des traits (le modèle s'y accroche), caméra fixe (« 85mm, eye-level »), bras et coudes entiers avec marge, fond chroma vert, pas de micro ni d'accessoire. Vérifier avec `compare_ref.py`, faire valider par Nass, puis inscrire l'ancre dans le tableau ci-dessus.

### B. Édition d'ancre (tenue, expression, angle léger, fond)

`generate.py --base outputs/convergence-ep03-cutout-nass-v3-2.jpg --edit "replace the charcoal t-shirt with a plain white crewneck t-shirt under an open dark navy overshirt" --keep "the solid green background" --out outputs/<slug>-nass-outfit.jpg`

Le script compose : « Image 1 is the approved portrait… Edit image 1: <changement>. Change only that. Keep everything else exactly the same as image 1: the face, facial features, skin texture, expression, hairstyle, head angle, body proportions, framing and lighting must remain identical… ». Un changement par appel. Pour enchaîner (tenue puis expression), la sortie validée devient le nouveau `--base`. Modèle : celui qui a produit l'ancre (gpt-image-2 pour Nass, Nano Banana 2 pour Sadek).

Une expression différente est une édition d'ancre (« change the expression to a sceptical look with one eyebrow slightly raised, mouth closed »), pas un nouveau portrait.

### C. Fond (sans personne)

`generate.py --prompt-file … --aspect 16:9 --out outputs/<slug>-bg-draft.jpg` en qualité par défaut (≈ 0,004 $) pour valider l'idée, puis le même prompt en `--quality high` pour le final si besoin. Prompt : lieu, lumière, profondeur de champ, « no people, no text », zone centrale plus sombre ou plus calme là où ira le texte. Deux tirages maximum. Fonds existants réutilisables : `outputs/convergence-ep03-bg-dark.jpg`, `outputs/convergence-ep01-bg-loft.jpg`, fond crème PIL via `bg_cream.py`.

Éviter le style IA générique que les spectateurs repèrent (lueurs vert et ambre, sujets uniformément éclairés, ciels dramatiques) : préférer un vrai lieu plausible, une lumière avec une direction, des matières.

### D. Scène complète (une personne, gros plan)

Réservée au cas où le visage occupe au moins 45 % du cadre (ex. « J'ai tout perdu ? » version H) : la fidélité se perd quand le visage est petit (arXiv 2609.04151). Références : 2-3 photos d'identité + la référence de composition passée comme image de pose. Pour deux personnes, on ne génère pas la scène : on assemble deux ancres avec `compose_podcast.py`.

## 6. Assemblage et harmonisation

Podcast : `compose_podcast.py bg.jpg gauche.jpg droite.jpg out.jpg --lines "…|…|…" --ep "ÉP. NN" --accent gold --theme dark --left-accent green --lead left --grade warm --drop 0.18 --scale 1.0 --lx 0.11 --rx 0.89`.

- `--lead` : la personne qui porte l'épisode est plus grande et un peu plus éclairée ; deux bustes identiques et symétriques sont l'erreur la plus courante des miniatures de podcast. Recadrer serré plutôt qu'un plan large.
- `--grade warm|cool` : un seul étalonnage sur tout ; `--lb/--rb` pour accorder la luminosité d'une personne au fond. Vérifier que la lumière vient du même côté sur les deux portraits et sur le fond ; sinon, retourner un portrait en miroir plutôt que de régénérer.
- Ombres : halo derrière chaque personne et ombre de contact sur la table, activées par défaut.
- Texte : posé en PIL (ou Canva), jamais généré ; 3 à 5 mots, dernière ligne en bloc accent, sous-titre « CONVERGENCE · ÉPISODE NN ».
- Solo : `composite.py` (échelle par la hauteur du visage, 35-50 % du cadre), puis `overlay.py`.

## 7. Vérification avant de montrer

1. `compare_ref.py sortie.jpg ref1.jpg ref2.jpg` puis ouvrir la planche : traits protégés intacts ? Sinon, rejeter et éditer (pas régénérer).
2. Les deux portraits d'une miniature ont le même rendu (netteté, grain, direction de lumière) ; sinon `--grade` et `--lb/--rb`, pas un nouveau tir.
3. `check.py final.jpg` : lisible à 256×144, luminosité, une famille de teintes.
4. Lecture d'ensemble : 2 éléments focaux, texte 3-5 mots qui complète le titre, aucune imagerie exclue, aucun chiffre non sourcé.
5. Montrer **un** résultat (deux si Nass a demandé deux tirages), avec la planche de comparaison disponible.

## 8. Règle des données réelles

Le modèle ne génère **jamais** un graphique de prix, un montant ou une capture de wallet : il inventerait les données. Le prompt réserve une zone vide (par exemple une carte crème vierge à bord noir) ; le vrai graphique (bougies d'exchange datées, données on-chain) ou la vraie capture est posé en PIL ou dans Canva à l'étape `-final`, avec la date, et la source notée dans `figure_source`.

## 9. Coûts et journal

Chaque appel de `generate.py` écrit une ligne dans `outputs/generation-log.jsonl` (date, modèle, mode, fichiers, coût). Avant une session : annoncer le coût prévu (ancre ≈ 0,23 $, édition ≈ 0,23 $ en high, fond brouillon < 0,01 $, Nano Banana ≈ 0,07 $). Repères : ép. 03 a coûté ≈ 5 $ en régénérant (15 détourages) ; la méthode par ancre vise moins de 1 $ par épisode.

## 10. Checklist

- [ ] Prompt en anglais, caméra et lumière fixes, traits décrits
- [ ] Ancre validée éditée (pas de nouveau portrait sans décision de Nass)
- [ ] Un seul changement dans l'appel, liste de préservation présente
- [ ] 2 tirages max, brouillon en qualité basse avant le high
- [ ] `compare_ref.py` ouvert : visage fidèle, yeux ouverts, barbe de la bonne couleur, pas de dents sauf demande
- [ ] Bras et coudes entiers, épaules visibles
- [ ] Deux portraits harmonisés (`--grade`, lumière du même côté), ombres de contact
- [ ] Une personne mène (`--lead`), recadrage serré, 2 éléments focaux
- [ ] Texte 3-5 mots posé en PIL/Canva, aucun texte ni chiffre généré
- [ ] Aucune imagerie levier / short / casino / argent facile, pas de style IA générique
- [ ] Coût noté dans le journal, choix loggé dans `memory/choices.json`
