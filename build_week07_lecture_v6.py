# -*- coding: utf-8 -*-
"""CLO835 Week 07 lecture v6 - Volumes: Attaching Disk Storage to Containers.

Built from the old lecture of the user, Week07/week7_old.pptx (14 slides). Each of its
14 slides stays, in the same order, with all its points. v5 had merged slides 3 and 4 and
removed the gitRepo diagram; this version keeps them. The cover and the Course Outline come
from the Week 12 v6 lecture. Each picture of the old file is now a native house diagram or a
house terminal.

The facts follow the Kubernetes v1.35 documents (the cluster of the course runs v1.35):
- gitRepo is deprecated and disabled by default, so an init container clones the repository.
- The in-tree drivers of awsElasticBlockStore (v1.27), azureDisk (v1.27) and
  gcePersistentDisk (v1.28) are removed. Cloud disks use a CSI driver.
- cinder, cephfs, glusterfs, rbd, vsphereVolume and the older types are not in v1.35.
The manifests of the emptyDir and the gitRepo slides are the live-tested manifests of the
Week 07 lab, so the lecture and the lab agree.

Input : Week12/Lecture_week12_v6.pptx, for the cover and the outline (read, never written)
        Week07/week7_old.pptx, the source of the content (read, never written)
Output: Week07/Lecture_week07_v6.pptx (the build refuses to overwrite it)

Run from the project root. It is guarded, so importing it writes nothing.
    python build_week07_lecture_v6.py
"""
import copy
import os
import sys

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches

import build_week08 as E
from build_week09_lecture_v6 import arrow, box, label, zone
from build_week12_lecture_v6 import finish, footer_guard
from build_week13_lecture_v8 import bullets, flow, keep_first, new_slide, set_only_run

SRC = "Week12/Lecture_week12_v6.pptx"
OLD = "Week07/week7_old.pptx"
OUT = "Week07/Lecture_week07_v6.pptx"
SLATE, STEPS = E.SLATE, E.STEPS
DOWN, LEFT = MSO_SHAPE.DOWN_ARROW, MSO_SHAPE.LEFT_ARROW

# The titles of the old file, in deck order. The build stops if the source changes.
OLD_TITLES = ["Volumes: Attaching Disk Storage to Containers", "Agenda", "K8s Volumes", "Volumes",
              "Volumes vs PersistentVolumes", "Volume Types", "Volume Types, Cont", "Volume Type: emptyDir",
              "Volume Lifecycle", "Using GitRepo Volume", "Pod Manifest with GitRepo", "Managing configuration",
              "Persistent Volumes: Amazon EBS", "Using NFS Volume"]

# The emptyDir Pod of lab Week 07, Step 1 on slide 4 (live-tested on 2026-10-27).
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

# The gitRepo replacement of lab Week 07, Step 3 on slide 6 (live-tested on 2026-10-27).
GIT_POD = """apiVersion: v1
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

EBS_POD = """apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-ebs-claim
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: ebs-sc
  resources:
    requests:
      storage: 4Gi
---
apiVersion: v1
kind: Pod
metadata:
  name: pod-using-my-ebs-volume
spec:
  containers:
  - image: maziar/kubia:v1
    name: container-using-my-ebs-volume
    volumeMounts:
    - mountPath: /my-ebs
      name: my-ebs-volume
  volumes:
  - name: my-ebs-volume
    persistentVolumeClaim:
      claimName: my-ebs-claim""".split("\n")

NFS_POD = """apiVersion: v1
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
      server: 192.168.0.55
      path: "/exports/assets\"""".split("\n")


def check_old():
    old = Presentation(OLD)
    titles = []
    for slide in old.slides:
        first = [sh for sh in slide.shapes if sh.has_text_frame and sh.text_frame.text.strip()][0]
        titles.append(" ".join(first.text_frame.text.split()))
    assert titles == OLD_TITLES, titles


def current_week(outline):
    """The blue tile of the current week moves from Week 12 to Week 7."""
    labels = {"Week 12: K8s – ConfigMaps & Secrets": None, "Week 7: K8s – Volumes": None}
    for sh in outline.shapes:
        if sh.has_text_frame and sh.text_frame.text in labels:
            labels[sh.text_frame.text] = sh
    blue, normal = labels["Week 12: K8s – ConfigMaps & Secrets"], labels["Week 7: K8s – Volumes"]
    frames = [[sh for sh in outline.shapes if sh.shape_type == 1 and sh.top == tb.top
               and abs(sh.left - (tb.left - Inches(0.16))) < Inches(0.02)][0] for tb in (blue, normal)]
    for one, two in (frames, (blue, normal)):
        one.left, two.left = two.left, one.left
        one.top, two.top = two.top, one.top
    set_only_run(blue, "Week 7: K8s – Volumes")
    set_only_run(normal, "Week 12: K8s – ConfigMaps & Secrets")


