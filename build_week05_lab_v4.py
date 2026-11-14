# -*- coding: utf-8 -*-
"""CLO835 Week 05 - revise the lab deck so it covers the lecture.

The Week 05 lecture teaches five things the lab never practised, and the lab
script holds three steps that appear on no slide. This builder adds seven
slides and extends one, then renumbers every footer.

Input : Week05/Lab_week05_v3.pptx   (never written)
Output: Week05/Lab_week05_v4.pptx

It is guarded, so importing it writes nothing.
"""
import os, re, io
from pptx import Presentation
from pptx.util import Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR

SRC = "Week05/Lab_week05_v3.pptx"
OUT = "Week05/Lab_week05_v4.pptx"
EMU = 914400

BLUE, SLATE, MUTED, HAIRLINE = "1FA8E0", "37465A", "868686", "E0E0E0"
TERM_BG, TERM_BAR = "2A2A2A", "3A3A3A"
RED, AMBER, GREEN = "FF5F56", "FFBD2E", "27C93F"
CMD, OUTP = "4EC9E0", "BABABA"
CALIBRI, CONSOLAS = "Calibri", "Consolas"


def _i(v):
    return int(round(float(v)))


def E(inches):
    return _i(float(inches) * EMU)


def _txt(slide, x, y, w, h, lines, size, font, align=PP_ALIGN.LEFT,
         bold=False, colour=None, spacing=None):
    tb = slide.shapes.add_textbox(E(x), E(y), E(w), E(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.TOP
    for k, (text, col) in enumerate(lines):
        p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
        p.alignment = align
        if spacing:
            p.line_spacing = spacing
        r = p.add_run()
        r.text = text
        r.font.name = font
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = RGBColor.from_string(col or colour or SLATE)
    return tb


def _box(slide, x, y, w, h, fill):
    sp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, E(x), E(y), E(w), E(h))
    sp.fill.solid()
    sp.fill.fore_color.rgb = RGBColor.from_string(fill)
    sp.line.fill.background()
    sp.shadow.inherit = False
    sp.text_frame.text = ""
    return sp


def _dot(slide, x, y, fill):
    sp = slide.shapes.add_shape(MSO_SHAPE.OVAL, E(x), E(y), E(0.13), E(0.13))
    sp.fill.solid()
    sp.fill.fore_color.rgb = RGBColor.from_string(fill)
    sp.line.fill.background()
    sp.shadow.inherit = False
    return sp


def line_colour(s):
    t = s.strip()
    if t.startswith("#"):
        return GREEN
    if t.startswith("$") or t.startswith("k ") or t.startswith("kubectl"):
        return CMD
    return OUTP


def terminal_slide(prs, layout, whale, title, term_title, body):
    """One full-width house terminal, with the house title, whale and footer."""
    s = prs.slides.add_slide(layout)
    _txt(s, 0.55, 0.40, 12.20, 0.85, [(title, BLUE)], 32, CALIBRI, bold=True)
    _box(s, 0.55, 1.45, 12.20, 5.10, TERM_BG)
    _box(s, 0.55, 1.45, 12.20, 0.32, TERM_BAR)
    for k, col in enumerate((RED, AMBER, GREEN)):
        _dot(s, 0.70 + k * 0.17, 1.55, col)
    _txt(s, 0.55, 1.49, 12.20, 0.32, [(term_title, OUTP)], 10, CALIBRI,
         align=PP_ALIGN.CENTER)
    # A rendered line is about 0.212 in tall at 11 pt with 1.15 spacing, and the
    # frame leaves 4.58 in. Drop the size when a block runs longer than that.
    size = 11 if len(body) <= 21 else 9
    _txt(s, 0.73, 1.87, 11.88, 4.63,
         [(l, line_colour(l)) for l in body], size, CONSOLAS, spacing=1.15)
    if whale:
        s.shapes.add_picture(io.BytesIO(whale), E(0.45), E(6.85), E(0.50), E(0.50))
    c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, E(0.50), E(7.05), E(12.83), E(7.05))
    c.line.color.rgb = RGBColor.from_string(HAIRLINE)
    c.line.width = Pt(0.5)
    _txt(s, 9.50, 7.12, 3.35, 0.30, [("CLO835, Fall 2026     0 / 0", MUTED)],
         10, CALIBRI, align=PP_ALIGN.RIGHT)
    return s


