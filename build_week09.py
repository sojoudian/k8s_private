"""Week09 — Lab02/Week05 design language applied to Week09.pptx.

Source: Week09/Week09.pptx — 57 slides, "PV, PVC, StorageClass and StatefulSets".
Original slide text preserved verbatim (no rephrasing). Same house treatment as
Week 6/7/8: bullets → blue title + multi-level bullets; shell/YAML → dark terminal
mockups; AWS/native diagrams → embedded originals (native-shape diagrams cropped
from the source render into Week09/assets/); Course Outline redrawn in palette;
workshop boundaries → LAB dividers.

Emits TWO decks from one set of per-slide functions (mirrors Week 8), with key
THEORY slides duplicated into the lab so it is self-contained:
  • Week09_lecture_style_v4.pptx — concepts (hostPath, PV/PVC/StorageClass, StatefulSets)
  • Week09_lab_style_v2.pptx     — Workshops 1/2/3, with recap theory duplicated in

v3 adopts the user's hand edits made in Week09_lecture_style_v2.pptx (2026-07-06):
deck renumbered to Week 10 (outline shifts +1 from EKS onward, Exam = Week 11);
sl05 image enlarged bottom-right; sl08 bullets widened to the left edge; sl22
retitled "How a PVC Binds to a PV"; PVC slides sl24/sl23 swapped (manifests before
pod usage); "Why StatefulSEts?" typo fixed and split into title slide + full-size
diagram slide (sl35 / sl35b).
"""

import os
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

CENTER, LEFT, RIGHT = PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.RIGHT
MIDDLE, TOP = MSO_ANCHOR.MIDDLE, MSO_ANCHOR.TOP

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
ASSETS_DIR = "Week09/assets"
LECTURE_VERSION = "v4"
LAB_VERSION     = "v2"

ASPECT = {}
for _fn in os.listdir(ASSETS_DIR):
    if _fn.lower().endswith((".png", ".jpg", ".jpeg")):
        try:
            ASPECT[_fn] = Image.open(os.path.join(ASSETS_DIR, _fn)).size
        except Exception:
            pass


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


def diagram_right(s, fname, box=(6.9, 1.6, 6.0, 4.95)):
    embed(s, fname, *box)


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
        p.line_spacing = 1.12
        if not para:
            r = p.add_run(); r.text = " "
            r.font.name = FONT_MONO; r.font.size = Pt(font_size)
            continue
        for text, color in para:
            r = p.add_run(); r.text = text
            r.font.name = FONT_MONO; r.font.size = Pt(font_size); r.font.color.rgb = color


_CMD_STARTS = ("$", "k ", "kubectl", "aws", "eksctl", "export", "curl", "rm",
               "vi ", "cat", "sudo", "/usr", "/ #", "ssh", "scp", "echo",
               "apk", "pkill", "unset", "helm", ">")


def _role(line):
    if line == "":
        return None
    st = line.lstrip()
    if st.startswith("#"):
        return TERM_GRN
    if "ERROR" in line or "error" in st[:6] or st.lower().startswith("fail"):
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


def yaml_terminal(s, x, y, w, h, title_text, lines, *, font_size=11):
    TOPKEYS = ("apiVersion", "kind", "metadata", "spec", "provisioner", "parameters")
    runs = []
    for ln in lines:
        if ln == "":
            runs.append([]); continue
        stripped = ln.lstrip()
        color = TERM_CYAN if (ln == stripped and any(stripped.startswith(k) for k in TOPKEYS)) else TERM_GRAY
        if stripped.startswith("#"):
            color = TERM_GRN
        runs.append([(ln, color)])
    terminal(s, Inches(x), Inches(y), Inches(w), Inches(h), title_text, runs, font_size=font_size)


def divider(s, kicker, text, subtitle=None):
    d = Inches(1.6); cx = Inches(13.333 / 2) - d / 2
    add_oval(s, cx, Inches(1.85), d, d, SLATE)
    add_text(s, cx, Inches(2.35), d, Inches(0.6), kicker,
             size=20, bold=True, color=WHITE, align=CENTER, anchor=MIDDLE)
    add_text(s, Inches(1.0), Inches(3.95), Inches(11.33), Inches(1.0), text,
             size=30, bold=True, color=SLATE, align=CENTER, line_spacing=1.05)
    if subtitle:
        add_text(s, Inches(1.0), Inches(5.05), Inches(11.33), Inches(0.6), subtitle,
                 size=15, italic=True, color=MUTED, align=CENTER)


def section(s, text):
    add_text(s, Inches(1.0), Inches(2.95), Inches(11.33), Inches(1.4), text,
             size=40, bold=True, color=SLATE, align=CENTER, anchor=MIDDLE, line_spacing=1.05)
    add_rect(s, Inches(13.333 / 2 - 1.2), Inches(4.55), Inches(2.4), Inches(0.06), BLUE)


def closing(s, text):
    add_oval(s, Inches(13.333 / 2) - Inches(0.8), Inches(2.2), Inches(1.6), Inches(1.6),
             WHITE, line=LIGHTBLUE, line_width=1.5)
    s.shapes.add_picture(K8S_LOGO, Inches(13.333 / 2) - Inches(0.6), Inches(2.4),
                         width=Inches(1.2), height=Inches(1.2))
    add_text(s, Inches(1.0), Inches(4.25), Inches(11.33), Inches(1.0), text,
             size=34, bold=True, color=BLUE, align=CENTER, line_spacing=1.05)


