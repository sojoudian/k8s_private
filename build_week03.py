"""Build Week03_lab_style.pptx using the EXACT Lab02 design language.

Palette and typography are pulled straight from Lab02.pptx's XML (see
analysis/lab02_xml/...) so this is verbatim, not approximated.
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from lxml import etree

# === EXACT Lab02 palette (hex from Lab02 XML) ===
BLUE        = RGBColor(0x1F, 0xA8, 0xE0)   # primary accent, titles, whale
SLATE       = RGBColor(0x37, 0x46, 0x5A)   # dark slate navy
BODY        = RGBColor(0x3F, 0x3F, 0x3F)   # body text
MUTED       = RGBColor(0x86, 0x86, 0x86)   # subtitles, footers
LIGHTBLUE   = RGBColor(0xCF, 0xDB, 0xEE)   # subtle accents
TERMBG      = RGBColor(0x2A, 0x2A, 0x2A)   # terminal background
TERM_RED    = RGBColor(0xFF, 0x5F, 0x56)   # traffic light red
TERM_YEL    = RGBColor(0xFF, 0xBD, 0x2E)   # traffic light yellow
TERM_GRN    = RGBColor(0x27, 0xC9, 0x3F)   # traffic light green
TERM_GRAY   = RGBColor(0xBA, 0xBA, 0xBA)   # terminal body text
TERM_ORANGE = RGBColor(0xFF, 0xBD, 0x2E)   # terminal keywords
TERM_CYAN   = RGBColor(0x4E, 0xC9, 0xE0)   # terminal commands
TERM_ERR    = RGBColor(0xF0, 0x71, 0x78)   # terminal errors
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
BLACK       = RGBColor(0x00, 0x00, 0x00)
FOOTER_GRAY = RGBColor(0x86, 0x86, 0x86)
RULE_GRAY   = RGBColor(0xE0, 0xE0, 0xE0)   # subtle horizontal separators
CARD_BG     = RGBColor(0xF4, 0xF7, 0xFB)   # very subtle card background
GOAL_GREEN  = RGBColor(0x27, 0xAE, 0x60)
ALERT_RED   = RGBColor(0xE7, 0x4C, 0x3C)

# Step block gradient palette (from Lab02 slide 5)
STEPS = [
    RGBColor(0x1F, 0xA8, 0xE0),
    RGBColor(0x21, 0x96, 0xA0),
    RGBColor(0x1F, 0x8F, 0xCD),
    RGBColor(0x1F, 0x7A, 0xB8),
    RGBColor(0x24, 0x66, 0xA0),
    RGBColor(0x37, 0x46, 0x5A),
]

FONT_SANS = "Calibri"
FONT_MONO = "Consolas"

# ===== Helpers =====

def add_text(slide, x, y, w, h, text, *, font=FONT_SANS, size=14, bold=False,
             italic=False, color=BODY, align=PP_ALIGN.LEFT,
             anchor=MSO_ANCHOR.TOP, line_spacing=1.15):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.margin_left = Inches(0)
    tf.margin_right = Inches(0)
    tf.margin_top = Inches(0)
    tf.margin_bottom = Inches(0)
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    lines = text.split("\n") if isinstance(text, str) else text
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line_spacing
        r = p.add_run()
        r.text = line
        r.font.name = font
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.italic = italic
        r.font.color.rgb = color
    return tb


def add_rich_text(slide, x, y, w, h, runs, *, align=PP_ALIGN.LEFT,
                  anchor=MSO_ANCHOR.TOP, line_spacing=1.2):
    """runs is a list of (text, kwargs) per paragraph (list-of-lists)."""
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.margin_left = Inches(0)
    tf.margin_right = Inches(0)
    tf.margin_top = Inches(0)
    tf.margin_bottom = Inches(0)
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    for i, para in enumerate(runs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line_spacing
        for text, kw in para:
            r = p.add_run()
            r.text = text
            r.font.name = kw.get("font", FONT_SANS)
            r.font.size = Pt(kw.get("size", 14))
            r.font.bold = kw.get("bold", False)
            r.font.italic = kw.get("italic", False)
            r.font.color.rgb = kw.get("color", BODY)
    return tb


def add_rect(slide, x, y, w, h, fill, line=None):
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(0.75)
    shp.shadow.inherit = False
    return shp


def add_rounded_rect(slide, x, y, w, h, fill, line=None, radius_ratio=0.05):
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    # Reduce the corner radius
    shp.adjustments[0] = radius_ratio
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(0.75)
    shp.shadow.inherit = False
    return shp


def add_oval(slide, x, y, w, h, fill, line=None):
    shp = slide.shapes.add_shape(MSO_SHAPE.OVAL, x, y, w, h)
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(0.75)
    shp.shadow.inherit = False
    return shp


def add_line(slide, x1, y1, x2, y2, color=RULE_GRAY, width=0.75):
    line = slide.shapes.add_connector(1, x1, y1, x2, y2)
    line.line.color.rgb = color
    line.line.width = Pt(width)
    return line


def text_in_shape(shape, text, *, font=FONT_SANS, size=14, bold=False,
                  italic=False, color=WHITE, align=PP_ALIGN.CENTER,
                  anchor=MSO_ANCHOR.MIDDLE):
    tf = shape.text_frame
    tf.margin_left = Inches(0.08)
    tf.margin_right = Inches(0.08)
    tf.margin_top = Inches(0.04)
    tf.margin_bottom = Inches(0.04)
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    lines = text.split("\n") if isinstance(text, str) else text
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        r = p.add_run()
        r.text = line
        r.font.name = font
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.italic = italic
        r.font.color.rgb = color


def whale_and_footer(slide, page_num, total=14):
    # Whale icon, bottom-left (~0.55" from left & bottom; about 0.55" wide)
    slide.shapes.add_picture("whale.png", Inches(0.45), Inches(6.85),
                             width=Inches(0.5), height=Inches(0.5))
    # Subtle horizontal separator above footer
    add_line(slide, Inches(0.5), Inches(7.05),
             Inches(12.83), Inches(7.05), color=RULE_GRAY, width=0.5)
    # Footer right: page number — wider box so 2-digit page numbers don't wrap
    add_text(slide, Inches(9.5), Inches(7.12), Inches(3.35), Inches(0.3),
             f"CLO835, Fall 2026     {page_num} / {total}",
             size=10, color=FOOTER_GRAY, align=PP_ALIGN.RIGHT)


def title(slide, text, x=Inches(0.55), y=Inches(0.4),
          w=Inches(12.2), h=Inches(0.8)):
    add_text(slide, x, y, w, h, text, size=32, bold=True, color=BLUE,
             line_spacing=1.05)


def bullet_paragraphs(slide, x, y, w, h, items, *, size=13, color=BODY,
                      bullet_color=SLATE, line_spacing=1.4):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.margin_left = Inches(0)
    tf.margin_right = Inches(0)
    tf.margin_top = Inches(0)
    tf.margin_bottom = Inches(0)
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.line_spacing = line_spacing
        p.space_after = Pt(6)
        # bullet square
        r0 = p.add_run()
        r0.text = "■  "
        r0.font.name = FONT_SANS
        r0.font.size = Pt(size)
        r0.font.color.rgb = bullet_color
        # body
        r1 = p.add_run()
        r1.text = item
        r1.font.name = FONT_SANS
        r1.font.size = Pt(size)
        r1.font.color.rgb = color
    return tb


def terminal(slide, x, y, w, h, title_text, body_runs, *, font_size=11):
    """body_runs: list of (text, color) tuples per paragraph (paras list of lists)."""
    # Main body
    panel = add_rect(slide, x, y, w, h, TERMBG)
    # Title bar
    bar_h = Inches(0.32)
    add_rect(slide, x, y, w, bar_h, RGBColor(0x3A, 0x3A, 0x3A))
    # Traffic lights
    dot_d = Inches(0.13)
    dot_y = y + Inches(0.10)
    add_oval(slide, x + Inches(0.15), dot_y, dot_d, dot_d, TERM_RED)
    add_oval(slide, x + Inches(0.32), dot_y, dot_d, dot_d, TERM_YEL)
    add_oval(slide, x + Inches(0.49), dot_y, dot_d, dot_d, TERM_GRN)
    # Title text in bar
    add_text(slide, x, y + Inches(0.04), w, bar_h, title_text,
             font=FONT_SANS, size=10, color=TERM_GRAY,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    # Body (rich runs)
    tb = slide.shapes.add_textbox(x + Inches(0.18), y + bar_h + Inches(0.10),
                                  w - Inches(0.32), h - bar_h - Inches(0.15))
    tf = tb.text_frame
    tf.margin_left = Inches(0)
    tf.margin_right = Inches(0)
    tf.margin_top = Inches(0)
    tf.margin_bottom = Inches(0)
    tf.word_wrap = True
    for i, para in enumerate(body_runs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.line_spacing = 1.15
        if not para:
            r = p.add_run()
            r.text = " "
            r.font.name = FONT_MONO
            r.font.size = Pt(font_size)
            continue
        for text, color in para:
            r = p.add_run()
            r.text = text
            r.font.name = FONT_MONO
            r.font.size = Pt(font_size)
            r.font.color.rgb = color


# ===== Setup =====

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank = prs.slide_layouts[6]  # 6 == Blank


# ============================================================
# SLIDE 1 - Title slide
# ============================================================
s = prs.slides.add_slide(blank)
# Tiny eyebrow for course code is NOT in Lab02 style; Lab02 title slide
# just has "CLO835 — Lab 2" big blue + small subtitle + circled Docker logo.
add_text(s, Inches(0.7), Inches(2.5), Inches(8.5), Inches(1.0),
         "CLO835 — Week 3", size=44, bold=True, color=BLUE,
         line_spacing=1.0)
add_text(s, Inches(0.7), Inches(3.5), Inches(7.8), Inches(1.4),
         "Docker Layers, Copy-on-Write and Storage",
         size=20, color=BODY, line_spacing=1.3)
# Light-blue circle behind Docker logo, then logo on top
logo_cx = Inches(10.4); logo_cy = Inches(3.75)
ring_r = Inches(2.0)
ring = add_oval(s, logo_cx - ring_r, logo_cy - ring_r,
                ring_r * 2, ring_r * 2, WHITE, line=LIGHTBLUE)
ring.line.width = Pt(1.5)
s.shapes.add_picture("docker_logo.jpg",
                     logo_cx - Inches(1.4), logo_cy - Inches(1.1),
                     width=Inches(2.8), height=Inches(2.2))
# Instructor line at bottom-left
add_rich_text(s, Inches(0.7), Inches(6.5), Inches(7), Inches(0.7),
              [[("Instructor: ", {"size": 12, "color": MUTED}),
                ("Professor Maziar", {"size": 12, "bold": True, "color": SLATE})],
               [("Seneca Polytechnic · ITAS Program",
                 {"size": 10.5, "italic": True, "color": MUTED})]])
# Whale icon and footer
s.shapes.add_picture("whale.png", Inches(0.45), Inches(6.85),
                     width=Inches(0.5), height=Inches(0.5))
add_text(s, Inches(9.5), Inches(7.12), Inches(3.35), Inches(0.3),
         "CLO835, Fall 2026     1 / 14", size=10, color=FOOTER_GRAY,
         align=PP_ALIGN.RIGHT)


# ============================================================
# SLIDE 2 - Learning Objectives (4 items)
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "What you'll learn this week")
add_text(s, Inches(0.55), Inches(1.05), Inches(12), Inches(0.4),
         "Four ideas this week. The first three are concepts; the fourth is the lab where they come together.",
         size=14, italic=True, color=MUTED)

# 2x2 grid of objectives — each item is a slate-filled circle with white number + heading + body
def objective(x, y, num, heading, body):
    d = Inches(0.75)
    add_oval(s, x, y, d, d, SLATE)
    add_text(s, x, y, d, d, str(num), size=22, bold=True, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, x + Inches(1.05), y + Inches(0.0), Inches(4.6), Inches(0.4),
             heading, size=15, bold=True, color=SLATE)
    add_text(s, x + Inches(1.05), y + Inches(0.45), Inches(4.6), Inches(1.5),
             body, size=12.5, color=BODY, line_spacing=1.35)

objective(Inches(0.55), Inches(2.0), 1, "Docker image layers",
          "How images are built as a stack of read-only layers and why "
          "layering matters for caching and image size.")
objective(Inches(7.0), Inches(2.0), 2, "The container R/W layer",
          "Where runtime changes live, and how copy-on-write isolates "
          "each container from its base image.")
objective(Inches(0.55), Inches(4.55), 3, "Volumes vs. bind mounts",
          "Two ways to persist data outside the container's writable "
          "layer, and when to use each.")
objective(Inches(7.0), Inches(4.55), 4, "Hands-on lab",
          "Run MySQL with and without a volume — observe data loss, "
          "then fix it.")

whale_and_footer(s, 2)


# ============================================================
# SLIDE 3 - What is a Docker layer?
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "What is a Docker layer?")
# Left column: intro text + 3 benefit pills
add_text(s, Inches(0.55), Inches(1.3), Inches(6.0), Inches(1.5),
         "A layer is the filesystem change produced by a single "
         "instruction in a Dockerfile.",
         size=14, color=BODY, line_spacing=1.4)
add_rich_text(s, Inches(0.55), Inches(2.4), Inches(6.0), Inches(1.5),
              [[("Each ", {"size": 14, "color": BODY}),
                ("FROM", {"size": 14, "bold": True, "color": BLUE, "font": FONT_MONO}),
                (", ", {"size": 14, "color": BODY}),
                ("RUN", {"size": 14, "bold": True, "color": BLUE, "font": FONT_MONO}),
                (", ", {"size": 14, "color": BODY}),
                ("COPY", {"size": 14, "bold": True, "color": BLUE, "font": FONT_MONO}),
                (", or ", {"size": 14, "color": BODY}),
                ("ADD", {"size": 14, "bold": True, "color": BLUE, "font": FONT_MONO}),
                (" adds a new read-only layer on top of the previous one. The image is the stack.",
                 {"size": 14, "color": BODY})]],
              line_spacing=1.4)

# 3 benefit rows: dark slate filled circle with white check + heading + body
def benefit(x, y, head, body):
    d = Inches(0.55)
    add_oval(s, x, y, d, d, SLATE)
    add_text(s, x, y, d, d, "✓", size=18, bold=True, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, x + Inches(0.75), y - Inches(0.02), Inches(5.0), Inches(0.4),
             head, size=13, bold=True, color=SLATE)
    add_text(s, x + Inches(0.75), y + Inches(0.30), Inches(5.5), Inches(0.6),
             body, size=11.5, color=BODY, line_spacing=1.3)

benefit(Inches(0.55), Inches(4.20), "Cached builds",
        "Unchanged layers are reused — rebuilds skip work that didn't change.")
benefit(Inches(0.55), Inches(5.10), "Smaller transfers",
        "Pulling an image only downloads layers you don't already have.")
benefit(Inches(0.55), Inches(6.00), "Immutability",
        "Layers are read-only. Runtime changes go to a separate writable layer.")

# Right column: stack of layer boxes — top to bottom = Layer 5 → Layer 1, then R/W
def layer_box(y, code, label):
    add_rect(s, Inches(7.0), Inches(y), Inches(5.8), Inches(0.62), TERMBG)
    add_text(s, Inches(7.15), Inches(y + 0.07), Inches(5.0), Inches(0.32),
             code, font=FONT_MONO, size=12.5, color=TERM_GRAY)
    add_text(s, Inches(7.15), Inches(y + 0.36), Inches(5.0), Inches(0.22),
             label, font=FONT_SANS, size=9, italic=True, color=BLUE)

layer_box(1.30, 'CMD ["python", "app.py"]', "Layer 5 · entrypoint")
layer_box(2.00, "COPY . /app",               "Layer 4 · application code")
layer_box(2.70, "RUN pip install -r requirements.txt", "Layer 3 · dependencies")
layer_box(3.40, "WORKDIR /app",              "Layer 2 · working dir")
layer_box(4.10, "FROM python:3.12-slim",     "Layer 1 · base image")

# Dashed R/W layer box on top of the stack
rw = add_rect(s, Inches(7.0), Inches(5.05), Inches(5.8), Inches(0.6), WHITE)
rw.line.color.rgb = BLUE
rw.line.width = Pt(1.5)
# dashed via XML
spPr = rw.line._get_or_add_ln()
spPr.append(etree.fromstring(
    '<a:prstDash val="dash" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>'))
add_text(s, Inches(7.0), Inches(5.05), Inches(5.8), Inches(0.6),
         "Container R/W layer (added when container starts)",
         size=11.5, bold=True, color=BLUE,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

whale_and_footer(s, 3)


# ============================================================
# SLIDE 4 - Copy-on-Write
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "Copy-on-Write: how containers stay isolated")

# Left: 3 numbered steps
def step(x, y, n, head, body):
    d = Inches(0.65)
    add_oval(s, x, y, d, d, SLATE)
    add_text(s, x, y, d, d, str(n), size=20, bold=True, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, x + Inches(0.9), y - Inches(0.05), Inches(5.0), Inches(0.4),
             head, size=14, bold=True, color=SLATE)
    add_text(s, x + Inches(0.9), y + Inches(0.32), Inches(5.5), Inches(1.2),
             body, size=12, color=BODY, line_spacing=1.35)

step(Inches(0.55), Inches(1.45), 1, "Read from a lower layer",
     "If a process only reads /etc/config, Docker serves the file "
     "directly from the image layer. No copy is made.")
step(Inches(0.55), Inches(3.25), 2, "Write triggers a copy",
     "On first write, the file is copied up into the container's R/W "
     "layer. Subsequent writes modify the copy, not the original.")
step(Inches(0.55), Inches(5.05), 3, "Lower layers stay clean",
     "The image is never mutated. Every container gets its own writable "
     "layer on top of the same shared read-only base.")

# Right: light Q&A card (Lab02 style — no dark content panels, only dark terminals)
add_rect(s, Inches(7.5), Inches(1.45), Inches(5.3), Inches(4.6), CARD_BG)
# left blue bar accent (Lab02 motif from agenda dividers / step blocks)
add_rect(s, Inches(7.5), Inches(1.45), Inches(0.10), Inches(4.6), BLUE)
add_text(s, Inches(7.75), Inches(1.65), Inches(5.0), Inches(0.35),
         "Key question", size=11, bold=True, color=BLUE)
add_text(s, Inches(7.75), Inches(2.05), Inches(4.95), Inches(1.1),
         "What happens to data in the R/W layer when the container is deleted?",
         size=15, bold=True, color=SLATE, line_spacing=1.3)
add_line(s, Inches(7.75), Inches(3.40), Inches(12.6), Inches(3.40),
         color=RULE_GRAY, width=0.75)
add_text(s, Inches(7.75), Inches(3.55), Inches(5.0), Inches(0.35),
         "Answer", size=11, bold=True, color=BLUE)
add_text(s, Inches(7.75), Inches(3.95), Inches(5.0), Inches(0.45),
         "It's gone.", size=18, bold=True, color=ALERT_RED)
add_rich_text(s, Inches(7.75), Inches(4.55), Inches(4.95), Inches(1.6),
              [[("The R/W layer is bound to the container's lifecycle. ",
                 {"size": 11.5, "color": BODY}),
                ("docker rm",
                 {"size": 11.5, "color": SLATE, "font": FONT_MONO, "bold": True}),
                (" deletes the layer and every change it held. The "
                 "underlying image layers are untouched — and useless for "
                 "recovering your data.",
                 {"size": 11.5, "color": BODY})]],
              line_spacing=1.35)

whale_and_footer(s, 4)


# ============================================================
# SLIDE 5 - Why this matters: ephemeral by default
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "The problem: containers are ephemeral by default")

# Left: Scenario (Lab02 style — bold dark slate inline heading, no mono caps kicker)
add_text(s, Inches(0.55), Inches(1.40), Inches(5.8), Inches(0.5),
         "The scenario", size=18, bold=True, color=SLATE)
add_rich_text(s, Inches(0.55), Inches(2.05), Inches(5.8), Inches(2.2),
              [[("You run MySQL in a container. A user signs up. ",
                 {"size": 13, "color": BODY}),
                ("The row is written to ",
                 {"size": 13, "color": BODY}),
                ("/var/lib/mysql",
                 {"size": 13, "color": SLATE, "font": FONT_MONO, "bold": True}),
                (" — which lives in the container's R/W layer.",
                 {"size": 13, "color": BODY})],
               [("", {"size": 6})],
               [("The container crashes. You run ",
                 {"size": 13, "color": BODY}),
                ("docker rm",
                 {"size": 13, "color": SLATE, "font": FONT_MONO, "bold": True}),
                (" to clean up. You restart MySQL.",
                 {"size": 13, "color": BODY})]],
              line_spacing=1.4)
add_text(s, Inches(0.55), Inches(4.7), Inches(5.8), Inches(0.6),
         "The user is gone.",
         size=22, bold=True, italic=True, color=SLATE)

# Right: The Fix (Lab02 style)
add_text(s, Inches(7.0), Inches(1.40), Inches(5.8), Inches(0.5),
         "The fix", size=18, bold=True, color=SLATE)
add_text(s, Inches(7.0), Inches(2.05), Inches(5.8), Inches(0.5),
         "Mount storage from outside the container",
         size=15, bold=True, color=BLUE)
add_text(s, Inches(7.0), Inches(2.55), Inches(5.8), Inches(0.5),
         "Docker gives you three options to keep data alive past "
         "container deletion:",
         size=12, color=MUTED, line_spacing=1.35)

# 3 step blocks
def fix_block(y, color, head, body):
    add_rect(s, Inches(7.0), Inches(y), Inches(2.2), Inches(0.85), color)
    add_text(s, Inches(7.0), Inches(y), Inches(2.2), Inches(0.85), head,
             size=15, bold=True, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(9.4), Inches(y + 0.08), Inches(3.5), Inches(0.7),
             body, size=11.5, color=BODY, line_spacing=1.35)

fix_block(3.40, STEPS[0], "Volumes",   "Managed by Docker. Best for most cases.")
fix_block(4.40, STEPS[1], "Bind mounts", "Map a host path directly. Good for dev.")
fix_block(5.40, STEPS[2], "tmpfs",       "In-memory only. Sensitive or scratch data.")

whale_and_footer(s, 5)


# ============================================================
# SLIDE 6 - Storage comparison table
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "Volume vs. bind mount vs. tmpfs")

rows = [
    ["",                 "Volume",                                       "Bind mount",                              "tmpfs"],
    ["Location",         "Docker-managed area\n(/var/lib/docker/volumes)", "Any host path you choose",              "Host RAM only"],
    ["Created with",     "docker volume create",                          "docker run -v /host:/ctr",               "--tmpfs /ctr/path"],
    ["Survives delete?", "Yes",                                           "Yes",                                    "No"],
    ["Survives reboot?", "Yes",                                           "Yes",                                    "No"],
    ["Portable hosts?",  "Yes (volume drivers)",                          "No (tied to host path)",                 "No"],
    ["Best for",         "Production data\n(databases, app state)",       "Live-editing source during dev",         "Secrets, caches, scratch"],
]

n_rows = len(rows)
n_cols = 4
table_left = Inches(0.55)
table_top = Inches(1.4)
table_w = Inches(12.2)
table_h = Inches(4.7)
col_widths = [Inches(2.0), Inches(3.4), Inches(3.4), Inches(3.4)]
row_h = table_h / n_rows

# Header
x = table_left
for c, cell in enumerate(rows[0]):
    add_rect(s, x, table_top, col_widths[c], row_h, SLATE if c > 0 else WHITE)
    add_text(s, x, table_top, col_widths[c], row_h, cell,
             size=12.5, bold=True,
             color=WHITE if c > 0 else SLATE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    x += col_widths[c]

# Body
for r, row in enumerate(rows[1:], start=1):
    x = table_left
    y = table_top + row_h * r
    band = (r % 2 == 0)
    for c, cell in enumerate(row):
        bg = CARD_BG if (band and c > 0) else WHITE
        add_rect(s, x, y, col_widths[c], row_h, bg)
        if c == 0:
            add_text(s, x + Inches(0.1), y, col_widths[c] - Inches(0.1), row_h, cell,
                     size=12, bold=True, color=SLATE,
                     align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)
        else:
            font = FONT_MONO if "docker" in cell or "--" in cell else FONT_SANS
            add_text(s, x + Inches(0.15), y, col_widths[c] - Inches(0.15), row_h, cell,
                     size=10.5 if font == FONT_MONO else 11.5,
                     color=BODY, font=font,
                     align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE,
                     line_spacing=1.2)
        x += col_widths[c]

# Bottom rule of thumb
add_rich_text(s, Inches(0.55), Inches(6.30), Inches(12.2), Inches(0.5),
              [[("Rule of thumb: ",
                 {"size": 13, "bold": True, "color": SLATE}),
                ("use volumes in production · use bind mounts while "
                 "developing on your laptop · use tmpfs for secrets you "
                 "never want on disk.",
                 {"size": 13, "italic": True, "color": MUTED})]])

whale_and_footer(s, 6)


# ============================================================
# SLIDE 7 - Three ways to change code (3 columns)
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "Three ways to change code in a container")

def way_col(x, w, n, color, head, term_lines, verdict_color, verdict_icon, verdict):
    # Number block strip
    add_rect(s, x, Inches(1.35), w, Inches(0.45), color)
    add_text(s, x, Inches(1.35), w, Inches(0.45), f"0{n}",
             size=18, bold=True, color=WHITE, font=FONT_MONO,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    # Title bar (dark)
    add_rect(s, x, Inches(1.80), w, Inches(0.55), SLATE)
    add_text(s, x, Inches(1.80), w, Inches(0.55), head,
             size=14, bold=True, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    # Terminal mockup (mini, no title bar)
    term_h = Inches(2.5)
    add_rect(s, x, Inches(2.55), w, term_h, TERMBG)
    # body text
    tb = s.shapes.add_textbox(x + Inches(0.18), Inches(2.65),
                              w - Inches(0.3), term_h - Inches(0.2))
    tf = tb.text_frame
    tf.margin_left = Inches(0); tf.margin_right = Inches(0)
    tf.margin_top = Inches(0); tf.margin_bottom = Inches(0)
    tf.word_wrap = True
    for i, (txt, col) in enumerate(term_lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.line_spacing = 1.25
        r = p.add_run()
        r.text = txt
        r.font.name = FONT_MONO
        r.font.size = Pt(10.5)
        r.font.color.rgb = col
    # Verdict card
    add_rect(s, x, Inches(5.30), w, Inches(0.95), CARD_BG)
    add_oval(s, x + Inches(0.18), Inches(5.50), Inches(0.55), Inches(0.55),
             verdict_color)
    add_text(s, x + Inches(0.18), Inches(5.50), Inches(0.55), Inches(0.55),
             verdict_icon, size=14, bold=True, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, x + Inches(0.90), Inches(5.55), w - Inches(1.05), Inches(0.7),
             verdict, size=11.5, color=BODY, line_spacing=1.3)

col_w = Inches(4.05)
gap = Inches(0.10)
x1 = Inches(0.55)
x2 = x1 + col_w + gap
x3 = x2 + col_w + gap

way_col(x1, col_w, 1, STEPS[3], "Rebuild the image",
        [("$ edit code locally", TERM_GRAY),
         ("$ docker build .", TERM_CYAN),
         ("  → rebuilds the image", TERM_GRN),
         ("$ docker run", TERM_CYAN),
         ("  → start a fresh container", TERM_GRN)],
        SLATE, "·", "Cleanest. Slowest feedback loop.")

way_col(x2, col_w, 2, STEPS[1], "Edit inside the container",
        [("$ docker exec -it <ctr> bash", TERM_CYAN),
         ("$ apt install vim", TERM_CYAN),
         ("  → install an editor", TERM_GRN),
         ("$ vim file", TERM_CYAN),
         ("  → lost on docker rm", TERM_ERR)],
        TERM_YEL, "!", "Quick hack. Changes disappear with the container.")

way_col(x3, col_w, 3, STEPS[0], "Bind-mount your source",
        [("$ docker run \\", TERM_CYAN),
         ("    -v $(pwd):/app …", TERM_CYAN),
         ("$ edit locally with your IDE", TERM_GRAY),
         ("  → container sees changes", TERM_GRN),
         ("    instantly", TERM_GRN)],
        TERM_GRN, "✓", "Best for active development.")

whale_and_footer(s, 7)


# ============================================================
# SLIDE 8 - Lab 02 section divider
# ============================================================
s = prs.slides.add_slide(blank)
# Lab02 section-divider motif: centered big slate circle with white number/text,
# heading below, italic subtitle, meta info row at bottom
d = Inches(1.6)
cx = Inches(13.333/2) - d/2
add_oval(s, cx, Inches(1.7), d, d, SLATE)
add_text(s, cx, Inches(1.7), d, d, "LAB", size=24, bold=True, color=WHITE,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(0.55), Inches(3.55), Inches(12.2), Inches(0.7),
         "Hands-on: Docker Storage", size=32, bold=True, color=SLATE,
         align=PP_ALIGN.CENTER)
add_text(s, Inches(0.55), Inches(4.25), Inches(12.2), Inches(0.5),
         "Lose data without a volume — then make it survive with a bind mount.",
         size=15, italic=True, color=MUTED, align=PP_ALIGN.CENTER)

# Meta row at bottom — 3 step blocks with key/value pairs
def meta_box(x, label, value):
    add_rect(s, x, Inches(5.35), Inches(3.65), Inches(0.55), BLUE)
    add_text(s, x, Inches(5.35), Inches(3.65), Inches(0.55), label,
             size=13, bold=True, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_rect(s, x, Inches(5.90), Inches(3.65), Inches(0.85), CARD_BG)
    add_text(s, x + Inches(0.2), Inches(5.95), Inches(3.45), Inches(0.75),
             value, size=11.5, color=BODY, line_spacing=1.3,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

meta_box(Inches(0.55), "Time",         "~30 minutes")
meta_box(Inches(4.85), "Prereqs",      "Docker installed; terminal access")
meta_box(Inches(9.15), "Deliverable",  "Lab notebook with commands, outputs, answers")

whale_and_footer(s, 8)


# ============================================================
# SLIDE 9 - Lab Part A
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "Part A — Run MySQL with no persistent storage")

# Goal panel
add_rect(s, Inches(0.55), Inches(1.30), Inches(12.2), Inches(0.55), CARD_BG)
add_rect(s, Inches(0.55), Inches(1.30), Inches(0.10), Inches(0.55), GOAL_GREEN)
add_rich_text(s, Inches(0.85), Inches(1.30), Inches(11.6), Inches(0.55),
              [[("GOAL   ",
                 {"size": 11.5, "bold": True, "color": GOAL_GREEN,
                  "font": FONT_MONO}),
                ("Create a database, write a row, delete the container, "
                 "and watch the data disappear.",
                 {"size": 12.5, "color": BODY})]],
              anchor=MSO_ANCHOR.MIDDLE)

# Terminal
terminal(s, Inches(0.55), Inches(2.05), Inches(8.4), Inches(4.4),
         "bash — docker",
         [[("# 1. Start a MySQL container (no volume, no mount)", TERM_GRN)],
          [("$ docker run --name mysql-db -d \\", TERM_CYAN)],
          [("    -e MYSQL_ROOT_PASSWORD=db_clo835 mysql:8", TERM_CYAN)],
          [],
          [("# 2. Open a shell inside the running container", TERM_GRN)],
          [("$ docker exec -it mysql-db bash", TERM_CYAN)],
          [],
          [("# 3. Create a DB and insert one row", TERM_GRN)],
          [("mysql> CREATE DATABASE foo;", TERM_GRAY)],
          [("mysql> USE foo;", TERM_GRAY)],
          [("mysql> CREATE TABLE pets (name VARCHAR(20),", TERM_GRAY)],
          [("    owner VARCHAR(20), species VARCHAR(20));", TERM_GRAY)],
          [("mysql> INSERT INTO pets VALUES", TERM_GRAY)],
          [("    ('Puffball','Diane','hamster');", TERM_GRAY)],
          [],
          [("# 4. Stop and remove the container", TERM_GRN)],
          [("$ docker stop mysql-db && docker rm mysql-db", TERM_CYAN)]],
         font_size=10.5)

# Right: Reflect panel — Lab02 style: small Calibri bold heading, no mono caps
add_text(s, Inches(9.20), Inches(2.05), Inches(3.6), Inches(0.4),
         "Reflect", size=13, bold=True, color=BLUE)
add_text(s, Inches(9.20), Inches(2.50), Inches(3.6), Inches(2.2),
         "After step 4, you re-run the same command from step 1.",
         size=13, bold=True, color=SLATE, line_spacing=1.35)
add_rich_text(s, Inches(9.20), Inches(3.40), Inches(3.6), Inches(2.5),
              [[("Where is the ", {"size": 12.5, "color": BODY}),
                ("pets", {"size": 12.5, "font": FONT_MONO,
                         "bold": True, "color": SLATE}),
                (" table?", {"size": 12.5, "color": BODY})],
               [("", {"size": 6})],
               [("Why?", {"size": 12.5, "color": BODY})],
               [("", {"size": 6})],
               [("Write your answer in your lab notebook before moving "
                 "to Part B.",
                 {"size": 11, "italic": True, "color": MUTED})]],
              line_spacing=1.4)

whale_and_footer(s, 9)


# ============================================================
# SLIDE 10 - Lab Part B
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "Part B — Now add a bind mount")

# Goal panel
add_rect(s, Inches(0.55), Inches(1.30), Inches(12.2), Inches(0.55), CARD_BG)
add_rect(s, Inches(0.55), Inches(1.30), Inches(0.10), Inches(0.55), GOAL_GREEN)
add_rich_text(s, Inches(0.85), Inches(1.30), Inches(11.6), Inches(0.55),
              [[("GOAL   ",
                 {"size": 11.5, "bold": True, "color": GOAL_GREEN,
                  "font": FONT_MONO}),
                ("Repeat Part A, but map /opt/data on the host to MySQL's "
                 "data directory. Prove the row survives.",
                 {"size": 12.5, "color": BODY})]],
              anchor=MSO_ANCHOR.MIDDLE)

# Terminal
terminal(s, Inches(0.55), Inches(2.05), Inches(8.4), Inches(4.7),
         "bash — docker",
         [[("# 1. Prepare the host directory", TERM_GRN)],
          [("$ mkdir -p /opt/data", TERM_CYAN)],
          [],
          [("# 2. Run MySQL with a bind mount", TERM_GRN)],
          [("$ docker run --name mysql-db -d \\", TERM_CYAN)],
          [("    -e MYSQL_ROOT_PASSWORD=db_clo835 \\", TERM_CYAN)],
          [("    -v /opt/data:/var/lib/mysql \\", TERM_CYAN)],
          [("    mysql:8", TERM_CYAN)],
          [],
          [("# 3. Insert a row (same SQL as Part A)", TERM_GRN)],
          [("$ docker exec -it mysql-db mysql -uroot -pdb_clo835", TERM_CYAN)],
          [],
          [("# 4. Destroy the container", TERM_GRN)],
          [("$ docker stop mysql-db && docker rm mysql-db", TERM_CYAN)],
          [],
          [("# 5. Start a BRAND-NEW container, same mount, same password", TERM_GRN)],
          [("$ docker run --name mysql-db -d \\", TERM_CYAN)],
          [("    -v /opt/data:/var/lib/mysql mysql:8", TERM_CYAN)],
          [],
          [("# 6. Confirm the row survives", TERM_GRN)],
          [('$ docker exec mysql-db mysql -uroot -pdb_clo835 \\', TERM_CYAN)],
          [('    -e "USE foo; SELECT * FROM pets;"', TERM_CYAN)]],
         font_size=9.5)

# Right: Expected output + Reflect (Lab02 style)
add_text(s, Inches(9.20), Inches(2.05), Inches(3.6), Inches(0.4),
         "Expected", size=13, bold=True, color=GOAL_GREEN)
add_text(s, Inches(9.20), Inches(2.50), Inches(3.6), Inches(0.3),
         "Step 6 should print:",
         size=11.5, color=BODY)
# Mini terminal for the table
add_rect(s, Inches(9.20), Inches(2.85), Inches(3.6), Inches(1.30), TERMBG)
expected = ("+----------+-------+---------+\n"
            "| name     | owner | species |\n"
            "+----------+-------+---------+\n"
            "| Puffball | Diane | hamster |\n"
            "+----------+-------+---------+")
add_text(s, Inches(9.32), Inches(2.92), Inches(3.4), Inches(1.18),
         expected, font=FONT_MONO, size=9, color=TERM_GRAY,
         line_spacing=1.1)

add_text(s, Inches(9.20), Inches(4.45), Inches(3.6), Inches(0.4),
         "Reflect", size=13, bold=True, color=BLUE)
add_rich_text(s, Inches(9.20), Inches(4.85), Inches(3.6), Inches(1.6),
              [[("Where on your host does the data actually live? Run ",
                 {"size": 11, "color": BODY}),
                ("ls /opt/data",
                 {"size": 11, "font": FONT_MONO, "bold": True, "color": SLATE}),
                (" and look.", {"size": 11, "color": BODY})]],
              line_spacing=1.4)

whale_and_footer(s, 10)


# ============================================================
# SLIDE 11 - Lab Part C: --mount
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "Part C — The modern --mount syntax")

# Two side-by-side terminals
add_rich_text(s, Inches(0.55), Inches(1.30), Inches(6.0), Inches(0.35),
              [[("Legacy:  ", {"size": 14, "bold": True, "color": SLATE}),
                ("-v", {"size": 14, "bold": True, "color": SLATE, "font": FONT_MONO})]])
terminal(s, Inches(0.55), Inches(1.70), Inches(6.0), Inches(2.4),
         "bash — legacy",
         [[("$ docker run --name mysql-db -d \\", TERM_CYAN)],
          [("    -e MYSQL_ROOT_PASSWORD=db_clo835 \\", TERM_CYAN)],
          [("    -v /opt/data:/var/lib/mysql \\", TERM_CYAN)],
          [("    mysql:8", TERM_CYAN)]],
         font_size=11)

add_rich_text(s, Inches(6.85), Inches(1.30), Inches(6.0), Inches(0.35),
              [[("Modern:  ", {"size": 14, "bold": True, "color": BLUE}),
                ("--mount", {"size": 14, "bold": True, "color": BLUE, "font": FONT_MONO})]])
terminal(s, Inches(6.85), Inches(1.70), Inches(6.0), Inches(2.4),
         "bash — modern",
         [[("$ docker run --name mysql-db -d \\", TERM_CYAN)],
          [("    -e MYSQL_ROOT_PASSWORD=db_clo835 \\", TERM_CYAN)],
          [("    --mount type=bind,source=/opt/data,target=/var/lib/mysql \\", TERM_CYAN)],
          [("    mysql:8", TERM_CYAN)]],
         font_size=11)

# Comparison table below
add_text(s, Inches(0.55), Inches(4.30), Inches(12.2), Inches(0.3),
         "How they differ", size=14, bold=True, color=SLATE)

rows = [
    ["",                "-v",                          "--mount"],
    ["Verbosity",       "Short, quick to type",        "Explicit key=value form"],
    ["Mount types",     "bind, volume",                "bind, volume, tmpfs"],
    ["Host path missing?","Silently created",          "Fails fast with a clear error"],
    ["Recommended for", "Quick demos",                 "Scripts, Compose files, production"],
]
table_left = Inches(0.55); table_top = Inches(4.70)
col_widths = [Inches(3.4), Inches(4.4), Inches(4.4)]
row_h = Inches(0.42)
x = table_left
for c, cell in enumerate(rows[0]):
    add_rect(s, x, table_top, col_widths[c], row_h,
             SLATE if c > 0 else WHITE)
    fnt = FONT_MONO if c > 0 else FONT_SANS
    add_text(s, x, table_top, col_widths[c], row_h, cell,
             size=12, bold=True, font=fnt,
             color=WHITE if c > 0 else SLATE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    x += col_widths[c]
for r, row in enumerate(rows[1:], start=1):
    x = table_left
    y = table_top + row_h * r
    band = (r % 2 == 0)
    for c, cell in enumerate(row):
        bg = CARD_BG if (band and c > 0) else WHITE
        add_rect(s, x, y, col_widths[c], row_h, bg)
        if c == 0:
            add_text(s, x + Inches(0.15), y, col_widths[c] - Inches(0.15), row_h, cell,
                     size=11.5, bold=True, color=SLATE,
                     align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)
        else:
            add_text(s, x + Inches(0.15), y, col_widths[c] - Inches(0.15), row_h, cell,
                     size=11, color=BODY,
                     align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)
        x += col_widths[c]

whale_and_footer(s, 11)


# ============================================================
# SLIDE 12 - Troubleshooting
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "Troubleshooting common errors")

errors = [
    ("Bind for 0.0.0.0:3306 failed: port is already allocated",
     "Another MySQL (host or container) is already on port 3306.",
     "docker ps  →  stop the conflicting container, or publish on a "
     "different host port with -p 3307:3306"),
    ("permission denied while trying to connect to /var/run/docker.sock",
     "Your user isn't in the docker group.",
     "sudo usermod -aG docker $USER  →  log out and back in"),
    ("Access denied for user 'root'@'localhost'",
     "Password in new container doesn't match the password used when "
     "/opt/data was first initialised.",
     "Reuse the original password, or delete /opt/data and start fresh."),
    ("docker: Error response from daemon: invalid mount config",
     "Typo in --mount, usually missing space or extra `=`.",
     "Correct form: --mount type=bind,source=/host,target=/ctr"),
]

y0 = 1.30
for i, (err, cause, fix) in enumerate(errors):
    y = Inches(y0 + i * 1.28)
    add_rect(s, Inches(0.55), y, Inches(12.2), Inches(1.18), CARD_BG)
    add_rect(s, Inches(0.55), y, Inches(0.10), Inches(1.18), SLATE)
    add_text(s, Inches(0.85), y + Inches(0.08), Inches(11.7), Inches(0.3),
             err, font=FONT_MONO, size=11, bold=True, color=SLATE)
    add_rich_text(s, Inches(0.85), y + Inches(0.42),
                  Inches(11.7), Inches(0.35),
                  [[("Cause:  ",
                     {"size": 11.5, "bold": True, "color": SLATE}),
                    (cause, {"size": 11.5, "color": BODY})]])
    add_rich_text(s, Inches(0.85), y + Inches(0.78),
                  Inches(11.7), Inches(0.35),
                  [[("Fix:  ",
                     {"size": 11.5, "bold": True, "color": TERM_GRN}),
                    (fix, {"size": 11.5, "color": BODY})]])

whale_and_footer(s, 12)


# ============================================================
# SLIDE 13 - Key takeaways
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "Key takeaways")

takeaways = [
    ("Images are stacks of read-only layers.",
     "Each Dockerfile instruction creates one. Caching, sharing, "
     "and immutability all flow from this."),
    ("Containers add a thin R/W layer on top.",
     "Copy-on-write means writes don't touch the image — but the "
     "R/W layer dies with the container."),
    ("Anything you care about lives outside the container.",
     "Use volumes (managed) or bind mounts (host paths) so data "
     "survives docker rm."),
    ("Prefer --mount over -v in new code.",
     "It's explicit, supports all mount types, and fails loudly "
     "when the host path is wrong."),
]

def takeaway(x, y, n, head, body):
    d = Inches(0.70)
    add_oval(s, x, y, d, d, SLATE)
    add_text(s, x, y, d, d, f"0{n}", size=18, bold=True, color=WHITE,
             font=FONT_MONO, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, x + Inches(1.0), y, Inches(4.8), Inches(0.5),
             head, size=14, bold=True, color=SLATE)
    add_text(s, x + Inches(1.0), y + Inches(0.42), Inches(4.8), Inches(1.4),
             body, size=12, color=BODY, line_spacing=1.35)

takeaway(Inches(0.55), Inches(1.45), 1, takeaways[0][0], takeaways[0][1])
takeaway(Inches(7.0),  Inches(1.45), 2, takeaways[1][0], takeaways[1][1])
takeaway(Inches(0.55), Inches(4.20), 3, takeaways[2][0], takeaways[2][1])
takeaway(Inches(7.0),  Inches(4.20), 4, takeaways[3][0], takeaways[3][1])

whale_and_footer(s, 13)


# ============================================================
# SLIDE 14 - Closing (Lab02 wrap-up style: LIGHT)
# ============================================================
s = prs.slides.add_slide(blank)
add_text(s, Inches(0.55), Inches(0.95), Inches(12), Inches(0.8),
         "Week 03 — wrap-up", size=44, bold=True, color=BLUE,
         line_spacing=1.0)
add_text(s, Inches(0.55), Inches(1.95), Inches(12), Inches(0.5),
         "From an empty image to data that survives docker rm.",
         size=16, italic=True, color=MUTED)

# Three step-blocks (Lab02 wrap-up motif)
def wrap_box(x, color, head, items):
    add_rect(s, x, Inches(2.85), Inches(3.85), Inches(0.55), color)
    add_text(s, x, Inches(2.85), Inches(3.85), Inches(0.55), head,
             size=15, bold=True, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_rect(s, x, Inches(3.40), Inches(3.85), Inches(1.6), CARD_BG)
    add_text(s, x, Inches(3.55), Inches(3.85), Inches(1.4),
             items, size=12, color=BODY, line_spacing=1.5,
             align=PP_ALIGN.CENTER)

wrap_box(Inches(0.55), STEPS[0], "Learned",
         "Image layers\nCopy-on-write\nR/W layer lifecycle")
wrap_box(Inches(4.74), STEPS[2], "Practised",
         "Lost data without a mount\nKept data with a bind mount\n-v vs. --mount")
wrap_box(Inches(8.93), STEPS[3], "Shipped",
         "MySQL container\nVolume-backed data\nReproducible from any host")

# Italic next-up line and centered Docker logo
add_text(s, Inches(0.55), Inches(5.40), Inches(12.2), Inches(0.4),
         "Next: orchestrate these images on Kubernetes (EKS).",
         size=15, italic=True, color=SLATE, align=PP_ALIGN.CENTER)
s.shapes.add_picture("docker_logo.jpg",
                     Inches(13.333/2) - Inches(0.85), Inches(5.85),
                     width=Inches(1.7), height=Inches(1.0))

whale_and_footer(s, 14)


# ===== Save =====
out = "Week03_lab_style.pptx"
prs.save(out)
print(f"wrote {out}")
