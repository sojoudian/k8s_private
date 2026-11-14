# -*- coding: utf-8 -*-
"""CLO835 Week 07 lab v2 - Volumes, in ONE workshop.

v1 had 5 workshops and 10 steps, and an NFS server on the master. The limit is
now the size of the Week 03 and Week 04 labs: at most Step 0 to Step 6. v2 keeps
the agenda of the lecture (Week07/Week07_lab_style_v5.pptx): emptyDir, the volume
lifecycle, the init container that replaces gitRepo, hostPath, and a
PersistentVolumeClaim with a StorageClass. NFS is left out.

The init container clones github.com/sojoudian/kubia, which exists. The fork
sojoudian/kubia-website-example of the lecture does not exist yet.
The local-path provisioner comes from the course repository (Week07/).

Outputs: Week07/Lab_week07_v2.pptx, Week07/localMachine_v2.sh,
Week07/Lab_week07_Blackboard_Submission_v2.md, ~/Documents/c/r/CLO835_Fall_2026/Week07/
Run from the project root. It is guarded, so importing it writes nothing.
"""
import os
import sys

import lab_kubeadm as L

F = L.FILE_MARK
MIRROR_DIR = "/private/tmp/claude-501/-Users-maziar-Downloads-k8s-week3/0b02113e-4049-4aa0-bece-9e5b05d8791f/scratchpad/clo835-mirrors"
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
    - {name: html, mountPath: /repo}
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
    image: busybox:1.36
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
    image: busybox:1.36
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
  "# an emptyDir. nginx serves the same folder.",
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
  "# The volume shadows the folder: only the fortune file.",
  "$ kubectl exec fortune -c web-server -- ls /usr/share/nginx/html",
  ], "fortune-pod.yaml", "fortune-pod.yaml", FORTUNE),
 ("step", "The volume lives as long as the Pod", "bash", [
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
 ("step2", "hostPath keeps data on one node", "bash", [
  "# A hostPath volume is a folder of the node.",
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
  "# The file outlived the Pod. It stays on workernode1.",
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
# Each step matches one slide of Lab_week07_v2.pptx.
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

BLACKBOARD = [
 ("emptyDir and the volume lifecycle", "Two containers of one Pod share an emptyDir volume.",
  ["Show two different fortunes from nginx, 10 seconds apart.",
   "Show that the volume shadows /usr/share/nginx/html.",
   "Show RESTARTS 1 after nginx -s stop, and the fortune still there.",
   "Show the new file time after you create the Pod again, and explain why."]),
 ("An init container clones a repository", "The init container replaces the deprecated gitRepo volume.",
  ["Show the log of the git-clone init container.",
   "Show the first lines of app.js from nginx."]),
 ("hostPath, PVC and StorageClass", "A hostPath volume stays on one node. A claim gets a volume from a StorageClass.",
  ["Show the note.txt file after the hostPath Pod is created again.",
   "Show the standard StorageClass, the Bound claim and its PersistentVolume.",
   "Explain the difference between a volume and a PersistentVolume.",
   "Show the clean-up and terraform destroy."]),
]


def sc_manifest():
    return open(os.path.join(MIRROR_DIR, "local-path-provisioner/v0.0.37/local-path-storage.yaml")).read()


if __name__ == "__main__":
    L.check_lines(SLIDES)
    L.make_lab("07", SLIDES, "Week07/Lab_week07_v2.pptx", SCRIPT_HEAD, script_path="Week07/localMachine_v2.sh")
    if "--no-repo" not in sys.argv:
        dst, files = L.make_repo_folder("07", "Volumes", CLEANUP, "Week07/localMachine_v2.sh",
                                        extra_files={SC_FILE: sc_manifest()})
        print("repo folder : %s (%d files)" % (dst, len(files)))
    L.blackboard_text("07", "The Terraform configuration in Week 07 creates the same three Ubuntu 26.04 EC2 "
                      "machines as Weeks 04 to 06.", BLACKBOARD, "Week07/Lab_week07_Blackboard_Submission_v2.md")
    print("blackboard  : Week07/Lab_week07_Blackboard_Submission_v2.md")
