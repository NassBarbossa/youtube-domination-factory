# Convergence EP.04 — « L'achat de la décennie sur le gold ? » (Nass seul, tourné le 2026-10-26, publié le 2026-10-27)

## Sources

| Rôle | Fichier | Format |
|---|---|---|
| YouTube | `D0gALJr-y1o` (`~/Videos/NassRiviera/youtube/D0gALJr-y1o.mp4`, téléchargé le 2026-10-27 sur le Mac) | 1920 × 1080, 60 i/s, 1 215,4 s. **Repère de temps seulement**, jamais pour l'image |
| Brut OBS 16:9 | à retrouver sur le PC Windows (`%USERPROFILE%\Videos\2026-10-26 …`) | à vérifier |
| Vertical (Aitum) | à vérifier sur le PC Windows (`… vertical.mkv`) | à vérifier |

Nass était seul : pas de caméra Sadek. La DA « Les deux droites » est prévue pour deux orateurs ; pour un épisode solo il faut une variante (voir plus bas), à proposer à Nass avant de construire.

## Décalages

À mesurer avec `offset.py` quand le brut est là (YouTube → brut).

## Mises en page vues sur le replay (YouTube, 1080p)

| Mise en page | Quand | Caméra Nass | Écran |
|---|---|---|---|
| cold open « carte » (« LE BTC À 60K », citation) | 0:00–0:30 env. | rond ≈ 330 px à gauche | — |
| « à l'écran » (scène 2 · live, « ÉP. 02 · À L'ÉCRAN » gravé) | majorité de l'épisode | **rond ≈ 330 px en bas à gauche**, étiquette « NASS » | TradingView plein cadre ≈ x 176–1744, y 100–950 |
| fullcam | fin (≈ 19:10) | grande fenêtre ≈ `[45, 105, 1425, 855]` (mesurée sur YouTube, à remesurer sur le brut) | — |

Comme pour l'EP.01, le rond « à l'écran » est trop petit pour remplir un cadre des deux droites sans flou : clips à construire sur l'écran réel avec le rond en médaillon, ou sur la fullcam quand le passage y est.

L'étiquette gravée dit « ÉP. 02 · À L'ÉCRAN » (OBS pas remis à jour) : à garder hors des recadrages.

**Signal cadre :** vers 15:00 un écran Axiom affiche un PnL OTC (+2,31 K, @punk6995) ; la description YouTube porte `#memecoins`. Tout passage memecoin est à signaler à Nass, pas à clipper.

## Transcription

`projects/ep04/transcript-youtube.json` (faster-whisper medium, CPU, Mac, 2026-10-27), **en temps YouTube**. Quand le brut sera là : mesurer le décalage et le reporter dans `raw_to_source`, ou retranscrire le brut.

## Candidats

Repérage complet du 2026-10-27 dans `context/transcripts/passages-2026-10-27.md` (texte exact + pourquoi : `passages-detail-2026-10-27.md`) (transcription : `context/transcripts/D0gALJr-y1o-words.json`, temps YouTube). Nass choisit.

| N° | Passage, idée | Minutage (YouTube) | Mise en page | Présence | Cadre | Statut |
|---|---|---|---|---|---|---|
| 41 | Personne n'achète le bottom parfait, « c'est uniquement par chance » | 03:19–04:24 (+ 04:29–04:38) | à l'écran (TradingView SOL) | Nass seul | couper 04:03–04:11 | à choisir |
| 42 | « Le gold, c'est l'achat de la décennie » : BTC 60K / 45K, 3 900 ou 4 000 | 07:38–08:16 | à l'écran (TradingView or) | Nass seul | position personnelle, pas d'appel à acheter : « si tu n'achètes pas là » à trancher | à décider |
| 43 | Réagir plutôt qu'anticiper, entrée au meilleur prix pour couper si ça s'invalide | 08:26–08:59 | à l'écran | Nass seul | ok | à choisir |
| 44 | Milieu de zone, attendre les bords ; « je ne comprends pas d'être baissier sur un support » | 06:25–07:22 | à l'écran | Nass seul | ok | à choisir |
| 45 | Clôture : trading très difficile, faites attention | 19:29–19:50 | fullcam | Nass seul | ok (teaser) | à choisir |
| 46 | Ce qui définit une tendance baissière (BTC) | 01:39–02:32 | à l'écran (TradingView BTC) | Nass seul | ok | à choisir |
| 47 | Re-rentrer une partie de ses SOL, « j'attends demain » | 04:43–05:11 | à l'écran (SOL) | Nass seul | actif précis | à décider |
| 48 | « T'étais sûr que ça allait monter ? Non. » invalidations | 15:57–16:19 | à l'écran (Axiom, memecoin) | Nass seul | écran memecoin : caméra seule ou autre fond | à décider |
| 49 | Baissier en TF mineur ok, en investissement non | 16:28–16:47 | à l'écran | Nass seul | ok (teaser) | à choisir |
| 50 | Intro solo, changement d'heure, « je ne vais pas débattre tout seul » | 00:36–01:10 | cold open / fullcam | Nass seul | ok | à choisir |