_OUTLINE = [
    "Week 1: Docker Introduction", "Week 2: Docker Image Management",
    "Week 3: Docker Networking, Storage & Security", "Week 4: K8s Introduction",
    "Week 5: K8s- PODs, ReplicaSets", "Week 6: K8s – Services & Deployments",
    "Week 7: K8s – Volumes", "Study Week",
    "Week 9: K8s- K8s- PVs & K8s in AKS", "Week 10: K8s: Storage classes & Statefulsets",
    "Week 11: Exam & Mock Exam week", "Week 12: K8s- Configmaps & Secrets",
    "Week 13: K8s – RBAC and AKS", "Week 14: K8s – HPA",
    "Week 15: Helm Charts & Deployment Automation", "Term End",
]


def course_outline(s, current_idx=9, highlights=None):
    highlights = highlights if highlights is not None else {current_idx: BLUE, 10: EXAM_RED}
    cols = 4
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
# Per-slide content functions (draw content + footer for page n / total)
# ============================================================================

def sl01(s, n, total, track):
    add_text(s, Inches(0.7), Inches(2.55), Inches(8.8), Inches(1.7),
             "PV, PVC, StorageClass\nand StatefulSets", size=38, bold=True, color=BLUE, line_spacing=1.12)
    add_text(s, Inches(0.7), Inches(4.55), Inches(8.5), Inches(0.6),
             f"Week 10 · {track}", size=22, color=SLATE)
    lcx = Inches(10.7); lcy = Inches(3.55); rr = Inches(1.8)
    add_oval(s, lcx - rr, lcy - rr, rr * 2, rr * 2, WHITE, line=LIGHTBLUE, line_width=1.5)
    s.shapes.add_picture(K8S_LOGO, lcx - Inches(1.25), lcy - Inches(1.25), width=Inches(2.5), height=Inches(2.5))
    s.shapes.add_picture(WHALE, Inches(0.45), Inches(6.85), width=Inches(0.5), height=Inches(0.5))
    add_text(s, Inches(9.5), Inches(7.12), Inches(3.35), Inches(0.3),
             f"CLO835, Fall 2026     {n} / {total}", size=10, color=FOOTER_GRAY, align=RIGHT)


def sl02(s, n, total):
    title(s, "Agenda")
    bullets(s, 1.7, [
        (0, "Kubernetes Volumes – hostPath"), (0, "PersistentVolume"),
        (0, "PersistentVolumeClaim"), (0, "StorageClass"), (0, "StatefulSet"),
    ], x=0.7, w=11.5, size=18, line_spacing=1.7)
    whale_and_footer(s, n, total)


def sl03(s, n, total):
    title(s, "Course Outline")
    course_outline(s, current_idx=9)
    whale_and_footer(s, n, total)


def sl04(s, n, total):
    title(s, "Volumes: hostPath")
    bullets(s, 1.55, [
        (0, "First persistent storage – not deleted when the pod is deleted"),
        (0, "hostPath should not be used to store application's data"),
        (0, "Used by pods to get access to host data, e.g. kubeconfig or /var/log or OS devices through file system"),
        (0, "Used as a persistent volume in simulated clusters like \"kind\" and \"minikube\""),
        (0, "Stored on a specific node – is it suitable for DB storage?"),
        (0, "What if we need to persist data in a cluster with multiple worker nodes?"),
    ], x=0.7, w=11.9, size=15, line_spacing=1.5)
    whale_and_footer(s, n, total)


def sl05(s, n, total):
    title(s, "hostPath Concerns")
    bullets(s, 1.7, [
        (0, "HostPaths can expose privileged system credentials"),
        (0, "Pods with identical configuration (such as created from a PodTemplate) may behave differently on different nodes due to different files on the nodes"),
        (0, "The files or directories created on the underlying hosts are only writable by root"),
    ], x=0.7, w=7.4, size=15, line_spacing=1.5)
    embed(s, "s05_1.jpg", 7.03, 4.93, 6.17, 2.02)
    whale_and_footer(s, n, total)


def sl06(s, n, total):
    title(s, "Data Sharing between the node and the Pod's containers with hostPath volume", size=20)
    embed(s, "fig_s06.png", 1.6, 1.7, 10.1, 4.7)
    whale_and_footer(s, n, total)


def sl07(s, n, total):
    title(s, "hostPath Configuration Example")
    yaml_terminal(s, 2.9, 1.55, 7.5, 4.9, "test-pd.yaml", [
        "apiVersion: v1", "kind: Pod", "metadata:", "  name: test-pd", "spec:",
        "  containers:", "  - image: k8s.gcr.io/test-webserver", "    name: test-container",
        "    volumeMounts:", "    - mountPath: /test-pd", "      name: test-volume",
        "  volumes:", "  - name: test-volume", "    hostPath:",
        "      # directory location on host", "      path: /data",
        "      # this field is optional", "      type: Directory",
    ], font_size=12)
    whale_and_footer(s, n, total)


