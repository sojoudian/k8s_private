"""Week02 — CLO835 Lab02 house design language applied to the Week 2 deck.

Source: week02/Week02.pptx — 27 slides, "Docker Image Management". The source is 4:3,
uses a full-bleed photo cover and photo backgrounds, and carries no whale and no footer.
This builder re-authors it in the exact CLO835 house design, the same way build_week01.py
re-authored Week 1.

Design language is REUSED, NOT COPIED: this module imports build_week12, the proven house
engine, so the palette, the fonts, the chrome, the terminal mockup, the bullet glyphs and
the coordinate guard are the SAME objects, not re-typed constants. The import is guarded,
so it never rebuilds Week12.

Original slide text is preserved VERBATIM (PROMPT.md R1). Typos are kept exactly:
"Container Newtork Namespace", "Push to registery", 'ENTRYPOINT [”sleep”]' with curly
quotes, and the doubled spaces.

Genuine diagrams and screenshots are embedded from week02/assets/ (extracted from the
source, downsampled and quantised: 3.6 MB of media -> 2.1 MB). Command and Dockerfile
blocks become house terminal mockups in Consolas. The slide-18 SmartArt process is
redrawn natively as a six-step house grid.

Content is inline in this file, so the build is reproducible from the repo alone.

Run from a directory that holds whale.png, docker_logo.jpg, Week04/<logo> and
week02/assets/. Sandbox only — the save path is relative to the working directory.
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

VERSION     = "v1"
WEEK_LABEL  = "Week 2"
DECK_TITLE  = "CLO835 – Portable Technologies In Cloud"
DECK_SUB    = "Docker Image Management"
ASSETS      = "week02/assets"
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


def _fit_term(s, x, y, w, ymax, ttl, code, hi=13, lo=8):
    """Content-fit terminal: shrink the font only until the block clears ymax."""
    fs = hi
    while fs > lo and _term_h(_eff_lines(code, w, fs), fs) > (ymax - y):
        fs -= 1
    h = min(ymax - y, _term_h(_eff_lines(code, w, fs), fs))
    auto_term(s, x, y, w, h, ttl, code, font_size=fs)
    return h


# ---------------------------------------------------------------- cover
def render_cover(s, n, total, role="Lecture"):
    """House cover. Week 2 is a Docker week, so the ring holds the Docker logo."""
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
# The Week 2 source slide 3 is a flowchart with 16 tiles and 15 block arrows, exactly
# like Week 1. This local renderer keeps the engine geometry and adds those arrows,
# using MSO_SHAPE arrows (never zero-extent connectors) per PROMPT.md R5, in LIGHTBLUE.
_OL_COLS, _OL_ROWS = 4, 4
_OL_X0, _OL_Y0 = 0.7, 1.75
_OL_TW, _OL_TH = 2.85, 1.02
_OL_GX, _OL_GY = 0.27, 0.28


def _ol_pos(idx):
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
    for idx in range(len(items) - 1):
        r, cc, x, y = _ol_pos(idx)
        r2, cc2, x2, y2 = _ol_pos(idx + 1)
        if r2 == r:
            ay = y + _OL_TH / 2.0 - 0.13
            if cc2 > cc:
                _arrow(s, MSO_SHAPE.RIGHT_ARROW, x + _OL_TW, ay, _OL_GX, 0.26)
            else:
                _arrow(s, MSO_SHAPE.LEFT_ARROW, x - _OL_GX, ay, _OL_GX, 0.26)
        else:
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


# ---------------------------------------------------------------- slide 18 process
def render_process(s, n, total, d):
    """Slide 18: the six-step SmartArt process, redrawn as a house numbered grid."""
    title(s, d["title"])
    steps = d["steps"]
    for i, (label, desc) in enumerate(steps):
        col, row = i % 3, i // 3
        x = 0.60 + col * 4.12
        y = 1.90 + row * 2.42
        dia = 0.66
        add_rounded_rect(s, Inches(x), Inches(y), Inches(3.88), Inches(2.10), CARD_BG,
                         line=RULE_GRAY, line_width=0.75, radius_ratio=0.05)
        add_rect(s, Inches(x), Inches(y + 0.05), Inches(0.12), Inches(2.00),
                 STEPS[i % len(STEPS)])
        add_oval(s, Inches(x + 0.30), Inches(y + 0.22), Inches(dia), Inches(dia),
                 STEPS[i % len(STEPS)])
        add_text(s, Inches(x + 0.30), Inches(y + 0.22), Inches(dia), Inches(dia),
                 str(i + 1), size=18, bold=True, color=WHITE, align=CENTER, anchor=MIDDLE)
        add_text(s, Inches(x + 1.08), Inches(y + 0.28), Inches(2.62), Inches(0.42),
                 label, size=15, bold=True, color=SLATE)
        add_text(s, Inches(x + 0.30), Inches(y + 1.02), Inches(3.40), Inches(0.98),
                 desc, size=11.5, color=BODY, line_spacing=1.20)
    whale_and_footer(s, n, total)


# ---------------------------------------------------------------- title + subtitle + figure
def render_title_sub_fig(s, n, total, d):
    """Slide 19: the source title carries two extra lines set with <a:br/>; keep all three."""
    title(s, d["title"])
    add_text(s, Inches(0.60), Inches(1.58), Inches(5.85), Inches(0.9),
             d["sub"], size=17, italic=True, color=MUTED, line_spacing=1.30)
    embed_fig(s, d["figures"][0]["file"], 6.70, 1.62, 6.10, 4.90)
    whale_and_footer(s, n, total)


# ---------------------------------------------------------------- generic
def render_content(s, n, total, d):
    body = [(b["level"], b["text"]) for b in d.get("body", [])]
    figs = d.get("figures", [])
    code = d.get("code_blocks", [])
    if d.get("title"):
        title(s, d["title"])
    if code and body and figs:
        bullets(s, 1.66, body, x=0.60, w=5.20, size=12.5, line_spacing=1.24, space_after=5)
        ch = _fit_term(s, 6.15, 1.66, 4.55, 4.40, d.get("term_title", "bash"),
                       code[0]["lines"], hi=12, lo=9)
        embed_fig(s, figs[0]["file"], *d.get("fig_box", (11.00, 1.70, 1.80, 1.40)))
    elif code and body:
        bullets(s, 1.66, body, x=0.60, w=6.05,
                size=d.get("bullet_size", 13.5), line_spacing=1.26, space_after=6)
        _fit_term(s, 7.05, 1.66, 5.75, 6.55, d.get("term_title", "bash"), code[0]["lines"],
                  hi=d.get("term_fs", 13), lo=9)
    elif code:
        _fit_term(s, 0.90, 1.66, 11.50, 6.55, d.get("term_title", "bash"), code[0]["lines"],
                  hi=d.get("term_fs", 14), lo=9)
    elif figs and body:
        bullets(s, 1.66, body, x=0.60, w=d.get("bullet_w", 5.85),
                size=d.get("bullet_size", 13.5), line_spacing=1.26, space_after=6)
        box = d.get("fig_box", (6.85, 1.66, 5.95, 4.85))
        embed_fig(s, figs[0]["file"], *box)
        if len(figs) > 1:
            embed_fig(s, figs[1]["file"], *d.get("fig_box2", (6.85, 4.00, 5.95, 2.45)))
    elif len(figs) > 1:
        embed_fig(s, figs[0]["file"], 0.60, 1.66, 5.95, 4.85)
        embed_fig(s, figs[1]["file"], 6.85, 1.66, 5.95, 4.85)
    elif figs:
        embed_fig(s, figs[0]["file"], 1.15, 1.66, 11.00, 4.90)
    elif body:
        sz = d.get("bullet_size", 16 if len(body) <= 6 else 14)
        bullets(s, 1.72, body, x=0.60, w=12.15, size=sz,
                line_spacing=d.get("ls", 1.36), space_after=d.get("sa", 9))
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


_CUSTOM.update({"process": render_process, "title_sub_fig": render_title_sub_fig})


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
# DECK — the 27 source slides, text VERBATIM (PROMPT.md R1).
# Typos are kept: "Newtork", "registery", 'ENTRYPOINT [”sleep”]' (curly quotes),
# "Containers Networking is Simple!", and the doubled spaces.
# ============================================================================

def _b(*items):
    return [{"level": lvl, "text": t} for lvl, t in items]


def _f(*names):
    return [{"file": n} for n in names]


def _c(*lines):
    return [{"lines": list(lines)}]


DECK = [
 # ---- 1 cover ----
 {"n": 1, "slide_type": "cover", "title": DECK_TITLE, "cover_role": "Lecture"},

 # ---- 2 section divider (SmartArt: "Containers" / "Week 2") ----
 {"n": 2, "slide_type": "section_divider", "kicker": "WEEK 2", "title": "Containers"},

 # ---- 3 Course Outline (16 tiles, flowchart) ----
 {"n": 3, "slide_type": "course_outline", "title": "Course Outline",
  "highlight": [1],
  "body": _b(
    (0, "Week 1 : Docker Introduction"),
    (0, "Week 2 : Docker Image Management"),
    (0, "Week 3 : Docker Networking, Storage & Security"),
    (0, "Week 4 : K8s Introduction"),
    (0, "Week 5 :K8s- PODs,  ReplicaSets"),
    (0, "Week 6 : K8s – Services & Deployments"),
    (0, "Week 7 : K8s  –  Volumes"),
    (0, "Study Week"),
    (0, "Week 8 : K8s- K8s- PVs & K8s in AKS"),
    (0, "Week 9 : K8s: Storage classes &  Statefulsets"),
    (0, "Week 10 : K8s-  Configmaps  & Secrets"),
    (0, "Week 11 : Exam & Mock Exam week"),
    (0, "Week 12 : K8s – RBAC and AKS"),
    # the user's Week 01 v4 edits, carried across so the two decks agree
    (0, "Week 13 : Project presentation  - K8s and HPA"),
    (0, "Week 14 : Project presentation - Helm"),
    (0, "Term End"),
  )},

 # ---- 4 Building Docker Image (diagram) ----
 {"n": 4, "slide_type": "content", "title": "Building Docker Image",
  "figures": _f("fig04.png")},

 # ---- 5 Building Docker Image (bullets + the Base/Parent/Custom Dockerfiles) ----
 {"n": 5, "slide_type": "content", "title": "Building Docker Image",
  "bullet_size": 14, "term_title": "bash  —  docker", "term_fs": 11,
  "body": _b(
    (0, "A Dockerfile is a text file of build instructions."),
    (0, "Images build in layers — each FROM stacks on a parent."),
    (0, "Base starts from scratch."),
    (0, "Parent extends a base with extra packages."),
    (0, "Custom Webapp copies app files on top."),
  ),
  "code_blocks": _c(
    "# Dockerfile - debian:buster-slim  (Base)",
    "FROM scratch",
    "ADD rootfs.tar.xz /",
    'CMD ["bash"]',
    "",
    "# Dockerfile - httpd  (Parent)",
    "FROM debian:buster-slim",
    "ENV HTTPD_PREFIX /usr/local/apache2",
    "ENV PATH $HTTPD_PREFIX/bin:$PATH",
    "WORKDIR $HTTPD_PREFIX",
    "<content trimmed>",
    "",
    "# Dockerfile - My Custom Webapp",
    "FROM httpd",
    "COPY index.html htdocs/index.html",
  )},

 # ---- 6 Building Docker Image (same bullets + the layered figure) ----
 {"n": 6, "slide_type": "content", "title": "Building Docker Image",
  "bullet_w": 6.05, "bullet_size": 14,
  "fig_box": (7.05, 1.66, 5.75, 4.85),
  "figures": _f("fig06.png"),
  "body": _b(
    (0, "A Dockerfile is a text file of build instructions."),
    (0, "Images build in layers — each FROM stacks on a parent."),
    (0, "Base starts from scratch."),
    (0, "Parent extends a base with extra packages."),
    (0, "Custom Webapp copies app files on top."),
  )},

 # ---- 7 BASE vs Parent Image (two figures) ----
 {"n": 7, "slide_type": "content", "title": "BASE vs Parent Image",
  "figures": _f("fig07_1.jpg", "fig07_2.jpg")},

 # ---- 8 The EXPOSE instruction ----
 {"n": 8, "slide_type": "content", "title": "The EXPOSE instruction",
  "bullet_w": 6.30, "bullet_size": 14,
  "fig_box": (7.30, 1.70, 5.50, 4.75),
  "figures": _f("fig08.jpg"),
  "body": _b(
    (0, "The EXPOSE instruction tells Docker what ports are to be published in this image."),
    (0, "EXPOSE 8080"),
    (0, "EXPOSE 80 443"),
    (0, "EXPOSE 53/tcp 53/udp"),
    (0, "All ports are private by default."),
    (0, "Declaring a port with EXPOSE is not enough to make it public."),
    (0, "The Dockerfile doesn't control on which port a service gets exposed."),
  )},

 # ---- 9 Exposing ports ----
 {"n": 9, "slide_type": "content", "title": "Exposing ports",
  "bullet_w": 6.30, "bullet_size": 14,
  "fig_box": (7.30, 1.70, 5.50, 4.75),
  "figures": _f("fig09.jpg"),
  "body": _b(
    (0, "When you docker run -p <port> ..., that port becomes public."),
    (0, "(Even if it was not declared with EXPOSE.)"),
    (0, "When you docker run -P ... (without port number), all ports declared with EXPOSE become public."),
    (0, "A public port is reachable from other containers and from outside the host."),
    (0, "A private port is not reachable from outside."),
  )},

 # ---- 10 CMD and ENTRYPOINT (figure) ----
 {"n": 10, "slide_type": "content", "title": "CMD and ENTRYPOINT",
  "figures": _f("fig10.jpg")},

 # ---- 11 Adding CMD to Dockerfile ----
 {"n": 11, "slide_type": "content", "title": "Adding CMD to Dockerfile",
  "bullet_size": 14, "term_title": "Dockerfile", "term_fs": 14,
  "body": _b(
    (0, "CMD defines a default command to run when none is given."),
    (0, "It can appear at any point in the file."),
    (0, "Each CMD will replace and override the previous one."),
    (0, "As a result, while you can have multiple CMD lines, it is useless."),
  ),
  "code_blocks": _c("FROM ubuntu", "RUN apt-get update", "CMD sleep 20")},

 # ---- 12 Adding ENTRYPOINT to the Dockerfile ----
 {"n": 12, "slide_type": "content", "title": "Adding ENTRYPOINT to the Dockerfile",
  "bullet_size": 13.5, "term_title": "Dockerfile", "term_fs": 14,
  "body": _b(
    (0, "Our new Dockerfile will look like this:"),
    (0, "ENTRYPOINT defines a base command (and its parameters) for the container."),
    (0, "The command line arguments are appended to those parameters."),
    (0, "Like CMD, ENTRYPOINT can appear anywhere, and replaces the previous value."),
    (0, "Why did we use JSON syntax for our ENTRYPOINT?"),
  ),
  "code_blocks": _c("FROM ubuntu", "RUN apt-get update", 'ENTRYPOINT [”sleep”]')},

 # ---- 13 CMD vs Entrypoint ----
 {"n": 13, "slide_type": "content", "title": "CMD vs Entrypoint",
  "bullet_w": 6.05, "bullet_size": 14,
  "fig_box": (7.05, 1.66, 5.75, 4.85),
  "figures": _f("fig13.png"),
  "body": _b(
    (0, "The default process invoked by Ubuntu container is bash."),
    (0, "If we specify the command at a runtime, the original CMD instruction is replaced if CMD is used in Dockerfile."),
    (0, "If we specify the command at a runtime, the command line parameter is appended to the ENTRYPOINT instruction in the Dockerfile."),
  )},

 # ---- 14 Using Environment Variables ----
 {"n": 14, "slide_type": "content", "title": "Using Environment Variables",
  "term_title": "bash — mysql",
  "fig_box": (11.05, 1.72, 1.75, 1.35),
  "figures": _f("fig14.jpg"),
  "body": _b(
    (0, "Example of MySQL image on DockerHub"),
    (0, "https://hub.docker.com/_/mysql"),
    (0, "Start a mysql server instance"),
    (0, "Starting a MySQL instance is simple:"),
    (0, "Where:"),
    (1, "some-mysql is the name you want to assign to your container,"),
    (1, "my-secret-pw is the password to be set for the MySQL root user"),
    (1, "tag is the tag specifying the MySQL version you want."),
  ),
  "code_blocks": _c("$ docker run --name some-mysql \\",
                    "      -e MYSQL_ROOT_PASSWORD=my-secret-pw \\",
                    "      -d mysql:tag")},

 # ---- 15 Publishing Docker Images (figure) ----
 {"n": 15, "slide_type": "content", "title": "Publishing Docker Images",
  "figures": _f("fig15.png")},

 # ---- 16 Docker Registry ----
 {"n": 16, "slide_type": "content", "title": "Docker Registry",
  "bullet_size": 17, "ls": 1.55, "sa": 18,
  "body": _b(
    (0, "Docker registries hold images"),
    (0, "These are public or private stores used to upload or download docker images"),
    (0, "It serves a collection of docker images created and shared by you or other docker registry users"),
    (0, "Docker registries are the distribution component of Docker"),
  )},

 # ---- 17 Image Tags and Registry Addresses ----
 {"n": 17, "slide_type": "content", "title": "Image Tags and Registry Addresses",
  "bullet_size": 13, "term_title": "bash — tag and push", "term_fs": 12,
  "body": _b(
    (0, "Docker images tags are like Git tags and branches."),
    (0, "They are like bookmarks pointing at a specific image ID."),
    (0, "Tagging an image doesn't rename an image: it adds another tag."),
    (0, "When pushing an image to a registry, the registry address is in the tag."),
    (0, "Example: registry.example.net:5000/image"),
    (0, "What about Docker Hub images?"),
    (0, "ubuntu is, in fact, library/ubuntu, i.e. index.docker.io/library/ubuntu"),
  ),
  "code_blocks": _c("# Tagging and publishing Docker image",
                    "docker tag <registry>/<user>/<image>:clo835-week2",
                    "docker push <registry>/<user>/<image>:clo835-week2")},

 # ---- 18 Creating a Simple Flask Web Application (SmartArt process) ----
 {"n": 18, "slide_type": "process", "title": "Creating a Simple Flask Web Application",
  "steps": [
    ("Clone",   "Clone application repo: https://github.com/sojoudian/simple-webapp-flask"),
    ("Create",  "Manually create a script that will result in a running application inside vanilla ubuntu containers."),
    ("Convert", "Convert this script to a Dockerfile"),
    ("Build",   "Build the Docker image using Docker file"),
    ("Test",    "Test the application  locally"),
    ("Publish the image", "Push to registery"),
  ]},

 # ---- 19 Container Networking Basics (title carries two <a:br/> lines) ----
 {"n": 19, "slide_type": "title_sub_fig", "title": "Container Networking Basics",
  "sub": "Containers Networking is Simple!\nJust kidding, it's not..",
  "figures": _f("fig19.jpg")},

 # ---- 20 Container Newtork Namespace (source typo kept) ----
 {"n": 20, "slide_type": "content", "title": "Container Newtork Namespace",
  "figures": _f("fig20.png")},

 # ---- 21 Containers Network Drivers ----
 {"n": 21, "slide_type": "content", "title": "Containers Network Drivers",
  "bullet_w": 6.05, "bullet_size": 14,
  "fig_box": (7.05, 1.80, 5.75, 4.55),
  "figures": _f("fig21.png"),
  "body": _b(
    (0, "When we install Docker, it comes with the drivers that support the networks below"),
    (1, "bridge (default)"),
    (1, "null"),
    (1, "host"),
    (0, "New network is created with docker network create"),
    (0, "The network is selected with docker run --net ...."),
    (0, "Each network is managed by a driver."),
  )},

 # ---- 22 The Default Bridge (two figures) ----
 {"n": 22, "slide_type": "content", "title": "The Default Bridge",
  "bullet_w": 6.05, "bullet_size": 12.5,
  "fig_box": (7.05, 1.66, 5.75, 2.35),
  "fig_box2": (7.05, 4.15, 5.75, 2.35),
  "figures": _f("fig22_1.png", "fig22_2.png"),
  "body": _b(
    (0, "By default, the container gets a virtual eth0 interface.(In addition to its own private lo loopback interface.)"),
    (0, "That interface is provided by a veth pair."),
    (0, "It is connected to the Docker bridge.(Named docker0 by default; configurable with --bridge.)"),
    (0, "Addresses are allocated on a private, internal subnet.(Docker uses 172.17.0.0/16 by default; configurable with --bip.)"),
    (0, "The container can have its own routes, iptables rules, etc."),
  )},

 # ---- 23 The Host Driver ----
 {"n": 23, "slide_type": "content", "title": "The Host Driver",
  "bullet_w": 6.05, "bullet_size": 13.5,
  "fig_box": (7.05, 1.70, 5.75, 4.75),
  "figures": _f("fig23.png"),
  "body": _b(
    (0, "Container is started with docker run --net host ..."),
    (0, "It sees (and can access) the network interfaces of the host."),
    (0, "It can bind any address, any port (for ill and for good)."),
    (0, "Network traffic doesn't have to go through NAT, bridge, or veth."),
    (0, "Performance = native!"),
    (0, "Use cases:"),
    (1, "Performance sensitive applications (VOIP, gaming, streaming...)"),
  )},

 # ---- 24 port mapping ----
 {"n": 24, "slide_type": "content",
  "title": 'What is port mapping in Docker?  "docker run –p 80:8080 <image>"',
  "bullet_w": 5.45, "bullet_size": 14,
  "fig_box": (6.45, 1.90, 6.35, 4.45),
  "figures": _f("fig24.png"),
  "body": _b(
    (0, "Port forwarding or, as it's also called, port mapping is just a way to say that data addressed to one socket is redirected to another by an intermediary (for instance, by a network router or a proxy process)."),
  )},

 # ---- 25 Proxy vs Kernel Port Forwarding ----
 {"n": 25, "slide_type": "content", "title": "Proxy vs Kernel Port Forwarding",
  "bullet_w": 5.45, "bullet_size": 14,
  "fig_box": (6.45, 1.75, 6.35, 4.70),
  "figures": _f("fig25.png"),
  "body": _b(
    (0, "There are two common ways to redirect network data (hence, implement port forwarding):"),
    (1, "By sneakily modifying the destination address of packets."),
    (1, "By explicitly putting a proxy between the client and the serv"),
  )},

 # ---- 26 Containers and Port Forwarding ----
 {"n": 26, "slide_type": "content", "title": "Containers and Port Forwarding",
  "bullet_w": 5.45, "bullet_size": 13.5,
  "fig_box": (6.45, 1.95, 6.35, 4.35),
  "figures": _f("fig26.png"),
  "body": _b(
    (0, "docker run --publish 8080:80 nginx command creates a regular port forwarding from the host's 0.0.0.0:8080 to the container's $CONT_IP:80"),
    (0, "in the case of Docker Engine, there is not much difference between port publishing and good old kernel space port forwarding"),
  )},

 # ---- 27 References ----
 {"n": 27, "slide_type": "content", "title": "References",
  "bullet_size": 16, "ls": 1.60, "sa": 16,
  "body": _b(
    (0, "https://iximiuz.com/en/posts/docker-publish-container-ports/"),
    (0, "https://iximiuz.com/en/posts/container-networking-is-simple/"),
  )},
]

_BY_N = {d["n"]: d for d in DECK}


def build_all():
    build_deck(DECK, f"week02/Week02_lecture_style_{VERSION}.pptx")


if __name__ == "__main__":
    # RUN-SAFETY: guarded, so importing this module never writes a deck.
    build_all()
