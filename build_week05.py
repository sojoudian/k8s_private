"""Week05_lab_style_v1.pptx — Lab02 design language applied to Week5.pptx.

Original slide text preserved verbatim (no rephrasing, no invented body).
Diagrams rendered natively in our palette for slides 4, 6, 14, 18, 21, 37.
YAML / command slides use the dark terminal mockup.
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
    RGBColor(0x1F, 0xA8, 0xE0), RGBColor(0x21, 0x96, 0xA0),
    RGBColor(0x1F, 0x8F, 0xCD), RGBColor(0x1F, 0x7A, 0xB8),
    RGBColor(0x24, 0x66, 0xA0), RGBColor(0x37, 0x46, 0x5A),
]

FONT_SANS = "Calibri"
FONT_MONO = "Consolas"

K8S_LOGO = "Week04/Kubernetes_logo_without_workmark.svg.png"
WHALE    = "whale.png"

VERSION  = "v12"
TOTAL    = 39


# ===== Coordinate-safety primitives =====
# Background: OOXML requires <a:off>/<a:ext> x/y/cx/cy to be integers.
# Python's `/` returns floats, and python-pptx will serialize a float Emu
# straight into XML as e.g. "4288536.0", which PowerPoint and Keynote then
# reject and reposition to (0,0) — see memory feedback-axis-aligned-arrows.
# `_i` coerces any float that leaks through arithmetic; `_sanitize_coords`
# is a save-time safety net that walks every shape and fixes any survivors.

def _i(v):
    if isinstance(v, float):
        return int(v)
    return v


def _sanitize_coords(prs):
    import re as _re
    DML = 'http://schemas.openxmlformats.org/drawingml/2006/main'
    targets = {f'{{{DML}}}off', f'{{{DML}}}ext',
               f'{{{DML}}}chOff', f'{{{DML}}}chExt'}
    int_re = _re.compile(r'-?\d+')
    for slide in prs.slides:
        for elem in slide.shapes._spTree.iter():
            if elem.tag in targets:
                for attr in ('x', 'y', 'cx', 'cy'):
                    v = elem.get(attr)
                    if v is not None and not int_re.fullmatch(v):
                        try:
                            elem.set(attr, str(int(float(v))))
                        except ValueError:
                            pass


# ===== Helpers =====

def add_text(s, x, y, w, h, text, *, font=FONT_SANS, size=14, bold=False,
             italic=False, color=BODY, align=PP_ALIGN.LEFT,
             anchor=MSO_ANCHOR.TOP, line_spacing=1.15):
    tb = s.shapes.add_textbox(_i(x), _i(y), _i(w), _i(h))
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
        r = p.add_run(); r.text = line
        r.font.name = font; r.font.size = Pt(size)
        r.font.bold = bold; r.font.italic = italic
        r.font.color.rgb = color
    return tb


def add_rich_text(s, x, y, w, h, runs, *, align=PP_ALIGN.LEFT,
                  anchor=MSO_ANCHOR.TOP, line_spacing=1.2):
    tb = s.shapes.add_textbox(_i(x), _i(y), _i(w), _i(h))
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
            r = p.add_run(); r.text = text
            r.font.name = kw.get("font", FONT_SANS)
            r.font.size = Pt(kw.get("size", 14))
            r.font.bold = kw.get("bold", False)
            r.font.italic = kw.get("italic", False)
            r.font.color.rgb = kw.get("color", BODY)
    return tb


def add_rect(s, x, y, w, h, fill, line=None, line_width=0.75):
    shp = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, _i(x), _i(y), _i(w), _i(h))
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line is None: shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(line_width)
    shp.shadow.inherit = False
    return shp


def add_rounded_rect(s, x, y, w, h, fill, line=None, line_width=0.75,
                     radius_ratio=0.06):
    shp = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                             _i(x), _i(y), _i(w), _i(h))
    shp.adjustments[0] = radius_ratio
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line is None: shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(line_width)
    shp.shadow.inherit = False
    return shp


def add_oval(s, x, y, w, h, fill, line=None, line_width=0.75):
    shp = s.shapes.add_shape(MSO_SHAPE.OVAL, _i(x), _i(y), _i(w), _i(h))
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line is None: shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(line_width)
    shp.shadow.inherit = False
    return shp


def add_hex(s, x, y, w, h, fill, line=None, line_width=0.75):
    shp = s.shapes.add_shape(MSO_SHAPE.HEXAGON, _i(x), _i(y), _i(w), _i(h))
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line is None: shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(line_width)
    shp.shadow.inherit = False
    return shp


def add_line(s, x1, y1, x2, y2, color=RULE_GRAY, width=0.75):
    ln = s.shapes.add_connector(1, _i(x1), _i(y1), _i(x2), _i(y2))
    ln.line.color.rgb = color
    ln.line.width = Pt(width)
    return ln


def add_arrow(s, x1, y1, x2, y2, color=SLATE, width=1.5):
    ln = s.shapes.add_connector(1, _i(x1), _i(y1), _i(x2), _i(y2))
    ln.line.color.rgb = color
    ln.line.width = Pt(width)
    e = ln.line._get_or_add_ln()
    e.append(etree.fromstring(
        '<a:tailEnd type="triangle" w="med" len="med" '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>'))
    return ln


def add_rect_outlined(s, x, y, w, h, color, line_width=2.5):
    shp = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, _i(x), _i(y), _i(w), _i(h))
    shp.fill.background()
    shp.line.color.rgb = color
    shp.line.width = Pt(line_width)
    shp.shadow.inherit = False
    return shp


def whale_and_footer(slide, page_num, total):
    slide.shapes.add_picture(WHALE, Inches(0.45), Inches(6.85),
                             width=Inches(0.5), height=Inches(0.5))
    add_line(slide, Inches(0.5), Inches(7.05),
             Inches(12.83), Inches(7.05), color=RULE_GRAY, width=0.5)
    add_text(slide, Inches(9.5), Inches(7.12), Inches(3.35), Inches(0.3),
             f"CLO835, Fall 2026     {page_num} / {total}",
             size=10, color=FOOTER_GRAY, align=PP_ALIGN.RIGHT)


def title(slide, text, y=0.40, size=32):
    add_text(slide, Inches(0.55), Inches(y), Inches(12.2), Inches(0.85),
             text, size=size, bold=True, color=BLUE, line_spacing=1.05)


def bullet_list(slide, y_start, items, *, size=14, bullet_color=BLUE,
                line_spacing=1.5, max_w=12.0, x=0.55):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y_start),
                                  Inches(max_w),
                                  Inches(max(0.5, 7.5 - y_start - 0.85)))
    tf = tb.text_frame
    tf.margin_left = Inches(0); tf.margin_right = Inches(0)
    tf.margin_top = Inches(0); tf.margin_bottom = Inches(0)
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.line_spacing = line_spacing
        p.space_after = Pt(4)
        r0 = p.add_run(); r0.text = "■  "
        r0.font.name = FONT_SANS; r0.font.size = Pt(size)
        r0.font.color.rgb = bullet_color
        r1 = p.add_run(); r1.text = item
        r1.font.name = FONT_SANS; r1.font.size = Pt(size)
        r1.font.color.rgb = BODY


def terminal(slide, x, y, w, h, title_text, body_runs, *, font_size=11):
    add_rect(slide, x, y, w, h, TERMBG)
    bar_h = Inches(0.32)
    add_rect(slide, x, y, w, bar_h, RGBColor(0x3A, 0x3A, 0x3A))
    dot_d = Inches(0.13); dot_y = y + Inches(0.10)
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
         "Kubernetes Core Concepts:\nPods, ReplicaSets, Deployments",
         size=36, bold=True, color=BLUE, line_spacing=1.10)
add_text(s, Inches(0.7), Inches(4.85), Inches(8.5), Inches(0.6),
         "Week 5", size=22, color=SLATE)
logo_cx = Inches(10.6); logo_cy = Inches(3.75); ring_r = Inches(1.8)
add_oval(s, logo_cx - ring_r, logo_cy - ring_r,
         ring_r * 2, ring_r * 2, WHITE, line=LIGHTBLUE, line_width=1.5)
s.shapes.add_picture(K8S_LOGO, logo_cx - Inches(1.25), logo_cy - Inches(1.25),
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
# SLIDE 3 — Pods vs Containers
# ============================================================
s = new_slide()
title(s, "Pods vs Containers")
bullet_list(s, 1.55, [
    "Pods are co-located groups of containers",
    "Pods (and not containers) represent the minimal deployment unit in K8s",
    "Containers in a pods are scheduled, started and terminated as one unit",
    "Containers in a pod share the same network, processes and can share the same filesystem",
], size=15, line_spacing=1.55)
whale_and_footer(s, 3, TOTAL)


# ============================================================
# SLIDE 4 — Pods – The best of VMs and Containers World  (DIAGRAM)
# ============================================================
s = new_slide()
title(s, "Pods – The best of VMs and Containers World")

# Pod box with 3 container slots inside (multi-tenant box)
pod_x = Inches(2.2); pod_y = Inches(1.80); pod_w = Inches(9.0); pod_h = Inches(4.30)
add_rounded_rect(s, pod_x, pod_y, pod_w, pod_h, CARD_BG, line=BLUE, line_width=1.8)
# "Kubernetes Pod" label at top
add_text(s, pod_x, pod_y + Inches(0.10), pod_w, Inches(0.32),
         "Kubernetes Pod — a multitenant \"box\"",
         size=13, bold=True, color=BLUE, align=PP_ALIGN.CENTER)
add_text(s, pod_x, pod_y + Inches(0.45), pod_w, Inches(0.28),
         "namespaces",
         size=10, italic=True, color=MUTED, align=PP_ALIGN.CENTER)

# 3 container slots
ctr_w = Inches(2.5); ctr_h = Inches(2.85); ctr_y = pod_y + Inches(0.85)
ctr_gap = (pod_w - 3 * ctr_w) / 4
labels = [("Nginx", "sidecar container", STEPS[1]),
          ("Web App", "main container", BLUE),
          ("Vault Agent", "init container", STEPS[3])]
for i, (head, sub, color) in enumerate(labels):
    cx = pod_x + ctr_gap + (ctr_w + ctr_gap) * i
    add_rect(s, cx, ctr_y, ctr_w, ctr_h, WHITE, line=SLATE, line_width=0.75)
    # Header strip
    add_rect(s, cx, ctr_y, ctr_w, Inches(0.50), color)
    add_text(s, cx, ctr_y, ctr_w, Inches(0.50), head,
             size=13, bold=True, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, cx, ctr_y + Inches(0.55), ctr_w, Inches(0.30), sub,
             size=10, italic=True, color=MUTED, align=PP_ALIGN.CENTER)
    # CPU / RAM / FS chips inside
    for j, chip in enumerate(["CPU limits", "RAM limits", "File System"]):
        cy = ctr_y + Inches(0.95 + j * 0.55)
        add_rect(s, cx + Inches(0.20), cy, ctr_w - Inches(0.40),
                 Inches(0.42), CARD_BG, line=SLATE, line_width=0.5)
        add_text(s, cx + Inches(0.20), cy, ctr_w - Inches(0.40),
                 Inches(0.42), chip, size=10, color=SLATE,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# Bottom strip — all containers share network
add_rect(s, pod_x + Inches(0.30), pod_y + pod_h - Inches(0.55),
         pod_w - Inches(0.60), Inches(0.40), STEPS[0])
add_text(s, pod_x + Inches(0.30), pod_y + pod_h - Inches(0.55),
         pod_w - Inches(0.60), Inches(0.40),
         "all containers share one network stack · 127.0.0.1 · single IP",
         size=10.5, bold=True, color=WHITE,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

whale_and_footer(s, 4, TOTAL)


# ============================================================
# SLIDE 5 — Pods Use Cases
# ============================================================
s = new_slide()
title(s, "Pods Use Cases")
bullet_list(s, 1.40, [
    "Containers are designed to run a single process – what if we need to run multiple related processes the way we run them on a VM",
    "Pods are logical hosts used to run tightly coupled application components",
    "Running multiple processes in a container adds a lot of complexity",
    "Running related processes as multiple isolated containers is not trivial",
    "Keeping track which containers are related",
    "Start and stop them simultaneously",
    "Scale them simultaneously",
    "Pod provides the best of both worlds",
    "Containers in the pod share Linux namespaces (UTS, Network IPC); docker containers have their own individual namespaces",
    "Containers in the pod are somewhat isolated – each container in the pod has its own filesystem",
    "Containers share the same loopback interface (127.0.0.1)",
], size=11.5, line_spacing=1.35)
whale_and_footer(s, 5, TOTAL)


# ============================================================
# SLIDE 6 — Splitting Application into Multiple Pods  (DIAGRAM)
# ============================================================
s = new_slide()
title(s, "Splitting Application into Multiple Pods")

# Left: 3-tier architecture diagram
diag_x = Inches(0.55); diag_y = Inches(1.55); diag_w = Inches(7.5); diag_h = Inches(4.9)
add_rounded_rect(s, diag_x, diag_y, diag_w, diag_h, WHITE, line=SLATE, line_width=1.5)
# Header bar
add_rect(s, diag_x, diag_y, diag_w, Inches(0.55), SLATE)
add_text(s, diag_x, diag_y, diag_w, Inches(0.55), "THREE-TIER ARCHITECTURE IN APPLICATION",
         size=14, bold=True, color=WHITE,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

tiers = [("WEB / PRESENTATION LAYER", STEPS[1]),
         ("APPLICATION LAYER", STEPS[2]),
         ("DATABASE LAYER", STEPS[3])]
for i, (label, color) in enumerate(tiers):
    y = diag_y + Inches(0.85 + i * 1.20)
    add_rect(s, diag_x + Inches(0.30), y, diag_w - Inches(0.60),
             Inches(1.00), WHITE, line=SLATE, line_width=1.0)
    add_rect(s, diag_x + Inches(0.30), y, Inches(2.40),
             Inches(1.00), SLATE)
    add_text(s, diag_x + Inches(0.30), y, Inches(2.40), Inches(1.00),
             label, size=11, bold=True, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
             line_spacing=1.15)
    # Icon area on right
    icon_x = diag_x + diag_w - Inches(1.60)
    add_rect(s, icon_x, y + Inches(0.20), Inches(1.20), Inches(0.60),
             color)

# Right: the question text
add_text(s, Inches(8.30), Inches(1.95), Inches(4.55), Inches(4.2),
         "Do you think a multi-tier application consisting of a frontend web server, application server and a backend database should be configured as a single pod or as two pods?",
         size=14, color=BODY, line_spacing=1.55)

whale_and_footer(s, 6, TOTAL)


# ============================================================
# SLIDE 7 — Running Multiple Containers in a Pod
# ============================================================
s = new_slide()
title(s, "Running Multiple Containers in a Pod")
bullet_list(s, 1.95, [
    "Do they need to be run together or can they run on different hosts?",
    "Do they represent a single whole or are they independent components?",
    "Must they be scaled together or individually?",
], size=16, line_spacing=1.7)
whale_and_footer(s, 7, TOTAL)


# ============================================================
# SLIDE 8 — Collocating Processes in the Pod
# ============================================================
s = new_slide()
title(s, "Collocating Processes in the Pod")
add_text(s, Inches(0.55), Inches(1.55), Inches(12.2), Inches(0.45),
         "Main process and a side car pattern",
         size=15, bold=True, color=SLATE)
bullet_list(s, 2.30, [
    "user input validation sidecar",
    "logging rotation sidecar",
    "content enrichment sidecar",
], size=15, line_spacing=1.7)
whale_and_footer(s, 8, TOTAL)


# ============================================================
# SLIDE 9 — Introducing Pod Descriptor
# ============================================================
s = new_slide()
title(s, "Introducing Pod Descriptor")
bullet_list(s, 1.55, [
    "Metadata includes the name, namespace, labels, and other information about the pod.",
    "Spec contains the actual description of the pod's contents, such as the pod's containers, volumes, and other data. Pod specification/contents (list of pod's containers, volumes, and so on)",
], size=14, line_spacing=1.5)
whale_and_footer(s, 9, TOTAL)


# ============================================================
# SLIDE 10 — YAML – Pod Descriptor  (TERMINAL)
# ============================================================
s = new_slide()
title(s, "YAML – Pod Descriptor")
terminal(s, Inches(0.55), Inches(1.40), Inches(12.2), Inches(5.20),
         "kubectl get po kubia-zxzij -o yaml",
         [[("apiVersion: v1", TERM_GRAY)],
          [("kind: Pod", TERM_GRAY)],
          [("metadata:", TERM_GRAY)],
          [("  annotations:", TERM_GRAY)],
          [("    kubernetes.io/created-by: ...", TERM_GRAY)],
          [("  creationTimestamp: 2016-03-18T12:37:50Z", TERM_GRAY)],
          [("  generateName: kubia-", TERM_GRAY)],
          [("  labels:", TERM_GRAY)],
          [("    run: kubia", TERM_GRAY)],
          [("  name: kubia-zxzij", TERM_GRAY)],
          [("  namespace: default", TERM_GRAY)],
          [("  resourceVersion: \"294\"", TERM_GRAY)],
          [("  selfLink: /api/v1/namespaces/default/pods/kubia-zxzij", TERM_GRAY)],
          [("  uid: 3a564dc0-ed06-11e5-ba3b-42010af00004", TERM_GRAY)],
          [("spec:", TERM_GRAY)],
          [("  containers:", TERM_GRAY)],
          [("  - image: luksa/kubia", TERM_GRAY)],
          [("    imagePullPolicy: IfNotPresent", TERM_GRAY)],
          [("    name: kubia", TERM_GRAY)],
          [("    ports:", TERM_GRAY)],
          [("    - containerPort: 8080", TERM_GRAY)],
          [("      protocol: TCP", TERM_GRAY)]],
         font_size=11)
whale_and_footer(s, 10, TOTAL)


# ============================================================
# SLIDE 11 — Creating Pods from Descriptor
# ============================================================
s = new_slide()
title(s, "Creating Pods from Descriptor")
terminal(s, Inches(0.55), Inches(1.55), Inches(12.2), Inches(4.95),
         "kubia-manual.yaml",
         [[("apiVersion: v1", TERM_GRAY)],
          [("kind: Pod", TERM_GRAY)],
          [("metadata:", TERM_GRAY)],
          [("  name: kubia-manual", TERM_GRAY)],
          [("spec:", TERM_GRAY)],
          [("  containers:", TERM_GRAY)],
          [("  - image: luksa/kubia", TERM_GRAY)],
          [("    name: kubia", TERM_GRAY)],
          [("    ports:", TERM_GRAY)],
          [("    - containerPort: 8080", TERM_GRAY)],
          [("      protocol: TCP", TERM_GRAY)]],
         font_size=13)
whale_and_footer(s, 11, TOTAL)


# ============================================================
# SLIDE 12 — Pods: Summary
# ============================================================
s = new_slide()
title(s, "Pods: Summary")
bullet_list(s, 1.55, [
    "Can have one or multiple containers",
    "Runs on a single node",
    "(Pod cannot \"straddle\" multiple nodes)",
    "Pods cannot be moved (e.g. in case of node outage)",
    "Pods cannot be scaled vertically (except by manually creating more Pods)",
], size=16, line_spacing=1.6)
whale_and_footer(s, 12, TOTAL)


# ============================================================
# SLIDE 13 — Pods: Summary Continued
# ============================================================
s = new_slide()
title(s, "Pods: Summary Continued")
bullet_list(s, 1.40, [
    "Pod is not a process; it's an environment for containers",
    "it cannot be \"restarted\"",
    "it cannot \"crash\"",
    "The containers in a Pod can crash",
    "They may or may not get restarted",
    "(depending on Pod's restart policy)",
    "If all containers exit successfully, the Pod ends in \"Succeeded\" phase",
    "If some containers fail and don't get restarted, the Pod ends in \"Failed\" phase",
], size=13, line_spacing=1.45)
whale_and_footer(s, 13, TOTAL)


# ============================================================
# SLIDE 14 — Organizing K8s Objects with Labels  (DIAGRAM)
# ============================================================
s = new_slide()
title(s, "Organizing K8s Objects with Labels")

# Grid of colored pod boxes scattered
pod_kinds = [
    ("Shopping\nCart pod",   STEPS[1]),
    ("Product\nCatalog pod", STEPS[2]),
    ("Order\nService pod",   STEPS[3]),
    ("UI pod",               MUTED),
    ("Account\nService pod", ALERT_RED),
]
# 18 random-ish placements within content area
import random
random.seed(5)
positions = [(x, y) for x in [1.0, 2.6, 4.2, 5.8, 7.4, 9.0, 10.6] for y in [1.6, 3.0, 4.4, 5.4]]
random.shuffle(positions)
positions = positions[:18]
pod_w = Inches(1.45); pod_h = Inches(0.85)
for i, (px, py) in enumerate(positions):
    label, color = pod_kinds[i % len(pod_kinds)]
    add_rounded_rect(s, Inches(px), Inches(py), pod_w, pod_h,
                     color, line=SLATE, line_width=0.6, radius_ratio=0.18)
    add_text(s, Inches(px), Inches(py), pod_w, pod_h, label,
             size=10, bold=True, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
             line_spacing=1.10)

whale_and_footer(s, 14, TOTAL)


# ============================================================
# SLIDE 15 — Labels in K8s
# ============================================================
s = new_slide()
title(s, "Labels in K8s")
bullet_list(s, 1.55, [
    "Arbitrary key-value pairs added to resource manifest",
    "Used by label selectors",
    "Added to metadata section of the manifest",
], size=15, line_spacing=1.6)
add_text(s, Inches(0.55), Inches(4.40), Inches(12.2), Inches(0.40),
         "Example", size=14, bold=True, color=SLATE)
bullet_list(s, 4.85, ["App", "Release"], size=15, line_spacing=1.6)
whale_and_footer(s, 15, TOTAL)


# ============================================================
# SLIDE 16 — Scaling Pods
# ============================================================
s = new_slide()
title(s, "Scaling Pods")
# Table-like layout with the source content
row1_y = Inches(1.60); row1_h = Inches(1.10)
add_line(s, Inches(0.55), row1_y, Inches(12.78), row1_y, color=RULE_GRAY, width=0.75)
add_text(s, Inches(0.55), row1_y + Inches(0.15), Inches(3.0), Inches(0.85),
         "Task: We need to create multiple containers of the same type",
         size=14, color=BODY, line_spacing=1.35)

row2_y = row1_y + row1_h; row2_h = Inches(1.50)
add_line(s, Inches(0.55), row2_y, Inches(12.78), row2_y, color=RULE_GRAY, width=0.75)
add_text(s, Inches(0.55), row2_y + Inches(0.15), Inches(3.0), Inches(0.40),
         "We can run the commands below multiple times",
         size=13, color=BODY, line_spacing=1.35)
add_text(s, Inches(3.80), row2_y + Inches(0.15), Inches(9.0), Inches(0.50),
         "kubectl run kubia –image luksa/kubia",
         size=18, color=SLATE, font=FONT_MONO)
add_text(s, Inches(3.80), row2_y + Inches(0.85), Inches(9.0), Inches(0.50),
         "kubectl create –f kubia-descriptor.yaml",
         size=18, color=SLATE, font=FONT_MONO)

row3_y = row2_y + row2_h; row3_h = Inches(0.80)
add_line(s, Inches(0.55), row3_y, Inches(12.78), row3_y, color=RULE_GRAY, width=0.75)
add_text(s, Inches(0.55), row3_y + Inches(0.20), Inches(3.0), Inches(0.40),
         "Is it the right way to scale?", size=14, color=BODY)
add_line(s, Inches(0.55), row3_y + row3_h, Inches(12.78), row3_y + row3_h, color=RULE_GRAY, width=0.75)

whale_and_footer(s, 16, TOTAL)


# ============================================================
# SLIDE 17 — Creating ReplicaSet from Descriptor
# YAML rendered line-by-line so the red box can sit on known Y coordinates.
# ============================================================
s = new_slide()
title(s, "Creating ReplicaSet from Descriptor")
add_text(s, Inches(0.55), Inches(1.65), Inches(5.5), Inches(0.45),
         "Why do we need it?", size=15, color=BODY)
bullet_list(s, 2.20, [
    "High Availability",
    "Load balancing & Scaling",
], size=15, line_spacing=1.7, x=0.55, max_w=5.5)
add_text(s, Inches(0.55), Inches(4.65), Inches(5.5), Inches(0.40),
         "POD Definition", size=15, bold=True, color=ALERT_RED)

# Terminal frame (background + title bar + traffic-light dots + title text)
term_x = Inches(6.30); term_y = Inches(1.45)
term_w = Inches(6.5);  term_h = Inches(5.05)
add_rect(s, term_x, term_y, term_w, term_h, TERMBG)
bar_h = Inches(0.32)
add_rect(s, term_x, term_y, term_w, bar_h, RGBColor(0x3A, 0x3A, 0x3A))
dot_d = Inches(0.13); dot_y = term_y + Inches(0.10)
add_oval(s, term_x + Inches(0.15), dot_y, dot_d, dot_d, TERM_RED)
add_oval(s, term_x + Inches(0.32), dot_y, dot_d, dot_d, TERM_YEL)
add_oval(s, term_x + Inches(0.49), dot_y, dot_d, dot_d, TERM_GRN)
add_text(s, term_x, term_y + Inches(0.04), term_w, bar_h,
         "replicaset-definition.yml",
         font=FONT_SANS, size=10, color=TERM_GRAY,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# YAML — one textbox per line so the red box can target an exact span
yaml_x  = term_x + Inches(0.18)
yaml_y0 = term_y + bar_h + Inches(0.10)
line_h  = Inches(0.22)
yaml_lines = [
    ("apiVersion: apps/v1",              TERM_CYAN),
    ("kind: ReplicaSet",                 TERM_CYAN),
    ("metadata:",                        TERM_CYAN),
    ("  name: myapp-replicaset",         TERM_GRAY),
    ("  labels:",                        TERM_GRAY),
    ("    app: myapp",                   TERM_GRAY),
    ("    type: front-end",              TERM_GRAY),
    ("spec:",                            TERM_CYAN),
    ("  template:",                      TERM_GRAY),
    ("    metadata:",                    TERM_GRAY),   # 9  — pod template begins
    ("      name: myapp-pod",            TERM_GRAY),
    ("      labels:",                    TERM_GRAY),
    ("        app: myapp",               TERM_GRAY),
    ("        type: front-end",          TERM_GRAY),
    ("    spec:",                        TERM_GRAY),
    ("      containers:",                TERM_GRAY),
    ("      - name: nginx-container",    TERM_GRAY),
    ("        image: nginx",             TERM_GRAY),   # 17 — pod template ends
    ("  replicas: 3",                    TERM_GRAY),
    ("  selector:",                      TERM_GRAY),
    ("    matchLabels:",                 TERM_GRAY),
    ("      type: front-end",            TERM_GRAY),
]
for i, (txt, color) in enumerate(yaml_lines):
    add_text(s, yaml_x, yaml_y0 + line_h * i,
             term_w - Inches(0.36), Inches(0.22),
             txt, font=FONT_MONO, size=10.5, color=color,
             line_spacing=1.0)

# Red outlined box around the pod template section (lines 9..17 inclusive)
box_top   = yaml_y0 + line_h * 9 - Inches(0.04)
box_bot   = yaml_y0 + line_h * 18 + Inches(0.04)
box_left  = term_x + Inches(0.20)
box_right = term_x + term_w - Inches(0.20)
add_rect_outlined(s, box_left, box_top,
                  box_right - box_left, box_bot - box_top,
                  ALERT_RED, line_width=2.5)

# Red arrow from "POD Definition" → upper-left area of the red box
arrow_start_x = Inches(2.20)
arrow_start_y = Inches(4.85)
arrow_end_x   = box_left + Inches(0.10)
arrow_end_y   = box_top + Inches(0.55)
add_arrow(s, arrow_start_x, arrow_start_y,
             arrow_end_x, arrow_end_y,
          color=ALERT_RED, width=2.5)

whale_and_footer(s, 17, TOTAL)


# ============================================================
# SLIDE 18 — How does ReplicaSet know what to Monitor?  (DIAGRAM)
# ============================================================
s = new_slide()
title(s, "How does ReplicaSet know what to Monitor?")

# Grid of pod boxes, some highlighted with "tier: front-end" label
add_text(s, Inches(0.55), Inches(1.50), Inches(12.2), Inches(0.35),
         "Labels and Selectors", size=14, bold=True, color=SLATE,
         align=PP_ALIGN.CENTER)

# Background area
add_rect(s, Inches(0.55), Inches(1.95), Inches(12.2), Inches(4.55),
         CARD_BG)

# replicaset selector card (top-left)
add_rect(s, Inches(0.85), Inches(2.10), Inches(3.4), Inches(0.85), TERMBG)
add_text(s, Inches(0.95), Inches(2.15), Inches(3.2), Inches(0.30),
         "replicaset-definition.yml",
         size=9, color=TERM_GRAY, font=FONT_MONO)
add_text(s, Inches(0.95), Inches(2.40), Inches(3.2), Inches(0.50),
         "selector:\n  matchLabels:\n    tier: front-end",
         size=9, color=TERM_CYAN, font=FONT_MONO, line_spacing=1.1)

# pod selector card (top-right)
add_rect(s, Inches(9.05), Inches(2.10), Inches(3.4), Inches(0.85), TERMBG)
add_text(s, Inches(9.15), Inches(2.15), Inches(3.2), Inches(0.30),
         "pod-definition.yml",
         size=9, color=TERM_GRAY, font=FONT_MONO)
add_text(s, Inches(9.15), Inches(2.40), Inches(3.2), Inches(0.50),
         "metadata:\n  labels:\n    tier: front-end",
         size=9, color=TERM_CYAN, font=FONT_MONO, line_spacing=1.1)

# Grid of pods — 3 highlighted (front-end), rest faded
import random
random.seed(7)
positions = []
for r in range(3):
    for c in range(6):
        positions.append((Inches(1.0 + c * 1.85), Inches(3.25 + r * 0.95)))
random.shuffle(positions)
highlight_idx = {0, 5, 11}
for i, (px, py) in enumerate(positions):
    pw = Inches(1.40); ph = Inches(0.75)
    fill = STEPS[0] if i in highlight_idx else LIGHTBLUE
    add_rect(s, px, py, pw, ph, fill, line=SLATE, line_width=0.4)
    add_text(s, px, py, pw, ph, "POD",
             size=9, bold=True,
             color=WHITE if i in highlight_idx else MUTED,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
             font=FONT_MONO)
    if i in highlight_idx:
        # small "tier: front-end" tag
        tag_x = px + pw + Inches(0.05)
        add_rect(s, tag_x, py + Inches(0.20), Inches(0.95), Inches(0.32),
                 TERM_YEL)
        add_text(s, tag_x, py + Inches(0.20), Inches(0.95), Inches(0.32),
                 "tier: front-end", size=7.5, bold=True, color=SLATE,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
                 font=FONT_MONO)

whale_and_footer(s, 18, TOTAL)


# ============================================================
# SLIDE 19 — Creating ReplicaSet from Descriptor
# ============================================================
s = new_slide()
title(s, "Creating ReplicaSet from Descriptor")
terminal(s, Inches(0.55), Inches(1.55), Inches(12.2), Inches(5.05),
         "kubectl",
         [[("$ kubectl apply -f replicaset-definition.yml", TERM_CYAN)],
          [("replicaset.apps/myapp-replicaset created", TERM_GRAY)],
          [],
          [("$ kubectl get replicasets", TERM_CYAN)],
          [("NAME                DESIRED   CURRENT   READY   AGE", TERM_GRAY)],
          [("myapp-replicaset    3         3         3       12s", TERM_GRAY)],
          [],
          [("$ kubectl get pods", TERM_CYAN)],
          [("NAME                       READY   STATUS    RESTARTS   AGE", TERM_GRAY)],
          [("myapp-replicaset-abcde     1/1     Running   0          15s", TERM_GRAY)],
          [("myapp-replicaset-fghij     1/1     Running   0          15s", TERM_GRAY)],
          [("myapp-replicaset-klmno     1/1     Running   0          15s", TERM_GRAY)]],
         font_size=12)
whale_and_footer(s, 19, TOTAL)


# ============================================================
# SLIDE 20 — Scaling Pods - ReplicaSet
# ============================================================
s = new_slide()
title(s, "Scaling Pods - ReplicaSet")
bullet_list(s, 1.40, [
    "Set of identical (replicated) Pods",
    "Defined by a pod template + number of desired replicas",
    "If there are not enough Pods, the Replica Set creates more (e.g. in case of node outage; or simply when scaling up)",
    "If there are too many Pods, the Replica Set deletes some (e.g. if a node was disconnected and comes back; or when scaling down)",
    "We can scale up/down a Replica Set",
    "we update the manifest of the Replica Set",
    "as a consequence, the Replica Set controller creates/deletes Pods",
], size=13, line_spacing=1.45)
whale_and_footer(s, 20, TOTAL)


# ============================================================
# SLIDE 21 — K8 Objects - Hierachy  (DIAGRAM)
# ============================================================
s = new_slide()
title(s, "K8 Objects - Hierachy")

# Vertical hierarchy similar to v04 slide 34
dx = Inches(3.40); dy = Inches(1.50); dw = Inches(6.50); dh = Inches(0.70)
add_rounded_rect(s, dx, dy, dw, dh, STEPS[1], radius_ratio=0.20)
add_text(s, dx, dy, dw, dh, "DEPLOYMENT",
         size=15, bold=True, color=WHITE, font=FONT_MONO,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

rs_y = Inches(2.75); rs_w = Inches(1.80); rs_h = Inches(0.90)
rs_xs = [dx + Inches(0.50), dx + Inches(2.35), dx + Inches(4.20)]
rs_versions = ["v1", "v2", "v3"]
rs_colors = [BLUE, STEPS[1], STEPS[2]]
for rsx, ver, col in zip(rs_xs, rs_versions, rs_colors):
    add_rect(s, rsx, rs_y, rs_w, rs_h, col)
    add_text(s, rsx, rs_y, rs_w, Inches(0.40),
             "REPLICA SET", size=9.5, bold=True, color=WHITE,
             font=FONT_MONO,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, rsx, rs_y + Inches(0.40), rs_w, Inches(0.50), ver,
             size=18, bold=True, color=WHITE, font=FONT_MONO,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_line(s, rsx + rs_w / 2, rs_y, dx + dw / 2, dy + dh,
             color=SLATE, width=0.75)

pod_y = Inches(4.05); pod_w = Inches(0.75); pod_h = Inches(0.65)
pod_xs_all = []
for rsx, col in zip(rs_xs, rs_colors):
    p1x = rsx + Inches(0.10)
    p2x = rsx + rs_w - pod_w - Inches(0.10)
    for pxx in [p1x, p2x]:
        add_oval(s, pxx, pod_y, pod_w, pod_h, WHITE,
                 line=col, line_width=1.5)
        add_text(s, pxx, pod_y, pod_w, pod_h, "POD",
                 size=9.5, bold=True, color=col, font=FONT_MONO,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        pod_xs_all.append(pxx + pod_w / 2)
        add_line(s, rsx + rs_w / 2, rs_y + rs_h,
                 pxx + pod_w / 2, pod_y, color=col, width=0.5)

node_y = Inches(5.30); node_w = Inches(1.70); node_h = Inches(1.10)
node_xs = [dx + Inches(0.30), dx + Inches(2.45), dx + Inches(4.60)]
for nxx in node_xs:
    add_hex(s, nxx, node_y, node_w, node_h, CARD_BG,
            line=BLUE, line_width=1.5)
    add_text(s, nxx, node_y, node_w, node_h, "NODE",
             size=12, bold=True, color=BLUE, font=FONT_MONO,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
for pcx in pod_xs_all:
    nxx = node_xs[hash(int(pcx * 100)) % 3]
    add_line(s, pcx, pod_y + pod_h,
             nxx + node_w / 2, node_y + Inches(0.20),
             color=MUTED, width=0.5)

# Left labels
labels = [("Deployment", dy + dh / 2),
          ("ReplicaSet", rs_y + rs_h / 2),
          ("Pods",       pod_y + pod_h / 2),
          ("Nodes",      node_y + node_h / 2)]
for lbl, yc in labels:
    add_text(s, Inches(0.55), yc - Inches(0.16), Inches(2.7),
             Inches(0.32), lbl, size=13, bold=True, color=SLATE)

whale_and_footer(s, 21, TOTAL)


# ============================================================
# SLIDE 22 — Pods -> ReplicaSets -> Deployments
# ============================================================
s = new_slide()
title(s, "Pods -> ReplicaSets -> Deployments")
bullet_list(s, 1.40, [
    "Replica Sets control identical Pods",
    "Deployments are used to roll out different Pods (different image, command, environment variables, ...)",
    "When we update a Deployment with a new Pod definition:",
    "a new Replica Set is created with the new Pod definition",
    "that new Replica Set is progressively scaled up",
    "meanwhile, the old Replica Set(s) is(are) scaled down",
    "This is a rolling update, minimizing application downtime",
    "When we scale up/down a Deployment, it scales up/down its Replica Set",
], size=13, line_spacing=1.45)
whale_and_footer(s, 22, TOTAL)


# ============================================================
# SLIDE 23 — Descriptor: Deployment  (TERMINAL)
# ============================================================
s = new_slide()
title(s, "Descriptor: Deployment")
terminal(s, Inches(0.55), Inches(1.55), Inches(12.2), Inches(5.05),
         "deployment-definition.yml",
         [[("apiVersion: apps/v1", TERM_CYAN)],
          [("kind: Deployment", TERM_CYAN)],
          [("metadata:", TERM_CYAN)],
          [("  name: myapp-deployment", TERM_GRAY)],
          [("  labels:", TERM_GRAY)],
          [("    app: myapp", TERM_GRAY)],
          [("    type: front-end", TERM_GRAY)],
          [("spec:", TERM_CYAN)],
          [("  template:", TERM_GRAY)],
          [("    metadata:", TERM_GRAY)],
          [("      name: myapp-pod", TERM_GRAY)],
          [("      labels:", TERM_GRAY)],
          [("        app: myapp", TERM_GRAY)],
          [("        type: front-end", TERM_GRAY)],
          [("    spec:", TERM_GRAY)],
          [("      containers:", TERM_GRAY)],
          [("      - name: nginx-container", TERM_GRAY)],
          [("        image: nginx", TERM_GRAY)],
          [("  replicas: 3", TERM_GRAY)],
          [("  selector:", TERM_GRAY)],
          [("    matchLabels:", TERM_GRAY)],
          [("      type: front-end", TERM_GRAY)]],
         font_size=11)
whale_and_footer(s, 23, TOTAL)


# ============================================================
# SLIDE 24 — Organizing Pods - Namespaces
# ============================================================
s = new_slide()
title(s, "Organizing Pods - Namespaces")
bullet_list(s, 1.55, [
    "Provide scope for object names",
    "Allows to organize complex systems into distinct groups",
    "Not all resources are namespaced",
    "Nodes",
    "Cluster Roles",
], size=15, line_spacing=1.6)
whale_and_footer(s, 24, TOTAL)


# ============================================================
# SLIDE 25 — Workshop 1 – Deployment of K8s Pod
# ============================================================
s = new_slide()
d = Inches(1.6); cx = Inches(13.333 / 2) - d / 2
add_oval(s, cx, Inches(1.7), d, d, SLATE)
add_text(s, cx, Inches(1.7), d, d, "LAB",
         size=24, bold=True, color=WHITE,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(0.55), Inches(3.80), Inches(12.2), Inches(0.7),
         "Workshop 1 – Deployment of K8s Pod",
         size=32, bold=True, color=SLATE, align=PP_ALIGN.CENTER)
whale_and_footer(s, 25, TOTAL)


# ============================================================
# SLIDE 26 — Deployment of K8s Pod  - Prerequisites  (title only)
# ============================================================
s = new_slide()
title(s, "Deployment of K8s Pod  - Prerequisites")
whale_and_footer(s, 26, TOTAL)


# ============================================================
# SLIDE 27 — Preparing the cluster  (title only)
# ============================================================
s = new_slide()
title(s, "Preparing the cluster")
whale_and_footer(s, 27, TOTAL)


# ============================================================
# SLIDE 28 — Nginx pod deployment
# ============================================================
s = new_slide()
title(s, "Niginx pod deployment")
terminal(s, Inches(0.55), Inches(1.45), Inches(12.2), Inches(5.10),
         "bash",
         [[("# Creating nginx pod", TERM_GRN)],
          [("$ kubectl run nginx --image nginx", TERM_CYAN)],
          [],
          [("# List all pods in a default namespace", TERM_GRN)],
          [("$ kubectl  get pods", TERM_CYAN)],
          [],
          [("# List all pods in all namespaces", TERM_GRN)],
          [("$ kubectl  get pods --all-namespaces", TERM_CYAN)],
          [],
          [("# Retrieve pod's descriptor", TERM_GRN)],
          [("$ kubectl  get pod nginx -o yaml", TERM_CYAN)],
          [],
          [("# Access nginx web server running in a pod", TERM_GRN)],
          [("$ kubectl port-forward nginx 8080:80", TERM_CYAN)],
          [("$ curl localhost:8080 # Send this command in a new terminal session", TERM_CYAN)]],
         font_size=11)
whale_and_footer(s, 28, TOTAL)


# ============================================================
# SLIDE 29 — Create pod manifest
# ============================================================
s = new_slide()
title(s, "Create pod manifest")
terminal(s, Inches(0.55), Inches(1.55), Inches(12.2), Inches(4.85),
         "bash",
         [[("# Create a manifest file", TERM_GRN)],
          [("$ alias k=kubectl", TERM_CYAN)],
          [("k run kubia --image luksa/kubia --dry-run=client -o yaml > kubia-manual.yaml", TERM_CYAN)],
          [],
          [("# Edit the manifest and create the pod", TERM_GRN)],
          [("k apply –f kubia-manual.yaml", TERM_CYAN)]],
         font_size=13)
whale_and_footer(s, 29, TOTAL)


# ============================================================
# SLIDE 30 — Kubia deployment with YAML manifest
# ============================================================
s = new_slide()
title(s, "Kubia deployment with YAML manifest")
terminal(s, Inches(0.55), Inches(1.45), Inches(12.2), Inches(5.10),
         "bash",
         [[("$ kubectl explain pods", TERM_CYAN)],
          [("$ kubectl explain pod.spec", TERM_CYAN)],
          [("$ kubectl create -f kubia-manual.yaml", TERM_CYAN)],
          [("$ kubectl get po kubia-manual -o yaml", TERM_CYAN)],
          [("$ kubectl logs kubia-manual", TERM_CYAN)],
          [("$ kubectl logs kubia-manual -c kubia", TERM_CYAN)],
          [("$ kubectl port-forward kubia-manual 8888:8080", TERM_CYAN)],
          [("$ curl localhost:8888", TERM_CYAN)]],
         font_size=13)
whale_and_footer(s, 30, TOTAL)


# ============================================================
# SLIDE 31 — Retrieving logs - Pingpong
# ============================================================
s = new_slide()
title(s, "Retrieving logs - Pingpong")
terminal(s, Inches(0.55), Inches(1.45), Inches(12.2), Inches(5.10),
         "bash",
         [[("# Get logs of the pod. By default, the command will only show the logs of the first container in the pod", TERM_GRN)],
          [("$ kubectl run pingpong --image alpine ping 127.0.0.1", TERM_CYAN)],
          [("$ kubectl logs pingpong", TERM_CYAN)],
          [("$ kubectl logs pingpong –c pingpong", TERM_CYAN)],
          [("$ kubectl logs pingpong --tail 1 --follow", TERM_CYAN)],
          [],
          [("# Full definition of the running pod", TERM_GRN)],
          [("$ kubectl get po  pingpong -o yaml", TERM_CYAN)]],
         font_size=12)
whale_and_footer(s, 31, TOTAL)


# ============================================================
# SLIDE 32 — Can we scale the pod? Deployments  => ReplicaSets => Pods
# ============================================================
s = new_slide()
title(s, "Can we scale the pod? Deployments  => ReplicaSets => Pods")
terminal(s, Inches(0.55), Inches(1.55), Inches(12.2), Inches(4.95),
         "bash",
         [[("# Let's try scaling the pod", TERM_GRN)],
          [("$ kubectl scale pod pingpong --replicas=3", TERM_CYAN)],
          [],
          [("# Let's create a deployment of the pingpong in it's own namespace", TERM_GRN)],
          [("alias k=kubectl", TERM_CYAN)],
          [("k create ns pingpong", TERM_CYAN)],
          [("kubectl create deployment pingpong --image=alpine:3.14 -n pingpong -- ping 127.0.0.1", TERM_CYAN)],
          [("kubectl get all –n pingpong", TERM_CYAN)]],
         font_size=12)
whale_and_footer(s, 32, TOTAL)


# ============================================================
# SLIDE 33 — Descriptor: Deployment
# ============================================================
s = new_slide()
title(s, "Descriptor: Deployment")
bullet_list(s, 1.45, [
    "Responsible for multiple versions of application (replicasets)",
    "Defines the way to perform rolling forward and rollback updates",
    "Does it by using ReplicaSets",
], size=15, line_spacing=1.55)
terminal(s, Inches(0.55), Inches(4.20), Inches(12.2), Inches(2.30),
         "bash",
         [[("k get deployment pingpong  -n pingpong -o yaml", TERM_CYAN)]],
         font_size=14)
whale_and_footer(s, 33, TOTAL)


# ============================================================
# SLIDE 34 — Descriptor: ReplicaSet  (title only)
# ============================================================
s = new_slide()
title(s, "Descriptor: ReplicaSet")
whale_and_footer(s, 34, TOTAL)


# ============================================================
# SLIDE 35 — Descriptor: Pod  (title only)
# ============================================================
s = new_slide()
title(s, "Descriptor: Pod")
whale_and_footer(s, 35, TOTAL)


# ============================================================
# SLIDE 36 — Scaling
# ============================================================
s = new_slide()
title(s, "Scaling")
terminal(s, Inches(0.55), Inches(1.55), Inches(12.2), Inches(4.85),
         "bash",
         [[("k scale deployment pingpong --replicas 3 -n pingpong", TERM_CYAN)],
          [("k scale deployment pingpong --replicas 1 -n pingpong", TERM_CYAN)]],
         font_size=15)
whale_and_footer(s, 36, TOTAL)


# ============================================================
# SLIDE 37 — Rolling out a new version – Updating alpine version to 3.15
# ============================================================
s = new_slide()
title(s, "Rolling out a new version – Updating alpine version to 3.15")
whale_and_footer(s, 37, TOTAL)


# ============================================================
# SLIDE 38 — Maintaining the desired state - Resilience
# ============================================================
s = new_slide()
title(s, "Maintaining the desired state - Resilience")
terminal(s, Inches(0.55), Inches(1.45), Inches(12.2), Inches(3.50),
         "bash",
         [[("watch kubectl get pods", TERM_CYAN)],
          [("kubectl delete pod pingpong-xxxxxxxxxx-yyyyy", TERM_CYAN)]],
         font_size=14)
add_text(s, Inches(0.55), Inches(5.20), Inches(12.2), Inches(0.40),
         "As soon as the pod is in \"Terminating\" state, the Replica Set replaces it",
         size=15, color=BODY)
add_text(s, Inches(0.55), Inches(5.85), Inches(12.2), Inches(0.40),
         "What will happen if we terminate the \"stand-alone\" pod?",
         size=15, color=BODY, italic=True)
whale_and_footer(s, 38, TOTAL)


# ============================================================
# SLIDE 39 — Workshop 1 – The End  (title only)
# ============================================================
s = new_slide()
title(s, "Workshop 1 – The End")
whale_and_footer(s, 39, TOTAL)


# ===== Save =====
_sanitize_coords(prs)   # final safety net: integer-coerce any float EMU coords
out = f"Week05/Week05_lab_style_{VERSION}.pptx"
prs.save(out)
print(f"wrote {out}")
