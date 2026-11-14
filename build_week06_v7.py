#!/usr/bin/env python3
"""CLO835 Week 06 lecture - v7.

Reads  Week06/Week06_lecture_style_v6.pptx
Writes Week06/Week06_lecture_style_v7.pptx

The only subject of v7 is REPETITION. The v6 deck states eleven facts on three
or more slides, carries three pairs of slides with one title, and holds two
bullets word for word on two slides. v7 removes the repeats.

Rule: state a point one time. State it a second time only in a summary.
Never state it a third time.

v6 is never written. Run this file from the project root.
"""

import copy
import os
import sys

from pptx import Presentation
from pptx.util import Inches, Pt

SRC = "Week06/Week06_lecture_style_v6.pptx"
DST = "Week06/Week06_lecture_style_v7.pptx"

FOOTER_PREFIX = "CLO835, Fall 2026"

# ---------------------------------------------------------------- deletions
# v6 slide numbers. Each one states only facts that another slide states.
DELETE = [
    9,   # Deployment Strategy      = slide 7 and slide 8 in one picture
    17,  # Exposing Containers...   = slide 16, merged into 16
    20,  # How can I access the POD = the question of 16, the answer of 27
    21,  # Introducing K8s Services = slide 18 and slide 19
    25,  # Kube-Proxy               = slide 26, merged into 26
    28,  # Service Type: NodePort   = slide 27 and slide 29
    32,  # Service Type: ClusterIP  = slide 31, slide 18 and slide 29
]

# ------------------------------------------------------------ text rewrites
# v6 slide number -> list of (level, text). Level 0 draws the square marker,
# level 1 draws the dash marker.
BULLETS = {
    # 16 takes the three challenges that slide 17 adds.
    16: [
        (0, "Imagine standard client-server configuration. How would we configure the "
            "access points for the clients?"),
        (0, "Challenges:"),
        (1, "We cannot use a Pod IP address. A Pod is ephemeral"),
        (1, "A client does not know the server address in advance"),
        (1, "Many Pods give the same service. A client cannot know which one to call"),
        (1, "A Pod can fail at any time"),
        (1, "A client outside the cluster has no route into the cluster"),
        (0, "We need one stable endpoint"),
    ],
    # The diagram and its caption already teach the tiers.
    18: [
        (0, "A Service gives one stable address to a group of Pods"),
        (0, "Enables loose coupling in our application"),
    ],
    # The three tiles beside these bullets name the three ways.
    23: [
        (0, "Services of type ClusterIP are not externally accessible"),
        (0, "Three ways reach the Service from inside the cluster:"),
    ],
    # 26 takes the facts of slide 25 and keeps its own diagram.
    26: [
        (0, "The API server creates the Service object, and gives it an IP address "
            "from a fixed range"),
        (0, "A Service is virtual. It has no process, no namespace and no interface"),
        (0, "A Service is an IP address and a port together"),
        (0, "Kube-proxy writes the iptables rules on every node"),
        (0, "Kube-proxy does not route the packet. The kernel does"),
    ],
    # Drops the second "any node" line and the kube-proxy line.
    27: [
        (0, "A port number is allocated for the service"),
        (0, "(by default, in the 30000-32767 range)"),
        (0, "That port is made available on all our nodes and anybody can connect to it"),
        (0, "Our code needs to be changed to connect to that new port number"),
        (0, "Sometimes it is the only option for external traffic, for example a "
            "kubeadm cluster"),
        (0, "Automatically will create a ClusterIP service"),
    ],
    # Drops the two bullets that slide 33 already carries, word for word.
    34: [
        (0, "Users can access this application using mentioned URLs"),
        (0, "However we need one URL like example-vote.com etc instead of node and ports"),
        (0, "K8s can integrate with native LB of cloud providers"),
    ],
    # Bullets 1 and 2 both named a list of IP addresses and ports. Slide 29
    # already explains the selector field, so the selector line goes.
    37: [
        (0, "An Endpoints resource (yes, plural) holds the list of IP addresses and "
            "ports that back a Service"),
        (0, "When a client connects, the service proxy selects one pair from the list, "
            "and it sends the connection to that address"),
    ],
    # Bullets 1 and 2 repeated slide 26. Only the choice stays.
    38: [
        (0, "Use a ClusterIP Service for a database that only the cluster calls"),
        (0, "Use a NodePort Service for a web application that a user calls from outside"),
    ],
}

# v6 slide number -> new title
RETITLE = {
    26: "Kube-Proxy",
    34: "Why a Load Balancer?",
}

# v6 slide number -> exact caption text to remove, because a bullet says it
DROP_CAPTION = {
    31: "A ClusterIP address never answers from outside the cluster.",
}

# 19 "Why Services?" keeps three rows. Row 3 repeats slide 36 (DNS), and
# row 5 repeats slide 18 (one stable address). Rows count from 1.
WHY_DROP_ROWS = [3, 5]
WHY_ROW_HEIGHT = 0.82
WHY_NEW_TOP = 2.49       # three rows, centred in the 1.50-6.70 band
WHY_NEW_PITCH = 1.20


# ------------------------------------------------------------------ helpers
def _emu(inches):
    return int(round(float(inches) * 914400))


def body_box(slide):
    """Return the bullet text frame of a slide, or None."""
    for shape in slide.shapes:
        if not shape.has_text_frame:
            continue
        text = shape.text_frame.text
        if text.startswith("▪") and FOOTER_PREFIX not in text:
            return shape
    return None


def title_box(slide):
    for shape in slide.shapes:
        if shape.has_text_frame and shape.name == "TextBox 1":
            return shape
    return None


