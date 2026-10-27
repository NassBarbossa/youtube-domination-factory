# Veille : générer des miniatures YouTube par IA (18 octobre 2026)

Recherche faite pendant la recharge OpenRouter. Sources nouvelles par rapport au skill (aucune n'était citée dans `generation-images.md`). Les chiffres des blogs d'éditeurs sont donnés pour ce qu'ils sont : des affirmations marketing, sauf mention contraire.

## 1. Fidélité du visage : quel modèle ?

| Modèle | Similarité faciale ArcFace (Pexels-100, arXiv 2607.25622) | Coût mesuré OpenRouter (1024², défaut) | Références max |
|---|---|---|---|
| GPT-Image-2 (`openai/gpt-image-2`) | **0,85** | 0,006 $ (`quality` low/auto) · 0,21 $ (high) | 16 |
| Nano Banana 2 (`google/gemini-3.1-flash-image`, modèle actuel du skill) | 0,59 | 0,067 $ | 14 |
| Nano Banana (v1) | 0,49 | — | — |
| FLUX Kontext | 0,49 | — | — |
| Qwen-Image | 0,46 | — | 4 |
| GPT-Image-1.5 (secours actuel de `generate.py`) | **0,33** | — | — |

- Benchmark académique unique, images en pied, une référence par sujet : à prendre comme un signal fort, pas une vérité. Un second papier (arXiv 2609.04151) note que GPT-Image-2 et Nano Banana 2 perdent tous deux l'identité quand le visage devient petit dans le cadre : générer le détourage en gros plan, puis le réduire au montage, est la bonne pratique (c'est déjà notre pipeline).
- Les comparatifs de blogs (Nano Banana Pro vs GPT Image 1.5) donnent Nano Banana devant sur la conservation du visage en transfert de style ; ils testent la version 1.5 de GPT Image, pas la 2.
- Riverflow 2.5 Pro (`sourceful/riverflow-v2.5-pro`, 0,064 $) est n° 1 Design Arena en image et en édition, 10 références, mais aucun test indépendant sur le visage.
- OpenRouter exige un solde ≥ 1 $ pour toute sortie image (erreur 402 constatée le 2026-10-18).

**À tester dès le solde rechargé (< 0,50 $ au total)** : le même détourage « choqué » avec `openai/gpt-image-2` (quality medium, `aspect_ratio` 3:4, `input_references` = 2 ou 3 photos de Nass) et avec `google/gemini-3.1-flash-image`, comparer la ressemblance ; fond avec Riverflow 2.5 Pro ou Nano Banana 2. Remplacer `gpt-image-1.5` par `gpt-image-2` dans `scripts/generate.py`.

## 2. Prompting (guide officiel Google, Nano Banana Pro)

- Phrase explicite : « Keep the person's facial features exactly the same as Image 1 », identité et tenue cohérentes.
- Jusqu'à 14 références dont 6 en haute fidélité : envoyer plusieurs angles de Nass, pas une seule photo.
- Décrire l'émotion ou la pose en précisant que l'identité ne change pas ; phrases complètes, pas de liste de mots-clés.
- Si l'image est bonne à 80 %, demander une modification ciblée plutôt que régénérer.
- Texte exact entre guillemets, style typographique décrit ; ratio écrit dans le prompt (« 16:9 landscape »).
- Conseil tiers (vidpros, bananathumbnail) : écrire le texte en dernier pour qu'il colle à l'expression ; une seule palette + une couleur d'accent ; un seul objet héros.

## 3. Ce que disent les données sur le design

**vidIQ, 500 vidéos « breakout », 30 niches, mois clos le 30 juin 2026** (la source la plus solide trouvée)
- 69 % montrent un visage, 80 % chez les plus grosses surperformances ; 56 % fort contraste ; 89 % visage ou contraste.
- Médiane du texte : 5 mots.
- Seulement 1 miniature sur 20 montre une expression exagérée (choc, cri) : l'expression doit coller au contenu.
- Visage à un quart ou un tiers du cadre, sans chevaucher le texte. Éviter le rouge, le blanc et le noir de l'interface YouTube ; orange, sarcelle, jaune, violet ressortent mieux.

**TubeAnalytics 2025-2026, vidéos ≥ 10 000 impressions, taille d'échantillon non publiée**
- Visage dominant à émotion claire : +18 à +32 % de CTR vs neutre/sans visage.
- Texte 3-5 mots fort contraste : +11 à +22 % en recherche, **-4 % en navigation** (accueil, suggestions).
- Fonds vifs et saturés : +8 à +14 % vs fonds ternes ou sombres.

**Paddy Galloway / équipe MrBeast**
- « Glance test » : tout doit se lire en une seconde en faisant défiler ; ≤ 3 éléments majeurs (texte, visage, sujet).
- Titre et miniature se lisent ensemble : ils se complètent, ne se répètent pas.
- ~50 concepts par vidéo chez MrBeast, jugés à petite taille.

**Conséquences pour « J'ai tout perdu ? »**
- La version C (fond noir, texte géant, courbe rouge, visage) respecte les 3 éléments et le glance test.
- Elle va contre deux données : fond sombre (-8 à -14 % vs fond vif) et rouge/noir = couleurs de l'interface YouTube. À trancher par Test & Compare plutôt qu'à la main : version C vs une variante fond vif.
- L'expression « choqué mains sur la tête » est le type d'expression que 1 miniature sur 20 utilise ; vidIQ demande qu'elle colle au contenu. Pour une vidéo transparence où la réponse est « du surplace », la variante sceptique est la plus défendable ; le choqué se joue au test.

