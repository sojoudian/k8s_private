# -*- coding: utf-8 -*-
"""CLO835 Week 12 lecture v6 - ConfigMaps and Secrets.

Fixes every defect of the check against PROMPT.md, DESIGN_LANGUAGE.md and PREFERENCES.md
(report 2026-10-31-13). The commands and manifests now run in slide order, in one
namespace, with a file for each --from-file. The summary uses the names of this lecture.
The slides follow the design rules for terminals, the footer guard, inline code,
small numbers and the palette. Each point stands on at most two slides.

Input : Week12/Lecture_week12_v5.pptx (read, never written)
Output: Week12/Lecture_week12_v6.pptx

Run from the project root. It is guarded, so importing it writes nothing.
    python build_week12_lecture_v6.py
"""
import copy
import re

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.text.text import _Run
from pptx.util import Inches, Pt

import build_week08 as E
from build_week09_lecture_v6 import arrow, box, remove_shape, shape_named, zone
from build_week10_lecture_v8 import add_bullet, set_lines, set_size, swap
from build_week12_lecture_v4 import set_title

SRC = "Week12/Lecture_week12_v5.pptx"
OUT = "Week12/Lecture_week12_v6.pptx"
TOTAL = 21
SLATE, STEPS = E.SLATE, E.STEPS
RIGHT = MSO_SHAPE.RIGHT_ARROW
LEVEL_2 = "996695"
FOOTER_GUARD = 6.70

CONFIG_MAP = ["apiVersion: v1", "kind: ConfigMap", "metadata:", "  name: app-config", "data:",
              "  APP_COLOR: blue", "  APP_MODE: prod", "", "$ kubectl apply -f config-map.yaml"]
SECRET_DATA = ["apiVersion: v1", "kind: Secret", "metadata:", "  name: app-secret", "data:",
               "  DB_Host: bXlzcWw=", "  DB_Password: cGFzd3Jk", "", "$ kubectl apply -f secret-data.yaml"]
IMPERATIVE_CM = ["$ kubectl create configmap \\", "    <config-name> --from-literal=<key>=<value>", "",
                 "$ kubectl create configmap \\", "    app-config --from-literal=APP_COLOR=blue \\",
                 "    --from-literal=APP_MODE=prod", "",
                 "$ kubectl create configmap \\", "    <config-name> --from-file=<path-to-file>", "",
                 "# The file name is the key.", "$ printf 'debug' > LOG_LEVEL", "$ kubectl create configmap \\",
                 "    app-config-file --from-file=LOG_LEVEL"]
IMPERATIVE_SECRET = ["$ kubectl create secret generic \\", "    <secret-name> --from-literal=<key>=<value>", "",
                     "$ kubectl create secret generic \\", "    app-secret --from-literal=DB_Host=mysql \\",
                     "    --from-literal=DB_Password=paswrd", "",
                     "$ kubectl create secret generic \\", "    <secret-name> --from-file=<path-to-file>", "",
                     "$ printf 'paswrd' > DB_Password", "$ kubectl create secret generic \\",
                     "    app-secret-file --from-file=DB_Password"]
TOKEN_COMMANDS = ["# Since v1.24, Kubernetes makes no token Secret.", "$ kubectl get secrets", "",
                  "# The Pod gets the token as files.", "$ kubectl exec secret-pod -- \\",
                  "    ls /var/run/secrets/kubernetes.io/serviceaccount"]
TOKEN_OUTPUT = ["NAME              TYPE     DATA   AGE", "app-secret        Opaque   2      2s",
                "app-secret-file   Opaque   1      2s", "", "ca.crt", "namespace", "token"]
MOUNT = ["$ kubectl exec secret-pod -- mount | grep secret-volume",
         "tmpfs on /etc/secret-volume type tmpfs (ro,relatime,size=7814528k,inode64,noswap)"]
