# -*- coding: utf-8 -*-
"""CLO835 Week 12 lecture v7 - ConfigMaps and Secrets.

v7 applies CLO835_STANDARDS.md (2026-11-10) to lecture v6. v6 stays on disk. The main changes:
- The slide kit of build_week07_lecture_v7.py: the cover title at 34 pt, the Course Outline at 12 pt
  with "Kubernetes", tab bullets, and house terminals (B1 to B6).
- The standard structure (B7): part dividers, Optional Topics, Key Takeaways, and
  "Lab Week 12 at a Glance".
- The examples use the objects of the lab (app-config, config-env, config-volume, app-secret,
  secret-pod, week12-dev). Each terminal labeled "Lab Week 12, Step N" takes its lines from
  build_week12_lab_v6.py, so the lecture and the lab cannot differ (C8). The sample outputs come from
  the live run of lab v6 on 2026-11-10 (Kubernetes v1.35.10).
- The words of the glossary (A1): directory, create, Kubernetes; no phrasal verbs.
- Each sample output line is a comment ("# ...") under its command (B5). The outputs are the live
  outputs of the lab run; no output is shortened or made up.
- The labels "Concept only: the lab does not run X." on the nginx, docker run and base64 examples (B7).
- After the independent review of 2026-11-10: A1 words ("configures", no "makes"); the reason why an
  image holds no configuration data; the condition of the Service variables; one statement of env,
  of the external store and of the Secret volume files; "within about one minute"; "Three common
  types"; the data of an immutable object; the ServiceAccount can also stop the token (v1.22, v1.24);
  code names in Consolas (zone_code, mono_head); the slide 14 arrow from the source; no command in a
  file panel; the four log lines of Step 1; the full "Not in the lab" note on slide 27.
- After review round 2 (2026-11-11): titles with no -ing form (slides 5, 16, 20, 24) and no two equal
  titles (slide 10); no fragment card (the config-env.yaml part left slide 8); points stated at most two
  times (slide 7 bullet, slide 17 bullet); a "Concept only" label on slide 21, and slide 21 left the
  Step 4 cell; "inject" as the one verb; "mount with subPath"; LOG_LEVEL in the slide 14 box; the Pod
  field has priority over the ServiceAccount field (slide 22); the TokenRequest token (v1.22) and no token
  Secret (v1.24) as two facts; "command and no args" ignores CMD (probe3.log).
- Lab v7 (standards v1.2, 2026-11-11) has no cleanup script, so Step 6 on slide 27 is "Destroy the
  cluster". Steps 1 to 5 of lab v7 are those of lab v6, so this builder still imports build_week12_lab_v6.
- After review round 3 (2026-11-11, scratchpad w12review/round3_decks.md): the divider of Part 1 says
  "command, args and env" (the point "configuration data outside the image" stays on slide 5 and in the
  takeaways); slides 7 and 14 show the kubectl wait of the lab; "within about two minutes" (kubelet sync
  period plus cache TTL); "stable in v1.22"; the token volume is inside the Pod on slide 23; "Your own
  projected volume"; the takeaway on base64 names the plain bytes in etcd; slide 27 names four more topics
  that the lab does not run; the security checklist of kubernetes.io supports slide 21 and is a reference.
- After review round 4 (2026-11-11, scratchpad w12review4/round4_decks.md): "does not watch" (no -ing form);
  slide 27 maps Step 1 to slide 5 too, and its notes name the Service environment variables and the projected
  volume; slide 19 says that mountPath sets the directory; the Part 1 divider has no code names in Calibri;
  slide 12 says "does not exist".
- After review round 5 (scratchpad w12review5/round5_decks.md): the fourth note line of slide 27 has 24
  words; its first line says "a value that you encode with base64"; the token line of slide 22 is a noun phrase.
- After review round 6 (scratchpad w12review6/round6_decks.md): "Since v1.22, the kubelet gets the token
  from the TokenRequest API" (TokenRequest is stable in v1.20; the bound token volume in v1.22); one
  instruction in one sentence on slides 11 and 27; the fourth note line of slide 27 has its articles.
- After review round 7 (scratchpad w12review7/round7_decks.md): "the permission to create Pods" (one word for
  one meaning: "right" is a direction in the lab); the caption of slide 24 is a full sentence.
- The cover has no subtitle. The v6 cover had the quote "Week 12 feels like 100"; A1 (ASD-STE100) forbids
  slang, so v7 does not keep it.
- New facts, each checked: a missing key stops the container start unless optional is true; a volume
  with subPath gets no update; tmpfs does not protect against kubectl exec or the API; data and
  stringData; the Secret types; immutable ConfigMaps and Secrets (stable in v1.21).

Input : Week12/Lecture_week12_v6.pptx, for the cover and the outline (read, never written)
Output: Week12/Lecture_week12_v7.pptx (the build refuses to overwrite it)

Run from the project root. It is guarded, so importing it writes nothing.
    .venv/bin/python build_week12_lecture_v7.py
"""
import os
import sys

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

