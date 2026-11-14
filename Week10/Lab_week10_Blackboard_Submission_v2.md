# Lab Week 10 Submission

Please submit a report that demonstrates all the main points of Lab Week 10.
The lab recording demonstrates every step required for this assignment. You may watch the recording and follow it directly, step by step, to complete the lab. Make sure your submission includes your own screenshots, command outputs, and explanations as described below.

The Terraform configuration in Week 10 creates the same three Ubuntu 26.04 EC2 machines as Weeks 04 to 09.

## 1. PersistentVolumes and claims

An administrator makes a PersistentVolume. A user claims it.
You must:
- Show the PV and the PVC, both Bound.
- Show note.txt read by a new writer Pod after you delete the first one.
- Explain the Retain reclaim policy.

## 2. StorageClasses and StatefulSets

A StorageClass makes a volume for each claim. A StatefulSet gives each pet a stable identity.
You must:
- Show the standard StorageClass.
- Show kubia-0 and kubia-1, their claims and their PVs.
- Show the data of kubia-0 before and after you delete the Pod.
- Show the DNS answer for kubia-0.kubia.default.svc.cluster.local.
- Explain why a Deployment cannot give this identity to its Pods.
- Show the clean-up and terraform destroy.

## Submission should include

- Name label on every screenshot
- Detailed explanation of commands being executed
- Highlight the output of commands executed

## Integrity Pledge

By submitting this assignment you affirm that you will not plagiarize, give or receive illegitimate help on assignments, papers or examinations. You will uphold fairness and honesty in your work and the work of others. Please read Seneca Academic Integrity policy for more details.
