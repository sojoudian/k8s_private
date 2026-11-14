"""Step-by-step Lab 03 guide. Same design language as
Week3_Hands_On_Lab.pptx — Lab02 palette, Calibri/Consolas, terminal
mockups with traffic-light dots, blue title top-left, whale + footer.

Builds Lab03_Guide.pptx; downstream conversion to PDF is done in shell."""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

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

# ===== helpers =====
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
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line is None: shp.line.fill.background()
    else: shp.line.color.rgb = line; shp.line.width = Pt(0.75)
    shp.shadow.inherit = False
    return shp

def add_oval(slide, x, y, w, h, fill, line=None):
    shp = slide.shapes.add_shape(MSO_SHAPE.OVAL, x, y, w, h)
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line is None: shp.line.fill.background()
    else: shp.line.color.rgb = line; shp.line.width = Pt(0.75)
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
    add_text(slide, x, y, w, h, text, size=30, bold=True, color=BLUE,
             line_spacing=1.05)

def goal_panel(slide, y, goal_text, h=Inches(0.55)):
    add_rect(slide, Inches(0.55), Inches(y), Inches(12.2), h, CARD_BG)
    add_rect(slide, Inches(0.55), Inches(y), Inches(0.10), h, GOAL_GREEN)
    add_rich_text(slide, Inches(0.85), Inches(y), Inches(11.6), h,
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
            r = p.add_run(); r.text = " "
            r.font.name = FONT_MONO; r.font.size = Pt(font_size)
            continue
        for text, color in para:
            r = p.add_run(); r.text = text
            r.font.name = FONT_MONO; r.font.size = Pt(font_size)
            r.font.color.rgb = color

def capture_panel(slide, x, y, w, h, title_text, items):
    """A 'What to capture' / 'Expected' style right-column panel."""
    add_text(slide, x, y, w, Inches(0.4), title_text,
             size=13, bold=True, color=BLUE)
    yy = y + Inches(0.40)
    for i, txt in enumerate(items):
        d = Inches(0.20)
        add_oval(slide, x, yy + Inches(0.05), d, d, GOAL_GREEN)
        add_text(slide, x + Inches(0.05), yy + Inches(0.05), d, d, "✓",
                 size=9, bold=True, color=WHITE,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        add_text(slide, x + Inches(0.35), yy, w - Inches(0.35), Inches(0.55),
                 txt, size=11.5, color=BODY, line_spacing=1.35)
        yy += Inches(0.65)


# ===== Setup =====
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank = prs.slide_layouts[6]
TOTAL = 18


# ============================================================
# SLIDE 1 - Title
# ============================================================
s = prs.slides.add_slide(blank)
add_text(s, Inches(0.7), Inches(1.95), Inches(12.0), Inches(0.6),
         "Lab 02 · Catch-up Guide", size=20, bold=True, color=MUTED,
         line_spacing=1.0)
add_text(s, Inches(0.7), Inches(2.50), Inches(8.5), Inches(1.4),
         "A step-by-step\nwalkthrough",
         size=40, bold=True, color=BLUE, line_spacing=1.05)
add_text(s, Inches(0.7), Inches(4.65), Inches(7.8), Inches(0.6),
         "Every command, every expected output, every answer. "
         "If you missed the class, this gets you through the lab "
         "and helps you understand why each step matters.",
         size=14, italic=True, color=MUTED, line_spacing=1.4)
# Docker logo in ring
logo_cx = Inches(10.6); logo_cy = Inches(3.75); ring_r = Inches(1.8)
ring = add_oval(s, logo_cx - ring_r, logo_cy - ring_r,
                ring_r * 2, ring_r * 2, WHITE, line=LIGHTBLUE)
ring.line.width = Pt(1.5)
s.shapes.add_picture("docker_logo.jpg",
                     logo_cx - Inches(1.25), logo_cy - Inches(0.98),
                     width=Inches(2.5), height=Inches(1.96))
add_rich_text(s, Inches(0.7), Inches(6.5), Inches(7), Inches(0.7),
              [[("Author: ", {"size": 12, "color": MUTED}),
                ("Professor Maziar", {"size": 12, "bold": True, "color": SLATE})],
               [("CLO835 · Week 3 · est. 30–45 min hands-on time",
                 {"size": 10.5, "italic": True, "color": MUTED})]])
s.shapes.add_picture("whale.png", Inches(0.45), Inches(6.85),
                     width=Inches(0.5), height=Inches(0.5))
add_text(s, Inches(9.5), Inches(7.12), Inches(3.35), Inches(0.3),
         f"CLO835, Fall 2026     1 / {TOTAL}",
         size=10, color=FOOTER_GRAY, align=PP_ALIGN.RIGHT)


# ============================================================
# SLIDE 2 - What you'll build
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "What you'll build (and submit)")
add_text(s, Inches(0.55), Inches(1.05), Inches(12), Inches(0.4),
         "Five deliverables. Each is one step in the same stack — "
         "MySQL + Adminer wired together with a private network, "
         "persistent data, and runtime hardening.",
         size=14, italic=True, color=MUTED, line_spacing=1.4)

def step_block(y, color, label, body):
    add_rect(s, Inches(0.55), Inches(y), Inches(1.9), Inches(0.85), color)
    add_text(s, Inches(0.55), Inches(y), Inches(1.9), Inches(0.85), label,
             size=14, bold=True, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(2.65), Inches(y + 0.08), Inches(5.0), Inches(0.75),
             body, size=12, color=BODY, line_spacing=1.35,
             anchor=MSO_ANCHOR.MIDDLE)

step_block(1.85, STEPS[0], "Networking",
           "Create clo835-net and confirm the subnet — slides 4.")
step_block(2.95, STEPS[1], "Storage",
           "Run MySQL on the net with a named volume — slides 5–6.")
step_block(4.05, STEPS[3], "Adminer",
           "Service discovery by name + browser login — slides 7–8.")
step_block(5.15, STEPS[5], "Security",
           "Scan, secret file, drop caps, no-new-privs — slides 9–11.")
step_block(6.25, STEPS[2], "Verify",
           "Data survives the restart, then clean tear-down — slides 12–13.")

# Right column: what's in the report
add_rect(s, Inches(8.45), Inches(1.80), Inches(4.4), Inches(5.4), CARD_BG)
add_rect(s, Inches(8.45), Inches(1.80), Inches(0.10), Inches(5.4), BLUE)
add_text(s, Inches(8.70), Inches(1.95), Inches(4.0), Inches(0.4),
         "Your report must include", size=13, bold=True, color=BLUE)
for i, item in enumerate([
    "5 evidence screenshots — one per step",
    "Name label on every screenshot",
    "Detailed explanation of every command",
    "Highlighted command output",
    "Answers to 5 reflection questions",
    "Integrity Pledge signed",
]):
    yy = 2.45 + i * 0.70
    d = Inches(0.22)
    add_oval(s, Inches(8.70), Inches(yy + 0.05), d, d, BLUE)
    add_text(s, Inches(8.75), Inches(yy + 0.05), d, d, str(i+1),
             size=9, bold=True, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(9.10), Inches(yy), Inches(3.6), Inches(0.6),
             item, size=11.5, color=BODY, line_spacing=1.35)

whale_and_footer(s, 2, TOTAL)


# ============================================================
# SLIDE 3 - Before you begin (prereqs)
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "Before you begin")
add_text(s, Inches(0.55), Inches(1.05), Inches(12), Inches(0.4),
         "Five-minute setup. Confirm these before running any docker commands.",
         size=14, italic=True, color=MUTED)

