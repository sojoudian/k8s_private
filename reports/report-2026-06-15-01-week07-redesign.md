# Report: Week 7 Redesign (Week07.pptx → Week07_lab_style_v1.pptx)
**Date**: 2026-06-15
**Sequence**: #01 for the day

## Summary
Redesigned `/Users/maziar/Downloads/Week07.pptx` ("Volumes: Attaching Disk Storage to Containers",
14 slides) into the exact CLO835 design language and saved it inside the project at
`Week07/Week07_lab_style_v1.pptx`. Content preserved verbatim; only the design changed.

## What Changed
- **Created** `build_week07.py` (project root) — generator based on `build_week06.py` (same palette,
  Calibri/Consolas, terminal, multi-level bullets, embed, coord guard).
- **Created** `Week07/Week07_lab_style_v1.pptx` + `.pdf` (14 slides).
- **Created** `Week07/assets/fig_gitrepo.jpg` (gitRepo diagram cropped from source).

## Technical Details
Comprehensive intake (recursive pic scan + SmartArt flag + rendered & viewed all 14 source slides):
no SmartArt; the title-only-looking slides hid content as images/native shapes — caught them:
- **Slide 10** "Using GitRepo Volume" = a native-shape diagram → cropped from source PDF
  (`pdftoppm -x -y -W -H -r200`) and embedded under our blue title.
- **Slides 11/13/14** = YAML manifests stored as images/text → redrawn as our dark terminal mockups
  (top-level keys cyan, body gray). Slide 11 also got 4 annotation cards (CARD_BG + blue accent bar +
  mono key + explanation) reproducing the source's gitRepo/repository/revision/directory callouts.
- Slides 1–9, 12 = cover + multi-level bullet slides in the exact palette/fonts.

Design: 16:9, blue Calibri titles at (0.55,0.40), STEPS bullets (▪/–), whale + footer "CLO835,
Fall 2026  N / 14", terminal mockups with traffic-light dots, K8s-logo-in-ring cover. Verbatim text
(incl. em-dashes, quirks). Float-coord guard applied.

## Results
- Built (14 slides), rendered, and visually QA'd every slide: clean, on-brand, no overflow,
  diagrams/terminals correctly placed. Output is in the project's `Week07/` folder as requested.

## Issues / Notes
- Single combined deck (not split into lecture/lab) — matches the source structure; the user can
  split later as they did for Weeks 5/6.
- Volume-type identifier names rendered in Calibri (sans) like the prior weeks' bullet slides, not
  inline mono — consistent with the existing decks.
