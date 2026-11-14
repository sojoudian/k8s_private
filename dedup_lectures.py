# -*- coding: utf-8 -*-
"""CLO835 - remove the repetition from the lectures after Week 06.

The rule (the user, 2026-10-14, for Week 06): state a point one time. State it
a second time only when it is needed. Never state it a third time. No two
slides carry the same title.

Six decks. Each one is read and never written; the output is its next version.
A slide that repeats a slide of an earlier lecture word for word is deleted too.

Run from the project root:   python dedup_lectures.py
It is guarded, so importing it writes nothing.
"""
import copy
import os
import re
import sys

from pptx import Presentation

from retarget_accounts import replace_in_paragraph

FOOTER_PREFIX = "CLO835, Fall 2026"
MARKERS = ("▪", "–", "•")

DECKS = {
    # ------------------------------------------------------------- Week 07
    "Week07/Week07_lab_style_v4.pptx": {
        "out": "Week07/Week07_lab_style_v5.pptx",
        "slides": 14,
        # 3 = its facts are on 4 (shared by containers), 5 (pod spec) and 9
        #     (lifecycle, survives restarts); its one new bullet moves to 4.
        # 10 = the gitRepo diagram: gitRepo was already on 6 and 11.
        "delete": [3, 10],
        "insert_first": [(4, 0, "Unlike Network, processes and CPU, filesystems are unique per container")],
        "replace": [(8, "By default, this volume will be an emptyDir (an empty directory)",
                     "By default, this volume will be an emptyDir")],
        # The PVC link is on 5 and 7; the manifest beside 13 shows claimName.
        "drop": [(13, "The Pod mounts the volume by referencing the PVC")],
    },
    # ------------------------------------------------------------- Week 08
    "Week09/Week08_lecture_style_v4.pptx": {
        "out": "Week09/Week08_lecture_style_v5.pptx",
        "slides": 13,
        # 6 = the managed control plane, already on 3 (and HA on 8).
        # 12 = the Week 07 "Volume Lifecycle" slide, word for word.
        "delete": [6, 12],
        "append": [(3, "TextBox 6", 0, "No SSH: you reach it only through the Kubernetes API")],
        # Slide 10 teaches public/private endpoints; slide 7 the worker types.
        "drop": [(5, "Amazon EKS API server can be either private or publicly accessible"),
                 (5, "Worker nodes can be self-managed or AWS managed")],
    },
    # ------------------------------------------------------------- Week 09
    "Week10/Week09_lecture_style_v6.pptx": {
        "out": "Week10/Week09_lecture_style_v7.pptx",
        "slides": 36,
        # 9 = the Week 07 NFS slide, word for word.
        # 10 = its challenges move to 8.
        # 26, 27, 28, 29, 30 = the four StatefulSet properties of slide 24,
        #     stated again; 31 keeps the ReplicaSet/StatefulSet contrast.
        # 33 = the per-pod DNS name of 32; clusterIP: None moves to 32.
        "delete": [9, 10, 26, 27, 28, 29, 30, 33],
        "append": [(8, None, 1, "locks the pod definition to a specific cluster")],
        "retitle": [(16, "A PersistentVolumeClaim and a Matching PersistentVolume")],
        "replace": [
            (24, "pod names are fixed (mysql-0, mysql-1) and survive restarts.",
                 "pod names carry an ordinal index from 0 (mysql-0, mysql-1) and survive restarts."),
            (31, " They can have individual volumes (data).", ""),
            (32, "Headless service doesn’t load balance the requests. Points to only Master.",
                 "A headless Service (clusterIP: None) does not load balance the requests. Points to only Master."),
        ],
        "insert_first": [(35, 0, "Each member of a clustered application must know the network identity of every other member")],
    },
    # ------------------------------------------------------------- Week 12
    "Week12/Week12_v2.pptx": {
        "out": "Week12/Week12_v3.pptx",
        "slides": 21,
        "retitle": [(7, "Example: Overriding ENTRYPOINT and CMD")],
        "drop": [
            (4, "The application can be configured through command line arguments, environment variables or through config files"),
            (5, "$ docker run -it docker.io/maziar/fortune:args 15", "TextBox 3"),
            (14, "Need to encode data in secrets file."),
            (15, "Secrets are not encrypted only encoded"),
            (18, "$ k exec fortune-https -c web-server -- mount | grep certs", "TextBox 3"),
        ],
        # Slide 13 also contradicted slide 15: etcd does not encrypt a Secret
        # unless encryption at rest is turned on.
        "replace": [(13, "Stored in etcd and are encrypted", "Stored in etcd")],
        # (slide, shape, first line, number of lines)
        "drop_lines": [
            (11, "TextBox 10", " ", 8),            # the ConfigMap of slide 10, again
            (11, "TextBox 17", "envFrom:", 4),     # the envFrom of the manifest beside it
            (15, "TextBox 10", " ", 10),           # the Secret of slide 14, again
            (15, "TextBox 17", "# inject ALL keys (envFrom)", 5),
        ],
    },
    # ------------------------------------------------------------- Week 13
    "week13/Week13_lecture_style_v6.pptx": {
        "out": "week13/Week13_lecture_style_v7.pptx",
        "slides": 22,
        # 21 = the kubeconfig picture; Week 14 slide 4 teaches it in full.
        "delete": [21],
        "drop": [
            (6, "Authentication plugin returns all the K8s groups the user belongs to"),
            (9, "RBAC authorization is the default in Amazon EKS"),
            (9, "Other authorization plugins supported by K8s:"),
            (9, "Attribute-based access control (ABAC) plugin"),
            (9, "Web-Hook plugin"),
            (9, "Custom plugin implementations."),
            (12, "Define a Role eg; Developers"),
            (12, "Associate the user to that role"),
            (16, 'Reminder – K8s does not support resource of type "user"'),
        ],
    },
    # ------------------------------------------------------------- Week 14
    "week14/Week14_lecture_style_v10.pptx": {
        "out": "week14/Week14_lecture_style_v11.pptx",
        "slides": 11,
        "retitle": [(5, "Kubectl Config – View the kubeconfig"),
                    (6, "Kubectl Config – List the Contexts"),
                    (7, "Kubectl Config – Switch and Define Contexts"),
                    (9, "How the HPA Calculates the Replica Count")],
        "replace": [
            (4, "kubectl uses the current-context by default; switch environments in one command:  "
                "kubectl config use-context <name>  (list them with kubectl config get-contexts).",
                "kubectl uses the current-context by default."),
            (5, "# kubeconfig lives at ~/.kube/config by default — view the merged config", "# View the merged config"),
            (6, "# List every context — each bundles a CLUSTER + USER + NAMESPACE", "# List every context"),
            (7, "# Define a context = one cluster + one user + a namespace", "# Define a context"),
            (8, "The HPA controller polls metrics server every 15 seconds and adjusts the number of replicas on the "
                "target resource (Deployment, ReplicaSet, Replication-Controller, or StatefulSet) to meet the target "
                "metric value",
                "The HPA controller polls the Metrics Server every 15 seconds. The target can be a Deployment, "
                "ReplicaSet, Replication-Controller, or StatefulSet"),
            (9, "Obtain metrics of all the pods managed by the scaled resource object.",
                "The HPA adds the metric of every pod and divides the sum by the target: (60 + 90 + 50) / 50 = 4 replicas."),
            (9, "Calculate the number of pods required to bring the metrics to (or close to) the specified target value.",
                "With two metrics, the HPA takes the larger result: max(4, 3) = 4 replicas."),
        ],
        "drop": [(9, "Update the replicas field of the scaled resource.")],
    },
}


