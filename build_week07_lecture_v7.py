# -*- coding: utf-8 -*-
"""CLO835 Week 07 lecture v7 - Volumes: Attaching Disk Storage to Containers.

Fixes the 37 defects and adds the 18 additions of
reports/report-2026-11-09-02-week07-week10-lecture-audit.md (tables 1 and 2).
v6 stays on disk. The main changes:
- The volume lifecycle is correct: only an ephemeral volume ends with its Pod.
- The lecture now teaches what the lab practises: hostPath (lab Step 4), and a claim with the
  StorageClass standard (lab Step 5). The EBS and NFS manifests carry the label "example only".
- New slides: a comparison table, the fortune diagram, the emptyDir and mount settings, the
  hostPath manifest, the claim on the course cluster, commands and troubleshooting, takeaways,
  a closing slide and the references.
- A tab after each bullet, so a wrapped line starts under the text of the first line.
- Code names in Consolas. Terminals at 11 or 12 pt. YAML in gray, $ commands in cyan.

This file also holds the slide kit that build_week10_lecture_v10.py imports.

Input : Week12/Lecture_week12_v6.pptx, for the cover and the outline (read, never written)
Output: Week07/Lecture_week07_v7.pptx (the build refuses to overwrite it)

Run from the project root. It is guarded, so importing it writes nothing.
    .venv/bin/python build_week07_lecture_v7.py
"""
import copy
import os
import re
import sys

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

import build_week08 as E
from build_week09_lecture_v6 import arrow, box, zone
from build_week12_lecture_v6 import finish, footer_guard
from build_week13_lecture_v8 import keep_first, set_only_run

VERSION = "v7"
SRC = "Week12/Lecture_week12_v6.pptx"
OUT = "Week07/Lecture_week07_%s.pptx" % VERSION
SLATE, BLUE, STEPS, RED = E.SLATE, E.BLUE, E.STEPS, E.ALERT_RED
DOWN, UP, LEFT, RIGHT = MSO_SHAPE.DOWN_ARROW, MSO_SHAPE.UP_ARROW, MSO_SHAPE.LEFT_ARROW, MSO_SHAPE.RIGHT_ARROW
BOTTOM = 6.70
TOP = 1.55
# level: (text margin in EMU, bullet color, bullet character). The bullet hangs 0.25 in to the left.
LEVEL = {0: (228600, E.BLUE, "▪"), 1: (612647, STEPS[1], "–"), 2: (996695, E.MUTED, "•")}
HANG = 228600


# ---------------------------------------------------------------- the slide kit

def new_slide(prs, title):
    """A blank slide with the house title (30 pt) and the blue rule under it."""
    s = prs.slides.add_slide(prs.slide_layouts[6])
    E.add_text(s, Inches(0.55), Inches(0.40), Inches(12.2), Inches(0.85), title, size=30, bold=True,
               color=E.BLUE, line_spacing=1.05)
    E.add_line(s, Inches(0.57), Inches(1.38), Inches(5.2), Inches(1.38), color=E.BLUE, width=2)
    return s


def runs(p, text, size, color=E.BODY, bold=False, code_color=SLATE):
    """Add the runs of text to paragraph p. Text between backticks is code: Consolas, bold, slate."""
    for k, part in enumerate(text.split("`")):
        if not part:
            continue
        r = p.add_run()
        r.text = part
        r.font.size = Pt(size)
        r.font.name = E.FONT_MONO if k % 2 else E.FONT_SANS
        r.font.bold = True if k % 2 else bold
        r.font.color.rgb = code_color if k % 2 else color


def bullets(s, x, y, w, items, size=16, after=6, h=None, spacing=1.12):
    """Each item is (level, text). The bullet run ends with a tab, and the hanging indent is a tab stop,
    so a wrapped line starts under the first word (a:buChar bullets do not show the square in PowerPoint)."""
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h or BOTTOM - y))
    frame = tb.text_frame
    frame.margin_left = frame.margin_right = frame.margin_top = frame.margin_bottom = 0
    frame.word_wrap = True
    for i, (lvl, text) in enumerate(items):
        margin, color, char = LEVEL[lvl]
        p = frame.paragraphs[0] if i == 0 else frame.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.line_spacing = spacing
        p.space_after = Pt(after)
        ppr = p._p.get_or_add_pPr()
        ppr.set("marL", str(margin))
        ppr.set("indent", str(-HANG))
        points = max(size - lvl, 12)
        r = p.add_run()
        r.text = char + "\t"
        r.font.name, r.font.size, r.font.bold = E.FONT_SANS, Pt(points), True
        r.font.color.rgb = color
        runs(p, text, points)
    return tb


def concept(s, x, y, w, h, head, items, accent, size=14):
    """A card with a colored bar, a heading and bullets."""
    E.add_rounded_rect(s, Inches(x), Inches(y), Inches(w), Inches(h), E.CARD_BG, line=E.RULE_GRAY, line_width=0.75,
                       radius_ratio=0.05)
    E.add_rect(s, Inches(x), Inches(y + 0.05), Inches(0.12), Inches(h - 0.10), accent)
    rich(s, x + 0.32, y + 0.16, w - 0.50, 0.45, head, size=15, color=accent, bold=True)
    bullets(s, x + 0.32, y + 0.74, w - 0.50, [(0, item) for item in items], size=size, after=6, h=h - 0.90)


