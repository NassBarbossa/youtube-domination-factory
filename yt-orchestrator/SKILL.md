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

### Phase 1 — Rédaction du script

**Exécutée séquentiellement** (attend completion avant Phase 2).

1. Spawn agent `yt-script` avec prompt :
   ```
   "Mode orchestrateur : Lis yt-script/SKILL.md, puis:
   1. Lis context/video-context.json (sections request et veille si disponible)
   2. Rédige le script complet avec markers [FACE CAM], [SCREEN], etc.
   3. Écris dans context/video-context.json → script.* (slug, file_path, word_count, structure)
   4. Fournis le titre du script à Nass"
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
