# Report: Week 08 (Amazon EKS) redesigned into CLO835 design language
**Date**: 2026-06-29
**Sequence**: #02 for the day

## Summary
Redesigned the source deck `Week08/Week08 -  K8s in the cloud, Amazon EKS.pptx` (33 slides, "Managed K8s – Amazon EKS") into the CLO835 "Lab02" house design language via a new builder `build_week08.py`, based on `build_week07.py`. Output: `Week08/Week08_lab_style_v1.pptx` (33 slides) + PDF + per-slide JPG previews. Original slide text preserved verbatim (R1), including the source's doubled "K8s- K8s-" outline typo.

## What Changed
- **Added** `build_week08.py` — the new builder (palette/fonts/chrome copied from build_week07.py + coord-safety guard `_i`/`_sanitize_coords`).
- **Added helpers** to this builder: `auto_term` (auto-colored terminal), `divider` (workshop section breaks), `closing` (logo-ring end slides), `course_outline` (native 4×4 grid, current week highlighted), `cost_card` (native EKS pricing card), `add_chevron` (axis-aligned MSO_SHAPE arrow, R5-safe), `hide`.
- **Created** `Week08/Week08_lab_style_v1.pptx` + `.pdf`.
- **Extracted** 17 embedded figures to `Week08/assets/sNN_M.{png,jpg}` (pixel dims tabulated in `ASPECT`).
- **Created** `analysis/week08/` (source PDF + 32 slide JPGs) and `Week08/preview/` (v1 output JPGs).

## Technical Details
Treatment per slide type (matches Week 6/7 hybrid):
- Cover → blue title "Managed K8s — Amazon EKS" + "Week 8" + K8s-logo ring.
- Bullet/text slides → blue title + multi-level `bullets()`.
- Shell/command slides (11,16,17,18,27,28,29,30) → dark terminal mockups, auto-colored (comments green, commands cyan, output gray, errors red).
- YAML (slide 19) → `yaml_terminal()` (top-level keys cyan).
- AWS architecture/console figures (5,6,7,15,24,25,26,27,29,30,31) → embedded originals, aspect-fit.
- Course Outline (3) → redrawn natively in palette (orange removed → STEPS/CARD_BG; Week 8 highlighted BLUE).
- Cost Estimate (4) → redrawn as a slate/white card with verbatim pricing math.
- Workshops (8,22) → LAB-style `divider`; "End of Workshop" (20,32) → `closing`.
- Source hidden slide 2 (Assumptions) → rebuilt and kept hidden (`show='0'`, R1).

## Results
- `Week08/Week08_lab_style_v1.pptx`: **33 slides** (== TOTAL), **0 float-EMU coords**, slide 2 hidden, 16:9 (13.333×7.5in). Verified via python-pptx spTree scan.
- ASPECT dict validated against real pixel dims (0 mismatches).
- Visual QA (LibreOffice render → JPG) on cover, Course Outline, cost card, architecture embed, terminal, and the densest slide (19) — all on-brand, no overflow.
- No local dev server started (offline build task); port rule N/A.

## Issues / Notes
- Verbatim typo "Week 8: K8s- K8s- PVs & K8s in AKS" preserved from source per R1.
- Builder inherits the project's known share-by-copy posture (engine duplicated from build_week07.py) — consistent with all prior weeks.
- Slides 13/14 are title-only in the source (kept title-only).
