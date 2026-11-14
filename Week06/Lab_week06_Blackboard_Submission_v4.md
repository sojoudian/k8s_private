# Lab Week 06 Submission

Please submit a report that demonstrates all the main points of Lab Week 06.
The lab recording demonstrates every step required for this assignment. You may watch the recording and follow it directly, step by step, to complete the lab. Make sure your submission includes your own screenshots, command outputs, and explanations as described below.

The Terraform configuration in Week 06 creates the same three Ubuntu 26.04 EC2 machines as Weeks 04 and 05.

## 1. Rollouts

A Deployment rolls out a new image with a new ReplicaSet, and it can roll back.
You must:
- Show the Deployment, its ReplicaSet and its 3 Pods.
- Show the two ReplicaSets after the rollout to maziar/kubia:v2.
- Show the rollout history before and after the undo, and explain why revision 1 becomes revision 3.

## 2. Labels

A ReplicaSet finds its Pods by label.
You must:
- Show the Pods with their labels.
- Show the new Pod that the ReplicaSet makes after you change the label of one Pod.
- Explain why the re-labelled Pod has no owner.

## 3. Services

A Service gives the Pods one stable name and address.
You must:
- Show the ClusterIP Service and its 3 endpoints.
- Show the client calls to http://kubia and to the full DNS name.
- Show the NodePort page from the public address of each of the three nodes.
- Show the clean-up and terraform destroy.

## Submission should include

- Name label on every screenshot
- Detailed explanation of commands being executed
- Highlight the output of commands executed

## Integrity Pledge

By submitting this assignment you affirm that you will not plagiarize, give or receive illegitimate help on assignments, papers or examinations. You will uphold fairness and honesty in your work and the work of others. Please read Seneca Academic Integrity policy for more details.
