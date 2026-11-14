# -*- coding: utf-8 -*-
"""CLO835 Week 10 lecture v8 - PV, PVC, StorageClass and StatefulSets.

Fixes every lecture defect of reports/report-2026-10-31-07-week10-standards-audit.md:
L1 to L3 Course Outline, L4 file name, L5 and L6 removed in-tree volume types, L7 image,
L8 and L9 wrong facts, L10 typing mistakes, L11 to L14 third-party images replaced by
native house diagrams, L15 and L16 commands that did not run, L17 bullets in ASD-STE100,
L18 title style.

Input : Week10/Week09_lecture_style_v7.pptx (read, never written)
Output: Week10/Lecture_week10_v8.pptx

Run from the project root. It is guarded, so importing it writes nothing.
    python build_week10_lecture_v8.py
    python build_week10_lecture_v8.py --dump DIR    # write the manifests of the slides to DIR
"""
import copy
import os
import sys

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

import build_week08 as E
from build_week09_lecture_v6 import arrow, box, label, remove_shape, shape_named, zone
from retarget_accounts import replace_in_paragraph

SRC = "Week10/Week09_lecture_style_v7.pptx"
OUT = "Week10/Lecture_week10_v8.pptx"
TOTAL = 28
SLATE, BLUE, STEPS = E.SLATE, E.BLUE, E.STEPS
RIGHT, LEFT, DOWN, UP = (MSO_SHAPE.RIGHT_ARROW, MSO_SHAPE.LEFT_ARROW, MSO_SHAPE.DOWN_ARROW, MSO_SHAPE.UP_ARROW)
TWO_WAY_H, TWO_WAY_V = MSO_SHAPE.LEFT_RIGHT_ARROW, MSO_SHAPE.UP_DOWN_ARROW

MANIFESTS = {
    "test-pd.yaml": """apiVersion: v1
kind: Pod
metadata:
  name: test-pd
spec:
  containers:
  - image: maziar/kubia:0.1
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
      type: DirectoryOrCreate""",
    "pod-using-my-nfs-volume.yaml": """apiVersion: v1
kind: Pod
metadata:
  name: pod-using-my-nfs-volume
spec:
  containers:
  - image: maziar/kubia:v1
    name: container-using-my-nfs-volume
    volumeMounts:
    - mountPath: /my-nfs
      name: my-nfs-volume
  volumes:
  - name: my-nfs-volume
    nfs:
      server: nfs.example.com
      path: /exports/data""",
    "kubia-pv.yaml": """apiVersion: v1
kind: PersistentVolume
metadata:
  name: kubia-pv
spec:
  capacity:
    storage: 1Gi
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  csi:
    driver: ebs.csi.aws.com
    volumeHandle: vol-049df61146c4d7901
    fsType: ext4""",
    "pvc-definition.yaml": """apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: myclaim
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: ""
  resources:
    requests:
      storage: 500Mi""",
    "pv-definition.yaml": """apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-vol1
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: ""
  capacity:
    storage: 1Gi
  csi:
    driver: ebs.csi.aws.com
    volumeHandle: vol-049df61146c4d7901
    fsType: ext4""",
    "kubia-pod.yaml": """apiVersion: v1
kind: Pod
metadata:
  name: kubia-pod
spec:
  containers:
  - image: maziar/kubia:v1
    name: kubia
    volumeMounts:
    - name: kubia-data
      mountPath: /var/data
    ports:
    - containerPort: 8080
      protocol: TCP
  volumes:
  - name: kubia-data
    persistentVolumeClaim:
      claimName: kubia-pvc""",
    "storageclass-fast.yaml": """apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
volumeBindingMode: WaitForFirstConsumer""",
    "kubia-pvc.yaml": """apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: kubia-pvc
spec:
  storageClassName: fast
  resources:
    requests:
      storage: 1Gi
  accessModes:
  - ReadWriteOnce""",
}