def sl08(s, n, total):
    title(s, "Persistent Volumes: Amazon EBS")
    bullets(s, 1.6, [
        (0, "Using a persistent volume requires:"),
        (1, "creating the volume out-of-band (outside of the Kubernetes API)"),
        (1, "referencing the volume in the pod description, with all its parameters"),
    ], x=0.01, w=5.84, size=14, line_spacing=1.5)
    yaml_terminal(s, 5.85, 1.5, 6.95, 5.0, "pod-using-my-ebs-volume.yaml", [
        "apiVersion: v1", "kind: Pod", "metadata:", "  name: pod-using-my-ebs-volume",
        "spec:", "  containers:", "  - image: ...", "    name: container-using-my-ebs-volume",
        "    volumeMounts:", "    - mountPath: /my-ebs", "      name: my-ebs-volume",
        "  volumes:", "  - name: my-ebs-volume", "    awsElasticBlockStore:",
        "      volumeID: vol-049df61146c4d7901", "      fsType: ext4",
    ], font_size=11)
    whale_and_footer(s, n, total)


def sl09(s, n, total):
    title(s, "Using NFS Volume")
    yaml_terminal(s, 3.3, 1.6, 8.7, 4.85, "pod-using-my-nfs-volume.yaml", [
        "apiVersion: v1", "kind: Pod", "metadata:", "  name: pod-using-my-nfs-volume",
        "spec:", "  containers:", "  - image: ...", "    name: container-using-my-nfs-volume",
        "    volumeMounts:", "    - mountPath: /my-nfs", "      name: my-nfs-volume",
        "  volumes:", "  - name: my-nfs-volume", "    nfs:",
        "      server: 192.168.0.55", "      path: \"/exports/assets\"",
    ], font_size=12)
    whale_and_footer(s, n, total)


def sl10(s, n, total):
    title(s, "Challenge of Volumes")
    bullets(s, 2.0, [
        (0, "Should be pre-deployed"),
        (0, "Requires the app developer to know the infrastructure details"),
        (0, "Locks pod definition to a specific cluster"),
    ], x=0.9, w=11.4, size=18, line_spacing=1.9)
    whale_and_footer(s, n, total)


def sl11(s, n, total):
    divider(s, "WORK\nSHOP 1", "Exploring hostPath")
    whale_and_footer(s, n, total)


def sl12(s, n, total):
    title(s, "Deploy MongoDB to Amazon EKS")
    auto_term(s, 0.7, 1.55, 11.9, 4.85, "bash — deploy mongodb", [
        "# Verify the cluster is running",
        "$ k get nodes",
        "# Create Amazon EKS cluster if there is no active cluster",
        "$ eksctl create cluster –f eks_config.yaml",
        "# Make sure the cluster is running",
        "$ k get nodes",
        "# Create the namespace",
        "$ k create ns  week9",
        "# Deploy mongodb app backed by the hostpath",
        "$k apply -f mongodb_hostpath.yaml -n week9",
    ], font_size=13)
    whale_and_footer(s, n, total)


def sl13(s, n, total):
    title(s, "Add Sample Data to MongoDB")
    auto_term(s, 0.55, 1.5, 12.25, 4.95, "bash — mongosh", [
        "# Start mongo shell in the mongo cotainer",
        "$ k exec -it mongodb -n week9 -- mongosh # mongo client was replaced with mongosh",
        "# Add sample json document to the DB",
        "> use mystore", "switched to db mystore",
        "> db.foo.insertOne({name:'foo'})", 'WriteResult({ "nInserted" : 1 })',
        "> db.foo.find()",
        '{ "_id" : ObjectId("57a61eb9de0cfd512374cc75"), "name" : "foo" }',
        "# Exit the container and mongoDB shell", "> exit", "Bye",
        "# Examine the node that the pod is scheduled to",
        "$ k get pods -o wide -n week9",
        "NAME      READY   STATUS    RESTARTS   AGE   IP               NODE",
        "mongodb   1/1     Running   0          13m   192.168.53.113   ip-192-168-40-207",
    ], font_size=10.5)
    whale_and_footer(s, n, total)


def sl14(s, n, total):
    title(s, "Add Sample Data to MongoDB")
    auto_term(s, 0.55, 1.5, 12.25, 4.95, "bash — mongosh", [
        "# Delete the pod and create a new one", "kubectl delete pod mongodb -n week9",
        "# Recreate the mongoDB pod", "$ k apply -f mongodb_hostpath.yaml -n week9",
        "# Let's examine the data – it turns out to be hit and miss. Why?",
        "$ k exec -it mongodb -n week9 --  mongosh", "> use mystore", "switched to db mystore",
        "> db.foo.find() # data persisted. What if the pod is scheduled to a different node?",
        '{ "_id" : ObjectId("62c5b2586a2dbca9f32d3213"), "name" : "foo" }',
        "# Examnine the node that the pod is scheduled to", "$ k get pods -n week9 -o wide",
        "NAME      READY   STATUS    RESTARTS   AGE     IP               NODE",
        "mongodb   1/1     Running   0          5m42s   192.168.53.113   ip-192-168-40-207",
    ], font_size=10.5)
    whale_and_footer(s, n, total)


def sl15(s, n, total):
    title(s, "HostPath with Amazon EBS")
    auto_term(s, 0.7, 1.7, 11.9, 4.3, "bash — ebs", [
        "# Provision Amazon EBS volume",
        "$ aws ec2 create-volume  --volume-type gp2  --size 80     --availability-zone us-east-1a",
        "# Update the mongodb_aws.yaml with the value of the volume just created",
        "$ k apply -f mongodb_aws.yaml -n week9",
        "# Using it is hit and miss – what if the pod is not assigned to the node in the AZ",
        "# of our Amazon EBS volume",
        "# There should be a better way!",
    ], font_size=12)
    whale_and_footer(s, n, total)