SLIDE7 = ["# The image maziar/fortune:args", 'ENTRYPOINT ["/bin/fortuneloop.sh"]', 'CMD ["10"]', "",
          "apiVersion: v1", "kind: Pod", "metadata:", "  name: fortune-sleeper-pod", "spec:", "  containers:",
          "  - name: fortune-sleeper", "    image: maziar/fortune:args", '    command: ["sleep"]', '    args: ["3600"]']

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

SECRET_ENV = """apiVersion: v1
kind: Pod
metadata:
  name: webapp-secret
  labels:
    name: webapp-secret
spec:
  containers:
  - name: webapp
    image: maziar/kubia:v1
    ports:
    - containerPort: 8080
    envFrom:
    - secretRef:
        name: app-secret"""

VOLUME_POD = """apiVersion: v1
kind: Pod
metadata:
  name: %s
spec:
  containers:
  - name: webapp
    image: maziar/kubia:v1
    env:
    - name: %s
      valueFrom:
        %s:
          name: %s
          key: %s
    volumeMounts:
    - name: %s
      mountPath: %s
  volumes:
  - name: %s
    %s:
      %s: %s"""
CONFIGMAP_VOLUME = VOLUME_POD % ("webapp-volume", "APP_COLOR", "configMapKeyRef", "app-config", "APP_COLOR",
                                 "app-config-volume", "/etc/app-config", "app-config-volume", "configMap",
                                 "name", "app-config")
SECRET_VOLUME = """apiVersion: v1
kind: Pod
metadata:
  name: secret-pod
spec:
  containers:
  - name: app
    image: maziar/alpine-curl
    command: ["sleep"]
    args: ["3600"]
    env:
    - name: DB_Password
      valueFrom:
        secretKeyRef:
          name: app-secret
          key: DB_Password
    volumeMounts:
    - name: app-secret-volume
      mountPath: /etc/secret-volume
  volumes:
  - name: app-secret-volume
    secret:
      secretName: app-secret"""

TITLES = {6: "Passing Command-line Arguments in Kubernetes", 7: "Example: Replacing ENTRYPOINT and CMD",
          8: "Injecting Configuration Data with Environment Variables", 18: "How the Kubelet Stores a Secret Volume"}

# slide, text box, lines, size, bar text, kind
TERMINALS = [
    (6, "TextBox 10", GENERIC_POD.split("\n"), 11, "generic-pod.yaml", "yaml"),
    (7, "TextBox 9", SLIDE7, 12, None, "yaml"),
    (8, "TextBox 10", FORTUNE_ENV.split("\n"), 11, "fortune-env.yaml", "yaml"),
    (10, "TextBox 10", IMPERATIVE_CM, 11, None, "cmd"),
    (10, "TextBox 17", CONFIG_MAP, 11, None, "yaml"),
    (11, "TextBox 17", CONFIGMAP_VOLUME.split("\n"), 10, "pod-configmap-volume.yaml", "yaml"),
    (14, "TextBox 10", IMPERATIVE_SECRET, 10, None, "cmd"),
    (14, "TextBox 17", SECRET_DATA, 10, None, "yaml"),
    (15, "TextBox 10", SECRET_ENV.split("\n"), 10, "pod-secret.yaml", "yaml"),
    (15, "TextBox 17", SECRET_VOLUME.split("\n"), 10, "secret-pod.yaml", "yaml"),
    (16, "TextBox 10", TOKEN_COMMANDS, 11, None, "cmd"),
    (16, "TextBox 17", TOKEN_OUTPUT, 11, None, "cmd"),
    (18, "TextBox 10", MOUNT, 14, None, "cmd"),
]
BARS = [(11, "TextBox 9", "pod-configmap.yaml")]

