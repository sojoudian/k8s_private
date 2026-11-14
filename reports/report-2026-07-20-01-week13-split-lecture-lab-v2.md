# Report: Week13 split into lecture + lab (v2)

**Date**: 2026-07-20
**Sequence**: #01 for the day

## Summary
Split the Week13 (RBAC + IRSA) v1 combined deck into a **lecture** deck and a **lab** deck (v2),
matching the other weeks' convention (Week06/09/12). Content unchanged — this is a partition of the
same 46 verbatim-preserving slides plus a synthetic "· Lab" cover. Lecture = concepts/theory + front/
back matter; Lab = the three workshops that apply them + cleanup.

## What Changed
- `build_week13.py`: `VERSION="v2"`; `render_cover` takes a `role` (Lecture/Lab); added
  `LECTURE_NS`/`LAB_NS` partitions, a synthetic `_LAB_COVER`, `build_deck()`, and `build_all()`
  (asserts the partition is disjoint and covers all 46). `__main__` now runs `build_all()`.
- New `week13/Week13_lecture_style_v2.pptx` (21 slides) and `week13/Week13_lab_style_v2.pptx`
  (26 slides = Lab cover + 25). v1 combined deck left in place.

## Partition
- **LECTURE (21):** 1–8 (cover/agenda/outline + authentication concepts), 15–20 (authorization +
  RBAC concepts), 31–35 (EKS-IAM concepts), 43 (kubeconfig concept), 45 (references).
- **LAB (26):** synthetic Lab cover + Workshop 1 serviceaccount (9–14, kept **hidden**), Workshop 2
  RBAC (21–30: connect/verify/grant/clusterroles), Workshop 2 IRSA (36–42: create cluster/IAM
  user/map/grant/eksctl), kubeconfig hands-on (44), Cleanup (46).

## How the partition was decided
Proposed a partition from the deck structure (workshops are clearly delineated), then validated it
with an **independent 3-agent classification panel**. Result: unanimous (3/0) on every slide, zero
disputes, agreeing with my split on 45/46. The one difference — slide 44 "Configuring local
environment – working with kubeconfig" (11 hands-on command bullets) — the panel unanimously placed
in **lab**; I'd leaned lecture. Deferred to the panel: concept (43) stays in lecture, hands-on (44)
goes to lab, which is exactly the lecture/lab philosophy. Adopted 44 → lab.

## Results
- Lecture: 21 slides, 0 hidden, 0 float coords, footers "N / 21" on every slide.
- Lab: 26 slides, 6 hidden (Workshop 1 at positions 2–7), 0 float coords, footers "N / 26".
- Covers verified: "Week 11 · Lecture" (1/21) and "Week 11 · Lab" (1/26). Both flows read coherently
  (lecture = theory progression; lab = Workshop 1 → Workshop 2 RBAC → Workshop 2 IRSA → kubeconfig →
  cleanup). Per-slide rendering is identical to the QA-passed v1, so no re-QA of slide internals needed.

## Issues / Notes
- Source labels BOTH visible workshops "Workshop 2" (slides 21 and 36) — a source inconsistency
  (Workshop 1 is the hidden serviceaccount set); preserved verbatim per R1.
- Covers still read "Week 11" (source self-label); same standing relabel question as the other decks.
- A `~$Week13_lab_style_v1.pptx` lock file is present — v1 is open in the user's viewer; v2 written alongside.