Écartés : trade de la semaine Axiom 10:23–16:23 (memecoin, **signalé**), Trump 17:38–18:11 (politique), « Anthropic 80 milliards » 18:40–19:16 (non vérifié), watchlist 05:13–05:49 (actifs précis).

## Clips rendus (série du 2026-11-09, thème convergence, Nass seul)

Numéros 41 à 55 à la suite des clips EP.01 (21 à 40). Monologue : états SOLO_N / SOLO_N+ et SOLO_E (écran TradingView recadré 380/160/1216/684 → 960 × 540 sous Nass). Deux scènes : « à l'écran » (rond 330 px en bas à gauche, crop 67/697/264/264, prescale 3,2, sharpen) et plein cadre (crop 330/110/700/700, prescale 1,3).

| N° | Clip | Minutage (YouTube) | Statut |
|---|---|---|---|
| 41 | « Épisode spécial : tout seul » : L'intro de l'épisode solo : à cause du changement d'heure, Nass et Sadek ne se sont pas accordé leurs violons. Épisode mené tranquillement, pas de débat : « je ne vais pas débattre tout seul, c'est un peu bizarre ». | 00:36–00:42 + 00:43–00:54 + 00:55–01:10 | **v1 rendue le 2026-11-09** : projet `{repo}/clip-convergence/projects/ep04/41-episode-special-tout-seul/`, export `{repo}/clip-convergence/exports/ep04/41-episode-special-tout-seul.mp4` |
| 42 | « Ce qui définit une tendance baissière » : Sur le BTC : un changement de structure potentiel, « sommet là, creux là, sommet là », début de tendance baissière en court terme. Et le rappel de la définition : des sommets de plus en plus bas et des points bas de plus en plus bas. Son écran TradingView sous lui quand il pointe. | 02:04–02:08 + 02:11–02:22 + 02:23–02:32 | **v1 rendue le 2026-11-09** : projet `{repo}/clip-convergence/projects/ep04/42-ce-qui-definit-une-tendance-baissiere/`, export `{repo}/clip-convergence/exports/ep04/42-ce-qui-definit-une-tendance-baissiere.mp4` |
| 43 | « Le bottom parfait, c'est par chance » : Acheter parfaitement au bottom : à posteriori c'est évident, dans l'action ça ne se passe pas comme ça. Revendre les parfaits sommets et acheter les parfaits bottoms, « quand vous êtes dans le feu de l'action, si vous arrivez à le faire, c'est uniquement par chance ». Coupe du « enlève-moi du replay » (04:03–04:11). Son écran SOL sous lui. | 03:23–03:34 + 03:34–03:46 + 04:12–04:25 | **v1 rendue le 2026-11-09** : projet `{repo}/clip-convergence/projects/ep04/43-le-bottom-parfait-c-est-par-chance/`, export `{repo}/clip-convergence/exports/ep04/43-le-bottom-parfait-c-est-par-chance.mp4` |
| 44 | « J'ai vendu à 115 et j'ai tenu » : Transparence : il avait partagé sur Telegram avoir vendu 70-80 % de ses SOL à 115 $. Ça a continué de monter, il n'a pas paniqué, il a tenu ; maintenant on est 15-20 % sous sa vente, et il pense re-rentrer une partie parce qu'il reste fondamentalement haussier à moyen terme. Son écran SOL sous lui. « Je vais attendre demain » laissé hors clip. | 03:06–03:15 + 04:29–04:43 + 04:47–04:58 | **v1 rendue le 2026-11-09** : projet `{repo}/clip-convergence/projects/ep04/44-j-ai-vendu-a-115-et-j-ai-tenu/`, export `{repo}/clip-convergence/exports/ep04/44-j-ai-vendu-a-115-et-j-ai-tenu.mp4` |
| 45 | « Milieu de zone ? On attend » : L'or en milieu de zone : c'est toujours plus difficile de prendre des positions, autant attendre les hauts ou les bas de zone. On se rapproche du bas du range. Il voit des gens baissiers, ni tort ni raison, mais il ne comprend pas d'être baissier sur un support comme ça. Son écran or sous lui. | 06:25–06:39 + 06:39–06:46 + 06:46–06:59 | **v1 rendue le 2026-11-09** : projet `{repo}/clip-convergence/projects/ep04/45-milieu-de-zone-on-attend/`, export `{repo}/clip-convergence/exports/ep04/45-milieu-de-zone-on-attend.mp4` |
| 46 | « Baissier sur l'or ? Je ne comprends pas » : Certains sont baissiers sur l'or : il ne comprend pas, personnellement, d'être baissier sur un support comme ça avec le contexte fondamental (guerre qui reprend, macro pas bien, la Russie). « Je ne vois pas pourquoi je serais baissier sur l'or à ce niveau-là. » Son écran or sous lui pendant le contexte. Partage 8 s avec le 45. | 06:52–07:04 + 07:04–07:21 | **v1 rendue le 2026-11-09** : projet `{repo}/clip-convergence/projects/ep04/46-baissier-sur-l-or-je-ne-comprends-pas/`, export `{repo}/clip-convergence/exports/ep04/46-baissier-sur-l-or-je-ne-comprends-pas.mp4` |
| 47 | « Le gold, l'achat de la décennie ? » : Sa position, pas un appel : « pour moi, je me positionne là », capture d'achat dans le replay ; 3 900 ou 4 000, pas de grande différence quand on vise un retour ; « pour moi, le gold, c'est l'achat de la décennie », l'achat de ce Q4 2026, « évidemment pas de conseil en investissement ». Coupe de « si tu n'achètes pas là… BTC 60K / 45K » (07:38–07:49). Son écran or sous lui. | 07:49–07:57 + 07:57–08:07 + 08:13–08:19 + 09:01–09:07 | **v1 rendue le 2026-11-09** : projet `{repo}/clip-convergence/projects/ep04/47-le-gold-l-achat-de-la-decennie/`, export `{repo}/clip-convergence/exports/ep04/47-le-gold-l-achat-de-la-decennie.mp4` |
| 48 | « Réagir plutôt qu'anticiper » : Sa façon d'investir : ne pas anticiper, réagir ; viser l'entrée au meilleur prix pour pouvoir couper si ça s'invalide sans trop perdre. Si tu attends la confirmation, la zone est déjà là, dur de tenir, tu repasses vite en BE voire en perte. Son écran or sous lui pour la démonstration. | 08:26–08:35 + 08:35–08:43 + 08:43–08:58 | **v1 rendue le 2026-11-09** : projet `{repo}/clip-convergence/projects/ep04/48-reagir-plutot-qu-anticiper/`, export `{repo}/clip-convergence/exports/ep04/48-reagir-plutot-qu-anticiper.mp4` |
| 49 | « Qui dit guerre dit pétrole » : Revue de marché : qui dit guerre dit reprise du pétrole ; les commodities, il a toujours refusé d'y toucher, mais c'est intéressant pour lire les tensions : depuis 20 jours le pétrole repart à la hausse. Pas d'avis sur l'or, juste le constat qu'il revient dans la zone du pic de la guerre, « ça se voyait graphiquement ». Son écran pétrole sous lui. | 09:13–09:21 + 09:21–09:35 + 09:35–09:44 + 09:49–09:58 | **v1 rendue le 2026-11-09** : projet `{repo}/clip-convergence/projects/ep04/49-qui-dit-guerre-dit-petrole/`, export `{repo}/clip-convergence/exports/ep04/49-qui-dit-guerre-dit-petrole.mp4` |
| 50 | « Encore un lundi noir ? » : Le programme : revue de marché. On avait annoncé un lundi noir la semaine dernière, au final plutôt ok en début de semaine, puis ça s'est gâté en fin de semaine : « est-ce qu'on a encore un lundi noir ou pas ? » Teaser de l'épisode, plein cadre. | 01:10–01:16 + 01:17–01:30 | **v1 rendue le 2026-11-09** : projet `{repo}/clip-convergence/projects/ep04/50-encore-un-lundi-noir/`, export `{repo}/clip-convergence/exports/ep04/50-encore-un-lundi-noir.mp4` |
| 51 | « Acheter avant le listing » : Ce qu'il partage dans la formation offerte : opérer des cryptos en dehors des échanges, achetées avant d'être listées sur un échange grand public (elles n'y arriveront sans doute jamais, trop petites). Analysées graphiquement comme l'or : pas un memecoin à 10 K, un truc en place depuis des semaines. Écran Axiom (memecoin) hors clip : caméra seule. | 15:06–15:22 + 15:22–15:42 | **v1 rendue le 2026-11-09** : projet `{repo}/clip-convergence/projects/ep04/51-acheter-avant-le-listing/`, export `{repo}/clip-convergence/exports/ep04/51-acheter-avant-le-listing.mp4` |
| 52 | « T'étais sûr que ça allait monter ? » : Sa règle : se placer dans le support, revendre à la résistance, sans chercher plus loin ; des invalidations, « si ça casse, je coupe, j'ai perdu, c'est comme ça ». Aux débutants qui demandent « t'étais sûr que ça allait monter ? » : « non, je ne sais pas », plus de chances de monter que de descendre. Écran Axiom hors clip : caméra seule. | 15:48–15:58 + 15:58–16:05 + 16:05–16:19 | **v1 rendue le 2026-11-09** : projet `{repo}/clip-convergence/projects/ep04/52-t-etais-sur-que-ca-allait-monter/`, export `{repo}/clip-convergence/exports/ep04/52-t-etais-sur-que-ca-allait-monter.mp4` |
| 53 | « Baissier ? Pas en investissement » : Il a du mal à comprendre ceux qui sont baissiers sur l'or : en time frame mineur, ok ; en investissement, non. Et le contexte : les cryptos sont fortement reliées au Nasdaq, avec la hausse des taux potentielle, la guerre et les mid-terms qui arrivent. Plein cadre. | 16:34–16:49 + 16:51–17:03 | **v1 rendue le 2026-11-09** : projet `{repo}/clip-convergence/projects/ep04/53-baissier-pas-en-investissement/`, export `{repo}/clip-convergence/exports/ep04/53-baissier-pas-en-investissement.mp4` |
| 54 | « Faites attention » : La clôture : semaine difficile, trading très difficile, « faites attention si vous ne savez pas ce que vous faites, c'est très difficile de trader actuellement ». Investir : le gold est bien, il est déjà en train de repartir. Plein cadre. | 19:31–19:42 + 19:42–19:52 | **v1 rendue le 2026-11-09** : projet `{repo}/clip-convergence/projects/ep04/54-faites-attention/`, export `{repo}/clip-convergence/exports/ep04/54-faites-attention.mp4` |
| 55 | « Sans Sadek, vous êtes moins virulents » : Teaser : fin de la revue de marché, place au trade de la semaine ; « aujourd'hui on n'est pas sur TikTok avec Sadek, donc vous êtes un peu moins virulents et actifs dans vos questions », mais sur Twitch, allez-y. Caméra seule. | 10:04–10:09 + 10:09–10:22 | **v1 rendue le 2026-11-09** : projet `{repo}/clip-convergence/projects/ep04/55-sans-sadek-moins-virulents/`, export `{repo}/clip-convergence/exports/ep04/55-sans-sadek-moins-virulents.mp4` |
**Fin des clips rendus.**
