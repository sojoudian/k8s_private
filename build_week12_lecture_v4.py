# -*- coding: utf-8 -*-
"""CLO835 Week 12 lecture v4 - ConfigMaps and Secrets.

Fixes every lecture defect of reports/report-2026-10-31-09-week12-standards-audit.md:
L1 cover, L2 to L4 Course Outline (Week 15 is the project presentation), L5 to L8 and
L12, L13 commands that did not run, L9 to L11 wrong or old facts, L14 typing mistakes,
L15 third-party images replaced by native house diagrams, L16 dead links, L17 bullets
in ASD-STE100, L18 title style, L19 terminal titles and colors.

Input : Week12/Week12_v3.pptx (read, never written)
Output: Week12/Lecture_week12_v4.pptx

Run from the project root. It is guarded, so importing it writes nothing.
    python build_week12_lecture_v4.py
    python build_week12_lecture_v4.py --dump DIR    # write the manifests of the slides to DIR
"""
import copy
import os
import sys

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

import build_week08 as E
from build_week09_lecture_v6 import arrow, box, label, remove_shape, shape_named, zone
from build_week10_lecture_v8 import caption, large_picture, place, set_lines, set_size, swap

SRC = "Week12/Week12_v3.pptx"
OUT = "Week12/Lecture_week12_v4.pptx"
TOTAL = 21
SLATE, BLUE, STEPS = E.SLATE, E.BLUE, E.STEPS
RIGHT, LEFT = MSO_SHAPE.RIGHT_ARROW, MSO_SHAPE.LEFT_ARROW

OUTLINE = [
    ["Week 1: Docker Introduction"], ["Week 2: Docker Image Management"],
    ["Week 3: Docker Networking, Storage & Security"], ["Week 4: K8s Introduction"],
    ["Week 5: K8s- PODs, ReplicaSets"], ["Week 6: K8s – Services & Deployments"],
    ["Week 7: K8s – Volumes"], ["Week 8: Study Week"],
    ["Week 9: K8s – PVs & K8s in EKS"], ["Week 10: K8s – StorageClasses & StatefulSets"],
    ["Week 11: Exam & Mock Exam week"], ["Week 12: K8s – ConfigMaps & Secrets"],
    ["Week 13: K8s – RBAC and EKS"], ["Week 14: K8s – HPA", "Project presentation"],
    ["Week 15: Project presentation"], ["Term End"],
]

SECTION_POD = """apiVersion: v1
kind: Pod
metadata:
  name: webapp
  labels:
    name: webapp
spec:
  containers:
  - name: webapp
    image: maziar/kubia:v1
    ports:
    - containerPort: 8080
    envFrom:
    - %sRef:
        name: %s"""

MANIFESTS = {
    "fortune-sleeper.yaml": """apiVersion: v1
kind: Pod
metadata:
  name: fortune-sleeper-pod
spec:
  containers:
  - name: fortune-sleeper
    image: maziar/fortune:args
    command: ["sleep"]
    args: ["3600"]""",
    "config-map.yaml": """apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_COLOR: blue
  APP_MODE: prod""",
    "secret-data.yaml": """apiVersion: v1
kind: Secret
metadata:
  name: app-secret
data:
  DB_Host: bXlzcWw=
  DB_User: cm9vdA==
  DB_Password: cGFzd3Jk""",
    "pod-configmap.yaml": SECTION_POD % ("configMap", "app-config"),
    "pod-secret.yaml": SECTION_POD % ("secret", "app-secret"),
}

# slide, text box, lines, font size, text box of the title bar, its text, kind of text
SLIDE7 = ["# The image maziar/fortune:args",
          'ENTRYPOINT ["/bin/fortuneloop.sh"]', 'CMD ["10"]', "",
          "# command replaces ENTRYPOINT. args replaces CMD."] + MANIFESTS["fortune-sleeper.yaml"].split("\n")