## 4. Outils : classements à prendre avec des pincettes

- Presque tous les « top 10 » sont publiés par l'outil classé premier (1of10, OverseerOS, TubeGen, Hooksnap, Vidocu). The Cascade Hub vend son propre kit mais note les outils honnêtement.
- Consensus malgré tout : **Canva** pour l'édition et le texte modifiable (15 $/mois) ; **Pikzels** pour le visage (20 à 80 $/mois, FaceSwap hors forfait à 20 $, outputs qui copient les références) ; **Nano Banana Pro** meilleure qualité brute en un essai ; **Ideogram 3.0** le moins cher à l'échelle (0,03 à 0,09 $/image).
- **Ask Studio (YouTube natif)** : génération gratuite dans YouTube Studio pour les chaînes éligibles, bureau seulement, vidéos longues, déploiement progressif depuis l'été 2026. Pas d'image de référence possible, tout par chat, 3 options en 1280×720, filigrane SynthID + C2PA. Vérifier si la chaîne Nassin Crypto a le bouton « Get suggestions » sous la miniature.
- **YouTube Test & Compare** : jusqu'à 3 miniatures, gagnante choisie au **temps de visionnage** (pas au CTR), souvent « inconclusive » tant que l'écart n'est pas significatif ; si une option est < 1280×720, tout le test est dégradé en 854×480.

## 5. Politique YouTube

- Une miniature générée par IA relève de l'« aide à la production » : pas de déclaration « contenu modifié ou synthétique » requise. Elle ne doit pas tromper sur le contenu, ni utiliser le visage d'autrui sans accord. Le propre visage du créateur, cohérent avec ce qu'on voit dans la vidéo, ne pose pas de problème dans les sources trouvées (pas de page officielle explicite sur ce cas précis).

## Sources

- vidIQ, Thumbnail Design Tips 2026 : https://vidiq.com/blog/post/youtube-thumbnail-design-tips/
- TubeAnalytics, Thumbnail CTR Patterns Study 2026 : https://www.tubeanalytics.net/resources/research/thumbnail-ctr-patterns-study-2026
- arXiv 2607.25622, Holistic Identity Preservation (table ArcFace) : https://arxiv.org/html/2607.25622v1
- arXiv 2609.04151, Persistent Identity Preservation benchmark : https://arxiv.org/html/2609.04151v1
- OpenRouter, Image Generation Models Compared (coûts mesurés 11 sept. 2026) : https://openrouter.ai/blog/insights/image-generation-models-compared/
- OpenRouter, fiche gpt-image-2 : https://openrouter.ai/openai/gpt-image-2
- Google AI, Nano Banana Pro prompting guide : https://dev.to/googleai/nano-banana-pro-prompting-guide-strategies-1h9n
- Paddy Galloway, glance test et règle des 3 éléments : https://x.com/PaddyG96/status/1811083499044044951 · https://x.com/PaddyG96/status/1450463472907657220
- Social Media Today, YouTube sur l'équipe miniatures de MrBeast : https://www.socialmediatoday.com/news/youtube-shares-insights-mrbeasts-team-creates-compelling-thumbnail/709817/
- The Cascade Hub, classement 2026 : https://thecascadehub.com/best-ai-thumbnail-makers-for-youtube-2026/
- 1of10, Best AI Thumbnail Generators (auto-classé n° 1) : https://1of10.com/blog/best-ai-thumbnail-generator/
- TubeBuddy, générateur Ask Studio : https://www.tubebuddy.com/blog/youtube-ai-thumbnail-generator/
- TechCrunch, Made On YouTube 23 sept. 2026 : https://techcrunch.com/2026/09/23/youtube-releases-new-ai-features-for-creators-within-its-studio-app/
- Engadget, nouveaux outils miniatures : https://www.engadget.com/2223150/youtube-new-tools-thumbnails/
- Influencer Marketing Hub, Test & Compare : https://influencermarketinghub.com/youtube-test-compare/
- vidIQ, Test & Compare : https://vidiq.com/blog/post/youtube-launches-new-thumbnail-testing-tool/
- Influencer Marketing Hub, inauthentic content & likeness : https://influencermarketinghub.com/youtube-inauthentic-content/
- Pikzels, AI thumbnails allowed? : https://pikzels.com/blog/are-ai-thumbnails-allowed-on-youtube
- Analytics Vidhya, GPT Image 1.5 vs Nano Banana Pro : https://www.analyticsvidhya.com/blog/2025/12/chatgpt-image-vs-nano-banana-pro/
- vidguru, 10 tests Nano Banana Pro vs GPT-Image 1.5 : https://www.vidguru.ai/blog/nano-banana-pro-vs-gpt-image-1-5-comparison.html
- Riverflow 2.5 (communiqué Sourceful) : https://www.accessnewswire.com/newsroom/en/computers-technology-and-internet/riverflow-launches-2.5-the-worlds-highest-rated-ai-image-model-1179030
- vidpros, prompts Nano Banana pour miniatures : https://vidpros.com/10-nano-banana-prompts-for-clickable-youtube-thumbnails/
- ThumbnailCreator, text vs no text (test unique ~4 900 impressions/variante) : https://www.thumbnailcreator.com/blog/text-placement-vs-no-text-thumbnail-impact
