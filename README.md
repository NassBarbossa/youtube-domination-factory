# 🎬 YouTube Domination Factory

**The AI-powered end-to-end YouTube video production pipeline.** One topic → Complete video + multi-platform content (Shorts, X threads, LinkedIn posts) in hours.

Built for the **Claude Code / AI trends / business opportunities** niche, targeting non-technical entrepreneurs (26-35, French-speaking).

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
User: "Fais une vidéo sur Claude Code 4"

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
| **yt-veille** | AI trend research & video ideas — automated daily scraping of 67 channels, composite scoring, top 25 report | "trouve moi des idees", "tendances IA", "sujet de video" |
| **yt-analytics** | Channel performance analysis | "analyse mes stats", "YouTube stats" |
| **yt-calendrier** | Editorial calendar planning | "calendrier", "schedule", "planning video" |

---

## 📖 How to Use

### 1. **Direct Topic (Fastest)**
```
/yt-orchestrator "Fais une vidéo sur Claude Code 4"
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
/yt-script "Write a script about AI agents"
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
   /yt-orchestrator "Fais une vidéo sur Claude Code 4"
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

**Target Audience:** Men 26-35, entrepreneurs/executives, non-technical, want to turn creativity/ideas into reality using AI

**Tone:** Calm, pedagogical, laid-back (Nass Riviera's voice)
- Never hype-bro or corporate
- No jargon without explanation
- Focus on business opportunity angle
- Every sentence must serve the viewer

**Content Mix (data-driven):**
- 40% Tutorials ("How to...")
- 25% News (trends, new features)
- 20% Deep dives (detailed explanations)
- 10% Comparisons (X vs Y)
- 5% Community engagement

---

## 🔄 Data Flow Example

**Input:** "Fais une vidéo sur les AI Agents"

```
Phase 1: yt-script reads request.topic → writes script.*
         └─ script.word_count = 1800
         └─ script.structure.shorts_moments = [{start:45, end:60, ...}, ...]

Phase 2a: yt-titres-seo reads script.* → writes titres_seo.*
          └─ winning_title = "I Built an AI Agency with 0 Employees"
          └─ primary_keyword = "AI agents"
          └─ secondary_keywords = ["claude code", "automation", ...]

Phase 2b: yt-miniature reads script.* + titres_seo.winning_title → writes miniature.*
          └─ text_overlay = "0 EMPLOYEES" (NOT repeating the title!)
          └─ color_palette = ["#FF6B00", "#FFFFFF"]

Phase 2c: yt-description reads script.* + titres_seo.* → writes description.*
          └─ hook_framework = "PAS" (Problem → Agitation → Solution in first 150 chars)
          └─ description_full = "Tu galères à gérer une équipe ? Ça te coûte..."
          └─ tags = ["claude code", "ai agents", "automation", ...]
          └─ sources = ["https://docs.anthropic.com/...", "https://..."]

Phase 3: USER VALIDATES → clicks "OK"

Phase 4: yt-repurposing reads validated script.* + titres_seo.winning_title → writes repurposing.*
         └─ shorts[0] = {hook: "0 employés, 1 IA — attends la fin", ...}  (5-7 word hooks, captions mandatory)
         └─ x_thread = "J'ai construit une agence IA sans employés..." (71-100 chars/tweet, NO link in thread)
         └─ x_reply_link = "Vidéo complète ici 👇 [URL]"  (link in reply = -50% reach penalty avoided)
         └─ linkedin = "Il y a 6 mois, j'avais 3 employés..." (1300-1600 chars, PAS framework hook)
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

---

## 🔮 Sprint 2 (In Progress)

- [x] Cron job for `yt-veille` — daily scraping at 5h30 SGT (67 channels, ~300 videos/day)
- [x] SQLite database for video metrics + daily snapshots
- [x] Composite scoring: views abs (30%) + velocity (25%) + outlier (15%) + views/subs (15%) + engagement (15%)
- [x] Tier-based channel weighting (Tier 1 ×1.5, Tier 2 ×1.2)
- [x] Time decay for freshness (< 24h ×1.0, 1-3d ×0.85, 3-6d ×0.65, 7d+ excluded)
- [x] Automated top 25 report → Notion + JSON for orchestrator
- [x] Topic extraction (claude-code, vibe-coding, ai-agents, etc.)
- [ ] Analytics integration (`yt-analytics` context protocol)
- [ ] Calendar sync (`yt-calendrier` context protocol)
- [ ] Posting schedule automation

### yt-veille Architecture

```
daily_monitor.py (cron 5h30 SGT)
    → Scrapes 67 YouTube channels via API
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
- **67 YouTube channels** tracked daily (US + FR)
- **~300 videos** scraped per day
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

Built with ❤️ for creators who want to scale without hiring a team.