# Left: prereqs checklist
add_text(s, Inches(0.55), Inches(1.65), Inches(6.0), Inches(0.4),
         "What you need", size=14, bold=True, color=SLATE)
def prereq(y, head, body):
    d = Inches(0.45)
    add_oval(s, Inches(0.55), Inches(y), d, d, GOAL_GREEN)
    add_text(s, Inches(0.55), Inches(y), d, d, "✓",
             size=14, bold=True, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(1.20), Inches(y - 0.05), Inches(5.5), Inches(0.3),
             head, size=12.5, bold=True, color=SLATE)
    add_text(s, Inches(1.20), Inches(y + 0.22), Inches(5.5), Inches(0.55),
             body, size=11, color=BODY, line_spacing=1.3)

prereq(2.15, "Docker Engine 24+",
       "Verify with docker --version. Desktop or daemon, doesn't matter.")
prereq(3.05, "A bash-like shell",
       "Terminal.app, iTerm2, Windows Terminal with WSL, Git Bash.")
prereq(3.95, "A web browser",
       "You'll open the Adminer UI at localhost:8080 in step 3.")
prereq(4.85, "A screenshot tool",
       "macOS: Cmd+Shift+4 · Windows: Snipping Tool · Linux: gnome-screenshot.")
prereq(5.75, "Permission to write in your home directory",
       "You'll create one local secret file (db_password.txt).")

# Right: verify terminal
terminal(s, Inches(7.4), Inches(1.85), Inches(5.4), Inches(4.55),
         "bash — verify your setup",
         [[("$ docker --version", TERM_CYAN)],
          [("Docker version 24.0.5, build ced0996", TERM_GRAY)],
          [],
          [("$ docker info | head -5", TERM_CYAN)],
          [("Client: Docker Engine", TERM_GRAY)],
          [(" Version:    24.0.5", TERM_GRAY)],
          [("Server:", TERM_GRAY)],
          [(" Containers: 0", TERM_GRAY)],
          [(" Running:    0", TERM_GRAY)],
          [],
          [("# create a working directory", TERM_GRN)],
          [("$ mkdir -p ~/clo835-lab03 && cd ~/clo835-lab03", TERM_CYAN)],
          [("$ pwd", TERM_CYAN)],
          [("/Users/you/clo835-lab03", TERM_GRAY)],
          [],
          [("# good to go.", TERM_GRN)]],
         font_size=10.5)

whale_and_footer(s, 3, TOTAL)


# ============================================================
# SLIDE 4 - Step 1: Create the network
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "Step 1 — Create the user-defined network")
goal_panel(s, 1.20,
           "Make a private bridge network clo835-net (subnet 172.28.0.0/16) "
           "so MySQL and Adminer can find each other by name.")