import build_week08 as E
import build_week12_lab_v1 as lab1
import build_week12_lab_v6 as lab
from build_week07_lecture_v7 import (BLUE, DOWN, LEFT, RIGHT, SLATE, STEPS, TOP, UP, agenda, arrow, box, bullets,
                                     caution, cover, grid, keep_first, new_slide, number_and_save, outline, rich,
                                     runs, term, text_slide, zone)

VERSION = "v7"
SRC = "Week12/Lecture_week12_v6.pptx"
OUT = "Week12/Lecture_week12_%s.pptx" % VERSION

# ---------------------------------------------------------------- the lab, as the single source of each command
LAB = {n: lab.SLIDES[2 + n][3] for n in range(1, 6)}       # Step 1 to Step 5 of Lab_week12_v6


def pick(step, *starts):
    """The lines of lab step `step` that start with one of `starts`, with their continuation lines."""
    lines, out, k = LAB[step], [], 0
    while k < len(lines):
        line = lines[k]
        if any(line.startswith(st) for st in starts):
            out.append(line)
            while line.rstrip().endswith("\\"):
                k += 1
                line = lines[k]
                out.append(line)
        k += 1
    missing = [st for st in starts if not any(l.startswith(st) for l in out)]
    assert not missing, (step, missing)
    return out


def run(step, *pairs):
    """Each lab command (found by its start) followed by its live output as comment lines (B5)."""
    out = []
    for start, output in pairs:
        out += pick(step, start) + ["# " + o for o in output]
    return out


ARGS_POD = lab1.ARGS_POD
CM_ENV_POD = lab.CM_ENV_POD
CM_VOL_POD = lab.no_busybox(lab1.CM_VOL_POD)
SECRET_POD = lab.SECRET_POD
DEV = lab.DEV
DEV_CM = DEV[DEV.index("kind: ConfigMap") - 1:DEV.index("  APP_MODE: dev") + 1]
DEV_SECRET = DEV[DEV.index("kind: Secret") - 1:]

NGINX = """user  nginx;
worker_processes  auto;
error_log  /var/log/nginx/error.log notice;

events {
    worker_connections  1024;
}

http {
    include       /etc/nginx/mime.types;
    sendfile      on;
    server {
        listen       80;
        root         /usr/share/nginx/html;
    }
}""".split("\n")

DOCKER = """FROM ubuntu:latest
RUN apt-get update ; apt-get -y install fortune
ADD fortuneloop.sh /bin/fortuneloop.sh
ENTRYPOINT ["/bin/fortuneloop.sh"]
CMD ["10"]

$ docker run -it docker.io/maziar/fortune:args 15
# 15 replaces CMD ["10"]: a new fortune every 15 s.""".split("\n")


def divider(prs, kicker, text, subtitle):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    E.divider(s, kicker, text, subtitle)
    return s


def zone_code(s, x, y, w, h, label, color=SLATE, fill=E.WHITE):
    """zone() of the kit, but backticks in the label mark a code name in Consolas (B3)."""
    E.add_rounded_rect(s, E.Inches(x), E.Inches(y), E.Inches(w), E.Inches(h), fill, line=color, line_width=1.25,
                       radius_ratio=0.03)
    tb = s.shapes.add_textbox(E.Inches(x + 0.14), E.Inches(y + 0.07), E.Inches(w - 0.28), E.Inches(0.3))
    frame = tb.text_frame
    frame.margin_left = frame.margin_right = frame.margin_top = frame.margin_bottom = 0
    runs(frame.paragraphs[0], label, 12, color=color, bold=True, code_color=color)