def rich(s, x, y, w, h, lines, size=13, color=E.BODY, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, bold=False,
         spacing=1.10, after=0):
    """A text box. Each line is a paragraph, and backticks mark code."""
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = tb.text_frame
    frame.margin_left = frame.margin_right = frame.margin_top = frame.margin_bottom = 0
    frame.word_wrap = True
    frame.vertical_anchor = anchor
    for i, line in enumerate([lines] if isinstance(lines, str) else lines):
        p = frame.paragraphs[0] if i == 0 else frame.add_paragraph()
        p.alignment = align
        p.line_spacing = spacing
        p.space_after = Pt(after)
        runs(p, line, size, color=color, bold=bold)
    return tb


def label(s, x, y, w, h, text, size=13, color=SLATE, align=PP_ALIGN.CENTER, bold=False):
    return rich(s, x, y, w, h, text, size=size, color=color, align=align, anchor=MSO_ANCHOR.MIDDLE, bold=bold,
                spacing=1.0)


def line_color(line, going):
    text = line.strip()
    if text.startswith("#"):
        return E.TERM_GRN
    if text.startswith("$") or going:
        return E.TERM_CYAN
    if text.startswith("error") or text.startswith("Error"):
        return E.TERM_RED
    return E.TERM_GRAY


def term(s, x, y, w, bar, lines, size=11, h=None, spacing=1.15):
    """A house terminal. YAML and output are gray, comments green, $ commands cyan."""
    rows, going = [], False
    for line in lines:
        rows.append(line)
    height = h or 0.32 + 0.10 + len(lines) * size * 1.17 * spacing / 72 + 0.18
    E.add_rect(s, Inches(x), Inches(y), Inches(w), Inches(height), E.TERMBG)
    E.add_rect(s, Inches(x), Inches(y), Inches(w), Inches(0.32), RGBColor(0x3A, 0x3A, 0x3A))
    for k, col in enumerate((E.TERM_RED, E.TERM_YEL, E.TERM_GRN)):
        E.add_oval(s, Inches(x + 0.15 + 0.17 * k), Inches(y + 0.10), Inches(0.13), Inches(0.13), col)
    E.add_text(s, Inches(x), Inches(y + 0.04), Inches(w), Inches(0.32), bar, size=10, color=E.TERM_GRAY,
               align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    tb = s.shapes.add_textbox(Inches(x + 0.18), Inches(y + 0.42), Inches(w - 0.32), Inches(height - 0.50))
    frame = tb.text_frame
    frame.margin_left = frame.margin_right = frame.margin_top = frame.margin_bottom = 0
    frame.word_wrap = True
    for i, line in enumerate(rows):
        p = frame.paragraphs[0] if i == 0 else frame.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.line_spacing = spacing
        r = p.add_run()
        r.text = line or " "
        r.font.name = E.FONT_MONO
        r.font.size = Pt(size)
        r.font.color.rgb = line_color(line, going)
        going = (line.strip().startswith("$") or going) and line.rstrip().endswith("\\")
    return y + height


def card(s, x, y, w, h, key, body, accent=BLUE, size=12.5, mono=True):
    """A card: a colored bar, a key line, and the body text (backticks mark code)."""
    E.add_rounded_rect(s, Inches(x), Inches(y), Inches(w), Inches(h), E.CARD_BG, line=E.RULE_GRAY, line_width=0.75,
                       radius_ratio=0.08)
    E.add_rect(s, Inches(x), Inches(y + 0.04), Inches(0.10), Inches(h - 0.08), accent)
    tb = rich(s, x + 0.26, y + 0.10, w - 0.40, 0.30, key, size=size, color=accent, bold=True)
    if mono:
        for r in tb.text_frame.paragraphs[0].runs:
            r.font.name = E.FONT_MONO
    rich(s, x + 0.26, y + 0.42, w - 0.40, h - 0.48, body, size=size, spacing=1.05)


def cards(s, x, y, w, items, h=0.95, gap=0.10, size=12.5, mono=True):
    """Each item is (key, body) or (key, body, height)."""
    for item in items:
        key, body, high = item if len(item) == 3 else item + (h,)
        card(s, x, y, w, high, key, body, size=size, mono=mono)
        y += high + gap
    return y


def caution(s, x, y, w, h, body, key="Caution", size=12.5):
    card(s, x, y, w, h, key, body, accent=RED, size=size, mono=False)


def grid(s, x, y, widths, rows, row_h=0.62, head_h=0.48, size=13):
    """A table drawn with house rectangles. rows[0] is the header."""
    yy = y
    for r, row in enumerate(rows):
        high = head_h if r == 0 else row_h
        xx = x
        for c, (cell, cw) in enumerate(zip(row, widths)):
            fill = SLATE if r == 0 else (E.CARD_BG if r % 2 else E.WHITE)
            E.add_rect(s, Inches(xx), Inches(yy), Inches(cw), Inches(high), fill, line=E.RULE_GRAY, line_width=0.75)
            rich(s, xx + 0.10, yy, cw - 0.20, high, cell, size=size, anchor=MSO_ANCHOR.MIDDLE,
                 color=E.WHITE if r == 0 else E.BODY, bold=r == 0)
            xx += cw
        yy += high
    return yy


def text_slide(prs, title, items, size=17, after=8, w=12.10):
    s = new_slide(prs, title)
    bullets(s, 0.60, TOP + 0.15, w, items, size=size, after=after)
    return s


def flow(s, x, y, w, text, fill=BLUE, kind=RIGHT, h=0.56):
    """An arrow shape with its label inside."""
    arrow(s, kind, x, y, w, h, fill=fill)
    inset = 0.22 if kind == LEFT else 0.06
    E.add_text(s, Inches(x + inset), Inches(y), Inches(w - 0.28), Inches(h), text, size=12, bold=True,
               color=E.WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.0)


def cover(prs, first, second, week):
    """The cover of the Week 12 v6 lecture, with the title in two lines."""
    s = prs.slides[0]
    by_name = {sh.name: sh for sh in s.shapes}
    shape = by_name["TextBox 1"]
    set_only_run(shape, first)
    para = shape.text_frame.paragraphs[0]._p
    para.addnext(copy.deepcopy(para))
    paragraph = shape.text_frame.paragraphs[1]
    paragraph.runs[0].text = second
    for extra in paragraph.runs[1:]:
        extra._r.getparent().remove(extra._r)
    for p in shape.text_frame.paragraphs:               # the Week 01 reference cover title is 34 pt
        for r in p.runs:
            r.font.size = Pt(34)
    set_only_run(by_name["TextBox 2"], "Week %d · Lecture" % week)
    by_name["TextBox 3"]._element.getparent().remove(by_name["TextBox 3"]._element)


def outline(prs, current):
    """The Course Outline: the blue tile moves from Week 12 to the current week. K8s becomes Kubernetes."""
    s = prs.slides[2]
    tiles = {sh.text_frame.text: sh for sh in s.shapes if sh.has_text_frame}
    blue, normal = tiles["Week 12: K8s – ConfigMaps & Secrets"], tiles[current]
    frames = [[sh for sh in s.shapes if sh.shape_type == 1 and sh.top == tb.top
               and abs(sh.left - (tb.left - Inches(0.16))) < Inches(0.02)][0] for tb in (blue, normal)]
    for one, two in (frames, (blue, normal)):
        one.left, two.left = two.left, one.left
        one.top, two.top = two.top, one.top
    set_only_run(blue, current)
    set_only_run(normal, "Week 12: K8s – ConfigMaps & Secrets")
    for sh in s.shapes:
        if sh.has_text_frame:
            for p in sh.text_frame.paragraphs:
                for r in p.runs:
                    r.text = r.text.replace("K8s – ", "Kubernetes – ").replace("K8s ", "Kubernetes ")
                    if r.font.size and r.font.size.pt == 10.5:
                        r.font.size = Pt(12)            # the body text minimum, also on the outline
    for sh in s.shapes:                                 # the right tiles ended at 12.91 in, past the footer rule
        if Inches(1.5) < sh.top < Inches(6.7) and sh.shape_type != 13:
            sh.left = sh.left - Inches(0.08)


def agenda(prs, items, size=18, after=9):
    s = prs.slides[1]
    old = [sh for sh in s.shapes if sh.name == "TextBox 3"][0]
    old._element.getparent().remove(old._element)
    bullets(s, 0.60, 1.75, 12.10, items, size=size, after=after)


def number_and_save(prs, built, title, out):
    total = len(built)
    for no, s in enumerate(built, 1):
        if no <= 3:
            for sh in s.shapes:
                if sh.has_text_frame and sh.text_frame.text.startswith("CLO835, Fall 2026"):
                    set_only_run(sh, "CLO835, Fall 2026     %d / %d" % (no, total))
        else:
            E.whale_and_footer(s, no, total)
    footer_guard(prs)
    finish(prs, title)
    E._sanitize_coords(prs)
    prs.save(out)
    print("wrote %s (%d slides)" % (out, total))


def set_pdf_info(path, title, author="Maziar Sojoudian"):
    """Add Title and Author to a PDF with an incremental update. The pages stay byte for byte."""
    data = open(path, "rb").read()
    tail = data[data.rindex(b"trailer"):]
    size = int(re.search(rb"/Size (\d+)", tail).group(1))
    root = re.search(rb"/Root (\d+ \d+ R)", tail).group(1)
    ident = re.search(rb"/ID \[[^\]]*\]", tail)
    prev = int(re.search(rb"startxref\s+(\d+)", tail).group(1))

    def esc(t):
        return t.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)").encode("latin-1")
    obj = b"%d 0 obj\n<< /Title (%s) /Author (%s) /Creator (Microsoft PowerPoint) >>\nendobj\n" % (
        size, esc(title), esc(author))
    start = len(data) + 1
    xref = b"xref\n%d 1\n%010d 00000 n \n" % (size, start)
    trailer = b"trailer\n<< /Size %d /Root %s /Info %d 0 R /Prev %d %s >>\nstartxref\n%d\n%%%%EOF\n" % (
        size + 1, root, size, prev, ident.group(0) if ident else b"", start + len(obj))
    open(path, "wb").write(data + b"\n" + obj + xref + trailer)


