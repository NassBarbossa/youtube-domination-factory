---
name: yt-orchestrator
description: Master orchestrator that spawns video production pipeline agents in sequence and parallel, manages shared context file, and ensures human validation at critical steps.
version: 2.0
triggers:
  - "fais une vidéo sur"
  - "lance le pipeline"
  - "produits une vidéo"
  - "crée une vidéo"
  - "sujet de vidéo"
  - "trouve moi des idées"
---

# yt-orchestrator — Master Orchestrator

## Mode d'emploi

Tu es l'orchestrateur principal du pipeline YouTube. Tu spawnes les agents dans le bon ordre, tu gères le fichier JSON partagé (`context/video-context.json`), et tu demandes la validation de Nass aux points critiques.

### Détection du mode

**Mode A** : Nass donne un sujet directement
```
"Fais une vidéo sur Claude 4"
"Lance le pipeline sur le topic: AI Agents"
```
→ **Saute Phase 0.5**, démarre directement à Phase 1 (yt-script)

**Mode B** : Nass cherche d'abord des idées
```
"Trouve moi des idées de vidéo"
"Quoi filmer cette semaine ?"
```
→ **Lance Phase 0.5** (yt-veille) pour générer des idées, demande validation, puis Phase 1

---

## Pipeline Phases

### Phase 0 — Initialisation

**Toujours exécutée** en premier.

1. Déterminer le mode (A ou B) en analysant l'input de Nass
2. Générer un `slug` (ex: `claude-4-features`) depuis le topic ou l'idée sélectionnée
3. Créer/initialiser `context/video-context.json` :
   - `_meta.slug` = slug généré
   - `_meta.status` = "in_progress"
   - `_meta.pipeline_step` = 0
   - `_meta.triggered_by` = "user" ou "schedule"
   - `_meta.created_at` = timestamp ISO
   - `request.raw_input` = input brut de Nass
   - `request.topic` = topic détecté ou à chercher
4. Annoncer à Nass : "🎬 Pipeline lancé sur : [topic]. Slug : [slug]. Prêt pour la phase suivante."

**Reprise de session** : Si `context/video-context.json` existe déjà avec un slug et `pipeline_step` > 0, lire le fichier existant et sauter à la phase correspondante.

---

### Phase 0.5 — Recherche de sujets (Mode B uniquement)

**Exécutée seulement si Mode B détecté.**

1. Spawn agent `yt-veille` avec prompt :
   ```
   "Mode orchestrateur : Lis yt-veille/SKILL.md, puis:
   1. Lis context/video-context.json (section request)
   2. Génère 3-5 idées de vidéo avec scoring
   3. Écris dans context/video-context.json → veille.selected_idea (laisse null pour l'instant)
   4. Fournis un résumé à Nass avec les 3-5 options"
   ```
2. Attendre completion du agent (utiliser TaskOutput si async)
3. Afficher les idées à Nass avec les scores
4. **PAUSE POUR VALIDATION** : Demander à Nass de choisir une idée
5. Enregistrer le choix dans `veille.selected_idea`
6. Mettre à jour `_meta.pipeline_step` = 1
7. Continuer vers Phase 1

---

### Phase 0.75 — Recherche de transcripts concurrents

**Exécutée après identification du sujet** (Mode A ou après choix Mode B).

1. Spawn agent `yt-transcript` avec prompt :
   ```
   "Mode orchestrateur : Lis yt-transcript/SKILL.md, puis:
   1. Lis context/video-context.json (sections request et veille si disponible)
   2. Identifie les vidéos concurrentes sur le sujet (DB veille + YouTube search si nécessaire)
   3. Fetch les transcripts (3-5 vidéos max)
   4. Analyse et synthétise dans un brief de recherche
   5. Écris dans context/video-context.json → research.*
   6. Sauvegarde le brief dans context/transcripts/[slug]/research-brief.md"
   ```
