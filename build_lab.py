"""Week 3 hands-on lab — single integrated exercise covering Networking,
Storage, and Security. Same Lab02 design language as new_Week3.pptx."""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

# === Lab02 palette (verbatim) ===
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

# ===== helpers (same as build_week3.py) =====

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

def whale_and_footer(slide, page_num, total):
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

def goal_panel(slide, y, goal_text):
    add_rect(slide, Inches(0.55), Inches(y), Inches(12.2), Inches(0.55), CARD_BG)
    add_rect(slide, Inches(0.55), Inches(y), Inches(0.10), Inches(0.55), GOAL_GREEN)
    add_rich_text(slide, Inches(0.85), Inches(y), Inches(11.6), Inches(0.55),
                  [[("GOAL   ",
                     {"size": 11.5, "bold": True, "color": GOAL_GREEN,
                      "font": FONT_MONO}),
                    (goal_text, {"size": 12.5, "color": BODY})]],
                  anchor=MSO_ANCHOR.MIDDLE)

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
TOTAL = 8


# ============================================================
# SLIDE 1 - Title
# ============================================================
s = prs.slides.add_slide(blank)
add_text(s, Inches(0.7), Inches(2.0), Inches(12.0), Inches(0.6),
         "Hands-on Lab", size=20, bold=True, color=MUTED, line_spacing=1.0)
add_text(s, Inches(0.7), Inches(2.55), Inches(8.5), Inches(1.4),
         "Networking, Storage\nand Security in one stack",
         size=40, bold=True, color=BLUE, line_spacing=1.05)
add_text(s, Inches(0.7), Inches(4.7), Inches(7.8), Inches(0.5),
         "Build a MySQL + Adminer stack with a user-defined network, "
         "a persistent volume, and a hardened runtime.",
         size=14, italic=True, color=MUTED, line_spacing=1.4)
# Docker logo in light-blue ring
logo_cx = Inches(10.6); logo_cy = Inches(3.75); ring_r = Inches(1.8)
ring = add_oval(s, logo_cx - ring_r, logo_cy - ring_r,
                ring_r * 2, ring_r * 2, WHITE, line=LIGHTBLUE)
ring.line.width = Pt(1.5)
s.shapes.add_picture("docker_logo.jpg",
                     logo_cx - Inches(1.25), logo_cy - Inches(0.98),
                     width=Inches(2.5), height=Inches(1.96))
add_rich_text(s, Inches(0.7), Inches(6.5), Inches(7), Inches(0.7),
              [[("Instructor: ", {"size": 12, "color": MUTED}),
                ("Professor Maziar", {"size": 12, "bold": True, "color": SLATE})],
               [("CLO835 · Week 3 · ~30 minutes",
                 {"size": 10.5, "italic": True, "color": MUTED})]])
s.shapes.add_picture("whale.png", Inches(0.45), Inches(6.85),
                     width=Inches(0.5), height=Inches(0.5))
add_text(s, Inches(9.5), Inches(7.12), Inches(3.35), Inches(0.3),
         f"CLO835, Fall 2026     1 / {TOTAL}",
         size=10, color=FOOTER_GRAY, align=PP_ALIGN.RIGHT)


# ============================================================
# SLIDE 2 - Overview
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "What you'll build")

add_text(s, Inches(0.55), Inches(1.05), Inches(12), Inches(0.4),
         "Three concepts, one stack. Each step lights up one of this "
         "week's pillars.",
         size=14, italic=True, color=MUTED)

# 3 step blocks on left
def step_block(y, color, label, body):
    add_rect(s, Inches(0.55), Inches(y), Inches(1.9), Inches(0.85), color)
    add_text(s, Inches(0.55), Inches(y), Inches(1.9), Inches(0.85), label,
             size=14, bold=True, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(2.65), Inches(y + 0.08), Inches(5.2), Inches(0.75),
             body, size=12, color=BODY, line_spacing=1.35,
             anchor=MSO_ANCHOR.MIDDLE)

step_block(1.85, STEPS[0], "Networking",
           "Create a user-defined network so containers find each other "
           "by name.")
