# -*- coding: utf-8 -*-
"""CLO835 Week 10 lab v4 - PersistentVolumes, StorageClasses and StatefulSets,
in ONE workshop.

v4 makes the lab agree with the lecture Week10/Lecture_week10_v10.pptx (2026-11-10):
- Step 1 runs kubectl describe pvc data-pvc, as the lecture shows for Step 1.
- Step 2 deletes the claim, and the PV data-pv becomes Released (Retain).
- Step 4 shows the Pods, the claims and the PVs in one table: Retain against Delete.
- Step 5 deletes the Pod dnstest, as the lecture shows for Step 5. The first read
  after the POST goes, because the POST answer shows the write.
- "Pod" replaces "pet", "directory" replaces "folder", "creates" replaces "makes",
  and no title holds the word "keeps", as in the lecture.
- The deck has a title and an author, and no blank thumbnail.
- The Blackboard text v4 is written by this builder, in the long form of Lab04.
The provisioner manifest stays the same as in v3. The cleanup script changes one comment.
Review fixes: comments on the early FailedBinding event, on CLAIM of a Released PV, and on
serviceName, which gives the DNS names.

v3 notes: the label is "Lab Week 10", maziar/alpine-curl replaces busybox, the lab
practises SRV records, and the master holds the provisioner manifest.

Outputs: Week10/Lab_week10_v4.pptx, Week10/localMachine_v4.sh,
Week10/Lab_week10_Blackboard_Submission_v4.md, ~/Documents/c/r/CLO835_Fall_2026/Week10/
Run from the project root. It is guarded, so importing it writes nothing.
It refuses to overwrite an output, unless you give --force.
"""
import os
import subprocess
import sys

from pptx import Presentation

import lab_kubeadm as L
from build_week12_lecture_v6 import finish

