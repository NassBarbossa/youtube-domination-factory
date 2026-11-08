# Convergence EP.03 — live du 2026-10-19

## Sources

| Rôle | Fichier | Format |
|---|---|---|
| Image et son des clips | `~/Videos/2026-10-19 15-13-23 vertical - son egalise.mkv` | 1080 × 1920, 60 i/s, 3 105,7 s, 4,7 Go (non égalisé : `… vertical.mkv`) |
| Brut 16:9 | `~/Videos/2026-10-19 15-13-21 - son egalise.mp4` | 1920 × 1080, 60 i/s, 3 016,1 s |
| Replay monté (local) | `~/Videos/Convergence ep03 - replay monte.mp4` | passages gardés : `~/Videos/montage-ep03/keep.json` |
| YouTube | `PJaScgDfiMk` (`~/Videos/NassRiviera/youtube/PJaScgDfiMk.mp4`) | repère de temps seulement. Ce n'est pas le montage de `keep.json` (voir les décalages) |
| Anciens clips (19/10) | `~/Videos/clips-ep03/` | style ffmpeg/ASS + B-roll, avant la DA. **Un clip « altseason » existe déjà**, avec une accroche réécrite et le disclaimer à l'image : demander à Nass s'il a été publié avant de refaire le 10 |

## Décalages

| Mesure | Résultat |
|---|---|
| brut → vertical | **vertical = brut − 1,76 s**, constant (`offset.py` à 1695, 1720, 2200 et 2270 s : scores 0,98 à 0,999) |
| brut → YouTube | **YouTube = brut − 245,6 s** à 2185, 2200 et 2270 s (scores 0,97 à 0,99), y compris de part et d'autre d'une coupe de `keep.json`. Le pilote avait noté ≈ −244 s plus tôt dans l'émission : à remesurer au passage choisi |

## Mises en page et zones (vertical)

L'émission alterne deux mises en page :

| Mise en page | Fichier de zones | Nass | Sadek | Écran |
|---|---|---|---|---|
| trois bandes (Nass / écran / Sadek) | `zones-trois-bandes.json` | `[26, 26, 1028, 514]` | `[26, 1284, 1028, 516]` | `[20, 740, 880, 480]`, affiché en 1012 × 552 |
| fullcam (deux grandes caméras) | `zones-fullcam.json` | `[26, 26, 1028, 828]` | `[26, 984, 1028, 822]` | — |

Les zones fullcam ont été vérifiées à l'image (2198,24 s) : elles restent à l'intérieur des étiquettes « NASS · SHINSEKAI ALPHA », « SADEK · IMPRIMANTE » et du badge LIVE. Les états de la DA sont calés sur les trois bandes ; pour la fullcam, ils sont à recaler (`references/deux-droites.md`).

## Transcription

`~/Videos/montage-ep03/transcript.json` (faster-whisper, 1 262 phrases), **en temps du brut 16:9**. Dans les `cut.json`, `raw_to_source` vaut −1.76. Pour `presence.py`, on passe `--offset -1.76`.

## Candidats

Minutages : YouTube, puis brut (temps de la transcription).

| N° | Passage, idée | Minutage | Qui | Mise en page | Présence | Cadre | Statut |
|---|---|---|---|---|---|---|---|
| 08 | « L'or est en solde » : −25 % sous le record ; le prix d'entrée exact compte peu pour un investisseur long terme | YT 24:07–24:48 + 26:06–27:13 · brut 1690,9–1870,5 | Sadek puis Nass | trois bandes | ok / ok | « impossible » et « guerre atomique » coupés | **fait** : pilote v2 validé le 2026-10-25. Projet `{repo}/yt-shorts-montage/projects/recycles/08-or-en-solde/`, export `{repo}/yt-shorts-montage/exports/recycles/08-or-en-solde.mp4`. Légende avec disclaimer à écrire à la publication |
| 09 | « Apprends-moi à faire de l'oseille » : compétence monnayable, vivre moins cher, un pourcentage dans l'or, le Bitcoin, le S&P 500 | YT 29:26–30:50 · brut ≈ 2012–2080 | Nass | trois bandes | **Sadek absent** (0 visage sur 68 images) | — | à décider avec Nass : montrer le deck à la place de Sadek, ou abandonner. Ancienne SPEC : `{repo}/yt-shorts-montage/projects/recycles/09-faire-de-l-oseille/` |
| 10 | « Altseason » : c'est un problème de définition ; un altcoin, c'est tout ce qui n'est pas Bitcoin ; la liquidité se concentre dans quelques actifs | YT 32:16–33:51 · brut 2181,7–2276,5 | Nass seul | **fullcam** | ok / ok (zones fullcam) | **memecoins** dans le passage (2214–2220, 2260–2268) : les couper et les signaler à Nass ; tokens nommés et prédiction « pas comme 2021 » coupés ; pas de FOMO | à faire. Plan proposé par l'agent de test du skill (3 morceaux, ~42,5 s, états B / B+) |

