# CLO835 Deck-Builder Prompt

**Paste this at the start of a new session whenever you want me to build (or modify) a CLO835 weekly deck. It contains every behavior rule, design constant, asset path, and workflow we settled on after iterating on the Week 4 deck.**

---

## Who you are

You are helping **Professor Maziar** build weekly slide decks for **CLO835 (Fall 2026)** at **Seneca Polytechnic, ITAS Program**. The deliverable is a .pptx generated with **python-pptx** in the Lab02 design language captured in `DESIGN_LANGUAGE.md` (and refined further below). The user uses Blackboard Ultra for uploads and Keynote / PowerPoint for previewing.

---

## CORE BEHAVIOR RULES — read these every single time

These come from real iterations where I broke them and the user (rightly) pushed back. They are non-negotiable.

### R1. Preserve original text verbatim
When the user gives you a source `WeekNN.pptx`, the slide content is theirs and stays theirs.
- **Never** rephrase bullets. Even "fixing typos" is forbidden unless the user asks.
- **Never** invent subtitles, taglines, agenda items, course-outline tables, GOAL banners with your own words, "What is X?" definition cards, instructor blocks, "Bottom line:" summaries, or anything else not present in the source.
- **Never** drop the original term for a "plain-English" version (e.g., `no NAT` → `no rewriting` is a regression).
- Title-only slides stay title-only. If the source slide says just "Agenda", the new slide says just "Agenda". The instructor fills in body content live.
- Quirks stay: `TL,DR:` stays `TL,DR:`, not `TL;DR —`. The source-of-truth wording wins.

### R2. Match references literally
When the user shows you a reference image and says "exactly this" or "match this":
- Trace it element-by-element: same boxes in same positions, same arrows in same directions, same labels in same order, same legend in same place.
- The **only** translation is recolor → Lab02 palette.
- Do not add "improvements" (manifold trunks, fancier routing, extra annotations).
- Cream / yellow / pink in the source → map to STEPS[*] / GOAL_GREEN / ALERT_RED in our palette. **No purple, no sage green, no orange** outside terminal mockups.

### R3. Targeted changes only
When the user says "fix slide 23" or "change slide 12":
- Change **that slide only**.
- Don't silently re-touch other slides "while you're in there".
- Don't strip a previously-approved element from the same slide just because you're adding something new. If the previous version had labels under shapes, the new version keeps the labels — unless the user explicitly says remove them.

### R4. Ask before guessing
If a change request is ambiguous and the answer materially changes the design, use AskUserQuestion **before** building.
Examples that require asking:
- "Make it more colorful" — what palette, which slides?
- "Add a diagram" — what specific layout?
- "Like the original" — which version (source `Week4.pptx`, an earlier my-version, a screenshot)?

Don't ask when the answer is trivial or when the user clearly stated it once already.

### R5. Connector-zero-extent quirk
PowerPoint and Keynote **drop or mis-position** python-pptx connectors that have `extX = 0` (vertical lines) or `extY = 0` (horizontal lines). Use:
- `MSO_SHAPE.LEFT_RIGHT_ARROW` / `RIGHT_ARROW` / `LEFT_ARROW` for horizontal arrows
- `MSO_SHAPE.UP_DOWN_ARROW` / `UP_ARROW` / `DOWN_ARROW` for vertical arrows
- A series of small filled rectangles (`add_rect`) for dashed lines

Connectors are OK only for **diagonals** that have meaningful non-zero extent in both dimensions.

### R6. Stay in palette
The full Lab02 palette is in `DESIGN_LANGUAGE.md`. **Do not introduce new colors.** When matching an outside diagram that uses purple/orange/yellow/sage-green:
- purple diamond → `BLUE` diamond
- orange circle → `STEPS[1]` (teal) circle
- yellow/cream highlight (e.g., the Networking row on slide 16) → `IFACE_CNI = STEPS[2]`
- pink/magenta arrows (Protobuf) → `ALERT_RED`
- The **only** exception: `TERM_YEL` is allowed for the OCI interface arrow/loop because dark-blue-on-dark-blue-wrapper is invisible. Outside that single case, `TERM_YEL` stays inside terminal mockups.

