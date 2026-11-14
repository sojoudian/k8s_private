# Lab Week 13 Submission

Please submit a report that demonstrates all the main points of Lab Week 13.
The lab recording demonstrates every step required for this assignment. You may watch the recording and follow it directly, step by step, to complete the lab. Make sure your submission includes your own screenshots, command outputs, and explanations as described below.

The Terraform configuration in Week 13 creates the same three Ubuntu 26.04 EC2 machines as Weeks 04 to 12.

## 1. Authentication

A user is an X509 certificate that the cluster CA signs. Kubernetes stores no users.
You must:
- Show kubectl auth whoami and the subject of the admin certificate.
- Show the error of kubectl get users, and explain it.
- Show /version answering without credentials and /api/v1/namespaces answering 403.
- Show the CertificateSigningRequest Pending, then Approved,Issued, and the subject of dev-user.crt.
- Show dev-user authenticated (auth whoami) but Forbidden to list pods.
- Explain how this maps to an IAM user on EKS.

## 2. ServiceAccounts

A Pod authenticates with the token of its ServiceAccount.
You must:
- Show the default and clo835 ServiceAccounts, and the decoded payload of the token.
- Show the 403 answer when curl-sa lists the Services with its token.

## 3. Roles and RoleBindings

A Role says what. A RoleBinding says who.
You must:
- Show the ServiceList after the service-reader Role and RoleBinding.
- Show what dev-user can and cannot do with the developer Role.
- Show kubectl auth can-i for both identities, and explain why a Role works in one namespace.

## 4. ClusterRoles and ClusterRoleBindings

A cluster-level resource needs a ClusterRoleBinding.
You must:
- Show the Forbidden answer with the RoleBinding, and the allowed answer with the ClusterRoleBinding.
- Show the default cluster roles and the binding of system:masters.
- Explain the role of super-admin.conf, and compare it with the creator of an EKS cluster.
- Show the clean-up and terraform destroy.

## Submission should include

- Name label on every screenshot
- Detailed explanation of commands being executed
- Highlight the output of commands executed

## Integrity Pledge

By submitting this assignment you affirm that you will not plagiarize, give or receive illegitimate help on assignments, papers or examinations. You will uphold fairness and honesty in your work and the work of others. Please read Seneca Academic Integrity policy for more details.
