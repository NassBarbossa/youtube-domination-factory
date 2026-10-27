# Veille : visages IA dans les miniatures, ce que recommandent les sources et ce que j'ai fait (20 octobre 2026)

Demande de Nass après les miniatures Convergence ép. 01 : « base-toi sur des recherches de vraies recommandations sur l'utilisation de l'IA pour générer des thumbnails, et compare à ce que tu as fait sur les différentes sessions ». Sources officielles (OpenAI, Google) distinguées des blogs d'éditeurs d'outils, qui vendent leur produit.

## 1. Ce que disent les sources

### Documentation officielle

**OpenAI, guide Image prompting et guide des modèles GPT Image**
- Pour une édition : « identify what should change and what must stay the same » ; dire « change only X » et lister ce qui est préservé (identité, géométrie, lumière).
- Pour une personne : « State which facial features and proportions must remain unchanged » ; exemple : « Do not change her face, facial features, skin tone, body shape, pose, or identity in any way ».
- Itérer en chaîne : « Start with one output, inspect it, and use it as the next input » ; « Keep each follow-up narrow so you can see which change helped » ; « Repeated edits can still change details you intended to preserve », donc répéter la liste de préservation à chaque tour.
- Limite reconnue : le modèle « may occasionally struggle to maintain visual consistency for recurring characters or brand elements across multiple generations ». Si une zone doit rester identique au pixel près : « composite the approved edit into the original image instead of relying on prompting alone ».
- `input_fidelity` : sur gpt-image-2, « Omit it. Image inputs are always processed at high fidelity » (sur gpt-image-1.5, mettre `high`).
- Masques : « Masking with GPT Image is entirely prompt-based », le masque guide sans précision exacte.

**Google, documentation Gemini image et billet officiel de prompting**
- « Multi-turn conversation is the recommended way to iterate on images » ; une édition se borne : « Keep everything else in the image exactly the same, preserving the original style, lighting, and composition ».
- « Don't expect a perfect image on the first try » ; ajustements petits et conversationnels (« une expression plus sérieuse, tout le reste identique »).
- Références : jusqu'à 14 images, mais 6 en haute fidélité sur Pro ; si les traits dérivent après beaucoup d'éditions, repartir d'une nouvelle conversation avec une description détaillée.
- Guide Nano Banana Pro (déjà dans la veille du 18 oct.) : « Keep the person's facial features exactly the same as Image 1 » ; si l'image est bonne à 80 %, demander une modification ciblée plutôt que régénérer.

### Guides praticiens (blogs d'outils, à prendre comme des pratiques, pas des preuves)

**Fidélité du visage**
- Apiyi (guide Nano Banana Pro) : « The model re-interprets facial structure; slight angle changes cause proportional drift ». Références : 1024 px ou plus, lumière frontale uniforme, une frontale + une à 45°, visage au moins un tiers du cadre, expression neutre, 2 à 3 références, fidélité maximale à 6 ou moins. Une photo prise en contre-plongée exagère la mâchoire. Garder la même description de caméra à chaque tir (« 3/4 portrait, eye-level, 85mm »), les mêmes paramètres et les mêmes références.
- Thumio : les prompts seuls donnent « a generic composite, and each regeneration drifts further from your face » ; insérer le vrai visage en dernier, une fois la composition fixée ; les photos envoyées à ChatGPT ou Gemini « don't persist and drift between generations ».
- AZ Big Media (créateur qui utilise Nano Banana) : une seule photo de référence « really clean, well-lit… neutral pose with a neutral expression… against a plain background », réutilisée partout ; règles visuelles de la chaîne écrites une fois et appliquées à chaque prompt ; 3 à 4 variantes, puis typographie à la main, correction colorimétrique contre la page de la chaîne, puis A/B test.
- Guides « character consistency » (nano2image, nenobanana, sider) : un seul changement par requête ; rappeler le verrou d'identité en début et en fin de prompt ; rejeter tout tirage où un trait protégé a changé.

**Assemblage de deux personnes**
- Phlearn, aipgen, Photoshop Harmonize : ce qui trahit un montage, c'est la lumière plus que les bords (« A subject can be cut out perfectly and still look pasted in, and the cause is usually light rather than edges ») ; vérifier la direction de la lumière avant la couleur ; sans ombre de contact, le sujet flotte.
- Banana Thumbnail : « You never want to use the raw output straight from the generator » ; un seul étalonnage sur le visage réel et le fond pour qu'ils « look like they belong in the same physical space » ; repeindre les reflets dans les yeux pour qu'ils suivent la lumière de la scène ; « Real emotion beats AI emotion every time ».

