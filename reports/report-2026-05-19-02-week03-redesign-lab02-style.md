# Report: Week03 Redesign in Lab02 Design Language
**Date**: 2026-05-19
**Sequence**: #02 for the day

## Summary
Redesigned `Week03_redesigned.pptx` (14 slides) to match the EXACT design language of `Lab02.pptx`, output as `Week03_lab_style.pptx`. Spec was derived empirically from the Lab02 XML (palette hex codes, fonts, sizes) rather than approximated — then encoded in a python-pptx build script. Rendered all 14 slides to PDF/JPG for visual QA, ran a fresh-eyes subagent review, and applied targeted fixes for the issues it flagged before declaring done.

## What Changed
- **`Week03_lab_style.pptx`** — new 14-slide deck (105 KB), built from scratch with python-pptx using widescreen 16:9 (13.33" × 7.5") dimensions, all slides on white background, blue Calibri titles top-left, dark-slate filled section circles, terminal mockups with traffic-light dots in Consolas, whale icon bottom-left, footer bottom-right.
- **`build_week03.py`** — ~600-line python-pptx generator. One function per slide; reusable helpers for `terminal()`, `step()`, `objective()`, `benefit()`, `whale_and_footer()`. Edits during QA tracked inline.
- **`whale.png`** + **`docker_logo.jpg`** — extracted from `Lab02.pptx` (`ppt/media/image2.png` and `image1.jpg`) and reused so the new deck shares Lab02's exact visual assets.
- **`analysis/`** — temporary scratch dir: Lab01/Lab02/Week03 XML unpacks, slide-by-slide JPG renders, and `text.md` extractions used to derive the spec. Safe to delete.

## Technical Details
**How the design language was reverse-engineered:**
1. Converted Lab02.pptx → PDF (`soffice --headless`) → JPG per page (`pdftoppm -jpeg -r 110`) to read every slide visually.
2. Unpacked `Lab02.pptx` as a zip and grepped `<a:srgbClr val="…">` in slide XML to extract the literal hex palette. Same for `typeface="…"` and font sizes (`sz="N"` in 1/100 pt).
3. Derived the exact spec — palette: `#1FA8E0` (primary blue), `#37465A` (dark slate), `#3F3F3F` (body), `#868686` (muted), `#CFDBEE` (light blue), step-block gradient `#1F7AB8 → #2466A0`; fonts: Calibri + Consolas; title 36pt bold blue top-left; whale icon at (0.45", 6.85"); footer pattern `CLO835, Fall 2026   N / 14`.
4. Confirmed scope with the user via AskUserQuestion (output filename, Lab02 verbatim vs blend, content preservation, closing-slide light vs dark) before any editing.
5. Generated the build, ran QA, fixed issues, re-rendered, re-QA'd.

**Slide layouts implemented:**
1. Title — blue 44pt + subtitle + Docker logo in light-blue ring
2. Learning objectives — 2×2 grid of dark-slate-circled numbers
3. What is a Docker layer? — text left, 5-layer terminal stack right, R/W dashed overlay, 3 ✓ benefits
4. Copy-on-Write — 3 numbered circles + light card with key question + red answer
5. The problem — scenario / fix two-column with blue-gradient option blocks
6. Comparison table — slate header, alternating row banding
7. Three ways to change code — 3-column step-block grid with mini terminals + verdict pills
8. Lab divider — centered slate circle + heading + 3 meta info blocks
9. Lab Part A — full terminal + reflect column
10. Lab Part B — full terminal + expected output + reflect
11. Lab Part C — side-by-side legacy/modern terminals + comparison table
12. Troubleshooting — 4 stacked error cards with slate left-bar
13. Key takeaways — 2×2 grid of circled-number takeaways
14. Wrap-up — Lab02-style 3 step blocks + italic next-up line + centered Docker logo

**QA loop:**
- First render → subagent fresh-eyes review found 5 issues:
  - Slide 1 subtitle wrapped unnecessarily (widened textbox)
  - Slide 4 dark navy Q&A panel deviated from Lab02 (all-white content) — converted to light card
  - Slide 5 mono caps "SCENARIO"/"THE FIX" kickers — softened to sentence-case Calibri headings
  - Slides 2 + 13 right-column body ran too close to right edge — pulled in 0.2"
  - Slide 11 mono caps "LEGACY"/"MODERN" — softened
  - Slide 12 too red — left bars changed to slate, error labels slate
- Second render: all issues resolved. Footer pages render `N / 14` on one line on all 14 slides (previously wrapped on slides 10-14 because the original footer textbox was sized for single-digit numbers).

## Results
**Final deliverable:** `Week03_lab_style.pptx` (105 KB, 14 slides), saved alongside the original Week03_redesigned.pptx (untouched).

**Design-language compliance vs Lab02:**
- ✅ White background everywhere (no dark navy content slides)
- ✅ Blue Calibri title 32-44pt at top-left of every content slide
- ✅ Tiny cyan-outline whale icon bottom-left of every content slide (reused from Lab02 media)
- ✅ Footer `CLO835, Fall 2026   N / 14` bottom-right in 10pt muted gray
- ✅ Subtle horizontal separator above footer
- ✅ Dark-slate (#37465A) filled circles with white numbers for section markers
- ✅ Calibri for body, Consolas for code and terminal mockups
- ✅ Terminal windows with red/yellow/green traffic-light dots and titled bar
- ✅ Step blocks in the Lab02 blue gradient palette
- ✅ Comparison tables with slate header + alternating row bands
- ✅ Italic gray subtitle + centered Docker logo on wrap-up

**Port allocation:** N/A — no dev server in this session.

## Issues / Notes
- **`analysis/` directory** is ~50 MB of intermediate artefacts. Safe to delete (`rm -rf analysis`) — not needed for the final deck.
- **Font availability**: The deck uses Calibri/Consolas explicitly. Windows + Office: present. macOS + Office: present. macOS + Keynote/Preview: substitutes (Helvetica/Menlo) — the rendered PDF from LibreOffice uses Carlito as the Calibri stand-in but the look still matches because the metrics are identical. If you open in PowerPoint on a machine without Calibri (rare on Mac these days), the file declares Calibri so PPT will substitute appropriately.
- **`Week03_redesigned.pptx`** (the original) is untouched per the user's "new file" choice. Delete it whenever you no longer need the comparison.
- **Lab01 contribution**: minimal. Lab01 is 4:3 plainer slides; Lab02 is the polished 16:9 deck that defines the design system. Per the user's "Lab02 verbatim" choice, Lab01 only contributed the terminal-window convention (which Lab02 also uses).
- **Future maintenance**: To re-skin with different content, edit `build_week03.py` (each slide block is clearly labeled `SLIDE N`) and re-run `.venv/bin/python build_week03.py`.
