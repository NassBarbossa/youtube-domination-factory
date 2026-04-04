# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

YouTube Domination Factory is a **modular AI skill system** for Claude Code that orchestrates the entire YouTube video production lifecycle. It targets the **Claude Code / AI trends / business opportunities** niche for a French-speaking audience (men 26-35, entrepreneurs/executives, non-technical).

The project is a collection of SKILL.md files loaded into Claude's skill system, plus Python scripts for automated veille (yt-veille) and analytics (yt-analytics) that run on a VPS.

## Architecture

Nine skills form a production pipeline:

```
yt-veille (Trend Research — automated daily scraping + scoring)
    ↓
yt-script (Script Writing)
    ├→ yt-titres-seo (SEO Titles) ──→ yt-miniature (Thumbnail Briefs)
    │                              └→ yt-description (Description & Tags)
    ├→ yt-montage (Editing Briefs)
    └→ yt-repurposing (Shorts, X threads, LinkedIn)

yt-analytics (Performance Analysis) ──→ yt-calendrier (Editorial Calendar)
```

Each module contains a single `SKILL.md` with YAML frontmatter (name, description, version, triggers) and markdown instructions. Some modules have a `references/` subfolder with templates or source lists.

## Key Inter-Skill Data Flows

- **yt-titres-seo → yt-miniature**: Title and thumbnail must COMPLEMENT each other, never duplicate
- **yt-titres-seo → yt-description**: Primary/secondary keywords are shared for SEO consistency
- **yt-montage → yt-description**: Timestamps must be coordinated for video chapters
- **yt-script → yt-repurposing**: Scripts must contain extractable Shorts moments
- **yt-analytics → yt-calendrier**: Performance data drives the content mix (40% tutorials, 25% news, 20% deep dives, 10% comparisons, 5% community)

## Content Voice

