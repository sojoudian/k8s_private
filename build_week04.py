"""Week04_lab_style_v13.pptx — Lab02 DESIGN ONLY applied to Week4.pptx.

Original slide text is preserved VERBATIM. No invented subtitles, no
rephrased bullets, no added GOAL banners or definition cards. Diagrams
built collaboratively earlier (slides 12, 15, 16, 20, 32, 34) are kept
because those are design, not content.
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from lxml import etree

# === Lab02 palette ===
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
    RGBColor(0x1F, 0xA8, 0xE0),
    RGBColor(0x21, 0x96, 0xA0),
    RGBColor(0x1F, 0x8F, 0xCD),
    RGBColor(0x1F, 0x7A, 0xB8),
    RGBColor(0x24, 0x66, 0xA0),
    RGBColor(0x37, 0x46, 0x5A),
]

FONT_SANS = "Calibri"
FONT_MONO = "Consolas"

K8S_LOGO    = "Week04/Kubernetes_logo_without_workmark.svg.png"
DOCKER_LOGO = "Week04/Docker_Logo.png"
WHALE       = "whale.png"

VERSION     = "v13"
TOTAL       = 38

# Shape vocabulary fills (for slide 12 + slide 20 diagrams)
DIAMOND_FILL  = BLUE
CIRCLE_FILL   = STEPS[1]
PENTAGON_FILL = STEPS[2]
TRIANGLE_FILL = STEPS[3]


# ===== Helpers =====

def add_text(slide, x, y, w, h, text, *, font=FONT_SANS, size=14, bold=False,
             italic=False, color=BODY, align=PP_ALIGN.LEFT,
             anchor=MSO_ANCHOR.TOP, line_spacing=1.15):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.margin_left = Inches(0); tf.margin_right = Inches(0)
    tf.margin_top = Inches(0); tf.margin_bottom = Inches(0)
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
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.margin_left = Inches(0); tf.margin_right = Inches(0)
    tf.margin_top = Inches(0); tf.margin_bottom = Inches(0)
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


def add_rect(slide, x, y, w, h, fill, line=None, line_width=0.75):
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line is None: shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(line_width)
    shp.shadow.inherit = False
    return shp


def add_rounded_rect(slide, x, y, w, h, fill, line=None, line_width=0.75,
                     radius_ratio=0.06):
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    shp.adjustments[0] = radius_ratio
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line is None: shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(line_width)
    shp.shadow.inherit = False
    return shp


def add_oval(slide, x, y, w, h, fill, line=None, line_width=0.75):
    shp = slide.shapes.add_shape(MSO_SHAPE.OVAL, x, y, w, h)
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line is None: shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(line_width)
    shp.shadow.inherit = False
    return shp


def add_hex(slide, x, y, w, h, fill, line=None, line_width=0.75):
    shp = slide.shapes.add_shape(MSO_SHAPE.HEXAGON, x, y, w, h)
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line is None: shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(line_width)
    shp.shadow.inherit = False
    return shp


def add_triangle(slide, x, y, w, h, fill, line=None, line_width=0.75):
    shp = slide.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE, x, y, w, h)
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line is None: shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(line_width)
    shp.shadow.inherit = False
    return shp


def add_pentagon(slide, x, y, w, h, fill, line=None, line_width=0.75):
    shp = slide.shapes.add_shape(MSO_SHAPE.REGULAR_PENTAGON, x, y, w, h)
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line is None: shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(line_width)
    shp.shadow.inherit = False
    return shp


def add_diamond(slide, x, y, w, h, fill, line=None, line_width=0.75):
    shp = slide.shapes.add_shape(MSO_SHAPE.DIAMOND, x, y, w, h)
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line is None: shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(line_width)
    shp.shadow.inherit = False
    return shp


def add_line(slide, x1, y1, x2, y2, color=RULE_GRAY, width=0.75):
    line = slide.shapes.add_connector(1, x1, y1, x2, y2)
    line.line.color.rgb = color
    line.line.width = Pt(width)
    return line


def add_dashed_line(slide, x1, y1, x2, y2, color=SLATE, width=0.75,
                    dash="dash"):
    line = slide.shapes.add_connector(1, x1, y1, x2, y2)
    line.line.color.rgb = color
    line.line.width = Pt(width)
    ln = line.line._get_or_add_ln()
    ln.append(etree.fromstring(
        f'<a:prstDash val="{dash}" '
        f'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>'))
    return line


def add_arrow(slide, x1, y1, x2, y2, color=SLATE, width=1.5):
    line = slide.shapes.add_connector(1, x1, y1, x2, y2)
    line.line.color.rgb = color
    line.line.width = Pt(width)
    ln = line.line._get_or_add_ln()
    ln.append(etree.fromstring(
        '<a:tailEnd type="triangle" w="med" len="med" '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>'))
    return line


def add_doublearrow(slide, x1, y1, x2, y2, color=SLATE, width=1.5):
    line = slide.shapes.add_connector(1, x1, y1, x2, y2)
    line.line.color.rgb = color
    line.line.width = Pt(width)
    ln = line.line._get_or_add_ln()
    ns = 'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
    ln.append(etree.fromstring(
        f'<a:headEnd type="triangle" w="med" len="med" {ns}/>'))
    ln.append(etree.fromstring(
        f'<a:tailEnd type="triangle" w="med" len="med" {ns}/>'))
    return line


def whale_and_footer(slide, page_num, total):
    slide.shapes.add_picture(WHALE, Inches(0.45), Inches(6.85),
                             width=Inches(0.5), height=Inches(0.5))
    add_line(slide, Inches(0.5), Inches(7.05),
             Inches(12.83), Inches(7.05), color=RULE_GRAY, width=0.5)
    add_text(slide, Inches(9.5), Inches(7.12), Inches(3.35), Inches(0.3),
             f"CLO835, Fall 2026     {page_num} / {total}",
             size=10, color=FOOTER_GRAY, align=PP_ALIGN.RIGHT)


def title(slide, text, y=0.40, size=32):
    add_text(slide, Inches(0.55), Inches(y), Inches(12.2), Inches(0.8),
             text, size=size, bold=True, color=BLUE, line_spacing=1.05)


def bullet_list(slide, y_start, items, *, size=14, bullet_color=BLUE,
                line_spacing=1.5, max_w=12.0, x=0.55):
    """Simple bullet list — small filled square bullet + text. Returns
    the y position of the bottom of the last line."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y_start),
                                  Inches(max_w), Inches(7.5 - y_start - 0.85))
    tf = tb.text_frame
    tf.margin_left = Inches(0); tf.margin_right = Inches(0)
    tf.margin_top = Inches(0); tf.margin_bottom = Inches(0)
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.line_spacing = line_spacing
        p.space_after = Pt(4)
        r0 = p.add_run()
        r0.text = "■  "
        r0.font.name = FONT_SANS; r0.font.size = Pt(size)
        r0.font.color.rgb = bullet_color
        r1 = p.add_run()
        r1.text = item
        r1.font.name = FONT_SANS; r1.font.size = Pt(size)
        r1.font.color.rgb = BODY


