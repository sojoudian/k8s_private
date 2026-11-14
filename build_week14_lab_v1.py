# -*- coding: utf-8 -*-
"""CLO835 Week 14 - kubeconfig, the Horizontal Pod Autoscaler and (optional) the
node role, on the kubeadm cluster.

The lecture (week14/Week14_lecture_style_v11.pptx) teaches the kubeconfig
(clusters, users, contexts; view, get-contexts, current-context, use-context,
set-context), the HorizontalPodAutoscaler (the control loop and the replica
calculation) and, as an optional activity, IRSA. The old lab repeated the Week 13
IAM workshop on EKS and never used the kubectl config commands. This lab
practises them, then the HPA, then shows why IRSA exists.

Outputs: week14/Lab_week14_v1.pptx, week14/localMachine_v1.sh,
week14/Lab_week14_Blackboard_Submission.md, ~/Documents/c/r/CLO835_Fall_2026/Week14/
Run from the project root. It is guarded, so importing it writes nothing.
"""
import sys

import lab_kubeadm as L

F = L.FILE_MARK
MS_URL = L.MIRRORS + "metrics-server/v0.7.1/components.yaml"
PATCH = ("'[{\"op\":\"add\",\"path\":\"/spec/template/spec/containers/0/args/-\","
         "\"value\":\"--kubelet-insecure-tls\"}]'")

CSR = """apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: viewer
spec:
  request: $(base64 -w0 < viewer.csr)
  signerName: kubernetes.io/kube-apiserver-client
  expirationSeconds: 86400
  usages:
  - client auth""".split("\n")

HPA = """apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: php-apache
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: php-apache
  minReplicas: 1
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50""".split("\n")

