# CLO835 PowerPoint Design Language

> **Purpose** — This file is the single source of truth for the look-and-feel of every CLO835
> course deck (Week 03 lecture, Lab 02 redesign, Lab 03 guide, Hands-on lab, etc.).
> It is derived **verbatim** from `Lab02.pptx`'s XML and the four `build_*.py` generators
> in this directory (`build_week3.py`, `build_week03.py`, `build_lab.py`, `build_lab_guide.py`),
> all of which already implement this language identically.
>
> Anything below is reproducible from the source files. If you have to invent something
> not listed here, **stop and check the existing decks first** — chances are the pattern
> already exists.

---

## 0. TL;DR — the five things that make every slide feel "ours"

1. **White background, blue Calibri title top-left** — 30–32 pt for content slides, 40–44 pt for cover.
2. **Dark "terminal mockup" rectangles** with red/yellow/green traffic-light dots and Consolas code, for every command sequence.
3. **Dark-slate filled circles with white numbers** for step / objective / takeaway markers.
4. **Tiny cyan whale icon bottom-left + thin gray rule + footer bottom-right** on every slide
   (`CLO835, Fall 2026     N / TOTAL`).
5. **Lab02 blue gradient step-blocks** (`#1FA8E0 → #2466A0 → #37465A`) for tagging the parts of a lab.

If those five elements are present, the deck is on-brand.

---

## 1. Canvas

| Property              | Value                       | EMU                |
| --------------------- | --------------------------- | ------------------ |
| Aspect ratio          | 16:9 widescreen             | —                  |
| Slide width           | **13.333 in**               | 12 192 000         |
| Slide height          | **7.5 in**                  | 6 858 000          |
| Background            | **White** (`#FFFFFF`)       | —                  |
| Slide-master layout   | `prs.slide_layouts[6]` (Blank) | —              |
| Content left margin   | **0.55 in**                 | —                  |
| Content right edge    | **12.75 in** (right margin = 0.583 in) | —       |
| Content top (titles)  | **0.40 in**                 | —                  |
| Content bottom (last band before footer) | **6.70 in**      | —              |
| Footer rule line      | y = **7.05 in**             | —                  |
| Footer text baseline  | y = **7.12 in**             | —                  |
| Whale icon position   | (0.45, 6.85), 0.5 × 0.5 in  | —                  |

> Do **not** use 10″ × 7.5″ (4:3). Lab01 was 4:3 and is the explicit "what we replaced" reference.

---

## 2. Color palette — verbatim from Lab02 XML

All hex values below are taken straight from `<a:srgbClr val="…"/>` in `Lab02.pptx`.

### 2.1 Brand & UI

| Token         | Hex       | python-pptx constant                  | Usage                                                          |
| ------------- | --------- | ------------------------------------- | -------------------------------------------------------------- |
| `BLUE`        | `#1FA8E0` | `RGBColor(0x1F, 0xA8, 0xE0)`          | Primary accent. All content-slide titles, links, headlines, "left-bar accents" on cards. |
| `SLATE`       | `#37465A` | `RGBColor(0x37, 0x46, 0x5A)`          | Dark-slate navy. Numbered circles, table headers, inline bold mono terms. |
| `BODY`        | `#3F3F3F` | `RGBColor(0x3F, 0x3F, 0x3F)`          | Body copy. Never pure black.                                   |
| `MUTED`       | `#868686` | `RGBColor(0x86, 0x86, 0x86)`          | Subtitles, footers, italic helper text, dividers' label text.  |
| `LIGHTBLUE`   | `#CFDBEE` | `RGBColor(0xCF, 0xDB, 0xEE)`          | Subtle outline of the Docker-logo ring on the title slide. **Outline only — not a fill.** |
| `WHITE`       | `#FFFFFF` | `RGBColor(0xFF, 0xFF, 0xFF)`          | Slide background, text on filled shapes, browser-chrome bg.    |
| `CARD_BG`     | `#F4F7FB` | `RGBColor(0xF4, 0xF7, 0xFB)`          | Subtle card / panel fill. Used everywhere a "soft container" is needed (GOAL banner, side panels, meta-info value cells, reflection cards, table-row banding). |
| `RULE_GRAY`   | `#E0E0E0` | `RGBColor(0xE0, 0xE0, 0xE0)`          | Thin horizontal separators (0.5–0.75 pt).                       |
| `FOOTER_GRAY` | `#868686` | `RGBColor(0x86, 0x86, 0x86)` (same as MUTED) | Footer line `CLO835, Fall 2026   N / TOTAL`. 10 pt.       |

### 2.2 Status / semantic

| Token         | Hex       | python-pptx                            | Usage                                                       |
| ------------- | --------- | -------------------------------------- | ----------------------------------------------------------- |
| `GOAL_GREEN`  | `#27AE60` | `RGBColor(0x27, 0xAE, 0x60)`           | GOAL banner left-bar; the green checkmark circle; "Answer"/"Expected" headings. |
| `ALERT_RED`   | `#E74C3C` | `RGBColor(0xE7, 0x4C, 0x3C)`           | "Tear down" headings, "Gotcha" cards' left-bar, "It's gone." callout. |