2. Attendre completion
3. Vérifier que `research.status` = "completed"
4. Mettre à jour `_meta.pipeline_step` = 1

---

### Phase 1 — Rédaction du script

**Exécutée séquentiellement** (attend completion avant Phase 2).

1. Spawn agent `yt-script` avec prompt :
   ```
   "Mode orchestrateur : Lis yt-script/SKILL.md, puis:
   1. Lis context/video-context.json (sections request, veille si disponible, et research)
   2. Utilise le brief de recherche (research.synthesis, key_facts, angles_missing) pour écrire un script avec un angle différenciant
   3. Rédige le script complet avec markers [FACE CAM], [SCREEN], etc.
   4. Écris dans context/video-context.json → script.* (slug, file_path, word_count, structure)
   5. Fournis le titre du script à Nass"
   ```
2. Attendre completion
3. Vérifier que `script.status` = "completed"
4. Mettre à jour `_meta.pipeline_step` = 2

---

### Phase 2 — Titres, miniature et description (Parallèle)

**Exécutée en PARALLÈLE** (3 agents en même temps).

Lance **3 appels Agent simultanés** :

#### Agent A : yt-titres-seo
```
"Mode orchestrateur : Lis yt-titres-seo/SKILL.md, puis:
1. Lis context/video-context.json (section script)
2. Génère 5 titres SEO optimisés avec primary/secondary keywords
3. Sélectionne le meilleur : winning_title
4. Écris dans context/video-context.json → titres_seo.*"
```

#### Agent B : yt-miniature
```
"Mode orchestrateur : Lis yt-miniature/SKILL.md, puis:
1. Lis context/video-context.json (sections script et titres_seo)
2. Crée un concept miniature avec layout, text_overlay, color_palette
3. ⚠️ IMPORTANT : text_overlay ne doit PAS répéter winning_title
4. Écris dans context/video-context.json → miniature.recommended_concept"
```

#### Agent C : yt-description
```
"Mode orchestrateur : Lis yt-description/SKILL.md, puis:
1. Lis context/video-context.json (sections script et titres_seo)
2. Rédige la description YouTube (200-500 chars) + 15-20 tags SEO
3. Écris dans context/video-context.json → description.* (description_full, tags, first_150_chars)"
```

3. Attendre que les 3 agents se terminent (TaskOutput avec block=true)
4. Vérifier que tous les 3 ont status = "completed"
5. Mettre à jour `_meta.pipeline_step` = 3

---

### Phase 3 — Validation humaine

**PAUSE OBLIGATOIRE** avant le repurposing.

1. Afficher à Nass un résumé formaté :
   ```
   ✨ PHASE 3 — VALIDATION REQUISE

   📺 Titre gagnant :
   [titres_seo.winning_title]

   🎨 Concept miniature :
   [miniature.recommended_concept.name]
   Layout: [layout]
   Texte overlay: [text_overlay]
   Palette: [color_palette]

   📝 Description (premiers 150 chars):
   [description.first_150_chars]

   Tags SEO: [tags - premiers 5]

   ➜ Dis "OK" pour valider, ou "modifie X" pour demander des ajustements
   ```

2. **ATTENDRE VALIDATION EXPLICITE** de Nass (réponse "OK" ou validation équivalente)
   - Si modification demandée : décrire le changement, relancer l'agent concerné seul, revenir à Phase 3
   - Si OK : continuer à Phase 4

3. Une fois validé, marquer dans le JSON :
   - `titres_seo.status` = "validated"
   - `miniature.status` = "validated"
   - `description.status` = "validated"
   - `_meta.pipeline_step` = 4

---

### Phase 4 — Repurposing (Shorts, X, LinkedIn)

**Exécutée séquentiellement** (attend validation Phase 3 avant de démarrer).

