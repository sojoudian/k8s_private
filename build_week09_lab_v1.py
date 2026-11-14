# -*- coding: utf-8 -*-
"""CLO835 Week 09 - Managed vs Self-managed Kubernetes, on the kubeadm cluster.

The lecture (Week09/Week08_lecture_style_v5.pptx) teaches what Amazon EKS runs
for you: the control plane (API server, scheduler, etcd, high availability,
upgrades), the worker node options, the VPC CNI and the API endpoint, IAM plus
RBAC, and eksctl with CloudFormation. The students have no EKS, so this lab
does the same jobs by hand on the self-managed kubeadm cluster, and each step
names the EKS feature that it replaces.

Outputs: Week09/Lab_week09_v1.pptx, Week09/localMachine_v1.sh,
Week09/Lab_week09_Blackboard_Submission.md, ~/Documents/c/r/CLO835_Fall_2026/Week09/
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
 ("title", "Workshop 1 – The Control Plane You Run Yourself"),
 ("prereq",),
 ("cluster",),
 ("step", "The control plane runs as static Pods", "bash", [
  "# On EKS, AWS runs the control plane, and you never see it. Here the master runs it.",
  "# The kubelet of the master starts every file of this folder as a static Pod.",
  "$ sudo ls /etc/kubernetes/manifests",
  "# etcd.yaml  kube-apiserver.yaml  kube-controller-manager.yaml  kube-scheduler.yaml",
  " ",
  "$ kubectl get pods -n kube-system -o wide | grep masternode",
  " ",
  "# No Deployment owns these Pods. Their owner is the node itself.",
  "$ kubectl get pod kube-scheduler-masternode -n kube-system -o jsonpath='{.metadata.ownerReferences[0].kind}{\"\\n\"}'",
  "# Node",
  ]),
 ("step", "etcd: the cluster database", "bash", [
  "# Every object of the cluster is a key in etcd. EKS runs etcd for you on three Availability Zones.",
  "# Here it is one Pod on one machine. Ask it directly, with its own certificates.",
  ] + ETCD + [
  "$ kubectl -n kube-system exec etcd-masternode -- $ETCD endpoint health",
  "$ kubectl -n kube-system exec etcd-masternode -- $ETCD member list -w table",
  " ",
  "# The namespaces of the cluster, as etcd keys:",
  "$ kubectl -n kube-system exec etcd-masternode -- $ETCD get /registry/namespaces --prefix --keys-only",
  " ",
  "# One member: no high availability. If this machine fails, the cluster stops.",
  ]),
 ("step", "You operate the control plane: stop the scheduler", "bash", [
  "# On EKS you never touch the scheduler. Here it is a file. Move the file away.",
  "$ sudo mv /etc/kubernetes/manifests/kube-scheduler.yaml /tmp/",
  "$ sleep 20; kubectl get pods -n kube-system | grep scheduler     # nothing: it is gone",
  " ",
  "# With no scheduler, a new Pod waits for a node.",
  "$ kubectl run no-scheduler --image=maziar/kubia:v1",
  "$ sleep 5; kubectl get pod no-scheduler -o wide                  # Pending, NODE <none>",
  " ",
  "# Put the file back. The scheduler starts, and it places the Pod.",
  "$ sudo mv /tmp/kube-scheduler.yaml /etc/kubernetes/manifests/",
  "$ sleep 40; kubectl get pod no-scheduler -o wide                 # Running on a worker",
  "$ kubectl delete pod no-scheduler --now",
  ]),
 ("step", "Certificates and upgrades are your job", "bash", [
  "# kubeadm made the certificates of the cluster. They expire one year after kubeadm init.",
  "$ sudo kubeadm certs check-expiration",
  " ",
  "# EKS upgrades and patches the control plane for you. Here you plan the upgrade yourself.",
  "$ sudo kubeadm upgrade plan 2>&1 | tail -15",
  "# It only reads. It changes nothing.",
  ]),
 ("end", "Workshop 1 – The End"),

 ("title", "Workshop 2 – Worker Nodes You Run Yourself"),
 ("step", "How a self-managed worker joins", "bash", [
  "# A managed node group joins by itself. Our workers joined with a bootstrap token.",
  "$ sudo kubeadm token list",
  " ",
  "# The command that a new EC2 worker would run to join the cluster:",
  "$ sudo kubeadm token create --print-join-command",
  "# kubeadm join 172.31.x.x:6443 --token ... --discovery-token-ca-cert-hash sha256:...",
  " ",
  "$ kubectl get nodes -o wide",
  ]),
 ("step", "Drain a node, as AWS does for a managed node group", "bash", [
  "$ kubectl create deployment kubia --image=maziar/kubia:v1 --replicas=4",
  "$ kubectl rollout status deployment/kubia",
  "$ kubectl get pods -l app=kubia -o wide             # spread over both workers",
  " ",
  "# Maintenance on workernode2: stop new Pods there, then move its Pods away.",
  "$ kubectl cordon workernode2",
  "$ kubectl drain workernode2 --ignore-daemonsets --delete-emptydir-data",
  "$ kubectl get pods -l app=kubia -o wide             # all four on workernode1",
  "$ kubectl get nodes                                 # workernode2 SchedulingDisabled",
  " ",
  "# The maintenance is done. Let the node take Pods again.",
  "$ kubectl uncordon workernode2",
  "$ kubectl get nodes",
  ]),
 ("end", "Workshop 2 – The End"),

 ("title", "Workshop 3 – Networking and Access"),
 ("step", "Pod addresses: an overlay, not VPC addresses", "bash", [
  "# The VPC CNI of EKS gives every Pod a real VPC address. Flannel gives an overlay network.",
  "$ kubectl get nodes -o wide                         # INTERNAL-IP 172.31.x.x: the VPC",
  "$ kubectl get pods -l app=kubia -o wide             # IP 10.244.x.x: the overlay",
  "$ kubectl get pods -n kube-flannel -o wide          # one Flannel Pod per node",
  " ",
  "# The VXLAN device that carries Pod traffic between the nodes:",
  "$ ip -4 addr show flannel.1",
  ]),
 ("step", "The API endpoint is private", "bash", [
  "# The security group of this week does not open 6443 to the internet.",
  "$ kubectl cluster-info                              # https://172.31.x.x:6443, a private address",
  " ",
  "# ON YOUR OWN MACHINE: the public address of the master does not answer.",
  "L$ curl -sk --max-time 5 https://<MASTER-PUBLIC-IP>:6443/version; echo \"exit $?\"",
  "# exit 28 is a time-out. Like an EKS private endpoint, the API answers only inside the VPC.",
  " ",
  "# ON THE MASTER: the same call works.",
  "$ curl -sk https://localhost:6443/version",
  ]),
 ("step", "Who are you? Authentication and authorization", "bash", [
  "# EKS maps your IAM identity to a Kubernetes user. kubeadm gave us a client certificate.",
  "$ kubectl auth whoami",
  "# Username kubernetes-admin, Groups [kubeadm:cluster-admins system:authenticated]",
  " ",
  "# The kubeconfig holds the API address, the certificate and the context.",
  "$ kubectl config view --minify",
  " ",
  "# RBAC decides what the user can do. This group is bound to cluster-admin.",
  "$ kubectl get clusterrolebinding kubeadm:cluster-admins -o wide",
  "$ kubectl auth can-i '*' '*' --all-namespaces       # yes",
  ]),
 ("step", "Infrastructure as code: Terraform, not CloudFormation", "bash", [
  "# eksctl writes CloudFormation stacks. Our cluster is Terraform state on your laptop.",
  "L$ terraform state list",
  "L$ terraform output public_ips",
  " ",
  "# On EKS the control plane costs 0.10 USD per hour, and the workers are billed as well.",
  "# Here you pay only for the three EC2 machines, and you run everything yourself.",
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
 ("end", "Workshop 3 – The End"),
]

SCRIPT_HEAD = """#!/bin/bash
# CLO835 - Week 09 - Managed vs Self-managed Kubernetes.
# Run these ON THE MASTER NODE, section by section. Do NOT run the whole file.
#
# Terraform builds 3 machines: 1 control plane and 2 workers. The cluster forms
# itself at boot, the same way it did in Weeks 04 to 07. The lecture teaches
# what Amazon EKS runs for you. This lab does those jobs by hand.
#
# Each step matches one slide of Lab_week09_v1.pptx.
"""

CLEANUP = """kubectl delete deployment kubia 2>/dev/null
kubectl delete pod no-scheduler --now 2>/dev/null
kubectl uncordon workernode2 2>/dev/null
if [ -f /tmp/kube-scheduler.yaml ]; then sudo mv /tmp/kube-scheduler.yaml /etc/kubernetes/manifests/; fi