def sl16(s, n, total):
    title(s, "Why to have hostPath at all – Examine kube-proxy")
    auto_term(s, 0.55, 1.7, 6.7, 4.2, "bash — kube-proxy", [
        "# System pods are using hostPath extensively",
        "$ k get all –n kube-proxy",
        "# Select any of the kube-proxy pods, the name",
        "# will be kube-proxy-<random string>",
        "$ k describe pod/kube-proxy-<random string>",
        "    -n kube-system",
    ], font_size=12)
    embed(s, "s16_1.png", 7.5, 2.5, 5.3, 2.6)
    whale_and_footer(s, n, total)


def sl17(s, n, total):
    closing(s, "Workshop 1 -  The End")
    whale_and_footer(s, n, total)


def sl18(s, n, total):
    section(s, "PV, PVC, and StorageClasses")
    whale_and_footer(s, n, total)


def sl19(s, n, total):
    title(s, "Introducing PersistentVolumes and PersistentVolumeClaims", size=22)
    embed(s, "fig_s19.png", 1.2, 1.9, 10.9, 4.4)
    whale_and_footer(s, n, total)


def sl20(s, n, total):
    title(s, "PersistentVolume Manifest")
    yaml_terminal(s, 0.7, 1.5, 6.6, 5.0, "mongodb-pv.yaml", [
        "apiVersion: v1", "kind: PersistentVolume", "metadata:", "  name: mongodb-pv",
        "spec:", "  capacity:", "    storage: 1Gi", "  accessModes:",
        "  - ReadWriteOnce", "  - ReadOnlyMany",
        "  persistentVolumeReclaimPolicy: Retain", "  gcePersistentDisk:",
        "    pdName: mongodb", "    fsType: ext4",
    ], font_size=12)
    add_text(s, Inches(7.7), Inches(1.9), Inches(5.1), Inches(0.5),
             "Defining the PersistentVolume's size, access modes and reclaim policy.",
             size=13, italic=True, color=MUTED, line_spacing=1.2)
    add_text(s, Inches(7.7), Inches(3.0), Inches(5.1), Inches(1.2),
             "It can be mounted by a single client for reading and writing, or by "
             "multiple clients for reading only. After the claim is released, the "
             "PersistentVolume should be retained (not erased or deleted).",
             size=13, color=BODY, line_spacing=1.25)
    whale_and_footer(s, n, total)


def sl21(s, n, total):
    title(s, "Decoupling pods from the underlying storage technology", size=24)
    embed(s, "fig_s21.png", 3.4, 1.6, 6.5, 4.9)
    whale_and_footer(s, n, total)


def sl22(s, n, total):
    title(s, "How a PVC Binds to a PV")
    bullets(s, 1.6, [
        (0, "When an application needs storage, it creates a PersistentVolumeClaim (either directly, or through a volume claim template in a Stateful Set)"),
        (0, "The PersistentVolumeClaim is initially Pending"),
        (0, "Kubernetes then looks for a suitable PersistentVolume (maybe one is immediately available; maybe we need to wait for provisioning)"),
        (0, "Once a suitable PersistentVolume is found, the PVC becomes Bound"),
        (0, "The PVC can then be used by a Pod (as long as the PVC is Pending, the Pod cannot run)"),
    ], x=0.7, w=11.9, size=15, line_spacing=1.5)
    whale_and_footer(s, n, total)


def sl23(s, n, total):
    title(s, "Using a PersistentVolumeClaim in a pod")
    yaml_terminal(s, 3.0, 1.5, 7.3, 5.0, "mongodb.yaml", [
        "apiVersion: v1", "kind: Pod", "metadata:", "  name: mongodb", "spec:",
        "  containers:", "  - image: mongo", "    name: mongodb", "    volumeMounts:",
        "    - name: mongodb-data", "      mountPath: /data/db", "    ports:",
        "    - containerPort: 27017", "      protocol: TCP", "  volumes:",
        "  - name: mongodb-data", "    persistentVolumeClaim:", "      claimName: mongodb-pvc",
    ], font_size=11)
    whale_and_footer(s, n, total)


def sl24(s, n, total):
    title(s, "Using a PersistentVolumeClaim in a pod")
    yaml_terminal(s, 0.6, 1.55, 6.0, 4.7, "pvc-definition.yaml", [
        "apiVersion: v1", "kind: PersistentVolumeClaim", "metadata:", "  name: myclaim",
        "spec:", "  accessModes:", "    - ReadWriteOnce", "  resources:",
        "    requests:", "      storage: 500Mi",
    ], font_size=11)
    yaml_terminal(s, 6.85, 1.55, 5.95, 4.7, "pv-definition.yaml", [
        "apiVersion: v1", "kind: PersistentVolume", "metadata:", "  name: pv-vol1",
        "spec:", "  accessModes:", "    - ReadWriteOnce", "  capacity:",
        "    storage: 1Gi", "  awsElasticBlockStore:", "    volumeID: <volume-id>",
        "    fsType: ext4",
    ], font_size=11)
    whale_and_footer(s, n, total)


def sl25(s, n, total):
    title(s, "Understanding the benefits of using PersistentVolumes and claims", size=22)
    embed(s, "s25_1.png", 3.9, 1.6, 5.6, 4.85)
    whale_and_footer(s, n, total)


