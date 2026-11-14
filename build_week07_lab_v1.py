# -*- coding: utf-8 -*-
"""CLO835 Week 07 - the Volumes lab on the kubeadm cluster (new; Week 07 had no lab).

The lecture (Week07/Week07_lab_style_v5.pptx) teaches emptyDir, the volume
lifecycle, the gitRepo type and its init-container replacement, hostPath,
PersistentVolumes through a PersistentVolumeClaim and a StorageClass, and NFS.
Each workshop practises one of them on the 3-node kubeadm cluster.

Outputs (one content list, so deck and script cannot differ):
  Week07/Lab_week07_v1.pptx
  Week07/localMachine_v1.sh
  Week07/Lab_week07_Blackboard_Submission.md
  ~/Documents/c/r/CLO835_Fall_2026/Week07/   (the 8 files of the house pattern)
Run from the project root. It is guarded, so importing it writes nothing.
"""
import sys

import lab_kubeadm as L

F = L.FILE_MARK
SC_URL = L.MIRRORS + "local-path-provisioner/v0.0.37/local-path-storage.yaml"

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

GITREPO = """apiVersion: v1
kind: Pod
metadata:
  name: gitrepo-volume-pod
spec:
  initContainers:
  - name: git-clone
    image: maziar/alpine-git
    args:
    - clone
    - https://github.com/sojoudian/kubia-website-example
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

CLAIM = """apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-claim
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: standard
  resources:
    requests:
      storage: 1Gi""".split("\n")

CLAIM_POD = """apiVersion: v1
kind: Pod
metadata:
  name: pod-using-my-claim
spec:
  containers:
  - name: shell
    image: busybox:1.36
    command: ["sleep", "3600"]
    volumeMounts:
    - mountPath: /my-data
      name: my-volume
  volumes:
  - name: my-volume
    persistentVolumeClaim:
      claimName: my-claim""".split("\n")

NFS_POD = """apiVersion: v1
kind: Pod
metadata:
  name: NAME