terminal(s, Inches(0.55), Inches(1.95), Inches(7.6), Inches(4.50),
         "bash — docker",
         [[("# create the network", TERM_GRN)],
          [("$ docker network create \\", TERM_CYAN)],
          [("    --driver bridge \\", TERM_CYAN)],
          [("    --subnet 172.28.0.0/16 \\", TERM_CYAN)],
          [("    clo835-net", TERM_CYAN)],
          [("3a7b1e9c8d5f...", TERM_GRAY)],
          [],
          [("# inspect to confirm", TERM_GRN)],
          [("$ docker network inspect clo835-net", TERM_CYAN)],
          [("[", TERM_GRAY)],
          [("  {", TERM_GRAY)],
          [("    \"Name\": \"clo835-net\",", TERM_GRAY)],
          [("    \"Driver\": \"bridge\",", TERM_GRAY)],
          [("    \"IPAM\": { \"Config\": [", TERM_GRAY)],
          [("      { \"Subnet\": \"172.28.0.0/16\" } ] },", TERM_GRAY)],
          [("    \"Containers\": {}", TERM_GRAY)],
          [("  }", TERM_GRAY)],
          [("]", TERM_GRAY)]],
         font_size=10)

capture_panel(s, Inches(8.40), Inches(1.95), Inches(4.4), Inches(4.5),
              "Capture for screenshot 1",
              ["Both commands (create + inspect)",
               "IPAM Subnet = 172.28.0.0/16",
               "Containers: {} (empty)",
               "Add your name label",
               "Highlight the Subnet line"])

whale_and_footer(s, 4, TOTAL)


# ============================================================
# SLIDE 5 - Step 2: MySQL with volume
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "Step 2 — Run MySQL on the network, backed by a volume")
goal_panel(s, 1.20,
           "Create a Docker-managed named volume mysql-data, run MySQL "
           "on clo835-net with that volume mounted at /var/lib/mysql, "
           "then verify it's up.")

terminal(s, Inches(0.55), Inches(1.95), Inches(7.6), Inches(4.55),
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
          [("8c4a92ff77ce0d2e7b1...", TERM_GRAY)],
          [],
          [("# 3. confirm it's running + the volume exists", TERM_GRN)],
          [("$ docker ps --format '{{.Names}}\\t{{.Status}}'", TERM_CYAN)],
          [("mysql-db    Up 12 seconds", TERM_GRAY)],
          [("$ docker volume ls", TERM_CYAN)],
          [("DRIVER  NAME", TERM_GRAY)],
          [("local   mysql-data", TERM_GRAY)]],
         font_size=10)

capture_panel(s, Inches(8.40), Inches(1.95), Inches(4.4), Inches(4.5),
              "Capture for screenshot 2 (part 1)",
              ["docker volume create output",
               "Full docker run command (all flags)",
               "docker ps line showing Up status",
               "docker volume ls showing mysql-data",
               "We'll add the row on the next slide"])

whale_and_footer(s, 5, TOTAL)


# ============================================================
# SLIDE 6 - Step 2: Seed + verify
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "Step 2 — Insert a row, prove the data is there")
goal_panel(s, 1.20,
           "Wait for MySQL to finish initialising (~10–15 seconds), then "
           "create a foo database, a pets table, and insert one row.")

terminal(s, Inches(0.55), Inches(1.95), Inches(7.6), Inches(4.55),
         "bash — docker",
         [[("# wait until mysql is ready (you'll see 'ready for connections')", TERM_GRN)],
          [("$ docker logs mysql-db 2>&1 | grep -m1 'ready for connections'", TERM_CYAN)],
          [("[Server] /usr/sbin/mysqld: ready for connections.", TERM_GRAY)],
          [],
          [("# create db + table + row + SELECT — all in one shot", TERM_GRN)],
          [("$ docker exec mysql-db \\", TERM_CYAN)],
          [("    mysql -uroot -pdb_clo835 --table -e \"", TERM_CYAN)],
          [("       CREATE DATABASE foo;", TERM_CYAN)],
          [("       USE foo;", TERM_CYAN)],
          [("       CREATE TABLE pets(name VARCHAR(20));", TERM_CYAN)],
          [("       INSERT INTO pets VALUES('Puffball');", TERM_CYAN)],
          [("       SELECT * FROM pets;\"", TERM_CYAN)],
          [("+----------+", TERM_GRAY)],
          [("| name     |", TERM_GRAY)],
          [("+----------+", TERM_GRAY)],
          [("| Puffball |", TERM_GRAY)],
          [("+----------+", TERM_GRAY)],
          [],
          [("# the row is in the named volume now.", TERM_GRN)],
          [("# (remember: the volume, not a host directory.)", TERM_GRN)]],
         font_size=9.5)

capture_panel(s, Inches(8.40), Inches(1.95), Inches(4.4), Inches(4.5),
              "Capture for screenshot 2 (part 2)",
              ["The full SELECT output table",
               "Puffball must be visible at the bottom",
               "Highlight the row line",
               "Remember: data is in the volume,",
               "not in any folder you can ls."])

whale_and_footer(s, 6, TOTAL)


# ============================================================
# SLIDE 7 - Step 3: Adminer + DNS
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "Step 3 — Start Adminer, then prove DNS works")
goal_panel(s, 1.20,
           "Run Adminer on the same network. Then use a throw-away alpine "
           "container to prove that the name 'mysql-db' resolves to an IP.")

