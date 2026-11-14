# -*- coding: utf-8 -*-
"""CLO835 - move every Docker Hub and GitHub name of the canonical decks to the
course accounts: Docker Hub "maziar" and GitHub "sojoudian".

Each deck is read and never written. The output is the next version of it.
The slides, the layout and the footers do not change; only the named text does.

Run from the project root:   python retarget_accounts.py
It is guarded, so importing it writes nothing.

The images were copied to Docker Hub on 27 Oct 2026 (docker buildx imagetools
create). The GitHub copies are forks, so each one keeps the name of its author.
The two manifests (Flannel, metrics-server) are in sojoudian/clo835-mirrors,
with the image names changed to maziar.
"""
import sys
from pptx import Presentation

GH = "https://github.com/sojoudian/"
MIRRORS = "https://raw.githubusercontent.com/sojoudian/clo835-mirrors/main/"

# (input deck, output deck, [(old text, new text), ...])
DECKS = [
    ("week01/Week01_lecture_style_v5.pptx", "week01/Week01_lecture_style_v6.pptx", [
        ("jenkins/jenkins", "maziar/kubia"),
    ]),
    ("Week04/FINAL/Lab_week04.pptx", "Week04/FINAL/Lab_week04_v2.pptx", [
        ("https://github.com/flannel-io/flannel/blob/master/Documentation/backends.md",
         GH + "flannel/blob/master/Documentation/backends.md"),
        ("https://github.com/flannel-io/flannel", GH + "flannel"),
        ("https://github.com/jpetazzo/container.training/tree/main/dockercoins",
         GH + "container.training/tree/main/dockercoins"),
        ("https://github.com/luksa/kubernetes-in-action", GH + "kubernetes-in-action"),
    ]),
    ("Week05/lecture_week05_v3.pptx", "Week05/lecture_week05_v4.pptx", [
        ("gcr.io/google_samples/gb-frontend:v5", "maziar/gb-frontend:v5"),
    ]),
    ("Week07/Week07_lab_style_v3.pptx", "Week07/Week07_lab_style_v4.pptx", [
        ("https://github.com/luksa/kubia-website-example.git", GH + "kubia-website-example.git"),
        ("alpine/git", "maziar/alpine-git"),
    ]),
    ("Week09/Week08_lecture_style_v3.pptx", "Week09/Week08_lecture_style_v4.pptx", [
        ("https://github.com/weaveworks/eksctl/tree/main/examples", GH + "eksctl/tree/main/examples"),
    ]),
    ("Week10/Week09_lecture_style_v4.pptx", "Week10/Week09_lecture_style_v5.pptx", [
        # registry.k8s.io/test-webserver is a schema 1 image; containerd 2 cannot pull it.
        ("k8s.gcr.io/test-webserver", "maziar/kubia:0.1"),
        ("alpine/curl", "maziar/alpine-curl"),
    ]),
    ("Week12/Week12.pptx", "Week12/Week12_v2.pptx", [
        ("docker.io/luksa/fortune:args", "docker.io/maziar/fortune:args"),
        ("luksa/fortune:env", "maziar/fortune:env"),
        ("https://github.com/mmumshad/simple-webapp-mysql", GH + "simple-webapp-mysql"),
        ("https://github.com/luksa/kubernetes-in-action/tree/master/Chapter07",
         GH + "kubernetes-in-action/tree/master/Chapter07"),
    ]),
    ("Week12/Week12_lab.pptx", "Week12/Week12_lab_v2.pptx", [
        ("luksa/fortune:env", "maziar/fortune:env"),
    ]),
    ("week14/Week14_lecture_style_v9.pptx", "week14/Week14_lecture_style_v10.pptx", [
        ("https://mjarosie.github.io/dev/2021/09/15/iam-roles-for-kubernetes-service-accounts-deep-dive.html",
         GH + "mjarosie.github.io/blob/master/_posts/2021-09-15-iam-roles-for-kubernetes-service-accounts-deep-dive.md"),
    ]),
    ("week14/Week14_lab_style_v10.pptx", "week14/Week14_lab_style_v11.pptx", [
        ("https://github.com/kubernetes-sigs/metrics-server/releases/download/v0.7.1/components.yaml",
         MIRRORS + "metrics-server/v0.7.1/components.yaml"),
        ("us.gcr.io/k8s-artifacts-prod/hpa-example", "maziar/hpa-example"),
        ("amazon/aws-cli", "maziar/aws-cli"),
    ]),
]


def paragraphs(shapes):
    """Every paragraph of every text frame, table cell and group member."""
    for sh in shapes:
        if sh.shape_type == 6:                       # a group
            yield from paragraphs(sh.shapes)
        if sh.has_text_frame:
            yield from sh.text_frame.paragraphs
        if getattr(sh, "has_table", False) and sh.has_table:
            for row in sh.table.rows:
                for cell in row.cells:
                    yield from cell.text_frame.paragraphs


def replace_in_paragraph(para, old, new):
    """Replace old with new, also when old spans more than one run. The text
    goes into the first run of the span, so that run keeps its format."""
    count = 0
    while True:
        runs = list(para.runs)
        text = "".join(r.text for r in runs)
        at = text.find(old)
        if at < 0:
            return count
        end, pos, first = at + len(old), 0, None
        for r in runs:
            a, b = pos, pos + len(r.text)
            pos = b
            if b <= at or a >= end:
                continue
            keep_head = r.text[:max(0, at - a)]
            keep_tail = r.text[max(0, end - a):] if end < b else ""
            if first is None:
                first = r
                r.text = keep_head + new + keep_tail
            else:
                r.text = keep_tail
        count += 1


def retarget(src, out, pairs):
    prs = Presentation(src)
    done = {old: 0 for old, _ in pairs}
    for slide in prs.slides:
        paras = list(paragraphs(slide.shapes))
        if slide.has_notes_slide:
            paras += list(slide.notes_slide.notes_text_frame.paragraphs)
        for p in paras:
            for old, new in pairs:          # longest first in each list
                done[old] += replace_in_paragraph(p, old, new)
    missed = [old for old, n in done.items() if n == 0]
    prs.save(out)
    return done, missed


if __name__ == "__main__":
    bad = 0
    for src, out, pairs in DECKS:
        done, missed = retarget(src, out, pairs)
        print("%-40s -> %s" % (src, out))
        for old, n in done.items():
            print("    %2d x  %s" % (n, old))
        if missed:
            bad += 1
            print("    NOT FOUND:", missed)
    sys.exit(1 if bad else 0)
