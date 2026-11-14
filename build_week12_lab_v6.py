# -*- coding: utf-8 -*-
"""CLO835 Week 12 lab v6 - ConfigMaps and Secrets, in ONE workshop.

v6 applies CLO835_STANDARDS.md (2026-11-10):
- The cluster slide works also in a clone made before the history rewrite of 2026-11-05:
  git fetch and git reset --hard origin/master replace git pull (C3, F1).
- A wait loop replaces "sleep 120" in Step 3 (C3: kubectl wait or a loop, not a long sleep).
- "Kubernetes" replaces "K8s" on the prerequisite slide; "stay" replaces "keeps", "creates"
  replaces "makes", and "master" replaces "control plane" in the script head (A1).
- The builder writes the Blackboard text (C2): Week12/Lab_week12_Blackboard_Submission_v6.md.
The cleanup script uses --ignore-not-found, so it waits for the deletion also when week12-dev does
not exist (the recovery test of 2026-11-10).
After the independent review of 2026-11-10:
- Each manifest is written with cat > file.yaml <<'EOF' (C3), as in Week 10; the pasted text shows
  the file, so each "display its contents" item of the Blackboard text has its screenshot.
- The cluster slide: "show", not "prints"; the sample output of kubectl get nodes is a comment (B5);
  a fact of the live cluster replaces the NodePort line (Week 12 has no Service).
- Step 3 says "within about one minute" one time; Step 4 has the title "A Secret, and the
  ServiceAccount token"; Step 6 says "destroy".
- The Blackboard text: args is a field of a container; "display its contents"; the item on
  configuration data in an image is in section 2; no "ETCD" and no "variable" alone.
- The repo files of Week 12 get the A1 words (repo_words()): master node, delete, destroy.

v5 notes follow.

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

Outputs: Week12/Lab_week12_v6.pptx, Week12/localMachine_v6.sh,
Week12/Lab_week12_Blackboard_Submission_v6.md, ~/Documents/c/r/CLO835_Fall_2026/Week12/
Run from the project root. It is guarded, so importing it writes nothing.
"""
import os
import sys

from pptx import Presentation

import build_week12_lab_v1 as v1
import lab_kubeadm as L
from build_week12_lecture_v6 import finish