### 2.3 Step-block / multi-stage gradient

The five-color sequence (light-blue → slate) used to tag steps / pillars / wrap-up boxes.
Pick `STEPS[0]` for the first concept, `STEPS[1]` for the second, etc.

```python
STEPS = [
    RGBColor(0x1F, 0xA8, 0xE0),  # 0 — primary blue
    RGBColor(0x21, 0x96, 0xA0),  # 1 — teal
    RGBColor(0x1F, 0x8F, 0xCD),  # 2 — mid blue
    RGBColor(0x1F, 0x7A, 0xB8),  # 3 — deeper blue
    RGBColor(0x24, 0x66, 0xA0),  # 4 — darker blue
    RGBColor(0x37, 0x46, 0x5A),  # 5 — slate (final / "Verify")
]
```

Convention: when there are 3 or 4 steps, use `STEPS[0]`, `STEPS[1]`, `STEPS[3]`, `STEPS[5]` for visual contrast.

### 2.4 Terminal palette (inside dark code mockups only)

| Token         | Hex       | Usage                                                       |
| ------------- | --------- | ----------------------------------------------------------- |
| `TERMBG`      | `#2A2A2A` | Terminal body background.                                   |
| Title-bar bg  | `#3A3A3A` | Bar at top of terminal (slightly lighter than body).        |
| `TERM_RED`    | `#FF5F56` | Traffic-light dot #1 (close).                               |
| `TERM_YEL`    | `#FFBD2E` | Traffic-light dot #2 (minimize). Also "warning" verdict icon. |
| `TERM_GRN`    | `#27C93F` | Traffic-light dot #3 (maximize). Also `# comments` and successful verdict icon. |
| `TERM_GRAY`   | `#BABABA` | Default terminal text — outputs, tool banners, results.     |
| `TERM_CYAN`   | `#4EC9E0` | All `$ command` lines and any continuation `\` lines.       |
| `TERM_ERR`    | `#F07178` | Error messages (`ERROR …`, `NXDOMAIN`, etc.).               |
| `TERM_ORANGE` | `#FFBD2E` | (Alias of `TERM_YEL`) — used for highlighted output strings like CVE counts. |

> **Convention inside terminals:**
> - `# something` lines → **green** (`TERM_GRN`)
> - `$ cmd …` and continuations → **cyan** (`TERM_CYAN`)
> - tool output → **gray** (`TERM_GRAY`)
> - errors → **red-ish pink** (`TERM_ERR`)

---

## 3. Typography

### 3.1 Two typefaces — never a third

| Role       | Font       | Where                                                              |
| ---------- | ---------- | ------------------------------------------------------------------ |
| `FONT_SANS`| **Calibri**| Everything except code: titles, body, callouts, footer, labels.   |
| `FONT_MONO`| **Consolas**| All code inside terminals, inline `command`-styled inline spans, `GOAL` keyword, `01/02` block numbers, IP addresses / paths / `--flags` written inline. |

`Lab02.pptx` uses these two and only these two (459 Consolas runs, 447 Calibri runs across 18 slides; see `analysis/lab02_xml/ppt/slides/`).

### 3.2 Type scale (point sizes used across the system)

| Use                                                | Size (pt) | Weight | Color   |
| -------------------------------------------------- | --------- | ------ | ------- |
| Cover slide H1 (`CLO835 — Week 3`)                 | **44**    | Bold   | `BLUE`  |
| Cover slide H1 (alt: lab guide multi-line)         | **40**    | Bold   | `BLUE`  |
| Closing slide H1 (`Submit your lab notebook.`)     | **44**    | Bold   | `BLUE`  |
| Closing slide H1 (alt: `Week 03 — wrap-up`)        | **44**    | Bold   | `BLUE`  |
| Section-divider heading                            | **32**    | Bold   | `SLATE` |
| Content-slide title (default)                      | **32**    | Bold   | `BLUE`  |
| Content-slide title (compact decks like Lab 03 Guide) | **30**  | Bold   | `BLUE`  |
| Cover subtitle / lead-in                           | **22**    | Reg    | `BODY`  |
| "Eyebrow" subtitle above title (cover, lab cover)  | **20**    | Bold   | `MUTED` |
| Scenario / The fix heading                         | **18**    | Bold   | `SLATE` |
| In-card "It's gone." callout                       | **18**    | Bold   | `ALERT_RED` |
| "The user is gone." dramatic line                  | **22**    | Bold italic | `SLATE` |
| Numbered-circle digit (objective, takeaway)        | **22**    | Bold   | `WHITE` |
| Numbered-circle digit (step, smaller)              | **18–20** | Bold   | `WHITE` |
| Section heading inside card                        | **15**    | Bold   | `SLATE` |
| Section heading (right-column accent)              | **13**    | Bold   | `BLUE` or `GOAL_GREEN` |
| Body text (large)                                  | **14**    | Reg    | `BODY`  |
| Body text (table / dense card)                     | **12–13** | Reg    | `BODY`  |
| Goal-banner body                                   | **12.5**  | Reg    | `BODY`  |
| "GOAL  " keyword (Consolas mono)                   | **11.5**  | Bold   | `GOAL_GREEN` |
| Italic muted subtitle / footer line                | **10.5–11** | Italic | `MUTED` |
| Footer "CLO835, Fall 2026  N / TOTAL"              | **10**    | Reg    | `FOOTER_GRAY` |
| Terminal body                                      | **9.5–11**| Reg    | per role |
| Terminal title bar                                 | **10**    | Reg    | `TERM_GRAY` |
| Tiny annotation under a layer-box                  | **9**     | Italic | `BLUE`  |