step_block(2.95, STEPS[1], "Storage",
           "Attach a named volume to MySQL so data survives docker rm.")
step_block(4.05, STEPS[3], "Security",
           "Scan the image, run as non-root, drop capabilities, mount "
           "the password as a secret.")
step_block(5.15, STEPS[5], "Verify",
           "Use Adminer to log in, confirm the row survives a restart.")

# Right column: meta info (Lab02-style 3 meta blocks vertically)
def meta_box(y, label, value):
    add_rect(s, Inches(8.45), Inches(y), Inches(1.7), Inches(0.45), BLUE)
    add_text(s, Inches(8.45), Inches(y), Inches(1.7), Inches(0.45), label,
             size=12, bold=True, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_rect(s, Inches(10.15), Inches(y), Inches(2.65), Inches(0.45), CARD_BG)
    add_text(s, Inches(10.30), Inches(y), Inches(2.50), Inches(0.45),
             value, size=11.5, color=BODY,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)

meta_box(1.85, "Time",        "~30 minutes")
meta_box(2.40, "Prereqs",     "Docker installed; bash shell")
meta_box(2.95, "Images",      "mysql:8 · adminer:latest")
meta_box(3.50, "Network",     "user-defined bridge")
meta_box(4.05, "Volume",      "named (mysql-data)")
meta_box(4.60, "Scanner",     "docker scout / trivy")
meta_box(5.15, "Deliverable", "Lab notebook (commands + output)")

whale_and_footer(s, 2, TOTAL)


# ============================================================
# SLIDE 3 - Step 1: Network
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "Step 1 — Create a user-defined network")
goal_panel(s, 1.30,
           "Make a private bridge network so MySQL and Adminer can find each "
           "other by name. The default bridge does NOT do DNS — that's the whole point.")

# Left: terminal
terminal(s, Inches(0.55), Inches(2.05), Inches(7.6), Inches(4.4),
         "bash — docker",
         [[("# 1. create the network", TERM_GRN)],
          [("$ docker network create \\", TERM_CYAN)],
          [("    --driver bridge \\", TERM_CYAN)],
          [("    --subnet 172.28.0.0/16 \\", TERM_CYAN)],
          [("    clo835-net", TERM_CYAN)],
          [("3a7b1e9c8d5f...", TERM_GRAY)],
          [],
          [("# 2. confirm it exists", TERM_GRN)],
          [("$ docker network ls | grep clo835", TERM_CYAN)],
          [("3a7b1e9c8d5f   clo835-net   bridge   local", TERM_GRAY)],
          [],
          [("# 3. inspect — note IPAM range and empty Containers map", TERM_GRN)],
          [("$ docker network inspect clo835-net", TERM_CYAN)],
          [("[ { \"Name\": \"clo835-net\",", TERM_GRAY)],
          [("    \"Driver\": \"bridge\",", TERM_GRAY)],
          [("    \"IPAM\": { \"Config\":", TERM_GRAY)],
          [("        [{ \"Subnet\": \"172.28.0.0/16\" }] },", TERM_GRAY)],
          [("    \"Containers\": {} } ]", TERM_GRAY)]],
         font_size=10.5)

# Right: Expected + Reflect
add_text(s, Inches(8.40), Inches(2.05), Inches(4.4), Inches(0.4),
         "Expected", size=13, bold=True, color=GOAL_GREEN)
add_text(s, Inches(8.40), Inches(2.45), Inches(4.4), Inches(0.8),
         "A bridge network named clo835-net with the subnet you asked for, "
         "and no containers attached yet.",
         size=11.5, color=BODY, line_spacing=1.35)

add_text(s, Inches(8.40), Inches(4.10), Inches(4.4), Inches(0.4),
         "Why a custom bridge?", size=13, bold=True, color=BLUE)
add_rich_text(s, Inches(8.40), Inches(4.50), Inches(4.4), Inches(1.8),
              [[("Only ",
                 {"size": 11, "color": BODY}),
                ("user-defined",
                 {"size": 11, "color": SLATE, "bold": True}),
                (" bridge networks enable name-based DNS resolution. The "
                 "default ",
                 {"size": 11, "color": BODY}),
                ("bridge",
                 {"size": 11, "font": FONT_MONO, "color": SLATE, "bold": True}),
                (" network does not.",
                 {"size": 11, "color": BODY})]],
              line_spacing=1.4)

