# -*- coding: utf-8 -*-
"""CLO835 Week 06 - repair the lecture deck.

The audit of 2026-10-14 found 14 defects in Week06_lecture_style_v5.pptx.
Three of them are kubectl commands that fail when a student copies them.
One more, found during the repair, is an Ingress manifest that uses an API
Kubernetes removed in version 1.22.

This builder reads v5 and writes v6. It never writes the input.
It is guarded, so an import writes nothing.

Input : Week06/Week06_lecture_style_v5.pptx
Output: Week06/Week06_lecture_style_v6.pptx
"""
import os, re, io, copy
from pptx import Presentation
from pptx.util import Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR

SRC = "Week06/Week06_lecture_style_v5.pptx"
OUT = "Week06/Week06_lecture_style_v6.pptx"
EMU = 914400

# ----------------------------------------------------------------- palette
BLUE, SLATE, TEAL = "1FA8E0", "37465A", "2196A0"
PALE, PALEBG, HAIR = "CFDBEE", "F4F7FB", "E0E0E0"
TERM_BG, TERM_BAR = "2A2A2A", "3A3A3A"
MUTED, GREY = "868686", "BABABA"
GREEN, RED, AMBER, TGREEN = "27AE60", "FF5F56", "FFBD2E", "27C93F"
CMD, OUTP = "4EC9E0", "BABABA"
B2, B3, B4 = "1F7AB8", "1F8FCD", "2466A0"
WHITE = "FFFFFF"
CALIBRI, CONSOLAS = "Calibri", "Consolas"


def _i(v):
    """python-pptx writes a float as "4288536.0"; PowerPoint then reads 0."""
    return int(round(float(v)))


def E(inches):
    return _i(float(inches) * EMU)


# ----------------------------------------------------------------- helpers
def drop(shape, slide=None):
    """Remove the shape. For a picture, drop the relationship as well.

    python-pptx keeps an image part that a relationship still names. Without
    this the deck keeps every screenshot inside the file.
    """
    if slide is not None and shape.shape_type == 13:
        rid = getattr(shape._element, "blip_rId", None)
        if rid:
            try:
                slide.part.drop_rel(rid)
            except KeyError:
                pass
    shape._element.getparent().remove(shape._element)