# ---------------------------------------------------------------- the manifests (lecture = lab)

FORTUNE = """apiVersion: v1
kind: Pod
metadata:
  name: fortune
spec:
  containers:
  - image: maziar/fortune:env
    name: html-generator
    env:
    - name: INTERVAL
      value: "10"
    volumeMounts:
    - name: html
      mountPath: /var/htdocs
  - image: nginx:alpine
    name: web-server
    volumeMounts:
    - name: html
      mountPath: /usr/share/nginx/html
      readOnly: true
    ports:
    - containerPort: 80
  volumes:
  - name: html
    emptyDir: {}""".split("\n")

# Lab Week 07 v3, Step 3: one YAML style.
GIT_POD = """apiVersion: v1
kind: Pod
metadata:
  name: gitrepo-volume-pod
spec:
  initContainers:
  - name: git-clone
    image: maziar/alpine-git
    args:
    - clone
    - --branch=master
    - https://github.com/sojoudian/kubia.git
    - /repo
    volumeMounts:
    - name: html
      mountPath: /repo
  containers:
  - image: nginx:alpine
    name: web-server
    volumeMounts:
    - name: html
      mountPath: /usr/share/nginx/html
      readOnly: true
  volumes:
  - name: html
    emptyDir: {}""".split("\n")