def terminal(slide, x, y, w, h, title_text, body_runs, *, font_size=11):
    add_rect(slide, x, y, w, h, TERMBG)
    bar_h = Inches(0.32)
    add_rect(slide, x, y, w, bar_h, RGBColor(0x3A, 0x3A, 0x3A))
    dot_d = Inches(0.13)
    dot_y = y + Inches(0.10)
    add_oval(slide, x + Inches(0.15), dot_y, dot_d, dot_d, TERM_RED)
    add_oval(slide, x + Inches(0.32), dot_y, dot_d, dot_d, TERM_YEL)
    add_oval(slide, x + Inches(0.49), dot_y, dot_d, dot_d, TERM_GRN)
    add_text(slide, x, y + Inches(0.04), w, bar_h, title_text,
             font=FONT_SANS, size=10, color=TERM_GRAY,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    tb = slide.shapes.add_textbox(x + Inches(0.18), y + bar_h + Inches(0.10),
                                  w - Inches(0.32), h - bar_h - Inches(0.15))
    tf = tb.text_frame
    tf.margin_left = Inches(0); tf.margin_right = Inches(0)
    tf.margin_top = Inches(0); tf.margin_bottom = Inches(0)
    tf.word_wrap = True
    for i, para in enumerate(body_runs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.line_spacing = 1.15
        if not para:
            r = p.add_run(); r.text = " "
            r.font.name = FONT_MONO; r.font.size = Pt(font_size)
            continue
        for text, color in para:
            r = p.add_run(); r.text = text
            r.font.name = FONT_MONO; r.font.size = Pt(font_size)
            r.font.color.rgb = color


# ===== Setup =====
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank = prs.slide_layouts[6]


def new_slide():
    return prs.slides.add_slide(blank)


# ============================================================
# SLIDE 1 — Cover
# ============================================================
s = new_slide()
add_text(s, Inches(0.7), Inches(2.6), Inches(8.5), Inches(1.6),
         "Introduction to Kubernetes",
         size=44, bold=True, color=BLUE, line_spacing=1.05)
add_text(s, Inches(0.7), Inches(4.2), Inches(8.5), Inches(0.6),
         "Week 4", size=22, color=SLATE)
# K8s logo in light-blue ring (decoration only)
logo_cx = Inches(10.6); logo_cy = Inches(3.75); ring_r = Inches(1.8)
ring = add_oval(s, logo_cx - ring_r, logo_cy - ring_r,
                ring_r * 2, ring_r * 2, WHITE, line=LIGHTBLUE,
                line_width=1.5)
s.shapes.add_picture(K8S_LOGO,
                     logo_cx - Inches(1.25), logo_cy - Inches(1.25),
                     width=Inches(2.5), height=Inches(2.5))
s.shapes.add_picture(WHALE, Inches(0.45), Inches(6.85),
                     width=Inches(0.5), height=Inches(0.5))
add_text(s, Inches(9.5), Inches(7.12), Inches(3.35), Inches(0.3),
         f"CLO835, Fall 2026     1 / {TOTAL}",
         size=10, color=FOOTER_GRAY, align=PP_ALIGN.RIGHT)


# ============================================================
# SLIDE 2 — Agenda  (title only)
# ============================================================
s = new_slide()
title(s, "Agenda")
whale_and_footer(s, 2, TOTAL)


# ============================================================
# SLIDE 3 — Course Outline  (title only)
# ============================================================
s = new_slide()
title(s, "Course Outline")
whale_and_footer(s, 3, TOTAL)


# ============================================================
# SLIDE 4 — The Need in Containers Orchestration Tool
# ============================================================
s = new_slide()
title(s, "The Need in Containers Orchestration Tool")
add_text(s, Inches(0.55), Inches(1.35), Inches(12.2), Inches(0.45),
         "Containers take care of packaging, running and sharing application images",
         size=15, color=BODY)
add_text(s, Inches(0.55), Inches(2.00), Inches(12.2), Inches(0.45),
         "The topics below are not covered by containerization:",
         size=15, color=BODY)
bullet_list(s, 2.65, [
    "Application components synchronization (web, app, db, messaging .. or 1000s of components in case of Google applications and services)",
    "Application components capacity scaling",
    "Underlying host capacity scaling",
    "Support of high availability",
    "Support of application SDLC",
], size=14)
whale_and_footer(s, 4, TOTAL)


# ============================================================
# SLIDE 5 — Container Orchestration  (title only)
# ============================================================
s = new_slide()
title(s, "Container Orchestration")
whale_and_footer(s, 5, TOTAL)


# ============================================================
# SLIDE 6 — Container Orchestration Technologies  (title only)
# ============================================================
s = new_slide()
title(s, "Container Orchestration Technologies")
whale_and_footer(s, 6, TOTAL)


# ============================================================
# SLIDE 7 — What is K8s?
# ============================================================
s = new_slide()
title(s, "What is K8s?")
bullet_list(s, 1.55, [
    "Kubernetes is a container management/Orchestration system",
    "It runs and manages containerized applications on a cluster",
], size=16)
whale_and_footer(s, 7, TOTAL)


# ============================================================
# SLIDE 8 — Main Advantages of using K8s  (title only)
# ============================================================
s = new_slide()
title(s, "Main Advantages of using K8s")
whale_and_footer(s, 8, TOTAL)


# ============================================================
# SLIDE 9 — From the Developers Perspective  (title only)
# ============================================================
s = new_slide()
title(s, "From the Developers Perspective")
whale_and_footer(s, 9, TOTAL)


# ============================================================
# SLIDE 10 — From the Operations Perspective  (title only)
# ============================================================
s = new_slide()
title(s, "From the Operations Perspective")
whale_and_footer(s, 10, TOTAL)


# ============================================================
# SLIDE 11 — Other Things That K8s Can Do
# ============================================================
s = new_slide()
title(s, "Other Things That K8s Can Do")
bullet_list(s, 1.55, [
    "Basic autoscaling",
    "Blue/green deployment, canary deployment",
    "Long running services, but also batch (one-off) jobs",
    "Overcommit our cluster and evict low-priority jobs",
    "Run services with stateful data (databases etc.)",
    "Fine-grained access control defining what can be done by whom on which resources",
    "Integrating third party services (service catalog)",
    "Automating complex tasks (operators)",
], size=13, line_spacing=1.4)
whale_and_footer(s, 11, TOTAL)


# ============================================================
# SLIDE 12 — K8s Architecture from 10,000 Feet  (DIAGRAM)
# ============================================================
s = new_slide()
title(s, "K8s Architecture from 10,000 Feet")

# Developer
dev_x = Inches(0.70); dev_y = Inches(2.0)
add_oval(s, dev_x, dev_y, Inches(0.85), Inches(0.85), SLATE)
add_text(s, dev_x, dev_y, Inches(0.85), Inches(0.85), "DEV",
         size=12, bold=True, color=WHITE,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, dev_x - Inches(0.20), dev_y + Inches(0.95), Inches(1.25),
         Inches(0.3), "Developer", size=11, bold=True, color=SLATE,
         align=PP_ALIGN.CENTER)

# App descriptor card (3 rows: diamond / circle / pentagon+triangle)
desc_x = Inches(2.20); desc_y = Inches(1.75); desc_w = Inches(2.10)
desc_h = Inches(3.50)
add_rect(s, desc_x, desc_y, desc_w, desc_h, CARD_BG, line=SLATE,
         line_width=1.2)
add_text(s, desc_x, desc_y + Inches(0.10), desc_w, Inches(0.30),
         "App descriptor", size=11, bold=True, color=SLATE,
         align=PP_ALIGN.CENTER)
tile_h = Inches(1.05); tile_w = Inches(1.30)
tile_x = desc_x + Inches(0.60)


def _descriptor_row(row_y, mult, label, draw_shapes):
    add_text(s, desc_x + Inches(0.10), row_y + Inches(0.35),
             Inches(0.40), Inches(0.30), mult,
             size=12, bold=True, color=SLATE, font=FONT_MONO,
             anchor=MSO_ANCHOR.MIDDLE)
    add_rect(s, tile_x, row_y, tile_w, tile_h,
             WHITE, line=SLATE, line_width=0.75)
    draw_shapes(row_y)
    add_text(s, tile_x, row_y + tile_h - Inches(0.34),
             tile_w, Inches(0.30), label,
             size=11, bold=True, color=SLATE, font=FONT_MONO,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


def _r1(ry):
    add_diamond(s, tile_x + Inches(0.40), ry + Inches(0.08),
                Inches(0.55), Inches(0.55), DIAMOND_FILL,
                line=SLATE, line_width=0.75)
_descriptor_row(desc_y + Inches(0.45), "1×", "service", _r1)


def _r2(ry):
    add_oval(s, tile_x + Inches(0.40), ry + Inches(0.08),
             Inches(0.55), Inches(0.55), CIRCLE_FILL,
             line=SLATE, line_width=0.75)
_descriptor_row(desc_y + Inches(1.55), "5×", "pods", _r2)


def _r3(ry):
    add_pentagon(s, tile_x + Inches(0.18), ry + Inches(0.10),
                 Inches(0.52), Inches(0.52), PENTAGON_FILL,
                 line=SLATE, line_width=0.75)
    add_triangle(s, tile_x + Inches(0.65), ry + Inches(0.12),
                 Inches(0.52), Inches(0.52), TRIANGLE_FILL,
                 line=SLATE, line_width=0.75)
_descriptor_row(desc_y + Inches(2.65), "2×", "sidecars", _r3)

# Arrow dev → descriptor
add_arrow(s, dev_x + Inches(0.85), dev_y + Inches(0.42),
          desc_x, dev_y + Inches(0.42), color=SLATE, width=1.8)

# K8s master box
mst_x = Inches(5.10); mst_y = Inches(2.85); mst_w = Inches(2.40)
mst_h = Inches(1.50)
add_rect(s, mst_x, mst_y, mst_w, mst_h, BLUE)
add_text(s, mst_x, mst_y, mst_w, mst_h, "Kubernetes\nmaster",
         size=15, bold=True, color=WHITE,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
         line_spacing=1.15)

# Arrow descriptor → master
add_arrow(s, desc_x + desc_w, mst_y + mst_h / 2,
          mst_x, mst_y + mst_h / 2, color=SLATE, width=1.8)

# Worker nodes cloud
cloud_x = Inches(8.20); cloud_y = Inches(1.55); cloud_w = Inches(4.60)
cloud_h = Inches(4.40)
add_rounded_rect(s, cloud_x, cloud_y, cloud_w, cloud_h, CARD_BG,
                 line=BLUE, line_width=1.5, radius_ratio=0.15)
add_text(s, cloud_x, cloud_y + Inches(0.10), cloud_w, Inches(0.32),
         "Worker nodes", size=10.5, bold=True, color=BLUE,
         align=PP_ALIGN.CENTER)

# 6 mini node tiles with varied shapes (matching slide 12 v5)
node_w = Inches(1.20); node_h = Inches(1.40)


def _shape(kind, x, y, w, h, color):
    if kind == "diamond":
        add_diamond(s, x, y, w, h, color, line=SLATE, line_width=0.6)
    elif kind == "circle":
        add_oval(s, x, y, w, h, color, line=SLATE, line_width=0.6)
    elif kind == "pentagon":
        add_pentagon(s, x, y, w, h, color, line=SLATE, line_width=0.6)
    elif kind == "triangle":
        add_triangle(s, x, y, w, h, color, line=SLATE, line_width=0.6)


tiles = [
    [("diamond", DIAMOND_FILL,  0.10, 0.15, 0.40, 0.40),
     ("circle",  CIRCLE_FILL,   0.65, 0.18, 0.35, 0.35)],
    [("pentagon", PENTAGON_FILL, 0.10, 0.15, 0.42, 0.42),
     ("triangle", TRIANGLE_FILL, 0.60, 0.30, 0.40, 0.40)],
    [("diamond",  DIAMOND_FILL,  0.08, 0.10, 0.35, 0.35),
     ("circle",   CIRCLE_FILL,   0.50, 0.10, 0.32, 0.32),
     ("triangle", TRIANGLE_FILL, 0.80, 0.50, 0.35, 0.35)],
    [("circle", CIRCLE_FILL, 0.35, 0.25, 0.50, 0.50)],
    [("circle",   CIRCLE_FILL,   0.10, 0.15, 0.32, 0.32),
     ("pentagon", PENTAGON_FILL, 0.50, 0.10, 0.42, 0.42),
     ("triangle", TRIANGLE_FILL, 0.30, 0.55, 0.40, 0.40)],
    [("circle", CIRCLE_FILL, 0.35, 0.25, 0.50, 0.50)],
]
for i in range(6):
    col = i % 3; row = i // 3
    nx = cloud_x + Inches(0.30) + (node_w + Inches(0.20)) * col
    ny = cloud_y + Inches(0.65) + (node_h + Inches(0.20)) * row
    add_rect(s, nx, ny, node_w, node_h, WHITE, line=SLATE, line_width=1)
    for kind, color, dx, dy, sw, sh in tiles[i]:
        _shape(kind, nx + Inches(dx), ny + Inches(dy),
               Inches(sw), Inches(sh), color)
    add_text(s, nx, ny + node_h - Inches(0.32), node_w, Inches(0.28),
             f"node-{i+1}", size=9, color=MUTED,
             font=FONT_MONO, align=PP_ALIGN.CENTER)

# Arrow master → cloud
add_arrow(s, mst_x + mst_w, mst_y + mst_h / 2,
          cloud_x, mst_y + mst_h / 2, color=SLATE, width=1.8)

whale_and_footer(s, 12, TOTAL)


# ============================================================
# SLIDE 13 — K8s Architecture
# ============================================================
s = new_slide()
title(s, "K8s Architecture")
bullet_list(s, 1.55, [
    "Master Nodes – Control plane",
    "Worker Nodes (or Nodes) - Data plane",
], size=18)
whale_and_footer(s, 13, TOTAL)


# ============================================================
# SLIDE 14 — K8s Components
# ============================================================
s = new_slide()
title(s, "K8s Components")
bullet_list(s, 1.55, [
    "API Server – Front end to K8s. Everything talks to this",
    "etcd: - Distributed reliable key value store to manage cluster. Multiple nodes and master info is stored in a distributed manner. Ensures logs are implemented",
    "Scheduler  - Distributing work or containers across multiple nodes. Looks for newly created containers and assign them to nodes",
    "Controller – Brains behind. Noticiing and responding when nodes or containers goes down. Responsible to bring up containers.",
    "Container runtime – Underlying s.w that is used to run containers",
    "Kubelet – Agent running on each node on cluster",
], size=12.5, line_spacing=1.4)
whale_and_footer(s, 14, TOTAL)


# ============================================================
# SLIDE 15 — K8s Components – What lies where?  (DIAGRAM)
# ============================================================
s = new_slide()
title(s, "K8s Components – What lies where?")

# Overlay Network bar
add_rect(s, Inches(0.55), Inches(1.50), Inches(12.2),
         Inches(0.40), BLUE)
add_text(s, Inches(0.55), Inches(1.50), Inches(12.2), Inches(0.40),
         "Overlay Network",
         size=12, bold=True, color=WHITE,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# Master column
mx = Inches(0.55); m_w = Inches(2.30)
mh = Inches(4.40); my = Inches(2.05)
add_rect(s, mx, my, m_w, mh, SLATE)
for i, lbl in enumerate(["API\nServer", "Scheduler", "Controller\nManager", "etcd"]):
    add_rect(s, mx + Inches(0.20), my + Inches(0.25 + i * 1.00),
             m_w - Inches(0.40), Inches(0.85),
             RGBColor(0x55, 0x6F, 0x88))
    add_text(s, mx + Inches(0.20), my + Inches(0.25 + i * 1.00),
             m_w - Inches(0.40), Inches(0.85), lbl,
             size=11, bold=True, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
             line_spacing=1.1)
add_text(s, mx, my + mh + Inches(0.05), m_w, Inches(0.28),
         "Master", size=11, bold=True, color=SLATE,
         align=PP_ALIGN.CENTER)

# 3 worker columns
worker_w = Inches(3.10); worker_gap = Inches(0.15)
worker_y = Inches(2.05); worker_h = Inches(4.40)
for n in range(3):
    wx_ = Inches(3.10) + (worker_w + worker_gap) * n
    add_rect(s, wx_, worker_y, worker_w, worker_h, CARD_BG, line=SLATE,
             line_width=0.75)
    for c in range(4):
        cx_ = wx_ + Inches(0.15 + c * 0.65)
        add_rect(s, cx_, worker_y + Inches(0.20), Inches(0.55),
                 Inches(0.55), STEPS[c % 4])
        add_text(s, cx_, worker_y + Inches(0.20), Inches(0.55),
                 Inches(0.55), f"C{c+1}", size=9, bold=True, color=WHITE,
                 font=FONT_MONO,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        cx_center = cx_ + Inches(0.275)
        add_dashed_line(s, cx_center, Inches(1.90),
                        cx_center, worker_y + Inches(0.20),
                        color=SLATE, width=0.75, dash="dash")
    add_rect(s, wx_ + Inches(0.15), worker_y + Inches(0.90),
             worker_w - Inches(0.30), Inches(0.45), BLUE)
    add_text(s, wx_ + Inches(0.15), worker_y + Inches(0.90),
             worker_w - Inches(0.30), Inches(0.45),
             "Container Runtime", size=10.5, bold=True, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_rect(s, wx_ + Inches(0.15), worker_y + Inches(1.40),
             (worker_w - Inches(0.30)) / 2 - Inches(0.05), Inches(0.45),
             STEPS[3])
    add_text(s, wx_ + Inches(0.15), worker_y + Inches(1.40),
             (worker_w - Inches(0.30)) / 2 - Inches(0.05), Inches(0.45),
             "Kubelet", size=10, bold=True, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_rect(s, wx_ + worker_w / 2 + Inches(0.05),
             worker_y + Inches(1.40),
             (worker_w - Inches(0.30)) / 2 - Inches(0.05), Inches(0.45),
             STEPS[3])
    add_text(s, wx_ + worker_w / 2 + Inches(0.05),
             worker_y + Inches(1.40),
             (worker_w - Inches(0.30)) / 2 - Inches(0.05), Inches(0.45),
             "kube-proxy", size=10, bold=True, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_rect(s, wx_ + Inches(0.15), worker_y + Inches(1.95),
             worker_w - Inches(0.30), Inches(0.45), MUTED)
    add_text(s, wx_ + Inches(0.15), worker_y + Inches(1.95),
             worker_w - Inches(0.30), Inches(0.45),
             "Operating System", size=10.5, bold=True, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_rect(s, wx_ + Inches(0.15), worker_y + Inches(2.50),
             worker_w - Inches(0.30), Inches(1.60), SLATE)
    add_text(s, wx_ + Inches(0.15), worker_y + Inches(2.50),
             worker_w - Inches(0.30), Inches(1.60),
             "Infrastructure", size=12, bold=True, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, wx_, worker_y + worker_h + Inches(0.05), worker_w,
             Inches(0.28),
             f"Node {n+1}", size=11, bold=True, color=SLATE,
             align=PP_ALIGN.CENTER)

whale_and_footer(s, 15, TOTAL)


# ============================================================
# SLIDE 16 — Components and Interfaces in K8s Cluster  (DIAGRAM)
# ============================================================
s = new_slide()
title(s, "Components and Interfaces in K8s Cluster")

# Interface colors (Lab02 palette)
IFACE_CNI      = STEPS[2]
IFACE_CRI      = GOAL_GREEN
IFACE_OCI      = TERM_YEL
IFACE_PROTOBUF = ALERT_RED
IFACE_GRPC     = STEPS[1]
IFACE_REST     = BLUE


def _arrow_shape(stype, x, y, w, h, color):
    shp = s.shapes.add_shape(stype, x, y, w, h)
    shp.fill.solid()
    shp.fill.fore_color.rgb = color
    shp.line.fill.background()
    shp.shadow.inherit = False
    return shp


def h_double(x_left, x_right, y_center, color, thickness=Inches(0.12)):
    return _arrow_shape(MSO_SHAPE.LEFT_RIGHT_ARROW,
                        x_left, y_center - thickness / 2,
                        x_right - x_left, thickness, color)


def v_double(x_center, y_top, y_bot, color, thickness=Inches(0.12)):
    return _arrow_shape(MSO_SHAPE.UP_DOWN_ARROW,
                        x_center - thickness / 2, y_top,
                        thickness, y_bot - y_top, color)


def h_arrow(x_from, x_to, y_center, color, thickness=Inches(0.12)):
    rtl = x_to < x_from
    stype = MSO_SHAPE.LEFT_ARROW if rtl else MSO_SHAPE.RIGHT_ARROW
    return _arrow_shape(stype, min(x_from, x_to), y_center - thickness / 2,
                        abs(x_to - x_from), thickness, color)


# User silhouette
head_d = Inches(0.40); head_x = Inches(0.55); head_y = Inches(1.45)
body_w = Inches(1.00); body_h = Inches(0.55)
body_x = head_x + head_d / 2 - body_w / 2
body_y = head_y + head_d - Inches(0.08)
add_oval(s, body_x, body_y, body_w, body_h, SLATE)
add_oval(s, head_x, head_y, head_d, head_d, SLATE)
add_text(s, body_x, body_y + body_h + Inches(0.05),
         body_w, Inches(0.28), "User",
         size=12, bold=True, color=SLATE, align=PP_ALIGN.CENTER)

# Master card
mx = Inches(1.85); my = Inches(1.30)
mw = Inches(10.95); mh = Inches(2.95)
add_rounded_rect(s, mx, my, mw, mh, CARD_BG, line=SLATE, line_width=1.5,
                 radius_ratio=0.02)
add_text(s, mx + Inches(0.20), my + Inches(0.08), Inches(3.0),
         Inches(0.28), "Master", size=12, bold=True, color=SLATE)


def _component(x, y, w, h, name, subtitle):
    add_rounded_rect(s, x, y, w, h, WHITE, line=SLATE,
                     line_width=1.0, radius_ratio=0.05)
    add_rich_text(s, x, y, w, h,
                  [[(name, {"size": 12, "bold": True, "color": SLATE})],
                   [(subtitle, {"size": 10, "color": MUTED})]],
                  align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
                  line_spacing=1.15)


# etcd
etcd_w = Inches(3.20); etcd_h = Inches(0.55)
etcd_x = mx + (mw - etcd_w) / 2
etcd_y = my + Inches(0.45)
add_rounded_rect(s, etcd_x, etcd_y, etcd_w, etcd_h, WHITE,
                 line=SLATE, line_width=1.0, radius_ratio=0.10)
add_text(s, etcd_x, etcd_y, etcd_w, etcd_h,
         "etcd (key-value DB, SSOT)",
         size=11, bold=True, color=SLATE,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

api_w = Inches(2.90); api_h = Inches(1.10)
api_x = mx + (mw - api_w) / 2
api_y = my + Inches(1.45)
_component(api_x, api_y, api_w, api_h, "API Server", "(REST API)")

cm_w = Inches(2.80); cm_x = mx + Inches(0.40); cm_y = api_y
_component(cm_x, cm_y, cm_w, api_h, "Controller Manager", "(Controller Loops)")

sch_w = Inches(2.80); sch_x = mx + mw - sch_w - Inches(0.40); sch_y = api_y
_component(sch_x, sch_y, sch_w, api_h, "Scheduler", "(Bind Pod to Node)")

api_cx = api_x + api_w / 2
api_cy = api_y + api_h / 2

v_double(api_cx, etcd_y + etcd_h, api_y, color=IFACE_GRPC)
protobuf_y = api_y + Inches(0.30)
h_double(cm_x + cm_w, api_x, protobuf_y, color=IFACE_PROTOBUF)
h_double(api_x + api_w, sch_x, protobuf_y, color=IFACE_PROTOBUF)
rest_y = api_y + Inches(0.85)
h_arrow(body_x + body_w - Inches(0.05), api_x + Inches(0.10),
        rest_y, color=IFACE_REST, thickness=Inches(0.10))

# Nodes card
nx = mx; ny = Inches(4.45); nw = mw; nh = Inches(2.15)
add_rounded_rect(s, nx, ny, nw, nh, CARD_BG, line=SLATE, line_width=1.5,
                 radius_ratio=0.02)
add_text(s, nx + Inches(0.20), ny + Inches(0.06), Inches(3.0),
         Inches(0.28), "Nodes", size=12, bold=True, color=SLATE)

node_gap = Inches(0.20)
total_node_w = nw - Inches(0.40) - 2 * node_gap
node_w_outer = total_node_w / 3
loop_w = Inches(0.18)
layer_h = Inches(0.28)
layer_gap = Inches(0.04)


def _selfloop_left(x_left, y_top, y_bottom, color):
    add_line(s, x_left, y_top, x_left - loop_w, y_top, color=color, width=1.5)
    add_line(s, x_left - loop_w, y_top, x_left - loop_w, y_bottom, color=color, width=1.5)
    add_arrow(s, x_left - loop_w, y_bottom, x_left, y_bottom, color=color, width=1.5)


def _selfloop_right(x_right, y_top, y_bottom, color):
    add_line(s, x_right, y_top, x_right + loop_w, y_top, color=color, width=1.5)
    add_line(s, x_right + loop_w, y_top, x_right + loop_w, y_bottom, color=color, width=1.5)
    add_arrow(s, x_right + loop_w, y_bottom, x_right, y_bottom, color=color, width=1.5)


kubelet_centers = []
kubelet_tops = []
for n in range(3):
    nx_wrapper = nx + Inches(0.20) + n * (node_w_outer + node_gap)
    ny_wrapper = ny + Inches(0.45)
    nh_wrapper = Inches(1.55)
    add_rect(s, nx_wrapper, ny_wrapper, node_w_outer, nh_wrapper, STEPS[4])
    layer_left_pad = Inches(0.32)
    layer_right_pad = Inches(0.32)
    layer_x = nx_wrapper + layer_left_pad
    layer_w = node_w_outer - layer_left_pad - layer_right_pad
    layer_top = ny_wrapper + Inches(0.10)
    net_y = layer_top
    add_rect(s, layer_x, net_y, layer_w, layer_h, IFACE_CNI)
    add_text(s, layer_x, net_y, layer_w, layer_h, "Networking",
             size=10, bold=True, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    kube_y = net_y + layer_h + layer_gap
    crun_y = kube_y + layer_h + layer_gap
    os_y   = crun_y + layer_h + layer_gap
    for ly, label in [(kube_y, "Kubelet"), (crun_y, "Container Runtime"), (os_y, "OS")]:
        add_rect(s, layer_x, ly, layer_w, layer_h, WHITE, line=SLATE, line_width=0.5)
        add_text(s, layer_x, ly, layer_w, layer_h, label,
                 size=10, bold=True, color=SLATE,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    _selfloop_left(layer_x, net_y + Inches(0.07), net_y + layer_h - Inches(0.05), IFACE_CNI)
    _selfloop_left(layer_x, kube_y + layer_h / 2, crun_y + layer_h / 2, IFACE_CRI)
    _selfloop_right(layer_x + layer_w, crun_y + layer_h / 2, os_y + layer_h / 2, IFACE_OCI)
    add_text(s, nx_wrapper, ny_wrapper + nh_wrapper - Inches(0.30),
             node_w_outer, Inches(0.28), f"Node {n+1}",
             size=11, bold=True, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    kubelet_centers.append(nx_wrapper + node_w_outer / 2)
    kubelet_tops.append(kube_y)

# Kubelet → API
api_bottom_y = api_y + api_h
for kub_cx, kub_top in zip(kubelet_centers, kubelet_tops):
    add_doublearrow(s, kub_cx, kub_top, api_cx, api_bottom_y,
                    color=IFACE_PROTOBUF, width=1.8)

# Legend (LEFT, vertical)
legend_x = Inches(0.20)
legend_y0 = ny + Inches(0.08)
add_text(s, legend_x, legend_y0, Inches(1.40), Inches(0.30),
         "Legend:", size=11, italic=True, color=MUTED, font=FONT_MONO)
for i, (label, color) in enumerate([
    ("CNI",      IFACE_CNI),
    ("CRI",      IFACE_CRI),
    ("OCI",      IFACE_OCI),
    ("Protobuf", IFACE_PROTOBUF),
    ("gRPC",     IFACE_GRPC),
    ("JSON",     IFACE_REST),
]):
    y = legend_y0 + Inches(0.38 + i * 0.27)
    _arrow_shape(MSO_SHAPE.LEFT_RIGHT_ARROW, legend_x, y,
                 Inches(0.55), Inches(0.12), color)
    add_text(s, legend_x + Inches(0.70), y - Inches(0.06),
             Inches(0.85), Inches(0.28),
             label, size=10.5, color=BODY, font=FONT_MONO,
             anchor=MSO_ANCHOR.MIDDLE)

whale_and_footer(s, 16, TOTAL)


# ============================================================
# SLIDE 17 — Running Application in K8s
# ============================================================
s = new_slide()
title(s, "Running Application in K8s")
bullet_list(s, 1.45, [
    "kubectl is (almost) the only tool we'll need to talk to Kubernetes",
    "It is a rich CLI tool around the Kubernetes API",
    "(Everything you can do with kubectl, you can do directly with the API)",
    "On our machines, there is a ~/.kube/config file with:",
    "    the Kubernetes API address",
    "    the path to our TLS certificates used to authenticate",
    "You can also use the --kubeconfig flag to pass a config file",
    "kubeconfig files organize information about clusters, users, namespaces, and authentication mechanisms. The kubectl command uses these files to find the information it needs to choose a cluster and communicate with it.",
    "kubectl can be pronounced \"Cube C T L\", \"Cube cuttle\", \"Cube cuddle\"...",
], size=11.5, line_spacing=1.35)
whale_and_footer(s, 17, TOTAL)


# ============================================================
# SLIDE 18 — Deploying Application in K8s - Prerequisites  (title only)
# ============================================================
s = new_slide()
title(s, "Deploying Application in K8s  -  Prerequisites")
whale_and_footer(s, 18, TOTAL)


# ============================================================
# SLIDE 19 — Running Application in K8s, Continued
# ============================================================
s = new_slide()
title(s, "Running Application in K8s, Continued")
bullet_list(s, 1.45, [
    "Package and publish your app in Docker registry",
    "Post a description of your app to K8s API",
    "The description will indicate the location of the application images",
    "How these images are related to each other",
    "The resources requirements",
    "The number of replicas to run",
    "Internally or externally discoverable services",
], size=14, line_spacing=1.5)
whale_and_footer(s, 19, TOTAL)


# ============================================================
# SLIDE 20 — Application Deployment Flow in K8s  (DIAGRAM)
# ============================================================
s = new_slide()
title(s, "Application Deployment Flow in K8s")

dev_x = Inches(0.55); dev_y = Inches(1.80)
add_oval(s, dev_x, dev_y, Inches(0.70), Inches(0.70), SLATE)
add_text(s, dev_x, dev_y, Inches(0.70), Inches(0.70), "DEV",
         size=11, bold=True, color=WHITE,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, dev_x - Inches(0.05), dev_y + Inches(0.75),
         Inches(0.80), Inches(0.3), "Developer", size=10, bold=True,
         color=SLATE, align=PP_ALIGN.CENTER)

# App descriptor with shape vocabulary
desc_x = Inches(0.55); desc_y = Inches(3.10); desc_w = Inches(1.60); desc_h = Inches(2.60)
add_rect(s, desc_x, desc_y, desc_w, desc_h, CARD_BG, line=SLATE, line_width=1.0)
add_text(s, desc_x, desc_y + Inches(0.05), desc_w, Inches(0.28),
         "App descriptor", size=10, bold=True, color=SLATE, align=PP_ALIGN.CENTER)

ry = desc_y + Inches(0.40)
add_text(s, desc_x + Inches(0.05), ry + Inches(0.10), Inches(0.30), Inches(0.30), "1×",
         size=11, bold=True, color=SLATE, font=FONT_MONO, anchor=MSO_ANCHOR.MIDDLE)
add_rect(s, desc_x + Inches(0.45), ry, Inches(1.05), Inches(0.55), WHITE, line=SLATE, line_width=0.6)
add_diamond(s, desc_x + Inches(0.75), ry + Inches(0.08), Inches(0.42), Inches(0.42), DIAMOND_FILL, line=SLATE, line_width=0.6)

ry = desc_y + Inches(1.10)
add_text(s, desc_x + Inches(0.05), ry + Inches(0.10), Inches(0.30), Inches(0.30), "5×",
         size=11, bold=True, color=SLATE, font=FONT_MONO, anchor=MSO_ANCHOR.MIDDLE)
add_rect(s, desc_x + Inches(0.45), ry, Inches(1.05), Inches(0.55), WHITE, line=SLATE, line_width=0.6)
add_oval(s, desc_x + Inches(0.75), ry + Inches(0.08), Inches(0.42), Inches(0.42), CIRCLE_FILL, line=SLATE, line_width=0.6)

ry = desc_y + Inches(1.80)
add_text(s, desc_x + Inches(0.05), ry + Inches(0.10), Inches(0.30), Inches(0.30), "2×",
         size=11, bold=True, color=SLATE, font=FONT_MONO, anchor=MSO_ANCHOR.MIDDLE)
add_rect(s, desc_x + Inches(0.45), ry, Inches(1.05), Inches(0.55), WHITE, line=SLATE, line_width=0.6)
add_pentagon(s, desc_x + Inches(0.50), ry + Inches(0.05), Inches(0.42), Inches(0.42), PENTAGON_FILL, line=SLATE, line_width=0.6)
add_triangle(s, desc_x + Inches(0.95), ry + Inches(0.08), Inches(0.40), Inches(0.40), TRIANGLE_FILL, line=SLATE, line_width=0.6)

# Image registry
reg_x = Inches(2.95); reg_y = Inches(1.90); reg_w = Inches(2.10); reg_h = Inches(1.10)
add_rounded_rect(s, reg_x, reg_y, reg_w, reg_h, CARD_BG, line=BLUE,
                 line_width=1.5, radius_ratio=0.10)
add_text(s, reg_x, reg_y + Inches(0.30), reg_w, Inches(0.50),
         "Image registry", size=12, bold=True, color=BLUE, align=PP_ALIGN.CENTER)

# Control plane
cp_x = Inches(2.95); cp_y = Inches(3.30); cp_w = Inches(2.10); cp_h = Inches(1.40)
add_rect(s, cp_x, cp_y, cp_w, cp_h, BLUE)
add_text(s, cp_x, cp_y, cp_w, cp_h, "Control Plane\n(master)",
         size=13, bold=True, color=WHITE,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.2)

# Arrows
add_arrow(s, dev_x + Inches(0.70), dev_y + Inches(0.35),
          reg_x, reg_y + Inches(0.50), color=SLATE, width=1.5)
add_arrow(s, desc_x + desc_w, desc_y + Inches(0.30),
          cp_x, cp_y + cp_h / 2, color=SLATE, width=1.5)
add_arrow(s, reg_x + reg_w / 2, reg_y + reg_h,
          reg_x + reg_w / 2, cp_y, color=MUTED, width=1.2)

# Worker tiles with same shape vocabulary
wx0 = Inches(6.00); wy0 = Inches(1.60); wnw = Inches(2.20)
wnh = Inches(1.50); wgap = Inches(0.10)


def _worker_shape(kind, x, y, w, h, color):
    if kind == "diamond":
        add_diamond(s, x, y, w, h, color, line=SLATE, line_width=0.5)
    elif kind == "circle":
        add_oval(s, x, y, w, h, color, line=SLATE, line_width=0.5)
    elif kind == "pentagon":
        add_pentagon(s, x, y, w, h, color, line=SLATE, line_width=0.5)
    elif kind == "triangle":
        add_triangle(s, x, y, w, h, color, line=SLATE, line_width=0.5)


worker_tiles = [
    [("diamond", DIAMOND_FILL,  0.10, 0.08, 0.40, 0.40),
     ("circle",  CIRCLE_FILL,   0.60, 0.10, 0.36, 0.36)],
    [("pentagon", PENTAGON_FILL, 0.12, 0.06, 0.42, 0.42),
     ("triangle", TRIANGLE_FILL, 0.62, 0.12, 0.38, 0.38)],
    [("diamond",  DIAMOND_FILL,  0.05, 0.06, 0.32, 0.32),
     ("circle",   CIRCLE_FILL,   0.48, 0.05, 0.32, 0.32),
     ("triangle", TRIANGLE_FILL, 0.90, 0.18, 0.30, 0.30)],
    [("circle", CIRCLE_FILL, 0.30, 0.10, 0.42, 0.42)],
    [("circle",   CIRCLE_FILL,   0.08, 0.10, 0.32, 0.32),
     ("pentagon", PENTAGON_FILL, 0.52, 0.06, 0.40, 0.40),
     ("triangle", TRIANGLE_FILL, 0.30, 0.32, 0.28, 0.28)],
    [("circle", CIRCLE_FILL, 0.30, 0.10, 0.42, 0.42)],
]
for i in range(6):
    col = i % 3; row = i // 3
    wx = wx0 + (wnw + wgap) * col
    wy = wy0 + (wnh + wgap) * row
    add_rect(s, wx, wy, wnw, wnh, WHITE, line=SLATE, line_width=1.0)
    for kind, color, dx, dy, sw, sh in worker_tiles[i]:
        _worker_shape(kind, wx + Inches(dx), wy + Inches(dy),
                      Inches(sw), Inches(sh), color)
    add_rect(s, wx + Inches(0.10), wy + Inches(0.65),
             wnw - Inches(0.20), Inches(0.32), MUTED)
    add_text(s, wx + Inches(0.10), wy + Inches(0.65),
             wnw - Inches(0.20), Inches(0.32), "containerd",
             size=8.5, bold=True, color=WHITE, font=FONT_MONO,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_rect(s, wx + Inches(0.10), wy + Inches(1.00),
             (wnw - Inches(0.20)) / 2 - Inches(0.03), Inches(0.32), STEPS[3])
    add_text(s, wx + Inches(0.10), wy + Inches(1.00),
             (wnw - Inches(0.20)) / 2 - Inches(0.03), Inches(0.32),
             "Kubelet", size=8.5, bold=True, color=WHITE, font=FONT_MONO,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_rect(s, wx + wnw / 2 + Inches(0.03), wy + Inches(1.00),
             (wnw - Inches(0.20)) / 2 - Inches(0.03), Inches(0.32), STEPS[3])
    add_text(s, wx + wnw / 2 + Inches(0.03), wy + Inches(1.00),
             (wnw - Inches(0.20)) / 2 - Inches(0.03), Inches(0.32),
             "kube-proxy", size=8.5, bold=True, color=WHITE, font=FONT_MONO,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

add_arrow(s, cp_x + cp_w, cp_y + cp_h / 2,
          wx0, cp_y + cp_h / 2, color=SLATE, width=1.8)
add_text(s, wx0, wy0 + wnh * 2 + wgap + Inches(0.10),
         (wnw + wgap) * 3, Inches(0.30),
         "Worker nodes", size=12, bold=True, color=SLATE, align=PP_ALIGN.CENTER)

whale_and_footer(s, 20, TOTAL)


# ============================================================
# SLIDE 21 — Ready for a Kubernetes deployment  (title only)
# ============================================================
s = new_slide()
title(s, "Ready for a Kubernetes deployment")
whale_and_footer(s, 21, TOTAL)


# ============================================================
# SLIDE 22 — K8s Network Model
# ============================================================
s = new_slide()
title(s, "K8s Network Model")
add_text(s, Inches(0.55), Inches(1.30), Inches(12.2), Inches(0.40),
         "TL,DR:", size=14, bold=True, color=SLATE)
add_text(s, Inches(0.55), Inches(1.75), Inches(12.2), Inches(0.45),
         "Our cluster (nodes and pods) is one big flat IP network.",
         size=15, color=BODY)
add_text(s, Inches(0.55), Inches(2.45), Inches(12.2), Inches(0.40),
         "In detail:", size=14, bold=True, color=SLATE)
bullet_list(s, 2.95, [
    "all nodes must be able to reach each other, without NAT",
    "all pods must be able to reach each other, without NAT",
    "pods and nodes must be able to reach each other, without NAT",
    "each pod is aware of its IP address (no NAT)",
    "Kubernetes doesn't mandate any particular implementation",
], size=14, line_spacing=1.5)
whale_and_footer(s, 22, TOTAL)


# ============================================================
# SLIDE 23 — K8s Networking
# ============================================================
s = new_slide()
title(s, "K8s Networking")
bullet_list(s, 1.55, [
    "K8s setup creates a internal private network  10.244.0.0.",
    "All PODS created within the node, gets an IP from this range",
    "They are reachable from one another",
    "Accessing other PODS with this internal IP might not be suggested as IP changes when PODs are recreated",
], size=14, line_spacing=1.5)
whale_and_footer(s, 23, TOTAL)


# ============================================================
# SLIDE 24 — K8s Networking (multi-node)
# ============================================================
s = new_slide()
title(s, "K8s Networking")
bullet_list(s, 1.55, [
    "In a multi-node cluster, as PODs get IP from same range, it could lead to IP conflict as 2 PODS can get same IP addresses",
    "Depending on platform different solutions are available (eg: CISCO, CILIUM, CALICO etc. are used)",
    "With Custom networking in place, it manages network and Ips in the nodes and assigns a different IP to every POD.",
    "With simple routing techniques, this is managed",
], size=13, line_spacing=1.5)
whale_and_footer(s, 24, TOTAL)


# ============================================================
# SLIDE 25 — K8s Networking (multi-node diagram follow-up)
# (User previously chose to keep both diagram variants; this is the
# routing/fix diagram. No invented body text.)
# ============================================================
s = new_slide()
title(s, "K8s Networking")

cl_x = Inches(0.55); cl_y = Inches(1.55); cl_w = Inches(12.2); cl_h = Inches(4.90)
add_rounded_rect(s, cl_x, cl_y, cl_w, cl_h, CARD_BG,
                 line=BLUE, line_width=1.5, radius_ratio=0.03)
add_text(s, cl_x, cl_y + cl_h - Inches(0.35), cl_w, Inches(0.32),
         "Kubernetes Cluster", size=12, bold=True, color=BLUE,
         align=PP_ALIGN.CENTER)


def _routed_node(x, y, w, h, host_ip, subnet, pod_ip):
    add_rounded_rect(s, x, y, w, h, WHITE, line=BLUE, line_width=1.0,
                     radius_ratio=0.04)
    add_rect(s, x + Inches(0.50), y + Inches(0.15),
             w - Inches(1.00), Inches(0.40), SLATE)
    add_text(s, x + Inches(0.50), y + Inches(0.15),
             w - Inches(1.00), Inches(0.40), host_ip,
             size=11, bold=True, color=WHITE, font=FONT_MONO,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_oval(s, x + Inches(0.60), y + Inches(0.70),
             w - Inches(1.20), Inches(0.80), BLUE)
    add_text(s, x + Inches(0.60), y + Inches(0.70),
             w - Inches(1.20), Inches(0.80), subnet,
             size=13, bold=True, color=WHITE, font=FONT_MONO,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    pw = Inches(1.40); ph = Inches(1.60)
    px = x + (w - pw) / 2; py = y + Inches(1.70)
    add_rect(s, px, py, pw, Inches(0.40), STEPS[3])
    add_text(s, px, py, pw, Inches(0.40), pod_ip,
             size=10, bold=True, color=WHITE, font=FONT_MONO,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_rect(s, px, py + Inches(0.40), pw, ph - Inches(0.40),
             WHITE, line=BLUE, line_width=1)
    add_text(s, px, py + ph - Inches(0.30), pw, Inches(0.25),
             "POD", size=10, bold=True, color=SLATE, font=FONT_MONO,
             align=PP_ALIGN.CENTER)
    add_text(s, x, y + h - Inches(0.32), w, Inches(0.28),
             "Node", size=11, bold=True, color=SLATE,
             align=PP_ALIGN.CENTER)


nw_ = Inches(5.30); nh_ = Inches(3.95)
_routed_node(cl_x + Inches(0.30), cl_y + Inches(0.30), nw_, nh_,
             "host  192.168.1.2", "10.244.0.0/24", "10.244.0.2")
_routed_node(cl_x + cl_w - nw_ - Inches(0.30), cl_y + Inches(0.30), nw_, nh_,
             "host  192.168.1.3", "10.244.1.0/24", "10.244.1.2")

hx = cl_x + cl_w / 2 - Inches(0.65); hy = cl_y + Inches(1.60)
add_hex(s, hx, hy, Inches(1.30), Inches(0.95), STEPS[1])
add_text(s, hx, hy, Inches(1.30), Inches(0.95), "Routing",
         size=12, bold=True, color=WHITE,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

whale_and_footer(s, 25, TOTAL)


# ============================================================
# SLIDE 26 — Hosting K8s Cluster
# ============================================================
s = new_slide()
title(s, "Hosting K8s Cluster")
add_text(s, Inches(0.55), Inches(1.30), Inches(12.2), Inches(0.45),
         "K8s cluster can run anywhere", size=15, color=BODY)
bullet_list(s, 2.05, [
    "On prem",
    "In public cloud, self-hosted",
    "In public cloud, as a managed service",
    "In a private cloud, Openstack",
    "On virtualized VMs",
    "On bare metal hosts",
    "OpenShift – commercial offering by IBM",
], size=14, line_spacing=1.55)
whale_and_footer(s, 26, TOTAL)


# ============================================================
# SLIDE 27 — Workshop 1 – Setting up K8s cluster with kind  (title only)
# ============================================================
s = new_slide()
title(s, "Workshop 1 – Setting up K8s cluster with kind")
whale_and_footer(s, 27, TOTAL)


# ============================================================
# SLIDE 28 — Relevant Links
# ============================================================
s = new_slide()
title(s, "Relevant Links")
add_text(s, Inches(0.55), Inches(1.65), Inches(12.2), Inches(0.45),
         "https://kind.sigs.k8s.io/docs/user/quick-start/",
         font=FONT_MONO, size=13, color=BLUE)
add_text(s, Inches(0.55), Inches(2.30), Inches(12.2), Inches(0.45),
         "https://www.eksworkshop.com/intermediate/200_migrate_to_eks/create-kind-cluster/",
         font=FONT_MONO, size=13, color=BLUE)
whale_and_footer(s, 28, TOTAL)


# ============================================================
# SLIDE 29 — Pre-requisites
# ============================================================
s = new_slide()
title(s, "Pre-requisites")
terminal(s, Inches(0.55), Inches(1.40), Inches(12.2), Inches(5.20),
         "bash",
         [[("# remove all the docker images in Cloud9", TERM_GRN)],
          [("docker rmi -f $(docker images -aq)", TERM_CYAN)],
          [],
          [("# install kind", TERM_GRN)],
          [("curl -sLo kind https://kind.sigs.k8s.io/dl/v0.11.0/kind-linux-amd64", TERM_CYAN)],
          [("sudo install -o root -g root -m 0755 kind /usr/local/bin/kind", TERM_CYAN)],
          [("rm -f ./kind", TERM_CYAN)],
          [],
          [("# Install kubectl – important! It should match cluster version 1.30", TERM_GRN)],
          [("# https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html", TERM_GRN)],
          [("curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.30.7/2024-12-12/bin/linux/amd64/kubectl", TERM_CYAN)],
          [("chmod +x ./kubectl", TERM_CYAN)],
          [("mkdir -p $HOME/bin && cp ./kubectl $HOME/bin/kubectl && export PATH=$PATH:$HOME/bin", TERM_CYAN)],
          [("echo 'export PATH=$PATH:$HOME/bin' >> ~/.bashrc", TERM_CYAN)],
          [("kubectl version --short --client", TERM_CYAN)]],
         font_size=10)
whale_and_footer(s, 29, TOTAL)


# ============================================================
# SLIDE 30 — Create Cluster Description and Deploy Cluster
# ============================================================
s = new_slide()
title(s, "Create Cluster Description and Deploy Cluster")
terminal(s, Inches(0.55), Inches(1.40), Inches(12.2), Inches(5.20),
         "bash",
         [[("# You can copy from this link # https://www.eksworkshop.com/intermediate/200_migrate_to_eks/create-kind-cluster/", TERM_GRN)],
          [("# delete all the docker images apart from kind from your Cloud9", TERM_GRN)],
          [("cat > kind.yaml <<EOF", TERM_CYAN)],
          [("kind: Cluster", TERM_GRAY)],
          [("apiVersion: kind.x-k8s.io/v1alpha4", TERM_GRAY)],
          [("nodes:", TERM_GRAY)],
          [("- role: control-plane", TERM_GRAY)],
          [("  image: kindest/node:v1.23.17@sha256:14d0a9a892b943866d7e6be119a06871291c517d279aedb816a4b4bc0ec0a5b3", TERM_GRAY)],
          [("  extraPortMappings:", TERM_GRAY)],
          [("  - containerPort: 30000", TERM_GRAY)],
          [("    hostPort: 30000", TERM_GRAY)],
          [("  - containerPort: 30001", TERM_GRAY)],
          [("    hostPort: 30001", TERM_GRAY)],
          [("EOF", TERM_CYAN)],
          [],
          [("# Create the cluster", TERM_GRN)],
          [("kind create cluster --config kind.yaml", TERM_CYAN)]],
         font_size=10)
whale_and_footer(s, 30, TOTAL)


# ============================================================
# SLIDE 31 — Deploy our first application
# ============================================================
s = new_slide()
title(s, "Deploy our first application")
terminal(s, Inches(0.55), Inches(1.55), Inches(12.2), Inches(4.80),
         "bash",
         [[("$ kubectl run nginx --image=nginx --port=80", TERM_CYAN)],
          [],
          [("# List the pods", TERM_GRN)],
          [("$ kubectl get pods", TERM_CYAN)],
          [],
          [("# What are pods?", TERM_GRN)]],
         font_size=14)
whale_and_footer(s, 31, TOTAL)


# ============================================================
# SLIDE 32 — Understanding the flow of "kubectl run" command  (title only)
# ============================================================
s = new_slide()
title(s, "Understanding the flow of \"kubectl run\" command")
whale_and_footer(s, 32, TOTAL)


# ============================================================
# SLIDE 33 — Expose your application
# ============================================================
s = new_slide()
title(s, "Expose your application")
terminal(s, Inches(0.55), Inches(1.55), Inches(12.2), Inches(4.80),
         "bash",
         [[("$ k expose pod nginx --type=NodePort --name nginx-http", TERM_CYAN)],
          [],
          [("# List services", TERM_GRN)],
          [("$ kubectl get services", TERM_CYAN)],
          [],
          [("# What are services?", TERM_GRN)]],
         font_size=14)
whale_and_footer(s, 33, TOTAL)


# ============================================================
# SLIDE 34 — All the components: Deployment, Service, Pods, Nodes  (title only)
# ============================================================
s = new_slide()
title(s, "All the components: Deployment, Service, Pods, Nodes")
whale_and_footer(s, 34, TOTAL)


# ============================================================
# SLIDE 35 — Access the application, Scale the pods, ...
# ============================================================
s = new_slide()
title(s, "Access the application, Scale the pods, Get more information on running pods and nodes, create a deploy a new version", size=22)
terminal(s, Inches(0.55), Inches(2.40), Inches(12.2), Inches(3.80),
         "bash",
         [[("$ curl <kind container IP>:80", TERM_CYAN)]],
         font_size=14)
whale_and_footer(s, 35, TOTAL)


# ============================================================
# SLIDE 36 — Deployment of K8s Dashboard  (title only)
# ============================================================
s = new_slide()
title(s, "Deployment of K8s Dashboard")
whale_and_footer(s, 36, TOTAL)


# ============================================================
# SLIDE 37 — Workshop 1 – The End  (title only)
# ============================================================
s = new_slide()
title(s, "Workshop 1 – The End")
whale_and_footer(s, 37, TOTAL)


# ============================================================
# SLIDE 38 — References
# ============================================================
s = new_slide()
title(s, "References")
for i, url in enumerate([
    "https://pycon2019.container.training/#1",
    "https://github.com/jpetazzo/container.training/tree/main/dockercoins",
    "https://www.eksworkshop.com/intermediate/200_migrate_to_eks/deploy-counter-app-kind/",
    "https://github.com/luksa/kubernetes-in-action",
    "https://kind.sigs.k8s.io/",
]):
    add_text(s, Inches(0.55), Inches(1.55 + i * 0.65), Inches(12.2),
             Inches(0.40), url, font=FONT_MONO, size=14, color=BLUE)
whale_and_footer(s, 38, TOTAL)


# ===== Save =====
out = f"Week04/Week04_lab_style_{VERSION}.pptx"
prs.save(out)
print(f"wrote {out}")
