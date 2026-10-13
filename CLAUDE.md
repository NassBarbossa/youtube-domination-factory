# CLAUDE.md

Guide pour Claude Code dans ce repo.

## Projet

YouTube Domination Factory : un ensemble de skills Claude Code qui produit les vidéos de la chaîne YouTube de **Nass Riviera**, chaîne **100 % crypto**. Chaque module `yt-*/` contient un `SKILL.md` (frontmatter `name` + `description`) et parfois `references/` (détails chargés à la demande) et `memory/` (choix passés).

**Cadre éditorial : `_shared/cadre-nass.md`** (narrative, avatar, offres, ton, règles de fond halal, charte, disclaimer). C'est la source unique : tous les skills le lisent, aucun ne le recopie. Le modifier là, et seulement là.

En deux lignes : on achète les cryptos en dehors des échanges, on achète les bons coins, et on ne les achète pas tous les jours. Le challenge 10K → 100K est abandonné.

## Skills

| Skill | Rôle |
|---|---|
| `yt-orchestrator` | Pipeline complet d'une vidéo (« fais une vidéo sur… ») |
| `yt-veille` | Idées de vidéos (veille automatique en pause, voir plus bas) |
| `yt-transcript` | Recherche concurrentielle avant un script |
| `yt-script` | Script + slides HTML (mode dictée « slide après ») |
| `yt-titres-seo` | Titres et mots-clés |
| `yt-miniature` | Briefs de miniatures |
| `yt-description` | Description et tags |
| `yt-repurposing` | Découpe d'une vidéo longue : Shorts, thread X, LinkedIn |
| `yt-shorts-script` / `yt-shorts-montage` | Shorts natifs 30-60 s (fondations, méthode de Nass à venir dans `references/`) |
| `yt-analytics` / `yt-calendrier` | Analyse des stats, calendrier éditorial |

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
- Chaque skill marche aussi seul, appelé directement (workflow interactif).
- Chemins relatifs = relatifs à la racine du repo.

## Veille automatique : en pause

Nass a désactivé le cron de la veille sur le VPS. **Ne pas la relancer, ne pas le proposer**, sauf demande de sa part. `yt-veille` et `yt-transcript` fonctionnent sans (sources web, yt-dlp, questions de l'audience).

Pour mémoire : scripts dans `yt-veille/scripts/`, base `veille.db` uniquement sur le VPS (`ssh root@72.62.253.227`, repo dans `/root/youtube-domination-factory`). Les scripts qui lisent `veille.db` s'exécutent sur le VPS ; les autres (yt-analytics, `get_transcript.py`) en local.

## Slides (HTML)

Règles complètes dans `yt-script/SKILL.md` et `yt-script/references/slides.md`. L'essentiel :

- Mode dictée : « …slide d'après… » = une slide, mots exacts de Nass ; ce qu'il n'a pas demandé est marqué `[PROP]`.
- Une animation sur mesure par slide clé ; toujours centré ; charte du cadre.
- `[slug].md` synchronisé avec le deck à chaque changement.
- Graphiques de prix : données réelles, date sous chaque prix.
- Vérifier avant de livrer : captures Playwright + Chrome (chevauchements, contraste, mots orphelins, erreurs JS), `deck.html#N` pour ouvrir la slide N.
- Formation offerte = 3 vidéos : `pourquoi-investir-2026`, `comment-devenir-riche`, `investissement-on-chain` (jamais « Vidéo 3 » sur les slides).

Marqueurs de script : `[FACE CAM]`, `[SCREEN]`, `[DEMO]`, `[B-ROLL]`.

## Maintenance

- Les skills installés (`~/.claude/skills/yt-*`) sont des jonctions vers ce repo : une modif ici est active tout de suite.
- Ajout/suppression de skill ou changement de phase → mettre à jour ce fichier et `README.md`.
