# -*- coding: utf-8 -*-
"""CLO835 Week 10 lab v3 - PersistentVolumes, StorageClasses and StatefulSets,
in ONE workshop.

v3 fixes the lab defects of report 2026-10-31-07: the label is "Lab Week 10", no
busybox image, the sample version is v1.35.10, the lab practises SRV records, and
the folder has 8 files, because the master holds the provisioner manifest. The
Blackboard text of v3 is a hand-written file, in the long form of the Lab04 item:
Week10/Lab_week10_Blackboard_Submission_v3.md.

v1 had 4 workshops and 17 steps. The limit is now the size of the Week 03 and
Week 04 labs: at most Step 0 to Step 6. v2 keeps the line of the lecture
(Week10/Lecture_week10_v8.pptx): a static PersistentVolume and a claim,
data that outlives the Pod, a StorageClass that provisions volumes, and a
StatefulSet whose pets keep their names, their data and their DNS names.
master-init.sh.tftpl writes the local-path manifest to the master.

Outputs: Week10/Lab_week10_v3.pptx, Week10/localMachine_v3.sh,
~/Documents/c/r/CLO835_Fall_2026/Week10/
Run from the project root. It is guarded, so importing it writes nothing.
"""
import os
import subprocess
import sys

import lab_kubeadm as L

F = L.FILE_MARK
SC_FILE = "local-path-storage.yaml"
PROXY = "localhost:8001/api/v1/namespaces/default/pods"

PV_PVC = """apiVersion: v1
kind: PersistentVolume
metadata:
  name: data-pv
spec:
  capacity: {storage: 1Gi}
  accessModes: [ReadWriteOnce]
  persistentVolumeReclaimPolicy: Retain
  storageClassName: ""
  hostPath: {path: /tmp/data-pv, type: DirectoryOrCreate}
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values: [workernode1]
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-pvc
spec:
  accessModes: [ReadWriteOnce]
  storageClassName: ""
  resources: {requests: {storage: 1Gi}}""".split("\n")

POD_PVC = """apiVersion: v1
kind: Pod
metadata:
  name: writer
spec:
  containers:
  - name: shell
    image: maziar/alpine-curl
    command: ["sleep", "3600"]
    volumeMounts:
    - name: data
      mountPath: /data
  volumes:
  - name: data
    persistentVolumeClaim:
      claimName: data-pvc""".split("\n")

STS = """apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: kubia
spec:
  serviceName: kubia
  replicas: 2
  selector:
    matchLabels: {app: kubia}
  template:
    metadata:
      labels: {app: kubia}
    spec:
      containers:
      - name: kubia
        image: maziar/kubia-pet
        ports:
        - {name: http, containerPort: 8080}
        volumeMounts:
        - {name: data, mountPath: /var/data}
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: [ReadWriteOnce]
      resources: {requests: {storage: 1Mi}}""".split("\n")