# slide, text box, manifest, font size, text box of the file name (None: name stays)
TERMINALS = [
    (7, "TextBox 8", "test-pd.yaml", 12, None),
    (8, "TextBox 9", "pod-using-my-nfs-volume.yaml", 11, "TextBox 8"),
    (11, "TextBox 8", "kubia-pv.yaml", 12, "TextBox 7"),
    (14, "TextBox 8", "pvc-definition.yaml", 11, None),
    (14, "TextBox 15", "pv-definition.yaml", 11, None),
    (15, "TextBox 8", "kubia-pod.yaml", 11, "TextBox 7"),
    (19, "TextBox 8", "storageclass-fast.yaml", 11, None),
    (19, "TextBox 15", "kubia-pvc.yaml", 11, "TextBox 14"),
]

SRV_LINES = [
    "# The headless Service of the lab. It has no cluster IP address.",
    "kubectl create service clusterip kubia --clusterip=None --tcp=80:8080",
    "",
    "# A client Pod asks the DNS server of the cluster for the SRV records.",
    "kubectl run dnstest --image=maziar/alpine-curl --restart=Never --command -- sleep 3600",
    "kubectl wait --for=condition=Ready pod/dnstest --timeout=120s",
    "kubectl exec dnstest -- nslookup -type=SRV kubia.default.svc.cluster.local",
]

TITLES = {
    6: "hostPath: Data Sharing with the Node",
    8: "Persistent Volumes: Storage in the Pod",
    10: "PersistentVolumes and PersistentVolumeClaims",
    12: "Decoupling Pods from the Storage Technology",
    15: "Using a PersistentVolumeClaim in a Pod",
    16: "Benefits of PersistentVolumes and Claims",
    17: "Provisioning Automation: StorageClass",
    18: "Using StorageClasses",
    19: "StorageClass Manifest",
    20: "Dynamic PersistentVolume Provisioning",
    24: "StatefulSets vs ReplicaSets",
    25: "Headless Service",
    26: "Adding Volumes to StatefulSet Pods",
    27: "Discovering Peers in a StatefulSet",
    28: "Peer Discovery through DNS",
}

