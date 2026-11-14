"""Week12 — CLO835 Lab02/Week05 house design language applied to the Week 12 deck.

Source: Week12/Week12.pptx — 37 slides, "ConfigMaps and Secrets" (the source deck
self-labels this as Week 10 on its cover and course outline; folder is Week12).
Original slide text preserved verbatim (no rephrasing, typos kept per PROMPT.md R1).

v2 splits the source into TWO decks like the other weeks: a LECTURE deck (theory +
front/back matter) and a LAB deck (Workshop 1 ConfigMaps + Workshop 2 Secrets, hands-on
steps + cleanup, own cover). Exact CLO835 palette + Calibri/Consolas + chrome, coordinate
guard, native course-outline grid, dark terminal mockups for shell/YAML, workshop dividers.
Content is baked into DECK (from the source deck); rendered by type-driven functions.
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
EXAM_RED    = RGBColor(0xFF, 0x6B, 0x6B)
STEPS = [
    RGBColor(0x1F, 0xA8, 0xE0), RGBColor(0x21, 0x96, 0xA0),
    RGBColor(0x1F, 0x8F, 0xCD), RGBColor(0x1F, 0x7A, 0xB8),
    RGBColor(0x24, 0x66, 0xA0), RGBColor(0x37, 0x46, 0x5A),
]
FONT_SANS, FONT_MONO = "Calibri", "Consolas"

K8S_LOGO = "Week04/Kubernetes_logo_without_workmark.svg.png"
WHALE    = "whale.png"
VERSION  = "v2"
WEEK_LABEL = "Week 10"            # source self-labels ConfigMaps & Secrets as Week 10
DECK_TITLE = "ConfigMaps & Secrets"
ASSETS_DIR = "Week12/assets"
# Slides whose core content is a genuine image-stored DIAGRAM (boxes/arrows/volumes)
# not reconstructable from text: embed the cropped original figure (house pattern).
# Slides 6 and 10 are rebuilt natively (their content is text/YAML/table) — see render_s06/s10.
FIG = {25: "fig25.png", 35: "fig35.png"}
FIG_ASPECT = {"fig25.png": [780, 360], "fig35.png": [704, 480], "fig09.png": [648, 440], "fig12.png": [732, 414]}


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
    shp = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, _i(x), _i(y), _i(w), _i(h))
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    shp.line.fill.background(); shp.shadow.inherit = False
    return shp


def add_down_arrow(s, x, y, w, h, fill):
    shp = s.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, _i(x), _i(y), _i(w), _i(h))
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    shp.line.fill.background(); shp.shadow.inherit = False
    return shp


def whale_and_footer(s, page_num, total):
    s.shapes.add_picture(WHALE, Inches(0.45), Inches(6.85), width=Inches(0.5), height=Inches(0.5))
    add_line(s, Inches(0.5), Inches(7.05), Inches(12.83), Inches(7.05), color=RULE_GRAY, width=0.5)
    add_text(s, Inches(9.5), Inches(7.12), Inches(3.35), Inches(0.3),
             f"CLO835, Fall 2026     {page_num} / {total}",
             size=10, color=FOOTER_GRAY, align=RIGHT)


def title(s, text, y=0.40, size=30):
    # Adaptive: shrink long titles so they don't dominate, and drop the underline
    # rule BELOW the (possibly wrapped) text so it never strikes through line 2.
    n = len(text)
    if n > 60:
        size = 25
    if n > 90:
        size = 22
    cpl = max(12, int(12.2 * 72 / (size * 0.50)))   # ~chars per 12.2in line
    lines = max(1, -(-n // cpl))                     # ceil
    line_h = size * 1.2 / 72.0                        # rendered line height (in)
    text_h = lines * line_h + 0.10
    ul_y = y + max(0.98, text_h + 0.06)
    add_text(s, Inches(0.55), Inches(y), Inches(12.2), Inches(text_h + 0.25),
             text, size=size, bold=True, color=BLUE, line_spacing=1.02)
    add_line(s, Inches(0.57), Inches(ul_y), Inches(5.2), Inches(ul_y), color=BLUE, width=2.0)


_GLYPH = {0: "▪  ", 1: "–  ", 2: "•  "}
_GCOL  = {0: BLUE, 1: STEPS[1], 2: MUTED}
_MARG  = {0: 0.0, 1: 0.42, 2: 0.84}


def bullets(s, y, items, *, x=0.6, w=12.1, size=15, line_spacing=1.32, space_after=8, level_step=1):
    h = max(0.5, 6.7 - y)
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
        sz = size - lvl * level_step
        r0 = p.add_run(); r0.text = _GLYPH[lvl]
        r0.font.name = FONT_SANS; r0.font.size = Pt(sz); r0.font.bold = True
        r0.font.color.rgb = _GCOL[lvl]
        r1 = p.add_run(); r1.text = text
        r1.font.name = FONT_SANS; r1.font.size = Pt(sz); r1.font.color.rgb = col
    return tb


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
    tb = s.shapes.add_textbox(x + Inches(0.18), y + bar_h + Inches(0.08),
                              w - Inches(0.32), h - bar_h - Inches(0.12))
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Inches(0)
    tf.word_wrap = True
    for i, para in enumerate(body_runs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = LEFT
        p.line_spacing = 1.12
        if not para:
            r = p.add_run(); r.text = " "
            r.font.name = FONT_MONO; r.font.size = Pt(font_size)
            continue
        for text, color in para:
            r = p.add_run(); r.text = text
            r.font.name = FONT_MONO; r.font.size = Pt(font_size); r.font.color.rgb = color


_CMD_STARTS = ("$", "k ", "k8s", "kubectl", "aws", "export", "curl", "rm", "vi ",
               "cat", "sudo", "/usr", "/ #", "ssh", "scp", "echo", "openssl", "eksctl",
               "docker", "base64", "kubeadm")


def _role(line):
    if line == "":
        return None
    st = line.lstrip()
    if st.startswith("#"):
        return TERM_GRN
    if "ERROR" in line or "error" in st[:6] or "fail" in st[:5].lower():
        return TERM_ERR
    if any(st.startswith(c) for c in _CMD_STARTS):
        return TERM_CYAN
    return TERM_GRAY


def auto_term(s, x, y, w, h, title_text, raw, *, font_size=11):
    runs = []
    for ln in raw:
        col = _role(ln)
        runs.append([] if col is None else [(ln, col)])
    terminal(s, Inches(x), Inches(y), Inches(w), Inches(h), title_text, runs, font_size=font_size)


def callout(s, x, y, w, h, text, accent=BLUE):
    add_rounded_rect(s, Inches(x), Inches(y), Inches(w), Inches(h), CARD_BG,
                     line=RULE_GRAY, line_width=0.75, radius_ratio=0.08)
    add_rect(s, Inches(x), Inches(y + 0.05), Inches(0.12), Inches(h - 0.10), accent)
    add_text(s, Inches(x + 0.34), Inches(y + 0.10), Inches(w - 0.55), Inches(h - 0.2),
             text, size=12.5, color=BODY, anchor=MIDDLE, line_spacing=1.15)


def divider(s, kicker, text, subtitle=None):
    d = Inches(1.6); cx = Inches(13.333 / 2) - d / 2
    add_oval(s, cx, Inches(1.85), d, d, SLATE)
    add_text(s, cx, Inches(2.35), d, Inches(0.6), kicker,
             size=20, bold=True, color=WHITE, align=CENTER, anchor=MIDDLE)
    add_text(s, Inches(1.0), Inches(3.95), Inches(11.33), Inches(1.1), text,
             size=28, bold=True, color=SLATE, align=CENTER, line_spacing=1.05)
    if subtitle:
        add_text(s, Inches(1.0), Inches(5.15), Inches(11.33), Inches(0.6), subtitle,
                 size=15, italic=True, color=MUTED, align=CENTER)


def closing(s, text):
    add_oval(s, Inches(13.333 / 2) - Inches(0.8), Inches(2.2), Inches(1.6), Inches(1.6),
             WHITE, line=LIGHTBLUE, line_width=1.5)
    s.shapes.add_picture(K8S_LOGO, Inches(13.333 / 2) - Inches(0.6), Inches(2.4),
                         width=Inches(1.2), height=Inches(1.2))
    add_text(s, Inches(1.0), Inches(4.25), Inches(11.33), Inches(1.0), text,
             size=32, bold=True, color=BLUE, align=CENTER, line_spacing=1.05)


def course_outline(s, items, highlights):
    cols, rows = 4, 4
    x0, y0 = 0.7, 1.75
    tw, th = 2.85, 1.02
    gx, gy = 0.27, 0.28
    for idx, label in enumerate(items):
        r, c = idx // cols, idx % cols
        # boustrophedon column so arrows read continuously
        cc = c if r % 2 == 0 else (cols - 1 - c)
        x = x0 + cc * (tw + gx); y = y0 + r * (th + gy)
        hi = idx in highlights
        fill = highlights[idx] if hi else CARD_BG
        line = SLATE if hi else RULE_GRAY
        add_rounded_rect(s, Inches(x), Inches(y), Inches(tw), Inches(th), fill,
                         line=line, line_width=1.5 if hi else 0.75, radius_ratio=0.10)
        add_text(s, Inches(x + 0.16), Inches(y), Inches(tw - 0.32), Inches(th),
                 label, size=10.5, bold=hi,
                 color=WHITE if hi else SLATE, anchor=MIDDLE, align=CENTER, line_spacing=1.02)


# ---------- title casing (house titles are not ALL-CAPS) ----------
_KEEP = {
    "configmaps": "ConfigMaps", "configmap": "ConfigMap", "secrets": "Secrets",
    "secret": "Secret", "k8s": "K8s", "kubernetes": "Kubernetes", "https": "HTTPS",
    "http": "HTTP", "pod": "POD", "pods": "PODs", "cmd": "CMD", "yaml": "YAML",
    "etcd": "ETCD", "scm": "SCM", "dns": "DNS", "rbac": "RBAC", "aks": "AKS",
    "eks": "EKS", "cont": "Cont", "entrypoint": "ENTRYPOINT", "nginx": "nginx",
    "docker": "Docker", "the": "the", "in": "in", "to": "to", "with": "with",
    "and": "and", "a": "a", "of": "of", "as": "as", "or": "or", "for": "for",
    "using": "using", "through": "through", "into": "into", "is": "is",
}
_SMALL = {"the", "in", "to", "with", "and", "a", "of", "as", "or", "for",
          "using", "through", "into", "is", "on", "by"}


def smart_title(t):
    t = " ".join(t.split())
    out = []
    for i, w in enumerate(t.split(" ")):
        lw = w.lower().strip(":,.-")
        punct = w[len(w.rstrip(":,.-")):]
        core = w.rstrip(":,.-")
        has_lower = any(ch.islower() for ch in core)
        has_upper_inner = any(ch.isupper() for ch in core[1:])
        if lw in _KEEP and not (i == 0 and lw in _SMALL):
            word = _KEEP[lw]           # stopwords stay lowercase EXCEPT as the first word
        elif has_upper_inner and has_lower:
            word = core            # genuine mixed case (e.g. ConfigMap), keep as-is
        elif lw in _SMALL and i != 0:
            word = lw
        else:
            word = core[:1].upper() + core[1:].lower() if core else core
        out.append(word + punct)
    return " ".join(out)


# ============================================================================
# Type-driven rendering
# ============================================================================

def _flatten_code(code_blocks):
    lines = []
    for i, blk in enumerate(code_blocks):
        if i > 0:
            lines.append("")
        lines.extend(blk.get("lines", []))
    return lines


def _fit_font(nlines, h_in, lo=7, hi=11):
    if nlines <= 0:
        return hi
    # A terminal reserves ~0.5in for its title bar + top/bottom padding, so the
    # text area is h-0.5, NOT the full h. Sizing against full h picks a font a
    # size too big and the last lines spill past the box. Use the real text area.
    usable = max(0.5, h_in - 0.5)
    f = int(usable * 72 / (nlines * 1.52))   # ~1.52x point-size per rendered line
    return max(lo, min(hi, f))


def _split_at_blank(code):
    blanks = [i for i, l in enumerate(code) if l.strip() == ""]
    mid = len(code) / 2.0
    if blanks:
        b = min(blanks, key=lambda i: abs(i - mid))
        if abs(b - mid) <= len(code) * 0.28:
            return code[:b], code[b + 1:]
    m = len(code) // 2
    return code[:m], code[m:]


def two_col_terminal(s, y, h, code, title_text="bash"):
    left, right = _split_at_blank(code)
    n = max(len(left), len(right))
    fs = _fit_font(n, h, lo=8, hi=10)
    auto_term(s, 0.7, y, 5.95, h, title_text, left, font_size=fs)
    auto_term(s, 6.85, y, 5.95, h, title_text, right, font_size=fs)


def embed_fig(s, fname, x, y, w, h, caption=None):
    aw, ah = FIG_ASPECT[fname]
    ar = aw / ah
    if (w / h) > ar:
        dh = h; dw = h * ar
    else:
        dw = w; dh = w / ar
    dx = x + (w - dw) / 2.0; dy = y + (h - dh) / 2.0
    add_rect(s, Inches(dx - 0.04), Inches(dy - 0.04), Inches(dw + 0.08), Inches(dh + 0.08),
             WHITE, line=RULE_GRAY, line_width=0.75)
    s.shapes.add_picture(os.path.join(ASSETS_DIR, fname),
                         _i(Inches(dx)), _i(Inches(dy)), _i(Inches(dw)), _i(Inches(dh)))
    if caption:
        add_text(s, Inches(x), Inches(y + h + 0.02), Inches(w), Inches(0.3), caption,
                 size=11, italic=True, color=MUTED, align=CENTER)


def render_cover(s, n, total, role="Lecture"):
    add_text(s, Inches(0.7), Inches(2.55), Inches(8.7), Inches(1.5),
             DECK_TITLE, size=42, bold=True, color=BLUE, line_spacing=1.05)
    add_text(s, Inches(0.72), Inches(4.15), Inches(8.5), Inches(0.6),
             f"{WEEK_LABEL} · {role}", size=22, color=SLATE)
    add_text(s, Inches(0.72), Inches(4.85), Inches(8.5), Inches(0.5),
             "“Week 10 feels like 100”", size=15, italic=True, color=MUTED)
    logo_cx = Inches(10.7); logo_cy = Inches(3.55); ring_r = Inches(1.8)
    add_oval(s, logo_cx - ring_r, logo_cy - ring_r, ring_r * 2, ring_r * 2, WHITE,
             line=LIGHTBLUE, line_width=1.5)
    s.shapes.add_picture(K8S_LOGO, logo_cx - Inches(1.25), logo_cy - Inches(1.25),
                         width=Inches(2.5), height=Inches(2.5))
    s.shapes.add_picture(WHALE, Inches(0.45), Inches(6.85), width=Inches(0.5), height=Inches(0.5))
    add_text(s, Inches(9.5), Inches(7.12), Inches(3.35), Inches(0.3),
             f"CLO835, Fall 2026     {n} / {total}", size=10, color=FOOTER_GRAY, align=RIGHT)


def _norm(l):
    return " ".join(l.split())


def render_content(s, body, code_blocks):
    items = [(min(b["level"], 2), b["text"]) for b in body]
    code = _flatten_code(code_blocks)
    # Some workshop slides had their command lines double-captured: once as body
    # bullets and again as the head of the terminal block (which also holds the
    # long command OUTPUT). Rendering both duplicates the commands and overflows
    # the terminal. If the body merely repeats terminal lines, drop it and let the
    # terminal (commands + output, house-styled) stand alone.
    code_set = set(_norm(l) for l in code if l.strip())
    if items and code_set:
        dup = sum(1 for _, t in items if _norm(t) in code_set)
        if dup >= max(1, int(0.7 * len(items))):
            items = []
    has_body = bool(items)
    has_code = any(ln.strip() for ln in code)
    if has_code:
        ncode = len(code)
        if has_body and ncode <= 14 and len(items) <= 4:
            # side-by-side: bullets left, terminal right
            bullets(s, 1.7, items, x=0.6, w=6.0, size=13.5, line_spacing=1.26, space_after=6)
            h = 5.0
            auto_term(s, 6.95, 1.7, 5.85, h, "bash", code, font_size=_fit_font(ncode, h, lo=9, hi=11))
        elif has_body:
            # ALL bullets on top (compact), code below (two-col if long) — never drop bullets
            bullets(s, 1.58, items, x=0.6, w=12.1, size=12, line_spacing=1.15, space_after=2)
            cy = min(1.58 + len(items) * 0.265 + 0.16, 3.75)
            h = 6.9 - cy
            if ncode <= 16:
                auto_term(s, 0.9, cy, 11.5, h, "bash", code, font_size=_fit_font(ncode, h, lo=8, hi=11))
            else:
                two_col_terminal(s, cy, h, code)
        elif ncode <= 24:
            fs = _fit_font(ncode, 5.15, lo=9, hi=12)
            # size the terminal to its content so a few lines don't leave a huge void
            needed = 0.5 + ncode * (fs * 1.52 / 72.0) + 0.22
            h = min(5.15, max(1.3, needed))
            auto_term(s, 0.9, 1.65, 11.5, h, "bash", code, font_size=fs)
        else:
            two_col_terminal(s, 1.65, 5.15, code)
    elif has_body:
        sz = 16 if len(items) <= 6 else 14
        bullets(s, 1.75, items, x=0.6, w=12.1, size=sz)
    else:
        pass


def comparison_table(s, x, y, w, headers, rows, col_ratios,
                     *, header_h=0.46, row_h=0.62, hsize=12.5, bsize=12):
    """House-style table: slate header row, alternating white/tint body rows, gray rules.
    First two columns render monospace/slate (they hold keywords)."""
    xs = [x]
    for r in col_ratios:
        xs.append(xs[-1] + w * r)
    add_rect(s, Inches(x), Inches(y), Inches(w), Inches(header_h), SLATE)
    for i, htext in enumerate(headers):
        cw = w * col_ratios[i]
        add_text(s, Inches(xs[i] + 0.14), Inches(y), Inches(cw - 0.24), Inches(header_h),
                 htext, size=hsize, bold=True, color=WHITE, anchor=MIDDLE)
    cy = y + header_h
    for ri, row in enumerate(rows):
        fill = WHITE if ri % 2 == 0 else CARD_BG
        add_rect(s, Inches(x), Inches(cy), Inches(w), Inches(row_h), fill,
                 line=RULE_GRAY, line_width=0.75)
        for i, cell in enumerate(row):
            cw = w * col_ratios[i]
            mono = (i < 2)
            add_text(s, Inches(xs[i] + 0.14), Inches(cy), Inches(cw - 0.24), Inches(row_h),
                     cell, font=FONT_MONO if mono else FONT_SANS, size=bsize,
                     color=SLATE if mono else BODY, anchor=MIDDLE, line_spacing=1.05)
        cy += row_h


def render_s06(s, n, total, d):
    """Passing command line arguments: bullets + pod.yaml terminal + Docker/K8s table."""
    title(s, smart_title(d["title"].replace("\n", " ")))
    items = [(min(b["level"], 2), b["text"]) for b in d["body"]]
    bullets(s, 1.85, items, x=0.6, w=5.85, size=14, line_spacing=1.32, space_after=12)
    yaml = d["code_blocks"][0]["lines"] if d["code_blocks"] else []
    auto_term(s, 6.85, 1.85, 5.95, 2.45, "pod.yaml", yaml, font_size=12)
    headers = ["Docker", "Kubernetes", "Description"]
    rows = [["ENTRYPOINT", "command", "The executable that's executed inside the container"],
            ["CMD", "args", "The arguments passed to the executable"]]
    comparison_table(s, 0.7, 4.85, 11.95, headers, rows, [0.17, 0.15, 0.68])
    whale_and_footer(s, n, total)


def render_s10(s, n, total, d):
    """ConfigMaps - Create: bullet hierarchy + imperative/declarative terminals (mirrors s22)."""
    title(s, smart_title(d["title"].replace("\n", " ")))
    items = [(min(b["level"], 2), b["text"]) for b in d["body"]]
    bullets(s, 1.55, items, x=0.6, w=12.0, size=15, line_spacing=1.16, space_after=3)
    imperative = [
        "kubectl create configmap",
        "    <config-name> --from-literal=<key>=<value>",
        "",
        "kubectl create configmap \\",
        "    app-config --from-literal=APP_COLOR=blue \\",
        "          --from-literal=APP_MOD=prod",
        "",
        "kubectl create configmap",
        "    <config-name> --from-file=<path-to-file>",
        "",
        "kubectl create configmap",
        "    app-config --from-file=app_config.properties",
    ]
    declarative = [
        "kubectl create -f",
        "",
        "apiVersion: v1",
        "kind: ConfigMap",
        "metadata:",
        "  name: app-config",
        "data:",
        "  APP_COLOR: blue",
        "  APP_MODE: prod",
        "",
        "kubectl create -f config-map.yaml",
    ]
    # content-fit both terminals (kill the empty black area) + auto-maximize the font
    cy = 3.15
    avail = 6.72 - cy
    nmax = max(len(imperative), len(declarative))
    fs = 13
    while fs > 9 and (0.5 + nmax * (fs * 1.52 / 72.0) + 0.22) > avail:
        fs -= 1
    h = 0.5 + nmax * (fs * 1.52 / 72.0) + 0.22
    auto_term(s, 0.7, cy, 5.95, h, "imperative", imperative, font_size=fs)
    auto_term(s, 6.85, cy, 5.95, h, "declarative", declarative, font_size=fs)
    whale_and_footer(s, n, total)


def _bullets_and_figure(s, n, total, d, fname, fig_box):
    """Bullets on the left, an embedded cropped source diagram on the right."""
    title(s, smart_title(d["title"].replace("\n", " ")))
    items = [(min(b["level"], 2), b["text"]) for b in d["body"]]
    bullets(s, 1.95, items, x=0.6, w=4.35, size=14.5, line_spacing=1.34, space_after=12)
    embed_fig(s, fname, *fig_box)
    whale_and_footer(s, n, total)


def render_s09(s, n, total, d):
    _bullets_and_figure(s, n, total, d, "fig09.png", (5.25, 1.75, 7.55, 4.85))


def render_s12(s, n, total, d):
    _bullets_and_figure(s, n, total, d, "fig12.png", (5.25, 1.75, 7.55, 4.85))


def render_s04(s, n, total, d):
    """Configuring containerized apps — user-tuned: uniform 14pt bullets (nudged up to
    y=1.47, level-1 not shrunk), nginx.conf split across two terminals (font 8)."""
    title(s, smart_title(d["title"].replace("\n", " ")))
    items = [(min(b["level"], 2), b["text"]) for b in d["body"]]
    bullets(s, 1.47, items, x=0.6, w=12.1, size=14, level_step=0,
            line_spacing=1.15, space_after=2)
    two_col_terminal(s, 3.33, 3.57, _flatten_code(d["code_blocks"]))
    whale_and_footer(s, n, total)


def render_s05(s, n, total, d):
    """Reminder: command-line args — user-tuned: 16pt uniform bullets and a 14pt terminal
    sized to its content, dropped to y=4.0 to clear the larger bullets."""
    title(s, smart_title(d["title"].replace("\n", " ")))
    items = [(min(b["level"], 2), b["text"]) for b in d["body"]]
    bullets(s, 1.55, items, x=0.6, w=12.1, size=16, level_step=0,
            line_spacing=1.3, space_after=6)
    code = _flatten_code(d["code_blocks"])
    fs = 14
    h = 0.5 + len(code) * (fs * 1.52 / 72.0) + 0.22   # fit terminal to its lines
    auto_term(s, 0.9, 4.0, 11.5, h, "bash", code, font_size=fs)
    whale_and_footer(s, n, total)


def render_s08(s, n, total, d):
    """Injecting config with env vars — same treatment as slide 5: 16pt uniform bullets +
    a content-fit terminal (was an over-tall box with a big empty black area). Terminal
    font is auto-maximized (<=14) to fill the space left by the taller bullets."""
    title(s, smart_title(d["title"].replace("\n", " ")))
    items = [(min(b["level"], 2), b["text"]) for b in d["body"]]
    bullets(s, 1.5, items, x=0.6, w=12.1, size=16, level_step=0,
            line_spacing=1.2, space_after=4)
    code = _flatten_code(d["code_blocks"])
    cy = 3.8
    avail = 6.72 - cy
    fs = 14
    while fs > 10 and (0.5 + len(code) * (fs * 1.52 / 72.0) + 0.22) > avail:
        fs -= 1
    h = 0.5 + len(code) * (fs * 1.52 / 72.0) + 0.22
    auto_term(s, 0.9, cy, 11.5, h, "bash", code, font_size=fs)
    whale_and_footer(s, n, total)


def render_s32(s, n, total, d):
    """Understanding secret volume storage (lecture slide 18) — same treatment as slide 5:
    16pt uniform bullets + a content-fit terminal (was a single command in a huge box)."""
    title(s, smart_title(d["title"].replace("\n", " ")))
    items = [(min(b["level"], 2), b["text"]) for b in d["body"]]
    bullets(s, 1.6, items, x=0.6, w=12.1, size=16, level_step=0,
            line_spacing=1.4, space_after=10)
    code = _flatten_code(d["code_blocks"])
    fs = 14
    h = 0.5 + len(code) * (fs * 1.52 / 72.0) + 0.22   # fit to content (kills the void)
    auto_term(s, 0.9, 4.25, 11.5, h, "bash", code, font_size=fs)
    whale_and_footer(s, n, total)


def render_s23(s, n, total, d):
    """Secrets-Inject: dense slide — bullets LEFT, two full-height terminals RIGHT
    (pod+secret manifests | the three ways to inject a Secret)."""
    title(s, smart_title(d["title"].replace("\n", " ")))
    items = [(min(b["level"], 2), b["text"]) for b in d["body"]]
    bullets(s, 1.8, items, x=0.55, w=4.3, size=12.5, line_spacing=1.3, space_after=9)
    blk = d["code_blocks"]
    left = list(blk[0]["lines"]) + [""] + ["# secret-data.yaml"] + list(blk[1]["lines"])
    right = []
    for lbl, b in zip(("# inject ALL keys (envFrom)", "# inject a SINGLE key (env)",
                       "# mount as a VOLUME"), blk[2:5]):
        if right:
            right.append("")
        right.append(lbl)
        right += list(b["lines"])
    y, h = 1.72, 5.15
    fs = _fit_font(max(len(left), len(right)), h, lo=7, hi=9)
    auto_term(s, 4.95, y, 3.9, h, "pod-definition.yaml", left, font_size=fs)
    auto_term(s, 8.95, y, 3.9, h, "inject methods", right, font_size=fs)
    whale_and_footer(s, n, total)


def render_slide(s, n, total, d):
    # n is the DISPLAY position within this deck (footer). Rendering decisions that
    # depend on the original source slide (custom layouts, embedded figures) key off
    # d["n"], the source slide number — so decks can be re-split/renumbered freely.
    st = d["slide_type"]
    orig = d.get("n", n)
    body = d.get("body", [])
    code = d.get("code_blocks", [])
    ttl = smart_title(d["title"].replace("\n", " "))

    if st == "cover":
        render_cover(s, n, total, d.get("cover_role", "Lecture"))
        return

    _CUSTOM = {4: render_s04, 5: render_s05, 6: render_s06, 8: render_s08,
               9: render_s09, 10: render_s10, 12: render_s12, 23: render_s23,
               32: render_s32}
    if orig in _CUSTOM:
        _CUSTOM[orig](s, n, total, d)
        return

    if st == "course_outline":
        title(s, "Course Outline")
        items = [b["text"] for b in body]
        # Only the Exam week is highlighted (EXAM_RED). Per the user, the Week 12 tile
        # is a normal card like every other week (no current-week BLUE highlight).
        hl = {}
        for i, lab in enumerate(items):
            if "exam" in lab.lower():
                hl[i] = EXAM_RED
        course_outline(s, items, hl)
        whale_and_footer(s, n, total)
        return

    if st in ("workshop_divider", "section_divider"):
        up = ttl.upper()
        if "THE END" in up or "END" == up:
            kick = "END"
            main = ttl
            closing(s, main if len(main) < 40 else "The End")
        else:
            # split "Workshop 1: ..." into kicker + main
            if ":" in d["title"]:
                left, right = d["title"].split(":", 1)
                kick = smart_title(left.strip())
                main = smart_title(right.strip())
            else:
                kick = "SECTION"; main = ttl
            sub = None
            if body:
                sub = body[0]["text"]
            divider(s, kick if len(kick) <= 12 else "SECTION", main, subtitle=sub)
        whale_and_footer(s, n, total)
        return

    # generic content slide
    title(s, ttl)
    if orig in FIG:
        # No caption: these figures are self-contained (adding body text under them
        # duplicates labels already inside the diagram, e.g. slide 35).
        embed_fig(s, FIG[orig], 0.95, 1.68, 11.43, 4.95, caption=None)
        whale_and_footer(s, n, total)
        return
    render_content(s, body, code)
    whale_and_footer(s, n, total)


DECK = [
 {
  "n": 1,
  "title": "WEEK 10\nFEELS LIKE 100",
  "subtitle": "CONFIGMAPS AND SECRETS",
  "slide_type": "cover",
  "body": [
   {
    "text": "WEEK 10",
    "level": 0
   },
   {
    "text": "FEELS LIKE 100",
    "level": 0
   },
   {
    "text": "CONFIGMAPS AND SECRETS",
    "level": 1
   },
   {
    "text": "I found my spirit animal",
    "level": 0
   },
   {
    "text": "Glonk",
    "level": 0
   },
   {
    "text": "(Glonk)",
    "level": 1
   },
   {
    "text": "Does absolutely nothing and dies.",
    "level": 1
   }
  ],
  "code_blocks": [],
  "diagram_description": "Two-part layout. LEFT: a tall dark slate-gray rectangular panel (like a book cover) with a thin lighter gray band across its top edge. Inside the panel, lower-third, large white sans-serif title 'WEEK 10 / FEELS LIKE 100' with a smaller gray subtitle 'CONFIGMAPS AND SECRETS' below it. RIGHT: a monospace-font heading 'I found my spirit animal' in bold black across the top; below it a cartoon illustration of a fat, smiling green blob/troll creature (rounded belly, arms folded, eyes closed contentedly) standing on small feet, casting a soft shadow. Under the creature, bold black label 'Glonk', italic '(Glonk)' beneath, and a small bold caption 'Does absolutely nothing and dies.'",
  "notes": "Joke/meme slide. Palette: dark slate-gray panel, white and gray text on left; black monospace heading and green creature on white on right. The 'Week 10' title mismatches the course-outline which lists ConfigMaps & Secrets as Week 10 too, but note MEMORY says canonical schedule puts ConfigMaps at Wk12 - the deck itself says WEEK 10. Preserve wording exactly."
 },
 {
  "n": 2,
  "title": "AGENDA",
  "subtitle": "",
  "slide_type": "agenda",
  "body": [
   {
    "text": "Configuring containerized applications",
    "level": 0
   },
   {
    "text": "Passing command line options to the application",
    "level": 0
   },
   {
    "text": "Setting environment variables exposed to the app",
    "level": 0
   },
   {
    "text": "Configuring apps through ConfigMaps",
    "level": 0
   },
   {
    "text": "Passing sensitive information to apps through Secrets",
    "level": 0
   }
  ],
  "code_blocks": [],
  "diagram_description": "Left side: large black title 'AGENDA' centered vertically. Right side: a dark slate-gray rounded rectangular panel filling the right two-thirds, containing five white agenda lines stacked vertically, each separated by thin horizontal olive/khaki divider lines. Top-left of slide has a short orange horizontal accent bar; a matching dark bar sits at top of the panel.",
  "notes": "Orange accent bar top-left, dark-gray content panel on right with white text and thin olive rule lines between items. Title in dark charcoal on white."
 },
 {
  "n": 3,
  "title": "COURSE OUTLINE",
  "subtitle": "",
  "slide_type": "course_outline",
  "body": [
   {
    "text": "Week 1: Docker Introduction",
    "level": 0
   },
   {
    "text": "Week 2: Docker Image Management",
    "level": 0
   },
   {
    "text": "Week 3: Docker Networking, Storage & Security",
    "level": 0
   },
   {
    "text": "Week 4: K8s Introduction",
    "level": 0
   },
   {
    "text": "Week 5:K8s- PODs, ReplicaSets",
    "level": 0
   },
   {
    "text": "Week 6: K8s – Services & Deployments",
    "level": 0
   },
   {
    "text": "Week 7: K8s - Volumes",
    "level": 0
   },
   {
    "text": "Study Week",
    "level": 0
   },
   {
    "text": "Week 09: K8s- K8s- PVs & K8s in AKS",
    "level": 0
   },
   {
    "text": "Week 10: K8s: Storage classes & Statefulsets",
    "level": 0
   },
   {
    "text": "Week 11: Exam & Mock Exam week\nK8s- Configmaps & Secrets",
    "level": 0
   },
   {
    "text": "Week 12: K8s",
    "level": 0
   },
   {
    "text": "Week 13: K8s – RBAC and AKS",
    "level": 0
   },
   {
    "text": "Week 14: K8s – HPA\nProject presentation",
    "level": 0
   },
   {
    "text": "Week 15: Project presentation",
    "level": 0
   },
   {
    "text": "Term End",
    "level": 0
   }
  ],
  "code_blocks": [],
  "diagram_description": "A boustrophedon (snaking) flowchart of rounded rectangles connected by thick block arrows, laid out in 4 rows of 4 boxes. Row 1 (left→right): 'Week 1: Docker Introduction' (highlighted with orange/peach fill) → 'Week 2: Docker Image Management' → 'Week 3: Docker Networking, Storage & Security' → 'Week 4: K8s Introduction'. A downward arrow drops from Week 4 to Row 2. Row 2 (right→left): 'Week 5:K8s- PODs, ReplicaSets' → 'Week 6: K8s – Services & Deployments' → 'Week 7: K8s - Volumes' → 'Study Week' (larger text). Downward arrow from Study Week to Row 3. Row 3 (left→right): 'Week 8: K8s- K8s- PVs & K8s in AKS' → 'Week 9: K8s: Storage classes & Statefulsets' → 'Week 10: K8s- Configmaps & Secrets' → 'Week 11: Exam & Mock Exam week'. Downward arrow from Week 11 to Row 4. Row 4 (right→left): 'Week 12: K8s – RBAC and AKS' → 'Week 13: K8s – HPA' → 'Week 14: Helm Charts & Deployment Automation' → 'Term End'. All boxes have thin gold/tan borders and white fill (except Week 1 peach); all arrows are tan/beige block arrows. The current topic box 'Week 10: K8s- Configmaps & Secrets' is NOT highlighted (only Week 1 is highlighted).",
  "notes": "Title 'COURSE OUTLINE' overlaps a horizontal 3-segment top rule bar (dark gray | orange | light gray) which crosses through the lettering. Highlighted box is Week 1 (orange), not the current week. Preserve exact typos/spacing: 'Week 5:K8s-' (no space), 'Week 8: K8s- K8s-' (doubled), 'Statefulsets', 'Configmaps'."
 },
 {
  "n": 4,
  "title": "CONFIGURING CONTAINERIZED APPLICATIONS",
  "subtitle": "",
  "slide_type": "concept_with_diagram",
  "body": [
   {
    "text": "The application can be configured through command line arguments, environment variables or through config files",
    "level": 0
   },
   {
    "text": "Application images are immutable. Should we bake the configuration data in? (not a great idea)",
    "level": 0
   },
   {
    "text": "Ways to pass configuration data to containerized applications by:",
    "level": 0
   },
   {
    "text": "Passing command-line arguments to containers",
    "level": 1
   },
   {
    "text": "Setting custom environment variables for each container",
    "level": 1
   },
   {
    "text": "Mounting configuration files into containers through a special type of volume",
    "level": 1
   }
  ],
  "code_blocks": [
   {
    "lang": "nginx",
    "lines": [
     "user       www www;  ## Default: nobody",
     "worker_processes  5;  ## Default: 1",
     "error_log  logs/error.log;",
     "pid        logs/nginx.pid;",
     "worker_rlimit_nofile 8192;",
     "",
     "events {",
     "  worker_connections  4096;  ## Default: 1024",
     "}",
     "",
     "http {",
     "  include    conf/mime.types;",
     "  include    /etc/nginx/proxy.conf;",
     "  include    /etc/nginx/fastcgi.conf;",
     "  index    index.html index.htm index.php;",
     "",
     "  default_type application/octet-stream;",
     "  log_format   main '$remote_addr - $remote_user [$time_local]  $status '",
     "    '\"$request\" $body_bytes_sent \"$http_referer\" '",
     "    '\"$http_user_agent\" \"$http_x_forwarded_for\"';",
     "  access_log   logs/access.log  main;",
     "  sendfile     on;",
     "  tcp_nopush   on;",
     "  server_names_hash_bucket_size 128; # this seems to be required for some vhosts",
     "",
     "  server { # php/fastcgi",
     "    listen       80;",
     "    server_name  domain1.com www.domain1.com;",
     "    access_log   logs/domain1.access.log  main;",
     "    root         html;",
     "",
     "    location ~ \\.php$ {",
     "      fastcgi_pass   127.0.0.1:1025;",
     "    }"
    ]
   }
  ],
  "diagram_description": "Left two-thirds: dark slate-gray rounded panel holding the white title 'CONFIGURING CONTAINERIZED APPLICATIONS' and the white bullet list (three top-level square bullets, the third expanding into three sub-bullets). Right third (outside the panel, on white background): a small screenshot-style code card labeled 'nginx.conf' at top-left, containing a light-gray box with a full nginx configuration file rendered in tiny monospace (syntax-highlighted). This illustrates a config-file example that could be mounted into a container.",
  "notes": "Top of slide has 3-segment rule bar (dark | orange | light gray). The nginx.conf is an embedded screenshot image (classic nginx sample config from the nginx wiki), rendered very small; transcribed here as best-readable. Bullets are white square markers; sub-bullets are smaller orange/tan squares."
 },
 {
  "n": 5,
  "title": "REMINDER: PASSING COMMAND-LINE ARGUMENTS TO DOCKER CONTAINERS",
  "subtitle": "",
  "slide_type": "concept",
  "body": [
   {
    "text": "Docker reminder",
    "level": 0
   },
   {
    "text": "ENTRYPOINT defines the executable invoked when the container is started.",
    "level": 1
   },
   {
    "text": "CMD specifies the arguments that get passed to the ENTRYPOINT.",
    "level": 1
   },
   {
    "text": "We can overwrite CMD arguments by providing command line parameters in docker cli",
    "level": 1
   },
   {
    "text": "$ docker run -it docker.io/luksa/fortune:args 15",
    "level": 1
   }
  ],
  "code_blocks": [
   {
    "lang": "bash",
    "lines": [
     "$ docker run -it docker.io/luksa/fortune:args 15"
    ]
   },
   {
    "lang": "dockerfile",
    "lines": [
     "FROM ubuntu:latest",
     "RUN apt-get update ; apt-get -y install fortune",
     "ADD fortuneloop.sh /bin/fortuneloop.sh",
     "ENTRYPOINT [\"/bin/fortuneloop.sh\"]",
     "CMD [\"10\"]"
    ]
   }
  ],
  "diagram_description": "Left third: dark slate-gray rounded panel with the large white multi-line title 'REMINDER: PASSING COMMAND-LINE ARGUMENTS TO DOCKER CONTAINERS'. Right two-thirds on white: top has a bulleted 'Docker reminder' list (one parent bullet, four sub-bullets, the last being a shell command). Lower area shows a monospace Dockerfile block of 5 lines. To the right of the Dockerfile, two annotation callouts with thin leader lines/arrows pointing left: an arrow from 'ENTRYPOINT [\"/bin/fortuneloop.sh\"]' labeled 'The exec form of the ENTRYPOINT instruction', and an arrow from 'CMD [\"10\"]' labeled 'The default argument for the executable'. The '15' in the docker run command overrides the default CMD '10'.",
  "notes": "Top rule bar 3-segment (dark | orange | light gray). Annotation labels are bold black with 'ENTRYPOINT' and key phrases emphasized. Command example uses image docker.io/luksa/fortune:args (Luksa 'Kubernetes in Action' sample image)."
 },
 {
  "n": 6,
  "title": "PASSING COMMAND LINE ARGUMENTS  IN KUBERNETES",
  "subtitle": "",
  "slide_type": "concept",
  "body": [
   {
    "text": "We will usually override the CMD arguments only and not the process started in the container",
    "level": 0
   },
   {
    "text": "We will provide the process as well in generic images like busybox",
    "level": 0
   }
  ],
  "code_blocks": [
   {
    "lang": "yaml",
    "lines": [
     "kind: Pod",
     "spec:",
     "  containers:",
     "  - image: some/image",
     "    command: [\"/bin/command\"]",
     "    args: [\"arg1\", \"arg2\", \"arg3\"]"
    ]
   }
  ],
  "diagram_description": "A 2-column comparison table at the bottom with a dark slate-blue header row. Columns: Docker | Kubernetes | Description. Row 1: ENTRYPOINT | command | The executable that's executed inside the container. Row 2: CMD | args | The arguments passed to the executable.",
  "notes": "Left side has two orange square bullet points. Right side shows a monospaced YAML snippet where the lines 'command: [\"/bin/command\"]' and 'args: [\"arg1\", \"arg2\", \"arg3\"]' are bold. Orange accent bar top-left."
 },
 {
  "n": 7,
  "title": "PASSING COMMAND LINE ARGUMENTS  IN KUBERNETES",
  "subtitle": "",
  "slide_type": "concept_with_diagram",
  "body": [],
  "code_blocks": [
   {
    "lang": "docker",
    "lines": [
     "FROM ubuntu",
     "ENTRYPOINT [\"sleep\"]",
     "CMD [\"5\"]"
    ]
   },
   {
    "lang": "yaml",
    "lines": [
     "apiVersion: v1",
     "kind: Pod",
     "metadata:",
     "  name: ubuntu-sleeper-pod",
     "spec:",
     "  containers:",
     "    - name: ubuntu-sleeper",
     "      image: ubuntu-sleeper",
     "      command:[\"sleep2.0\"]",
     "      args:[\"10\"]"
    ]
   }
  ],
  "diagram_description": "Two panels connected by blue arrows illustrating how Docker's ENTRYPOINT and CMD map to Kubernetes command and args. LEFT panel (white box, purple border): a Dockerfile fragment with 'FROM ubuntu' (FROM in orange/pink, ubuntu in gray), 'ENTRYPOINT [\"sleep\"]' (ENTRYPOINT in magenta/pink), and 'CMD [\"5\"]' (CMD in magenta/pink). RIGHT panel (dark terminal titled 'pod-definition.yml'): a Pod YAML manifest with syntax highlighting (keys in orange/bold, values in white/gray). Two thick blue right-pointing arrows: one from ENTRYPOINT to the 'command:[\"sleep2.0\"]' line, one from CMD to the 'args:[\"10\"]' line. The command and args lines are rendered in large bold orange text.",
  "notes": "Dockerfile keywords ENTRYPOINT and CMD are in magenta/pink. The terminal panel has a titlebar 'pod-definition.yml'. Top has three colored bars (dark slate, orange, gray). Title is smaller/normal weight here, not the big header style."
 },
 {
  "n": 8,
  "title": "INJECTING CONFIGURATION WITH ENVIRONMENT VARIABLES",
  "subtitle": "",
  "slide_type": "concept",
  "body": [
   {
    "text": "Variables are set at the container level, not a pod level",
    "level": 0
   },
   {
    "text": "Kubernetes automatically injects environment variables corresponding to all services in the namespace",
    "level": 0
   },
   {
    "text": "Drawbacks:",
    "level": 0
   },
   {
    "text": "Environment variables defined in the Pod manifest are hard coded. It makes it difficult to maintain different values in prod and nonprod environments",
    "level": 1
   },
   {
    "text": "Configuration should not be part of the Pod description",
    "level": 0
   }
  ],
  "code_blocks": [
   {
    "lang": "yaml",
    "lines": [
     "kind: Pod",
     "spec:",
     "  containers:",
     "  - image: luksa/fortune:env",
     "    env:",
     "    - name: INTERVAL",
     "      value: \"30\"",
     "    name: html-generator"
    ]
   }
  ],
  "diagram_description": "",
  "notes": "Title is white text inside a large dark slate-blue vertical rectangle occupying the left third of the slide (this is the title-block style). Body bullets are orange squares, top-right. YAML snippet is bottom-center in monospaced font, with 'env:', '- name: INTERVAL', and 'value: \"30\"' in bold. To the right of the YAML is an annotation in bold slate-gray text: 'Adding a single variable to the environment variable list' with a vertical divider line to its left. Top has dark-slate/orange/gray bars."
 },
 {
  "n": 9,
  "title": "CONFIGMAPS",
  "subtitle": "",
  "slide_type": "concept_with_diagram",
  "body": [
   {
    "text": "ConfigMap is a resource in K8s",
    "level": 0
   },
   {
    "text": "Contains key/value pairs",
    "level": 0
   },
   {
    "text": "Configuration parameters made accessible to containers as environment variables of files in a mounted folder",
    "level": 0
   }
  ],
  "code_blocks": [],
  "diagram_description": "Diagram on the right. A large green rounded rectangle labeled 'Pod' at the bottom contains two shapes: a white cloud labeled 'Environment variables' (top), and an orange cylinder (database/volume shape) labeled 'configMap volume' (bottom). To the right of the green Pod box sits an orange rectangle labeled 'ConfigMap' containing monospaced text 'key1=value1', 'key2=value2', '...'. Two black arrows point from inside the Pod to the ConfigMap box: one from the 'Environment variables' cloud, and one from the 'configMap volume' cylinder, both curving right into the ConfigMap rectangle.",
  "notes": "Large 'CONFIGMAPS' title in normal weight, upper-left. Three orange square bullets on the left. Orange accent bar top-left. Note the typo in the third bullet: 'environment variables of files' (should be 'or files')."
 },
 {
  "n": 10,
  "title": "CONFIGMAPS - CREATE",
  "subtitle": "",
  "slide_type": "command_terminal",
  "body": [
   {
    "text": "2 Step Process",
    "level": 0
   },
   {
    "text": "Create a Config Map",
    "level": 1
   },
   {
    "text": "Imperative",
    "level": 2
   },
   {
    "text": "Declarative",
    "level": 2
   },
   {
    "text": "Inject a ConfigMap in the POD",
    "level": 1
   }
  ],
  "code_blocks": [
   {
    "lang": "bash",
    "lines": [
     "kubectl create configmap",
     "    <config-name> --from-literal=<key>=<value>"
    ]
   },
   {
    "lang": "bash",
    "lines": [
     "kubectl create configmap \\",
     "    app-config --from-literal=APP_COLOR=blue \\",
     "          --from-literal=APP_MOD=prod"
    ]
   },
   {
    "lang": "bash",
    "lines": [
     "kubectl create configmap",
     "    <config-name> --from-file=<path-to-file>"
    ]
   },
   {
    "lang": "bash",
    "lines": [
     "kubectl create configmap",
     "    app-config --from-file=app_config.properties"
    ]
   },
   {
    "lang": "bash",
    "lines": [
     "kubectl create -f"
    ]
   },
   {
    "lang": "yaml",
    "lines": [
     "apiVersion: v1",
     "kind: ConfigMap",
     "metadata:",
     "  name: app-config",
     "data:",
     "  APP_COLOR: blue",
     "  APP_MODE: prod"
    ]
   },
   {
    "lang": "bash",
    "lines": [
     "kubectl create -f config-map.yaml"
    ]
   }
  ],
  "diagram_description": "Right side is a busy composite screenshot with two horizontal bands, each headed by a 'Create ConfigMap' circular arrow icon with a blue '1' inside. TOP band (Imperative): a gray 'ConfigMap' tab-labeled dark box showing 'APP_COLOR: blue' and 'APP_MODE: prod'; a magenta/pink 'Imperative' pill; and a stack of four dark terminal command boxes (green triangle prompt) showing the --from-literal and --from-file variants. BOTTOM band (Declarative): the same gray ConfigMap box (APP_COLOR: blue / APP_MODE: prod); a green 'Declarative' pill; a terminal showing 'kubectl create -f'; a dark 'config-map.yaml' titled box containing the ConfigMap YAML manifest; and a bottom terminal 'kubectl create -f config-map.yaml'. Bottom-left of the slide has three small colored config boxes side by side: 'app-config' (dark/black, APP_COLOR: blue / APP_MODE: prod), 'mysql-config' (green, port: 3306 / max_allowed_packet: 128M), and 'redis-config' (purple/navy, port: 6379 / rdb-compression: yes).",
  "notes": "Left column: title 'CONFIGMAPS - CREATE' upper-left, then '2 Step Process' with a numbered list (1) Create a Config Map -> Imperative, Declarative; (2) Inject a ConfigMap in the POD. Note typo in imperative example: '--from-literal=APP_MOD=prod' (missing 'E', should be APP_MODE). The three colored config boxes at bottom-left illustrate multiple named ConfigMaps. Orange accent bar top-left."
 },
 {
  "n": 11,
  "title": "CONFIGMAPS - INJECT",
  "subtitle": "",
  "slide_type": "concept_with_diagram",
  "body": [
   {
    "text": "Inject into POD",
    "level": 0
   },
   {
    "text": "Can be used as just env variable, as a single env variable or file using Volume",
    "level": 0
   }
  ],
  "code_blocks": [
   {
    "lang": "yaml",
    "lines": [
     "apiVersion: v1",
     "kind: Pod",
     "metadata:",
     "  name: simple-webapp-color",
     "  labels:",
     "    name: simple-webapp-color",
     "spec:",
     "  containers:",
     "  - name: simple-webapp-color",
     "    image: simple-webapp-color",
     "    ports:",
     "      - containerPort: 8080",
     "    envFrom:",
     "      - configMapRef:",
     "          name: app-config"
    ]
   },
   {
    "lang": "yaml",
    "lines": [
     "apiVersion: v1",
     "kind: ConfigMap",
     "metadata:",
     "  name: app-config",
     "data:",
     "  APP_COLOR: blue",
     "  APP_MODE: prod"
    ]
   },
   {
    "lang": "yaml",
    "lines": [
     "envFrom:",
     "  - configMapRef:",
     "      name: app-config"
    ]
   },
   {
    "lang": "yaml",
    "lines": [
     "env:",
     "  - name: APP_COLOR",
     "    valueFrom:",
     "      configMapKeyRef:",
     "        name: app-config",
     "        key: APP_COLOR"
    ]
   },
   {
    "lang": "yaml",
    "lines": [
     "volumes:",
     "- name: app-config-volume",
     "  configMap:",
     "    name: app-config"
    ]
   }
  ],
  "diagram_description": "Right side of slide has two dark code panels at top: left labeled 'pod-definition.yaml' (grey tab header) showing the Pod YAML, with the envFrom/configMapRef block circled in a red rounded rectangle; right labeled 'config-map.yaml' (grey tab header) showing the ConfigMap YAML with 'name: app-config' highlighted by a dashed box. A red arrow points from the 'Inject into POD' bullet (bottom left) up to the red-circled envFrom block in the pod-definition panel. To the right, a green circular '2' progress ring with caption 'Inject into Pod'. Below the top panels are three stacked horizontal dark code bars, each with a colored callout tab on one side: (1) top bar shows envFrom/configMapRef/name: app-config with a magenta/pink tab on the right labeled 'ENV'; (2) middle bar has a blue tab on the LEFT labeled 'SINGLE ENV' and code on the right showing env/name: APP_COLOR/valueFrom/configMapKeyRef/name: app-config/key: APP_COLOR; (3) bottom bar shows volumes/name: app-config-volume/configMap/name: app-config with a green tab on the right labeled 'VOLUME'. Standard slide has orange horizontal accent bar top-left above the title.",
  "notes": "Three color-coded methods of injecting a ConfigMap: pink ENV (all vars via envFrom), blue SINGLE ENV (one var via configMapKeyRef), green VOLUME (mount as files). YAML in code panels is syntax-highlighted (keys in blue/tan, values in white). Red circle and red arrow emphasize the envFrom injection point."
 },
 {
  "n": 12,
  "title": "MULTI-ENVIRONMENT SUPPORT USING CONFIGMAPS",
  "subtitle": "",
  "slide_type": "concept_with_diagram",
  "body": [
   {
    "text": "Pods share the same manifest referencing configuration values from configMap",
    "level": 0
   },
   {
    "text": "ConfigMaps are created from different manifests and have environment-specific values",
    "level": 0
   }
  ],
  "code_blocks": [],
  "diagram_description": "Left column is a dark slate vertical panel containing the title at top, then two black rounded rectangles each with an icon on the left and text on the right: first has a large checkmark icon with text 'Pods share the same manifest referencing configuration values from configMap'; second has a people/group icon with text 'ConfigMaps are created from different manifests and have environment-specific values'. Right area shows two dashed-border rectangles side by side. Left dashed box labeled 'Namespace: development' contains a green stacked 'Pod(s)' box with a black arrow pointing right to an orange box labeled 'ConfigMap: app-config (contains development values)'. Right dashed box labeled 'Namespace: production' contains a green stacked 'Pod(s)' box with a black arrow pointing right to an orange box labeled 'ConfigMap: app-config (contains production values)'. A bold label at top 'ConfigMaps created from different manifests' has two curved arrows pointing down into each ConfigMap (orange) box. A bold label at bottom 'Pods created from the same pod manifests' has two curved arrows pointing up into each Pod(s) (green) box.",
  "notes": "Illustrates identical Pod manifests deployed across development and production namespaces, each referencing an app-config ConfigMap that holds environment-specific values. Green = Pods, orange = ConfigMaps, dashed boxes = namespaces. Top accent bars: orange and grey segments across the top of the content area."
 },
 {
  "n": 13,
  "title": "WORKSHOP 1: CONFIGURE APPLICATIONS WITH ENVIRONMENT VARIABLES AND CONFIGMAPS",
  "subtitle": "",
  "slide_type": "workshop_divider",
  "body": [],
  "code_blocks": [],
  "diagram_description": "",
  "notes": "Section/workshop divider slide. Large dark grey title text on white background. Decorative bars: top-left orange bar and top-right grey bar; bottom-center dark slate bar. No body content."
 },
 {
  "n": 14,
  "title": "CONFIGURE INTERVAL IN FORTUNE TELLING APPLICATION USING ENVIRONMENT VARIABLES VALUE IN THE POD MANIFEST",
  "subtitle": "",
  "slide_type": "workshop_step",
  "body": [
   {
    "text": "# Deploy fortune application, configure the interval with environment variables populated from the Pod manifest",
    "level": 0
   },
   {
    "text": "$ k create ns week10",
    "level": 0
   },
   {
    "text": "$ k create –f fortune-pod-env.yaml -n week10",
    "level": 0
   },
   {
    "text": "$ k describe pod fortune-env –n week10",
    "level": 0
   },
   {
    "text": "# Is the interval value reflected in the log?",
    "level": 0
   },
   {
    "text": "$ k logs fortune-env -c html-generator -n week10",
    "level": 0
   }
  ],
  "code_blocks": [
   {
    "lang": "bash",
    "lines": [
     "# Deploy fortune application, configure the interval with environment variables populated from the Pod manifest",
     "$ k create ns week10",
     "$ k create –f fortune-pod-env.yaml -n week10",
     "$ k describe pod fortune-env –n week10",
     "# Is the interval value reflected in the log?",
     "$ k logs fortune-env -c html-generator -n week10"
    ]
   },
   {
    "lang": "text",
    "lines": [
     "Namespace:      week10",
     "Priority:       0",
     "Node:           ip-192-168-82-156.ec2.internal/192.168.82.156",
     "Start Time:     Mon, 11 Jul 2022 17:58:45 +0000",
     "Labels:         <none>",
     "Annotations:    kubernetes.io/psp: eks.privileged",
     "Status:         Running",
     "IP:             192.168.67.125",
     "IPs:",
     "  IP:   192.168.67.125",
     "Containers:",
     "  html-generator:",
     "    Container ID:   docker://cce73c2148e7705d26119452fd6624...",
     "    Image:          luksa/fortune:env",
     "    Image ID:       docker-pullable://luksa/fortune@sha256:...",
     "    Port:           <none>",
     "    Host Port:      <none>",
     "    State:          Running",
     "      Started:      Mon, 11 Jul 2022 17:58:50 +0000",
     "    Ready:          True",
     "    Restart Count:  0",
     "    Environment:",
     "      INTERVAL:  30"
    ]
   }
  ],
  "diagram_description": "Right half of the slide is a screenshot of a black terminal showing the output of 'kubectl describe pod'. It lists pod fields (Namespace, Priority, Node, Start Time, Labels, Annotations, Status, IP, IPs, Containers > html-generator with Container ID, Image luksa/fortune:env, Image ID, Port, Host Port, State Running, Started, Ready True, Restart Count 0). At the bottom the 'Environment:' section shows 'INTERVAL: 30' enclosed in a thick orange rectangle highlight. Text is white/green monospace on black. Some lines are truncated at the right edge (Container ID and Image ID cut off).",
  "notes": "Left column bullets are the command steps; right column is the terminal screenshot proving the INTERVAL env var (=30) was injected from the Pod manifest. Orange accent bar top-left above the left-column title. The orange box highlights 'INTERVAL: 30' as the key result. Note the source uses en-dashes '–f' and '–n' in some commands (likely autocorrect artifacts, preserved)."
 },
 {
  "n": 15,
  "title": "CONFIGURE INTERVAL IN FORTUNE TELLING APPLICATION USING ENVIRONMENT VARIABLES VALUE FROM THE CONFIGMAP",
  "subtitle": "",
  "slide_type": "workshop_step",
  "body": [
   {
    "text": "# Create configMap from the manifest",
    "level": 0
   },
   {
    "text": "$ k create -f fortune-config.yaml -n week10",
    "level": 0
   },
   {
    "text": "# use fortune-pod-env-configmap.yaml to deploy the application",
    "level": 0
   },
   {
    "text": "$ k create –f fortune-pod-env-configmap.yaml -n week10",
    "level": 0
   },
   {
    "text": "$ k describe pod fortune-env-from-configmap   -n week10",
    "level": 0
   },
   {
    "text": "# Is the interval value reflected in the log?",
    "level": 0
   },
   {
    "text": "$ k logs fortune-env-from-configmap -c html-generator -n week10",
    "level": 0
   },
   {
    "text": "# Log into container and verify the environment variable was set",
    "level": 0
   },
   {
    "text": "$ k exec -it fortune-env-from-configmap -n week10 -c html-generator -- /bin/bash",
    "level": 0
   },
   {
    "text": "# printenv | grep -i interval",
    "level": 0
   }
  ],
  "code_blocks": [
   {
    "lang": "bash",
    "lines": [
     "# Create configMap from the manifest",
     "$ k create -f fortune-config.yaml -n week10",
     "# use fortune-pod-env-configmap.yaml to deploy the application",
     "$ k create –f fortune-pod-env-configmap.yaml -n week10",
     "$ k describe pod fortune-env-from-configmap   -n week10",
     "# Is the interval value reflected in the log?",
     "$ k logs fortune-env-from-configmap -c html-generator -n week10",
     "# Log into container and verify the environment variable was set",
     "$ k exec -it fortune-env-from-configmap -n week10 -c html-generator -- /bin/bash",
     "# printenv | grep -i interval"
    ]
   },
   {
    "lang": "text",
    "lines": [
     "Containers:",
     "  html-generator:",
     "    Container ID:   docker://12eac7a1572eb1593e14f7521e9b91583130b79c8f37e6d3f558f52617c159d9",
     "    Image:          luksa/fortune:env",
     "    Image ID:       docker-pullable://luksa/fortune@sha256:8af10b8eb1b1dcc6512e0061c0722db43f4795ae...",
     "    Port:           <none>",
     "    Host Port:      <none>",
     "    State:          Running",
     "      Started:      Mon, 11 Jul 2022 18:33:03 +0000",
     "    Ready:          True",
     "    Restart Count:  0",
     "    Environment:",
     "      INTERVAL:  <set to the key 'sleep-interval' of config map 'fortune-config'>  Optional: false",
     "    Mounts:"
    ]
   }
  ],
  "diagram_description": "Bottom-right of the slide is a screenshot of a black terminal showing 'kubectl describe pod' output for the html-generator container: Container ID (full docker hash), Image luksa/fortune:env, Image ID (docker-pullable sha256), Port <none>, Host Port <none>, State Running, Started Mon 11 Jul 2022 18:33:03 +0000, Ready True, Restart Count 0, Environment: INTERVAL: <set to the key 'sleep-interval' of config map 'fortune-config'> Optional: false, then 'Mounts:' beginning at the bottom cut off. White/green monospace text on black.",
  "notes": "Left column is a full-height dark slate panel with the long title in white. Right column top is the command list; bottom is the terminal screenshot. Key difference from slide 14: here INTERVAL is sourced from a ConfigMap key ('sleep-interval' of config map 'fortune-config') rather than a literal value. Top accent bars: dark, orange, and grey segments. Note en-dash '–f' preserved in the 'k create –f fortune-pod-env-configmap.yaml' command; the describe command has a double space before '-n week10' (preserved)."
 },
 {
  "n": 16,
  "title": "WHAT IF APPLICATION IS ACCEPTING CONFIGURATION THROUGH COMMAND LINE ARGUMENTS ONLY?",
  "subtitle": "",
  "slide_type": "yaml_manifest",
  "body": [
   {
    "text": "# Provide arguments that act is CMD in DOCKERFILE. The value is hard coded in the pod manifest",
    "level": 0
   },
   {
    "text": "k apply -f fortune-pod-args.yaml -n week10",
    "level": 0
   },
   {
    "text": "# Use configMap to provide the value in agrs and decouple pod manifest from the configuration data",
    "level": 0
   }
  ],
  "code_blocks": [
   {
    "lang": "yaml",
    "lines": [
     "kind: Pod",
     "metadata:",
     "  name: fortune-args-from-configmap",
     "spec:",
     "  containers:",
     "  - image: luksa/fortune:args",
     "    env:",
     "    - name: INTERVAL",
     "      valueFrom:",
     "        configMapKeyRef:",
     "          name: fortune-config",
     "          key: sleep-interval",
     "    args: [\"$(INTERVAL)\"]"
    ]
   }
  ],
  "diagram_description": "",
  "notes": "Left side: dark terminal-style code box with syntax highlighting (keys in red/pink, values in white, $(INTERVAL) in teal) framed by a dark bordered rounded rectangle on a white card. Right side: three orange square bullets of prose. Intentional typos in bullets ('act is CMD', 'agrs'). Standard house header with three horizontal bars (dark slate, orange, gray)."
 },
 {
  "n": 17,
  "title": "DIFFERENT WAYS TO CREATE CONFIGMAPS",
  "subtitle": "",
  "slide_type": "command_terminal",
  "body": [
   {
    "text": "# From all the files in the folder",
    "level": 0
   },
   {
    "text": "$ kubectl create configmap my-config --from-file=/path/to/dir",
    "level": 0
   },
   {
    "text": "# From literal values provided in command line",
    "level": 0
   },
   {
    "text": "$ kubectl create configmap fortune-config --from-literal=sleep-interval=25 --from-literal=sky-color=blue",
    "level": 0
   }
  ],
  "code_blocks": [
   {
    "lang": "bash",
    "lines": [
     "# From all the files in the folder",
     "$ kubectl create configmap my-config --from-file=/path/to/dir",
     "# From literal values provided in command line",
     "$ kubectl create configmap fortune-config --from-literal=sleep-interval=25 --from-literal=sky-color=blue"
    ]
   }
  ],
  "diagram_description": "",
  "notes": "Text-only slide. Four orange square bullets; comment lines (#) alternate with command lines ($). Note double space in title 'WAYS  TO'. Content sits in the vertical middle-left of the slide."
 },
 {
  "n": 18,
  "title": "USING A CONFIGMAP VOLUME TO EXPOSE CONFIGMAP ENTRIES AS FILES",
  "subtitle": "",
  "slide_type": "command_terminal",
  "body": [
   {
    "text": "# Delete the previous configMap",
    "level": 0
   },
   {
    "text": "$ k delete configmap fortune-config –n week10",
    "level": 0
   },
   {
    "text": "# Create a new configMap from the files in the configmap-files folder. Each file becomes a key entry in the configMap",
    "level": 0
   },
   {
    "text": "$ kubectl create configmap fortune-config --from-file=configmap-files -n week10",
    "level": 0
   },
   {
    "text": "# Examine the data in the configMap",
    "level": 0
   },
   {
    "text": "$ k get configmap/fortune-config  -n week10 -o yaml",
    "level": 0
   },
   {
    "text": "# The nginx configuration will get loaded from the configMap",
    "level": 0
   },
   {
    "text": "$ k apply -f fortune-pod-configmap-volume.yaml -n week10",
    "level": 0
   }
  ],
  "code_blocks": [
   {
    "lang": "bash",
    "lines": [
     "# Delete the previous configMap",
     "$ k delete configmap fortune-config –n week10",
     "# Create a new configMap from the files in the configmap-files folder. Each file becomes a key entry in the configMap",
     "$ kubectl create configmap fortune-config --from-file=configmap-files -n week10",
     "# Examine the data in the configMap",
     "$ k get configmap/fortune-config  -n week10 -o yaml",
     "# The nginx configuration will get loaded from the configMap",
     "$ k apply -f fortune-pod-configmap-volume.yaml -n week10"
    ]
   },
   {
    "lang": "yaml",
    "lines": [
     "irimag:~/environment/week10 $ k get configmap/fortune-config  -n week10 -o yaml",
     "apiVersion: v1",
     "data:",
     "  my-nginx-config.conf: |-",
     "    server {",
     "        listen 80;",
     "        server_name www.kubia-example.com;",
     "        gzip on;",
     "        gzip_types text/plain application/xml;",
     "        location / {",
     "            root /usr/share/nginx/html;",
     "            index index.html index.htm;",
     "        }",
     "    }",
     "  sleep-interval: \"22\"",
     "kind: ConfigMap"
    ]
   }
  ],
  "diagram_description": "Left side: a dark terminal screenshot (white/green monospace text on black) showing the output of 'k get configmap/fortune-config -n week10 -o yaml'. The prompt 'irimag:~/environment/week10' is in green. It displays the ConfigMap YAML: apiVersion v1, a data section containing 'my-nginx-config.conf' with a full nginx server block (listen 80, server_name www.kubia-example.com, gzip on, gzip_types text/plain application/xml, location / with root /usr/share/nginx/html and index directives), plus 'sleep-interval: \"22\"', and 'kind: ConfigMap'. The terminal image is inside a dark bordered rounded rectangle on a white card, occupying the left half.",
  "notes": "The terminal screenshot content is captured as the second (yaml) code block. Right side: eight orange square bullets alternating comment/command. Header title spans two lines. Double space in 'VOLUME  TO'. Note the en-dash character in the delete command."
 },
 {
  "n": 19,
  "title": "USING A CONFIGMAP VOLUME TO EXPOSE CONFIGMAP ENTRIES AS FILES, CONT",
  "subtitle": "",
  "slide_type": "command_terminal",
  "body": [
   {
    "text": "# Verifying the settings of nginx",
    "level": 0
   },
   {
    "text": "$ k port-forward fortune-configmap-volume 8080:80 -n week10",
    "level": 0
   },
   {
    "text": "$ kubectl exec fortune-configmap-volume -c web-server ls /etc/nginx/conf.d",
    "level": 0
   },
   {
    "text": "$ curl -H \"Accept-Encoding: gzip\" -I localhost:8080",
    "level": 0
   },
   {
    "text": "# Examine the content of the mounted /etc/nginx/conf.d directory :",
    "level": 0
   },
   {
    "text": "$ kubectl exec fortune-configmap-volume -c web-server  -n week10 -- ls /etc/nginx/conf.d",
    "level": 0
   }
  ],
  "code_blocks": [
   {
    "lang": "bash",
    "lines": [
     "# Verifying the settings of nginx",
     "$ k port-forward fortune-configmap-volume 8080:80 -n week10",
     "$ kubectl exec fortune-configmap-volume -c web-server ls /etc/nginx/conf.d",
     "$ curl -H \"Accept-Encoding: gzip\" -I localhost:8080",
     "# Examine the content of the mounted /etc/nginx/conf.d directory :",
     "$ kubectl exec fortune-configmap-volume -c web-server  -n week10 -- ls /etc/nginx/conf.d"
    ]
   },
   {
    "lang": "bash",
    "lines": [
     "irimag:~/environment $ curl -H \"Accept-Encoding: gzip\" -I localhost:8080",
     "HTTP/1.1 200 OK",
     "Server: nginx/1.23.0",
     "Date: Mon, 11 Jul 2022 23:09:34 GMT",
     "Content-Type: text/html",
     "Last-Modified: Mon, 11 Jul 2022 23:09:14 GMT",
     "Connection: keep-alive",
     "ETag: W/\"62ccad9a-4a\"",
     "Content-Encoding: gzip"
    ]
   }
  ],
  "diagram_description": "Right side: a dark terminal screenshot (black background, colored/white monospace text) showing the result of the curl command. The prompt line 'irimag:~/environment $ curl -H \"Accept-Encoding: gzip\" -I localhost:8080' is followed by HTTP response headers: HTTP/1.1 200 OK, Server: nginx/1.23.0, Date: Mon, 11 Jul 2022 23:09:34 GMT, Content-Type: text/html, Last-Modified: Mon, 11 Jul 2022 23:09:14 GMT, Connection: keep-alive, ETag: W/\"62ccad9a-4a\", Content-Encoding: gzip. Header labels appear bold/highlighted. The screenshot sits in a dark bordered rounded rectangle on a white card occupying the right half (upper portion), with empty white space below.",
  "notes": "Left side: six orange square bullets alternating comment and command lines. The terminal screenshot on the right is the output of the curl command shown in the third-from-top bullet. Title wraps to two lines ending with ', CONT'."
 },
 {
  "n": 20,
  "title": "WORKSHOP 1:  THE END",
  "subtitle": "",
  "slide_type": "section_divider",
  "body": [],
  "code_blocks": [],
  "diagram_description": "",
  "notes": "Section divider layout. Title 'WORKSHOP 1:  THE END' (note double space after colon) in dark gray, left-aligned, centered vertically. Top of slide has two horizontal bars: a wide orange bar on the left and a shorter gray bar on the right. A single wide dark slate bar spans across the lower portion of the slide. No body text."
 },
 {
  "n": 21,
  "title": "STORING SENSITIVE DATA IN K8S: INTRODUCING SECRETS",
  "subtitle": "",
  "slide_type": "concept_with_diagram",
  "body": [
   {
    "text": "Key value pairs that are stored as base64 encoded strings",
    "level": 0
   },
   {
    "text": "Like configMaps, available to containers as environment variables or mounted files",
    "level": 0
   },
   {
    "text": "Never stored on the disk of the underlying host",
    "level": 0
   },
   {
    "text": "Stored in etcd and are encrypted",
    "level": 0
   },
   {
    "text": "Size is limited to 1MB",
    "level": 0
   },
   {
    "text": "Available to application in its original form, application does not need to decode it",
    "level": 0
   }
  ],
  "code_blocks": [],
  "diagram_description": "Six circular icon badges arranged in a 3-column, 2-row grid, each with descriptive text to its right. Row 1: (1) sandy-yellow circle with a black key icon -> 'Key value pairs that are stored as base64 encoded strings'; (2) slate-blue circle with a black square icon -> 'Like configMaps, available to containers as environment variables or mounted files'; (3) gray circle with a black floppy-disk/save icon -> 'Never stored on the disk of the underlying host'. Row 2: (4) olive-green circle with a black padlock icon -> 'Stored in etcd and are encrypted'; (5) teal/green circle with a black square icon -> 'Size is limited to 1MB'; (6) sandy-yellow circle with a black square icon -> 'Available to application in its original form, application does not need to decode it'.",
  "notes": "Dark charcoal background slide with white text. Top edge has three horizontal accent bars: dark slate (left), orange (center), gray (right). Title in large white all-caps. Several icons render as plain black squares (missing/broken glyphs) rather than meaningful icons."
 },
 {
  "n": 22,
  "title": "SECRETS- CREATE",
  "subtitle": "",
  "slide_type": "concept_with_diagram",
  "body": [
   {
    "text": "2 Step Process",
    "level": 0
   },
   {
    "text": "Create a Secret",
    "level": 1
   },
   {
    "text": "Imperative",
    "level": 2
   },
   {
    "text": "Declarative",
    "level": 2
   },
   {
    "text": "Base64 format encoding. Need to provide encoded data",
    "level": 3
   },
   {
    "text": "Inject a Secret in the POD",
    "level": 1
   },
   {
    "text": "Need to encode data in secrets file.",
    "level": 0
   }
  ],
  "code_blocks": [
   {
    "lang": "bash",
    "lines": [
     "kubectl create secret generic",
     "    <secret-name> --from-literal=<key>=<value>"
    ]
   },
   {
    "lang": "bash",
    "lines": [
     "kubectl create secret generic \\",
     "    app-secret --from-literal=DB_Host=mysql      \\",
     "               --from-literal=DB_User=root",
     "               --from-literal=DB_Password=paswrd"
    ]
   },
   {
    "lang": "bash",
    "lines": [
     "kubectl create secret generic",
     "    <secret-name> --from-file=<path-to-file>"
    ]
   },
   {
    "lang": "bash",
    "lines": [
     "kubectl create secret generic \\",
     "    app-secret --from-file=app_secret.properties"
    ]
   },
   {
    "lang": "bash",
    "lines": [
     "kubectl create -f"
    ]
   },
   {
    "lang": "yaml",
    "lines": [
     "apiVersion: v1",
     "kind: Secret",
     "metadata:",
     "    name: app-secret",
     "data:",
     "    DB_Host: bXlzcWw=",
     "    DB_User: cm9vdA==",
     "    DB_Password: cGFzd3Jk"
    ]
   },
   {
    "lang": "bash",
    "lines": [
     "kubectl create -f secret-data.yaml"
    ]
   }
  ],
  "diagram_description": "Right two-thirds of slide is a screenshot with two horizontal bands. Top band (labeled Imperative, magenta tag): a dark 'Secret' box showing 'DB_Host: mysql / DB_User: root / DB_Password: paswrd', beside it four dark terminal command boxes each prefixed with a play-triangle (blue for template, green for filled example). A blue circular badge with '1' and caption 'Create Secret' sits lower-left of this band. Bottom band (labeled Declarative, green tag): another 'Secret' box with the same DB_Host/DB_User/DB_Password values, a 'kubectl create -f' terminal, and a 'secret-data.yaml' terminal box containing the Secret YAML manifest; a 'kubectl create -f secret-data.yaml' command at the bottom. Another blue '1 / Create Secret' badge at lower-left.",
  "notes": "White-background content slide. Left column has an orange accent bar at top and a bulleted outline with an orange-numbered ordered list (1, 2) nested under it. Base64 encoded values in the YAML: DB_Host: bXlzcWw= (mysql), DB_User: cm9vdA== (root), DB_Password shown as cGFzZz3Jk in screenshot. Text/code in the screenshot is low-resolution."
 },
 {
  "n": 23,
  "title": "SECRETS- INJECT",
  "subtitle": "",
  "slide_type": "concept_with_diagram",
  "body": [
   {
    "text": "Inject into POD",
    "level": 0
   },
   {
    "text": "Secrets are not encrypted only encoded",
    "level": 0
   },
   {
    "text": "Do not check-in  secret objects to SCM",
    "level": 0
   },
   {
    "text": "Secrets in ETCD are not encrypted. Need to enable encryption at rest",
    "level": 0
   },
   {
    "text": "Anyone able to create pods/deployments in the same namespace has access to secrets.",
    "level": 0
   },
   {
    "text": "Consider 3rd party secret store providers",
    "level": 0
   },
   {
    "text": "AWS, Azure etc.",
    "level": 1
   }
  ],
  "code_blocks": [
   {
    "lang": "yaml",
    "lines": [
     "apiVersion: v1",
     "kind: Pod",
     "metadata:",
     "  name: simple-webapp-color",
     "  labels:",
     "    name: simple-webapp-color",
     "spec:",
     "  containers:",
     "  - name: simple-webapp-color",
     "    image: simple-webapp-color",
     "    ports:",
     "      - containerPort: 8080",
     "    envFrom:",
     "      - secretRef:",
     "          name: app-secret"
    ]
   },
   {
    "lang": "yaml",
    "lines": [
     "apiVersion: v1",
     "kind: Secret",
     "metadata:",
     "  name: app-secret",
     "data:",
     "  DB_Host: bXlzcWw=",
     "  DB_User: cm9vdA==",
     "  DB_Password: cGFzd3Jk"
    ]
   },
   {
    "lang": "yaml",
    "lines": [
     "envFrom:",
     "  - secretRef:",
     "      name: app-config"
    ]
   },
   {
    "lang": "yaml",
    "lines": [
     "env:",
     "  - name: DB_Password",
     "    valueFrom:",
     "      secretKeyRef:",
     "        name: app-secret",
     "        key: DB_Password"
    ]
   },
   {
    "lang": "yaml",
    "lines": [
     "volumes:",
     "- name: app-secret-volume",
     "  secret:",
     "    secretName: app-secret"
    ]
   }
  ],
  "diagram_description": "Right two-thirds is a screenshot. Top area: two side-by-side dark terminal boxes - left 'pod-definition.yaml' (the Pod manifest) with the envFrom/secretRef block circled in red; right 'secret-data.yaml' (the Secret manifest with base64 data). A red arrow points from the 'Inject into POD' bullet on the left to the circled envFrom block. A green circular badge '2 / Inject into Pod' sits at right below the boxes. Bottom area: three stacked dark YAML snippet cards, each with a colored angled tab on the right: magenta tab 'ENV' (envFrom/secretRef name: app-config), blue tab 'SINGLE ENV' on left (env/valueFrom/secretKeyRef for DB_Password), green tab 'VOLUME' (volumes/secret/secretName: app-secret). These illustrate three ways to inject a Secret: all env vars, a single env var, or as a volume.",
  "notes": "White-background slide, orange accent bar top-left over the bulleted list. Red highlight circle and red connector arrow emphasize the envFrom injection. Screenshot text is orange/gray monospace."
 },
 {
  "n": 24,
  "title": "DEFAULT SECRETS",
  "subtitle": "",
  "slide_type": "concept_with_diagram",
  "body": [
   {
    "text": "Default secrets are mounted into every container we run unless specified otherwise",
    "level": 0
   },
   {
    "text": "Default secrets are mounted as files into \"/var/run/secrets/kubernetes.io/serviceaccount\" folder in the container",
    "level": 0
   },
   {
    "text": "The folder has 3 entiries.",
    "level": 0
   },
   {
    "text": "ca.crt",
    "level": 1
   },
   {
    "text": "namespace",
    "level": 1
   },
   {
    "text": "token",
    "level": 1
   },
   {
    "text": "Default secrets allow containers to communicate with K8s API using read-only permissions",
    "level": 0
   }
  ],
  "code_blocks": [
   {
    "lang": "bash",
    "lines": [
     "/environment $ k get secrets -n kube-system",
     "                                     TYPE",
     "tach-controller-token-mfkmj          kubernetes.io/s",
     "d-provider-token-mgxds               kubernetes.io/s",
     "-token-xnxl8                         kubernetes.io/s",
     "ate-controller-token-7svx5           kubernetes.io/s",
     "le-aggregation-controller-token-tj29p kubernetes.io/s",
     "token-cpqph                          kubernetes.io/s",
     "controller-token-24wlk               kubernetes.io/s",
     "et-controller-token-mqb7f            kubernetes.io/s",
     "token-xzltz                          kubernetes.io/s",
     "nt-controller-token-jdn4q            kubernetes.io/s",
     "on-controller-token-s6j4t            kubernetes.io/s",
     "resource-controller-token-9fjcj      kubernetes.io/s",
     "-controller-token-66v5c              kubernetes.io/s",
     "slice-controller-token-pnth5         kubernetes.io/s",
     "slicemirroring-controller-token-bf76l kubernetes.io/s",
     "ontroller-token-q66tg                kubernetes.io/s"
    ]
   }
  ],
  "diagram_description": "Left side is a black terminal screenshot (with a dark border/drop shadow) showing the output of 'k get secrets -n kube-system'. The command line 'k get secrets -n kube-system' is highlighted in cyan/teal. Below is a two-column listing: left column shows service-account token secret names (left-truncated at the frame edge, e.g. tach-controller-token-mfkmj, d-provider-token-mgxds, -token-xnxl8, ...), right column shows the TYPE 'kubernetes.io/s...' (right-truncated). Right side is the bulleted text list.",
  "notes": "White-background content slide with three accent bars at top (dark slate, orange center, gray right). Title in dark gray all-caps. Terminal names are cut off at both the left and right edges of the screenshot frame. Note typo 'entiries' in the body (preserved)."
 },
 {
  "n": 25,
  "title": "THE DEFAULT-TOKEN SECRET IS CREATED AUTOMATICALLY AND A CORRESPONDING VOLUME IS MOUNTED IN EACH POD AUTOMATICALLY.",
  "subtitle": "",
  "slide_type": "concept_with_diagram",
  "body": [],
  "code_blocks": [],
  "diagram_description": "Nested-box architecture diagram, left-to-right flow. Outer rounded green box labeled 'Pod' at bottom. Inside it a blue rounded box labeled 'Container'. Inside that a light-gray box labeled 'Filesystem' showing an ASCII directory tree: '/' -> 'var/' -> 'run/' -> 'secrets/' -> 'kubernetes.io/' -> 'serviceaccount/' (indented tree with L-shaped connectors). A black arrow runs from 'serviceaccount/' rightward to a purple/lavender cylinder (database/volume shape) labeled 'Default token secret volume'. A second black arrow runs from the cylinder rightward to a purple-header table titled 'Default token Secret' with three rows, two columns each: 'ca.crt | ...', 'namespace | ...', 'token | ...' (left cells in monospace font).",
  "notes": "White-background slide, three accent bars at top (dark slate, orange center, gray right). Title is a full-sentence all-caps heading wrapping across two/three lines. Color scheme: green Pod box, blue Container box, gray Filesystem box, lavender/purple cylinder and table. No bullet body text - the diagram is the entire content."
 },
 {
  "n": 26,
  "title": "WORKSHOP 2: WORKING WITH K8S SECRETS",
  "subtitle": "",
  "slide_type": "workshop_divider",
  "body": [],
  "code_blocks": [],
  "diagram_description": "",
  "notes": "Section-divider slide on white background. Left third is a dark slate-gray vertical panel (with a thin lighter bar across its top) containing the white all-caps title 'WORKSHOP 2: WORKING WITH K8S SECRETS'. Right side features a large 3D cartoon illustration of an orange kitten/fox character with big purple eyes and a white adhesive bandage (X-shaped) taped over its mouth, and a purple collar - implying 'keeping a secret / staying quiet'. Playful tone."
 },
 {
  "n": 27,
  "title": "GOALS",
  "subtitle": "",
  "slide_type": "agenda",
  "body": [
   {
    "text": "Learn how to create the secrets",
    "level": 0
   },
   {
    "text": "Compare Secrets and ConfigMaps in K8s",
    "level": 0
   },
   {
    "text": "Learn how to use K8s secrets in the application",
    "level": 0
   }
  ],
  "code_blocks": [],
  "diagram_description": "Three horizontally-arranged goal items. Each item has a circular light-peach/pink icon badge on the left with a blue icon inside, and text to the right. Left badge: a head/brain profile silhouette with gear cogs (representing 'learn/think'). Middle badge: a blue checkmark. Right badge: a blue padlock. Icons sit on a row roughly centered vertically. Above the title are three horizontal accent bars (dark slate, orange, gray) spanning the top of the slide.",
  "notes": "Standard house 'GOALS' agenda layout. Title 'GOALS' in large gray uppercase, upper-left. Three decorative top rule bars (dark slate, orange, light gray). Peach circular icon backgrounds with blue glyphs."
 },
 {
  "n": 28,
  "title": "EXPLORING DEFAULT SECRETS",
  "subtitle": "",
  "slide_type": "command_terminal",
  "body": [],
  "code_blocks": [
   {
    "lang": "bash",
    "lines": [
     "$ k create ns week10",
     "$ k get secrets -n week10 -o yaml",
     "$ k describe  secrets -n week10",
     "# Create mypod pod in the week10 namespace using nginx image",
     "$ k run mypod --image nginx  -n week10",
     "$ k describe pod mypod –n week10",
     "# Explore the secrets mounted",
     "# at  /var/run/secrets/kubernetes.io/serviceaccount/",
     "$ k exec mypod -n week10 -- ls /var/run/secrets/kubernetes.io/serviceaccount/",
     "$ kubectl exec mypod -n week10 -- cat /var/run/secrets/kubernetes.io/serviceaccount/namespace",
     "$ kubectl exec mypod -n week10 -- cat /var/run/secrets/kubernetes.io/serviceaccount/token",
     "$ kubectl exec mypod -n week10 -- cat /var/run/secrets/kubernetes.io/serviceaccount/ca.crt"
    ]
   }
  ],
  "diagram_description": "",
  "notes": "Left-side layout: title 'EXPLORING DEFAULT SECRETS' in white uppercase on a large dark-slate rectangular panel occupying the left third/quarter of the slide. Commands are bulleted (small orange square bullets) on the right. Two lines are wrapped comment+continuation: '# Explore the secrets mounted' with '# at  /var/run/secrets/kubernetes.io/serviceaccount/' on the next line within the same bullet. Note the mix of 'k' and 'kubectl' aliases, and the en-dash '–n' typo in 'k describe pod mypod –n week10'. Top accent bars: dark slate, orange, gray."
 },
 {
  "n": 29,
  "title": "WORKING WITH SECRETS – CREATE A SECRET, COMPARE K8S SERCRETS AND CONFIGMAPS",
  "subtitle": "",
  "slide_type": "command_terminal",
  "body": [],
  "code_blocks": [
   {
    "lang": "bash",
    "lines": [
     "# Create the private key and the certificate",
     "$ openssl genrsa -out https.key 2048",
     "$ openssl req -new -x509 -key https.key -out https.cert -days 3650 -subj /CN=www.kubia-example.com",
     "# Create a secret with the key and the certificate",
     "$ k create secret generic fortune-https --from-file=https.key --from-file=https.cert -n week10",
     "# Comparing Secrets and ConfigMaps",
     "$ k create -f configMaps/fortune-config.yaml -n week10",
     "$ k get secret fortune-https -o yaml –n week10",
     "$ k get configmap fortune-config  -n week10 -o yaml"
    ]
   }
  ],
  "diagram_description": "",
  "notes": "Full-width title spanning two lines in gray uppercase at top. NOTE the intentional typo 'SERCRETS' in the title. Bulleted command list (small orange square bullets) fills the body. Note '–n week10' uses an en-dash in the 'k get secret' line, and double space before 'k get configmap'. Top accent bars: dark slate, orange, gray."
 },
 {
  "n": 30,
  "title": "MODIFYING G CONFIGMAP  TO WORK WITH CERTIFICATES",
  "subtitle": "",
  "slide_type": "concept_with_diagram",
  "body": [
   {
    "text": "# Create fortune-config from the files in configmap-files folder",
    "level": 0
   },
   {
    "text": "$ k create configmap fortune-config  --from-file=week10/secrets/configmap-files/ -n week10",
    "level": 0
   },
   {
    "text": "# This nginx config configures the server to read the certificate and key files from /etc/nginx/certs",
    "level": 0
   }
  ],
  "code_blocks": [
   {
    "lang": "yaml",
    "lines": [
     "data:",
     "my-nginx-config.conf: |",
     "    server {",
     "        listen 80;",
     "        listen 443 ssl;",
     "        server_name www.kubia-example.com;",
     "        ssl_certificate certs/https.cert;",
     "        ssl_certificate_key certs/https.key;",
     "        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;",
     "        ssl_ciphers HIGH:!aNULL:!MD5;",
     "        location / {",
     "            root /usr/share/nginx/html;",
     "            index index.html index.htm;",
     "        }",
     "}"
    ]
   }
  ],
  "diagram_description": "Left side: a dark terminal/code panel (black background, light monospace text) showing the ConfigMap 'data:' block with the embedded nginx config (my-nginx-config.conf). The panel is bordered by a thin dark rounded rectangle. Right side: three bulleted lines (orange square bullets) describing the create-configmap command and its purpose. The code panel shows a text cursor '|' after 'server_name www.kubia-example.com;'.",
  "notes": "Title has an odd stray 'G': 'MODIFYING G CONFIGMAP  TO WORK WITH CERTIFICATES' (intentional typo preserved). The YAML is rendered as an image (dark editor screenshot), not live text – rebuild as a code block. Note the closing '}' at column 0 (nginx block close) after the server block. Top accent bars: dark slate, orange, gray."
 },
 {
  "n": 31,
  "title": "DEPLOY  THE POD, VERIFY HTTPS CONNECTION",
  "subtitle": "",
  "slide_type": "command_terminal",
  "body": [],
  "code_blocks": [
   {
    "lang": "bash",
    "lines": [
     "# Deploy the fortune application",
     "$ k create -f week10/secrets/fortune-pod-https.yaml -n week10",
     "# Verify HTTPS connection using port-forwarding to the pod and curl command",
     "$ k port-forward fortune-https -n week10 8443:443",
     "$ curl https://localhost:8443 -k -v"
    ]
   },
   {
    "lang": "bash",
    "lines": [
     "* ALPN, server accepted to use http/1.1",
     "* Server certificate:",
     "*  subject: CN=www.kubia-example.com",
     "*  start date: Jul 13 15:36:42 2022 GMT",
     "*  expire date: Jul 10 15:36:42 2032 GMT",
     "*  issuer: CN=www.kubia-example.com",
     "*  SSL certificate verify result: self signed certificate (18), continuing anyway.",
     "> GET / HTTP/1.1",
     "> Host: localhost:8443",
     "> User-Agent: curl/7.79.1",
     "> Accept: */*",
     ">",
     "* Mark bundle as not supporting multiuse",
     "< HTTP/1.1 200 OK",
     "< Server: nginx/1.23.0"
    ]
   }
  ],
  "diagram_description": "Left side: title 'DEPLOY THE POD, VERIFY HTTPS CONNECTION' in white uppercase on a large dark-slate rectangular panel (left quarter of slide). Right side upper area: bulleted command list (orange square bullets). Right side lower area: a black terminal screenshot showing the verbose curl output of the HTTPS/TLS handshake and HTTP 200 response.",
  "notes": "The curl output is an embedded black terminal screenshot image (light/white monospace text), not live text. It shows the TLS handshake details (self-signed cert), request headers, and the '< HTTP/1.1 200 OK' / '< Server: nginx/1.23.0' response confirming HTTPS works. Top accent bars: dark slate, orange, gray."
 },
 {
  "n": 32,
  "title": "UNDERSTANDING  THE WAY SECRET VOLUMES ARE STORED",
  "subtitle": "",
  "slide_type": "concept",
  "body": [
   {
    "text": "# Secret volumes look like files on the disk at /ect/nginx/certs folder.",
    "level": 0
   },
   {
    "text": "# It contradicts the statement that secrets are not stored on host's filesystem.",
    "level": 0
   },
   {
    "text": "# K8s secrets are stored on \"in-memory filesystem\" /tmpfs",
    "level": 0
   },
   {
    "text": "$ k exec fortune-https -c web-server -- mount | grep certs",
    "level": 0
   },
   {
    "text": "# Sensitive data stored in a secret is never written to the disk where it could be compromised",
    "level": 0
   }
  ],
  "code_blocks": [
   {
    "lang": "bash",
    "lines": [
     "$ k exec fortune-https -c web-server -- mount | grep certs"
    ]
   }
  ],
  "diagram_description": "A vertical orange accent bar/rule separates the left title column from the right bullet column. Title 'UNDERSTANDING THE WAY SECRET VOLUMES ARE STORED' in dark gray uppercase on the left (three lines). Bullets (orange square markers) on the right. Top and bottom of slide each have a full-width light-gray horizontal band/bar with a subtle drop shadow.",
  "notes": "Different template variant: two full-width gray banner bars (top and bottom) instead of the tri-color accent bars, and a vertical orange divider between title and bullets. Note typos preserved: '/ect/nginx/certs' (should be /etc), and '/tmpfs' (tmpfs). The mount|grep command is a shell command embedded among the comment bullets. Extra double space in 'UNDERSTANDING  THE'."
 },
 {
  "n": 33,
  "title": "NOTES ABOUT SECRETS AS ENVIRONMENT VARIABLES",
  "subtitle": "",
  "slide_type": "concept",
  "body": [
   {
    "text": "Secrets can be provided to the containers via environment variables",
    "level": 0
   },
   {
    "text": "This is not the recommended way to use secrets",
    "level": 0
   },
   {
    "text": "Environment variables are often dumped into log files those exposing the secrets",
    "level": 1
   },
   {
    "text": "Child processes will inherit environment variables exposing application to the supply chain attack if the third-party libraries are compromised",
    "level": 1
   }
  ],
  "code_blocks": [],
  "diagram_description": "",
  "notes": "Dark charcoal background. Title on left in orange (uppercase). Two decorative horizontal bars at top: left bar gray/blue, right bar orange. Bullets on right in white with orange square bullet markers; child bullets use smaller orange squares."
 },
 {
  "n": 34,
  "title": "WORKSHOP 2: THE END",
  "subtitle": "",
  "slide_type": "workshop_divider",
  "body": [
   {
    "text": "WORKSHOP 2: THE END",
    "level": 0
   }
  ],
  "code_blocks": [],
  "diagram_description": "On the right, a Kubernetes Secret consumption flow diagram. Top: a green ellipse labeled 'API'. Two yellow/orange arrows fan down from API to two blue file-icon boxes side by side: left box labeled 'Pod' with a white gears-and-play-button icon, right box labeled 'Secret' with a white padlock icon. Both blue boxes have yellow arrows pointing down and converging into a green ellipse labeled 'node'. From the node ellipse a single yellow arrow points down to a red icon cluster (red gears with play button beside a red database/storage cylinder icon), representing the container/kubelet consuming the secret on the node.",
  "notes": "White background on right. Title sits inside a dark charcoal vertical rectangular panel on the left (light-on-dark, white text, uppercase). Diagram uses Google/Kubernetes-style icon art (blue file icons, green ellipses, yellow arrows, red container icons)."
 },
 {
  "n": 35,
  "title": "SUMMARY: INJECTING DATA INTO CONTAINERS IN KUBERNETES",
  "subtitle": "",
  "slide_type": "summary",
  "body": [
   {
    "text": "Default token Secret and volume not shown",
    "level": 0
   }
  ],
  "code_blocks": [],
  "diagram_description": "Large architecture diagram (from Kubernetes in Action, Luksa) on the right showing how ConfigMap and Secret data are injected into a Pod. A big green rounded rectangle labeled 'Pod' at the bottom contains two light-blue container boxes and three volume cylinders. Top blue box 'Container: web-server' contains three white mount-path boxes stacked: '/etc/nginx/conf.d/', '/etc/nginx/certs/', '/usr/share/nginx/html/'. Bottom blue box 'Container: html-generator' contains a white cloud shape labeled 'Environment variables:' with 'INTERVAL=25' inside, and a white box '/var/htdocs'. Between the containers and the right side are three volume cylinders: an orange cylinder 'configMap volume: config', a blue cylinder 'secret volume: certs', and a gray/blue cylinder 'emptyDir volume: html'. Arrows: '/etc/nginx/conf.d/' -> configMap volume: config; '/etc/nginx/certs/' -> secret volume: certs; '/usr/share/nginx/html/' -> emptyDir volume: html; '/var/htdocs' -> emptyDir volume: html. On the far right two colored tables: an orange table titled 'ConfigMap: fortune-config' with two rows — row1 key 'my-nginx-config.conf' value 'server { ... }', row2 key 'sleep-interval' value '25'; a blue/purple table titled 'Secret: fortune-https' with three rows — 'https.cert | ...', 'https.key | ...', 'foo | ...'. A solid arrow goes from 'configMap volume: config' to the ConfigMap table (my-nginx-config.conf row). A solid arrow goes from 'secret volume: certs' to the Secret table. A dashed arrow goes from the 'Environment variables: INTERVAL=25' cloud to the ConfigMap 'sleep-interval / 25' row (env var sourced from configMap key). A dashed line also connects toward the Secret 'foo' entry. Below the two tables a small caption box reads 'Default token Secret and volume not shown'.",
  "notes": "White background. Title inside a dark charcoal vertical panel on the left (white uppercase text). This is the classic Luksa 'combining volumes, configMaps and secrets' summary figure. The '/etc/nginx/certs/' box arrow crosses over to the secret volume."
 },
 {
  "n": 36,
  "title": "REFERENCES",
  "subtitle": "",
  "slide_type": "references",
  "body": [
   {
    "text": "https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/",
    "level": 0
   },
   {
    "text": "https://kubernetes.io/docs/tutorials/configuration/",
    "level": 0
   },
   {
    "text": "https://github.com/mmumshad/simple-webapp-mysql",
    "level": 0
   },
   {
    "text": "https://kubernetes.io/docs/concepts/configuration/secret/",
    "level": 0
   },
   {
    "text": "https://kubernetes.io/docs/tasks/inject-data-application/distribute-credentials-secure/",
    "level": 0
   },
   {
    "text": "https://github.com/luksa/kubernetes-in-action/tree/master/Chapter07",
    "level": 0
   }
  ],
  "code_blocks": [],
  "diagram_description": "",
  "notes": "Light/white background theme. Title 'REFERENCES' in dark gray uppercase. Three decorative horizontal bars across the top: dark charcoal (left), orange (center), gray (right). Links are gray underlined hyperlinks with small gray square bullet markers."
 },
 {
  "n": 37,
  "title": "CLEANUP",
  "subtitle": "",
  "slide_type": "cleanup",
  "body": [],
  "code_blocks": [
   {
    "lang": "bash",
    "lines": [
     "# Delete the cluster",
     "$ eksctl delete cluster  --name clo835",
     "# Stop cloud9 instance"
    ]
   }
  ],
  "diagram_description": "Left side: a bordered rectangular image/screenshot of the handwritten word 'Important' in black cursive/marker script, underlined and scribbled beneath in red crayon/pencil, with a red pencil resting diagonally across the lower right of the image.",
  "notes": "Light/white background theme. Title 'CLEANUP' in dark gray uppercase. Three decorative horizontal bars at top: dark charcoal, orange, gray. Command text is plain dark monospace-style lines on the right, not in a styled terminal box. Note double space between 'cluster' and '--name' in the eksctl command, preserved verbatim."
 }
]
_BY_N = {d["n"]: d for d in DECK}

# v2 split — like the other weeks (Week06/09/10 each ship a lecture deck + a lab deck).
# LECTURE = theory/concepts + front/back matter (no hands-on). LAB = the two workshops
# (dividers + hands-on steps + goals) + cleanup, with its own cover. Every source slide
# lands in exactly one deck.
LECTURE_NS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 21, 22, 23, 24, 25, 32, 33, 35, 36]
LAB_NS     = [13, 14, 15, 16, 17, 18, 19, 20, 26, 27, 28, 29, 30, 31, 34, 37]
_LAB_COVER = {"n": 0, "slide_type": "cover", "title": "", "subtitle": "",
              "body": [], "code_blocks": [], "diagram_description": "", "notes": "",
              "cover_role": "Lab"}


def build_deck(slides, out):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]
    total = len(slides)
    for i, d in enumerate(slides, 1):
        s = prs.slides.add_slide(blank)
        render_slide(s, i, total, d)
    _sanitize_coords(prs)
    prs.save(out)
    print(f"wrote {out}  ({total} slides)")


def build_all():
    lecture = [_BY_N[n] for n in LECTURE_NS]
    lab = [_LAB_COVER] + [_BY_N[n] for n in LAB_NS]
    build_deck(lecture, f"Week12/Week12_lecture_style_{VERSION}.pptx")
    build_deck(lab, f"Week12/Week12_lab_style_{VERSION}.pptx")


if __name__ == "__main__":
    # RUN-SAFETY: guarded so importing never writes; run from a dir that has
    # Week12/assets/, Week04/<logo>, and whale.png (repo root or sandbox).
    build_all()
