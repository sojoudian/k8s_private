# Lab Week 14 Submission

Please submit a report that demonstrates all the main points of Lab Week 14.
The lab recording demonstrates every step required for this assignment. You may watch the recording and follow it directly, step by step, to complete the lab. Make sure your submission includes your own screenshots, command outputs, and explanations as described below.

The Terraform configuration in Week 14 creates the same three Ubuntu 26.04 EC2 machines as Weeks 04 to 13.

## 1. Working with Kubeconfig

A kubeconfig holds clusters, users and contexts. A context joins one cluster, one user and a namespace.
You must:
- Show kubectl config view, get-contexts and current-context.
- Show the viewer certificate issued, and the ClusterRoleBinding to the view role.
- Show use-context context-1: get pods allowed, create deployment Forbidden.
- Show set-context --current --namespace=dev in get-contexts.
- Show viewer.kubeconfig used with --kubeconfig, and the merged view with KUBECONFIG.
- Explain what changes when you switch context.

## 2. Horizontal Pod Autoscaling

The HPA adjusts the replicas of php-apache to keep the average CPU at 50 %.
You must:
- Show kubectl top nodes after the Metrics Server patch, and explain --kubelet-insecure-tls.
- Show kubectl get hpa before the load, while REPLICAS climbs, and after the load stops.
- Show the Metrics section of kubectl describe hpa, and calculate the desired replicas from it.
- Explain the control loop: query, calculate, update the Scale sub-resource.

## 3. Optional: Why IRSA Exists

A Pod on these nodes gets the IAM role of its node.
You must:
- Show aws sts get-caller-identity from the awscli Pod.
- Explain the risk, and how IRSA solves it on EKS.
- Show the clean-up and terraform destroy.

## Submission should include

- Name label on every screenshot
- Detailed explanation of commands being executed
- Highlight the output of commands executed

## Integrity Pledge

By submitting this assignment you affirm that you will not plagiarize, give or receive illegitimate help on assignments, papers or examinations. You will uphold fairness and honesty in your work and the work of others. Please read Seneca Academic Integrity policy for more details.
