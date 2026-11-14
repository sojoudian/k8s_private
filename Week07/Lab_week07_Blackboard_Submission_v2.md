# Lab Week 07 Submission

Please submit a report that demonstrates all the main points of Lab Week 07.
The lab recording demonstrates every step required for this assignment. You may watch the recording and follow it directly, step by step, to complete the lab. Make sure your submission includes your own screenshots, command outputs, and explanations as described below.

The Terraform configuration in Week 07 creates the same three Ubuntu 26.04 EC2 machines as Weeks 04 to 06.

## 1. emptyDir and the volume lifecycle

Two containers of one Pod share an emptyDir volume.
You must:
- Show two different fortunes from nginx, 10 seconds apart.
- Show that the volume shadows /usr/share/nginx/html.
- Show RESTARTS 1 after nginx -s stop, and the fortune still there.
- Show the new file time after you create the Pod again, and explain why.

## 2. An init container clones a repository

The init container replaces the deprecated gitRepo volume.
You must:
- Show the log of the git-clone init container.
- Show the first lines of app.js from nginx.

## 3. hostPath, PVC and StorageClass

A hostPath volume stays on one node. A claim gets a volume from a StorageClass.
You must:
- Show the note.txt file after the hostPath Pod is created again.
- Show the standard StorageClass, the Bound claim and its PersistentVolume.
- Explain the difference between a volume and a PersistentVolume.
- Show the clean-up and terraform destroy.

## Submission should include

- Name label on every screenshot
- Detailed explanation of commands being executed
- Highlight the output of commands executed

## Integrity Pledge

By submitting this assignment you affirm that you will not plagiarize, give or receive illegitimate help on assignments, papers or examinations. You will uphold fairness and honesty in your work and the work of others. Please read Seneca Academic Integrity policy for more details.