### 3.3 Line spacing

| Context                            | `line_spacing` value |
| ---------------------------------- | -------------------- |
| Titles (tight)                     | **1.05**             |
| Cover subtitle / body big          | **1.3 – 1.4**        |
| Body paragraphs (default)          | **1.35 – 1.4**       |
| Card / panel body                  | **1.3 – 1.35**       |
| Terminal body                      | **1.15 – 1.25**      |
| Generic text helper default        | **1.15**             |

### 3.4 Casing rules

- **Sentence case** for titles. `"What you'll learn this week"` ✓, `"WHAT YOU'LL LEARN THIS WEEK"` ✗.
- **No MONO CAPS** for kicker labels. Use `"The scenario"` / `"The fix"` in Calibri Bold Slate.
  (Lab02 had no `SCENARIO:` mono-caps kickers; an earlier Week 03 draft used them and was
  explicitly walked back — keep them out.)
- **Em dash with spaces** for step subtitles: `"Step 1 — Create the user-defined network"`.
- **Middot `·`** for meta separators: `"CLO835 · Week 3 · ~30 minutes"`.
- **Sentence-final period dropped** in big display lines: `"The user is gone"` is allowed; longer subtitles
  may end with a period.
- **Code identifiers** (`docker rm`, `MYSQL_ROOT_PASSWORD_FILE`, `/var/lib/mysql`, `bridge`) are **inline mono +
  bold + Slate** when called out inside body copy. Same rule inside table cells.

---

## 4. Layout grid

A 16:9 slide is **13.333 in × 7.5 in**. Use the following invariant anchors.

```
 x:  0.55                            6.85 (col gap ≈ 0.10)      12.78
     ┌──────────────────────────────┬──────────────────────────────┐  ← y = 0.40  title row (top)
     │                              │                              │
     │                              │                              │
     │   LEFT COLUMN                │   RIGHT COLUMN               │
     │   (≈ 6.0 in)                 │   (≈ 5.9–6.0 in)             │
     │                              │                              │
     │                              │                              │
     ├──────────────────────────────┴──────────────────────────────┤  ← y = 7.05  rule (0.5 pt RULE_GRAY)
     │ whale 0.45,6.85           CLO835, Fall 2026     N / TOTAL   │
     └──────────────────────────────────────────────────────────────┘  ← y = 7.50
```

- **Title** occupies (0.55, 0.40) → (12.75, 1.20). Always 0.55 in from the left, never centered.
- **First content band** starts at **y = 1.05** for italic muted lead-ins, or **y = 1.20–1.30** for the GOAL banner /
  first text block.
- **Two-column layout**: left col ends at x ≈ 6.55–8.40 depending on whether the right side is a Capture/Reflect panel
  (4.4 in wide, starting at 8.40) or a full right column (5.9 in wide, starting at 6.85–7.0).
- **Three-column lab-step pattern**: left = terminal (≈ 7.6 in wide), right = capture/expected panel (≈ 4.4 in wide
  at x = 8.40).
- **Three-column "comparison cards"**: 3 × ~4.05 in wide, 0.10 in gaps, starting at x = 0.55.
- **Footer guard**: keep all content above **y = 6.70**.

---

## 5. Chrome — present on every slide

### 5.1 Whale + footer (mandatory)

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

- `whale.png` is the small **cyan-outline Docker whale**, extracted from `Lab02.pptx/ppt/media/image2.png`.
- The horizontal rule above the footer is **always 0.5 pt** `RULE_GRAY`.
- Footer textbox is **3.35 in wide** (NOT smaller — earlier versions wrapped on 2-digit page numbers).
- Footer string is exactly `CLO835, Fall 2026     N / TOTAL` (5 spaces, em-style separation).

### 5.2 Title helper (mandatory on every content slide)

```python
def title(slide, text, x=Inches(0.55), y=Inches(0.4),
          w=Inches(12.2), h=Inches(0.8)):
    add_text(slide, x, y, w, h, text, size=32, bold=True, color=BLUE,
             line_spacing=1.05)
```

(Use `size=30` instead of 32 in compact step-by-step decks like `Lab03_Guide.pptx`.)

### 5.3 Cover-slide chrome (different from content slides)