**Écartés (cadre) :**
- le trading de Sadek et sa communauté « l'Imprimante » ;
- la partie politique ;
- « l'or n'ira pas à 2 100, c'est impossible » ;
- la « guerre atomique » ;
- le trading avec liquidation.

**Repérage du 2026-10-27 (Mac, temps YouTube)** : candidats 11 à 21 dans `context/transcripts/passages-2026-10-27.md` (texte exact + pourquoi : `passages-detail-2026-10-27.md`) (« le trading est un jeu de menteurs » 40:13–41:07, deux règles anti-instinctives, budget pour commencer, supports / résistances, « l'investissement c'est facile, le trading c'est dur », range et indécision). Transcription YouTube : `context/transcripts/PJaScgDfiMk-words.json` (YouTube ≈ brut − 245,6 s au passage mesuré, à remesurer).

## Clips rendus (série du 2026-11-09, sans validation par clip, à revoir en lot)

Source : replay YouTube `PJaScgDfiMk` (720p, 30 i/s), seule source présente sur ce Mac (bruts OBS sur le PC Windows). Trois mises en page selon le moment : 18:00–27:20 ronds caméra + TradingView ; 27:20–28:20 et 31:46,8–38:20 fullcam (deux fenêtres) ; 28:20–31:46,8 ronds + slide ; 38:20–fin « punk » (la fenêtre de Nass montre son avatar, Sadek seul à l'image). Caméra de Sadek noire 31:54–32:02 et 41:54–42:58 : candidats 12 (« trader moins ») et 21 (« venu au trading ») écartés pour ça, remplacés par « Payer pour apprendre ? » et « Une bonne situation financière ? ». Candidat 08 (« L'or est en solde ») refait en DA « Les deux droites » (clip 60).

| N° | Clip | Coupe (YouTube) | Statut |
|---|---|---|---|
| 56 | « Un range bien dégoûtant » : Nass sur le graphique : depuis le 28 septembre, rien ne s'est passé, on est dans un range bien dégoûtant ; un peu de résilience acheteuse, on le casse peut-être aujourd'hui, mais « on n'est pas sorti de l'auberge ». Son écran TradingView sous lui. | 18:00–18:05 + 18:07–18:18 + 18:20–18:33 | **v1 rendue le 2026-11-09** : projet `{repo}/clip-convergence/projects/ep03/56-un-range-bien-degoutant/`, export `{repo}/clip-convergence/exports/ep03/56-un-range-bien-degoutant.mp4` |
| 57 | « Pile ou face » : Sadek sur le range : « on s'est fait éclater » la semaine d'avant, trop d'indécision, à l'achat comme à la vente tu es touché, c'est pile ou face ; décision de se concentrer sur l'éducatif ; « j'ai pas envie de trader tant qu'on sort pas de cette zone, j'ai besoin d'une tendance ». Coupe de « je pourrais te montrer les retraits » (19:06–19:18). | 18:41–18:48 + 18:48–19:01 + 19:02–19:06 + 19:18–19:24 | **v1 rendue le 2026-11-09** : projet `{repo}/clip-convergence/projects/ep03/57-pile-ou-face/`, export `{repo}/clip-convergence/exports/ep03/57-pile-ou-face.mp4` |
| 58 | « Si les actions chutent ? » : Nass demande les corrélations ; Sadek : si les actions chutent, il voit l'or monter, le Bitcoin continuer une montée tranquille en escalier, une rotation de liquidités ; les actions ne chutent jamais vraiment, elles corrigent. Coupe avant « vous ne reverrez jamais le NAS100 à 16 000 » (certitude). | 21:30–21:33 + 21:33–21:51 + 21:51–21:59 | **v1 rendue le 2026-11-09** : projet `{repo}/clip-convergence/projects/ep03/58-si-les-actions-chutent/`, export `{repo}/clip-convergence/exports/ep03/58-si-les-actions-chutent.mp4` |
| 59 | « Au milieu de range, on temporise » : Sadek, côté investissement : acheter sur les supports, revendre sur les résistances ; au milieu de range, ça peut partir dans les deux sens, ce n'est pas une zone où se presser et cliquer partout : temporiser, analyser, attendre une direction claire et la suivre. Coupe de « ou alors shorter pour ceux qui shortent ». L'écran or de Nass pendant l'explication. | 23:27–23:39 + 23:40–23:46 + 23:46–23:58 + 23:59–24:08 | **v1 rendue le 2026-11-09** : projet `{repo}/clip-convergence/projects/ep03/59-au-milieu-de-range-on-temporise/`, export `{repo}/clip-convergence/exports/ep03/59-au-milieu-de-range-on-temporise.mp4` |
| 60 | « L'or est en solde » : Sadek : pas une question de zone, une question de moment ; en investissement, acheter de l'or à ce prix est un très bon prix, en trading avec peu de marge de manœuvre, attention. Nass sur son graphique : du point haut on est sur une correction de 30 %, « les soldes » entre guillemets ; en achat long terme, se positionner là n'est pas très risqué ; le prix d'entrée exact n'est pas le plus important quand vous êtes investisseur. Reprise en DA du pilote 08 (validé le 2026-10-25). « L'or n'ira pas à 2 100, c'est impossible » (24:51) et la guerre atomique restent hors clip. | 24:14–24:23 + 24:28–24:40 + 26:17–26:27 + 26:28–26:39 + 27:08–27:13 | **v1 rendue le 2026-11-09** : projet `{repo}/clip-convergence/projects/ep03/60-l-or-est-en-solde/`, export `{repo}/clip-convergence/exports/ep03/60-l-or-est-en-solde.mp4` |
| 61 | « Apprends-moi à faire de l'oseille » : Question du chat lue par Nass : deux points de vue ; Sadek, focalisez-vous sur le trading ; Nass, développer des compétences monnayables, une activité digitale, et pendant que vous charbonnez, un pourcentage de vos rentrées dans les marchés : l'or, le Bitcoin, le S&P 500. Coupe de « partir de la France… en Asie avec 600–800 € » (30:04–30:33). | 29:28–29:35 + 29:35–29:42 + 29:42–29:50 + 30:33–30:46 | **v1 rendue le 2026-11-09** : projet `{repo}/clip-convergence/projects/ep03/61-apprends-moi-a-faire-de-l-oseille/`, export `{repo}/clip-convergence/exports/ep03/61-apprends-moi-a-faire-de-l-oseille.mp4` |
| 63 | « C'est quoi l'altseason ? » : « Quand aura lieu l'altseason ? » : le commentaire qui trigger Nass depuis des années, parce que c'est un problème de définition : un altcoin, c'est tout coin alternatif à Bitcoin. Aujourd'hui il y a une inflation des cryptos (tout le monde peut créer la sienne en une seconde), la liquidité ne peut plus aller partout, elle se concentre dans quelques actifs. Coupes : memecoins à 5 000 de market cap (32:47–32:57, signalé), tokens nommés et « pas comme 2021 » (32:57–33:34). | 32:16–32:20 + 32:24–32:27 + 32:27–32:39 + 33:34–33:50 | **v1 rendue le 2026-11-09** : projet `{repo}/clip-convergence/projects/ep03/63-c-est-quoi-l-altseason/`, export `{repo}/clip-convergence/exports/ep03/63-c-est-quoi-l-altseason.mp4` |
| 62 | « Budget pour commencer ? » : Question du chat : budget pour commencer ? Nass, en investissement : 10 à 20 % de votre salaire par mois ; Sadek, en trading : le moins possible, « vous allez perdre de l'argent au début », ça prend les bonnes habitudes, n'allez pas mettre tout votre capital. Fin avant le passage en fullcam (31:46,8) ; « ne faites pas cette erreur-là » (31:46,5) tombe sur le changement de mise en page, non repris. | 31:11–31:23 + 31:23–31:27 + 31:27–31:37 + 31:38–31:43 | **v1 rendue le 2026-11-09** : projet `{repo}/clip-convergence/projects/ep03/62-budget-pour-commencer/`, export `{repo}/clip-convergence/exports/ep03/62-budget-pour-commencer.mp4` |
| 64 | « L'investissement c'est facile, le trading c'est dur » : Question du chat : est-ce que c'est dur le trading ? Nass : l'investissement c'est facile, le trading c'est dur. Sadek : totalement d'accord, très difficile, émotionnellement (« si des fois je suis un peu à cran, c'est que c'est très difficile »), jamais il dira que c'est facile ; par contre quand ça paye et que tu sais minimiser ton exposition, c'est génial. Son trade en lots (34:58) reste hors clip. | 34:29–34:33 + 34:35–34:46 + 34:46–34:58 | **v1 rendue le 2026-11-09** : projet `{repo}/clip-convergence/projects/ep03/64-le-trading-c-est-dur/`, export `{repo}/clip-convergence/exports/ep03/64-le-trading-c-est-dur.mp4` |
**Fin des clips rendus.**