spec:
  nodeSelector:
    kubernetes.io/hostname: NODE
  containers:
  - name: shell
    image: busybox:1.36
    command: ["sleep", "3600"]
    volumeMounts:
    - name: my-nfs-volume
      mountPath: /my-nfs
  volumes:
  - name: my-nfs-volume
    nfs:
      server: $NFS_IP
      path: /srv/nfs""".split("\n")

SLIDES = [
 ("title", "Workshop 1 – emptyDir: Sharing Files between Containers"),
 ("prereq",),
 ("cluster",),
 ("step2", "Two containers, one emptyDir volume", "bash", [
  "# The fortune Pod of the lecture: html-generator writes a new fortune",
  "# every 10 seconds into an emptyDir, and nginx serves the same folder.",
  "$ cat > fortune-pod.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f fortune-pod.yaml",
  "$ kubectl wait --for=condition=Ready pod/fortune --timeout=120s",
  "$ kubectl get pod fortune -o wide",
  " ",
  "# The master reaches each Pod IP. Call nginx two times, 10 s apart.",
  "$ POD_IP=$(kubectl get pod fortune -o jsonpath='{.status.podIP}')",
  "$ curl -s http://$POD_IP; sleep 10; curl -s http://$POD_IP",
  " ",
  "# The writer and the reader are two containers. One volume joins them.",
  "$ kubectl logs fortune -c html-generator --tail=3",
  ], "fortune-pod.yaml", "fortune-pod.yaml", FORTUNE),
 ("step", "The volume shadows the folder", "bash", [
  "# nginx:alpine ships index.html and 50x.html in /usr/share/nginx/html.",
  "# The emptyDir is mounted over that folder, so only the fortune file is there.",
  "$ kubectl exec fortune -c web-server -- ls -l /usr/share/nginx/html",
  " ",
  "# web-server mounts the volume read-only. Try to write a file.",
  "$ kubectl exec fortune -c web-server -- sh -c 'echo hi > /usr/share/nginx/html/x.html'",
  "# sh: can't create /usr/share/nginx/html/x.html: Read-only file system",
  " ",
  "# The emptyDir is a folder on the node that runs the Pod:",
  "#   /var/lib/kubelet/pods/<pod-uid>/volumes/kubernetes.io~empty-dir/html",
  "$ kubectl get pod fortune -o jsonpath='{.metadata.uid}{\"\\n\"}'",
  ]),
 ("step", "The volume lives as long as the Pod", "bash", [
  "# A container restart keeps the volume. Stop nginx: the container exits,",
  "# and the kubelet starts it again in the same Pod.",
  "$ kubectl exec fortune -c web-server -- nginx -s stop",
  "$ sleep 5; kubectl get pod fortune        # RESTARTS is now 1",
  "$ curl -s http://$POD_IP                 # the fortune file is still there",
  " ",
  "# A new Pod gets a new, empty volume. Delete the Pod and create it again.",
  "$ kubectl delete pod fortune",
  "$ kubectl apply -f fortune-pod.yaml",
  "$ kubectl wait --for=condition=Ready pod/fortune --timeout=120s",
  "$ kubectl exec fortune -c web-server -- stat -c '%y' /usr/share/nginx/html/index.html",
  "# The file is new: its time is the start of the new Pod.",
  ]),
 ("end", "Workshop 1 – The End"),

 ("title", "Workshop 2 – Cloning a Git Repository into a Volume"),
 ("step2", "gitRepo is deprecated: an init container clones", "bash", [
  "# The gitRepo volume type is deprecated. explain says so.",
  "$ kubectl explain pod.spec.volumes.gitRepo | head -8",
  " ",
  "# The pattern of the lecture: an init container clones the",
  "# repository into an emptyDir, and nginx serves it.",
  "$ cat > gitrepo-volume-pod.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f gitrepo-volume-pod.yaml",
  "$ kubectl wait --for=condition=Ready pod/gitrepo-volume-pod --timeout=120s",
  "$ kubectl get pod gitrepo-volume-pod   # STATUS Running, after Init:0/1",
  "$ kubectl logs gitrepo-volume-pod -c git-clone",
  " ",
  "# nginx serves the files of the repository.",
  "$ GIT_IP=$(kubectl get pod gitrepo-volume-pod -o jsonpath='{.status.podIP}')",
  "$ curl -s http://$GIT_IP | head -5",
  ], "gitrepo-volume-pod.yaml", "gitrepo-volume-pod.yaml", GITREPO),
 ("end", "Workshop 2 – The End"),

 ("title", "Workshop 3 – hostPath: Data on One Node"),
 ("step2", "hostPath keeps data on one node", "bash", [
  "# A hostPath volume is a folder of the node. It outlives the Pod.",
  "$ cat > hostpath-pod.yaml <<'EOF'",
  F,
  "EOF",
  "# Run the Pod on workernode1 and write a file into the volume.",
  "$ kubectl apply -f hostpath-pod.yaml",
  "$ kubectl wait --for=condition=Ready pod/hostpath-pod --timeout=60s",
  "$ kubectl exec hostpath-pod -- sh -c 'date > /data/written-by-pod.txt'",
  " ",
  "# Delete the Pod, start it again on the same node: the file is there.",
  "$ kubectl delete pod hostpath-pod --now",
  "$ kubectl apply -f hostpath-pod.yaml",
  "$ kubectl wait --for=condition=Ready pod/hostpath-pod --timeout=60s",
  "$ kubectl exec hostpath-pod -- cat /data/written-by-pod.txt",
  " ",
  "# Move the Pod to workernode2: the folder there is empty.",
  "$ kubectl delete pod hostpath-pod --now",
  "$ sed 's/workernode1/workernode2/' hostpath-pod.yaml | kubectl apply -f -",
  "$ kubectl wait --for=condition=Ready pod/hostpath-pod --timeout=60s",
  "$ kubectl exec hostpath-pod -- ls -l /data",
  "# Empty: the data stayed on workernode1.",
  ], "hostpath-pod.yaml", "hostpath-pod.yaml", HOSTPATH),
 ("end", "Workshop 3 – The End"),

 ("title", "Workshop 4 – PersistentVolumeClaims and a StorageClass"),
 ("step", "A StorageClass for the cluster", "bash", [
  "# On EKS, the EBS CSI driver provisions a disk for each claim. This cluster has no cloud",
  "# driver, so we install the local-path provisioner from the course mirror.",
  "$ kubectl apply -f " + SC_URL,
  "$ kubectl -n local-path-storage rollout status deploy/local-path-provisioner",
  " ",
  "# One StorageClass, the default. A claim with no class gets it.",
  "$ kubectl get storageclass",
  "# NAME                 PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE",
  "# standard (default)   rancher.io/local-path   Delete          WaitForFirstConsumer",
  " ",
  "# A PersistentVolume is an API resource. A plain volume is not.",
  "$ kubectl api-resources | grep -i persistentvolume",
  ]),
 ("step2", "A PersistentVolumeClaim requests the storage", "bash", [
  "# The claim asks for 1 Gi of the standard class.",
  "$ cat > my-claim.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f my-claim.yaml",
  " ",
  "# WaitForFirstConsumer: no PV is made until a Pod",
  "# uses the claim, so the claim stays Pending.",
  "$ kubectl get pvc my-claim",
  "$ kubectl describe pvc my-claim | tail -3",
  "$ kubectl get pv",
  ], "my-claim.yaml", "my-claim.yaml", CLAIM),
 ("step2", "The Pod mounts the volume through the claim", "bash", [
  "$ cat > pod-using-my-claim.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f pod-using-my-claim.yaml",
  "$ kubectl wait --for=condition=Ready pod/pod-using-my-claim --timeout=120s",
  "$ kubectl get pvc,pv                 # Bound, and a new PV",
  " ",
  "# Write data, delete the Pod, mount the same claim again.",
  "$ kubectl exec pod-using-my-claim -- sh -c 'echo kept > /my-data/note.txt'",
  "$ kubectl delete pod pod-using-my-claim --now",
  "$ kubectl apply -f pod-using-my-claim.yaml",
  "$ kubectl wait --for=condition=Ready pod/pod-using-my-claim --timeout=120s",
  "$ kubectl exec pod-using-my-claim -- cat /my-data/note.txt",
  " ",
  "# 'kept': the claim outlives the Pod. This PV is a folder of",
  "# one node, so the Pod returns to that node:",
  "$ kubectl describe pv | grep -A3 'Node Affinity'",
  ], "pod-using-my-claim.yaml", "pod-using-my-claim.yaml", CLAIM_POD),
 ("end", "Workshop 4 – The End"),

 ("title", "Workshop 5 – An NFS Volume"),
 ("step2", "One NFS share, two Pods on two nodes", "bash", [
  "# Terraform made an NFS server on the master: /srv/nfs. Every",
  "# node has the NFS client (nfs-common) from bootstrap.sh.",
  "$ sudo exportfs -v",
  "$ NFS_IP=$(kubectl get node masternode -o jsonpath='{.status.addresses[0].address}')",
  "$ echo $NFS_IP                  # the private IP of the master",
  " ",
  "# No quotes on EOF: the shell writes the address into the file.",
  "$ cat > nfs-pod.yaml <<EOF",
  F,
  "EOF",
  "$ for n in 1 2; do sed \"s/NAME/nfs-pod-$n/;s/NODE/workernode$n/\" nfs-pod.yaml | kubectl apply -f -; done",
  "$ kubectl wait --for=condition=Ready pod/nfs-pod-1 pod/nfs-pod-2 --timeout=120s",
  "$ kubectl get pods nfs-pod-1 nfs-pod-2 -o wide",
  " ",
  "# Write on workernode1, read on workernode2.",
  "$ kubectl exec nfs-pod-1 -- sh -c 'date > /my-nfs/hello.txt'",
  "$ kubectl exec nfs-pod-2 -- cat /my-nfs/hello.txt",
  "# One share for two nodes: an NFS volume is not tied to a node.",
  ], "nfs-pod.yaml", "nfs-pod.yaml", NFS_POD),
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
 ("end", "Workshop 5 – The End"),
]

SCRIPT_HEAD = """#!/bin/bash
# CLO835 - Week 07 - Volumes: attaching disk storage to containers.
# Run these ON THE MASTER NODE, section by section. Do NOT run the whole file.
#
# Terraform builds 3 machines: 1 control plane and 2 workers. The cluster forms
# itself at boot, the same way it did in Weeks 04 to 06. The master also runs an
# NFS server (/srv/nfs) for Workshop 5, and every node has the NFS client.
#
# Each step matches one slide of Lab_week07_v1.pptx.
"""

CLEANUP = """kubectl delete pod fortune gitrepo-volume-pod hostpath-pod pod-using-my-claim nfs-pod-1 nfs-pod-2 --now 2>/dev/null
kubectl delete pvc my-claim 2>/dev/null
kubectl delete -f """ + SC_URL + """ 2>/dev/null
rm -f ./fortune-pod.yaml ./gitrepo-volume-pod.yaml ./hostpath-pod.yaml ./my-claim.yaml ./pod-using-my-claim.yaml ./nfs-pod.yaml

