# -*- coding: utf-8 -*-
"""CLO835 Week 12 lab v5 - ConfigMaps and Secrets, in ONE workshop.

v5 fixes the lab defects of report 2026-10-31-13: the lab has at most 40 commands, the
ConfigMap step now uses --from-literal and --from-file in one command, each Pod sets
command and args as the lecture does, each Explain line has its answer on a slide, the
etcd step reads the Secret of week12-dev, and the master applies a Flannel manifest with
the images of the maziar account. The Blackboard text of v5 is
Week12/Lab_week12_Blackboard_Submission_v5.md.

v4 fixed the lab defects of report 2026-10-31-11: the comment on tmpfs no longer says
"never on disk", the lab now practises envFrom with secretRef and a Secret from
--from-file, and tee writes each manifest and shows it, so that each "display its
contents" line of the Blackboard text has a command. The Blackboard text of v4 is a
hand-written file.

v3 fixed the lab defects of report 2026-10-31-09: the label is "Lab Week 12", no
busybox image, the sample version is v1.35.10, and the lab practises --from-file,
configMapKeyRef, a declarative ConfigMap and Secret, two environments, and the
ServiceAccount token.

v1 had 4 workshops and 15 steps. The limit is now the size of the Week 03 and
Week 04 labs: at most Step 0 to Step 6. v2 keeps the line of the lecture
(Week12/Lecture_week12_v6.pptx): args, environment variables, a ConfigMap as variables
and as a volume, a Secret as a variable and as a volume, and the Secret in etcd.
Every object lives in the namespace week12, so the clean-up is one command.

Outputs: Week12/Lab_week12_v5.pptx, Week12/localMachine_v5.sh,
~/Documents/c/r/CLO835_Fall_2026/Week12/
Run from the project root. It is guarded, so importing it writes nothing.
"""
import os
import sys

from pptx import Presentation

import build_week12_lab_v1 as v1
import lab_kubeadm as L
from build_week12_lecture_v6 import finish

OUT = "Week12/Lab_week12_v5.pptx"
F = L.FILE_MARK
N = "-n week12"
D = "-n week12-dev"
IMAGE = "maziar/alpine-curl"

CM_ENV_POD = """apiVersion: v1
kind: Pod
metadata:
  name: config-env
spec:
  containers:
  - name: app
    image: maziar/alpine-curl
    command: ["sleep"]
    args: ["3600"]
    env:
    - name: GREETING
      value: hello
    - name: COLOR
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: APP_COLOR
    envFrom:
    - configMapRef:
        name: app-config""".split("\n")

SECRET_POD = """apiVersion: v1
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
    envFrom:
    - secretRef:
        name: app-secret
    volumeMounts:
    - name: app-secret-volume
      mountPath: /etc/secret-volume
  volumes:
  - name: app-secret-volume
    secret:
      secretName: app-secret""".split("\n")

# A declarative ConfigMap and Secret for a second environment.
DEV = """apiVersion: v1
kind: Namespace
metadata:
  name: week12-dev
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: week12-dev
data:
  APP_COLOR: red
  APP_MODE: dev
---
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
  namespace: week12-dev
data:
  DB_Password: ZGV2LXBhc3M=""".split("\n")


def no_busybox(lines):
    """The image of the maziar account, and command and args as the lecture shows them."""
    out = []
    for line in lines:
        if line.strip() == 'command: ["sleep", "3600"]':
            out += ['    command: ["sleep"]', '    args: ["3600"]']
        else:
            out.append(line.replace("busybox:1.36", IMAGE))
    return out


def own_flannel(dst):
    """The master writes the Flannel manifest, so the cluster needs no outside account."""
    path = os.path.join(dst, "master-init.sh.tftpl")
    master = open(path, encoding="utf8").read()
    manifest = open("Week12/assets/kube-flannel-v0.28.10.yml", encoding="utf8").read()
    assert "${" not in manifest and "%{" not in manifest
    url = "until kubectl apply -f https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml; do\n"
    note = "# The API server drops connections for a moment right after init, and again\n"
    assert master.count(url) == 1 and master.count(note) == 1
    master = master.replace(url, "until kubectl apply -f /root/kube-flannel.yml; do\n")
    block = ("# Flannel v0.28.10 (Apache License 2.0). The images are copies on the maziar account.\n"
             "cat > /root/kube-flannel.yml <<'MANIFEST'\n%sMANIFEST\n\n" % manifest)
    open(path, "w", encoding="utf8").write(master.replace(note, block + note))


