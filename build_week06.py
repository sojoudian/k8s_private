"""Week06_lab_style — Lab02/Week05 design language applied to Week6.pptx.

Source: Week06/Week6.pptx (71 slides: Deployment Rollouts, Labels & Selectors,
Services, + 4 workshops). Original slide text preserved verbatim (no rephrasing,
no invented body). Hybrid diagram treatment (per user choice):
  - command / YAML slides  -> our dark terminal mockup (redrawn from verbatim text)
  - conceptual figures      -> original figure embedded from Week06/assets/
  - text slides             -> blue title + multi-level bullets
  - workshop boundaries      -> LAB section divider
  - Course Outline           -> redrawn natively with the CANONICAL schedule
                                (Week 8 = Break, Week 9 = EKS) per project memory.
Hidden source slides 22 and 57 are rebuilt and kept hidden. Footer numbers N / 71.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

CENTER, LEFT, RIGHT = PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.RIGHT
MIDDLE, TOP = MSO_ANCHOR.MIDDLE, MSO_ANCHOR.TOP

# === Lab02 palette (verbatim, matches DESIGN_LANGUAGE.md / build_week05.py) ===
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

K8S_LOGO   = "Week04/Kubernetes_logo_without_workmark.svg.png"
WHALE      = "whale.png"
ASSETS_DIR = "Week06/assets"
VERSION    = "v2"
TOTAL      = 71

# Native pixel sizes of every extracted figure (for distortion-free embedding).
ASPECT = {
    "s04_1.png": (719, 981), "s04_2.png": (860, 645), "s05_1.jpg": (2048, 1365),
    "s06_1.png": (1402, 463), "s06_2.png": (923, 512), "s07_1.png": (617, 480),
    "s08_1.png": (614, 485), "s09_1.png": (1508, 607), "s09_2.png": (1517, 598),
    "s10_1.png": (1228, 462), "s16_1.png": (975, 473), "s16_2.png": (1545, 893),
    "s16_3.png": (1212, 613), "s17_1.png": (1204, 503), "s17_2.png": (1277, 348),
    "s19_1.jpg": (2048, 1365), "s20_1.jpg": (2048, 1428), "s22_1.png": (2000, 1003),
    "s23_1.png": (2052, 1336), "s24_1.png": (2000, 1350), "s25_1.jpg": (2048, 1152),
    "s27_1.png": (1028, 519), "s29_1.png": (900, 435), "s30_1.png": (1608, 1707),
    "s31_1.png": (700, 811), "s32_1.png": (1478, 806), "s34_1.png": (1671, 832),
    "s35_1.png": (671, 391), "s36_1.png": (1236, 962), "s37_1.png": (807, 444),
    "s38_1.png": (1050, 368), "s39_1.png": (800, 332), "s39_2.png": (1004, 336),
    "s40_1.png": (2394, 1408), "s41_1.png": (756, 500), "s41_2.png": (1197, 453),
    "s42_1.png": (1274, 1078), "s43_1.png": (667, 509), "s43_2.png": (474, 461),
    "s44_1.png": (1340, 928), "s46_1.png": (1286, 370), "s47_1.png": (1239, 690),
    "s47_2.png": (1280, 716), "s49_1.png": (1082, 450), "s56_1.png": (518, 204),
    "s58_2.png": (689, 109), "s65_1.png": (887, 500), "s66_1.png": (1786, 1047),
    "s66_3.png": (1895, 1019), "s67_1.png": (383, 293), "s68_1.png": (1793, 969),
    "s68_2.png": (867, 587), "s71_1.jpg": (2048, 1365),
}


# ===== Coordinate-safety primitives (from build_week05.py) =====
def _i(v):
    return int(v) if isinstance(v, float) else v


def _sanitize_coords(prs):
    import re as _re
    DML = 'http://schemas.openxmlformats.org/drawingml/2006/main'
    targets = {f'{{{DML}}}off', f'{{{DML}}}ext', f'{{{DML}}}chOff', f'{{{DML}}}chExt'}
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


# ===== Base helpers =====
def add_text(s, x, y, w, h, text, *, font=FONT_SANS, size=14, bold=False,
             italic=False, color=BODY, align=LEFT, anchor=TOP, line_spacing=1.15):
    tb = s.shapes.add_textbox(_i(x), _i(y), _i(w), _i(h))
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Inches(0)
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


def add_rect(s, x, y, w, h, fill, line=None, line_width=0.75):
    shp = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, _i(x), _i(y), _i(w), _i(h))
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line; shp.line.width = Pt(line_width)
    shp.shadow.inherit = False
    return shp


def add_rounded_rect(s, x, y, w, h, fill, line=None, line_width=0.75, radius_ratio=0.10):
    shp = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, _i(x), _i(y), _i(w), _i(h))
    shp.adjustments[0] = radius_ratio
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line; shp.line.width = Pt(line_width)
    shp.shadow.inherit = False
    return shp


def add_oval(s, x, y, w, h, fill, line=None, line_width=0.75):
    shp = s.shapes.add_shape(MSO_SHAPE.OVAL, _i(x), _i(y), _i(w), _i(h))
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line; shp.line.width = Pt(line_width)
    shp.shadow.inherit = False
    return shp


def add_line(s, x1, y1, x2, y2, color=RULE_GRAY, width=0.75):
    ln = s.shapes.add_connector(1, _i(x1), _i(y1), _i(x2), _i(y2))
    ln.line.color.rgb = color; ln.line.width = Pt(width)
    return ln


def whale_and_footer(s, page_num, total=TOTAL):
    s.shapes.add_picture(WHALE, Inches(0.45), Inches(6.85), width=Inches(0.5), height=Inches(0.5))
    add_line(s, Inches(0.5), Inches(7.05), Inches(12.83), Inches(7.05), color=RULE_GRAY, width=0.5)
    add_text(s, Inches(9.5), Inches(7.12), Inches(3.35), Inches(0.3),
             f"CLO835, Fall 2026     {page_num} / {total}",
             size=10, color=FOOTER_GRAY, align=RIGHT)


def title(s, text, y=0.40, size=32):
    add_text(s, Inches(0.55), Inches(y), Inches(12.2), Inches(0.85),
             text, size=size, bold=True, color=BLUE, line_spacing=1.05)


# Multi-level bullets (the hierarchy fix the existing builders lacked).
_GLYPH = {0: "▪  ", 1: "–  ", 2: "•  "}
_GCOL  = {0: BLUE, 1: STEPS[1], 2: MUTED}
_MARG  = {0: 0.0, 1: 0.45, 2: 0.90}


def bullets(s, y, items, *, x=0.55, w=12.0, size=14, line_spacing=1.4, space_after=7):
    h = max(0.5, 7.5 - y - 0.8)
    tb = s.shapes.add_textbox(_i(Inches(x)), _i(Inches(y)), _i(Inches(w)), _i(Inches(h)))
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Inches(0)
    tf.word_wrap = True
    for i, it in enumerate(items):
        lvl, text = it[0], it[1]
        col = it[2] if len(it) > 2 else BODY
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = LEFT
        p.line_spacing = line_spacing
        p.space_after = Pt(space_after)
        pPr = p._p.get_or_add_pPr()
        pPr.set('marL', str(int(Inches(_MARG[lvl] + 0.25))))
        pPr.set('indent', str(-int(Inches(0.25))))
        sz = size - lvl
        r0 = p.add_run(); r0.text = _GLYPH[lvl]
        r0.font.name = FONT_SANS; r0.font.size = Pt(sz); r0.font.bold = True
        r0.font.color.rgb = _GCOL[lvl]
        r1 = p.add_run(); r1.text = text
        r1.font.name = FONT_SANS; r1.font.size = Pt(sz); r1.font.color.rgb = col
    return tb


def embed(s, fname, x, y, w, h, *, halign='center', valign='middle'):
    aw, ah = ASPECT[fname]
    ar = aw / ah
    if (w / h) > ar:
        dh = h; dw = h * ar
    else:
        dw = w; dh = w / ar
    dx = x + (w - dw) * (0.5 if halign == 'center' else (0.0 if halign == 'left' else 1.0))
    dy = y + (h - dh) * (0.5 if valign == 'middle' else (0.0 if valign == 'top' else 1.0))
    s.shapes.add_picture(os.path.join(ASSETS_DIR, fname),
                         _i(Inches(dx)), _i(Inches(dy)), _i(Inches(dw)), _i(Inches(dh)))


def terminal(s, x, y, w, h, title_text, body_runs, *, font_size=11):
    add_rect(s, x, y, w, h, TERMBG)
    bar_h = Inches(0.32)
    add_rect(s, x, y, w, bar_h, RGBColor(0x3A, 0x3A, 0x3A))
    dot_d = Inches(0.13); dot_y = y + Inches(0.10)
    add_oval(s, x + Inches(0.15), dot_y, dot_d, dot_d, TERM_RED)
    add_oval(s, x + Inches(0.32), dot_y, dot_d, dot_d, TERM_YEL)
    add_oval(s, x + Inches(0.49), dot_y, dot_d, dot_d, TERM_GRN)
    add_text(s, x, y + Inches(0.04), w, bar_h, title_text,
             font=FONT_SANS, size=10, color=TERM_GRAY, align=CENTER, anchor=MIDDLE)
    tb = s.shapes.add_textbox(x + Inches(0.18), y + bar_h + Inches(0.10),
                              w - Inches(0.32), h - bar_h - Inches(0.15))
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Inches(0)
    tf.word_wrap = True
    for i, para in enumerate(body_runs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = LEFT
        p.line_spacing = 1.15
        if not para:
            r = p.add_run(); r.text = " "
            r.font.name = FONT_MONO; r.font.size = Pt(font_size)
            continue
        for text, color in para:
            r = p.add_run(); r.text = text
            r.font.name = FONT_MONO; r.font.size = Pt(font_size); r.font.color.rgb = color


def _role(line):
    st = line.strip()
    if st == "":
        return None
    if st.startswith("#"):
        return TERM_GRN
    low = st.lower()
    if low.startswith("explain") or low.startswith("exlain"):
        return TERM_YEL
    if st.startswith("curl:") or "Failed to connect" in st or "refused" in st:
        return TERM_ERR
    if st.startswith("root@") or st.startswith("-bash"):
        return TERM_GRAY
    cmds = ("$", "k ", "K ", "kubectl", "scp", "ssh", "sudo", "docker",
            "curl", "cat", "watch", "alias")
    if any(st.startswith(c) for c in cmds):
        return TERM_CYAN
    return TERM_GRAY


def auto_term(s, x, y, w, h, title_text, raw, *, font_size=12):
    runs = [[] if (ln == "" or ln is None) else [(ln, _role(ln))] for ln in raw]
    terminal(s, Inches(x), Inches(y), Inches(w), Inches(h), title_text, runs, font_size=font_size)


def divider(s, text, subtitle=None):
    d = 1.6; cx = 13.333 / 2 - d / 2
    add_oval(s, Inches(cx), Inches(1.85), Inches(d), Inches(d), SLATE)
    add_text(s, Inches(cx), Inches(1.85), Inches(d), Inches(d), "LAB",
             size=24, bold=True, color=WHITE, align=CENTER, anchor=MIDDLE)
    add_text(s, Inches(0.8), Inches(3.95), Inches(11.73), Inches(0.95), text,
             size=30, bold=True, color=SLATE, align=CENTER, line_spacing=1.1)
    if subtitle:
        add_text(s, Inches(0.8), Inches(5.05), Inches(11.73), Inches(0.5), subtitle,
                 size=15, italic=True, color=MUTED, align=CENTER)


def figure_caption(s, text):
    add_text(s, Inches(0.55), Inches(1.30), Inches(12.2), Inches(0.32), text,
             size=13, bold=True, color=SLATE, align=CENTER)


# ===== Setup =====
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank = prs.slide_layouts[6]


def new_slide():
    return prs.slides.add_slide(blank)


def hide(s):
    s._element.set('show', '0')


# ============================================================
# SLIDE 1 — Cover
# ============================================================
s = new_slide()
add_text(s, Inches(0.7), Inches(2.30), Inches(8.7), Inches(2.0),
         "Kubernetes Core Concepts:\nDeployment Rollouts, Labels\nand Selectors, Services",
         size=30, bold=True, color=BLUE, line_spacing=1.12)
add_text(s, Inches(0.7), Inches(4.95), Inches(8.5), Inches(0.6), "Week 6", size=22, color=SLATE)
logo_cx = Inches(10.7); logo_cy = Inches(3.55); ring_r = Inches(1.8)
add_oval(s, logo_cx - ring_r, logo_cy - ring_r, ring_r * 2, ring_r * 2,
         WHITE, line=LIGHTBLUE, line_width=1.5)
s.shapes.add_picture(K8S_LOGO, logo_cx - Inches(1.25), logo_cy - Inches(1.25),
                     width=Inches(2.5), height=Inches(2.5))
s.shapes.add_picture(WHALE, Inches(0.45), Inches(6.85), width=Inches(0.5), height=Inches(0.5))
add_text(s, Inches(9.5), Inches(7.12), Inches(3.35), Inches(0.3),
         f"CLO835, Fall 2026     1 / {TOTAL}", size=10, color=FOOTER_GRAY, align=RIGHT)

# ============================================================
# SLIDE 2 — Agenda (modular: Rollouts / Deployments / Services).
# Source agenda was a SmartArt graphic that text-extraction missed, so an
# earlier pass wrongly built this title-only. The 3 items are verbatim.
# ============================================================
s = new_slide()
title(s, "Agenda")
_agenda = [("01", "Rollouts", STEPS[0]), ("02", "Deployments", STEPS[1]), ("03", "Services", STEPS[3])]
_acx, _acw, _ach, _ay0, _agap, _atile = 0.9, 11.5, 1.3, 1.8, 0.4, 0.95
for _ai, (_anum, _albl, _acol) in enumerate(_agenda):
    _acy = _ay0 + _ai * (_ach + _agap)
    add_rounded_rect(s, Inches(_acx), Inches(_acy), Inches(_acw), Inches(_ach),
                     CARD_BG, line=RULE_GRAY, line_width=0.75, radius_ratio=0.07)
    _aty = _acy + (_ach - _atile) / 2
    add_rounded_rect(s, Inches(_acx + 0.32), Inches(_aty), Inches(_atile), Inches(_atile),
                     _acol, radius_ratio=0.22)
    add_text(s, Inches(_acx + 0.32), Inches(_aty), Inches(_atile), Inches(_atile), _anum,
             font=FONT_MONO, size=20, bold=True, color=WHITE, align=CENTER, anchor=MIDDLE)
    add_text(s, Inches(_acx + 1.75), Inches(_acy), Inches(_acw - 2.3), Inches(_ach), _albl,
             size=26, bold=True, color=SLATE, anchor=MIDDLE)
whale_and_footer(s, 2)

# ============================================================
# SLIDE 3 — Course Outline (redrawn; CANONICAL schedule)
# ============================================================
s = new_slide()
title(s, "Course Outline")
weeks = [
    (1, "Docker Introduction"), (2, "Docker Image Management"),
    (3, "Docker Networking, Storage & Security"), (4, "K8s Introduction"),
    (5, "K8s – PODs, ReplicaSets"), (6, "K8s – Services & Deployments"),
    (7, "K8s – Volumes"), (8, "Break"), (9, "EKS + production patterns"),
    (10, "K8s – Storage Classes & StatefulSets"), (11, "K8s – ConfigMaps & Secrets"),
    (12, "Exam & Mock Exam week"), (13, "K8s – RBAC"),
    (14, "Helm Charts & Deployment Automation"), (None, "Term End"),
]
cw, ch, gx, gy = 2.30, 1.45, 0.18, 0.20
x0, y0 = 0.55, 1.70
for idx, (wk, topic) in enumerate(weeks):
    col = idx % 5; row = idx // 5
    cx = x0 + col * (cw + gx); cy = y0 + row * (ch + gy)
    if wk == 6:
        fill, txt, outline = BLUE, WHITE, None
    elif wk == 8:
        fill, txt, outline = SLATE, WHITE, None
    elif wk is None:
        fill, txt, outline = CARD_BG, SLATE, RULE_GRAY
    else:
        fill, txt, outline = WHITE, SLATE, RULE_GRAY
    add_rounded_rect(s, Inches(cx), Inches(cy), Inches(cw), Inches(ch),
                     fill, line=outline, line_width=1.0, radius_ratio=0.07)
    label = (f"Week {wk}\n{topic}" if wk is not None else topic)
    add_text(s, Inches(cx + 0.12), Inches(cy), Inches(cw - 0.24), Inches(ch),
             label, size=12, bold=True, color=txt,
             align=CENTER, anchor=MIDDLE, line_spacing=1.12)
whale_and_footer(s, 3)

# ============================================================
# SLIDE 4 — Deployment Recap
# ============================================================
s = new_slide()
title(s, "Deployment Recap")
bullets(s, 1.55, [
    (0, "Deployment object comes higher in the hierarchy (POD → ReplicaSet → Deployment)"),
    (0, "Provides us with Capability to upgrade underlying instances seamlessly"),
    (1, "Rolling updates"),
    (1, "Undo Changes"),
    (1, "Pause and Resume Changes as needed"),
], x=0.55, w=5.7, size=14, line_spacing=1.45)
terminal(s, Inches(6.55), Inches(1.55), Inches(6.25), Inches(4.95),
         "deployment-definition.yml",
         [[("apiVersion: apps/v1", TERM_CYAN)], [("kind: Deployment", TERM_CYAN)],
          [("metadata:", TERM_CYAN)], [("  name: myapp-deployment", TERM_GRAY)],
          [("  labels:", TERM_GRAY)], [("    app: myapp", TERM_GRAY)],
          [("    type: front-end", TERM_GRAY)], [("spec:", TERM_CYAN)],
          [("  replicas: 3", TERM_GRAY)], [("  selector:", TERM_GRAY)],
          [("    matchLabels:", TERM_GRAY)], [("      type: front-end", TERM_GRAY)],
          [("  template:", TERM_GRAY)], [("    metadata:", TERM_GRAY)],
          [("      labels:", TERM_GRAY)], [("        type: front-end", TERM_GRAY)],
          [("    spec:", TERM_GRAY)], [("      containers:", TERM_GRAY)],
          [("      - name: nginx-container", TERM_GRAY)], [("        image: nginx", TERM_GRAY)]],
         font_size=11)
whale_and_footer(s, 4)

# ============================================================
# SLIDE 5 — Deployment Rollouts
# ============================================================
s = new_slide()
title(s, "Deployment Rollouts")
bullets(s, 1.60, [
    (0, "Rollout is a process or creating or upgrading application containers"),
    (0, "Rollout happens when"),
    (1, "We create a new deployment"),
    (1, "Update images used in the existing deployment"),
    (0, "Rollout creates a new deployment revision"),
    (0, "Revisions help in keeping history and enable rollback"),
], x=0.55, w=7.0, size=15, line_spacing=1.6)
embed(s, "s05_1.jpg", 8.0, 1.7, 4.8, 4.7)
whale_and_footer(s, 5)

# ============================================================
# SLIDE 6 — Rollout & Versioning
# ============================================================
s = new_slide()
title(s, "Rollout & Versioning")
embed(s, "s06_1.png", 0.55, 1.45, 12.2, 2.55, valign='top')
auto_term(s, 2.6, 4.25, 8.1, 2.25, "kubectl rollout", [
    "> kubectl rollout status deployment/myapp-deployment",
    "Waiting for rollout to finish: 9 of 10 updated replicas are available...",
    "deployment \"myapp-deployment\" successfully rolled out",
    "",
    "> kubectl rollout history deployment/myapp-deployment",
], font_size=11)
whale_and_footer(s, 6)

# ============================================================
# SLIDE 7 — Rollout Strategies: Rollout
# ============================================================
s = new_slide()
title(s, "Rollout Strategies: Rollout")
bullets(s, 2.3, [(0, "Default strategy"), (0, "No downtime")], x=0.55, w=4.3, size=16, line_spacing=1.7)
embed(s, "s07_1.png", 5.0, 1.45, 7.8, 5.0)
whale_and_footer(s, 7)

# ============================================================
# SLIDE 8 — Rollout Strategies: Recreate
# ============================================================
s = new_slide()
title(s, "Rollout Strategies: Recreate")
bullets(s, 2.3, [(0, "Application downtime"), (0, "Should be specified explicitly")],
        x=0.55, w=4.3, size=16, line_spacing=1.7)
embed(s, "s08_1.png", 5.0, 1.45, 7.8, 5.0)
whale_and_footer(s, 8)

# ============================================================
# SLIDE 9 — Deployment Strategy
# ============================================================
s = new_slide()
title(s, "Deployment Strategy")
embed(s, "s09_1.png", 0.7, 1.75, 11.9, 4.55)
whale_and_footer(s, 9)

# ============================================================
# SLIDE 10 — Summary
# ============================================================
s = new_slide()
title(s, "Summary")
embed(s, "s10_1.png", 1.0, 1.7, 11.3, 4.7)
whale_and_footer(s, 10)

# ============================================================
# SLIDE 11 — Workshop 1 divider
# ============================================================
s = new_slide()
divider(s, "Workshop 1 – Deployment Rollouts, Revisions and Rollbacks")
whale_and_footer(s, 11)

# ============================================================
# SLIDE 12 — Working with deployment (terminal)
# ============================================================
s = new_slide()
title(s, "Working with deployment")
auto_term(s, 0.55, 1.5, 12.2, 5.0, "bash", [
    "# Copy deployment file to the machine runnign kind K8s cluster",
    "scp -i week6 week6Session1/deployment.yaml <your public IP>:/tmp",
    "# Log into EC2, start docker daemon on EC2",
    "sudo systemctl start docker",
    "# Create new namespace and create and nginx deployment",
    "k create ns nginx",
    "k apply –f /tmp/deployment.yaml",
    "# Lets see the status of our deployment",
    "k rollout status deployment.apps/deployment-nginx  -n nginx",
    "k get all –n nginx",
    "# Why is there only one rollout?",
    "k rollout history deployment.apps/deployment-nginx  -n nginx",
], font_size=12)
whale_and_footer(s, 12)

# ============================================================
# SLIDE 13 — Creating Revisions (terminal)
# ============================================================
s = new_slide()
title(s, "Creating Revisions")
auto_term(s, 0.55, 1.5, 12.2, 5.0, "bash", [
    "# Re-create the deployment and record change history",
    "k apply -f /tmp/deployment.yaml --record",
    "k rollout history deployment.apps/deployment-nginx  -n nginx",
    "# Change nginx image version in the YAML",
    "k apply -f /tmp/deployment.yaml --record",
    "K get pods –n nginx",
    "# Change again with \"kubectl edit\"",
    "k edit deployment.apps/deployment-nginx -n nginx",
    "k rollout status deployment.apps/deployment-nginx  -n nginx",
], font_size=13)
whale_and_footer(s, 13)

# ============================================================
# SLIDE 14 — Rollback (terminal)
# ============================================================
s = new_slide()
title(s, "Rollback")
auto_term(s, 0.55, 1.45, 12.2, 5.1, "bash", [
    "# Rollback one revision",
    "k rollout undo deployment.apps/deployment-nginx  -n nginx",
    "k rollout history deployment.apps/deployment-nginx  -n nginx",
    "# Update deployment manifest to point to non-existent version on nginx",
    "k edit deployment.apps/deployment-nginx  -n nginx",
    "# Are the pods replaced with a new version?",
    "k get deployment.apps/deployment-nginx  -n nginx",
    "# Are the previous pods terminated?",
    "k get pods –n nginx",
    "# Let's roll back the unsuccessful deployment",
    "k rollout undo deployment.apps/deployment-nginx  -n nginx",
    "k get pods -n nginx",
], font_size=12)
whale_and_footer(s, 14)

# ============================================================
# SLIDE 15 — Workshop 1 — The End
# ============================================================
s = new_slide()
divider(s, "Workshop 1 – The End")
whale_and_footer(s, 15)

# ============================================================
# SLIDE 16 — Labels Recap (figures)
# ============================================================
s = new_slide()
title(s, "Labels Recap")
embed(s, "s16_2.png", 0.55, 1.5, 7.3, 5.0)
embed(s, "s16_3.png", 8.0, 2.6, 4.9, 3.4)
whale_and_footer(s, 16)

# ============================================================
# SLIDE 17 — Labels & Selectors (figures + terminal)
# ============================================================
s = new_slide()
title(s, "Labels & Selectors")
embed(s, "s17_1.png", 0.55, 1.55, 6.1, 3.3, valign='top')
embed(s, "s17_2.png", 6.85, 1.95, 6.0, 2.5, valign='top')
auto_term(s, 0.55, 5.35, 8.5, 1.0, "bash",
          ["$ kubectl get pods –selector app=App1"], font_size=14)
whale_and_footer(s, 17)

# ============================================================
# SLIDE 18 — Workshop 2 divider
# ============================================================
s = new_slide()
divider(s, "Workshop 2 – Using Labels to Organize K8s Pods")
whale_and_footer(s, 18)

# ============================================================
# SLIDE 19 — Assigning Labels to Pods (terminal)
# ============================================================
s = new_slide()
title(s, "Assigning Labels to Pods")
auto_term(s, 0.55, 1.55, 12.2, 4.9, "bash", [
    "$ kubectl create -f kubia-manual-with-labels.yaml",
    "$ kubectl get po --show-labels",
    "$ kubectl get po -L creation_method,env",
    "$ kubectl label po kubia-manual creation_method=manual",
    "$ kubectl label po kubia-manual-v2 env=debug --overwrite",
    "$ kubectl get po -L creation_method,env",
], font_size=13)
whale_and_footer(s, 19)

# ============================================================
# SLIDE 20 — Using Labels (terminal)
# ============================================================
s = new_slide()
title(s, "Using Labels")
auto_term(s, 0.55, 1.55, 12.2, 4.0, "bash", [
    "$ kubectl get po -l creation_method=manual",
    "$ kubectl get po -l env",
    "$ kubectl get po -l '!env'",
], font_size=14)
whale_and_footer(s, 20)

# ============================================================
# SLIDE 21 — Workshop 2 — The End
# ============================================================
s = new_slide()
divider(s, "Workshop 2 – The End")
whale_and_footer(s, 21)

# ============================================================
# SLIDE 22 — Services in the Traditional Environment (HIDDEN in source)
# ============================================================
s = new_slide()
title(s, "Services in the Traditional Environment")
embed(s, "s22_1.png", 1.4, 1.55, 10.5, 4.9)
whale_and_footer(s, 22)
hide(s)

# ============================================================
# SLIDE 23 — Traditional Service Discovery – Server-Side
# ============================================================
s = new_slide()
title(s, "Traditional Service Discovery – Server-Side")
embed(s, "s23_1.png", 2.2, 1.5, 8.9, 5.0)
whale_and_footer(s, 23)

# ============================================================
# SLIDE 24 — K8s Service - Similarly Labeled Pods
# ============================================================
s = new_slide()
title(s, "K8s Service  - Similarly Labeled Pods")
embed(s, "s24_1.png", 2.2, 1.5, 8.9, 5.0)
whale_and_footer(s, 24)

# ============================================================
# SLIDE 25 — Exposing containers
# ============================================================
s = new_slide()
title(s, "Exposing containers")
bullets(s, 1.55, [
    (0, "Imagine standard client-server configuration. How would we configure the access points for the clients?"),
    (0, "Challenges:"),
    (1, "We cannot configure pod's IP – pods are ephemeral"),
    (1, "Clients do not know server IP upfront"),
    (1, "Multiple pods can provide the same service – clients have no way to know"),
    (0, "We need a single IP endpoint"),
], x=0.55, w=7.0, size=14, line_spacing=1.45)
embed(s, "s25_1.jpg", 8.0, 1.55, 4.8, 4.9)
whale_and_footer(s, 25)

# ============================================================
# SLIDE 26 — Exposing Containers in Kubernetes
# ============================================================
s = new_slide()
title(s, "Exposing Containers in Kubernetes")
bullets(s, 1.6, [
    (0, "We can connect to our pods using their IP address"),
    (0, "Then we need to figure out a lot of things:"),
    (1, "how do we look up the IP address of the pod(s)?"),
    (1, "how do we connect from outside the cluster?"),
    (1, "how do we load balance traffic?"),
    (1, "what if a pod fails?"),
    (0, "Kubernetes has a resource type named Service"),
    (0, "Services address all these questions!"),
], x=0.55, w=11.5, size=15, line_spacing=1.5)
whale_and_footer(s, 26)

# ============================================================
# SLIDE 27 — Services
# ============================================================
s = new_slide()
title(s, "Services")
bullets(s, 1.7, [
    (0, "Services enable connectivity b/w group of PODS"),
    (0, "Helps communication between backend and frontend pods"),
    (0, "Helps communication with external source"),
    (0, "Enables loose coupling in our application"),
], x=0.55, w=6.3, size=15, line_spacing=1.7)
embed(s, "s27_1.png", 6.9, 1.7, 5.9, 4.4)
whale_and_footer(s, 27)

# ============================================================
# SLIDE 28 — Why Services? (title only)
# ============================================================
s = new_slide()
title(s, "Why Services?")
whale_and_footer(s, 28)

# ============================================================
# SLIDE 29 — How can I access the POD?
# ============================================================
s = new_slide()
title(s, "How can I access the POD?")
bullets(s, 1.7, [
    (0, "SSH into the Node and Curl to POD IP – Not desired as its from Inside the node"),
    (0, "How to access from my Laptop without SSH into Node? Need something in middle to ensure we can access it → Service to the rescue (Listens on Port of Node and Fwds it to a port on POD)"),
    (0, "Type of Service – NodePort"),
], x=0.55, w=6.2, size=14, line_spacing=1.45)
embed(s, "s29_1.png", 6.9, 1.9, 5.9, 4.3)
whale_and_footer(s, 29)

# ============================================================
# SLIDE 30 — Introducing Kubernetes Services
# ============================================================
s = new_slide()
title(s, "Introducing Kubernetes Services")
bullets(s, 1.8, [
    (0, "Immutable point of entry to a group of pods providing the same service"),
    (0, "Clients open connections to this IP/port and client's requests are routed to pod backing the service"),
    (0, "Services are automatically added to an internal DNS zone"),
], x=0.55, w=6.3, size=15, line_spacing=1.55)
embed(s, "s30_1.png", 7.0, 1.5, 5.8, 5.0)
whale_and_footer(s, 30)

# ============================================================
# SLIDE 31 — Types of Services
# ============================================================
s = new_slide()
title(s, "Types of Services")
bullets(s, 1.7, [
    (0, "There are different types of services:"),
    (1, "ClusterIP, NodePort, LoadBalancer, ExternalName"),
    (0, "There are also headless services"),
    (0, "Services can also have optional external IPs"),
    (0, "There is also another resource type called Ingress"),
    (0, "(specifically for HTTP services)"),
], x=0.55, w=6.5, size=15, line_spacing=1.5)
embed(s, "s31_1.png", 7.4, 1.6, 5.4, 4.8)
whale_and_footer(s, 31)

# ============================================================
# SLIDE 32 — Accessing the Service
# ============================================================
s = new_slide()
title(s, "Accessing the Service")
bullets(s, 1.8, [
    (0, "Services of type ClusterIP are not externally accessible"),
    (0, "We can access this service in different ways"),
    (1, "Run a pod in the cluster that will access this service"),
    (1, "Execute curl with kubectl exec command"),
    (1, "ssh into one of the Kubernetes nodes and use the curl command."),
], x=0.55, w=6.3, size=15, line_spacing=1.55)
embed(s, "s32_1.png", 6.9, 1.8, 5.9, 4.4)
whale_and_footer(s, 32)

# ============================================================
# SLIDE 33 — Creating Service Imperatively (terminal)
# ============================================================
s = new_slide()
title(s, "Creating Service Imperatively")
auto_term(s, 0.55, 1.6, 12.2, 4.5, "bash", [
    "# Create a deployment with single replica",
    "kubectl create deploy nginx-deployment --image=nginx",
    "# Scale the deployment to 3 replicas",
    "kubectl scale deploy nginx-deployment --replicas=3 deployment",
    "# Expose the container on port 80",
    "kubectl expose deployment nginx-deployment --port=80",
], font_size=13)
whale_and_footer(s, 33)

# ============================================================
# SLIDE 34 — Kube-Proxy (bullets + figure)
# ============================================================
s = new_slide()
title(s, "Kube-Proxy")
bullets(s, 1.55, [
    (0, "Services are created by KubeProxy"),
    (0, "Service is given an IP address"),
    (0, "Service is virtual no process, namespaces or interfaces unlike containers/PODS"),
    (0, "Service is assigned an IP address from pre-defined range"),
    (0, "Kube-Proxy creates fwding rules on each node in cluster i.e. any traffic to svc IP is fwded to POD ip"),
    (0, "Its actually IP and Port combination"),
    (0, "Kube-proxy creates and deletes the service rules (eg: for NodePort IPtable rule is created to fwd all traffic on all nodes to respective PODs)"),
], x=0.55, w=6.0, size=12.5, line_spacing=1.3)
embed(s, "s34_1.png", 6.7, 1.7, 6.1, 4.6)
whale_and_footer(s, 34)

# ============================================================
# SLIDE 35 — How does it work?
# ============================================================
s = new_slide()
title(s, "How does it work?")
bullets(s, 2.0, [
    (0, "Kube-proxy modifies IPTABLES on each node to create rules for the services we define."),
    (0, "Kube-proxy does not do the actual routing"),
], x=0.55, w=4.4, size=15, line_spacing=1.5)
embed(s, "s35_1.png", 5.0, 1.7, 7.8, 4.6)
whale_and_footer(s, 35)

# ============================================================
# SLIDE 36 — Service Type: NodePort (bullets + figure)
# ============================================================
s = new_slide()
title(s, "Service Type: NodePort")
bullets(s, 1.5, [
    (0, "A port number is allocated for the service"),
    (0, "(by default, in the 30000-32767 range)"),
    (0, "That port is made available on all our nodes and anybody can connect to it"),
    (0, "(we can connect to any node on that port to reach the service)"),
    (0, "Our code needs to be changed to connect to that new port number"),
    (0, "Under the hood: kube-proxy sets up a bunch of iptables rules on our nodes"),
    (0, "Sometimes, it's the only available option for external traffic (e.g. most clusters deployed with kubeadm or on-premises)"),
    (0, "Automatically will create a ClusterIP service"),
], x=0.55, w=6.0, size=12, line_spacing=1.28)
embed(s, "s36_1.png", 6.7, 1.6, 6.1, 4.8)
whale_and_footer(s, 36)

# ============================================================
# SLIDE 37 — Service Type: NodePort (bullets + figure)
# ============================================================
s = new_slide()
title(s, "Service Type: NodePort")
bullets(s, 1.8, [
    (0, "Service automatically selects Pods with same selector and load balances automatically"),
    (0, "Algorithm used is Random"),
    (0, "Pods distributed across multiple nodes – When Svc created, K8s automatically creates our svc spanning across all nodes and maps the target port to same node port on all nodes enabling access from any node in cluster."),
], x=0.55, w=6.0, size=13, line_spacing=1.4)
embed(s, "s37_1.png", 6.7, 1.8, 6.1, 4.4)
whale_and_footer(s, 37)

# ============================================================
# SLIDE 38 — Service Manifest (figure)
# ============================================================
s = new_slide()
title(s, "Service Manifest")
embed(s, "s38_1.png", 1.0, 1.7, 11.3, 4.6)
whale_and_footer(s, 38)

# ============================================================
# SLIDE 39 — Using Named Ports (figures)
# ============================================================
s = new_slide()
title(s, "Using Named Ports")
embed(s, "s39_1.png", 1.5, 1.55, 10.3, 2.35, valign='top')
embed(s, "s39_2.png", 1.5, 4.05, 10.3, 2.35, valign='top')
whale_and_footer(s, 39)

# ============================================================
# SLIDE 40 — Service Type: ClusterIP (bullets + figure)
# ============================================================
s = new_slide()
title(s, "Service Type: ClusterIP")
bullets(s, 1.65, [
    (0, "It's the default service type"),
    (0, "A virtual IP address is allocated for the service"),
    (0, "(in an internal, private range; e.g. 10.96.0.0/12)"),
    (0, "This IP address is reachable only from within the cluster (nodes and pods)"),
    (0, "Our code can connect to the service using the original port number"),
    (0, "Perfect for internal communication, within the cluster"),
], x=0.55, w=6.0, size=13, line_spacing=1.4)
embed(s, "s40_1.png", 6.7, 1.7, 6.1, 4.6)
whale_and_footer(s, 40)

# ============================================================
# SLIDE 41 — Service Type: ClusterIP (bullets + figures)
# ============================================================
s = new_slide()
title(s, "Service Type: ClusterIP")
bullets(s, 1.65, [
    (0, "Ips cannot be relied on as PODs get new Ips everytime"),
    (0, "To use a single interface a service is required."),
    (0, "We can have backend pods or redis pods created as service"),
    (0, "Each service gets an IP and name to be used to access service"),
    (0, "Cluster IP service can be used to access backend apps/Data stores"),
    (0, "Target Port is backend port and Port is the port on which service is exposed"),
], x=0.55, w=5.9, size=12.5, line_spacing=1.35)
embed(s, "s41_1.png", 6.6, 1.6, 6.2, 2.4, valign='top')
embed(s, "s41_2.png", 6.6, 4.1, 6.2, 2.3, valign='top')
whale_and_footer(s, 41)

# ============================================================
# SLIDE 42 — Service Type: LoadBalancer (bullets + figure)
# ============================================================
s = new_slide()
title(s, "Service Type: LoadBalancer")
bullets(s, 1.8, [
    (0, "An external load balancer is allocated for the service"),
    (0, "This is available only when the underlying infrastructure provides some kind of \"load balancer as a service\""),
    (0, "Each service of that type will typically cost a little bit of money"),
    (0, "Ideally, traffic would flow directly from the load balancer to the pods"),
    (0, "In practice, it will often flow through a NodePort first"),
], x=0.55, w=6.2, size=13, line_spacing=1.45)
embed(s, "s42_1.png", 7.1, 1.6, 5.7, 4.8)
whale_and_footer(s, 42)

# ============================================================
# SLIDE 43 — Service Type: LoadBalancer (bullets + figures)
# ============================================================
s = new_slide()
title(s, "Service Type: LoadBalancer")
bullets(s, 1.8, [
    (0, "Users can access this application using mentioned URLs"),
    (0, "However we need one URL like example-vote.com etc instead of node and ports"),
    (0, "K8s can integrate with native LB of cloud providers"),
    (0, "An external load balancer is allocated for the service"),
    (0, "In practice, it will often flow through a NodePort first"),
], x=0.55, w=6.2, size=13, line_spacing=1.45)
embed(s, "s43_1.png", 7.1, 1.55, 5.7, 2.6, valign='top')
embed(s, "s43_2.png", 7.7, 4.25, 4.5, 2.2, valign='top')
whale_and_footer(s, 43)

# ============================================================
# SLIDE 44 — Summary - Services (figure)
# ============================================================
s = new_slide()
title(s, "Summary - Services")
embed(s, "s44_1.png", 1.4, 1.6, 10.5, 4.8)
whale_and_footer(s, 44)

# ============================================================
# SLIDE 45 — Discovering Services (bullets + terminal session)
# ============================================================
s = new_slide()
title(s, "Discovering Services")
bullets(s, 1.5, [
    (0, "Through Environment Variables"),
    (0, "Through DNS servers and FQDNs"),
], x=0.55, w=12.0, size=14, line_spacing=1.4)
auto_term(s, 0.55, 2.6, 12.2, 3.9, "bash", [
    "$ kubectl exec -it kubia-3inly bash",
    "root@kubia-3inly:/#",
    "# Inside the container",
    "root@kubia-3inly:/# curl http://kubia.default.svc.cluster.local",
    "You’ve hit kubia-5asi2",
    "root@kubia-3inly:/# curl http://kubia.default",
    "You’ve hit kubia-3inly",
    "root@kubia-3inly:/# curl http://kubia",
    "You’ve hit kubia-8awf3",
    "root@kubia-3inly:/# cat /etc/resolv.conf",
    "search default.svc.cluster.local svc.cluster.local cluster.local ..",
], font_size=11)
whale_and_footer(s, 45)

# ============================================================
# SLIDE 46 — Service Endpoints (bullets + figure)
# ============================================================
s = new_slide()
title(s, "Service Endpoints")
bullets(s, 1.55, [
    (0, "An Endpoints resource (yes, plural) is a list of IP addresses and ports exposing a service."),
    (0, "The selector is used to build a list of IPs and ports, which is then stored in the Endpoints resource."),
    (0, "When a client connects to a service, the service proxy selects one of those IP and port pairs and redirects the incoming connection to the server listening at that location."),
], x=0.55, w=11.3, size=14, line_spacing=1.45)
embed(s, "s46_1.png", 0.7, 4.3, 11.9, 2.1, valign='top')
whale_and_footer(s, 46)

# ============================================================
# SLIDE 47 — Service Networking (bullets + figures)
# ============================================================
s = new_slide()
title(s, "Service Networking")
bullets(s, 1.6, [
    (0, "Blue and Orange POD are on same node"),
    (0, "Accessing a POD on other nodes - While a POD is hosted on node, svc is hosted across cluster but only accessible within cluster (Cluster IP)"),
    (0, "If Orange POD were to be DB, then cluster IP is good"),
    (0, "If Purple is Web app, a NodePort is created to ensure user can access from outside"),
], x=0.55, w=5.7, size=12.5, line_spacing=1.35)
embed(s, "s47_1.png", 6.5, 1.5, 6.3, 2.45, valign='top')
embed(s, "s47_2.png", 6.5, 4.05, 6.3, 2.45, valign='top')
whale_and_footer(s, 47)

# ============================================================
# SLIDE 48 — Ingress Resource (title only)
# ============================================================
s = new_slide()
title(s, "Ingress Resource")
whale_and_footer(s, 48)

# ============================================================
# SLIDE 49 — Understanding Ingress (bullets + figure)
# ============================================================
s = new_slide()
title(s, "Understanding Ingress")
bullets(s, 1.8, [
    (0, "Layer 7 load balancer"),
    (1, "Provides cookie-based session affinity"),
    (1, "Level 7 routing"),
    (0, "Requires ingress controller to be installed in the cluster"),
], x=0.55, w=6.0, size=15, line_spacing=1.55)
embed(s, "s49_1.png", 6.7, 2.0, 6.1, 4.0)
whale_and_footer(s, 49)

# ============================================================
# SLIDE 50 — Workshop 3 divider
# ============================================================
s = new_slide()
divider(s, "Workshop 3 – Using K8s Services")
whale_and_footer(s, 50)

# ============================================================
# SLIDE 51 — Example: 2-Tier Web application (title only)
# ============================================================
s = new_slide()
title(s, "Example: 2-Tier Web application")
whale_and_footer(s, 51)

# ============================================================
# SLIDE 52 — Create the Namespace (terminal)
# ============================================================
s = new_slide()
title(s, "Create the Namespace")
auto_term(s, 0.55, 1.55, 12.2, 4.6, "bash", [
    "# Copy all the deployment files to the EC2 with our kind cluster",
    "scp -i week6 week6Session2/* 100.27.36.251:/tmp/",
    "# log into you EC2",
    "ssh -i week6 [EC2 public IP]",
    "# Verify the cluster is running",
    "k get nodes",
    "# Create a namespace for our Guestbook application",
    "k create ns guestbook",
], font_size=13)
whale_and_footer(s, 52)

# ============================================================
# SLIDE 53 — Deploying application components: MongoDB (terminal)
# ============================================================
s = new_slide()
title(s, "Deploying application components: MongoDB")
auto_term(s, 0.55, 1.55, 12.2, 4.95, "bash", [
    "# Deploy application component – MongoDB",
    "k apply -f /tmp/mongo-deployment.yaml -n guestbook",
    "# Verify the successful deployment",
    "k rollout status deployment.apps/mongo -n guestbook",
    "k describe -n guestbook  deployment.apps/mongo",
    "# Create service to expose mongoDB to internal cluster users",
    "k apply -f /tmp/mongo-service.yaml  -n guestbook",
    "Explain: what type of service did we create? Why is this the right type of service to use with Mongo DB?",
    "# Verify the service is created",
    "k get svc -n guestbook",
    "# Examine Service Endpoints",
    "K describe service mongo -n guestbook",
], font_size=11)
whale_and_footer(s, 53)

# ============================================================
# SLIDE 54 — Deploy Application Components: Frontend (terminal)
# ============================================================
s = new_slide()
title(s, "Deploy Application Components: Frontend")
auto_term(s, 0.55, 1.55, 12.2, 4.6, "bash", [
    "# Create frontend deployment",
    "k apply -f /tmp/frontend-deployment.yaml -n guestbook",
    "# Verify the successful deployment",
    "k rollout status deployment.apps/frontend -n guestbook",
    "k describe -n guestbook deployment.apps/frontend",
    "# Create service to expose mongoDB to internal cluster users",
    "k apply -f /tmp/frontend-service.yaml  -n guestbook",
    "# Verify the service is created",
    "k get svc -n guestbook",
], font_size=13)
whale_and_footer(s, 54)

# ============================================================
# SLIDE 55 — Connecting to GuestBook Application with ClusterIP (terminal)
# ============================================================
s = new_slide()
title(s, "Connecting to GuestBook Application with ClusterIP")
auto_term(s, 0.55, 1.55, 12.2, 4.5, "bash", [
    "# Our ClusterIP service listens on port 80. We will forward local port 8080 to service port 80 with port-forward",
    "k port-forward svc/frontend 8080:80 -n guestbook",
    "# Verify access to the service from another terminal window",
    "curl localhost:8080",
    "# Open port 8080 in the Security Group and try to access the application via [PublicIP]:8080 in the browser.",
    "# Explain: Was it successful? Why?",
], font_size=12)
whale_and_footer(s, 55)

# ============================================================
# SLIDE 56 — Connecting to GuestBook Application with NodePort (terminal)
# ============================================================
s = new_slide()
title(s, "Connecting to GuestBook Application with NodePort")
auto_term(s, 0.55, 1.55, 12.2, 4.2, "bash", [
    "# Update the service type to NodePort",
    "k apply -f /tmp/frontend-serviceNodePort.yaml -n guestbook",
    "# Verify that the port forward is still running, and we can still connect via kubectl port forward",
    "curl localhost:8080",
    "# Open port 30001 in the Security Group and try connection from the browser with [EC2 Public IP]:30001",
], font_size=12)
whale_and_footer(s, 56)

# ============================================================
# SLIDE 57 — Connecting ... NodePort 30100 (HIDDEN in source)
# ============================================================
s = new_slide()
title(s, "Connecting to GuestBook Application with NodePort – change the NodePort to 30100")
auto_term(s, 0.55, 2.05, 12.2, 4.0, "bash", [
    "# Try connecting with the different NodePort, e.g. 30100. Update the NodePort in the frontend-serviceNodePort.yaml and update the service",
    "k apply -f /tmp/frontend-serviceNodePort.yaml -n guestbook",
    "# Verify we can still connect with ClusterIP",
    "curl localhost:8080",
    "# Update EC2 Security Group and try connecting to the application from the browser using [EC2 Public IP]:30100",
    "# Exlain: Was it successful? Why?",
], font_size=12)
whale_and_footer(s, 57)
hide(s)

# ============================================================
# SLIDE 58 — Frontend connection to MongoDB – how does it work?
# ============================================================
s = new_slide()
title(s, "Frontend connection to MongoDB – how does it work?")
bullets(s, 1.55, [
    (0, "We will research Pod template"),
    (0, "Google paulczar/gb-frontend"),
    (0, "Find it on DockeHub"),
    (0, "Look at the digest"),
    (0, "Look for guestbook.php and mongodb"),
    (0, "https://github.com/kevinraymond/php-guestbook/blob/main/app/guestbook.php", BLUE),
    (0, "The answer"),
], x=0.55, w=7.2, size=13.5, line_spacing=1.4)
terminal(s, Inches(7.55), Inches(1.95), Inches(5.25), Inches(1.6), "guestbook.php",
         [[("// this references the \"mongo\" service", TERM_GRN)],
          [("$messages = (new MongoDB\\Client(", TERM_GRAY)],
          [("    'mongodb://mongo'))->guestbook->messages;", TERM_CYAN)],
          [("$method = $_SERVER['REQUEST_METHOD'];", TERM_GRAY)]],
         font_size=9)
add_text(s, Inches(0.55), Inches(5.25), Inches(12.2), Inches(0.45),
         "Explain: Would our application work if we give our MongoDB service a different name?",
         size=14, bold=True, italic=True, color=SLATE)
whale_and_footer(s, 58)

# ============================================================
# SLIDE 59 — Changing MongoDB Service Name (terminal w/ error)
# ============================================================
s = new_slide()
title(s, "Changing MongoDB Service Name")
auto_term(s, 0.55, 1.55, 12.2, 4.95, "bash", [
    "# Delete the mongo service and frontend deployment and service",
    "k delete svc frontend -n guestbook",
    "k delete deployment  frontend -n guestbook",
    "k delete svc mongo -n guestbook",
    "# Update the /tmp/mongo-service.yaml  and rename the service",
    "# Apply the changes",
    "k apply -f /tmp/mongo-service.yaml -n guestbook",
    "k apply /tmp/frontend-deployment.yaml",
    "k apply -f /tmp/frontend-service.yaml -n guestbook",
    "# Verify we can still connect with ClusterIP",
    "curl localhost:8080",
    "-bash-4.2$ curl localhost:8080",
    "curl: (7) Failed to connect to localhost port 8080 after 0 ms: Connection refused",
], font_size=11)
whale_and_footer(s, 59)

# ============================================================
# SLIDE 60 — Workshop 3 — The End divider
# ============================================================
s = new_slide()
divider(s, "Workshop 3 – The End")
whale_and_footer(s, 60)

# ============================================================
# SLIDE 61 — Workshop 4 divider
# ============================================================
s = new_slide()
divider(s, "Workshop 4 – DNS in K8s")
whale_and_footer(s, 61)

# ============================================================
# SLIDE 62 — Creating a deployment for our HTTP server (terminal)
# ============================================================
s = new_slide()
title(s, "Creating a deployment for our HTTP server")
auto_term(s, 0.55, 1.55, 12.2, 4.3, "bash", [
    "# Create a deployment for this very lightweight HTTP server:",
    "k create deployment blue --image=jpetazzo/color",
    "# Scale it to 10 replicas:",
    "k scale deployment blue --replicas=10",
    "# Pods are created",
    "k get pods -l app=blue",
], font_size=13)
whale_and_footer(s, 62)

# ============================================================
# SLIDE 63 — Exposing our deployment – Create ClusterIP service (terminal)
# ============================================================
s = new_slide()
title(s, "Exposing our deployment – Create ClusterIP service")
auto_term(s, 0.55, 1.55, 12.2, 4.0, "bash", [
    "# Expose the HTTP port of our server",
    "k expose deployment blue --port=80",
    "# Look up which IP address was allocated",
    "k get svc",
    "k get svc blue -o yaml",
], font_size=13)
whale_and_footer(s, 63)

# ============================================================
# SLIDE 64 — Test the Access to the Application (terminal)
# ============================================================
s = new_slide()
title(s, "Test the Access to the Application")
auto_term(s, 0.55, 1.55, 12.2, 4.6, "bash", [
    "# Test the service from inside the K8s \"node\" that runs as a container in our environment",
    "docker exec -it [CONTAINER ID] /bin/bash",
    "# Send curl request to ClusterIP from the bash prompt of the container that simulates our master node. Try it a few times! Our requests are load balanced across multiple pods.",
    "curl [ClusterIp of blue service]",
    "# Result",
    "root@kind-control-plane:/# curl 10.96.136.226",
    "🔵This is pod default/blue-796f87cc56-9dmrx on linux/amd64, serving / for 10.244.0.1:44398.",
], font_size=11)
whale_and_footer(s, 64)

# ============================================================
# SLIDE 65 — Services and endpoints (bullets + terminal)
# ============================================================
s = new_slide()
title(s, "Services and endpoints")
bullets(s, 1.5, [
    (0, "A service has a number of \"endpoints\""),
    (0, "Each endpoint is a host + port where the service is available"),
    (0, "The endpoints are maintained and updated automatically by Kubernetes"),
], x=0.55, w=12.0, size=14, line_spacing=1.4)
auto_term(s, 0.55, 3.25, 12.2, 3.25, "bash", [
    "# Get service Endpoints",
    "k describe service blue",
    "k get endpoints",
    "k describe endpoints blue",
    "k get endpoints blue -o yaml",
    "# Compare to the output below",
    "k get pods -l app=blue -o wide",
], font_size=12)
whale_and_footer(s, 65)

# ============================================================
# SLIDE 66 — DNS in K8s (bullets + figure)
# ============================================================
s = new_slide()
title(s, "DNS in K8s")
bullets(s, 1.8, [
    (0, "In the kube-system namespace, there should be a service named kube-dns."),
    (0, "This is the internal DNS server that can resolve service names"),
    (0, "The default domain name for the service we created is default.svc.cluster.local"),
], x=0.55, w=6.0, size=14, line_spacing=1.5)
embed(s, "s66_1.png", 6.95, 1.7, 5.55, 4.6)
whale_and_footer(s, 66)

# ============================================================
# SLIDE 67 — DNS in K8s (figure)
# ============================================================
s = new_slide()
title(s, "DNS in K8s")
embed(s, "s67_1.png", 3.5, 1.6, 6.3, 4.8)
whale_and_footer(s, 67)

# ============================================================
# SLIDE 68 — DNS in K8s (bullets + figure)
# ============================================================
s = new_slide()
title(s, "DNS in K8s")
bullets(s, 1.5, [
    (0, "CoreDNS is deployed as replicaset in K8s cluster"),
    (0, "CoreDNS exposes a service by default (kube-dns). The IP addr of this server is configured as nameserver on PODs. This is done automatically."),
    (0, "CoreDNS requires a config file which is /etc/coredns/Corefile"),
    (0, "Plugins are configured to handling errors, monitoring etc."),
    (0, "Cluster-local – every record falls under this domain"),
    (0, "Pods option – responsible for creating  records for PODS in cluster"),
    (0, "Any record that dns server cant solve is fwded to Name server configured in etc/resolv.conf"),
], x=0.55, w=6.2, size=12, line_spacing=1.3)
embed(s, "s68_1.png", 6.95, 1.9, 5.55, 4.3)
whale_and_footer(s, 68)

# ============================================================
# SLIDE 69 — Examine DNS in the pod (terminal)
# ============================================================
s = new_slide()
title(s, "Examine DNS in the pod")
auto_term(s, 0.55, 1.55, 12.2, 4.6, "bash", [
    "# log into blue pod",
    "k exec -it blue-796f87cc56-7tbfc -- /bin/sh",
    "# Examine the nameservers defined in the pod.",
    "# What is running on IP is 10.96.0.10?",
    "# What are the entries in the resolv.conf file?",
    "cat /etc/resolv.conf",
    "search default.svc.cluster.local svc.cluster.local cluster.local ec2.internal",
    "nameserver 10.96.0.10",
    "options ndots:5",
], font_size=13)
whale_and_footer(s, 69)

# ============================================================
# SLIDE 70 — Workshop 4 — The End divider
# ============================================================
s = new_slide()
divider(s, "Workshop 4 – The End")
whale_and_footer(s, 70)

# ============================================================
# SLIDE 71 — Additional Resources
# ============================================================
s = new_slide()
title(s, "Additional Resources")
bullets(s, 1.7, [
    (0, "https://kubernetes.io/docs/concepts/services-networking/service/", BLUE),
    (0, "https://medium.com/devops-mojo/kubernetes-service-types-overview-introduction-to-k8s-service-types-what-are-types-of-kubernetes-services-ea6db72c3f8c", BLUE),
    (0, "https://docs.vmware.com/en/VMware-Cloud-Foundation/services/vcf-developer-ready-infrastructure-v1/GUID-6F184EC5-AFC1-4D0A-A5D5-1E31EE938438.html", BLUE),
    (0, "https://container.training/kube-selfpaced.yml.html#273", BLUE),
    (0, "https://www.bookstack.cn/read/kubernetes-1.21-en/59a313e057e11c1b.md", BLUE),
    (0, "https://arthurchiao.art/blog/cracking-k8s-node-proxy/", BLUE),
    (0, "https://iximiuz.com/en/posts/service-discovery-in-kubernetes/", BLUE),
], x=0.55, w=11.9, size=12, line_spacing=1.5)
whale_and_footer(s, 71)


# ===== Save =====
_sanitize_coords(prs)
out = f"Week06/Week06_lab_style_{VERSION}.pptx"
prs.save(out)
print(f"wrote {out}  ({len(prs.slides.__iter__.__self__._sldIdLst)} slides)")
