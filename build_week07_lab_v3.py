# -*- coding: utf-8 -*-
"""CLO835 Week 07 lab v3 - Volumes, in ONE workshop.

v3 fixes the lab defects 28, 34, 35, 36 and 37 of
reports/report-2026-11-09-02-week07-week10-lecture-audit.md:
- Step 2 says "An emptyDir lives as long as the Pod", because a persistent volume does not.
- The lab name is "Lab Week 07", as in the Blackboard texts.
- maziar/alpine-curl replaces busybox:1.36 in Steps 4 and 5, and busybox in the helper Pod of the local-path
  manifest (as in the live-tested Week 10 manifest). "Kubernetes" replaces "K8s" on slide 2.
- The init container manifest uses one YAML style.
- "directory" replaces "folder", as in the lecture.
- The Blackboard text has the long form of Lab04, with no pledge.
- The file has a title and an author, and no blank thumbnail. "stays" replaces "keeps".
The local-path manifest comes from the course repository, not from a scratchpad copy.

v2 notes follow.


v1 had 5 workshops and 10 steps, and an NFS server on the master. The limit is
now the size of the Week 03 and Week 04 labs: at most Step 0 to Step 6. v2 keeps
the agenda of the lecture (Week07/Week07_lab_style_v5.pptx): emptyDir, the volume
lifecycle, the init container that replaces gitRepo, hostPath, and a
PersistentVolumeClaim with a StorageClass. NFS is left out.

The init container clones github.com/sojoudian/kubia, which exists. The fork
sojoudian/kubia-website-example of the lecture does not exist yet.
The local-path provisioner comes from the course repository (Week07/).

Outputs: Week07/Lab_week07_v3.pptx, Week07/localMachine_v3.sh,
Week07/Lab_week07_Blackboard_Submission_v3.md, ~/Documents/c/r/CLO835_Fall_2026/Week07/
Run from the project root. It is guarded, so importing it writes nothing.
"""
import os
import sys

from pptx import Presentation

import lab_kubeadm as L
from build_week12_lecture_v6 import finish

F = L.FILE_MARK
SC_FILE = "local-path-storage.yaml"
SC_URL = L.RAW + "Week07/" + SC_FILE

FORTUNE = """apiVersion: v1
kind: Pod
metadata:
  name: fortune
spec:
  containers:
  - image: maziar/fortune:env
    name: html-generator
    env:
    - name: INTERVAL
      value: "10"
    volumeMounts:
    - name: html
      mountPath: /var/htdocs
  - image: nginx:alpine
    name: web-server
    volumeMounts:
    - name: html
      mountPath: /usr/share/nginx/html
      readOnly: true
    ports:
    - containerPort: 80
  volumes:
  - name: html
    emptyDir: {}""".split("\n")

GITCLONE = """apiVersion: v1
kind: Pod
metadata:
  name: gitrepo-volume-pod
spec:
  initContainers:
  - name: git-clone
    image: maziar/alpine-git
    args:
    - clone
    - --branch=master
    - https://github.com/sojoudian/kubia.git
    - /repo
    volumeMounts:
    - name: html
      mountPath: /repo
  containers:
  - image: nginx:alpine
    name: web-server
    volumeMounts:
    - name: html
      mountPath: /usr/share/nginx/html
      readOnly: true
  volumes:
  - name: html
    emptyDir: {}""".split("\n")

HOSTPATH = """apiVersion: v1
kind: Pod
metadata:
  name: hostpath-pod
spec:
  nodeSelector:
    kubernetes.io/hostname: workernode1
  containers:
  - name: shell
    image: maziar/alpine-curl
    command: ["sleep", "3600"]
    volumeMounts:
    - name: node-data
      mountPath: /data
  volumes:
  - name: node-data
    hostPath:
      path: /tmp/clo835-week07
      type: DirectoryOrCreate""".split("\n")

CLAIM_POD = """apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-claim
spec:
  accessModes: [ReadWriteOnce]
  storageClassName: standard
  resources:
    requests: {storage: 1Gi}
---
apiVersion: v1
kind: Pod
metadata:
  name: pod-using-my-claim
spec:
  containers:
  - name: shell
    image: maziar/alpine-curl
    command: ["sleep", "3600"]
    volumeMounts:
    - {name: my-volume, mountPath: /my-data}
  volumes:
  - name: my-volume
    persistentVolumeClaim:
      claimName: my-claim""".split("\n")