def code_box(s, x, y, w, h, head, code, fill, size=13, mono_head=False):
    """A box with a heading in Calibri and code lines in Consolas (white on the fill color).
    mono_head=True: the heading is a code name too (B3), so it is in Consolas."""
    E.add_rounded_rect(s, E.Inches(x), E.Inches(y), E.Inches(w), E.Inches(h), fill, radius_ratio=0.10)
    lines = [head] + (code.split("\n") if code else [])
    tb = E.add_text(s, E.Inches(x + 0.08), E.Inches(y), E.Inches(w - 0.16), E.Inches(h), lines, size=size,
                    bold=True, color=E.WHITE, align=E.CENTER, anchor=E.MIDDLE, line_spacing=1.05)
    for p in tb.text_frame.paragraphs[1:]:
        for r in p.runs:
            r.font.name = E.FONT_MONO
            r.font.bold = False
    if mono_head:
        for r in tb.text_frame.paragraphs[0].runs:
            r.font.name = E.FONT_MONO


def concept(s, x, y, w, text):
    """The label of B7 for a concept that the lab does not run."""
    rich(s, x, y, w, 0.45, text, size=13, color=E.MUTED)


def caption(s, y, text, x=0.70, w=11.95):
    rich(s, x, y, w, 0.42, text, size=14, color=E.MUTED, align=PP_ALIGN.CENTER)


# ---------------------------------------------------------------- Part 1: arguments and environment variables

def s_part1(prs):
    return divider(prs, "Part 1", "Arguments and Environment Variables",
                   "The command, the arguments and the environment variables of a container")


def s_config(prs):
    s = new_slide(prs, "Configuration Data of an Application")
    bullets(s, 0.60, 1.65, 6.30, [
        (0, "An application image is immutable, so each change of a value in the image needs a new image. "
            "Do not put the configuration data in the image"),
        (0, "Kubernetes injects the configuration data into a container with three methods:"),
        (1, "Command-line arguments: `command` and `args`"),
        (1, "Environment variables: `env` and `envFrom`"),
        (1, "Files in a volume, from a ConfigMap or a Secret"),
        (0, "Many applications read a configuration file. Example: `nginx.conf` configures the nginx web server")],
        size=16, after=8, h=3.90)
    term(s, 7.20, 1.65, 5.50, "nginx.conf (example only)", NGINX, size=11, spacing=1.05)
    # A line of a configuration file is no error: the gray of the file, not the red of an error line.
    for sh in s.shapes:
        if sh.has_text_frame:
            for par in sh.text_frame.paragraphs:
                for r in par.runs:
                    if r.text.startswith("error_log"):
                        r.font.color.rgb = E.TERM_GRAY
    concept(s, 0.60, 5.75, 6.30, "Concept only: the lab does not run nginx.")
    return s


def s_docker(prs):
    s = new_slide(prs, "Reminder: Command-line Arguments in Docker")
    bullets(s, 0.60, 1.65, 12.10, [
        (0, "Two Dockerfile instructions set what a container runs:"),
        (1, "`ENTRYPOINT` sets the executable that runs when the container starts"),
        (1, "`CMD` sets the arguments that Docker gives to the `ENTRYPOINT`"),
        (1, "A value after the image name in `docker run` replaces the `CMD` arguments")],
        size=16, after=6, h=1.95)
    y = term(s, 0.60, 3.75, 12.10, "Dockerfile of maziar/fortune:args, and docker run (example only)", DOCKER,
             size=12, spacing=1.05)
    concept(s, 0.60, y + 0.15, 12.10, "Concept only: the lab does not run `docker run`. Step 1 uses this image.")
    return s


def s_args(prs):
    s = new_slide(prs, "command and args in Kubernetes")
    end = grid(s, 0.60, 1.65, [1.50, 1.60, 2.70], [
        ["Docker", "Kubernetes", "Meaning"],
        ["`ENTRYPOINT`", "`command`", "The executable that runs in the container"],
        ["`CMD`", "`args`", "The arguments of the executable"]], row_h=0.70, size=13)
    bullets(s, 0.60, end + 0.30, 5.80, [
        (0, "Usually, you set `args` only"),
        (0, "When you set `command` and no `args`, the container also ignores the `CMD` of the image"),
        (0, "With a generic image, for example `maziar/alpine-curl`, you set both: `command: [\"sleep\"]` and "
            "`args: [\"3600\"]`")], size=15, after=6, h=2.40)
    y = term(s, 6.65, 1.65, 6.05, "fortune-args.yaml (Lab Week 12, Step 1)", ARGS_POD, size=11, spacing=1.05)
    term(s, 6.65, y + 0.20, 6.05, "Lab Week 12, Step 1",
         run(1, ("$ kubectl apply", ["pod/fortune-args created"])) +
         ["$ kubectl wait --for=condition=Ready pod/fortune-args \\", "    " + lab.N + " --timeout=120s",
          "# pod/fortune-args condition met"] +
         run(1, ("$ sleep 6;", ["Configured to generate new fortune every 2 seconds",
                             "Wed Nov 11 03:54:30 UTC 2026 Writing fortune to /var/htdocs/index.html",
                             "Wed Nov 11 03:54:32 UTC 2026 Writing fortune to /var/htdocs/index.html",
                             "Wed Nov 11 03:54:34 UTC 2026 Writing fortune to /var/htdocs/index.html"])),
         size=10, spacing=1.05)
    return s