whale_and_footer(s, 3, TOTAL)


# ============================================================
# SLIDE 4 - Step 2: MySQL with a volume
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "Step 2 — MySQL on the network, backed by a volume")
goal_panel(s, 1.30,
           "Run MySQL on clo835-net with a named volume so the data dir "
           "lives outside the container. Then write one row.")

# Left: terminal
terminal(s, Inches(0.55), Inches(2.05), Inches(7.6), Inches(4.4),
         "bash — docker",
         [[("# 1. create the named volume (explicit is better)", TERM_GRN)],
          [("$ docker volume create mysql-data", TERM_CYAN)],
          [("mysql-data", TERM_GRAY)],
          [],
          [("# 2. start MySQL on the network, with the volume", TERM_GRN)],
          [("$ docker run -d \\", TERM_CYAN)],
          [("    --name mysql-db \\", TERM_CYAN)],
          [("    --network clo835-net \\", TERM_CYAN)],
          [("    -e MYSQL_ROOT_PASSWORD=db_clo835 \\", TERM_CYAN)],
          [("    --mount type=volume,source=mysql-data,target=/var/lib/mysql \\", TERM_CYAN)],
          [("    mysql:8", TERM_CYAN)],
          [],
          [("# 3. seed one row — proof that data lives on the volume", TERM_GRN)],
          [("$ docker exec mysql-db \\", TERM_CYAN)],
          [("    mysql -uroot -pdb_clo835 --table -e \"", TERM_CYAN)],
          [("       CREATE DATABASE foo;", TERM_CYAN)],
          [("       USE foo;", TERM_CYAN)],
          [("       CREATE TABLE pets(name VARCHAR(20));", TERM_CYAN)],
          [("       INSERT INTO pets VALUES('Puffball');", TERM_CYAN)],
          [("       SELECT * FROM pets;\"", TERM_CYAN)]],
         font_size=10)

# Right: Expected
add_text(s, Inches(8.40), Inches(2.05), Inches(4.4), Inches(0.4),
         "Expected", size=13, bold=True, color=GOAL_GREEN)
add_text(s, Inches(8.40), Inches(2.45), Inches(4.4), Inches(0.6),
         "mysql-db running, attached to clo835-net, volume mounted.",
         size=11.5, color=BODY, line_spacing=1.35)

# Mini terminal for verification output
add_rect(s, Inches(8.40), Inches(3.20), Inches(4.4), Inches(1.55), TERMBG)
add_text(s, Inches(8.55), Inches(3.30), Inches(4.20), Inches(1.35),
         "$ docker ps --format \\\n   '{{.Names}}\\t{{.Status}}'\n"
         "mysql-db   Up 12 seconds\n\n$ docker volume ls\nDRIVER  NAME\n"
         "local   mysql-data",
         font=FONT_MONO, size=9.5, color=TERM_GRAY, line_spacing=1.2)

add_text(s, Inches(8.40), Inches(5.00), Inches(4.4), Inches(0.4),
         "Why a volume, not a bind mount?", size=12.5, bold=True, color=BLUE)
add_text(s, Inches(8.40), Inches(5.40), Inches(4.4), Inches(0.8),
         "Named volumes are Docker-managed, portable across hosts, and "
         "the right default for databases.",
         size=11, color=BODY, line_spacing=1.4)

whale_and_footer(s, 4, TOTAL)


# ============================================================
# SLIDE 5 - Step 3: Adminer + service discovery
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "Step 3 — Connect a web UI by container name")
goal_panel(s, 1.30,
           "Start Adminer on the same network and point it at \"mysql-db\" "
           "by name — no IPs. This is service discovery in action.")