# ------------------------------------------------------------------ content
SIDECAR = [
 "# A Pod may hold more than one container. They share one IP",
 "# address, so they reach each other on 127.0.0.1.",
 "$ cat > sidecar.yaml <<'EOF'",
 "apiVersion: v1",
 "kind: Pod",
 "metadata:",
 "  name: web-with-sidecar",
 "  labels:",
 "    app: web",
 "spec:",
 "  containers:",
 "  - name: web",
 "    image: nginx",
 "  - name: logger",
 "    image: alpine",
 "    command: [\"sh\", \"-c\", \"while true; do date; sleep 5; done\"]",
 "EOF",
 "$ kubectl apply -f sidecar.yaml",
 " ",
 "# READY reads 2/2. Use -c to pick which container you read.",
 "$ kubectl get pod web-with-sidecar",
 "$ kubectl logs web-with-sidecar -c logger",
]

LABELS = [
 "# A label is a key and a value. A selector picks objects by label.",
 "# Add labels to the pods you already created.",
 "$ kubectl label pod nginx app=web rel=stable",
 "$ kubectl label pod kubia app=kubia rel=beta",
 " ",
 "# Read them back.",
 "$ kubectl get pods --show-labels",
 " ",
 "# Select by label. A ReplicaSet uses the same mechanism.",
 "$ kubectl get pods -l app=web",
 "$ kubectl get pods -l 'rel in (stable,beta)'",
 "$ kubectl get pods -l app!=web",
 " ",
 "# Change one label, then select again. The result changes.",
 "$ kubectl label pod nginx rel=canary --overwrite",
 "$ kubectl get pods -l rel=canary",
]

RSMANIFEST = [
 "# Write a ReplicaSet by hand, the way the lecture shows it.",
 "$ cat > rs.yaml <<'EOF'",
 "apiVersion: apps/v1",
 "kind: ReplicaSet",
 "metadata:",
 "  name: kubia-rs",
 "spec:",
 "  replicas: 3",
 "  selector:",
 "    matchLabels:",
 "      app: kubia-rs",
 "  template:",
 "    metadata:",
 "      labels:",
 "        app: kubia-rs",
 "    spec:",
 "      containers:",
 "      - name: kubia",
 "        image: maziar/kubia",
 "EOF",
 "$ kubectl apply -f rs.yaml",
 " ",
 "# The selector is how the ReplicaSet finds the pods it owns.",
 "$ kubectl get rs kubia-rs",
 "$ kubectl get pods -l app=kubia-rs",
]

ROLLOUT = [
 "# A Deployment changes its image without stopping the service.",
 "# Move alpine 3.14 to 3.15.",
 "$ kubectl set image deployment/pingpong alpine=alpine:3.15 -n pingpong",
 " ",
 "# Watch the change finish.",
 "$ kubectl rollout status deployment/pingpong -n pingpong",
 " ",
 "# A second ReplicaSet appears. The first one scales down to zero.",
 "$ kubectl get all -n pingpong",
 "$ kubectl get rs -n pingpong",
]

ROLLBACK = [
 "# A Deployment keeps its old ReplicaSets, so you can go back.",
 "$ kubectl rollout history deployment/pingpong -n pingpong",
 " ",
 "# Go back one revision.",
 "$ kubectl rollout undo deployment/pingpong -n pingpong",
 "$ kubectl rollout status deployment/pingpong -n pingpong",
 " ",
 "# The old ReplicaSet scales up again. The new one scales to zero.",
 "$ kubectl get all -n pingpong",
 " ",
 "# This is why you never delete a ReplicaSet a Deployment owns.",
]

NODEPORT = [
 "# Nothing above left the cluster. Publish the nginx pod.",
 "$ kubectl expose pod nginx --type=NodePort --port=80 --name=nginx-http",
 " ",
 "# kubectl picks a random port. Pin it to 30000.",
 "$ kubectl patch svc nginx-http -p \\",
 "    '{\"spec\":{\"ports\":[{\"port\":80,\"targetPort\":80,\"nodePort\":30000}]}}'",
 "$ kubectl get svc nginx-http",
 " ",
 "# ON YOUR OWN MACHINE, read the public addresses.",
 "$ terraform output public_ips",
 " ",
 "# Open http://<any-node-public-ip>:30000/ in a browser.",
 "# EVERY node answers, not only the node that runs the pod.",
]