# Lab Week 07 v3, Step 4: maziar/alpine-curl replaces busybox.
HOSTPATH = """apiVersion: v1
kind: Pod
metadata:
  name: hostpath-pod
spec:
  nodeSelector:
    kubernetes.io/hostname: workernode1
  containers:
  - name: shell
    image: maziar/alpine-curl
    command: ["sleep", "3600"]
    volumeMounts:
    - name: node-data
      mountPath: /data
  volumes:
  - name: node-data
    hostPath:
      path: /tmp/clo835-week07
      type: DirectoryOrCreate""".split("\n")

SETTINGS = """spec:
  containers:
  - name: app
    image: maziar/kubia:v1
    volumeMounts:
    - name: cache
      mountPath: /cache
    - name: config
      mountPath: /etc/app/app.conf
      subPath: app.conf
      readOnly: true
  volumes:
  - name: cache
    emptyDir:
      medium: Memory
      sizeLimit: 64Mi
  - name: config
    configMap:
      name: app-config""".split("\n")

NFS_POD = """apiVersion: v1
kind: Pod
metadata:
  name: pod-using-my-nfs-volume
spec:
  containers:
  - image: maziar/kubia:v1
    name: container-using-my-nfs-volume
    volumeMounts:
    - mountPath: /my-nfs
      name: my-nfs-volume
  volumes:
  - name: my-nfs-volume
    nfs:
      server: 192.168.0.55
      path: "/exports/assets\"""".split("\n")

CLAIM = """# my-claim.yaml: the claim, then the Pod pod-using-my-claim
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-claim
spec:
  accessModes: [ReadWriteOnce]
  storageClassName: standard
  resources:
    requests: {storage: 1Gi}
# ... the Pod pod-using-my-claim names claimName: my-claim

$ kubectl apply -f my-claim.yaml
$ kubectl wait --for=condition=Ready pod/pod-using-my-claim --timeout=180s
$ kubectl get pvc,pv                # Bound, and a new PV""".split("\n")

EBS = """apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ebs-sc
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
volumeBindingMode: WaitForFirstConsumer
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-ebs-claim
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: ebs-sc
  resources:
    requests:
      storage: 4Gi""".split("\n")

COMMANDS = """# The volumes and the mounts of a Pod.
$ kubectl describe pod fortune
$ kubectl exec fortune -c web-server -- ls /usr/share/nginx/html

# The log of an init container.
$ kubectl logs gitrepo-volume-pod -c git-clone

# Volumes are not API objects. PersistentVolumes are.
$ kubectl get volumes
error: the server doesn't have a resource type "volumes"
$ kubectl get pv

# The events of a claim tell why it is Pending.
$ kubectl describe pvc my-claim""".split("\n")


# ---------------------------------------------------------------- the slides

def s_volumes(prs):
    return text_slide(prs, "Volumes in Kubernetes", [
        (0, "A volume is a directory that Kubernetes mounts into the containers of a Pod"),
        (0, "Each container has its own filesystem. The containers of a Pod share the network, but not the "
            "filesystem"),
        (0, "The containers of a Pod can share a volume. Each container can mount it at a different path"),
        (0, "You define a volume in the Pod specification, under `volumes`"),
        (0, "You mount the volume in each container that needs it, under `volumeMounts`"),
        (0, "Kubernetes mounts the volumes when the Pod starts. It unmounts them when the Pod stops")])


def s_purposes(prs):
    s = text_slide(prs, "What Volumes Are For", [
        (0, "Volumes have many purposes:"),
        (1, "Share files between the containers of a Pod (`emptyDir`)"),
        (1, "Share files between a container and its node (`hostPath`)"),
        (1, "Give configuration data from Kubernetes to the containers (`configMap`)"),
        (1, "Give credentials from Kubernetes to the containers (`secret`)"),
        (1, "Store persistent data for stateful services (`persistentVolumeClaim`, `nfs`)")])
    caution(s, 0.60, 4.75, 12.10, 1.05, "Kubernetes stores the data of a Secret in etcd with no encryption by "
            "default. An administrator must turn on encryption at rest for etcd. Week 12 teaches Secrets.")
    return s


def s_versus(prs):
    return text_slide(prs, "Volumes vs PersistentVolumes", [
        (0, "Volumes and PersistentVolumes have similar names, but they are different objects"),
        (0, "Volumes:"),
        (1, "are part of the Pod specification"),
        (1, "are not API objects, so `kubectl get volumes` gives an error"),
        (0, "PersistentVolumes:"),
        (1, "are API objects, so `kubectl get persistentvolumes` works"),
        (1, "represent real storage, for example a disk of a SAN (Storage Area Network) or an Amazon EBS "
            "(Elastic Block Store) volume"),
        (1, "connect to a Pod only through a PersistentVolumeClaim (PVC)"),
        (0, "Weeks 9 and 10 teach PersistentVolumes in detail")], size=17, after=7)


