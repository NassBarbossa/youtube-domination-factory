---
name: yt-orchestrator
description: Pilote la production complète d'une vidéo YouTube de la chaîne crypto de Nass Riviera, du sujet au repurposing (recherche, script, titres, miniature, description, Shorts/X/LinkedIn), avec les validations de Nass et un fichier de contexte partagé. Déclencheurs : « fais une vidéo sur… », « lance le pipeline », « vidéo complète sur… », « crée une vidéo sur… », « make a video about… », « run the pipeline ». Pas pour chercher des idées ou un sujet de vidéo (« trouve-moi des idées », « sujet de vidéo », « quoi filmer ») → yt-veille ; pas pour une seule étape (script, titre, miniature…) → le skill de cette étape.
---

# yt-orchestrator

**Cadre** : lis d'abord `C:\Users\User\youtube-domination-factory\_shared\cadre-nass.md` (narrative, avatar, offres, ton, règles de fond, charte). Il prime sur ce fichier.

Chemins relatifs = relatifs à la racine du repo `C:\Users\User\youtube-domination-factory`. Contrat du fichier partagé : `context/SCHEMA.md` (sections, champs, statuts). Structure vide : `context/video-context.template.json`.

Tu enchaînes les skills dans l'ordre, tu es le **seul à écrire** dans `context/video-context.json`, et tu t'arrêtes là où Nass doit décider.

**Garde-fou** : si le sujet demandé touche au levier, aux futures, au short, au lending/« earn » à intérêt, au jeu d'argent ou aux memecoins, ne lance pas le pipeline : signale-le à Nass et propose un angle compatible avec le cadre.

## Séquence

| Phase | Qui | Où | Pause |
|---|---|---|---|
| 0 | orchestrateur : slug, mode, funnel, JSON | conversation principale | oui (funnel) |
| 0.5 | yt-veille (Mode B seulement) | conversation principale | oui (choix de l'idée) |
| 0.75 | yt-transcript | agent | non |
| 1 | yt-script (1a structure → 1b écriture) | conversation principale | oui (validations de yt-script) |
| 2a | yt-titres-seo | agent | non |
| 2bc | yt-miniature + yt-description | 2 agents en parallèle | non |
| 3 | orchestrateur : relecture rapide + récap | conversation principale | oui (validation) |
| 4 | yt-repurposing | agent | non |
| 5 | orchestrateur : récap, export, mémoire | conversation principale | non |

`_meta.pipeline_step` = dernière phase **terminée** (`"0"`, `"0.5"`, `"0.75"`, `"1"`, `"2a"`, `"2bc"`, `"3"`, `"4"`, `"5"`). Tu ne l'écris qu'une fois la phase finie, avec une entrée dans `pipeline_log` et `_meta.updated_at`.

## Démarrage et reprise (règle unique)

Lis `context/video-context.json` (s'il n'existe pas, copie le template).

- `_meta.status == "completed"` → copie le fichier dans `context/archive/<slug>-<YYYYMMDD-HHMMSS>.json`, puis remplace-le par le template et démarre la Phase 0.
- Sinon, si `_meta.slug` est renseigné → dis à Nass où en est le pipeline (`slug`, dernière phase finie) et propose de **reprendre à la phase suivante** ou de **redémarrer** (redémarrer = archiver de la même façon, puis template).
- Sinon (fichier vide) → Phase 0.

## Phase 0 — Initialisation

1. **Mode** : A si Nass donne un sujet (« Fais une vidéo sur comment acheter sa première crypto en dehors des échanges », « Lance le pipeline sur : comment je reconnais un bon coin ») ; B s'il demande d'abord des idées dans le cadre d'une vidéo complète (« Lance le pipeline, mais trouve d'abord le sujet »).
2. **Funnel** : demande à Nass TOP, MIDDLE ou BOTTOM, en une ligne chacun (durée, profondeur, CTA du cadre). En Mode B, il peut répondre « après le choix de l'idée » : tu le redemandes alors en fin de Phase 0.5.
3. Lis les leçons existantes (voir `references/feedback-loop.md`, § Usage en Phase 0).
4. Écris : `_meta.slug` (kebab-case depuis le sujet ; en Mode B, `null` jusqu'au choix de l'idée), `_meta.mode`, `_meta.status = "in_progress"`, `_meta.triggered_by = "user"`, `_meta.created_at`, `request.raw_input` (phrase de Nass telle quelle), `request.topic`, `request.funnel`, puis `pipeline_step = "0"`.
5. Annonce en une ligne : sujet, slug, funnel, phase suivante.

## Phase 0.5 — Idées (Mode B seulement)

Dans la conversation principale : invoque le skill `yt-veille` (outil Skill) en lui donnant `request.raw_input`. La veille automatique est en pause (désactivée par Nass) : ne pas la relancer ni le proposer ; yt-veille travaille avec ses sources sans cron. Il présente des idées, **Nass choisit**.

