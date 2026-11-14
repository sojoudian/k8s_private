# -*- coding: utf-8 -*-
"""CLO835 Week 12 lab v3 - ConfigMaps and Secrets, in ONE workshop.

v3 fixes the lab defects of report 2026-10-31-09: the label is "Lab Week 12", no
busybox image, the sample version is v1.35.10, and the lab now practises --from-file,
configMapKeyRef, a declarative ConfigMap and Secret, two environments, and the
ServiceAccount token. The Blackboard text of v3 is a hand-written file, in the long
form of the Lab04 item: Week12/Lab_week12_Blackboard_Submission_v3.md.

v1 had 4 workshops and 15 steps. The limit is now the size of the Week 03 and
Week 04 labs: at most Step 0 to Step 6. v2 keeps the line of the lecture
(Week12/Lecture_week12_v4.pptx): args, environment variables, a ConfigMap as variables
and as a volume, a Secret as a variable and as a volume, and the Secret in etcd.
Every object lives in the namespace week12, so the clean-up is one command.

Outputs: Week12/Lab_week12_v3.pptx, Week12/localMachine_v3.sh,
~/Documents/c/r/CLO835_Fall_2026/Week12/
Run from the project root. It is guarded, so importing it writes nothing.
"""
import sys

import build_week12_lab_v1 as v1
import lab_kubeadm as L

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
    command: ["sleep", "3600"]
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
    return [line.replace("busybox:1.36", IMAGE) for line in lines]


