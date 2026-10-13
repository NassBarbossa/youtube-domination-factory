# TODO — YouTube Domination Factory

État au 2026-10-13, branche `rebrand/crypto` (en avance sur `master`, pas encore mergée).

## 1. Installer sur un nouvel ordi

```bash
git clone https://github.com/NassBarbossa/youtube-domination-factory.git
cd youtube-domination-factory
git checkout rebrand/crypto
```

Les skills désignent la racine du repo par `{repo}`, définie dans chaque fichier comme `~/youtube-domination-factory` (Mac) ou `C:\Users\User\youtube-domination-factory` (Windows). **Si le repo est ailleurs**, remplace le chemin de ton OS dans les `.md` (hors `outputs/`, `shows/`, `docs/`) :

```bash
# Mac — exemple si le repo est dans ~/Projets/ydf
grep -rl '~/youtube-domination-factory' --include='*.md' . | grep -v -E '/(outputs|shows|docs)/' | xargs sed -i '' 's#~/youtube-domination-factory#~/Projets/ydf#g'
```

```powershell
# Windows
$old = 'C:\Users\User\youtube-domination-factory'
$new = (Get-Location).Path
Get-ChildItem -Recurse -Include *.md | Where-Object { $_.FullName -notmatch '\\(outputs|shows|docs)\\' } |
  ForEach-Object { $c = Get-Content $_.FullName -Raw -Encoding utf8; if ($c.Contains($old)) { [IO.File]::WriteAllText($_.FullName, $c.Replace($old, $new)) } }
```

Brancher les skills dans Claude Code (liens vers le repo, une modif est active tout de suite) :

```bash
# Mac
cd ~/youtube-domination-factory
for d in yt-*/; do d=${d%/}; [ -f "$d/SKILL.md" ] && ln -sfn "../../youtube-domination-factory/$d" ~/.claude/skills/"$d"; done
```

```powershell
# Windows
$skills = "$env:USERPROFILE\.claude\skills"
Get-ChildItem . -Directory -Filter 'yt-*' | Where-Object { Test-Path "$($_.FullName)\SKILL.md" } |
  ForEach-Object { New-Item -ItemType Junction -Path "$skills\$($_.Name)" -Target $_.FullName }
```

Si d'anciennes copies `yt-*` existent déjà dans `~/.claude/skills`, les supprimer avant (ce sont les versions IA de mars). Supprimer aussi `yt-montage` s'il est là.

