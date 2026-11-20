# -*- coding: utf-8 -*-
"""CLO835 Week 12 lecture v8 - ConfigMaps and Secrets.

v8 applies the audit of 2026-11-18 (loop report 2026-11-18-06) to lecture v7. v7 stays on disk.
- L1 (syllabus, Part 2 Section 7): a new slide 19 is "Image Pull Secrets". It shows the Secret type
  kubernetes.io/dockerconfigjson and kubectl create secret docker-registry. It shows imagePullSecrets in a
  Pod and in a ServiceAccount. It is "Concept only", because the lab pulls only public images.
- L2: slide 8 states the $(NAME) reference in a value, in command and in args. Slide 12 shows MESSAGE.
- L3: slide 13 states defaultMode (the lab sets 0440) and items ("Concept only").
- L4: slide 12 states that env has priority over envFrom. The lab shows it with GREETING=hi.
- L5: slide 28 ("Lab Week 12 at a Glance") lists the topics that the lab does not run in one list.
  Each line of the list names its part, and the list has no repeated "Also not in the lab".
- L6: each terminal labeled "Lab Week 12, Step N" and each manifest of the lab come from build_week12_lab_v8
  (C8). Slide 7 is the exception. Its kubectl wait lines are in the v7 function s_args, and its
  fortune-args.yaml comes from build_week12_lab_v1. Both agree with Step 1 of lab v8.
- The slides after slide 18 move by one, so slide 28 names the new numbers.
Review round 1 (2026-11-18, scratchpad w12review_r1/lecture.md):
- M1 (C4): slide 20 shows the tmpfs size of the live passes of 2026-11-18 (size=7814528k).
- M2 (B7): the last takeaway says "By default" and names the projected volume (automount can be false).
- S1, S2 (B7): "Concept only" labels name each concept that the lab does not run.
  The labels are on slides 7, 8, 12, 13, 17, 21, 23 and 24.
- S3 (B7, no point three times): takeaway 3 states only the change at run time.
- S4 (B7): slide 8 drops "A ConfigMap prevents this". Slide 14 and takeaway 4 state it.
- S5 (B3): "The ServiceAccount `default`" with the name in Consolas.
Review round 2 (scratchpad w12review_r2/lecture.md):
- M1 (B7): takeaway 3 drops "Only", because Secret volume files and the token file also change.
- S1, S2, S4 (B7): slides 10 and 16 get a label. The slide 23 label also names the renewal of the token
  and the permissions of `default`. The slide 19 label says what the lab does not do.
- S3 (C8): slide 28 names the risks of slide 22 (a log file, a child process), not the Secret in env.
The sample outputs of Step 2 are the values of the v8 manifest. Live passes 1 and 2 show the same values
(C4). Slides 10 and 14 show the key GREETING of lab v8, and the agenda names the pull Secret of slide 19.
The cover and the outline are those of v7. The builder imports all other slides from v7 and does not
copy them.
Review round 3 (scratchpad w12review_r3/lecture.md): the labels of slides 10 and 16 name the size limit
of a ConfigMap and of a Secret. The slide 16 label names only the type kubernetes.io/tls, and bullet 5 points
to slide 19 for the type kubernetes.io/dockerconfigjson. The slide 21 label also names the risk of the permission to
create Pods. Slide 28 names each topic one time.

Input : Week12/Lecture_week12_v6.pptx, for the cover, the agenda and the outline (the builder reads it and
never writes it)
Output: Week12/Lecture_week12_v8.pptx (the build does not overwrite it, unless you give --force)

Run from the project root. The code that writes the deck runs only under __main__, so an import writes
nothing.
    .venv/bin/python build_week12_lecture_v8.py
"""
import os
import sys

from pptx import Presentation

