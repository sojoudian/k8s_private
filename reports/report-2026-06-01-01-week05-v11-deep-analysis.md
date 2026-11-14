# Report: Deep analysis of Week05_lab_style_v11.pptx
**Date**: 2026-06-01
**Sequence**: #01 for the day

## Summary
Full deep audit of `Week05/Week05_lab_style_v11.pptx` (39 slides) — visual inspection of every slide plus structural XML scan. Headline finding: a **float-coordinate XML defect** that affects connectors on slides 6, 17, and 21. In LibreOffice/PDF these render acceptably, but PowerPoint/Keynote cannot parse non-integer EMU values and silently mis-position the shape (which is what the user observed on slide 17 with the red arrow appearing "at the top of the page"). Slide 21's entire deployment hierarchy diagram is at risk for the same reason, and slide 21's POD→NODE lines also have a layout bug (all 6 lines originate from the same anchor). A separate content gap: slides 34, 35, and 39 in the source had pictures (likely YAML descriptor blocks) that were silently dropped in the build.

## What Changed
No file changes in this report — analysis only. Two artifacts produced:
- `Week05/v11_jpgs/slide-01.jpg` … `slide-39.jpg` — per-slide renders used for visual inspection.
- This report.

## Technical Details

### Methodology
1. Rendered the v11 PDF to per-slide JPGs at 90 DPI via `pdftoppm`.
2. Visually inspected every one of the 39 slides.
3. Walked the `.pptx` XML to find:
   - non-integer values inside `<a:off>` / `<a:ext>` / `<a:chOff>` / `<a:chExt>`
   - shapes whose bounding box exits the 13.333×7.5 in canvas
   - connectors with zero extent in one dimension (axis-aligned-connector hazard)
4. Diffed verbatim text frames between `Week5.pptx` (source) and v11 (built) using python-pptx, comparing titles and bullets.
5. Cross-checked source slides flagged as title-only against the source picture count, to surface image-backed content that was dropped.

### Root cause: float coordinates in OOXML

OOXML demands EMU coordinates be **integers** inside `<a:off x="…" y="…">` and `<a:ext cx="…" cy="…">`. In Python, the `/` operator always returns a float, so an expression like `box_target_y = (box_top + box_bot) / 2` produces a float; when python-pptx writes that to XML it serialises as `"4288536.0"` (decimal point preserved). LibreOffice happens to round-trip such values, but Keynote and PowerPoint reject them and fall back to coordinate `0`. That is why slide 17's red diagonal arrow renders correctly in the PDF but appears at the top edge of the slide in the user's screenshot.

The same defect exists on:
- **Slide 6** — 4 small connectors used to decorate the database icon (the disc "spine" lines). They are tiny so it has not been noticed, but in Keynote they will fly to (0,0).
- **Slide 17** — the known POD-Definition → red-box arrow.
- **Slide 21** — **every single connector** in the Deployment → ReplicaSet → Pod → Node hierarchy is stored with float coordinates. This is the deck's most complex diagram and it is silently broken for any PowerPoint or Keynote viewer.

### Slide 21 has a second, independent layout bug
The 6 POD→NODE connectors (`Connector 40`–`Connector 45`) all share the same starting X (`x = 4.55 in`), so all six lines converge at the leftmost POD and fan downward instead of starting from each individual POD. Visible in the PDF as a "spaghetti" of lines all originating at one circle.

### Title-only slides that actually had image content in the source
Per memory `feedback-text-extract-misses-images`, the python-pptx text extractor only sees text frames. Cross-checking by picture count:

| Slide | Source title | Source pictures | Built result |
|-------|--------------|----------------|--------------|
| 33 | Descriptor: Deployment | 1 image | Already redrawn natively in v11 (good) |
| **34** | Descriptor: ReplicaSet | **1 image** | **TITLE-ONLY in build (missing YAML)** |
| **35** | Descriptor: Pod | **1 image** | **TITLE-ONLY in build (missing YAML)** |
| **39** | Workshop 1 – The End | **1 image** | **TITLE-ONLY in build (missing closing image)** |

These three slides violate Rule 1 — they have source content that did not make it into the build.

### Axis-aligned connectors (zero extent)
Almost every slide uses `add_line` (a python-pptx connector with `cy=0`) for the footer horizontal rule. Per memory `feedback-axis-aligned-arrows`, this is technically a known-fragile pattern in Keynote/PowerPoint. Empirically the footer rule has been rendering OK in the user's environment, so this is a latent risk rather than an observed failure. The reliable fix is the `hline()` thin-rectangle helper. Worth fixing pre-emptively for the footer rule and for `Connector 11` on slide 21 (a true vertical connector with `cx=0`).

## Results

### Per-slide visual issue list (observed in the LibreOffice PDF render)