**Miniatures de podcast**
- 1of10 : « The most common mistake is giving both people equal size and equal weight, which leaves the eye with nowhere to go » ; « Two people in chairs with microphones, shot wide, is the most common podcast thumbnail and the least effective » ; « A posed studio shot reads as an advert » ; recadrer serré ; quatre mots de texte ; une couleur d'accent constante rend la chaîne reconnaissable.
- Castos (top podcasts YouTube 2026) : « Their thumbnails look different from each other, but each show's thumbnails look like they belong to the same family » ; émotion vraie, « not the exaggerated 'YouTube face' » ; les shows live tirent des vrais moments de l'épisode.
- Guides de gabarits : gabarit fixe pour la marque (logo, couleurs, police, bande de titre), contenu variable par épisode ; « every episode looks the same except guest face » est une erreur listée.

**Ce que les spectateurs rejettent**
- wthumb (septembre 2026) : « The turnoff is the lie and the sameness, not the tool » ; signes : peau trop lisse et éclairée uniformément, scènes inventées, « repetitive styling » (orange et sarcelle, sujets lumineux, ciels dramatiques) ; conseil : « Use a real photo of yourself or leave people out » ; vérifier à taille réelle et à taille de fil.
- YouTube : une miniature générée est de l'aide à la production, pas de label requis ; ce qui est interdit, c'est de tromper sur le contenu.

## 2. Ce que j'ai fait, session par session