import build_week08 as E
import build_week12_lab_v8 as lab8
import build_week12_lecture_v7 as V
from build_week07_lecture_v7 import (LEFT, STEPS, TOP, UP, agenda, arrow, bullets, cover, grid, keep_first,
                                     new_slide, number_and_save, outline, rich, term)

VERSION = "v8"
SRC = "Week12/Lecture_week12_v6.pptx"
OUT = "Week12/Lecture_week12_%s.pptx" % VERSION

# The v7 slide functions read these module globals at call time. Point them at lab v8 (C8).
V.lab = lab8
V.LAB = {n: lab8.SLIDES[2 + n][3] for n in range(1, 6)}
V.CM_ENV_POD = lab8.CM_ENV_POD
V.CM_VOL_POD = lab8.CM_VOL_POD
V.SECRET_POD = lab8.SECRET_POD
V.DEV = lab8.DEV
V.DEV_CM = lab8.DEV[lab8.DEV.index("kind: ConfigMap") - 1:lab8.DEV.index("  APP_MODE: dev") + 1]
V.DEV_SECRET = lab8.DEV[lab8.DEV.index("kind: Secret") - 1:]
run, code_box, zone_code, concept = V.run, V.code_box, V.zone_code, V.concept


def s_env(prs):
    s = new_slide(prs, "Environment Variables in the Pod Manifest")
    bullets(s, 0.60, 1.65, 12.10, [
        (0, "You set environment variables for each container, not for the Pod"),
        (0, "`env` sets a name and a value. The value is fixed in the manifest"),
        (0, "`$(NAME)` in a `value`, in `command` or in `args` gives the value of an environment variable. In "
            "`env`, the environment variable must come earlier in the list"),
        (0, "The kubelet also injects environment variables for the Services of the namespace that exist when "
            "the container starts, and `KUBERNETES_SERVICE_HOST` for the API server"),
        (0, "A fixed value needs one manifest for each environment, for example development and production")],
        size=17, after=11, h=4.20)
    concept(s, 0.60, 5.60, 12.10, "Concept only: the lab does not show the environment variables of the other "
                                  "Services.")
    return s


def s_cm(prs):
    s = new_slide(prs, "The ConfigMap Object")
    bullets(s, 0.60, 1.70, 5.60, [
        (0, "A ConfigMap is a Kubernetes object in a namespace"),
        (0, "It holds key/value pairs, up to 1 MiB"),
        (0, "A container gets the values as environment variables, or as files in a volume"),
        (0, "The Pod and the ConfigMap must be in the same namespace")], size=16, after=10, h=4.40)
    V.zone(s, 6.50, 1.70, 3.70, 4.50, "Pod", color=STEPS[1], fill=E.CARD_BG)
    V.zone(s, 6.75, 2.15, 3.20, 1.75, "Container", color=V.SLATE)
    V.box(s, 7.00, 2.60, 2.70, 1.05, "Environment variables", STEPS[1], size=15)
    V.box(s, 6.75, 4.30, 3.20, 1.55, "ConfigMap volume", STEPS[3], size=15)
    code_box(s, 10.95, 2.25, 1.75, 3.50, "ConfigMap", "app-config\n \nAPP_COLOR\nAPP_MODE\nGREETING\nLOG_LEVEL",
             V.SLATE, size=13)
    arrow(s, LEFT, 10.25, 2.92, 0.60, 0.42)
    arrow(s, LEFT, 10.25, 4.86, 0.60, 0.42)
    concept(s, 0.60, 4.40, 5.60, "Concept only: the lab does not test the size limit of a ConfigMap.")
    return s


