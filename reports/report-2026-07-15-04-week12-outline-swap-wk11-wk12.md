# Report: Swap Week 11 / Week 12 tiles in Week12 lecture Course Outline

**Date**: 2026-07-15
**Sequence**: #04 for the day

## Summary
Per the user, swapped the topics on the Week 11 and Week 12 tiles of the lecture Course Outline so numbering stays in order: **Week 11 = Exam & Mock Exam week** (red) and **Week 12 = K8s- Configmaps & Secrets** (blue, current week). This aligns the deck's own week tile (Week 12) with its `Week12/` folder. Rebuilt and redelivered.

## What Changed
- `wk12_content.json` slide 3 body: tile [10] "Week 11: K8s- Configmaps & Secrets" -> "Week 11: Exam & Mock Exam week"; tile [11] "Week 12: Exam & Mock Exam week" -> "Week 12: K8s- Configmaps & Secrets".
- `build_week12.py` regenerated; `Week12/Week12_lecture_style_v2.pptx` (+ lab v2, unchanged) rebuilt and redelivered.
- Memory: `clo835-course-schedule.md`, `project-week12-deck.md`, `MEMORY.md` updated to Exam=Wk11 / ConfigMaps=Wk12.

## Technical Details
- Interpreted "swap" as exchanging the two topics between the Week 11 and Week 12 slots (keeping numeric order 09,10,11,12), rather than swapping grid positions (which would read 10,12,11 out of order). This also makes ConfigMaps=Week 12, matching the folder.
- Highlight logic is content-based, so the BLUE current-week marker auto-moved to the Week 12 (ConfigMaps) tile and EXAM_RED to the Week 11 (Exam) tile with no code change. Rendered slide 3 at 130 dpi and verified. 0 float coords; footers 1/21.

## Results
- Slide 3 row 3 now: Week 09 · Week 10 · **Week 11: Exam & Mock Exam week (red)** · **Week 12: K8s- Configmaps & Secrets (blue)**. Only this slide changed; rest of both v2 decks identical.

## Issues / Notes
- **Cover still says "Week 10" (OPEN):** the outline now marks this deck as Week 12, and the folder agrees, but both v2 covers (and v1) still read "Week 10 · Lecture/Lab" with the "Week 10 feels like 100" tagline. User has scoped both recent edits to slide 3 only, so covers were left untouched. Flipping WEEK_LABEL to "Week 12" is a one-line change when the user wants it.
