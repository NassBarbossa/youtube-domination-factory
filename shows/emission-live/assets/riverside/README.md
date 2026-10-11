# Convergence — Pack Riverside

Fichiers prêts à importer dans Riverside, aux formats demandés par sa documentation (vérifiée le 03/10/2026).

## Dans le studio (pendant le live) — menu **Brand** de la barre latérale

| Où dans Riverside | Fichier | Spéc. Riverside |
|---|---|---|
| **Logo** | `logo-studio-512.png` | JPG/PNG, carré 1:1 conseillé, 5 Mo max. S'affiche dans un coin (au choix). |
| **Background** (derrière les vignettes vidéo) | `fond-studio-1920x1080.png` | JPG/PNG 16:9, 1920 × 1080 conseillé. |
| **Overlay** (par-dessus tout l'écran) | `overlay-1920x1080.png` | JPG/PNG 16:9, transparence acceptée. Barre du haut (logo + épisode) et bandeau de cours en bas, le milieu reste transparent. |
| **Brand color** | Or `#C98A0B` ou Vert `#0F8A5F` | Couleur d'accent du studio. |
| **Brand font** (noms des participants) | Choisir *Inter* si proposée, sinon la sans-serif la plus proche | Liste imposée par Riverside, pas d'import de police. |

⚠️ **Overlay personnalisé** : d'après l'aide Riverside, les plans **Pro et Grow** ne permettent pas d'importer ses propres images d'overlay (seulement la bibliothèque Riverside). Il faut un plan **Business** (ou Webinar) pour utiliser `overlay-1920x1080.png`. Le logo et le fond, eux, marchent sur tous les plans.

⚠️ **Bandeau de cours** : sur Riverside, l'overlay est une image fixe, donc le bandeau ne défile pas et ses valeurs sont des **exemples**. Avant chaque live : mettre à jour `obs/convergence.js` (tableau `COURS`) puis régénérer l'overlay (ou demander à Claude).

## Fonds de caméra (chaque animateur, dans **Visual effects → Backgrounds**)

| Fichier | Pour | Spéc. Riverside |
|---|---|---|
| `fond-camera-cohost-1920x1080.png` | le co-host (accent or, « Marchés · Or ») | PNG/JPG < 4 Mo, 4096 px max. Plans Pro, Grow, Webinar, Business. |
| `fond-camera-nass-1920x1080.png` | Nass (accent vert, « Crypto ») | idem |

À n'utiliser que si vous filmez sans vrai décor : le détourage automatique n'est jamais parfait.

## Media Board (images et vidéos jouées en plein écran pendant le live)

| Fichier | Moment |
|---|---|
| `../video/convergence-intro-clair-1920x1080.mp4` | Ouverture du live (6 s) |
| `media-attente.png` | Avant le début (« On commence dans un instant ») |
| `media-sujet-exemple.png` | Exemple de carte de tendance. Pour chaque sujet, générer la sienne avec `obs/3-sujet.html?n=…&titre=…&mot=…&tags=…` |
| `media-fin.png` | Fin du live |

Spéc. Riverside : PNG/JPG, vidéos MP4/WEBM en H.264, 1080p max, 1 Go max. Le MOV transparent n'est **pas** accepté par le Media Board.

## Éditeur (montage du replay) — **Brand** dans l'éditeur

| Où | Fichier | Spéc. Riverside |
|---|---|---|
| **Logos** | `logo-editeur-128x72.png` | JPG/PNG, exactement 128 × 72 px. |
| **Colors** (5 max) | `#0B0E11` · `#C98A0B` · `#0F8A5F` · `#F2EFE8` · `#C8323F` | Hex. |
| **Design → Background** | `fond-studio-1920x1080.png` | Image. |
| **Intros** 16:9 | `../video/convergence-intro-clair-1920x1080.mp4` | Une version par format, sinon recadrage. |
| **Intros** 9:16 | `../video/convergence-intro-clair-1080x1920.mp4` | Pour les clips verticaux (Shorts, Reels, TikTok). |
| **Intros** 1:1 | `../video/convergence-intro-clair-1080x1080.mp4` | Pour les posts carrés. |

Plans de l'éditeur Brand : Pro, Grow, Webinar, Business.

## Ce qui ne passe pas dans Riverside

- Les écrans `obs/*.html` sont des pages animées : Riverside n'accepte que des **images fixes** (overlay, fond) et des **vidéos** (Media Board). Les PNG de ce dossier en sont les versions fixes.
- Le **compte à rebours** animé n'existe pas en image fixe. Si besoin, Claude peut générer une vidéo de compte à rebours en MP4 pour le Media Board.
- Les **bandeaux de noms** (lower thirds) se font directement dans Riverside (menu **Text**), avec les couleurs de la marque.

`_sources.html` = la page qui génère ces visuels (paramètre `?v=fond|overlay|cam-cohost|cam-nass|logoed`).