IMPERATIVE_CM = ["kubectl create configmap \\", "    <config-name> --from-literal=<key>=<value>", "",
                 "kubectl create configmap \\", "    app-config --from-literal=APP_COLOR=blue \\",
                 "    --from-literal=APP_MODE=prod", "",
                 "kubectl create configmap \\", "    <config-name> --from-file=<path-to-file>", "",
                 "kubectl create configmap \\", "    app-config --from-file=app_config.properties"]
IMPERATIVE_SECRET = ["kubectl create secret generic \\", "    <secret-name> --from-literal=<key>=<value>", "",
                     "kubectl create secret generic \\", "    app-secret --from-literal=DB_Host=mysql \\",
                     "    --from-literal=DB_User=root \\", "    --from-literal=DB_Password=paswrd", "",
                     "kubectl create secret generic \\", "    <secret-name> --from-file=<path-to-file>", "",
                     "kubectl create secret generic \\", "    app-secret --from-file=app_secret.properties"]
TOKEN_COMMANDS = ["# Since v1.24, Kubernetes makes no token Secret.",
                  "kubectl get secrets -n week12", "",
                  "# The Pod gets the token as files.",
                  "kubectl exec secret-pod -n week12 -- \\",
                  "    ls /var/run/secrets/kubernetes.io/serviceaccount"]
TOKEN_OUTPUT = ["NAME         TYPE     DATA   AGE", "app-secret   Opaque   2      10s", "",
                "ca.crt", "namespace", "token"]
TERMINALS = [
    (7, "TextBox 9", SLIDE7, 12, "TextBox 8", "Dockerfile and fortune-sleeper.yaml", "yaml"),
    (10, "TextBox 10", IMPERATIVE_CM, 11, None, None, "cmd"),
    (10, "TextBox 17", MANIFESTS["config-map.yaml"].split("\n") + ["", "kubectl create -f config-map.yaml"], 11,
     None, None, "yaml"),
    (11, "TextBox 10", MANIFESTS["pod-configmap.yaml"].split("\n"), 11, "TextBox 9", "pod-definition.yaml", "yaml"),
    (14, "TextBox 10", IMPERATIVE_SECRET, 10, "TextBox 9", "imperative", "cmd"),
    (14, "TextBox 17", MANIFESTS["secret-data.yaml"].split("\n") + ["", "kubectl create -f secret-data.yaml"], 10,
     "TextBox 16", "declarative", "yaml"),
    (15, "TextBox 10", MANIFESTS["pod-secret.yaml"].split("\n"), 10, None, None, "yaml"),
    (16, "TextBox 10", TOKEN_COMMANDS, 11, "TextBox 9", "commands", "cmd"),
    (16, "TextBox 17", TOKEN_OUTPUT, 11, "TextBox 16", "output", "out"),
    (18, "TextBox 10", ["$ kubectl exec secret-pod -n week12 -- mount | grep secret-volume"], 14, None, None, "cmd"),
]
BARS = [(4, "TextBox 9", "nginx.conf, part 1"), (4, "TextBox 16", "nginx.conf, part 2"),
        (5, "TextBox 9", "docker run and Dockerfile"), (8, "TextBox 9", "pod.yaml"),
        (11, "TextBox 16", "inject methods")]

TITLES = {
    5: "Reminder: Command-line Arguments in Docker",
    10: "ConfigMaps: Create", 11: "ConfigMaps: Inject",
    12: "Multiple Environments with ConfigMaps",
    13: "Storing Sensitive Data: Introducing Secrets",
    14: "Secrets: Create", 15: "Secrets: Inject",
    16: "ServiceAccount Tokens",
    17: "The ServiceAccount Token Volume of a Pod",
}