# ------------------------------------------------------------------ helpers
def norm(text):
    text = text.replace("’", "'").replace("“", '"').replace("”", '"')
    text = text.strip()
    for m in MARKERS:
        if text.startswith(m):
            text = text[len(m):].strip()
    return re.sub(r"\s+", " ", text)


def para_text(p):
    return "".join(r.text for r in p.runs)


def text_shapes(slide):
    for sh in slide.shapes:
        if sh.has_text_frame and not sh.text_frame.text.startswith(FOOTER_PREFIX):
            yield sh


def find_paras(slide, text, shape_name=None):
    hits = []
    for sh in text_shapes(slide):
        if shape_name and sh.name != shape_name:
            continue
        for p in sh.text_frame.paragraphs:
            if norm(para_text(p)) == norm(text):
                hits.append((sh, p))
    return hits


def one(hits, what):
    if len(hits) != 1:
        raise SystemExit("%s: %d matches" % (what, len(hits)))
    return hits[0]


def level_of(p):
    t = para_text(p).lstrip()
    return 1 if t.startswith("–") else (2 if t.startswith("•") else 0)


def body_shape(slide, shape_name=None):
    """The bullet frame of a slide: the frame whose text starts with a marker."""
    for sh in text_shapes(slide):
        if shape_name and sh.name != shape_name:
            continue
        if shape_name or sh.text_frame.text.lstrip().startswith("▪"):
            return sh
    raise SystemExit("no bullet frame")