CLEANUP = [
 "# ON THE MASTER - remove the Kubernetes objects.",
 "$ bash cleanup_lab05.sh",
 " ",
 "# Confirm that nothing is left.",
 "$ kubectl get all --all-namespaces | grep -E 'nginx|kubia|pingpong'",
 " ",
 "# ON YOUR OWN MACHINE - remove the three EC2 machines.",
 "$ terraform destroy",
 " ",
 "# Always destroy. The Learner Lab budget is small.",
]

NEW = [
 # (position to insert at, 1-based, in the FINAL deck), title, term title, body
 (6,  "Two containers in one Pod",            "sidecar.yaml",       SIDECAR),
 (8,  "Labels and selectors",                 "bash",               LABELS),
 (10, "Creating a ReplicaSet from a descriptor", "rs.yaml",         RSMANIFEST),
 (12, "Rolling out a new version",            "bash",               ROLLOUT),
 (14, "Rollback - history and undo",          "bash",               ROLLBACK),
 (16, "Reach the Pod from your browser",      "bash",               NODEPORT),
 (17, "Clean up",                             "bash",               CLEANUP),
]

EXPLAIN = [
 " ",
 "# Read the schema before you write YAML.",
 "k explain pod.spec",
 "k explain pod.spec.containers",
]

FOOTER_RE = re.compile(r"^CLO835,\s+Fall\s+\d{4}\s+\d+\s*/\s*\d+$")


def whale_blob(prs):
    for s in prs.slides:
        for sh in s.shapes:
            if sh.shape_type == 13 and (sh.width or 0) < E(0.8):
                return sh.image.blob
    return None


def set_footer(slide, n, total):
    for sh in slide.shapes:
        if sh.has_text_frame and FOOTER_RE.match(sh.text_frame.text.strip()):
            runs = [r for p in sh.text_frame.paragraphs for r in p.runs]
            if not runs:
                return False
            runs[0].text = "CLO835, Fall 2026     %d / %d" % (n, total)
            for r in runs[1:]:
                r.text = ""
            return True
    return False


def sanitize(prs):
    ns = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
    fixed = 0
    for s in prs.slides:
        for el in s.shapes._spTree.iter():
            if el.tag in (ns+"off", ns+"ext", ns+"chOff", ns+"chExt"):
                for k in ("x", "y", "cx", "cy"):
                    v = el.get(k)
                    if v and ("." in v or "e" in v.lower()):
                        el.set(k, str(_i(float(v))))
                        fixed += 1
    return fixed


def move(prs, old, new):
    lst = prs.slides._sldIdLst
    ids = list(lst)
    el = ids[old]
    lst.remove(el)
    lst.insert(new, el)


def build():
    prs = Presentation(SRC)
    assert len(prs.slides._sldIdLst) == 11, "expected the 11-slide v3"
    whale = whale_blob(prs)
    layout = list(prs.slides)[3].slide_layout

    # 1. extend slide 5 with kubectl explain, in the free rows of its terminal
    s5 = list(prs.slides)[4]
    model = s5.shapes[16]          # the last one-line box of the left terminal
    runs = [r for p in model.text_frame.paragraphs for r in p.runs]
    size = runs[0].font.size.pt if runs and runs[0].font.size else 10
    for k, text in enumerate(EXPLAIN):
        y = 3.29 + 0.22 * (k + 1)
        _txt(s5, 0.73, y, 6.64, 0.24, [(text, line_colour(text))],
             size, CONSOLAS)

    # 2. append the new slides, then move each into place
    for pos, title, term, body in NEW:
        terminal_slide(prs, layout, whale, title, term, body)
        move(prs, len(prs.slides._sldIdLst) - 1, pos - 1)

    # 3. the old rollout slide now follows the new command slide
    S = list(prs.slides)
    for s in S:
        for sh in s.shapes:
            if sh.has_text_frame and sh.text_frame.text.strip().startswith(
                    "Rolling out a new version – Updating alpine"):
                r = [x for p in sh.text_frame.paragraphs for x in p.runs][0]
                r.text = "Rollout in progress - two ReplicaSets"

    # 4. renumber every footer
    S = list(prs.slides)
    total = sum(1 for s in S if s.element.get("show") != "0")
    n = 0
    ok = 0
    for s in S:
        if s.element.get("show") != "0":
            n += 1
        ok += 1 if set_footer(s, n, total) else 0

    f = sanitize(prs)
    prs.save(OUT)
    print("slides      : %d (%d visible)" % (len(S), total))
    print("footers set : %d" % ok)
    print("floats fixed: %d" % f)
    print("saved       : %s" % OUT)


if __name__ == "__main__":
    build()
