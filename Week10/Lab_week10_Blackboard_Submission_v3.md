# Lab Week 10: Persistent Storage and StatefulSets

## Submission Instructions

Submit a report demonstrating your completion and understanding of all 7 sections of Lab Week 10.

The lab recording demonstrates the steps required to complete this assignment. You may follow the recording step by step. However, your submission must include your own screenshots, actual command outputs, and explanations for all required tasks.

## 1. Build the Cluster and Verify Its Status

The Week 10 Terraform configuration creates three Ubuntu 26.04 EC2 instances, as in Weeks 04 to 09: one control-plane node and two worker nodes. The Kubernetes cluster initializes automatically at boot.

You must:

- Run terraform init and terraform apply.
- Run terraform output public_ips and terraform output private_ips, and show the addresses of all three nodes.
- Show an SSH session connected to the control-plane node.
- Run kubectl get nodes -o wide and show all three nodes in the Ready state.
- Run kubectl get pods -n kube-system and show the control-plane pods in the Running state.
- Explain why this cluster has no StorageClass at the start of the lab.

## 2. Create a PersistentVolume and a Claim

An administrator creates a PersistentVolume. A user claims it with a PersistentVolumeClaim. Use localMachine.sh to create both from a manifest.

You must:

- Create pv-pvc.yaml and display its contents.
- Apply the manifest using kubectl apply -f pv-pvc.yaml.
- Run the kubectl wait command for the data-pvc claim.
- Run kubectl get pv,pvc and show that both are Bound.
- Explain what the Retain reclaim policy does.
- Explain what the nodeAffinity block does in this PersistentVolume.

## 3. Show That the Data Outlives the Pod

A Pod names the claim, not the storage. The data stays when the Pod goes.

You must:

- Create writer.yaml and display its contents.
- Apply the manifest and wait until the writer Pod is Ready.
- Run kubectl get pod writer -o wide and identify the node.
- Write the date to /data/note.txt in the writer Pod.
- Delete the writer Pod, then create it again.
- Run kubectl exec writer -- cat /data/note.txt and show the same data.
- Explain why the new Pod reads the same data.
- Explain why the Pod manifest names the claim and not the storage.

## 4. Provision Volumes with a StorageClass

A StorageClass makes a volume for each claim. The control-plane node already holds the provisioner manifest.

You must:

- Run kubectl apply -f local-path-storage.yaml.
- Run the kubectl rollout status command for the local-path-provisioner Deployment.
- Run kubectl get storageclass and show the default StorageClass.
- Explain what WaitForFirstConsumer means.
- Explain what the EBS CSI driver does on EKS, and what the local-path provisioner does on this cluster.

## 5. Create a StatefulSet and Its Headless Service

A StatefulSet gives each Pod a stable identity. A headless Service has no cluster IP address.

You must:

- Create the headless Service using the kubectl create service clusterip command.
- Create kubia-statefulset.yaml and display its contents.
- Apply the manifest using kubectl apply -f kubia-statefulset.yaml.
- Run kubectl rollout status statefulset/kubia and show that the rollout completes.
- Run kubectl get pods -l app=kubia -o wide and kubectl get pvc,pv.
- Identify the claim and the PersistentVolume of each Pod.
- Explain why kubia-0 starts before kubia-1.
- Explain what volumeClaimTemplates does.

## 6. Show the Identity of a Pet and Discover Its Peers

A pet keeps its name, its data and its DNS name. A clustered application finds its peers through DNS.

You must:

- Start kubectl proxy, write data to kubia-0 with the POST command, and read it with the curl command.
- Delete the kubia-0 Pod and wait until the new kubia-0 is Ready.
- Read the data of kubia-0 again and show that it is the same.
- Create the dnstest Pod and wait until it is Ready.
- Run the nslookup command for kubia-0.kubia.default.svc.cluster.local and show the result.
- Run the nslookup command for kubia.default.svc.cluster.local and show the addresses of both Pods.
- Run nslookup -type=SRV for kubia.default.svc.cluster.local and show the result.
- Explain what the new kubia-0 keeps, and what can change.
- Explain why a Deployment cannot give this identity to its Pods.
- Explain what the name of a headless Service returns, and how an application uses SRV records to find its peers.

## 7. Clean Up and Destroy the Cluster

At the end of the lab, remove the Kubernetes objects and destroy all three EC2 instances.

You must:

- Run bash cleanup_lab10.sh on the control-plane node.
- Run kubectl get pods,pvc,pv and show that nothing is left.
- From the Week 10 directory on your own machine, run terraform destroy.
- Include the final Terraform output showing Destroy complete!.
- State the number of resources Terraform removed.
- Explain why the clean-up deletes the claims before it deletes the provisioner.

## Submission Requirements

Your report must include all of the following:

- Your name clearly visible in every screenshot.
- Screenshots demonstrating the required commands and results in all 7 sections.
- Actual output from the commands you executed.
- Clear, detailed explanations of the commands, their purpose, and the results.
- Highlighted or clearly visible output where appropriate.
- Answers to every explanation question specified in the lab.

Important: Use your own screenshots and outputs from your lab environment. Screenshots or outputs copied from the recording or another student's submission do not demonstrate your own work.