def sl26(s, n, total):
    title(s, "Provisioning Automation: Storage Class")
    bullets(s, 1.7, [
        (0, "What if we have multiple storage systems available? (e.g. NFS and iSCSI; or AzureFile and AzureDisk; or Cinder and Ceph...)"),
        (0, "What if we have a storage system with multiple tiers? (e.g. SAN with RAID1 and RAID5; general purpose vs. io optimized EBS...)"),
        (0, "Kubernetes lets us define storage classes to represent these (see if you have any available at the moment with kubectl get storageclasses)"),
    ], x=0.7, w=11.9, size=16, line_spacing=1.6)
    whale_and_footer(s, n, total)


def sl27(s, n, total):
    title(s, "Using storage classes")
    bullets(s, 1.75, [
        (0, "Optionally, each PV and each PVC can reference a StorageClass (field spec.storageClassName)"),
        (0, "When creating a PVC, specifying a StorageClass means “use that particular storage system to provision the volume!”"),
        (0, "Storage classes are necessary for dynamic provisioning (but we can also ignore them and perform manual provisioning)"),
    ], x=0.7, w=11.9, size=16, line_spacing=1.7)
    whale_and_footer(s, n, total)


def sl28(s, n, total):
    title(s, "Storage Class Manifest")
    yaml_terminal(s, 0.6, 1.6, 6.0, 4.3, "storageclass-fast.yaml", [
        "apiVersion: storage.k8s.io/v1", "kind: StorageClass", "metadata:",
        "  name: fast", "provisioner: kubernetes.io/gce-pd", "parameters:",
        "  type: pd-ssd", "  zone: europe-west1-b",
    ], font_size=11)
    yaml_terminal(s, 6.85, 1.6, 5.95, 4.3, "mongodb-pvc.yaml", [
        "apiVersion: v1", "kind: PersistentVolumeClaim", "metadata:",
        "  name: mongodb-pvc", "spec:", "  storageClassName: fast", "  resources:",
        "    requests:", "      storage: 100Mi", "  accessModes:", "    - ReadWriteOnce",
    ], font_size=11)
    whale_and_footer(s, n, total)


def sl29(s, n, total):
    title(s, "Dynamic PersistentVolume Provisioning", size=26)
    embed(s, "fig_s29.png", 1.3, 1.75, 10.7, 4.6)
    whale_and_footer(s, n, total)


def sl30(s, n, total):
    divider(s, "WORK\nSHOP 2", "PV, PVC, StorageClasses")
    whale_and_footer(s, n, total)


def sl31(s, n, total):
    title(s, "Amazon EBS backed Volume – Data persists independent of the hosting node", size=20)
    auto_term(s, 0.55, 1.5, 12.25, 4.95, "bash — redis + PVC", [
        "# Create redis deployment, service and PVC", "$ k get sc", "$ k create ns week9",
        "$ k apply -f redis_service.yaml -n week9", "$ k apply -f redis_pvc.yaml -n week9",
        "# Review the created PVC and PV, describe the created PV and PVC", "$ k get pvc –n week9",
        "$ k apply -f redis_deployment.yaml -n week9",
        "# Add PVC mount to Redis deployment manifest and redeploy Redis",
        "$ k delete deployment redis -n week9",
        "$ eksctl create addon --name aws-ebs-csi-driver --cluster clo835 \\",
        "    --service-account-role-arn arn:aws:iam::[YOUR AWS ACCOUNT]:role/LabRole --force",
        "$ k apply -f redis_deployment.yaml -n week9",
    ], font_size=11)
    whale_and_footer(s, n, total)


def sl32(s, n, total):
    title(s, "Store data in redis and Recreate the pod")
    auto_term(s, 0.55, 1.5, 12.25, 4.95, "bash — redis-cli", [
        "# Run redis cli client",
        "$ kubectl run redis-cli --rm -ti --image=redis:3.2.5 --restart=Never -- /bin/sh",
        "# redis-cli -h redis.week9.svc.cluster.local", "> set foo bar", "> get foo",
        '"bar"', "> quit", "# Delete the pod", "$ k delete pod-xxx redis -n week9",
        "# Notice if the pod got rescheduled to another node", "$ k get pods –n week9",
        "# run redis cli and verify data is still availble when the pod gets rescheduled",
        "$  kubectl run redis-cli --rm -ti --image=redis:3.2.5 --restart=Never -- /bin/bash",
        "# redis-cli -h redis.week9.svc.cluster.local", "> get foo",
    ], font_size=10.5)
    whale_and_footer(s, n, total)


def sl33(s, n, total):
    closing(s, "Workshop 2 – The End")
    whale_and_footer(s, n, total)


def sl34(s, n, total):
    section(s, "deploying clustered applications")
    whale_and_footer(s, n, total)