REPLACE = {
    1: [("Week 10 · Lecture", "Week 12 · Lecture"), ("“Week 10 feels like 100”", "“Week 12 feels like 100”")],
    2: [("Setting environment variables exposed to the app", "Setting environment variables for the application"),
        ("Configuring apps through ConfigMaps", "Configuring applications through ConfigMaps"),
        ("Passing sensitive information to apps through Secrets", "Passing sensitive data to applications through Secrets")],
    4: [("Application images are immutable. Should we bake the configuration data in? (not a great idea)",
         "Application images are immutable. Do not put the configuration data in the image"),
        ("Ways to pass configuration data to containerized applications by:",
         "You can give configuration data to a containerized application in 3 ways:"),
        ("Passing command-line arguments to containers", "Pass command-line arguments to the containers"),
        ("Setting custom environment variables for each container", "Set custom environment variables for each container"),
        ("Mounting configuration files into containers through a special type of volume",
         "Mount configuration files into the containers through a special type of volume")],
    5: [("ENTRYPOINT defines the executable invoked when the container is started.",
         "ENTRYPOINT sets the executable that runs when the container starts."),
        ("CMD specifies the arguments that get passed to the ENTRYPOINT.",
         "CMD sets the arguments that Docker gives to the ENTRYPOINT."),
        ("We can overwrite CMD arguments by providing command line parameters in docker cli",
         "You can replace the CMD arguments with parameters on the docker command line.")],
    6: [("We will usually override the CMD arguments only and not the process started in the container",
         "Usually, we replace the CMD arguments only, not the process in the container"),
        ("We will provide the process as well in generic images like busybox",
         "With a generic image, we also set the process"),
        ("The executable that's executed inside the container", "The executable that runs inside the container"),
        ("The arguments passed to the executable", "The arguments of the executable")],
    8: [("Variables are set at the container level, not a pod level", "You set variables for each container, not for the Pod"),
        ("Kubernetes automatically injects environment variables corresponding to all services in the namespace",
         "Kubernetes injects environment variables for all the Services in the namespace"),
        ("Drawbacks:", "Problems:"),
        ("Environment variables defined in the Pod manifest are hard coded. It makes it difficult to maintain different values in prod and nonprod environments",
         "The Pod manifest holds fixed values, so different values for production and development are difficult"),
        ("Configuration should not be part of the Pod description", "The Pod description should not hold the configuration")],
    9: [("ConfigMap is a resource in K8s", "A ConfigMap is a Kubernetes resource"),
        ("Contains key/value pairs", "It holds key/value pairs"),
        ("Configuration parameters made accessible to containers as environment variables of files in a mounted folder",
         "Containers get the values as environment variables or as files in a mounted folder")],
    10: [("2 Step Process", "A 2-step process:"), ("Create a Config Map", "Create a ConfigMap"),
         ("Inject a ConfigMap in the POD", "Inject the ConfigMap into the Pod")],
    11: [("Inject into POD", "Inject the ConfigMap into the Pod"),
         ("Can be used as just env variable, as a single env variable or file using Volume",
          "Use all the keys as variables, one key as a variable, or a volume with files")],
    12: [("Pods share the same manifest referencing configuration values from configMap",
          "Pods in each namespace use the same manifest, and it references a ConfigMap"),
         ("ConfigMaps are created from different manifests and have environment-specific values",
          "Each namespace has its own ConfigMap, with the values of that environment")],
    13: [("Key value pairs that are stored as base64 encoded strings", "A Secret holds key/value pairs as base64 strings"),
         ("Like configMaps, available to containers as environment variables or mounted files",
          "Like a ConfigMap, a Secret gives values to containers as environment variables or mounted files"),
         ("Never stored on the disk of the underlying host",
          "On a worker node, the kubelet keeps a Secret in memory (tmpfs), not on disk"),
         ("Stored in etcd", "etcd stores the Secret on the control-plane disk, and by default it is not encrypted"),
         ("Size is limited to 1MB", "The size limit is 1 MiB"),
         ("Available to application in its original form, application does not need to decode it",
          "The application gets the original value, so it does not decode it")],
    14: [("2 Step Process", "A 2-step process:"),
         ("Base64 format encoding. Need to provide encoded data", "The manifest must hold base64 encoded data"),
         ("Inject a Secret in the POD", "Inject the Secret into the Pod")],
    15: [("Inject into POD", "Inject the Secret into the Pod"),
         ("Do not check-in  secret objects to SCM", "Do not put Secret objects in source control"),
         ("Secrets in ETCD are not encrypted. Need to enable encryption at rest",
          "By default, Secrets in etcd are not encrypted. Turn on encryption at rest"),
         ("Anyone able to create pods/deployments in the same namespace has access to secrets.",
          "A user who can create Pods or Deployments in the namespace can read its Secrets"),
         ("Consider 3rd party secret store providers", "Consider an external secret store"),
         ("AWS, Azure etc.", "For example, AWS Secrets Manager")],
    16: [("Default secrets are mounted into every container we run unless specified otherwise",
          "Kubernetes mounts a ServiceAccount token into every container, unless you turn this off"),
         ("Default secrets are mounted as files into \"/var/run/secrets/kubernetes.io/serviceaccount\" folder in the container",
          "The files are in the folder /var/run/secrets/kubernetes.io/serviceaccount"),
         ("The folder has 3 entiries.", "The folder has 3 entries:"),
         ("Default secrets allow containers to communicate with K8s API using read-only permissions",
          "The token is short-lived, and no Secret holds it. The default ServiceAccount has API discovery permissions only")],
    18: [("# Secret volumes look like files on the disk at /ect/nginx/certs folder.",
          "A Secret volume looks like files in the folder /etc/secret-volume"),
         ("# It contradicts the statement that secrets are not stored on host's filesystem.",
          "The kubelet keeps these files in an in-memory file system (tmpfs)"),
         ("# K8s secrets are stored on \"in-memory filesystem\" /tmpfs",
          "The kubelet does not write them to the disk of the node"),
         ("# Sensitive data stored in a secret is never written to the disk where it could be compromised",
          "etcd on the control plane still stores the Secret")],
    19: [("Secrets can be provided to the containers via environment variables",
          "You can give a Secret to a container as an environment variable"),
         ("This is not the recommended way to use secrets", "This is not the recommended method"),
         ("Environment variables are often dumped into log files those exposing the secrets",
          "Applications often write environment variables to log files, and this exposes the Secret"),
         ("Child processes will inherit environment variables exposing application to the supply chain attack if the third-party libraries are compromised",
          "Child processes get the variables too. A compromised third-party library can then read the Secret")],
    21: [("https://github.com/sojoudian/simple-webapp-mysql", "https://kubernetes.io/docs/concepts/configuration/configmap/"),
         ("https://github.com/sojoudian/kubernetes-in-action/tree/master/Chapter07",
          "https://kubernetes.io/docs/concepts/security/service-accounts/")],
}