Outils utiles : Python 3 (`pip install youtube-transcript-api yt-dlp`), Node + Playwright + Chrome (vérif des slides), HyperFrames (Shorts). Fichier `.env` à recréer à la main (`OPENROUTER_API_KEY` pour la génération d'images des miniatures) : il n'est pas dans git.

## 2. Ce qui a été fait (2026-10-13)

- Les 3 vidéos de la formation offerte sont publiées (5, 7 et 11 octobre) : fiches dans `context/archive/<slug>-20261013-published.json` avec ID YouTube et date, en-têtes des scripts mis à jour. Prochaine vidéo = première hors série, dans la narrative.
- Décisions prises : wallet public abandonné ; charte miniatures à part (blanc + orange + bleus, photo réaliste) ; table « Liens » complète dans le cadre.
- Chemins portables Mac / Windows (`{repo}`), `.env` recréé sur le Mac.

- Audit complet de la factory.
- Shift de narrative : **challenge 10K → 100K abandonné**. Narrative = acheter les cryptos en dehors des échanges, acheter les bons coins, pas tous les jours. Memecoins hors sujet.
- Cadre écrit une seule fois : `_shared/cadre-nass.md`. Les skills y renvoient ; les règles halal s'appliquent sans être répétées dans les contenus (seul rappel visible : « Pas un conseil en investissement. »).
- Orchestrateur refait : script et choix d'idée avec Nass dans la conversation, titre avant miniature/description, un seul écrivain du contexte (`context/runs/<slug>/`), reprise fiable, contrat dans `context/SCHEMA.md`.
- Skills allégés (~4 100 → ~1 850 lignes), contradictions résolues, détails déplacés dans `references/`.
- Veille automatique : **en pause volontaire** (cron désactivé par Nass). Ne pas relancer sans décision de Nass.

## 3. À trancher par Nass

- [x] Wallet public : abandonné (2026-10-13), on ne le donne plus. Reste à retirer du site nassriviera.com (`~/nassriviera-challenge/public/index.html`, hors de ce repo) et de la page challenge.
- [x] Miniatures : charte à part validée (2026-10-13) : blanc + orange + bleus, photo réaliste (voir cadre). Sable/or réservé aux slides.
- [ ] Mix de contenus proposé dans `yt-calendrier` : éducation 35 % · acheter hors échanges 25 % · reconnaître un bon coin 20 % · actu + Convergence 15 % · communauté 5 % ; rythme 3 vidéos/semaine.
- [x] Liens donnés (2026-10-13) : site, Telegram, X, Instagram, chaîne, playlist formation, Convergence (lives de la chaîne), Twitch → table « Liens » du cadre.
- [ ] Email de partage des Google Docs (actuellement `quentin.riviere69@gmail.com`).
- [ ] Bio « À propos » de la description (`yt-description`), écrite d'après le cadre : à valider.
- [ ] Hashtags LinkedIn : 3-5 ou aucun.
- [ ] Shorts : déposer la méthode de script et le style de montage dans `yt-shorts-script/references/` et `yt-shorts-montage/references/` ; choisir l'outil d'avatar/voix IA ; préciser « 1 plan par ~0,8 s max ».
- [ ] Fiscalité FR dans `yt-veille/references/sources.md` : corrigé en 3916-bis (comptes à l'étranger) et 2086 (plus-values), à valider.

## 4. Assets à fournir

- [ ] Photos de Nass : neutre, sérieuse bouche fermée, poing sous le menton (`yt-miniature/references/nass/`).
- [ ] Référence du punk @punk6995 dans `yt-miniature/references/punk/` (une copie existe dans `yt-shorts-montage/projects/wallets/02-c-est-quoi-un-wallet/assets/punk6995.jpg`).
- [ ] Les portraits `wmremove-*.png` ont le fond de l'ancienne charte : garder ou refaire ?
- [ ] `composite.py` cité dans `yt-miniature/memory/choices.json` est absent du repo.

## 5. Code à corriger

- [x] `yt-analytics/analyze.py` : plus de CTR estimé (« n/d »), ouverture du rapport portable Mac/Windows (2026-10-13).
- [x] `yt-analytics/feedback_analyzer.py` : lit `_meta.youtube_video_id` et `_meta.published_at`, médiane sur toutes les vidéos de la période, périodes IA / crypto séparées (pivot 2026-10-07), listes vides et index `None` protégés (2026-10-13).
- [x] `yt-analytics/generate_dashboard.py` : totaux exclus, une section par période (2026-10-13).
- [x] `yt-analytics/parse_youtube_csv.py` : accepte l'export YouTube Studio en français (c'est le cas de Nass) et en anglais ; il refusait tous les CSV du dossier `inputs/` (2026-10-13).
- [x] Dépendances épinglées : `yt-veille/scripts`, `yt-analytics`, `yt-miniature/scripts` (2026-10-13).
- [x] `context/backlog.json` vidé, les 81 sujets IA sont dans `context/archive/backlog-ia-2026-03-31.json` (2026-10-13).
- [x] `yt-miniature/scripts/` (dont `composite.py`) et les polices `yt-miniature/assets/fonts/` ajoutés au repo (2026-10-13).
- [ ] **OAuth YouTube : le jeton est expiré (`invalid_grant`).** Nass lance `python3 yt-analytics/auth.py` (navigateur), puis `python3 yt-analytics/feedback_analyzer.py` pour rattacher les stats des 3 vidéos de la formation aux choix de miniature.
- [ ] Repo lourd (110 Mo de `.git`, 131 Mo de fichiers suivis dont ~100 Mo de vidéos dans `shows/`) : Git LFS n'est installé sur aucune machine. Décision de Nass : installer LFS des deux côtés, ou sortir les rendus du repo.
- [ ] `scripts/export_script.py` : export .docx figé sur un script IA de mars (contenu en dur). À supprimer ou à généraliser.
- [ ] Merger `rebrand/crypto` dans `master` une fois validé.

## 6. Veille (seulement si Nass décide de la relancer)

- [ ] `report.py` écrit `context/veille-top15.json` au lieu de `veille-top25.json` (nom lu par les skills), et le fichier reste sur le VPS.
- [ ] Filtre halal : n'exclut rien du top 25, rate « futures », « short x50 », « intérêts USDC », et exclut à tort les descriptions avec lien d'affiliation → filtre sur le titre avec limites de mots (`\b`), lu depuis `config/keywords.json`.
- [ ] Vieilles vidéos IA : rester seulement sur les chaînes de `channels.json`, limiter le maintien des « anomalies » à 30 jours.
- [ ] Cron : code de sortie ≠ 0 si trop d'échecs, `flock`, alerte en cas d'échec ; `report.py` doit charger le `.env` (Notion) et vérifier les réponses HTTP.
- [ ] La clé API YouTube apparaît en clair dans `/var/log/yt-veille.log` (URL d'erreur) : masquer.
- [ ] VPS encore sur `master` (`b6b1048`, chaînes IA) : `git checkout rebrand/crypto` le jour de la relance.