def sl35(s, n, total):
    title(s, "Why StatefulSets?")
    add_text(s, Inches(0.7), Inches(1.45), Inches(11.9), Inches(0.45),
             "Because some apps (databases, clustered systems) need things Deployments cannot give:",
             size=15, color=BODY, line_spacing=1.3)
    rows = [
        ("Stable identity",
         "pod names are fixed (mysql-0, mysql-1) and survive restarts. Deployment pods get random names and IPs."),
        ("Stable network address",
         "each pod gets its own DNS name via the headless service, so \"the master\" is always reachable at mysql-0."),
        ("Per-pod storage",
         "each replica gets its own PVC that reattaches to the same pod after rescheduling. Deployment replicas share one volume."),
        ("Ordered operations",
         "pods start, scale, and update one at a time, in sequence (master before slaves). Deployments start all pods in parallel."),
    ]
    y = 2.15
    for i, (head, body) in enumerate(rows, 1):
        add_oval(s, Inches(0.7), Inches(y), Inches(0.5), Inches(0.5), SLATE)
        add_text(s, Inches(0.7), Inches(y), Inches(0.5), Inches(0.5), str(i),
                 size=16, bold=True, color=WHITE, align=CENTER, anchor=MIDDLE)
        add_text(s, Inches(1.45), Inches(y - 0.02), Inches(10.9), Inches(0.3),
                 head, size=15, bold=True, color=SLATE)
        add_text(s, Inches(1.45), Inches(y + 0.32), Inches(10.9), Inches(0.65),
                 body, size=13, color=BODY, line_spacing=1.3)
        y += 1.12
    whale_and_footer(s, n, total)


def sl35b(s, n, total):
    title(s, "Why StatefulSets?")
    embed(s, "s35_1.png", 2.09, 0.97, 9.1, 6.1)
    whale_and_footer(s, n, total)


def sl36(s, n, total):
    title(s, "WHY CAN’T WE USE DEPLOYMENTS??", size=26)
    bullets(s, 1.75, [
        (0, "All Pods are deployed in parallel"),
        (0, "No ordinality is maintained"),
        (0, "Cant really identify MASTER as name and IP will change as POD is recreated"),
        (0, "Cannot maintain a sequence"),
    ], x=0.6, w=6.1, size=15, line_spacing=1.55)
    diagram_right(s, "s36_1.png", box=(6.9, 1.7, 6.0, 4.6))
    whale_and_footer(s, n, total)


def sl37(s, n, total):
    title(s, "WHAT ARE STATEFULSETS??", size=28)
    bullets(s, 1.55, [
        (0, "Assigns Unique Ordinality Index to each pod (starts at 0 and increments by 1)"),
        (0, "Uses a Static Name (mysql-0, mysql-1 etc..)"),
        (0, "Even if POD fails, it will come up with same name"),
        (0, "Statefulset maintains a sticky identity. Master is always the MASTER with name mysql-0"),
        (0, "Scale up and down is in Order, graceful deployment"),
        (0, "Each pod gets stable, unique network identifier"),
    ], x=0.6, w=6.15, size=13.5, line_spacing=1.4)
    diagram_right(s, "s37_1.png", box=(6.95, 1.55, 5.9, 4.95))
    whale_and_footer(s, n, total)


def sl38(s, n, total):
    title(s, "SCALING PODS that reference Persistent volume", size=24)
    bullets(s, 1.7, [
        (0, "All the replicas in the replicaset are identical"),
        (0, "All pods in the replicaset will reference the same volume since volume are defined at a pod level"),
        (0, "When we are deploying a stateful application (DB) and each replica needs to have an independent storage"),
    ], x=0.6, w=6.1, size=15, line_spacing=1.55)
    diagram_right(s, "s38_1.png", box=(7.0, 2.4, 5.9, 2.4))
    whale_and_footer(s, n, total)


def sl39(s, n, total):
    title(s, "Stable network identity for pods")
    bullets(s, 1.9, [
        (0, "Clustered applications also require that each instance has a long-lived stable identity (hostname and IP)"),
        (0, "Each member of the stateful application's cluster need to know network identities of all member of the cluster"),
        (0, "This would not work with applications created with K8s deployment – each time the pods is re-created it's IP and hostname changes"),
    ], x=0.7, w=11.9, size=16, line_spacing=1.7)
    whale_and_footer(s, n, total)


def sl40(s, n, total):
    title(s, "Statefulsets")
    bullets(s, 1.5, [
        (0, "StatefulSet manages the deployment and scaling of a set of Pods, and provides guarantees about the ordering and uniqueness of these Pods, suitable for applications that require one or more of the following."),
        (0, "Applications are treated as non-fungible individuals, with each one having a stable name and state. (pets vs cattle analogy)"),
        (0, "Stable, unique network identifiers"),
        (0, "Stable, persistent storage"),
        (0, "Ordered, graceful deployment and scaling"),
        (0, "Ordered, automated rolling updates"),
    ], x=0.6, w=9.0, size=13.5, line_spacing=1.35)
    embed(s, "s40_1.png", 9.9, 1.7, 2.9, 2.6)
    whale_and_footer(s, n, total)


def sl41(s, n, total):
    title(s, "Sttatefulsets vs replicasets")
    bullets(s, 1.75, [
        (0, "Pods in ReplicaSet are like cattle. They are indistinguishable and replaceable. If the pod dies a new pod with anew IP/hostname and data is created."),
        (0, "Pods in Stateful sets are like pets. When a \"pet\" dies, it needs to be resurrected with the same name, IP and data. Pods in Statefulsets are not replicas of each other. They can have individual volumes (data)."),
    ], x=0.6, w=6.1, size=14, line_spacing=1.45)
    diagram_right(s, "s41_1.png", box=(7.0, 2.4, 5.9, 2.2))
    whale_and_footer(s, n, total)


def sl42(s, n, total):
    title(s, "HEADLESS SERVICE")
    bullets(s, 1.6, [
        (0, "Normal service cannot be used as it load balances the requests and our objective is to write only to master."),
        (0, "An IP cannot be used only to write as it might change. Even the Pod dns cannot be used as it has IP in it."),
        (0, "Headless service doesn’t load balance the requests. Points to only Master."),
        (0, "Uses Pod DNS which is mysql-0.mysql-h.default.svc.cluster.local"),
    ], x=0.6, w=6.2, size=13.5, line_spacing=1.4)
    diagram_right(s, "s42_1.png", box=(7.4, 1.55, 5.4, 4.95))
    whale_and_footer(s, n, total)