# Left: terminal
terminal(s, Inches(0.55), Inches(2.05), Inches(7.6), Inches(4.4),
         "bash — docker",
         [[("# 1. start Adminer on clo835-net, publish port 8080", TERM_GRN)],
          [("$ docker run -d \\", TERM_CYAN)],
          [("    --name adminer \\", TERM_CYAN)],
          [("    --network clo835-net \\", TERM_CYAN)],
          [("    -p 8080:8080 \\", TERM_CYAN)],
          [("    adminer:latest", TERM_CYAN)],
          [],
          [("# 2. prove DNS works from inside the network", TERM_GRN)],
          [("$ docker run --rm \\", TERM_CYAN)],
          [("    --network clo835-net \\", TERM_CYAN)],
          [("    alpine nslookup mysql-db", TERM_CYAN)],
          [("Name:    mysql-db", TERM_GRAY)],
          [("Address: 172.28.0.2", TERM_GRAY)],
          [],
          [("# 3. open the Adminer UI", TERM_GRN)],
          [("# Browser → http://localhost:8080", TERM_GRN)],
          [("#   System:   MySQL", TERM_GRN)],
          [("#   Server:   mysql-db        ← BY NAME, not IP", TERM_GRN)],
          [("#   Username: root", TERM_GRN)],
          [("#   Password: db_clo835", TERM_GRN)]],
         font_size=10.5)

# Right: Expected
add_text(s, Inches(8.40), Inches(2.05), Inches(4.4), Inches(0.4),
         "Expected", size=13, bold=True, color=GOAL_GREEN)
add_text(s, Inches(8.40), Inches(2.45), Inches(4.4), Inches(0.6),
         "Adminer login succeeds. You can browse the foo database and see "
         "the pets table with Puffball.",
         size=11.5, color=BODY, line_spacing=1.35)

# Architecture mini-diagram
add_rect(s, Inches(8.40), Inches(3.55), Inches(4.4), Inches(2.0), CARD_BG, line=BLUE)
add_text(s, Inches(8.55), Inches(3.65), Inches(4.1), Inches(0.3),
         "clo835-net   ·   172.28.0.0/16",
         size=10, bold=True, color=BLUE, font=FONT_MONO)

# Two container boxes
add_rect(s, Inches(8.65), Inches(4.10), Inches(1.65), Inches(0.75), BLUE)
add_text(s, Inches(8.65), Inches(4.10), Inches(1.65), Inches(0.40),
         "adminer", size=11, bold=True, color=WHITE, font=FONT_MONO,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(8.65), Inches(4.45), Inches(1.65), Inches(0.30),
         ":8080", size=9, color=WHITE, font=FONT_MONO,
         align=PP_ALIGN.CENTER)

add_rect(s, Inches(10.90), Inches(4.10), Inches(1.75), Inches(0.75), STEPS[1])
add_text(s, Inches(10.90), Inches(4.10), Inches(1.75), Inches(0.40),
         "mysql-db", size=11, bold=True, color=WHITE, font=FONT_MONO,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(10.90), Inches(4.45), Inches(1.75), Inches(0.30),
         "vol: mysql-data", size=9, color=WHITE, font=FONT_MONO,
         align=PP_ALIGN.CENTER)

add_line(s, Inches(10.30), Inches(4.48), Inches(10.90), Inches(4.48),
         color=BLUE, width=1.5)
add_text(s, Inches(10.30), Inches(4.85), Inches(0.60), Inches(0.25),
         "DNS", size=8, color=BLUE, italic=True, bold=True,
         align=PP_ALIGN.CENTER)

add_text(s, Inches(8.55), Inches(5.05), Inches(4.1), Inches(0.4),
         "Outside → :8080 → adminer → mysql-db",
         size=9.5, color=MUTED, italic=True,
         align=PP_ALIGN.CENTER)

whale_and_footer(s, 5, TOTAL)


# ============================================================
# SLIDE 6 - Step 4: Security hardening
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "Step 4 — Now harden it")
goal_panel(s, 1.30,
           "Apply the four pillars in order: scan the image, restart the "
           "MySQL container as non-root, drop capabilities, and stop "
           "passing the password through an env var.")

