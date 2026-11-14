# Lab Week 12 Submission

Please submit a report that demonstrates all the main points of Lab Week 12.
The lab recording demonstrates every step required for this assignment. You may watch the recording and follow it directly, step by step, to complete the lab. Make sure your submission includes your own screenshots, command outputs, and explanations as described below.

The Terraform configuration in Week 12 creates the same three Ubuntu 26.04 EC2 machines as Weeks 04 to 10.

## 1. Command-line Arguments

ENTRYPOINT and CMD of Docker are command and args in Kubernetes.
You must:
- Show the logs of fortune-args with "every 2 seconds".
- Show ubuntu-sleeper-pod going from Running to Completed, and its command and args.
- Explain which field replaces ENTRYPOINT and which replaces CMD.

## 2. Environment Variables

A variable is set per container in the Pod manifest.
You must:
- Show printenv INTERVAL in fortune-env, and the KUBERNETES_SERVICE variables.
- Explain the drawback of a hard-coded value.

## 3. ConfigMaps

A ConfigMap holds key/value pairs, created three ways and consumed three ways.
You must:
- Show the three ConfigMaps: from a literal, from a file and from a manifest.
- Show APP_COLOR, APP_MODE and INTERVAL in config-env.
- Show the files of the ConfigMap volume, and APP_COLOR changing to green in the file only.
- Show APP_MODE development in dev and production in prod, from one Pod manifest.
- Explain why a volume follows a change and an environment variable does not.

## 4. Secrets

A Secret is base64, not encrypted. A volume is safer than an environment variable.
You must:
- Show the Secret made imperatively, then declaratively, and the decoded password.
- Show the Secret volume files and the tmpfs mount.
- Show the child process and /proc/1/environ seeing the password.
- Show the service account files, and that no Secret object holds the token.
- Show the password in plain text in etcd, and explain encryption at rest.
- Show the clean-up and terraform destroy.

## Submission should include

- Name label on every screenshot
- Detailed explanation of commands being executed
- Highlight the output of commands executed

## Integrity Pledge

By submitting this assignment you affirm that you will not plagiarize, give or receive illegitimate help on assignments, papers or examinations. You will uphold fairness and honesty in your work and the work of others. Please read Seneca Academic Integrity policy for more details.