def new_para(shape, level, text, where):
    """Clone a paragraph of the same level (or the first one), set its text."""
    paras = shape.text_frame.paragraphs
    template = next((p for p in paras if level_of(p) == level), paras[0])
    clone = copy.deepcopy(template._p)
    if where == "first":
        paras[0]._p.addprevious(clone)
    else:
        paras[-1]._p.addnext(clone)
    p = next(q for q in shape.text_frame.paragraphs if q._p is clone)
    runs = p.runs
    marker = {0: "▪  ", 1: "–  ", 2: "•  "}[level]
    if len(runs) >= 2 and norm(runs[0].text) == "":
        runs[0].text = marker
        runs[1].text = text
        for r in runs[2:]:
            r.text = ""
    else:
        runs[0].text = marker + text
        for r in runs[1:]:
            r.text = ""


def delete_slide(prs, index):
    lst = prs.slides._sldIdLst
    entry = list(lst)[index]
    rid = entry.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
    lst.remove(entry)
    prs.part.drop_rel(rid)


def drop_lines(slide, shape_name, first, count):
    sh = next(s for s in slide.shapes if s.name == shape_name)
    paras = sh.text_frame.paragraphs
    start = next(i for i, p in enumerate(paras) if norm(para_text(p)) == norm(first))
    if start + count > len(paras):
        raise SystemExit("drop_lines past the end in %s" % shape_name)
    for p in paras[start:start + count]:
        p._p.getparent().remove(p._p)


def build(src, spec):
    prs = Presentation(src)
    slides = list(prs.slides)
    if len(slides) != spec["slides"]:
        raise SystemExit("%s: expected %d slides, found %d" % (src, spec["slides"], len(slides)))
    log = []
    for n, title in spec.get("retitle", []):
        sh = next(s for s in slides[n - 1].shapes if s.name == "TextBox 1")
        runs = sh.text_frame.paragraphs[0].runs
        runs[0].text = title
        for r in runs[1:]:
            r.text = ""
        for extra in sh.text_frame.paragraphs[1:]:
            extra._p.getparent().remove(extra._p)
        log.append("retitle %d" % n)
    for n, old, new in spec.get("replace", []):
        k = sum(replace_in_paragraph(p, old, new)
                for sh in text_shapes(slides[n - 1]) for p in sh.text_frame.paragraphs)
        if k != 1:
            raise SystemExit("%s slide %d replace: %d matches for %r" % (src, n, k, old[:40]))
        log.append("replace %d" % n)
    for item in spec.get("drop", []):
        n, text = item[0], item[1]
        _, p = one(find_paras(slides[n - 1], text, item[2] if len(item) > 2 else None),
                   "%s slide %d drop %r" % (src, n, text[:40]))
        p._p.getparent().remove(p._p)
        log.append("drop %d" % n)
    for n, shape_name, first, count in spec.get("drop_lines", []):
        drop_lines(slides[n - 1], shape_name, first, count)
        log.append("drop_lines %d" % n)
    for n, level, text in spec.get("insert_first", []):
        new_para(body_shape(slides[n - 1]), level, text, "first")
        log.append("insert %d" % n)
    for n, shape_name, level, text in spec.get("append", []):
        new_para(body_shape(slides[n - 1], shape_name), level, text, "last")
        log.append("append %d" % n)
    for n in sorted(spec.get("delete", []), reverse=True):
        delete_slide(prs, n - 1)
        log.append("delete %d" % n)
    kept = list(prs.slides)
    for i, s in enumerate(kept, 1):
        for sh in s.shapes:
            if sh.has_text_frame and sh.text_frame.text.startswith(FOOTER_PREFIX):
                runs = sh.text_frame.paragraphs[0].runs
                runs[0].text = "%s     %d / %d" % (FOOTER_PREFIX, i, len(kept))
                for r in runs[1:]:
                    r.text = ""
    for s in kept:
        for sh in s.shapes:
            for name in ("left", "top", "width", "height"):
                v = getattr(sh, name, None)
                if v is not None:
                    setattr(sh, name, int(v))
    prs.save(spec["out"])
    return len(slides), len(kept), log


if __name__ == "__main__":
    for src, spec in DECKS.items():
        if os.path.exists(spec["out"]):
            sys.exit("refusing to overwrite " + spec["out"])
        before, after, log = build(src, spec)
        print("%-40s %2d -> %2d slides, %d edits" % (spec["out"], before, after, len(log)))
