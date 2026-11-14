# Lab Week 12 Submission

Please submit a report that demonstrates all the main points of Lab Week 12.
The lab recording demonstrates every step required for this assignment. You may watch the recording and follow it directly, step by step, to complete the lab. Make sure your submission includes your own screenshots, command outputs, and explanations as described below.

The Terraform configuration in Week 12 creates the same three Ubuntu 26.04 EC2 machines as Weeks 04 to 10.

## 1. Arguments and ConfigMaps

args replace the CMD of the image. A ConfigMap keeps the configuration out of the manifest.
You must:
- Show the fortune-args log with the 2-second interval.
- Show the app-config ConfigMap and the three variables in config-env.
- Show the files of the ConfigMap volume, and APP_COLOR before and after the patch.
- Explain why the variable in config-env is still blue.

## 2. Secrets

A Secret is base64, not encrypted.
You must:
- Show the decoded DB_Password.
- Show DB_Password as a variable and DB_Host as a file, and the tmpfs mount.
- Show the password in plain text in etcd, and name two ways to protect it.
- Show the clean-up and terraform destroy.

## Submission should include

- Name label on every screenshot
- Detailed explanation of commands being executed
- Highlight the output of commands executed

## Integrity Pledge

By submitting this assignment you affirm that you will not plagiarize, give or receive illegitimate help on assignments, papers or examinations. You will uphold fairness and honesty in your work and the work of others. Please read Seneca Academic Integrity policy for more details.
