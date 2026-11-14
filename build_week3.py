"""Build Week3_lab_style.pptx — Lab02 design language, content for
'Docker Networking, Storage & Security'. Sources: Week3.pptx (existing
course material) for networking + storage; security pillars added from
standard Docker hardening practices."""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from lxml import etree

# === Lab02 palette (verbatim from Lab02.pptx XML) ===
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
TERM_ORANGE = RGBColor(0xFF, 0xBD, 0x2E)
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

# ===== helpers (identical to build_week03.py) =====

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

def whale_and_footer(slide, page_num, total=14):
    slide.shapes.add_picture("whale.png", Inches(0.45), Inches(6.85),
                             width=Inches(0.5), height=Inches(0.5))
    add_line(slide, Inches(0.5), Inches(7.05),
             Inches(12.83), Inches(7.05), color=RULE_GRAY, width=0.5)
    add_text(slide, Inches(9.5), Inches(7.12), Inches(3.35), Inches(0.3),
             f"CLO835, Fall 2026     {page_num} / {total}",
             size=10, color=FOOTER_GRAY, align=PP_ALIGN.RIGHT)

def title(slide, text, x=Inches(0.55), y=Inches(0.4),
          w=Inches(12.2), h=Inches(0.8)):
    add_text(slide, x, y, w, h, text, size=32, bold=True, color=BLUE,
             line_spacing=1.05)

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
blank = prs.slide_layouts[6]

TOTAL = 14


# ============================================================
# SLIDE 1 - Title
# ============================================================
s = prs.slides.add_slide(blank)
add_text(s, Inches(0.7), Inches(2.4), Inches(8.5), Inches(1.0),
         "CLO835 — Week 3", size=44, bold=True, color=BLUE,
         line_spacing=1.0)
add_text(s, Inches(0.7), Inches(3.4), Inches(7.8), Inches(1.4),
         "Docker Networking, Storage and Security",
         size=22, color=BODY, line_spacing=1.3)
add_text(s, Inches(0.7), Inches(4.15), Inches(7.8), Inches(0.5),
         "Three things every container engineer ships with.",
         size=14, italic=True, color=MUTED)
# Docker logo in light-blue ring
logo_cx = Inches(10.4); logo_cy = Inches(3.75); ring_r = Inches(2.0)
ring = add_oval(s, logo_cx - ring_r, logo_cy - ring_r,
                ring_r * 2, ring_r * 2, WHITE, line=LIGHTBLUE)
ring.line.width = Pt(1.5)
s.shapes.add_picture("docker_logo.jpg",
                     logo_cx - Inches(1.4), logo_cy - Inches(1.1),
                     width=Inches(2.8), height=Inches(2.2))
add_rich_text(s, Inches(0.7), Inches(6.5), Inches(7), Inches(0.7),
              [[("Instructor: ", {"size": 12, "color": MUTED}),
                ("Professor Maziar", {"size": 12, "bold": True, "color": SLATE})],
               [("Seneca Polytechnic · ITAS Program",
                 {"size": 10.5, "italic": True, "color": MUTED})]])
s.shapes.add_picture("whale.png", Inches(0.45), Inches(6.85),
                     width=Inches(0.5), height=Inches(0.5))
add_text(s, Inches(9.5), Inches(7.12), Inches(3.35), Inches(0.3),
         f"CLO835, Fall 2026     1 / {TOTAL}",
         size=10, color=FOOTER_GRAY, align=PP_ALIGN.RIGHT)


# ============================================================
# SLIDE 2 - Agenda
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "What you'll learn this week")
add_text(s, Inches(0.55), Inches(1.05), Inches(12), Inches(0.4),
         "Three topics, layered. Each one is something containers need before they leave your laptop.",
         size=14, italic=True, color=MUTED)

