# Report: Week14 v9 — move course-outline highlight to Week 13 (RBAC)

**Date**: 2026-07-27
**Sequence**: #09 for the day

## Summary
Moved the blue "current-week" highlight on the slide-3 course outline from "Week 1: Docker
Introduction" to "Week 13: K8s – RBAC and AKS" (this deck's topic); Week 1 now renders as a normal
card like every other week. Rebuilt as v9.

## What Changed
- `assemble_week14.py`: course-outline `highlight` index `[0]` → `[12]` (the "Week 13: K8s – RBAC and
  AKS" tile in reading order).
- `build_week14.py`: `VERSION="v9"`.
- New `week14/Week14_lecture_style_v9.pptx` (11 slides) + `week14/Week14_lab_style_v9.pptx` (23,
  unchanged — no outline slide).

## Results
- Slide 3: "Week 13: K8s – RBAC and AKS" tile is blue-highlighted; Week 1 is a normal card. 0 float
  coords. Delivered v9; v1–v8 retained; source untouched. Outline text otherwise identical to v8
  (the user's verbatim tiles kept).