| Session | Volume | Méthode | Écart avec les sources |
|---|---|---|---|
| Formation offerte (4 oct., 3 vidéos) | 165 fichiers, 11 à 17 itérations par miniature | Fond généré + détourage généré, puis greffe du visage d'un tirage validé sur un autre buste | Fini par la bonne méthode (visage validé posé en dernier), mais atteinte par essais successifs ; retours « visage fidèle, yeux ouverts, barbe pas orange » = dérives typiques de la régénération |
| J'abandonne (18 oct.) | 50 fichiers, versions A à H | H = scène complète en un tir, 3 photos d'identité, visage à 55 % du cadre | Scène entière régénérée = risque de dérive maximal selon les sources, mais ça a marché parce que le visage était grand (arXiv 2609.04151 : l'identité se perd quand le visage est petit) |
| Convergence ép. 03 (20 oct.) | 45 fichiers, 15 détourages (7 Nass, 8 Sadek), 5 modèles d'expression Sadek, 1 fond, ≈ 5 $ | Détourages régénérés de zéro à chaque retour, deux modèles (GPT-Image-2 pour Nass, Nano Banana 2 pour Sadek), fond à part, assemblage sans étalonnage commun, micros puis sans | Jamais d'édition d'un tirage validé ; pose, tenue, expression et lumière changées en même temps ; deux rendus photo différents sans harmonisation ; poids égal aux deux personnes ; plan studio posé |
| Convergence ép. 01 (20 oct.) | 13 fichiers, 6 détourages (4 Nass, 2 Sadek), 1 fond, ≈ 1,1 $ | Mêmes détourages puis régénération de Nass deux fois, quatre variables changées d'un coup par rapport au tirage validé de l'ép. 03 (angle, tenue, expression, direction de lumière), puis nouveau tir au lieu d'éditer | Exactement l'inverse du « change only X, keep everything else » ; vérification sur planches réduites, pas à taille réelle |

Appels image sur Convergence en deux jours : 28, tous en génération avec références (`input_references`), aucun en édition d'un tirage précédent, aucun chaînage « sortie → entrée suivante ».

## 3. Comparaison point par point

| Recommandation (source) | Ce que j'ai fait | Verdict |
|---|---|---|
| Éditer un tirage approuvé, « change only X » (OpenAI, Google) | Régénéré de zéro à chaque retour | Non respecté, cause principale des visages différents |
| Une variable par requête (OpenAI « keep each follow-up narrow », guides consistency) | Angle + tenue + expression + lumière changés ensemble | Non respecté |
| Chaîner : la sortie devient l'entrée suivante (OpenAI, Google multi-turn) | Chaque appel indépendant, mêmes photos renvoyées | Non respecté |
| Verrou d'identité explicite dans le prompt (OpenAI, Google) | Présent (« Reproduce HIS exact face… », description des traits) | Respecté |
| Même description de caméra et mêmes paramètres à chaque tir (Apiyi) | Caméra constante (85 mm), mais direction de lumière changée selon la position | Partiel |
| Références : 2-3 photos, frontale + 45°, lumière uniforme, ≥ 1024 px, neutre (Apiyi, AZ Big Media) | 4 photos de Nass dont le selfie piscine (plein soleil, main, contre-plongée) ; les deux selfies mur passent la grille | Partiel : retirer la photo piscine ; mes refs de Sadek sont pourtant petites (322 et 588 px) et il sort bien, donc la qualité des refs n'explique pas tout |
| Visage réel inséré en dernier, fond et corps générés avant (Thumio, Banana Thumbnail, wthumb) | Jamais sur Convergence ; fait une fois sur la formation (greffe) | Non respecté |
| Un seul étalonnage, lumière cohérente, ombres de contact (Phlearn, Banana Thumbnail) | Deux modèles, deux lumières, un fond, aucune harmonisation ni ombre | Non respecté, cause de l'effet collé |
| Variantes : 3-4 du fond ou de la scène, puis test (AZ Big Media, MrBeast) | Variantes du visage lui-même, par grilles | Détourné : les variantes se font sur la scène, pas sur le visage |
| Vérifier chaque sortie contre la référence à taille réelle et à taille de fil (wthumb, guides) | Planches réduites à 650 px, puis « fidèle » écrit sans comparaison | Non respecté |
| Une personne domine, recadrer, pas de plan studio posé (1of10) | Deux bustes symétriques, plan studio, micros au départ | Non respecté |
| Gabarit de marque fixe, contenu variable par épisode (Castos, 1of10) | Gabarit fixe correct ; variation limitée au texte | Partiel |
| Pas de style IA générique (lueurs vert et ambre, sujets éclairés uniformément) (wthumb) | Fond sombre à lueurs vert et ambre, peau lissée | Non respecté |

## 4. Ce que ça change pour la suite (règles, dans l'ordre)

1. **Un portrait ancre par personne**, validé par Nass (pour lui : `outputs/convergence-ep03-cutout-nass-v3-2.jpg` qu'il a gardé pour l'ép. 03 ; pour Sadek : `nb-sadek-1`). Chaque épisode part de l'ancre en **édition** : « change only the outfit and the background, keep face, expression, hairstyle, proportions and lighting identical », une variable par appel, la sortie validée devient la nouvelle entrée.
2. **Ou vrai visage en dernier** : composition (fond, corps) d'abord, puis insertion du visage réel ou de l'ancre, puis un seul étalonnage, ombre de contact, reflets des yeux.
3. **Références** : garder les deux selfies mur, retirer la piscine ; idéalement une photo propre dédiée (face, lumière uniforme, fond uni, neutre).
4. **Vérification** avant de montrer : comparaison à taille réelle avec la référence, rejet si un trait protégé a bougé ; test à taille de fil.
5. **Mise en page podcast** : une personne domine selon l'épisode, recadrage serré, accent de marque constant, expression et sujet variables.
6. **Nombre de tirages** : ce que Nass demande (deux), et sur la scène, pas sur le visage.

## Sources

- OpenAI, Image prompting guide : https://developers.openai.com/api/docs/guides/image-prompting
- OpenAI, Image generation guide (masques, références, limites) : https://developers.openai.com/api/docs/guides/image-generation
- OpenAI Cookbook, GPT Image models prompting guide : https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide
- Google, documentation Gemini image generation : https://ai.google.dev/gemini-api/docs/image-generation
- Google Developers Blog, prompting Gemini 2.5 Flash Image : https://developers.googleblog.com/en/how-to-prompt-gemini-2-5-flash-image-generation-for-the-best-results/
- Google AI, Nano Banana Pro prompting guide : https://dev.to/googleai/nano-banana-pro-prompting-guide-strategies-1h9n
- Apiyi, Nano Banana Pro face consistency guide : https://help.apiyi.com/en/nano-banana-pro-face-consistency-guide-en.html
- Thumio, Put your face in AI thumbnails : https://thumio.com/blog/put-your-face-in-ai-thumbnails
- AZ Big Media, consistent thumbnails with Nano Banana : https://azbigmedia.com/business/business-and-social-media/creating-consistent-youtube-thumbnails-that-actually-look-like-a-channel-with-nano-banana/
- nano2image, character consistency : https://nano2image.com/nano-banana/image-to-image/character-consistency
- nenobanana, 12 prompts character consistency : https://www.nenobanana.com/blogs/nano-banana-character-consistency-12-prompts-that-actually-work--2026-guide
- Phlearn, match lighting for composites : https://phlearn.com/tutorial/match-lighting-any-composite/
- aipgen, combine photos with matching light : https://aipgen.com/blog/combine-photos-with-matching-light/
- Photoshop Harmonize : https://photoshoptrainingchannel.com/how-to-use-photoshops-new-harmonize-tool-for-perfect-composites-and-sharper-results/
- Banana Thumbnail, why AI thumbnails fail : https://blog.bananathumbnail.com/ai-youtube-thumbnails-2/
- 1of10, podcast thumbnails : https://1of10.com/thumbnail-generator/podcast
- Castos, top podcasts on YouTube 2026 : https://castos.com/top-podcasts-on-youtube-2026/
- wthumb, are AI thumbnails a turnoff : https://wthumb.co/blog/are-ai-thumbnails-a-turnoff
- Podsqueeze, cover art et thumbnails : https://podsqueeze.com/blog/how-to-make-podcast-cover-art-and-episode-thumbnails/
- arXiv 2609.04151 (identité perdue quand le visage est petit) : https://arxiv.org/html/2609.04151v1