def sl43(s, n, total):
    title(s, "Exposing Statefulsets")
    bullets(s, 2.1, [
        (0, "Headless service, ClusterIP: None"),
        (0, "Each pod has its own DNS enty, e.g. a-0.foo.default.svc.cluster.local"),
    ], x=4.6, w=8.2, size=16, line_spacing=1.7)
    embed(s, "s43_1.png", 0.9, 1.7, 3.2, 4.4)
    whale_and_footer(s, n, total)


def sl44(s, n, total):
    title(s, "Adding volumes to statefulset's pods", size=26)
    bullets(s, 1.7, [
        (0, "Storage needs to be persistent and decoupled from pods"),
        (0, "Each pod needs to reference a different PVC"),
        (0, "PVCs need to be created by Statefulset and not separately as we did for the stateless pods"),
    ], x=0.6, w=6.1, size=15, line_spacing=1.55)
    diagram_right(s, "s44_1.png", box=(7.0, 2.3, 5.9, 2.4))
    whale_and_footer(s, n, total)


def sl45(s, n, total):
    divider(s, "WORK\nSHOP 3", "StatefulSets")
    whale_and_footer(s, n, total)


def sl46(s, n, total):
    title(s, "Application functionality")
    bullets(s, 1.8, [
        (0, "On \"POST\", store the data in a local file"),
        (0, "On GET, return the hostname and the content of the file"),
        (0, "https://github.com/luksa/kubernetes-in-action/blob/master/Chapter10/kubia-pet-image/app.js", BLUE),
    ], x=0.6, w=6.2, size=14, line_spacing=1.6)
    diagram_right(s, "s46_1.png", box=(7.2, 1.7, 5.6, 4.5))
    whale_and_footer(s, n, total)


def sl47(s, n, total):
    title(s, "What are we creating?")
    bullets(s, 1.9, [
        (0, "StatefulSet"),
        (0, "Governing service"),
        (0, "PersistentVolumeClaims as part of StatefulSet manifest. Volume provisioning will be handled by AWS EBS provisioner if we use default StorageClass gp2."),
        (0, "https://github.com/luksa/kubernetes-in-action/blob/master/Chapter10/kubia-statefulset.yaml", BLUE),
    ], x=0.7, w=11.9, size=16, line_spacing=1.7)
    whale_and_footer(s, n, total)


def sl48(s, n, total):
    title(s, "Deployment - statefulset")
    auto_term(s, 0.55, 1.7, 7.0, 4.4, "bash — statefulset", [
        "# Pods are created one by one, unlike replicaset",
        "# where all pods are created at once",
        "$ kubectl patch storageclass gp2 -p \\",
        "  '{\"metadata\": {\"annotations\":",
        "  {\"storageclass.kubernetes.io/is-default-class\":\"true\"}}}'",
        "$ k create –f kubia-statefulset.yaml", "$ k get pvc", "$ k get pv",
    ], font_size=11.5)
    embed(s, "s48_1.png", 7.8, 2.1, 5.0, 3.6)
    whale_and_footer(s, n, total)


def sl49(s, n, total):
    title(s, "Communicating with the application via proxy", size=24)
    auto_term(s, 0.55, 1.6, 7.6, 3.05, "bash — proxy", [
        "$ kubectl proxy",
        "$ curl localhost:8001/api/v1/namespaces/default/pods/kubia-0/proxy/",
        "curl -X POST -d \"Hey there! This greeting was submitted to kubia-0.\"",
        "curl localhost:8001/api/v1/namespaces/default/pods/kubia-0/proxy/",
        "curl localhost:8001/api/v1/namespaces/default/pods/kubia-1/proxy/",
    ], font_size=11)
    embed(s, "s49_1.png", 1.5, 4.9, 9.0, 1.55)
    whale_and_footer(s, n, total)


def sl50(s, n, total):
    title(s, "DELETING A STATEFUL POD TO SEE IF THE RESCHEDULED POD IS REATTACHED TO THE SAME STORAGE", size=17)
    auto_term(s, 1.0, 1.85, 11.3, 3.4, "bash — delete pod", [
        "$ kubectl delete po kubia-0",
        "$ kubectl get po # Execute a few times",
        "$ curl localhost:8001/api/v1/namespaces/default/pods/kubia-0/proxy/",
        "# persistent volume gets re-attached to a \"new\" kibia-0 pod",
    ], font_size=13)
    whale_and_footer(s, n, total)


def sl51(s, n, total):
    title(s, "EXPOSING STATEFUL PODS THROUGH A REGULAR clusterip SERVICE", size=20)
    auto_term(s, 1.0, 1.75, 11.3, 3.0, "bash — clusterip", [
        "$ k create -f kubia-clusterIP.yaml",
        "$ k proxy",
        "$ curl localhost:8001/api/v1/namespaces/default/services/kubia-public/proxy/",
    ], font_size=13)
    whale_and_footer(s, n, total)