def two_lines(shape, first, second):
    """The cover title in two lines, as in the old file, so that it stays clear of the logo."""
    set_only_run(shape, first)
    para = shape.text_frame.paragraphs[0]._p
    para.addnext(copy.deepcopy(para))
    set_only_run_of(shape.text_frame.paragraphs[1], second)


def set_only_run_of(paragraph, text):
    paragraph.runs[0].text = text
    for extra in paragraph.runs[1:]:
        extra._r.getparent().remove(extra._r)


def yaml(s, x, y, w, h, bar, lines, size=10):
    """A house terminal for a manifest. The position is in inches."""
    E.yaml_terminal(s, x, y, w, h, bar, lines, font_size=size)


def card(s, x, y, w, h, key, body):
    """E.annot_card with 12 pt body text, the smallest body size of the house."""
    E.add_rounded_rect(s, Inches(x), Inches(y), Inches(w), Inches(h), E.CARD_BG,
                       line=E.RULE_GRAY, line_width=0.75, radius_ratio=0.10)
    E.add_rect(s, Inches(x), Inches(y + 0.04), Inches(0.10), Inches(h - 0.08), E.BLUE)
    E.add_text(s, Inches(x + 0.28), Inches(y + 0.13), Inches(w - 0.45), Inches(0.34), key,
               font=E.FONT_MONO, size=12, bold=True, color=E.BLUE)
    E.add_text(s, Inches(x + 0.28), Inches(y + 0.48), Inches(w - 0.45), Inches(h - 0.56), body,
               size=12, color=E.BODY, line_spacing=1.08)


def cards(s, x, y, w, items, h=0.92, gap=0.12):
    """Each item is (key, body) or (key, body, height)."""
    for item in items:
        key, body, high = item if len(item) == 3 else item + (h,)
        card(s, x, y, w, high, key, body)
        y += high + gap


def text_slide(prs, title, items, size=18, after=9):
    s = new_slide(prs, title)
    bullets(s, 0.60, 1.75, 12.10, items, size=size, after=after)
    return s


def slide4(prs):
    return text_slide(prs, "K8s Volumes", [
        (0, "Each container has its own filesystem. The containers of a Pod share the network, but not the filesystem"),
        (0, "The data in a volume stays when a container restarts"),
        (0, "The containers of a Pod can share a volume"),
        (0, "You define a volume in the Pod specification"),
        (0, "A volume follows the lifecycle of its Pod:"),
        (1, "Kubernetes mounts the volume when the Pod starts"),
        (1, "Kubernetes unmounts the volume when the Pod ends")])


def slide5(prs):
    return text_slide(prs, "Volumes", [
        (0, "A volume is a special directory that Kubernetes mounts in a container"),
        (0, "Volumes have many purposes:"),
        (1, "Share files and directories between containers that run on the same node"),
        (1, "Share files and directories between containers and their host"),
        (1, "Store configuration information in Kubernetes and give it to containers"),
        (1, "Store credentials and secrets in Kubernetes, and give them to containers safely"),
        (1, "Store persistent data for stateful services")])


def slide6(prs):
    return text_slide(prs, "Volumes vs PersistentVolumes", [
        (0, "Volumes and PersistentVolumes are related, but they are very different"),
        (0, "Volumes:"),
        (1, "are part of the Pod specification. The next slides show this"),
        (1, "are not API resources, so `kubectl get volumes` gives an error"),
        (0, "PersistentVolumes:"),
        (1, "are API resources, so `kubectl get persistentvolumes` works"),
        (1, "are real storage volumes, for example on a SAN or on Amazon EBS"),
        (1, "connect to a Pod only through a PersistentVolumeClaim"),
        (1, "The Week 10 lecture teaches PersistentVolumes in detail")], size=17, after=7)


def slide7(prs):
    return text_slide(prs, "Volume Types", [
        (0, "emptyDir: a simple empty directory for temporary data"),
        (0, "hostPath: mounts a directory of the worker node filesystem into the Pod"),
        (0, "gitRepo: clones a Git repository into an empty directory. Kubernetes deprecated it, and v1.35 "
            "disables it by default"),
        (0, "nfs: mounts an NFS share into the Pod"),
        (0, "Cloud provider storage now uses a CSI driver. Kubernetes removed these in-tree drivers:"),
        (1, "gcePersistentDisk (Google Compute Engine Persistent Disk): removed in v1.28, now `pd.csi.storage.gke.io`"),
        (1, "awsElasticBlockStore (Amazon Elastic Block Store volume): removed in v1.27, now `ebs.csi.aws.com`"),
        (1, "azureDisk (Microsoft Azure Disk volume): removed in v1.27, now `disk.csi.azure.com`")],
        size=17, after=7)