def objective(x, y, num, heading, body):
    d = Inches(0.75)
    add_oval(s, x, y, d, d, SLATE)
    add_text(s, x, y, d, d, str(num), size=22, bold=True, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, x + Inches(1.05), y + Inches(0.0), Inches(4.6), Inches(0.4),
             heading, size=15, bold=True, color=SLATE)
    add_text(s, x + Inches(1.05), y + Inches(0.45), Inches(4.6), Inches(1.5),
             body, size=12.5, color=BODY, line_spacing=1.35)

objective(Inches(0.55), Inches(2.0), 1, "Docker networking",
          "How containers talk to each other and the outside world. "
          "Drivers, DNS-based service discovery, and the CNM vs CNI models.")
objective(Inches(7.0), Inches(2.0), 2, "Persistent storage",
          "Why containers lose data on delete by default — and the three "
          "ways to make it survive: volumes, bind mounts, and tmpfs.")
objective(Inches(0.55), Inches(4.55), 3, "Container security",
          "The four pillars: trusted images, runtime isolation, secrets "
          "handling, and network policy. Defend at every layer.")
objective(Inches(7.0), Inches(4.55), 4, "Decision frameworks",
          "When to use bridge vs overlay, -v vs --mount, root vs non-root. "
          "By the end you'll know which knob to turn.")
whale_and_footer(s, 2, TOTAL)


# ============================================================
# SLIDE 3 - What is a Docker network?
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "What is a Docker network?")

# Left: text
add_text(s, Inches(0.55), Inches(1.30), Inches(6.0), Inches(0.5),
         "A virtual switch for containers.",
         size=18, bold=True, color=SLATE)
add_text(s, Inches(0.55), Inches(1.90), Inches(6.0), Inches(2.0),
         "Conceptually, a Docker network behaves like a VLAN or a Wi-Fi SSID. "
         "Each network has its own subnet, its own DNS zone, and its own scope "
         "(local to one host, or global across many).",
         size=13, color=BODY, line_spacing=1.4)
add_text(s, Inches(0.55), Inches(3.50), Inches(6.0), Inches(0.5),
         "Three things to remember",
         size=14, bold=True, color=BLUE)

def fact(y, head, body):
    d = Inches(0.45)
    add_oval(s, Inches(0.55), Inches(y), d, d, SLATE)
    add_text(s, Inches(0.55), Inches(y), d, d, "✓",
             size=14, bold=True, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(1.15), Inches(y - 0.04), Inches(5.5), Inches(0.3),
             head, size=12.5, bold=True, color=SLATE)
    add_text(s, Inches(1.15), Inches(y + 0.22), Inches(5.5), Inches(0.5),
             body, size=11, color=BODY, line_spacing=1.3)

fact(4.05, "Containers join a default network at start",
     "Usually the `bridge` network, unless you say otherwise.")
fact(4.85, "Containers can be on zero, one, or many networks",
     "Attachments can change at runtime with docker network connect.")
fact(5.65, "Containers find each other by name on user-defined networks",
     "Each network has its own DNS — no hard-coded IPs needed.")

# Right: simple diagram — host box containing bridge + 3 containers
host_x = Inches(7.2); host_y = Inches(1.30)
host_w = Inches(5.6); host_h = Inches(4.95)
host = add_rect(s, host_x, host_y, host_w, host_h, WHITE, line=SLATE)
host.line.width = Pt(1.5)
add_text(s, host_x + Inches(0.15), host_y + Inches(0.10),
         host_w - Inches(0.3), Inches(0.3),
         "Docker host", size=11, bold=True, color=SLATE)

# Bridge network inside
br_x = host_x + Inches(0.30); br_y = host_y + Inches(0.55)
br_w = host_w - Inches(0.60); br_h = Inches(3.20)
br = add_rect(s, br_x, br_y, br_w, br_h, CARD_BG, line=BLUE)
br.line.width = Pt(1.25)
add_text(s, br_x + Inches(0.15), br_y + Inches(0.10),
         br_w - Inches(0.3), Inches(0.3),
         "bridge network   ·   172.17.0.0/16",
         font=FONT_MONO, size=10, bold=True, color=BLUE)