REPLACE = {
    4: [("with 3 methods:", "with three methods:")],
    5: [("ENTRYPOINT sets the executable that runs when the container starts.",
         "ENTRYPOINT sets the executable that runs when the container starts"),
        ("CMD sets the arguments that Docker passes to the ENTRYPOINT.",
         "CMD sets the arguments that Docker passes to the ENTRYPOINT"),
        ("You can replace the CMD arguments in the docker run command.",
         "You can replace the CMD arguments in the docker run command")],
    8: [("You set variables for each container, not for the Pod",
         "You set environment variables for each container, not for the Pod"),
        ("Kubernetes injects environment variables for all the Services in the namespace",
         "The kubelet injects environment variables for the Services of the namespace that exist when the Pod starts, "
         "and for the API server"),
        ("The Pod manifest should not hold the configuration", "The Pod manifest should not hold the configuration data")],
    9: [("A ConfigMap is a Kubernetes resource", "A ConfigMap is a Kubernetes object"),
        ("Containers get the values as environment variables or as files in a mounted folder",
         "Containers get the values as environment variables or as files in a volume")],
    10: [("A 2-step process:", "A two-step process:")],
    11: [("Step 2 has 3 methods", "Step 2 has three methods"),
         ("Use all the keys as variables, one key as a variable, or a volume with files",
          "Use all the keys as environment variables, one key as an environment variable, or a volume with files")],
    13: [("A Secret holds key/value pairs as base64 strings",
          "A Secret holds key/value pairs as base64 strings. base64 is an encoding, not encryption"),
         ("etcd stores the Secret on the control-plane disk", "etcd stores the Secret on the disk of the master node")],
    14: [("A Secret uses the same 2 steps:", "A Secret uses the same two steps:"),
         ("The manifest must hold base64 encoded data",
          "The data field must hold base64 strings. The stringData field takes plain text")],
    15: [("Step 2 has the same 3 methods as a ConfigMap", "Step 2 has the same three methods as a ConfigMap"),
         ("Do not put Secret objects in source control", "Do not put Secret manifests in source control"),
         ("By default, Secrets in etcd are not encrypted. Turn on encryption at rest",
          "By default, etcd stores Secrets without encryption. Turn on encryption at rest")],
    16: [("The folder has 3 entries:", "The folder has three files:")],
    19: [("This is not the recommended method", "A Secret in an environment variable is not the recommended method"),
         ("Child processes get the variables too. A compromised third-party library can then read the Secret",
          "Child processes get the environment variables too. A third-party program can then read the Secret")],
}
REMOVE = {
    13: ["Like a ConfigMap, a Secret injects values into containers as environment variables or mounted files",
         "On a worker node, the kubelet stores a Secret in memory (tmpfs), not on disk"],
    14: ["Imperative", "Declarative"],
    19: ["You can inject a Secret into a container as an environment variable"],
}
BULLETS = {
    16: [("ca.crt", "ca.crt: the certificate that verifies the API server"),
         ("namespace", "namespace: the namespace of the Pod"),
         ("token", "token: identifies the ServiceAccount to the API server")],
}
# slide, {run size now: run size then}. The body scale of DESIGN_LANGUAGE.md starts at 12 pt.
BODY_SIZES = {14: {12.0: 14, 11.0: 13, 10.0: 12}, 15: {11.5: 12}, 16: {12.0: 14, 11.0: 13}}
# Code in body copy is inline mono, bold and Slate. In a diagram box only the font changes.
BODY_CODE = {4: ["nginx.conf"], 5: ["ENTRYPOINT", "CMD", "docker run"], 6: ["CMD"],
             14: ["data", "stringData"], 16: ["/var/run/secrets/kubernetes.io/serviceaccount", "ca.crt", "namespace:", "token:"],
             18: ["/etc/secret-volume"]}
DIAGRAM_CODE = {9: ["key1=value1", "key2=value2"], 12: ["app-config"],
                17: ["/var/run/secrets/", "kubernetes.io/serviceaccount", "ca.crt", "namespace", "token",
                     "kube-api-access-<id>", "kube-root-ca.crt"],
                20: ["/etc/app-config", "/etc/secret-volume", "app-config", "app-secret", "APP_COLOR", "APP_MODE",
                     "DB_Host", "DB_Password"]}