def s_env(prs):
    s = new_slide(prs, "Environment Variables in the Pod Manifest")
    bullets(s, 0.60, 1.65, 12.10, [
        (0, "You set environment variables for each container, not for the Pod"),
        (0, "`env` sets a name and a value. The value is fixed in the manifest"),
        (0, "The kubelet also injects environment variables for the Services of the namespace that exist when "
            "the container starts, and `KUBERNETES_SERVICE_HOST` for the API server"),
        (0, "A fixed value needs one manifest for each environment, for example development and production. "
            "A ConfigMap prevents this")], size=18, after=12, h=4.60)
    return s


# ---------------------------------------------------------------- Part 2: ConfigMaps

def s_part2(prs):
    return divider(prs, "Part 2", "ConfigMaps", "Configuration data as a Kubernetes object")


def s_cm(prs):
    s = new_slide(prs, "The ConfigMap Object")
    bullets(s, 0.60, 1.70, 5.60, [
        (0, "A ConfigMap is a Kubernetes object in a namespace"),
        (0, "It holds key/value pairs, up to 1 MiB"),
        (0, "A container gets the values as environment variables, or as files in a volume"),
        (0, "The Pod and the ConfigMap must be in the same namespace")], size=16, after=10, h=4.40)
    zone(s, 6.50, 1.70, 3.70, 4.50, "Pod", color=STEPS[1], fill=E.CARD_BG)
    zone(s, 6.75, 2.15, 3.20, 1.75, "Container", color=SLATE)
    box(s, 7.00, 2.60, 2.70, 1.05, "Environment variables", STEPS[1], size=15)
    box(s, 6.75, 4.30, 3.20, 1.55, "ConfigMap volume", STEPS[3], size=15)
    code_box(s, 10.95, 2.40, 1.75, 3.20, "ConfigMap", "app-config\n \nAPP_COLOR\nAPP_MODE\nLOG_LEVEL", SLATE, size=13)
    arrow(s, LEFT, 10.25, 2.92, 0.60, 0.42)
    arrow(s, LEFT, 10.25, 4.86, 0.60, 0.42)
    return s


def s_cm_create(prs):
    s = new_slide(prs, "ConfigMaps: Create")
    bullets(s, 0.60, 1.62, 12.10, [
        (0, "Create the ConfigMap first. Then inject it into the Pod"),
        (0, "Imperative: `--from-literal` gives a key and a value. `--from-file` creates one key from a file, and "
            "the file name is the key"),
        (0, "Declarative: a manifest with a `data` field, and `kubectl apply`")], size=15, after=5, h=1.55)
    term(s, 0.60, 3.35, 6.40, "Lab Week 12, Step 2",
         run(2, ("$ printf", []), ("$ kubectl create configmap", ["configmap/app-config created"])), size=11,
         spacing=1.05)
    term(s, 7.25, 3.35, 5.45, "config-dev.yaml, the ConfigMap (Lab Week 12, Step 5)",
         DEV_CM, size=11, spacing=1.05)
    return s


def s_cm_env(prs):
    s = new_slide(prs, "ConfigMaps: Inject as Environment Variables")
    bullets(s, 0.60, 1.62, 6.60, [
        (0, "`valueFrom` with `configMapKeyRef` reads one key into a new name"),
        (0, "`envFrom` with `configMapRef` injects every key. The key is the name"),
        (0, "If the ConfigMap or the key does not exist, the container does not start, unless the reference sets "
            "`optional: true`")], size=14, after=5, h=2.70)
    term(s, 0.60, 4.45, 6.60, "Lab Week 12, Step 2",
         run(2, ("$ kubectl exec", ["hello", "blue", "blue", "prod", "debug", "10.96.0.1"])), size=10,
         spacing=1.0)
    term(s, 7.45, 1.62, 5.25, "config-env.yaml (Lab Week 12, Step 2)", CM_ENV_POD, size=10.5, spacing=1.0)
    return s