# 3 containers as small rounded boxes
ctr_w = Inches(1.40); ctr_h = Inches(0.85)
ctr_y = br_y + Inches(1.10)
gap = (br_w - 3 * ctr_w) / 4
for i in range(3):
    cx = br_x + gap + (ctr_w + gap) * i
    add_rect(s, cx, ctr_y, ctr_w, ctr_h, BLUE)
    add_text(s, cx, ctr_y, ctr_w, ctr_h - Inches(0.30),
             f"container {i+1}", size=11, bold=True, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, cx, ctr_y + Inches(0.50), ctr_w, Inches(0.30),
             f"172.17.0.{i+2}", size=9, color=WHITE, font=FONT_MONO,
             align=PP_ALIGN.CENTER)

# Caption
add_text(s, br_x + Inches(0.15), br_y + br_h - Inches(0.4),
         br_w - Inches(0.3), Inches(0.3),
         "Each network gets a subnet · containers get IPs from it",
         size=10, italic=True, color=MUTED, align=PP_ALIGN.CENTER)

# External
add_text(s, host_x + Inches(0.30), host_y + host_h - Inches(0.65),
         host_w - Inches(0.6), Inches(0.5),
         "Outside world reaches containers only through published ports (-p HOST:CTR).",
         size=10.5, italic=True, color=MUTED, line_spacing=1.3,
         align=PP_ALIGN.CENTER)

whale_and_footer(s, 3, TOTAL)


# ============================================================
# SLIDE 4 - Network drivers comparison
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "Network drivers — pick the right one")

rows = [
    ["Driver",   "Scope",            "What it does",                                   "Use it when"],
    ["bridge",   "Single host",      "Default. Isolated virtual switch on one host.",  "Most local development"],
    ["host",     "Single host",      "Shares the host network stack — no isolation.",  "You need the fastest path"],
    ["overlay",  "Multi-host",       "Virtual network spanning Swarm/cluster nodes.",  "Containers across machines"],
    ["macvlan",  "Single host",      "Each container gets a MAC on the physical net.", "Containers need real LAN IPs"],
    ["none",     "Nothing",          "No interfaces at all (except loopback).",        "Maximum isolation, batch jobs"],
]

n_rows = len(rows)
col_w = [Inches(1.9), Inches(2.2), Inches(4.6), Inches(3.5)]
left = Inches(0.55); top = Inches(1.40)
row_h = Inches(0.75)

x = left
for c, cell in enumerate(rows[0]):
    add_rect(s, x, top, col_w[c], row_h, SLATE)
    add_text(s, x, top, col_w[c], row_h, cell,
             size=12.5, bold=True, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    x += col_w[c]

for r, row in enumerate(rows[1:], start=1):
    x = left
    y = top + row_h * r
    band = (r % 2 == 0)
    for c, cell in enumerate(row):
        bg = CARD_BG if band else WHITE
        add_rect(s, x, y, col_w[c], row_h, bg)
        if c == 0:
            add_text(s, x + Inches(0.2), y, col_w[c] - Inches(0.2), row_h, cell,
                     font=FONT_MONO, size=12, bold=True, color=BLUE,
                     align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)
        elif c == 1:
            add_text(s, x + Inches(0.15), y, col_w[c] - Inches(0.15), row_h, cell,
                     size=11.5, color=SLATE, bold=True,
                     align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)
        else:
            add_text(s, x + Inches(0.15), y, col_w[c] - Inches(0.15), row_h, cell,
                     size=11, color=BODY,
                     align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE,
                     line_spacing=1.25)
        x += col_w[c]

add_rich_text(s, Inches(0.55), Inches(6.15), Inches(12.2), Inches(0.5),
              [[("Rule of thumb: ",
                 {"size": 13, "bold": True, "color": SLATE}),
                ("use ",
                 {"size": 13, "color": MUTED, "italic": True}),
                ("bridge",
                 {"size": 13, "font": FONT_MONO, "bold": True, "color": BLUE}),
                (" for local dev · ",
                 {"size": 13, "color": MUTED, "italic": True}),
                ("overlay",
                 {"size": 13, "font": FONT_MONO, "bold": True, "color": BLUE}),
                (" for multi-host · ",
                 {"size": 13, "color": MUTED, "italic": True}),
                ("host",
                 {"size": 13, "font": FONT_MONO, "bold": True, "color": BLUE}),
                (" only when you've measured a real reason to.",
                 {"size": 13, "color": MUTED, "italic": True})]])

whale_and_footer(s, 4, TOTAL)


# ============================================================
# SLIDE 5 - Working with networks (commands)
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "Working with networks — the commands you'll use")