def txt(sl, x, y, w, h, lines, size, font=CALIBRI, align=PP_ALIGN.LEFT,
        bold=False, colour=SLATE, spacing=None, anchor=MSO_ANCHOR.TOP):
    tb = sl.shapes.add_textbox(E(x), E(y), E(w), E(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    for k, item in enumerate(lines):
        s, col = item if isinstance(item, tuple) else (item, colour)
        p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
        p.alignment = align
        if spacing:
            p.line_spacing = spacing
        r = p.add_run()
        r.text = s
        r.font.name = font
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = RGBColor.from_string(col)
    return tb


def box(sl, x, y, w, h, fill, shape=MSO_SHAPE.RECTANGLE, line=None, lw=1.0):
    sp = sl.shapes.add_shape(shape, E(x), E(y), E(w), E(h))
    if fill is None:
        sp.fill.background()
    else:
        sp.fill.solid()
        sp.fill.fore_color.rgb = RGBColor.from_string(fill)
    if line:
        sp.line.color.rgb = RGBColor.from_string(line)
        sp.line.width = Pt(lw)
    else:
        sp.line.fill.background()
    sp.shadow.inherit = False
    sp.text_frame.text = ""
    return sp


def tile(sl, x, y, w, h, label, fill, fg=WHITE, size=10, bold=True,
         shape=MSO_SHAPE.ROUNDED_RECTANGLE, line=None, sub=None):
    sp = box(sl, x, y, w, h, fill, shape=shape, line=line)
    tf = sp.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = E(0.04)
    tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    rows = [(label, fg, size, bold)]
    if sub:
        rows.append((sub, fg, size - 2, False))
    for k, (s, c, sz, bd) in enumerate(rows):
        p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = s
        r.font.name = CALIBRI
        r.font.size = Pt(sz)
        r.font.bold = bd
        r.font.color.rgb = RGBColor.from_string(c)
    return sp


def arrow(sl, x, y, w, h, fill=SLATE, right=True, down=False):
    """Axis-aligned arrows must be MSO_SHAPE arrows, not connectors."""
    s = MSO_SHAPE.DOWN_ARROW if down else MSO_SHAPE.RIGHT_ARROW
    if not down and not right:
        s = MSO_SHAPE.LEFT_ARROW
    sp = sl.shapes.add_shape(s, E(x), E(y), E(w), E(h))
    sp.fill.solid()
    sp.fill.fore_color.rgb = RGBColor.from_string(fill)
    sp.line.fill.background()
    sp.shadow.inherit = False
    sp.text_frame.text = ""
    return sp


def rule(sl, x1, y1, x2, y2, colour=HAIR, width=0.75, dash=False):
    c = sl.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, E(x1), E(y1), E(x2), E(y2))
    c.line.color.rgb = RGBColor.from_string(colour)
    c.line.width = Pt(width)
    if dash:
        from pptx.enum.dml import MSO_LINE_DASH_STYLE
        c.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    return c


def line_colour(s):
    t = s.strip()
    if t.startswith("#"):
        return TGREEN
    if t.startswith("$") or t.startswith("kubectl"):
        return CMD
    return OUTP


def terminal(sl, x, y, w, h, title, body, size=11, colour=None):
    """One house terminal panel inside the given box."""
    box(sl, x, y, w, h, TERM_BG)
    box(sl, x, y, w, 0.30, TERM_BAR)
    for k, col in enumerate((RED, AMBER, TGREEN)):
        d = box(sl, x + 0.14 + k * 0.17, y + 0.09, 0.12, 0.12, col, shape=MSO_SHAPE.OVAL)
    txt(sl, x, y + 0.04, w, 0.30, [(title, OUTP)], 10, align=PP_ALIGN.CENTER)
    pick = colour or line_colour
    txt(sl, x + 0.18, y + 0.40, w - 0.36, h - 0.52,
        [(l, pick(l)) for l in body], size, CONSOLAS, spacing=1.15)


def yaml_colour(s):
    t = s.strip()
    if t.startswith("#"):
        return TGREEN
    if t.startswith("$") or t.startswith("kubectl"):
        return CMD
    if ":" in t and not t.startswith("-"):
        return CMD
    return OUTP


def note(sl, x, y, w, h, lines, size=11):
    txt(sl, x, y, w, h, [(l, SLATE) for l in lines], size, CALIBRI,
        bold=True, spacing=1.1)


# ------------------------------------------------------- text repairs
# (slide number, exact old text, new text)
TEXT_FIX = [
 # --- slide 5: the sentence says "or creating" where it means "of creating"
 (5, "Rollout is a process or creating or upgrading application containers",
     "A rollout is the process that creates or upgrades the application containers"),
 # --- slide 4: one image name across the deck, and never an untagged image
 (4, "- name: nginx-container", "- name: kubia"),
 (4, "image: nginx", "image: maziar/kubia:1.0"),
 # --- slide 12: an EN DASH (U+2013) stands where kubectl needs two hyphens
 (12, "$ kubectl get pods –selector app=App1",
      "$ kubectl get pods --selector app=App1"),
 # --- slide 18: "b/w" is not an approved word
 (18, "Services enable connectivity b/w group of PODS",
      "A Service gives one stable address to a group of Pods"),
 # --- slide 19: card 3 was a fragment of card 2
 (19, "There are multiple service types; some of them allow external traffic",
      "Some Service types accept external traffic, such as NodePort and LoadBalancer"),
 (19, "(e.g. LoadBalancer and NodePort)",
      "A Service keeps one DNS name for the life of the application"),
 # --- slide 24: a stray word breaks the scale command
 (24, "# Create a deployment with single replica",
      "# Create a Deployment with one replica"),
 (24, "kubectl create deploy nginx-deployment --image=nginx",
      "kubectl create deploy kubia --image=maziar/kubia:1.0"),
 (24, "# Scale the deployment to 3 replicas",
      "# Scale the Deployment to three replicas"),
 (24, "kubectl scale deploy nginx-deployment --replicas=3 deployment",
      "kubectl scale deploy kubia --replicas=3"),
 (24, "# Expose the container on port 80",
      "# Create a ClusterIP Service on port 80"),
 (24, "kubectl expose deployment nginx-deployment --port=80",
      "kubectl expose deploy kubia --port=80 --target-port=8080"),
 # --- slide 25: kube-proxy does not create the Service. The API server does.
 (25, "Services are created by KubeProxy",
      "The API server creates the Service object"),
 (25, "Service is virtual no process, namespaces or interfaces unlike containers/PODS",
      "A Service is virtual. It has no process, no namespace and no interface"),
 (25, "Kube-Proxy creates fwding rules on each node in cluster i.e. any traffic to svc IP is fwded to POD ip",
      "Kube-proxy writes forwarding rules on each node. Traffic to the Service IP goes to a Pod IP"),
 (25, "Its actually IP and Port combination",
      "A Service is an IP address and a port together"),
 (25, "Kube-proxy creates and deletes the service rules (eg: for NodePort IPtable rule is created to fwd all traffic on all nodes to respective PODs)",
      "Kube-proxy adds and removes these rules. For a NodePort it adds a rule on every node"),
 # --- slide 27
 (27, "Under the hood: kube-proxy sets up a bunch of iptables rules on our nodes",
      "Kube-proxy writes a set of iptables rules on each node"),
 (27, "Sometimes, it’s the only available option for external traffic (e.g. most clusters deployed with kubeadm or on-premises)",
      "Sometimes it is the only option for external traffic, for example a kubeadm cluster"),
 (27, "Sometimes, it's the only available option for external traffic (e.g. most clusters deployed with kubeadm or on-premises)",
      "Sometimes it is the only option for external traffic, for example a kubeadm cluster"),
 # --- slide 28
 (28, "Algorithm used is Random", "The default algorithm is random"),
 (28, "Pods distributed across multiple nodes – When Svc created, K8s automatically creates our svc spanning across all nodes and maps the target port to same node port on all nodes enabling access from any node in cluster.",
      "The Pods are on different nodes. Kubernetes opens the same node port on every node, so any node accepts the traffic."),
 # --- slide 31
 (31, "It’s the default service type", "It is the default Service type"),
 (31, "It's the default service type", "It is the default Service type"),
 # --- slide 32
 (32, "Ips cannot be relied on as PODs get new Ips everytime",
      "Do not use a Pod IP address. A new Pod gets a new IP address"),
 (32, "To use a single interface a service is required.",
      "Use a Service to get one stable address"),
 (32, "We can have backend pods or redis pods created as service",
      "Put the backend Pods and the Redis Pods behind their own Service"),
 (32, "Each service gets an IP and name to be used to access service",
      "Each Service gets an IP address and a DNS name"),
 (32, "Cluster IP service can be used to access backend apps/Data stores",
      "Use a ClusterIP Service for a backend application or a data store"),
 (32, "Target Port is backend port and Port is the port on which service is exposed",
      "targetPort is the container port. port is the Service port"),
 # --- slide 33
 (33, "Each service of that type will typically cost a little bit of money",
      "Each Service of this type has a cost"),
 # --- slide 36: kubectl needs "--" before the command since version 1.18
 (36, "$ kubectl exec -it kubia-3inly bash",
      "$ kubectl exec -it kubia-3inly -- bash"),
 (36, "You’ve hit kubia-5asi2", "You've hit kubia-5asi2"),
 (36, "You’ve hit kubia-3inly", "You've hit kubia-3inly"),
 (36, "You’ve hit kubia-8awf3", "You've hit kubia-8awf3"),
 (36, "search default.svc.cluster.local svc.cluster.local cluster.local ..",
      "search default.svc.cluster.local svc.cluster.local cluster.local"),
]


def apply_text_fix(prs):
    """Replace at run level, then at paragraph level.

    A pattern can straddle two runs. A run-level pass alone misses it.
    """
    done = set()
    for n, old, new in TEXT_FIX:
        sl = prs.slides[n - 1]
        for sh in sl.shapes:
            if not sh.has_text_frame:
                continue
            for p in sh.text_frame.paragraphs:
                for r in p.runs:
                    if old in r.text:
                        r.text = r.text.replace(old, new)
                        done.add((n, old))
                joined = "".join(r.text for r in p.runs)
                if old in joined and p.runs:
                    p.runs[0].text = joined.replace(old, new)
                    for r in p.runs[1:]:
                        r.text = ""
                    done.add((n, old))
    missed = [(n, o[:48]) for n, o, _ in TEXT_FIX if (n, o) not in done]
    return missed


# ------------------------------------------------------- course outline
# The user's own schedule edit of 2026-07-15: a Study Week, the exam BEFORE
# ConfigMaps, and no Helm. The v5 grid had ConfigMaps before the exam.
OUTLINE = [
 ("Week 1",  "Docker Introduction"),
 ("Week 2",  "Docker Image Management"),
 ("Week 3",  "Docker Networking, Storage & Security"),
 ("Week 4",  "K8s Introduction"),
 ("Week 5",  "K8s – PODs, ReplicaSets"),
 ("Week 6",  "K8s – Services & Deployments"),
 ("Week 7",  "K8s – Volumes"),
 ("Week 8",  "Study Week"),
 ("Week 9",  "Persistent Volumes, EKS"),
 ("Week 10", "K8s – Storage Classes & StatefulSets"),
 ("Week 11", "Mid-Term Exam"),
 ("Week 12", "K8s – ConfigMaps & Secrets"),
 ("Week 13", "K8s – RBAC"),
 ("Week 14", "HPA & Final Project"),
 ("Week 15", "Final Project · Term End"),
]
TODAY = 5          # index of "Week 6" in OUTLINE


def rebuild_outline(sl):
    for sh in list(sl.shapes):
        keep = (sh.shape_type == 13                      # the whale
                or sh.shape_type == 9                    # the hairline
                or (sh.has_text_frame
                    and ("Course Outline" in sh.text_frame.text
                         or "CLO835" in sh.text_frame.text)))
        if not keep:
            drop(sh, sl)
    for k, (wk, topic) in enumerate(OUTLINE):
        col, row = k % 5, k // 5
        x = 0.55 + col * 2.48
        y = 1.70 + row * 1.65
        now = (k == TODAY)
        tl = box(sl, x, y, 2.30, 1.45, BLUE if now else PALEBG,
                 shape=MSO_SHAPE.ROUNDED_RECTANGLE,
                 line=None if now else HAIR)
        tf = tl.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = E(0.12)
        tf.margin_top = tf.margin_bottom = E(0.10)
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        rows = [(wk, WHITE if now else BLUE, 13, True),
                (topic, WHITE if now else SLATE, 11, False)]
        if now:
            rows.append(("Today", WHITE, 10, True))
        for j, (s, c, sz, bd) in enumerate(rows):
            p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
            p.alignment = PP_ALIGN.LEFT
            r = p.add_run()
            r.text = s
            r.font.name = CALIBRI
            r.font.size = Pt(sz)
            r.font.bold = bd
            r.font.color.rgb = RGBColor.from_string(c)


# ===================================================================
#  Native diagrams. Each one replaces a third-party screenshot.
#  Every position below is measured against the frame it sits in.
# ===================================================================

def d06_revisions(sl, x, y, w, h):
    """Rollout & Versioning - two revisions of the same Deployment."""
    box(sl, x, y, w, h, PALEBG, line=HAIR)
    txt(sl, x + 0.20, y + 0.22, 1.30, 0.26, [("Revision 1", MUTED)], 11, bold=True)
    txt(sl, x + 0.20, y + 1.42, 1.30, 0.26, [("Revision 2", MUTED)], 11, bold=True)
    for k in range(6):
        cx = x + 1.60 + k * 0.98
        tile(sl, cx, y + 0.18, 0.86, 0.46, "kubia", B3, sub="1.0", size=9)
        tile(sl, cx, y + 1.38, 0.86, 0.46, "kubia", GREEN, sub="2.0", size=9)
    arrow(sl, x + w / 2 - 0.16, y + 0.78, 0.32, 0.48, fill=BLUE, down=True)
    txt(sl, x + w / 2 + 0.26, y + 0.88, 2.60, 0.30,
        [("kubectl set image", BLUE)], 11, bold=True)
    txt(sl, x + 0.20, y + h - 0.44, w - 0.40, 0.30,
        [("One Deployment. One revision for each image tag.", MUTED)], 11)


def _pod_row(sl, x, y, n, label, fill, w=0.80, h=0.56, gap=0.14, sub=None):
    for k in range(n):
        tile(sl, x + k * (w + gap), y, w, h, label, fill, size=10, sub=sub)


def d07_rolling(sl, x, y, w, h):
    """Four steps of a rolling update."""
    panel = (w - 0.30) / 2
    ph = (h - 0.30) / 2
    steps = [("a", 3, 0), ("b", 2, 1), ("c", 1, 2), ("d", 0, 3)]
    for k, (tag, old, new) in enumerate(steps):
        px = x + (k % 2) * (panel + 0.30)
        py = y + (k // 2) * (ph + 0.30)
        box(sl, px, py, panel, ph, PALEBG, line=HAIR)
        txt(sl, px + 0.12, py + 0.08, 0.40, 0.24, [(tag + ".", MUTED)], 11, bold=True)
        tile(sl, px + 0.18, py + 0.80, 0.72, 0.62, "LB", B4, size=10)
        cx = px + 1.10
        for j in range(old):
            tile(sl, cx + j * 0.78, py + 0.42, 0.70, 0.52, "v1", B3, size=10)
        for j in range(new):
            tile(sl, cx + j * 0.78, py + 1.26, 0.70, 0.52, "v2", GREEN, size=10)
        txt(sl, cx, py + 0.98, 1.20, 0.22, [("old", MUTED)], 9)
        txt(sl, cx, py + 1.82, 1.20, 0.22, [("new", MUTED)], 9)
    txt(sl, x, y + h + 0.04, w, 0.26,
        [("Kubernetes removes one old Pod only after a new Pod is ready.", MUTED)], 11)


def d08_recreate(sl, x, y, w, h):
    """Three steps of a recreate update, with the outage in the middle."""
    pw = (w - 0.40) / 3
    for k, (tag, n, fill, cap) in enumerate(
            [("a", 3, B3, "v1 serves traffic"),
             ("b", 3, GREY, "all Pods stop"),
             ("c", 3, GREEN, "v2 serves traffic")]):
        px = x + k * (pw + 0.20)
        box(sl, px, y, pw, h - 0.50, PALEBG, line=HAIR)
        txt(sl, px + 0.12, y + 0.10, 0.40, 0.24, [(tag + ".", MUTED)], 11, bold=True)
        tile(sl, px + 0.18, y + 1.70, 0.70, 0.60, "LB", B4, size=10)
        for j in range(n):
            tile(sl, px + 1.05, y + 0.70 + j * 0.78, pw - 1.25, 0.60,
                 "v1" if k == 0 else ("v1" if k == 1 else "v2"), fill, size=10)
        txt(sl, px + 0.12, y + h - 0.76, pw - 0.24, 0.26,
            [(cap, MUTED)], 10, align=PP_ALIGN.CENTER)
    box(sl, x + pw + 0.20, y + h - 0.44, pw, 0.36, RED,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    txt(sl, x + pw + 0.20, y + h - 0.37, pw, 0.26,
        [("Application down", WHITE)], 11, bold=True, align=PP_ALIGN.CENTER)


def d09_strategy(sl, x, y, w, h):
    """Recreate against RollingUpdate on one timeline."""
    rows = [("Recreate", True), ("Rolling update", False)]
    for ri, (name, recreate) in enumerate(rows):
        ry = y + ri * (h / 2)
        tile(sl, x, ry + 0.55, 1.40, 0.56, name, B4, size=11)
        if recreate:
            for k in range(5):
                tile(sl, x + 1.70 + k * 0.92, ry + 0.30, 0.82, 0.52,
                     "kubia", B3, sub="1.0", size=9)
                arrow(sl, x + 1.70 + k * 0.92 + 0.33, ry + 0.90, 0.16, 0.42,
                      fill=RED, down=True)
            box(sl, x + 6.40, ry + 0.30, 1.30, 1.10, RED,
                shape=MSO_SHAPE.ROUNDED_RECTANGLE)
            txt(sl, x + 6.40, ry + 0.62, 1.30, 0.50,
                [("Application", WHITE), ("down", WHITE)], 11, bold=True,
                align=PP_ALIGN.CENTER)
            for k in range(5):
                tile(sl, x + 7.90 + k * 0.68, ry + 0.30, 0.62, 0.52,
                     "kubia", GREEN, sub="2.0", size=8)
        else:
            for k in range(10):
                new = k % 2 == 1
                tile(sl, x + 1.70 + k * 0.92, ry + 0.30, 0.82, 0.52,
                     "kubia", GREEN if new else B3,
                     sub="2.0" if new else "1.0", size=9)
                arrow(sl, x + 1.70 + k * 0.92 + 0.33, ry + 0.90, 0.16, 0.42,
                      fill=GREEN if new else RED, down=True)
        txt(sl, x + 1.70, ry + 1.38, 9.40, 0.26,
            [("no request is lost" if not recreate
              else "every Pod stops before the new Pod starts", MUTED)], 10)


S10_ROWS = [
 ("Create",   ["kubectl create -f deployment.yaml"]),
 ("Get",      ["kubectl get deployments"]),
 ("Update",   ["kubectl apply -f deployment.yaml",
               "kubectl set image deployment/kubia kubia=maziar/kubia:2.0"]),
 ("Status",   ["kubectl rollout status deployment/kubia",
               "kubectl rollout history deployment/kubia"]),
 ("Rollback", ["kubectl rollout undo deployment/kubia"]),
]


def d10_summary(sl, x, y, w, h):
    """The command summary, as house terminal bars instead of a screenshot."""
    lines = sum(len(c) for _, c in S10_ROWS)
    bar = 0.44
    gap = (h - lines * bar) / (lines + 1)
    i = 0
    for label, cmds in S10_ROWS:
        top = y + gap + i * (bar + gap)
        tile(sl, x, top, 1.60, bar, label, B4, size=11)
        for j, c in enumerate(cmds):
            ty = y + gap + (i + j) * (bar + gap)
            box(sl, x + 1.85, ty, w - 1.85, bar, TERM_BG)
            txt(sl, x + 2.00, ty + 0.11, w - 2.15, bar,
                [("$ " + c, CMD)], 12, CONSOLAS)
        i += len(cmds)


def d11_labels(sl, x, y, w, h):
    """Labels recap - the same Pods, without labels and with labels."""
    half = (w - 0.40) / 2
    box(sl, x, y, half, h, PALEBG, line=HAIR)
    txt(sl, x + 0.15, y + 0.14, half - 0.30, 0.28,
        [("No labels - one flat set", MUTED)], 11, bold=True)
    for k in range(12):
        tile(sl, x + 0.25 + (k % 4) * 0.98, y + 0.60 + (k // 4) * 0.74,
             0.86, 0.56, "Pod", B3, size=10)
    rx = x + half + 0.40
    box(sl, rx, y, half, h, PALEBG, line=HAIR)
    txt(sl, rx + 0.15, y + 0.14, half - 0.30, 0.28,
        [("With labels - three groups", MUTED)], 11, bold=True)
    groups = [("app=kubia", B3), ("app=auth", TEAL), ("app=db", B4)]
    for g, (name, col) in enumerate(groups):
        gy = y + 0.60 + g * 0.74
        txt(sl, rx + 0.20, gy + 0.16, 1.30, 0.26, [(name, SLATE)], 10, bold=True)
        for k in range(4):
            tile(sl, rx + 1.60 + k * 0.90, gy, 0.80, 0.56, "Pod", col, size=10)


def d12_selector(sl, x, y, w, h):
    """Labels and selectors - a selector picks one labelled group."""
    box(sl, x, y, w, h, PALEBG, line=HAIR)
    pods = [("App1", "Front-end", B3), ("App2", "Web-Servers", TEAL),
            ("App3", "Auth", B4), ("App4", "Image-proc", B2),
            ("App5", "DB", SLATE)]
    for k, (app, fn, col) in enumerate(pods):
        px = x + 0.22 + (k % 3) * 1.92
        py = y + 0.22 + (k // 3) * 1.06
        tile(sl, px, py, 1.78, 0.40, "app=" + app, col, size=10)
        tile(sl, px, py + 0.44, 1.78, 0.40, "function=" + fn, PALE,
             fg=SLATE, size=10)


def d12_pick(sl, x, y, w, h):
    """The one Pod that the selector returns."""
    box(sl, x, y, w, h, PALEBG, line=HAIR)
    txt(sl, x + 0.18, y + 0.14, w - 0.36, 0.28,
        [("--selector app=App1 returns one group", MUTED)], 11, bold=True)
    tile(sl, x + 0.22, y + 0.54, 1.90, 0.40, "app=App1", B3, size=10)
    tile(sl, x + 0.22, y + 0.98, 1.90, 0.40, "function=Front-end", PALE,
         fg=SLATE, size=10)
    arrow(sl, x + 2.30, y + 0.78, 0.60, 0.34, fill=BLUE)
    tile(sl, x + 3.05, y + 0.66, 1.70, 0.62, "1 Pod", GREEN, size=12)


def d13_traditional(sl, x, y, w, h):
    """A virtual machine against a named group of machines."""
    half = (w - 0.50) / 2
    box(sl, x, y, half, h, PALEBG, line=HAIR)
    txt(sl, x + 0.18, y + 0.16, half - 0.36, 0.30,
        [("A virtual machine - one box", BLUE)], 13, bold=True)
    for k, (name, col) in enumerate([("Web App", B3), ("Nginx", TEAL),
                                     ("Vault agent", B4)]):
        tile(sl, x + 0.40, y + 0.70 + k * 0.72, half - 0.80, 0.56, name, col, size=11)
    tile(sl, x + 0.40, y + 2.92, half - 0.80, 0.56, "Kernel", SLATE, size=11)
    txt(sl, x + 0.18, y + h - 0.60, half - 0.36, 0.44,
        [("One address, for example 192.168.10.5", MUTED)], 11)
    rx = x + half + 0.50
    box(sl, rx, y, half, h, PALEBG, line=HAIR)
    txt(sl, rx + 0.18, y + 0.16, half - 0.36, 0.30,
        [("A service - a named group of boxes", BLUE)], 13, bold=True)
    for k in range(8):
        tile(sl, rx + 0.30 + (k % 4) * 1.08, y + 0.70 + (k // 4) * 0.72,
             0.96, 0.56, "Box %02d" % (k + 1), B3, size=10)
    tile(sl, rx + 0.90, y + 2.60, half - 1.80, 0.52, "Service discovery",
         B4, size=11)
    txt(sl, rx + 0.18, y + h - 0.60, half - 0.36, 0.44,
        [("The clients use the name, never the address.", MUTED)], 11)


def d14_discovery(sl, x, y, w, h):
    """Server-side discovery - the client only knows the load balancer."""
    box(sl, x, y, w, h, PALEBG, line=HAIR)
    tile(sl, x + 0.25, y + 1.60, 1.30, 0.70, "Client", B4, size=12)
    arrow(sl, x + 1.65, y + 1.82, 0.60, 0.26, fill=SLATE)
    tile(sl, x + 2.35, y + 1.50, 1.60, 0.90, "Load", B3, sub="balancer", size=12)
    txt(sl, x + 2.35, y + 1.16, 1.60, 0.26, [("10.4.32.1", MUTED)], 10,
        align=PP_ALIGN.CENTER)
    box(sl, x + 4.35, y + 0.35, w - 4.70, 2.60, None, line=SLATE, lw=1.25)
    txt(sl, x + 4.45, y + 0.10, 2.60, 0.26, [("foobar service", SLATE)], 11, bold=True)
    for k in range(4):
        tile(sl, x + 4.55, y + 0.60 + k * 0.58, 1.60, 0.46,
             "instance #%02d" % (k + 1), B3, size=9)
        txt(sl, x + 6.30, y + 0.68 + k * 0.58, 1.40, 0.26,
            [("172.16.0.%d" % (18 + k * 7), MUTED)], 9)
    arrow(sl, x + 3.98, y + 1.76, 0.30, 0.26, fill=SLATE)
    tile(sl, x + 2.20, y + 3.15, 1.90, 0.60, "Service registry", SLATE, size=11)
    arrow(sl, x + 3.05, y + 2.48, 0.22, 0.60, fill=TEAL, down=True)
    txt(sl, x + 0.25, y + 3.20, 1.80, 0.50,
        [("The registry holds", MUTED), ("the live addresses.", MUTED)], 10)
    txt(sl, x + 4.35, y + 3.20, w - 4.70, 0.50,
        [("A new instance adds an entry. A failed instance loses its entry.", MUTED)], 10)


def d15_similar(sl, x, y, w, h):
    """One Service in front of two Deployments that share one label."""
    box(sl, x, y, w, h, PALEBG, line=HAIR)
    half = (w - 0.60) / 2
    for k, (name, ver, col) in enumerate([("Deployment 1", "ver=release", B3),
                                          ("Deployment 2", "ver=canary", TEAL)]):
        dx = x + 0.20 + k * (half + 0.20)
        box(sl, dx, y + 0.22, half, 1.60, WHITE, line=HAIR)
        txt(sl, dx + 0.12, y + 0.32, half - 0.24, 0.26, [(name, SLATE)], 11, bold=True)
        txt(sl, dx + 0.12, y + 0.60, half - 0.24, 0.26,
            [("app=foo  " + ver, MUTED)], 10, CONSOLAS)
        for j in range(4):
            tile(sl, dx + 0.16 + j * (half - 0.32) / 4, y + 0.92, 
                 (half - 0.32) / 4 - 0.08, 0.52, "Pod", col, size=9)
    arrow(sl, x + w / 2 - 0.16, y + 1.95, 0.32, 0.46, fill=BLUE, down=True)
    tile(sl, x + w / 2 - 1.70, y + 2.52, 3.40, 0.74, "service/foo", B4, size=14)
    txt(sl, x + w / 2 - 2.40, y + 3.34, 4.80, 0.28,
        [("foo.default.svc.cluster.local", TEAL)], 12, CONSOLAS,
        align=PP_ALIGN.CENTER)
    txt(sl, x + 0.20, y + 3.80, w - 0.40, 0.56,
        [("The Service matches on the label app=foo. It knows nothing about a "
          "Deployment or a ReplicaSet.", MUTED)], 11)


def d18_services(sl, x, y, w, h):
    """Each tier answers on its own Service."""
    box(sl, x, y, w, h, PALEBG, line=HAIR)
    tiers = [("front end", B3), ("back end", TEAL), ("database", SLATE)]
    band = (h - 0.95) / 3
    for k, (name, col) in enumerate(tiers):
        by = y + 0.30 + k * band
        tile(sl, x + 0.20, by, 1.70, 0.52, "Service", col, size=11)
        txt(sl, x + 0.20, by + 0.56, 1.70, 0.24, [(name, MUTED)], 10,
            align=PP_ALIGN.CENTER)
        arrow(sl, x + 2.02, by + 0.13, 0.38, 0.26, fill=SLATE)
        pods = 2 if k < 2 else 1
        for j in range(pods):
            tile(sl, x + 2.55 + j * 1.25, by, 1.15, 0.52, "Pod", col, size=10)
        if k < 2:
            arrow(sl, x + 0.90, by + 0.84, 0.26, band - 0.84, fill=BLUE, down=True)
    txt(sl, x + 0.20, y + h - 0.38, w - 0.40, 0.28,
        [("Each tier calls the next tier by its Service name.", MUTED)], 11)


def d20_access(sl, x, y, w, h):
    """A laptop reaches a Pod through a node port."""
    box(sl, x, y, w, h, PALEBG, line=HAIR)
    tile(sl, x + 0.18, y + h / 2 - 0.34, 1.15, 0.68, "Laptop", B4, size=11)
    arrow(sl, x + 1.42, y + h / 2 - 0.13, 0.36, 0.26, fill=BLUE)
    nx, nw = x + 1.90, w - 2.10
    box(sl, nx, y + 0.22, nw, h - 0.72, WHITE, line=HAIR)
    txt(sl, nx + 0.12, y + 0.28, 1.40, 0.24, [("Node", MUTED)], 10, bold=True)
    rows = [("port 30000", AMBER, SLATE), ("Service", B3, WHITE),
            ("Pod   8080", TEAL, WHITE)]
    for k, (lab, col, fg) in enumerate(rows):
        ry = y + 0.62 + k * 0.84
        tile(sl, nx + 0.35, ry, nw - 0.70, 0.46, lab, col, fg=fg, size=11)
        if k < 2:
            arrow(sl, nx + nw / 2 - 0.10, ry + 0.50, 0.20, 0.26, fill=SLATE,
                  down=True)
    txt(sl, x + 0.18, y + h - 0.40, w - 0.36, 0.28,
        [("The node port is open on every node.", MUTED)], 11)


def d21_intro(sl, x, y, w, h):
    """Traffic reaches the Pods through one Service."""
    box(sl, x, y, w, h, PALEBG, line=HAIR)
    cx = x + w / 2
    txt(sl, x, y + 0.14, w, 0.28, [("Traffic", SLATE)], 12, bold=True,
        align=PP_ALIGN.CENTER)
    arrow(sl, cx - 0.14, y + 0.48, 0.28, 0.34, fill=SLATE, down=True)
    tile(sl, cx - 1.20, y + 0.88, 2.40, 0.62, "LoadBalancer", B4, size=11)
    arrow(sl, cx - 0.14, y + 1.56, 0.28, 0.34, fill=SLATE, down=True)
    box(sl, x + 0.25, y + 1.96, w - 0.50, h - 2.36, WHITE, line=HAIR)
    txt(sl, x + 0.38, y + 2.02, 1.60, 0.24, [("Cluster", MUTED)], 10, bold=True)
    tile(sl, cx - 1.20, y + 2.34, 2.40, 0.62, "Service", B3, size=11)
    for k in range(3):
        px = x + 0.55 + k * ((w - 1.10) / 3)
        arrow(sl, px + (w - 1.10) / 6 - 0.11, y + 3.02, 0.22, 0.30,
              fill=SLATE, down=True)
        tile(sl, px, y + 3.38, (w - 1.10) / 3 - 0.18, 0.62, "Pod", TEAL, size=11)


def d22_types(sl, x, y, w, h):
    """The four Service types, one quadrant each."""
    qw = (w - 0.26) / 2
    qh = (h - 0.26) / 2
    quads = [("ClusterIP", "inside the cluster only", B3),
             ("NodePort", "a port on every node", TEAL),
             ("LoadBalancer", "one external address", B4),
             ("ExternalName", "a DNS CNAME, no proxy", SLATE)]
    for k, (name, cap, col) in enumerate(quads):
        qx = x + (k % 2) * (qw + 0.26)
        qy = y + (k // 2) * (qh + 0.26)
        box(sl, qx, qy, qw, qh, PALEBG, line=HAIR)
        tile(sl, qx + 0.14, qy + 0.14, qw - 0.28, 0.46, name, col, size=12)
        txt(sl, qx + 0.14, qy + 0.68, qw - 0.28, 0.26, [(cap, MUTED)], 10,
            align=PP_ALIGN.CENTER)
        if k == 3:
            tile(sl, qx + 0.45, qy + 1.10, qw - 0.90, 0.52, "external host", GREY,
                 fg=SLATE, size=10)
        else:
            tile(sl, qx + 0.45, qy + 1.06, qw - 0.90, 0.42, "Service", col, size=10)
            for j in range(3):
                tile(sl, qx + 0.22 + j * ((qw - 0.44) / 3), qy + 1.62,
                     (qw - 0.44) / 3 - 0.10, 0.42, "Pod", PALE, fg=SLATE, size=9)


def d23_accessing(sl, x, y, w, h):
    """The three ways to reach a ClusterIP Service."""
    box(sl, x, y, w, h, PALEBG, line=HAIR)
    rows = [("1", "Run a Pod in the cluster, then call the Service name"),
            ("2", "Use kubectl exec, then run curl inside a Pod"),
            ("3", "Open an SSH session to a node, then run curl")]
    for k, (n, s) in enumerate(rows):
        ry = y + 0.26 + k * 0.76
        tile(sl, x + 0.22, ry, 0.46, 0.46, n, B4, size=12, shape=MSO_SHAPE.OVAL)
        txt(sl, x + 0.85, ry + 0.10, w - 1.10, 0.32, [(s, SLATE)], 11)
    box(sl, x + 0.22, y + 2.62, w - 0.44, 0.52, TERM_BG)
    txt(sl, x + 0.38, y + 2.74, w - 0.70, 0.34,
        [("$ kubectl exec -it kubia-7nog1 -- curl http://kubia", CMD)], 11, CONSOLAS)


def d25_kubeproxy(sl, x, y, w, h):
    """The API server tells kube-proxy on each node to write the rules."""
    box(sl, x, y, w, h, PALEBG, line=HAIR)
    tile(sl, x + w / 2 - 1.40, y + 0.16, 2.80, 0.50, "kube-apiserver", B4, size=11)
    nw = (w - 0.80) / 3
    for k in range(3):
        nx = x + 0.20 + k * (nw + 0.20)
        box(sl, nx, y + 0.94, nw, h - 1.40, WHITE, line=HAIR)
        arrow(sl, nx + nw / 2 - 0.10, y + 0.70, 0.20, 0.22, fill=SLATE, down=True)
        tile(sl, nx + 0.12, y + 1.08, nw - 0.24, 0.40, "kubelet", B3, size=10)
        tile(sl, nx + 0.12, y + 1.56, nw - 0.24, 0.40, "kube-proxy", TEAL, size=10)
        tile(sl, nx + 0.12, y + 2.06, nw - 0.24, 0.40, "iptables rules", AMBER,
             fg=SLATE, size=10)
        txt(sl, nx, y + h - 0.34, nw, 0.26,
            [("node %d" % (k + 1), MUTED)], 10, align=PP_ALIGN.CENTER)
    txt(sl, x + 0.20, y + h - 0.02, w - 0.40, 0.26, [("", MUTED)], 9)


def d26_howitworks(sl, x, y, w, h):
    """The path of one request, from the client to a Pod."""
    box(sl, x, y, w, h, PALEBG, line=HAIR)
    tile(sl, x + 0.25, y + 0.20, 1.40, 0.56, "etcd", SLATE, size=11)
    arrow(sl, x + 1.75, y + 0.36, 0.50, 0.24, fill=SLATE)
    tile(sl, x + 2.40, y + 0.20, 2.10, 0.56, "kube-apiserver", B4, size=11)
    half = (w - 0.70) / 2
    for k in range(2):
        nx = x + 0.25 + k * (half + 0.20)
        box(sl, nx, y + 1.20, half, h - 1.70, WHITE, line=HAIR)
        txt(sl, nx + 0.12, y + 1.26, 1.40, 0.24,
            [("node %d" % (k + 1), MUTED)], 10, bold=True)
        tile(sl, nx + 0.20, y + 1.60, half - 0.40, 0.44, "kube-proxy", TEAL, size=10)
        arrow(sl, nx + half / 2 - 0.10, y + 2.10, 0.20, 0.26, fill=SLATE, down=True)
        tile(sl, nx + 0.20, y + 2.42, half - 0.40, 0.44, "iptables", AMBER,
             fg=SLATE, size=10)
        tile(sl, nx + 0.20, y + 3.00, half - 0.40, 0.44,
             "Pod of service A" if k == 0 else "no Pod of service A",
             B3 if k == 0 else GREY, fg=WHITE if k == 0 else SLATE, size=10)
    txt(sl, x + 0.25, y + h - 0.40, w - 0.50, 0.32,
        [("A request to the Service IP on node 2 still reaches the Pod on node 1.",
          MUTED)], 11)


def d27_nodeport(sl, x, y, w, h):
    """An external client reaches the Service through any node."""
    box(sl, x, y, w, h, PALEBG, line=HAIR)
    tile(sl, x + w / 2 - 1.10, y + 0.18, 2.20, 0.48, "external client", B4, size=11)
    arrow(sl, x + w / 2 - 0.11, y + 0.70, 0.22, 0.26, fill=SLATE, down=True)
    tile(sl, x + 0.60, y + 1.02, w - 1.20, 0.48, "Service", B3, size=11)
    half = (w - 0.70) / 2
    for k in range(2):
        nx = x + 0.25 + k * (half + 0.20)
        arrow(sl, nx + half / 2 - 0.10, y + 1.56, 0.20, 0.26, fill=SLATE, down=True)
        box(sl, nx, y + 1.92, half, h - 2.30, WHITE, line=HAIR)
        tile(sl, nx + 0.22, y + 2.10, half - 0.44, 0.46, "port 30123", AMBER,
             fg=SLATE, size=10)
        arrow(sl, nx + half / 2 - 0.09, y + 2.64, 0.18, 0.24, fill=SLATE, down=True)
        tile(sl, nx + 0.22, y + 2.98, half - 0.44, 0.46, "Pod   8080", TEAL, size=10)
        txt(sl, nx, y + h - 0.36, half, 0.26,
            [("node %d" % (k + 1), MUTED)], 10, align=PP_ALIGN.CENTER)


def d28_ports(sl, x, y, w, h):
    """The three ports of a NodePort Service."""
    box(sl, x, y, w, h, PALEBG, line=HAIR)
    rows = [("3", "nodePort", "30000-32767", "on every node", AMBER, SLATE),
            ("2", "port", "80", "on the Service", B3, WHITE),
            ("1", "targetPort", "8080", "on the container", TEAL, WHITE)]
    for k, (n, name, val, where, col, fg) in enumerate(rows):
        ry = y + 0.26 + k * 0.94
        tile(sl, x + 0.22, ry + 0.06, 0.46, 0.46, n, B4, size=12,
             shape=MSO_SHAPE.OVAL)
        tile(sl, x + 0.86, ry, 1.70, 0.58, name, col, fg=fg, size=11)
        txt(sl, x + 2.72, ry + 0.06, 1.60, 0.30, [(val, SLATE)], 13, CONSOLAS,
            bold=True)
        txt(sl, x + 2.72, ry + 0.34, w - 3.00, 0.26, [(where, MUTED)], 10)


def d29_manifest(sl, x, y, w, h):
    """The Service manifest, in a house terminal, with the three notes."""
    body = [
        "apiVersion: v1",
        "kind: Service",
        "metadata:",
        "  name: kubia",
        "spec:",
        "  ports:",
        "  - port: 80",
        "    targetPort: 8080",
        "  selector:",
        "    app: kubia",
    ]
    tw = w * 0.52
    terminal(sl, x, y, tw, h, "service.yaml", body, size=13, colour=yaml_colour)
    nx = x + tw + 0.45
    notes = [(0.55, "port 80", "the port that the Service answers on"),
             (1.60, "targetPort 8080", "the port inside the container"),
             (2.65, "selector app: kubia", "every Pod with this label joins the Service")]
    for dy, head, sub in notes:
        tile(sl, nx, y + dy, 2.55, 0.42, head, B4, size=11)
        txt(sl, nx + 2.70, y + dy + 0.02, w - tw - 3.20, 0.60,
            [(sub, SLATE)], 11)
        arrow(sl, nx - 0.40, y + dy + 0.08, 0.34, 0.26, fill=BLUE, right=False)


def d30_namedports(sl, x, y, w, h):
    """A named port in the Pod, then the same name in the Service."""
    pod = [
        "kind: Pod",
        "spec:",
        "  containers:",
        "  - name: kubia",
        "    ports:",
        "    - name: http",
        "      containerPort: 8080",
        "    - name: https",
        "      containerPort: 8443",
    ]
    svc = [
        "apiVersion: v1",
        "kind: Service",
        "spec:",
        "  ports:",
        "  - name: http",
        "    port: 80",
        "    targetPort: http",
        "  - name: https",
        "    port: 443",
        "    targetPort: https",
    ]
    half = (w - 0.50) / 2
    terminal(sl, x, y, half, h, "pod.yaml", pod, size=12, colour=yaml_colour)
    terminal(sl, x + half + 0.50, y, half, h, "service.yaml", svc, size=12,
             colour=yaml_colour)
    arrow(sl, x + half + 0.08, y + h / 2 - 0.16, 0.34, 0.32, fill=BLUE)


def d31_clusterip(sl, x, y, w, h):
    """A ClusterIP Service answers inside the cluster only."""
    box(sl, x, y, w, h, PALEBG, line=HAIR)
    iw = w - 1.95
    box(sl, x + 0.20, y + 0.20, iw, h - 0.92, WHITE, line=HAIR)
    txt(sl, x + 0.34, y + 0.28, 2.40, 0.24, [("Kubernetes cluster", MUTED)], 10,
        bold=True)
    tile(sl, x + 0.40, y + 0.62, iw - 0.40, 0.48, "Service  10.96.0.17", B3, size=11)
    cw = (iw - 0.40) / 3
    for k in range(3):
        px = x + 0.40 + k * cw
        arrow(sl, px + cw / 2 - 0.09, y + 1.16, 0.18, 0.22, fill=SLATE, down=True)
        tile(sl, px + 0.06, y + 1.44, cw - 0.12, 0.48, "Pod", TEAL, size=10)
    tile(sl, x + 0.40, y + 2.10, iw - 0.40, 0.44, "CoreDNS  kubia.default.svc",
         B4, size=10)
    tile(sl, x + iw + 0.52, y + h / 2 - 0.38, 1.18, 0.62, "external", GREY,
         fg=SLATE, sub="client", size=10)
    box(sl, x + iw + 0.26, y + h / 2 - 0.22, 0.30, 0.30, RED, shape=MSO_SHAPE.OVAL)
    txt(sl, x + 0.20, y + h - 0.40, w - 0.40, 0.28,
        [("A ClusterIP address never answers from outside the cluster.", MUTED)], 11)


def d32_tiers(sl, x, y, w, h):
    """Three tiers, each behind its own ClusterIP Service."""
    box(sl, x, y, w, h, PALEBG, line=HAIR)
    tiers = [("front-end", B3), ("back-end", TEAL), ("redis", B4)]
    for k, (name, col) in enumerate(tiers):
        ry = y + 0.22 + k * 0.72
        txt(sl, x + 0.18, ry + 0.14, 1.10, 0.26, [(name, SLATE)], 10, bold=True)
        for j in range(3):
            tile(sl, x + 1.40 + j * 0.72, ry, 0.64, 0.52, "Pod", col, size=9)
        tile(sl, x + 3.70, ry, 1.70, 0.52, "Service", col, size=10)


def d32_term(sl, x, y, w, h, size=9):
    """The manifest and the list that proves it."""
    body = [
        "apiVersion: v1",
        "kind: Service",
        "metadata:",
        "  name: back-end",
        "spec:",
        "  type: ClusterIP",
        "  ports:",
        "  - port: 80",
        "    targetPort: 8080",
        "  selector:",
        "    app: back-end",
    ]
    terminal(sl, x, y, w, h, "service-back-end.yaml", body, size=size,
             colour=yaml_colour)


def d33_loadbalancer(sl, x, y, w, h):
    """A cloud load balancer in front of the node ports."""
    box(sl, x, y, w, h, PALEBG, line=HAIR)
    tile(sl, x + w / 2 - 1.10, y + 0.16, 2.20, 0.44, "external client", B4, size=11)
    arrow(sl, x + w / 2 - 0.11, y + 0.64, 0.22, 0.24, fill=SLATE, down=True)
    tile(sl, x + 0.45, y + 0.92, w - 0.90, 0.50, "cloud load balancer", B2, size=11)
    txt(sl, x + 0.45, y + 1.46, w - 0.90, 0.24, [("130.211.53.173", MUTED)], 10,
        align=PP_ALIGN.CENTER)
    arrow(sl, x + w / 2 - 0.11, y + 1.74, 0.22, 0.24, fill=SLATE, down=True)
    tile(sl, x + 0.60, y + 2.04, w - 1.20, 0.44, "Service", B3, size=11)
    half = (w - 0.70) / 2
    for k in range(2):
        nx = x + 0.25 + k * (half + 0.20)
        arrow(sl, nx + half / 2 - 0.09, y + 2.52, 0.18, 0.22, fill=SLATE, down=True)
        box(sl, nx, y + 2.84, half, h - 3.22, WHITE, line=HAIR)
        tile(sl, nx + 0.20, y + 2.98, half - 0.40, 0.42, "port 32143", AMBER,
             fg=SLATE, size=10)
        tile(sl, nx + 0.20, y + 3.50, half - 0.40, 0.42, "Pod   8080", TEAL, size=10)
        txt(sl, nx, y + h - 0.34, half, 0.24,
            [("node %d" % (k + 1), MUTED)], 10, align=PP_ALIGN.CENTER)


def d34_urls(sl, x, y, w, h):
    """One name for the users, instead of many node addresses."""
    box(sl, x, y, w, h, PALEBG, line=HAIR)
    txt(sl, x + 0.18, y + 0.16, w - 0.36, 0.26,
        [("without a load balancer", MUTED)], 10, bold=True)
    for k in range(4):
        txt(sl, x + 0.22, y + 0.50 + k * 0.30, w - 0.44, 0.26,
            [("http://192.168.56.7%d:30008" % k, SLATE)], 10, CONSOLAS)
    arrow(sl, x + w / 2 - 0.14, y + 1.80, 0.28, 0.34, fill=BLUE, down=True)
    txt(sl, x + 0.18, y + 2.24, w - 0.36, 0.26,
        [("with a load balancer", MUTED)], 10, bold=True)
    tile(sl, x + 0.30, y + 2.56, w - 0.60, 0.56, "http://kubia.example.com", B4,
         size=12)


S35_TABLE = [
 ["Feature", "ClusterIP", "NodePort", "LoadBalancer"],
 ["Reach", "inside the cluster only",
  "any node, on one high port", "one external address"],
 ["Clients", "Pods and nodes", "clients that can reach a node",
  "clients on the internet"],
 ["Manifest", "type: ClusterIP", "type: NodePort", "type: LoadBalancer"],
 ["Port range", "the Service port", "30000-32767",
  "the load balancer port"],
 ["Needs a cloud", "no", "no", "yes"],
]


def d35_table(sl, x, y, w, h):
    """The comparison, as a native table."""
    rows, cols = len(S35_TABLE), 4
    gt = sl.shapes.add_table(rows, cols, E(x), E(y), E(w), E(h))
    tbl = gt.table
    tbl.columns[0].width = E(w * 0.19)
    for c in range(1, 4):
        tbl.columns[c].width = E(w * 0.27)
    for r in range(rows):
        tbl.rows[r].height = E(h / rows)
        for c in range(cols):
            cell = tbl.cell(r, c)
            cell.text = ""
            cell.margin_left = cell.margin_right = E(0.10)
            cell.margin_top = cell.margin_bottom = E(0.05)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            head = (r == 0)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor.from_string(
                B4 if head else (PALEBG if r % 2 else WHITE))
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT
            run = p.add_run()
            run.text = S35_TABLE[r][c]
            mono = (r == 3 and c > 0)
            run.font.name = CONSOLAS if mono else CALIBRI
            run.font.size = Pt(11)
            run.font.bold = head or c == 0
            run.font.color.rgb = RGBColor.from_string(WHITE if head else SLATE)
    return gt


def d37_endpoints(sl, x, y, w, h):
    """kubectl describe svc, in a house terminal."""
    body = [
        "$ kubectl describe svc kubia",
        "Name:              kubia",
        "Namespace:         default",
        "Selector:          app=kubia",
        "Type:              ClusterIP",
        "IP:                10.111.249.153",
        "Port:              <unset>  80/TCP",
        "Endpoints:         10.108.1.4:8080,10.108.2.5:8080,10.108.2.6:8080",
        "Session Affinity:  None",
    ]
    terminal(sl, x, y, w, h, "kubectl describe svc kubia", body, size=11)


def d38_networking(sl, x, y, w, h):
    """Inside the cluster, then from outside through a node port."""
    half = (h - 0.30) / 2
    for band, (cap, external) in enumerate(
            [("ClusterIP - the Pods call each other", False),
             ("NodePort - a client outside reaches the same Pods", True)]):
        by = y + band * (half + 0.30)
        box(sl, x, by, w, half, PALEBG, line=HAIR)
        txt(sl, x + 0.14, by + 0.10, w - 0.28, 0.24, [(cap, MUTED)], 10, bold=True)
        nw = (w - 0.56) / 3
        for k in range(3):
            nx = x + 0.14 + k * (nw + 0.14)
            box(sl, nx, by + 0.42, nw, half - 0.76, WHITE, line=HAIR)
            if external:
                tile(sl, nx + 0.08, by + 0.50, nw - 0.16, 0.30, "30000", AMBER,
                     fg=SLATE, size=9)
            tile(sl, nx + 0.08, by + (0.88 if external else 0.56), nw - 0.16, 0.34,
                 "Pod", [B3, B4, TEAL][k], size=9)
            txt(sl, nx, by + half - 0.30, nw, 0.22,
                [("node %d" % (k + 1), MUTED)], 9, align=PP_ALIGN.CENTER)


def d39_ingress(sl, x, y, w, h):
    """One Ingress sends four host and path rules to four Services."""
    box(sl, x, y, w, h, PALEBG, line=HAIR)
    tile(sl, x + 0.25, y + h / 2 - 0.34, 1.45, 0.68, "Client", B4, size=12)
    arrow(sl, x + 1.80, y + h / 2 - 0.13, 0.45, 0.26, fill=SLATE)
    tile(sl, x + 2.35, y + h / 2 - 0.46, 1.60, 0.92, "Ingress", B2, size=13)
    rules = ["kubia.example.com/kubia", "kubia.example.com/foo",
             "foo.example.com", "bar.example.com"]
    for k, r in enumerate(rules):
        ry = y + 0.30 + k * ((h - 0.90) / 4)
        txt(sl, x + 4.15, ry + 0.04, 3.05, 0.26, [(r, SLATE)], 11, CONSOLAS)
        arrow(sl, x + 7.30, ry + 0.06, 0.40, 0.22, fill=SLATE)
        tile(sl, x + 7.85, ry - 0.08, 1.45, 0.50, "Service", B3, size=10)
        for j in range(3):
            tile(sl, x + 9.50 + j * 0.78, ry - 0.08, 0.70, 0.50, "Pod", TEAL,
                 size=9)
    txt(sl, x + 0.25, y + h - 0.34, w - 0.50, 0.26,
        [("One address and one certificate serve every rule.", MUTED)], 11)


def d40_ingress_yaml(sl, x, y, w, h):
    """The Ingress manifest on the API that Kubernetes 1.35 accepts.

    The v5 deck showed extensions/v1beta1. Kubernetes REMOVED that API in
    version 1.22, and the backend keys changed with it.
    """
    body = [
        "apiVersion: networking.k8s.io/v1",
        "kind: Ingress",
        "metadata:",
        "  name: kubia",
        "spec:",
        "  rules:",
        "  - host: kubia.example.com",
        "    http:",
        "      paths:",
        "      - path: /",
        "        pathType: Prefix",
        "        backend:",
        "          service:",
        "            name: kubia-nodeport",
        "            port:",
        "              number: 80",
    ]
    terminal(sl, x, y, w, h, "ingress.yaml", body, size=11, colour=yaml_colour)


# --------------------------------------------------------- extra text fixes
TEXT_FIX += [
 (38, "Blue and Orange POD are on same node",
      "A ClusterIP Service reaches a Pod on any node of the cluster"),
 (38, "Accessing a POD on other nodes - While a POD is hosted on node, svc is hosted across cluster but only accessible within cluster (Cluster IP)",
      "A Pod runs on one node. A Service covers every node, inside the cluster"),
 (38, "If Orange POD were to be DB, then cluster IP is good",
      "Use a ClusterIP Service for a database that only the cluster calls"),
 (38, "If Purple is Web app, a NodePort is created to ensure user can access from outside",
      "Use a NodePort Service for a web application that a user calls from outside"),
 (6, "> kubectl rollout status deployment/myapp-deployment",
     "$ kubectl rollout status deployment/kubia"),
 (6, "deployment \"myapp-deployment\" successfully rolled out",
     "deployment \"kubia\" successfully rolled out"),
 (6, "> kubectl rollout history deployment/myapp-deployment",
     "$ kubectl rollout history deployment/kubia"),
]

# A terminal paragraph takes its colour from its content, never from the line
# that it replaced.
RECOLOUR = [6, 10, 24, 36]

KEEP_NAMES = ("Picture 10", "Picture 11", "Picture 12")


def recolour_terminals(prs):
    for n in RECOLOUR:
        for sh in prs.slides[n - 1].shapes:
            if not sh.has_text_frame:
                continue
            runs = [r for p in sh.text_frame.paragraphs for r in p.runs]
            if not runs or not all(r.font.name == CONSOLAS for r in runs):
                continue
            for p in sh.text_frame.paragraphs:
                s = "".join(r.text for r in p.runs)
                col = line_colour(s)
                for r in p.runs:
                    r.font.color.rgb = RGBColor.from_string(col)


# ----------------------------------------------- screenshot replacement map
# slide -> (picture names to delete, [(function, left, top, width, height)])
REPLACE = {
 6:  (["Picture 2"],  [(d06_revisions, 2.79, 1.45, 7.72, 2.55)]),
 7:  (["Picture 3"],  [(d07_rolling, 5.69, 1.45, 6.43, 4.60)]),
 8:  (["Picture 3"],  [(d08_recreate, 5.74, 1.45, 6.33, 5.00)]),
 9:  (["Picture 2"],  [(d09_strategy, 1.00, 1.60, 11.30, 4.80)]),
 10: (["Picture 2"],  [(d10_summary, 1.00, 1.70, 11.30, 4.70)]),
 11: (["Picture 2", "Picture 3"], [(d11_labels, 0.55, 2.20, 12.20, 3.00)]),
 13: (["Picture 2"],  [(d13_traditional, 1.00, 1.50, 11.30, 4.60)]),
 14: (["Picture 2"],  [(d14_discovery, 1.30, 1.70, 10.70, 3.90)]),
 15: (["Picture 2"],  [(d15_similar, 1.30, 1.55, 10.70, 4.50)]),
 18: (["Picture 3"],  [(d18_services, 6.90, 1.70, 5.90, 4.10)]),
 20: (["Picture 3"],  [(d20_access, 6.90, 1.90, 5.90, 3.40)]),
 21: (["Picture 3"],  [(d21_intro, 7.00, 1.50, 5.70, 4.80)]),
 22: (["Picture 3"],  [(d22_types, 6.30, 1.50, 6.45, 4.90)]),
 23: (["Picture 3"],  [(d23_accessing, 6.90, 1.90, 5.90, 3.30)]),
 25: (["Picture 3"],  [(d25_kubeproxy, 6.70, 1.75, 6.10, 3.30)]),
 26: (["Picture 3"],  [(d26_howitworks, 5.00, 1.90, 7.80, 4.10)]),
 27: (["Picture 3"],  [(d27_nodeport, 6.70, 1.70, 6.10, 4.00)]),
 28: (["Picture 3"],  [(d28_ports, 6.70, 1.90, 6.10, 3.20)]),
 29: (["Picture 2"],  [(d29_manifest, 1.00, 1.80, 11.30, 3.40)]),
 30: (["Picture 2", "Picture 3"], [(d30_namedports, 1.60, 1.75, 10.10, 3.30)]),
 31: (["Picture 3"],  [(d31_clusterip, 6.70, 1.90, 6.10, 3.60)]),
 32: (["Picture 3", "Picture 4"],
      [(d32_tiers, 6.60, 1.60, 6.20, 2.40),
       (d32_term, 6.60, 4.15, 6.20, 2.35)]),
 33: (["Picture 3"],  [(d33_loadbalancer, 7.11, 1.60, 5.70, 4.50)]),
 34: (["Picture 3", "Picture 4"], [(d34_urls, 7.40, 1.70, 5.40, 3.30)]),
 35: (["Picture 2"],  [(d35_table, 1.60, 1.70, 10.10, 4.50)]),
 37: (["Picture 3"],  [(d37_endpoints, 1.60, 3.85, 9.10, 2.45)]),
 38: (["Picture 3", "Picture 4"], [(d38_networking, 6.60, 1.80, 6.20, 4.00)]),
 39: (["Picture 5"],  [(d39_ingress, 0.70, 1.55, 11.90, 4.70)]),
 40: (["Picture 3"],  [(d40_ingress_yaml, 6.55, 1.45, 6.20, 5.00)]),
}

HIDE = [13]            # the source deck hides this slide; v4 and v5 lost that.


def redraw_slide12(sl):
    """Slide 12 needs the terminal moved, so it is drawn from nothing."""
    for sh in list(sl.shapes):
        keep = (sh.shape_type == 9
                or (sh.shape_type == 13 and sh.width < E(1.0))
                or (sh.has_text_frame
                    and ("Labels & Selectors" in sh.text_frame.text
                         or "CLO835" in sh.text_frame.text)))
        if not keep:
            drop(sh, sl)
    d12_selector(sl, 0.55, 1.45, 6.10, 2.50)
    d12_pick(sl, 6.85, 1.45, 5.90, 2.50)
    terminal(sl, 0.55, 4.35, 12.20, 1.65, "bash",
             ["# Show every Pod that carries the label app=App1",
              "$ kubectl get pods --selector app=App1",
              "NAME             READY   STATUS    RESTARTS   AGE",
              "kubia-7nog1      1/1     Running   0          2m"], size=12)


FOOTER_RE = re.compile(r"^CLO835,\s+Fall\s+\d{4}\s+\d+\s*/\s*\d+$")


def set_footer(sl, n, total):
    for sh in sl.shapes:
        if not sh.has_text_frame:
            continue
        if not FOOTER_RE.match(sh.text_frame.text.strip()):
            continue
        for p in sh.text_frame.paragraphs:
            runs = p.runs
            if not runs:
                continue
            runs[0].text = "CLO835, Fall 2026     %d / %d" % (n, total)
            for r in runs[1:]:
                r.text = ""
        return True
    return False


def hide(sl, on=True):
    sl._element.set("show", "0" if on else "1")


def sanitize(prs):
    """A float EMU makes PowerPoint read 0 and move the shape to the corner."""
    ns = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
    fixed = 0
    for sl in prs.slides:
        for el in sl._element.iter():
            if el.tag in (ns + "off", ns + "ext"):
                for k in ("x", "y", "cx", "cy"):
                    v = el.get(k)
                    if v is not None and "." in v:
                        el.set(k, str(_i(float(v))))
                        fixed += 1
    return fixed


def build():
    prs = Presentation(SRC)
    total = len(prs.slides)

    missed = apply_text_fix(prs)
    rebuild_outline(prs.slides[2])
    redraw_slide12(prs.slides[11])

    for n, (names, draws) in REPLACE.items():
        sl = prs.slides[n - 1]
        for sh in list(sl.shapes):
            if sh.shape_type == 13 and sh.name in names:
                drop(sh, sl)
        for fn, x, y, w, h in draws:
            fn(sl, x, y, w, h)

    recolour_terminals(prs)

    for n in HIDE:
        hide(prs.slides[n - 1])

    for i, sl in enumerate(prs.slides, 1):
        set_footer(sl, i, total)

    fixed = sanitize(prs)
    prs.save(OUT)
    return OUT, total, missed, fixed


if __name__ == "__main__":
    out, total, missed, fixed = build()
    print("wrote", out, "-", total, "slides;", fixed, "float coordinates coerced")
    if missed:
        print("TEXT NOT FOUND:")
        for n, s in missed:
            print("  slide %d: %s" % (n, s))
