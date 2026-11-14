# Lab Week 09 Submission

Please submit a report that demonstrates all the main points of Lab Week 09.
The lab recording demonstrates every step required for this assignment. You may watch the recording and follow it directly, step by step, to complete the lab. Make sure your submission includes your own screenshots, command outputs, and explanations as described below.

The Terraform configuration in Week 09 creates the same three Ubuntu 26.04 EC2 machines as Weeks 04 to 07. You run on them what EKS runs for you.

## 1. The control plane you run yourself

On EKS, AWS runs the control plane. On the kubeadm cluster, the master runs it as static Pods.
You must:
- Show sudo ls /etc/kubernetes/manifests and the control-plane Pods on masternode.
- Show etcdctl endpoint health, member list and the namespace keys.
- Show the Pending Pod while the scheduler is away, and the same Pod Running after you put it back.

## 2. Certificates, upgrades and worker nodes

A managed service renews, upgrades, joins and drains for you. Here you do it.
You must:
- Show kubeadm certs check-expiration, kubeadm upgrade plan and the join command.
- Show the four kubia Pods before and after the drain of workernode2.
- Explain the difference between cordon and drain.
- Explain three jobs that EKS does for you that you did by hand in this lab.
- Show the clean-up and terraform destroy.

## Submission should include

- Name label on every screenshot
- Detailed explanation of commands being executed
- Highlight the output of commands executed

## Integrity Pledge

By submitting this assignment you affirm that you will not plagiarize, give or receive illegitimate help on assignments, papers or examinations. You will uphold fairness and honesty in your work and the work of others. Please read Seneca Academic Integrity policy for more details.
