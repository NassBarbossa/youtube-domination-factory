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