| # | Title | Issue | Severity |
|---|------|-------|----------|
| 1 | Title slide | Clean | — |
| 2 | Agenda | Clean (added intentionally on user request) | — |
| 3 | Pods vs Containers | Clean | — |
| 4 | Pods – The best of VMs and Containers World | Clean | — |
| 5 | Pods Use Cases | Bullet hierarchy preserved correctly | — |
| 6 | Splitting Application into Multiple Pods | 4 decorative connectors on DB icon have float coords | **Low** (Keynote: invisible) |
| 7 | Running Multiple Containers in a Pod | Clean | — |
| 8 | Collocating Processes in the Pod | Clean | — |
| 9 | Introducing Pod Descriptor | Clean | — |
| 10 | YAML – Pod Descriptor | Last line ("cpu: 100m") clipped at terminal bottom | **Low** |
| 11 | Creating Pods from Descriptor | Clean | — |
| 12 | Pods: Summary | Clean | — |
| 13 | Pods: Summary Continued | Clean | — |
| 14 | Organizing K8s Objects with Labels | Layout is decorative – source has labels with specific pod colors; the build chose its own. Acceptable if the prof signs off | **Info** |
| 15 | Labels in K8s | Clean | — |
| 16 | Scaling Pods | Clean | — |
| **17** | Creating ReplicaSet from Descriptor | **Red arrow uses float coords → renders at top of slide in Keynote/PPT** | **HIGH** |
| 18 | How does ReplicaSet know what to Monitor? | Yellow "tier: front-end" tag overlaps the adjacent POD card; bottom-row tag is truncated | **Med** |
| 19 | Creating ReplicaSet from Descriptor (terminal) | Clean | — |
| 20 | Scaling Pods - ReplicaSet | Clean | — |
| **21** | K8 Objects - Hierachy | **All hierarchy connectors stored with float coords (silent fail in PPT/Keynote). Also: 6 POD→NODE lines all originate from the same POD.** Also: title is "Hierachy" — misspelling preserved from source | **HIGH** |
| 22 | Pods -> ReplicaSets -> Deployments | All bullets at L1; source had no nesting, so OK | — |
| 23 | Descriptor: Deployment | YAML overruns the terminal box bottom; "type: front-end" clipped | **Low** |
| 24 | Organizing Pods - Namespaces | Clean | — |
| 25 | Workshop 1 – Deployment of K8s Pod | LAB title-card pattern | — |
| 26 | Deployment of K8s Pod - Prerequisites | Title-only (matches source) | — |
| 27 | Preparing the cluster | Title-only (matches source) | — |
| 28–32 | Workshop terminals | Clean | — |
| 33 | Descriptor: Deployment | YAML overflows terminal bottom; bullet body verbatim | **Low** |
| **34** | Descriptor: ReplicaSet | **TITLE-ONLY in build, source had a YAML image** | **HIGH** |
| **35** | Descriptor: Pod | **TITLE-ONLY in build, source had a YAML image** | **HIGH** |
| 36 | Scaling | Clean | — |
| 37 | Rolling out a new version | Title-only (matches source) | — |
| 38 | Maintaining the desired state - Resilience | Clean | — |
| 39 | Workshop 1 – The End | Title-only; source had a closing image | **Low** |

### Structural audit totals
- **Float-coordinate connectors**: 21 connectors on 3 slides (slide 6: 4, slide 17: 1, slide 21: 16).
- **Off-canvas shapes**: 0.
- **Zero-extent connectors**: 41 (mostly the footer rule – latent risk per memory).

### Verbatim text (source vs build)
- All title and bullet text compared cleanly except for non-breaking-space → space normalisation (cosmetically identical).
- No paraphrasing detected in the body content of inspected slides.
- Slide 2 Agenda content is non-verbatim, but added at user's explicit prior request – memory captures this.

## Priority fix list (recommend for v12)

1. **Slide 17 — red arrow position** (HIGH). Cast all connector coordinates to `int()` and/or decompose the diagonal into an L-shape using `hline`/`vline`. This is exactly the pattern in memory `feedback-axis-aligned-arrows`.
2. **Slide 21 — hierarchy diagram** (HIGH). Same int-cast across every connector. Additionally, re-anchor each POD→NODE line to start from its own POD instead of all six from (4.55, 4.70). Also fix the title "Hierachy" → "Hierarchy" (unless prof wants source spelling preserved).
3. **Slides 34, 35, 39 — missing image content** (HIGH). Render the source slides to JPG, recreate the YAML / closing imagery natively in our terminal-mockup style.
4. **Slide 18 — overlapping yellow tags** (MED). Move "tier: front-end" labels outside the next POD card or shrink them; the bottom row truncation is a clipping artifact.
5. **Slides 10, 23, 33 — YAML terminal overflow** (LOW). Terminal heights are too short for their content; enlarge or shrink Consolas size.
6. **Slide 6 — DB icon micro-connectors** (LOW). Same int-cast; alternatively replace with thin filled rectangles via `hline`/`vline`.

## Issues / Notes

- **The float-coordinate bug almost certainly affects more than just slide 17 in the user's actual viewer.** Slide 21's whole hierarchy is at risk and the user hasn't reported it because it hasn't been opened in PowerPoint/Keynote yet (or the rendering happened to land near the original location).
- The memory entry `feedback-axis-aligned-arrows.md` already captured this exact failure mode in Week 4 slide 16; I did not apply the learning when I wrote v11's arrow code (`(box_top + box_bot) / 2` produces a float, and I passed it to `add_connector` without an int-cast). Adding an `int()` cast inside `add_arrow` would have prevented the whole class of bug.
- Pre-emptively converting `add_line` footer rules to `hline()` rectangles would eliminate the 41 latent zero-extent connectors and harden the deck against future viewer changes.
- Title typo "K8 Objects - Hierachy" on slide 21 is verbatim from the source — leaving it in is faithful to Rule 1, fixing it would be a paraphrase. Worth raising with the user explicitly.