def slide8(prs):
    return text_slide(prs, "Volume Types, Continued", [
        (0, "Other volume types: iscsi, fc (Fibre Channel) and local (a disk, a partition or a directory of the node, "
            "through a static PersistentVolume only)"),
        (0, "Kubernetes deprecated flexVolume in v1.23. Use the csi volume type and the CSI driver of the storage vendor"),
        (0, "Kubernetes removed the in-tree drivers of these old types: cinder, cephfs, flocker, glusterfs, quobyte, rbd, "
            "vsphereVolume, photonPersistentDisk and scaleIO"),
        (0, "configMap, secret and downwardAPI: special types that give Kubernetes resources and cluster "
            "information to the Pod"),
        (0, "persistentVolumeClaim: uses persistent storage that an administrator or a provisioner created")], size=17, after=9)


def slide9(prs):
    s = new_slide(prs, "Volume Type: emptyDir")
    bullets(s, 0.60, 1.75, 5.70, [
        (0, "Start with a simple Pod manifest"),
        (0, "Add a volume to that Pod manifest"),
        (0, "Mount that volume in the containers of the Pod"),
        (0, "When the volume names no type, Kubernetes makes it an emptyDir (an empty directory)"),
        (0, "The volume \"shadows\" the directory where Kubernetes mounts it. The old files of that directory are "
            "not visible"),
        (0, "In this Pod, html-generator writes a page into the volume, and nginx serves the same page")],
        size=16, after=8)
    yaml(s, 6.55, 1.50, 6.20, 5.15, "fortune-pod.yaml", FORTUNE, size=9)
    return s


def slide10(prs):
    return text_slide(prs, "Volume Lifecycle", [
        (0, "A volume has the same lifecycle as its Pod"),
        (0, "So Kubernetes creates a volume when it starts the Pod on a node"),
        (0, "This is true for emptyDir volumes"),
        (0, "Kubernetes does not \"create\" other volumes, for example remote storage. It \"attaches\" them"),
        (0, "A volume stays when a container restarts"),
        (0, "Kubernetes deletes an emptyDir volume when it deletes the Pod. It only unmounts or detaches remote storage, "
            "so the data stays")])


def slide11(prs):
    s = new_slide(prs, "Using a Git Repository in a Volume")
    E.add_text(s, Inches(0.60), Inches(1.55), Inches(12.10), Inches(0.62),
               "The gitRepo volume type did these steps itself. Kubernetes deprecated it, so an init container and an "
               "emptyDir volume do the same job.", size=15, color=E.BODY)
    box(s, 0.60, 3.30, 1.70, 1.00, "User or controller", STEPS[5], size=14)
    flow(s, 2.38, 3.52, 1.36, "1. Create")
    zone(s, 3.80, 2.35, 5.40, 4.25, "Pod", color=STEPS[1], fill=E.CARD_BG)
    box(s, 4.05, 2.95, 2.25, 0.95, "Container\nnginx", STEPS[0], size=14)
    box(s, 6.70, 2.95, 2.25, 0.95, "Init container\ngit clone", STEPS[3], size=14)
    box(s, 4.60, 5.05, 3.80, 1.00, "emptyDir volume", SLATE, size=15)
    arrow(s, DOWN, 5.00, 3.98, 0.36, 1.00, fill=STEPS[0])
    label(s, 5.42, 4.18, 1.10, 0.60, "3. Mount", size=13, align=PP_ALIGN.LEFT)
    arrow(s, DOWN, 7.65, 3.98, 0.36, 1.00, fill=STEPS[3])
    label(s, 8.07, 4.18, 1.05, 0.60, "2. Write", size=13, align=PP_ALIGN.LEFT)
    box(s, 10.55, 2.95, 2.20, 0.95, "Git repository", STEPS[4], size=14)
    flow(s, 9.02, 3.15, 1.48, "2. Clone", kind=LEFT)
    E.add_text(s, Inches(9.45), Inches(4.30), Inches(3.30), Inches(2.30),
               ["1. The user or a controller creates a Pod with an init container and an emptyDir volume.",
                "2. The init container clones the repository into the volume. Then it stops.",
                "3. The container starts, with the volume mounted at its mount path."],
               size=12.5, color=E.BODY, line_spacing=1.12)
    return s