- No top-left blue title — the H1 sits roughly centered vertically (y ≈ 2.4–2.55) on the left half.
- A **Docker logo** sits on the right half (x ≈ 10.4) inside a **light-blue outlined ring** (`LIGHTBLUE`, line
  width 1.5 pt) **larger than the logo** so the logo is centered inside it.
- Below the title: instructor block (`"Instructor: " + "Professor Maziar"` two-tone, plus an italic muted
  third line like `"CLO835 · Week 3 · ~30 minutes"` or `"Seneca Polytechnic · ITAS Program"`).
- Whale + footer are still drawn (page = 1).

---

## 6. Reusable components — the design system

Each component below already exists as a helper function in the four `build_*.py` files.
Treat the function signatures as the canonical contract.

### 6.1 `add_text(slide, x, y, w, h, text, *, font=FONT_SANS, size=14, bold=False, italic=False, color=BODY, align=LEFT, anchor=TOP, line_spacing=1.15)`

The base textbox. All margins set to 0; `word_wrap=True`. Always use this instead of inserting raw
`slide.shapes.add_textbox(...)`.

### 6.2 `add_rich_text(slide, x, y, w, h, runs, *, align=LEFT, anchor=TOP, line_spacing=1.2)`

For mixed-style paragraphs. `runs` is a list of paragraphs, each a list of `(text, kwargs)` tuples.
Use whenever you have to bold/mono **part** of a sentence (e.g., inline `docker rm` inside body copy).

### 6.3 Shapes: `add_rect`, `add_rounded_rect`, `add_oval`, `add_line`

- All shapes default to **no border**, **no shadow** (`shp.shadow.inherit = False`).
- Lines default to `RULE_GRAY` at 0.75 pt.
- Rounded rectangle uses `radius_ratio = 0.05` (small, subtle).
- To draw a dashed border (rare — used for the R/W layer overlay), append a `<a:prstDash val="dash"/>`
  element to the shape's `<a:ln>`:
  ```python
  spPr = rw.line._get_or_add_ln()
  spPr.append(etree.fromstring(
      '<a:prstDash val="dash" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>'))
  ```

### 6.4 **Terminal mockup** — the signature visual

Specification:

| Part            | Detail                                                        |
| --------------- | ------------------------------------------------------------- |
| Body            | `TERMBG` (#2A2A2A) rectangle, full `w × h`                     |
| Title bar       | `#3A3A3A` rectangle across the top, height **0.32 in**         |
| Traffic-light dots | 3 ovals, **0.13 in diameter**, at y = bar_top + 0.10 in, x positions: `x + 0.15`, `x + 0.32`, `x + 0.49`. Fills: red, yellow, green (in that order). |
| Title text      | Calibri **10 pt** `TERM_GRAY`, centered in the title bar (typical: `"bash — docker"`, `"bash — cleanup"`, `"bash — verify"`, `"bash — example"`). |
| Body textbox    | inset `0.18 in` left, body text starts `bar_h + 0.10 in` below the bar top, ends `0.15 in` from the bottom. |
| Code font       | Consolas, **9–11 pt** depending on density (default 11 pt; 9–10 pt for dense slides). |
| Code line spacing | **1.15**.                                                  |
| Empty paragraphs (blank lines) | Allowed and recommended — `[]` in the body runs list inserts one. |

Code-coloring convention (already noted in §2.4): comments = green, commands = cyan, output = gray,
errors = red-pink.

```python
terminal(slide, x, y, w, h, "bash — docker",
         [[("# 1. create the network", TERM_GRN)],
          [("$ docker network create \\", TERM_CYAN)],
          [("    --driver bridge \\", TERM_CYAN)],
          [("    clo835-net", TERM_CYAN)],
          [("3a7b1e9c8d5f...", TERM_GRAY)]],
         font_size=10)
```

### 6.5 **GOAL panel** (lab-step header)

A subtle horizontal banner that introduces each lab step. Pattern:

```
┌─┬──────────────────────────────────────────────────────────────┐
│G│ GOAL   <one-line description of what the student is doing>   │
└─┴──────────────────────────────────────────────────────────────┘
```

- Outer rectangle: `CARD_BG` fill, full width (typically 0.55 → 12.75, height **0.55 in**).
- Left bar: 0.10 in wide overlay rect, fill = `GOAL_GREEN`.
- Text: rich-text with `"GOAL   "` in Consolas **11.5 pt bold GOAL_GREEN**, followed by the description in
  Calibri **12.5 pt BODY**, anchored MIDDLE.
- `y` placement: **1.20** (right under the title) on most content/lab slides.
- For longer goals that need to wrap, use `h = 0.65–0.75 in` instead.

### 6.6 **Capture / Expected / Reflect right-column panel**

Vertical right column used opposite a terminal mockup on lab-step slides. Two variants:

**(a) Capture panel (`Lab03_Guide.pptx` style)** — heading + checklist of items:

```
Capture for screenshot 1            ← 13 pt Bold BLUE heading
✓  Both commands (create + inspect)
✓  IPAM Subnet = 172.28.0.0/16
✓  ...
```

Each row = small green oval (0.20 in) with white `✓` (9 pt bold), then text in 11.5 pt BODY.
Row pitch = **0.65 in**. Start x = 8.40 in, width = 4.4 in.

**(b) Expected / Reflect text panel (`new_Week3.pptx` style)**:

```
Expected                            ← 13 pt Bold GOAL_GREEN
<one-paragraph description, 11.5 pt BODY, 1.35 line-spacing>

Why ___?                            ← 13 pt Bold BLUE (or 12.5 pt for tighter slides)
<rich-text paragraph with inline mono spans>
```

### 6.7 **Step block** (multi-stage tag)

The colored rectangle + body row pattern used to label the parts of a lab.

```
┌────────────┐  Networking — Create clo835-net …
│ Networking │  (12 pt body in slate, single-line-ish, anchor MIDDLE)
└────────────┘
   x=0.55       x=2.65
   w=1.90       w=5.0
   h=0.85
```

- Block: filled rectangle, color from `STEPS[i]`, **0.85 in tall**.
- Block label: Calibri **14 pt bold white**, centered, anchor MIDDLE.
- Body to the right of the block: Calibri **12 pt BODY**, line-spacing 1.35, anchor MIDDLE.
- Vertical pitch between blocks: **1.10 in**.

### 6.8 **Objective / Takeaway grid** (numbered-circle pattern)

2×2 grid of items, each prefixed by a dark slate circle with a big white number.

```
●(1)   Heading in 15 pt Bold SLATE
       Body in 12.5 pt BODY, 1.35 line-spacing, ~4.6 in wide
```

- Circle diameter: **0.75 in** for "objective" big circles; **0.55 in** for "takeaway"; **0.45 in** for "fact rows";
  **0.55 in** for closing-slide "reflect" prompts.
- Circle fill: `SLATE`. Number font: 22 pt bold WHITE, centered MIDDLE-CENTER.
- Variant: **Numbered with `"01"/"02"`** in Consolas (mono) when the surrounding label is mono — e.g., the
  three-column "ways to change code" pattern.
- Variant: **Checkmark instead of number** — circle is still SLATE (or GOAL_GREEN for prereq lists), with a
  white `✓` glyph.

### 6.9 **Section divider** (full-slide chapter break)

Used to introduce a lab inside a lecture deck.

```
              ●(LAB)               ← big slate circle, 1.6 in diameter, centered
                                       white "LAB" in 24 pt bold

      Hands-on: Docker Storage     ← 32 pt bold SLATE centered

  Lose data without a volume —     ← 15 pt italic MUTED centered
   then make it survive with a
              bind mount.

  [ Time | Prereqs | Deliverable ] ← 3 horizontal meta blocks (see §6.10)
```

### 6.10 **Meta info block** (key + value pair)

Two horizontal halves: a colored "label" on the left, a card-bg "value" on the right.

```
┌──────┬─────────────────────┐
│ Time │ ~30 minutes         │   ← Label: 12–13 pt bold WHITE on BLUE
└──────┴─────────────────────┘     Value: 11.5 pt BODY on CARD_BG
```

Used vertically stacked on Slide 2 overviews, or in three side-by-side blocks on the lab section divider.

### 6.11 **Comparison table**

```
┌──────────┬──────────┬──────────┬──────────┐
│          │ Heading1 │ Heading2 │ Heading3 │   ← header row: slate fill, white 12.5 pt bold,
│          │ (slate)  │ (slate)  │ (slate)  │     leftmost header is WHITE bg with SLATE text
├──────────┼──────────┼──────────┼──────────┤
│  Label1  │ <body>   │ <body>   │ <body>   │   ← alternating row banding:
│          │          │          │          │     odd rows = WHITE, even rows = CARD_BG
├──────────┼──────────┼──────────┼──────────┤     (only the body columns get banded; the label
│  Label2  │ <body>   │ <body>   │ <body>   │     column stays WHITE)
└──────────┴──────────┴──────────┴──────────┘
```

- Row height: ~0.42–0.75 in.
- Label column: Calibri 12 pt bold SLATE, left-aligned with 0.10–0.15 in inset.
- Body cells: 11 pt BODY, anchor MIDDLE, left-aligned with 0.15 in inset.
- If a cell value contains code (`docker run …`, `--mount`, `/path/`), switch its font to Consolas at 10.5 pt.

### 6.12 **Left-bar accent card** (the "blue-bar card" motif)

A horizontal card with a 0.10-in-wide colored bar pinned to its left edge. Used for:
- The GOAL banner (left bar = GOAL_GREEN).
- "Your report must include" sidebar (left bar = BLUE).
- "Gotcha" callouts (left bar = ALERT_RED).
- Reflection-answer "Question" cards (left bar = BLUE).
- Troubleshooting error cards (left bar = SLATE).
- Integrity Pledge card (left bar = SLATE).

The bar is always **0.10 in wide**, full height of the card.

### 6.13 **Numbered pillar row** (small, dense)

Used for "what you just did" lists where a step has a small colored numeric circle + 2 short lines.

```
●  Image                                ← circle 0.40 in, color from STEPS[]
   Scan with Scout or Trivy before…       Heading: 11.5 pt bold SLATE
                                          Body:    10  pt BODY, 1.3 line
```

### 6.14 **Architecture mini-diagram**

When showing a small network or container layout:

- Outer host rectangle: WHITE fill, SLATE 1.5 pt outline, label `"Docker host"` 11 pt bold SLATE inside top-left.
- Network rectangle: `CARD_BG` fill, BLUE 1.25 pt outline. Label inside top-left in Consolas 10 pt bold BLUE,
  e.g., `"clo835-net   ·   172.28.0.0/16"`.
- Container boxes: filled rectangles with `STEPS[*]` colors, label in Consolas 11 pt bold WHITE on top,
  second line in 9 pt WHITE.
- Connecting line: solid BLUE, **1.5 pt**.
- "DNS" labels in BLUE bold italic 8 pt directly above/below the line.

### 6.15 **Browser-window mockup** (lab guide style)

For showing UI screens:

- Outer rectangle: WHITE fill, SLATE 1 pt outline.
- Chrome bar at top: `#ECECEC` fill (or use `CARD_BG`), height 0.40 in.
- Three traffic-light dots: 0.13 in each, at left edge of the chrome bar, fills TERM_RED/YEL/GRN.
- URL bar: `http://localhost:8080` in Consolas 10 pt SLATE, anchor MIDDLE.
- Body of the mockup: form fields drawn as small rectangles (CARD_BG or WHITE fills with SLATE outline);
  highlighted (focused) field has a BLUE outline, **1.5 pt** width and CARD_BG fill.

### 6.16 **Verdict pill** (icon + sentence)

Used at the bottom of three-column comparison cards.

```
  ●  Cleanest. Slowest feedback loop.       ← circle 0.55 in, fill = SLATE / TERM_YEL / TERM_GRN
                                              icon: "·", "!", or "✓"
                                              caption: 11.5 pt BODY, 1.3 line-spacing
```

### 6.17 **Bullet paragraphs (square bullet)**

When bullets are needed (rare; prefer numbered circles), use a Calibri filled square `■  ` glyph in
the same `bullet_color` (default SLATE), followed by the body text. **Never** use PowerPoint's default
bullet characters — they don't match the system.

---

## 7. Slide templates — the catalogue

Use these as the starting layouts for new slides. Each maps to a real precedent in `build_*.py`.

| # | Template name              | Anchor file & slide                     | Use for                                                                     |
| - | -------------------------- | --------------------------------------- | --------------------------------------------------------------------------- |
| 1 | **Cover**                  | `build_week3.py` slide 1                | First slide of any deck. Title left, Docker-logo-in-ring right, instructor block bottom-left. |
| 2 | **Lab-cover (alt)**        | `build_lab.py` slide 1, `build_lab_guide.py` slide 1 | Cover for a hands-on or catch-up guide. Eyebrow subtitle ("Hands-on Lab"), two-line H1, italic explanation. |
| 3 | **Objectives 2×2**         | `build_week03.py` slide 2, `build_week3.py` slide 2 | "What you'll learn this week" — 4 numbered objectives in a grid. |
| 4 | **Concept slide (text + diagram)** | `build_week3.py` slide 3        | Concept with three "fact" rows on the left and an architecture mini-diagram on the right. |
| 5 | **Comparison table**       | `build_week3.py` slide 4, slide 10; `build_week03.py` slide 6 | Driver/storage/syntax comparisons. Header row, banded body, rule-of-thumb line below. |
| 6 | **Commands + terminal**    | `build_week3.py` slide 5                | Left = list of `cmd_row` cards in CARD_BG, right = full terminal mockup. |
| 7 | **Concept + gotcha**       | `build_week3.py` slide 6                | Left = concept text + red gotcha card, right = terminal. |
| 8 | **Two model cards**        | `build_week3.py` slide 7                | Two big side-by-side cards comparing models (CNM vs CNI, etc.). |
| 9 | **Layer stack**            | `build_week3.py` slide 8, `build_week03.py` slide 3 | Stack of dark layer-boxes with mono code + italic blue label, plus a dashed R/W overlay. |
| 10| **Scenario / Fix**         | `build_week3.py` slide 9, `build_week03.py` slide 5 | Two-column "the scenario" / "the fix" with 3 small step-block options on the right. |
| 11| **Three-column ways**      | `build_week03.py` slide 7               | Three vertical columns: numeric kicker, dark heading bar, mini terminal, verdict pill. |
| 12| **Lab section divider**    | `build_week03.py` slide 8               | Big centered slate circle + heading + 3 meta blocks. |
| 13| **Lab step**               | `build_week03.py` slide 9–10, `build_lab.py` slide 3–7 | Title + GOAL banner + left terminal + right Expected/Reflect panel. |
| 14| **Lab step (with capture)**| `build_lab_guide.py` slide 4–12         | Title + GOAL banner + left terminal + right Capture-checklist panel. |
| 15| **Side-by-side terminals** | `build_week03.py` slide 11, `build_week3.py` slide 11, `build_lab.py` slide 7 | Two short terminals side by side, with a comparison table beneath. |
| 16| **Troubleshooting list**   | `build_week03.py` slide 12              | 4 stacked left-bar accent cards: mono error → cause → fix. |
| 17| **Four pillars 2×2**       | `build_week3.py` slide 12               | 4 colored numbered pillars, each with a red "Risk" and green "Do" line. |
| 18| **Key takeaways 2×2**      | `build_week03.py` slide 13, `build_week3.py` slide 13 | 4 numbered circles with heading + body, used as the second-to-last slide. |
| 19| **Reflection answer**      | `build_lab_guide.py` slide 13–17        | Question card top, "Answer" paragraphs left, optional proof terminal right. |
| 20| **Closing — light**        | `build_week03.py` slide 14              | Big blue H1 + italic subtitle, 3 step-block "wrap-up" boxes, centered Docker logo. |
| 21| **Closing — submit**       | `build_lab.py` slide 8                  | "Submit your lab notebook." headline + Reflect questions in numbered circles. |
| 22| **Report + Integrity**     | `build_lab_guide.py` slide 18           | Numbered report-contents list on the left, Integrity Pledge card on the right. |

---

## 8. Voice & tone (so the words match the design)

- **Conversational and concrete.** Never say "Configure persistent storage solutions for stateful applications".
  Say "Mount storage from outside the container".
- **Earned punch lines.** A slide's dramatic line ("The user is gone.", "It's gone.", "the row is in the named
  volume now.") arrives at the end of a build-up; it never opens the slide.
- **One verb per step.** "Create the network." "Run MySQL on the network." Not "Network creation: a how-to."
- **Show the failure when teaching a fix.** The Step-5 lab slide intentionally prints
  `ERROR 1049 (42000): Unknown database 'foo'` — this is a feature, not a bug.
- **No exclamation marks** in body copy. Emphasis is carried by colour and weight.
- **Numbers over numerals when small** in body copy: "five deliverables", not "5 deliverables".
  Numerals when they're an identifier ("Layer 5", "Pillar 1", "Step 3").
- **Em dash `—` with spaces** as a thought break; never `--`, never `-`.
- **Title-cased fixed labels**: GOAL, Expected, Capture, Reflect, Reflect, Question, Answer, Proof, Verify,
  Tear down. These are stable across the system — don't invent new ones.

---

## 9. Required assets

Both files live in this directory and **must be present** for any build script to run.

| File              | Source                                                | Use                                |
| ----------------- | ----------------------------------------------------- | ---------------------------------- |
| `whale.png`       | Extracted from `Lab02.pptx/ppt/media/image2.png`      | Bottom-left chrome on every slide. |
| `docker_logo.jpg` | Extracted from `Lab02.pptx/ppt/media/image1.jpg`      | Centered in the light-blue ring on the cover slide; sometimes used centered at the bottom of the closing slide. |

> **Do not replace** the whale with another image, recolor it, or scale it past 0.5 in.
> If a new deck is for a non-Docker topic, replace `docker_logo.jpg` but **keep the whale** —
> it's the course's visual signature.

---

## 10. Python-pptx scaffold

A new deck should be created from one of the four existing `build_*.py` files (don't start from scratch).
The minimum viable skeleton is below — copy this and add slides:

```python
"""<deck description>. Lab02 design language."""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

# ---- Palette (verbatim from this DESIGN_LANGUAGE.md) ----
BLUE        = RGBColor(0x1F, 0xA8, 0xE0)
SLATE       = RGBColor(0x37, 0x46, 0x5A)
BODY        = RGBColor(0x3F, 0x3F, 0x3F)
MUTED       = RGBColor(0x86, 0x86, 0x86)
LIGHTBLUE   = RGBColor(0xCF, 0xDB, 0xEE)
TERMBG      = RGBColor(0x2A, 0x2A, 0x2A)
TERM_RED    = RGBColor(0xFF, 0x5F, 0x56)
TERM_YEL    = RGBColor(0xFF, 0xBD, 0x2E)
TERM_GRN    = RGBColor(0x27, 0xC9, 0x3F)
TERM_GRAY   = RGBColor(0xBA, 0xBA, 0xBA)
TERM_CYAN   = RGBColor(0x4E, 0xC9, 0xE0)
TERM_ERR    = RGBColor(0xF0, 0x71, 0x78)
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
FOOTER_GRAY = RGBColor(0x86, 0x86, 0x86)
RULE_GRAY   = RGBColor(0xE0, 0xE0, 0xE0)
CARD_BG     = RGBColor(0xF4, 0xF7, 0xFB)
GOAL_GREEN  = RGBColor(0x27, 0xAE, 0x60)
ALERT_RED   = RGBColor(0xE7, 0x4C, 0x3C)
STEPS = [
    RGBColor(0x1F, 0xA8, 0xE0), RGBColor(0x21, 0x96, 0xA0),
    RGBColor(0x1F, 0x8F, 0xCD), RGBColor(0x1F, 0x7A, 0xB8),
    RGBColor(0x24, 0x66, 0xA0), RGBColor(0x37, 0x46, 0x5A),
]
FONT_SANS, FONT_MONO = "Calibri", "Consolas"

# ---- Copy helpers from build_week3.py: add_text, add_rich_text,
#      add_rect, add_oval, add_line, terminal, title,
#      whale_and_footer.  They are stable; do not re-implement. ----

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
blank = prs.slide_layouts[6]
TOTAL = <n>   # set to final slide count

# ---- Slide 1: Cover ----
# (use the "Cover" template from §7, row 1)

# ---- Slide 2 … TOTAL: pick templates from §7 ----

prs.save("YourDeck.pptx")
```

---

## 11. Build → preview workflow

```bash
# from project root
.venv/bin/python build_<your_script>.py

# render to PDF (for visual QA)
soffice --headless --convert-to pdf YourDeck.pptx

# render PDF pages to JPGs for slide-by-slide review
pdftoppm -jpeg -r 110 YourDeck.pdf analysis/<deckname>/slide
```

QA loop, ALWAYS:

1. Render to PDF + JPG.
2. Spot-check the cover, one lab-step slide, and the closing slide visually.
3. Look at footer rendering on a slide with a 2-digit `N / TOTAL` — the footer textbox must be wide
   enough that nothing wraps.
4. Look for overlapping shapes (especially right-column panels that hit the footer rule).
5. Fix in the Python script, **never** in PowerPoint directly. The script is the source of truth.

---

## 12. File-naming conventions

| Artifact                          | Convention                                                                  |
| --------------------------------- | --------------------------------------------------------------------------- |
| Build scripts                     | `build_<deck>.py` (e.g., `build_week3.py`, `build_lab_guide.py`)            |
| Output decks                      | `<DescriptiveName>.pptx` (e.g., `Week3_Hands_On_Lab.pptx`, `Lab03_Guide.pptx`) |
| Render byproducts                 | `analysis/<deckname>/slide-NN.jpg` + `<deckname>.pdf`                       |
| Reports                           | `reports/report-YYYY-MM-DD-NN-<short-description>.md` (per project rules)   |

---

## 13. Things that are **not** in the design language (don't reach for them)

These were tried and explicitly walked back. Do not use:

- Mono caps kicker labels (`SCENARIO:`, `THE FIX:`, `LEGACY:`, `MODERN:`).
  Use Calibri Bold Slate sentence case instead.
- Dark navy content panels with white text. Dark backgrounds are reserved for **terminal mockups only**.
- Pure black (`#000000`). Use `BODY` (`#3F3F3F`).
- Yellow / orange highlights for emphasis. Emphasis is `BLUE` or `SLATE`. Yellow is reserved for the warning
  traffic-light dot.
- PowerPoint default bullet glyphs. If bullets are needed, use the `■  ` square in the same color as the text.
- Drop shadows on any shape. Every helper explicitly sets `shp.shadow.inherit = False`.
- More than two typefaces. Calibri + Consolas only.
- 4:3 (10 × 7.5) aspect ratio. Always 16:9.
- Centered titles. Titles are always at x = 0.55.
- Cover slides without the Docker logo in the light-blue ring. Even a guide cover uses this motif.
- Whale-less slides. Even the cover and closing slides have the whale at (0.45, 6.85).

---

## 14. Quick verification checklist (use before declaring a deck "done")

- [ ] Slide size = 13.333 × 7.5 in.
- [ ] Every content slide has a top-left BLUE title at (0.55, 0.40), 30–32 pt bold.
- [ ] Every slide has the whale at (0.45, 6.85) and the footer at the bottom-right.
- [ ] Footer reads exactly `CLO835, Fall 2026     N / TOTAL` with the correct N and TOTAL.
- [ ] Every terminal mockup has the three traffic-light dots in red/yellow/green order, a Consolas title
      in the dark bar, and Consolas body in the right palette (green comments / cyan commands / gray output /
      red errors).
- [ ] All numbered markers are SLATE filled circles with white numbers (or `STEPS[*]` colors for step blocks).
- [ ] GOAL banners use `CARD_BG` fill + `GOAL_GREEN` left bar, with the `"GOAL   "` keyword in Consolas.
- [ ] No text uses any font other than Calibri or Consolas.
- [ ] No drop shadows. No emoji unless absolutely deliberate. No mono caps kickers.
- [ ] All two-digit page numbers render on one line (footer width ≥ 3.35 in).
- [ ] PDF render via `soffice --headless` has no overlapping shapes and no text overflow.

---

*End of spec. If something is ambiguous, the four `build_*.py` files in this directory are the
ground truth — read them.*
