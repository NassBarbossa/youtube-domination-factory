# Content Machine — génération du post LinkedIn

Chargé par `yt-repurposing` (Step 4) quand le post LinkedIn est généré. Le thread X ne passe pas par la Content Machine (elle est optimisée LinkedIn) : il suit le Step 3 du SKILL.md.

La Content Machine est un projet externe indépendant : `C:\Users\User\content-machine`. On la lit, on ne la modifie jamais (seule exception : le log de choix, voir plus bas).

**Priorité** : le cadre (`_shared/cadre-nass.md`) et les règles de `yt-repurposing` priment sur la Content Machine. Si `config/brand.md` décrit encore l'ancien positionnement (IA / Claude Code / VibeCoding), l'ignorer sur ce point et le signaler : « La Content Machine est encore sur l'ancien positionnement IA » (en mode autonome : dans `open_questions[]`).

## Avant chaque exécution

1. **Vérifier la version** : comparer le hash du dernier commit (`git -C C:\Users\User\content-machine log -1 --format=%h`) avec celui stocké dans `yt-repurposing/last_cm_version.txt`. Si différent : relire tous les fichiers ci-dessous, mettre à jour `last_cm_version.txt`, signaler « Content Machine mise à jour détectée — config rechargée ».
2. **Config** :
   - `config/brand.md` → audience, ton, positionnement
   - `core/rules.md` → mise en forme, limites, mots interdits
3. **Engines** :
   - `engines/a-oneshot/hook/SKILL.md` → hooks curiosité
   - `engines/a-oneshot/post/SKILL.md` → post one-shot
   - `engines/b-iterative/hook/SKILL.md` → hooks outcome-first
   - `engines/b-iterative/post/SKILL.md` → post en 4 passes
4. **Voice memory** (si elle existe) : `platforms/linkedin/memory/voice.md`

(Chemins relatifs à `C:\Users\User\content-machine`.)

## Workflow LinkedIn

1. **Extraire le sujet** du script vidéo : l'angle patrimoine / l'insight, pas un résumé.
2. **Identifier le type** : story | tips | contrarian | transformation | lesson | behind-the-scenes.
3. **Extraire les détails concrets** du script : scène exacte, moment clé, preuves vérifiables (transaction on-chain, prix daté avec sa source).
4. **Générer selon le mode** :
   - **Mode manuel (Nass en direct)** : générer avec les deux engines — Engine A (curiosité, one-shot) et Engine B (outcome-first, 4 passes ; « outcome » = ce que le lecteur comprend ou évite, jamais un gain promis). Présenter les deux côte à côte, Nass choisit, puis logger le choix dans `memory/ab-test.json` de la Content Machine.
   - **Mode autonome (agent lancé par l'orchestrateur)** : une seule proposition, avec l'engine le plus adapté au type identifié (story/lesson/behind-the-scenes → A ; tips/contrarian/transformation → B). Noter l'engine utilisé et, dans `open_questions[]`, « Variante avec l'autre engine à générer si Nass veut comparer ». Pas de log dans `ab-test.json` (pas de choix de Nass).
5. **Vérifier la conformité** : règles de fond du cadre, aucune promesse de gain, chiffres réels et datés, disclaimer présent.

## Règles

- Respecter `core/rules.md` (mise en forme, limites, mots interdits) et le brand voice de `config/brand.md`, sauf contradiction avec le cadre ou avec `yt-repurposing` (qui priment).
- 1 phrase par ligne, 1 emoji max.
- **Hashtags** : la règle de `yt-repurposing` s'applique (3-5 en fin de post). Si `core/rules.md` dit « pas de hashtags », la règle du skill prime et le désaccord est remonté à Nass (question ouverte).
- Longueur : 1300-1600 caractères ; hook ≤ 210-235 caractères visibles avant « …voir plus » (hypothèses à tester, voir SKILL.md).
- Au moins une preuve concrète par post (prix daté et sourcé, transaction on-chain, date).
- Disclaimer « Pas un conseil en investissement. », une fois, en fin de post.