def set_title(slide, text):
    frame = shape_named(slide, "TextBox 1").text_frame
    para = frame.paragraphs[0]
    assert len(frame.paragraphs) == 1
    para.runs[0].text = text
    para.runs[0].font.size = Pt(30)
    for extra in para.runs[1:]:
        extra._r.getparent().remove(extra._r)


def title_rule(slide):
    rules = [sh for sh in slide.shapes if sh.shape_type == 9 and sh.top < Inches(2)]
    assert len(rules) == 1, len(rules)
    return rules[0]


def recolor(slide, name, kind):
    """A command is cyan and a comment is green. Output and continuation lines are gray."""
    for p in shape_named(slide, name).text_frame.paragraphs:
        for r in p.runs:
            line = r.text.lstrip()
            if line.startswith("#"):
                r.font.color.rgb = E.TERM_GRN
            elif kind == "cmd" and line.startswith(("kubectl", "$")):
                r.font.color.rgb = E.TERM_CYAN
            elif kind == "yaml" and line.startswith("kubectl"):
                r.font.color.rgb = E.TERM_CYAN
            elif kind != "yaml":
                r.font.color.rgb = E.TERM_GRAY


def set_outline(slide):
    boxes = [sh for sh in slide.shapes if sh.has_text_frame and sh.name != "TextBox 1" and sh.top < Inches(6.8)
             and sh.text_frame.text.strip()]
    assert len(boxes) == 16, len(boxes)
    boxes.sort(key=lambda sh: (sh.top, sh.left))
    for sh, lines in zip(boxes, OUTLINE):
        frame = sh.text_frame
        while len(frame.paragraphs) > len(lines):
            frame.paragraphs[-1]._p.getparent().remove(frame.paragraphs[-1]._p)
        while len(frame.paragraphs) < len(lines):
            frame._txBody.append(copy.deepcopy(frame.paragraphs[0]._p))
        for p, line in zip(frame.paragraphs, lines):
            p.runs[0].text = line
    current = boxes[11]
    frame = [sh for sh in slide.shapes if sh.shape_type == 1 and sh.top == current.top
             and abs(sh.left - (current.left - Inches(0.16))) < Inches(0.02)]
    assert len(frame) == 1, len(frame)
    frame[0].fill.solid()
    frame[0].fill.fore_color.rgb = BLUE
    for r in current.text_frame.paragraphs[0].runs:
        r.font.bold = True
        r.font.color.rgb = E.WHITE


