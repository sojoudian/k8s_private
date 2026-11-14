# Report: PowerPoint Design Language Specification
**Date**: 2026-05-23
**Sequence**: #01 for the day

## Summary
Performed a comprehensive architectural analysis of the entire `k8s_week3/` project and
extracted the exact PowerPoint design language used across all four existing decks
(`Week3.pptx`, `Lab02.pptx`, `Week3_Hands_On_Lab.pptx`, `Lab03_Guide.pptx`, and their
intermediate generators). Captured the result as a single self-contained spec file,
`DESIGN_LANGUAGE.md`, that future deck-generation work can read once and reproduce the
style verbatim — no re-derivation from XML required.

## What Changed
- **`DESIGN_LANGUAGE.md`** — new (~21 KB) spec file at the project root. 14 sections covering:
  canvas/dimensions, full color palette (brand + semantic + step gradient + terminal palette,
  all hex values verified against Lab02 XML), typography (fonts + type scale + line spacing +
  casing rules), layout grid, mandatory chrome, all 17 reusable components (terminal, GOAL
  panel, step block, objective grid, comparison table, browser mockup, etc.), a catalogue of
  22 named slide templates with file/slide references, voice & tone, required assets,
  python-pptx scaffold, build workflow, file-naming conventions, anti-patterns to avoid,
  and a verification checklist.

## Technical Details

### How the spec was derived
1. **Inventoried the codebase**: 4 generator scripts (`build_week3.py`, `build_week03.py`,
   `build_lab.py`, `build_lab_guide.py`) — ~3300 LoC total — plus existing prior reports
   in `reports/` and the unpacked OOXML in `analysis/lab02_xml/`.
2. **Confirmed the palette empirically** by greping `<a:srgbClr val="…"/>` across all 18
   Lab02 slide XML files. Top colors (by frequency) match the constants already declared
   in the build scripts: `1FA8E0` blue, `37465A` slate, `868686` muted, `2A2A2A` terminal
   bg, `CFDBEE` lightblue, `3F3F3F` body. Step-gradient colors (`2466A0`, `2196A0`,
   `1F8FCD`, `1F7AB8`) also confirmed in slide5/6 XML.
3. **Confirmed typography**: 459 Consolas + 447 Calibri runs across 18 Lab02 slides — no
   third typeface. Confirmed most-used point sizes are 12pt, 14pt, 10pt, 28pt, 13pt,
   16pt, 15pt, 36pt, 18pt, 20pt, 44pt — matches the type scale already used in the
   build scripts.
4. **Confirmed canvas dimensions** from `presentation.xml`: `sldSz cx="12192000" cy="6858000"`
   = 13.333 × 7.5 in = 16:9 widescreen.
5. **Cross-referenced the four build scripts** to identify which design decisions are
   "convention" (used identically across all four files) vs. "variant" (e.g., title
   size 30 vs 32 for compact decks vs. lecture decks). The spec records both.
6. **Cross-referenced the existing reports** in `reports/` (especially
   `report-2026-05-19-02-week03-redesign-lab02-style.md`) for design decisions that were
   walked back during prior QA — captured them in §13 "Things that are not in the design
   language" so they don't recur.

### Structure of the spec
The file is laid out in dependency order so a future reader (human or AI) can copy
verbatim:

| § | Topic | Why it's there |
| - | --- | --- |
| 0 | TL;DR | The five must-have visual ingredients for "feels like ours". |
| 1 | Canvas | Slide dimensions + content-area anchors. |
| 2 | Color palette | All hex values + python-pptx constants + per-color usage rules. |
| 3 | Typography | Two-font rule, full type scale (12 named sizes), line spacing, casing. |
| 4 | Layout grid | The 0.55/6.85/12.75 column anchors + the y=7.05 footer rule. |
| 5 | Chrome | Whale + footer + title helpers (copy-paste-able functions). |
| 6 | Components | 17 reusable components, each with precise sizes and roles. |
| 7 | Slide templates | A catalogue mapping 22 layouts to specific build_*.py slides. |
| 8 | Voice & tone | How copy choices reinforce the visual system. |
| 9 | Required assets | `whale.png` + `docker_logo.jpg`. |
| 10 | Python-pptx scaffold | Drop-in starter so new decks don't reinvent the palette. |
| 11 | Build workflow | The `soffice → pdftoppm` QA loop, codified. |
| 12 | File naming | `build_<deck>.py`, `<DeckName>.pptx`, `analysis/<deck>/slide-NN.jpg`. |
| 13 | Anti-patterns | What was tried and walked back (mono caps kickers, dark content panels, etc.). |
| 14 | Checklist | A pre-flight checklist before declaring a deck done. |

## Results
- **`DESIGN_LANGUAGE.md`** committed at `/Users/maziar/Downloads/k8s_week3/DESIGN_LANGUAGE.md`.
- File size: ~21 KB, 14 sections, ~600 lines of markdown.
- All color hex values, font sizes, and dimension anchors are verified against the
  source PowerPoint XML — nothing is approximated.
- The spec is **self-sufficient**: a fresh contributor (or a fresh Claude session) can
  build a new on-brand deck from this file plus the two media assets, without reading
  any of the existing build scripts.
- A new deck only needs to (a) copy the helper functions from any `build_*.py`,
  (b) pick templates from §7 of the spec, and (c) follow the checklist in §14.

**Port allocation**: N/A — no dev server in this session.

## Issues / Notes
- **Spec is descriptive, not prescriptive about content.** It tells you exactly how to
  *render* a deck on-brand; it does not dictate what topics or how many slides. That
  remains a per-deck decision (and the existing four decks show the range — from
  8-slide compact labs to 18-slide step-by-step guides).
- **Two title-size variants** are listed explicitly: 32 pt (lecture decks like
  `build_week3.py`) and 30 pt (compact step-by-step decks like `build_lab_guide.py`).
  Either is on-brand; pick based on density.
- **`docker_logo.jpg` is swappable** for non-Docker decks. The whale is not — it's the
  course's visual signature across all CLO835 material.
- **The spec deliberately omits motion / animations.** None of the existing decks use
  PowerPoint transitions; the static design carries the whole load.
- **`analysis/` subdirectory** (~50 MB of intermediate XML unpacks and JPG renders)
  is not referenced by the spec and remains safe to delete; the spec was finalized
  before any cleanup.
