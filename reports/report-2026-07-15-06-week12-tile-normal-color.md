# Report: Make Week 12 outline tile a normal card color

**Date**: 2026-07-15
**Sequence**: #06 for the day

## Summary
Per the user, removed the blue current-week highlight from the Week 12 tile on the lecture Course Outline (slide 3) so it looks like every other week's card. Only the Exam (Week 11) tile stays highlighted (red). Rebuilt and redelivered.

## What Changed
- `build_week12.py` course-outline highlight logic: dropped the `startswith("Week 12") -> BLUE` rule; now highlights only `"exam" -> EXAM_RED`.
- Rebuilt + redelivered `Week12/Week12_lecture_style_v2.pptx` (+ lab v2 unchanged). Memory `project-week12-deck.md` updated.

## Technical Details
- The Week 12 tile ("Week 12: K8s") now renders with the default card fill (CARD_BG light gray), gray border, slate non-bold text — identical to Weeks 1-10, 13-15. No data change; only the highlight map changed. Verified against render at 130 dpi. 0 float coords; footers 1/21.

## Results
- Slide 3: only the Week 11 Exam tile is colored (red); all other tiles including Week 12 are the standard light-gray card. Only this slide changed.

## Issues / Notes
- Cover-vs-outline label mismatch still OPEN and untouched (covers say "Week 10").