def slide9(s):
    remove_shape(s, "Rectangle 4")
    zone(s, 5.5, 1.85, 4.2, 4.6, "Pod", color=STEPS[1], fill=E.CARD_BG)
    box(s, 5.8, 2.4, 3.6, 1.45, "Environment variables", STEPS[1], size=15)
    box(s, 5.8, 4.45, 3.6, 1.65, "configMap volume", STEPS[3], size=15)
    box(s, 10.4, 2.4, 2.3, 3.7, "ConfigMap\n\nkey1=value1\nkey2=value2", SLATE, size=15)
    arrow(s, LEFT, 9.75, 2.95, 0.6, 0.36)
    arrow(s, LEFT, 9.75, 5.1, 0.6, 0.36)


def slide12(s):
    remove_shape(s, "Rectangle 4")
    label(s, 5.25, 1.75, 7.55, 0.4, "ConfigMaps come from different manifests", size=13.5)
    for x, name, values in ((5.25, "Namespace: development", "development values"),
                            (9.15, "Namespace: production", "production values")):
        zone(s, x, 2.2, 3.65, 3.2, name, color=BLUE)
        box(s, x + 0.15, 2.85, 1.3, 2.3, "Pods", STEPS[1], size=14)
        arrow(s, RIGHT, x + 1.49, 3.82, 0.36, 0.34)
        box(s, x + 1.9, 2.85, 1.6, 2.3, "ConfigMap\napp-config\n\n" + values, STEPS[3], size=13)
    label(s, 5.25, 5.5, 7.55, 0.4, "Pods come from the same manifest", size=13.5)


def slide17(s):
    remove_shape(s, "Rectangle 3")
    zone(s, 0.7, 1.6, 7.7, 5.05, "Pod", color=STEPS[1], fill=E.CARD_BG)
    zone(s, 0.95, 2.05, 4.3, 4.35, "Container", color=SLATE)
    box(s, 1.15, 2.55, 3.9, 3.6, "/var/run/secrets/\nkubernetes.io/serviceaccount/\n\nca.crt\nnamespace\ntoken",
        SLATE, size=14)
    arrow(s, RIGHT, 5.3, 4.15, 0.4, 0.36)
    box(s, 5.75, 2.05, 2.4, 4.35, "Projected volume\n\nkube-api-access", STEPS[1], size=14)
    for y, text in ((1.8, "token\n\nfrom the TokenRequest API"), (3.45, "ca.crt\n\nfrom the ConfigMap kube-root-ca.crt"),
                    (5.1, "namespace\n\nfrom the Pod")):
        arrow(s, RIGHT, 8.2, y + 0.57, 0.65, 0.36)
        box(s, 8.9, y, 3.85, 1.5, text, STEPS[3], size=14)