SLIDES = [
 ("title", "Workshop 1 – Persistent Storage and StatefulSets"),
 ("prereq",),
 ("cluster",),
 ("step2", "A PersistentVolume and a claim", "bash", [
  "# The administrator makes the PV: a folder of",
  "# workernode1. The user claims it with a PVC.",
  "$ cat > pv-pvc.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f pv-pvc.yaml",
  " ",
  "# The claim finds the PV: both become Bound.",
  "$ kubectl wait --for=jsonpath='{.status.phase}'=Bound pvc/data-pvc --timeout=60s",
  "$ kubectl get pv,pvc",
  " ",
  "# Retain: when the claim goes, the PV and its",
  "# data stay for the administrator.",
  ], "pv-pvc.yaml", "pv-pvc.yaml", PV_PVC),
 ("step2", "The data outlives the Pod", "bash", [
  "# The Pod names the claim, not the storage.",
  "$ cat > writer.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f writer.yaml",
  "$ kubectl wait --for=condition=Ready pod/writer --timeout=120s",
  "$ kubectl get pod writer -o wide     # on workernode1",
  "$ kubectl exec writer -- sh -c 'date > /data/note.txt'",
  " ",
  "# Delete the Pod. A new Pod gets the same data.",
  "$ kubectl delete pod writer --now",
  "$ kubectl apply -f writer.yaml",
  "$ kubectl wait --for=condition=Ready pod/writer --timeout=120s",
  "$ kubectl exec writer -- cat /data/note.txt",
  ], "writer.yaml", "writer.yaml", POD_PVC),
 ("step", "A StorageClass provisions the volumes", "bash", [
  "# On EKS, the EBS CSI driver makes a disk for each claim. Here the local-path",
  "# provisioner makes a folder on a node. The master holds its manifest.",
  "$ kubectl apply -f " + SC_FILE,
  "$ kubectl -n local-path-storage rollout status deployment/local-path-provisioner",
  " ",
  "# One StorageClass, the default. A claim with no class gets it.",
  "$ kubectl get storageclass",
  "# NAME                 PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE",
  "# standard (default)   rancher.io/local-path   Delete          WaitForFirstConsumer",
  " ",
  "# WaitForFirstConsumer: the PV is made only when a Pod uses the claim.",
  ]),
 ("step2", "A StatefulSet and its headless Service", "bash", [
  "# The headless Service (no ClusterIP) names the pets.",
  "$ kubectl create service clusterip kubia --clusterip=None --tcp=80:8080",
  " ",
  "# Each pet gets a claim from the template, and the",
  "# StorageClass makes a PV for each claim.",
  "$ cat > kubia-statefulset.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f kubia-statefulset.yaml",
  " ",
  "# kubia-0 first, then kubia-1. Each has its own PV.",
  "$ kubectl rollout status statefulset/kubia --timeout=300s",
  "$ kubectl get pods -l app=kubia -o wide",
  "$ kubectl get pvc,pv",
  ], "kubia-statefulset.yaml", "kubia-statefulset.yaml", STS),
 ("step", "A pet keeps its name, its data and its DNS name", "bash", [
  "# kubectl proxy listens on 8001 and adds your credentials to each request.",
  "$ kubectl proxy --port=8001 >/dev/null 2>&1 &",
  "$ sleep 2; curl -s -X POST -d 'Hello kubia-0' " + PROXY + "/kubia-0/proxy/",
  "$ curl -s " + PROXY + "/kubia-0/proxy/",
  " ",
  "# Delete kubia-0. The StatefulSet makes a new kubia-0 with the same claim.",
  "$ kubectl delete pod kubia-0",
  "$ sleep 5; kubectl wait --for=condition=Ready pod/kubia-0 --timeout=180s",
  "$ curl -s " + PROXY + "/kubia-0/proxy/          # the same data",
  " ",
  "# The headless Service gives each pet a stable DNS name. The IP address can change.",
  "$ kubectl run dnstest --image=maziar/alpine-curl --restart=Never --command -- sleep 3600",
  "$ kubectl wait --for=condition=Ready pod/dnstest --timeout=120s",
  "$ kubectl exec dnstest -- nslookup kubia-0.kubia.default.svc.cluster.local",
  " ",
  "# The name of the Service returns all the pets. SRV records name each one: peers use them.",
  "$ kubectl exec dnstest -- nslookup kubia.default.svc.cluster.local",
  "$ kubectl exec dnstest -- nslookup -type=SRV kubia.default.svc.cluster.local",
  ]),
 ("step", "Clean up", "bash", [
  "# ON THE MASTER - stop the proxy and remove the Kubernetes objects.",
  "$ bash cleanup_lab10.sh",
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
# CLO835 - Week 10 - PersistentVolumes, StorageClasses and StatefulSets.
# Run these ON THE MASTER NODE, section by section. Do NOT run the whole file.
#
# Terraform builds 3 machines: 1 control plane and 2 workers. The cluster forms
# itself at boot, the same way it did in Weeks 04 to 09.
#
# Each step matches one slide of Lab_week10_v3.pptx.
"""

CLEANUP = """pkill -f "kubectl proxy" 2>/dev/null
kubectl delete pod writer dnstest --now 2>/dev/null
kubectl delete statefulset kubia 2>/dev/null
kubectl delete service kubia 2>/dev/null
kubectl delete pvc data-pvc data-kubia-0 data-kubia-1 2>/dev/null
kubectl delete pv data-pv 2>/dev/null
# The provisioner deletes the PVs of the pets. Wait for that, then remove the provisioner.
for i in $(seq 30); do [ -z "$(kubectl get pv -o name)" ] && break; sleep 2; done
kubectl delete storageclass standard 2>/dev/null
kubectl delete namespace local-path-storage 2>/dev/null
kubectl delete clusterrolebinding local-path-provisioner-bind 2>/dev/null
kubectl delete clusterrole local-path-provisioner-role 2>/dev/null
rm -f ./pv-pvc.yaml ./writer.yaml ./kubia-statefulset.yaml

kubectl get pods,pvc,pv"""


def sc_manifest():
    """The manifest of Week 07, with a helper image of the course account."""
    text = subprocess.check_output(["git", "-C", L.REPO, "show", "HEAD:Week07/" + SC_FILE]).decode("utf8")
    old = "image: docker.io/library/busybox"
    if text.count(old) != 1:
        raise SystemExit("the manifest changed")
    return text.replace(old, "image: docker.io/maziar/alpine-curl")


def master_extra():
    return ("# Step 3 of localMachine.sh applies this file.\n"
            "cat > /home/ubuntu/%s <<'MANIFEST'\n%sMANIFEST\n"
            "chown ubuntu:ubuntu /home/ubuntu/%s\n") % (SC_FILE, sc_manifest(), SC_FILE)


if __name__ == "__main__":
    L.check_lines(SLIDES)
    L.make_lab("10", SLIDES, "Week10/Lab_week10_v3.pptx", SCRIPT_HEAD, script_path="Week10/localMachine_v3.sh",
               prereq_title="Lab Week 10 - Prerequisites", node_version="v1.35.10")
    if "--no-repo" not in sys.argv:
        dst, files = L.make_repo_folder("10", "PersistentVolumes, StorageClasses and StatefulSets", CLEANUP,
                                        "Week10/localMachine_v3.sh", master_extra=master_extra(),
                                        lab_label="Lab Week 10")
        old_file = os.path.join(dst, SC_FILE)
        if os.path.exists(old_file):
            os.remove(old_file)
        print("repo folder : %s (%d files)" % (dst, len(files)))
