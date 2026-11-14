# Report: Week 09 (PV, PVC, StorageClass, StatefulSets) redesigned into CLO835 design language
**Date**: 2026-07-06
**Sequence**: #01 for the day

## Summary
Redesigned the source deck `Week09/Week09.pptx` (57 slides, "PV, PVC, StorageClass and StatefulSets") into the CLO835 "Lab02" house design language via a new builder `build_week09.py`, using the exact same treatment as Week 08. Output: single combined `Week09/Week09_lab_style_v1.pptx` (57 slides) + PDF + JPG previews. Original slide text preserved verbatim (R1), including source typos ("StatefulSEts", "Sttatefulsets", "ramdom", "availble", "cotainer", "Examnine", "kibia-0", "anew", "enty").

## What Changed
- **Added** `build_week09.py` — new builder (engine copied from build_week08.py + coord-safety guard). `ASPECT` is auto-populated from the assets folder via Pillow (avoids a hand-maintained dimension table for 34 images).
- **Created** `Week09/Week09_lab_style_v1.pptx` (57 slides) + `.pdf`.
- **Extracted** 30 embedded figures to `Week09/assets/sNN_M.{png,jpg}`.
- **Cropped** 4 native-shape diagrams (slides 6, 19, 21, 29) from a 180-dpi source render → `Week09/assets/fig_sNN.png` (original dark title bars trimmed off).
- **Created** `analysis/week09/` (source PDF + 57 slide JPGs + contact sheets) and `Week09/preview/`.

## Technical Details
Treatment per slide type (same hybrid as Week 6/7/8):
- Cover → blue title "PV, PVC, StorageClass and StatefulSets" + "Week 9" + K8s-logo ring.
- Bullet/text slides → blue title + multi-level `bullets()`.
- Shell slides (12–16, 31, 32, 48–52, 54, 55, 57) → dark terminal mockups, auto-colored (`auto_term`).
- YAML manifests (7, 8, 9, 20, 23, 24, 28) → `yaml_terminal` (top-level keys cyan, comments green); side-by-side pairs for 24 (PVC+PV) and 28 (StorageClass+PVC).
- AWS/native diagrams → embedded originals: extracted images (5, 16, 25, 35–44, 46, 48, 49, 53, 54) and cropped native diagrams (6, 19, 21, 29).
- Course Outline (3) → redrawn natively in palette, **Week 9 highlighted blue**, and the **Week 10 = Exam** red highlight carried over from the user's earlier Week-08 curriculum swap (kept consistent across decks).
- Section headers (18, 34) → centered slate `section()`; Workshops (11, 30, 45) → LAB `divider`; "The End" slides (17, 33, 56) → logo-ring `closing`.

## Results
- `Week09/Week09_lab_style_v1.pptx`: **57 slides** (== TOTAL), **0 float-EMU coords**, no hidden slides, 16:9 (13.333×7.5in). Verified via python-pptx spTree scan.
- Full visual QA: rendered to PDF→JPG and reviewed all 57 via 5 contact sheets — no overflow, all diagrams aspect-correct, terminals fit.
- No local dev server started (offline build task); port rule N/A.

## Issues / Notes
- Single combined deck (not split into lecture/lab) — matches the initial Week-08 redesign. Can be split later on request (build_week08.py has the split pattern).
- Verbatim typos preserved per R1 (see Summary).
- Course-outline consistency decision: reused the swapped outline (Exam=Week 10) rather than the source's Exam=Week 11, to keep all course decks consistent with the user's prior edit.