terminal(s, Inches(0.55), Inches(1.95), Inches(7.6), Inches(4.55),
         "bash — docker",
         [[("# 1. start Adminer, publish port 8080 to the host", TERM_GRN)],
          [("$ docker run -d \\", TERM_CYAN)],
          [("    --name adminer \\", TERM_CYAN)],
          [("    --network clo835-net \\", TERM_CYAN)],
          [("    -p 8080:8080 \\", TERM_CYAN)],
          [("    adminer:latest", TERM_CYAN)],
          [],
          [("# 2. prove DNS by resolving mysql-db from inside the network", TERM_GRN)],
          [("$ docker run --rm \\", TERM_CYAN)],
          [("    --network clo835-net \\", TERM_CYAN)],
          [("    alpine nslookup mysql-db", TERM_CYAN)],
          [("Server:   127.0.0.11      ← Docker's embedded DNS", TERM_GRAY)],
          [("Address:  127.0.0.11:53", TERM_GRAY)],
          [],
          [("Name:    mysql-db", TERM_GRAY)],
          [("Address: 172.28.0.2       ← real IP from your subnet", TERM_GRAY)]],
         font_size=10.5)

capture_panel(s, Inches(8.40), Inches(1.95), Inches(4.4), Inches(4.5),
              "Capture for screenshot 3 (part 1)",
              ["docker run command for adminer",
               "nslookup command",
               "Server: 127.0.0.11 (Docker's DNS)",
               "Address: 172.28.0.2 (real IP)",
               "Highlight both lines"])

whale_and_footer(s, 7, TOTAL)


# ============================================================
# SLIDE 8 - Step 3: Browser login
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "Step 3 — Log in via the browser using the container NAME")
goal_panel(s, 1.20,
           "Open the Adminer UI at http://localhost:8080 and log in with "
           "Server = mysql-db (not an IP). Take a browser screenshot.")

# Left: a mock browser window showing the Adminer login form
add_rect(s, Inches(0.55), Inches(1.95), Inches(6.8), Inches(4.55), WHITE, line=SLATE)
# Browser chrome
add_rect(s, Inches(0.55), Inches(1.95), Inches(6.8), Inches(0.40),
         RGBColor(0xEC, 0xEC, 0xEC))
add_oval(s, Inches(0.70), Inches(2.05), Inches(0.13), Inches(0.13), TERM_RED)
add_oval(s, Inches(0.88), Inches(2.05), Inches(0.13), Inches(0.13), TERM_YEL)
add_oval(s, Inches(1.06), Inches(2.05), Inches(0.13), Inches(0.13), TERM_GRN)
add_text(s, Inches(1.40), Inches(2.02), Inches(5.8), Inches(0.32),
         "http://localhost:8080",
         font=FONT_MONO, size=10, color=SLATE,
         anchor=MSO_ANCHOR.MIDDLE)

# Adminer "login form" mock
form_x = Inches(1.20); form_y = Inches(2.65)
add_text(s, form_x, form_y, Inches(5.0), Inches(0.4),
         "Login — Adminer", size=15, bold=True, color=SLATE)

def field(y, label, value, highlight=False):
    add_text(s, form_x, Inches(y), Inches(1.6), Inches(0.32),
             label, size=11.5, color=BODY,
             anchor=MSO_ANCHOR.MIDDLE)
    bg = CARD_BG if highlight else WHITE
    line_color = BLUE if highlight else SLATE
    box = add_rect(s, form_x + Inches(1.7), Inches(y), Inches(3.3),
                   Inches(0.32), bg, line=line_color)
    box.line.width = Pt(1.5 if highlight else 0.5)
    add_text(s, form_x + Inches(1.8), Inches(y), Inches(3.1), Inches(0.32),
             value, font=FONT_MONO, size=11,
             color=BLUE if highlight else SLATE,
             bold=highlight, anchor=MSO_ANCHOR.MIDDLE)

field(3.15, "System",   "MySQL")
field(3.60, "Server",   "mysql-db", highlight=True)
field(4.05, "Username", "root")
field(4.50, "Password", "db_clo835")
field(4.95, "Database", "foo")

# arrow + caption to the highlighted field
add_text(s, form_x + Inches(5.10), Inches(3.55), Inches(2.5), Inches(0.45),
         "← BY NAME, not IP", size=10, italic=True, bold=True, color=BLUE,
         anchor=MSO_ANCHOR.MIDDLE)

# Login button
btn = add_rect(s, form_x + Inches(1.7), Inches(5.45), Inches(1.2),
               Inches(0.35), BLUE)
add_text(s, form_x + Inches(1.7), Inches(5.45), Inches(1.2), Inches(0.35),
         "Login", size=11, bold=True, color=WHITE,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# Right: what to capture
capture_panel(s, Inches(7.65), Inches(1.95), Inches(5.15), Inches(4.5),
              "Capture for screenshot 3 (part 2)",
              ["Browser address bar: localhost:8080",
               "Server field shows mysql-db (NOT 172.28.0.2)",
               "After login, browse to foo → pets",
               "Capture the pets table showing Puffball",
               "Crop to the relevant area, add your name"])

whale_and_footer(s, 8, TOTAL)


# ============================================================
# SLIDE 9 - Step 4: Scan + prepare secret
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "Step 4 — Scan the image, prepare a secret file")
goal_panel(s, 1.20,
           "First two of four security pillars: scan mysql:8 for known CVEs, "
           "then write the password to a file with 0600 permissions.")