REPLACE = {
    3: [("Study Week", "Week 8: Study Week"),
        ("Week 9: K8s- K8s- PVs & K8s in AKS", "Week 9: K8s – PVs & K8s in EKS"),
        ("Week 10: K8s: Storage classes & Statefulsets", "Week 10: K8s – StorageClasses & StatefulSets"),
        ("Week 13: K8s – RBAC and AKS", "Week 13: K8s – RBAC and EKS")],
    4: [("First persistent storage – not deleted when the pod is deleted",
         "hostPath is the first persistent storage: it stays when you delete the Pod"),
        ("hostPath should not be used to store application's data", "Do not use hostPath to store application data"),
        ("Used by pods to get access to host data, e.g. kubeconfig or /var/log or OS devices through file system",
         "Pods use hostPath to read host data, for example kubeconfig, /var/log or OS devices"),
        ("Used as a persistent volume for single-node tests only",
         "Use hostPath as a persistent volume for single-node tests only"),
        ("Stored on a specific node – is it suitable for DB storage?",
         "The data stays on one node. Is this suitable for a database?"),
        ("What if we need to persist data in a cluster with multiple worker nodes?",
         "How do we keep data in a cluster with many worker nodes?")],
    5: [("HostPaths can expose privileged system credentials", "A hostPath volume can expose privileged system credentials"),
        ("Pods with identical configuration (such as created from a PodTemplate) may behave differently on different nodes due to different files on the nodes",
         "Pods with the same configuration can behave differently on different nodes, because the files on the nodes differ"),
        ("The files or directories created on the underlying hosts are only writable by root",
         "Only root can write to the files and directories on the host")],
    8: [("Using a persistent volume requires:", "With a volume directly in the Pod description:"),
        ("creating the volume out-of-band (outside of the Kubernetes API)",
         "you create the volume outside of the Kubernetes API"),
        ("referencing the volume in the pod description, with all its parameters",
         "you reference the volume with all its parameters"),
        ("locks the pod definition to a specific cluster", "the Pod definition works on one specific cluster only")],
    11: [("Defining the PersistentVolume's size, access modes and reclaim policy.",
          "This manifest sets the size, the access mode and the reclaim policy."),
         ("It can be mounted by a single client for reading and writing, or by multiple clients for reading only. After the claim is released, the PersistentVolume should be retained (not erased or deleted).",
          "The csi block names the EBS CSI driver and the EBS volume. One node can mount the volume for reading and writing. When the claim goes, Kubernetes keeps the PersistentVolume. It does not erase or delete it.")],
    13: [("When an application needs storage, it creates a PersistentVolumeClaim (either directly, or through a volume claim template in a Stateful Set)",
          "When an application needs storage, it creates a PersistentVolumeClaim, directly or through a volume claim template in a StatefulSet"),
         ("The PersistentVolumeClaim is initially Pending", "The PersistentVolumeClaim is Pending at first"),
         ("Kubernetes then looks for a suitable PersistentVolume (maybe one is immediately available; maybe we need to wait for provisioning)",
          "Kubernetes then looks for a suitable PersistentVolume. One can be available, or a provisioner can create one"),
         ("Once a suitable PersistentVolume is found, the PVC becomes Bound",
          "When Kubernetes finds a suitable PersistentVolume, the PVC becomes Bound"),
         ("The PVC can then be used by a Pod (as long as the PVC is Pending, the Pod cannot run)",
          "A Pod can then use the PVC. While the PVC is Pending, the Pod cannot run")],
    17: [("What if we have multiple storage systems available? (e.g. NFS and iSCSI; or AzureFile and AzureDisk; or Cinder and Ceph...)",
          "What if we have many storage systems? For example, NFS and iSCSI, or Amazon EBS and Amazon EFS"),
         ("What if we have a storage system with multiple tiers? (e.g. SAN with RAID1 and RAID5; general purpose vs. io optimized EBS...)",
          "What if one storage system has many tiers? For example, general purpose and I/O optimized EBS"),
         ("Kubernetes lets us define storage classes to represent these (see if you have any available at the moment with kubectl get storageclasses)",
          "A StorageClass represents each one. Use kubectl get storageclass to list them")],
    18: [("Optionally, each PV and each PVC can reference a StorageClass (field spec.storageClassName)",
          "Each PV and each PVC can reference a StorageClass (field spec.storageClassName)"),
         ("When creating a PVC, specifying a StorageClass means “use that particular storage system to provision the volume!”",
          "A PVC that names a StorageClass asks that storage system to provision the volume"),
         ("Storage classes are necessary for dynamic provisioning (but we can also ignore them and perform manual provisioning)",
          "Dynamic provisioning needs a StorageClass. Manual provisioning does not")],
    21: [("deploying clustered applications", "Deploying Clustered Applications")],
    22: [("Because some apps (databases, clustered systems) need things Deployments cannot give:",
          "Some applications (databases, clustered systems) need things that a Deployment cannot give:"),
         ("pod names carry an ordinal index from 0 (mysql-0, mysql-1) and survive restarts. Deployment pods get random names and IPs.",
          "Pod names have an ordinal index from 0 (mysql-0, mysql-1), and they stay after a restart. Deployment Pods get random names."),
         ("each pod gets its own DNS name via the headless service, so \"the master\" is always reachable at mysql-0.",
          "Each Pod gets its own DNS name through the headless Service, so the master is always at mysql-0."),
         ("Per-pod storage", "Storage for each Pod"),
         ("each replica gets its own PVC that reattaches to the same pod after rescheduling. Deployment replicas share one volume.",
          "Each Pod gets its own PVC, and the PVC stays with that Pod after a restart. Deployment replicas share one volume."),
         ("pods start, scale, and update one at a time, in sequence (master before slaves). Deployments start all pods in parallel.",
          "Pods start, scale and update one at a time, in order (master before slaves). A Deployment starts its Pods in parallel.")],
    24: [("Pods in ReplicaSet are like cattle. They are indistinguishable and replaceable. If the pod dies a new pod with anew IP/hostname and data is created.",
          "Pods in a ReplicaSet are like cattle. They are the same, and you can replace them. When a Pod dies, the new Pod gets a new name, a new IP address and no data."),
         ("Pods in Stateful sets are like pets. When a \"pet\" dies, it needs to be resurrected with the same name, IP and data. Pods in Statefulsets are not replicas of each other.",
          "Pods in a StatefulSet are like pets. When a pet dies, the new Pod gets the same name, DNS name and data. Its IP address can change. These Pods are not replicas of each other.")],
    25: [("Normal service cannot be used as it load balances the requests and our objective is to write only to master.",
          "A normal Service load balances the requests, but we must write to the master only."),
         ("An IP cannot be used only to write as it might change. Even the Pod dns cannot be used as it has IP in it.",
          "A Pod IP address can change, so we cannot use it. The default Pod DNS name holds the IP address, so it changes too."),
         ("A headless Service (clusterIP: None) does not load balance the requests. Points to only Master.",
          "A headless Service (clusterIP: None) does not load balance. Its DNS name returns the IP addresses of all the Pods."),
         ("Uses Pod DNS which is mysql-0.mysql-h.default.svc.cluster.local",
          "Each Pod gets a stable DNS name. The master is mysql-0.mysql-h.default.svc.cluster.local")],
    26: [("Storage needs to be persistent and decoupled from pods", "Storage must be persistent and separate from the Pods"),
         ("Each pod needs to reference a different PVC", "Each Pod must reference a different PVC"),
         ("PVCs need to be created by Statefulset and not separately as we did for the stateless pods",
          "The StatefulSet creates the PVCs. We do not create them separately, as we did for stateless Pods")],
    27: [("Application should be K8s agnostic so querying K8s API to find all the pods in the cluster is undesirable",
          "An application should not depend on Kubernetes, so it should not query the Kubernetes API to find its peers"),
         ("K8s uses DNS SRV records to facilitate the discovery. Kubernetes creates SRV records to point to the hostnames of the pods backing a headless service.",
          "Kubernetes creates DNS SRV records that point to the hostnames of the Pods behind a headless Service")],
    28: [("Data stored by individual pods is independent – this is not a cluster yet",
          "Each Pod stores its own data, so this is not a cluster yet"),
         ("We can improve the functionality by discovering all the pods in the StatefulSet and serving data from all the pods in the cluster",
          "A Pod can find all the Pods of the StatefulSet, and serve the data of all of them")],
}