def paragraph_with(slide, name, text):
    hits = [p for p in shape_named(slide, name).text_frame.paragraphs if p.runs and p.runs[-1].text == text]
    assert len(hits) == 1, (text, len(hits))
    return hits[0]


def body_sizes(slide, sizes):
    for p in shape_named(slide, "TextBox 3").text_frame.paragraphs:
        for r in p.runs:
            if r.font.size and r.font.size.pt in sizes:
                r.font.size = Pt(sizes[r.font.size.pt])


def recolor(slide, name, kind):
    """A command and its continuation lines are cyan, a comment is green, and output is gray."""
    going = False
    for p in shape_named(slide, name).text_frame.paragraphs:
        for r in p.runs:
            line = r.text.strip()
            if line.startswith("#"):
                r.font.color.rgb = E.TERM_GRN
            elif line.startswith("$") or going:
                r.font.color.rgb = E.TERM_CYAN
            elif kind == "cmd":
                r.font.color.rgb = E.TERM_GRAY
            going = (line.startswith("$") or going) and line.endswith("\\")


def inline_code(slide, tokens, body=True, min_height=0.35):
    """Split each run at the tokens. The titles, the terminals and the terminal bars stay."""
    pattern = re.compile("(" + "|".join(r"(?<![\w/.-])%s(?![\w-])" % re.escape(t) for t in tokens) + ")")
    for sh in slide.shapes:
        if not sh.has_text_frame or sh.name == "TextBox 1" or sh.height < Inches(min_height):
            continue
        for p in sh.text_frame.paragraphs:
            for r in list(p.runs):
                parts = pattern.split(r.text)
                if r.font.name == E.FONT_MONO or len(parts) == 1:
                    continue
                for i, part in enumerate(parts):
                    if not part:
                        continue
                    new = copy.deepcopy(r._r)
                    r._r.addprevious(new)
                    run = _Run(new, p)
                    run.text = part
                    if i % 2:
                        run.font.name = E.FONT_MONO
                        if body:
                            run.font.bold = True
                            run.font.color.rgb = SLATE
                r._r.getparent().remove(r._r)


def colon_outside(slide):
    """The colon after a file name is punctuation, so it stays in Calibri."""
    for p in shape_named(slide, "TextBox 3").text_frame.paragraphs:
        runs = p.runs
        for run, after in zip(runs, runs[1:]):
            if run.font.name == E.FONT_MONO and run.text.endswith(":"):
                run.text = run.text[:-1]
                after.text = ":" + after.text


def slide3(s):
    tiles = [sh for sh in s.shapes if sh.shape_type == 1 and sh.fill.type == 1 and str(sh.fill.fore_color.rgb) == "FF6B6B"]
    assert len(tiles) == 1, len(tiles)
    tiles[0].fill.fore_color.rgb = E.ALERT_RED
    for sh in s.shapes:
        if sh.has_text_frame and sh.text_frame.text == "Week 5: K8s – Pods, ReplicaSets":
            return
    raise SystemExit("slide 3: the Week 5 label is missing")


def slide6(s):
    for name in ("TextBox 16", "TextBox 17", "TextBox 20", "TextBox 21"):
        for r in shape_named(s, name).text_frame.paragraphs[0].runs:
            r.font.bold = True
            r.font.color.rgb = SLATE
    # The 10 lines of generic-pod.yaml keep the taller terminal of v5.
    assert shape_named(s, "Rectangle 4").height == Inches(2.85)
    # The table ends where the terminal ends.
    for name in ("Rectangle 11", "Rectangle 15", "Rectangle 19"):
        shape_named(s, name).width = Inches(12.10)