def sl52(s, n, total):
    title(s, "Discovering peers in a StatefulSet", size=28)
    bullets(s, 1.35, [
        (0, "Application should be K8s agnostic so querying K8s API to find all the pods in the cluster is undesirable"),
        (0, "K8s uses DNS SRV records to facilitate the discovery. Kubernetes creates SRV records to point to the hostnames of the pods backing a headless service."),
    ], x=0.6, w=12.1, size=13, line_spacing=1.35)
    auto_term(s, 0.6, 3.35, 12.2, 3.05, "bash — SRV discovery", [
        "# create headless service", "k apply -f kubia-headless.yaml",
        "# discovering the SRV records for the kubia cluster",
        "k run -it dnstest-alpine --image=alpine/curl --rm --restart=Never -- /bin/ash",
        "apk update", "apk add bind-tools # Installs dig and nslookup",
        "# dig SRV kubia.default.svc.cluster.local",
    ], font_size=11.5)
    whale_and_footer(s, n, total)


def sl53(s, n, total):
    title(s, "Implementing peer discovery through DNS", size=26)
    bullets(s, 1.7, [
        (0, "Data stored by individual pods is independent – this is not a cluster yet"),
        (0, "We can improve the functionality by discovering all the pods in the StatefulSet and serving data from all the pods in the cluster"),
        (0, "github.com/luksa/kubernetes-in-action/.../kubia-pet-peers-image/app.js#L46", BLUE),
    ], x=0.6, w=6.2, size=14, line_spacing=1.5)
    diagram_right(s, "s53_1.png", box=(7.0, 2.2, 5.9, 3.6))
    whale_and_footer(s, n, total)


def sl54(s, n, total):
    title(s, "Updating a StatefulSet")
    auto_term(s, 0.55, 1.7, 6.6, 2.5, "bash — update", [
        "$ k edit statefulset kubia",
        "# Update container image to luksa/kubia-pet-peers",
        "$ k get po",
    ], font_size=12.5)
    embed(s, "s54_1.png", 7.5, 1.8, 5.3, 3.9)
    whale_and_footer(s, n, total)


def sl55(s, n, total):
    title(s, "Trying out our clustered data store")
    auto_term(s, 0.7, 1.7, 11.9, 4.3, "bash — clustered store", [
        "# Send POST to a ramdom pod though ClusterIP service",
        "$ curl -X POST -d \"The sun is shining\" \\",
        "    localhost:8001/api/v1/namespaces/default/services/kubia-public/proxy/",
        "$ curl -X POST -d \"The rain is raining\" \\",
        "    localhost:8001/api/v1/namespaces/default/services/kubia-public/proxy/",
        "# Reading data from a clustered data store",
        "$ curl localhost:8001/api/v1/namespaces/default/services/kubia-public/proxy/",
    ], font_size=12)
    whale_and_footer(s, n, total)


def sl56(s, n, total):
    closing(s, "Workshop 3 the end")
    whale_and_footer(s, n, total)


def sl57(s, n, total):
    title(s, "Cleanup")
    auto_term(s, 0.7, 1.6, 11.9, 4.6, "bash — cleanup", [
        "# kill proxy", "pkill -f 'kubectl proxy --port=8080'",
        "# delete dashboard",
        "kubectl delete -f https://raw.githubusercontent.com/kubernetes/dashboard/\\",
        "    ${DASHBOARD_VERSION}/aio/deploy/recommended.yaml",
        "unset DASHBOARD_VERSION",
        "# Delete the week8 namespace", "$ k delete ns week8",
        "# Delete the cluster", "$ eksctl delete cluster --name clo835 --region us-east-1",
        "# Stop cloud9 instance",
        "https://docs.aws.amazon.com/eks/latest/userguide/managing-ebs-csi.html",
    ], font_size=12)
    whale_and_footer(s, n, total)


# ============================================================================
# Deck composition — theory duplicated into the lab for context
# ============================================================================

LECTURE = [
    lambda s, n, t: sl01(s, n, t, "Lecture"),
    sl02, sl03,
    sl04, sl05, sl06, sl07, sl08, sl09, sl10,          # hostPath theory
    sl18, sl19, sl20, sl21, sl22, sl24, sl23, sl25, sl26, sl27, sl28, sl29,  # PV/PVC/SC (manifests before pod usage)
    sl34, sl35, sl35b, sl36, sl37, sl38, sl39, sl40, sl41, sl42, sl43, sl44, # StatefulSets
    sl52, sl53,                                          # peer-discovery concept
]

LAB = [
    lambda s, n, t: sl01(s, n, t, "Lab"),
    sl04, sl06,                                          # recap: hostPath theory
    sl11, sl12, sl13, sl14, sl15, sl16, sl17,           # Workshop 1
    sl19, sl29,                                          # recap: PV/PVC + dynamic provisioning
    sl30, sl31, sl32, sl33,                              # Workshop 2
    sl37, sl44,                                          # recap: StatefulSet theory
    sl45, sl46, sl47, sl48, sl49, sl50, sl51, sl52, sl53, sl54, sl55, sl56, sl57,  # Workshop 3
]


def build(deck, out):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]
    total = len(deck)
    for i, fn in enumerate(deck, 1):
        s = prs.slides.add_slide(blank)
        fn(s, i, total)
    _sanitize_coords(prs)
    prs.save(out)
    print(f"wrote {out}  ({total} slides)")


# ===== Save =====
if __name__ == "__main__":
    build(LECTURE, f"Week09/Week09_lecture_style_{LECTURE_VERSION}.pptx")
    build(LAB, f"Week09/Week09_lab_style_{LAB_VERSION}.pptx")
