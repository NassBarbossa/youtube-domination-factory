# Titres : ce que disent les sources, ce que dit le skill, ce qu'on a fait (20 octobre 2026)

Demande de Nass : une analyse fondée sur de vraies recommandations, comparée au skill `yt-titres-seo` et aux titres produits et mesurés. Sources lues le 20 octobre 2026 (liens ci-dessous), données YouTube Studio du 13 octobre 2026 (`yt-analytics/outputs/analytics-2026-10-13.json` et `-notes.json`), mémoire des choix (`memory/choices.json`). Rien ici ne vient de mémoire : chaque chiffre a sa source ou son fichier.

## 1. Les sources, et le poids à leur donner

| Source | Nature | Ce qu'elle dit |
|---|---|---|
| [YouTube Help, « Make great titles and thumbnails »](https://support.google.com/youtube/answer/12340300) | Officiel | « Make sure your title accurately represents the video. » « Viewers may only see part of your title » : rester court, mots-clés d'abord, « Save episode numbers and branding for the end ». « Limit ALL CAPS and emoji. » Deux familles : titres « searchable » (ce qu'on tape) et titres « intriguing » (curiosité, pour le fil) ; choisir selon où la vidéo sera vue. Aucune longueur chiffrée. |
| [YouTube Help, « A/B test titles & thumbnails »](https://support.google.com/youtube/answer/16391400) | Officiel | Jusqu'à 3 titres et/ou miniatures. YouTube « optimize[s] tests for overall watch time over other metrics, like click-through-rate » ; résultat Winner / Performed Same / Inconclusive ; test fini en deux semaines au plus ; « test older videos first » ; options bien différentes, sinon pas de gagnant. Les archives de lives sont éligibles. |
| [YouTube Help, « Podcast discovery tips »](https://support.google.com/youtube/answer/12950577) | Officiel | « Each video is titled with the episode name and, optionally, the show name. » « Don't add extra words to your podcast title (including 'podcast,' unless that is part of your show's name). » |
| [air.io, étude 11 niches, 18 080 chaînes](https://air.io/en/audience-growth/how-to-write-a-youtube-title-that-gets-clicked-research-across-11-niches) | Données larges, métrique = taux d'engagement médian (pas le CTR) | « 30–50 characters is the universal sweet spot » ; 90+ caractères sous-performent. Business : « titles with specific dollar figures, percentages, or timeframes consistently outperform generic variants ». Point d'interrogation : fort positif en Education et Business, « question marks work when the viewer already has the question ». Crochets : positif modeste, les tags [2026] font mieux en Business et Education. Majuscules intégrales : négatif en Education. Cadrage négatif : marche en Business et Education « when it helps viewers avoid a mistake », l'indignation fabriquée sous-performe. Curiosité : la catégorie émotionnelle la plus forte. Recherche : mot-clé « in the first 40% of the title » ; fil : « hook strength matters more than keyword placement ». |
| [Humble & Brag, 12 règles](https://humbleandbrag.com/blog/youtube-title-best-practices), citant Subsub.io (120 703 titres) | Agence + jeu de données tiers | Moins de 60 caractères ; « the median title length of top-performing videos was eight words » ; les 3 à 5 premiers mots portent la décision ; titre complémentaire de la miniature : « 1 to 2 percentage points of CTR » chez leurs clients ; 1 ou 2 mots forts, « three or more start to feel like spam » ; « capitalise at most one word per title » ; crochets légèrement au-dessus ; petits nombres impairs ; A/B 48 h minimum, une variable ; année = « 12-month shelf life » ; réécrire les titres à fortes impressions et faible CTR. |
| 1of10 (extrait de recherche, page non relue) | Outil, Outlier Score sur 62 Md de vues | Les titres de 5 mots ont l'engagement médian le plus haut. C'est l'origine de la règle « ≤ 30 caractères et 5 mots » du skill. |
| ytgrowth, 28 947 vidéos (extrait de recherche, page en 403) | Données larges | Corrélation longueur du titre / performance r = 0,0046, autrement dit nulle. |
| [Prepublish, étude 349 hooks](https://prepublish.ai/blog/youtube-hook-study) | Données, 36 chaînes de 10 k à 6,6 M d'abonnés | Les ouvertures qui « engage the title's promise » : 87,0 % des hits contre 77,9 % des flops. Le titre est une promesse que les 45 premières secondes doivent reprendre. |
| [The Audacity to Podcast](https://theaudacitytopodcast.com/should-you-include-guest-names-in-your-podcast-episode-titles/), [Metadata Reactor](https://metadatareactor.com/blog/podcast-seo-youtube-guide/) | Guides podcast | Nom de l'invité en titre s'il est connu dans la niche, sinon son expertise ; un numéro d'épisode placé avant le sujet cache le mot-clé. |

Lecture d'ensemble : les seules sources officielles (YouTube) ne fixent aucune longueur, demandent la fidélité, le mot-clé devant et la marque à la fin. Les grandes bases (air.io, Subsub) convergent vers 30 à 60 caractères et 5 à 8 mots ; la seule étude qui a mesuré la corrélation longueur / performance la trouve nulle. Aucune source ne soutient un plafond à 30 caractères, sauf 1of10 par le nombre de mots.

## 2. Le skill, règle par règle

| Règle du skill | Ce que disent les sources | Verdict |
|---|---|---|
| « ≤ 30 caractères et 5 mots max » | 30–50 (air.io), < 60 et médiane 8 mots (Subsub), r ≈ 0 (ytgrowth), 5 mots (1of10 seul) | Contredite. À remplacer par 30–60 caractères, promesse dans les 5 premiers mots. |
| 8 formules T1–T8, aucune question | Point d'interrogation = signal fort en Education et Business (air.io) ; 4 des 5 titres publiés sont des questions (voir § 3) | Manque. Ajouter une formule T9 « la question que l'avatar se pose déjà ». |
| Mot-clé « de préférence au début » | YouTube : mots-clés d'abord ; air.io : premiers 40 % ; H&B : 3 à 5 premiers mots | Conforme. Préciser : marque et numéro d'épisode à la fin (YouTube). |
| Biais négatif parmi les mécanismes, « jamais une panique de marché » | air.io : marche quand il aide à éviter une erreur, l'indignation sous-performe | Conforme, nuance déjà juste. |
| Un seul mot en majuscules max | YouTube « Limit ALL CAPS », air.io négatif en Education, H&B un mot | Conforme. Le suffixe de marque « CONVERGENCE [EP.NN] » est toléré (branding à la fin). Ajouter : pas de « !! » ni d'emoji. |
| « Pas de listes chiffrées » | Business : chiffres précis, pourcentages et délais font mieux (air.io) ; petites listes impaires (H&B) | Partiel. Garder l'interdit « N cryptos à acheter » (conformité), dire que les chiffres réels et sourcés et les délais sont un plus. |
| Rien sur l'année dans le titre | [2026] positif en Business et Education (air.io) ; durée de vie 12 mois (H&B) | Manque. Année pour les sujets datés (marché, « en 2026 »), pas pour les tutoriels intemporels (wallet, seed phrase). |
| Rien sur le test A/B des titres | YouTube : 3 titres, gagnant au temps de visionnage, anciennes vidéos d'abord, archives de lives éligibles | Manque. Ajouter une section « Retitrage et test ». |
| Scoring SEO et Clic à poids égal | YouTube : choisir « searchable » ou « intriguing » ; air.io : en fil, le hook compte plus que le mot-clé ; chaîne : recherche 3 % du trafic, 73 % abonnés / playlist / page de chaîne | À ajuster. Décider le type du titre avant de générer ; vidéo pour le fil → Clic prime ; tutoriel tapé → SEO prime. |
| Hypothèses du feedback-loop (40–60 caractères, 6–10 mots, crochets, mot-clé dans les 5 premiers mots, ≤ 3 mots en majuscules, pas d'emoji) | Plus proches des sources que la règle principale | Le skill se contredit (règle ≤ 30, hypothèse 40–60). Aligner la règle sur ces hypothèses. |
| Mode autonome : `winning_title` « ≤ 30 caractères, 5 mots max » | Idem première ligne | À mettre à jour avec la règle. |
| Fidélité au contenu, pas de clickbait | YouTube : « accurately represents the video » | Conforme. |
| Vérification par l'autocomplétion YouTube | air.io : la question marche quand le spectateur l'a déjà | Conforme : l'autocomplétion est exactement la liste des questions qu'il a déjà. |

## 3. Ce qu'on a produit et mesuré

| Vidéo | Titre publié | Car. | Mots | Forme | CTR | Impr. | Origine |
|---|---|---|---|---|---|---|---|
| Pourquoi investir | « Pourquoi il faut investir en 2026 ? (Formation Offerte) » | 55 | 9 | question + parenthèse | 16,0 % | 426 | Nass |
| Devenir riche | « Comment devenir riche grâce à l'investissement ? » | 48 | 7 | question | 9,9 % | 585 | Nass |
| IOC | « Investis en cryptos avec cette méthode !! » | 41 | 7 | impératif + « !! » | 34,3 % | 73 | Nass |
| Convergence ép. 01 | « CONVERGENCE [EP.01] : Podcast investissement w/ Sadek » | 53 | 7 | marque d'abord | 10,7 % | 328 | Nass |
| Convergence ép. 03 | « Or ou Bitcoin en 2026 , que choisir ? CONVERGENCE [EP.03] » | 57 | 11 | question + suffixe | pas encore de données | | skill + Nass |

Ce que ça dit :

- Les cinq titres font 41 à 57 caractères et 7 à 11 mots. Aucun n'applique la règle « ≤ 30 caractères ». Le seul titre sorti du skill (ép. 03, « Or ou Bitcoin en 2026 ? », 23 caractères) a été allongé par Nass à 57 caractères avec « que choisir ? » et le suffixe de marque. Ses choix vont dans le sens des sources, pas de la règle.
- Les CTR de 10 à 16 % sur 328 à 585 impressions sont élevés (les notes d'analyse situent la moitié des chaînes entre 2 et 10 %). Titres et miniatures font cliquer. Le 9,9 % de « Devenir riche » change à la fois le titre et la miniature (mur de billets contre billet déchiré) : on ne peut pas attribuer l'écart au titre. Le 34,3 % de l'IOC repose sur 73 impressions, illisible.
- Ép. 01 : marque d'abord, puis « Podcast investissement », le mot que YouTube demande d'enlever des titres de podcast. Le sujet de l'épisode n'apparaît pas. La recherche n'a apporté que 5,6 % des 125 vues (7 vues) : retitrer ne perd presque rien. L'ép. 03 suit déjà le bon ordre (sujet en question, marque à la fin).
- Ce que j'ai fait dans les sessions : pour l'ép. 03, 7 titres tous ≤ 30 caractères ; pour l'ép. 01, 7 titres tous ≤ 30 caractères (« Bull run 2026, c'est reparti ? », 30 caractères). La contrainte de longueur était la mauvaise ; la forme question, le mot-clé devant et le suffixe à la fin étaient justes. Avec la règle corrigée, les mêmes titres se proposent avec un complément de promesse (ex. « Bull run 2026 : c'est reparti, ou pas ? » puis le suffixe).

## 4. Modifications appliquées à `SKILL.md` et `references/feedback-loop.md` (go de Nass, 20 octobre 2026)

1. **Longueur** : remplacer « ≤ 30 caractères et 5 mots max » par « 30 à 60 caractères, la promesse tient dans les 5 premiers mots (ce qui reste visible quand YouTube tronque), suffixe de marque ou d'épisode à la fin, jamais au début ». Même changement dans le JSON du mode autonome.
2. **Formule T9, question** : « [Sujet] en [année] : [la question qu'il se pose] ? » (« Or ou Bitcoin en 2026, que choisir ? »), à utiliser quand l'autocomplétion montre que la question existe déjà.
3. **Type de titre avant génération** : « searchable » (tutoriel que l'avatar tape) ou « intriguing » (vidéo pour le fil, l'actu, le live). Le type fixe le poids du scoring : SEO prime sur le premier, Clic sur le second. Rappeler le chiffre de la chaîne : recherche 3 % du trafic au 13 octobre 2026.
4. **Année** : présente pour un sujet daté, absente d'un tutoriel intemporel.
5. **Majuscules et ponctuation** : un mot en majuscules max hors suffixe de marque ; pas de « !! », pas d'emoji.
6. **Chiffres** : un chiffre réel et sourcé ou un délai concret est un plus en finance ; l'interdit ne porte que sur les listes « N cryptos à acheter » et les promesses.
7. **Section « Retitrage et test »** : pour une vidéo publiée à fortes impressions et faible CTR, ou au titre qui ne dit pas le sujet, proposer 3 titres distincts et lancer un test A/B dans Studio (gagnant au temps de visionnage, deux semaines max, archives de lives éligibles) ; logger `ab_test_winner` et `title_type` dans `choices.json`. Pour une chaîne à quelques centaines d'impressions par vidéo, dire à Nass que le résultat sera souvent « Inconclusive » : on retient quand même le titre le plus fidèle.
8. **Convergence** : gabarit « [Question de l'épisode] CONVERGENCE [EP.NN] », sans le mot « podcast », nom de l'invité dans la description et les tags, dans le titre seulement si l'épisode porte sur lui.
9. **Feedback-loop** : supprimer la contradiction (hypothèse 40–60 contre règle ≤ 30), ajouter `title_type` et `ab_test_winner`, et dater la recalibration : quand dix vidéos auront dépassé 1 000 impressions.

## 5. Ce qui reste non prouvé

- Nombres impairs, mots forts, crochets : petits effets, données d'agences ou d'outils, jamais mesurés ici.
- Tout est corrélationnel et hors de la chaîne : cinq vidéos à moins de 600 impressions chacune ne permettent de trancher aucune règle. Le feedback-loop tranchera, pas une étude de plus.
