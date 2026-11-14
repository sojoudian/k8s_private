# Lab Week 09 Submission

Please submit a report that demonstrates all the main points of Lab Week 09.
The lab recording demonstrates every step required for this assignment. You may watch the recording and follow it directly, step by step, to complete the lab. Make sure your submission includes your own screenshots, command outputs, and explanations as described below.

The Terraform configuration in Week 09 creates the same three Ubuntu 26.04 EC2 machines as Weeks 04 to 07. You run on them what EKS runs for you.

## 1. The Control Plane You Run Yourself

On EKS, AWS runs the control plane. On the kubeadm cluster, the master runs it as static Pods.
You must:
- Show sudo ls /etc/kubernetes/manifests and the four control-plane Pods on masternode.
- Show etcdctl endpoint health, member list and the namespace keys.
- Show the Pending Pod while the scheduler is away, and the same Pod Running after you put it back.
- Show kubeadm certs check-expiration and kubeadm upgrade plan.
- Explain three jobs that EKS does for you that you did by hand in this workshop.

## 2. Worker Nodes You Run Yourself

A managed node group joins and drains its nodes by itself. Here you do it.
You must:
- Show kubeadm token create --print-join-command.
- Show the four kubia Pods before the drain, on both workers, and after the drain, on workernode1.
- Show workernode2 as SchedulingDisabled, then Ready again after uncordon.
- Explain the difference between cordon and drain.

## 3. Networking and Access

Flannel gives the Pods an overlay network. The API endpoint of this cluster is private.
You must:
- Show the node addresses (172.31.x.x) and the Pod addresses (10.244.x.x).
- Show the time-out of the call to port 6443 from your own machine, and the answer on the master.
- Show kubectl auth whoami and the cluster role binding of kubeadm:cluster-admins.
- Show terraform state list.
- Explain how the EKS VPC CNI differs from Flannel, and how IAM and RBAC share the work on EKS.
- Show the clean-up and terraform destroy.

## Submission should include

- Name label on every screenshot
- Detailed explanation of commands being executed
- Highlight the output of commands executed

## Integrity Pledge

By submitting this assignment you affirm that you will not plagiarize, give or receive illegitimate help on assignments, papers or examinations. You will uphold fairness and honesty in your work and the work of others. Please read Seneca Academic Integrity policy for more details.
