# Lab Week 14 Submission

Please submit a report that demonstrates all the main points of Lab Week 14.
The lab recording demonstrates every step required for this assignment. You may watch the recording and follow it directly, step by step, to complete the lab. Make sure your submission includes your own screenshots, command outputs, and explanations as described below.

The Terraform configuration in Week 14 creates the same three Ubuntu 26.04 EC2 machines as Weeks 04 to 13.

## 1. Working with kubeconfig

A kubeconfig holds clusters, users and contexts. A context joins one cluster, one user and a namespace.
You must:
- Show the approved viewer certificate and the ClusterRoleBinding to the view role.
- Show use-context context-1: get pods allowed, create deployment Forbidden.
- Show get-contexts after you switch back to the admin.
- Explain what changes when you switch context.

## 2. Horizontal Pod Autoscaling

The HPA adjusts the replicas of php-apache to keep the average CPU at 50 %.
You must:
- Show kubectl top nodes, and explain --kubelet-insecure-tls.
- Show kubectl get hpa before the load and while REPLICAS climbs.
- Show the Metrics section of kubectl describe hpa, and calculate the desired replicas from it.
- Show terraform destroy.

## Submission should include

- Name label on every screenshot
- Detailed explanation of commands being executed
- Highlight the output of commands executed

## Integrity Pledge

By submitting this assignment you affirm that you will not plagiarize, give or receive illegitimate help on assignments, papers or examinations. You will uphold fairness and honesty in your work and the work of others. Please read Seneca Academic Integrity policy for more details.
