# -*- coding: utf-8 -*-
"""CLO835 Week 10 lecture v12 - lecture v11 with no clean-up text (the user, 2026-11-11).

The labs have no cleanup script now: terraform destroy removes the three machines. Lab v5 Step 6
is "Destroy the cluster", so:
- Slide 23 drops the bullet on the order of the clean-up.
- Slide 37 (Lab Week 10 at a Glance): Step 6 is "Destroy the cluster", with no lecture slide.
Every other slide is v11 (imported, not copied).

Output: Week10/Lecture_week10_v12.pptx. Run from the project root. It is guarded, so importing it
writes nothing. It refuses to overwrite the output, unless you give --force.
"""
import os
import sys

from pptx import Presentation

import build_week08 as E
import build_week10_lecture_v11 as v11

VERSION = "v12"
OUT = "Week10/Lecture_week10_%s.pptx" % VERSION


def s_course(prs):
    s = v11.new_slide(prs, "Storage on the Course Cluster")
    v11.bullets(s, 0.60, 1.62, 12.10, [
        (0, "kubeadm installs no provisioner, so a new cluster has no StorageClass"),
        (0, "The lab installs the local-path provisioner. It makes a directory on a node for each claim"),
        (0, "Its StorageClass `standard` is the default, with `WaitForFirstConsumer` and `reclaimPolicy: Delete`"),
        (0, "A claim with no class gets `standard`"),
        (0, "A static `hostPath` or `local` PV needs `nodeAffinity`, so that its Pods run on the node with the data"),
        (0, "On Amazon EKS (Week 9), the EBS CSI driver is the provisioner, and the storage is an EBS volume")],
        size=15, after=5, h=3.45)
    v11.term(s, 0.60, 5.05, 12.10, "Lab Week 10, Step 3", v11.STEP3, size=11, spacing=1.05)
    return s


def s_lab(prs):
    s = v11.new_slide(prs, "Lab Week 10 at a Glance")
    end = v11.grid(s, 0.60, v11.TOP + 0.10, [2.20, 6.70, 3.20], [
        ["Lab step", "What you do", "Lecture slides"],
        ["Step 1", "Create the PV `data-pv` and the claim `data-pvc`", "11, 13, 14, 16, 17"],
        ["Step 2", "Show that the data stays after the Pod and the claim", "13, 14, 17, 18"],
        ["Step 3", "Install the provisioner and the StorageClass `standard`", "21, 23"],
        ["Step 4", "Create the StatefulSet `kubia` and its headless Service", "14, 29, 30, 31"],
        ["Step 5", "Show the identity of a Pod, its DNS name and the SRV records", "26, 28, 29, 33"],
        ["Step 6", "Destroy the cluster", "-"]], row_h=0.55, size=14)
    v11.rich(s, 0.60, end + 0.25, 12.10, 0.75, "Not in the lab: NFS, MySQL replication, the collection of the data "
             "of the peers, the update settings of slide 32 and the optional topics.", size=14, color=E.MUTED)
    return s


assert v11.SLIDES.count(v11.s_course) == 1 and v11.SLIDES.count(v11.s_lab) == 1
SLIDES = [{v11.s_course: s_course, v11.s_lab: s_lab}.get(f, f) for f in v11.SLIDES]


def main():
    if os.path.exists(OUT) and "--force" not in sys.argv:
        sys.exit("%s exists. Bump VERSION; never overwrite a delivered deck." % OUT)
    prs = Presentation(v11.SRC)
    v11.keep_first(prs, 3)
    v11.cover(prs, "PV, PVC, StorageClass", "and StatefulSets", 10)
    v11.agenda(prs, [
        (0, "`hostPath`: data on one node"),
        (0, "PersistentVolumes and claims"),
        (1, "Access modes, phases and reclaim policies"),
        (0, "StorageClasses and dynamic provisioning"),
        (1, "Storage on the course cluster, and a Pending claim"),
        (0, "StatefulSets"),
        (1, "Headless Services"),
        (1, "Updates and ordinals"),
        (1, "How Pods find their peers")])
    v11.outline(prs, "Week 10: K8s – StorageClasses & StatefulSets")
    built = [prs.slides[0], prs.slides[1], prs.slides[2]] + [make(prs) for make in SLIDES]
    v11.number_and_save(prs, built, "CLO835 Week 10 Lecture: PV, PVC, StorageClass and StatefulSets", OUT)


if __name__ == "__main__":
    main()