SLIDES = [
 ("title", "Workshop 1 – ConfigMaps and Secrets"),
 ("prereq",),
 ("cluster",),
 ("step2", "args replaces the CMD of the image", "bash", [
  "# A namespace for the objects of the lab.",
  "$ kubectl create namespace week12",
  " ",
  "# The image: ENTRYPOINT [\"/bin/fortuneloop.sh\"], CMD [\"10\"].",
  "# args replaces CMD, and command replaces",
  "# ENTRYPOINT. This Pod writes a fortune every 2 s.",
  "# tee writes the file and shows it.",
  "$ tee fortune-args.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f fortune-args.yaml " + N,
  "$ kubectl wait --for=condition=Ready pod/fortune-args " + N + " --timeout=120s",
  "$ sleep 6; kubectl logs fortune-args " + N + " | head -4",
  ], "fortune-args.yaml", "fortune-args.yaml", v1.ARGS_POD),
 ("step2", "Environment variables from a ConfigMap", "bash", [
  "# The ConfigMap keeps the values out of the manifest.",
  "# --from-file makes one key from a file. The file name is the key.",
  "$ printf 'debug' > LOG_LEVEL",
  "$ kubectl create configmap app-config " + N + " \\",
  "    --from-literal=APP_COLOR=blue --from-literal=APP_MODE=prod \\",
  "    --from-file=LOG_LEVEL",
  " ",
  "# env sets one value. configMapKeyRef reads one key.",
  "# envFrom injects every key.",
  "# Kubernetes injects KUBERNETES_SERVICE_HOST for the API server.",
  "$ tee config-env.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f config-env.yaml " + N,
  "$ kubectl wait --for=condition=Ready pod/config-env " + N + " --timeout=120s",
  "$ kubectl exec config-env " + N + " -- \\",
  "    printenv GREETING COLOR APP_COLOR APP_MODE LOG_LEVEL KUBERNETES_SERVICE_HOST",
  ], "config-env.yaml", "config-env.yaml", CM_ENV_POD),
 ("step2", "A ConfigMap as a volume", "bash", [
  "# Each key becomes a file in the volume.",
  "$ tee config-volume.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f config-volume.yaml " + N,
  "$ kubectl wait --for=condition=Ready pod/config-volume " + N + " --timeout=120s",
  "$ kubectl exec config-volume " + N + " -- ls /etc/app-config",
  "$ kubectl exec config-volume " + N + " -- cat /etc/app-config/APP_COLOR; echo",
  " ",
  "# Change the ConfigMap. The kubelet updates the file in about a minute.",
  "# An environment variable gets its value when the container starts.",
  "# It does not change while the container runs.",
  "$ kubectl patch configmap app-config " + N + " -p '{\"data\":{\"APP_COLOR\":\"green\"}}'",
  "$ sleep 120; kubectl exec config-volume " + N + " -- cat /etc/app-config/APP_COLOR; echo",
  "$ kubectl exec config-env " + N + " -- printenv APP_COLOR     # still blue",
  ], "config-volume.yaml", "config-volume.yaml", no_busybox(v1.CM_VOL_POD)),
 ("step2", "A Secret as an environment variable and as a volume", "bash", [
  "$ printf 'paswrd' > DB_Password",
  "$ kubectl create secret generic app-secret " + N + " \\",
  "    --from-literal=DB_Host=mysql --from-file=DB_Password",
  "# base64 is an encoding, not encryption. Anyone can decode it, with no key.",
  "$ kubectl get secret app-secret " + N + " -o jsonpath='{.data.DB_Password}' | base64 -d; echo",
  " ",
  "# secretKeyRef reads one key. secretRef injects every key.",
  "$ tee secret-pod.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f secret-pod.yaml " + N,
  "$ kubectl wait --for=condition=Ready pod/secret-pod " + N + " --timeout=120s",
  "$ kubectl exec secret-pod " + N + " -- printenv DB_Password DB_Host",
  "$ kubectl exec secret-pod " + N + " -- cat /etc/secret-volume/DB_Host; echo",
  "# On the node, the volume is in memory (tmpfs), not on the disk.",
  "$ kubectl exec secret-pod " + N + " -- mount | grep secret-volume",
  " ",
  "# The Pod also gets a ServiceAccount token as files. No Secret holds it.",
  "$ kubectl exec secret-pod " + N + " -- ls /var/run/secrets/kubernetes.io/serviceaccount",
  "$ kubectl get secrets " + N + "     # app-secret only",
  ], "secret-pod.yaml", "secret-pod.yaml", SECRET_POD),
 ("step2", "A second environment, and a Secret in etcd", "bash", [
  "# The same Pod manifest in a second namespace gets other values.",
  "$ tee config-dev.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f config-dev.yaml",
  "$ kubectl apply -f config-env.yaml " + D,
  "$ kubectl wait --for=condition=Ready pod/config-env " + D + " --timeout=120s",
  "$ kubectl exec config-env " + D + " -- printenv APP_COLOR APP_MODE   # red, dev",
  " ",
  "# By default etcd stores a Secret as plain bytes. Read it from etcd.",
  ] + v1.ETCD + [
  "$ kubectl -n kube-system exec etcd-masternode -- $ETCD \\",
  "    get /registry/secrets/week12-dev/app-secret | grep -a -o dev-pass",
  "# dev-pass: the password, in plain bytes, in the cluster database.",
  "# Protect it: encryption at rest, RBAC, or an external secret store.",
  ], "config-dev.yaml", "config-dev.yaml", DEV),
 ("step", "Clean up", "bash", [
  "# ON THE MASTER - delete the Kubernetes objects.",
  "# Each Pod, ConfigMap and Secret belongs to one namespace. Kubernetes deletes them with it.",
  "# This step takes about 40 seconds.",
  "$ bash cleanup_lab12.sh",
  " ",
  "# ON YOUR OWN MACHINE - remove the three EC2 instances.",
  "L$ terraform destroy",
  " ",
  "# Always destroy. The Learner Lab budget is small.",
  ]),
 ("end", "Workshop 1 – The End"),
]

