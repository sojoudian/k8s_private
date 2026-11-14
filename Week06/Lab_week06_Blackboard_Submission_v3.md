# Lab Week 06 Submission

Please submit a report that demonstrates all the main points of Lab Week 06.
The lab recording demonstrates every step required for this assignment. You may watch the recording and follow it directly, step by step, to complete the lab. Make sure your submission includes your own screenshots, command outputs, and explanations as described below.

## 1. Build the Cluster and Check It

The Terraform configuration in Week 06 creates the same three Ubuntu 26.04 EC2 machines as Week 05: one control plane and two workers. The cluster forms itself at boot.
You must:
- Run terraform init and terraform apply.
- Show an SSH session connected to the control-plane machine.
- Show kubectl get nodes -o wide with all three nodes Ready.
- Show kubectl get pods -n kube-system with the control-plane pods Running.

## 2. A Deployment and a Rollout

A Deployment owns ReplicaSets, and each ReplicaSet owns Pods.
You must:
- Show deployment.yaml and kubectl apply -f deployment.yaml.
- Show kubectl get deploy,rs,pods -o wide with 3 Pods of maziar/kubia:v1.
- Annotate revision 1, then roll out maziar/kubia:v2 with kubectl set image, and annotate revision 2.
- Show kubectl rollout status and kubectl get rs -o wide with two ReplicaSets, and state how many Pods each one holds.
- Show the curl of the newest Pod IP returning This is v2 running in pod.
- Explain why the Deployment keeps the old ReplicaSet with 0 Pods.
- Explain what terminationGracePeriodSeconds: 5 changes when an old Pod stops.

## 3. History, Rollback and a Failed Rollout

You must:
- Show kubectl rollout history with a CHANGE-CAUSE for each revision.
- Show kubectl rollout undo, then the history again.
- Explain why revision 1 became revision 3.
- Show kubectl rollout undo --to-revision=2.
- Roll out the tag maziar/kubia:v9, and show kubectl rollout status stopping after 60 seconds.
- Show kubectl get pods with the 3 old Pods Running and the new Pod unable to pull its image.
- Explain why no old Pod stopped, with the default values maxSurge 25% and maxUnavailable 25%.
- Roll back the failed rollout, and show the Pods Running.

## 4. Rollout Strategies

You must:
- Change the strategy to Recreate, and show the strategy with kubectl get deployment kubia -o jsonpath.
- Show the watch of the second SSH session while the Recreate rollout runs.
- State the order in which the old Pods stop and the new Pods start.
- Explain which strategy causes downtime, and why.
- Pause the Deployment, change the image, and show that UP-TO-DATE is 0 and the v1 ReplicaSet keeps its 3 Pods.
- Resume the Deployment, and show the rollout that follows.
- Explain why the resume makes no new ReplicaSet.

## 5. Labels and Selectors

You must:
- Apply pods-with-labels.yaml, and show kubectl get pods --show-labels and kubectl get pods -L creation_method,env.
- Add one label and change one label with --overwrite, and show the result.
- Show one selector of each kind: equality, existence (env and '!env'), set (in), and two conditions.
- Change the app label of one kubia Pod to kubia-debug.
- Show kubectl get pods -L app with the replacement Pod that the ReplicaSet made.
- Show that the re-labelled Pod has no owner.
- Explain how the ReplicaSet decides which Pods it owns.

## 6. A ClusterIP Service

You must:
- Show service.yaml, and explain port, targetPort, and the named port http.
- Show kubectl describe svc kubia and kubectl get endpointslices, and state which Pods are endpoints.
- Explain why the kubia-debug Pod is not an endpoint.
- Reach the Service in the three ways: from the client Pod, from inside a kubia Pod, and from the master with the ClusterIP.
- Show that the calls of the client Pod reach different Pods.
- Scale the Deployment to 1, then to 0, then to 3, and show the endpoints after each change.
- Show the error of the client when the Service has no endpoint.
- Explain why you wait until the Pods are gone before this call.

## 7. How a Service Works

You must:
- Show the kube-proxy Pods, one on each node.
- Show the iptables rules for default/kubia:http on the master.
- Explain why a Service has no process, and how a call to the ClusterIP reaches a Pod on another node.

## 8. Reach the Service from Outside

You must:
- Show service-nodeport.yaml and kubectl get svc kubia-nodeport with 80:30000/TCP.
- Open all three public addresses in your browser, and capture all three:
    - http://<master-public-ip>:30000
    - http://<worker1-public-ip>:30000
    - http://<worker2-public-ip>:30000
- Show kubectl get svc kubia-lb with EXTERNAL-IP <pending>, and the curl of its node port.
- Explain why a kubeadm cluster gives no external address to a LoadBalancer Service.
- Show ingress.yaml, kubectl get ingress kubia with no ADDRESS, and kubectl get ingressclass.
- Explain what an Ingress needs before it can serve a rule.

## 9. A Rolling Update through the Service

You must:
- Show the output of the second SSH session while the rollout from v2 to v1 runs.
- Mark the first v1 answer and the last v2 answer.
- State how many calls failed.
- Explain the result with the RollingUpdate strategy.

## 10. Service Discovery

You must:
- Show the kube-dns Service and the CoreDNS Pods.
- Show the /etc/resolv.conf of the client Pod, and explain the nameserver and the search line.
- Reach the Service with the full name, with kubia.default, and with kubia.
- Show the KUBIA_SERVICE variables of the client Pod, and show that kubia-manual has none.
- Explain why the two Pods differ.
- Create the Service kubia-v2, delete the Service kubia, and show the error of a call to kubia.
- Explain why the client of a two-tier application must use the correct Service name.

## 11. Destroy the Cluster

At the end of the lab, delete all three machines.
You must:
- Run bash cleanup_lab06.sh on the control-plane machine, and show the cluster is empty.
- Run terraform destroy from the Week 06 directory.
- Show the final output containing Destroy complete!.
- State how many resources Terraform removed.

## Submission Requirements

Your submission must include:
- Your name clearly visible on every screenshot.
- Detailed explanations of the commands being executed.
- The output of the commands you executed.
- Screenshots that clearly demonstrate the required results.
- Highlighted or clearly visible command outputs where appropriate.

## Integrity Pledge

By submitting this assignment, you affirm that you will not plagiarize, give or receive illegitimate help on assignments, papers, or examinations. You will uphold fairness and honesty in your work and in the work of others.
Please read the Seneca Academic Integrity Policy for more details.
