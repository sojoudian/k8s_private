# Report: Week14 (RBAC-continued / HPA / IRSA) — v1 house-design redesign

**Date**: 2026-07-27
**Sequence**: #01 for the day

## Summary
Redesigned the new `week14/Week12.pptx` (30 slides; "Introduction to K8s RBAC, Continued / Horizontal
Pods Autoscaling / IRSA"; self-labels "Week 12") into the exact CLO835 Lab02 house design as
`week14/Week14_lab_style_v1.pptx` — a single combined v1 deck like the other weeks' v1. Content
preserved verbatim (PROMPT.md R1); redesign only. Built via the proven `build_week12` engine import,
the same extraction→crop→assemble→build→adversarial-QA pipeline used for Week13.

## What Changed (new files)
- `week14/Week14_lab_style_v1.pptx` — 30 slides, 2 hidden (23,24 kept hidden per source).
- `build_week14.py` (repo root) — imports `build_week12` (guarded) for the palette/coord-guard/
  terminal/bullets/divider/closing/course-outline helpers; adds week14 cover (meme dropped, "Week 12"
  label + the two continuation topics), whitespace normalization (`\xa0`/`\x0b`→space), acronym fixup,
  command-list→terminal, figure+terminal layout, wide-diagram full-width layout, full-bleed screenshot
  handling. Loads `week14/week14_deck.json`.
- `assemble_week14.py` (repo root) — builds the deck JSON from the extraction + crop data; crops 7
  genuine diagrams/screenshots into `week14/assets/`; hardcodes the verbatim slide-3 course outline.
- `week14/week14_deck.json`, `week14/assets/fig{10,11,17,20,21,23,24}.png`.

## Process
1. Rendered all 30 slides (incl. hidden 23,24 via an all-shown copy) + dumped verbatim text — the deck
   is image-heavy (YAML/kubectl/aws-cli terminals + diagrams + AWS-console screenshots in pictures).
2. Parallel verbatim extraction of all 30 slides (title/hier-bullets/code transcription/diagram flag).
3. Crop-box measurement over the 12 figure-bearing slides — kept 7 (diagrams/screenshots), dropped 5
   decorative (workshop-divider photos on 14/22, "Goals"/"Cleanup" clipart on 15/30, discussion clipart
   on 18 whose real output is body text).
4. Assemble → crop → build → **adversarial QA** comparing every rebuilt slide to its source.

## Redesign decisions (per R1)
- Cover: meme dropped → house cover; "Week 12 · Lecture" self-label kept verbatim.
- Course Outline: native 4×4 boustrophedon grid, 16 verbatim tiles (source's ORIGINAL numbering:
  Week 8=PVs … Week 14=Helm; Week 1 highlighted). NOTE: this differs from the Week13 deck's renumbered
  outline — each deck's own slide-3 is reproduced faithfully.
- Workshop dividers (4,14,22) → house slate-circle dividers; "End of workshop N" (13,19,27) → closings.
- Command/aws-cli lists → house dark terminal mockups; genuine diagrams/screenshots → cropped & embedded.
- Full-bleed screenshots: slide 17 (IAM console) and slide 24 (fully-annotated kube-ops-view with 7
  labels+arrows) embedded whole, no duplicate house title.
- Source typos/spacing kept ("withmultiple", "workshop1", double spaces, "Kube-Sytem").

## QA findings fixed (5 raised → all resolved)
- Slides 10 & 23 (MAJOR): a figure + a command/code block — my figure branch only handled
  body-commands, so the terminal was dropped. Fixed: figure+terminal layout renders both.
- Slide 24 (MAJOR): tight crop cut off the 7 annotation labels/arrows. Fixed: crop the whole annotated
  slide and embed full-bleed.
- Slide 1 (MINOR): "Horizontal Pod" → restored source's plural "Horizontal Pods".
- Slide 8 (MINOR): title "Configmap.check" merged (image-extraction lost the source's `\x0b` break);
  restored to "ConfigMap. Check" via override.

## Results
- 30 slides, 2 hidden (23,24), **0 float coordinates**, footers "N / 30" correct on every slide, 7
  embedded figures. Full-deck adversarial QA clean after fixes. Delivered to `week14/`; source
  `week14/Week12.pptx` untouched (2,829,324 bytes, unchanged).

## Issues / Notes
- Cover self-labels "Week 12" (source's own label; folder is `week14` — same folder-vs-label offset as
  the other decks). Source's slide-3 outline uses original week numbering; not reconciled with the
  Week13 deck's renumbered outline (both faithful to their own source).
- Only v1 (combined) built, as the redesign brief asked. A lecture/lab split (v2) can follow if wanted.
