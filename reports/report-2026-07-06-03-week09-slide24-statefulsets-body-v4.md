# Report: Week09 slide 24 — "Why StatefulSets?" body added, lecture v4
**Date**: 2026-07-06
**Sequence**: #03 for the day

## Summary
Added the user-supplied body content to lecture slide 24 ("Why StatefulSets?", previously title-only after the v3 split) using the house numbered-circle pattern, bumped LECTURE_VERSION to v4, and shipped `Week09/Week09_lecture_style_v4.pptx`.

## What Changed
- `build_week09.py` — sl35 now draws: intro line + 4 rows of SLATE circle (0.5in, white bold number) + bold SLATE heading + BODY text; LECTURE_VERSION v3→v4; docstring updated.
- `Week09/Week09_lecture_style_v4.pptx` — new canonical lecture deck (36 slides).
- `Week09/Week09_lecture_style_v4.pdf` — render proof.
- Lab deck untouched (built in scratch dir; only lecture v4 copied into the repo).

## Technical Details
Treatment per DESIGN_LANGUAGE §6.8 (numbered-circle rows): user's four "N- Label: text" items split at the colon into bold slate headings ("Stable identity", "Stable network address", "Per-pod storage", "Ordered operations") with the explanations verbatim as 13pt body; numbers live in the circles. Rows at y=2.15, pitch 1.12in; last row bottom ≈6.6in, inside the 6.70 content guard. All coords through `_i()` + `_sanitize_coords`.

## Results
- Verify: 36 slides, 0 float coords, 0 hidden, footers all "N / 36".
- Visual QA of slide 24: on-palette, no overflow, whale + footer intact (see render).

## Issues / Notes
- Slide 25 (full-size diagram) is unchanged and now directly illustrates this list.
- v2 (hand-edited) and v3 remain on disk per R8 versioning.
