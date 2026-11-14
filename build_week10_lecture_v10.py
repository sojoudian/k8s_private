# -*- coding: utf-8 -*-
"""CLO835 Week 10 lecture v10 - PV, PVC, StorageClass and StatefulSets.

Fixes the 49 defects and adds the 22 additions of
reports/report-2026-11-09-02-week07-week10-lecture-audit.md (tables 3 and 4).
v9 stays on disk. One builder now makes the whole deck (v9 needed two scripts), with the slide
kit of build_week07_lecture_v7.py, so both lectures have one design and one Course Outline.
The main changes:
- The examples use the course cluster, as the lab does: the hostPath PV data-pv with
  nodeAffinity, the claim data-pvc, the writer Pod, and the StorageClass standard of the
  local-path provisioner. Amazon EBS stays as one "On Amazon EKS" card.
- A StatefulSet updates and scales down from the highest ordinal. MySQL uses source and replica.
- New slides: access modes, PV phases and reclaim policies, storage on the course cluster,
  a Pending claim, the StatefulSet manifest, updates and ordinals, optional topics,
  takeaways, and the map of the lab steps.

Input : Week12/Lecture_week12_v6.pptx, for the cover and the outline (read, never written)
Output: Week10/Lecture_week10_v10.pptx (the build refuses to overwrite it)

Run from the project root. It is guarded, so importing it writes nothing.
    .venv/bin/python build_week10_lecture_v10.py
"""
import os
import sys

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

import build_week08 as E
from build_week07_lecture_v7 import (BLUE, DOWN, LEFT, RIGHT, SLATE, STEPS, TOP, UP, agenda, arrow, box, bullets,
                                     card, cards, caution, cover, grid, keep_first, label, new_slide, number_and_save,
                                     outline, rich, term, text_slide, zone)

VERSION = "v10"
SRC = "Week12/Lecture_week12_v6.pptx"
OUT = "Week10/Lecture_week10_%s.pptx" % VERSION
TWO_WAY_H, TWO_WAY_V = MSO_SHAPE.LEFT_RIGHT_ARROW, MSO_SHAPE.UP_DOWN_ARROW

TEST_PD = """apiVersion: v1
kind: Pod
metadata:
  name: test-pd
spec:
  containers:
  - image: maziar/kubia:v1
    name: test-container
    volumeMounts:
    - mountPath: /test-pd
      name: test-volume
  volumes:
  - name: test-volume
    hostPath:
      # directory location on host
      path: /data
      # this field is optional
      type: DirectoryOrCreate""".split("\n")

# Lab Week 10, Step 1 (pv-pvc.yaml): the PV part, then the claim part.
DATA_PV = """apiVersion: v1
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
          values: [workernode1]""".split("\n")

DATA_PVC = """apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-pvc
spec:
  accessModes: [ReadWriteOnce]
  storageClassName: ""
  resources: {requests: {storage: 1Gi}}""".split("\n")

# Lab Week 10, Step 2.
WRITER = """apiVersion: v1
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

BIND = """$ kubectl apply -f pv-pvc.yaml

# The claim finds the PV: both become Bound.
$ kubectl wait --for=jsonpath='{.status.phase}'=Bound pvc/data-pvc --timeout=60s
$ kubectl get pv,pvc

# The Events at the end tell why a claim is Pending.
$ kubectl describe pvc data-pvc""".split("\n")

# The StorageClass of local-path-storage.yaml (Lab Week 10, Step 3).
STANDARD = """apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: standard
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"
provisioner: rancher.io/local-path
volumeBindingMode: WaitForFirstConsumer
reclaimPolicy: Delete""".split("\n")

STEP3 = """$ kubectl apply -f local-path-storage.yaml
$ kubectl -n local-path-storage rollout status deployment/local-path-provisioner
$ kubectl get storageclass
# NAME                 PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE
# standard (default)   rancher.io/local-path   Delete          WaitForFirstConsumer""".split("\n")

