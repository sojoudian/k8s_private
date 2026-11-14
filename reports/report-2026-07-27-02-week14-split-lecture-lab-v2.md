# Report: Week14 split into lecture + lab (v2)

**Date**: 2026-07-27
**Sequence**: #02 for the day

## Summary
Split the Week14 (RBAC-continued / HPA / IRSA) v1 combined deck into a **lecture** deck and a **lab**
deck (v2), matching the other weeks' convention (Week06/09/12/13). Content unchanged — a partition of
the same 30 verbatim-preserving slides plus a synthetic "· Lab" cover. Lecture = concepts/theory +
front/back matter; Lab = the three workshops + cleanup.

## What Changed
- `build_week14.py`: `VERSION="v2"`; added `LECTURE_NS`/`LAB_NS` partitions, a synthetic `_LAB_COVER`,
  and `build_all()` (asserts the partition is disjoint and covers all 30). `__main__` now runs
  `build_all()`; `build()` (v1 combined) retained.
- New `week14/Week14_lecture_style_v2.pptx` (8 slides) + `week14/Week14_lab_style_v2.pptx` (23 slides =
  Lab cover + 22). v1 combined deck left in place.

## Partition
- **LECTURE (8):** 1 (cover), 2 (agenda), 3 (course outline), 11 (kubeconfig CONCEPT + diagram),
  20 (HPA concept), 21 (autoscaling process concept), 28 (optional group activity), 29 (references).
- **LAB (23):** synthetic Lab cover + Workshop 1 (4-10, 12, 13 — divider/goal/steps/kubeconfig
  hands-on/closing), Workshop 2 (14-19), Workshop 3 (22-27, incl. hidden 23/24), Cleanup (30).

## How the partition was decided
Proposed the partition from the deck structure (three clearly delineated workshops), then validated
with an **independent 3-agent classification panel**. Result: unanimous (3/0) on every slide, zero
disputes, agreeing with my split on 29/30. The one difference — slide 11 "Understanding Kubeconfig"
(the kubeconfig CONCEPT + diagram, sandwiched inside Workshop 1) — the panel unanimously placed in
**lecture**; I'd left it in lab. Deferred to the panel (concept → lecture, hands-on slide 12 → lab),
exactly the Week13 precedent (slide 44). Adopted 11 → lecture.

## Results
- Lecture: 8 slides, 0 hidden, 0 float coords, footers "N / 8" on every slide.
- Lab: 23 slides, 2 hidden (kube-ops-view slides at positions 18/19), 0 float coords, footers "N / 23".
- Covers verified: "Week 12 · Lecture" (1/8) and "Week 12 · Lab" (1/23). Both flows coherent (lecture =
  kubeconfig + HPA theory + front/back matter; lab = Workshop 1 → 2 → 3 → cleanup). Per-slide rendering
  identical to the QA-passed v1, so no re-QA of slide internals needed.

## Issues / Notes
- Covers self-label "Week 12" (source's own label; folder is `week14`) — same standing offset as the
  other decks.
- The lab's title-less full-image slides (IAM console screenshot; kube-ops-view) show only the footer
  text by design — correct.