def footer_box(slide):
    for shape in slide.shapes:
        if shape.has_text_frame and shape.text_frame.text.startswith(FOOTER_PREFIX):
            return shape
    return None


def set_bullets(shape, items, size0, size1):
    """Rewrite a bullet frame. Keep the run formatting of the source frame."""
    frame = shape.text_frame
    paragraphs = frame.paragraphs
    template0 = copy.deepcopy(paragraphs[0]._p)
    template1 = None
    for para in paragraphs:
        if para.runs and para.runs[0].text.startswith("–"):
            template1 = copy.deepcopy(para._p)
            break
    if template1 is None:
        template1 = copy.deepcopy(template0)

    body = frame._txBody
    for para in list(frame.paragraphs):
        body.remove(para._p)

    for level, _ in items:
        body.append(copy.deepcopy(template1 if level else template0))

    for para, (level, text) in zip(frame.paragraphs, items):
        runs = para.runs
        runs[0].text = "–  " if level else "▪  "
        runs[0].font.size = Pt(size1 if level else size0)
        if len(runs) > 1:
            runs[1].text = text
            runs[1].font.size = Pt(size1 if level else size0)
        for extra in runs[2:]:
            extra.text = ""


def drop(shape, slide):
    """Remove a shape, and release the image part if the shape is a picture."""
    element = shape._element
    try:
        rel_id = element.blip_rId
    except AttributeError:
        rel_id = None
    if rel_id:
        try:
            slide.part.drop_rel(rel_id)
        except Exception:
            pass
    element.getparent().remove(element)


def delete_slide(prs, index):
    """Remove the slide at a zero-based index."""
    id_list = prs.slides._sldIdLst
    entries = list(id_list)
    rel_key = ("{http://schemas.openxmlformats.org/officeDocument/2006/"
               "relationships}id")
    rel_id = entries[index].get(rel_key)
    id_list.remove(entries[index])
    prs.part.drop_rel(rel_id)


def trim_why_services(slide):
    """Keep three of the five rows of 'Why Services?', then re-centre them."""
    rows = {}
    for shape in slide.shapes:
        top = round(shape.top / 914400.0, 2)
        if 1.50 <= top <= 6.40 and shape.width > _emu(0.3):
            rows.setdefault(round(top, 1), []).append(shape)
    # A row holds four shapes. Group them by the band of the row background.
    bands = []
    for shape in slide.shapes:
        if shape.name.startswith("Rounded Rectangle") and shape.width > _emu(10):
            bands.append(round(shape.top / 914400.0, 3))
    bands.sort()
    if len(bands) != 5:
        raise SystemExit("slide 19: expected 5 rows, found %d" % len(bands))

    members = {band: [] for band in bands}
    for shape in slide.shapes:
        top = shape.top / 914400.0
        for band in bands:
            if band - 0.02 <= top <= band + WHY_ROW_HEIGHT - 0.02:
                members[band].append(shape)
                break

    for row_number in sorted(WHY_DROP_ROWS, reverse=True):
        for shape in list(members[bands[row_number - 1]]):
            drop(shape, slide)
        del members[bands[row_number - 1]]

    for index, band in enumerate(sorted(members)):
        new_top = WHY_NEW_TOP + index * WHY_NEW_PITCH
        delta = _emu(new_top - band)
        for shape in members[band]:
            shape.top = shape.top + delta


def sanitize(prs):
    """Coerce every coordinate to an integer. A float teleports a shape."""
    for slide in prs.slides:
        for shape in slide.shapes:
            for name in ("left", "top", "width", "height"):
                value = getattr(shape, name, None)
                if value is not None:
                    setattr(shape, name, int(value))


# -------------------------------------------------------------------- build
def build():
    if not os.path.exists(SRC):
        raise SystemExit("missing source: %s" % SRC)

    prs = Presentation(SRC)
    slides = list(prs.slides)
    if len(slides) != 41:
        raise SystemExit("expected 41 slides in v6, found %d" % len(slides))

    # 1. Edit the slides that stay, while the v6 numbers still apply.
    for number, items in BULLETS.items():
        slide = slides[number - 1]
        shape = body_box(slide)
        if shape is None:
            raise SystemExit("slide %d: no bullet frame" % number)
        size0 = 13 if number in (26, 27, 31) else (14 if number in (16, 37) else 15)
        set_bullets(shape, items, size0, size0 - 1)

    for number, text in RETITLE.items():
        shape = title_box(slides[number - 1])
        shape.text_frame.paragraphs[0].runs[0].text = text

    for number, caption in DROP_CAPTION.items():
        slide = slides[number - 1]
        for shape in list(slide.shapes):
            if shape.has_text_frame and shape.text_frame.text.strip() == caption:
                drop(shape, slide)

    trim_why_services(slides[18])     # slide 19

    # 2. Delete the repeated slides, highest number first.
    for number in sorted(DELETE, reverse=True):
        delete_slide(prs, number - 1)

    # 3. Renumber every footer.
    kept = list(prs.slides)
    total = len(kept)
    for index, slide in enumerate(kept, 1):
        shape = footer_box(slide)
        if shape is None:
            continue
        run = shape.text_frame.paragraphs[0].runs[0]
        run.text = "%s     %d / %d" % (FOOTER_PREFIX, index, total)

    sanitize(prs)
    prs.save(DST)
    return DST, total


if __name__ == "__main__":
    path, count = build()
    size = os.path.getsize(path) / 1048576.0
    print("wrote %s  %d slides  %.2f MB" % (path, count, size))
