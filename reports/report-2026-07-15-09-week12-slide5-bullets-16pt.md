# Report: Adopt user's slide-5 bullet font bump (14 -> 16 pt)

**Date**: 2026-07-15
**Sequence**: #09 for the day

## Summary
The user again edited slide 5 of the delivered lecture deck directly (font size). Read-and-diffed the file: all bullets went 14 -> 16 pt (uniform) and the terminal was dropped to y~4.0 to clear the taller bullet block (terminal font/height unchanged). Baked into `render_s05` and redelivered.

## What Changed
- Backed up the user's file to `scratchpad/user_edited_lecture_v2_s5.pptx`.
- `build_week12.py` `render_s05`: bullets `size=14` -> `size=16`; terminal y `3.5` -> `4.0`. Terminal font stays 14, height still content-fit.
- Rebuilt + redelivered `Week12/Week12_lecture_style_v2.pptx` (+ lab v2 unchanged). Memory updated.

## Technical Details
- python-pptx diff (my build vs user edit): bullet text runs all 16 pt (only the first line's leading glyph "▪" left at 14, an artifact of the user's text selection); bash bar y 3.54->4.02, terminal code y 3.90->4.38; terminal font unchanged 14. So: bullets bigger, terminal shifted down, nothing else.
- Rebuild verified by font dump (bullets 16, bar y=4.04, code y=4.40, font 14) and render at 120 dpi: bigger bullets, terminal clears them, footer clear, no overflow.

## Results
- Slide 5 matches the user's manual edit and is now in source. Only slide 5 changed.

## Issues / Notes
- Cover-vs-outline "Week 10" label mismatch still open and untouched.