def slide9(s):
    remove_shape(s, "Rounded Rectangle 11")
    remove_shape(s, "TextBox 12")
    remove_shape(s, "Rounded Rectangle 13")
    remove_shape(s, "TextBox 14")
    zone(s, 5.65, 2.25, 3.9, 1.8, "Container", color=SLATE)
    box(s, 5.85, 2.65, 3.5, 1.2, "Environment variables", STEPS[1], size=15)
    box(s, 5.8, 4.45, 3.6, 1.65, "ConfigMap volume", STEPS[3], size=15)


def slide12(s):
    for shape, text, x in (("Rounded Rectangle 15", "development", 5.25), ("Rounded Rectangle 22", "production", 9.15)):
        remove_shape(s, shape)
        box(s, x + 1.9, 2.85, 1.6, 2.3, "ConfigMap\napp-config\n\n%s\nvalues" % text, STEPS[3], size=13)
    remove_shape(s, "TextBox 16")
    remove_shape(s, "TextBox 23")


def slide14(s):
    para = paragraph_with(s, "TextBox 3", "The data field must hold base64 strings. The stringData field takes plain text")
    para.runs[0].text = para.runs[0].text.replace("–", "•")
    para._p.pPr.set("marL", LEVEL_2)


def slide16(s):
    dy = Inches(0.65)
    for name in ("Rectangle 4", "Rectangle 5", "Oval 6", "Oval 7", "Oval 8", "TextBox 9", "TextBox 10",
                 "Rectangle 11", "Rectangle 12", "Oval 13", "Oval 14", "Oval 15", "TextBox 16", "TextBox 17"):
        shape_named(s, name).top += dy
    for name, height in (("Rectangle 4", 2.45), ("Rectangle 11", 2.45), ("TextBox 10", 2.0), ("TextBox 17", 2.0)):
        shape_named(s, name).height = Inches(height)
    shape_named(s, "TextBox 3").height = Inches(2.75)


def slide17(s):
    swap(s, "kube-api-access", "kube-api-access-<id>")
    swap(s, "kubernetes.io/serviceaccount/", "kubernetes.io/serviceaccount")


def slide18(s):
    shape_named(s, "Rectangle 4").height = Inches(1.35)
    shape_named(s, "TextBox 10").height = Inches(0.91)


def slide20(s):
    keep = {"TextBox 1", "Picture 5", "TextBox 7"}
    for sh in list(s.shapes):
        if sh.name not in keep and sh.shape_type != 9:
            sh._element.getparent().remove(sh._element)
    zone(s, 0.6, 1.5, 7.5, 5.15, "Pod", color=STEPS[1], fill=E.CARD_BG)
    zone(s, 0.75, 1.9, 3.75, 4.6, "Container: webapp", color=SLATE)
    rows = [(2.45, "/etc/app-config", "ConfigMap volume", "ConfigMap app-config\nAPP_COLOR, APP_MODE"),
            (3.85, "/etc/secret-volume", "Secret volume", "Secret app-secret\nDB_Host, DB_Password")]
    for y, path, volume, source in rows:
        box(s, 0.9, y, 3.45, 0.95, path, SLATE, size=13)
        arrow(s, RIGHT, 4.55, y + 0.3, 0.5, 0.34)
        box(s, 5.1, y, 2.85, 0.95, volume, STEPS[3], size=13)
        arrow(s, RIGHT, 8.0, y + 0.3, 0.55, 0.34)
        box(s, 8.6, y, 4.2, 0.95, source, STEPS[5], size=13)
    box(s, 0.9, 5.25, 3.45, 0.95, "Environment variable\nAPP_COLOR", STEPS[3], size=13)
    arrow(s, RIGHT, 4.55, 5.55, 4.0, 0.34)
    box(s, 8.6, 5.25, 4.2, 0.95, "ConfigMap app-config\nAPP_COLOR", STEPS[5], size=13)