1. Spawn agent `yt-repurposing` avec prompt :
   ```
   "Mode orchestrateur : Lis yt-repurposing/SKILL.md, puis:
   1. Lis context/video-context.json (sections script et titres_seo - validés)
   2. Découpe le script en Shorts clips (15-60s avec hook)
   3. Crée un thread X partir du hook + 3-5 tweets
   4. Crée un post LinkedIn avec angle professionnel
   5. Écris dans context/video-context.json → repurposing.* (shorts[], x_thread_hook, linkedin_hook)"
   ```

2. Attendre completion
3. Vérifier que `repurposing.status` = "completed"
4. Mettre à jour `_meta.pipeline_step` = 5

---

### Phase 5 — Récapitulatif et archivage

**Dernière phase** — préparation pour publication.

1. Générer un **récap formaté** pour Nass :
   ```
   ✅ PIPELINE COMPLÉTÉ — [topic]

   📜 Script: [word_count] mots, [reading_time_min] min de lecture
   📺 Titre: [winning_title]
   🎨 Miniature: [concept_name] — [color_palette]
   🔖 Tags: [primary_keyword], [secondary_keywords]

   📱 Repurposing:
   - [N] Shorts générés
   - Thread X: [snippet des 2 premiers tweets]
   - LinkedIn: [snippet]

   Tous les fichiers sont prêts dans context/video-context.json
   Prêt pour upload yt-calendrier ou montage manuel.
   ```

2. Archiver le JSON complet : copier `context/video-context.json` vers `context/archive/[slug]-[timestamp].json`
3. Mettre à jour `_meta.status` = "completed"
4. Mettre à jour `_meta.pipeline_step` = 5

---

## Gestion des erreurs

### Pendant une phase

**Si un agent retourne une erreur** :

1. Logger l'erreur dans `pipeline_log` :
   ```json
   {
     "phase": 2,
     "agent": "yt-titres-seo",
     "error": "Exception: ...",
     "timestamp": "2026-03-16T12:34:56Z",
     "retries": 1
   }
   ```

2. Afficher à Nass : "❌ Erreur dans [agent] (Phase [N]). Détail : [error]. Relancer ? (oui/non)"

3. Options :
   - **Relancer seul** : respawn le même agent
   - **Ignorer et continuer** : (si non-bloquant) passer à Phase suivante
   - **Annuler pipeline** : marquer `_meta.status` = "failed", archiver

### Reprise de session

**Au démarrage** :

1. Chercher `context/video-context.json` existant
2. Lire `_meta.pipeline_step`
3. Si ≥ 1 et < 5 : proposer à Nass "Reprendre depuis Phase [N] ?" ou "Redémarrer ?"
4. Si validé pour reprise : lancer directement à la bonne phase

---

## Context Protocol

**Tu es invoqué soit directement par Nass, soit by le système** (future automation). Dans les deux cas :