terminal(s, Inches(0.55), Inches(1.95), Inches(7.6), Inches(4.55),
         "bash — docker",
         [[("# Pillar 1 — IMAGE: scan for vulnerabilities", TERM_GRN)],
          [("$ docker scout cves mysql:8", TERM_CYAN)],
          [("   ✓ Image stored for indexing", TERM_GRAY)],
          [("   ✓ Indexed 432 packages", TERM_GRAY)],
          [("", TERM_GRAY)],
          [("   ## Overview", TERM_GRAY)],
          [("                    │  Analyzed Image", TERM_GRAY)],
          [("    Target          │  mysql:8", TERM_GRAY)],
          [("    digest          │  d12...", TERM_GRAY)],
          [("    vulnerabilities │  ", TERM_GRAY),
           ("3C 7H 21M 18L", TERM_ORANGE := RGBColor(0xFF,0xBD,0x2E))],
          [],
          [("# (Alternative: trivy image mysql:8)", TERM_GRN)],
          [],
          [("# Pillar 3 — SECRETS: write password to a file, 0600 perms", TERM_GRN)],
          [("$ echo 'db_clo835' > ./db_password.txt", TERM_CYAN)],
          [("$ chmod 600 ./db_password.txt", TERM_CYAN)],
          [("$ ls -l ./db_password.txt", TERM_CYAN)],
          [("-rw-------  1 you  staff  10 Nov 15 14:32 db_password.txt", TERM_GRAY)]],
         font_size=10)

capture_panel(s, Inches(8.40), Inches(1.95), Inches(4.4), Inches(4.5),
              "Capture for screenshot 4 (part 1)",
              ["Scan output showing CVE count",
               "ls -l line: leading -rw-------",
               "(no group/other perms)",
               "File name: db_password.txt",
               "Highlight both pieces"])

whale_and_footer(s, 9, TOTAL)


# ============================================================
# SLIDE 10 - Step 4: Rebuild MySQL hardened
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "Step 4 — Rebuild MySQL with all four pillars active")
goal_panel(s, 1.20,
           "Stop the old MySQL, start a new one with secret-from-file, "
           "cap-drop=ALL + selective adds, and no-new-privileges.")

terminal(s, Inches(0.55), Inches(1.95), Inches(7.6), Inches(4.55),
         "bash — docker",
         [[("# remove the un-hardened container", TERM_GRN)],
          [("# (the volume from Step 2 stays put, untouched)", TERM_GRN)],
          [("$ docker rm -f mysql-db", TERM_CYAN)],
          [("mysql-db", TERM_GRAY)],
          [],
          [("# new mount source: a host dir that doesn't exist yet", TERM_GRN)],
          [("$ mkdir -p $PWD/mysql-data", TERM_CYAN)],
          [],
          [("# restart MySQL — all four pillars at once", TERM_GRN)],
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
          [("    mysql:8", TERM_CYAN)],
          [("b46d26cee73a...", TERM_GRAY)]],
         font_size=8.5)

capture_panel(s, Inches(8.40), Inches(1.95), Inches(4.4), Inches(4.5),
              "What changed vs. step 2",
              ["Mount type SWITCHED: volume → bind mount",
               "Password file mounted at /run/secrets",
               "MYSQL_ROOT_PASSWORD_FILE (not _PASSWORD)",
               "--cap-drop=ALL + 5 selective adds",
               "--security-opt=no-new-privileges"])

whale_and_footer(s, 10, TOTAL)


# ============================================================
# SLIDE 11 - Step 4: Verify hardening
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "Step 4 — Prove the hardening is active")
goal_panel(s, 1.20,
           "Inspect the container's HostConfig to confirm CapDrop, CapAdd, "
           "and SecurityOpt are what you set.")

terminal(s, Inches(0.55), Inches(1.95), Inches(7.6), Inches(4.55),
         "bash — verify",
         [[("# read the security fields from docker inspect", TERM_GRN)],
          [("$ docker inspect mysql-db --format \\", TERM_CYAN)],
          [("    '{{json .HostConfig.CapDrop}} | {{json .HostConfig.CapAdd}}'", TERM_CYAN)],
          [("[\"ALL\"] | [\"CHOWN\",\"SETGID\",\"SETUID\",\"DAC_OVERRIDE\",\"FOWNER\"]", TERM_GRAY)],
          [],
          [("$ docker inspect mysql-db --format \\", TERM_CYAN)],
          [("    '{{json .HostConfig.SecurityOpt}}'", TERM_CYAN)],
          [("[\"no-new-privileges\"]", TERM_GRAY)],
          [],
          [("# bonus: prove the secret file is readonly inside the container", TERM_GRN)],
          [("$ docker exec mysql-db ls -l /run/secrets/db_password", TERM_CYAN)],
          [("-r--------  1 root root  10  Nov 15  /run/secrets/db_password", TERM_GRAY)],
          [],
          [("# bonus: the password is NOT in the process environment", TERM_GRN)],
          [("$ docker exec mysql-db env | grep -i PASSWORD", TERM_CYAN)],
          [("MYSQL_ROOT_PASSWORD_FILE=/run/secrets/db_password", TERM_GRAY)],
          [("# (file PATH only, never the value)", TERM_GRN)]],
         font_size=10)

capture_panel(s, Inches(8.40), Inches(1.95), Inches(4.4), Inches(4.5),
              "Capture for screenshot 4 (part 2)",
              ["CapDrop: [\"ALL\"]",
               "CapAdd: [CHOWN, SETGID, SETUID, DAC_OVERRIDE, FOWNER]",
               "SecurityOpt: [no-new-privileges]",
               "env | grep PASSWORD shows only the PATH",
               "Highlight each of the four lines"])

whale_and_footer(s, 11, TOTAL)


# ============================================================
# SLIDE 12 - Step 5: Verify survival + tear down
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "Step 5 — Check what happened to the row, then tear it down")
goal_panel(s, 1.20,
           "Run the same SELECT against the hardened container. The "
           "result may surprise you — then remove EVERY resource "
           "(both the volume and the host directory).")

