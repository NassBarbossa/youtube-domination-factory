---
name: yt-transcript
description: Recherche concurrentielle avant un script YouTube de la chaîne crypto de Nass Riviera — trouve 3 à 5 vidéos concurrentes sur un sujet, récupère leurs transcripts, en tire les faits (sourcés et vérifiés), les angles couverts et les angles manquants, et produit un brief de recherche pour yt-script. Déclencheurs : « recherche concurrentielle », « qu'est-ce que les autres ont dit sur… », « analyse les concurrents », « brief de recherche », « research brief », « competitor research ». Competitive research on a chosen topic before scripting. Pas pour récupérer le transcript d'une seule URL (« donne-moi le transcript de cette vidéo ») → youtube-transcript ; pas pour trouver un sujet → yt-veille.
metadata:
  author: NassRiviera
  category: youtube-workflow
  tags: [research, transcript, analysis, youtube]
---

# YT Transcript — recherche concurrentielle

**Cadre** : lis d'abord `C:\Users\User\youtube-domination-factory\_shared\cadre-nass.md` (narrative, avatar, offres, ton, règles de fond, charte). Il prime sur ce fichier.

Chemins relatifs = relatifs à la racine du repo `C:\Users\User\youtube-domination-factory`.

## Rôle

Tu es le chercheur de la factory : tu récupères ce que les concurrents ont dit sur un sujet, tu analyses leurs angles et tu produis un brief que yt-script utilisera pour écrire un script différenciant.

## Workflow

### 1. Trouver les vidéos concurrentes

La DB de la veille automatique n'est pas disponible (veille en pause, désactivée par Nass — ne pas la relancer sans qu'il le demande). On cherche directement sur YouTube :

```bash
yt-dlp --flat-playlist --print "%(id)s %(title)s %(channel)s %(view_count)s" "ytsearch10:<requête>"
```

- Vérifier d'abord `yt-dlp --version`. Au 2026-10-13, yt-dlp n'est pas installé sur le PC de Nass : l'installer avec `pip install yt-dlp` (ou `uv tool run yt-dlp …` si uv est installé) et le dire à Nass.
- Lancer 2-3 requêtes (FR d'abord, puis US) : mots-clés du sujet, variante débutant (« … pour débutant », « … expliqué »).
- Repli : WebSearch (`site:youtube.com <requête>`).
- Les chaînes de référence sont dans `yt-veille/references/sources.md` : à privilégier à pertinence égale.

Sélectionner **3 à 5 vidéos** (au-delà c'est du bruit) : pertinence d'abord, puis vues, puis fraîcheur. Sujet d'actualité : privilégier les dernières semaines. Sujet evergreen (wallet, self-custody, fiscalité, comment reconnaître un bon coin) : pas de limite de date.

Aucune vidéo trouvée → le signaler : terrain vierge, c'est une info utile.

### 2. Récupérer les transcripts

En local (la règle « VPS uniquement » ne concerne que `veille.db`) :

```bash
python yt-transcript/scripts/get_transcript.py "VIDEO_ID"
```

(`uv run yt-transcript/scripts/get_transcript.py "VIDEO_ID"` marche aussi si uv est installé ; la dépendance `youtube-transcript-api` est déjà installée dans le Python local.)

Sauvegarder chaque transcript tel quel dans `context/transcripts/<slug>/<video_id>-transcript.txt`. Ne jamais modifier le texte brut. Pas de sous-titres disponibles → le noter et passer à la vidéo suivante.

### 3. Analyser

Pour chaque transcript : faits clés (chiffres, dates, noms, citations), angle principal, structure, ce qui est bien fait (hooks, moments forts), ce qui est raté (sujets survolés, faits manquants, angles ignorés).

**Faits et vérification** : chaque fait garde sa `source` (chaîne + vidéo, ou lien). Il est `verified: true` seulement si tu l'as recoupé toi-même avec une source primaire (donnée on-chain, CoinGecko, texte officiel, site de l'émetteur) ; noter alors la source primaire et la date. Un chiffre qu'on ne trouve que chez un concurrent reste `verified: false` : yt-script ne le reprend pas tel quel (il le vérifie ou le laisse de côté). Un chiffre de gain d'un concurrent n'est jamais un fait.

### 4. Synthétiser

Le brief répond à :
1. Quels faits sont vérifiés ? Lesquels sont seulement cités par des concurrents ?
2. Quels angles tout le monde couvre (à couvrir, pas à prendre comme angle principal) ?
3. Quels angles personne ne couvre (notre différenciation) ?
4. Quel angle recommander à Nass, dans la narrative du cadre ?

Ne jamais recommander un angle exclu par les règles de fond (levier, futures, short, lending à intérêt, jeu), même si les concurrents le couvrent ; un angle memecoin → le signaler à Nass.

## Brief

`context/transcripts/<slug>/research-brief.md` :

```markdown
# Brief de recherche — [Sujet]

## Vidéos analysées
| # | Chaîne | Titre | Video ID | Vues |
|---|--------|-------|----------|------|

## Faits clés
| Fait | Source | Vérifié (source primaire, date) |
|------|--------|---------------------------------|

## Angles couverts par les concurrents
- Angle — couvert par A, B, C

## Angles manquants (opportunités)
- Angle — personne n'en parle / survolé

## Citations utilisables
- « Citation exacte » — source

## Recommandation d'angle pour Nass
[1-2 paragraphes]
```

## Appel direct par Nass

Workflow ci-dessus, avec interaction (Nass peut ajuster la sélection des vidéos). Pour un simple transcript d'une URL, c'est le skill `youtube-transcript`.

## Mode orchestrateur (Phase 0.75)

- **Entrée** : `context/video-context.json` en lecture seule — `request.topic`, `request.funnel`, `veille.selected_idea` (Mode B).
- **Workflow** : étapes 1 à 4 sans poser de question ; une info manque → `open_questions[]`.
- **Sortie** : écrire `context/runs/<slug>/research.json` et le brief, renvoyer le JSON dans le message final. Ne jamais écrire dans `context/video-context.json` : l'orchestrateur fusionne.

```json
{
  "research": {
    "status": "completed",
    "videos_analyzed": 4,
    "transcripts": [
      {
        "video_id": "abc123",
        "channel": "[chaîne]",
        "title": "[titre]",
        "views": null,
        "file": "context/transcripts/<slug>/abc123-transcript.txt"
      }
    ],
    "key_facts": [
      {"fact": "[fait]", "source": "[chaîne — video_id, ou lien]", "verified": false, "verified_by": null}
    ],
    "angles_covered": ["[angle]"],
    "angles_missing": ["[angle]"],
    "recommended_angle": "[angle recommandé]",
    "synthesis": "[résumé]",
    "brief_file": "context/transcripts/<slug>/research-brief.md",
    "open_questions": []
  }
}
```