def s_types(prs):
    return text_slide(prs, "Volume Types", [
        (0, "`emptyDir`: an empty directory for temporary data"),
        (0, "`hostPath`: Kubernetes mounts a file or a directory of the node filesystem into the Pod"),
        (0, "`nfs`: Kubernetes mounts a share of an NFS (Network File System) server into the Pod"),
        (0, "`persistentVolumeClaim`: the name of a claim. The Week 10 lecture teaches claims"),
        (0, "`configMap`, `secret` and `downwardAPI`: configuration data, credentials and Pod information, as files"),
        (0, "`projected`: many of these sources in one directory"),
        (0, "`ephemeral`: a claim that Kubernetes creates for the Pod, and deletes with the Pod"),
        (0, "`csi`: a volume of a CSI (Container Storage Interface) driver, which the storage vendor supplies"),
        (0, "`image`: the files of an OCI image, read-only. It is beta in v1.35, and the container runtime must "
            "support it")], size=16, after=7)


def s_types2(prs):
    return text_slide(prs, "Volume Types, Continued", [
        (0, "`gitRepo`: deprecated. Since v1.33, Kubernetes turns it off by default"),
        (1, "The feature gate `GitRepoVolumeDriver` turns it on again. CVE-2024-10220 is the reason that it is off"),
        (1, "A ValidatingAdmissionPolicy can block the `gitRepo` type in a cluster"),
        (0, "An in-tree driver is part of the Kubernetes code. Kubernetes removed many of them. Use the CSI driver "
            "of the vendor:"),
        (1, "`awsElasticBlockStore` and `azureDisk`: removed in v1.27. Now `ebs.csi.aws.com` and `disk.csi.azure.com`"),
        (1, "`gcePersistentDisk`: removed in v1.28. Now `pd.csi.storage.gke.io`"),
        (1, "`azureFile`: removed in v1.30. Now `file.csi.azure.com`"),
        (1, "Also removed: `cephfs`, `cinder`, `flocker`, `glusterfs`, `photonPersistentDisk`, `quobyte`, `rbd`, "
            "`scaleIO`, `storageos` and `vsphereVolume`. `portworxVolume` is deprecated"),
        (0, "`flexVolume` is deprecated since v1.23. Use `csi`"),
        (0, "`local`, `iscsi` and `fc` (Fibre Channel): disks of a node or of a storage network. `local` works "
            "through a static PersistentVolume only")], size=15, after=6)


def s_table(prs):
    s = new_slide(prs, "Ephemeral and Persistent Volume Types")
    end = grid(s, 0.60, TOP + 0.10, [3.05, 2.60, 1.40, 1.85, 3.20], [
        ["Type", "Data lifetime", "Scope", "Many nodes", "Typical use"],
        ["`emptyDir`", "Ends with the Pod", "One Pod", "No", "Temporary files, files that containers share"],
        ["`hostPath`", "Stays on the node", "One node", "No", "Node agents, tests on one node"],
        ["`nfs`", "Stays on the NFS server", "The cluster", "Yes", "Files that many Pods share"],
        ["`persistentVolumeClaim`", "Stays after the Pod. The reclaim policy decides", "The cluster",
         "The access mode decides", "Databases, stateful services"]], row_h=0.80, size=14)
    rich(s, 0.60, end + 0.25, 12.10, 0.40, "The data of `configMap` and `secret` also ends with the Pod.", size=14)
    return s


def s_fortune_diagram(prs):
    s = new_slide(prs, "Two Containers Share an emptyDir")
    zone(s, 0.60, 1.70, 7.70, 4.85, "Pod fortune", color=STEPS[1], fill=E.CARD_BG)
    box(s, 0.95, 2.30, 3.10, 1.15, "html-generator\nmaziar/fortune:env", STEPS[3], size=14)
    box(s, 4.85, 2.30, 3.10, 1.15, "web-server\nnginx:alpine", STEPS[0], size=14)
    box(s, 2.20, 5.10, 4.50, 1.05, "emptyDir volume html", SLATE, size=15)
    arrow(s, DOWN, 2.40, 3.52, 0.38, 1.52, fill=STEPS[3])
    label(s, 2.85, 3.85, 1.95, 0.80, "writes to\n`/var/htdocs`", size=12.5, align=PP_ALIGN.LEFT)
    arrow(s, UP, 6.15, 3.52, 0.38, 1.52, fill=STEPS[0])
    label(s, 3.95, 3.85, 2.10, 0.80, "reads from\n`/usr/share/nginx/html`", size=12.5, align=PP_ALIGN.RIGHT)
    box(s, 10.95, 2.40, 1.80, 0.95, "Client", SLATE, size=14)
    flow(s, 8.02, 2.60, 2.86, "HTTP, port 80", kind=LEFT)
    rich(s, 8.75, 3.85, 4.00, 2.70, [
        "1. `html-generator` writes a new fortune into the volume every 10 seconds.",
        "2. `nginx` serves the same file from its own mount path, read-only.",
        "3. A client reads the fortune from `nginx` on port 80."], size=13.5, spacing=1.10, after=6)
    return s