kubectl get pods,deployments | grep -E "kubia|no-scheduler\""""

BLACKBOARD = [
 ("The Control Plane You Run Yourself",
  "On EKS, AWS runs the control plane. On the kubeadm cluster, the master runs it as static Pods.",
  ["Show sudo ls /etc/kubernetes/manifests and the four control-plane Pods on masternode.",
   "Show etcdctl endpoint health, member list and the namespace keys.",
   "Show the Pending Pod while the scheduler is away, and the same Pod Running after you put it back.",
   "Show kubeadm certs check-expiration and kubeadm upgrade plan.",
   "Explain three jobs that EKS does for you that you did by hand in this workshop."]),
 ("Worker Nodes You Run Yourself",
  "A managed node group joins and drains its nodes by itself. Here you do it.",
  ["Show kubeadm token create --print-join-command.",
   "Show the four kubia Pods before the drain, on both workers, and after the drain, on workernode1.",
   "Show workernode2 as SchedulingDisabled, then Ready again after uncordon.",
   "Explain the difference between cordon and drain."]),
 ("Networking and Access",
  "Flannel gives the Pods an overlay network. The API endpoint of this cluster is private.",
  ["Show the node addresses (172.31.x.x) and the Pod addresses (10.244.x.x).",
   "Show the time-out of the call to port 6443 from your own machine, and the answer on the master.",
   "Show kubectl auth whoami and the cluster role binding of kubeadm:cluster-admins.",
   "Show terraform state list.",
   "Explain how the EKS VPC CNI differs from Flannel, and how IAM and RBAC share the work on EKS.",
   "Show the clean-up and terraform destroy."]),
]

if __name__ == "__main__":
    L.check_lines(SLIDES)
    L.make_lab("09", SLIDES, "Week09/Lab_week09_v1.pptx", SCRIPT_HEAD, script_path="Week09/localMachine_v1.sh")
    if "--no-repo" not in sys.argv:
        dst, files = L.make_repo_folder("09", "Managed vs Self-managed Kubernetes", CLEANUP, "Week09/localMachine_v1.sh")
        print("repo folder : %s (%d files)" % (dst, len(files)))
    L.blackboard_text("09", "The Terraform configuration in Week 09 creates the same three Ubuntu 26.04 EC2 "
                      "machines as Weeks 04 to 07. You run on them what EKS runs for you.",
                      BLACKBOARD, "Week09/Lab_week09_Blackboard_Submission.md")
    print("blackboard  : Week09/Lab_week09_Blackboard_Submission.md")