Puis écris `veille.ideas[]` et `veille.selected_idea` (`{title, format, angle, hook_suggestion}`), `veille.status = "completed"`, le slug et `request.topic` d'après l'idée choisie, le funnel s'il restait à décider, et `pipeline_step = "0.5"`.

## Phase 0.75 — Recherche concurrente (agent)

Lance un agent avec ce prompt (remplace `<slug>`) :

> Mode autonome, lancé par yt-orchestrator. Lis `C:\Users\User\youtube-domination-factory\yt-transcript\SKILL.md` et applique sa section mode autonome. Entrée : `context/video-context.json` en lecture seule (`request`, `veille.selected_idea`). Cherche 3 à 5 vidéos concurrentes sur le sujet : DB veille sur le VPS si elle répond ; sinon (DB injoignable, vide ou sans résultat sur ce sujet), recherche YouTube via le web ou yt-dlp. Ne relance pas la veille automatique. Récupère les transcripts, écris le brief dans `context/transcripts/<slug>/research-brief.md` et la section `research` dans `context/runs/<slug>/research.json` (chaque `key_facts[]` = `{fact, verified, source}` ; `verified: true` seulement avec une source primaire). N'écris jamais dans `context/video-context.json`. Ne pose aucune question : ce qui manque va dans `open_questions[]`. Renvoie le JSON de la section dans ton message final.

Fusion, puis `pipeline_step = "0.75"`. Si aucune vidéo concurrente n'est trouvée, c'est une info (terrain vierge) : la phase est quand même terminée.

## Phase 1 — Script (conversation principale)

yt-script a besoin de Nass (structure 1a → validation → écriture 1b, hook, sections dictées) : il ne tourne pas en agent.