def slide20(s):
    remove_shape(s, "Rectangle 3")
    zone(s, 0.6, 1.5, 7.5, 5.15, "Pod", color=STEPS[1], fill=E.CARD_BG)
    zone(s, 0.75, 1.9, 3.6, 2.7, "Container: web-server", color=SLATE)
    for y, text in ((2.3, "/etc/nginx/conf.d/"), (3.0, "/etc/nginx/certs/"), (3.7, "/usr/share/nginx/html/")):
        box(s, 0.9, y, 3.3, 0.6, text, SLATE, size=13)
        arrow(s, RIGHT, 4.4, y + 0.13, 0.55, 0.34)
    zone(s, 0.75, 4.7, 3.6, 1.85, "Container: html-generator", color=SLATE)
    box(s, 0.9, 5.1, 3.3, 0.6, "/var/htdocs", SLATE, size=13)
    arrow(s, RIGHT, 4.4, 5.23, 0.55, 0.34)
    box(s, 0.9, 5.8, 3.3, 0.6, "Variable INTERVAL=25", STEPS[3], size=13)
    box(s, 5.0, 2.3, 2.95, 0.6, "configMap volume", STEPS[3], size=13)
    box(s, 5.0, 3.0, 2.95, 0.6, "secret volume", STEPS[3], size=13)
    box(s, 5.0, 3.7, 2.95, 2.0, "emptyDir volume", STEPS[1], size=13)
    arrow(s, RIGHT, 8.0, 2.43, 0.55, 0.34)
    box(s, 8.6, 1.8, 4.2, 0.95, "ConfigMap fortune-config\nmy-nginx-config.conf, sleep-interval", STEPS[5], size=13)
    arrow(s, RIGHT, 8.0, 3.13, 0.55, 0.34)
    box(s, 8.6, 2.85, 4.2, 0.95, "Secret fortune-https\nhttps.cert, https.key, foo", STEPS[5], size=13)
    label(s, 8.6, 3.95, 4.2, 0.95, "INTERVAL comes from sleep-interval. The slide does not show the ServiceAccount token volume.",
          size=12.5, align=PP_ALIGN.LEFT)


DIAGRAMS = {9: slide9, 12: slide12, 17: slide17, 20: slide20}


def main():
    prs = Presentation(SRC)
    assert len(prs.slides) == TOTAL
    set_outline(prs.slides[2])
    for no, pairs in REPLACE.items():
        for old, new in pairs:
            swap(prs.slides[no - 1], old, new)
    for no, text in TITLES.items():
        set_title(prs.slides[no - 1], text)
    rule_top = title_rule(prs.slides[3]).top
    for no in (5, 17):
        place(shape_named(prs.slides[no - 1], "TextBox 1"), 0.55, 0.40, 12.20, 0.85)
        title_rule(prs.slides[no - 1]).top = rule_top
    for no, name, lines, size, bar, bar_text, kind in TERMINALS:
        set_lines(prs.slides[no - 1], name, lines, size, yaml=(kind == "yaml"))
        recolor(prs.slides[no - 1], name, kind)
        if bar:
            shape_named(prs.slides[no - 1], bar).text_frame.paragraphs[0].runs[0].text = bar_text
    for no, name, text in BARS:
        shape_named(prs.slides[no - 1], name).text_frame.paragraphs[0].runs[0].text = text
    recolor(prs.slides[3], "TextBox 10", "out")
    set_size(prs.slides[10], "TextBox 17", 11)
    set_size(prs.slides[14], "TextBox 17", 10)
    for no, draw in DIAGRAMS.items():
        remove_shape(prs.slides[no - 1], large_picture(prs.slides[no - 1]))
        draw(prs.slides[no - 1])
    place(shape_named(prs.slides[16 - 1], "TextBox 3"), 0.60, 1.45, 12.10, 2.10)
    # The terminals of these slides ended in the footer band.
    for no in (4, 11, 14, 15, 16):
        for sh in prs.slides[no - 1].shapes:
            if sh.top + sh.height > Inches(6.75) and sh.top < Inches(6.5) and sh.name != "TextBox 3":
                sh.height = Inches(6.75) - sh.top
    E._sanitize_coords(prs)
    prs.save(OUT)
    print("wrote %s (%d slides)" % (OUT, TOTAL))


if __name__ == "__main__":
    if "--dump" in sys.argv:
        folder = sys.argv[sys.argv.index("--dump") + 1]
        for name, text in MANIFESTS.items():
            with open(os.path.join(folder, name), "w") as f:
                f.write(text + "\n")
    else:
        main()