# Left: bullets explaining commands
add_text(s, Inches(0.55), Inches(1.40), Inches(6.0), Inches(0.5),
         "Four verbs cover 99% of daily work.",
         size=16, bold=True, color=SLATE)

def cmd_row(y, cmd, desc):
    add_rect(s, Inches(0.55), Inches(y), Inches(2.0), Inches(0.45), CARD_BG)
    add_text(s, Inches(0.55), Inches(y), Inches(2.0), Inches(0.45),
             cmd, size=11.5, bold=True, color=BLUE, font=FONT_MONO,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(2.75), Inches(y + 0.05), Inches(3.8), Inches(0.45),
             desc, size=12, color=BODY,
             anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.3)

cmd_row(2.10, "ls",        "List networks on this host.")
cmd_row(2.65, "create",    "Make a new user-defined network.")
cmd_row(3.20, "inspect",   "See driver, subnet, attached containers.")
cmd_row(3.75, "connect",   "Attach an existing container to a network.")
cmd_row(4.30, "disconnect","Detach a container from a network.")
cmd_row(4.85, "rm",        "Remove an unused network.")

add_rich_text(s, Inches(0.55), Inches(5.60), Inches(6.0), Inches(0.6),
              [[("All prefixed by ",
                 {"size": 11, "color": MUTED, "italic": True}),
                ("docker network ",
                 {"size": 11, "font": FONT_MONO, "bold": True, "color": SLATE}),
                ("— e.g. ",
                 {"size": 11, "color": MUTED, "italic": True}),
                ("docker network create …",
                 {"size": 11, "font": FONT_MONO, "color": SLATE})]])

# Right: terminal mockup
terminal(s, Inches(7.0), Inches(1.40), Inches(5.8), Inches(4.95),
         "bash — docker",
         [[("# list what already exists", TERM_GRN)],
          [("$ docker network ls", TERM_CYAN)],
          [("NETWORK ID     NAME       DRIVER", TERM_GRAY)],
          [("6bde79dfcf70   bridge     bridge", TERM_GRAY)],
          [("8d9c78725538   none       null", TERM_GRAY)],
          [("eb0eeab782f4   host       host", TERM_GRAY)],
          [],
          [("# create a user-defined bridge", TERM_GRN)],
          [("$ docker network create \\", TERM_CYAN)],
          [("    --driver bridge \\", TERM_CYAN)],
          [("    --subnet 172.20.0.0/16 \\", TERM_CYAN)],
          [("    app-net", TERM_CYAN)],
          [],
          [("# attach a container at start", TERM_GRN)],
          [("$ docker run -d \\", TERM_CYAN)],
          [("    --network app-net \\", TERM_CYAN)],
          [("    --name web nginx", TERM_CYAN)],
          [],
          [("# see what's inside", TERM_GRN)],
          [("$ docker network inspect app-net", TERM_CYAN)]],
         font_size=10)

whale_and_footer(s, 5, TOTAL)


# ============================================================
# SLIDE 6 - Service discovery in a custom network
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "Service discovery: containers find each other by name")

# Left: explanation
add_text(s, Inches(0.55), Inches(1.40), Inches(6.0), Inches(0.5),
         "User-defined networks have built-in DNS.",
         size=16, bold=True, color=SLATE)