def s_emptydir(prs):
    s = new_slide(prs, "Volume Type: emptyDir")
    bullets(s, 0.60, 1.75, 5.75, [
        (0, "Start with a Pod manifest"),
        (0, "Add a volume to the Pod, under `volumes`"),
        (0, "Mount the volume in each container, under `volumeMounts`"),
        (0, "If a volume has no type, Kubernetes makes it an `emptyDir`"),
        (0, "The volume hides the old files of the directory where Kubernetes mounts it"),
        (0, "`html-generator` writes a page into the volume. `nginx` serves the same page"),
        (0, "Lab Week 07, Step 1 uses this manifest")], size=16, after=8)
    term(s, 6.60, 1.48, 6.15, "fortune-pod.yaml", FORTUNE, size=11, h=5.22, spacing=1.0)
    return s


def s_settings(prs):
    s = new_slide(prs, "emptyDir and Mount Settings")
    bullets(s, 0.60, 1.75, 6.40, [
        (0, "`medium: Memory`: Kubernetes puts the volume in RAM (tmpfs). The files count against the memory limit "
            "of the container"),
        (0, "`sizeLimit`: the maximum size of the volume. The kubelet can evict the Pod when the volume uses more"),
        (0, "`readOnly: true`: the container can read the volume, but it cannot write to it"),
        (0, "`recursiveReadOnly: Enabled`: the mounts below the mount path are read-only too (stable in v1.33)"),
        (0, "`subPath`: mount one file or one subdirectory of the volume, not all of it")], size=15, after=9)
    term(s, 7.35, 1.48, 5.40, "settings-example.yaml (part of a Pod, not in the lab)", SETTINGS, size=12, spacing=1.12)
    return s


def s_lifecycle(prs):
    s = new_slide(prs, "Volume Lifecycle")
    bullets(s, 0.60, 1.62, 12.10, [
        (0, "The data in a volume stays when a container restarts"),
        (0, "Ephemeral volumes (`emptyDir`, `configMap`, `secret`) end with their Pod. Kubernetes creates them "
            "when it starts the Pod on a node, and deletes them with the Pod"),
        (0, "Persistent storage (PersistentVolumes, NFS, `hostPath`) does not end with the Pod. Kubernetes only "
            "unmounts or detaches it, so the data stays"),
        (0, "A provisioner can create remote storage for a claim. Kubernetes then attaches that storage to the node")],
        size=15, after=6, h=2.55)
    lanes = (("Pod", 4.90, STEPS[0], 4.30, 10.10, "The Pod runs"),
             ("`emptyDir` data", 5.45, STEPS[1], 4.30, 10.10, "Kubernetes creates it and deletes it with the Pod"),
             ("PV, NFS or `hostPath` data", 6.00, SLATE, 4.30, 12.75, "The data stays after the Pod ends"))
    for x, text in ((4.30, "1. The Pod starts"), (7.20, "2. A container restarts"), (10.10, "3. You delete the Pod")):
        E.add_rect(s, Inches(x - 0.015), Inches(4.72), Inches(0.03), Inches(1.80), E.MUTED)
        label(s, x - 1.30, 4.28, 2.60, 0.40, text, size=13, bold=True)
    for name, y, fill, x0, x1, text in lanes:
        label(s, 0.60, y, 2.70, 0.44, name, size=13, align=PP_ALIGN.LEFT, bold=True)
        box(s, x0, y, x1 - x0, 0.44, text, fill, size=12.5)
    return s


def s_git_diagram(prs):
    s = new_slide(prs, "Using a Git Repository in a Volume")
    rich(s, 0.60, 1.55, 12.10, 0.62, "The `gitRepo` type cloned a repository itself. It is deprecated, so an init "
         "container clones the repository into an `emptyDir` volume.", size=15)
    box(s, 0.60, 3.70, 2.10, 1.00, "User or controller", STEPS[5], size=14)
    flow(s, 2.78, 3.92, 1.00, "1.", kind=RIGHT)
    box(s, 4.10, 2.25, 2.50, 0.75, "Git repository", STEPS[4], size=14)
    zone(s, 3.85, 3.10, 5.85, 3.45, "Pod", color=STEPS[1], fill=E.CARD_BG)
    box(s, 4.10, 3.55, 2.50, 0.95, "Init container\ngit clone", STEPS[3], size=14)
    box(s, 6.95, 3.55, 2.50, 0.95, "Container\nnginx", STEPS[0], size=14)
    box(s, 4.60, 5.40, 4.35, 0.85, "emptyDir volume", SLATE, size=15)
    arrow(s, DOWN, 5.16, 3.02, 0.38, 0.52, fill=STEPS[4])
    label(s, 5.60, 3.02, 0.70, 0.50, "2.", size=13, bold=True, align=PP_ALIGN.LEFT)
    arrow(s, DOWN, 5.16, 4.53, 0.38, 0.85, fill=STEPS[3])
    label(s, 5.60, 4.65, 0.70, 0.50, "3.", size=13, bold=True, align=PP_ALIGN.LEFT)
    arrow(s, UP, 8.01, 4.53, 0.38, 0.85, fill=STEPS[0])
    label(s, 7.30, 4.65, 0.65, 0.50, "4.", size=13, bold=True, align=PP_ALIGN.RIGHT)
    rich(s, 9.95, 2.25, 2.80, 4.30, [
        "1. The user or a controller creates the Pod.",
        "2. The init container clones the repository.",
        "3. It writes the files into the volume. Then it stops.",
        "4. nginx starts. It serves the files of the volume."], size=13.5, spacing=1.10, after=8)
    return s


