# -*- coding: utf-8 -*-
"""CLO835 Week 09 lab v2 - Managed vs Self-managed Kubernetes, in ONE workshop.

v1 had 3 workshops and 11 steps. The limit is now the size of the Week 03 and
Week 04 labs: at most Step 0 to Step 6. v2 keeps the jobs that EKS does for you
and that you do by hand on kubeadm: the control plane as static Pods, etcd, the
scheduler, certificates and upgrades, and the worker nodes (join and drain).

Outputs: Week09/Lab_week09_v2.pptx, Week09/localMachine_v2.sh,
Week09/Lab_week09_Blackboard_Submission_v2.md, ~/Documents/c/r/CLO835_Fall_2026/Week09/
Run from the project root. It is guarded, so importing it writes nothing.
"""
import sys

import lab_kubeadm as L

ETCD = [
  '$ ETCD="etcdctl --endpoints=https://127.0.0.1:2379 \\',
  '    --cacert=/etc/kubernetes/pki/etcd/ca.crt \\',
  '    --cert=/etc/kubernetes/pki/etcd/server.crt \\',
  '    --key=/etc/kubernetes/pki/etcd/server.key"',
]

SLIDES = [
 ("title", "Workshop 1 – The Kubernetes Jobs that EKS Does for You"),
 ("prereq",),
 ("cluster",),
 ("step", "The control plane runs as static Pods", "bash", [
  "# On EKS, AWS runs the control plane, and you never see it. Here the master runs it.",
  "# The kubelet of the master starts every file of this folder as a static Pod.",
  "$ sudo ls /etc/kubernetes/manifests",
  "$ kubectl get pods -n kube-system -o wide | grep masternode",
  " ",
  "# No Deployment owns these Pods. Their owner is the node itself.",
  "$ kubectl get pod kube-scheduler-masternode -n kube-system \\",
  "    -o jsonpath='{.metadata.ownerReferences[0].kind}{\"\\n\"}'",
  "# Node",
  ]),
 ("step", "etcd: the cluster database", "bash", [
  "# Every object of the cluster is a key in etcd. EKS runs etcd for you on three Availability Zones.",
  "# Here it is one Pod on one machine. Ask it directly, with its own certificates.",
  ] + ETCD + [
  "$ kubectl -n kube-system exec etcd-masternode -- $ETCD endpoint health",
  "$ kubectl -n kube-system exec etcd-masternode -- $ETCD member list -w table",
  "$ kubectl -n kube-system exec etcd-masternode -- $ETCD get /registry/namespaces --prefix --keys-only",
  " ",
  "# One member: no high availability. If this machine fails, the cluster stops.",
  ]),
 ("step", "You operate the control plane: stop the scheduler", "bash", [
  "# On EKS you never touch the scheduler. Here it is a file. Move the file away.",
  "$ sudo mv /etc/kubernetes/manifests/kube-scheduler.yaml /tmp/",
  "$ kubectl wait --for=delete pod/kube-scheduler-masternode -n kube-system --timeout=90s",
  "$ kubectl get pods -n kube-system -l component=kube-scheduler   # No resources found",
  " ",
  "# With no scheduler, a new Pod waits for a node.",
  "$ kubectl run no-scheduler --image=maziar/kubia:v1",
  "$ sleep 5; kubectl get pod no-scheduler -o wide                  # Pending, NODE <none>",
  " ",
  "# Put the file back. The scheduler starts, and it places the Pod.",
  "$ sudo mv /tmp/kube-scheduler.yaml /etc/kubernetes/manifests/",
  "$ kubectl wait --for=condition=Ready pod/no-scheduler --timeout=120s",
  "$ kubectl get pod no-scheduler -o wide                           # Running on a worker",
  ]),
 ("step", "Certificates, upgrades and new nodes are your job", "bash", [
  "# kubeadm made the certificates of the cluster. They expire one year after kubeadm init.",
  "$ sudo kubeadm certs check-expiration",
  " ",
  "# EKS upgrades the control plane for you. Here you plan the upgrade yourself.",
  "# It only reads. It changes nothing.",
  "$ sudo kubeadm upgrade plan 2>&1 | tail -15",
  " ",
  "# A managed node group joins by itself. A new EC2 worker would run this command:",
  "$ sudo kubeadm token create --print-join-command",
  "# kubeadm join 172.31.x.x:6443 --token ... --discovery-token-ca-cert-hash sha256:...",
  ]),
 ("step", "Drain a node, as AWS does for a managed node group", "bash", [
  "$ kubectl create deployment kubia --image=maziar/kubia:v1 --replicas=4",
  "$ kubectl rollout status deployment/kubia",
  "$ kubectl get pods -l app=kubia -o wide             # spread over both workers",
  " ",
  "# Maintenance on workernode2: stop new Pods there, then move its Pods away.",
  "$ kubectl cordon workernode2",
  "$ kubectl drain workernode2 --ignore-daemonsets --delete-emptydir-data --force",
  "$ kubectl get pods -l app=kubia -o wide             # all four on workernode1",
  "$ kubectl get nodes                                 # workernode2 SchedulingDisabled",
  " ",
  "# The maintenance is done. Let the node take Pods again.",
  "$ kubectl uncordon workernode2",
  "$ kubectl get nodes",
  ]),
 ("step", "Clean up", "bash", [
  "# ON THE MASTER - remove the Kubernetes objects.",
  "$ bash cleanup_lab09.sh",
  " ",
  "# Confirm that nothing is left.",
  "$ kubectl get pods,deployments | grep -E 'kubia|no-scheduler'",
  " ",
  "# ON YOUR OWN MACHINE - remove the three EC2 machines.",
  "L$ terraform destroy",
  " ",
  "# Always destroy. The Learner Lab budget is small.",
  ]),
 ("end", "Workshop 1 – The End"),
]