def s_cm_vol(prs):
    s = new_slide(prs, "A ConfigMap as a Volume")
    bullets(s, 0.60, 1.62, 6.60, [
        (0, "Each key becomes a file in the volume. The file name is the key"),
        (0, "When the ConfigMap changes, the kubelet updates the files within about two minutes"),
        (0, "An environment variable gets its value when the container starts. It does not change"),
        (0, "A mount with `subPath` gets no update")], size=14, after=5, h=2.45)
    term(s, 0.60, 4.15, 6.60, "Lab Week 12, Step 3",
         run(3, ("$ kubectl patch", ["configmap/app-config patched"]), ("$ until", ["green"]),
             ("$ kubectl exec config-env", ["blue"])), size=10, spacing=1.0)
    term(s, 7.45, 1.62, 5.25, "config-volume.yaml (Lab Week 12, Step 3)", CM_VOL_POD, size=10.5, spacing=1.0)
    return s


def s_envs(prs):
    s = new_slide(prs, "Multiple Environments with ConfigMaps")
    bullets(s, 0.60, 1.70, 5.30, [
        (0, "The Pods of each namespace come from the same manifest, and it names the ConfigMap `app-config`"),
        (0, "Each namespace has its own `app-config`, with the values of that environment")],
        size=15, after=8, h=2.60)
    for x, ns, vals in ((6.20, "Namespace: `week12`", "APP_COLOR=blue\nAPP_MODE=prod\nLOG_LEVEL=debug"),
                        (9.50, "Namespace: `week12-dev`", "APP_COLOR=red\nAPP_MODE=dev")):
        zone_code(s, x, 1.62, 3.10, 2.73, ns, color=BLUE)
        code_box(s, x + 0.25, 2.02, 2.60, 0.72, "Pod", "config-env", STEPS[1], size=13)
        arrow(s, UP, x + 1.36, 2.78, 0.38, 0.32)     # from the source to the Pod, as on slides 10, 23 and 24
        code_box(s, x + 0.25, 3.10, 2.60, 1.20, "ConfigMap, at creation", "app-config\n" + vals, STEPS[3],
                 size=12)
    term(s, 0.60, 4.45, 12.10, "Lab Week 12, Step 5",
         run(5, ("$ kubectl apply -f config-dev.yaml", ["namespace/week12-dev created",
                                                        "configmap/app-config created", "secret/app-secret created"]),
             ("$ kubectl apply -f config-env.yaml", ["pod/config-env created"]),
             ("$ kubectl wait", ["pod/config-env condition met"]),
             ("$ kubectl exec config-env", ["red", "dev"])), size=9, spacing=1.0)
    return s


# ---------------------------------------------------------------- Part 3: Secrets

def s_part3(prs):
    return divider(prs, "Part 3", "Secrets", "Sensitive data for containers")


def s_secrets(prs):
    s = new_slide(prs, "The Secret Object")
    bullets(s, 0.60, 1.62, 12.10, [
        (0, "A Secret holds key/value pairs, and the API shows each value in base64"),
        (0, "base64 is an encoding, not encryption. Anyone can decode it, with no key"),
        (0, "etcd stores the Secret on the disk of the master node. The size limit is 1 MiB"),
        (0, "The container gets the decoded value, so the application does not decode it"),
        (0, "Three common types: `Opaque` (from `kubectl create secret generic`), `kubernetes.io/tls` and "
            "`kubernetes.io/dockerconfigjson`")], size=15, after=5, h=2.75)
    term(s, 0.60, 4.55, 12.10, "Lab Week 12, Step 4",
         run(4, ("$ printf", []), ("$ kubectl create secret", ["secret/app-secret created"]),
             ("$ kubectl get secret app-secret", ["paswrd"])), size=11, spacing=1.0)
    return s


