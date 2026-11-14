# Report: Week12 split into lecture + lab decks (v2)

**Date**: 2026-07-15
**Sequence**: #02 for the day

## Summary
Split the combined Week12 ConfigMaps & Secrets deck (v1, 37 slides) into two decks — a lecture deck and a lab/workshop deck — matching the convention the other weeks use (Week06/09/10 each ship `WeekNN_lecture_style_vN.pptx` + `WeekNN_lab_style_vN.pptx`). Delivered as v2. Every one of the 37 source slides lands in exactly one deck; content is unchanged from the already-QA-clean v1 slides, so the split is a pure partition + renumber + a new lab cover.

## What Changed
- **NEW** `Week12/Week12_lecture_style_v2.pptx` — 21 slides (theory + front/back matter).
- **NEW** `Week12/Week12_lab_style_v2.pptx` — 17 slides (new lab cover + the two workshops + cleanup).
- `build_week12.py` (repo root) — refactored: `build_all()` now emits both decks; `render_slide` decouples display position (footer) from source slide id (`d["n"]`) so decks can be renumbered; `render_cover` takes a role ("Lecture"/"Lab"). Version bumped to v2.
- v1 combined deck (`Week12_lab_style_v1.pptx`) and source `Week12.pptx` left untouched. Assets unchanged.

## Technical Details
- Split logic (mirrors the Week06 lecture-vs-lab division: lecture = concepts/theory, lab = hands-on workshops with dividers):
  - **LECTURE (21):** source slides 1–12 (cover, agenda, course outline, ConfigMaps theory incl. Create/Inject command syntax), 21–25 (Secrets theory), 32–33 (secret storage notes), 35–36 (summary, references).
  - **LAB (17):** new house-style lab cover (subtitle "Week 10 · Lab") + source 13–20 (Workshop 1: dividers + fortune-app hands-on), 26–31 (Workshop 2: divider, goals, secrets/HTTPS hands-on), 34 (Workshop 2 end), 37 (cleanup).
- Rationale: command-syntax teaching slides (ConfigMaps/Secrets Create & Inject, 10/11/22/23) stay in the lecture — Week06 kept "Creating Service Imperatively" in its lecture — while the fortune-app/secrets exercises that APPLY them go in the lab.
- Verification: deterministic assertion confirmed all 37 source slides covered exactly once (0 missing, 0 duplicated); lecture contains 0 workshop/divider/hands-on slides; lab contains the workshop dividers + steps + cleanup. Both decks rendered to contact sheets and eyeballed; both covers checked at full res. 0 float coordinates in either deck. Underlying slide content was already cleared by two independent 6-agent QA passes in the v1 work.

## Results
- Two clean, correctly-partitioned decks. Lecture flows ConfigMaps theory -> Secrets theory -> summary -> references (footers 1/21..21/21). Lab flows WS1 (divider->steps->end) -> WS2 (divider->goals->steps->end) -> cleanup (footers 1/17..17/17). Lab cover reads "Week 10 · Lab", lecture cover "Week 10 · Lecture".
- File sizes: lecture 728 KB, lab 168 KB, both 0 floats.

## Issues / Notes
- **Week-10-vs-Week-12 label still open (unchanged from v1):** both v2 covers + the lecture course-outline tile still say "Week 10" (verbatim from source). The canonical Fall 2026 schedule says Wk12 = ConfigMaps, so this is likely a stale source label. Relabel is a one-line `WEEK_LABEL` change + rebuild; still awaiting the user's decision (they moved to the split before answering).
- Naming clarification for the user: `_lab_style_` in the filename originally meant "styled like Lab02" (design language), but the project also uses `_lab_style_` vs `_lecture_style_` to distinguish workshop vs lecture CONTENT when a week is split — which is what v2 now does.
- RUN-SAFETY unchanged: `build_week12.py` is guarded and writes only its own `Week12/*.pptx`; authored in the isolated sandbox (`scratchpad/bx12/`); no canonical decks touched.
