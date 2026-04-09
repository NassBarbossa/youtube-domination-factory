---
name: yt-transcript
description: Fetch transcripts of competing YouTube videos on a given topic, analyze them, and produce a research brief for yt-script. Use when a topic has been identified and we need to understand what competitors have covered before writing our script.
metadata:
  author: NassRiviera
  version: 1.0.0
  category: youtube-workflow
  tags: [research, transcript, analysis, youtube]
---

# YT Transcript — Competitive Research & Synthesis

## Identity

Tu es le chercheur de la factory. Ton job : récupérer ce que les concurrents ont dit sur un sujet, analyser leurs angles, et produire un brief de recherche que le scriptwriter utilisera pour écrire un script avec un angle différenciant.

## Mission

1. Identifier les vidéos concurrentes sur le sujet
2. Récupérer les transcripts bruts
3. Analyser : faits, angles, trous
4. Produire un brief de recherche synthétique

## Workflow

### Step 1: Identifier les vidéos concurrentes

Sources (dans cet ordre) :
1. **DB veille** (priorité) — chercher dans la DB SQLite sur le VPS les vidéos liées au topic :
   ```bash
   ssh root@72.62.253.227 "cd /root/youtube-domination-factory/yt-veille/scripts && python3 -c \"
   import sqlite3
   conn = sqlite3.connect('data/veille.db')
   rows = conn.execute(\\\"SELECT v.video_id, v.title, c.handle FROM videos v JOIN channels c ON v.channel_id = c.channel_id WHERE LOWER(v.title) LIKE '%KEYWORD%'\\\").fetchall()
   for r in rows: print(f'{r[0]} | {r[2]} | {r[1]}')
   conn.close()
   \""
   ```
2. **YouTube search** (fallback) — si la DB n'a pas assez de résultats

Sélectionner **3-5 vidéos max** les plus pertinentes (priorité aux Tier 1, aux scores élevés, et aux vidéos récentes).

### Step 2: Récupérer les transcripts

Pour chaque vidéo, exécuter :
```bash
uv run yt-transcript/scripts/get_transcript.py "VIDEO_ID"
```

Sauvegarder chaque transcript dans `context/transcripts/[slug]/[video_id]-transcript.txt`.

**RÈGLE** : Ne JAMAIS modifier le transcript brut. Le fichier sauvegardé est le texte exact retourné par l'API.

### Step 3: Analyser les transcripts

Pour chaque transcript, extraire :
- **Faits clés** : chiffres, dates, noms, citations spécifiques
- **Angle principal** : quelle histoire le créateur raconte
- **Structure** : comment il a organisé son contenu
- **Ce qu'il a bien fait** : moments forts, hooks efficaces
- **Ce qu'il a raté** : sujets survolés, faits manquants, angles ignorés

### Step 4: Synthétiser le brief de recherche

Produire une synthèse qui répond à :
1. **Quels faits sont confirmés par plusieurs sources ?** (= fiable, à utiliser)
2. **Quels angles ont été couverts par tout le monde ?** (= on doit le couvrir mais pas en faire notre angle principal)
3. **Quels angles personne n'a couverts ?** (= notre opportunité de différenciation)
4. **Quels faits/chiffres spécifiques utiliser dans notre script ?**
5. **Quel angle recommandé pour Nass ?** (basé sur les trous + la voix Nass)

## Output

Sauvegarder le brief dans `context/transcripts/[slug]/research-brief.md` avec ce format :

```markdown
# Research Brief — [Topic]

## Vidéos analysées
| # | Chaîne | Titre | Video ID |
|---|--------|-------|----------|
| 1 | ... | ... | ... |

## Faits clés (confirmés par 2+ sources)
- Fait 1 (sources : chaîne A, chaîne B)
- Fait 2 (sources : chaîne A, chaîne C)

## Angles couverts par les concurrents
- Angle 1 — couvert par A, B, C
- Angle 2 — couvert par A, B

## Angles manquants (opportunités)
- Angle 1 — personne n'en parle
- Angle 2 — survolé mais pas approfondi

## Chiffres & citations utilisables
- "Citation exacte" — source
- Chiffre : XX — source

## Recommandation d'angle pour Nass
[1-2 paragraphes : quel angle prendre et pourquoi]
```

## Rules

- JAMAIS plus de 5 vidéos — au-delà c'est du bruit
- JAMAIS modifier les transcripts — la source doit rester pure
- TOUJOURS citer les sources dans le brief (quelle chaîne a dit quoi)
- Privilégier les vidéos des 7 derniers jours sur le sujet
- Si aucune vidéo n'existe sur le sujet → le signaler (c'est une info utile : terrain vierge)

---

## Context Protocol (Mode Autonome — Orchestrateur)

Quand tu es invoqué par `yt-orchestrator` en Phase 0.75, suis ce protocole :

### Input

Lire `context/video-context.json` :
- `request.topic` : le sujet de la vidéo
- `veille.selected_idea` : si Mode B, l'idée choisie par Nass

### Workflow autonome

1. Extraire le keyword principal depuis le topic
2. Chercher les vidéos dans la DB veille (Step 1)
3. Fetch les transcripts (Step 2)
4. Analyser et synthétiser (Step 3-4)
5. Écrire le brief dans `context/transcripts/[slug]/research-brief.md`

### Output

Écrire dans `context/video-context.json` → `research` :

```json
{
  "research": {
    "status": "completed",
    "videos_analyzed": 4,
    "transcripts": [
      {
        "video_id": "abc123",
        "channel": "Nick Saraev",
        "title": "Claude Mythos Preview: Everything You Need to Know",
        "file": "context/transcripts/slug/abc123-transcript.txt"
      }
    ],
    "key_facts": ["fact1", "fact2"],
    "angles_covered": ["angle1", "angle2"],
    "angles_missing": ["angle1"],
    "recommended_angle": "L'angle recommandé pour Nass",
    "synthesis": "Résumé complet de la recherche",
    "brief_file": "context/transcripts/slug/research-brief.md"
  }
}
```

---

## Mode Manuel (Préservé)

Si Nass t'appelle directement avec `/yt-transcript`, tu peux :
- Récupérer le transcript d'une seule vidéo : `/yt-transcript VIDEO_URL`
- Lancer une recherche complète sur un sujet : `/yt-transcript research "Claude Mythos"`