add_text(s, Inches(0.55), Inches(1.95), Inches(6.0), Inches(0.4),
         "Check (no error suppression — we want to see it)",
         size=13, bold=True, color=GOAL_GREEN)
terminal(s, Inches(0.55), Inches(2.35), Inches(6.0), Inches(2.30),
         "bash — check",
         [[("$ docker exec mysql-db bash -c \\", TERM_CYAN)],
          [("    'mysql -uroot \\", TERM_CYAN)],
          [("     -p\"$(cat /run/secrets/db_password)\" \\", TERM_CYAN)],
          [("     -e \"USE foo; SELECT * FROM pets;\"'", TERM_CYAN)],
          [("ERROR 1049 (42000): Unknown database 'foo'", TERM_ERR)],
          [],
          [("# Puffball isn't here. Find out why (Reflection 5).", TERM_GRN)]],
         font_size=10.5)

add_text(s, Inches(0.55), Inches(4.85), Inches(6.0), Inches(0.4),
         "Tear down — BOTH storage locations", size=13, bold=True, color=ALERT_RED)
terminal(s, Inches(0.55), Inches(5.25), Inches(6.0), Inches(1.45),
         "bash — cleanup",
         [[("$ docker rm -f mysql-db adminer", TERM_CYAN)],
          [("$ docker network rm clo835-net", TERM_CYAN)],
          [("$ docker volume rm mysql-data   # Step 2 storage", TERM_CYAN)],
          [("$ rm -rf ./mysql-data           # Step 4 storage", TERM_CYAN)],
          [("$ rm ./db_password.txt", TERM_CYAN)]],
         font_size=10.5)

# Right: verify clean
add_text(s, Inches(6.85), Inches(1.95), Inches(6.0), Inches(0.4),
         "Verify nothing was left", size=13, bold=True, color=BLUE)
terminal(s, Inches(6.85), Inches(2.35), Inches(6.0), Inches(4.35),
         "bash — confirm clean",
         [[("# four checks — all should be empty/'gone'", TERM_GRN)],
          [("$ docker ps -a --filter network=clo835-net", TERM_CYAN)],
          [("(no rows)", TERM_GRAY)],
          [],
          [("$ docker network ls | grep clo835", TERM_CYAN)],
          [("(no rows)", TERM_GRAY)],
          [],
          [("$ docker volume ls | grep mysql-data", TERM_CYAN)],
          [("(no rows)", TERM_GRAY)],
          [],
          [("$ ls -d ./mysql-data 2>/dev/null || echo gone", TERM_CYAN)],
          [("gone", TERM_GRAY)],
          [],
          [("$ ls db_password.txt 2>/dev/null || echo gone", TERM_CYAN)],
          [("gone", TERM_GRAY)],
          [],
          [("# clean. submit your report.", TERM_GRN)]],
         font_size=10)

whale_and_footer(s, 12, TOTAL)


# ============================================================
# SLIDES 13–17 — Reflection answers
# ============================================================

def reflection(num, question, answer_paras, evidence_runs=None, evidence_title=None):
    s = prs.slides.add_slide(blank)
    title(s, f"Reflection {num} — answer key")

    # Question card
    add_rect(s, Inches(0.55), Inches(1.20), Inches(12.2), Inches(1.10),
             CARD_BG)
    add_rect(s, Inches(0.55), Inches(1.20), Inches(0.10), Inches(1.10),
             BLUE)
    add_text(s, Inches(0.85), Inches(1.30), Inches(11.6), Inches(0.32),
             "Question", size=11, bold=True, color=BLUE)
    add_text(s, Inches(0.85), Inches(1.60), Inches(11.6), Inches(0.65),
             question, size=12.5, color=SLATE, italic=True,
             line_spacing=1.35)

    # Left: answer — one textbox spanning the available height, paragraphs
    # separated by blank lines (avoids overlap when text is long).
    add_text(s, Inches(0.55), Inches(2.55), Inches(7.0), Inches(0.4),
             "Answer", size=14, bold=True, color=GOAL_GREEN)
    runs = []
    for i, para in enumerate(answer_paras):
        if i > 0:
            runs.append([("", {"size": 6})])   # blank line spacer
        if isinstance(para, str):
            runs.append([(para, {"size": 11.5, "color": BODY})])
        else:
            runs.append(para)
    add_rich_text(s, Inches(0.55), Inches(3.00), Inches(7.0), Inches(4.0),
                  runs, line_spacing=1.4)

    # Right: evidence / terminal proof
    if evidence_runs:
        add_text(s, Inches(7.85), Inches(2.55), Inches(5.0), Inches(0.4),
                 evidence_title or "Proof", size=14, bold=True, color=BLUE)
        terminal(s, Inches(7.85), Inches(2.95), Inches(5.0), Inches(3.55),
                 "bash — example",
                 evidence_runs, font_size=10)

    whale_and_footer(s, 12 + num, TOTAL)


