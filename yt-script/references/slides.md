# Système de slides — détail (yt-script)

Référence chargée depuis `yt-script/SKILL.md` (Step 4, Phase C). Les règles courtes (mode dictée, centrage, animation sur mesure, `.md` synchronisé, données datées, vérif Playwright) restent dans le SKILL.md ; ce fichier contient le détail.

Charte : celle de `_shared/cadre-nass.md`, déjà codée en variables CSS dans `yt-script/references/slide-template.html` (`--bg`, `--sand`, `--sand-light`, `--sand-dark`, `--cream`, `--punk`, `--punk-dark`, `--grey-dark`, `--grey`). Partir du template, ne pas recoder la charte.

## 1. Marqueurs `[SLIDE: …]` (hors mode dictée)

Principe : une slide apparaît chaque fois que l'information passe mieux à l'image qu'à l'oral. Chaque marqueur du script devient une slide HTML.

| Déclencheur | Type | Format du marqueur | Exemple |
|---|---|---|---|
| Terme technique / jargon | `definition` | `[SLIDE: definition \| "Terme" \| Explication simple en 1 phrase]` | `[SLIDE: definition \| "Seed phrase" \| Les 12 ou 24 mots qui donnent accès à ton wallet. Qui les a, a tes cryptos.]` |
| Chiffre / statistique | `stat` | `[SLIDE: stat \| "Chiffre réel" \| Contexte court + source]` | `[SLIDE: stat \| "21 millions" \| Nombre maximum de bitcoins — bitcoin.org]` |
| Comparaison avant/après | `compare` | `[SLIDE: compare \| Label A : valeur A \| Label B : valeur B]` | `[SLIDE: compare \| Exchange centralisé : tes cryptos chez eux \| Wallet perso : tes cryptos chez toi]` |
| Liste de 3+ éléments | `bullets` | `[SLIDE: bullets \| Titre \| Item 1 \| Item 2 \| Item 3]` | `[SLIDE: bullets \| Avant d'acheter un coin \| Liquidité \| Contrat \| Répartition des holders]` |
| Citation | `quote` | `[SLIDE: quote \| "Citation exacte" \| Source]` | `[SLIDE: quote \| "A purely peer-to-peer version of electronic cash" \| Satoshi Nakamoto, whitepaper Bitcoin, 2008]` |
| Punchline / concept clé | `statement` | `[SLIDE: statement \| La phrase]` | `[SLIDE: statement \| On achète avant que ce soit connu de tous.]` |
| Timeline / chronologie | `timeline` | `[SLIDE: timeline \| Date 1 : événement \| Date 2 : événement]` | `[SLIDE: timeline \| 3 janv. 2009 : premier bloc Bitcoin \| 16 mars 2020 : lancement de Solana (mainnet beta)]` |
| Logos / marques | `logos` | `[SLIDE: logos \| Titre \| Marque1, Marque2, Marque3]` | `[SLIDE: logos \| Les wallets que tu vas utiliser \| Phantom, MetaMask]` |
| Graphique de prix | `chart` | `[SLIDE: chart \| Token \| Point 1 : prix (date) \| Point 2 : prix (date) \| Source]` | Données réelles uniquement (bougies d'exchange, date de création du pool), date sous chaque étiquette |

Autres types utilisés dans les squelettes : `transition`, `usecase`.

### Ordonnancement et nombre

- Une slide `definition` vient avant la slide `stat` ou `compare` qui utilise ce terme (d'abord comprendre, ensuite voir le chiffre).
- Audience débutante en crypto : chaque terme (wallet, seed phrase, DEX, CEX, liquidité, slippage, gas, explorer…) a sa slide `definition`.
- Nombre de slides : celui du tableau funnel du SKILL.md (TOP 12-18 · MIDDLE 20-28 · BOTTOM 30+). Les slides de transition comptent dans le total.
- Un concept par slide (jamais stat + définition ensemble). 4+ items du même type (ex. 4 blockchains) → une grille plutôt que 4 slides.
- Hors mode dictée, les slides résument visuellement : on ne recopie pas le script mot pour mot.

### Logos

Quand le script cite des marques, blockchains, tokens, wallets ou plateformes : vrais logos officiels, jamais d'icône SVG faite main ni d'émoji.
1. Télécharger les PNG officiels (fond transparent, ~512 px) dans `yt-script/outputs/logos/`, en kebab-case (`phantom.png`, `metamask.png`, `sol.png`).
2. Intégrer via `<img src="logos/[nom].png">`.
3. Sources : sites officiels, kits presse, UXWing, Brandfetch, SVGPorn.
4. Vaut aussi pour les slides `bullets` / grilles de plateformes : un vrai logo par carte.
5. Un SVG noir sur fond blanc est converti en version claire sans fond pour le fond sombre (ex. `logos/okx-white.svg`).

## 2. Squelette Google Doc (Phase B) — format

```
---
SLIDE 01 — [TYPE: transition]
Section : Acheter avant les autres
Sous-titre : Ce qui se passe avant qu'un token arrive sur un exchange
---

---
SLIDE 02 — [TYPE: definition]
Terme : DEX
Explication : Une plateforme d'échange sans intermédiaire : tu échanges directement depuis ton wallet.
Visuel : grosses lettres qui tombent + acronyme décomposé
---

---
SLIDE 03 — [TYPE: stat]
Chiffre : 21 millions
Contexte : le nombre maximum de bitcoins qui existeront un jour
Source : bitcoin.org
Visuel : compteur animé + carte crème néo-brutale
---
```

Chaque entrée : numéro + type, texte exact à l'écran, notes visuelles (effet, layout), source + date pour tout chiffre ou prix.

## 3. Mise en page et univers

- **Centrage** : `<section class="slide center …">` + `<div class="slide-content center">` sur toutes les slides, y compris transitions et layouts image + texte (le bloc entier est centré). Diagrammes (camemberts…) centrés, en grand, titre au-dessus, détail en dessous.
- **Polices** : Archivo Black (titres, chiffres) + Public Sans (400/600/800), déjà chargées par le template :
  `<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Public+Sans:wght@400;600;800&display=swap" rel="stylesheet">`
- **Cartes** : `.card` crème, `border: 3px solid #0B0B0B`, `box-shadow: 8px 8px 0 #9C7748`. Puces de liste = petits carrés (clin d'œil pixel).
- **Textes** : secondaire `rgba(244,239,231,0.78)`, muted `rgba(244,239,231,0.45)`.
- **Fond** : noir uni `#0B0B0B` + grille très légère (`.slide::before`, déjà dans le template). Les anciens fonds `bg-nass.png` / `bg-nass-v2.jpg` (grille orange/cyan) appartiennent à l'ancienne charte : ne plus les utiliser. Un fond illustré de la nouvelle charte (ex. montagnes au crépuscule) va sur `body` en `position: fixed` — jamais en `cover` sur chaque slide (saut visuel entre slides).

```css
body { background: var(--bg); } /* ou : url('[fond-nouvelle-charte]') center / cover fixed no-repeat, var(--bg); */
.slide { background: transparent; }
.glow-sand { background: linear-gradient(135deg, rgba(11,11,11,0.4) 0%, rgba(219,177,127,0.07) 100%); }
.glow-punk { background: linear-gradient(135deg, rgba(100,133,150,0.07) 0%, rgba(11,11,11,0.4) 100%); }
.glow-both { background: transparent; }
.glow-risk { background: linear-gradient(135deg, rgba(59,58,55,0.35) 0%, rgba(11,11,11,0.4) 100%); } /* baisse, risque, achat perdant */
```

- **Watermark** fixe « Nass Riviera » en bas à gauche (déjà dans le template) :
```css
.watermark { position: fixed; bottom: clamp(1rem, 2vw, 2rem); left: clamp(1.5rem, 3vw, 3rem); font-family: var(--font-display); font-size: clamp(0.65rem, 1vw, 0.85rem); color: rgba(244,239,231,0.25); z-index: 50; pointer-events: none; }
```
- **Disclaimer** : `<p class="disclaimer">Pas un conseil en investissement.</p>` sur la slide CTA (toujours) et, discrètement, sur une slide qui montre un token précis, un achat ou une performance.
- **Slides de transition** : gros numéro de section en filigrane (« 01 », « 02 ») en dégradé sable → bleu punk à 15 % d'opacité, barre de couleur (sable ou bleu punk) au-dessus du titre, titre en Archivo Black + sous-titre.
- **Visuels de concepts** : personnes/rôles = bonhommes SVG détaillés (tête + corps + attribut) ou le punk pixel pour Nass, pas d'icônes abstraites ; grilles de plateformes = 2×2 en cartes crème avec le vrai logo ; avant/après montré visuellement (ex. 20 bonhommes gris → 2 bonhommes sable, ceux qui achètent avant le listing) ; graphiques de prix = données réelles datées.
- **Assets brand** : si une image de Nass ou du punk @punk6995 est dans `yt-script/outputs/` (ex. `youtube_watermark_150x150.png`), l'utiliser sur la slide parcours.

## 4. Animations de base (template)

| Contexte | Animation | Classe CSS |
|---|---|---|
| Entrée standard | Fade + slide up | `reveal` |
| Bullet points | Slide from left, décalé | `reveal-left` |
| Gros chiffres | Scale in (0.7 → 1) | `reveal-scale` |
| Quotes / moments dramatiques | Blur in | `reveal-blur` |
| Punchlines | Dégradé animé (sable → sable clair) | `gradient-shift` |
| Titre slide 1 | Glitch (sable / bleu punk) | `glitch` |
| Stats numériques | Compteur JS de 0 à N | `counter` data-target="N" |
| Quotes | Curseur typing clignotant | `typing-cursor` |
| CTA | Pulse sur l'ombre pleine de la carte | `cta-pulse` |
| Slide titre | Particules tombantes sable/or (canvas) | `#particleCanvas` |

Particules (slide titre) : ~120 particules, 1-4 px, opacité 20-80 %, 70 % sable `219,177,127` / 30 % crème `244,239,231`, vitesse verticale 0.3-1.1 avec légère dérive ; variante carrée (pixel) possible.

Ces animations de base ne suffisent pas pour une slide clé : voir la bibliothèque ci-dessous.

## 5. Bibliothèque de patterns sur mesure (deck de référence)

Deck de référence : `yt-script/outputs/investissement-on-chain-visual.html` (validé « gigabanger » par Nass). On reprend ses **patterns d'animation** (structure HTML/CSS/JS), mais avec la charte du cadre : ce deck est encore dans l'ancienne charte (Syne/Inter, `#FF6B35` / `#00E5FF`).

| Intention | Pattern | Classes |
|---|---|---|
| Transformation / potentiel | Bonhomme gris → flash → super-héros (cape, masque, emblème) puis décollage | `hero-stage transform` / `fly` |
| Punchline choc (« banger ») | Mots en slam + flash blanc + tremblement + rayons qui tournent + mini-courbe « Toi / Les autres » | `bang-slide` |
| Chaos / abondance | Bouton martelé qui fait jaillir 24 tokens sur tout l'écran | `mint-slide` |
| Univers « Far West » | Coucher de soleil rétro, cactus, virevoltant, affiche WANTED, police **Rye** (exception de charte propre à cette scène), impacts de balle | `farwest` (+ `crew-slide` pour la bande de cowboys) |
| Rareté (« très peu », « encore moins ») | Grille de points qui s'éteignent / 3 points → 1 sable/or | `fr-crowd`, `few-dots` |
| Sigle | Grosses lettres qui tombent + « **C**entralized **EX**change » | `dex-big`, `cex-acro` |
| Rôle d'une plateforme | Logo en haut + 2 cartes numérotées animées | `okx-role` |
| Choix | Chemin qui se sépare en 1 / 2, étiquettes `Choix 1` / `Choix 2` | `fork`, `choice-tag` |
| Régularité | 12 barres Jan → Déc qui montent | `months` |
| Fin / validation | Drapeau à damier, gros ✓ | `flag`, `ok-check` |
| CTA description | Pastille « Lien dans la description » + flèche ↓ qui rebondit | `desc-cta` |

### Conversion ancienne charte → charte du cadre (OBSOLÈTE depuis le 2026-10-16 : Nass a remis la charte orange / cyan pour les slides, voir `_shared/cadre-nass.md` ; on reprend le deck de référence tel quel, tableau gardé pour mémoire)

À appliquer à chaque pattern copié depuis le deck de référence :

| Ancien | Nouveau |
|---|---|
| `--orange` / `#FF6B35` | `--sand` / `#DBB17F` |
| `--cyan` / `#00E5FF` | `--punk` / `#648596` |
| `--red` | `--sand-dark` (`#9C7748`) ou `--grey` (`#9A968D`) |
| fond `#0A0A0A` | `--bg` / `#0B0B0B` |
| `Syne` | `Archivo Black` |
| `Inter` | `Public Sans` |
| badge `.pt-date` `#FFB020` | `--sand-light` / `#F3D6A8` |

### Règles techniques

- Déclencher les animations via `.visible` (ajoutée par l'IntersectionObserver), avec des `animation-delay` pour laisser le texte arriver d'abord (~1 s).
- Préfixer les classes par slide et vérifier avec `grep` qu'un nom n'existe pas déjà : un conflit (ex. `.dl` déjà utilisé par `def-lines`) a cassé le « DEX » géant.
- Graphiques de prix : la date sous chaque étiquette de prix (`.pt-date`), chaque date venant d'une source réelle (bougies Binance, date de création du pool, horodatage décodé de l'ID du tweet) — jamais de mémoire.

## 6. Vérification Playwright (détail)

- `chromium.launch({channel:'chrome'})`, viewport 1600×900, attendre la fin des animations, capturer chaque slide modifiée.
- Regarder les captures : chevauchements, texte illisible (crème sur sable, sable sur crème), mot orphelin (utiliser `&nbsp;`), éléments hors cadre.
- Aucune erreur JS (`pageerror`).
- Ouvrir le deck sur la bonne slide avec `fichier.html#N` (navigation par ancre du template).