1. **Lis toujours** le `context/video-context.json` existant en premier (s'il existe)
2. **Initialise** ou **mets à jour** le JSON au fur et à mesure des phases
3. **Loggue** chaque phase dans `pipeline_log`
4. **Demande la validation** explicitement à Nass (ne pas supposer)

---

## Règles de compatibilité

- **Mode manuel préservé** : Chaque skill (yt-script, yt-titres-seo, etc.) continue de fonctionner en appel direct si Nass les trigger manuellement. Cette architecture orchestrator est **transparent** — elle ne force personne.
- **JSON optionnel** : Si Nass appelle `/yt-script` directement, le skill ignore le JSON et fonctionne classiquement.
- **Pas de breaking changes** : les triggers existants continuent de marcher.

---

## Checklist d'implémentation

- [ ] Détecter mode A vs B
- [ ] Initialiser slug et JSON Phase 0
- [ ] Spawn Phase 0.5 (yt-veille) — Mode B
- [ ] Demander validation Nass → idée
- [ ] Spawn Phase 1 (yt-script)
- [ ] Spawn Phase 2 en parallèle (yt-titres-seo + yt-miniature + yt-description)
- [ ] Afficher résumé Phase 3 + demander validation (titre, miniature, description)
- [ ] Spawn Phase 4 (yt-repurposing) avec titre validé
- [ ] Générer récap Phase 5
- [ ] Archiver JSON
- [ ] Gestion erreurs + reprise session

---

## Mode de fonctionnement

**Tu dois maîtriser le tool `Agent`** pour spawner d'autres Claude instances. Exemple :

```python
# Spawn yt-script en Mode B autonome
agent_result = Agent(
  subagent_type="general-purpose",
  description="Rédaction script YouTube autonome",
  prompt="""
  Mode orchestrateur : Lis yt-script/SKILL.md...
  """
)
```

Voir documentation Claude Code sur `Agent` tool pour detailsopening le passage de données au JSON.

---

## Feedback Loop — Self-Improvement System (Orchestrator Level)

L'orchestrator a **deux niveaux de feedback** qui fonctionnent ensemble :

### Niveau 1 : Meta-Feedback (auto-analyse du pipeline)

L'orchestrator s'analyse lui-même : comment le pipeline a tourné, sa vitesse, ses erreurs.

#### Après chaque pipeline terminé

Logger dans `yt-orchestrator/memory/pipeline_runs.json` :

```json
{
  "video_slug": "slug-de-la-video",
  "mode": "A|B",
  "started_at": "2026-03-29T10:00:00Z",
  "completed_at": "2026-03-29T13:30:00Z",
  "total_duration_min": 210,
  "phases": {
    "phase_0_init": {"duration_min": 2, "status": "success"},
    "phase_0.5_veille": {"duration_min": 15, "status": "success|skipped"},
    "phase_1_script": {"duration_min": 105, "status": "success", "retries": 0},
    "phase_2a_titres": {"duration_min": 10, "status": "success"},
    "phase_2b_miniature": {"duration_min": 12, "status": "success"},
    "phase_2c_description": {"duration_min": 8, "status": "success"},
    "phase_3_validation": {"duration_min": 30, "status": "success", "changes_requested": ["titre"]},
    "phase_4_repurposing": {"duration_min": 20, "status": "success"},
    "phase_5_recap": {"duration_min": 5, "status": "success"}
  },
  "errors": [],
  "validation_rounds": 1,
  "changes_requested_at_validation": ["titre"],
  "skills_used": {
    "titres_seo": {"title_style": "chiffre", "char_count": 42},
    "miniature": {"concept": "cyan-face-dark", "has_face": true},
    "script": {"hook_type": "curiosity-gap", "duration_min": 11, "structure": "tutorial"},
    "veille": {"source": "daily_monitor", "topic_category": "claude-code", "outlier_score": 3.1}
  },
  "performance": null
}
```

#### Ce qu'on en extrait (meta_lessons) :

- **Bottleneck** : quelle phase prend le plus de temps en moyenne → optimiser
- **Taux de complétion** : % de pipelines terminés vs abandonnés
- **Retries** : quels agents échouent le plus souvent
- **Validation** : combien de rounds de changements à Phase 3 en moyenne → si > 2, les agents en amont doivent mieux calibrer
- **Vitesse totale** : temps moyen du pipeline → corrélation avec la performance vidéo (plus rapide = trend encore chaude ?)

Exemple de meta_lesson :
```json
{
  "rule": "Phase 1 (script) est le bottleneck — 50% du temps total en moyenne",
  "evidence": "Moyenne 105 min sur 210 min totales, sur 5 pipelines",
  "action": "Envisager de pré-écrire les outlines avant de lancer le pipeline complet",
  "sample_size": 5,
  "confidence": "medium"
}
```

### Niveau 2 : Cross-Feedback (combinaisons gagnantes)

L'orchestrator lit les leçons de chaque skill et identifie les **combinaisons** qui performent ensemble.

#### Avant chaque nouveau pipeline

1. Lire `yt-orchestrator/memory/lessons.json`
2. Lire les `memory/lessons.json` de chaque skill (titres, miniature, script, veille)
3. Si des cross-lessons existent, les injecter dans les prompts des agents :
   - "Combinaison gagnante : titre chiffre + miniature cyan + hook curiosity = 3× la moyenne"
   - "Éviter : titre descriptif + miniature sans visage = sous-performance systématique"
4. Mentionner à Nass : "Basé sur [N] vidéos, la combinaison [X] est ta meilleure formule"

#### Après chaque analyse du feedback_analyzer

Croiser les données de performance avec les choix combinés de chaque pipeline :

```json
{
  "winning_combos": [
    {
      "combo": {
        "title_style": "chiffre",
        "thumbnail_concept": "cyan-face-dark",
        "hook_type": "curiosity-gap",
        "topic_category": "claude-code"
      },
      "avg_performance_index": 2.3,
      "count": 3,
      "confidence": "medium",
      "example_video": "2000e-1h-vibecoding"
    }
  ],
  "losing_combos": [
    {
      "combo": {
        "title_style": "descriptif",
        "thumbnail_concept": "text-overlay-bright",
        "hook_type": "statement",
        "topic_category": "ai-news"
      },
      "avg_performance_index": 0.6,
      "count": 2,
      "confidence": "low",
      "example_video": "nvidia-gtc-recap"
    }
  ]
}
```

#### Analyse des corrélations croisées

L'orchestrator cherche des patterns entre skills :

| Corrélation | Question posée | Exemple de leçon |
|-------------|---------------|-----------------|
| Titre × Miniature | Quels duos titre+miniature performent ? | "Titre chiffre + miniature visage = CTR 6.5% vs 3.2% pour les autres combos" |
| Script × Rétention × Titre | Est-ce que le style de hook corrèle avec le CTR du titre ? | "Les hooks curiosity gap ont un meilleur CTR que les hooks statement — le titre promet, le hook livre" |
| Veille × Performance globale | Les sujets trend convertissent-ils mieux selon le packaging ? | "Les outliers OpenClaw marchent mieux avec un titre 'how-to' qu'un titre 'news'" |
| Vitesse × Performance | Publier vite améliore-t-il les vues ? | "Les pipelines < 48h font 2.1× la moyenne vs 0.8× pour les > 7 jours" |

#### Format des cross_lessons

```json
{
  "cross_lessons": [
    {
      "rule": "Titre chiffre + miniature cyan + hook curiosity gap = formule gagnante",
      "evidence": "3 vidéos avec cette combinaison : performance index moyen 2.3x vs 0.9x pour les autres",
      "skills_involved": ["titres_seo", "miniature", "script"],
      "sample_size": 3,
      "confidence": "medium",
      "created_at": "2026-04-15"
    },
    {
      "rule": "Les pipelines complétés en < 48h performent 2× mieux",
      "evidence": "Corrélation -0.65 entre durée pipeline et performance index sur 8 vidéos",
      "skills_involved": ["orchestrator"],
      "sample_size": 8,
      "confidence": "medium",
      "created_at": "2026-04-20"
    }
  ]
}
```

### Confidence Levels

- `low` : < 5 pipelines complétés
- `medium` : 5-15 pipelines complétés
- `high` : > 15 pipelines complétés

### Intégration avec le Feedback Analyzer

Le script `yt-analytics/feedback_analyzer.py` met à jour les performances individuelles par skill. L'orchestrator ajoute une couche supplémentaire :

1. Après que `feedback_analyzer.py` a tourné, l'orchestrator peut relire les `lessons.json` de chaque skill
2. Il croise les données pour trouver les combinaisons inter-skills
3. Il met à jour ses propres `cross_lessons` et `winning_combos`

Cette analyse croisée se fait soit :
- Manuellement quand Nass demande "analyse mes performances"
- Automatiquement au début de chaque nouveau pipeline (lecture des leçons existantes)
