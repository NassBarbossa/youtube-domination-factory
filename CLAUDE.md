# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

YouTube Domination Factory is a **modular AI skill system** for Claude Code that orchestrates the entire YouTube video production lifecycle. It targets the **Claude Code / AI trends / business opportunities** niche for a French-speaking audience (men 26-35, entrepreneurs/executives, non-technical).

There are no build steps, dependencies, tests, or runtime — the project is a collection of SKILL.md files loaded into Claude's skill system.

## Architecture

Nine skills form a production pipeline:

```
yt-veille (Trend Research & Ideas)
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