MYSQL_STEPS = ["1.  Set up the master first, then the slaves",
               "2.  Clone the data from the master to slave-1",
               "3.  Start continuous replication from the master to slave-1",
               "4.  Wait until slave-1 is ready",
               "5.  Clone the data from slave-1 to slave-2",
               "6.  Start continuous replication from the master to slave-2",
               "7.  Set the master address on each slave"]


def swap(slide, old, new):
    """Replace old in the one run that holds it. A miss stops the build."""
    hits = 0
    for sh in slide.shapes:
        if sh.has_text_frame:
            for p in sh.text_frame.paragraphs:
                for r in p.runs:
                    if old in r.text:
                        r.text = r.text.replace(old, new)
                        hits += 1
    if not hits:
        # The source splits some bullets over runs. new never holds old on these lines.
        hits = sum(replace_in_paragraph(p, old, new) for sh in slide.shapes if sh.has_text_frame
                   for p in sh.text_frame.paragraphs)
    assert hits == 1, (old, hits)


def large_picture(slide):
    big = [sh for sh in slide.shapes if sh.shape_type == 13 and sh.width > Inches(1)]
    assert len(big) == 1, len(big)
    return big[0].name


def set_title(slide, text):
    box_ = shape_named(slide, "TextBox 1")
    para = box_.text_frame.paragraphs[0]
    assert len(box_.text_frame.paragraphs) == 1
    para.runs[0].text = text
    para.runs[0].font.size = Pt(32)
    for extra in para.runs[1:]:
        extra._r.getparent().remove(extra._r)