# Lab Week 10, Step 4 (kubia-statefulset.yaml), in two halves of 13 lines.
STATEFULSET = """apiVersion: apps/v1
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

SRV = """# Lab Week 10, Step 4 created the headless Service kubia and the StatefulSet kubia.
$ kubectl run dnstest --image=maziar/alpine-curl --restart=Never --command -- sleep 3600
$ kubectl wait --for=condition=Ready pod/dnstest --timeout=120s
$ kubectl exec dnstest -- nslookup -type=SRV kubia.default.svc.cluster.local
$ kubectl delete pod dnstest""".split("\n")


def divider(prs, kicker, text, subtitle):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    E.divider(s, kicker, text, subtitle)
    return s


def caption(s, y, text):
    rich(s, 0.70, y, 11.95, 0.42, text, size=14, color=E.MUTED, align=PP_ALIGN.CENTER)


# ---------------------------------------------------------------- Part 1: hostPath

def s_part1(prs):
    return divider(prs, "Part 1", "hostPath Volumes", "Data on one node")


def s_hostpath(prs):
    return text_slide(prs, "Volumes: hostPath", [
        (0, "A `hostPath` volume mounts a file or a directory of the node into the Pod"),
        (0, "The data stays when you delete the Pod. It stays on that node only: a Pod on another node does not see it"),
        (0, "If the node fails, or the Pod moves to another node, the Pod loses the data"),
        (0, "Pods use `hostPath` to read node data, for example `/var/log`, a kubeconfig file or a device"),
        (0, "Use `hostPath` as persistent storage only for tests on a single node. Do not store application data in it"),
        (0, "How can a Pod get the same data on any node of a cluster? Part 2 answers this"),
        (0, "Lab Week 07, Step 4 practises `hostPath`")], size=17, after=9)


def s_concerns(prs):
    s = text_slide(prs, "hostPath Concerns", [
        (0, "A `hostPath` volume can expose privileged system credentials"),
        (0, "Pods with the same configuration can behave differently on different nodes, because the files on the nodes "
            "differ"),
        (0, "Some files and directories on the node are accessible only by root"),
        (0, "Kubernetes does not count `hostPath` data as ephemeral storage of the Pod. The data can fill the disk of "
            "the node"),
        (0, "Use a `local` PersistentVolume instead of `hostPath` when you can")], size=17, after=9)
    caution(s, 0.60, 4.80, 12.10, 1.05, "Avoid `hostPath` when you can. If you must use it, mount only the necessary "
            "file or directory. Set `readOnly: true` on the mount.")
    return s


def s_sharing(prs):
    s = new_slide(prs, "hostPath: Data Sharing with the Node")
    for x, w, name, pods in ((0.8, 6.6, "Node 1", 2), (7.7, 4.8, "Node 2", 1)):
        zone(s, x, 1.6, w, 4.2, name)
        step = (w - 0.3) / pods
        for k in range(pods):
            px = x + 0.3 + k * step
            zone(s, px, 2.05, step - 0.3, 1.85, "Pod", color=STEPS[1], fill=E.CARD_BG)
            box(s, px + 0.3, 2.55, step - 0.9, 1.1, "hostPath volume", STEPS[1], size=14)
            arrow(s, DOWN, px + (step - 0.3) / 2 - 0.19, 3.95, 0.38, 0.55)
        box(s, x + 0.3, 4.55, w - 0.6, 0.95, "/some/path/on/host", SLATE, size=15)
    caption(s, 5.98, "Pods on one node share the directory. A Pod on another node sees a different directory.")
    return s


def s_example(prs):
    s = new_slide(prs, "hostPath Configuration Example")
    term(s, 0.55, 1.50, 6.30, "test-pd.yaml", TEST_PD, size=12, spacing=1.10)
    cards(s, 7.15, 1.55, 5.60, [
        ("path: /data", "The directory on the node. The container sees it at `/test-pd`.", 0.82),
        ("type: DirectoryOrCreate", "If the directory does not exist, Kubernetes makes it. With no type, Kubernetes "
                                    "does no check before the mount.", 0.98),
        ("image: maziar/kubia:v1", "Any image works. The volume does not depend on the application.", 0.82)])
    return s


def s_limits(prs):
    s = text_slide(prs, "Volumes in the Pod Specification: the Limits", [
        (0, "With a volume type directly in the Pod specification, for example `nfs` (Week 7):"),
        (1, "you create the storage outside of the Kubernetes API"),
        (1, "you put all the details of the storage in the Pod manifest"),
        (1, "the Pod manifest works on one specific cluster only"),
        (0, "Cloud disks have no in-tree driver now. The old `awsElasticBlockStore` field still exists, but Kubernetes "
            "sends it to the EBS CSI driver"),
        (0, "For a cloud disk, use a PersistentVolumeClaim, or a generic ephemeral volume")], size=17, after=8)
    card(s, 0.60, 4.85, 12.10, 1.05, "CSI (Container Storage Interface)", "A standard API between Kubernetes and a "
         "storage driver. Each vendor supplies its driver outside of the Kubernetes code, for example "
         "`ebs.csi.aws.com`. Week 7, slide 8 lists the removed in-tree types.", mono=False)
    return s


# ---------------------------------------------------------------- Part 2: PV, PVC and StorageClass

def s_part2(prs):
    return divider(prs, "Part 2", "PV, PVC and StorageClasses", "Storage that does not depend on one node")


def s_process(prs):
    s = new_slide(prs, "PersistentVolumes and PersistentVolumeClaims")
    cols = (2.4, 6.0, 9.6)
    box(s, 0.55, 1.85, 1.6, 1.65, "Administrator", SLATE, size=14)
    box(s, cols[0], 1.85, 3.15, 1.65, "1. Set up the storage: an NFS share, a disk, or a directory of a node",
        STEPS[3], size=14)
    arrow(s, RIGHT, cols[0] + 3.2, 2.5, 0.4, 0.36)
    box(s, cols[1], 1.85, 3.15, 1.65, "2. Create a PersistentVolume (PV) through the Kubernetes API", STEPS[3], size=14)
    arrow(s, DOWN, cols[1] + 1.39, 3.55, 0.38, 0.55)
    box(s, 0.55, 4.15, 1.6, 1.85, "User", SLATE, size=14)
    box(s, cols[0], 4.15, 3.15, 1.85, "3. Create a PersistentVolumeClaim (PVC)", STEPS[1], size=14)
    arrow(s, RIGHT, cols[0] + 3.2, 4.9, 0.4, 0.36)
    box(s, cols[1], 4.15, 3.15, 1.85, "4. Kubernetes binds the claim to a PV with at least the requested size, and "
        "the same access mode, volume mode and class", STEPS[5], size=13.5)
    arrow(s, RIGHT, cols[1] + 3.2, 4.9, 0.4, 0.36)
    box(s, cols[2], 4.15, 3.15, 1.85, "5. Create a Pod with a volume that names the claim", STEPS[1], size=14)
    return s


def s_access(prs):
    s = new_slide(prs, "Access Modes")
    end = grid(s, 0.60, TOP + 0.10, [2.80, 1.40, 7.90], [
        ["Access mode", "Short form", "Meaning"],
        ["`ReadWriteOnce`", "RWO", "One node mounts the volume for reading and writing. Many Pods on that node can "
                                   "use it."],
        ["`ReadOnlyMany`", "ROX", "Many nodes mount the volume for reading only."],
        ["`ReadWriteMany`", "RWX", "Many nodes mount the volume for reading and writing."],
        ["`ReadWriteOncePod`", "RWOP", "One Pod in the whole cluster mounts the volume for reading and writing "
                                       "(stable in v1.29). CSI volumes only."]], row_h=0.72, size=14)
    rich(s, 0.60, end + 0.25, 12.10, 0.80, [
        "A volume type supports only some access modes. A `hostPath` PV supports `ReadWriteOnce` only.",
        "NFS supports `ReadWriteOnce`, `ReadOnlyMany` and `ReadWriteMany`."], size=14, spacing=1.12, after=4)
    return s


def s_pv(prs):
    s = new_slide(prs, "PersistentVolume Manifest")
    term(s, 0.55, 1.50, 6.40, "data-pv (pv-pvc.yaml, Lab Week 10, Step 1)", DATA_PV, size=12, spacing=1.10)
    cards(s, 7.20, 1.55, 5.55, [
        ("persistentVolumeReclaimPolicy: Retain", "When you delete the claim, the PV becomes Released. Its data stays "
                                                  "until an administrator deletes or reuses it.", 1.18),
        ("storageClassName: \"\"", "This PV has no StorageClass. It binds to a claim that asks for no class, for "
                                   "example a claim with `storageClassName: \"\"`.", 0.98),
        ("hostPath:", "The storage is a directory of workernode1. A `local` PV, a disk of the node, is the production "
                      "form.", 0.98),
        ("nodeAffinity:", "Kubernetes runs each Pod that uses this PV on workernode1, because the data is there.",
         0.98)])
    return s


def s_phases(prs):
    s = new_slide(prs, "PV Phases and Reclaim Policies")
    grid(s, 0.60, TOP + 0.10, [1.70, 4.25], [
        ["Phase", "Meaning"],
        ["`Available`", "The PV is free. No claim is bound to it."],
        ["`Bound`", "The PV is bound to a claim."],
        ["`Released`", "Someone deleted the claim. The data stays, but no new claim can bind to the PV."],
        ["`Failed`", "The automatic reclaim of the PV failed."]], row_h=0.92, size=14)
    grid(s, 6.75, TOP + 0.10, [1.55, 4.45], [
        ["Policy", "When you delete the claim"],
        ["`Retain`", "The PV and its data stay. An administrator cleans up. This is the default for a static PV."],
        ["`Delete`", "Kubernetes deletes the PV and the storage. This is the default for a dynamic PV."],
        ["`Recycle`", "Deprecated. Use dynamic provisioning."]], row_h=1.22, size=14)
    return s


def s_decoupling(prs):
    s = new_slide(prs, "Decoupling Pods from the Storage Technology")
    zone(s, 0.8, 1.5, 11.7, 1.2, "PersistentVolumes: cluster level, no namespace", color=STEPS[4], fill=E.CARD_BG)
    for k in range(6):
        box(s, 1.0 + k * 1.92, 1.92, 1.6, 0.62, "PV", STEPS[3], size=14)
    for x, ns, user in ((0.8, "Namespace A", "User A"), (6.8, "Namespace B", "User B")):
        zone(s, x, 3.15, 5.7, 1.95, ns, color=BLUE)
        box(s, x + 0.2, 3.72, 1.35, 1.1, user, SLATE, size=14)
        arrow(s, RIGHT, x + 1.6, 4.09, 0.36, 0.34)
        box(s, x + 2.0, 3.72, 1.45, 1.1, "PVC", STEPS[3], size=14)
        arrow(s, RIGHT, x + 3.5, 4.09, 0.36, 0.34)
        box(s, x + 3.9, 3.72, 1.6, 1.1, "Pods", STEPS[1], size=14)
        arrow(s, UP, x + 2.54, 2.72, 0.36, 0.41)
        arrow(s, DOWN, x + 4.52, 5.12, 0.36, 0.38)
    zone(s, 0.8, 5.52, 11.7, 1.15, "Nodes: cluster level, no namespace", color=STEPS[4], fill=E.CARD_BG)
    for k in range(6):
        box(s, 1.0 + k * 1.92, 5.94, 1.6, 0.62, "Node", SLATE, size=14)
    return s


def s_binds(prs):
    s = new_slide(prs, "How a Claim Binds to a PV")
    bullets(s, 0.60, 1.62, 12.10, [
        (0, "An application asks for storage with a claim: directly, or through a volume claim template of a "
            "StatefulSet"),
        (0, "The claim is Pending at first. Kubernetes looks for a matching PV. If there is none, the provisioner of "
            "the StorageClass can create one"),
        (0, "When Kubernetes finds a matching PV, the claim becomes Bound. While the claim is Pending, a Pod that uses "
            "it cannot start"),
        (0, "With `volumeBindingMode: WaitForFirstConsumer`, the claim stays Pending until a Pod uses it. This is "
            "normal")], size=16, after=7, h=2.30)
    term(s, 0.60, 4.00, 12.10, "Lab Week 10, Step 1", BIND, size=11, spacing=1.08)
    return s


def s_claim_pod(prs):
    s = new_slide(prs, "A Claim and a Pod That Uses It")
    end = term(s, 0.55, 1.50, 6.05, "data-pvc (pv-pvc.yaml, Lab Week 10, Step 1)", DATA_PVC, size=12, spacing=1.10)
    cards(s, 0.55, end + 0.15, 6.05, [
        ("storageClassName: \"\"", "The claim asks for a PV with no class, so Kubernetes binds it to `data-pv`. No "
                                   "provisioner creates a volume.", 0.98),
        ("claimName: data-pvc", "The name of the claim. Step 2 deletes this Pod and creates it again.", 0.80)])
    end = term(s, 6.85, 1.50, 5.90, "writer.yaml (Lab Week 10, Step 2)", WRITER, size=12, spacing=1.10)
    rich(s, 6.85, end + 0.15, 5.90, 0.70, "Step 2 writes `/data/note.txt`, deletes the Pod and creates it again. "
         "The new Pod reads the same file.", size=13)
    return s


def s_benefits(prs):
    s = new_slide(prs, "Benefits of PersistentVolumes and Claims")
    cols = (2.7, 5.25, 7.8, 10.35)
    box(s, 0.55, 1.75, 1.85, 1.5, "Direct volume", SLATE, size=14)
    box(s, cols[0], 1.75, 2.1, 1.5, "Pod\n(nfs volume)", STEPS[1], size=14)
    label(s, cols[0] + 2.15, 1.95, 5.45, 0.36, "The Pod names the storage", size=13)
    arrow(s, RIGHT, cols[0] + 2.15, 2.35, 5.45, 0.36)
    box(s, cols[3], 1.75, 2.1, 1.5, "NFS server", STEPS[5], size=14)
    box(s, 0.55, 3.95, 1.85, 1.5, "With a claim", SLATE, size=14)
    box(s, cols[0], 3.95, 2.1, 1.5, "Pod\n(claimName)", STEPS[1], size=14)
    arrow(s, RIGHT, cols[0] + 2.12, 4.53, 0.41, 0.36)
    box(s, cols[1], 3.95, 2.1, 1.5, "PVC\ndata-pvc", STEPS[3], size=14)
    arrow(s, RIGHT, cols[1] + 2.12, 4.53, 0.41, 0.36)
    box(s, cols[2], 3.95, 2.1, 1.5, "PV\ndata-pv", STEPS[3], size=14)
    arrow(s, RIGHT, cols[2] + 2.12, 4.53, 0.41, 0.36)
    box(s, cols[3], 3.95, 2.1, 1.5, "A directory of workernode1", STEPS[5], size=14)
    caption(s, 5.75, "The Pod manifest names only the claim. It works on another cluster that has a claim with the "
                     "same name.")
    return s


def s_sc(prs):
    return text_slide(prs, "Provisioning Automation: StorageClass", [
        (0, "A cluster can have many storage systems, for example NFS and iSCSI, or Amazon EBS and Amazon EFS"),
        (0, "One storage system can have many tiers, for example the General Purpose SSD (`gp3`) and the Provisioned "
            "IOPS SSD (`io2`) volumes of Amazon EBS"),
        (0, "A StorageClass represents one storage system, or one tier of it"),
        (0, "An administrator creates the StorageClasses. A user names one in a claim"),
        (0, "Use `kubectl get storageclass` to list the StorageClasses of a cluster")], size=18, after=12)


def s_using_sc(prs):
    return text_slide(prs, "Using StorageClasses", [
        (0, "A PV and a PVC can name a StorageClass in the field `spec.storageClassName`"),
        (0, "A claim that names a StorageClass gets a matching static PV of that class, if one exists. If not, the "
            "provisioner of the class creates a PV"),
        (0, "`storageClassName: \"\"` turns off dynamic provisioning for the claim. The claim binds only to a PV with "
            "no class"),
        (0, "A claim with no `storageClassName` field gets the default StorageClass"),
        (0, "The annotation `storageclass.kubernetes.io/is-default-class: \"true\"` marks the default class"),
        (0, "A claim with no class that exists before the default class gets the default class later (retroactive "
            "default, stable in v1.28)"),
        (0, "Dynamic provisioning needs a StorageClass. Manual provisioning does not")], size=16, after=8)


def s_sc_manifest(prs):
    s = new_slide(prs, "StorageClass Manifest")
    end = term(s, 0.55, 1.50, 6.55, "standard (local-path-storage.yaml, Lab Week 10, Step 3)", STANDARD, size=12,
               spacing=1.10)
    card(s, 0.55, end + 0.20, 6.55, 1.05, "On Amazon EKS", "`provisioner: ebs.csi.aws.com` and the setting `type: gp3` "
         "give an EBS volume for each claim (Week 9).", mono=False)
    cards(s, 7.35, 1.55, 5.40, [
        ("provisioner:", "It creates the PVs of this class. The local-path provisioner makes a directory on a node.",
         0.98),
        ("volumeBindingMode:", "`Immediate` (the default) binds the claim at once. `WaitForFirstConsumer` waits for a "
                               "Pod, so the PV is on the node of the Pod.", 1.18),
        ("reclaimPolicy:", "`Delete` (the default): Kubernetes deletes the PV and the storage with the claim.", 0.98),
        ("allowVolumeExpansion:", "Not set here. With `true`, you can make a claim larger. A volume can grow, but it "
                                  "cannot shrink.", 0.98)])
    return s


def s_dynamic(prs):
    s = new_slide(prs, "Dynamic PersistentVolume Provisioning")
    cols = (0.7, 4.75, 8.8)
    rows = (1.6, 4.25)
    cells = [(0, 0, "1. The administrator installs a provisioner, if the cluster has none.", STEPS[3]),
             (1, 0, "2. The administrator creates StorageClasses, and marks one as the default.", STEPS[3]),
             (2, 0, "3. The user creates a claim that names a StorageClass, or names none.", STEPS[1]),
             (2, 1, "4. Kubernetes asks the provisioner of that class for a new PV, with the size and the access mode "
                    "of the claim.", SLATE),
             (1, 1, "5. The provisioner creates the storage and the PV. The claim becomes Bound.", SLATE),
             (0, 1, "6. The user creates a Pod that uses the claim.", STEPS[1])]
    for c, r, text, fill in cells:
        box(s, cols[c], rows[r], 3.45, 2.1, text, fill, size=14.5)
    arrow(s, RIGHT, cols[0] + 3.5, 2.47, 0.5, 0.36)
    arrow(s, RIGHT, cols[1] + 3.5, 2.47, 0.5, 0.36)
    arrow(s, DOWN, cols[2] + 1.53, 3.74, 0.38, 0.47)
    arrow(s, LEFT, cols[1] + 3.5, 5.12, 0.5, 0.36)
    arrow(s, LEFT, cols[0] + 3.5, 5.12, 0.5, 0.36)
    return s


def s_course(prs):
    s = new_slide(prs, "Storage on the Course Cluster")
    bullets(s, 0.60, 1.62, 12.10, [
        (0, "kubeadm installs no provisioner, so a new cluster has no StorageClass"),
        (0, "The lab installs the local-path provisioner. It makes a directory on a node for each claim"),
        (0, "Its StorageClass `standard` is the default, with `WaitForFirstConsumer` and `reclaimPolicy: Delete`"),
        (0, "A claim with no class gets `standard`"),
        (0, "A static `hostPath` or `local` PV needs `nodeAffinity`, so that its Pods run on the node with the data"),
        (0, "The clean-up deletes the claims before the provisioner, because the provisioner deletes the PVs and their "
            "directories"),
        (0, "On Amazon EKS (Week 9), the EBS CSI driver is the provisioner, and the storage is an EBS volume")],
        size=15, after=5, h=3.45)
    term(s, 0.60, 5.05, 12.10, "Lab Week 10, Step 3", STEP3, size=11, spacing=1.05)
    return s


def s_pending(prs):
    s = new_slide(prs, "Troubleshooting a Pending Claim")
    end = grid(s, 0.60, TOP + 0.10, [2.70, 5.00, 4.40], [
        ["Cause", "What you see", "What to do"],
        ["No StorageClass", "`kubectl get storageclass` shows none, and the claim names no class",
         "Install a provisioner, or name a class"],
        ["`WaitForFirstConsumer`", "No Pod uses the claim yet", "Nothing: this is normal. Create the Pod"],
        ["No matching PV", "The size, the access mode, the class or the selector of the PV differ",
         "Correct the claim or the PV"],
        ["No provisioner runs", "The Pod of the provisioner is not Running", "Read its Deployment and its logs"]],
        row_h=0.78, size=14)
    term(s, 0.60, end + 0.30, 12.10, "bash", ["# The Events at the end of the output tell the reason.",
                                               "$ kubectl describe pvc data-pvc"], size=12)
    return s


# ---------------------------------------------------------------- Part 3: StatefulSets

def s_part3(prs):
    return divider(prs, "Part 3", "Deploying Clustered Applications", "StatefulSets and headless Services")


def s_why(prs):
    s = new_slide(prs, "Why StatefulSets?")
    rich(s, 0.60, 1.55, 12.10, 0.45, "Some applications (databases, clustered systems) need things that a Deployment "
         "cannot give:", size=16)
    items = [("1. Stable identity", "Each Pod name has an ordinal index from 0 (`mysql-0`, `mysql-1`). A new Pod gets "
                                    "the same name. Deployment Pods get random names."),
             ("2. Stable network address", "Each Pod gets its own DNS name through a headless Service, so the source "
                                           "database is always at `mysql-0`."),
             ("3. Storage for each Pod", "Each Pod gets its own claim, and the claim stays with that Pod after a "
                                         "restart. The Pods of a Deployment share the claims of the template."),
             ("4. Ordered operations", "Kubernetes creates and scales up the Pods in order: 0, 1, 2. It scales down and "
                                       "updates them in reverse order, from the highest ordinal. A Deployment starts "
                                       "its Pods in parallel.")]
    for k, (head, body) in enumerate(items):
        card(s, 0.60 + (k % 2) * 6.15, 2.20 + (k // 2) * 2.25, 5.95, 2.05, head, body, mono=False, size=14)
    return s


def s_mysql(prs):
    s = new_slide(prs, "MySQL Replication without Kubernetes")
    rich(s, 0.55, 1.60, 6.40, 4.40, [
        "1.  Set up the source first, then the replicas",
        "2.  Clone the data from the source to replica-1",
        "3.  On replica-1, set the address of the source with `CHANGE REPLICATION SOURCE TO`. Then start "
        "replication",
        "4.  Wait until replica-1 is ready",
        "5.  Clone the data from replica-1 to replica-2",
        "6.  On replica-2, set the address of the source. Then start replication from the source"],
        size=15, spacing=1.15, after=8)
    rich(s, 0.55, 6.05, 6.40, 0.45, "Concept only: the lab does not run MySQL.", size=13, color=E.MUTED)
    box(s, 7.3, 1.75, 5.3, 1.0, "mysql-source", SLATE, size=16)
    arrow(s, DOWN, 8.29, 2.8, 0.38, 0.6)
    arrow(s, DOWN, 11.24, 2.8, 0.38, 0.6)
    label(s, 8.8, 2.9, 2.3, 0.4, "Replication", size=13)
    box(s, 7.3, 3.45, 2.35, 1.3, "mysql-replica-1", STEPS[3], size=15)
    arrow(s, RIGHT, 9.7, 3.92, 0.5, 0.36)
    label(s, 9.45, 3.5, 1.0, 0.35, "Clone", size=13)
    box(s, 10.25, 3.45, 2.35, 1.3, "mysql-replica-2", STEPS[3], size=15)
    label(s, 7.05, 4.85, 2.85, 0.40, "`SOURCE_HOST=mysql-source`", size=12)
    label(s, 10.0, 4.85, 2.85, 0.40, "`SOURCE_HOST=mysql-source`", size=12)
    rich(s, 7.3, 5.45, 5.3, 0.90, "Each replica names the source by its host name. Without Kubernetes, an "
         "administrator sets each name.", size=13, color=E.MUTED)
    return s


def s_versus(prs):
    s = new_slide(prs, "StatefulSets vs ReplicaSets")
    bullets(s, 0.60, 1.65, 6.10, [
        (0, "The Pods of a ReplicaSet are replaceable. They are the same, and any Pod can take the place of another"),
        (0, "A new Pod of a ReplicaSet gets a new name and a new IP address. It gets old data only if the template "
            "names a shared claim"),
        (0, "Each Pod of a StatefulSet has a fixed identity. A new Pod gets the same name, the same DNS name and the "
            "same claim. Its IP address can change"),
        (0, "All Pods of a StatefulSet come from one template, but each Pod has its own state")], size=16, after=9)
    for y, name, fill, pods in ((1.75, "ReplicaSet kubia-rs", SLATE, ("kubia-rs-dsfwx", "kubia-rs-fewrb",
                                                                     "kubia-rs-jwejc")),
                                (4.25, "StatefulSet kubia", STEPS[3], ("kubia-0", "kubia-1", "kubia-2"))):
        box(s, 6.95, y + 0.45, 2.15, 1.1, name, fill, size=14)
        arrow(s, RIGHT, 9.12, y + 0.82, 0.45, 0.36)
        for k, pod in enumerate(pods):
            box(s, 9.65, y + k * 0.7, 3.10, 0.6, pod, STEPS[1], size=14)
    return s


def s_headless(prs):
    s = new_slide(prs, "Headless Service")
    bullets(s, 0.60, 1.62, 6.30, [
        (0, "A normal Service sends each request to one of its Pods. The application must write to the source only"),
        (0, "A new Pod gets a new IP address. The default DNS name of a Pod holds its IP address, so it changes too:"),
        (1, "`10-40-2-8.default.pod.cluster.local`"),
        (0, "A headless Service (`clusterIP: None`) does no load balancing. Its DNS name returns the IP addresses of "
            "all its ready Pods"),
        (0, "With `serviceName` in the StatefulSet, each Pod gets a stable DNS name")], size=15, after=8, h=3.30)
    term(s, 0.55, 5.05, 6.40, "Lab Week 10, Step 4", ["# A headless Service has no cluster IP address.",
                                                      "$ kubectl create service clusterip kubia --clusterip=None "
                                                      "--tcp=80:8080"], size=11)
    box(s, 7.1, 1.7, 5.65, 0.85, "Headless Service mysql-h", SLATE, size=14.5)
    for k, (name, fill) in enumerate((("mysql-0\nsource", STEPS[3]), ("mysql-1\nreplica", STEPS[0]),
                                      ("mysql-2\nreplica", STEPS[0]))):
        x = 7.1 + k * 1.975
        arrow(s, DOWN, x + 0.68, 2.6, 0.38, 0.45)
        box(s, x, 3.1, 1.75, 1.05, name, fill, size=14)
    label(s, 7.1, 4.25, 5.65, 0.40, "`mysql-0.mysql-h.default.svc.cluster.local`", size=13)
    E.add_rounded_rect(s, 7.1 * 914400, 4.85 * 914400, 5.65 * 914400, 1.20 * 914400, E.CARD_BG, line=E.RULE_GRAY,
                       line_width=0.75, radius_ratio=0.08)
    E.add_rect(s, 7.1 * 914400, 4.90 * 914400, 0.12 * 914400, 1.10 * 914400, BLUE)
    rich(s, 7.45, 4.95, 5.20, 1.00, "`mysql-1` and `mysql-2` use `SOURCE_HOST=mysql-0.mysql-h`. The name stays when "
         "the Pod gets a new IP address.", size=13.5)
    return s


def s_manifest(prs):
    s = new_slide(prs, "The StatefulSet Manifest")
    term(s, 0.55, 1.50, 6.00, "kubia-statefulset.yaml, lines 1 to 13", STATEFULSET[:13], size=12, spacing=1.08)
    end = term(s, 6.75, 1.50, 6.00, "lines 14 to 26 (Lab Week 10, Step 4)", STATEFULSET[13:], size=12, spacing=1.08)
    for k, (key, body) in enumerate((
            ("serviceName: kubia", "The headless Service that gives each Pod its DNS name, for example `kubia-0.kubia`."),
            ("replicas: 2", "Kubernetes creates `kubia-0`, waits until it is Ready, then creates `kubia-1`."),
            ("volumeClaimTemplates:", "One claim for each Pod: `data-kubia-0` and `data-kubia-1`. They name no class, "
                                      "so `standard` creates each PV."))):
        card(s, 0.55 + k * 4.10, end + 0.20, 3.95, 6.65 - end - 0.20, key, body)
    return s


def s_volumes(prs):
    s = new_slide(prs, "Adding Volumes to StatefulSet Pods")
    bullets(s, 0.60, 1.65, 6.10, [
        (0, "The storage must be persistent and separate from the Pods"),
        (0, "Each Pod must use a different claim"),
        (0, "The StatefulSet creates the claims from `volumeClaimTemplates`. You do not create them yourself, as you "
            "do for a Deployment"),
        (0, "A claim name is the template name, the StatefulSet name and the ordinal, for example `data-kubia-0`"),
        (0, "`persistentVolumeClaimRetentionPolicy` (stable in v1.32) sets `whenDeleted` and `whenScaled`. The default "
            "for both is `Retain`: the claims stay after a delete or a scale-down")], size=15, after=8)
    zone(s, 6.95, 1.9, 1.85, 3.9, "StatefulSet kubia")
    box(s, 7.08, 2.4, 1.6, 1.4, "Pod template", STEPS[1], size=13.5)
    box(s, 7.08, 4.0, 1.6, 1.6, "Volume claim template", STEPS[3], size=13.5)
    for k in range(2):
        y = 2.40 + k * 1.60
        arrow(s, RIGHT, 8.84, y + 0.36, 0.24, 0.3)
        box(s, 9.10, y, 1.05, 1.02, "kubia-%d" % k, STEPS[1], size=12.5)
        arrow(s, RIGHT, 10.17, y + 0.36, 0.21, 0.3)
        box(s, 10.40, y, 1.45, 1.02, "data-kubia-%d" % k, STEPS[3], size=12.5)
        arrow(s, RIGHT, 11.87, y + 0.36, 0.20, 0.3)
        box(s, 12.09, y, 0.66, 1.02, "PV", STEPS[5], size=12.5)
    return s


def s_updates(prs):
    return text_slide(prs, "StatefulSet Updates and Ordinals", [
        (0, "`updateStrategy: RollingUpdate` (the default): Kubernetes updates one Pod at a time, from the highest "
            "ordinal to 0"),
        (1, "`partition: N`: only the Pods with an ordinal of N or higher get the update, for example for a canary"),
        (1, "`maxUnavailable`: more than one Pod can be unavailable during the update (beta)"),
        (0, "`updateStrategy: OnDelete`: Kubernetes updates a Pod only when you delete it"),
        (0, "`podManagementPolicy: Parallel`: when it scales, Kubernetes creates and deletes the Pods at the same "
            "time, not in order"),
        (0, "`minReadySeconds`: a new Pod must be Ready for this time before Kubernetes continues"),
        (0, "`spec.ordinals.start` (stable in v1.31): the first ordinal. With 1, the Pods are `kubia-1` and `kubia-2`"),
        (0, "The label `apps.kubernetes.io/pod-index` (stable in v1.32) holds the ordinal of each Pod"),
        (0, "The lab uses the default settings. It does not practise these settings")],
        size=16, after=8)


def s_peers(prs):
    s = new_slide(prs, "Discovering Peers in a StatefulSet")
    bullets(s, 0.60, 1.62, 12.10, [
        (0, "Each member of a clustered application must know the network identity of each other member"),
        (0, "An application should not depend on Kubernetes, so it should not query the Kubernetes API to find its "
            "peers"),
        (0, "Kubernetes creates a DNS SRV record for each named port of a headless Service. Each record names the host "
            "name of one ready Pod"),
        (0, "With `publishNotReadyAddresses: true`, the DNS records also name the Pods that are not ready"),
        (0, "An SRV name has the form `_port._protocol.service.namespace.svc.cluster.local`. The port of the lab "
            "Service has the name `80-8080`"),
        (0, "CoreDNS caches the answers for up to 30 seconds, so a new Pod can be missing from DNS for a short time")],
        size=15, after=6, h=2.35)
    term(s, 0.60, 4.05, 12.10, "Lab Week 10, Steps 4 and 5", SRV, size=11, spacing=1.05)
    return s


def s_dns(prs):
    s = new_slide(prs, "Peer Discovery through DNS")
    bullets(s, 0.60, 1.62, 12.10, [
        (0, "Each Pod stores its own data, so this is not a cluster yet"),
        (0, "A Pod can find all the Pods of the StatefulSet through DNS, and serve the data of all of them")],
        size=16, after=6, h=0.95)
    rich(s, 0.60, 2.85, 4.30, 0.80, "Concept only: the lab does not run this collection of data.", size=13,
         color=E.MUTED)
    box(s, 1.0, 4.85, 2.0, 1.05, "curl", SLATE, size=15)
    label(s, 3.05, 4.65, 2.10, 0.36, "1. `GET /`", size=13)
    arrow(s, TWO_WAY_H, 3.05, 5.19, 2.10, 0.36)
    label(s, 3.05, 5.62, 2.10, 0.62, "6. Return the collected data", size=13)
    box(s, 5.2, 2.80, 2.0, 0.65, "DNS", STEPS[5], size=14)
    arrow(s, TWO_WAY_V, 6.01, 3.50, 0.38, 0.75)
    label(s, 6.45, 3.65, 1.90, 0.40, "2. SRV lookup", size=13, align=PP_ALIGN.LEFT)
    box(s, 5.2, 4.30, 2.0, 2.30, "kubia-0\n\n3. Read its own data", STEPS[3], size=14)
    label(s, 7.25, 4.25, 2.40, 0.36, "4. `GET /data`", size=13)
    arrow(s, RIGHT, 7.25, 4.62, 2.40, 0.36)
    label(s, 7.25, 5.50, 2.40, 0.36, "5. `GET /data`", size=13)
    arrow(s, RIGHT, 7.25, 5.87, 2.40, 0.36)
    box(s, 9.7, 4.30, 2.0, 1.00, "kubia-1", STEPS[3], size=14)
    box(s, 9.7, 5.55, 2.0, 1.00, "kubia-2", STEPS[3], size=14)
    return s


def s_optional(prs):
    return text_slide(prs, "Optional Topics", [
        (0, "VolumeSnapshot (stable in v1.20): a copy of a volume at one point in time. The CSI driver must support it"),
        (0, "VolumeAttributesClass: changes the attributes of an existing volume, for example its IOPS"),
        (0, "Generic ephemeral volumes: a claim for each Pod. Kubernetes creates the claim with the Pod, and deletes it "
            "with the Pod"),
        (0, "These topics are not in the lab")], size=18, after=12)


def s_takeaways(prs):
    return text_slide(prs, "Key Takeaways", [
        (0, "`hostPath` data stays on one node. It is for tests and node agents"),
        (0, "An administrator creates PersistentVolumes. A user asks for storage with a claim, and the Pod names the "
            "claim"),
        (0, "A StorageClass and its provisioner create a PV for each claim"),
        (0, "The reclaim policy decides what happens to the PV and its data after you delete the claim"),
        (0, "A StatefulSet gives each Pod a stable name, a stable DNS name and its own claim"),
        (0, "A headless Service and its SRV records let the Pods find their peers")], size=18, after=11)


def s_lab(prs):
    s = new_slide(prs, "Lab Week 10 at a Glance")
    end = grid(s, 0.60, TOP + 0.10, [2.20, 6.70, 3.20], [
        ["Lab step", "What you do", "Lecture slides"],
        ["Step 1", "Create the PV `data-pv` and the claim `data-pvc`", "11, 13, 14, 16, 17"],
        ["Step 2", "Show that the data stays after the Pod", "17, 18"],
        ["Step 3", "Install the provisioner and the StorageClass `standard`", "21, 23"],
        ["Step 4", "Create the StatefulSet `kubia` and its headless Service", "29, 30, 31"],
        ["Step 5", "Show the identity of a Pod, its DNS name and the SRV records", "26, 28, 29, 33"],
        ["Step 6", "Clean up, and destroy the cluster", "23"]], row_h=0.55, size=14)
    rich(s, 0.60, end + 0.25, 12.10, 0.75, "Not in the lab: NFS, MySQL replication, the collection of the data of the "
         "peers, the Released phase, the update settings of slide 32 and the optional topics.", size=14, color=E.MUTED)
    return s


SLIDES = [s_part1, s_hostpath, s_concerns, s_sharing, s_example, s_limits,
          s_part2, s_process, s_access, s_pv, s_phases, s_decoupling, s_binds, s_claim_pod, s_benefits, s_sc,
          s_using_sc, s_sc_manifest, s_dynamic, s_course, s_pending,
          s_part3, s_why, s_mysql, s_versus, s_headless, s_manifest, s_volumes, s_updates, s_peers, s_dns,
          s_optional, s_takeaways, s_lab]


def main():
    if os.path.exists(OUT) and "--force" not in sys.argv:
        sys.exit("%s exists. Bump VERSION; never overwrite a delivered deck." % OUT)
    prs = Presentation(SRC)
    keep_first(prs, 3)
    cover(prs, "PV, PVC, StorageClass", "and StatefulSets", 10)
    agenda(prs, [
        (0, "`hostPath`: data on one node"),
        (0, "PersistentVolumes and claims"),
        (1, "Access modes, phases and reclaim policies"),
        (0, "StorageClasses and dynamic provisioning"),
        (1, "Storage on the course cluster, and a Pending claim"),
        (0, "StatefulSets"),
        (1, "Headless Services"),
        (1, "Updates and ordinals"),
        (1, "How Pods find their peers")])
    outline(prs, "Week 10: K8s – StorageClasses & StatefulSets")
    built = [prs.slides[0], prs.slides[1], prs.slides[2]] + [make(prs) for make in SLIDES]
    number_and_save(prs, built, "CLO835 Week 10 Lecture: PV, PVC, StorageClass and StatefulSets", OUT)


if __name__ == "__main__":
    main()
