# -*- coding: utf-8 -*-
"""CLO835 Week 12 lab v2 - ConfigMaps and Secrets, in ONE workshop.

v1 had 4 workshops and 15 steps. The limit is now the size of the Week 03 and
Week 04 labs: at most Step 0 to Step 6. v2 keeps the line of the lecture
(Week12/Week12_v3.pptx): args, environment variables, a ConfigMap as variables
and as a volume, a Secret as a variable and as a volume, and the Secret in etcd.
Every object lives in the namespace week12, so the clean-up is one command.

Outputs: Week12/Lab_week12_v2.pptx, Week12/localMachine_v2.sh,
Week12/Lab_week12_Blackboard_Submission_v2.md, ~/Documents/c/r/CLO835_Fall_2026/Week12/
Run from the project root. It is guarded, so importing it writes nothing.
"""
import sys

import build_week12_lab_v1 as v1
import lab_kubeadm as L

F = L.FILE_MARK
N = "-n week12"

CM_ENV_POD = """apiVersion: v1
kind: Pod
metadata:
  name: config-env
spec:
  containers:
  - name: app
    image: busybox:1.36
    command: ["sleep", "3600"]
    env:
    - name: GREETING
      value: hello
    envFrom:
    - configMapRef:
        name: app-config""".split("\n")

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
  "$ kubectl get configmap app-config " + N + " -o yaml",
  " ",
  "# env sets one value. envFrom injects every key.",
  "$ cat > config-env.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f config-env.yaml " + N,
  "$ kubectl wait --for=condition=Ready pod/config-env " + N + " --timeout=120s",
  "$ kubectl exec config-env " + N + " -- printenv GREETING APP_COLOR APP_MODE",
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
  ], "config-volume.yaml", "config-volume.yaml", v1.CM_VOL_POD),
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
  ], "secret-pod.yaml", "secret-pod.yaml", v1.SECRET_POD),
 ("step", "A Secret in etcd is not encrypted", "bash", [
  "# By default etcd stores a Secret as plain bytes. Read it from etcd directly.",
  ] + v1.ETCD + [
  "$ kubectl -n kube-system exec etcd-masternode -- $ETCD get /registry/secrets/week12/app-secret | grep -a -o paswrd",
  "# paswrd: the password, in plain text, in the cluster database.",
  " ",
  "# Protect it: turn on encryption at rest, limit who can read Secrets with RBAC,",
  "# or keep the value in an external secret store.",
  ]),
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
# itself at boot, the same way it did in Weeks 04 to 10. Every object of the lab
# lives in the namespace week12.
#
# Each step matches one slide of Lab_week12_v2.pptx.
"""

CLEANUP = """kubectl delete namespace week12 2>/dev/null
rm -f ./fortune-args.yaml ./config-env.yaml ./config-volume.yaml ./secret-pod.yaml

kubectl get namespaces | grep week12"""

BLACKBOARD = [
 ("Arguments and ConfigMaps", "args replace the CMD of the image. A ConfigMap keeps the configuration out of the manifest.",
  ["Show the fortune-args log with the 2-second interval.",
   "Show the app-config ConfigMap and the three variables in config-env.",
   "Show the files of the ConfigMap volume, and APP_COLOR before and after the patch.",
   "Explain why the variable in config-env is still blue."]),
 ("Secrets", "A Secret is base64, not encrypted.",
  ["Show the decoded DB_Password.",
   "Show DB_Password as a variable and DB_Host as a file, and the tmpfs mount.",
   "Show the password in plain text in etcd, and name two ways to protect it.",
   "Show the clean-up and terraform destroy."]),
]

if __name__ == "__main__":
    L.check_lines(SLIDES)
    L.make_lab("12", SLIDES, "Week12/Lab_week12_v2.pptx", SCRIPT_HEAD, script_path="Week12/localMachine_v2.sh")
    if "--no-repo" not in sys.argv:
        dst, files = L.make_repo_folder("12", "ConfigMaps and Secrets", CLEANUP, "Week12/localMachine_v2.sh")
        print("repo folder : %s (%d files)" % (dst, len(files)))
    L.blackboard_text("12", "The Terraform configuration in Week 12 creates the same three Ubuntu 26.04 EC2 "
                      "machines as Weeks 04 to 10.", BLACKBOARD, "Week12/Lab_week12_Blackboard_Submission_v2.md")
    print("blackboard  : Week12/Lab_week12_Blackboard_Submission_v2.md")