def line_color(line, yaml):
    if line.lstrip().startswith("#"):
        return E.TERM_GRN
    if not yaml:
        return E.TERM_CYAN
    return E.TERM_CYAN if line.split(":")[0] in ("apiVersion", "kind", "metadata", "spec", "provisioner",
                                                 "parameters", "volumeBindingMode") else E.TERM_GRAY


def set_lines(slide, name, lines, size, yaml=True):
    frame = shape_named(slide, name).text_frame
    for p in list(frame.paragraphs[1:]):
        p._p.getparent().remove(p._p)
    first = frame.paragraphs[0]
    for r in list(first.runs):
        r._r.getparent().remove(r._r)
    for i, line in enumerate(lines):
        p = first if i == 0 else frame.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.line_spacing = 1.15
        r = p.add_run()
        r.text = line or " "
        r.font.name = E.FONT_MONO
        r.font.size = Pt(size)
        r.font.color.rgb = line_color(line, yaml)


def set_size(slide, name, size):
    for p in shape_named(slide, name).text_frame.paragraphs:
        for r in p.runs:
            r.font.size = Pt(size)


def place(shape, x, y, w, h):
    shape.left, shape.top, shape.width, shape.height = Inches(x), Inches(y), Inches(w), Inches(h)


def add_bullet(slide, name, text):
    """A new level-0 bullet: a copy of the first paragraph, so the format stays."""
    frame = shape_named(slide, name).text_frame
    frame._txBody.append(copy.deepcopy(frame.paragraphs[0]._p))
    frame.paragraphs[-1].runs[-1].text = text


def caption(s, y, text):
    E.add_text(s, Inches(0.7), Inches(y), Inches(11.95), Inches(0.4), text, size=13.5, italic=True,
               color=E.MUTED, align=PP_ALIGN.CENTER)


def slide5(s):
    place(shape_named(s, "TextBox 2"), 0.70, 1.70, 11.90, 2.75)
    E.callout(s, 0.70, 4.70, 11.90, 1.35,
              "Warning: a hostPath volume has many security risks. Avoid it when you can. If you must use it, "
              "scope it to the required file or directory, and mount it as ReadOnly.")


def slide6(s):
    for x, w, name, pods in ((0.8, 6.6, "Node 1", 2), (7.7, 4.8, "Node 2", 1)):
        zone(s, x, 1.6, w, 4.2, name)
        step = (w - 0.3) / pods
        for k in range(pods):
            px = x + 0.3 + k * step
            zone(s, px, 2.05, step - 0.3, 1.85, "Pod", color=STEPS[1], fill=E.CARD_BG)
            box(s, px + 0.3, 2.55, step - 0.9, 1.1, "hostPath volume", STEPS[1], size=14)
            arrow(s, DOWN, px + (step - 0.3) / 2 - 0.19, 3.95, 0.38, 0.55)
        box(s, x + 0.3, 4.55, w - 0.6, 0.95, "/some/path/on/host", SLATE, size=15)
    caption(s, 5.98, "Pods on one node share the folder. A Pod on another node sees a different folder.")


