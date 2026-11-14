# Lab Week 06: Rollouts, Labels, and Services

## Submission Instructions

Submit a report demonstrating your completion and understanding of all 7 sections of Lab Week 06.

The lab recording demonstrates the steps required to complete this assignment. You may follow the recording step by step. However, your submission must include your own screenshots, actual command outputs, and explanations for all required tasks.

## 1. Build the Cluster and Verify Its Status

The Week 06 Terraform configuration creates three Ubuntu 26.04 EC2 instances, as in Weeks 04 and 05: one control-plane node and two worker nodes. The Kubernetes cluster initializes automatically at boot.

You must:

- Run terraform init and terraform apply.
- Run terraform output public_ips and terraform output private_ips, and show the addresses of all three nodes.
- Show an SSH session connected to the control-plane node.
- Run kubectl get nodes -o wide and show all three nodes in the Ready state.
- Run kubectl get pods -n kube-system and show the control-plane pods in the Running state.
- Explain how the cluster forms at boot without a kubeadm command from you.

## 2. Create a Deployment from a Manifest

A Deployment manages a ReplicaSet, and the ReplicaSet manages the Pods. Use localMachine.sh to create the Deployment from a manifest.

You must:

- Create deployment.yaml and display its contents.
- Apply the manifest using kubectl apply -f deployment.yaml.
- Run kubectl rollout status deployment/kubia and show that the rollout completes.
- Run kubectl get deploy,rs,pods -o wide and identify the Deployment, the ReplicaSet, and the three Pods.
- Explain which object creates the Pods, and how the Pod names show this.

## 3. Roll Out a New Version and Roll Back

A rollout creates a new revision of the Deployment. The Deployment keeps the old ReplicaSet so that it can roll back.

You must:

- Annotate the Deployment with the change cause image maziar/kubia:v1.
- Update the Deployment image to maziar/kubia:v2 using kubectl set image.
- Annotate the Deployment with the change cause image maziar/kubia:v2.
- Run kubectl rollout status and show that the rollout completes.
- Run kubectl get rs -o wide, show both ReplicaSets, and state how many Pods each ReplicaSet manages.
- Run kubectl rollout history deployment/kubia and show both revisions.
- Roll back the Deployment using kubectl rollout undo.
- Run kubectl rollout status again and show that the rollback completes.
- Run kubectl rollout history again and show the new list of revisions.
- Explain what the CHANGE-CAUSE column shows and where its value comes from.
- Explain why revision 1 becomes revision 3 after the rollback.

## 4. Use Labels to Control a ReplicaSet

A ReplicaSet finds its Pods by label. When the label of a Pod no longer matches the selector, the ReplicaSet no longer counts that Pod.

You must:

- Run kubectl get pods --show-labels and kubectl get pods -l app=kubia.
- Save the name of the newest Pod in the POD variable, then run kubectl label pod $POD app=kubia-debug --overwrite.
- Run kubectl rollout status deployment/kubia and kubectl get pods -L app.
- Show the three Pods with app=kubia and the one Pod with app=kubia-debug.
- Run kubectl get pod $POD -o jsonpath='{.metadata.ownerReferences}'; echo and show the result.
- Explain why the ReplicaSet creates a new Pod after the label change.
- Explain why the re-labelled Pod keeps running and why it has no owner.

## 5. Create a ClusterIP Service and Use Its DNS Name

A ClusterIP Service gives a group of Pods one stable name and one stable address inside the cluster.

You must:

- Create service.yaml and display its contents.
- Apply the manifest using kubectl apply -f service.yaml.
- Run kubectl get svc kubia and show the ClusterIP address.
- Run kubectl get endpointslices -l kubernetes.io/service-name=kubia and show the three endpoints.
- Create the client Pod using the maziar/alpine-curl image and wait until it is Ready.
- Run the four calls to http://kubia from the client Pod and show the responses.
- Run kubectl exec client -- curl -s http://kubia.default.svc.cluster.local and show the response.
- Explain why the kubia-debug Pod is not one of the three endpoints.
- Explain what targetPort: http means in service.yaml.
- Explain each part of the name kubia.default.svc.cluster.local, and why the short name kubia also works from the client Pod.

## 6. Expose the Application with a NodePort Service

A NodePort Service opens the same port on every node, allowing access from outside the cluster when network access is configured correctly.

You must:

- Create service-nodeport.yaml and display its contents.
- Apply the manifest using kubectl apply -f service-nodeport.yaml.
- Run kubectl get svc kubia-nodeport and show 80:30000/TCP.
- Run curl -s http://localhost:30000 on the control-plane node and show the response.
- Run terraform output public_ips on your own machine.
- Open each of the following public addresses in your browser and capture a screenshot of the result:
  - http://<master-public-ip>:30000
  - http://<worker1-public-ip>:30000
  - http://<worker2-public-ip>:30000
- Explain how a request to port 30000 on a node reaches a kubia Pod.
- Explain the difference between a ClusterIP Service and a NodePort Service.

## 7. Destroy the Cluster

At the end of the lab, destroy all three EC2 instances. This also deletes every Kubernetes object and every file of the lab.

You must:

- From the Week 06 directory, run terraform destroy.
- Include the final Terraform output showing Destroy complete!.
- State the number of resources Terraform removed.
- Explain why you destroy the cluster at the end of every lab.

## Submission Requirements

Your report must include all of the following:

- Your name clearly visible in every screenshot.
- Screenshots demonstrating the required commands and results in all 7 sections.
- Actual output from the commands you executed.
- Clear, detailed explanations of the commands, their purpose, and the results.
- Highlighted or clearly visible output where appropriate.
- Answers to every explanation question specified in the lab.

Use your own screenshots and outputs from your lab environment. Screenshots or outputs copied from the recording or another student's submission do not demonstrate your own work.

## Academic Integrity Pledge

By submitting this assignment, you affirm that you will not plagiarize or provide or receive unauthorized assistance on assignments, papers, or examinations. You agree to uphold fairness and honesty in your own work and in the work of others.

Please review the Seneca Academic Integrity Policy for further details.