SLIDES = [
 ("title", "Workshop 1 – Volumes: Attaching Storage to Containers"),
 ("prereq",),
 ("cluster",),
 ("step2", "Two containers share one emptyDir", "bash", [
  "# html-generator writes a new fortune every 10 s into",
  "# an emptyDir. nginx serves the same directory.",
  "$ cat > fortune-pod.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f fortune-pod.yaml",
  "$ kubectl wait --for=condition=Ready pod/fortune --timeout=120s",
  " ",
  "# The master reaches each Pod IP. Call nginx 2 times.",
  "$ POD_IP=$(kubectl get pod fortune -o jsonpath='{.status.podIP}')",
  "$ curl -s http://$POD_IP; sleep 10; curl -s http://$POD_IP",
  " ",
  "# The volume hides the old files: only the fortune file.",
  "$ kubectl exec fortune -c web-server -- ls /usr/share/nginx/html",
  ], "fortune-pod.yaml", "fortune-pod.yaml", FORTUNE),
 ("step", "An emptyDir lives as long as the Pod", "bash", [
  "# A container restart keeps the volume. Stop nginx: the kubelet starts it again.",
  "$ kubectl exec fortune -c web-server -- nginx -s stop",
  "$ sleep 5; kubectl get pod fortune                  # RESTARTS is now 1",
  "$ curl -s http://$POD_IP                            # the fortune is still there",
  " ",
  "# A new Pod gets a new, empty volume.",
  "$ kubectl delete pod fortune",
  "$ kubectl apply -f fortune-pod.yaml",
  "$ kubectl wait --for=condition=Ready pod/fortune --timeout=120s",
  "$ kubectl exec fortune -c web-server -- stat -c '%y' /usr/share/nginx/html/index.html",
  "# The file is new: its time is the start of the new Pod.",
  ]),
 ("step2", "gitRepo is deprecated: an init container clones", "bash", [
  "# The init container clones a repository into an",
  "# emptyDir. Then nginx starts and serves it.",
  "$ cat > gitrepo-volume-pod.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f gitrepo-volume-pod.yaml",
  "$ kubectl wait --for=condition=Ready pod/gitrepo-volume-pod --timeout=120s",
  "$ kubectl logs gitrepo-volume-pod -c git-clone",
  " ",
  "# nginx serves the files of the repository.",
  "$ GIT_IP=$(kubectl get pod gitrepo-volume-pod \\",
  "    -o jsonpath='{.status.podIP}')",
  "$ curl -s http://$GIT_IP/app.js | head -5",
  ], "gitrepo-volume-pod.yaml", "gitrepo-volume-pod.yaml", GITCLONE),
 ("step2", "hostPath data stays on one node", "bash", [
  "# A hostPath volume is a directory of the node.",
  "$ cat > hostpath-pod.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f hostpath-pod.yaml",
  "$ kubectl wait --for=condition=Ready pod/hostpath-pod --timeout=60s",
  "$ kubectl exec hostpath-pod -- sh -c 'date > /data/note.txt'",
  " ",
  "# Delete the Pod and start it again on the same node.",
  "$ kubectl delete pod hostpath-pod --now",
  "$ kubectl apply -f hostpath-pod.yaml",
  "$ kubectl wait --for=condition=Ready pod/hostpath-pod --timeout=60s",
  "$ kubectl exec hostpath-pod -- cat /data/note.txt",
  "# The file is still there. It stays on workernode1.",
  ], "hostpath-pod.yaml", "hostpath-pod.yaml", HOSTPATH),
 ("step2", "A PersistentVolumeClaim and a StorageClass", "bash", [
  "# No cloud driver here, so install the",
  "# local-path provisioner of the course repository.",
  "$ REPO=" + L.RAW.rstrip("/"),
  "$ kubectl apply -f $REPO/Week07/" + SC_FILE,
  "$ kubectl get storageclass          # standard (default)",
  " ",
  "# The claim and a Pod that uses it.",
  "$ cat > my-claim.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f my-claim.yaml",
  "$ kubectl wait --for=condition=Ready pod/pod-using-my-claim --timeout=180s",
  "$ kubectl get pvc,pv                # Bound, and a new PV",
  " ",
  "$ kubectl exec pod-using-my-claim -- sh -c 'echo kept > /my-data/note.txt'",
  "$ kubectl exec pod-using-my-claim -- cat /my-data/note.txt",
  ], "my-claim.yaml", "my-claim.yaml", CLAIM_POD),
 ("step", "Clean up", "bash", [
  "# ON THE MASTER - remove the Kubernetes objects.",
  "$ bash cleanup_lab07.sh",
  " ",
  "# Confirm that nothing is left.",
  "$ kubectl get pods,pvc,pv",
  " ",
  "# ON YOUR OWN MACHINE - remove the three EC2 machines.",
  "L$ terraform destroy",
  " ",
  "# Always destroy. The Learner Lab budget is small.",
  ]),
 ("end", "Workshop 1 – The End"),
]