# Left: terminal with hardening commands
terminal(s, Inches(0.55), Inches(2.05), Inches(7.6), Inches(4.4),
         "bash — docker",
         [[("# 1. IMAGE — scan for vulnerabilities", TERM_GRN)],
          [("$ docker scout cves mysql:8", TERM_CYAN)],
          [("   (or: trivy image mysql:8)", TERM_GRAY)],
          [],
          [("# 2. SECRETS — keep the password OFF the command line", TERM_GRN)],
          [("$ echo 'db_clo835' > ./db_password.txt", TERM_CYAN)],
          [("$ chmod 600 ./db_password.txt", TERM_CYAN)],
          [],
          [("# 3. RUNTIME — restart MySQL hardened (bind mount now)", TERM_GRN)],
          [("$ docker rm -f mysql-db", TERM_CYAN)],
          [("$ mkdir -p $PWD/mysql-data", TERM_CYAN)],
          [("$ docker run -d \\", TERM_CYAN)],
          [("    --name mysql-db \\", TERM_CYAN)],
          [("    --network clo835-net \\", TERM_CYAN)],
          [("    --mount type=bind,source=$PWD/mysql-data,target=/var/lib/mysql \\", TERM_CYAN)],
          [("    --mount type=bind,source=$PWD/db_password.txt,target=/run/secrets/db_password,readonly \\", TERM_CYAN)],
          [("    -e MYSQL_ROOT_PASSWORD_FILE=/run/secrets/db_password \\", TERM_CYAN)],
          [("    --cap-drop=ALL \\", TERM_CYAN)],
          [("    --cap-add=CHOWN \\", TERM_CYAN)],
          [("    --cap-add=SETGID \\", TERM_CYAN)],
          [("    --cap-add=SETUID \\", TERM_CYAN)],
          [("    --cap-add=DAC_OVERRIDE \\", TERM_CYAN)],
          [("    --cap-add=FOWNER \\", TERM_CYAN)],
          [("    --security-opt=no-new-privileges \\", TERM_CYAN)],
          [("    mysql:8", TERM_CYAN)]],
         font_size=9)

# Right: pillar checklist
add_text(s, Inches(8.40), Inches(2.05), Inches(4.4), Inches(0.4),
         "What you just did", size=13, bold=True, color=BLUE)

def pillar_row(y, n, label, body, color):
    d = Inches(0.40)
    add_oval(s, Inches(8.40), Inches(y), d, d, color)
    add_text(s, Inches(8.40), Inches(y), d, d, str(n),
             size=12, bold=True, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(8.95), Inches(y - 0.02), Inches(3.8), Inches(0.3),
             label, size=11.5, bold=True, color=SLATE)
    add_text(s, Inches(8.95), Inches(y + 0.22), Inches(3.8), Inches(0.55),
             body, size=10, color=BODY, line_spacing=1.3)

pillar_row(2.55, 1, "Image",   "Scan with Scout or Trivy before you ship.",
           STEPS[0])
pillar_row(3.40, 2, "Secrets", "Password in a file with 0600, mounted read-only at /run/secrets/.",
           STEPS[2])
pillar_row(4.25, 3, "Runtime", "Drop ALL caps · add back the 5 MySQL needs · no-new-privs.",
           STEPS[1])
pillar_row(5.10, 4, "Network", "Stayed on clo835-net — never published MySQL's 3306 to the host.",
           STEPS[3])

whale_and_footer(s, 6, TOTAL)


# ============================================================
# SLIDE 7 - Verify + Tear down
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "Check what happened to the row — then clean up")
goal_panel(s, 1.30,
           "Run the same SELECT against the hardened container. The "
           "result may surprise you — then tear down every resource "
           "you created.")

# Left: verify terminal (deliberate visible error)
add_text(s, Inches(0.55), Inches(2.05), Inches(6.0), Inches(0.4),
         "Check", size=13, bold=True, color=GOAL_GREEN)
