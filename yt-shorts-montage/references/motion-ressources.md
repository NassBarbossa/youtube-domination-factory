# Ressources motion & montage (fournies par Nass, 2026-10-08)

Deux sources, résumées fidèlement. Elles alimentent la section « Méthode » du SKILL.md.

## 1. « Claude Motion Tips » (Notion withian)
Source : https://withian.notion.site/Claude-Motion-Tips-3ef057be92ba807db689d2571b6b7adf

### Effets open source (utilisables dans une composition HyperFrames, tout est HTML/JS)
Consigne de la source : donner le projet à Claude, lui demander de l'étudier, de trouver des démos et de proposer des idées.

| Projet | Ce que ça apporte | Démos |
|---|---|---|
| [Matter.js](https://github.com/liabru/matter-js) | Gravité, collisions, rebonds, ressorts. Faire tomber et s'empiler des cartes de mots. | https://brm.io/matter-js/demo/ |
| [Rough.js](https://github.com/rough-stuff/rough) | Contours « dessinés à la main », hachures : schémas, formes, logos. | https://roughjs.com/ |
| [PixiJS](https://github.com/pixijs/pixijs) + [filters](https://github.com/pixijs/filters) | Glitch, glow, ASCII, distorsion bulge, hachures sur texte ou image. | https://pixijs.io/filters/examples/ |
| [Anime.js](https://github.com/juliangarnier/anime) | Chorégraphie coordonnée de texte, formes et SVG. | https://animejs.com/ |
| [p5.brush](https://github.com/acamposuribe/p5.brush#core-concepts-in-1-minute) | Crayon, fusain, marqueur, aquarelle, hachures : textures faites main. | [teaser](https://editor.p5js.org/acamposuribe/sketches/bkb_CyJyi) · [Brush Maker](https://acamposuribe.github.io/p5.brush/tools/brush-maker.html) |
| [thinking-orbs](https://github.com/RareFormLabs/thinking-orbs) | Orbes en points animées (réflexion, recherche, chargement). | https://rareformlabs.github.io/thinking-orbs/ |

⚠️ Dans HyperFrames, tout effet doit rester **seekable et déterministe** (pas de `Math.random()` / `Date.now()`, simulation physique pilotée par le temps de la timeline, ou pré-calculée). Voir `/hyperframes-core`.

### Inspiration : 400+ vidéos faites avec Claude
Pour trouver un mouvement à adapter (révélation de texte, transition, rythme) :
- Galerie Skillry : https://skillry.dev/ai-videos/opus-5-5
- Collection GitHub (vidéos, posts sources, prompts partagés) : https://github.com/yihui-dev/awesome-opus5-5-videos

### Trois habitudes de travail (prompts exacts de la source)
**01 — Brief structuré en XML** (style, références, timing et livrable séparés ; recommandé par Anthropic) :
```
<art_direction>
Warm cream background. Brown type. Yellow textured brush accents.
</art_direction>
<references>
Use my attached frames for brush texture and text interaction.
</references>
<timing>
1 second total. Brush sweep at 0.00s; text lands at 0.35s;
hold the finished composition from 0.75s to 1.00s.
</timing>
<deliverable>
1080 x 1080, 30 fps. One shot. Export an MP4.
</deliverable>
```

**02 — Tester une seconde d'abord** (l'effet le plus dur, avant toute la vidéo) :
```
Before building the full video, make a 1-second test of a textured
brush circle drawing onto the screen. Use p5.js + p5.brush,
1080 x 1080 at 30 fps, with my supplied palette.
Share a playable preview so I can check the texture and motion
before expanding this effect into the full video.
```

**03 — Planche d'images clés avant le rendu** :
```
Before exporting the final video, show a contact sheet at the start,
each major beat or transition, and the final hold.
Label every frame with its timestamp.
Check for cropped text, accidental overlaps and elements
disappearing during transitions.
Wait for my feedback before the final render.
```
Ensuite : jouer un court aperçu pour juger le rythme et le mouvement.

## 2. « Montage avec Claude Code » (laforet.dev, Nicolas)
Source : https://laforet.dev/articles/montage-claude-code

Pipeline « rushes bruts → Reel Instagram monté » :

| Fonction | Outil de l'article | Équivalent retenu chez nous |
|---|---|---|
| Moteur vidéo | Remotion (vidéos en React) | **HyperFrames** (HTML + GSAP), déjà validé sur nos vidéos ; Remotion reste installé si besoin |
| Découpe des silences | FFmpeg | FFmpeg (`silencedetect` sur la forme d'onde) |
| Transcription + timings | Deepgram Nova-3 FR (payant) | `npx hyperframes transcribe` (Whisper local, gratuit) ; Deepgram en option |
| Cadrage / zoom sur le visage | MediaPipe | MediaPipe si besoin d'un suivi auto ; sinon punch-in HyperFrames (`/hyperframes-keyframes`) |
| Bruitages | Kenney, Pixabay, Freesound (CC0), Mixkit | Idem, **Freesound CC0 / Kenney en priorité** (licence claire) + SFX bundlés media-use |
| Musique | Pixabay Music (sans voix) | Pixabay Music ou synthé numpy (playbook) |
| Polices / icônes | Google Fonts / Iconify | Idem (Archivo Black + Public Sans) |

**Règle clé** : « Les timings de Deepgram ratent les vrais silences de 200 à 300 ms. » → **couper sur la forme d'onde du son, jamais sur les timestamps de la transcription.**

Méthode de l'article (recherche → `/grill-with-docs` → spec → tickets → un ticket par conversation, skills Matt Pocock) : **non retenue** pour les Shorts (doublon avec nos skills superpowers, trop lourd pour des vidéos de 30-60 s).
