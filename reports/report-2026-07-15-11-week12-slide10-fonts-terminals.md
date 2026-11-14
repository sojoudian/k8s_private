# Report: Slide 10 — bigger fonts + content-fit terminals (like slide 5)

**Date**: 2026-07-15
**Sequence**: #11 for the day

## Summary
Applied the slide-5 treatment to slide 10 ("ConfigMaps - Create"), which is denser: a 3-level bullet hierarchy plus two ~12-line terminals (imperative/declarative) that had empty black area at the bottom and small fonts. Enlarged the bullets (hierarchy kept) and made both terminals content-fit with a maximized font. Rebuilt and redelivered.

## What Changed
- `build_week12.py` `render_s10`: bullets 13 -> 15 base (hierarchy preserved via level_step, so 15/14/13 instead of 13/12/11); terminals switched from a fixed h=3.55/font-10 to content-fit height with an auto-maximized font, landing at 11 pt, starting y=3.15, bottom 6.62.
- Rebuilt + redelivered `Week12/Week12_lecture_style_v2.pptx` (+ lab v2 unchanged). 

## Technical Details
- Slide 10 is much denser than slides 5/8 (two 12-line terminals + a 3-level nested list), so fonts can't grow as far. Kept the bullet size-hierarchy (not uniform 16) because it's a genuine nested list (2 Step Process -> Create a Config Map -> Imperative/Declarative -> Inject). 
- Tried pushing terminals to 12 pt (cy=2.9) but the taller bullets collided with the terminal tops, so reverted to cy=3.15/font 11 (verified clean). Both terminals share one content-fit height (based on the 12-line imperative), so the 11-line declarative keeps ~1 extra line of padding — intentional, keeps the two boxes the same height. Verified at 120 dpi: no collision, void much reduced, footer clear. 0 float coords.

## Results
- Slide 10 consistent with the others: bigger bullets (15/14/13) and terminals (11 pt), void largely gone. Only slide 10 changed.

## Issues / Notes
- Terminal font is 11 pt (slides 5/8 reached 13-14) because slide 10 carries roughly double the content; growing further would collide with the bullets or clip commands.
- Cover-vs-outline "Week 10" label mismatch still open and untouched.