add_text(s, Inches(0.55), Inches(2.05), Inches(6.0), Inches(2.2),
         "Put two containers on the same user-defined network and each one "
         "can resolve the other by container name. No IPs, no /etc/hosts, "
         "no orchestrator required.",
         size=13, color=BODY, line_spacing=1.4)

# Gotcha box
add_rect(s, Inches(0.55), Inches(4.05), Inches(6.0), Inches(1.50), CARD_BG)
add_rect(s, Inches(0.55), Inches(4.05), Inches(0.10), Inches(1.50), ALERT_RED)
add_text(s, Inches(0.80), Inches(4.15), Inches(5.65), Inches(0.4),
         "Gotcha", size=12, bold=True, color=ALERT_RED)
add_rich_text(s, Inches(0.80), Inches(4.50), Inches(5.65), Inches(1.0),
              [[("The ", {"size": 12, "color": BODY}),
                ("default ", {"size": 12, "color": BODY, "italic": True}),
                ("bridge network does NOT do this. Name-based DNS only works "
                 "on networks ", {"size": 12, "color": BODY}),
                ("you create yourself", {"size": 12, "color": SLATE, "bold": True}),
                (". Always create one before linking apps.",
                 {"size": 12, "color": BODY})]],
              line_spacing=1.35)

# Right: terminal
terminal(s, Inches(7.0), Inches(1.40), Inches(5.8), Inches(4.95),
         "bash — docker",
         [[("# 1. make a network for the app", TERM_GRN)],
          [("$ docker network create app-net", TERM_CYAN)],
          [],
          [("# 2. start redis on it", TERM_GRN)],
          [("$ docker run -d \\", TERM_CYAN)],
          [("    --network app-net \\", TERM_CYAN)],
          [("    --name redis redis:7", TERM_CYAN)],
          [],
          [("# 3. start a web app on the same network", TERM_GRN)],
          [("# point it at redis BY NAME", TERM_GRN)],
          [("$ docker run -d \\", TERM_CYAN)],
          [("    --network app-net \\", TERM_CYAN)],
          [("    --name web -p 8080:80 \\", TERM_CYAN)],
          [("    -e REDIS_HOST=redis \\", TERM_CYAN)],
          [("    myapp:1.0", TERM_CYAN)],
          [],
          [("# 4. prove DNS works", TERM_GRN)],
          [("$ docker run --rm --network app-net \\", TERM_CYAN)],
          [("    alpine nslookup redis", TERM_CYAN)],
          [("Name:   redis", TERM_GRAY)],
          [("Address: 172.20.0.2", TERM_GRAY)]],
         font_size=9.5)

whale_and_footer(s, 6, TOTAL)


# ============================================================
# SLIDE 7 - CNM vs CNI
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "Two models: Docker (CNM) vs Kubernetes (CNI)")

add_text(s, Inches(0.55), Inches(1.15), Inches(12.2), Inches(0.5),
         "Same goal — connect containers — different philosophies.",
         size=14, italic=True, color=MUTED)