def s_cm_env(prs):
    s = new_slide(prs, "ConfigMaps: Inject as Environment Variables")
    bullets(s, 0.60, 1.62, 6.60, [
        (0, "`valueFrom` with `configMapKeyRef` reads one key into a new name"),
        (0, "`envFrom` with `configMapRef` injects every key. The key is the name"),
        (0, "When `env` and `envFrom` set the same name, the value of `env` has priority. So `GREETING` shows "
            "`hello`, not `hi`"),
        (0, "If the ConfigMap or the key does not exist, the container does not start, unless the reference sets "
            "`optional: true`")], size=13, after=4, h=2.70)
    concept(s, 0.60, 3.80, 6.60, "Concept only: the lab does not run `optional: true`.")
    term(s, 0.60, 4.40, 6.60, "Lab Week 12, Step 2",
         run(2, ("$ kubectl exec", ["hello", "blue", "hello blue", "blue", "prod", "debug", "10.96.0.1"])),
         size=10, spacing=1.0)
    term(s, 7.45, 1.62, 5.25, "config-env.yaml (Lab Week 12, Step 2)", V.CM_ENV_POD, size=10.5, spacing=1.0)
    return s


def s_cm_vol(prs):
    s = new_slide(prs, "A ConfigMap as a Volume")
    bullets(s, 0.60, 1.62, 6.60, [
        (0, "Each key becomes a file in the volume. The file name is the key"),
        (0, "`defaultMode` sets the permissions of the files, for example `0440`"),
        (0, "`items` selects some keys only, and sets the file name of each key"),
        (0, "When the ConfigMap changes, the kubelet updates the files within about two minutes"),
        (0, "An environment variable gets its value when the container starts. It does not change"),
        (0, "A mount with `subPath` gets no update")], size=13, after=4, h=2.95)
    term(s, 0.60, 3.90, 6.60, "Lab Week 12, Step 3",
         run(3, ("$ kubectl patch", ["configmap/app-config patched"]), ("$ until", ["green"]),
             ("$ kubectl exec config-env", ["blue"])), size=10, spacing=1.0)
    y = term(s, 7.45, 1.62, 5.25, "config-volume.yaml (Lab Week 12, Step 3)", V.CM_VOL_POD, size=10.5,
             spacing=1.0)
    concept(s, 7.45, y + 0.15, 5.25, "Concept only: the lab does not run `items` or `subPath`.")
    return s


def s_envs(prs):
    s = new_slide(prs, "Multiple Environments with ConfigMaps")
    bullets(s, 0.60, 1.70, 5.30, [
        (0, "The Pods of each namespace come from the same manifest, and it names the ConfigMap `app-config`"),
        (0, "Each namespace has its own `app-config`, with the values of that environment")],
        size=15, after=8, h=2.60)
    for x, ns, vals in ((6.20, "Namespace: `week12`", "APP_COLOR=blue\nAPP_MODE=prod\nGREETING=hi\nLOG_LEVEL=debug"),
                        (9.50, "Namespace: `week12-dev`", "APP_COLOR=red\nAPP_MODE=dev")):
        zone_code(s, x, 1.62, 3.10, 2.73, ns, color=V.BLUE)
        code_box(s, x + 0.25, 1.98, 2.60, 0.60, "Pod", "config-env", STEPS[1], size=13)
        arrow(s, UP, x + 1.36, 2.62, 0.38, 0.28)
        code_box(s, x + 0.25, 2.94, 2.60, 1.34, "ConfigMap, at creation", "app-config\n" + vals, STEPS[3],
                 size=12)
    term(s, 0.60, 4.45, 12.10, "Lab Week 12, Step 5",
         run(5, ("$ kubectl apply -f config-dev.yaml", ["namespace/week12-dev created",
                                                        "configmap/app-config created", "secret/app-secret created"]),
             ("$ kubectl apply -f config-env.yaml", ["pod/config-env created"]),
             ("$ kubectl wait", ["pod/config-env condition met"]),
             ("$ kubectl exec config-env", ["red", "dev"])), size=9, spacing=1.0)
    return s


def labeled(make, x, y, w, text):
    """A slide of v7 with a "Concept only" label (review round 1, S2: slides 7, 21 and 24)."""
    def build(prs):
        s = make(prs)
        concept(s, x, y, w, text)
        return s
    build.__name__ = make.__name__
    return build