def slide10(s):
    cols = (2.4, 6.0, 9.6)
    box(s, 0.55, 1.85, 1.6, 1.65, "Administrator", SLATE, size=14)
    box(s, cols[0], 1.85, 3.15, 1.65, "1. Set up network storage (NFS or similar)", STEPS[3], size=15)
    arrow(s, RIGHT, cols[0] + 3.2, 2.5, 0.4, 0.36)
    box(s, cols[1], 1.85, 3.15, 1.65, "2. Create a PersistentVolume (PV) through the Kubernetes API", STEPS[3], size=15)
    arrow(s, DOWN, cols[1] + 1.39, 3.55, 0.38, 0.55)
    box(s, 0.55, 4.15, 1.6, 1.65, "User", SLATE, size=14)
    box(s, cols[0], 4.15, 3.15, 1.65, "3. Create a PersistentVolumeClaim (PVC)", STEPS[1], size=15)
    arrow(s, RIGHT, cols[0] + 3.2, 4.8, 0.4, 0.36)
    box(s, cols[1], 4.15, 3.15, 1.65, "4. Kubernetes binds the PVC to a PV of the correct size and access mode",
        STEPS[5], size=15)
    arrow(s, RIGHT, cols[1] + 3.2, 4.8, 0.4, 0.36)
    box(s, cols[2], 4.15, 3.15, 1.65, "5. Create a Pod with a volume that references the PVC", STEPS[1], size=15)


def slide12(s):
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
    zone(s, 0.8, 5.52, 11.7, 1.2, "Nodes: cluster level, no namespace", color=STEPS[4], fill=E.CARD_BG)
    for k in range(6):
        box(s, 1.0 + k * 1.92, 5.94, 1.6, 0.62, "Node", SLATE, size=14)


def slide16(s):
    cols = (2.7, 5.25, 7.8, 10.35)
    box(s, 0.55, 1.75, 1.85, 1.5, "Direct volume", SLATE, size=14)
    box(s, cols[0], 1.75, 2.1, 1.5, "Pod\n(nfs volume)", STEPS[1], size=14)
    label(s, cols[0] + 2.15, 2.0, 5.45, 0.32, "The Pod names the storage", size=13)
    arrow(s, RIGHT, cols[0] + 2.15, 2.35, 5.45, 0.36)
    box(s, cols[3], 1.75, 2.1, 1.5, "NFS server", STEPS[5], size=14)
    box(s, 0.55, 3.95, 1.85, 1.5, "With a claim", SLATE, size=14)
    box(s, cols[0], 3.95, 2.1, 1.5, "Pod\n(claimName)", STEPS[1], size=14)
    arrow(s, RIGHT, cols[0] + 2.12, 4.53, 0.41, 0.36)
    box(s, cols[1], 3.95, 2.1, 1.5, "PVC\nkubia-pvc", STEPS[3], size=14)
    arrow(s, RIGHT, cols[1] + 2.12, 4.53, 0.41, 0.36)
    box(s, cols[2], 3.95, 2.1, 1.5, "PV\nkubia-pv", STEPS[3], size=14)
    arrow(s, RIGHT, cols[2] + 2.12, 4.53, 0.41, 0.36)
    box(s, cols[3], 3.95, 2.1, 1.5, "Amazon EBS volume", STEPS[5], size=14)
    caption(s, 5.75, "The Pod names the claim, not the storage. The same Pod manifest works on another cluster.")


def slide20(s):
    cols = (0.7, 4.75, 8.8)
    rows = (1.6, 4.25)
    cells = [(0, 0, "1. The administrator sets up a PersistentVolume provisioner, if the cluster has none.", STEPS[3]),
             (1, 0, "2. The administrator creates one or more StorageClasses, and marks one as the default.", STEPS[3]),
             (2, 0, "3. The user creates a PVC that names a StorageClass, or names none to use the default.", STEPS[1]),
             (2, 1, "4. Kubernetes finds the StorageClass and asks its provisioner for a new PV. The PVC gives the size and the access mode.", SLATE),
             (1, 1, "5. The provisioner creates the storage and a PersistentVolume. Kubernetes binds the PV to the PVC.", SLATE),
             (0, 1, "6. The user creates a Pod with a volume that references the PVC by name.", STEPS[1])]
    for c, r, text, fill in cells:
        box(s, cols[c], rows[r], 3.45, 2.1, text, fill, size=14.5)
    arrow(s, RIGHT, cols[0] + 3.5, 2.47, 0.5, 0.36)
    arrow(s, RIGHT, cols[1] + 3.5, 2.47, 0.5, 0.36)
    arrow(s, DOWN, cols[2] + 1.53, 3.74, 0.38, 0.47)
    arrow(s, LEFT, cols[1] + 3.5, 5.12, 0.5, 0.36)
    arrow(s, LEFT, cols[0] + 3.5, 5.12, 0.5, 0.36)