1. Invoque le skill `yt-script` (outil Skill) en lui indiquant : mode pipeline, sujet `request.topic`, funnel `request.funnel` (déjà choisi, ne pas le redemander), idée `veille.selected_idea` si Mode B, brief `research.brief_file` et `research.angles_missing[]`.
2. Suis son workflow avec ses pauses de validation. Après la structure validée, tu peux écrire `script.status = "structure_ready"` (utile en cas de reprise).
3. Une fois `yt-script/outputs/<slug>.md` (et `-visual.html`) écrits, remplis `script.*` (voir SCHEMA ; reprends `context/runs/<slug>/script.json` si yt-script l'a produit), `script.status = "completed"`, puis `pipeline_step = "1"`.

## Phase 2a — Titres (agent)

> Mode autonome, lancé par yt-orchestrator. Lis `C:\Users\User\youtube-domination-factory\yt-titres-seo\SKILL.md` et applique sa section mode autonome. Entrée : `context/video-context.json` en lecture seule (`request`, `script`, `research.angles_missing`). Produis le nombre de titres défini dans yt-titres-seo, choisis `winning_title`, donne `primary_keyword` et `secondary_keywords[]`. Écris la section dans `context/runs/<slug>/titres_seo.json`, jamais dans `context/video-context.json`. Pas de question : `open_questions[]`. Renvoie le JSON dans ton message final.

Fusion, puis `pipeline_step = "2a"`.

## Phase 2bc — Miniature et description (2 agents en parallèle)

Lance les deux agents dans le même message, une fois `titres_seo` fusionné.

> Mode autonome, lancé par yt-orchestrator. Lis `C:\Users\User\youtube-domination-factory\yt-miniature\SKILL.md` et applique sa section mode autonome. Entrée : `context/video-context.json` en lecture seule (`script`, `titres_seo.winning_title`, `titres_seo.primary_keyword`). Le texte de la miniature complète le titre, il ne le répète pas ; tout chiffre affiché est réel, avec `figure_source`. Écris la section dans `context/runs/<slug>/miniature.json`, jamais dans `context/video-context.json`. Pas de question : `open_questions[]`. Renvoie le JSON dans ton message final.

> Mode autonome, lancé par yt-orchestrator. Lis `C:\Users\User\youtube-domination-factory\yt-description\SKILL.md` et applique sa section mode autonome. Entrée : `context/video-context.json` en lecture seule (`request.funnel`, `script`, `research`, `titres_seo`). Liens d'offres en placeholders `[lien …]`. Écris la section dans `context/runs/<slug>/description.json`, jamais dans `context/video-context.json`. Pas de question : `open_questions[]`. Renvoie le JSON dans ton message final.

Attends les deux notifications de fin, fusionne les deux sections, puis `pipeline_step = "2bc"`. Si un seul des deux échoue, relance-le seul (voir Erreurs).

## Phase 3 — Validation

1. **Relecture rapide** (sans l'annoncer comme une étape) : titre, texte et visuel de la miniature, description, relus contre les règles de fond du cadre (vocabulaire de jeu ou de levier, chiffres sans source, memecoin, promesse de gain, challenge abandonné, disclaimer présent une fois dans la description). Un problème → corrige-le en relançant l'agent concerné, ou signale-le à Nass dans le récap.
2. Présente :

   ```
   Phase 3 — validation

   Titre : [titres_seo.winning_title]
   Autres titres : [titres_seo.all_titles]
   Miniature : [recommended_concept.name] — [layout], texte : [text_overlay], palette : [color_palette]
   Description (150 premiers caractères) : [description.first_150_chars]
   Tags : [5 premiers tags]
   Questions ouvertes : [open_questions des trois sections, s'il y en a]
   Points à revoir : [seulement si la relecture a trouvé quelque chose]

   « OK » pour valider, ou « modifie X ».
   ```

3. Modification demandée → relance le seul agent concerné avec la consigne de Nass (si le titre change, relance aussi miniature et description), fusionne, reviens au récap.
4. OK explicite de Nass → `titres_seo.status`, `miniature.status`, `description.status` = `"validated"`, puis `pipeline_step = "3"`.

## Phase 4 — Repurposing (agent)

> Mode autonome, lancé par yt-orchestrator. Lis `C:\Users\User\youtube-domination-factory\yt-repurposing\SKILL.md` et applique sa section mode autonome. Entrée : `context/video-context.json` en lecture seule (`request.funnel`, `script`, `titres_seo`, `miniature`, `description`, tous validés). Produis `shorts[]`, `x_thread_full`, `linkedin_full` et les autres champs de la section. Écris-la dans `context/runs/<slug>/repurposing.json`, jamais dans `context/video-context.json`. Pas de question : `open_questions[]`. Renvoie le JSON dans ton message final.

Fusion, puis `pipeline_step = "4"`.

## Phase 5 — Récap, export, mémoire

1. **Export** : crée deux documents via Google Drive (`create_file`) ou Claude Docs, selon ce qui est connecté — `[Script] {winning_title}` (contenu de `script.file_path`) et `[Repurposing] {winning_title}` (Shorts, thread X, LinkedIn). Partage avec `quentin.riviere69@gmail.com`. Liens dans `script.google_doc_url` et `repurposing.google_doc_url`. Rien de connecté → le dire et donner les chemins locaux.
2. **Mémoire** (détail et formats : `references/feedback-loop.md`) : ajoute une entrée avec `niche: "crypto"` dans `yt-script/memory/choices.json`, `yt-titres-seo/memory/choices.json`, `yt-miniature/memory/choices.json`, et `yt-veille/memory/choices.json` en Mode B ; ajoute le run dans `yt-orchestrator/memory/pipeline_runs.json`.
3. Écris `_meta.status = "completed"`, `_meta.completed_at`, `pipeline_step = "5"`. L'archivage se fait au prochain démarrage (règle unique ci-dessus).
4. Récap à Nass :

   ```
   Pipeline terminé — [request.topic]

   Script : [word_count] mots, ~[reading_time_min] min — [file_path]
   Titre : [winning_title]
   Miniature : [recommended_concept.name]
   Mots-clés : [primary_keyword], [secondary_keywords]
   Repurposing : [N] Shorts, thread X, post LinkedIn
   Documents : [liens]

   À la publication, donne-moi l'ID ou l'URL de la vidéo pour relier les stats.
   ```

5. Quand Nass donne l'ID : écris `_meta.youtube_video_id` (et `published_at` s'il le donne) dans `context/video-context.json`, ou dans le fichier archivé s'il a déjà été archivé, ainsi que dans l'entrée de `pipeline_runs.json`.

## Fusion d'une section

1. Lis `context/runs/<slug>/<section>.json` (à défaut, le JSON du message final de l'agent).
2. Vérifie que c'est du JSON valide, que `status == "completed"` et que les champs clés de `context/SCHEMA.md` sont présents.
3. Remplace la section dans `context/video-context.json`, ajoute l'entrée `pipeline_log` `{phase, agent, status, timestamp, notes}`, mets à jour `_meta.updated_at`.
4. Remonte les `open_questions[]` à Nass au prochain point de pause (au plus tard en Phase 3).

## Erreurs

Un agent échoue ou renvoie une section invalide : log `{phase, agent, status: "failed", error, timestamp, retries}` dans `pipeline_log`, ne touche pas à `pipeline_step`, et propose à Nass : relancer l'agent seul, continuer sans (si la phase n'est pas bloquante, statut `skipped`), ou arrêter (`_meta.status = "failed"`).

## Hors pipeline

Chaque skill appelé directement par Nass garde son workflow interactif et n'écrit pas dans `context/video-context.json`.
