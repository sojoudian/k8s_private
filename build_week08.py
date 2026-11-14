"""Week08 — Lab02/Week05 design language applied to the Week 8 deck.

Source: Week08/"Week08 -  K8s in the cloud, Amazon EKS.pptx" — 33 slides,
"Managed K8s – Amazon EKS". Original slide text preserved verbatim (no rephrasing).

This builder emits TWO decks from one set of per-slide functions (mirrors the
Week 5/6 lecture/lab split, but with deliberate THEORY DUPLICATION so the lab is
self-contained):
  • Week08_lecture_style_v1.pptx — concepts taught before the Wed lab
    (cover, course outline, cost, EKS architecture x3, volume lifecycle, reading)
  • Week08_lab_style_v3.pptx — hands-on Workshops 1 & 2, with the architecture
    and volume-lifecycle THEORY slides duplicated in for context.

Treatment (same house style as Week 6/7): bullet slides → blue title + multi-level
bullets; shell/YAML → dark terminal mockup; AWS architecture/console figures →
embedded originals; Course Outline + Cost estimate → redrawn natively in palette;
workshop boundaries → LAB dividers. Exact CLO835 palette + Calibri/Consolas + chrome.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

CENTER, LEFT, RIGHT = PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.RIGHT
MIDDLE, TOP = MSO_ANCHOR.MIDDLE, MSO_ANCHOR.TOP

# === Lab02 palette (verbatim, matches DESIGN_LANGUAGE.md) ===
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
EXAM_RED    = RGBColor(0xFF, 0x6B, 0x6B)
STEPS = [
    RGBColor(0x1F, 0xA8, 0xE0), RGBColor(0x21, 0x96, 0xA0),
    RGBColor(0x1F, 0x8F, 0xCD), RGBColor(0x1F, 0x7A, 0xB8),
    RGBColor(0x24, 0x66, 0xA0), RGBColor(0x37, 0x46, 0x5A),
]
FONT_SANS, FONT_MONO = "Calibri", "Consolas"

K8S_LOGO   = "Week04/Kubernetes_logo_without_workmark.svg.png"
WHALE      = "whale.png"
ASSETS_DIR = "Week08/assets"
LECTURE_VERSION = "v3"
LAB_VERSION     = "v3"
ASPECT = {
    "s05_1.png": (1280, 720), "s06_1.png": (1280, 530), "s06_2.png": (1280, 538),
    "s07_1.png": (1296, 620), "s15_1.png": (1263, 900), "s17_1.png": (1207, 534),
    "s19_1.png": (1173, 465), "s24_1.png": (669, 350),  "s25_1.jpg": (2048, 1365),
    "s26_1.jpg": (1242, 218), "s27_1.png": (648, 450),  "s28_1.jpg": (2048, 1365),
    "s29_1.png": (384, 81),   "s29_2.png": (592, 96),   "s30_1.png": (1138, 601),
    "s30_2.png": (730, 346),  "s31_1.png": (1208, 1208),
}


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


def add_text(s, x, y, w, h, text, *, font=FONT_SANS, size=14, bold=False,
             italic=False, color=BODY, align=LEFT, anchor=TOP, line_spacing=1.15):
    tb = s.shapes.add_textbox(_i(x), _i(y), _i(w), _i(h))
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Inches(0)
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    for i, line in enumerate(text.split("\n") if isinstance(text, str) else text):
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
    if line is None: shp.line.fill.background()
    else:
        shp.line.color.rgb = line; shp.line.width = Pt(line_width)
    shp.shadow.inherit = False
    return shp


def add_rounded_rect(s, x, y, w, h, fill, line=None, line_width=0.75, radius_ratio=0.10):
    shp = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, _i(x), _i(y), _i(w), _i(h))
    shp.adjustments[0] = radius_ratio
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line is None: shp.line.fill.background()
    else:
        shp.line.color.rgb = line; shp.line.width = Pt(line_width)
    shp.shadow.inherit = False
    return shp


def add_oval(s, x, y, w, h, fill, line=None, line_width=0.75):
    shp = s.shapes.add_shape(MSO_SHAPE.OVAL, _i(x), _i(y), _i(w), _i(h))
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line is None: shp.line.fill.background()
    else:
        shp.line.color.rgb = line; shp.line.width = Pt(line_width)
    shp.shadow.inherit = False
    return shp


def add_line(s, x1, y1, x2, y2, color=RULE_GRAY, width=0.75):
    ln = s.shapes.add_connector(1, _i(x1), _i(y1), _i(x2), _i(y2))
    ln.line.color.rgb = color; ln.line.width = Pt(width)
    return ln


def add_chevron(s, x, y, w, h, fill):
    """Axis-aligned right arrow (MSO_SHAPE — never a zero-extent connector)."""
    shp = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, _i(x), _i(y), _i(w), _i(h))
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    shp.line.fill.background(); shp.shadow.inherit = False
    return shp


def hide(s):
    s._element.set('show', '0')


def whale_and_footer(s, page_num, total):
    s.shapes.add_picture(WHALE, Inches(0.45), Inches(6.85), width=Inches(0.5), height=Inches(0.5))
    add_line(s, Inches(0.5), Inches(7.05), Inches(12.83), Inches(7.05), color=RULE_GRAY, width=0.5)
    add_text(s, Inches(9.5), Inches(7.12), Inches(3.35), Inches(0.3),
             f"CLO835, Fall 2026     {page_num} / {total}",
             size=10, color=FOOTER_GRAY, align=RIGHT)


def title(s, text, y=0.40, size=32):
    add_text(s, Inches(0.55), Inches(y), Inches(12.2), Inches(0.85),
             text, size=size, bold=True, color=BLUE, line_spacing=1.05)


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


_CMD_STARTS = ("$", "k ", "k8s", "kubectl", "aws", "export", "curl", "rm", "vi ",
               "cat", "sudo", "/usr", "/ #", "ssh", "scp", "echo")


def _role(line):
    if line == "":
        return None
    st = line.lstrip()
    if st.startswith("#"):
        return TERM_GRN          # comment
    if "ERROR" in line or "error" in st[:6] or "fail" in st[:5].lower():
        return TERM_ERR
    if any(st.startswith(c) for c in _CMD_STARTS):
        return TERM_CYAN         # command
    return TERM_GRAY             # output / prose


def auto_term(s, x, y, w, h, title_text, raw, *, font_size=11):
    """raw: list of plain strings; classified to command/comment/output colors."""
    runs = []
    for ln in raw:
        col = _role(ln)
        runs.append([] if col is None else [(ln, col)])
    terminal(s, Inches(x), Inches(y), Inches(w), Inches(h), title_text, runs, font_size=font_size)


def yaml_terminal(s, x, y, w, h, title_text, lines, *, font_size=11):
    TOPKEYS = ("apiVersion", "kind", "metadata", "spec")
    runs = []
    for ln in lines:
        if ln == "":
            runs.append([]); continue
        stripped = ln.lstrip()
        color = TERM_CYAN if (ln == stripped and any(stripped.startswith(k) for k in TOPKEYS)) else TERM_GRAY
        runs.append([(ln, color)])
    terminal(s, Inches(x), Inches(y), Inches(w), Inches(h), title_text, runs, font_size=font_size)


def annot_card(s, x, y, w, h, key, body):
    add_rounded_rect(s, Inches(x), Inches(y), Inches(w), Inches(h), CARD_BG,
                     line=RULE_GRAY, line_width=0.75, radius_ratio=0.10)
    add_rect(s, Inches(x), Inches(y + 0.04), Inches(0.10), Inches(h - 0.08), BLUE)
    add_text(s, Inches(x + 0.28), Inches(y + 0.13), Inches(w - 0.45), Inches(0.34), key,
             font=FONT_MONO, size=12, bold=True, color=BLUE)
    add_text(s, Inches(x + 0.28), Inches(y + 0.48), Inches(w - 0.45), Inches(h - 0.58), body,
             size=11, color=BODY, line_spacing=1.12)


def _list_box(s, x, y, w, h, items, *, size=12.5, line_spacing=1.25, space_after=5):
    tb = s.shapes.add_textbox(_i(Inches(x)), _i(Inches(y)), _i(Inches(w)), _i(Inches(h)))
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Inches(0)
    tf.word_wrap = True
    for i, it in enumerate(items):
        lvl, text = it if isinstance(it, tuple) else (0, it)
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.line_spacing = line_spacing
        p.space_after = Pt(space_after)
        pPr = p._p.get_or_add_pPr()
        pPr.set('marL', str(int(Inches(_MARG[lvl] + 0.22))))
        pPr.set('indent', str(-int(Inches(0.22))))
        sz = size - (1 if lvl else 0)
        r0 = p.add_run(); r0.text = _GLYPH[lvl]
        r0.font.name = FONT_SANS; r0.font.size = Pt(sz); r0.font.bold = True; r0.font.color.rgb = _GCOL[lvl]
        r1 = p.add_run(); r1.text = text
        r1.font.name = FONT_SANS; r1.font.size = Pt(sz); r1.font.color.rgb = BODY
    return tb


def concept_card(s, x, y, w, h, header, items, accent, *, body_size=12.5):
    add_rounded_rect(s, Inches(x), Inches(y), Inches(w), Inches(h), CARD_BG,
                     line=RULE_GRAY, line_width=0.75, radius_ratio=0.05)
    add_rect(s, Inches(x), Inches(y + 0.05), Inches(0.12), Inches(h - 0.10), accent)
    add_text(s, Inches(x + 0.32), Inches(y + 0.16), Inches(w - 0.5), Inches(0.45),
             header, size=14.5, bold=True, color=accent)
    _list_box(s, x + 0.32, y + 0.74, w - 0.55, h - 0.9, items, size=body_size)


def callout(s, x, y, w, h, text, accent=BLUE):
    add_rounded_rect(s, Inches(x), Inches(y), Inches(w), Inches(h), CARD_BG,
                     line=RULE_GRAY, line_width=0.75, radius_ratio=0.08)
    add_rect(s, Inches(x), Inches(y + 0.05), Inches(0.12), Inches(h - 0.10), accent)
    add_text(s, Inches(x + 0.34), Inches(y), Inches(w - 0.55), Inches(h),
             text, size=13.5, color=BODY, anchor=MIDDLE)


def divider(s, kicker, text, subtitle=None):
    """Workshop / section divider: slate circle + big slate title."""
    d = Inches(1.6); cx = Inches(13.333 / 2) - d / 2
    add_oval(s, cx, Inches(1.85), d, d, SLATE)
    add_text(s, cx, Inches(2.35), d, Inches(0.6), kicker,
             size=22, bold=True, color=WHITE, align=CENTER, anchor=MIDDLE)
    add_text(s, Inches(1.0), Inches(3.95), Inches(11.33), Inches(1.0), text,
             size=30, bold=True, color=SLATE, align=CENTER, line_spacing=1.05)
    if subtitle:
        add_text(s, Inches(1.0), Inches(5.05), Inches(11.33), Inches(0.6), subtitle,
                 size=15, italic=True, color=MUTED, align=CENTER)


def closing(s, text):
    add_oval(s, Inches(13.333 / 2) - Inches(0.8), Inches(2.2), Inches(1.6), Inches(1.6),
             WHITE, line=LIGHTBLUE, line_width=1.5)
    s.shapes.add_picture(K8S_LOGO, Inches(13.333 / 2) - Inches(0.6), Inches(2.4),
                         width=Inches(1.2), height=Inches(1.2))
    add_text(s, Inches(1.0), Inches(4.25), Inches(11.33), Inches(1.0), text,
             size=34, bold=True, color=BLUE, align=CENTER, line_spacing=1.05)


def cost_card(s):
    """Slide 4 — Amazon EKS pricing-calculator content, redrawn in palette (verbatim numbers)."""
    cx, cw = 3.0, 9.6
    add_rounded_rect(s, Inches(cx), Inches(1.65), Inches(cw), Inches(0.7), SLATE, radius_ratio=0.06)
    add_text(s, Inches(cx + 0.35), Inches(1.65), Inches(cw - 0.7), Inches(0.7),
             "Configure Amazon EKS", size=18, bold=True, color=WHITE, anchor=MIDDLE)
    add_rounded_rect(s, Inches(cx), Inches(2.45), Inches(cw), Inches(3.55), CARD_BG,
                     line=RULE_GRAY, line_width=0.75, radius_ratio=0.03)
    add_text(s, Inches(cx + 0.35), Inches(2.7), Inches(cw - 0.7), Inches(0.35),
             "Region", size=13, bold=True, color=SLATE)
    add_text(s, Inches(cx + 0.35), Inches(3.05), Inches(cw - 0.7), Inches(0.35),
             "US East (N. Virginia)", size=13, color=BODY)
    add_line(s, Inches(cx + 0.35), Inches(3.55), Inches(cx + cw - 0.35), Inches(3.55),
             color=RULE_GRAY, width=0.75)
    add_text(s, Inches(cx + 0.35), Inches(3.7), Inches(cw - 0.7), Inches(0.35),
             "EKS Cluster Pricing", size=13, bold=True, color=SLATE)
    add_text(s, Inches(cx + 0.35), Inches(4.05), Inches(cw - 0.7), Inches(0.35),
             "Number of EKS Clusters:  1", size=13, color=BODY)
    add_text(s, Inches(cx + 0.35), Inches(4.45), Inches(cw - 0.7), Inches(0.4),
             "1 Clusters x 0.10 USD per hour x 730 hours per month = 73.00 USD",
             font=FONT_MONO, size=12.5, color=BODY)
    add_rect(s, Inches(cx), Inches(5.15), Inches(cw), Inches(0.85), SLATE)
    add_rect(s, Inches(cx), Inches(5.15), Inches(0.12), Inches(0.85), GOAL_GREEN)
    add_text(s, Inches(cx + 0.35), Inches(5.15), Inches(cw - 0.7), Inches(0.85),
             "EKS Total Cost (monthly):  73.00 USD", size=18, bold=True, color=WHITE, anchor=MIDDLE)
    add_text(s, Inches(cx), Inches(6.15), Inches(cw), Inches(0.3),
             "Control plane only — worker nodes are billed separately.",
             size=11, italic=True, color=MUTED, align=CENTER)


_OUTLINE = [
    "Week 1: Docker Introduction", "Week 2: Docker Image Management",
    "Week 3: Docker Networking, Storage & Security", "Week 4: K8s Introduction",
    "Week 5: K8s- PODs, ReplicaSets", "Week 6: K8s – Services & Deployments",
    "Week 7: K8s – Volumes", "Study Week",
    "Week 8: K8s- K8s- PVs & K8s in AKS", "Week 9: K8s: Storage classes & Statefulsets",
    "Week 10: Exam & Mock Exam week", "Week 11: K8s- Configmaps & Secrets",
    "Week 12: K8s – RBAC and AKS", "Week 13: K8s – HPA",
    "Week 14: Helm Charts & Deployment Automation", "Term End",
]


def course_outline(s, current_idx=8, highlights=None):
    # idx -> fill color for emphasised tiles (white bold text, slate border)
    highlights = highlights if highlights is not None else {current_idx: BLUE, 10: EXAM_RED}
    cols, rows = 4, 4
    x0, y0 = 0.7, 1.6
    tw, th = 2.85, 1.05
    gx, gy = 0.27, 0.30
    for idx, label in enumerate(_OUTLINE):
        r, c = idx // cols, idx % cols
        x = x0 + c * (tw + gx); y = y0 + r * (th + gy)
        hi = idx in highlights
        fill = highlights[idx] if hi else CARD_BG
        line = SLATE if hi else RULE_GRAY
        add_rounded_rect(s, Inches(x), Inches(y), Inches(tw), Inches(th), fill,
                         line=line, line_width=1.5 if hi else 0.75, radius_ratio=0.10)
        add_text(s, Inches(x + 0.18), Inches(y), Inches(tw - 0.36), Inches(th),
                 label, size=11.5, bold=hi,
                 color=WHITE if hi else SLATE, anchor=MIDDLE, line_spacing=1.05)
        if c < cols - 1 and idx + 1 < len(_OUTLINE):
            add_chevron(s, Inches(x + tw + 0.02), Inches(y + th / 2 - 0.11),
                        Inches(gx - 0.04), Inches(0.22), LIGHTBLUE)


# ============================================================================
# Per-slide content functions — each draws content + footer for page (n / total)
# ============================================================================

def sl_cover(s, n, total, track):
    add_text(s, Inches(0.7), Inches(2.7), Inches(8.7), Inches(1.4),
             "Managed K8s — Amazon EKS", size=40, bold=True, color=BLUE, line_spacing=1.1)
    add_text(s, Inches(0.7), Inches(4.25), Inches(8.5), Inches(0.6),
             f"Week 8 · {track}", size=22, color=SLATE)
    logo_cx = Inches(10.7); logo_cy = Inches(3.55); ring_r = Inches(1.8)
    add_oval(s, logo_cx - ring_r, logo_cy - ring_r, ring_r * 2, ring_r * 2, WHITE, line=LIGHTBLUE, line_width=1.5)
    s.shapes.add_picture(K8S_LOGO, logo_cx - Inches(1.25), logo_cy - Inches(1.25), width=Inches(2.5), height=Inches(2.5))
    s.shapes.add_picture(WHALE, Inches(0.45), Inches(6.85), width=Inches(0.5), height=Inches(0.5))
    add_text(s, Inches(9.5), Inches(7.12), Inches(3.35), Inches(0.3),
             f"CLO835, Fall 2026     {n} / {total}", size=10, color=FOOTER_GRAY, align=RIGHT)


def sl_assumptions(s, n, total):
    title(s, "Assumptions")
    add_text(s, Inches(0.55), Inches(1.25), Inches(12.2), Inches(0.5),
             "The actions below should be completed before we continue to Amazon EKS.",
             size=14, italic=True, color=MUTED)
    bullets(s, 1.95, [
        (0, "You received email from AWS and created your root credentials"),
        (0, "You created a user with Admin permissions, the user has programmatic and console access"),
        (0, "You logged out from your root account, switched to the user you created. From this point on, you will be using the user credentials, never root credentials."),
        (0, "You can work in us-east-1 and us-west-2 regions only, preference to us-east-1"),
        (0, "Make sure budget alerts are set up. The monthly projected limit should be set to 30USD. Please reach out if you do not see budget alert set up in the CloudWatch service"),
    ], x=0.7, w=11.9, size=14, line_spacing=1.45)
    whale_and_footer(s, n, total)


def sl_course_outline(s, n, total):
    title(s, "Course Outline")
    course_outline(s, current_idx=8)
    whale_and_footer(s, n, total)


def sl_cost(s, n, total):
    title(s, "Cluster COST Estimate – Control Plane Only!")
    cost_card(s)
    whale_and_footer(s, n, total)


def sl_arch_highlevel(s, n, total):
    title(s, "Amazon EKS -  High level Architecture")
    bullets(s, 1.55, [
        (0, "Master nodes are running in AWS VPC, not in our VPC"),
        (0, "Amazon EKS API server can be either private or publicly accessible"),
        (0, "Worker nodes can be self-managed or AWS managed"),
    ], x=0.55, w=5.1, size=14, line_spacing=1.5)
    embed(s, "s05_1.png", 5.85, 1.5, 7.0, 4.9)
    whale_and_footer(s, n, total)


def sl_cluster_creation(s, n, total):
    title(s, "Amazon EKS Cluster creation")
    add_text(s, Inches(0.55), Inches(1.08), Inches(12.2), Inches(0.35),
             "Cluster creation spans two layers: the steps you run, and the managed "
             "control plane AWS provisions underneath.", size=13, color=BODY)
    # Row 1 — the workflow you run (blue timeline)
    add_text(s, Inches(0.55), Inches(1.55), Inches(3.4), Inches(0.4),
             "The workflow you run", size=14, bold=True, color=SLATE)
    bullets(s, 2.0, [
        (0, "Create the EKS cluster"),
        (0, "Provision worker nodes"),
        (0, "Launch add-ons"),
        (0, "Launch workloads"),
    ], x=0.55, w=3.4, size=12.5, line_spacing=1.3, space_after=4)
    embed(s, "s06_1.png", 4.1, 1.55, 8.6, 2.35)
    # Row 2 — what AWS provisions underneath (orange timeline)
    add_text(s, Inches(0.55), Inches(4.15), Inches(3.4), Inches(0.4),
             "Inside “Create EKS cluster” —\nwhat AWS manages for you",
             size=14, bold=True, color=SLATE, line_spacing=1.05)
    bullets(s, 5.0, [
        (0, "Create HA control plane"),
        (0, "IAM integration"),
        (0, "Certificate management"),
        (0, "Set up load balancer"),
    ], x=0.55, w=3.4, size=12.5, line_spacing=1.3, space_after=4)
    embed(s, "s06_2.png", 4.1, 4.15, 8.6, 2.35)
    whale_and_footer(s, n, total)


def sl_arch_comms(s, n, total):
    title(s, "EKS ARCHITECTURE FOR CONTROL PLANE AND WORKER NODE COMMUNICATION", size=22)
    embed(s, "s07_1.png", 1.0, 1.6, 11.33, 4.85)
    whale_and_footer(s, n, total)


def sl_w1_divider(s, n, total):
    divider(s, "WORK\nSHOP 1", "Creating Amazon EKS cluster with eksctl")
    whale_and_footer(s, n, total)


def sl_w1_goals(s, n, total):
    title(s, "Goals")
    bullets(s, 1.8, [
        (0, "Installing pre-requisites and configuring Cloud9 environment"),
        (0, "Configuring local environment"),
        (0, "Deployment K8s dashboard"),
    ], x=0.7, w=11.8, size=17, line_spacing=1.7)
    add_text(s, Inches(0.7), Inches(5.0), Inches(11.8), Inches(0.4),
             "https://www.eksworkshop.com/010_introduction/", font=FONT_MONO, size=13, color=BLUE)
    whale_and_footer(s, n, total)


def sl_disk(s, n, total):
    title(s, "Increase disk space of Cloud9 Environment")
    bullets(s, 1.8, [
        (0, "https://www.eksworkshop.com/020_prerequisites/workspace/", BLUE),
        (0, "The commands are available in Week8-Document."),
        (0, "Please note that we are not following all the workshop instructions."),
    ], x=0.7, w=11.8, size=16, line_spacing=1.7)
    whale_and_footer(s, n, total)


def sl_disable_creds(s, n, total):
    title(s, "Disable  temporary credentials")
    auto_term(s, 0.7, 1.55, 11.9, 4.8, "bash — credentials", [
        "# Make sure you are using AWS CLI version 2. Use these instructions to",
        "# update the AWS CLI version in your Cloud9 environment.",
        "$ /usr/local/bin/aws –-version",
        "",
        "# Configure your permanent credentials and disable Cloud9 temporary credentials",
        "$ /usr/local/bin/aws cloud9 update-environment \\",
        "      --environment-id $C9_PID --managed-credentials-action DISABLE",
        "$ rm -vf ${HOME}/.aws/credentials",
        "",
        "# Copy and paste the following credentials from AWS Academy into",
        "# ~/.aws/credentials in Cloud9",
    ], font_size=13)
    whale_and_footer(s, n, total)


def sl_prereqs(s, n, total):
    title(s, "Installing pre-requisites")
    bullets(s, 1.45, [
        (0, "Install kubectl - https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html"),
        (0, "Install eksctl  - https://docs.aws.amazon.com/eks/latest/userguide/eksctl.html"),
        (0, "Configure your permanent credentials and disable Cloud9 temporary credentials"),
        (0, "Update eks_config.yaml with your account id and correct K8s image (1.35)"),
        (0, "Create the cluster - this step will take a few minutes"),
        (0, "Update your Kube config"),
        (0, "Optional"),
        (1, "Increase disk space of Cloud9"), (1, "Install jq"), (1, "Update AWS CLI"),
        (1, "Install bash completion"), (1, "Add kubectl alias"),
        (1, "Set loadBalancer Controller version"), (1, "Enable eksctl bash completion"),
    ], x=0.7, w=11.9, size=13.5, line_spacing=1.3, space_after=4)
    whale_and_footer(s, n, total)


def sl_explore_cfn(s, n, total):
    title(s, "Explore  The created Resources  with CloudFormation")
    whale_and_footer(s, n, total)


def sl_explore_eks(s, n, total):
    title(s, "Explore  The Created cluster with Amazon EKS")
    whale_and_footer(s, n, total)


def sl_cluster_ready(s, n, total):
    title(s, "Cluster is ready – What runs in the cluster?")
    add_text(s, Inches(0.55), Inches(1.2), Inches(12.2), Inches(0.4),
             "Examine the cluster in AWS Console", size=14, color=BODY)
    embed(s, "s15_1.png", 3.0, 1.7, 7.3, 4.75)
    whale_and_footer(s, n, total)


def sl_use_kubectl(s, n, total):
    title(s, "Use Kubectl  to work with amazon EKS")
    auto_term(s, 1.0, 1.7, 11.3, 4.3, "bash — kubectl", [
        "# Can we use kubectl command?",
        "k get nodes",
        "",
        "# Update ~/.kube/config",
        "aws eks update-kubeconfig --name clo835 --region us-east-1",
        "",
        "# Update ~/.aws/config and remove the line aws_session_token=",
    ], font_size=14)
    whale_and_footer(s, n, total)


def sl_deploy_dashboard(s, n, total):
    title(s, "Deploy k8s dashboard")
    auto_term(s, 0.7, 1.6, 11.9, 4.5, "bash — dashboard", [
        'export DASHBOARD_VERSION="v2.0.0"',
        "kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/\\",
        "    ${DASHBOARD_VERSION}/aio/deploy/recommended.yaml",
        "",
        "# If above link doesn’t work use this -",
        "# https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.0-beta8/\\",
        "#     aio/deploy/recommended.yaml",
        "",
        "k get all -n kubernetes-dashboard",
    ], font_size=13)
    whale_and_footer(s, n, total)


def sl_view_dashboard(s, n, total):
    title(s, "View  the Dashboard from cloud9")
    bullets(s, 1.4, [
        (0, "Since this is deployed to our private cluster, we need to access it via a proxy. kube-proxy is available to proxy our requests to the dashboard service. In your workspace, run the following command:"),
    ], x=0.7, w=11.9, size=14, line_spacing=1.4)
    auto_term(s, 0.7, 2.85, 11.9, 1.0, "bash — proxy", [
        "kubectl proxy --port=8080 --address=0.0.0.0 --disable-filter=true &",
    ], font_size=13)
    bullets(s, 4.15, [
        (0, "This will start the proxy, listen on port 8080, listen on all interfaces, and will disable the filtering of non-localhost requests."),
        (0, "This command will continue to run in the background of the current terminal’s session."),
    ], x=0.7, w=11.9, size=14, line_spacing=1.4)
    whale_and_footer(s, n, total)


def sl_explore_dashboard(s, n, total):
    title(s, "Exploring Kubernetes Dashboard")
    bullets(s, 1.35, [
        (0, "Now we can access the Kubernetes Dashboard"),
        (0, "In your Cloud9 environment, click Tools / Preview / Preview Running Application"),
        (0, "Scroll to the end of the URL and append:"),
        (1, "/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/"),
        (0, "The Cloud9 Preview browser doesn’t support token auth — press Pop Out to open the login screen in a regular browser tab"),
        (0, "Copy the token output, click the Token radio button, paste it, then press Sign In"),
    ], x=0.55, w=6.4, size=12.5, line_spacing=1.3, space_after=5)
    yaml_terminal(s, 7.2, 1.4, 5.65, 2.65, "dashboard-adminuser.yaml", [
        "apiVersion: v1", "kind: ServiceAccount", "metadata:",
        "  name: admin-user", "  namespace: kubernetes-dashboard",
    ], font_size=12)
    auto_term(s, 7.2, 4.25, 5.65, 2.15, "bash — token", [
        "$ kubectl apply -f \\",
        "    dashboard-adminuser.yaml",
        "",
        "$ kubectl -n kubernetes-dashboard \\",
        "    create token admin-user",
    ], font_size=12)
    whale_and_footer(s, n, total)


def sl_w1_end(s, n, total):
    closing(s, "End of  Workshop 1")
    whale_and_footer(s, n, total)


def sl_volume_lifecycle(s, n, total):
    title(s, "Volume Lifecycle")
    bullets(s, 1.75, [
        (0, "The lifecycle of a volume is linked to the pod's lifecycle"),
        (0, "This means that a volume is created when the pod is created"),
        (0, "This is mostly relevant for emptyDir volumes"),
        (0, "(other volumes, like remote storage, are not \"created\" but rather \"attached\" )"),
        (0, "A volume survives across container restarts"),
        (0, "A volume is destroyed (or, for remote storage, detached) when the pod is destroyed"),
    ], x=0.7, w=11.8, size=16, line_spacing=1.6)
    whale_and_footer(s, n, total)


def sl_w2_divider(s, n, total):
    divider(s, "WORK\nSHOP 2", "Deployment of our first application to Amazon EKS")
    whale_and_footer(s, n, total)


def sl_w2_goals(s, n, total):
    title(s, "Goals")
    bullets(s, 2.0, [
        (0, "Deployment of containerized application that uses emptyDir Volume to share data between containers"),
        (0, "Serving the application to external users with LoadBalancer service"),
    ], x=0.7, w=11.8, size=17, line_spacing=1.7)
    whale_and_footer(s, n, total)


def sl_desc1(s, n, total):
    title(s, "Description")
    bullets(s, 1.55, [
        (0, "Application is running as two containers in the same pod"),
        (0, "One process is generating random fortune every 10 seconds and writes it to a shared volumes"),
        (0, "The same volume is mounted into nginx container as /usr/share/nginx/html. Nginx serves the fortunes from this folder"),
    ], x=0.55, w=6.4, size=14, line_spacing=1.5)
    embed(s, "s24_1.png", 7.2, 1.7, 5.6, 4.6)
    whale_and_footer(s, n, total)


def sl_desc2(s, n, total):
    title(s, "Description")
    bullets(s, 1.55, [
        (0, "Application is running as two containers in the same pod"),
        (0, "One process is generating random fortune every 10 seconds and writes it to a shared volumes"),
        (0, "The same volume is mounted into nginx container as /usr/share/nginx/html. Nginx serves the fortunes from this folder"),
    ], x=0.55, w=6.4, size=14, line_spacing=1.5)
    embed(s, "s25_1.jpg", 7.2, 1.7, 5.6, 4.6)
    whale_and_footer(s, n, total)


def sl_pod_manifest(s, n, total):
    title(s, "Pod Manifest")
    embed(s, "s26_1.jpg", 1.5, 2.3, 10.3, 3.4)
    whale_and_footer(s, n, total)


def sl_deploy_access(s, n, total):
    title(s, "Deploy and Access the application")
    auto_term(s, 0.55, 1.6, 7.0, 4.8, "bash — deploy", [
        "# Create a namespace",
        "$ k create ns week8",
        "",
        "# Deploy the pod",
        "$ k apply -f fortune_pod.yaml -n week8",
        "$ k get all –n week8",
        "",
        "# Access the app via port forwarding",
        "$ kubectl port-forward fortune 8080:80 -n week8",
        "$ curl http://localhost:8080",
    ], font_size=12)
    embed(s, "s27_1.png", 7.8, 1.9, 5.0, 4.2)
    whale_and_footer(s, n, total)


def sl_examine_volume(s, n, total):
    title(s, "Examine the mounted volume")
    auto_term(s, 0.7, 1.6, 11.9, 4.8, "bash — exec", [
        "# Attach shell to web-server container inside fortune Pod",
        "$ k exec  fortune -it -n week8 -c web-server -- sh",
        "/ # cat /usr/share/nginx/html/index.html",
        "Try the Moo Shu Pork.  It is especially good today.",
        "",
        "# Wait 10 seconds",
        "/ # cat /usr/share/nginx/html/index.html",
        "You will be run over by a beer truck.",
        "",
        "# Try upating the index.html file",
        "/ # vi /usr/share/nginx/html/index.html",
        "Why does the editing attempt fail?",
    ], font_size=13)
    whale_and_footer(s, n, total)


def sl_nodeport(s, n, total):
    title(s, "Expose Fortunes via NodePort")
    auto_term(s, 0.55, 1.6, 7.2, 3.4, "bash — nodeport", [
        "$ k expose pod fortune -n week8 --type NodePort -n week8",
        "",
        "# K8s assigned a NodePort randomly. There only one pod",
        "# and 2 nodes.",
        "# What IP should we use to access the application?",
        "# The IPs of both nodes respond. Why?",
    ], font_size=12)
    embed(s, "s29_1.png", 8.0, 1.7, 4.8, 1.1, halign='center', valign='top')
    embed(s, "s29_2.png", 8.0, 3.0, 4.8, 1.3, halign='center', valign='top')
    whale_and_footer(s, n, total)


def sl_lb1(s, n, total):
    title(s, "Expose Fortunes via LoadBalancer")
    auto_term(s, 0.7, 1.55, 11.9, 1.55, "bash — loadbalancer", [
        "$ k delete service fortune -n week8",
        "$ k expose pod fortune -n week8 --type LoadBalancer  -n week8",
    ], font_size=13)
    embed(s, "s30_1.png", 2.4, 3.35, 8.5, 3.05)
    whale_and_footer(s, n, total)


def sl_lb2(s, n, total):
    title(s, "Expose Fortunes via LoadBalancer")
    embed(s, "s31_1.png", 3.9, 1.5, 5.5, 5.0)
    whale_and_footer(s, n, total)


def sl_w2_end(s, n, total):
    closing(s, "End of  Workshop 2")
    whale_and_footer(s, n, total)


def sl_reading(s, n, total):
    title(s, "Additional Reading")
    bullets(s, 1.8, [
        (0, "https://kubernetes.io/docs/concepts/storage/volumes/", BLUE),
        (0, "https://kubernetes.io/docs/tasks/configure-pod-container/configure-volume-storage/", BLUE),
        (0, "https://aws.amazon.com/premiumsupport/knowledge-center/eks-persistent-storage/", BLUE),
        (0, "https://docs.giantswarm.io/getting-started/persistent-volumes/aws/", BLUE),
        (0, "https://github.com/weaveworks/eksctl/tree/main/examples", BLUE),
        (0, "https://eksctl.io/", BLUE),
    ], x=0.7, w=11.9, size=14, line_spacing=1.7)
    whale_and_footer(s, n, total)


# ---- Concept / theory slides (lecture) -------------------------------------

def sl_managed_vs_self(s, n, total):
    title(s, "Managed vs Self-managed Kubernetes")
    add_text(s, Inches(0.55), Inches(1.12), Inches(12.2), Inches(0.4),
             "EKS is managed Kubernetes: AWS runs the hard parts so you can focus on your apps.",
             size=14, color=BODY)
    concept_card(s, 0.7, 1.75, 5.8, 4.15, "AWS runs for you", [
        "The control plane",
        "API server & scheduler",
        "etcd (the cluster database)",
        "Multi-AZ high availability",
        "Version upgrades & patching",
    ], BLUE, body_size=13)
    concept_card(s, 6.85, 1.75, 5.8, 4.15, "You own", [
        "Worker nodes (EC2 or Fargate)",
        "Your workloads (pods, services)",
        "Scaling & app configuration",
        "App data & access policies",
    ], SLATE, body_size=13)
    add_text(s, Inches(0.7), Inches(6.05), Inches(11.95), Inches(0.4),
             "Why EKS?  Less cluster operations — more time on your applications.",
             size=13.5, italic=True, color=MUTED, align=CENTER)
    whale_and_footer(s, n, total)


def sl_control_plane(s, n, total):
    title(s, "The EKS Control Plane")
    add_text(s, Inches(0.55), Inches(1.12), Inches(12.2), Inches(0.4),
             "The control plane is the brain of the cluster — and AWS fully manages it.",
             size=14, color=BODY)
    bullets(s, 1.7, [
        (0, "Fully managed by AWS — you never install, run, or upgrade it"),
        (0, "Highly available across multiple Availability Zones (multi-AZ)"),
        (0, "Runs the API server, scheduler, controllers, and etcd"),
        (0, "AWS handles scaling, monitoring, and patching for you"),
        (0, "No SSH and no master access — you reach it only through the Kubernetes API"),
    ], x=0.7, w=11.8, size=15.5, line_spacing=1.55)
    callout(s, 0.7, 5.55, 11.95, 0.85,
            "You interact with the cluster using kubectl — never by logging into servers.", BLUE)
    whale_and_footer(s, n, total)


def sl_worker_nodes(s, n, total):
    title(s, "Worker Node Options")
    add_text(s, Inches(0.55), Inches(1.12), Inches(12.2), Inches(0.4),
             "Where your pods actually run. EKS gives you three choices:", size=14, color=BODY)
    concept_card(s, 0.55, 1.75, 3.85, 4.0, "Managed Node Groups", [
        "EC2 nodes AWS provisions for you",
        "AWS handles create, update & drain",
        "Easiest day-to-day option",
    ], BLUE, body_size=12.5)
    concept_card(s, 4.7, 1.75, 3.85, 4.0, "Self-managed EC2", [
        "You create & run the EC2 nodes",
        "Full control over the instances",
        "More setup & maintenance",
    ], STEPS[3], body_size=12.5)
    concept_card(s, 8.85, 1.75, 3.85, 4.0, "Fargate", [
        "Serverless — no nodes to manage",
        "AWS runs each pod for you",
        "Pay per pod, not per node",
    ], STEPS[1], body_size=12.5)
    add_text(s, Inches(0.55), Inches(5.95), Inches(12.2), Inches(0.4),
             "One cluster can mix managed node groups and Fargate.",
             size=13.5, italic=True, color=MUTED, align=CENTER)
    whale_and_footer(s, n, total)


def sl_networking(s, n, total):
    title(s, "EKS Networking")
    add_text(s, Inches(0.55), Inches(1.12), Inches(12.2), Inches(0.4),
             "Pods live inside your VPC and get real network identities.", size=14, color=BODY)
    bullets(s, 1.75, [
        (0, "VPC CNI — every pod gets a real VPC IP address (not a hidden overlay network)"),
        (0, "The cluster API endpoint can be public, private, or both:"),
        (1, "Public — reach the cluster API from the internet"),
        (1, "Private — reach it only from inside your VPC"),
        (0, "Control plane ↔ worker nodes talk over AWS-managed ENIs placed in your VPC, secured with TLS"),
    ], x=0.7, w=11.8, size=15, line_spacing=1.5)
    add_text(s, Inches(0.7), Inches(5.95), Inches(11.95), Inches(0.4),
             "This is the control-plane ↔ node path shown in the previous diagram.",
             size=13, italic=True, color=MUTED)
    whale_and_footer(s, n, total)


def sl_access_provisioning(s, n, total):
    title(s, "Access & Provisioning")
    concept_card(s, 0.7, 1.5, 5.8, 4.5, "Authentication & authorization", [
        "Who you are → AWS IAM (your user or role)",
        "What you can do in the cluster → Kubernetes RBAC",
        "aws eks update-kubeconfig wires kubectl to the cluster using your IAM identity",
    ], BLUE, body_size=13)
    concept_card(s, 6.85, 1.5, 5.8, 4.5, "eksctl & provisioning", [
        "eksctl = the official CLI to create & manage EKS clusters",
        "Under the hood it builds AWS CloudFormation stacks (Infrastructure as Code)",
        "You describe the cluster in a config file: eks_config.yaml",
    ], SLATE, body_size=13)
    whale_and_footer(s, n, total)


# ============================================================================
# Deck composition.  THEORY slides marked (dup) appear in BOTH decks so the
# lab is self-contained with theory next to the practical steps.
# ============================================================================

LECTURE = [
    lambda s, n, t: sl_cover(s, n, t, "Lecture"),
    sl_course_outline,
    sl_managed_vs_self,         # NEW — the "why EKS" concept (before cost/architecture)
    sl_cost,
    sl_arch_highlevel,          # theory (dup in lab)
    sl_control_plane,           # NEW — zooms into the managed control plane
    sl_worker_nodes,            # NEW — the other half: where pods run
    sl_cluster_creation,        # theory (dup in lab)
    sl_arch_comms,              # theory (dup in lab)
    sl_networking,              # NEW — concept text for the comms diagram above
    sl_access_provisioning,     # NEW — IAM/RBAC + eksctl/CloudFormation
    sl_volume_lifecycle,        # theory (dup in lab)
    sl_reading,
]

LAB = [
    lambda s, n, t: sl_cover(s, n, t, "Lab"),
    sl_assumptions,             # prerequisites (kept hidden, as in source)
    # --- theory recap for context (duplicated from the lecture) ---
    sl_arch_highlevel,
    sl_arch_comms,
    # --- Workshop 1 ---
    sl_w1_divider, sl_w1_goals, sl_disk, sl_disable_creds, sl_prereqs,
    sl_explore_cfn, sl_explore_eks, sl_cluster_ready, sl_use_kubectl,
    sl_deploy_dashboard, sl_view_dashboard, sl_explore_dashboard, sl_w1_end,
    # --- theory recap before Workshop 2 (duplicated) ---
    sl_volume_lifecycle,
    # --- Workshop 2 ---
    sl_w2_divider, sl_w2_goals, sl_desc1, sl_desc2, sl_pod_manifest,
    sl_deploy_access, sl_examine_volume, sl_nodeport, sl_lb1, sl_lb2, sl_w2_end,
    sl_reading,
]

# Slide index (1-based) within the LAB deck that must stay hidden (the
# Assumptions prerequisite slide — preserves the source's hidden state).
LAB_HIDDEN = {2}


def build(deck, out, hidden=frozenset()):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]
    total = len(deck)
    for i, fn in enumerate(deck, 1):
        s = prs.slides.add_slide(blank)
        fn(s, i, total)
        if i in hidden:
            hide(s)
    _sanitize_coords(prs)
    prs.save(out)
    print(f"wrote {out}  ({total} slides)")


# ===== Save =====
if __name__ == "__main__":
    build(LECTURE, f"Week08/Week08_lecture_style_{LECTURE_VERSION}.pptx")
    build(LAB, f"Week08/Week08_lab_style_{LAB_VERSION}.pptx", hidden=LAB_HIDDEN)
