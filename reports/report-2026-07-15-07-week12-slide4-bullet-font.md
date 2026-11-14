# Report: Adopt user's slide-4 font-size edit into the Week12 builder

**Date**: 2026-07-15
**Sequence**: #07 for the day

## Summary
The user edited slide 4 ("Configuring Containerized Applications") of the delivered `Week12_lecture_style_v2.pptx` directly (no screenshot), mostly a font-size change. I read the edited file, diffed it against my last generated version to isolate the change, and baked it into the builder so future rebuilds preserve it.

## What Changed
- Backed up the user's edited file to `scratchpad/user_edited_lecture_v2.pptx` before touching anything.
- `build_week12.py`: added `render_s04` (slide 4) rendering bullets at a uniform **14 pt** at y=1.47; added a `level_step` kwarg to `bullets()` (default 1; `level_step=0` disables per-level shrink so sub-bullets stay 14 pt too); registered slide 4 in `_CUSTOM`.
- Rebuilt + redelivered `Week12/Week12_lecture_style_v2.pptx` (+ lab v2 unchanged). Memory `project-week12-deck.md` updated.

## Technical Details
- Diff (my build vs user edit) via python-pptx font-size dump: the only change was the bullets — level 0: 12->14 pt, level 1: 11->14 pt (now uniform), and the block nudged up y=1.58->1.47. Title (30), the two nginx terminals (8 pt), and the "bash" bars (10 pt) were unchanged; I reproduced those identically via the existing `two_col_terminal` at y=3.33/h=3.57.
- Verified the rebuild: all 6 bullets now 14 pt at y=1.47 (font dump match) and rendered at 120 dpi — larger bullets, no collision with the terminals, no overflow.

## Results
- Slide 4 in the rebuilt deck matches the user's manual edit; the change is now in source so it survives future regenerations. Only slide 4 changed.

## Issues / Notes
- Method note: when the user edits the delivered PPTX directly, the reliable way to adopt is read-and-diff the file with python-pptx (extract per-run font size/position), not guess. Backup first so a rebuild can't clobber unadopted edits.
- Cover-vs-outline "Week 10" label mismatch still open and untouched.