def s_secret_decl(prs):
    s = new_slide(prs, "Secrets: Declarative")
    bullets(s, 0.60, 1.62, 6.40, [
        (0, "The `data` field must hold base64 strings"),
        (0, "The `stringData` field takes plain text, and Kubernetes encodes it"),
        (0, "Do not put a Secret manifest in source control")],
        size=15, after=6, h=2.30)
    y = term(s, 0.60, 4.00, 6.40, "base64 (example only)", [
        "$ echo -n dev-pass | base64", "# ZGV2LXBhc3M=", "$ echo ZGV2LXBhc3M= | base64 -d; echo", "# dev-pass"],
        size=11, spacing=1.05)
    concept(s, 0.60, y + 0.12, 6.40, "Concept only: the lab does not encode a value with base64.")
    term(s, 7.25, 1.62, 5.45, "config-dev.yaml, the Secret (Lab Week 12, Step 5)", DEV_SECRET, size=11,
         spacing=1.05)
    return s


def s_secret_inject(prs):
    s = new_slide(prs, "Secrets: Inject")
    bullets(s, 0.60, 1.62, 6.60, [
        (0, "A Secret uses the same references as a ConfigMap: one key, every key, or a volume"),
        (0, "`secretKeyRef` reads one key. `secretRef` injects every key")], size=15, after=6, h=1.90)
    term(s, 0.60, 3.70, 6.60, "Lab Week 12, Step 4",
         run(4, ("$ kubectl exec secret-pod " + lab.N + " -- printenv", ["paswrd", "mysql"]),
             ("$ kubectl exec secret-pod " + lab.N + " -- cat", ["mysql"])), size=10.5, spacing=1.05)
    term(s, 7.45, 1.62, 5.25, "secret-pod.yaml (Lab Week 12, Step 4)", SECRET_POD, size=9.5, spacing=1.0)
    return s


def s_tmpfs(prs):
    s = new_slide(prs, "How the Kubelet Stores a Secret Volume")
    bullets(s, 0.60, 1.62, 12.10, [
        (0, "With a Secret volume, each key of the Secret becomes a file in the directory that `mountPath` sets: "
            "`/etc/secret-volume`"),
        (0, "The kubelet stores these files in an in-memory file system (tmpfs), not on the disk of the node"),
        (0, "tmpfs does not protect the data from a user who can run `kubectl exec` in the Pod, or read the "
            "Secret through the API")], size=16, after=8, h=2.60)
    term(s, 0.60, 3.90, 12.10, "Lab Week 12, Step 4",
         run(4, ("$ kubectl exec secret-pod " + lab.N + " -- mount",
                 ["tmpfs on /etc/secret-volume type tmpfs (ro,relatime,size=7814532k,inode64,noswap)"])), size=12,
         spacing=1.05)
    return s


def s_protect(prs):
    s = new_slide(prs, "Protection of a Secret")
    bullets(s, 0.60, 1.62, 12.10, [
        (0, "By default, etcd stores a Secret as plain bytes. Configure encryption at rest"),
        (0, "A user who can create Pods in a namespace can read each Secret of that namespace. Limit this with RBAC")],
        size=15, after=6, h=1.85)
    term(s, 0.60, 3.05, 12.10, "Lab Week 12, Step 5",
         run(5, ("$ ETCD=", []), ("$ kubectl -n kube-system", ["dev-pass"])), size=11, spacing=1.05)
    return s


def s_env_note(prs):
    s = text_slide(prs, "Secrets as Environment Variables", [
        (0, "An environment variable is not the recommended method for a Secret"),
        (1, "Applications often write their environment variables to log files, and the log files then hold the "
            "Secret"),
        (1, "Each child process gets the environment variables too, so a third-party program can read the Secret"),
        (0, "A Secret volume is the better method")], size=18, after=12)
    concept(s, 0.60, 4.30, 12.10, "Concept only: the lab does not show a Secret in a log file or in a child process.")
    return s


def s_sa(prs):
    s = new_slide(prs, "ServiceAccount Tokens")
    bullets(s, 0.60, 1.58, 12.10, [
        (0, "Kubernetes mounts a ServiceAccount token into every container, unless "
            "`automountServiceAccountToken` is `false`. The field of the Pod has priority over the field of its "
            "ServiceAccount"),
        (0, "The files are in the directory `/var/run/secrets/kubernetes.io/serviceaccount`:"),
        (1, "`ca.crt`: the certificate that verifies the API server"),
        (1, "`namespace`: the namespace of the Pod"),
        (1, "`token`: the token that identifies the ServiceAccount to the API server"),
        (0, "Since v1.22, the kubelet gets the token from the TokenRequest API and renews it"),
        (0, "Since v1.24, Kubernetes creates no token Secret for a ServiceAccount"),
        (0, "The default ServiceAccount has API discovery permissions only")], size=14, after=2, h=2.85)
    term(s, 0.60, 4.50, 12.10, "Lab Week 12, Step 4",
         run(4, ("$ kubectl exec secret-pod " + lab.N + " -- ls", ["ca.crt", "namespace", "token"]),
             ("$ kubectl get secrets", ["NAME         TYPE     DATA   AGE", "app-secret   Opaque   2      28s"])),
         size=11, spacing=1.0)
    return s


