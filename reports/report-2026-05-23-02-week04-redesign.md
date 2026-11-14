# Report: Week 04 Redesign in Lab02 Design Language
**Date**: 2026-05-23
**Sequence**: #02 for the day

## Summary
Converted the user's original `Week04/Week4.pptx` (Intro to Kubernetes, 37 slides) into a
new 38-slide deck `Week04/Week04_lab_style.pptx` rendered verbatim in the Lab02 design
language documented in `DESIGN_LANGUAGE.md`. Per the user's choices, ALL architecture
diagrams were redrawn natively with python-pptx shapes (no embedded PDFs), and BOTH
"slide 24" variants from the source materials were preserved as separate slides (one for
the multi-node IP conflict, one for the routing-fix). The K8s logo was used as the
cover-ring image. Built, rendered to PDF and per-slide JPGs, spot-checked the high-stakes
slides, fixed five QA issues in a single batch, re-rendered, verified.

## What Changed
- **`Week04/Week04_lab_style.pptx`** — new 38-slide deck (~140 KB). 16:9 widescreen,
  blue Calibri titles, whale + footer on every slide, Lab02 palette throughout.
- **`build_week04.py`** — ~1500-line python-pptx generator. Reuses every helper from
  `build_week3.py` so palette and layout primitives stay identical; adds two new helpers
  (`add_hex` for hexagon shapes, `add_arrow` for arrow-headed connectors, `section_divider`
  for the centered chapter-break template).
- **`Week04/preview/slide-NN.jpg`** — 38 per-slide JPG renders at 90 dpi for visual QA.
  Safe to delete.
- **`Week04/Week04_lab_style.pdf`** — the LibreOffice PDF render used as the JPG source.
- **`Week04/preview-slide *.jpg`** — temporary references rendered from the user's
  diagram PDFs (slides 12, 13, 14, 15, 16, 20, 23, 24-top, 24-bottom, 31, 33, 7), used to
  understand the source diagrams before redrawing them natively. Safe to delete.

## Technical Details

### Slide map (38 slides)
1. Cover — "Introduction to Kubernetes", K8s logo in LIGHTBLUE ring
2. Agenda — 5 numbered objective rows
3. Course Outline — 8-week course with status pills (Done/Today/Next/Soon)
4. Why we need an orchestration tool — left text, right 5 red-bar gap cards
5. Container Orchestration — section divider with 3 meta blocks
6. Container Orchestration Technologies — 4-column card grid (K8s, Swarm, Mesos, Nomad)
7. What is Kubernetes? — definition + 3 facts + K8s logo with 6 features in a ring
8. Main advantages of K8s — 2×2 numbered-circle grid
9. From the Developer's Perspective — 2-column (do/stop) checklists
10. From the Operations Perspective — 2-column (gets/gives) left-bar cards
11. Other things K8s can do — 4×2 colored card grid (8 features)
12. K8s architecture from 10,000 feet — redrawn dev→descriptor→master→workers
13. K8s architecture — control plane vs data plane (2 big component cards)
14. K8s components — 3×2 colored component cards
15. What lies where — redrawn master column + 3 worker columns
16. Components & interfaces — redrawn master card with 4 boxes + nodes card with 3 columns
17. Running an application — meet kubectl (left facts + right terminal)
18. Deploying to K8s — 5 numbered prereqs (full-width cards)
19. Running an application — full picture (6-step horizontal flow + manifest contents)
20. Application deployment flow — redrawn dev+descriptor+registry+CP+6 worker nodes
21. Ready for K8s deployment — section divider with 3 meta blocks
22. K8s network model — big TL;DR banner + 5 numbered rules
23. K8s networking — single node (redrawn host+cloud+3 pods) + 3 rules
24. K8s networking — multi-node CONFLICT (top variant: red X between two clashing nodes)
25. K8s networking — multi-node FIX (bottom variant: routing hex between two distinct subnets)
26. Hosting K8s cluster — 7 hosting options in a 3-column grid
27. Workshop 1 — section divider with Time/Prereqs/Deliverable meta
28. Relevant links — 4 left-bar accent cards with URLs
29. Workshop pre-requisites — full-width terminal mockup
30. Create the cluster description, then deploy — terminal + checklist
31. Deploy our first application — terminal + "What is a pod?" card
32. Flow of "kubectl run" — 8 numbered step boxes + 3 actor pills
33. Expose your application — terminal + "What is a Service?" card
34. Deployment · ReplicaSet · Pods · Nodes — redrawn 4-tier hierarchy
35. Access · scale · inspect · roll forward — two side-by-side terminals
36. Bonus: deploy the K8s dashboard — terminal + browser URL + checklist
37. Workshop 1 — that's a cluster — closing slide with 3 wrap-up boxes + K8s logo
38. References & further reading — 5 left-bar accent cards with URLs

### Design fidelity vs Lab02
- ✅ Slide size: 13.333 × 7.5 in.
- ✅ Palette: `#1FA8E0` blue, `#37465A` slate, `#3F3F3F` body, full Lab02 palette.
- ✅ Fonts: Calibri (sans) + Consolas (mono) only.
- ✅ Title: blue 32 pt bold at (0.55, 0.40) on every content slide; 44 pt on cover/closing.
- ✅ Chrome: whale at (0.45, 6.85) + horizontal rule at y=7.05 + footer
  "CLO835, Fall 2026  N / 38" right-aligned. All 38 slides.