def slide12(prs):
    s = new_slide(prs, "Pod Manifest with a Git Repository")
    yaml(s, 0.55, 1.50, 6.90, 5.15, "gitrepo-volume-pod.yaml", GIT_POD, size=9)
    cards(s, 7.70, 1.55, 5.05, [
        ("initContainers:", "It runs to completion before nginx starts."),
        ("sojoudian/kubia.git", "The init container clones this Git repository. nginx then serves its files, "
                                "for example /app.js.", 1.10),
        ("--branch=master", "Git checks out the master branch."),
        ("/repo", "Git clones into the root directory of the volume."),
        ("emptyDir: {}", "It starts empty. nginx serves it read-only.")], gap=0.08)
    return s


def slide13(prs):
    return text_slide(prs, "Managing Configuration", [
        (0, "Some applications need configuration"),
        (0, "Our code can get its configuration with many methods:"),
        (1, "command-line arguments"),
        (1, "environment variables"),
        (1, "configuration files"),
        (1, "configuration servers (the configuration comes from a database, an API or another source)"),
        (1, "other methods, because programmers find many solutions"),
        (0, "How do you do these things with containers and Kubernetes?")])


def slide14(prs):
    s = new_slide(prs, "Persistent Volumes: Amazon EBS")
    bullets(s, 0.60, 1.75, 5.30, [
        (0, "With the old awsElasticBlockStore type:"),
        (1, "you created the EBS volume outside of the Kubernetes API"),
        (1, "you put the volume ID and all its settings in the Pod"),
        (0, "Kubernetes v1.27 removed that in-tree driver. The EBS CSI driver (`ebs.csi.aws.com`) now manages "
            "EBS volumes"),
        (0, "A StorageClass (`ebs-sc`) tells the driver to create the volume"),
        (0, "A PersistentVolumeClaim requests the storage, and the Pod uses the claim"),
        (0, "This manifest needs the EBS CSI driver, for example on Amazon EKS. The kubeadm cluster of the lab uses "
            "the StorageClass `standard`")], size=15, after=8)
    yaml(s, 6.15, 1.50, 6.60, 5.15, "ebs-pvc-and-pod.yaml", EBS_POD, size=9)
    return s


def slide15(prs):
    s = new_slide(prs, "Using an NFS Volume")
    yaml(s, 0.55, 1.50, 6.90, 4.61, "pod-using-my-nfs-volume.yaml", NFS_POD, size=12)
    cards(s, 7.70, 1.55, 5.05, [
        ("nfs:", "The Pod mounts an NFS share directly. It needs no PersistentVolume."),
        ("server: 192.168.0.55", "An example address of an NFS server. Each node must reach the server."),
        ("path: \"/exports/assets\"", "The directory that the NFS server exports."),
        ("mountPath: /my-nfs", "The directory in the container. Each node needs the nfs-common package (the NFS client on Ubuntu).")], h=1.05)
    return s


def main():
    if os.path.exists(OUT) and "--force" not in sys.argv:
        sys.exit("%s exists. Bump the version; never overwrite a delivered deck." % OUT)
    check_old()
    prs = Presentation(SRC)
    keep_first(prs, 3)
    cover, agenda, outline = prs.slides[0], prs.slides[1], prs.slides[2]
    by_name = {sh.name: sh for sh in cover.shapes}
    two_lines(by_name["TextBox 1"], "Volumes: Attaching Disk", "Storage to Containers")
    set_only_run(by_name["TextBox 2"], "Week 7 · Lecture")
    by_name["TextBox 3"]._element.getparent().remove(by_name["TextBox 3"]._element)
    current_week(outline)
    old = [sh for sh in agenda.shapes if sh.name == "TextBox 3"][0]
    old._element.getparent().remove(old._element)
    bullets(agenda, 0.60, 1.75, 12.10, [
        (0, "Volumes"),
        (1, "emptyDir"),
        (1, "hostPath"),
        (1, "A Git repository in a volume"),
        (1, "NFS"),
        (0, "Managing configuration"),
        (0, "PersistentVolumes (PV) and PersistentVolumeClaims (PVC)"),
        (0, "StorageClass")], size=18, after=10)
    built = [cover, agenda, outline]
    for make in (slide4, slide5, slide6, slide7, slide8, slide9, slide10, slide11, slide12, slide13, slide14,
                 slide15):
        built.append(make(prs))
    total = len(built)
    for no, s in enumerate(built, 1):
        if no <= 3:
            for sh in s.shapes:
                if sh.has_text_frame and sh.text_frame.text.startswith("CLO835, Fall 2026"):
                    set_only_run(sh, "CLO835, Fall 2026     %d / %d" % (no, total))
        else:
            E.whale_and_footer(s, no, total)
    footer_guard(prs)
    finish(prs, "CLO835 Week 7 Lecture: Volumes, Attaching Disk Storage to Containers")
    E._sanitize_coords(prs)
    prs.save(OUT)
    print("wrote %s (%d slides)" % (OUT, total))


if __name__ == "__main__":
    main()