def s_sa_vol(prs):
    s = new_slide(prs, "The ServiceAccount Token Volume of a Pod")
    # Review round 3: the projected volume is part of the Pod, so its box is inside the Pod box. Only the
    # sources of the files are outside the Pod.
    zone_code(s, 0.60, 1.70, 8.45, 4.40, "Pod `secret-pod`", color=STEPS[1], fill=E.CARD_BG)
    zone_code(s, 0.85, 2.15, 3.85, 3.70, "Container `app`", color=SLATE)
    code_box(s, 1.05, 2.70, 3.45, 2.90, "Mounted at",
             "/var/run/secrets/\nkubernetes.io/serviceaccount\n \nca.crt\nnamespace\ntoken", STEPS[3], size=13)
    arrow(s, LEFT, 4.80, 3.78, 0.50, 0.45)
    zone_code(s, 5.40, 2.15, 3.45, 3.70, "Projected volume", color=BLUE)
    rich(s, 5.55, 2.45, 3.20, 0.35, "`kube-api-access-<id>`", size=12, color=E.BODY)
    for k, (key, src, ext) in enumerate((("token", "The TokenRequest API", True),
                                         ("ca.crt", ["The ConfigMap", "`kube-root-ca.crt`"], True),
                                         ("namespace", "The file `namespace` holds the namespace of the Pod", False))):
        y = 2.95 + k * 0.95
        code_box(s, 5.65, y, 2.95, 0.75, key, "", SLATE, size=14, mono_head=True)
        if ext:
            arrow(s, LEFT, 9.15, y + 0.17, 0.55, 0.40)
        rich(s, 9.80, y, 2.90, 0.75, src, size=14, color=E.BODY, anchor=E.MIDDLE)
    return s


def s_summary(prs):
    s = new_slide(prs, "Summary: Data for a Container")
    zone(s, 0.70, 1.65, 7.10, 4.55, "Pods of the lab", color=STEPS[1], fill=E.CARD_BG)
    rows = (("Environment of the container", "", "`configMapKeyRef`, `configMapRef`", ("ConfigMap", "app-config"),
             STEPS[1]),
            ("Files of a ConfigMap", "/etc/app-config", "a ConfigMap volume", ("ConfigMap", "app-config"), STEPS[3]),
            ("Environment, from a Secret", "", "`secretKeyRef`, `secretRef`", ("Secret", "app-secret"), SLATE),
            ("Files in tmpfs", "/etc/secret-volume", "a Secret volume", ("Secret", "app-secret"), SLATE))
    for k, (what, path, how, (kind, name), col) in enumerate(rows):
        y = 2.10 + k * 1.00
        code_box(s, 0.95, y, 3.20, 0.82, what, path, col, size=13)
        rich(s, 4.30, y, 3.40, 0.82, how, size=13, color=E.BODY, anchor=E.MIDDLE)
        arrow(s, LEFT, 8.00, y + 0.21, 0.70, 0.40)
        code_box(s, 8.85, y, 3.85, 0.82, kind, name, SLATE if kind == "Secret" else STEPS[3], size=13)
    caption(s, 6.25, "A container also gets command-line arguments (`command` and `args`) and fixed values "
                     "(`env` with `value`)")
    return s


def s_optional(prs):
    return text_slide(prs, "Optional Topics", [
        (0, "`immutable: true` (stable in v1.21): Kubernetes rejects each change to the data of the ConfigMap or "
            "the Secret, and the kubelet does not watch it"),
        (0, "Your own projected volume can put a ConfigMap, a Secret and a ServiceAccount token in one directory"),
        (0, "Encryption at rest: an EncryptionConfiguration file for the API server, for example with a KMS "
            "provider (KMS v2 is stable in v1.29)"),
        (0, "The External Secrets Operator copies values from a store such as AWS Secrets Manager into Secrets"),
        (0, "These topics are not in the lab or in the quiz")], size=17, after=11)


