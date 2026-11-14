# Lab Week 07: Volumes

## Submission Instructions

Submit a report demonstrating your completion and understanding of all 7 sections of Lab Week 07.

The lab recording demonstrates the steps required to complete this assignment. You may follow the recording step by step. However, your submission must include your own screenshots, actual command outputs, and explanations for all required tasks.

## 1. Build the Cluster and Verify Its Status

The Week 07 Terraform configuration creates three Ubuntu 26.04 EC2 instances, as in Weeks 04 to 06: one master node and two worker nodes. The Kubernetes cluster initializes automatically at boot.

You must:

- Run terraform init and terraform apply.
- Run terraform output public_ips and terraform output private_ips, and show the addresses of all three nodes.
- Show an SSH session connected to the master node.
- Run kubectl get nodes -o wide and show all three nodes in the Ready state.
- Run kubectl get pods -n kube-system and show the system Pods in the Running state.

## 2. Two Containers Share One emptyDir

Two containers of one Pod share an emptyDir volume. html-generator writes a new fortune every 10 seconds, and nginx serves the same directory.

You must:

- Create fortune-pod.yaml and display its contents.
- Apply the manifest using kubectl apply -f fortune-pod.yaml, and run the kubectl wait command for the fortune Pod.
- Run the two curl commands and show two different fortunes, 10 seconds apart.
- Run kubectl exec fortune -c web-server -- ls /usr/share/nginx/html and show that only the fortune file is there.
- Explain why the old files of /usr/share/nginx/html are not visible.
- Explain how the two containers share one file, with two different mount paths.

## 3. An emptyDir Lives as Long as the Pod

A container restart keeps the volume. A new Pod gets a new, empty volume.

You must:

- Stop nginx with kubectl exec fortune -c web-server -- nginx -s stop.
- Run kubectl get pod fortune and show RESTARTS 1.
- Run the curl command again and show that the fortune is still there.
- Delete the fortune Pod, apply the manifest again, and run the kubectl wait command.
- Run the stat command and show the time of index.html.
- Explain why index.html has a new time.
- Explain which volume types end with the Pod, and which volume types have data that stays after the Pod.

## 4. An Init Container Clones a Repository

The gitRepo volume type is deprecated, and Kubernetes turns it off by default. An init container clones the repository into an emptyDir volume.

You must:

- Create gitrepo-volume-pod.yaml and display its contents.
- Apply the manifest using kubectl apply -f gitrepo-volume-pod.yaml, and run the kubectl wait command.
- Run kubectl logs gitrepo-volume-pod -c git-clone and show the log of the init container.
- Run the curl command and show the first lines of app.js from nginx.
- Explain why args starts with clone and not with git.
- Explain why a new commit in the repository needs a new Pod.

## 5. hostPath Data Stays on One Node

A hostPath volume mounts a directory of the node into the Pod. The data stays on that node.

You must:

- Create hostpath-pod.yaml and display its contents.
- Apply the manifest using kubectl apply -f hostpath-pod.yaml, and run the kubectl wait command.
- Write the date to /data/note.txt with the kubectl exec command.
- Delete the hostpath-pod Pod, apply the manifest again, and run the kubectl wait command.
- Run kubectl exec hostpath-pod -- cat /data/note.txt and show the same date.
- Explain why this manifest needs the nodeSelector.
- Explain one security risk of a hostPath volume.

## 6. A PersistentVolumeClaim and a StorageClass

A claim asks for storage. The StorageClass standard and its provisioner create a PersistentVolume for the claim.

You must:

- Install the local-path provisioner with the kubectl apply command.
- Run kubectl get storageclass and show the default StorageClass standard.
- Create my-claim.yaml and display its contents.
- Apply the manifest using kubectl apply -f my-claim.yaml, and run the kubectl wait command for the pod-using-my-claim Pod.
- Run kubectl get pvc,pv and show the Bound claim and its PersistentVolume.
- Write to /my-data/note.txt and read the file again with the two kubectl exec commands.
- Explain the difference between a volume and a PersistentVolume.
- Explain what WaitForFirstConsumer means for the claim.

## 7. Clean Up and Destroy the Cluster

At the end of the lab, remove the Kubernetes objects and destroy all three EC2 instances.

You must:

- Run bash cleanup_lab07.sh on the master node.
- Run kubectl get pods,pvc,pv and show that nothing is left.
- From the Week07 directory on your own machine, run terraform destroy.
- Include the final Terraform output showing Destroy complete!.
- State the number of resources Terraform removed.
- Explain why the clean-up deletes the claim before it deletes the provisioner.

## Submission Requirements

Your report must include all of the following:

- Your name clearly visible in every screenshot.
- Screenshots demonstrating the required commands and results in all 7 sections.
- Actual output from the commands you executed.
- Clear, detailed explanations of the commands, their purpose, and the results.
- Highlighted or clearly visible output where appropriate.
- Answers to every explanation question specified in the lab.

Important: Use your own screenshots and outputs from your lab environment. Screenshots or outputs copied from the recording or another student's submission do not demonstrate your own work.
