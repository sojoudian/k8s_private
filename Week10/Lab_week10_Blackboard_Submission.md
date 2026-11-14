# Lab Week 10 Submission

Please submit a report that demonstrates all the main points of Lab Week 10.
The lab recording demonstrates every step required for this assignment. You may watch the recording and follow it directly, step by step, to complete the lab. Make sure your submission includes your own screenshots, command outputs, and explanations as described below.

The Terraform configuration in Week 10 creates the same three Ubuntu 26.04 EC2 machines as Weeks 04 to 09.

## 1. hostPath

MongoDB keeps its data in a hostPath folder of workernode1.
You must:
- Show the document in mystore after the Pod is deleted and created again on workernode1.
- Show the empty result after the Pod moves to workernode2.
- Show the hostPath volumes of a kube-proxy Pod.
- Explain why hostPath is not suitable for database storage in a multi-node cluster.

## 2. PersistentVolumes and Claims

An administrator posts a PV. A user claims it. A Pod uses the claim.
You must:
- Show the PV Available, then Bound to mongodb-pvc.
- Show the document that survives a new Pod with the same claim.
- Show the PV Released after the claim is deleted, and explain the Retain policy.
- Explain how a claim decouples the Pod from the storage technology.

## 3. StorageClasses and Dynamic Provisioning

The local-path provisioner makes a PV for each claim.
You must:
- Show kubectl get storageclasses before and after the install.
- Show the claim redis-data Pending, then Bound, and the PV that the provisioner made.
- Show the key foo still present after the Redis Pod is deleted.
- Explain WaitForFirstConsumer, and why a local-path PV keeps the Pod on one node.

## 4. StatefulSets

The kubia StatefulSet runs two pets with stable names, stable DNS names and their own storage.
You must:
- Show the pets start in order, and the two claims data-kubia-0 and data-kubia-1.
- Show the greeting POSTed to kubia-0, and kubia-0 still holding it after it is deleted.
- Show the dig SRV answer of the headless Service.
- Show the collated data of all pets after the update to maziar/kubia-pet-peers.
- Explain why a Deployment cannot give these guarantees.
- Show the clean-up and terraform destroy.

## Submission should include

- Name label on every screenshot
- Detailed explanation of commands being executed
- Highlight the output of commands executed

## Integrity Pledge

By submitting this assignment you affirm that you will not plagiarize, give or receive illegitimate help on assignments, papers or examinations. You will uphold fairness and honesty in your work and the work of others. Please read Seneca Academic Integrity policy for more details.