def s_takeaways(prs):
    return text_slide(prs, "Key Takeaways", [
        (0, "Do not put the configuration data in the image. Inject it into the container when it starts"),
        (0, "`args` replaces the `CMD` of an image, and `command` replaces its `ENTRYPOINT`"),
        (0, "A ConfigMap gives values as environment variables or as files. Only the files change at run time"),
        (0, "The same manifest gets other values from the ConfigMap of each namespace"),
        (0, "The data of a Secret is base64, not encryption, and etcd stores it as plain bytes. Protect it with "
            "encryption at rest, RBAC or an external store"),
        (0, "Each Pod gets a ServiceAccount token as files. The kubelet renews it, and no Secret holds it")],
        size=17, after=11)


def s_lab(prs):
    s = new_slide(prs, "Lab Week 12 at a Glance")
    end = grid(s, 0.60, TOP + 0.10, [2.00, 7.10, 3.00], [
        ["Lab step", "What you do", "Lecture slides"],
        ["Step 1", "Replace the `CMD` of an image with `args`.", "5, 6, 7"],
        ["Step 2", "Create the ConfigMap `app-config`. Inject it as environment variables.", "8, 10, 11, 12"],
        ["Step 3", "Use the ConfigMap as a volume. Change it.", "13"],
        ["Step 4", "Create the Secret `app-secret`. Inject it. Find the ServiceAccount token.",
         "16, 18, 19, 22, 23"],
        ["Step 5", "Use a second namespace. Read a Secret from etcd.", "11, 14, 17, 20"],
        ["Step 6", "Destroy the cluster.", "–"]], row_h=0.44, size=13.5)
    rich(s, 0.60, end + 0.18, 12.10, 1.00, [
        "Not in the lab: nginx, `docker run`, `stringData`, a value that you encode with base64, and the limit of 1 MiB.",
        "Also not in the lab: `optional: true`, `subPath`, `automountServiceAccountToken: false`, and the risks of "
        "a Secret in an environment variable.",
        "Also not in the lab: the permissions of the ServiceAccount `default`, RBAC, the Secret types "
        "`kubernetes.io/tls` and `kubernetes.io/dockerconfigjson`, and the optional topics.",
        "Also not in the lab: `command` with no `args`, the renewal of the token, and the risk to Secrets from "
        "the permission to create Pods.",
        "Also not in the lab: the environment variables of the other Services, and the projected volume "
        "`kube-api-access-<id>` with its sources."],
        size=13, color=E.MUTED, after=2)
    return s


def s_references(prs):
    return text_slide(prs, "References", [
        (0, "kubernetes.io/docs/concepts/configuration/configmap/"),
        (0, "kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/"),
        (0, "kubernetes.io/docs/concepts/configuration/secret/"),
        (0, "kubernetes.io/docs/tasks/inject-data-application/distribute-credentials-secure/"),
        (0, "kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/"),
        (0, "kubernetes.io/docs/tasks/administer-cluster/encrypt-data/"),
        (0, "kubernetes.io/docs/concepts/security/service-accounts/"),
        (0, "kubernetes.io/docs/concepts/security/security-checklist/")], size=16, after=10)


SLIDES = [s_part1, s_config, s_docker, s_args, s_env,
          s_part2, s_cm, s_cm_create, s_cm_env, s_cm_vol, s_envs,
          s_part3, s_secrets, s_secret_decl, s_secret_inject, s_tmpfs, s_protect, s_env_note, s_sa, s_sa_vol,
          s_summary, s_optional, s_takeaways, s_lab, s_references]


def main():
    if os.path.exists(OUT) and "--force" not in sys.argv:
        sys.exit("%s exists. Bump VERSION; never overwrite a delivered deck." % OUT)
    prs = Presentation(SRC)
    keep_first(prs, 3)
    cover(prs, "ConfigMaps", "and Secrets", 12)
    agenda(prs, [
        (0, "Configuration data outside the container image"),
        (1, "Arguments with `command` and `args`"),
        (1, "Values with `env`"),
        (0, "ConfigMaps"),
        (1, "As environment variables and as a volume"),
        (1, "One manifest for many environments"),
        (0, "Secrets"),
        (1, "Create, inject, store and protect a Secret"),
        (1, "The ServiceAccount token of a Pod")])
    outline(prs, "Week 12: K8s – ConfigMaps & Secrets")
    built = [prs.slides[0], prs.slides[1], prs.slides[2]] + [make(prs) for make in SLIDES]
    number_and_save(prs, built, "CLO835 Week 12 Lecture: ConfigMaps and Secrets", OUT)


if __name__ == "__main__":
    main()
