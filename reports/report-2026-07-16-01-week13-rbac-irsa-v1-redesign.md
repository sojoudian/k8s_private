# Report: Week13 (RBAC + IRSA) — v1 house-design redesign

**Date**: 2026-07-16
**Sequence**: #01 for the day

## Summary
Redesigned the new `week13/week13.pptx` (46 slides, "Introduction to K8s RBAC + IRSA", self-labels
"Week 11") into the exact CLO835 Lab02 house design as `week13/Week13_lab_style_v1.pptx` — a single
combined v1 deck like the other weeks. Content preserved verbatim (PROMPT.md R1); this was a redesign
only, no content changes. Built via a data-driven generator that reuses the proven, guarded
`build_week12` engine, with genuine diagrams cropped from the source and embedded, and all
terminal/YAML/kubectl content rebuilt as house terminal mockups.

## What Changed (new files)
- `week13/Week13_lab_style_v1.pptx` — 46 slides, 6 hidden (9–14, preserved from source).
- `build_week13.py` (repo root) — imports `build_week12` (guarded) for the palette/coord-guard/
  terminal/bullets/divider/closing/course-outline helpers; adds week13 cover, dispatch,
  self-contained figure-embed, command-body→terminal logic, acronym fixup, and hidden-slide handling.
  Loads content from `week13/week13_deck.json`.
- `assemble_week13.py` (repo root) — builds `week13/week13_deck.json` from the extraction + crop data
  and crops the diagram figures into `week13/assets/`.
- `week13/week13_deck.json`, `week13/assets/fig*.png` (17 cropped diagrams).

## Process
1. Rendered all 46 source slides (incl. hidden) to images + dumped verbatim text. The deck is
   heavily image-based (YAML/kubectl/terminal output and architecture diagrams live inside pictures),
   so visual reading was mandatory — python-pptx text extraction alone misses that content.
2. Fanned out a **verbatim extraction** across all 46 slides (structured: title, hierarchical
   bullets, code transcription, diagram-vs-terminal classification).
3. Measured tight **diagram crop boxes** + re-read truncated terminals in a second parallel pass.
4. Assembled the DECK, cropped 17 diagrams, built, rendered, and ran an **adversarial QA workflow**
   comparing every rebuilt slide to its source (verbatim + layout). Fixed all findings, rebuilt, re-verified.

## Redesign decisions (per PROMPT.md)
- Cover: memes dropped → house cover ("Introduction to K8s RBAC" / "Week 11 · Lecture" / IRSA subtitle).
- Slide 3 Course Outline: rebuilt natively as the 4×4 boustrophedon grid, 16 verbatim week labels.
  **The source highlights "Week 1: Docker Introduction" (blue) — reproduced faithfully (not touched).**
- Genuine diagrams (auth flow, 2×2 auth-methods grid, RBAC who/what, IRSA, kubeconfig, namespace/
  cluster-scope) cropped from the source and embedded as-is (the week12 FIG pattern).
- Command lists rendered as dark terminal mockups (house style); YAML/output as terminals.
- Source typos kept verbatim ("Withmultiple", "Kuberntes", "defaul t", "kube-porxy", doubled "K8s-").
- 6 hidden source slides (Workshop 1 serviceaccount section, 9–14) kept hidden.

## QA findings fixed
- Slide 21 mis-classified as a bare divider → restored as content with its RBAC namespace/cluster-scope diagram.
- Slides 25 & 27 dropped their command bullets → command-body→terminal fix restores them (fig+commands layout).
- Slide 27 diagram top-labels clipped → re-cropped with more top margin.
- Slides 32/10/9 terminal "voids" → content-fit / independent-height terminals.
- Slide 10 title demoted to a bullet by the extractor → restored via override.
- Title acronyms (Api/Sa/Iam/Eks) → acronym fixup so they read API/SA/IAM/EKS/RBAC/AWS.

## Results
- 46 slides, 6 hidden (9–14), **0 float coordinates**, footers "N / 46" on every slide, 17 embedded
  diagrams. Full-deck adversarial QA clean after fixes. Delivered to `week13/`; source deck untouched.

## Issues / Notes
- Cover reads "Week 11 · Lecture" (source self-label), consistent with the other weeks' folder-vs-label
  offset (folder week13 = topic "Week 11" RBAC). Same standing label question as the other decks.
- Course-outline highlights Week 1 because the source does; flip on request.
- Only v1 built (combined deck), as asked. A lecture/lab split (v2) can follow if wanted.