SLIDES = [
 ("title", "Workshop 1 – Working with Kubeconfig"),
 ("prereq",),
 ("cluster",),
 ("step", "Read the kubeconfig", "bash", [
  "# kubectl reads ~/.kube/config: clusters (where), users (who) and contexts (one of each).",
  "$ kubectl config view",
  "$ kubectl config get-contexts",
  "$ kubectl config current-context                # kubernetes-admin@kubernetes",
  ]),
 ("step2", "A second user: viewer", "bash", [
  "# The cluster CA signs a certificate for viewer, and the",
  "# built-in ClusterRole view gives read-only access.",
  "$ openssl genrsa -out viewer.key 2048",
  "$ openssl req -new -key viewer.key -out viewer.csr -subj \"/CN=viewer/O=viewers\"",
  "$ cat > viewer-csr.yaml <<EOF",
  F,
  "EOF",
  "$ kubectl apply -f viewer-csr.yaml",
  "$ kubectl certificate approve viewer",
  "$ kubectl get csr viewer -o jsonpath='{.status.certificate}' | base64 -d > viewer.crt",
  "$ kubectl create clusterrolebinding viewer-view --clusterrole=view --user=viewer",
  ], "viewer-csr.yaml", "viewer-csr.yaml", CSR),
 ("step", "Define a context and switch to it", "bash", [
  "# A context = one cluster + one user + a namespace.",
  "$ kubectl config set-credentials viewer --client-certificate=viewer.crt --client-key=viewer.key --embed-certs=true",
  "$ kubectl config set-context context-1 --cluster=kubernetes --user=viewer --namespace=dev",
  "$ kubectl create namespace dev",
  "$ kubectl config get-contexts",
  " ",
  "# Switch context: the cluster, the user AND the namespace change together.",
  "$ kubectl config use-context context-1",
  "$ kubectl config current-context                # context-1",
  "$ kubectl get pods                              # as viewer, in dev: allowed",
  "$ kubectl create deployment web --image=maziar/kubia:v1     # Forbidden: view cannot create",
  " ",
  "# Back to the admin. Pin a default namespace on the current context.",
  "$ kubectl config use-context kubernetes-admin@kubernetes",
  "$ kubectl config set-context --current --namespace=dev",
  "$ kubectl config get-contexts                   # NAMESPACE dev",
  "$ kubectl config set-context --current --namespace=default",
  ]),
 ("step", "A kubeconfig file of its own", "bash", [
  "# Give a colleague one file with one context in it.",
  "$ kubectl config view --minify --flatten --context=context-1 > viewer.kubeconfig",
  "$ kubectl --kubeconfig=viewer.kubeconfig config get-contexts",
  "$ kubectl --kubeconfig=viewer.kubeconfig get pods -A | head -5",
  " ",
  "# KUBECONFIG can merge several files into one view.",
  "$ KUBECONFIG=~/.kube/config:viewer.kubeconfig kubectl config get-contexts",
  ]),
 ("end", "Workshop 1 – The End"),

 ("title", "Workshop 2 – Horizontal Pod Autoscaling"),
 ("step", "Deploy the Metrics Server", "bash", [
  "# The HPA reads CPU use from the Metrics Server. Install it from the course mirror.",
  "$ kubectl apply -f " + MS_URL,
  " ",
  "# A kubeadm kubelet serves a self-signed certificate. Let metrics-server accept it.",
  "$ kubectl -n kube-system patch deployment metrics-server --type=json -p " + PATCH,
  "$ kubectl -n kube-system rollout status deployment/metrics-server",
  "$ kubectl get apiservice v1beta1.metrics.k8s.io           # AVAILABLE True",
  "$ sleep 30; kubectl top nodes",
  ]),
 ("step", "The sample application", "bash", [
  "# A PHP page that burns CPU on every request.",
  "$ kubectl create deployment php-apache --image=maziar/hpa-example",
  "$ kubectl set resources deployment php-apache --requests=cpu=200m",
  "$ kubectl expose deployment php-apache --port=80",
  "$ kubectl rollout status deployment/php-apache",
  "$ kubectl get pods -l app=php-apache",
  ]),
 ("step2", "A HorizontalPodAutoscaler resource", "bash", [
  "# Keep the average CPU at 50 % of the request, with",
  "# 1 to 10 replicas.",
  "$ cat > hpa.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f hpa.yaml",
  "$ sleep 30; kubectl get hpa php-apache",
  "# TARGETS cpu: 0%/50%   REPLICAS 1",
  " ",
  "# The HPA controller polls the Metrics Server every 15 s.",
  ], "hpa.yaml", "hpa.yaml", HPA),
 ("step", "Generate load and watch the HPA scale", "bash", [
  "# SECOND SSH SESSION - watch the HPA. Ctrl+C to stop.",
  "$ kubectl get hpa php-apache -w",
  " ",
  "# FIRST SSH SESSION - a Pod that calls the application in a loop.",
  "$ kubectl run load-generator --image=busybox:1.36 --restart=Never -- /bin/sh -c \"while sleep 0.01; do wget -q -O- http://php-apache; done\"",
  " ",
  "# In a minute or two, REPLICAS climbs. The calculation of the lecture:",
  "#   desired replicas = ceil( current replicas x current CPU / target CPU )",
  "$ kubectl describe hpa php-apache | grep -A3 Metrics",
  " ",
  "# Stop the load. After the 5-minute stabilization window, the HPA scales down.",
  "$ kubectl delete pod load-generator --now",
  ]),
 ("end", "Workshop 2 – The End"),

 ("title", "Workshop 3 (Optional) – Why IRSA Exists"),
 ("step", "Every Pod has the role of its node", "bash", [
  "# On EKS, IRSA gives one ServiceAccount its own IAM role. Without it, a Pod gets the role of its node.",
  "$ kubectl run awscli --image=maziar/aws-cli --restart=Never --env=AWS_DEFAULT_REGION=us-east-1 --command -- sleep 3600",
  "$ kubectl wait --for=condition=Ready pod/awscli --timeout=120s",
  "$ kubectl exec awscli -- aws sts get-caller-identity",
  "# \"Arn\": \"arn:aws:sts::<account>:assumed-role/LabRole/i-...\"  : the role of the node",
  " ",
  "# Every Pod on these nodes can act as LabRole. IRSA, or one role per workload, prevents that.",
  "$ kubectl delete pod awscli --now",
  ]),
 ("step", "Clean up", "bash", [
  "# ON THE MASTER - remove the Kubernetes objects and the viewer user.",
  "$ bash cleanup_lab14.sh",
  " ",
  "# Confirm that nothing is left.",
  "$ kubectl get hpa,deployments,pods",
  " ",
  "# ON YOUR OWN MACHINE - remove the three EC2 machines.",
  "L$ terraform destroy",
  " ",
  "# Always destroy. The Learner Lab budget is small.",
  ]),
 ("end", "Workshop 3 – The End"),
]

