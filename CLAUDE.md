# CLAUDE.md

Guide pour Claude Code dans ce repo.

## Projet

YouTube Domination Factory : un ensemble de skills Claude Code qui produit les vidéos de la chaîne YouTube de **Nass Riviera** ([Nassin Crypto](https://www.youtube.com/@NassinCrypto)), chaîne **100 % crypto**. Chaque module `yt-*/` (et `clip-convergence/`) contient un `SKILL.md` (frontmatter `name` + `description`) et parfois `references/` (détails chargés à la demande), `memory/` (choix passés) et `scripts/`.

**Cadre éditorial : `_shared/cadre-nass.md`.** Narrative, avatar, offres, table des liens, ton, règles de fond halal, charte des slides, charte des miniatures, disclaimer. C'est la source unique : tous les skills le lisent, aucun ne le recopie. Le modifier là, et seulement là.

En deux lignes : on achète les cryptos en dehors des échanges, on achète les bons coins, et on ne les achète pas tous les jours. Abandonnés : le challenge 10K → 100K et le wallet public.

## Chemins

Le repo vit à `~/youtube-domination-factory` (Mac) ou `C:\Users\User\youtube-domination-factory` (Windows). Les skills désignent cette racine par `{repo}` et chaque fichier redonne les deux emplacements : une session Claude lit le bon chemin quelle que soit la machine. Les chemins relatifs partent de la racine. Les skills installés (`~/.claude/skills/yt-*`, `~/.claude/skills/clip-convergence`) sont des liens (symlinks Mac, jonctions Windows) vers ce repo : une modif ici est active tout de suite.

Hors git, à recréer sur chaque machine : `yt-analytics/.studio-profile/` (session Chrome de `studio_ctr.py`, connexion une fois), `.env` à la racine (`OPENROUTER_API_KEY`), `yt-analytics/client_secret.json` et `yt-analytics/token.json` (OAuth YouTube, `python3 yt-analytics/auth.py` pour le refaire, en choisissant le compte de la nouvelle chaîne ; il doit être « utilisateur test » de l'application OAuth dans la console Google Cloud).

## Skills

| Skill | Rôle |
|---|---|
| `yt-orchestrator` | Pipeline complet d'une vidéo (« fais une vidéo sur… ») |
| `yt-veille` | Idées de vidéos (veille automatique en pause, voir plus bas) |
| `yt-transcript` | Recherche concurrentielle avant un script |
| `yt-script` | Script + slides HTML (mode dictée « slide après ») |
| `yt-titres-seo` | Titres et mots-clés |
| `yt-miniature` | Briefs de miniatures, portraits ancres édités via OpenRouter, montage PIL (`scripts/`), gabarits Convergence |
| `yt-description` | Description et tags |
| `yt-repurposing` | Découpe d'une vidéo longue : Shorts, thread X, LinkedIn |
| `yt-shorts-script` / `yt-shorts-montage` | Shorts natifs 30-60 s (fondations, méthode de Nass à venir dans `references/`) |
| `clip-convergence` | Shorts tirés du live Convergence : deux caméras, vraies voix, DA « Les deux droites » (pilote EP.03 validé le 2026-10-25) |
| `yt-analytics` | Analyse des stats YouTube |

## Pipeline (yt-orchestrator)

```
0     Init : slug, funnel (TOP/MIDDLE/BOTTOM), JSON depuis le template      conversation principale
0.5   yt-veille (Mode B seulement) → Nass choisit l'idée                    conversation principale, pause
0.75  yt-transcript → brief de recherche                                    agent
1     yt-script, avec les validations de Nass                               conversation principale, pauses
2a    yt-titres-seo                                                         agent
2b/c  yt-miniature + yt-description (ont besoin du titre gagnant)           agents en parallèle
3     Validation titre / miniature / description                           pause
4     yt-repurposing                                                        agent
5     Récap, archive, mémoire des choix                                     conversation principale
```

- **Contexte partagé** : `context/video-context.json`, contrat dans `context/SCHEMA.md`, modèle vide dans `context/video-context.template.json`.
- **Un seul écrivain** : les agents lisent le JSON et écrivent leur section dans `context/runs/<slug>/<section>.json` ; l'orchestrateur fusionne. Personne d'autre n'écrit dans `video-context.json`.
- **Archives** : une vidéo terminée va dans `context/archive/<slug>-<horodatage>.json`. À la publication, Nass donne l'ID YouTube : on remplit `_meta.youtube_video_id` et `_meta.published_at` dans la fiche archivée. C'est par là que `yt-analytics/feedback_analyzer.py` relie les stats aux choix. Une vidéo faite skill par skill, hors orchestrateur, reçoit quand même sa fiche (voir les trois `*-20261013-published.json` de la formation).
- Chaque skill marche aussi seul, appelé directement (workflow interactif).

## Vidéos publiées (période crypto)

Les vidéos crypto sont sur une **nouvelle chaîne, Nassin Crypto** ; l'ancienne chaîne Nass Riviera (période IA) est de l'historique, jamais mélangé aux moyennes crypto. Formation offerte, playlist dans le cadre : `pourquoi-investir-2026` (2026-10-05, `njfEJFd7hQ8`), `comment-devenir-riche` (2026-10-07, `FVajDtrHsPU`), `investissement-on-chain` (2026-10-11, `71HX4YUNrNs`).

Lives Convergence (replays sur la chaîne, miniatures validées dans `shows/emission-live/assets/youtube/miniatures/`) : ép. 01 (live du 8 oct., `ZjNa7wxwFkM`), ép. 03 « Le trading est un jeu de menteurs » (live du 19 oct., `PJaScgDfiMk`, miniature v2 validée le 27 oct.), ép. 04 « L'or, l'achat de la décennie » (Nass seul, tourné le 26 oct., ID à renseigner à la publication).

## Code (Python 3, local)

| Dossier | Scripts | Dépendances |
|---|---|---|
| `yt-analytics/` | `parse_youtube_csv.py` (export FR ou EN), `generate_report.py`, `generate_dashboard.py`, `analyze.py` et `feedback_analyzer.py` (API, OAuth), `auth.py`, `studio_ctr.py` (CTR et impressions lus dans YouTube Studio via Playwright, `uv run`), `studio_retention.py` (pourcentage à 30 s, moments forts et creux de la rétention, même profil Studio) | `yt-analytics/requirements.txt`, uv |
| `yt-miniature/scripts/` | `generate.py` (API Images OpenRouter : génération et édition d'ancre, `--n` ≤ 2, journal des coûts, stdlib), `compare_ref.py` (visage à taille réelle contre la référence), `compose_podcast.py` (deux bustes Convergence : `--lead`, `--grade`), `compose_vs.py` et `compose_vs_brand.py` (face à face, texte en bas, branding Convergence `--theme cream|dark`), `compose_solo_brand.py` (solo Convergence : étoiles dans les yeux, lingots, ancrage par les yeux), `composite.py`, `overlay.py`, `banner.py`, `pfp.py`, `bg_cream.py`, `check.py` | `yt-miniature/scripts/requirements.txt` (Pillow, numpy) |
| `yt-veille/scripts/` | `outliers_rss.py` (outliers des chaînes de référence par flux RSS, stdlib), veille automatique (en pause), tests `pytest` (75 tests) | `yt-veille/scripts/requirements.txt` (inutile pour `outliers_rss.py`) |
| `yt-transcript/scripts/` | `get_transcript.py` (`uv run`, dépendance inline) | uv |
| `clip-convergence/scripts/` | `transcribe.py`, `words.py`, `offset.py` (recalage audio), `presence.py` (fauteuil vide), `build_media.py`, `qa_voice.py`, `face_track.py` (YuNet), `build_screen.py`, `qa_render.py` ; sources = enregistrements OBS du PC Windows | `clip-convergence/scripts/requirements.txt`, ffmpeg |

Vérification rapide après une modif : `git ls-files '*.py' | xargs python3 -m py_compile`, puis `python3 -m pytest -q` dans `yt-veille/scripts`. Les scripts qui lisent `veille.db` tournent sur le VPS ; tous les autres en local.

## Veille automatique : en pause

Nass a désactivé le cron de la veille sur le VPS. **Ne pas la relancer, ne pas le proposer**, sauf demande de sa part. `yt-veille` et `yt-transcript` fonctionnent sans (flux RSS des chaînes de référence via `outliers_rss.py`, sources web, yt-dlp, questions de l'audience).

Pour mémoire : scripts dans `yt-veille/scripts/`, base `veille.db` uniquement sur le VPS (`ssh root@72.62.253.227`, repo dans `/root/youtube-domination-factory`). `context/backlog.json` est vide ; les 81 sujets IA sont archivés dans `context/archive/backlog-ia-2026-03-31.json`.

## Slides (HTML)

Règles complètes dans `yt-script/SKILL.md` et `yt-script/references/slides.md`. L'essentiel :

- Mode dictée : « …slide d'après… » = une slide, mots exacts de Nass ; ce qu'il n'a pas demandé est marqué `[PROP]`.
- Une animation sur mesure par slide clé ; toujours centré ; charte sable/or du cadre.
- `[slug].md` synchronisé avec le deck à chaque changement.
- Graphiques de prix : données réelles, date sous chaque prix.
- Vérifier avant de livrer : captures Playwright + Chrome (chevauchements, contraste, mots orphelins, erreurs JS), `deck.html#N` pour ouvrir la slide N.
- Formation offerte = 3 vidéos : `pourquoi-investir-2026`, `comment-devenir-riche`, `investissement-on-chain` (jamais « Vidéo 3 » sur les slides).

Marqueurs de script : `[FACE CAM]`, `[SCREEN]`, `[DEMO]`, `[B-ROLL]`.

## Miniatures

Charte à part, validée par Nass : photo réaliste de lui, texte haut blanc, texte bas orange `#FF6B35`, tons bleus dans l'image. Le sable/or reste aux slides. Références et retours sur les visages dans `yt-miniature/SKILL.md` et `yt-miniature/memory/`.

Visages générés : méthode sourcée du 2026-10-20 dans `yt-miniature/references/generation-images.md` (portrait ancre validé, édité avec « change only X », jamais régénéré ; une variable par appel ; deux tirages max ; vérification à taille réelle ; assemblage harmonisé). Les demandes de Nass sont traduites dans ce cadre (table dans `yt-miniature/SKILL.md`).

## Titres et scripts

Règles sourcées du 2026-10-20, comparaison avec les sources et les données de la chaîne dans `yt-titres-seo/references/veille-titres-2026-10-20.md` et `yt-script/references/veille-scripts-2026-10-20.md`. Titres : 30 à 60 caractères, promesse dans les 5 premiers mots, suffixe de marque à la fin, formule T9 (question), type searchable / intriguing, retitrage + test A/B d'une vidéo publiée. Scripts : hook à cinq signaux (pas de salutation, promesse du titre reprise, raison de rester, affirmation concrète, pas de bloc de contexte), promesse de titre écrite avant la dictée, 30-45 mots dictés et 3,5-4,5 slides par minute visée, passe rétention en `[PROP]`, repères de rétention lus dans Studio (`yt-analytics/studio_retention.py`), jamais des chiffres de vendeurs.

## Maintenance

- Ajout/suppression de skill ou changement de phase → mettre à jour ce fichier et `README.md`.
- Décisions en attente et dette technique : `TODO.md`.
- Jamais de chemin absolu propre à une machine dans un `.md` : passer par `{repo}`.