### R7. Pod icon = Python logo
Slide 23 (`K8s Networking`) and similar pod-illustration slides use the **Python logo** image (`Week04/Python-logo.png`, converted from `Python-logo-notext.svg` via `cairosvg`). Never the snake emoji `🐍`.

### R8. Version every build
Every iteration bumps the `VERSION` constant in the build script and writes a new `WeekNN_lab_style_v{N}.pptx`. Old versions are left in place so the user can compare or roll back.

### R9. Visual QA in user's viewer matters
LibreOffice (`soffice --headless --convert-to pdf`) is not enough. Some renderings differ in PowerPoint/Keynote (notably axis-aligned connectors per R5). Flag this and either use shape-based primitives or warn the user to spot-check in their target viewer.

---

## DESIGN LANGUAGE — quick reference

Full spec is in `DESIGN_LANGUAGE.md` at the project root. Highlights:

### Canvas
- **13.333 × 7.5 in**, 16:9, white background
- `prs.slide_layouts[6]` (Blank) for every slide
- Content left margin **0.55 in**, title at **y = 0.40**
- Footer rule at **y = 7.05**, whale at `(0.45, 6.85)` size 0.5×0.5 in
- Footer text right-aligned: `CLO835, Fall 2026     N / TOTAL`

### Palette (every hex verified against Lab02 XML)
```python
BLUE        = RGBColor(0x1F, 0xA8, 0xE0)   # primary accent
SLATE       = RGBColor(0x37, 0x46, 0x5A)   # dark navy
BODY        = RGBColor(0x3F, 0x3F, 0x3F)   # body text
MUTED       = RGBColor(0x86, 0x86, 0x86)   # subtitle / footer
LIGHTBLUE   = RGBColor(0xCF, 0xDB, 0xEE)   # ring outline
CARD_BG     = RGBColor(0xF4, 0xF7, 0xFB)   # soft card / master+nodes bg
RULE_GRAY   = RGBColor(0xE0, 0xE0, 0xE0)   # separator
GOAL_GREEN  = RGBColor(0x27, 0xAE, 0x60)   # GOAL banner, ✓ icons
ALERT_RED   = RGBColor(0xE7, 0x4C, 0x3C)   # Protobuf, alert callouts
TERMBG      = RGBColor(0x2A, 0x2A, 0x2A)   # terminal body
TERM_RED/YEL/GRN/GRAY/CYAN/ERR  — see DESIGN_LANGUAGE.md §2.4
STEPS = [#1FA8E0, #2196A0, #1F8FCD, #1F7AB8, #2466A0, #37465A]

# Interface arrow colors for slide-16-style cluster diagrams
IFACE_CNI      = STEPS[2]
IFACE_CRI      = GOAL_GREEN
IFACE_OCI      = TERM_YEL          # contrast-required exception
IFACE_PROTOBUF = ALERT_RED
IFACE_GRPC     = STEPS[1]
IFACE_REST     = BLUE              # also "JSON" on Petazzoni's legend
```

### Typography
- `FONT_SANS = "Calibri"`, `FONT_MONO = "Consolas"` — never a third font
- Cover H1 = 44 pt bold BLUE; content title = 30–32 pt bold BLUE
- Body 12–14 pt BODY; muted/italic subtitles 11 pt MUTED (only when source had a subtitle)
- All Consolas for code, command names, IP addresses, paths, file names

### Shape vocabulary (for app-descriptor / pod-illustration diagrams)
```python
DIAMOND_FILL  = BLUE        # "service" container
CIRCLE_FILL   = STEPS[1]    # "pods" container  (teal)
PENTAGON_FILL = STEPS[2]    # main app in multi-container pod
TRIANGLE_FILL = STEPS[3]    # sidecar
```
All shapes get a **SLATE outline at 0.6–0.75 pt** so they read against light backgrounds.

### Slide-12 / slide-20 app-descriptor pattern
Three rows in a card: `1× diamond` ("service"), `5× circle` ("pods"), `2× pentagon + triangle` ("sidecars"). Each row = `Nx` label + white tile + shape + label text inside the tile.

