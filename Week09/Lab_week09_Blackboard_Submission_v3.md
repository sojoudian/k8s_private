# Lab Week 09: The Kubernetes Jobs that EKS Does for You

## Submission Instructions

Submit a report demonstrating your completion and understanding of all 7 sections of Lab Week 09.

The lab recording demonstrates the steps required to complete this assignment. You may follow the recording step by step. However, your submission must include your own screenshots, actual command outputs, and explanations for all required tasks.

## 1. Build the Cluster and Verify Its Status

The Week 09 Terraform configuration creates three Ubuntu 26.04 EC2 instances: one control-plane node and two worker nodes. The Kubernetes cluster initializes automatically at boot. On this cluster, you do the jobs that Amazon EKS does for you.

You must:

- Run terraform init and terraform apply.
- Run terraform output public_ips and terraform output private_ips, and show the addresses of all three nodes.
- Show an SSH session connected to the control-plane node.
- Run kubectl get nodes -o wide and show all three nodes in the Ready state.
- Run kubectl get pods -n kube-system and show the control-plane pods in the Running state.
- Explain which parts of this cluster AWS would run for you on EKS.

## 2. Inspect the Control Plane

On EKS, AWS runs the control plane, and you never see it. On this cluster, the control-plane node runs it as static Pods.

You must:

- Run sudo ls /etc/kubernetes/manifests and show the files.
- Run kubectl get pods -n kube-system -o wide | grep masternode.
- Run the kubectl get pod kube-scheduler-masternode command with the jsonpath output and show that the owner kind is Node.
- Explain what a static Pod is, and which component starts it.

## 3. Query the Cluster Database

Every object of the cluster is a key in etcd. EKS runs etcd for you across three Availability Zones.

You must:

- Set the ETCD variable, as the lab shows.
- Run etcdctl endpoint health and show the result.
- Run etcdctl member list -w table and show the result.
- Run etcdctl get /registry/namespaces --prefix --keys-only and show the keys.
- Explain why one etcd member gives no high availability.

## 4. Stop and Restore the Scheduler

On EKS, you never touch the scheduler. On this cluster, the scheduler is a file.

You must:

- Move kube-scheduler.yaml out of /etc/kubernetes/manifests and show that the scheduler Pod is gone.
- Create the no-scheduler Pod and show that it stays Pending with no node.
- Move the file back and show that the Pod reaches the Running state on a node.
- Explain why the Pod stays Pending while the scheduler is stopped.

## 5. Identity, Certificates, Upgrades, New Nodes, and Storage

A managed service does these jobs for you. On this cluster, they are your job.

You must:

- Run kubectl auth whoami and kubectl auth can-i delete nodes, and show the results.
- Run sudo kubeadm certs check-expiration and state when the certificates expire.
- Run sudo kubeadm upgrade plan 2>&1 | tail -15 and show the result.
- Run sudo kubeadm token create --print-join-command and show the result, with the token hidden.
- Run kubectl get csidrivers,storageclass and show the result.
- Explain how EKS identifies you, and how this cluster identifies you.
- Explain what EKS needs in order to create a PersistentVolume, and why this cluster cannot do this.

## 6. Compare the Pod Network and Drain a Node

On EKS, the VPC CNI gives each Pod a VPC IP address, and AWS drains a node of a managed node group for you.

You must:

- Create the kubia Deployment with four replicas and run kubectl rollout status.
- Run kubectl get pods -l app=kubia -o wide and show the Pod IP addresses.
- Run kubectl get nodes -o wide and show the node INTERNAL-IP addresses.
- Run kubectl cordon workernode2 and kubectl drain workernode2, then show all four Pods on workernode1.
- Run kubectl get nodes and show that workernode2 is SchedulingDisabled.
- Run kubectl uncordon workernode2 and show the result.
- Explain why the Pod IP addresses on this cluster differ from the node addresses, and what the VPC CNI changes on EKS.
- Explain the difference between cordon and drain.

## 7. Clean Up and Destroy the Cluster

At the end of the lab, remove the Kubernetes objects and destroy all three EC2 instances.

You must:

- Run bash cleanup_lab09.sh on the control-plane node.
- Run kubectl get pods,deployments | grep -E 'kubia|no-scheduler' and show that nothing is left.
- From the Week 09 directory on your own machine, run terraform state list and show the result.
- Run terraform destroy.
- Include the final Terraform output showing Destroy complete!.
- State the number of resources Terraform removed.
- Explain which tool does the job of Terraform on EKS, and what that tool creates.
- Explain what you pay for on this cluster, and what EKS adds to the cost.

## Submission Requirements

Your report must include all of the following:

- Your name clearly visible in every screenshot.
- Screenshots demonstrating the required commands and results in all 7 sections.
- Actual output from the commands you executed.
- Clear, detailed explanations of the commands, their purpose, and the results.
- Highlighted or clearly visible output where appropriate.
- Answers to every explanation question specified in the lab.

Use your own screenshots and outputs from your lab environment. Screenshots or outputs copied from the recording or another student's submission do not demonstrate your own work.

## Academic Integrity Pledge

By submitting this assignment, you affirm that you will not plagiarize or provide or receive unauthorized assistance on assignments, papers, or examinations. You agree to uphold fairness and honesty in your own work and in the work of others.

Please review the Seneca Academic Integrity Policy for further details.
