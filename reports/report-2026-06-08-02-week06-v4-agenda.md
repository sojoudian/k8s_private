# Report: Week 6 — Rebuild the modular Agenda (v4)
**Date**: 2026-06-08
**Sequence**: #02 for the day

## Summary
The Agenda slide (lecture deck, slide 2) was empty/title-only in my v2 and the user's v3 decks.
The original `Week6.pptx` agenda was a **modular 3-item layout (Rollouts / Deployments / Services)**
stored as a SmartArt graphic — which python-pptx text-extraction returned as just "Agenda", so an
earlier pass wrongly built it title-only (the `text-extract-misses-images` trap). Recreated the
modular agenda in our design language and saved as `Week06/Week06_lecture_style_v4.pptx`.

## What Changed
- **Created** `Week06/Week06_lecture_style_v4.pptx` (41 slides) — the user's `lecture_style_v3`
  edited IN PLACE (only slide 2; the rest of their split untouched).
- **Edited** `build_week06.py` slide-2 block — now emits the modular agenda (syntax-checked, not run).

## Technical Details
- Confirmed the source agenda by rendering `Week6.pptx` slide 2: three lavender bars, blue icon
  boxes (only "Rollouts" had a real gears icon; "Deployments"/"Services" used placeholder icons),
  labels Rollouts / Deployments / Services (used verbatim, R1).
- Iterated the existing deck rather than regenerating (PROMPT.md), because the user's v3 split was
  done by hand and `build_week06.py` still emits the old single combined deck — regenerating would
  have destroyed their split.
- New agenda design (our language): 3 `CARD_BG` rounded modules (full width, RULE_GRAY outline),
  each with a STEPS-colored rounded tile (`01`=STEPS[0] blue, `02`=STEPS[1] teal, `03`=STEPS[3]
  deep-blue) holding a white Consolas number, plus a SLATE bold 26pt Calibri label. Float-coord
  sanitizer applied before save.
- Slide 2 went from 4 shapes (title + chrome) to 16 (added 3×{card, tile, number, label}).

## Results
- `Week06_lecture_style_v4.pptx` slide 2 rendered and verified: modular agenda present, on-brand,
  title/whale/footer (2/71) intact. v1/v2/v3 retained.

## Issues / Notes
- Lab deck (`Week06_lab_style_v3.pptx`) is unchanged (no agenda) — still v3, not bumped.
- `build_week06.py` remains the OLD single-combined generator (not run; would overwrite v2). Refactor
  to emit the lecture/lab split is still pending user confirmation.
- Minor: LibreOffice renders a faint shadow on the rounded cards/tiles despite `shadow.inherit=False`;
  it reads as subtle "card depth" and matches the original's look — left as-is.
