# Report: Week14 v8 — adopt user's slide-3 course-outline edit (verbatim)

**Date**: 2026-07-27
**Sequence**: #08 for the day

## Summary
The user hand-edited the course-outline slide of `Week14_lecture_style_v7.pptx` (they called it "slide
2"; the real change was on slide 3, confirmed by a full-deck semantic diff — only slide 3 differs) and
said "adopt them". After I offered a fix-typos vs adopt-verbatim question and they rejected it and
repeated the instruction, I adopted the tiles EXACTLY as shown (verbatim, typos kept). Rebuilt as v8.

## What Changed
- `assemble_week14.py` OUTLINE: replaced with the user's renumbered tiles in boustrophedon reading
  order, verbatim — including the mid-edit slips they left in: `11: Exam & Mock Exam week` (no "Week"),
  `Week 12: K8s- Configmaps & SecretsWeek` (stray "Week"), and two "Week 13" tiles (`Week 13: K8s –
  RBAC and AKS`, `Week 13: Project presentation`) plus `Week 14: Project presentation`. Week 1 stays
  highlighted.
- `build_week14.py`: `VERSION="v8"`.
- New `week14/Week14_lecture_style_v8.pptx` (11 slides) + `week14/Week14_lab_style_v8.pptx` (23, no
  outline slide, unchanged). Rebuilt slide 3 verified to match the user's tiles exactly.

## Results
- Slide 3 reproduces the user's edit tile-for-tile. 0 float coords on both v8 decks. Delivered v8;
  v1–v7 retained; source untouched.

## Notes
- Adopted VERBATIM per the user's explicit direction (they rejected the "fix typos" option). The
  `11:`/`SecretsWeek`/duplicate-`Week 13` are the user's text, kept as typed — flagged here only for the
  record, not corrected. Saved a memory (feedback-adopt-verbatim-dont-ask): on "adopt my changes",
  reproduce the edit exactly, don't ask or fix; trust the diff over the cited slide number.