def s_secrets(prs):
    s = new_slide(prs, "The Secret Object")
    bullets(s, 0.60, 1.62, 12.10, [
        (0, "A Secret holds key/value pairs, and the API shows each value in base64"),
        (0, "base64 is an encoding, not encryption. Anyone can decode it, with no key"),
        (0, "etcd stores the Secret on the disk of the master node. The size limit is 1 MiB"),
        (0, "The container gets the decoded value, so the application does not decode it"),
        (0, "Three common types: `Opaque` (from `kubectl create secret generic`), `kubernetes.io/tls` and "
            "`kubernetes.io/dockerconfigjson` (slide 19)")], size=15, after=5, h=2.75)
    concept(s, 0.60, 3.95, 12.10, "Concept only: the lab does not create a Secret of the type `kubernetes.io/tls`, "
                                  "or test the size limit of a Secret.")
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
    concept(s, 0.60, y + 0.12, 6.40, "Concept only: the lab does not run `stringData` or encode a value with base64.")
    term(s, 7.25, 1.62, 5.45, "config-dev.yaml, the Secret (Lab Week 12, Step 5)", V.DEV_SECRET, size=11,
         spacing=1.05)
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
         run(4, ("$ kubectl exec secret-pod " + lab8.N + " -- mount",
                 ["tmpfs on /etc/secret-volume type tmpfs (ro,relatime,size=7814528k,inode64,noswap)"])), size=12,
         spacing=1.05)
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
        (0, "The ServiceAccount `default` has API discovery permissions only")], size=14, after=2, h=2.85)
    concept(s, 0.60, 4.20, 12.10, "Concept only: the lab does not run `automountServiceAccountToken: false`, or "
                                  "show the renewal of the token or the permissions of `default`.")
    term(s, 0.60, 4.66, 12.10, "Lab Week 12, Step 4",
         run(4, ("$ kubectl exec secret-pod " + lab8.N + " -- ls", ["ca.crt", "namespace", "token"]),
             ("$ kubectl get secrets", ["NAME         TYPE     DATA   AGE", "app-secret   Opaque   2      28s"])),
         size=11, spacing=1.0)
    return s


def s_takeaways(prs):
    return V.text_slide(prs, "Key Takeaways", [
        (0, "Do not put the configuration data in the image. Inject it into the container when it starts"),
        (0, "`args` replaces the `CMD` of an image, and `command` replaces its `ENTRYPOINT`"),
        (0, "The files of a ConfigMap volume change at run time. An environment variable does not change"),
        (0, "The same manifest gets other values from the ConfigMap of each namespace"),
        (0, "The data of a Secret is base64, not encryption, and etcd stores it as plain bytes. Protect it with "
            "encryption at rest, RBAC or an external store"),
        (0, "By default, each Pod gets a ServiceAccount token in a projected volume. The kubelet renews it, and "
            "no Secret holds it")],
        size=17, after=11)


PULL_CMD = [
    "$ kubectl create secret docker-registry regcred \\",
    "    -n week12 --docker-username=<your-account> \\",
    "    --docker-password=\"$HUB_TOKEN\"",
    "# --docker-server has the default https://index.docker.io/v1/",
]
PULL_POD = """apiVersion: v1
kind: Pod
metadata:
  name: private-app
spec:
  containers:
  - name: app
    image: <your-account>/<private-image>:<tag>
  imagePullSecrets:
  - name: regcred""".split("\n")