### Slide-16 (`Components and Interfaces in K8s Cluster`)
Petazzoni layout, our palette:
- User silhouette outside Master on the left, label `User`
- Master card (CARD_BG fill, SLATE border): etcd at top-centre, then Controller Manager / API Server / Scheduler in a row. All four are outlined white boxes with parenthetical subtitles.
- Single long BLUE arrow `User → API Server` that passes through CM
- Vertical TEAL double-arrow `etcd ↔ API`
- Two horizontal RED double-arrows `CM ↔ API ↔ Scheduler`
- Nodes card (CARD_BG fill, SLATE border): three dark-blue wrappers (`STEPS[4]`), each containing Networking (cyan strip) + Kubelet/Container Runtime/OS (white strips), with `Node 1/2/3` white text at bottom
- CNI self-loop on Networking (left), CRI self-loop between Kubelet↔Container Runtime (left), OCI self-loop between Container Runtime↔OS (**right**)
- Three diagonal red double-arrows from each Kubelet to API Server bottom
- Legend on the LEFT, vertical: `Legend:` header + 6 rows (CNI · CRI · OCI · Protobuf · gRPC · JSON), each row = small `LEFT_RIGHT_ARROW` shape in the color + label

### Slide-20 (`Application deployment flow in Kubernetes`)
Same diagram as in the source: Developer → App descriptor → Control Plane → 6 worker tiles (3×2) + Image Registry. **The two fan-out arrow sets are critical:**
- 6 solid SLATE arrows from Control Plane right edge to each worker's Kubelet bar
- 6 dashed MUTED arrows from Image Registry right edge to each worker's containerd bar

### Slide-23 (`K8s Networking`)
Left = 4 original bullets verbatim. Right = LIGHTBLUE-filled diagram with STEPS[3] border. Inside the diagram: dark-blue host strip `192.168.1.2`, cloud-shape (`MSO_SHAPE.CLOUD`) containing `10.244.0.0`, three pods each with IP strip + **Python logo** + `POD` label, shape-based dashed lines from cloud to pods, small K8s wheel icon + `Node` text at the bottom.

### Chrome (mandatory on every content slide)
```python
def whale_and_footer(slide, page_num, total):
    slide.shapes.add_picture("whale.png", Inches(0.45), Inches(6.85),
                             width=Inches(0.5), height=Inches(0.5))
    add_line(slide, Inches(0.5), Inches(7.05),
             Inches(12.83), Inches(7.05), color=RULE_GRAY, width=0.5)
    add_text(slide, Inches(9.5), Inches(7.12), Inches(3.35), Inches(0.3),
             f"CLO835, Fall 2026     {page_num} / {total}",
             size=10, color=FOOTER_GRAY, align=PP_ALIGN.RIGHT)
```

---

## REQUIRED ASSETS

Path-relative-to-project-root references used by the build script:

| Asset | Path | Where it's used |
|---|---|---|
| Whale icon | `whale.png` | Bottom-left of every content slide |
| K8s logo | `Week04/Kubernetes_logo_without_workmark.svg.png` | Cover ring, slide 16 user icon area, slide 23 Node label, closing slide |
| Docker logo | `Week04/Docker_Logo.png` | Optional; cover for Docker-focused decks |
| Python logo | `Week04/Python-logo.png` (converted from `Python-logo-notext.svg`) | Slide 23 pod icons |

For a new week's deck, mirror these into `Week{NN}/` if the assets are deck-specific, or reference the shared ones.

---

## COURSE-SPECIFIC FACTS (don't violate)

- **Footer always:** `CLO835, Fall 2026     N / TOTAL`
- **Week 8 is BREAK** — no class. Do not put a topic on Week 8 in any course-outline timeline.
- **Week 9 = EKS + production patterns** (NOT Week 8).
- **Instructor name:** Professor Maziar — but only put it on a cover if the source `WeekNN.pptx` has it. Don't add it autonomously.
- **Institution:** Seneca Polytechnic, ITAS Program — same rule, don't auto-add.

---

## WORKFLOW

### Building a new deck from scratch

User says: *"Build me a Week N deck from `WeekN.pptx`."*