terminal(s, Inches(0.55), Inches(2.45), Inches(6.0), Inches(3.95),
         "bash — check",
         [[("# stack is healthy?", TERM_GRN)],
          [("$ docker ps --filter network=clo835-net", TERM_CYAN)],
          [("NAMES      STATUS         PORTS", TERM_GRAY)],
          [("adminer    Up 2 minutes   :8080->8080", TERM_GRAY)],
          [("mysql-db   Up 30 seconds  3306/tcp", TERM_GRAY)],
          [],
          [("# did the row come back? (no 2>/dev/null —", TERM_GRN)],
          [("# we want to SEE any error)", TERM_GRN)],
          [("$ docker exec mysql-db bash -c \\", TERM_CYAN)],
          [("    'mysql -uroot \\", TERM_CYAN)],
          [("     -p\"$(cat /run/secrets/db_password)\" \\", TERM_CYAN)],
          [("     -e \"USE foo; SELECT * FROM pets;\"'", TERM_CYAN)],
          [("ERROR 1049 (42000): Unknown database 'foo'", TERM_ERR)],
          [],
          [("# Puffball isn't here. Why? (Reflection 5)", TERM_GRN)]],
         font_size=10.5)

# Right: tear down terminal — both volume AND host dir
add_text(s, Inches(6.85), Inches(2.05), Inches(6.0), Inches(0.4),
         "Tear down", size=13, bold=True, color=ALERT_RED)
terminal(s, Inches(6.85), Inches(2.45), Inches(6.0), Inches(4.40),
         "bash — cleanup",
         [[("# stop and remove the containers", TERM_GRN)],
          [("$ docker rm -f mysql-db adminer", TERM_CYAN)],
          [],
          [("# remove the network", TERM_GRN)],
          [("$ docker network rm clo835-net", TERM_CYAN)],
          [],
          [("# remove BOTH storage locations:", TERM_GRN)],
          [("# (1) the volume from Step 2", TERM_GRN)],
          [("$ docker volume rm mysql-data", TERM_CYAN)],
          [("# (2) the host dir from Step 4", TERM_GRN)],
          [("$ rm -rf ./mysql-data", TERM_CYAN)],
          [],
          [("# delete the local secret file", TERM_GRN)],
          [("$ rm ./db_password.txt", TERM_CYAN)],
          [],
          [("# confirm — should all print nothing/'gone'", TERM_GRN)],
          [("$ docker ps -a --filter network=clo835-net", TERM_CYAN)],
          [("$ docker volume ls | grep mysql-data", TERM_CYAN)],
          [("$ ls -d ./mysql-data 2>/dev/null || echo gone", TERM_CYAN)]],
         font_size=10)

whale_and_footer(s, 7, TOTAL)


# ============================================================
# SLIDE 8 - Closing
# ============================================================
s = prs.slides.add_slide(blank)
add_text(s, Inches(0.55), Inches(1.30), Inches(12), Inches(1.0),
         "Submit your lab notebook.", size=44, bold=True, color=BLUE,
         line_spacing=1.0)
add_text(s, Inches(0.55), Inches(2.40), Inches(12), Inches(0.7),
         "Commands you ran, outputs you saw, answers to the reflections below.",
         size=18, italic=True, color=SLATE, line_spacing=1.3)

# 3 reflection prompts
def reflect(y, n, q):
    d = Inches(0.55)
    add_oval(s, Inches(0.55), Inches(y), d, d, SLATE)
    add_text(s, Inches(0.55), Inches(y), d, d, str(n),
             size=16, bold=True, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(1.35), Inches(y + 0.05), Inches(11.0), Inches(0.5),
             q, size=14, color=BODY, line_spacing=1.4)

add_text(s, Inches(0.55), Inches(3.55), Inches(12), Inches(0.4),
         "Reflect", size=14, bold=True, color=BLUE)

reflect(4.00, 1, "What would break if you put MySQL on the default bridge network instead?")
reflect(4.85, 2, "Where is the Puffball row right now — and what command would have migrated it across the volume → bind switch?")
reflect(5.70, 3, "Which of the four security pillars did this lab NOT touch — and how would you add it?")

add_text(s, Inches(0.55), Inches(6.60), Inches(12), Inches(0.4),
         "Good luck — Professor Maziar  ·  CLO835 · Seneca Polytechnic · ITAS Program",
         size=11, italic=True, color=MUTED)

whale_and_footer(s, 8, TOTAL)


# ===== Save =====
out = "Week3_Hands_On_Lab.pptx"
prs.save(out)
print(f"wrote {out}")