- **Tone**: Calm, pedagogical, laid-back (Nass Riviera's voice) — never hype-bro or corporate
- **Language**: French-first, accessible to non-technical people
- **Rule**: No filler — every sentence serves the viewer
- **Angle**: Always explain the concrete business/time-saving opportunity behind AI topics

## Script Markers

Scripts use visual markers: `[FACE CAM]`, `[SCREEN]`, `[DEMO]`, `[B-ROLL]` to indicate shot types for the editing team.

---

# Multi-Agent Architecture v2.0

Starting from March 2026, the system supports **automated multi-agent orchestration** in addition to manual skill-by-skill workflows. This dramatically reduces manual copy-paste between skills and enables end-to-end pipeline automation.

## How It Works

### The Orchestrator

One master skill (`yt-orchestrator`) manages the entire pipeline:
- Detects user intent (Mode A: topic provided, Mode B: find ideas first)
- Creates a shared JSON context file (`context/video-context.json`)
- Spawns agent instances using Claude Code's `Agent` tool
- Passes context to each agent, collects outputs, feeds them to the next agent
- Pauses for human validation at critical steps (Phase 3: title, thumbnail, description)
- Handles errors and session recovery

### Shared Context File

**Location**: `context/video-context.json`

This single JSON file is the "bus" through which all agents communicate:
```json
{
  "_meta": {version, slug, status, pipeline_step, ...},
  "request": {raw_input, topic, language},
  "veille": {selected_idea, status, ...},
  "script": {slug, file_path, word_count, structure, ...},
  "titres_seo": {winning_title, keywords, ...},
  "miniature": {recommended_concept, ...},
  "description": {description_full, tags, ...},
  "repurposing": {shorts[], x_thread_full, linkedin_full, ...},
  "pipeline_log": [...]
}
```

Each agent:
1. **Reads** from its input section (e.g., yt-script reads `request.topic` and `veille.selected_idea`)
2. **Writes** to its output section (e.g., yt-script writes `script.*`)
3. **Ignores** sections it doesn't care about

### Two Modes of Operation

#### Mode A: Topic Provided
User says: *"Fais une vidéo sur Claude Code 4"*

```
yt-orchestrator
├─ Phase 1 → yt-script (writes script.*)
├─ Phase 2 → [parallel] yt-titres-seo + yt-miniature + yt-description
├─ Phase 3 → PAUSE for human validation (title ✓ thumbnail ✓ description ✓)
└─ Phase 4 → yt-repurposing (writes shorts, threads, LinkedIn posts)
```

#### Mode B: Find Ideas First
User says: *"Trouve moi un sujet de vidéo"*

```
yt-orchestrator
├─ Phase 0.5 → yt-veille (generates 3-5 ideas, PAUSE for choice)
├─ Phase 1 → yt-script (writes script.*)
├─ Phase 2 → [parallel] yt-titres-seo + yt-miniature + yt-description
├─ Phase 3 → PAUSE for human validation
└─ Phase 4 → yt-repurposing
```

### Pipeline Phases

| Phase | Agent(s) | Action | Pause? |
|-------|----------|--------|--------|
| 0 | orchestrator | Init slug, create JSON | No |
| 0.5 | yt-veille | Generate ideas (Mode B only) | **Yes** — user chooses |
| 1 | yt-script | Write full script | No |
| 2a | yt-titres-seo | Generate titles & keywords | No |
| 2b | yt-miniature | Design thumbnail concept | No (parallel with 2a/2c) |
| 2c | yt-description | Write description & tags | No (parallel with 2a/2b) |
| 3 | orchestrator | Present validation summary | **Yes** — user validates title, thumbnail, description |
| 4 | yt-repurposing | Create shorts, threads, LinkedIn posts | No |
| 5 | orchestrator | Generate recap, archive JSON | No |

### Context Protocol (in Each Skill)

Each skill now has a **Context Protocol** section that defines:
- **Autonomous mode**: How to read from JSON, process without user interaction, write back to JSON
- **Manual mode**: Traditional workflow (preserved for backward compatibility)

When `yt-orchestrator` spawns an agent, it provides:
```
"Read context/video-context.json as input.
Operate autonomously (no interactive validation).
Write your outputs directly to context/video-context.json.
Report completion."
```

### Session Recovery

If the pipeline is interrupted:
1. `yt-orchestrator` reads `_meta.pipeline_step`
2. Offers to resume from that step or restart
3. Agents read the existing JSON and continue from where it left off

---

## Manual Mode (Fully Preserved)

**Every skill continues to work 100% normally if called directly.**

Examples:
- `/yt-script "write a script about Claude Code"` → Uses classic workflow (Step 1-6 with interaction)
- `/yt-titres-seo` → Presents 5 title options for choice
- `/yt-miniature` → Shows 3 concepts for selection

The Context Protocol is **transparent** — it only activates when:
1. An agent is spawned by `yt-orchestrator` (detected via prompt)
2. `context/video-context.json` exists and is passed as input

Manual invocation is never forced. Nass can still:
- Mix orchestrated and manual workflows
- Call individual skills directly
- Manually copy-paste between skills (old way still works)

---

## Key Design Decisions

1. **One-way data flow from script to repurposing** — ensures dependencies are met
2. **Parallel Phase 2** — faster turnaround (3 agents at once instead of sequentially)
3. **Validation pause before repurposing** — title/thumbnail/description must be approved before creating multi-platform content
4. **Archive versioning** — each completed pipeline is saved to `context/archive/[slug]-[timestamp].json` for history
5. **No breaking changes** — manual mode still works, orchestrator is optional

---

## Implementation Checklist

- [x] Create `context/video-context.json` template
- [x] Create `yt-orchestrator/SKILL.md` (master orchestrator)
- [x] Add Context Protocol to `yt-script/SKILL.md`
- [x] Add Context Protocol to `yt-titres-seo/SKILL.md`
- [x] Add Context Protocol to `yt-miniature/SKILL.md`
- [x] Add Context Protocol to `yt-description/SKILL.md`
- [x] Add Context Protocol to `yt-repurposing/SKILL.md`
- [x] Add Context Protocol to `yt-veille/SKILL.md`
- [ ] Delete `yt-montage/` (replaced by better tooling)
- [ ] Update `yt-analytics/SKILL.md` (Sprint 2)
- [x] Implement cron job for `yt-veille` — daily scraping at 5h30 SGT
- [x] SQLite database (veille.db) — channels, videos, snapshots tables
- [x] Composite scoring (views abs 30%, velocity 25%, outlier 15%, views/subs 15%, engagement 15%)
- [x] Tier-based channel weighting (67 channels, Tier 1-3 + Non classé)
- [x] Time decay for video freshness
- [x] report.py — top 25 → Notion + JSON (context/veille-top25.json)
- [x] Upgraded slide system for yt-script (responsive, animations, keyboard nav)

---

## Testing the v2.0

**Quick Test**:
```
User: "Fais une vidéo sur Claude Code 4"

Expected:
1. yt-orchestrator detects Mode A
2. Generates slug "claude-code-4"
3. Spawns yt-script
4. Spawns yt-titres-seo, yt-miniature, yt-description in parallel
5. Presents validation summary
6. Awaits "OK" from user
7. Spawns yt-repurposing
8. Presents final recap
```

All intermediate data should be visible in `context/video-context.json`.

---

## Maintenance & GitHub

### When Pushing to GitHub

**Important:** Every time you make architecture changes and push to GitHub, **update README.md** to keep documentation in sync.

**Checklist before `git push`:**

- [ ] Architecture changes? → Update [README.md](README.md) sections:
  - "The Pipeline" (if phases change)
  - "Skills Included" (if skills are added/removed)
  - "Data Flow Example" (if context structure changes)

- [ ] New skill added? → Add row to "Skills Included" table in README

- [ ] Phase changes or orchestrator logic modified? → Update "The Pipeline" diagram in README

- [ ] New features? → Update "Key Features" checklist

- [ ] Sprint 2 progress? → Update "Sprint 2 (Planned)" section

**Example commit message:**
```
git commit -m "feat: Add new Phase X

- Modified yt-orchestrator/SKILL.md (Phase X logic)
- Updated CLAUDE.md (architecture section)
- Updated README.md (pipeline diagram + data flow)"
```

### README Structure

The README.md is the **public-facing documentation**. Keep these sections up-to-date:
- Quick Start (if triggers change)
- Architecture v2.0 → The Pipeline (if phases change)
- Skills Included (if skills change)
- Data Flow Example (if context.json structure changes)
- Key Features (if capabilities change)
- Sprint 2 (if roadmap updates)

CLAUDE.md is the **internal guidance** for developers. It's more detailed but README is what users see first.
