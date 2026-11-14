"""Week01 — CLO835 Lab02 house design language applied to the Week 1 deck.

Source: week01/Week01.pptx — 38 slides, "CLO835 – Portable Technologies In Cloud"
(Docker Introduction). The source is 4:3, uses six typefaces and twenty off-palette
colours, and carries no whale or footer. This builder re-authors it in the exact
CLO835 house design.

Design language is REUSED, NOT COPIED: this module imports build_week12, the proven
house engine, so the palette, the fonts, the chrome, the terminal mockup, the bullet
glyphs, the course-outline grid and the coordinate guard are the SAME objects, not
re-typed constants. The import is guarded, so it never rebuilds Week12.

Original slide text is preserved VERBATIM (PROMPT.md R1). Typos, double spaces and
the three disagreeing course outlines are kept exactly as the source has them.
Genuine diagrams and screenshots are embedded from week01/assets/ (extracted from the
source and downsampled: 10.9 MB -> 1.4 MB). Native source diagrams (slide 15
monolith/microservices, slide 22 bar chart, slide 25 benefit grid, slide 26 role
cards) are REDRAWN natively in the palette, per PROMPT.md R2/R6.

Content is inline in this file, so the build is reproducible from the repo alone
(week13 and week14 depend on a scratchpad path that no longer exists).

Run from a directory that holds whale.png, docker_logo.jpg, Week04/<logo> and
week01/assets/. Sandbox only — the save path is relative to the working directory.
"""

import os
import build_week12 as bw
from build_week12 import (
    Inches, Pt, MSO_SHAPE,
    BLUE, SLATE, BODY, MUTED, LIGHTBLUE, WHITE, CARD_BG, RULE_GRAY, FOOTER_GRAY,
    GOAL_GREEN, TERMBG, TERM_GRAY, TERM_CYAN, TERM_GRN, STEPS,
    FONT_SANS, FONT_MONO, WHALE,
    CENTER, LEFT, RIGHT, MIDDLE, TOP,
    add_text, add_rect, add_rounded_rect, add_oval, add_line,
    title, bullets, auto_term, terminal, divider, closing, course_outline,
    comparison_table, whale_and_footer, smart_title, _sanitize_coords,
)

VERSION     = "v5"          # v5: carried the user's slide-3/4 edits into the slide-5 table (and slide 4 Dec 09)
WEEK_LABEL  = "Week 1"
DECK_TITLE  = "CLO835 – Portable Technologies In Cloud"
DECK_SUB    = "Docker Introduction"
ASSETS      = "week01/assets"
DOCKER_LOGO = "docker_logo.jpg"


# ---------------------------------------------------------------- figure embed
def embed_fig(s, fname, x, y, w, h):
    """Aspect-correct embed inside a white card with a hairline rule (house pattern)."""
    from PIL import Image
    path = os.path.join(ASSETS, fname)
    iw, ih = Image.open(path).size
    ar = iw / ih
    if (w / h) > ar:
        dh = h; dw = h * ar
    else:
        dw = w; dh = w / ar
    dx = x + (w - dw) / 2.0
    dy = y + (h - dh) / 2.0
    add_rect(s, Inches(dx - 0.04), Inches(dy - 0.04), Inches(dw + 0.08), Inches(dh + 0.08),
             WHITE, line=RULE_GRAY, line_width=0.75)
    s.shapes.add_picture(path, bw._i(Inches(dx)), bw._i(Inches(dy)),
                         bw._i(Inches(dw)), bw._i(Inches(dh)))


def _term_h(nlines, fs):
    return 0.5 + nlines * (fs * 1.52 / 72.0) + 0.22


