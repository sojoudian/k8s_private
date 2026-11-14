# Report: Week 05 v12 — float-coord bug fix at the helper level
**Date**: 2026-06-01
**Sequence**: #03 for the day

## Summary
Built `Week05/Week05_lab_style_v12.pptx`. Root-caused and patched the "arrow at the top of the page" bug at the helper level so it cannot recur. Replaced slide 17 with a manual YAML render so the red box can sit on known Y coordinates, and re-added the diagonal red arrow from "POD Definition" to the box. Verified zero float coordinates across the entire 39-slide deck after the patch.

## What Changed
- **`build_week05.py`**:
  - Bumped `VERSION` from `v1` to `v12`.
  - Added `_i(v)` int-coercer near the top of the file.
  - Added `_sanitize_coords(prs)` save-time safety net that walks every slide's `<a:off>`/`<a:ext>`/`<a:chOff>`/`<a:chExt>` and coerces any non-integer x/y/cx/cy to int.
  - Wrapped every shape-coord argument in `add_text`, `add_rich_text`, `add_rect`, `add_rounded_rect`, `add_oval`, `add_hex`, `add_line`, `add_arrow` with `_i(...)`.
  - Added new helper `add_rect_outlined(s, x, y, w, h, color, line_width=2.5)` — no fill, used for the red callout box.
  - Replaced the slide 17 block: terminal frame drawn manually (background + bar + traffic-light dots + title), YAML rendered line-by-line at known Y positions, red outlined box sitting on lines 9–17, red diagonal arrow from "POD Definition" up-right into the box.
  - Wired `_sanitize_coords(prs)` immediately before `prs.save(out)`.
- **`Week05/Week05_lab_style_v12.pptx`** — new build output.
- **`Week05/Week05_lab_style_v12.pdf`** — LibreOffice render.
- **`Week05/v11_jpgs/v12_slide17-17.jpg`** — slide 17 visual confirmation.
- **`~/.claude/projects/.../memory/feedback-float-coord-bug.md`** — new memory entry capturing the bug class, the fix, and the verification step.
- **`~/.claude/projects/.../memory/MEMORY.md`** — index updated to include the new entry.

## Technical Details

### Root cause
OOXML demands integer EMU for `<a:off x=… y=…>` and `<a:ext cx=… cy=…>`. Python's `/` operator returns a float. python-pptx serializes that float verbatim — e.g. `4288536.0` — and PowerPoint / Keynote silently fall back to `0` when they hit a non-integer value. LibreOffice tolerates it, so the `soffice → pdftoppm` QA loop is blind to the issue.

The v11 slide 17 arrow had `box_target_y = (box_top + box_bot) / 2`. That float landed in `<a:off y="4288536.0">` and PowerPoint dropped it to y=0, which is why the arrow ended up at the very top of the page on every viewer except LibreOffice.

This same bug class infected slides 6 (decorative DB-icon connectors), 17 (red arrow), and 21 (every connector in the Deployment → ReplicaSet → Pod → Node hierarchy — 16 connectors).

### Fix — three layers
1. **Primary**: `_i(v)` coercer wrapping every shape-coord argument in every helper. Floats cannot reach the XML.
2. **Secondary**: `_sanitize_coords(prs)` post-pass that walks every slide and coerces any survivor in `<a:off>/<a:ext>/<a:chOff>/<a:chExt>`. Belt and suspenders.
3. **Style**: prefer integer division (`//`) over `/` whenever computing a midpoint or split. Documented in the memory entry.

### Slide 17 redesign approach
Used a **manual line-by-line YAML render** instead of the `terminal()` helper. The helper renders all lines as a single textbox with paragraph spacing, which means line Y positions aren't directly knowable from outside. Manual rendering lets the red box sit at `yaml_y0 + line_h * 9 - Inches(0.04)` to `yaml_y0 + line_h * 18 + Inches(0.04)` — exactly the pod template section, with small visual padding.

Arrow: diagonal from `(2.20, 4.85)` to `(box_left + 0.10, box_top + 0.55)`. Both endpoints constructed from integer Emu via `Inches(...)` plus integer-Emu arithmetic. No float arithmetic in the path.

## Results
- **Latest file**: `/Users/maziar/Downloads/k8s_week3/Week05/Week05_lab_style_v12.pptx`
- **Floats in `<a:off>`/`<a:ext>` across all 39 slides**: **0** (verified via direct XML scan).
- **Slide 17 visual** (from LibreOffice PDF render at 100 dpi): title at top-left, "Why do we need it?" + two bullets on the left, "POD Definition" in ALERT_RED below the bullets, YAML terminal on the right with the red outlined box wrapping `metadata: → image: nginx`, red diagonal arrow from "POD Definition" up-right into the box. Matches the user's reference image.
- **All other slides**: untouched at the per-slide level. The helper change is opaque to existing slides — they were already passing integer-Emu values via `Inches(...)`.

**Port allocation**: N/A — no dev server.

## Issues / Notes
- The helper-level fix is local to `build_week05.py`. The other five build scripts (`build_week03.py`, `build_week3.py`, `build_week04.py`, `build_lab.py`, `build_lab_guide.py`) still carry the same latent bug. They have not exhibited it in the user's reports yet, but per the share-by-copy architecture noted in the morning's architectural analysis (report 2026-06-01-02), they will need the same patch when iterated on. The right long-term fix is to extract `clo835_design/` as a shared module so the helpers only exist in one place.
- The memory entry `feedback-float-coord-bug.md` is now indexed in `MEMORY.md` so any future session picks it up automatically.
- Slide 17 in v12 uses 22 hand-positioned text boxes for YAML instead of one paragraph-stacked textbox. Total shape count on the slide went up by ~22, but the deck size only grew from 210 KB (v11) to ~211 KB — negligible.
- The line height constant `line_h = Inches(0.22)` was chosen empirically from the v11 manual-render slide; it's the spacing that matches Consolas 10.5pt with `line_spacing=1.0`. If the YAML font ever changes, this constant needs to change too.
- LibreOffice rendered v11 "correctly" because it tolerates malformed coords; the bug was invisible until the user opened it in Keynote. **Future visual QA should include opening the .pptx in the user's actual viewer**, not just relying on `soffice` PDF output — this rule was already in PROMPT.md R9 but has now been reinforced with a concrete instance.
