"""Week07_lab_style — Lab02/Week05 design language applied to Week7.pptx.

Source: /Users/maziar/Downloads/Week07.pptx — 14 slides, "Volumes: Attaching Disk
Storage to Containers". Original slide text preserved verbatim (no rephrasing).
Treatment (same as Week 6): bullet slides → blue title + multi-level bullets;
YAML manifests → dark terminal mockup; the gitRepo diagram → embedded original.
Exact CLO835 palette + Calibri/Consolas + chrome.
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
STEPS = [
    RGBColor(0x1F, 0xA8, 0xE0), RGBColor(0x21, 0x96, 0xA0),
    RGBColor(0x1F, 0x8F, 0xCD), RGBColor(0x1F, 0x7A, 0xB8),
    RGBColor(0x24, 0x66, 0xA0), RGBColor(0x37, 0x46, 0x5A),
]
FONT_SANS, FONT_MONO = "Calibri", "Consolas"

K8S_LOGO   = "Week04/Kubernetes_logo_without_workmark.svg.png"
WHALE      = "whale.png"
ASSETS_DIR = "Week07/assets"
VERSION    = "v3"
TOTAL      = 14
ASPECT = {"fig_gitrepo.jpg": (2300, 920)}


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


def whale_and_footer(s, page_num, total=TOTAL):
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


def yaml_terminal(s, x, y, w, h, title_text, lines, *, font_size=11):
    """lines: list of raw YAML strings. Top-level keys (no indent, ends ':') = cyan; rest gray."""
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


# ===== Setup =====
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank = prs.slide_layouts[6]


def new_slide():
    return prs.slides.add_slide(blank)


# SLIDE 1 — Cover
s = new_slide()
add_text(s, Inches(0.7), Inches(2.55), Inches(8.7), Inches(1.8),
         "Volumes: Attaching Disk\nStorage to Containers",
         size=36, bold=True, color=BLUE, line_spacing=1.12)
add_text(s, Inches(0.7), Inches(4.7), Inches(8.5), Inches(0.6), "Week 7", size=22, color=SLATE)
logo_cx = Inches(10.7); logo_cy = Inches(3.55); ring_r = Inches(1.8)
add_oval(s, logo_cx - ring_r, logo_cy - ring_r, ring_r * 2, ring_r * 2, WHITE, line=LIGHTBLUE, line_width=1.5)
s.shapes.add_picture(K8S_LOGO, logo_cx - Inches(1.25), logo_cy - Inches(1.25), width=Inches(2.5), height=Inches(2.5))
s.shapes.add_picture(WHALE, Inches(0.45), Inches(6.85), width=Inches(0.5), height=Inches(0.5))
add_text(s, Inches(9.5), Inches(7.12), Inches(3.35), Inches(0.3),
         f"CLO835, Fall 2026     1 / {TOTAL}", size=10, color=FOOTER_GRAY, align=RIGHT)

# SLIDE 2 — Agenda
s = new_slide()
title(s, "Agenda")
bullets(s, 1.7, [
    (0, "Volumes"),
    (1, "emptyDir"),
    (1, "hostPath"),
    (0, "PersistentVolumes (PV) and PersistentVolumeClaims (PVC)"),
    (0, "StorageClass"),
], x=0.7, w=11.5, size=18, line_spacing=1.6)
whale_and_footer(s, 2)

# SLIDE 3 — K8s Volumes
s = new_slide()
title(s, "K8s Volumes")
bullets(s, 1.55, [
    (0, "Unlike Network, processes and CPU, filesystems are unique per container"),
    (0, "Used to persist data between container invocations"),
    (0, "Can be shared by containers in a pod"),
    (0, "Defined as part of the pod spec"),
    (0, "Share pod’s lifecycle"),
    (1, "Initiated when pod starts"),
    (1, "Terminated when a pod is terminated"),
], x=0.7, w=11.8, size=16, line_spacing=1.55)
whale_and_footer(s, 3)

# SLIDE 4 — Volumes
s = new_slide()
title(s, "Volumes")
bullets(s, 1.55, [
    (0, "Volumes are special directories that are mounted in containers"),
    (0, "Volumes can have many different purposes:"),
    (1, "share files and directories between containers running on the same machine"),
    (1, "share files and directories between containers and their host"),
    (1, "centralize configuration information in Kubernetes and expose it to containers"),
    (1, "manage credentials and secrets and expose them securely to containers"),
    (1, "store persistent data for stateful services"),
], x=0.7, w=11.8, size=15, line_spacing=1.5)
whale_and_footer(s, 4)

# SLIDE 5 — Volumes vs PersistentVolumes
s = new_slide()
title(s, "Volumes vs PersistentVolumes")
bullets(s, 1.55, [
    (0, "Volumes and Persistent Volumes are related, but very different!"),
    (0, "Volumes:"),
    (1, "appear in Pod specifications (we'll see that in a few slides)"),
    (1, "do not exist as API resources (cannot do kubectl get volumes)"),
    (0, "Persistent Volumes:"),
    (1, "are API resources (can do kubectl get persistentvolumes)"),
    (1, "correspond to concrete volumes (e.g. on a SAN, EBS, etc.)"),
    (1, "cannot be associated with a Pod directly; but through a Persistent Volume Claim"),
    (1, "won't be discussed further in this section"),
], x=0.7, w=11.8, size=14, line_spacing=1.4)
whale_and_footer(s, 5)

# SLIDE 6 — Volume Types
s = new_slide()
title(s, "Volume Types")
bullets(s, 1.55, [
    (0, "emptyDir—A simple empty directory used for storing transient data."),
    (0, "hostPath—Used for mounting directories from the worker node’s filesystem into the pod."),
    (0, "gitRepo—A volume initialized by checking out the contents of a Git repository."),
    (0, "nfs—An NFS share mounted into the pod."),
    (1, "gcePersistentDisk (Google Compute Engine Persistent Disk)"),
    (1, "awsElasticBlockStore (Amazon Web Services Elastic Block Store Volume)"),
    (1, "azureDisk (Microsoft Azure Disk Volume)—Used for mounting cloud provider-specific storage."),
], x=0.7, w=11.9, size=14, line_spacing=1.45)
whale_and_footer(s, 6)

# SLIDE 7 — Volume Types, Cont
s = new_slide()
title(s, "Volume Types, Cont")
bullets(s, 1.85, [
    (0, "cinder, cephfs, iscsi, flocker, glusterfs, quobyte, rbd, flexVolume, vsphereVolume, photonPersistentDisk, scaleIO—Used for mounting other types of network storage."),
    (0, "configMap, secret, downward API—Special types of volumes used to expose certain Kubernetes resources and cluster information to the pod."),
    (0, "persistentVolumeClaim—A way to use a pre- or dynamically provisioned persistent storage."),
], x=0.7, w=11.9, size=15, line_spacing=1.55)
whale_and_footer(s, 7)

# SLIDE 8 — Volume Type: emptyDir
s = new_slide()
title(s, "Volume Type: emptyDir")
bullets(s, 1.75, [
    (0, "We will start with the simplest Pod manifest we can find"),
    (0, "We will add a volume to that Pod manifest"),
    (0, "We will mount that volume in a container in the Pod"),
    (0, "By default, this volume will be an emptyDir (an empty directory)"),
    (0, "It will \"shadow\" the directory where it's mounted"),
], x=0.7, w=11.8, size=16, line_spacing=1.7)
whale_and_footer(s, 8)

# SLIDE 9 — Volume Lifecycle
s = new_slide()
title(s, "Volume Lifecycle")
bullets(s, 1.75, [
    (0, "The lifecycle of a volume is linked to the pod's lifecycle"),
    (0, "This means that a volume is created when the pod is created"),
    (0, "This is mostly relevant for emptyDir volumes"),
    (0, "(other volumes, like remote storage, are not \"created\" but rather \"attached\" )"),
    (0, "A volume survives across container restarts"),
    (0, "A volume is destroyed (or, for remote storage, detached) when the pod is destroyed"),
], x=0.7, w=11.8, size=16, line_spacing=1.6)
whale_and_footer(s, 9)

# SLIDE 10 — Using GitRepo Volume (diagram)
s = new_slide()
title(s, "Using GitRepo Volume")
embed(s, "fig_gitrepo.jpg", 1.0, 1.7, 11.3, 4.7)
whale_and_footer(s, 10)

# SLIDE 11 — Pod Manifest with GitRepo (MODERN: gitRepo is deprecated since K8s 1.11,
# so clone with an initContainer into an emptyDir instead)
s = new_slide()
title(s, "Pod Manifest with GitRepo")
yaml_terminal(s, 0.55, 1.4, 6.9, 5.25, "gitrepo-volume-pod.yaml", [
    "apiVersion: v1", "kind: Pod", "metadata:", "  name: gitrepo-volume-pod",
    "spec:", "  initContainers:", "  - name: git-clone", "    image: alpine/git",
    "    args:", "    - clone", "    - --single-branch", "    - --branch=master",
    "    - https://github.com/luksa/kubia-website-example.git", "    - /repo",
    "    volumeMounts:", "    - name: html", "      mountPath: /repo",
    "  containers:", "  - image: nginx:alpine", "    name: web-server",
    "    volumeMounts:", "    - name: html",
    "      mountPath: /usr/share/nginx/html", "      readOnly: true",
    "  volumes:", "  - name: html", "    emptyDir: {}",
], font_size=9)
annot_card(s, 7.7, 1.55, 5.1, 1.05, "initContainers:", "Runs to completion before the app container starts.")
annot_card(s, 7.7, 2.78, 5.1, 1.05, "image: alpine/git", "A tiny Git image performs the clone.")
annot_card(s, 7.7, 4.01, 5.1, 1.05, "args: clone ...", "Clones the master branch into the shared /repo volume.")
annot_card(s, 7.7, 5.24, 5.1, 1.15, "emptyDir: {}", "A plain empty volume — the modern replacement for the deprecated gitRepo type.")
whale_and_footer(s, 11)

# SLIDE 12 — Managing configuration
s = new_slide()
title(s, "Managing configuration")
bullets(s, 1.6, [
    (0, "Some applications need to be configured"),
    (0, "There are many ways for our code to pick up configuration:"),
    (1, "command-line arguments"),
    (1, "environment variables"),
    (1, "configuration files"),
    (1, "configuration servers (getting configuration from a database, an API...)"),
    (1, "... and more (because programmers can be very creative!)"),
    (0, "How can we do these things with containers and Kubernetes?"),
], x=0.7, w=11.8, size=15, line_spacing=1.5)
whale_and_footer(s, 12)

# SLIDE 13 — Persistent Volumes: Amazon EBS (MODERN: the in-tree awsElasticBlockStore
# volume is deprecated/removed; use the EBS CSI driver via a StorageClass + PVC)
s = new_slide()
title(s, "Persistent Volumes: Amazon EBS")
bullets(s, 1.75, [
    (0, "Modern approach: provision EBS with the EBS CSI driver (the in-tree awsElasticBlockStore volume is deprecated)"),
    (0, "A StorageClass (ebs-sc → ebs.csi.aws.com) provisions the volume dynamically"),
    (0, "A PersistentVolumeClaim requests the storage"),
    (0, "The Pod mounts the volume by referencing the PVC"),
], x=0.55, w=5.0, size=13.5, line_spacing=1.45)
yaml_terminal(s, 5.75, 1.4, 7.05, 5.25, "ebs-pvc-and-pod.yaml", [
    "apiVersion: v1", "kind: PersistentVolumeClaim", "metadata:",
    "  name: my-ebs-claim", "spec:", "  accessModes:", "  - ReadWriteOnce",
    "  storageClassName: ebs-sc", "  resources:", "    requests:",
    "      storage: 4Gi", "---",
    "apiVersion: v1", "kind: Pod", "metadata:",
    "  name: pod-using-my-ebs-volume", "spec:", "  containers:",
    "  - image: ...", "    name: container-using-my-ebs-volume",
    "    volumeMounts:", "    - mountPath: /my-ebs", "      name: my-ebs-volume",
    "  volumes:", "  - name: my-ebs-volume", "    persistentVolumeClaim:",
    "      claimName: my-ebs-claim",
], font_size=9)
whale_and_footer(s, 13)

# SLIDE 14 — Using NFS Volume (terminal)
s = new_slide()
title(s, "Using NFS Volume")
yaml_terminal(s, 3.3, 1.6, 8.7, 4.85, "pod-using-my-nfs-volume.yaml", [
    "apiVersion: v1", "kind: Pod", "metadata:", "  name: pod-using-my-nfs-volume",
    "spec:", "  containers:", "  - image: ...", "    name: container-using-my-nfs-volume",
    "    volumeMounts:", "    - mountPath: /my-nfs", "      name: my-nfs-volume",
    "  volumes:", "  - name: my-nfs-volume", "    nfs:",
    "      server: 192.168.0.55", "      path: \"/exports/assets\"",
], font_size=12)
whale_and_footer(s, 14)

# ===== Save =====
_sanitize_coords(prs)
out = f"Week07/Week07_lab_style_{VERSION}.pptx"
prs.save(out)
print(f"wrote {out}  ({len(list(prs.slides))} slides)")