def model_card(x, color, head, sub, rows):
    add_rect(s, x, Inches(1.80), Inches(5.9), Inches(0.65), color)
    add_text(s, x, Inches(1.80), Inches(5.9), Inches(0.65), head,
             size=16, bold=True, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_rect(s, x, Inches(2.45), Inches(5.9), Inches(0.50), SLATE)
    add_text(s, x, Inches(2.45), Inches(5.9), Inches(0.50), sub,
             size=11.5, color=WHITE, italic=True,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_rect(s, x, Inches(2.95), Inches(5.9), Inches(3.25), CARD_BG)
    for i, (label, body) in enumerate(rows):
        ry = 3.15 + i * 0.75
        add_text(s, x + Inches(0.25), Inches(ry), Inches(5.5), Inches(0.3),
                 label, size=12, bold=True, color=SLATE)
        add_text(s, x + Inches(0.25), Inches(ry + 0.30), Inches(5.4), Inches(0.45),
                 body, size=11, color=BODY, line_spacing=1.3)

model_card(Inches(0.55), STEPS[0],
           "Docker — CNM", "Container Network Model · driver-based",
           [("Topology", "Many isolated networks per host."),
            ("Service discovery", "Built-in DNS, scoped per network."),
            ("Isolation", "On by default — bridging requires explicit work."),
            ("Plugins", "Drivers via libnetwork (bridge, overlay, macvlan…).")])

model_card(Inches(6.85), STEPS[3],
           "Kubernetes — CNI", "Container Network Interface · plugin-based",
           [("Topology", "Single flat cluster network — every pod reachable."),
            ("Service discovery", "Cluster DNS, scoped per namespace."),
            ("Isolation", "Off by default — needs NetworkPolicy resources."),
            ("Plugins", "Calico, Cilium, Flannel, AWS VPC CNI…")])

whale_and_footer(s, 7, TOTAL)


# ============================================================
# SLIDE 8 - Layers & Copy-on-Write
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "Images are layers; containers add a writable one")

# Left: explanation
add_rich_text(s, Inches(0.55), Inches(1.30), Inches(6.0), Inches(2.0),
              [[("An image is a stack of read-only layers. Each ",
                 {"size": 13, "color": BODY}),
                ("FROM", {"size": 13, "bold": True, "color": BLUE, "font": FONT_MONO}),
                (", ", {"size": 13, "color": BODY}),
                ("RUN", {"size": 13, "bold": True, "color": BLUE, "font": FONT_MONO}),
                (", ", {"size": 13, "color": BODY}),
                ("COPY", {"size": 13, "bold": True, "color": BLUE, "font": FONT_MONO}),
                (", or ", {"size": 13, "color": BODY}),
                ("ADD", {"size": 13, "bold": True, "color": BLUE, "font": FONT_MONO}),
                (" appends one. The container starts with a thin "
                 "writable layer on top.", {"size": 13, "color": BODY})]],
              line_spacing=1.4)

add_text(s, Inches(0.55), Inches(3.20), Inches(6.0), Inches(0.5),
         "Copy-on-Write in three moves",
         size=14, bold=True, color=BLUE)

def step(y, n, head, body):
    d = Inches(0.55)
    add_oval(s, Inches(0.55), Inches(y), d, d, SLATE)
    add_text(s, Inches(0.55), Inches(y), d, d, str(n),
             size=16, bold=True, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(1.30), Inches(y - 0.04), Inches(5.0), Inches(0.3),
             head, size=12.5, bold=True, color=SLATE)
    add_text(s, Inches(1.30), Inches(y + 0.25), Inches(5.0), Inches(0.6),
             body, size=11, color=BODY, line_spacing=1.3)

step(3.85, 1, "Read",  "Pulls from the lowest layer that has the file.")
step(4.75, 2, "Write", "First write copies the file UP into the R/W layer.")
step(5.65, 3, "Delete","Removing the container removes the R/W layer.")

# Right: layer stack
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

rw = add_rect(s, Inches(7.0), Inches(5.05), Inches(5.8), Inches(0.6), WHITE)
rw.line.color.rgb = BLUE
rw.line.width = Pt(1.5)
spPr = rw.line._get_or_add_ln()
spPr.append(etree.fromstring(
    '<a:prstDash val="dash" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>'))
add_text(s, Inches(7.0), Inches(5.05), Inches(5.8), Inches(0.6),
         "Container R/W layer (added when container starts)",
         size=11.5, bold=True, color=BLUE,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

whale_and_footer(s, 8, TOTAL)


# ============================================================
# SLIDE 9 - Ephemeral by default (the problem)
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "Containers are ephemeral by default")

add_text(s, Inches(0.55), Inches(1.40), Inches(5.8), Inches(0.5),
         "The scenario", size=18, bold=True, color=SLATE)
add_rich_text(s, Inches(0.55), Inches(2.05), Inches(5.8), Inches(2.2),
              [[("You run MySQL in a container. A user signs up. "
                 "The row is written to ",
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

add_text(s, Inches(7.0), Inches(1.40), Inches(5.8), Inches(0.5),
         "The fix", size=18, bold=True, color=SLATE)
add_text(s, Inches(7.0), Inches(2.05), Inches(5.8), Inches(0.5),
         "Mount storage from outside the container",
         size=15, bold=True, color=BLUE)
add_text(s, Inches(7.0), Inches(2.55), Inches(5.8), Inches(0.5),
         "Docker gives you three options to keep data alive past container deletion:",
         size=12, color=MUTED, line_spacing=1.35)

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

whale_and_footer(s, 9, TOTAL)


# ============================================================
# SLIDE 10 - Storage comparison table
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "Volume vs bind mount vs tmpfs")

rows = [
    ["",                 "Volume",                                       "Bind mount",                              "tmpfs"],
    ["Location",         "Docker-managed area\n(/var/lib/docker/volumes)", "Any host path you choose",              "Host RAM only"],
    ["Created with",     "docker volume create",                          "docker run -v /host:/ctr",               "--tmpfs /ctr/path"],
    ["Survives delete?", "Yes",                                           "Yes",                                    "No"],
    ["Survives reboot?", "Yes",                                           "Yes",                                    "No"],
    ["Portable hosts?",  "Yes (volume drivers)",                          "No (tied to host path)",                 "No"],
    ["Best for",         "Production data\n(databases, app state)",       "Live-editing source during dev",         "Secrets, caches, scratch"],
]

table_left = Inches(0.55); table_top = Inches(1.4)
table_h = Inches(4.7); n_rows = len(rows)
col_widths = [Inches(2.0), Inches(3.4), Inches(3.4), Inches(3.4)]
row_h = table_h / n_rows

x = table_left
for c, cell in enumerate(rows[0]):
    add_rect(s, x, table_top, col_widths[c], row_h,
             SLATE if c > 0 else WHITE)
    add_text(s, x, table_top, col_widths[c], row_h, cell,
             size=12.5, bold=True,
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

add_rich_text(s, Inches(0.55), Inches(6.30), Inches(12.2), Inches(0.5),
              [[("Rule of thumb: ",
                 {"size": 13, "bold": True, "color": SLATE}),
                ("use volumes in production · use bind mounts while "
                 "developing on your laptop · use tmpfs for secrets you "
                 "never want on disk.",
                 {"size": 13, "italic": True, "color": MUTED})]])

whale_and_footer(s, 10, TOTAL)


# ============================================================
# SLIDE 11 - -v vs --mount
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "Mount syntax: -v vs --mount")

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

whale_and_footer(s, 11, TOTAL)


# ============================================================
# SLIDE 12 - Security: Four pillars
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "Container security — the four pillars")

add_text(s, Inches(0.55), Inches(1.05), Inches(12.2), Inches(0.4),
         "Defence in depth. Skip a layer, and the others have to work harder.",
         size=14, italic=True, color=MUTED)

def pillar(x, y, num, head, risk_label, risk, do_label, do, color):
    # Number circle
    d = Inches(0.75)
    add_oval(s, x, y, d, d, color)
    add_text(s, x, y, d, d, str(num),
             size=22, bold=True, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    # Heading
    add_text(s, x + Inches(1.0), y + Inches(0.0), Inches(4.8), Inches(0.4),
             head, size=15, bold=True, color=SLATE)
    # Risk line
    add_rich_text(s, x + Inches(1.0), y + Inches(0.45), Inches(4.8), Inches(0.4),
                  [[(risk_label + ":  ",
                     {"size": 10.5, "bold": True, "color": ALERT_RED}),
                    (risk, {"size": 10.5, "color": BODY})]],
                  line_spacing=1.3)
    # Do line
    add_rich_text(s, x + Inches(1.0), y + Inches(0.90), Inches(4.8), Inches(0.8),
                  [[(do_label + ":  ",
                     {"size": 10.5, "bold": True, "color": GOAL_GREEN}),
                    (do, {"size": 10.5, "color": BODY})]],
                  line_spacing=1.3)

pillar(Inches(0.55), Inches(1.85), 1, "Image",
       "Risk", "Vulnerable base, malicious package, untrusted publisher.",
       "Do",   "Use slim official bases · scan with Trivy / docker scan · "
               "pin by digest · sign with Cosign.",
       STEPS[0])
pillar(Inches(7.0),  Inches(1.85), 2, "Runtime",
       "Risk", "Container runs as root and escapes to the host.",
       "Do",   "Set USER non-root · --read-only · --cap-drop=ALL · "
               "--security-opt=no-new-privileges.",
       STEPS[1])
pillar(Inches(0.55), Inches(4.30), 3, "Secrets",
       "Risk", "Passwords / API keys baked into images or leaked via env.",
       "Do",   "Never COPY .env · use BuildKit --secret · inject at "
               "runtime via secret manager (Vault, AWS SM).",
       STEPS[2])
pillar(Inches(7.0),  Inches(4.30), 4, "Network",
       "Risk", "Containers reachable from anywhere; daemon socket exposed.",
       "Do",   "User-defined networks · publish only what's needed · "
               "TLS on dockerd · never share /var/run/docker.sock.",
       STEPS[3])

whale_and_footer(s, 12, TOTAL)


# ============================================================
# SLIDE 13 - Key takeaways
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "Key takeaways")

takeaways = [
    ("Networking is a virtual switch.",
     "Default bridge gets you started. User-defined networks unlock "
     "DNS-based service discovery — use them."),
    ("Storage outlives containers only outside them.",
     "Volumes for production, bind mounts for dev, tmpfs for secrets. "
     "Prefer --mount over -v in new code."),
    ("Containers are not VMs.",
     "They share the host kernel. Image, runtime, secrets, and network "
     "all need hardening — defence in depth."),
    ("Docker is one model, not THE model.",
     "Kubernetes uses CNI: a single flat network with NetworkPolicy. "
     "Same problems, different defaults."),
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

whale_and_footer(s, 13, TOTAL)


# ============================================================
# SLIDE 14 - Closing
# ============================================================
s = prs.slides.add_slide(blank)
add_text(s, Inches(0.55), Inches(1.30), Inches(12), Inches(1.0),
         "Questions?", size=54, bold=True, color=BLUE,
         line_spacing=1.0)
add_text(s, Inches(0.55), Inches(2.55), Inches(12), Inches(0.7),
         "See you next week.", size=28, italic=True, color=SLATE)

# Subtle separator
add_line(s, Inches(0.55), Inches(4.30),
         Inches(4.50), Inches(4.30), color=BLUE, width=1.5)

add_text(s, Inches(0.55), Inches(4.55), Inches(12), Inches(0.45),
         "Good luck,", size=16, italic=True, color=MUTED)
add_text(s, Inches(0.55), Inches(5.05), Inches(12), Inches(0.45),
         "Professor Maziar", size=18, bold=True, color=SLATE)
add_text(s, Inches(0.55), Inches(5.85), Inches(12), Inches(0.45),
         "CLO835 · Seneca Polytechnic · ITAS Program",
         size=11, color=MUTED, italic=True)

# Docker logo right side, faded by sitting inside light blue ring
logo_cx = Inches(10.6); logo_cy = Inches(4.0); ring_r = Inches(1.6)
ring = add_oval(s, logo_cx - ring_r, logo_cy - ring_r,
                ring_r * 2, ring_r * 2, WHITE, line=LIGHTBLUE)
ring.line.width = Pt(1.2)
s.shapes.add_picture("docker_logo.jpg",
                     logo_cx - Inches(1.15), logo_cy - Inches(0.9),
                     width=Inches(2.3), height=Inches(1.8))

whale_and_footer(s, 14, TOTAL)


# ===== Save =====
out = "Week3_lab_style.pptx"
prs.save(out)
print(f"wrote {out}")