SCRIPT_HEAD = """#!/bin/bash
# CLO835 - Week 07 - Volumes: attaching storage to containers.
# Run these ON THE MASTER NODE, section by section. Do NOT run the whole file.
#
# Terraform builds 3 machines: 1 control plane and 2 workers. The cluster forms
# itself at boot, the same way it did in Weeks 04 to 06.
#
# Each step matches one slide of Lab_week07_v3.pptx.
"""

CLEANUP = """kubectl delete pod fortune gitrepo-volume-pod hostpath-pod pod-using-my-claim --now 2>/dev/null
kubectl delete pvc my-claim 2>/dev/null
# The provisioner deletes the PV of the claim. Wait for that, then remove the provisioner.
for i in $(seq 30); do [ -z "$(kubectl get pv -o name)" ] && break; sleep 2; done
kubectl delete storageclass standard 2>/dev/null
kubectl delete namespace local-path-storage 2>/dev/null
kubectl delete clusterrolebinding local-path-provisioner-bind 2>/dev/null
kubectl delete clusterrole local-path-provisioner-role 2>/dev/null
rm -f ./fortune-pod.yaml ./gitrepo-volume-pod.yaml ./hostpath-pod.yaml ./my-claim.yaml

kubectl get pods,pvc,pv"""

# The Blackboard text, in the long form of the item "Lab04 - 2.5%" (Lab Week 06): one section for each step,
# "You must:", the Explain items last, and no pledge. Each Explain item has its answer in the lecture v7.
BLACKBOARD_TEXT = """# Lab Week 07: Volumes

## Submission Instructions

Submit a report demonstrating your completion and understanding of all 7 sections of Lab Week 07.

The lab recording demonstrates the steps required to complete this assignment. You may follow the recording step by step. However, your submission must include your own screenshots, actual command outputs, and explanations for all required tasks.

## 1. Build the Cluster and Verify Its Status

The Week 07 Terraform configuration creates three Ubuntu 26.04 EC2 instances, as in Weeks 04 to 06: one master node and two worker nodes. The Kubernetes cluster initializes automatically at boot.

You must:

- Run terraform init and terraform apply.
- Run terraform output public_ips and terraform output private_ips, and show the addresses of all three nodes.
- Show an SSH session connected to the master node.
- Run kubectl get nodes -o wide and show all three nodes in the Ready state.
- Run kubectl get pods -n kube-system and show the system Pods in the Running state.

## 2. Two Containers Share One emptyDir

Two containers of one Pod share an emptyDir volume. html-generator writes a new fortune every 10 seconds, and nginx serves the same directory.

You must:

- Create fortune-pod.yaml and display its contents.
- Apply the manifest using kubectl apply -f fortune-pod.yaml, and run the kubectl wait command for the fortune Pod.
- Run the two curl commands and show two different fortunes, 10 seconds apart.
- Run kubectl exec fortune -c web-server -- ls /usr/share/nginx/html and show that only the fortune file is there.
- Explain why the old files of /usr/share/nginx/html are not visible.
- Explain how the two containers share one file, with two different mount paths.

## 3. An emptyDir Lives as Long as the Pod

A container restart keeps the volume. A new Pod gets a new, empty volume.

You must:

- Stop nginx with kubectl exec fortune -c web-server -- nginx -s stop.
- Run kubectl get pod fortune and show RESTARTS 1.
- Run the curl command again and show that the fortune is still there.
- Delete the fortune Pod, apply the manifest again, and run the kubectl wait command.
- Run the stat command and show the time of index.html.
- Explain why index.html has a new time.
- Explain which volume types end with the Pod, and which volume types have data that stays after the Pod.

## 4. An Init Container Clones a Repository

The gitRepo volume type is deprecated, and Kubernetes turns it off by default. An init container clones the repository into an emptyDir volume.

You must:

- Create gitrepo-volume-pod.yaml and display its contents.
- Apply the manifest using kubectl apply -f gitrepo-volume-pod.yaml, and run the kubectl wait command.
- Run kubectl logs gitrepo-volume-pod -c git-clone and show the log of the init container.
- Run the curl command and show the first lines of app.js from nginx.
- Explain why args starts with clone and not with git.
- Explain why a new commit in the repository needs a new Pod.

## 5. hostPath Data Stays on One Node

A hostPath volume mounts a directory of the node into the Pod. The data stays on that node.

You must:

- Create hostpath-pod.yaml and display its contents.
- Apply the manifest using kubectl apply -f hostpath-pod.yaml, and run the kubectl wait command.
- Write the date to /data/note.txt with the kubectl exec command.
- Delete the hostpath-pod Pod, apply the manifest again, and run the kubectl wait command.
- Run kubectl exec hostpath-pod -- cat /data/note.txt and show the same date.
- Explain why this manifest needs the nodeSelector.
- Explain one security risk of a hostPath volume.

## 6. A PersistentVolumeClaim and a StorageClass

A claim asks for storage. The StorageClass standard and its provisioner create a PersistentVolume for the claim.

You must:

- Install the local-path provisioner with the kubectl apply command.
- Run kubectl get storageclass and show the default StorageClass standard.
- Create my-claim.yaml and display its contents.
- Apply the manifest using kubectl apply -f my-claim.yaml, and run the kubectl wait command for the pod-using-my-claim Pod.
- Run kubectl get pvc,pv and show the Bound claim and its PersistentVolume.
- Write to /my-data/note.txt and read the file again with the two kubectl exec commands.
- Explain the difference between a volume and a PersistentVolume.
- Explain what WaitForFirstConsumer means for the claim.

## 7. Clean Up and Destroy the Cluster

At the end of the lab, remove the Kubernetes objects and destroy all three EC2 instances.

You must:

- Run bash cleanup_lab07.sh on the master node.
- Run kubectl get pods,pvc,pv and show that nothing is left.
- From the Week07 directory on your own machine, run terraform destroy.
- Include the final Terraform output showing Destroy complete!.
- State the number of resources Terraform removed.
- Explain why the clean-up deletes the claim before it deletes the provisioner.

## Submission Requirements

Your report must include all of the following:

- Your name clearly visible in every screenshot.
- Screenshots demonstrating the required commands and results in all 7 sections.
- Actual output from the commands you executed.
- Clear, detailed explanations of the commands, their purpose, and the results.
- Highlighted or clearly visible output where appropriate.
- Answers to every explanation question specified in the lab.

Important: Use your own screenshots and outputs from your lab environment. Screenshots or outputs copied from the recording or another student's submission do not demonstrate your own work.
"""


