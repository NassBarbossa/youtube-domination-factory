# 🎬 YouTube Domination Factory

**The AI-powered end-to-end YouTube video production pipeline.** One topic → Complete video + multi-platform content (Shorts, X threads, LinkedIn posts) in hours.

Construit pour la chaîne YouTube **100 % crypto** de Nass Riviera — « Investisseur on-chain · spot, zéro levier, wallet public » ([nassriviera.com](https://nassriviera.com)). Public : hommes francophones de 25 à 40 ans, déjà investisseurs (surtout immobilier), débutants en crypto.

## ✨ What It Does

Instead of manually calling 9 separate tools and copy-pasting outputs between them, YouTube Domination Factory **automates the entire workflow**:

```
📝 Topic Input
    ↓
🎯 Script Generation
    ↓
[Parallel] Title + Thumbnail + Description
    ↓
✅ Human Validation Pause
    ↓
📱 Multi-Platform Repurposing (Shorts + X + LinkedIn)
    ↓
🎉 Final Video Package
```

**One command. One file. Zero manual work between steps.**

---

## 🚀 Quick Start

### Mode A: You Have a Topic

```
User: "Fais une vidéo sur comment acheter sa première crypto on-chain"

→ yt-orchestrator spawns the entire pipeline autonomously
→ Returns fully-written script, SEO titles, thumbnail brief, description, Shorts, X thread, LinkedIn post
→ Everything ready to publish
```

### Mode B: You Want Ideas First

```
User: "Trouve moi un sujet de vidéo"

→ yt-veille generates 3-5 trending ideas with scoring
→ You pick one
→ Rest of pipeline runs automatically
```

---

## 📊 Architecture v2.0

### The Pipeline

```
yt-orchestrator (Master)
├─ Phase 0: Initialize context (slug, JSON bus)
├─ Phase 0.5: yt-veille (idea generation — Mode B only)
├─ Phase 1: yt-script (full video script)
├─ Phase 2: [Parallel execution]
│   ├─ yt-titres-seo (SEO-optimized titles + keywords)
│   ├─ yt-miniature (thumbnail concept brief)
│   └─ yt-description (YouTube description + tags)
├─ Phase 3: 🛑 VALIDATION PAUSE (user approves title, thumbnail, description)
├─ Phase 4: yt-repurposing (Shorts clips + X threads + LinkedIn posts)
└─ Phase 5: Recap + Archive JSON
```

### Shared Context File

All agents communicate through a single JSON bus: **`context/video-context.json`**

```json
{
  "_meta": {slug, status, pipeline_step, ...},
  "request": {topic, language, ...},
  "script": {full_script, structure, word_count, ...},
  "titres_seo": {winning_title, keywords, ...},
  "miniature": {recommended_concept, ...},
  "description": {full_description, hook_framework, tags, enriched_keywords, sources, cta_type, ...},
  "repurposing": {shorts[], x_thread, x_reply_link, linkedin_post, linkedin_format_bonus, ...},
  "pipeline_log": [...]
}
```

**No manual copy-paste.** Data flows automatically from script → titles → thumbnail → description → repurposing.

---

## 🛠️ Skills Included

| Skill | Purpose | Triggers |
|-------|---------|----------|
| **yt-orchestrator** | Master pipeline controller | "fais une vidéo sur", "lance le pipeline", "trouve moi des idées" |
| **yt-script** | Full video scriptwriting | "ecris le script", "prepare le script" |
| **yt-titres-seo** | SEO-optimized title generation | "titre video", "SEO title" |
| **yt-miniature** | Thumbnail concept briefs | "miniature", "thumbnail", "design thumbnail" |
| **yt-description** | YouTube description + tags | "ecris la description", "YouTube description" |
| **yt-repurposing** | Multi-platform content transformation | "repurpose", "shorts", "thread X", "LinkedIn post" |
| **yt-shorts-script** | Scripts de Shorts natifs (30-60 s, 9:16) — fondations | "écris un short", "script short", "bombarde les shorts" |
| **yt-shorts-montage** | Montage des Shorts (HyperFrames, sous-titres, 1080×1920) — fondations | "monte le short", "montage short" |
| **yt-veille** | Veille crypto & idées de vidéos — scraping quotidien automatisé des chaînes suivies, scoring composite, rapport top 25 | "trouve moi des idees", "tendances crypto", "sujet de video" |
| **yt-analytics** | Channel performance analysis | "analyse mes stats", "YouTube stats" |
| **yt-calendrier** | Editorial calendar planning | "calendrier", "schedule", "planning video" |

---

## 📖 How to Use

### 1. **Direct Topic (Fastest)**
```
/yt-orchestrator "Fais une vidéo sur comment acheter sa première crypto on-chain"
```
Pipeline runs → You get validation prompt at Phase 3 → Approve → Done ✅

### 2. **Search Ideas First**
```
/yt-orchestrator "Trouve moi un sujet de vidéo"
```
→ yt-veille generates ideas → You pick one → Pipeline continues

### 3. **Individual Skills (Manual Mode)**
Each skill still works standalone:
```
/yt-script "Écris le script sur le wallet public du challenge 10K → 100K"
/yt-titres-seo
/yt-miniature
```
100% backward compatible — Context Protocol is **transparent**.

---

## ⚙️ Setup & Installation

### Requirements
- **Claude Code** (claude.ai/code) with skill system access
- No dependencies, no build steps, no runtime environment
- Just text files (SKILL.md) + JSON

### Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/NassBarbossa/youtube-domination-factory.git
   ```

2. **Load skills into Claude Code**
   - Copy all `yt-*/SKILL.md` files into Claude's skills directory
   - Restart Claude Code

3. **Ready to go!**
   ```
   /yt-orchestrator "Fais une vidéo sur comment acheter sa première crypto on-chain"
   ```

---

## 📚 Documentation

- **[CLAUDE.md](CLAUDE.md)** — Deep dive into architecture, multi-agent design, context protocol
- **[yt-orchestrator/SKILL.md](yt-orchestrator/SKILL.md)** — Orchestrator phases, error handling, session recovery
- **[yt-script/SKILL.md](yt-script/SKILL.md)** — Script writing framework + context protocol
- **[yt-titres-seo/SKILL.md](yt-titres-seo/SKILL.md)** — SEO title generation + context protocol
- **[yt-miniature/SKILL.md](yt-miniature/SKILL.md)** — Thumbnail concept design + context protocol
- **[yt-description/SKILL.md](yt-description/SKILL.md)** — YouTube description + tags + context protocol
- **[yt-repurposing/SKILL.md](yt-repurposing/SKILL.md)** — Multi-platform repurposing + context protocol
- **[yt-veille/SKILL.md](yt-veille/SKILL.md)** — Trend research + idea generation + context protocol

---

## 🎯 Content Voice & Audience

**Positionnement :** « Nass Riviera · Investisseur on-chain · spot, zéro levier, wallet public ». Avatar visuel : le punk pixel @punk6995 (Barbossa).

**Target Audience** (mots de Nass) :
> « C'est des hommes entre 25 et 40 ans. Ils sont débutants, voire débutants plus. C'est déjà des investisseurs, principalement en immobilier avec crédit, mais ils n'ont pas commencé encore à investir dans la crypto. Peut-être un peu de bourse, mais pas de crypto. Et il n'y comprend rien, il ne connaît rien. Et nous, du coup, on vend le fait qu'on achète des cryptos en dehors des échanges avant qu'elles soient connues de tous. »

**Offres :** challenge public 10K → 100K $ (wallet public Solana + EVM, chaque trade expliqué en live avant le résultat), formation offerte en 3 vidéos (« Pourquoi investir en 2026 », « Comment devenir riche », « L'investissement on-chain »), communauté privée (trades du challenge en direct), live hebdo « Convergence » avec Sadek (marchés / or).

**Ton :** direct, transparent, pédagogique (la voix de Nass Riviera)
- « Les bons trades comme les mauvais. Pas de compte démo, pas de screen retouché. »
- Jamais hype, jamais de promesse de gain
- Aucun jargon sans explication
- Chaque phrase sert le spectateur
- Disclaimer systématique : « Pas un conseil en investissement. »

**Règle halal (non négociable) :** spot uniquement. Jamais de levier, futures, short, marge, prêt/emprunt à intérêt (lending, yield à intérêt), ni de casino/paris/jeu d'argent. Jamais d'incitation au crédit. Memecoins et tokens en pré-lancement présentés comme des paris risqués à petite taille, risque dit clairement. Pas de chiffres inventés, pas de faux témoignages. Détails dans [CLAUDE.md](CLAUDE.md).

**Charte :** fond noir `#0B0B0B`, sable/or `#DBB17F` (clair `#F3D6A8`, foncé `#9C7748`), crème `#F4EFE7`, bleu punk `#648596` / `#4F6C7B`, gris `#3B3A37` / `#9A968D`. Polices Archivo Black (titres) + Public Sans (texte). Univers punk pixel, montagnes au crépuscule, cartes crème à bord noir avec ombre pleine.

**Content Mix :** tutoriels, actus, deep dives, comparatifs, communauté — répartition à recalibrer sur les données de la chaîne crypto.

---

## 🔄 Data Flow Example

**Input:** "Fais une vidéo sur comment acheter sa première crypto on-chain"

```
Phase 1: yt-script reads request.topic → writes script.*
         └─ script.word_count = 1800
         └─ script.structure.shorts_moments = [{start:45, end:60, ...}, ...]

Phase 2a: yt-titres-seo reads script.* → writes titres_seo.*
          └─ winning_title = "Acheter une crypto AVANT qu'elle soit sur Binance"
          └─ primary_keyword = "acheter crypto on-chain"
          └─ secondary_keywords = ["wallet crypto", "investir crypto débutant", ...]

Phase 2b: yt-miniature reads script.* + titres_seo.winning_title → writes miniature.*
          └─ text_overlay = "AVANT TOUT LE MONDE" (NOT repeating the title!)
          └─ color_palette = ["#0B0B0B", "#DBB17F", "#F4EFE7"]

Phase 2c: yt-description reads script.* + titres_seo.* → writes description.*
          └─ hook_framework = "PAS" (Problem → Agitation → Solution in first 150 chars)
          └─ description_full = "Tu investis déjà dans l'immobilier mais la crypto te paraît floue ? ..."
          └─ tags = ["crypto débutant", "acheter crypto on-chain", "wallet crypto", ...]
          └─ sources = ["https://solscan.io/...", "https://..."]

Phase 3: USER VALIDATES → clicks "OK"

Phase 4: yt-repurposing reads validated script.* + titres_seo.winning_title → writes repurposing.*
         └─ shorts[0] = {hook: "Tu achètes tes cryptos au mauvais endroit", ...}  (5-7 word hooks, captions mandatory)
         └─ x_thread = "La plupart des gens achètent une crypto quand elle arrive sur un exchange..." (71-100 chars/tweet, NO link in thread)
         └─ x_reply_link = "Vidéo complète ici 👇 [URL]"  (link in reply = -50% reach penalty avoided)
         └─ linkedin = "Tu as un crédit immobilier, un PEA, et zéro crypto..." (1300-1600 chars, PAS framework hook, disclaimer inclus)
```

**Result:** All outputs in `context/video-context.json` + individual files in `yt-script/outputs/`, etc.

---

## ✅ Key Features

- ✅ **Autonomous pipeline** — One command, entire workflow runs
- ✅ **Parallel execution** — Titles, thumbnail, description generated simultaneously
- ✅ **Human validation** — Pause before repurposing for final approval
- ✅ **Multi-platform** — Shorts + X threads + LinkedIn posts auto-generated
- ✅ **Shared context** — Single JSON file for all inter-agent communication
- ✅ **Session recovery** — Interrupt and resume from any phase
- ✅ **Manual mode preserved** — Every skill still works standalone
- ✅ **Error handling** — Pipeline logs + error reporting
- ✅ **No breaking changes** — 100% backward compatible
- ✅ **Dictated slides** — Say "slide après" sentence by sentence: one slide per sentence, custom animation each, auto-checked with Playwright screenshots

---

## 🔮 Sprint 2 (In Progress)

- [x] Cron job for `yt-veille` — daily scraping at 5h30 SGT (liste des chaînes suivies en refonte pour la niche crypto)
- [x] SQLite database for video metrics + daily snapshots
- [x] Composite scoring: views abs (30%) + velocity (25%) + outlier (15%) + views/subs (15%) + engagement (15%)
- [x] Tier-based channel weighting (Tier 1 ×1.5, Tier 2 ×1.2)
- [x] Time decay for freshness (< 24h ×1.0, 1-3d ×0.85, 3-6d ×0.65, 7d+ excluded)
- [x] Automated top 25 report → Notion + JSON for orchestrator
- [x] Topic extraction (catégories à adapter à la niche crypto)
- [ ] Analytics integration (`yt-analytics` context protocol)
- [ ] Calendar sync (`yt-calendrier` context protocol)
- [ ] Posting schedule automation

### yt-veille Architecture

```
daily_monitor.py (cron 5h30 SGT)
    → Scrapes the tracked YouTube channels via API
    → Stores in SQLite: channels, videos, snapshots

scoring.py (stateless)
    → Computes composite score from DB data
    → No storage — called on demand

report.py (after scrape)
    → Applies tier boost + time decay
    → Generates top 25
    → Pushes to Notion (daily table)
    → Writes context/veille-top25.json for orchestrator
```

---

## 📊 Stats

- **9 specialized skills** + 1 orchestrator
- **Chaînes YouTube crypto** suivies chaque jour (liste en refonte)
- **5 validation phases** in the pipeline
- **2 operation modes** (topic-driven or idea-driven)
- **3 parallel agents** in Phase 2
- **1 shared JSON bus** for all communication
- **1 SQLite DB** for veille data
- **100% backward compatible** with manual workflows

---

## 🤝 Contributing

This is a production system for **Nass Riviera's YouTube channel**.

To contribute:
1. Understand the voice/audience (see Content Voice section)
2. Test changes in isolation first (manual skill trigger)
3. Test end-to-end pipeline ("fais une vidéo sur...")
4. Update CLAUDE.md if architecture changes
5. Submit PR with clear description

---

## 📜 License

MIT (or your preferred license)

---

## 🎬 Built With

- **Claude Code** — AI skill system
- **Claude API** — Multi-agent orchestration
- **Markdown + JSON** — Skills + context management

---

## 💬 Questions?

Check [CLAUDE.md](CLAUDE.md) for deeper architecture documentation or review individual skill files for specific functionality.

**Quick reference:**
- How does the orchestrator work? → [yt-orchestrator/SKILL.md](yt-orchestrator/SKILL.md)
- How do agents share data? → [CLAUDE.md](CLAUDE.md#shared-context-file)
- How to run a pipeline? → [Quick Start](#quick-start) above
- Can I use just one skill? → Yes! Each skill works independently.

---

**Status:** ✅ v2.0 Live — Multi-Agent Architecture

Built with ❤️ pour la chaîne crypto de Nass Riviera. Pas un conseil en investissement.
