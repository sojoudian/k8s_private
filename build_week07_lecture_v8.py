# -*- coding: utf-8 -*-
"""CLO835 Week 07 lecture v8 - lecture v7 with no clean-up text (the user, 2026-11-11).

The labs have no cleanup script now: terraform destroy removes the three machines. Lab v4 has no
clean-up step, so slide 18 drops "So the clean-up deletes the claim before the provisioner".
Every other slide is v7 (imported, not copied).

Output: Week07/Lecture_week07_v8.pptx. Run from the project root. It is guarded, so importing it
writes nothing. It refuses to overwrite the output, unless you give --force.
"""
import os
import sys

from pptx import Presentation

import build_week07_lecture_v7 as v7

VERSION = "v8"
OUT = "Week07/Lecture_week07_%s.pptx" % VERSION


def s_claim(prs):
    s = v7.new_slide(prs, "A Claim and a StorageClass on the Course Cluster")
    v7.bullets(s, 0.60, 1.75, 5.30, [
        (0, "A kubeadm cluster has no provisioner and no StorageClass at the start"),
        (0, "The lab installs the local-path provisioner (`rancher.io/local-path`). Its StorageClass `standard` is "
            "the default"),
        (0, "`WaitForFirstConsumer`: the provisioner waits for a Pod that uses the claim. Until then, the claim is "
            "Pending"),
        (0, "The provisioner creates a PersistentVolume: a directory on the node of the Pod"),
        (0, "`reclaimPolicy: Delete`: when you delete the claim, the provisioner deletes the PV and its directory")],
        size=15, after=8)
    v7.term(s, 6.15, 1.50, 6.60, "Lab Week 07, Step 5", v7.CLAIM, size=11, spacing=1.12)
    return s


assert v7.SLIDES.count(v7.s_claim) == 1
SLIDES = [s_claim if f is v7.s_claim else f for f in v7.SLIDES]


def main():
    if os.path.exists(OUT) and "--force" not in sys.argv:
        sys.exit("%s exists. Bump VERSION; never overwrite a delivered deck." % OUT)
    prs = Presentation(v7.SRC)
    v7.keep_first(prs, 3)
    v7.cover(prs, "Volumes: Attaching Disk", "Storage to Containers", 7)
    v7.agenda(prs, [
        (0, "What a volume is, and what it is for"),
        (0, "Volume types, ephemeral and persistent"),
        (1, "`emptyDir` and the mount settings"),
        (1, "The volume lifecycle"),
        (1, "An init container that clones a Git repository"),
        (1, "`hostPath` and NFS"),
        (0, "An introduction to claims and StorageClasses"),
        (0, "Useful commands, and how to find a problem"),
        (0, "How applications get their configuration")])
    v7.outline(prs, "Week 7: K8s – Volumes")
    built = [prs.slides[0], prs.slides[1], prs.slides[2]] + [make(prs) for make in SLIDES]
    v7.number_and_save(prs, built, "CLO835 Week 7 Lecture: Volumes, Attaching Disk Storage to Containers", OUT)


if __name__ == "__main__":
    main()