def slide23(s):
    E.add_text(s, Inches(0.55), Inches(1.6), Inches(6.2), Inches(4.9), MYSQL_STEPS, size=15, line_spacing=1.75)
    box(s, 7.3, 1.75, 5.3, 1.0, "mysql-master", SLATE, size=16)
    arrow(s, DOWN, 8.29, 2.8, 0.38, 0.6)
    arrow(s, DOWN, 11.24, 2.8, 0.38, 0.6)
    label(s, 8.8, 2.9, 2.3, 0.4, "Replication", size=12.5)
    box(s, 7.3, 3.45, 2.35, 1.3, "mysql-slave-1", STEPS[3], size=15)
    arrow(s, RIGHT, 9.7, 3.92, 0.5, 0.36)
    label(s, 9.45, 3.5, 1.0, 0.35, "Clone", size=12.5)
    box(s, 10.25, 3.45, 2.35, 1.3, "mysql-slave-2", STEPS[3], size=15)
    label(s, 7.05, 4.85, 2.85, 0.35, "MASTER_HOST=mysql-master", size=12)
    label(s, 10.0, 4.85, 2.85, 0.35, "MASTER_HOST=mysql-master", size=12)


def slide24(s):
    place(shape_named(s, "TextBox 2"), 0.60, 1.55, 6.10, 5.0)
    set_size(s, "TextBox 2", 17)
    for y, name, fill, pods in ((1.75, "ReplicaSet A", SLATE, ("Pod A-dsfwx", "Pod A-fewrb", "Pod A-jwejc")),
                                (4.25, "StatefulSet A", STEPS[3], ("Pod A-0", "Pod A-1", "Pod A-2"))):
        box(s, 7.0, y + 0.45, 2.0, 1.1, name, fill, size=14)
        arrow(s, RIGHT, 9.05, y + 0.82, 0.5, 0.36)
        for k, pod in enumerate(pods):
            box(s, 9.6, y + k * 0.7, 3.0, 0.6, pod, STEPS[1], size=13.5)


def slide25(s):
    place(shape_named(s, "TextBox 2"), 0.60, 1.60, 6.20, 5.0)
    set_size(s, "TextBox 2", 15)
    box(s, 7.1, 1.7, 5.7, 0.85, "Headless Service mysql-h (clusterIP: None)", SLATE, size=14.5)
    for k, (name, fill) in enumerate((("mysql-0\nmaster", STEPS[3]), ("mysql-1", STEPS[0]), ("mysql-2", STEPS[0]))):
        x = 7.1 + k * 1.975
        arrow(s, DOWN, x + 0.68, 2.6, 0.38, 0.45)
        box(s, x, 3.1, 1.75, 1.05, name, fill, size=14)
    label(s, 7.1, 4.2, 5.7, 0.35, "mysql-0.mysql-h.default.svc.cluster.local", size=12.5)
    E.callout(s, 7.1, 4.75, 5.7, 1.2, "mysql-1 and mysql-2 use MASTER_HOST=mysql-0.mysql-h")