# Reflection 1 — default bridge / DNS
reflection(
    1,
    "Why is the default bridge network not sufficient, and would "
    "docker run --network bridge ... alpine nslookup mysql-db still "
    "resolve the name?",
    [
        "The default bridge network does NOT include Docker's embedded "
        "DNS server. Containers on it can reach each other ONLY by IP. "
        "Name-based discovery is exclusive to user-defined networks.",

        "So the nslookup command would FAIL — alpine would query its "
        "DNS resolver, never reach Docker's embedded DNS, and return "
        "NXDOMAIN for 'mysql-db'. You'd have to hard-code the MySQL "
        "container's IP, which changes every restart.",

        "That's why step 1 of this lab creates clo835-net up front: "
        "everything that follows depends on name resolution.",
    ],
    [[("# on the DEFAULT bridge — fails:", TERM_GRN)],
     [("$ docker run --rm --network bridge \\", TERM_CYAN)],
     [("    alpine nslookup mysql-db", TERM_CYAN)],
     [("** server can't find mysql-db: NXDOMAIN", TERM_ERR)],
     [],
     [("# on clo835-net — works:", TERM_GRN)],
     [("$ docker run --rm --network clo835-net \\", TERM_CYAN)],
     [("    alpine nslookup mysql-db", TERM_CYAN)],
     [("Name:    mysql-db", TERM_GRAY)],
     [("Address: 172.28.0.2", TERM_GRAY)]],
    evidence_title="Side-by-side proof",
)

# Reflection 2 — the lab used BOTH; compare them
reflection(
    2,
    "This lab used a named volume (Step 2) and a bind mount (Step 4). "
    "For each, name one thing it does that the other does not. Then "
    "say which one you'd pick for a real production MySQL — and why.",
    [
        "Named volume — wins on management. Docker picks the on-disk "
        "path, sets ownership for MySQL's uid 999 automatically, and "
        "lets you swap in a volume driver that replicates across "
        "hosts. You also don't need to add DAC_OVERRIDE / FOWNER caps "
        "to make MySQL boot — perms are already right.",

        "Bind mount — wins on visibility and portability with the lab "
        "files. ./mysql-data sits right next to your code; you can ls "
        "it, tar it, version-control sibling configs, and reason "
        "about exactly where every byte lives.",

        "Production: named volume. The security and perms benefits "
        "outweigh the visibility benefit, and volume drivers let you "
        "treat storage as an infrastructure concern rather than a "
        "filesystem concern. Use bind mounts for source code you're "
        "live-editing, not for database state.",
    ],
    [[("# Step 2 — opaque, managed:", TERM_GRN)],
     [("$ docker volume inspect mysql-data \\", TERM_CYAN)],
     [("    | jq '.[0].Mountpoint'", TERM_CYAN)],
     [("\"/var/lib/docker/volumes/", TERM_GRAY)],
     [(" mysql-data/_data\"", TERM_GRAY)],
     [],
     [("# Step 4 — visible, yours to manage:", TERM_GRN)],
     [("$ ls ./mysql-data | head -3", TERM_CYAN)],
     [("auto.cnf", TERM_GRAY)],
     [("binlog.000001", TERM_GRAY)],
     [("ca.pem", TERM_GRAY)]],
    evidence_title="Management vs. visibility",
)

# Reflection 3 — DNS evidence
reflection(
    3,
    "How does service discovery work on a user-defined network, and "
    "what evidence in the nslookup output proves DNS is resolving by "
    "container name (not via /etc/hosts)?",
    [
        "When you create a user-defined network, Docker attaches an "
        "embedded DNS server at 127.0.0.11 to every container on that "
        "network. Each container's /etc/resolv.conf points to it. "
        "Docker registers every running container by name + alias and "
        "keeps that table in sync as containers come and go.",

        "Two pieces of the nslookup output prove DNS — not "
        "/etc/hosts — did the work:",

        ("'Server: 127.0.0.11' tells you a DNS query was sent over the "
         "network to Docker's embedded resolver. /etc/hosts is a "
         "static file; it never shows up as a Server line."),

        "The 'Address' line returns an IP from your /16 subnet "
        "(172.28.0.x), and that IP changes if you recreate the "
        "container. A static /etc/hosts entry could never track that.",
    ],
)

# Reflection 4 — capabilities + no-new-privileges
reflection(
    4,
    "Why is dropping all capabilities and adding back only the "
    "required ones safer than running with the default capability "
    "set, and what specific attack does no-new-privileges prevent?",
    [
        "Docker's default capability set is ~14 Linux caps — many of "
        "which a database doesn't need (NET_ADMIN, NET_RAW, "
        "MKNOD, AUDIT_WRITE…). Every cap is an extra attack surface "
        "if a process is compromised. Least privilege means: drop "
        "everything, then add back the smallest set the workload "
        "actually requires. For MySQL that's chown, setuid, setgid, "
        "dac_override, and fowner — the entrypoint needs them to "
        "initialise /var/lib/mysql.",

        "no-new-privileges blocks the SUID bit. Concretely: if an "
        "attacker gets a shell in the container and tries to escalate "
        "by running a setuid root binary (the classic example is "
        "/usr/bin/su or a vulnerable suid mount helper), the kernel "
        "will simply not honour the setuid bit for that process or "
        "any of its children.",

        "Combined, they collapse the post-exploitation toolkit: the "
        "shell starts with fewer powers AND cannot pick up new ones.",
    ],
    [[("# defaults vs hardened:", TERM_GRN)],
     [],
     [("# DEFAULT", TERM_ERR)],
     [("$ docker inspect <ctr> | \\", TERM_CYAN)],
     [("    jq '.[0].HostConfig.CapAdd'", TERM_CYAN)],
     [("null  ← uses Docker's full default set", TERM_GRAY)],
     [],
     [("# HARDENED", TERM_GRN)],
     [("$ docker inspect mysql-db | \\", TERM_CYAN)],
     [("    jq '.[0].HostConfig.CapAdd'", TERM_CYAN)],
     [("[", TERM_GRAY)],
     [("  \"CHOWN\",", TERM_GRAY)],
     [("  \"SETGID\",", TERM_GRAY)],
     [("  \"SETUID\",", TERM_GRAY)],
     [("  \"DAC_OVERRIDE\",", TERM_GRAY)],
     [("  \"FOWNER\"", TERM_GRAY)],
     [("]", TERM_GRAY)]],
    evidence_title="Five caps vs. fourteen",
)