VERSION = "v6"
OUT = "Week12/Lab_week12_%s.pptx" % VERSION
SCRIPT = "Week12/localMachine_%s.sh" % VERSION
BLACKBOARD = "Week12/Lab_week12_Blackboard_Submission_%s.md" % VERSION
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
  "$ cat > fortune-args.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f fortune-args.yaml " + N,
  "$ kubectl wait --for=condition=Ready pod/fortune-args " + N + " --timeout=120s",
  "$ sleep 6; kubectl logs fortune-args " + N + " | head -4",
  ], "fortune-args.yaml", "fortune-args.yaml", v1.ARGS_POD),
 ("step2", "Environment variables from a ConfigMap", "bash", [
  "# The values stay in the ConfigMap, not in the manifest.",
  "# --from-file creates one key from a file. The file name is the key.",
  "$ printf 'debug' > LOG_LEVEL",
  "$ kubectl create configmap app-config " + N + " \\",
  "    --from-literal=APP_COLOR=blue --from-literal=APP_MODE=prod \\",
  "    --from-file=LOG_LEVEL",
  " ",
  "# env sets one value. configMapKeyRef reads one key.",
  "# envFrom injects every key.",
  "# The kubelet injects KUBERNETES_SERVICE_HOST for the API server.",
  "$ cat > config-env.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f config-env.yaml " + N,
  "$ kubectl wait --for=condition=Ready pod/config-env " + N + " --timeout=120s",
  "# printenv shows one value for each name, in the order of the names.",
  "$ kubectl exec config-env " + N + " -- \\",
  "    printenv GREETING COLOR APP_COLOR APP_MODE LOG_LEVEL KUBERNETES_SERVICE_HOST",
  ], "config-env.yaml", "config-env.yaml", CM_ENV_POD),
 ("step2", "A ConfigMap as a volume", "bash", [
  "# Each key becomes a file in the volume.",
  "$ cat > config-volume.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f config-volume.yaml " + N,
  "$ kubectl wait --for=condition=Ready pod/config-volume " + N + " --timeout=120s",
  "$ kubectl exec config-volume " + N + " -- ls /etc/app-config",
  "$ kubectl exec config-volume " + N + " -- cat /etc/app-config/APP_COLOR; echo",
  " ",
  "# Change the ConfigMap. The kubelet updates the file within about one minute.",
  "# An environment variable gets its value when the container starts.",
  "# It does not change while the container runs.",
  "$ kubectl patch configmap app-config " + N + " -p '{\"data\":{\"APP_COLOR\":\"green\"}}'",
  "# Wait until the file shows green.",
  "$ until kubectl exec config-volume " + N + " -- \\",
  "    cat /etc/app-config/APP_COLOR | grep green; do sleep 5; done",
  "$ kubectl exec config-env " + N + " -- printenv APP_COLOR     # still blue",
  ], "config-volume.yaml", "config-volume.yaml", no_busybox(v1.CM_VOL_POD)),
 ("step2", "A Secret, and the ServiceAccount token", "bash", [
  "$ printf 'paswrd' > DB_Password",
  "$ kubectl create secret generic app-secret " + N + " \\",
  "    --from-literal=DB_Host=mysql --from-file=DB_Password",
  "# base64 is an encoding, not encryption. Anyone can decode it, with no key.",
  "$ kubectl get secret app-secret " + N + " -o jsonpath='{.data.DB_Password}' | base64 -d; echo",
  " ",
  "# secretKeyRef reads one key. secretRef injects every key.",
  "# When env and envFrom set the same name, the value of env wins.",
  "$ cat > secret-pod.yaml <<'EOF'",
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
  "$ cat > config-dev.yaml <<'EOF'",
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
 ("step", "Delete the objects, and destroy the cluster", "bash", [
  "# ON THE MASTER - delete the Kubernetes objects.",
  "# Each Pod, ConfigMap and Secret belongs to one namespace. Kubernetes deletes them with it.",
  "# This step takes about 40 seconds.",
  "$ bash cleanup_lab12.sh",
  " ",
  "# ON YOUR OWN MACHINE - destroy the three EC2 instances.",
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
# Terraform builds 3 machines: 1 master and 2 workers. The cluster forms
# itself at boot, as in Weeks 04 to 10. The objects of the lab
# are in the namespaces week12 and week12-dev.
#
# Each step matches one slide of Lab_week12_v6.pptx.
"""

# --ignore-not-found: kubectl delete waits for the deletion only when each name exists. Without it, a student
# who stops before Step 5 (no week12-dev) gets week12 still Terminating (recovery test, 2026-11-10).
CLEANUP = """kubectl delete namespace week12 week12-dev --ignore-not-found
rm -f ./fortune-args.yaml ./config-env.yaml ./config-volume.yaml ./secret-pod.yaml
rm -f ./config-dev.yaml ./LOG_LEVEL ./DB_Password

kubectl get namespaces | grep week12"""

# Step 0 of localMachine.sh: the commands of the cluster slide (slide 3). The commands of your own machine
# are comments, because the script runs on the master (review of 2026-11-10, S15).
STEP0 = [
    "# ON YOUR OWN MACHINE - get the repo, build 1 master + 2 workers (slide 3).",
    "# No clone yet? git clone https://github.com/sojoudian/CLO835_Fall_2026.git",
    "# git reset --hard replaces your local changes in the repo with the files of GitHub.",
    "# ON YOUR OWN MACHINE:  cd CLO835_Fall_2026 && git fetch && git reset --hard origin/master",
    "# ON YOUR OWN MACHINE:  cd Week12 && terraform init",
    "# ON YOUR OWN MACHINE:  terraform apply          # Terraform asks for key_name",
    "# ON YOUR OWN MACHINE:  terraform output public_ips",
    "# ON YOUR OWN MACHINE:  terraform output private_ips",
    "# ON YOUR OWN MACHINE:  ssh -i <your-key>.pem ubuntu@<masternode-public-ip>",
    "# ON THE MASTER - all three nodes must reach Ready. The workers take a few minutes to join.",
    "kubectl get nodes -o wide",
    "kubectl get pods -n kube-system",
]

CLUSTER_EDITS = {
    # A clone made before the history rewrite of 2026-11-05 cannot pull; fetch and reset work in each clone.
    "# ON YOUR MACHINE - build 1 master + 2 workers": "# ON YOUR OWN MACHINE - get the repo, build 1 master + 2 workers",
    "$ cd week5_code": "$ cd CLO835_Fall_2026 && git fetch && git reset --hard origin/master",
    "$ terraform init": "$ cd Week12 && terraform init",
    # STE: no -ing form in a title.
    "Preparing the cluster": "Build and check the cluster",
    # B5 and A1 (review of 2026-11-10): "show", not "prints"; each command shows one kind of address.
    "# Every run prints BOTH addresses of all three nodes":
        "# These two commands show the public and the private addresses.",
    # Week 12 has no Service, so the NodePort line gives a fact of the live cluster in its place.
    "# NodePort 30000-32767 is open on both workers.": "# Each node runs Ubuntu 26.04 and containerd 2.2.2.",
    # B5: a sample output line is a comment, and the sample command starts with $.
    "ubuntu@masternode:~$ kubectl get nodes": "$ kubectl get nodes",
    "NAME          STATUS   ROLES           AGE   VERSION": "# NAME          STATUS   ROLES           AGE   VERSION",
    "masternode    Ready    control-plane   4m    v1.35.0": "# masternode    Ready    control-plane   4m    v1.35.10",
    "workernode1   Ready    worker          3m    v1.35.0": "# workernode1   Ready    worker          3m    v1.35.10",
    "workernode2   Ready    worker          3m    v1.35.0": "# workernode2   Ready    worker          3m    v1.35.10",
}

BLACKBOARD_TEXT = "# Lab Week 12: ConfigMaps and Secrets\n\n## Submission Instructions\n\nSubmit a report demonstrating your completion and understanding of all 7 sections of Lab Week 12.\n\nThe lab recording demonstrates the steps required to complete this assignment. You may follow the recording step by step. However, your submission must include your own screenshots, actual command outputs, and explanations for all required tasks.\n\n## 1. Build the Cluster and Verify Its Status\n\nThe Week 12 Terraform configuration creates three Ubuntu 26.04 EC2 instances, as in Weeks 04 to 10: one master node and two worker nodes. The Kubernetes cluster initializes automatically at boot.\n\nYou must:\n\n- Update the repo with git fetch and git reset --hard origin/master, then run terraform init and terraform apply.\n- Run terraform output public_ips and terraform output private_ips, and show the addresses of all three nodes.\n- Show an SSH session connected to the master node.\n- Run kubectl get nodes -o wide and show all three nodes in the Ready state.\n- Run kubectl get pods -n kube-system and show the control-plane Pods in the Running state.\n\n## 2. Replace the CMD of an Image\n\nThe args field of a container replaces the CMD of its image. The command field replaces the ENTRYPOINT. Copy the commands of each step from localMachine.sh, and run them on the master node.\n\nYou must:\n\n- Create the week12 namespace.\n- Create fortune-args.yaml and display its contents.\n- Apply the manifest and wait until the fortune-args Pod is Ready.\n- Run kubectl logs fortune-args -n week12 | head -4, and show the interval of 2 seconds.\n- Explain why you do not put configuration data in a container image.\n- Explain which Docker instruction the command field replaces, and which instruction the args field replaces.\n\n## 3. Use a ConfigMap as Environment Variables\n\nThe values stay in a ConfigMap, not in the Pod manifest.\n\nYou must:\n\n- Create the LOG_LEVEL file, then create the app-config ConfigMap with --from-literal and --from-file.\n- Create config-env.yaml and display its contents.\n- Apply the manifest and wait until the config-env Pod is Ready.\n- Run the printenv command for GREETING, COLOR, APP_COLOR, APP_MODE, LOG_LEVEL and KUBERNETES_SERVICE_HOST, and show the values.\n- Explain the difference between --from-literal and --from-file.\n- Explain the difference between env, configMapKeyRef and envFrom.\n\n## 4. Use a ConfigMap as a Volume\n\nEach key of a ConfigMap becomes a file in the volume.\n\nYou must:\n\n- Create config-volume.yaml and display its contents.\n- Apply the manifest and wait until the config-volume Pod is Ready.\n- Run the ls and cat commands on /etc/app-config, and show the value of APP_COLOR.\n- Change APP_COLOR to green with kubectl patch.\n- Run the until loop, and show the new value green in the file.\n- Show that APP_COLOR in the config-env Pod is still blue.\n- Explain why the file changes and the environment variable does not change.\n\n## 5. Use a Secret, and Find the ServiceAccount Token\n\nKubernetes injects the data of a Secret into a container as an environment variable or as a file. Each Pod also gets a ServiceAccount token.\n\nYou must:\n\n- Create the DB_Password file, then create the app-secret Secret with --from-literal and --from-file.\n- Read DB_Password with the jsonpath command and base64 -d.\n- Create secret-pod.yaml and display its contents.\n- Apply the manifest and wait until the secret-pod Pod is Ready.\n- Show DB_Password and DB_Host as environment variables, and DB_Host as a file.\n- Run the mount command, and show that the Secret volume is tmpfs.\n- Run the ls command on /var/run/secrets/kubernetes.io/serviceaccount and show the three files.\n- Run kubectl get secrets -n week12 and show that no Secret holds the token.\n- Explain the difference between secretKeyRef and secretRef.\n- Explain why base64 is not encryption.\n- Explain what tmpfs protects, and what it does not protect.\n- Explain which permissions the default ServiceAccount has.\n- Explain why an environment variable is not the recommended method for a Secret.\n\n## 6. Use a Second Environment, and Read a Secret from etcd\n\nThe same Pod manifest gets other values in another namespace. By default, etcd stores a Secret as plain bytes.\n\nYou must:\n\n- Create config-dev.yaml and display its contents.\n- Apply the manifest with kubectl apply -f config-dev.yaml.\n- Apply config-env.yaml in the week12-dev namespace and wait until the Pod is Ready.\n- Run the printenv command in week12-dev, and show red and dev.\n- Store the etcdctl command and its certificate flags, as the lab shows.\n- Run the etcdctl get command for the Secret of week12-dev, and show dev-pass in the output.\n- Explain why config-dev.yaml holds a base64 value in the data field of the Secret.\n- Explain how the same Pod manifest gets other values in the second namespace.\n- Explain two methods that protect a Secret.\n\n## 7. Delete the Objects and Destroy the Cluster\n\nAt the end of the lab, delete the Kubernetes objects and destroy all three EC2 instances.\n\nYou must:\n\n- Run bash cleanup_lab12.sh on the master node, and show that both namespaces are deleted.\n- From the Week12 directory on your own machine, run terraform destroy.\n- Include the final Terraform output, which shows the message Destroy complete!\n- State the number of resources Terraform destroyed.\n- Explain why the deletion of a namespace deletes the Pods, ConfigMaps and Secrets in it.\n\n## Submission Requirements\n\nYour report must include all of the following:\n\n- Your name clearly visible in every screenshot.\n- Screenshots demonstrating the required commands and results in all 7 sections.\n- Actual output from the commands you executed.\n- Clear, detailed explanations of the commands, their purpose, and the results.\n- Highlighted or clearly visible output where appropriate.\n- Answers to every explanation question specified in the lab.\n\nImportant: Use your own screenshots and outputs from your lab environment. Screenshots or outputs copied from the recording or another student's submission do not demonstrate your own work.\n"


def repo_words(dst):
    """A1 words in the repo files of Week 12 (review of 2026-11-10). The cleanup header changes in
    cleanup_lab12.sh and in master-init.sh.tftpl together, so master-init still writes the same script."""
    head_old = ("# CLO835 - Lab Week 12 - remove everything the lab creates inside the cluster.\n"
                "# The three machines are removed by \"terraform destroy\" on your own laptop.\n")
    head_new = ("# CLO835 - Lab Week 12 - delete the objects and the files that the lab creates.\n"
                "# On your own machine, \"terraform destroy\" destroys the three machines.\n")
    edits = {
        "cleanup_lab12.sh": [(head_old, head_new)],
        "master-init.sh.tftpl": [
            (head_old, head_new),
            ("# === Control-plane init. This is appended after bootstrap.sh and runs as root. ===",
             "# === Control-plane init. Terraform appends this to bootstrap.sh, and it runs as root. ==="),
            ("# would kill this whole script, so the apply retries until it sticks.",
             "# would stop this whole script, so the apply tries again until it works."),
            ("# The last step of localMachine.sh calls ./cleanup_lab12.sh. The student runs\n"
             "# terraform on their own laptop, so that file never reaches this node. Write it\n"
             "# here, so the last step of the lab works with no copying.",
             "# The last step of localMachine.sh runs bash cleanup_lab12.sh. The student runs\n"
             "# terraform on their own machine, so that file never reaches this node. Write it\n"
             "# here, so the last step of the lab works with no copy."),
            ("  You are on the CONTROL PLANE node. kubectl is ready.", "  You are on the MASTER node. kubectl is ready."),
            ("# kubeconfig for the ubuntu user, so kubectl works right after you SSH in.",
             "# kubeconfig for the ubuntu user, so kubectl works when you connect with SSH."),
            ("# Label the workers as they join. This runs in the background, so cloud-init\n"
             "# is not blocked while it waits.",
             "# Label the workers as they join. This runs in the background, so cloud-init\n"
             "# continues while it waits."),
        ],
        "bootstrap.sh": [
            ("# 1. Turn swap off. kubelet refuses to start while swap is on.",
             "# 1. Stop swap. The kubelet does not start while swap is on."),
            ("#    8951-byte overlay. A NodePort reply bigger than 1500 bytes is dropped on\n"
             "#    the way to a browser on the internet, so the page never loads while the\n"
             "#    headers arrive fine. 1500 here makes Flannel compute 1450.",
             "#    8951-byte overlay. The internet path drops a NodePort reply bigger than\n"
             "#    1500 bytes, so a browser gets the headers but never the page. With 1500\n"
             "#    here, Flannel uses 1450."),
            ("# 3. Kernel modules and sysctls for the pod network.", "# 3. Kernel modules and sysctls for the Pod network."),
        ],
        "variables.tf": [("The AWS Academy Learner Lab ships one called LabInstanceProfile (LabRole); the Learner Lab "
                          "forbids creating IAM roles but allows passing this one.",
                          "The AWS Academy Learner Lab has the profile LabInstanceProfile (LabRole). The Learner Lab "
                          "blocks the creation of IAM roles, but it allows this profile.")],
        ".gitignore": [("# Keys / secrets \u2014 never commit these", "# Keys and secrets: never commit these")],
        "main.tf": [('description = "Week12 Kubernetes control-plane node"', 'description = "Week12 Kubernetes master node"')],
    }
    for name, pairs in edits.items():
        path = os.path.join(dst, name)
        text = open(path, encoding="utf8").read()
        for old, new in pairs:
            assert text.count(old) == 1, (name, old[:50])
            text = text.replace(old, new)
        open(path, "w", encoding="utf8").write(text)


def cluster_comment_color(prs):
    """B5: the sample output lines of the cluster panel are comments, so they get the comment color
    of the line "# Three real nodes. ..." on the same slide."""
    slide = prs.slides[2]
    shapes = [sh for sh in slide.shapes if sh.has_text_frame]
    model = [sh for sh in shapes if sh.text_frame.text.startswith("# Three real nodes")]
    assert len(model) == 1
    green = model[0].text_frame.paragraphs[0].runs[0].font.color.rgb
    names = ("# NAME ", "# masternode ", "# workernode1 ", "# workernode2 ")
    hit = 0
    for sh in shapes:
        if sh.text_frame.text.startswith(names):
            for p in sh.text_frame.paragraphs:
                for r in p.runs:
                    r.font.color.rgb = green
            hit += 1
    assert hit == 4, hit
    # With "# " the node lines have 55 characters: 4.41 in at 10.5 pt, in boxes of 4.39 in. The left panel
    # uses 10 pt, so the lines of the right panel get 10 pt too (4.20 in), and no line wraps.
    from pptx.util import Pt
    for sh in shapes:
        if sh.left > 8 * 914400 and sh.top > 1.9 * 914400:
            for p in sh.text_frame.paragraphs:
                for r in p.runs:
                    r.font.size = Pt(10)


def kubernetes_not_k8s(prs):
    """One word for one meaning: Kubernetes, not K8s (the prerequisite slide)."""
    for slide in prs.slides:
        for sh in slide.shapes:
            if sh.has_text_frame:
                for p in sh.text_frame.paragraphs:
                    for r in p.runs:
                        r.text = r.text.replace("K8s", "Kubernetes")


if __name__ == "__main__":
    for out in (OUT, SCRIPT, BLACKBOARD):
        if os.path.exists(out) and "--force" not in sys.argv:
            sys.exit("%s exists. Bump the version; never overwrite a delivered file." % out)
    L.check_lines(SLIDES)
    L.make_lab("12", SLIDES, OUT, SCRIPT_HEAD, step0=STEP0, script_path=SCRIPT,
               prereq_title="Lab Week 12 - Prerequisites", node_version="v1.35.10", cluster_edits=CLUSTER_EDITS)
    prs = Presentation(OUT)
    kubernetes_not_k8s(prs)
    cluster_comment_color(prs)
    finish(prs, "CLO835 Week 12 Lab: ConfigMaps and Secrets")
    prs.save(OUT)
    if "--no-repo" not in sys.argv:
        dst, files = L.make_repo_folder("12", "ConfigMaps and Secrets", CLEANUP, SCRIPT, lab_label="Lab Week 12")
        own_flannel(dst)
        repo_words(dst)
        print("repo folder : %s (%d files)" % (dst, len(files)))
    open(BLACKBOARD, "w", encoding="utf8").write(BLACKBOARD_TEXT)
    print("blackboard  : %s" % BLACKBOARD)