DIAGRAMS = {3: slide3, 6: slide6, 9: slide9, 12: slide12, 14: slide14, 16: slide16, 17: slide17, 18: slide18, 20: slide20}


def footer_guard(prs):
    """Keep all content above y = 6.70 in."""
    limit = Inches(FOOTER_GUARD)
    for slide in prs.slides:
        for sh in slide.shapes:
            if sh.top < Inches(6.5) and sh.top + sh.height > limit:
                sh.height = limit - sh.top


def finish(prs, title):
    """The file properties, the picture names, and no blank thumbnail."""
    prs.core_properties.title = title
    prs.core_properties.author = "Maziar Sojoudian"
    prs.core_properties.last_modified_by = "Maziar Sojoudian"
    prs.core_properties.comments = ""
    for slide in prs.slides:
        for sh in slide.shapes:
            if sh.shape_type == 13:
                name = "Kubernetes logo" if sh.width > 914400 else "Docker whale logo"
                sh._element.xpath(".//p:cNvPr")[0].set("descr", name)
    rels = prs.part.package._rels
    for rid in [k for k, rel in rels.items() if rel.reltype.endswith("/thumbnail")]:
        rels.pop(rid)


def slide4_terminals(slide):
    frame = shape_named(slide, "TextBox 17").text_frame
    blank = [p for p in frame.paragraphs if not p.text.strip()]
    assert len(blank) == 2, len(blank)
    blank[1]._p.getparent().remove(blank[1]._p)
    for name in ("TextBox 10", "TextBox 17"):
        set_size(slide, name, 9)
        for p in shape_named(slide, name).text_frame.paragraphs:
            p.line_spacing = 1.15


def main():
    prs = Presentation(SRC)
    assert len(prs.slides) == TOTAL
    slides = prs.slides
    for no, text in TITLES.items():
        set_title(slides[no - 1], text)
    for no, pairs in REPLACE.items():
        for old, new in pairs:
            swap(slides[no - 1], old, new)
    for no, texts in REMOVE.items():
        for text in texts:
            para = paragraph_with(slides[no - 1], "TextBox 3", text)
            para._p.getparent().remove(para._p)
    for no, pairs in BULLETS.items():
        for old, new in pairs:
            paragraph_with(slides[no - 1], "TextBox 3", old).runs[-1].text = new
    for no, sizes in BODY_SIZES.items():
        body_sizes(slides[no - 1], sizes)
    add_bullet(slides[1], "TextBox 3", "Reading the ServiceAccount token of a Pod")
    slide4_terminals(slides[3])
    set_size(slides[10], "TextBox 10", 10)
    for no, name, lines, size, bar, kind in TERMINALS:
        set_lines(slides[no - 1], name, lines, size, yaml=(kind == "yaml"))
        recolor(slides[no - 1], name, kind)
        if bar:
            bar_name = "TextBox 8" if no == 7 else ("TextBox 9" if name == "TextBox 10" else "TextBox 16")
            shape_named(slides[no - 1], bar_name).text_frame.paragraphs[0].runs[0].text = bar
    for no, name, text in BARS:
        shape_named(slides[no - 1], name).text_frame.paragraphs[0].runs[0].text = text
    for no, draw in DIAGRAMS.items():
        draw(slides[no - 1])
    for no, tokens in BODY_CODE.items():
        inline_code(slides[no - 1], tokens)
    for no, tokens in DIAGRAM_CODE.items():
        inline_code(slides[no - 1], tokens, body=False)
    inline_code(slides[19], ["webapp"], body=False, min_height=0.25)
    colon_outside(slides[15])
    footer_guard(prs)
    finish(prs, "CLO835 Week 12 Lecture: ConfigMaps and Secrets")
    E._sanitize_coords(prs)
    prs.save(OUT)
    print("wrote %s (%d slides)" % (OUT, TOTAL))


if __name__ == "__main__":
    main()