# Reflection 5 — the migration gotcha
reflection(
    5,
    "Step 7 returned 'Unknown database: foo'. The Puffball row from "
    "Step 2 didn't come back. Where exactly is it now, why couldn't "
    "the new container see it, and what command would have migrated "
    "the data across the volume → bind switch?",
    [
        "Where is Puffball? Still inside the named volume mysql-data, "
        "at /var/lib/docker/volumes/mysql-data/_data on the host. "
        "docker rm tears down the container but does NOT touch "
        "volumes — the data is intact, just unreferenced.",

        "Why didn't the new container see it? Step 4 mounted "
        "$PWD/mysql-data (a brand-new, empty host directory) at "
        "/var/lib/mysql. MySQL saw an empty data dir, ran its "
        "first-time initialiser, and built a fresh, default mysql "
        "system DB. No foo, no pets. Different mount source = "
        "different storage location.",

        "How to migrate? Briefly attach BOTH storage locations to one "
        "throwaway container and copy across. The two-container "
        "alpine + cp trick is one common pattern — there are others "
        "(docker cp out of the volume to a tar file then untar into "
        "the bind dir, or mysqldump in Step 2 and mysql restore "
        "after Step 4). The point: switching mount types is a real "
        "migration, not a free upgrade.",
    ],
    [[("# migrate volume → bind dir in one shot:", TERM_GRN)],
     [("$ docker run --rm \\", TERM_CYAN)],
     [("    -v mysql-data:/from \\", TERM_CYAN)],
     [("    -v $PWD/mysql-data:/to \\", TERM_CYAN)],
     [("    alpine sh -c \\", TERM_CYAN)],
     [("    'cp -a /from/. /to/'", TERM_CYAN)],
     [],
     [("# THEN run Step 4's hardened MySQL,", TERM_GRN)],
     [("# which now sees the migrated data.", TERM_GRN)]],
    evidence_title="The migrate-then-restart trick",
)


# ============================================================
# SLIDE 18 - Your report + Integrity Pledge
# ============================================================
s = prs.slides.add_slide(blank)
title(s, "Your report + Integrity pledge")
add_text(s, Inches(0.55), Inches(1.05), Inches(12), Inches(0.4),
         "Put it all together. One PDF or single document, in this order.",
         size=14, italic=True, color=MUTED)

# Left: report contents checklist
add_text(s, Inches(0.55), Inches(1.60), Inches(6.0), Inches(0.4),
         "What to include", size=14, bold=True, color=BLUE)
items = [
    ("01", "Cover", "Your name, student ID, course, lab number."),
    ("02", "Screenshot 1", "Network create + inspect output."),
    ("03", "Screenshot 2", "MySQL running + volume + Puffball row."),
    ("04", "Screenshot 3", "Adminer browser + nslookup + UI showing the row."),
    ("05", "Screenshot 4", "Image scan + secret file perms + docker inspect."),
    ("06", "Screenshot 5", "SELECT after restart + clean tear-down."),
    ("07", "Answers", "Five reflection answers, in order."),
    ("08", "Integrity Pledge", "Signed and dated."),
]
for i, (n, head, body) in enumerate(items):
    yy = 2.10 + i * 0.55
    d = Inches(0.36)
    add_oval(s, Inches(0.55), Inches(yy + 0.05), d, d, SLATE)
    add_text(s, Inches(0.55), Inches(yy + 0.05), d, d, n,
             size=9, bold=True, color=WHITE, font=FONT_MONO,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(1.05), Inches(yy), Inches(2.0), Inches(0.32),
             head, size=12, bold=True, color=SLATE)
    add_text(s, Inches(3.10), Inches(yy), Inches(3.6), Inches(0.5),
             body, size=11, color=BODY, line_spacing=1.3)

# Right: Integrity Pledge card
add_rect(s, Inches(7.4), Inches(1.60), Inches(5.4), Inches(5.0),
         CARD_BG)
add_rect(s, Inches(7.4), Inches(1.60), Inches(0.10), Inches(5.0),
         SLATE)
add_text(s, Inches(7.65), Inches(1.75), Inches(5.0), Inches(0.4),
         "Integrity Pledge", size=14, bold=True, color=BLUE)
add_text(s, Inches(7.65), Inches(2.25), Inches(5.0), Inches(4.0),
         "By submitting this assignment you affirm that you will not "
         "plagiarize, give or receive illegitimate help on assignments, "
         "papers or examinations. You will uphold fairness and honesty "
         "in your work and the work of others.\n\n"
         "Please read the Seneca Academic Integrity policy for more "
         "details.\n\n"
         "Signed: _____________________________\n\n"
         "Date:   _____________________________",
         size=11.5, color=BODY, line_spacing=1.5)

whale_and_footer(s, 18, TOTAL)


# ===== Save =====
out = "Lab03_Guide.pptx"
prs.save(out)
print(f"wrote {out}")