kubectl get pods,pvc,pv"""

MASTER_EXTRA = """# Week 07: an NFS server for Workshop 5. The Pods on the workers mount /srv/nfs.
apt-get install -y nfs-kernel-server
mkdir -p /srv/nfs
chmod 777 /srv/nfs
echo "/srv/nfs *(rw,sync,no_subtree_check,no_root_squash)" >> /etc/exports
exportfs -ra
systemctl enable --now nfs-server"""

BLACKBOARD = [
 ("emptyDir: Two Containers, One Volume",
  "The fortune Pod runs a writer and nginx. They share one emptyDir volume.",
  ["Show kubectl get pod fortune -o wide with the Pod Running and READY 2/2.",
   "Show two curl calls to the Pod IP, 10 seconds apart, with two different fortunes.",
   "Show ls -l of /usr/share/nginx/html in web-server, and explain why 50x.html is not there.",
   "Show the failed write into the read-only mount.",
   "Show RESTARTS 1 after nginx -s stop, and the fortune file still served.",
   "Explain why a container restart keeps the volume, but a new Pod gets an empty one."]),
 ("gitRepo and the Init Container",
  "The gitRepo volume type is deprecated. An init container clones the repository into an emptyDir.",
  ["Show the deprecation text of kubectl explain pod.spec.volumes.gitRepo.",
   "Show the Pod going from Init:0/1 to Running, and the logs of git-clone.",
   "Show curl to the Pod IP returning the website of the repository.",
   "Explain why the init container must finish before nginx starts."]),
 ("hostPath: Data on One Node",
  "A hostPath volume is a folder of the node, not of the Pod.",
  ["Show the file still present after the Pod is deleted and started again on workernode1.",
   "Show the empty folder after the Pod moves to workernode2.",
   "Explain why hostPath is not suitable for a database in a cluster with many workers."]),
 ("PersistentVolumeClaim and StorageClass",
  "The local-path provisioner gives the cluster a default StorageClass, as the EBS CSI driver does on EKS.",
  ["Show kubectl get storageclass with standard (default).",
   "Show the claim Pending before the Pod exists, and Bound after.",
   "Show the PV that the provisioner made, and the note.txt that survives a new Pod.",
   "Explain the difference between a volume in a Pod spec and a PersistentVolume.",
   "Explain WaitForFirstConsumer, and the Node Affinity of a local-path PV."]),
 ("NFS Volume",
  "The master exports /srv/nfs. Two Pods on two workers mount the same share.",
  ["Show sudo exportfs -v on the master.",
   "Show kubectl get pods -o wide with nfs-pod-1 on workernode1 and nfs-pod-2 on workernode2.",
   "Show the file written by nfs-pod-1 and read by nfs-pod-2.",
   "Explain why an NFS volume, unlike hostPath, is not tied to a node.",
   "Show the clean-up and terraform destroy."]),
]

if __name__ == "__main__":
    L.check_lines(SLIDES)
    L.make_lab("07", SLIDES, "Week07/Lab_week07_v1.pptx", SCRIPT_HEAD,
               script_path="Week07/localMachine_v1.sh")
    if "--no-repo" not in sys.argv:
        dst, files = L.make_repo_folder("07", "Volumes", CLEANUP, "Week07/localMachine_v1.sh",
                                        extra_packages="nfs-common", master_extra=MASTER_EXTRA)
        print("repo folder : %s (%d files)" % (dst, len(files)))
    L.blackboard_text("07", "The Terraform configuration in Week 07 creates the same three Ubuntu 26.04 "
                      "EC2 machines as Weeks 04 to 06. The master also runs an NFS server.",
                      BLACKBOARD, "Week07/Lab_week07_Blackboard_Submission.md")
    print("blackboard  : Week07/Lab_week07_Blackboard_Submission.md")