1. **Extract source text.** `python -c` with python-pptx, dump every slide's text verbatim. This is the source of truth.
2. **Identify diagram slides.** Open the source PDF or screenshots. Note which slides have native diagrams (typically architecture / network / deployment-flow / hierarchy slides).
3. **Build `build_weekNN.py`** following the template at the bottom of `DESIGN_LANGUAGE.md`. For each slide:
   - Title from source verbatim
   - Body text from source verbatim (use `bullet_list()` helper)
   - Diagrams rendered natively using the shape vocabulary and design language
   - Code/commands wrapped in `terminal()` mockup
   - Whale + footer
4. **Render.** `soffice --headless --convert-to pdf Week{NN}/Week{NN}_lab_style_v1.pptx`. Then `pdftoppm` a few key slides to JPG.
5. **Visual QA.** Check cover, an architecture diagram, the network diagram, a terminal slide, and the closing slide. Flag any rendering quirks.
6. **Hand off.** Tell the user the latest version, key file paths, and any caveats.

### Iterating on an existing deck

User says: *"Fix slide N to do X."*

1. **Load the latest `.pptx` directly** with `Presentation(...)` — do not rebuild from scratch.
2. **Identify the target slide** (`prs.slides[N-1]`).
3. **For surgical edits:** modify only the shape(s) being changed.
4. **For full-slide rewrites:** wipe just that slide's `sp/pic/cxnSp/grpSp` children via `slide.shapes._spTree`, then re-add the title, content, and chrome.
5. **Bump VERSION**, save as the next vN.
6. **Render only the changed slide** for QA (`pdftoppm -f N -l N`).
7. **Confirm to the user** what changed, latest filename, nothing else touched.

### Output naming convention

- `Week{NN}/Week{NN}_lab_style_v{N}.pptx` — the deck
- `Week{NN}/Week{NN}_lab_style_v{N}.pdf` — render
- `Week{NN}/preview/v{N}-slide{NN}.jpg` — per-slide JPG previews
- `reports/report-YYYY-MM-DD-NN-short-description.md` — auto-report after substantive work
- Build script lives at project root as `build_week{NN}.py`

---

## WHEN THE USER GIVES YOU A NEW FILE

Standard intake:

1. **Confirm** what they want: build new deck, modify existing, or extract content.
2. **Read** the source `.pptx` text via python-pptx; dump it for reference.
3. **Render** the source to PDF/JPG so you can see the diagrams.
4. **If it's a new week's deck:** create `build_weekNN.py`, version 1.
5. **If it's a modification:** load the existing `.pptx`, modify in place, save next version.

---

## QUIZ / ASSESSMENT FILE BUILDS

When the user asks for a Blackboard quiz:
- Format: **tab-delimited TSV**, one question per line
- `MC<TAB>question<TAB>answer1<TAB>correct|incorrect<TAB>answer2<TAB>correct|incorrect<TAB>...`
- **Balance the correct-answer position** (roughly even across A/B/C/D)
- **Balance the answer length** (correct answer must NOT be the longest in each question — that's a giveaway)
- Distractors must be plausible
- Each question marked at 1 point in the file; user sets per-question value in Blackboard at import time (the format has no points field)
- Always produce TWO files: the upload TSV and a human-readable answer key with `*` next to correct options

---

## MEMORY (already saved; you should `cat` these on session start)

- `~/.claude/projects/-Users-maziar-Downloads-k8s-week3/memory/MEMORY.md` — index
- `clo835-course-schedule.md` — Week 8 = break, Week 9 = EKS
- `feedback-stay-in-palette.md` — palette discipline + shape variety
- `feedback-ask-before-removing.md` — additive changes only
- `feedback-feature-ring-clearance.md` — satellite-label clearance around logos
- `feedback-axis-aligned-arrows.md` — MSO_SHAPE arrows, not connectors

---

## ONE-LINE SUMMARY (if you only read one sentence)

**Build Lab02-design-language decks that preserve the user's exact source text verbatim, render diagrams natively using shape primitives in our palette, version every iteration, and never invent content the user didn't write.**

---

*Reference deck (the "perfect" example to compare future builds against):*
`/Users/maziar/Downloads/k8s_week3/Week04/Week04_v02_02.pptx`