def sc_manifest():
    """The local-path manifest of the course repository (Week07). Its helper Pod uses maziar/alpine-curl,
    as the live-tested Week 10 manifest does, not docker.io/library/busybox."""
    text = open(os.path.join(L.REPO, "Week07", SC_FILE), encoding="utf8").read()
    return text.replace("image: docker.io/library/busybox", "image: docker.io/maziar/alpine-curl")


if __name__ == "__main__":
    for out in ("Week07/Lab_week07_v3.pptx", "Week07/localMachine_v3.sh", "Week07/Lab_week07_Blackboard_Submission_v3.md"):
        if os.path.exists(out) and "--force" not in sys.argv:
            sys.exit("%s exists. Bump the version; never overwrite a delivered file." % out)
    L.check_lines(SLIDES)
    sc = sc_manifest()
    L.make_lab("07", SLIDES, "Week07/Lab_week07_v3.pptx", SCRIPT_HEAD, script_path="Week07/localMachine_v3.sh",
               prereq_title="Lab Week 07 - Prerequisites")
    deck = Presentation("Week07/Lab_week07_v3.pptx")
    finish(deck, "CLO835 Week 7 Lab: Volumes")          # file title and author, no blank thumbnail
    for slide in deck.slides:                           # one word for one meaning: Kubernetes, not K8s
        for sh in slide.shapes:
            if sh.has_text_frame:
                for p in sh.text_frame.paragraphs:
                    for r in p.runs:
                        r.text = r.text.replace("K8s", "Kubernetes")
    deck.save("Week07/Lab_week07_v3.pptx")
    if "--no-repo" not in sys.argv:
        dst, files = L.make_repo_folder("07", "Volumes", CLEANUP, "Week07/localMachine_v3.sh",
                                        extra_files={SC_FILE: sc}, lab_label="Lab Week 07")
        print("repo folder : %s (%d files)" % (dst, len(files)))
    open("Week07/Lab_week07_Blackboard_Submission_v3.md", "w", encoding="utf8").write(BLACKBOARD_TEXT)
    print("blackboard  : Week07/Lab_week07_Blackboard_Submission_v3.md")
