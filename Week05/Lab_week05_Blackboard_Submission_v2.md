# Lab Week 05 Submission

Please submit a report that demonstrates all the main points of Lab Week 05.
The lab recording demonstrates every step required for this assignment. You may watch the recording and follow it directly, step by step, to complete the lab. Make sure your submission includes your own screenshots, command outputs, and explanations as described below.

## 1. Build the Cluster and Check It

The Terraform configuration in Week 05 creates the same three Ubuntu 26.04 EC2 machines as Week 04: one control plane and two workers. The cluster forms itself at boot.
You must:
- Run terraform init and terraform apply.
- Show an SSH session connected to the control-plane machine.
- Show kubectl get nodes -o wide with all three nodes Ready.
- Show kubectl get pods -n kube-system with the control-plane pods Running.
- Explain why you run every kubectl command of this lab on the control plane only.

## 2. Your First Pod

Run nginx as a single pod by following localMachine.sh.
You must:
- Show kubectl run nginx --image nginx, then kubectl get pods.
- Show kubectl get pod nginx -o yaml, and name three fields you never typed.
- Reach the pod with kubectl port-forward nginx 8080:80, and show curl http://localhost:8080 returning Welcome to nginx!.
- Explain why the port forward works although no Service exists yet.
- Explain what the API server adds to the object after you create it.

## 3. A Pod from a Manifest

A manifest is a file you can keep, read and commit. A command is not.
You must:
- Show kubectl run kubia --image maziar/kubia --dry-run=client -o yaml > kubia-manual.yaml.
- Show the contents of kubia-manual.yaml.
- Show kubectl apply -f kubia-manual.yaml, and show the pod Running.
- Show kubectl explain pod.spec and kubectl explain pod.spec.containers.
- Explain what --dry-run=client does, and why nothing reaches the cluster.

## 4. Two Containers in One Pod

A pod may hold more than one container. The containers share one IP address.
You must:
- Apply the web-with-sidecar manifest with the web and logger containers.
- Show kubectl get pod web-with-sidecar with READY reading 2/2.
- Show kubectl logs web-with-sidecar -c logger.
- Run pingpong, and show kubectl logs pingpong and kubectl logs pingpong --tail 1 --follow.
- Explain why -c is necessary for one pod and not for the other.
- Explain how the two containers reach each other on 127.0.0.1.

## 5. Labels and Selectors

A label is a key and a value. A selector picks objects by label.
You must:
- Label the nginx pod and the kubia pod, and show kubectl get pods --show-labels.
- Show kubectl get pods -l app=web and kubectl get pods -l 'rel in (stable,beta)'.
- Change one label with --overwrite, and show that the same selector now returns a different result.
- Explain how a ReplicaSet uses this same mechanism to find the pods it owns.
- Explain what happens to a pod that you re-label out of its ReplicaSet selector.

## 6. Pods, ReplicaSets and Deployments

A bare pod does not scale. A Deployment does.
You must:
- Show kubectl scale pod pingpong --replicas=3 failing, and quote the error.
- Create the pingpong namespace and the pingpong Deployment with alpine:3.14.
- Show kubectl get all -n pingpong, and name the three objects in the chain.
- Apply the kubia-rs ReplicaSet manifest with three replicas.
- Show kubectl get rs kubia-rs and kubectl get pods -l app=kubia-rs.
- Explain why the ReplicaSet selector must match the template labels.

## 7. Scale, Roll Forward and Roll Back

You must:
- Scale the pingpong Deployment to 3 replicas, then back to 1, and show kubectl get all -n pingpong after each change.
- Roll forward to alpine:3.15 with kubectl set image, and show kubectl rollout status.
- Show kubectl get rs -n pingpong with two ReplicaSets, and state how many pods each one holds.
- Show kubectl rollout history and kubectl rollout undo.
- Show kubectl rollout status after the undo, and show the image back at alpine:3.14.
- Explain why the Deployment keeps the old ReplicaSet instead of deleting it.

## 8. Maintaining the Desired State

The controller compares the desired state with the live state, and it corrects the difference.
You must:
- Scale the pingpong Deployment to 3 replicas, and show the three pods.
- Delete one pod by name, and show that a replacement pod appears at once.
- Delete the stand-alone pingpong pod, and show that nothing replaces it.
- Explain which object restores the first pod, and why no object restores the second one.

## 9. Reach the Pod from Your Browser

Nothing above left the cluster. A NodePort publishes the pod on every node.
You must:
- Show kubectl expose pod nginx --type=NodePort --port=80 --name=nginx-http.
- Pin the node port to 30000 with kubectl patch, and show kubectl get svc nginx-http with 80:30000/TCP.
- Show curl http://localhost:30000 on the control-plane machine returning Welcome to nginx!.
- Open all three public addresses in your browser, and capture all three:
    - http://<master-public-ip>:30000
    - http://<worker1-public-ip>:30000
    - http://<worker2-public-ip>:30000
- State which single node runs the pod.
- Explain why the other two nodes still serve the page.

## 10. Destroy the Cluster

At the end of the lab, delete all three machines.
You must:
- Run terraform destroy from the Week 05 directory.
- Show the final output containing Destroy complete!.
- State how many resources Terraform removed.
- Explain why a stopped EC2 machine can still result in charges.

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