SCRIPT_HEAD = """#!/bin/bash
# CLO835 - Week 12 - ConfigMaps and Secrets.
# Run these ON THE MASTER NODE, section by section. Do NOT run the whole file.
#
# Terraform builds 3 machines: 1 control plane and 2 workers. The cluster forms
# itself at boot, the same way it did in Weeks 04 to 10. The objects of the lab
# are in the namespaces week12 and week12-dev.
#
# Each step matches one slide of Lab_week12_v5.pptx.
"""

CLEANUP = """kubectl delete namespace week12 week12-dev 2>/dev/null
rm -f ./fortune-args.yaml ./config-env.yaml ./config-volume.yaml ./secret-pod.yaml
rm -f ./config-dev.yaml ./LOG_LEVEL ./DB_Password

kubectl get namespaces | grep week12"""

if __name__ == "__main__":
    L.check_lines(SLIDES)
    L.make_lab("12", SLIDES, OUT, SCRIPT_HEAD, script_path="Week12/localMachine_v5.sh",
               prereq_title="Lab Week 12 - Prerequisites", node_version="v1.35.10")
    prs = Presentation(OUT)
    # One name for the computer of the student, as on the Clean up slide.
    runs = [r for sh in prs.slides[2].shapes if sh.has_text_frame for p in sh.text_frame.paragraphs for r in p.runs
            if r.text.startswith("# ON YOUR MACHINE")]
    assert len(runs) == 1, len(runs)
    runs[0].text = runs[0].text.replace("ON YOUR MACHINE", "ON YOUR OWN MACHINE")
    finish(prs, "CLO835 Week 12 Lab: ConfigMaps and Secrets")
    prs.save(OUT)
    if "--no-repo" not in sys.argv:
        dst, files = L.make_repo_folder("12", "ConfigMaps and Secrets", CLEANUP, "Week12/localMachine_v5.sh",
                                        lab_label="Lab Week 12")
        own_flannel(dst)
        print("repo folder : %s (%d files)" % (dst, len(files)))