def slide26(s):
    place(shape_named(s, "TextBox 2"), 0.60, 1.60, 6.10, 5.0)
    set_size(s, "TextBox 2", 17)
    zone(s, 6.95, 1.9, 1.85, 3.9, "StatefulSet A")
    box(s, 7.08, 2.4, 1.6, 1.4, "Pod template", STEPS[1], size=13.5)
    box(s, 7.08, 4.0, 1.6, 1.6, "Volume claim template", STEPS[3], size=13.5)
    for k in range(3):
        y = 1.95 + k * 1.35
        arrow(s, RIGHT, 8.84, y + 0.36, 0.26, 0.3)
        box(s, 9.12, y, 1.0, 1.02, "Pod A-%d" % k, STEPS[1], size=12.5)
        arrow(s, RIGHT, 10.14, y + 0.36, 0.26, 0.3)
        box(s, 10.42, y, 1.0, 1.02, "PVC A-%d" % k, STEPS[3], size=12.5)
        arrow(s, RIGHT, 11.44, y + 0.36, 0.26, 0.3)
        box(s, 11.72, y, 1.0, 1.02, "PV", STEPS[5], size=12.5)


def slide28(s):
    place(shape_named(s, "TextBox 2"), 0.60, 1.40, 11.90, 1.35)
    set_size(s, "TextBox 2", 16)
    box(s, 1.0, 4.55, 2.0, 1.05, "curl", SLATE, size=15)
    label(s, 3.05, 4.5, 2.1, 0.35, "1. GET /", size=12.5)
    arrow(s, TWO_WAY_H, 3.05, 4.9, 2.1, 0.36)
    label(s, 3.05, 5.3, 2.1, 0.55, "6. Return the collected data", size=12.5)
    box(s, 5.2, 2.85, 2.0, 0.65, "DNS", STEPS[5], size=14)
    arrow(s, TWO_WAY_V, 6.01, 3.53, 0.38, 0.42)
    label(s, 6.45, 3.55, 1.9, 0.35, "2. SRV lookup", size=12.5, align=PP_ALIGN.LEFT)
    box(s, 5.2, 3.98, 2.0, 2.65, "kubia-0\n\n3. Read its own data", STEPS[3], size=14)
    label(s, 7.25, 3.98, 2.4, 0.35, "4. GET /data", size=12.5)
    arrow(s, RIGHT, 7.25, 4.34, 2.4, 0.36)
    label(s, 7.25, 5.3, 2.4, 0.35, "5. GET /data", size=12.5)
    arrow(s, RIGHT, 7.25, 5.66, 2.4, 0.36)
    box(s, 9.7, 4.0, 2.0, 1.05, "kubia-1", STEPS[3], size=14)
    box(s, 9.7, 5.32, 2.0, 1.05, "kubia-2", STEPS[3], size=14)


DIAGRAMS = {5: slide5, 6: slide6, 10: slide10, 12: slide12, 16: slide16, 20: slide20, 23: slide23,
            24: slide24, 25: slide25, 26: slide26, 28: slide28}


def main():
    prs = Presentation(SRC)
    assert len(prs.slides) == TOTAL
    for no, pairs in REPLACE.items():
        for old, new in pairs:
            swap(prs.slides[no - 1], old, new)
    for no, text in TITLES.items():
        set_title(prs.slides[no - 1], text)
    for no, name, manifest, size, name_box in TERMINALS:
        set_lines(prs.slides[no - 1], name, MANIFESTS[manifest].split("\n"), size)
        if name_box:
            shape_named(prs.slides[no - 1], name_box).text_frame.paragraphs[0].runs[0].text = manifest
    set_lines(prs.slides[26], "TextBox 9", SRV_LINES, 11.5, yaml=False)
    add_bullet(prs.slides[7], "TextBox 2",
               "Amazon EBS has no direct volume type in a Pod. It needs a PersistentVolume and the EBS CSI driver")
    for no, draw in DIAGRAMS.items():
        remove_shape(prs.slides[no - 1], large_picture(prs.slides[no - 1]))
        draw(prs.slides[no - 1])
    E._sanitize_coords(prs)
    prs.save(OUT)
    print("wrote %s (%d slides)" % (OUT, TOTAL))


if __name__ == "__main__":
    if "--dump" in sys.argv:
        folder = sys.argv[sys.argv.index("--dump") + 1]
        for name, text in MANIFESTS.items():
            with open(os.path.join(folder, name), "w") as f:
                f.write(text + "\n")
    else:
        main()
