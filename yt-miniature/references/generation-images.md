# Génération d'images — Nano Banana 2 via OpenRouter

Chargé par `yt-miniature/SKILL.md` quand Nass veut générer le fond ou une version de la miniature. Pas de génération en mode autonome (pipeline) : on livre le concept, Nass déclenche la génération.

`{repo}` = racine du dépôt youtube-domination-factory (Mac : `~/youtube-domination-factory` · Windows : `C:\Users\User\youtube-domination-factory`) ; les chemins relatifs partent de là.

## Configuration de l'API

- Endpoint : `https://openrouter.ai/api/v1/chat/completions`
- Modèle : `google/gemini-3.1-flash-image-preview`
- Clé : `OPENROUTER_API_KEY` dans le `.env` à la racine du repo
- Coût indicatif : environ 0,07 $ par génération (le coût réel est renvoyé dans `usage.cost`)
- Sortie : image en base64 dans `response.choices[0].message.images[0].image_url.url`
- Le prompt est en anglais (le modèle répond mieux en anglais).

## Photos de référence

Dossier : `yt-miniature/references/nass/` (ne pas modifier ces fichiers). Fichiers réellement présents :

| Fichier | Expression / usage |
|---------|--------------------|
| `surprised.jpg` | sourcils levés, bouche ouverte |
| `curious.jpg` | sourcil levé, regard engagé |
| `confident.png` | léger sourire, regard direct |
| `confident-wide.png` | confiant, plan plus large |
| `focused.jpg` | regard vers un écran, concentré |
| `skeptical.jpg` | un sourcil levé, léger froncement |
| `NassCloseSmile.png` | sourire, plan serré |
| `NassDistantSmile.png` | sourire, plan large |
| `*-2026-10.jpg` (19 photos : neutre, réfléchi, salut, surpris, sourire, et versions hautes) | référence actuelle, octobre 2026 |

À fournir par Nass :
- `neutral.*` — expression neutre de base (absente). En attendant, repli sur `confident.png`.
- Une photo **sérieuse, bouche fermée** et une pose **poing sous le menton** : ce sont les expressions retenues sur les miniatures de la formation offerte, sans photo de référence dédiée dans le dossier.
- Référence du punk @punk6995 dans `yt-miniature/references/punk/` (dossier absent). En attendant, une copie existe dans le repo : `yt-shorts-montage/projects/wallets/02-c-est-quoi-un-wallet/assets/punk6995.jpg`.

**Choix de la photo** : prendre le fichier le plus proche de l'expression du concept ; à défaut, `confident.png`. Adapter le type MIME du data URL à l'extension (`image/jpeg` pour `.jpg`, `image/png` pour `.png`).

**Punk** : si le concept utilise le punk, joindre aussi sa référence (deuxième `image_url`) pour que le modèle respecte ses attributs. Ne jamais laisser le modèle inventer un autre punk.

## Commande

```bash
# 1. Photo de référence selon l'expression du concept
REF_PHOTO="yt-miniature/references/nass/confident.png"
REF_MIME="image/png"   # image/jpeg pour un .jpg

# 2. Encodage base64
REF_B64=$(base64 -w 0 "$REF_PHOTO")

# 3. Appel OpenRouter
source .env && curl -s "https://openrouter.ai/api/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -d "{
    \"model\": \"google/gemini-3.1-flash-image-preview\",
    \"messages\": [{
      \"role\": \"user\",
      \"content\": [
        {\"type\": \"text\", \"text\": \"[PROMPT EN ANGLAIS]\"},
        {\"type\": \"image_url\", \"image_url\": {\"url\": \"data:$REF_MIME;base64,$REF_B64\"}}
      ]
    }],
    \"max_tokens\": 4096
  }" | node -e "
    const d=[];
    process.stdin.on('data',c=>d.push(c));
    process.stdin.on('end',()=>{
      const r=JSON.parse(d.join(''));
      const img=r.choices[0].message.images[0];
      const b64=img.image_url.url.replace(/^data:image\/\w+;base64,/,'');
      require('fs').writeFileSync('yt-miniature/outputs/[SLUG]-thumbnail.jpg', Buffer.from(b64,'base64'));
      console.log('Saved. Cost:', r.usage.cost, 'USD');
    })"
```

## Fichiers de sortie

```
yt-miniature/outputs/[slug]-thumbnail.jpg        — génération brute (sans texte, sans données)
yt-miniature/outputs/[slug]-thumbnail-final.jpg  — après Canva : texte + vrai graphique / vraie capture
```

