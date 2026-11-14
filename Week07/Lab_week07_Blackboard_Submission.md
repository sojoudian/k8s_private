# Lab Week 07 Submission

Please submit a report that demonstrates all the main points of Lab Week 07.
The lab recording demonstrates every step required for this assignment. You may watch the recording and follow it directly, step by step, to complete the lab. Make sure your submission includes your own screenshots, command outputs, and explanations as described below.

The Terraform configuration in Week 07 creates the same three Ubuntu 26.04 EC2 machines as Weeks 04 to 06. The master also runs an NFS server.

## 1. emptyDir: Two Containers, One Volume

The fortune Pod runs a writer and nginx. They share one emptyDir volume.
You must:
- Show kubectl get pod fortune -o wide with the Pod Running and READY 2/2.
- Show two curl calls to the Pod IP, 10 seconds apart, with two different fortunes.
- Show ls -l of /usr/share/nginx/html in web-server, and explain why 50x.html is not there.
- Show the failed write into the read-only mount.
- Show RESTARTS 1 after nginx -s stop, and the fortune file still served.
- Explain why a container restart keeps the volume, but a new Pod gets an empty one.

## 2. gitRepo and the Init Container

The gitRepo volume type is deprecated. An init container clones the repository into an emptyDir.
You must:
- Show the deprecation text of kubectl explain pod.spec.volumes.gitRepo.
- Show the Pod going from Init:0/1 to Running, and the logs of git-clone.
- Show curl to the Pod IP returning the website of the repository.
- Explain why the init container must finish before nginx starts.

## 3. hostPath: Data on One Node

A hostPath volume is a folder of the node, not of the Pod.
You must:
- Show the file still present after the Pod is deleted and started again on workernode1.
- Show the empty folder after the Pod moves to workernode2.
- Explain why hostPath is not suitable for a database in a cluster with many workers.

## 4. PersistentVolumeClaim and StorageClass

The local-path provisioner gives the cluster a default StorageClass, as the EBS CSI driver does on EKS.
You must:
- Show kubectl get storageclass with standard (default).
- Show the claim Pending before the Pod exists, and Bound after.
- Show the PV that the provisioner made, and the note.txt that survives a new Pod.
- Explain the difference between a volume in a Pod spec and a PersistentVolume.
- Explain WaitForFirstConsumer, and the Node Affinity of a local-path PV.

## 5. NFS Volume

The master exports /srv/nfs. Two Pods on two workers mount the same share.
You must:
- Show sudo exportfs -v on the master.
- Show kubectl get pods -o wide with nfs-pod-1 on workernode1 and nfs-pod-2 on workernode2.
- Show the file written by nfs-pod-1 and read by nfs-pod-2.
- Explain why an NFS volume, unlike hostPath, is not tied to a node.
- Show the clean-up and terraform destroy.

## Submission should include

- Name label on every screenshot
- Detailed explanation of commands being executed
- Highlight the output of commands executed

## Integrity Pledge

By submitting this assignment you affirm that you will not plagiarize, give or receive illegitimate help on assignments, papers or examinations. You will uphold fairness and honesty in your work and the work of others. Please read Seneca Academic Integrity policy for more details.