VERSION = "v4"
DECK = "Week10/Lab_week10_%s.pptx" % VERSION
SCRIPT = "Week10/localMachine_%s.sh" % VERSION
BLACKBOARD = "Week10/Lab_week10_Blackboard_Submission_%s.md" % VERSION
NODE_VERSION = "v1.35.10"

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
  "# The administrator creates the PV: a directory of",
  "# workernode1. The user asks for it with a PVC.",
  "$ cat > pv-pvc.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f pv-pvc.yaml",
  " ",
  "# The claim finds the PV: both become Bound.",
  "$ kubectl wait --for=jsonpath='{.status.phase}'=Bound pvc/data-pvc --timeout=60s",
  "$ kubectl get pv,pvc",
  " ",
  "# The Events at the end tell why a claim is Pending.",
  "$ kubectl describe pvc data-pvc",
  "# The Events can show an early FailedBinding event.",
  "# The Status field gives the result: Bound.",
  ], "pv-pvc.yaml", "pv-pvc.yaml", PV_PVC),
 ("step2", "The data stays after the Pod and the claim", "bash", [
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
  " ",
  "# Retain: delete the Pod and the claim.",
  "# The PV and its data stay.",
  "$ kubectl delete pod writer --now",
  "$ kubectl delete pvc data-pvc",
  "$ kubectl get pv data-pv       # STATUS Released",
  "# CLAIM still names data-pvc, so no new",
  "# claim can bind to data-pv.",
  ], "writer.yaml", "writer.yaml", POD_PVC),
 ("step", "A StorageClass provisions the volumes", "bash", [
  "# On EKS, the EBS CSI driver creates an EBS volume for each claim. Here the local-path",
  "# provisioner creates a directory on a node. The master holds its manifest.",
  "$ kubectl apply -f " + SC_FILE,
  "$ kubectl -n local-path-storage rollout status deployment/local-path-provisioner",
  " ",
  "# One StorageClass, the default. A claim with no class gets it.",
  "$ kubectl get storageclass",
  "# NAME                 PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE",
  "# standard (default)   rancher.io/local-path   Delete          WaitForFirstConsumer",
  " ",
  "# WaitForFirstConsumer: the provisioner creates the PV only when a Pod uses the claim.",
  ]),
 ("step2", "A StatefulSet and its headless Service", "bash", [
  "# Create a headless Service (clusterIP: None). With",
  "# serviceName in the StatefulSet, the Service gives",
  "# each Pod a DNS name.",
  "$ kubectl create service clusterip kubia --clusterip=None --tcp=80:8080",
  " ",
  "# Each Pod gets a claim from the template, and",
  "# the StorageClass creates a PV for each claim.",
  "$ cat > kubia-statefulset.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f kubia-statefulset.yaml",
  " ",
  "# kubia-0 first, then kubia-1. Each has its own claim.",
  "$ kubectl rollout status statefulset/kubia --timeout=300s",
  "$ kubectl get pods,pvc,pv -o wide",
  "# data-pv: Retain, Released. The new PVs: Delete, Bound.",
  ], "kubia-statefulset.yaml", "kubia-statefulset.yaml", STS),
 ("step", "The identity of a Pod and its DNS names", "bash", [
  "# kubectl proxy listens on 8001 and adds your credentials to each request.",
  "$ kubectl proxy --port=8001 >/dev/null 2>&1 &",
  "$ sleep 2; curl -s -X POST -d 'Hello kubia-0' " + PROXY + "/kubia-0/proxy/",
  " ",
  "# Delete kubia-0. The StatefulSet creates a new kubia-0 with the same claim.",
  "$ kubectl delete pod kubia-0",
  "$ sleep 5; kubectl wait --for=condition=Ready pod/kubia-0 --timeout=180s",
  "$ curl -s " + PROXY + "/kubia-0/proxy/          # the same data",
  " ",
  "# The headless Service gives each Pod a stable DNS name. The IP address can change.",
  "$ kubectl run dnstest --image=maziar/alpine-curl --restart=Never --command -- sleep 3600",
  "$ kubectl wait --for=condition=Ready pod/dnstest --timeout=120s",
  "$ kubectl exec dnstest -- nslookup kubia-0.kubia.default.svc.cluster.local",
  " ",
  "# The name of the Service returns all the Pods. Each SRV record names one Pod.",
  "$ kubectl exec dnstest -- nslookup kubia.default.svc.cluster.local",
  "$ kubectl exec dnstest -- nslookup -type=SRV kubia.default.svc.cluster.local",
  "$ kubectl delete pod dnstest",
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
# Each step matches one slide of Lab_week10_v4.pptx.
"""

# The cleanup of v3, with one comment changed: "StatefulSet Pods" replaces "pets".
CLEANUP = """pkill -f "kubectl proxy" 2>/dev/null
kubectl delete pod writer dnstest --now 2>/dev/null
kubectl delete statefulset kubia 2>/dev/null
kubectl delete service kubia 2>/dev/null
kubectl delete pvc data-pvc data-kubia-0 data-kubia-1 2>/dev/null
kubectl delete pv data-pv 2>/dev/null
# The provisioner deletes the PVs of the StatefulSet Pods. Wait for that, then remove the provisioner.
for i in $(seq 30); do [ -z "$(kubectl get pv -o name)" ] && break; sleep 2; done
kubectl delete storageclass standard 2>/dev/null
kubectl delete namespace local-path-storage 2>/dev/null
kubectl delete clusterrolebinding local-path-provisioner-bind 2>/dev/null
kubectl delete clusterrole local-path-provisioner-role 2>/dev/null
rm -f ./pv-pvc.yaml ./writer.yaml ./kubia-statefulset.yaml

kubectl get pods,pvc,pv"""

BLACKBOARD_TEXT = """# Lab Week 10: Persistent Storage and StatefulSets

## Submission Instructions

Submit a report demonstrating your completion and understanding of all 7 sections of Lab Week 10.

The lab recording demonstrates the steps required to complete this assignment. You may follow the recording step by step. However, your submission must include your own screenshots, actual command outputs, and explanations for all required tasks.

## 1. Build the Cluster and Verify Its Status

The Week 10 Terraform configuration creates three Ubuntu 26.04 EC2 instances, as in Weeks 04 to 09: one control-plane node and two worker nodes. The Kubernetes cluster initializes automatically at boot.

You must:

- Run terraform init and terraform apply.
- Run terraform output public_ips and terraform output private_ips, and show the addresses of all three nodes.
- Show an SSH session connected to the control-plane node.
- Run kubectl get nodes -o wide and show all three nodes in the Ready state.
- Run kubectl get pods -n kube-system and show the control-plane pods in the Running state.
- Explain why this cluster has no StorageClass at the start of the lab.

## 2. Create a PersistentVolume and a Claim

An administrator creates a PersistentVolume. A user asks for storage with a PersistentVolumeClaim. Use localMachine.sh to create both from a manifest.

You must:

- Create pv-pvc.yaml and display its contents.
- Apply the manifest using kubectl apply -f pv-pvc.yaml.
- Run the kubectl wait command for the data-pvc claim.
- Run kubectl get pv,pvc and show that both are Bound.
- Run kubectl describe pvc data-pvc and show the Status, the Volume and the Events of the claim.
- Explain why the claim data-pvc binds to data-pv and not to a new volume.
- Explain what the nodeAffinity block does in this PersistentVolume.

## 3. Show That the Data Stays after the Pod and the Claim

A Pod names the claim, not the storage. The data stays when you delete the Pod. With the Retain policy, the PersistentVolume and its data also stay when you delete the claim.

You must:

- Create writer.yaml and display its contents.
- Apply the manifest and wait until the writer Pod is Ready.
- Run kubectl get pod writer -o wide and identify the node.
- Write the date to /data/note.txt in the writer Pod.
- Delete the writer Pod, then create it again.
- Run kubectl exec writer -- cat /data/note.txt and show the same data.
- Delete the writer Pod and the claim data-pvc.
- Run kubectl get pv data-pv and show the STATUS Released.
- Explain why the new Pod reads the same data.
- Explain what the Retain reclaim policy does, and why no new claim can bind to a Released PersistentVolume.

## 4. Provision Volumes with a StorageClass

A StorageClass and its provisioner create a volume for each claim. The control-plane node already holds the provisioner manifest.

You must:

- Run kubectl apply -f local-path-storage.yaml.
- Run the kubectl rollout status command for the local-path-provisioner Deployment.
- Run kubectl get storageclass and show the default StorageClass.
- Explain what WaitForFirstConsumer means.
- Explain what the EBS CSI driver does on EKS, and what the local-path provisioner does on this cluster.

## 5. Create a StatefulSet and Its Headless Service

A StatefulSet gives each Pod a stable identity. A headless Service has no cluster IP address.

You must:

- Create the headless Service using the kubectl create service clusterip command.
- Create kubia-statefulset.yaml and display its contents.
- Apply the manifest using kubectl apply -f kubia-statefulset.yaml.
- Run kubectl rollout status statefulset/kubia and show that the rollout completes.
- Run kubectl get pods,pvc,pv -o wide.
- Identify the claim and the PersistentVolume of each Pod, and the reclaim policy of each PersistentVolume.
- Explain why kubia-0 starts before kubia-1.
- Explain what volumeClaimTemplates does.

## 6. Show the Identity of a Pod and Discover Its Peers

A Pod of a StatefulSet gets the same name, the same claim and the same DNS name when Kubernetes creates it again. A clustered application finds its peers through DNS.

You must:

- Start kubectl proxy, write data to kubia-0 with the POST command, and show the answer.
- Delete the kubia-0 Pod and wait until the new kubia-0 is Ready.
- Read the data of kubia-0 with the curl command and show that it is the data that you wrote.
- Create the dnstest Pod and wait until it is Ready.
- Run the nslookup command for kubia-0.kubia.default.svc.cluster.local and show the result.
- Run the nslookup command for kubia.default.svc.cluster.local and show the addresses of both Pods.
- Run nslookup -type=SRV for kubia.default.svc.cluster.local and show the result.
- Delete the dnstest Pod.
- Explain what the new kubia-0 gets again, and what can change.
- Explain why a Deployment cannot give this identity to its Pods.
- Explain what the name of a headless Service returns, and how an application uses SRV records to find its peers.

## 7. Clean Up and Destroy the Cluster

At the end of the lab, remove the Kubernetes objects and destroy all three EC2 instances.

You must:

- Run bash cleanup_lab10.sh on the control-plane node.
- Run kubectl get pods,pvc,pv and show that nothing is left.
- From the Week 10 directory on your own machine, run terraform destroy.
- Include the final Terraform output showing Destroy complete!.
- State the number of resources Terraform removed.
- Explain why the clean-up deletes the claims before it deletes the provisioner.

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
    """The manifest of Week 07, with a helper image of the course account."""
    text = subprocess.check_output(["git", "-C", L.REPO, "show", "HEAD:Week07/" + SC_FILE]).decode("utf8")
    new = "image: docker.io/maziar/alpine-curl"
    old = "image: docker.io/library/busybox"
    if text.count(old) == 1:
        return text.replace(old, new)
    if text.count(new) == 1:                     # HEAD already holds the Week 07 v3 manifest
        return text
    raise SystemExit("the manifest changed")


def master_extra():
    return ("# Step 3 of localMachine.sh applies this file.\n"
            "cat > /home/ubuntu/%s <<'MANIFEST'\n%sMANIFEST\n"
            "chown ubuntu:ubuntu /home/ubuntu/%s\n") % (SC_FILE, sc_manifest(), SC_FILE)


if __name__ == "__main__":
    for out in (DECK, SCRIPT, BLACKBOARD):
        if os.path.exists(out) and "--force" not in sys.argv:
            sys.exit("%s exists. Bump the version; never overwrite a delivered file." % out)
    L.check_lines(SLIDES)
    L.make_lab("10", SLIDES, DECK, SCRIPT_HEAD, script_path=SCRIPT,
               prereq_title="Lab Week 10 - Prerequisites", node_version=NODE_VERSION)
    deck = Presentation(DECK)
    finish(deck, "CLO835 Week 10 Lab: Persistent Storage and StatefulSets")
    for slide in deck.slides:                   # one word for one meaning: Kubernetes, not K8s
        for sh in slide.shapes:
            if sh.has_text_frame:
                for p in sh.text_frame.paragraphs:
                    for r in p.runs:
                        r.text = r.text.replace("K8s", "Kubernetes")
    deck.save(DECK)
    if "--no-repo" not in sys.argv:
        dst, files = L.make_repo_folder("10", "PersistentVolumes, StorageClasses and StatefulSets", CLEANUP,
                                        SCRIPT, master_extra=master_extra(), lab_label="Lab Week 10")
        old_file = os.path.join(dst, SC_FILE)
        if os.path.exists(old_file):
            os.remove(old_file)
        print("repo folder : %s (%d files)" % (dst, len(files)))
    open(BLACKBOARD, "w", encoding="utf8").write(BLACKBOARD_TEXT)
    print("blackboard  : %s" % BLACKBOARD)
