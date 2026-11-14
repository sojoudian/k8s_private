# Assignment 2 Submission

Please submit a report that demonstrates all the main points of Assignment 2.
Week 05 and Week 06 teach every command that this assignment needs. Make sure your submission includes your own screenshots, command outputs, and explanations as described below.

The starter files are in the course repository, in the `assignment-2` folder:
https://github.com/sojoudian/CLO835_Fall_2026

You build one small web service. GitHub Actions builds the image and pushes it to Docker Hub. You deploy it to the three-node Kubernetes cluster of Week 05, then you release a second version and roll it back.

| Version | The application answers |
|---|---|
| 0.2 | Hello world from the CLO835 class! |
| 0.3 | Hello world from the CLO835 class and <your-student-id>! |

## 1. Your Own Repository

The pipeline runs only from the root of a repository. A workflow in a sub-folder never runs.
You must:
- Copy the contents of the assignment-2 folder to the root of a new repository of your own.
- Show the repository on GitHub, with .github/workflows/docker.yml at the root.
- Give the full address of your repository in the report.
- Show git log with your commits, all of them before the due date.
- Explain why the workflow does not run when the folder sits one level down.

## 2. Choose One Language and Make Version 0.2

Choose one starter from the apps folder. Programming is not the subject of this course.
You must:
- State which language you chose.
- Show the MESSAGE constant of your starter.
- Run the application on your own machine, and show curl http://localhost:8080 returning Hello world from the CLO835 class!.
- Show curl http://localhost:8080/healthz returning 200.
- Explain what the /healthz and /readyz paths are for.

## 3. The Dockerfile

The Dockerfile in the starter holds TODO comments only. You write it.
You must:
- Show your finished Dockerfile.
- Show docker build and docker run on your own machine.
- Show curl http://localhost:8080 answering from inside the container.
- Explain which base image you chose, and why.
- Explain why the image must be built for linux/amd64, and what exec format error means.

## 4. The GitHub Actions Pipeline

The workflow file holds TODO comments only. You write the steps.
You must:
- Create the two repository secrets DOCKERHUB_USERNAME and DOCKERHUB_TOKEN, and show the Secrets page with the two names visible.
- Show your finished .github/workflows/docker.yml.
- Show a green workflow run in the Actions tab.
- Show the image on Docker Hub, with the tag 0.2 and with the commit SHA tag.
- Explain why a token is a secret and never a line in the file.
- Explain what the commit SHA tag gives you that the version tag does not.

## 5. The Kubernetes Cluster

The cluster is the same three-node kubeadm cluster that Week 05 builds. It is not kind, and not minikube.
You must:
- Run terraform init and terraform apply from the Week 05 folder.
- Show an SSH session connected to the control-plane machine.
- Show kubectl get nodes -o wide with all three nodes Ready.
- Explain why you run every kubectl command of this assignment on the control plane.

## 6. Deploy Version 0.2

The two manifests in the k8s folder hold TODO comments only. You write them.
You must:
- Show your finished deployment.yaml, with 3 replicas.
- Show your finished service.yaml, a NodePort Service pinned to port 30000.
- Run kubectl apply -f deployment.yaml -f service.yaml.
- Show kubectl get deploy,rs,pods,svc with three pods Running and 80:30000/TCP.
- Show kubectl get pods -o wide, and state which node runs each pod.
- Explain why the Service selector must match the pod labels of the Deployment.

## 7. Reach the Application from Every Node

A NodePort opens on every node, not only on a node that runs a pod.
You must:
- Show curl http://localhost:30000 on the control-plane machine.
- Open all three public addresses in your browser, and capture all three:
    - http://<master-public-ip>:30000
    - http://<worker1-public-ip>:30000
    - http://<worker2-public-ip>:30000
- Show that every address answers Hello world from the CLO835 class!.
- Explain why a node that runs no pod still serves the page.

## 8. Release Version 0.3

Version 0.3 carries your own Seneca student ID. Each running application is then unique.
You must:
- Change the MESSAGE constant, commit, and push.
- Show the second green workflow run, and show the tag 0.3 on Docker Hub.
- Run kubectl set image, then kubectl rollout status.
- Show kubectl get rs with two ReplicaSets, and state how many pods each one holds.
- Capture the browser on a node public address, with your student ID visible.
- Explain why the pods change one at a time, and why no request is lost.

## 9. Roll Back

A Deployment keeps its old ReplicaSets, so you can go back.
You must:
- Show kubectl rollout history for your Deployment.
- Run kubectl rollout undo, then kubectl rollout status.
- Capture the browser again, and show the answer back at version 0.2.
- State which ReplicaSet held the pods before the undo, and which one holds them after.
- Explain why the rollback does not need a new image build.

## 10. The Report

The report is mandatory. Use the report.md file in the starter.
You must:
- Give your name, your student ID, your language, your image name, and your repository address.
- List every problem that you met, and how you solved it.
- Give the output of kubectl rollout history, kubectl get rs, and kubectl get pods -o wide.
- Add one browser screenshot for version 0.2, and one for version 0.3.

## 11. Destroy the Cluster

At the end of the assignment, delete all three machines.
You must:
- Run kubectl delete -f deployment.yaml -f service.yaml.
- Run terraform destroy from the Week 05 folder.
- Show the final output containing Destroy complete!.
- Explain why a stopped EC2 machine can still result in charges.

## Submission Requirements

Your submission must include:
- Your name clearly visible on every screenshot.
- The full address of your GitHub repository.
- The full name of your Docker Hub image.
- Detailed explanations of the commands being executed.
- The output of the commands you executed.
- Screenshots that clearly demonstrate the required results.
- Highlighted or clearly visible command outputs where appropriate.

## Integrity Pledge

By submitting this assignment, you affirm that you will not plagiarize, give or receive illegitimate help on assignments, papers, or examinations. You will uphold fairness and honesty in your work and in the work of others.
Please read the Seneca Academic Integrity Policy for more details.