SLIDES = [
 ("title", "Workshop 1 – ConfigMaps and Secrets"),
 ("prereq",),
 ("cluster",),
 ("step2", "args replace the CMD of the image", "bash", [
  "# One namespace for the whole lab.",
  "$ kubectl create namespace week12",
  " ",
  "# The image: ENTRYPOINT [\"/bin/fortuneloop.sh\"], CMD [\"10\"].",
  "# args replaces CMD, and command would replace",
  "# ENTRYPOINT. This Pod writes a fortune every 2 s.",
  "$ cat > fortune-args.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f fortune-args.yaml " + N,
  "$ kubectl wait --for=condition=Ready pod/fortune-args " + N + " --timeout=120s",
  "$ sleep 6; kubectl logs fortune-args " + N + " --tail=4",
  ], "fortune-args.yaml", "fortune-args.yaml", v1.ARGS_POD),
 ("step2", "Environment variables from a ConfigMap", "bash", [
  "# The ConfigMap keeps the values out of the manifest.",
  "$ kubectl create configmap app-config " + N + " \\",
  "    --from-literal=APP_COLOR=blue --from-literal=APP_MODE=prod",
  " ",
  "# --from-file makes one key from a file.",
  "$ printf 'LOG_LEVEL=debug\\n' > app.properties",
  "$ kubectl create configmap app-file " + N + " --from-file=app.properties -o yaml",
  " ",
  "# env sets one value. configMapKeyRef reads one key.",
  "# envFrom injects every key.",
  "$ cat > config-env.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f config-env.yaml " + N,
  "$ kubectl wait --for=condition=Ready pod/config-env " + N + " --timeout=120s",
  "$ kubectl exec config-env " + N + " -- printenv GREETING COLOR APP_COLOR APP_MODE",
  ], "config-env.yaml", "config-env.yaml", CM_ENV_POD),
 ("step2", "A ConfigMap as a volume", "bash", [
  "# Each key becomes a file in the mounted folder.",
  "$ cat > config-volume.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f config-volume.yaml " + N,
  "$ kubectl wait --for=condition=Ready pod/config-volume " + N + " --timeout=120s",
  "$ kubectl exec config-volume " + N + " -- ls /etc/app-config",
  "$ kubectl exec config-volume " + N + " -- cat /etc/app-config/APP_COLOR; echo",
  " ",
  "# Change the ConfigMap. The file follows in about a",
  "# minute. A variable never changes in a running Pod.",
  "$ kubectl patch configmap app-config " + N + " -p '{\"data\":{\"APP_COLOR\":\"green\"}}'",
  "$ sleep 90; kubectl exec config-volume " + N + " -- cat /etc/app-config/APP_COLOR; echo",
  "$ kubectl exec config-env " + N + " -- printenv APP_COLOR     # still blue",
  ], "config-volume.yaml", "config-volume.yaml", no_busybox(v1.CM_VOL_POD)),
 ("step2", "A Secret as a variable and as a volume", "bash", [
  "$ kubectl create secret generic app-secret " + N + " \\",
  "    --from-literal=DB_Host=mysql --from-literal=DB_Password=paswrd",
  "# base64 is an encoding, not encryption.",
  "$ kubectl get secret app-secret " + N + " -o jsonpath='{.data.DB_Password}' | base64 -d; echo",
  " ",
  "$ cat > secret-pod.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f secret-pod.yaml " + N,
  "$ kubectl wait --for=condition=Ready pod/secret-pod " + N + " --timeout=120s",
  "$ kubectl exec secret-pod " + N + " -- printenv DB_Password",
  "$ kubectl exec secret-pod " + N + " -- cat /etc/secret-volume/DB_Host; echo",
  "# The volume is in memory (tmpfs), never on disk.",
  "$ kubectl exec secret-pod " + N + " -- mount | grep secret-volume",
  " ",
  "# The Pod also gets a ServiceAccount token as files. No Secret holds it.",
  "$ kubectl exec secret-pod " + N + " -- ls /var/run/secrets/kubernetes.io/serviceaccount",
  "$ kubectl get secrets " + N + "     # app-secret only",
  ], "secret-pod.yaml", "secret-pod.yaml", no_busybox(v1.SECRET_POD)),
 ("step2", "A second environment, and a Secret in etcd", "bash", [
  "# The same Pod manifest in a second namespace gets other values.",
  "$ cat > config-dev.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f config-dev.yaml",
  "$ kubectl apply -f config-env.yaml " + D,
  "$ kubectl wait --for=condition=Ready pod/config-env " + D + " --timeout=120s",
  "$ kubectl exec config-env " + D + " -- printenv APP_COLOR APP_MODE   # red, dev",
  "$ kubectl get secret app-secret " + D + " \\",
  "    -o jsonpath='{.data.DB_Password}' | base64 -d; echo",
  " ",
  "# By default etcd stores a Secret as plain bytes. Read it from etcd.",
  ] + v1.ETCD + [
  "$ kubectl -n kube-system exec etcd-masternode -- $ETCD \\",
  "    get /registry/secrets/week12/app-secret | grep -a -o paswrd",
  "# paswrd: the password, in plain text, in the cluster database.",
  "# Protect it: encryption at rest, RBAC, or an external secret store.",
  ], "config-dev.yaml", "config-dev.yaml", DEV),
 ("step", "Clean up", "bash", [
  "# ON THE MASTER - remove the Kubernetes objects.",
  "$ bash cleanup_lab12.sh",
  " ",
  "# Confirm that nothing is left.",
  "$ kubectl get namespaces | grep week12",
  " ",
  "# ON YOUR OWN MACHINE - remove the three EC2 machines.",
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
# live in the namespaces week12 and week12-dev.
#
# Each step matches one slide of Lab_week12_v3.pptx.
"""

CLEANUP = """kubectl delete namespace week12 week12-dev 2>/dev/null
rm -f ./fortune-args.yaml ./config-env.yaml ./config-volume.yaml ./secret-pod.yaml
rm -f ./config-dev.yaml ./app.properties

kubectl get namespaces | grep week12"""

if __name__ == "__main__":
    L.check_lines(SLIDES)
    L.make_lab("12", SLIDES, "Week12/Lab_week12_v3.pptx", SCRIPT_HEAD, script_path="Week12/localMachine_v3.sh",
               prereq_title="Lab Week 12 - Prerequisites", node_version="v1.35.10")
    if "--no-repo" not in sys.argv:
        dst, files = L.make_repo_folder("12", "ConfigMaps and Secrets", CLEANUP, "Week12/localMachine_v3.sh",
                                        lab_label="Lab Week 12")
        print("repo folder : %s (%d files)" % (dst, len(files)))