def s_git_pod(prs):
    s = new_slide(prs, "Pod Manifest with a Git Repository")
    term(s, 0.55, 1.48, 6.75, "gitrepo-volume-pod.yaml (Lab Week 07, Step 3)", GIT_POD, size=11, h=5.22, spacing=1.0)
    end = cards(s, 7.55, 1.50, 5.20, [
        ("initContainers:", "It runs to completion before nginx starts. It runs one time, so a new commit needs a "
                            "new Pod.", 0.98),
        ("image: maziar/alpine-git", "The ENTRYPOINT of the image is `git`, so `args` starts with `clone`.", 0.80),
        ("--branch=master", "Git checks out the master branch. Add `--depth=1` to copy only the last commit: "
                            "the clone is smaller.", 0.98),
        ("/repo", "Git clones into the root of the volume. nginx serves all of it, also the `.git` directory. "
                  "Do not use this method for a private repository.", 1.18)], gap=0.10)
    rich(s, 7.55, end + 0.10, 5.20, 0.62, "A native sidecar container (`restartPolicy: Always`, stable in v1.33) "
         "can pull new commits while the Pod runs.", size=12.5, color=E.MUTED)
    return s


def s_hostpath(prs):
    s = new_slide(prs, "hostPath: A Directory of the Node")
    term(s, 0.55, 1.50, 6.40, "hostpath-pod.yaml (Lab Week 07, Step 4)", HOSTPATH, size=12, spacing=1.12)
    end = cards(s, 7.20, 1.55, 5.55, [
        ("nodeSelector:", "The Pod runs on workernode1 again, so it finds the same directory.", 0.82),
        ("path: /tmp/clo835-week07", "A directory of the node. The data stays when you delete the Pod, but only on "
                                     "this node.", 0.98),
        ("type: DirectoryOrCreate", "Kubernetes creates the directory if it is not there. The other types are "
                                    "`Directory`, `File`, `FileOrCreate`, `Socket`, `CharDevice` and `BlockDevice`.",
         1.18)], gap=0.10)
    caution(s, 7.20, end + 0.05, 5.55, 1.40, "A `hostPath` volume gives the Pod access to the filesystem of the node. "
            "The Baseline Pod Security Standard forbids it. Use it for tests and node agents only.")
    return s


def s_nfs(prs):
    s = new_slide(prs, "Using an NFS Volume")
    end = term(s, 0.55, 1.50, 6.75, "pod-using-my-nfs-volume.yaml (example only: not in the lab)", NFS_POD, size=12,
               spacing=1.12)
    rich(s, 0.55, end + 0.20, 6.75, 1.00, [
        "The data stays on the server after the Pod ends.",
        "A Pod cannot set NFS mount settings. A PersistentVolume can, with `mountOptions`."],
        size=13.5, spacing=1.10, after=4)
    cards(s, 7.55, 1.55, 5.20, [
        ("nfs:", "The Pod mounts an NFS share directly, with no PersistentVolume. Each node needs an NFS client: the "
                 "`nfs-common` package on Ubuntu.", 1.20),
        ("server: 192.168.0.55", "An example address. You need your own NFS server, and each node must reach it.", 0.98),
        ("path: \"/exports/assets\"", "The directory that the NFS server exports.", 0.80),
        ("mountPath: /my-nfs", "The directory in the container. Many Pods on many nodes can read and write the "
                               "share at the same time.", 1.18)], gap=0.10)
    return s


def s_claim(prs):
    s = new_slide(prs, "A Claim and a StorageClass on the Course Cluster")
    bullets(s, 0.60, 1.75, 5.30, [
        (0, "A kubeadm cluster has no provisioner and no StorageClass at the start"),
        (0, "The lab installs the local-path provisioner (`rancher.io/local-path`). Its StorageClass `standard` is "
            "the default"),
        (0, "`WaitForFirstConsumer`: the provisioner waits for a Pod that uses the claim. Until then, the claim is "
            "Pending"),
        (0, "The provisioner creates a PersistentVolume: a directory on the node of the Pod"),
        (0, "`reclaimPolicy: Delete`: when you delete the claim, the provisioner deletes the PV and its directory. "
            "So the clean-up deletes the claim before the provisioner")],
        size=15, after=8)
    term(s, 6.15, 1.50, 6.60, "Lab Week 07, Step 5", CLAIM, size=11, spacing=1.12)
    return s


def s_ebs(prs):
    s = new_slide(prs, "Amazon EBS Volumes on Amazon EKS")
    bullets(s, 0.60, 1.75, 6.10, [
        (0, "The old `awsElasticBlockStore` type needed an EBS volume that you created outside of Kubernetes, and its "
            "ID in the Pod"),
        (0, "On Amazon EKS, the EBS CSI driver (`ebs.csi.aws.com`) creates and attaches the volumes:"),
        (1, "Install the Amazon EBS CSI driver add-on (`aws-ebs-csi-driver`)"),
        (1, "Give the driver an IAM role with the AWS managed policy that the EKS user guide names"),
        (1, "EKS Auto Mode includes a driver. Its provisioner is `ebs.csi.eks.amazonaws.com`"),
        (0, "The StorageClass `ebs-sc` tells the driver to create a `gp3` volume for each claim"),
        (0, "The course cluster has no EBS driver, so these manifests create no volume there")], size=15, after=7)
    term(s, 6.95, 1.50, 5.80, "ebs-sc-and-claim.yaml (example only: Amazon EKS)", EBS, size=11, spacing=1.10)
    return s


