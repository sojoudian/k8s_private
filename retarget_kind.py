# -*- coding: utf-8 -*-
"""CLO835 - remove kind (Kubernetes in Docker) from the current decks.

The course labs build a kubeadm cluster on EC2: 1 master and 2 workers. These
decks still named kind. Each deck is read and never written; the output is
the next version of it. Only the named text changes.

Run from the project root:   python retarget_kind.py
It is guarded, so importing it writes nothing.
"""
import sys
from retarget_accounts import retarget

WEEK04 = [
    ("Why orchestration · what K8s is · architecture · networking · and a hands-on cluster with kind.",
     "Why orchestration · what K8s is · architecture · networking · and a hands-on cluster with kubeadm."),
    ("Hands-on with kind", "Hands-on with kubeadm"),
    ("Spin up a local cluster, deploy nginx, expose it, and inspect it with kubectl. End-to-end in one workshop.",
     "Build a 3-node cluster on EC2, deploy nginx, expose it, and inspect it with kubectl. End-to-end in one workshop."),
    ("The same manifests run on your laptop (kind/minikube), in any cloud (EKS, GKE, AKS), on-prem, and at the edge.",
     "The same manifests run on your own VMs (kubeadm), in any cloud (EKS, GKE, AKS), on-prem, and at the edge."),
    ("    server: https://127.0.0.1:6443", "    server: https://172.31.16.10:6443"),
    ("CURRENT   NAME       CLUSTER", "CURRENT   NAME                          CLUSTER"),
    ("*         kind-kind  kind-kind", "*         kubernetes-admin@kubernetes   kubernetes"),
    ("Local (kind / minikube) or remote (EKS / GKE / AKS). Today we'll use kind.",
     "Self-built (kubeadm) or managed (EKS / GKE / AKS). Today we use kubeadm on EC2."),
    ("kubectl + kind on your laptop", "kubectl + kubeadm on EC2"),
    ("In this course: we'll use kind locally for Week 4–7, then EKS for Week 8.",
     "In this course: kubeadm on three EC2 machines (1 master, 2 workers) for the labs."),
]

HOSTPATH = [
    ('Used as a persistent volume in simulated clusters like "kind" and "minikube"',
     "Used as a persistent volume for single-node tests only"),
]

DECKS = [
    ("Week04/FINAL/Week04.pptx", "Week04/FINAL/Week04_v2.pptx", WEEK04),
    ("finalWork/Week04.pptx", "finalWork/Week04_v2.pptx", WEEK04),
    ("Week10/Week09_lecture_style_v5.pptx", "Week10/Week09_lecture_style_v6.pptx", HOSTPATH),
    ("CLO835_Workshops_Lab_v1.pptx", "CLO835_Workshops_Lab_v2.pptx", HOSTPATH),
    ("finalWork/Week09.pptx", "finalWork/Week09_v2.pptx", HOSTPATH),
    ("finalWork/Lab07.pptx", "finalWork/Lab07_v2.pptx", HOSTPATH),
]

if __name__ == "__main__":
    bad = 0
    for src, out, pairs in DECKS:
        done, missed = retarget(src, out, pairs)
        print("%-38s -> %s" % (src, out))
        for old, n in done.items():
            print("    %2d x  %s" % (n, old[:70]))
        if missed:
            bad += 1
            print("    NOT FOUND:", [m[:50] for m in missed])
    sys.exit(1 if bad else 0)
