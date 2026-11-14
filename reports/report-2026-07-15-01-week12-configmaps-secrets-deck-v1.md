# Report: Week12 (ConfigMaps & Secrets) lecture rebuilt in CLO835 house design — v1

**Date**: 2026-07-15
**Sequence**: #01 for the day

## Summary
Rebuilt the newly added `Week12/Week12.pptx` (37-slide "ConfigMaps and Secrets" lecture) into the exact CLO835 house design language, delivered as `Week12/Week12_lab_style_v1.pptx` (37 slides, 0 float coords, PowerPoint/Keynote-safe). Workflow: rendered the source to images, extracted structured content with a 7-agent parallel workflow, generated a self-contained house-style builder, then ran two full adversarial QA passes (6 agents each, all 37 slides vs source) and fixed every major and most minor findings. Second QA pass: 0 majors, 0 overflow, 0 redundant titles; 2 minor illustrative omissions remain by design.

## What Changed
- **NEW** `Week12/Week12_lab_style_v1.pptx` — the rebuilt 37-slide house-style deck (deliverable).
- **NEW** `Week12/assets/fig09.png, fig12.png, fig25.png, fig35.png` — cropped source diagrams embedded natively (ConfigMap concept, dev/prod multi-env, default-token Secret, injection summary).
- **NEW** `build_week12.py` (repo root) — self-contained, DECK-driven builder (guarded with `if __name__ == "__main__"`, unlike the other builders, so importing never overwrites).
- Source `Week12/Week12.pptx` left untouched.

## Technical Details
- Engine: exact Lab02/Week05 palette (BLUE #1FA8E0, SLATE #37465A, Calibri/Consolas), 13.333x7.5in blank canvas, whale+footer chrome, coordinate guard (`_i()` + `_sanitize_coords`) so no float coords serialize (the "4288536.0" teleport bug). Content baked into `DECK` from the source; type-driven renderers (cover, course_outline boustrophedon grid with current-week BLUE + exam RED highlights, dividers, terminals, bullets, native table).
- Slides 6 and 10 were rebuilt **natively** (not embedded screenshots): s6 = bullets + `pod.yaml` terminal + a slate-header Docker/Kubernetes/Description table; s10 = bullet hierarchy + imperative/declarative terminals (mirrors the s22 Secrets-Create layout). Source `APP_MOD` typo preserved verbatim.
- Slides 9, 12, 23 fixed after QA pass 1: s9/s12 = bullets-left + embedded cropped diagram-right; s23 (dense Secrets-Inject) = bullets-left + two full-height terminals right (pod+secret manifests | three inject methods).
- Slides 25, 35 kept their genuine diagrams but re-cropped tighter to drop the source's own restated title (no duplicate heading).
- Key bug fixes: (1) `title()` now shrinks long titles and drops the underline rule BELOW wrapped text; (2) `smart_title()` no longer lowercases a leading stopword ("the"->"The"); (3) render_content drops command bullets that were double-captured as both bullets and terminal head (was causing duplication + overflow on s14/15/17/18/19); (4) `_fit_font` now sizes against the terminal's real text area (h-0.5 for title bar + padding) instead of full height, eliminating bottom-spill; (5) removed redundant caption under self-contained figures; (6) corrected a mis-OCR'd base64 sample `cGFzZz3Jk` -> `cGFzd3Jk` (base64 "paswrd") on slides 22 and 23.

## Results
- 37/37 slides render clean. Two independent 6-agent QA passes: pass 1 found 3 majors (s9/s12 dropped diagrams, s23 overflow) + minors — all fixed; pass 2 = 0 majors, 0 overflow, 0 redundant titles.
- 2 remaining MINOR omissions (intentional): s5's two decorative Dockerfile callout annotations (concepts covered by bullets), s10's secondary mysql-config/redis-config example boxes (adding them back re-introduces the source clutter the clean rebuild removed).
- Output: 760 KB, 0 float coordinates verified via XML scan.

## Issues / Notes
- **Week-number label mismatch (needs user confirmation):** the source deck self-labels this content as **"Week 10"** on its cover and course outline even though the folder is `Week12`. Preserved "Week 10" verbatim per the source-fidelity rule. Awaiting user decision on whether to relabel to Week 12.
- RUN-SAFETY: `build_week12.py` saves to `Week12/Week12_lab_style_v1.pptx` (cwd-relative) and reads assets from `Week12/assets/`, `Week04/<logo>`, `whale.png`. Run only from the repo root or an isolated sandbox; it overwrites only its own deliverable. All authoring/rendering here was done in an isolated sandbox (`scratchpad/bx12/`); no canonical decks were touched.