def s_commands(prs):
    s = new_slide(prs, "Commands and Troubleshooting")
    term(s, 0.55, 1.50, 6.95, "extra commands for the lab objects (not lab steps)", COMMANDS, size=11, spacing=1.15)
    cards(s, 7.75, 1.55, 5.00, [
        ("A claim stays Pending", "There is no default StorageClass. Or the class uses `WaitForFirstConsumer`, and no "
                                  "Pod uses the claim yet. Read the Events of the claim.", 1.42),
        ("An NFS mount fails", "The node has no NFS client (`nfs-common`), or it cannot reach the server. The Pod "
                               "stays in ContainerCreating.", 1.18),
        ("A gitRepo Pod fails", "The `gitRepo` driver is off (slide 8). Use an init container and an `emptyDir`.",
         0.98)], gap=0.12, size=12.5, mono=False)
    return s


def s_config(prs):
    return text_slide(prs, "Configuration for Applications", [
        (0, "Many applications need configuration"),
        (0, "An application can get its configuration from:"),
        (1, "command-line arguments"),
        (1, "environment variables"),
        (1, "configuration files"),
        (1, "configuration servers: a database, an API or another source"),
        (0, "Kubernetes gives this configuration to a container:"),
        (1, "`args` in the Pod specification gives the arguments"),
        (1, "`env` gives environment variables, also from a ConfigMap or a Secret"),
        (1, "a `configMap` or a `secret` in a volume gives configuration files"),
        (0, "The Week 12 lecture teaches ConfigMaps and Secrets")], size=17, after=5)


def s_takeaways(prs):
    return text_slide(prs, "Key Takeaways", [
        (0, "A volume is a directory that the containers of a Pod share. You define it in the Pod specification"),
        (0, "`emptyDir` data ends with the Pod. `hostPath` data stays on one node. NFS and PersistentVolume data stay "
            "after the Pod"),
        (0, "An init container and an `emptyDir` replace the deprecated `gitRepo` type"),
        (0, "A Pod uses persistent storage through a claim. A StorageClass and its provisioner create the volume"),
        (0, "Cloud disks use a CSI driver. Kubernetes removed their in-tree drivers")], size=18, after=12)


def s_next(prs):
    s = new_slide(prs, "Lab Week 07 and the Next Lectures")
    for k, (head, items, accent) in enumerate((
            ("Lab Week 07", ["Steps 1 and 2: an `emptyDir` and its lifecycle", "Step 3: an init container clones a "
                             "repository", "Step 4: a `hostPath` volume", "Step 5: a claim and a StorageClass"], STEPS[0]),
            ("Week 10 lecture", ["PersistentVolumes and claims", "StorageClasses and dynamic provisioning",
                                 "StatefulSets and headless Services"], STEPS[3]),
            ("Week 12 lecture", ["ConfigMaps", "Secrets", "Configuration files in a volume"], SLATE))):
        concept(s, 0.60 + k * 4.10, 1.80, 3.90, 3.10, head, items, accent)
    return s


def s_references(prs):
    return text_slide(prs, "References", [
        (0, "Volumes: `kubernetes.io/docs/concepts/storage/volumes/`"),
        (0, "Ephemeral volumes: `kubernetes.io/docs/concepts/storage/ephemeral-volumes/`"),
        (0, "PersistentVolumes: `kubernetes.io/docs/concepts/storage/persistent-volumes/`"),
        (0, "StorageClasses: `kubernetes.io/docs/concepts/storage/storage-classes/`"),
        (0, "Secrets: `kubernetes.io/docs/concepts/configuration/secret/`"),
        (0, "Sidecar containers: `kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/`"),
        (0, "Pod Security Standards: `kubernetes.io/docs/concepts/security/pod-security-standards/`"),
        (0, "Feature gates: `kubernetes.io/docs/reference/command-line-tools-reference/feature-gates/`"),
        (0, "The EBS CSI driver on EKS: `docs.aws.amazon.com/eks/latest/userguide/ebs-csi.html`")], size=15, after=8)


SLIDES = [s_volumes, s_purposes, s_versus, s_types, s_types2, s_table, s_fortune_diagram, s_emptydir, s_settings,
          s_lifecycle, s_git_diagram, s_git_pod, s_hostpath, s_nfs, s_claim, s_ebs, s_commands, s_config,
          s_takeaways, s_next, s_references]


def main():
    if os.path.exists(OUT) and "--force" not in sys.argv:
        sys.exit("%s exists. Bump VERSION; never overwrite a delivered deck." % OUT)
    prs = Presentation(SRC)
    keep_first(prs, 3)
    cover(prs, "Volumes: Attaching Disk", "Storage to Containers", 7)
    agenda(prs, [
        (0, "What a volume is, and what it is for"),
        (0, "Volume types, ephemeral and persistent"),
        (1, "`emptyDir` and the mount settings"),
        (1, "The volume lifecycle"),
        (1, "An init container that clones a Git repository"),
        (1, "`hostPath` and NFS"),
        (0, "An introduction to claims and StorageClasses"),
        (0, "Useful commands, and how to find a problem"),
        (0, "How applications get their configuration")])
    outline(prs, "Week 7: K8s – Volumes")
    built = [prs.slides[0], prs.slides[1], prs.slides[2]] + [make(prs) for make in SLIDES]
    number_and_save(prs, built, "CLO835 Week 7 Lecture: Volumes, Attaching Disk Storage to Containers", OUT)


if __name__ == "__main__":
    main()