def s_pull(prs):
    s = new_slide(prs, "Image Pull Secrets")
    bullets(s, 0.60, 1.62, 6.00, [
        (0, "A private registry asks for a user name and a password before it sends an image"),
        (0, "A Secret of the type `kubernetes.io/dockerconfigjson` holds them. `kubectl create secret "
            "docker-registry` creates it"),
        (0, "The Pod names the Secret in `imagePullSecrets`. The kubelet uses it to pull the image"),
        (0, "The Secret must be in the namespace of the Pod"),
        (0, "A ServiceAccount can also list `imagePullSecrets`. Then each new Pod of that ServiceAccount gets them")],
        size=14, after=6, h=3.90)
    y = term(s, 6.85, 1.62, 5.85, "Create a pull Secret (example only)", PULL_CMD, size=11, spacing=1.05)
    term(s, 6.85, y + 0.20, 5.85, "private-app.yaml (example only)", PULL_POD, size=11, spacing=1.05)
    concept(s, 0.60, 5.70, 6.00, "Concept only: the lab does not create a pull Secret, because it pulls only public "
                                 "images.")
    return s


def s_lab(prs):
    s = new_slide(prs, "Lab Week 12 at a Glance")
    end = grid(s, 0.60, TOP + 0.10, [2.00, 7.10, 3.00], [
        ["Lab step", "What you do", "Lecture slides"],
        ["Step 1", "Replace the `CMD` of an image with `args`.", "5, 6, 7"],
        ["Step 2", "Create the ConfigMap `app-config`. Inject it as environment variables.", "8, 10, 11, 12"],
        ["Step 3", "Use the ConfigMap as a volume. Change it.", "13"],
        ["Step 4", "Create the Secret `app-secret`. Inject it. Find the ServiceAccount token.",
         "16, 18, 20, 23, 24"],
        ["Step 5", "Use a second namespace. Read a Secret from etcd.", "11, 14, 17, 21"],
        ["Step 6", "Destroy the cluster.", "–"]], row_h=0.44, size=13.5)
    rich(s, 0.60, end + 0.15, 12.10, 1.10, [
        "Not in the lab, Part 1: nginx, `docker run`, `command` with no `args`, and the environment variables of "
        "the other Services.",
        "Part 2: `optional: true`, `items`, `subPath`, and the size limit of a ConfigMap.",
        "Part 3: the size limit of a Secret, the type `kubernetes.io/tls`, `stringData`, a value that you encode "
        "with base64, image pull Secrets, and RBAC.",
        "Part 3, the token: `automountServiceAccountToken: false`, the permissions of `default`, its renewal, and "
        "`kube-api-access-<id>`.",
        "Part 3, the risks: a Secret in a log file or in a child process, and the permission to create Pods. "
        "Slide 26: the optional topics."],
        size=12.5, color=E.MUTED, after=1)
    return s


SLIDES = [V.s_part1, V.s_config, V.s_docker,
          labeled(V.s_args, 0.60, 5.80, 5.80, "Concept only: the lab does not run `command` with no `args`."),
          s_env,
          V.s_part2, s_cm, V.s_cm_create, s_cm_env, s_cm_vol, s_envs,
          V.s_part3, s_secrets, s_secret_decl, V.s_secret_inject, s_pull, s_tmpfs,
          labeled(V.s_protect, 0.60, 5.20, 12.10, "Concept only: the lab does not configure encryption at rest or "
                  "RBAC, or show the risk of the permission to create Pods."),
          V.s_env_note, s_sa,
          labeled(V.s_sa_vol, 0.60, 6.20, 8.45, "Concept only: the lab does not show the sources of `kube-api-access-<id>`."),
          V.s_summary, V.s_optional, s_takeaways, s_lab, V.s_references]


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
        (1, "A Secret for the pull of a private image"),
        (1, "The ServiceAccount token of a Pod")])
    outline(prs, "Week 12: K8s – ConfigMaps & Secrets")
    built = [prs.slides[0], prs.slides[1], prs.slides[2]] + [make(prs) for make in SLIDES]
    assert len(built) == 29, len(built)
    number_and_save(prs, built, "CLO835 Week 12 Lecture: ConfigMaps and Secrets", OUT)


if __name__ == "__main__":
    main()