Pipeline utilisé sur la formation offerte (octobre 2026, d'après `memory/choices.json`) : fond généré, détourage de Nass en studio, greffe du visage sur le buste, puis composition. Le script `composite.py` cité dans ces notes n'est pas dans le repo.

## Règle des données réelles

Le modèle ne génère **jamais** un graphique de prix, un montant ou une capture de wallet : il inventerait les données. Le prompt réserve une zone vide (par exemple une carte crème vierge à bord noir) ; le vrai graphique (bougies d'exchange datées, données on-chain) ou la vraie capture est posé dans Canva à l'étape `-final`, avec la date en Public Sans, et la source notée dans `figure_source`.

## Cadre de prompt

Source : guide de prompting Nano Banana de Google Cloud.

Formule : `[Sujet] + [Action] + [Lieu / contexte] + [Composition] + [Style]`

- Narratif, pas une liste de mots-clés : décrire la scène comme un directeur artistique.
- Formulation positive : décrire ce qu'on veut (« empty background ») plutôt que ce qu'on ne veut pas.
- Préciser l'objectif photo (« 85mm portrait lens, f/1.8, shallow depth of field »).
- Préciser la lumière (« warm sand-gold rim light », « soft split lighting »).
- Décrire les matières (« matte cream paper card with a thick black border », « crisp pixel-art edges »).

## Template (anglais)

Remplacer les `[PLACEHOLDERS]` par les valeurs du concept. Toujours joindre la photo de référence de Nass (et celle du punk s'il apparaît).

```
Generate a photorealistic YouTube thumbnail, 1280x720, 16:9 aspect ratio.

[SUBJECT] A man (use the EXACT face from my attached reference photo — do not modify, generate, or replace any facial features) positioned on the [LEFT/RIGHT] third of the frame, face filling approximately [35-50]% of the frame.

[ACTION] [EXPRESSION — e.g. "Looking directly at camera with calm, focused curiosity — slight eyebrow raise, eyes engaged, mouth closed, conveying 'let me show you exactly what I did' transparency."]

[LOCATION/CONTEXT] [BACKGROUND — e.g. "Standing against a deep matte black background (#0B0B0B) with a soft silhouette of mountains at dusk along the bottom edge, their ridges catching a faint sand-gold glow (#DBB17F)." Secondary element if any: "On the right third, a blank matte cream card (#F4EFE7) with a thick solid black border and a hard flat drop shadow (#9C7748), completely empty, reserved for a real chart added later." OR "A crisp pixel-art punk character (match the attached @punk6995 reference exactly) standing on the right third."]

[COMPOSITION] Medium close-up shot, rule of thirds, two focal points maximum (face + [SECOND ELEMENT]). Shot on an 85mm portrait lens at f/1.8, shallow depth of field — face tack-sharp, background softly blurred. Safe zones clear: no important elements in bottom-right, top-right, or bottom-left corners.

[STYLE] High-end YouTube thumbnail photography style. Black, sand-gold and cream color palette (#0B0B0B, #DBB17F, #F4EFE7) [optional accent: muted punk blue #648596]. Dramatic [LIGHTING — e.g. "warm sand-gold rim light from the right side"]. High contrast on facial features. Face bright and well-exposed against the dark background. Clean, minimal composition with empty negative space around the subject. Export-ready, sRGB, ultra sharp. The image contains no text, numbers, charts, coins or logos.
```

## Exemple : « Acheter hors des exchanges »

```
Generate a photorealistic YouTube thumbnail, 1280x720, 16:9 aspect ratio.

A man (use the EXACT face from my attached reference photo — do not modify, generate, or replace any facial features) positioned on the left third of the frame, face filling approximately 45% of the frame.

Looking directly at camera with calm, focused attention — eyes engaged, mouth closed, slight determination. Conveying transparency and seriousness, not excitement or greed.

Standing against a deep matte black background (#0B0B0B) with a soft silhouette of mountains at dusk along the bottom edge, their ridges catching a faint sand-gold glow (#DBB17F). On the right third, a blank matte cream card (#F4EFE7) with a thick solid black border and a hard flat drop shadow (#9C7748), slightly tilted, completely empty, reserved for a real on-chain transaction screenshot added later.

Medium close-up shot, rule of thirds, two focal points maximum (face and the cream card). Shot on an 85mm portrait lens at f/1.8, shallow depth of field — face tack-sharp, background softly blurred.

High-end YouTube thumbnail photography style. Black, sand-gold and cream color palette with a dramatic warm sand-gold rim light (#DBB17F) from the right side illuminating the face. High contrast on facial features. Face bright and well-exposed against the dark background. Clean, minimal composition with empty negative space around the subject. Export-ready, sRGB, ultra sharp. The image contains no text, numbers, charts, coins or logos.
```

À l'étape `-final` (Canva) : poser dans la carte crème la capture réelle de la transaction sur l'explorateur, datée, et noter la source dans `figure_source`.

## Checklist avant validation

- [ ] Prompt en anglais
- [ ] Photo de référence de Nass jointe (et référence @punk6995 si le punk apparaît)
- [ ] C'est bien le visage de Nass / le bon punk
- [ ] Expression visible et naturelle, différente des vidéos précédentes (pas d'euphorie « argent facile »)
- [ ] 2 éléments focaux max
- [ ] Fond noir `#0B0B0B` sans encombrement, sujet lumineux
- [ ] Dominante sable/or `#DBB17F` (pas l'ancienne charte orange / cyan)
- [ ] Aucun texte, chiffre ou graphique généré (ajoutés dans Canva à partir de données réelles)
- [ ] Tout chiffre affiché est réel, daté et sourcé ; aucune capture retouchée
- [ ] Aucune imagerie levier / short / casino / argent facile
- [ ] Pas de watermark
