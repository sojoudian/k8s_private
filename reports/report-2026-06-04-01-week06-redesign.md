# Report: Week 6 Deck Redesign (Week6.pptx → Week06_lab_style_v2.pptx)
**Date**: 2026-06-04
**Sequence**: #01 for the day

## Summary
Redesigned the 71-slide source `Week06/Week6.pptx` (Deployment Rollouts, Labels & Selectors,
Services, + 4 workshops) into the CLO835 Lab02/Week-05 design language. Built a new generator
`build_week06.py` (based on `build_week05.py`, the only prior builder with the coordinate-safety
guard), produced `Week06/Week06_lab_style_v1.pptx`, ran a fresh-eyes visual-QA pass (6 parallel
agents over all 69 rendered pages), fixed every genuine finding, and shipped
`Week06/Week06_lab_style_v2.pptx` (final). Scope/treatment were confirmed with the user before
building (full 71-slide deck · hybrid diagrams · canonical schedule).

## What Changed
- **Created** `build_week06.py` (~720 lines) — generator with the full Week-05 palette/helper set
  plus three new helpers: multi-level `bullets()` (the hierarchy fix prior builders lacked),
  `embed()` (aspect-correct figure placement), `auto_term()` (auto-colored terminal from command
  text), and `divider()` (LAB section breaks).
- **Created** `Week06/assets/` — 71 figure images extracted from the source slides (for the hybrid
  embed treatment).
- **Created** `Week06/Week06_lab_style_v1.pptx` / `.pdf`, then **v2** (final) after QA fixes.
- **Created** `ARCHITECTURE_ANALYSIS_PROMPT.md` earlier this session (separate task).

## Technical Details
**Decisions confirmed with the user (AskUserQuestion):**
1. Scope → one full 71-slide deck (1:1 with source order).
2. Diagrams → hybrid: command/YAML slides redrawn as our dark terminal mockups; conceptual figures
   embedded from the originals; text slides = blue title + multi-level bullets; workshop boundaries
   = LAB dividers.
3. Course Outline → **canonical schedule** (Week 8 = Break, Week 9 = EKS + production patterns),
   overriding the source's 14-week/AKS outline. Week 6 highlighted as current.

**Build mechanics:**
- 16:9 (13.333×7.5), `slide_layouts[6]`, palette/fonts identical to `DESIGN_LANGUAGE.md`
  (Calibri + Consolas; BLUE #1FA8E0 titles; STEPS gradient; terminal coloring green/cyan/gray/red).
- Source verbatim text extracted with paragraph indent levels (`/tmp/wk6_text.txt`) and preserved
  exactly, including source typos and en-dashes (`–f`, `–n`, `runnign`, `DockeHub`, `Exlain`) per
  rule R1. Hidden source slides 22 and 57 rebuilt and kept hidden (`show="0"`); footers number N/71.
- Coordinate-safety guard (`_i()` + `_sanitize_coords()`) carried over from `build_week05.py`.

**QA pass (workflow `wk6-visual-qa`, 6 agents, 23 findings):** 4 "empty body" flags (Agenda,
Why Services?, Ingress Resource, Example: 2-Tier) were **intentionally title-only in the source**
(R1) and match the Week-05 template — left as-is. Genuine fixes applied:
- Slide 9: dropped two illegible `describe` screenshots; enlarged the recreate/rolling diagram.
- Slides 66 & 68 (DNS figures): shrunk width to add right-edge margin (was clipping).
- Slide 46: narrowed bullet column for right margin.
- Slide 58: replaced the tiny PHP screenshot with a clean `guestbook.php` terminal; reduced gap.
- Slide 71: reduced URL font/width so the long medium.com link fits.

## Results
- `Week06/Week06_lab_style_v2.pptx` — 71 slides (2 hidden), renders to 69 pages, all 6 fixed slides
  verified clean. Build command: `.venv/bin/python build_week06.py` → wrote v2.
- v1 retained alongside v2 (R8: version every build, keep old).

## Issues / Notes
- **Course outline weeks 10–14** (Storage Classes/StatefulSets, ConfigMaps/Secrets, Exam, RBAC,
  Helm) are a best-effort canonical layout derived from the source topics minus the Break/EKS
  corrections — the professor should verify these later weeks.
- **Embedded third-party figures** carry baked-in attributions/watermarks (e.g.
  "Containerlabs.kubedaily.com | @BiradarSangam" on slide 29, "DevOps Map"/"Ajeesh Real" on the
  Types-of-Services figure). Left in place (academic attribution; removing needs image editing).
- **Source command typos preserved verbatim** (en-dashes will not run if copy-pasted). Flagged for
  the professor; not changed without instruction (R1).
- A few embedded source figures are inherently low-resolution (e.g. the Types-of-Services quadrant);
  they are as legible as the originals allow.
