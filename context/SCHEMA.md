# Contrat de `context/video-context.json`

Source unique du format du fichier partagé par le pipeline vidéo. Structure vide : `context/video-context.template.json`. Les chemins sont relatifs à la racine du repo ; `{repo}` = racine du dépôt youtube-domination-factory (Mac : `~/youtube-domination-factory` · Windows : `C:\Users\User\youtube-domination-factory`).

## Règles d'écriture

- **Un seul écrivain** : `yt-orchestrator`. Il crée le fichier depuis le template, fusionne les sections et tient `_meta` et `pipeline_log`.
- **Agents lancés en autonome** (yt-transcript, yt-titres-seo, yt-miniature, yt-description, yt-repurposing) : lisent `context/video-context.json` en lecture seule, écrivent leur section dans `context/runs/<slug>/<section>.json` (ex. `titres_seo.json`, contenu = l'objet de la section, sans la clé englobante) et renvoient ce JSON dans leur message final. Ils ne posent pas de question : ce qui manque va dans `open_questions[]`.
- **Skills lancés dans la conversation principale** (yt-veille en Phase 0.5, yt-script en Phase 1) : ils dialoguent avec Nass ; l'orchestrateur écrit ensuite leur section.
- **Appel direct par Nass** (hors pipeline) : les skills n'écrivent pas dans ce fichier.

## Statuts

| Champ | Valeurs |
|---|---|
| `_meta.status` | `null` (fichier vide) · `in_progress` · `completed` · `failed` |
| `<section>.status` | `null` (pas commencé) · `in_progress` · `structure_ready` (script seulement, entre 1a et 1b) · `completed` · `validated` (après la Phase 3) · `failed` · `skipped` |
| `_meta.pipeline_step` | dernière phase **terminée**, en chaîne : `"0"`, `"0.5"`, `"0.75"`, `"1"`, `"2a"`, `"2bc"`, `"3"`, `"4"`, `"5"` ; `null` tant que rien n'est fini |

Ordre des phases : `0 → 0.5 (Mode B seulement) → 0.75 → 1 → 2a → 2bc → 3 → 4 → 5`.

Reprise (règle unique, appliquée par l'orchestrateur au démarrage) : si `_meta.status == "completed"`, archiver le fichier dans `context/archive/<slug>-<YYYYMMDD-HHMMSS>.json` puis repartir du template ; sinon, si un slug existe, proposer de reprendre à la phase qui suit `pipeline_step` (ou de redémarrer, ce qui archive de la même façon).

## Sections

### `_meta` — orchestrateur

| Champ | Type | Note |
|---|---|---|
| `version` | string | `"3.0"` |
| `slug` | string | kebab-case, ex. `premiere-crypto-hors-echange` ; en Mode B, fixé après le choix de l'idée |
| `status`, `pipeline_step` | string | voir Statuts |
| `mode` | `"A"` \| `"B"` | A : sujet donné ; B : recherche d'idées d'abord |
| `triggered_by` | `"user"` | |
| `created_at`, `updated_at`, `completed_at` | ISO 8601 | |
| `youtube_video_id` | string \| null | rempli à la publication (Nass donne l'ID ou l'URL), sert à relier les stats YouTube aux choix du pipeline. Peut être ajouté après coup dans le fichier archivé. |
| `published_at` | ISO 8601 \| null | date de publication, si connue |

### `request` — orchestrateur (Phase 0)

`raw_input` (phrase de Nass telle quelle), `topic`, `funnel` (`"TOP"` \| `"MIDDLE"` \| `"BOTTOM"`, demandé à Nass en Phase 0), `language` (`"fr"`).

### `veille` — yt-veille, conversation principale (Phase 0.5, Mode B)

- `ideas[]` : `{title, format, angle, hook_suggestion}` + champs optionnels de yt-veille (`length`, `seo_keywords[]`, `scores`, `halal_check`).
- `selected_idea` : l'élément de `ideas[]` choisi par Nass, avec au minimum `{title, format, angle, hook_suggestion}`.
- `open_questions[]`.

### `research` — yt-transcript, agent (Phase 0.75)

- `videos_analyzed` (int), `transcripts[]` : `{video_id, channel, title, date, file}`.
- `key_facts[]` : `{fact, verified, source}` — `verified: true` seulement si le fait est confirmé par une source primaire (doc officielle, explorateur on-chain, données de prix datées) notée dans `source` ; un fait repris d'une vidéo concurrente sans confirmation reste `verified: false` avec la vidéo en `source`.
- `angles_covered[]`, `angles_missing[]`, `recommended_angle`, `synthesis`, `brief_file` (`context/transcripts/<slug>/research-brief.md`), `open_questions[]`.

### `script` — yt-script, conversation principale (Phase 1)

`slug`, `funnel` (copie de `request.funnel`), `file_path` (`yt-script/outputs/<slug>.md`), `visual_path` (`yt-script/outputs/<slug>-visual.html`), `word_count`, `reading_time_min`, `structure` `{hook, sections[{title, key_points[]}], timestamps_raw[{time, label}], shorts_moments[{start, end, description}]}`, `google_doc_url`, `open_questions[]`.

### `titres_seo` — yt-titres-seo, agent (Phase 2a)

`all_titles[]` (le nombre défini dans yt-titres-seo), `winning_title`, `primary_keyword`, `secondary_keywords[]`, `open_questions[]`.

### `miniature` — yt-miniature, agent (Phase 2b)

`recommended_concept` `{name, layout, main_visual, text_overlay, font_style, color_palette[], face_expression, emotion_conveyed, contrast_trick, figure_source, …}` — `text_overlay` ne répète pas `winning_title` ; tout chiffre affiché est réel, avec sa source dans `figure_source` (sinon `null`). `rejected_concepts[{name, reason}]`, `scoring`, `open_questions[]`.

### `description` — yt-description, agent (Phase 2c)

`description_full`, `first_150_chars`, `hook_framework`, `tags[]`, `enriched_keywords[]`, `sources[]`, `cta_type`, `open_questions[]`. Liens d'offres en placeholders `[lien …]` tant que Nass ne les a pas donnés.

### `repurposing` — yt-repurposing, agent (Phase 4)

`shorts[]` `{number, title, hook, content, punchline, text_overlay, source_timestamp}`, `x_thread_hook`, `x_thread_full`, `x_reply_link`, `linkedin_hook`, `linkedin_full`, `linkedin_format_bonus`, `posting_schedule`, `google_doc_url`, `open_questions[]`.

### `pipeline_log[]` — orchestrateur

Une entrée par phase terminée ou en erreur : `{phase, agent, status, timestamp, notes, error?, retries?}`.

## Hors contrat

- Pas de section `compliance` : il n'y a pas de phase conformité. L'orchestrateur relit rapidement titre, miniature et description en Phase 3 contre les règles de fond de `_shared/cadre-nass.md`.
- Mémoire des choix (`yt-*/memory/choices.json`, `yt-orchestrator/memory/pipeline_runs.json`) : écrite par l'orchestrateur en Phase 5, voir `yt-orchestrator/references/feedback-loop.md`.
