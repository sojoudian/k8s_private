# -*- coding: utf-8 -*-
"""CLO835 Week 12 lecture v5 - ConfigMaps and Secrets.

Fixes the lecture defects of reports/report-2026-10-31-11-week12-preferences-check.md:
D1 bullets word for word on two slides, D2 the etcd point on 3 slides, D3 one word for
one meaning, D4 the label of Week 5, D5 manifests that do not apply as shown, D6 the
bullets of slides 4, 5 and 8, D7 the level of the base64 bullet.

Input : Week12/Lecture_week12_v4.pptx (read, never written)
Output: Week12/Lecture_week12_v5.pptx

Run from the project root. It is guarded, so importing it writes nothing.
    python build_week12_lecture_v5.py
"""
from pptx import Presentation
from pptx.util import Inches

import build_week08 as E
from build_week09_lecture_v6 import shape_named
from build_week10_lecture_v8 import add_bullet, set_lines, swap
from build_week12_lecture_v4 import recolor, set_title

SRC = "Week12/Lecture_week12_v4.pptx"
OUT = "Week12/Lecture_week12_v5.pptx"
TOTAL = 21
LOWER_LEVEL = "1380743"

GENERIC_POD = """apiVersion: v1
kind: Pod
metadata:
  name: generic-pod
spec:
  containers:
  - name: generic
    image: maziar/alpine-curl
    command: ["sleep"]
    args: ["3600"]"""

FORTUNE_ENV = """apiVersion: v1
kind: Pod
metadata:
  name: fortune-env
spec:
  containers:
  - image: maziar/fortune:env
    env:
    - name: INTERVAL
      value: "30"
    name: html-generator"""

REPLACE = {
    2: [("Passing command line options to the application", "Passing command-line arguments to the application"),
        ("Passing sensitive data to applications through Secrets",
         "Injecting sensitive data into applications through Secrets")],
    3: [("Week 5: K8s- PODs, ReplicaSets", "Week 5: K8s – Pods, ReplicaSets")],
    4: [("You can give configuration data to a containerized application in 3 ways:",
         "You can inject configuration data into a containerized application with 3 methods:")],
    5: [("Docker reminder", "Two Dockerfile instructions set what a container runs:"),
        ("CMD sets the arguments that Docker gives to the ENTRYPOINT.",
         "CMD sets the arguments that Docker passes to the ENTRYPOINT."),
        ("You can replace the CMD arguments with parameters on the docker command line.",
         "You can replace the CMD arguments in the docker run command.")],
    6: [("Usually, we replace the CMD arguments only, not the process in the container",
         "Usually, you replace the CMD arguments only, not the executable in the container"),
        ("With a generic image, we also set the process", "With a generic image, you also set the executable")],
    8: [("Problems:", "The Pod manifest should not hold the configuration"),
        ("The Pod manifest holds fixed values, so different values for production and development are difficult",
         "With fixed values, production and development each need a different manifest")],
    11: [("Inject the ConfigMap into the Pod", "Step 2 has 3 methods")],
    13: [("Like a ConfigMap, a Secret gives values to containers as environment variables or mounted files",
          "Like a ConfigMap, a Secret injects values into containers as environment variables or mounted files"),
         ("On a worker node, the kubelet keeps a Secret in memory (tmpfs), not on disk",
          "On a worker node, the kubelet stores a Secret in memory (tmpfs), not on disk"),
         ("etcd stores the Secret on the control-plane disk, and by default it is not encrypted",
          "etcd stores the Secret on the control-plane disk")],
    14: [("A 2-step process:", "A Secret uses the same 2 steps:")],
    15: [("Inject the Secret into the Pod", "Step 2 has the same 3 methods as a ConfigMap")],
    18: [("The kubelet keeps these files in an in-memory file system (tmpfs)",
          "The kubelet stores these files in an in-memory file system (tmpfs)")],
    19: [("You can give a Secret to a container as an environment variable",
          "You can inject a Secret into a container as an environment variable")],
}
REMOVE = {
    8: "The Pod description should not hold the configuration",
    18: "etcd on the control plane still stores the Secret",
}
BARS = [(6, "TextBox 9", "generic-pod.yaml"), (8, "TextBox 9", "fortune-env.yaml")]


def paragraph_with(slide, name, text):
    hits = [p for p in shape_named(slide, name).text_frame.paragraphs if text in "".join(r.text for r in p.runs)]
    assert len(hits) == 1, (text, len(hits))
    return hits[0]


def lower_level(para):
    assert para.runs[0].text.startswith("•")
    para.runs[0].text = para.runs[0].text.replace("•", "–")
    para._p.pPr.set("marL", LOWER_LEVEL)


def main():
    prs = Presentation(SRC)
    assert len(prs.slides) == TOTAL
    slides = prs.slides
    for no, pairs in REPLACE.items():
        for old, new in pairs:
            swap(slides[no - 1], old, new)
    for no, text in REMOVE.items():
        para = paragraph_with(slides[no - 1], "TextBox 3", text)
        para._p.getparent().remove(para._p)
    set_title(slides[5], "Passing Command-line Arguments in Kubernetes")
    add_bullet(slides[3], "TextBox 3", "Example: this nginx.conf file holds the configuration data of a web server")
    lower_level(paragraph_with(slides[13], "TextBox 3", "The manifest must hold base64 encoded data"))
    for no, text in ((6, GENERIC_POD), (8, FORTUNE_ENV)):
        set_lines(slides[no - 1], "TextBox 10", text.split("\n"), 11, yaml=True)
        recolor(slides[no - 1], "TextBox 10", "yaml")
    for no, name, text in BARS:
        shape_named(slides[no - 1], name).text_frame.paragraphs[0].runs[0].text = text
    # The 10 lines of generic-pod.yaml need a taller terminal. The table starts at 4.85 in.
    shape_named(slides[5], "Rectangle 4").height = Inches(2.85)
    shape_named(slides[5], "TextBox 10").height = Inches(2.41)
    E._sanitize_coords(prs)
    prs.save(OUT)
    print("wrote %s (%d slides)" % (OUT, TOTAL))


if __name__ == "__main__":
    main()