SCRIPT_HEAD = """#!/bin/bash
# CLO835 - Week 14 - Kubeconfig and the Horizontal Pod Autoscaler.
# Run these ON THE MASTER NODE, section by section. Do NOT run the whole file.
#
# Terraform builds 3 machines: 1 control plane and 2 workers. The cluster forms
# itself at boot, the same way it did in Weeks 04 to 13. Workshop 2 installs the
# Metrics Server from the course mirror. Workshop 3 is optional.
#
# Each step matches one slide of Lab_week14_v1.pptx.
"""

CLEANUP = """kubectl config use-context kubernetes-admin@kubernetes 2>/dev/null
kubectl delete hpa php-apache 2>/dev/null
kubectl delete deployment php-apache 2>/dev/null
kubectl delete service php-apache 2>/dev/null
kubectl delete pod load-generator awscli --now 2>/dev/null
kubectl delete namespace dev 2>/dev/null
kubectl delete clusterrolebinding viewer-view 2>/dev/null
kubectl delete csr viewer 2>/dev/null
kubectl config delete-context context-1 2>/dev/null
kubectl config delete-user viewer 2>/dev/null
kubectl delete -f """ + MS_URL + """ 2>/dev/null
rm -f ./viewer.key ./viewer.csr ./viewer.crt ./viewer-csr.yaml ./viewer.kubeconfig ./hpa.yaml

kubectl get hpa,deployments,pods"""

BLACKBOARD = [
 ("Working with Kubeconfig",
  "A kubeconfig holds clusters, users and contexts. A context joins one cluster, one user and a namespace.",
  ["Show kubectl config view, get-contexts and current-context.",
   "Show the viewer certificate issued, and the ClusterRoleBinding to the view role.",
   "Show use-context context-1: get pods allowed, create deployment Forbidden.",
   "Show set-context --current --namespace=dev in get-contexts.",
   "Show viewer.kubeconfig used with --kubeconfig, and the merged view with KUBECONFIG.",
   "Explain what changes when you switch context."]),
 ("Horizontal Pod Autoscaling",
  "The HPA adjusts the replicas of php-apache to keep the average CPU at 50 %.",
  ["Show kubectl top nodes after the Metrics Server patch, and explain --kubelet-insecure-tls.",
   "Show kubectl get hpa before the load, while REPLICAS climbs, and after the load stops.",
   "Show the Metrics section of kubectl describe hpa, and calculate the desired replicas from it.",
   "Explain the control loop: query, calculate, update the Scale sub-resource."]),
 ("Optional: Why IRSA Exists",
  "A Pod on these nodes gets the IAM role of its node.",
  ["Show aws sts get-caller-identity from the awscli Pod.",
   "Explain the risk, and how IRSA solves it on EKS.",
   "Show the clean-up and terraform destroy."]),
]

if __name__ == "__main__":
    L.check_lines(SLIDES)
    L.make_lab("14", SLIDES, "week14/Lab_week14_v1.pptx", SCRIPT_HEAD, script_path="week14/localMachine_v1.sh")
    if "--no-repo" not in sys.argv:
        dst, files = L.make_repo_folder("14", "Kubeconfig and the Horizontal Pod Autoscaler", CLEANUP,
                                        "week14/localMachine_v1.sh")
        print("repo folder : %s (%d files)" % (dst, len(files)))
    L.blackboard_text("14", "The Terraform configuration in Week 14 creates the same three Ubuntu 26.04 EC2 "
                      "machines as Weeks 04 to 13.", BLACKBOARD, "week14/Lab_week14_Blackboard_Submission.md")
    print("blackboard  : week14/Lab_week14_Blackboard_Submission.md")