- ✅ Terminal mockups with red/yellow/green traffic-light dots, dark title bar,
  Consolas code in green/cyan/gray/error palette. Used 12 times across the deck.
- ✅ Step blocks use the STEPS gradient (`STEPS[0..5]`).
- ✅ Left-bar accent cards (CARD_BG + 0.10-in colored bar) used for GOAL banners,
  link lists, sidebars, alert callouts.
- ✅ Section dividers (slides 5, 21, 27) use the centered slate circle + heading +
  italic subtitle + 3 meta blocks pattern.
- ✅ K8s logo (Week04/Kubernetes_logo_without_workmark.svg.png) used on cover, slide 7
  (features ring), and slide 37 (closing).
- ✅ No drop shadows; no mono caps kickers; no emoji except the snake icon inside the
  POD boxes (deliberate, matches the source diagrams).

### QA loop
First render → 5 layout issues found via per-slide JPG inspection:

| Slide | Issue                                                                       | Fix                                                              |
| ----- | --------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| 15    | Node labels clipped by a physical-network bar at y=6.70                     | Removed the redundant bar; reduced node-label font from 12→11    |
| 16    | (a) Subtitle clipped by Master card · (b) USR→API arrow cut through the Controller Manager box · (c) per-node labels overlapped the bottom legend | (a) Removed subtitle · (b) Re-routed the arrow up and over the master card · (c) Dropped per-node labels (the "Nodes" header is enough) and moved the legend to y=6.65 |
| 25    | CNI plugins legend overlapped the snake icons inside the pod boxes          | Moved the legend OUTSIDE the cluster card to y=6.60              |
| 29    | Terminal body overflowed the dark frame at the bottom                       | Extended terminal h from 4.55 → 4.70 in and condensed 2 lines    |
| 30    | Terminal body overflowed (same root cause)                                  | Extended terminal h from 4.55 → 4.70 in and merged 2 status lines |
| 36    | (a) Missing white "✓" inside the green ovals · (b) bottom alert was a thin red bar with floating text | (a) Added text + sized the ovals from 0.22→0.26 · (b) Re-built as a proper left-bar accent card |

After fixes → re-render → all 6 slides verified clean.

### Inputs used
- `Week04/Week4.pptx` — source content (text extracted via python-pptx for the slide map).
- `Week04/Kubernetes_logo_without_workmark.svg.png` — K8s logo (cover, slide 7, closing).
- `Week04/Docker_Logo.png` — declared as `DOCKER_LOGO` constant but not embedded in the
  final deck. Could be added on the workshop slides if desired.
- `Week04/slide *.pdf` / `.png` files — used as visual reference only; redrawn natively
  with python-pptx shapes per the user's choice.
- `whale.png` (from the project root, originally extracted from Lab02) — bottom-left chrome.

## Results
- **Final deliverable:** `Week04/Week04_lab_style.pptx` (38 slides, ~140 KB).
- **Render:** clean LibreOffice PDF render, no overlapping shapes, no text overflow,
  footer renders correctly with 2-digit `N / 38` page numbers on all 38 slides.
- **Coverage:** every slide of the original Week 4 deck has a counterpart in the new
  deck (37 → 38, with the dual "slide 24" preserved as separate slides per the user's
  choice).
- **All diagrams redrawn natively** — no embedded PDF images. Notable redraws: K8s
  features ring (slide 7), 10,000-foot architecture (slide 12), control/data plane cards
  (slide 13), six-component grid (slide 14), what-lies-where master+nodes layout (slide
  15), components & interfaces (slide 16), application deployment flow (slide 20),
  single-node networking (slide 23), multi-node conflict + fix (slides 24-25), kubectl
  run 8-step flow (slide 32), Deployment-ReplicaSet-Pod-Node hierarchy (slide 34).

**Port allocation:** N/A — no dev server in this session.

## Issues / Notes
- **Docker logo** is declared as a constant (`DOCKER_LOGO`) but isn't placed on any
  slide in the final deck. The course is K8s-focused, so the K8s logo carries the visual.
  If you want a Docker logo on (e.g.) the workshop opening or alongside the kubelet
  diagrams, the asset is loaded and ready — just one line to insert.
- **Snake emoji 🐍** is used inside the POD mockups on slides 23, 24, 25 to match the
  source diagrams' "snake-in-a-box" pod visual. It renders fine in LibreOffice and
  modern PowerPoint; if a target machine lacks an emoji font, it will render as a box.
  Safe to replace with a small SLATE filled circle if that's a concern.
- **Slide 16 arrow** now routes up and over the master card. This is the cleanest
  routing given USR is positioned beside the master (not above it). If you'd rather move
  USR to a different position, it's a 2-line edit in the script.
- **Source content preserved verbatim where possible.** The text from each source slide
  was re-cast into Lab02-style components (numbered objectives, step blocks, GOAL
  banners). Some additional commentary was added on the K8s component cards (slide 14)
  and the agenda (slide 2) to explain each concept in the design's voice — feel free to
  trim if you want a more literal port.
- **`build_week04.py` follows the same pattern as `build_week3.py`** — to re-skin or
  edit, search for `# SLIDE N` comment markers; each slide block is clearly delimited.
- **Preview JPG artefacts** (`Week04/preview/`, `Week04/preview-slide *.jpg`) are not
  needed for the final deliverable. Safe to delete with `rm -rf Week04/preview*` if you
  want a tidier folder.