SCRIPT_HEAD = """#!/bin/bash
# CLO835 - Week 09 - Managed vs Self-managed Kubernetes.
# Run these ON THE MASTER NODE, section by section. Do NOT run the whole file.
#
# Terraform builds 3 machines: 1 control plane and 2 workers. The cluster forms
# itself at boot, the same way it did in Weeks 04 to 07. The lecture teaches
# what Amazon EKS runs for you. This lab does those jobs by hand.
#
# Each step matches one slide of Lab_week09_v2.pptx.
"""

CLEANUP = """kubectl delete deployment kubia 2>/dev/null
kubectl delete pod no-scheduler --now 2>/dev/null
kubectl uncordon workernode2 2>/dev/null
if [ -f /tmp/kube-scheduler.yaml ]; then sudo mv /tmp/kube-scheduler.yaml /etc/kubernetes/manifests/; fi

kubectl get pods,deployments | grep -E "kubia|no-scheduler\""""

BLACKBOARD = [
 ("The control plane you run yourself",
  "On EKS, AWS runs the control plane. On the kubeadm cluster, the master runs it as static Pods.",
  ["Show sudo ls /etc/kubernetes/manifests and the control-plane Pods on masternode.",
   "Show etcdctl endpoint health, member list and the namespace keys.",
   "Show the Pending Pod while the scheduler is away, and the same Pod Running after you put it back."]),
 ("Certificates, upgrades and worker nodes",
  "A managed service renews, upgrades, joins and drains for you. Here you do it.",
  ["Show kubeadm certs check-expiration, kubeadm upgrade plan and the join command.",
   "Show the four kubia Pods before and after the drain of workernode2.",
   "Explain the difference between cordon and drain.",
   "Explain three jobs that EKS does for you that you did by hand in this lab.",
   "Show the clean-up and terraform destroy."]),
]

if __name__ == "__main__":
    L.check_lines(SLIDES)
    L.make_lab("09", SLIDES, "Week09/Lab_week09_v2.pptx", SCRIPT_HEAD, script_path="Week09/localMachine_v2.sh")
    if "--no-repo" not in sys.argv:
        dst, files = L.make_repo_folder("09", "Managed vs Self-managed Kubernetes", CLEANUP, "Week09/localMachine_v2.sh")
        print("repo folder : %s (%d files)" % (dst, len(files)))
    L.blackboard_text("09", "The Terraform configuration in Week 09 creates the same three Ubuntu 26.04 EC2 "
                      "machines as Weeks 04 to 07. You run on them what EKS runs for you.",
                      BLACKBOARD, "Week09/Lab_week09_Blackboard_Submission_v2.md")
    print("blackboard  : Week09/Lab_week09_Blackboard_Submission_v2.md")
