# Lab Week 13 Submission

Please submit a report that demonstrates all the main points of Lab Week 13.
The lab recording demonstrates every step required for this assignment. You may watch the recording and follow it directly, step by step, to complete the lab. Make sure your submission includes your own screenshots, command outputs, and explanations as described below.

The Terraform configuration in Week 13 creates the same three Ubuntu 26.04 EC2 machines as Weeks 04 to 12.

## 1. Users and authentication

A Kubernetes user is a certificate that the cluster CA signed.
You must:
- Show kubectl auth whoami as kubernetes-admin.
- Show the approved CSR and the subject of dev-user.crt.
- Show kubectl auth whoami and the Forbidden error for dev-user, and explain the difference between authentication and authorization.

## 2. Roles and ServiceAccounts

A RoleBinding gives the rules of a Role to a user or a ServiceAccount, in one namespace.
You must:
- Show what dev-user can and cannot do after the developer Role, and kubectl auth can-i --list.
- Show the Forbidden answer of the API to the Pod, then the ServiceList after the service-reader Role.
- Show the two can-i answers for week13 and default, and explain them.
- Show the clean-up and terraform destroy.

## Submission should include

- Name label on every screenshot
- Detailed explanation of commands being executed
- Highlight the output of commands executed

## Integrity Pledge

By submitting this assignment you affirm that you will not plagiarize, give or receive illegitimate help on assignments, papers or examinations. You will uphold fairness and honesty in your work and the work of others. Please read Seneca Academic Integrity policy for more details.