def _eff_lines(g, w_in, fs):
    cpl = max(10, int(w_in * 72 / (fs * 0.60)))
    return sum(max(1, -(-len(l) // cpl)) for l in g)


# ---------------------------------------------------------------- cover
def render_cover(s, n, total, role="Lecture"):
    """House cover. Week 1 is a Docker week, so the ring holds the Docker logo
    (DESIGN_LANGUAGE.md §5.3 / §9), not the K8s mark used by the K8s weeks."""
    add_text(s, Inches(0.7), Inches(2.25), Inches(7.95), Inches(1.8),
             DECK_TITLE, size=34, bold=True, color=BLUE, line_spacing=1.10)
    add_text(s, Inches(0.72), Inches(4.28), Inches(7.9), Inches(0.6),
             f"{WEEK_LABEL} · {role}", size=22, color=SLATE)
    add_text(s, Inches(0.72), Inches(4.96), Inches(7.9), Inches(0.5),
             DECK_SUB, size=15, italic=True, color=MUTED)
    logo_cx = Inches(10.85); logo_cy = Inches(3.55); ring_r = Inches(1.70)
    add_oval(s, logo_cx - ring_r, logo_cy - ring_r, ring_r * 2, ring_r * 2, WHITE,
             line=LIGHTBLUE, line_width=1.5)
    s.shapes.add_picture(DOCKER_LOGO, logo_cx - Inches(1.3), logo_cy - Inches(1.02),
                         width=Inches(2.6), height=Inches(2.04))
    s.shapes.add_picture(WHALE, Inches(0.45), Inches(6.85), width=Inches(0.5), height=Inches(0.5))
    add_text(s, Inches(9.5), Inches(7.12), Inches(3.35), Inches(0.3),
             f"CLO835, Fall 2026     {n} / {total}", size=10, color=FOOTER_GRAY, align=RIGHT)


# ---------------------------------------------------------------- course outline
# The engine's course_outline() draws the boustrophedon tile grid but no arrows.
# The Week 1 source draws the same grid AS A FLOWCHART: 14 block arrows on slide 3
# and 15 on slide 4, following the snaking reading order. This local renderer keeps
# the engine's exact geometry and adds those direction pointers, using MSO_SHAPE
# arrows (never zero-extent connectors) per PROMPT.md R5, in LIGHTBLUE — the house
# arrow colour already used by build_week08.course_outline().
_OL_COLS, _OL_ROWS = 4, 4
_OL_X0, _OL_Y0 = 0.7, 1.75
_OL_TW, _OL_TH = 2.85, 1.02
_OL_GX, _OL_GY = 0.27, 0.28


def _ol_pos(idx):
    """Grid position of item idx, identical to build_week12.course_outline()."""
    r, c = idx // _OL_COLS, idx % _OL_COLS
    cc = c if r % 2 == 0 else (_OL_COLS - 1 - c)
    return r, cc, _OL_X0 + cc * (_OL_TW + _OL_GX), _OL_Y0 + r * (_OL_TH + _OL_GY)


def _arrow(s, kind, x, y, w, h, fill=LIGHTBLUE):
    shp = s.shapes.add_shape(kind, bw._i(Inches(x)), bw._i(Inches(y)),
                             bw._i(Inches(w)), bw._i(Inches(h)))
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    shp.line.fill.background(); shp.shadow.inherit = False
    return shp


def course_outline_flow(s, items, highlights):
    """Tile grid + the flow arrows the source flowchart shows."""
    # arrows first, so a tile always paints over its own edge
    for idx in range(len(items) - 1):
        r, cc, x, y = _ol_pos(idx)
        r2, cc2, x2, y2 = _ol_pos(idx + 1)
        if r2 == r:
            ay = y + _OL_TH / 2.0 - 0.13
            if cc2 > cc:                                   # row reads left -> right
                _arrow(s, MSO_SHAPE.RIGHT_ARROW, x + _OL_TW, ay, _OL_GX, 0.26)
            else:                                          # row reads right -> left
                _arrow(s, MSO_SHAPE.LEFT_ARROW, x - _OL_GX, ay, _OL_GX, 0.26)
        else:                                              # drop to the next row
            _arrow(s, MSO_SHAPE.DOWN_ARROW,
                   x + _OL_TW / 2.0 - 0.13, y + _OL_TH, 0.26, _OL_GY)
    for idx, label in enumerate(items):
        r, cc, x, y = _ol_pos(idx)
        hi = idx in highlights
        fill = highlights[idx] if hi else CARD_BG
        line = SLATE if hi else RULE_GRAY
        add_rounded_rect(s, Inches(x), Inches(y), Inches(_OL_TW), Inches(_OL_TH), fill,
                         line=line, line_width=1.5 if hi else 0.75, radius_ratio=0.10)
        add_text(s, Inches(x + 0.16), Inches(y), Inches(_OL_TW - 0.32), Inches(_OL_TH),
                 label, size=10.5, bold=hi,
                 color=WHITE if hi else SLATE, anchor=MIDDLE, align=CENTER,
                 line_spacing=1.02)


# ---------------------------------------------------------------- schedule table
def render_schedule(s, n, total, d):
    """Slide 5: the 15-row schedule table, redrawn in the house table style."""
    title(s, d["title"])
    rows = d["rows"]
    x, y, w = 0.60, 1.62, 12.15
    hh, rh = 0.36, 0.315
    ratios = [0.10, 0.10, 0.52, 0.28]
    xs = [x]
    for r in ratios:
        xs.append(xs[-1] + w * r)
    add_rect(s, Inches(x), Inches(y), Inches(w), Inches(hh), SLATE)
    for i, h in enumerate(d["headers"]):
        add_text(s, Inches(xs[i] + 0.12), Inches(y), Inches(w * ratios[i] - 0.2), Inches(hh),
                 h, size=11.5, bold=True, color=WHITE, anchor=MIDDLE)
    cy = y + hh
    for ri, row in enumerate(rows):
        fill = WHITE if ri % 2 == 0 else CARD_BG
        add_rect(s, Inches(x), Inches(cy), Inches(w), Inches(rh), fill,
                 line=RULE_GRAY, line_width=0.5)
        for i, cell in enumerate(row):
            mono = (i < 2)
            add_text(s, Inches(xs[i] + 0.12), Inches(cy), Inches(w * ratios[i] - 0.2), Inches(rh),
                     cell, font=FONT_MONO if mono else FONT_SANS, size=10,
                     color=SLATE if mono else BODY, anchor=MIDDLE, line_spacing=1.0)
        cy += rh
    whale_and_footer(s, n, total)


# ---------------------------------------------------------------- policies
def render_policies(s, n, total, d):
    """Slide 6: policies on the left, the assessment breakdown as a house table."""
    title(s, d["title"])
    bullets(s, 1.70, [(0, t) for t in d["policies"]], x=0.60, w=6.05,
            size=13.5, line_spacing=1.30, space_after=10)
    add_text(s, Inches(6.95), Inches(1.62), Inches(5.85), Inches(0.4),
             d["panel_title"], size=15, bold=True, color=SLATE)
    x, y, w = 6.95, 2.12, 5.85
    rh = 0.52
    for i, (label, pct) in enumerate(d["assessment"]):
        fill = WHITE if i % 2 == 0 else CARD_BG
        add_rect(s, Inches(x), Inches(y + i * rh), Inches(w), Inches(rh), fill,
                 line=RULE_GRAY, line_width=0.5)
        add_rect(s, Inches(x), Inches(y + i * rh), Inches(0.10), Inches(rh), STEPS[i % len(STEPS)])
        add_text(s, Inches(x + 0.30), Inches(y + i * rh), Inches(w - 1.55), Inches(rh),
                 label, size=12.5, color=BODY, anchor=MIDDLE)
        add_text(s, Inches(x + w - 1.15), Inches(y + i * rh), Inches(0.95), Inches(rh),
                 pct, font=FONT_MONO, size=13, bold=True, color=BLUE,
                 align=RIGHT, anchor=MIDDLE)
    ty = y + len(d["assessment"]) * rh
    add_rect(s, Inches(x), Inches(ty), Inches(w), Inches(rh), SLATE)
    add_text(s, Inches(x + 0.30), Inches(ty), Inches(w - 1.55), Inches(rh),
             "Total", size=12.5, bold=True, color=WHITE, anchor=MIDDLE)
    add_text(s, Inches(x + w - 1.15), Inches(ty), Inches(0.95), Inches(rh),
             "100%", font=FONT_MONO, size=13, bold=True, color=WHITE,
             align=RIGHT, anchor=MIDDLE)
    whale_and_footer(s, n, total)


# ---------------------------------------------------------------- native diagrams
def render_micro(s, n, total, d):
    """Slide 15: bullets left; the monolith -> microservices diagram redrawn natively."""
    title(s, d["title"])
    bullets(s, 1.68, [(b["level"], b["text"]) for b in d["body"]], x=0.60, w=5.75,
            size=13.5, line_spacing=1.26, space_after=4)
    # monolith stack
    mx, my, mw = 7.05, 2.35, 1.95
    add_text(s, Inches(mx), Inches(1.90), Inches(mw), Inches(0.32),
             "Monolithic", size=13, bold=True, color=SLATE, align=CENTER)
    for i, lbl in enumerate(("UI", "Logic", "Data")):
        add_rect(s, Inches(mx), Inches(my + i * 0.92), Inches(mw), Inches(0.88), STEPS[i])
        add_text(s, Inches(mx), Inches(my + i * 0.92), Inches(mw), Inches(0.88), lbl,
                 size=13, bold=True, color=WHITE, align=CENTER, anchor=MIDDLE)
    add_text(s, Inches(mx), Inches(my + 2.85), Inches(mw), Inches(0.3),
             "Tightly coupled", size=11, italic=True, color=MUTED, align=CENTER)
    # arrow (MSO shape, never a zero-extent connector — PROMPT.md R5)
    ar = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, bw._i(Inches(9.25)), bw._i(Inches(3.45)),
                            bw._i(Inches(0.85)), bw._i(Inches(0.46)))
    ar.fill.solid(); ar.fill.fore_color.rgb = STEPS[1]
    ar.line.fill.background(); ar.shadow.inherit = False
    # microservices grid
    gx, gy, cw, ch = 10.35, 2.35, 1.14, 0.72
    add_text(s, Inches(gx), Inches(1.90), Inches(cw * 2 + 0.18), Inches(0.32),
             "Microservices", size=13, bold=True, color=SLATE, align=CENTER)
    for i, lbl in enumerate(("Auth", "API", "Cart", "Pay", "Mail", "Log")):
        cx = gx + (i % 2) * (cw + 0.18)
        cy = gy + (i // 2) * (ch + 0.20)
        add_rounded_rect(s, Inches(cx), Inches(cy), Inches(cw), Inches(ch),
                         STEPS[i % len(STEPS)], radius_ratio=0.12)
        add_text(s, Inches(cx), Inches(cy), Inches(cw), Inches(ch), lbl,
                 size=11.5, bold=True, color=WHITE, align=CENTER, anchor=MIDDLE)
    add_text(s, Inches(gx), Inches(gy + 2.85), Inches(cw * 2 + 0.18), Inches(0.3),
             "Loosely coupled", size=11, italic=True, color=MUTED, align=CENTER)
    whale_and_footer(s, n, total)


def render_bar_chart(s, n, total, d):
    """Slide 22: the source chart redrawn natively as a house horizontal bar chart."""
    title(s, d["title"])
    add_text(s, Inches(0.60), Inches(1.52), Inches(12.15), Inches(0.34),
             d["chart_title"], size=13, bold=True, color=SLATE)
    rows = d["rows"]
    top, rh = 2.02, 0.62
    lab_w, bar_x, bar_max = 4.55, 5.35, 6.55
    top_val = max(v for _, v in rows)
    for i, (lab, val) in enumerate(rows):
        y = top + i * rh
        add_text(s, Inches(0.60), Inches(y), Inches(lab_w), Inches(rh - 0.10),
                 lab, size=12, color=BODY, align=RIGHT, anchor=MIDDLE)
        add_line(s, Inches(bar_x), Inches(y), Inches(bar_x), Inches(y + rh - 0.10),
                 color=RULE_GRAY, width=0.75)
        wpx = bar_max * val / 100.0
        add_rect(s, Inches(bar_x + 0.03), Inches(y + 0.10), Inches(wpx), Inches(rh - 0.30),
                 STEPS[i % len(STEPS)])
        add_text(s, Inches(bar_x + wpx + 0.14), Inches(y), Inches(0.9), Inches(rh - 0.10),
                 f"{val}%", font=FONT_MONO, size=12.5, bold=True, color=SLATE, anchor=MIDDLE)
    add_text(s, Inches(0.60), Inches(top + len(rows) * rh + 0.10), Inches(12.15), Inches(0.3),
             d["axis_label"], size=11, italic=True, color=MUTED)
    whale_and_footer(s, n, total)


def render_benefit_grid(s, n, total, d):
    """Slide 25: the six benefits redrawn as a numbered house grid, plus the source photo."""
    title(s, d["title"])
    items = d["items"]
    for i, txt in enumerate(items):
        col, row = i % 2, i // 2
        x = 0.60 + col * 3.75
        y = 1.95 + row * 1.55
        dia = 0.62
        add_oval(s, Inches(x), Inches(y), Inches(dia), Inches(dia), STEPS[i % len(STEPS)])
        add_text(s, Inches(x), Inches(y), Inches(dia), Inches(dia), str(i + 1),
                 size=18, bold=True, color=WHITE, align=CENTER, anchor=MIDDLE)
        add_text(s, Inches(x + 0.82), Inches(y - 0.02), Inches(2.80), Inches(1.30),
                 txt, size=13, color=BODY, line_spacing=1.22)
    embed_fig(s, d["figure"], 8.35, 1.95, 4.45, 4.35)
    whale_and_footer(s, n, total)


def render_two_cards(s, n, total, d):
    """Slide 26: the Developer / Administrator split, redrawn as two house cards."""
    title(s, d["title"])
    for i, card in enumerate(d["cards"]):
        x = 0.60 + i * 6.20
        w = 5.95
        accent = BLUE if i == 0 else SLATE
        add_rounded_rect(s, Inches(x), Inches(1.68), Inches(w), Inches(4.55), CARD_BG,
                         line=RULE_GRAY, line_width=0.75, radius_ratio=0.04)
        add_rect(s, Inches(x), Inches(1.73), Inches(0.12), Inches(4.45), accent)
        add_text(s, Inches(x + 0.34), Inches(1.84), Inches(w - 0.55), Inches(0.40),
                 card["head"], size=16, bold=True, color=accent)
        add_text(s, Inches(x + 0.34), Inches(2.32), Inches(w - 0.55), Inches(0.55),
                 card["lead"], size=13, color=BODY, line_spacing=1.20)
        for j, it in enumerate(card["items"]):
            iy = 3.02 + j * 0.44
            add_oval(s, Inches(x + 0.42), Inches(iy + 0.09), Inches(0.14), Inches(0.14), accent)
            add_text(s, Inches(x + 0.72), Inches(iy), Inches(w - 1.0), Inches(0.40),
                     it, size=13, color=BODY, anchor=MIDDLE)
        add_rect(s, Inches(x + 0.34), Inches(5.42), Inches(w - 0.60), Inches(0.62), WHITE,
                 line=RULE_GRAY, line_width=0.5)
        add_text(s, Inches(x + 0.50), Inches(5.42), Inches(w - 0.92), Inches(0.62),
                 card["foot"], size=12.5, bold=True, color=SLATE, anchor=MIDDLE,
                 line_spacing=1.10)
    whale_and_footer(s, n, total)


def render_dockerfile(s, n, total, d):
    """Slide 36: the Dockerfile, finally in a house terminal mockup with Consolas."""
    title(s, d["title"])
    code = d["dockerfile"]
    y0, ymax, w = 1.58, 6.62, 7.35
    fs = 12
    while fs > 8 and _term_h(_eff_lines(code, w, fs), fs) > (ymax - y0):
        fs -= 1
    th = min(ymax - y0, _term_h(_eff_lines(code, w, fs), fs))
    auto_term(s, 0.60, y0, w, th, d["term_title"], code, font_size=fs)
    x = 8.25
    add_text(s, Inches(x), Inches(1.62), Inches(4.55), Inches(0.36),
             d["side_head"], font=FONT_MONO, size=14, bold=True, color=BLUE)
    bullets(s, 2.06, [(0, t) for t in d["side"]], x=x, w=4.55,
            size=12.5, line_spacing=1.24, space_after=7)
    auto_term(s, x, 4.95, 4.55, _term_h(len(d["tag_lines"]), 11), "bash — tag",
              d["tag_lines"], font_size=11)
    whale_and_footer(s, n, total)


def render_run(s, n, total, d):
    """Slide 38: the two RUN forms, each in its own house terminal."""
    title(s, d["title"])
    add_text(s, Inches(0.60), Inches(1.56), Inches(12.15), Inches(0.36),
             d["lead"], size=16, color=BODY)
    y = 2.20
    for i, blk in enumerate(d["blocks"]):
        x = 0.60 + i * 6.20
        add_text(s, Inches(x), Inches(y), Inches(5.95), Inches(0.90),
                 blk["text"], size=13, color=BODY, line_spacing=1.24)
        auto_term(s, x, y + 1.05, 5.95, _term_h(len(blk["code"]), 13), blk["term"],
                  blk["code"], font_size=13)
    whale_and_footer(s, n, total)


# ---------------------------------------------------------------- generic
def render_content(s, n, total, d):
    body = [(b["level"], b["text"]) for b in d.get("body", [])]
    figs = d.get("figures", [])
    code = d.get("code_blocks", [])
    if d.get("title"):
        title(s, d["title"])
    if figs and body:
        bw_ = d.get("bullet_w", 5.85)
        bs = d.get("bullet_size", 13.5)
        bullets(s, 1.66, body, x=0.60, w=bw_, size=bs, line_spacing=1.26, space_after=6)
        box = d.get("fig_box", (6.85, 1.66, 5.95, 4.85))
        embed_fig(s, figs[0]["file"], *box)
    elif figs and len(figs) > 1:
        embed_fig(s, figs[0]["file"], 0.60, 1.62, 5.95, 4.85)
        embed_fig(s, figs[1]["file"], 6.85, 1.62, 5.95, 4.85)
    elif figs:
        if d.get("title"):
            embed_fig(s, figs[0]["file"], 1.15, 1.62, 11.0, 4.95)
        else:
            embed_fig(s, figs[0]["file"], 0.80, 0.70, 11.73, 6.05)
    elif code:
        lines = []
        for i, cb in enumerate(code):
            if i:
                lines.append("")
            lines.extend(cb["lines"])
        fs = 13
        while fs > 9 and _term_h(_eff_lines(lines, 11.5, fs), fs) > 5.0:
            fs -= 1
        auto_term(s, 0.90, 1.62, 11.5, _term_h(_eff_lines(lines, 11.5, fs), fs),
                  "bash", lines, font_size=fs)
    elif body:
        sz = d.get("bullet_size", 16 if len(body) <= 6 else 14)
        bullets(s, 1.72, body, x=0.60, w=12.15, size=sz,
                line_spacing=d.get("ls", 1.34), space_after=d.get("sa", 8))
    whale_and_footer(s, n, total)


_CUSTOM = {}


def render_slide(s, n, total, d):
    st = d["slide_type"]
    if st == "cover":
        render_cover(s, n, total, d.get("cover_role", "Lecture"))
        return
    if st == "section_divider":
        divider(s, d["kicker"], d["title"], subtitle=d.get("subtitle"))
        whale_and_footer(s, n, total)
        return
    if st == "course_outline":
        title(s, d["title"])
        labels = [b["text"] for b in d["body"]]
        hl = {i: BLUE for i in d.get("highlight", [])}
        course_outline_flow(s, labels, hl)
        whale_and_footer(s, n, total)
        return
    if st in _CUSTOM:
        _CUSTOM[st](s, n, total, d)
        return
    render_content(s, n, total, d)


_CUSTOM.update({
    "schedule":     render_schedule,
    "policies":     render_policies,
    "micro":        render_micro,
    "bar_chart":    render_bar_chart,
    "benefit_grid": render_benefit_grid,
    "two_cards":    render_two_cards,
    "dockerfile":   render_dockerfile,
    "run_instr":    render_run,
})


def build_deck(slides, out):
    prs = bw.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]
    total = len(slides)
    for i, d in enumerate(slides, 1):
        s = prs.slides.add_slide(blank)
        render_slide(s, i, total, d)
        if d.get("hidden"):
            s._element.set("show", "0")
    _sanitize_coords(prs)
    prs.save(out)
    nh = sum(1 for d in slides if d.get("hidden"))
    print(f"wrote {out}  ({total} slides, {nh} hidden)")


# ============================================================================
# DECK — the 38 source slides, text VERBATIM (PROMPT.md R1).
# Typos, double spaces and the three disagreeing course outlines are kept.
# ============================================================================

def _b(*items):
    """(level, text) pairs -> body dicts."""
    return [{"level": lvl, "text": t} for lvl, t in items]


def _f(name):
    return [{"file": name}]


DECK = [
 # ---- 1 cover ----
 {"n": 1, "slide_type": "cover", "title": DECK_TITLE, "cover_role": "Lecture"},

 # ---- 2 Meet & Greet ----
 {"n": 2, "slide_type": "section_divider", "kicker": "WEEK 1", "title": "Meet & Greet",
  "subtitle": None},

 # ---- 3 Course Outline (SmartArt, week numbers) ----
 {"n": 3, "slide_type": "course_outline", "title": "Course Outline",
  "highlight": [0],
  "body": _b(
    (0, "Week 1 : Docker Introduction"),
    (0, "Week 2 : Docker Image Management"),
    (0, "Week 3 : Docker Networking, Storage & Security"),
    (0, "Week 4 : K8s Introduction"),
    (0, "Week 5 :K8s- PODs,  ReplicaSets"),
    (0, "Week 6 : K8s – Services & Deployments"),
    (0, "Week 7 : K8s  –  Volumes"),
    (0, "Study Week"),
    (0, "Week 8 : K8s- K8s- PVs & K8s in  EKS"),
    (0, "Week 9 : K8s: Storage classes &  Statefulsets"),
    (0, "Week 10 : K8s-  Configmaps  & Secrets"),
    (0, "Week 11 : Exam & Mock Exam week"),
    (0, "Week 12 : K8s – RBAC and AKS"),
    (0, "Week 13 : Project presentation  - K8s and HPA"),
    (0, "Week 14 : Project presentation - Helm"),
  )},

 # ---- 4 Course Outline (SmartArt, dates) ----
 {"n": 4, "slide_type": "course_outline", "title": "Course Outline",
  "highlight": [0],
  "body": _b(
    (0, "Sep 09 : Docker Introduction"),
    (0, "Sep 16 : Docker Image Management     Assignment 1 Release"),
    (0, "Sep 23 : Docker Networking, Storage & Security     Quiz  1"),
    (0, "Sep 30: K8s Introduction  Assignment 1- Due Date"),
    (0, "Oct 07:K8s- PODs,  ReplicaSets     Quiz2   Assignment 2  release"),
    (0, "Oct 14: K8s – Services & Deployments"),
    (0, "Oct 21 : K8s - Volumes"),
    (0, "Oct 28 : Study Week   Assignment 2- Due date"),
    (0, "Nov 04 :   K8s- PVs & K8s in  EKS   Final Project Release"),
    (0, "Nov 11 : K8s: Storage classes &  Statefulsets              Quiz 3"),
    (0, "Nov 18 :  Exam"),
    (0, "Nov 25 :  K8s-  Configmaps  & Secrets   Quiz 4"),
    (0, "Dec 02 : K8s – RBAC and  EKS  Final Project Due date"),
    (0, "Dec 09 : Project presentation - K8s and HPA  Quiz  5"),
    (0, "Dec 16 : Project presentation - Helm"),
    (0, "Dec 20 : Term End"),
  )},

 # ---- 5 Course Outline (table) ----
 {"n": 5, "slide_type": "schedule", "title": "Course Outline",
  "headers": ["Week", "Date", "Topic", "Milestones"],
  "rows": [
    ["Week 01", "Sep 09", "Docker Introduction", ""],
    ["Week 02", "Sep 16", "Docker Image Management", "Assignment 1 Release"],
    ["Week 03", "Sep 23", "Docker Networking, Storage & Security", "Quiz 1"],
    ["Week 04", "Sep 30", "K8s Introduction", "Assignment 1 Due"],
    ["Week 05", "Oct 07", "K8s - PODs, ReplicaSets", "Quiz 2, Assignment 2 Release"],
    ["Week 06", "Oct 14", "K8s – Services & Deployments", ""],
    ["Week 07", "Oct 21", "K8s - Volumes", ""],
    ["Week 08", "Oct 28", "Study Week", "Assignment 2 Due"],
    ["Week 09", "Nov 04", "K8s - PVs & K8s in EKS", "Final Project Release"],
    ["Week 10", "Nov 11", "K8s: Storage Classes & Statefulsets", "Quiz 3"],
    ["Week 11", "Nov 18", "Exam", ""],
    ["Week 12", "Nov 25", "K8s - Configmaps & Secrets", "Quiz 4"],
    ["Week 13", "Dec 02", "K8s – RBAC and EKS", "Final Project Due"],
    ["Week 14", "Dec 09", "Project presentation - K8s and HPA", "Quiz 5"],
    ["Week 15", "Dec 16", "Project presentation - Helm", ""],
  ]},

 # ---- 6 Course Policies + Assessment Summary ----
 {"n": 6, "slide_type": "policies", "title": "Course Policies",
  "policies": [
    "Achieve a weighted average of 50% or better on the overall course",
    "Achieve a weighted average of 50% or better for the individual assignments & Tests",
    "Achieve a grade of 50% or better for the final project",
    "Must satisfactorily complete all labs, individual assignments, and projects",
  ],
  "panel_title": "Assessment Summary",
  "assessment": [
    ("Labs (2.5% × 8)", "20%"),
    ("Quizzes (2% × 5)", "10%"),
    ("Individual Assignments (15% × 2)", "30%"),
    ("Tests", "20%"),
    ("Final Project", "20%"),
  ]},

 # ---- 7 section divider ----
 {"n": 7, "slide_type": "section_divider", "kicker": "WEEK 1", "title": "Containers",
  "subtitle": None},

 # ---- 8 Agenda (visual order of the source SmartArt) ----
 {"n": 8, "slide_type": "content", "title": "Agenda", "bullet_size": 15, "ls": 1.42, "sa": 6,
  "body": _b(
    (0, "Benefits of Containerized Applications"),
    (0, "Introduction to Containers"),
    (0, "What is Docker"),
    (0, "Docker Architecture"),
    (0, "Run Docker Containers"),
    (0, "Create Docker Images"),
    (0, "Publish Docker Images with Amazon ECR"),
    (0, "Networks in Docker"),
    (0, "Docker  Storage"),
    (0, "Docker Concepts in Depth"),
    (0, "Build and Push to Amazon ECR  from Cloud9"),
    (0, "Build and Push to Amazon ECR with GitHub Actions"),
  )},

 # ---- 9 Why do you need Docker? ----
 {"n": 9, "slide_type": "content", "title": "Why do you need Docker?",
  "bullet_w": 5.55, "bullet_size": 13,
  "fig_box": (6.55, 1.66, 6.25, 4.85),
  "figures": _f("fig09.jpg"),
  "body": _b(
    (0, "Compatibility/Dependency:"),
    (1, "Many different stacks:"),
    (2, "languages"), (2, "frameworks"), (2, "databases"),
    (0, "Long Setup time"),
    (0, "Many different targets:"),
    (1, "individual development environments"),
    (1, "pre-production, QA, staging..."),
    (1, "production: on prem, cloud, hybrid"),
    (0, "Used for developing, building and shipping application"),
  )},

 # ---- 10 The Deployment Problem ----
 {"n": 10, "slide_type": "content", "title": "The Deployment Problem",
  "figures": _f("fig10.png")},

 # ---- 11 shipping industry ----
 {"n": 11, "slide_type": "content", "title": "The parallel with the shipping industry",
  "figures": [{"file": "fig11_1.png"}, {"file": "fig11_2.png"}]},

 # ---- 12 Escape dependency hell ----
 {"n": 12, "slide_type": "content", "title": "Escape dependency hell",
  "bullet_size": 15, "ls": 1.36, "sa": 10,
  "body": _b(
    (0, "Step 1: Document all dependencies and setup steps in an INSTALL.txt file"),
    (0, "Step 2: Convert those instructions into an install.sh script and verify it runs on your machine"),
    (0, "Step 3: Translate the script into a Dockerfile — each install step becomes a Docker layer"),
    (0, "Step 4: Build and test the Docker image locally"),
    (0, "Step 5: Share the image — if it builds on your machine, it builds anywhere"),
    (0, "No more “works on my machine” — no more “worked in dev, ops problem now!”"),
  )},

 # ---- 13 Devs vs Ops, before Docker ----
 {"n": 13, "slide_type": "content", "title": "Devs vs Ops, before Docker",
  "bullet_w": 6.05, "bullet_size": 13.5,
  "fig_box": (7.05, 1.80, 5.75, 4.50),
  "figures": _f("fig13.jpg"),
  "body": _b(
    (0, "Drop a tarball (or a commit hash) with instructions."),
    (0, "Dev environment very different from production."),
    (0, "Ops don’t always have a dev environment themselves ..."),
    (0, "... and when they do, it can differ from the devs’."),
    (0, "Ops have to sort out differences and make it work ..."),
    (0, "... or bounce it back to devs."),
    (0, "Shipping code causes frictions and delays."),
  )},

 # ---- 14 Devs vs Ops, after Docker ----
 {"n": 14, "slide_type": "content", "title": "Devs vs Ops, after Docker",
  "bullet_size": 14, "ls": 1.30, "sa": 6,
  "body": _b(
    (0, "For Developers:"),
    (1, "Package your app as a container image or a Compose file — a single, portable artifact"),
    (1, "Ship with confidence — if it runs locally, it runs in production"),
    (1, "Self-service releases become possible without waiting on Ops"),
    (0, "For Operations:"),
    (1, "Every delivery is a runnable container — no more guessing dependencies"),
    (1, "Use the same image across dev, staging, and production environments"),
    (1, "Still adapt for production specifics, but with a reliable reference point"),
    (0, "Docker bridges the Dev/Ops gap — one artifact, every environment."),
  )},

 # ---- 15 Why Containers? (native diagram) ----
 {"n": 15, "slide_type": "micro", "title": "Why Containers?",
  "body": _b(
    (0, "The software industry has changed"),
    (0, "Before:"),
    (1, "monolithic applications"), (1, "long development cycles"),
    (1, "single environment"), (1, "slowly scaling up"),
    (0, "Now:"),
    (1, "decoupled services"), (1, "fast, iterative improvements"),
    (1, "multiple environments"), (1, "quickly scaling out"),
  )},

 # ---- 16 What are Containers ----
 {"n": 16, "slide_type": "content", "title": "What are Containers",
  "bullet_size": 15, "ls": 1.40, "sa": 14,
  "body": _b(
    (0, "LXC (Linux Containers) is an operating-system-level virtualization method for running multiple isolated Linux systems (containers) on a control host using a single Linux kernel."),
    (0, "The Linux kernel provides cgroups — allows limitation and prioritization of resources (CPU, memory, block I/O, network) without the need for virtual machines."),
    (0, "Namespace isolation — provides complete isolation of an application’s view of the OS environment, including process trees, networking, user IDs, and mounted file systems."),
  )},

 # ---- 17 image-only ----
 {"n": 17, "slide_type": "content", "title": "", "figures": _f("fig17.png")},

 # ---- 18 What Docker Does? ----
 {"n": 18, "slide_type": "content", "title": "What Docker Does?", "figures": _f("fig18.png")},

 # ---- 19 Containers vs VMs ----
 {"n": 19, "slide_type": "content", "title": "Containers vs VMs",
  "bullet_w": 4.15, "bullet_size": 14,
  "fig_box": (5.05, 1.66, 7.75, 4.85),
  "figures": _f("fig19.png"),
  "body": _b(
    (0, "Small/Light weight and Fast"),
    (0, "Portable"),
    (0, "Heavy weight, non portable"),
  )},

 # ---- 20 Containers & VMs ----
 {"n": 20, "slide_type": "content", "title": "Containers & VMs", "figures": _f("fig20.png")},

 # ---- 21 Containers Adoption Rate ----
 {"n": 21, "slide_type": "content", "title": "Containers Adoption Rate",
  "figures": _f("fig21.png")},

 # ---- 22 Perceived Benefits (native chart) ----
 {"n": 22, "slide_type": "bar_chart", "title": "Perceived Benefits from containers adoption",
  "chart_title": "What benefits has your organization realized from operating Kubernetes?",
  "axis_label": "% of respondents",
  "rows": [
    ("Improved resource utilization", 56),
    ("Shortened software development cycles", 53),
    ("Containerized monolithic applications", 50),
    ("Enabled our move to the cloud", 42),
    ("Reduced public cloud costs", 33),
    ("Other", 2),
    ("We have not realized any benefits", 5),
  ]},

 # ---- 23 What is Docker ----
 {"n": 23, "slide_type": "content", "title": "What is Docker",
  "bullet_w": 6.35, "bullet_size": 14,
  "fig_box": (7.35, 2.55, 5.45, 2.60),
  "figures": _f("fig23.png"),
  "body": _b(
    (0, "Docker is an open-source project that automates the deployment of applications inside software containers."),
    (0, "Docker containers wrap up a piece of software in a complete file system that contains everything it needs to run: code, runtime, system tools, and system libraries — anything you can install on a server."),
    (0, "This guarantees that it will always run the same, regardless of the environment it runs in."),
  )},

 # ---- 24 Docker Architecture ----
 {"n": 24, "slide_type": "content", "title": "Docker Architecture",
  "bullet_w": 5.25, "bullet_size": 13,
  "fig_box": (6.20, 1.80, 6.60, 4.55),
  "figures": _f("fig24.png"),
  "body": _b(
    (0, "“Installing Docker” really means “Installing the Docker Engine and CLI”."),
    (0, "The Docker Engine is a daemon (a service running in the background)."),
    (0, "This daemon manages containers, the same way that a hypervisor manages VMs."),
    (0, "We interact with the Docker Engine by using the Docker CLI."),
    (0, "The Docker CLI and the Docker Engine communicate through an API."),
    (0, "There are many other programs and client libraries which use that API."),
  )},

 # ---- 25 What makes docker containers so popular ----
 {"n": 25, "slide_type": "benefit_grid", "title": "What makes docker containers so popular",
  "figure": "fig25.jpg",
  "items": [
    "Build once, run everywhere",
    "Dependencies isolation",
    "Ease of use with docker command line tool",
    "Scalability with the orchestration tools",
    "Up and running in seconds",
    "Massive scale",
  ]},

 # ---- 26 Developers and Admins ----
 {"n": 26, "slide_type": "two_cards", "title": "Developers and Admins: Separation of concerns",
  "cards": [
    {"head": "The Developer",
     "lead": "Responsible for the “inside” of the container",
     "items": ["Code", "Libraries", "Package manager", "Application", "Data"],
     "foot": "All Linux servers  look the same"},
    {"head": "The Administrator",
     "lead": "Responsible for the “outside” of the container",
     "items": ["Logging", "Monitoring", "Remote Access", "Networking", "Security"],
     "foot": "Start, stop, attach, migrate all the containerized apps the same way"},
  ]},

 # ---- 27 Understanding Docker Images ----
 {"n": 27, "slide_type": "content", "title": "Understanding Docker Images",
  "figures": _f("fig27.png")},

 # ---- 28 What is an image? ----
 {"n": 28, "slide_type": "content", "title": "What is an image?",
  "bullet_size": 14, "ls": 1.32, "sa": 7,
  "body": _b(
    (0, "Image = files + metadata"),
    (0, "These files form the root filesystem of our container."),
    (0, "The metadata can indicate a number of things, e.g.:"),
    (1, "the author of the image"),
    (1, "the command to execute in the container when starting it"),
    (1, "environment variables to be set"),
    (1, "etc."),
    (0, "Images are made of layers, conceptually stacked on top of each other."),
    (0, "Each layer can add, change, and remove files and/or metadata."),
    (0, "Images can share layers to optimize disk usage, transfer times, and memory use."),
  )},
]

_LAYERS_BODY = _b(
    (0, "Each of the following items will correspond to one layer:"),
    (1, "CentOS base layer"),
    (1, "Packages and configuration files added by our local IT"),
    (1, "JRE"),
    (1, "Tomcat"),
    (1, "Our application’s dependencies"),
    (1, "Our application code and assets"),
    (1, "Our application configuration"),
    (0, "(Note: app config is generally added by orchestration facilities.)"),
)

DECK += [
 # ---- 29 + 30 Image Layers (the source ships this slide TWICE, verbatim) ----
 {"n": 29, "slide_type": "content", "title": "Image Layers Example for Java Web Applications",
  "bullet_w": 6.30, "bullet_size": 13.5,
  "fig_box": (7.40, 1.90, 5.40, 4.35),
  "figures": _f("fig29.jpg"), "body": _LAYERS_BODY},
 {"n": 30, "slide_type": "content", "title": "Image Layers Example for Java Web Applications",
  "bullet_w": 6.30, "bullet_size": 13.5,
  "fig_box": (7.40, 1.90, 5.40, 4.35),
  "figures": _f("fig29.jpg"), "body": _LAYERS_BODY},

 # ---- 31 Containers and Images ----
 {"n": 31, "slide_type": "content", "title": "Containers and Images",
  "bullet_w": 4.35, "bullet_size": 13,
  "fig_box": (5.25, 1.80, 7.55, 4.55),
  "figures": _f("fig31_1.png"),
  "body": _b(
    (0, "An image is a read-only filesystem."),
    (0, "A container is an encapsulated set of processes,running in a read-write copy of that filesystem."),
    (0, "To optimize container boot time, copy-on-write is used instead of regular copy."),
    (0, "docker run starts a container from a given image."),
  )},

 # ---- 32 Differences between containers and images ----
 {"n": 32, "slide_type": "content", "title": "Differences between containers and images",
  "bullet_size": 16, "ls": 1.55, "sa": 16,
  "body": _b(
    (0, "An image is a read-only filesystem."),
    (0, "A container is an encapsulated set of processes, running in a read-write copy of that filesystem."),
    (0, "To optimize container boot time,  copy-on-write  is used instead of regular copy."),
    (0, "docker run starts a container from a given image."),
  )},

 # ---- 33 Immutable images ----
 {"n": 33, "slide_type": "content",
  "title": "Docker Images Are Immutable. So how can we change them?",
  "bullet_w": 5.95, "bullet_size": 14,
  "fig_box": (6.95, 2.20, 5.85, 4.10),
  "figures": _f("fig33.png"),
  "body": _b(
    (0, "We don’t."),
    (0, "We create a new container from that image."),
    (0, "Then we make changes to that container."),
    (0, "When we are satisfied with those changes, we transform them into a new layer."),
    (0, "A new image is created by stacking the new layer on top of the old image."),
  )},

 # ---- 34 Images Namespaces ----
 {"n": 34, "slide_type": "content", "title": "Images Namespaces",
  "bullet_size": 15, "ls": 1.45, "sa": 14,
  "body": _b(
    (0, "There are three namespaces:"),
    (1, "Official images- gated by Docker Inc, authored and maintained by third parties  e.g. ubuntu, busybox …"),
    (1, "User (and organizations) images for DockerHub users  e.g. jenkins/jenkins"),
    (1, "Self-hosted images – not hosted in DockerHub"),
    (2, "e.g. registry.example.com:5000/my-private/image"),
  )},

 # ---- 35 Docker File ----
 {"n": 35, "slide_type": "content", "title": "Docker File",
  "bullet_size": 16, "ls": 1.50, "sa": 16,
  "body": _b(
    (0, "Docker can build images by reading the instructions provided in Dockerfile"),
    (0, "A Dockerfile is a text document that contains all the commands a user could call to assemble an image"),
    (0, "Using docker build users can create an automated build that executes a set of command line instructions in succession"),
    (0, "The docker build command builds an image from a Dockerfile and a context"),
  )},

 # ---- 36 Docker File: Example ----
 {"n": 36, "slide_type": "dockerfile", "title": "Docker File: Example",
  "term_title": "Dockerfile",
  "dockerfile": [
    "# Each instruction in this file generates a new layer that gets pushed to your local image cache",
    "# Lines preceeded by # are regarded as comments and ignored",
    "# The line below states we will base our new image on the Latest Official Ubuntu",
    "FROM ubuntu:latest",
    "# Identify the maintainer of an image",
    "LABEL maintainer=\"myname@somecompany.com\"",
    "# Update the image to the latest packages",
    "RUN apt-get update && apt-get upgrade -y",
    "# Install NGINX to test.",
    "RUN apt-get install nginx -y",
    "# Expose port 80",
    "EXPOSE 80",
    "# Last is the actual command to start up NGINX within our Container",
    "CMD [\"nginx\", \"-g\", \"daemon off;\"]",
  ],
  "side_head": "$ docker build  (used 99% of the time)",
  "side": [
    "Performs a repeatable build sequence.",
    "This is the preferred method!",
    "Images can be stored on your Docker host or in docker registry",
  ],
  "tag_lines": [
    "# Adding tags",
    "$ docker tag <image id> nginx",
  ]},

 # ---- 37 Dockerfile usage summary ----
 {"n": 37, "slide_type": "content", "title": "Dockerfile usage summary",
  "bullet_size": 14, "ls": 1.34, "sa": 8,
  "body": _b(
    (0, "Dockerfile instructions are executed in order."),
    (0, "Each instruction creates a new layer in the image."),
    (0, "Docker maintains a cache with the layers of previous builds."),
    (0, "When there are no changes in the instructions and files making a layer, the builder re-uses the cached layer, without executing the instruction for that layer."),
    (0, "The FROM instruction MUST be the first non-comment instruction."),
    (0, "Lines starting with # are treated as comments."),
    (0, "Some instructions (like CMD or ENTRYPOINT) update a piece of metadata."),
    (1, "(As a result, each call to these instructions makes the previous one useless.)"),
  )},

 # ---- 38 The RUN instruction ----
 {"n": 38, "slide_type": "run_instr", "title": "The RUN instruction",
  "lead": "The RUN instruction can be specified in two ways.",
  "blocks": [
    {"text": "With shell wrapping, which runs the specified command inside a shell, with /bin/sh -c:",
     "term": "shell form", "code": ["RUN  apt-get update"]},
    {"text": "Or using the exec method, which avoids shell string expansion, and allows execution "
             "in images that don’t have /bin/sh:",
     "term": "exec form", "code": ["RUN  [ \"apt-get\", \"update\" ]"]},
  ]},
]

_BY_N = {d["n"]: d for d in DECK}


def build_all():
    build_deck(DECK, f"week01/Week01_lecture_style_{VERSION}.pptx")


if __name__ == "__main__":
    # RUN-SAFETY: guarded, so importing this module never writes a deck.
    build_all()
