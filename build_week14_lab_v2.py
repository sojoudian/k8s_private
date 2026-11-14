# -*- coding: utf-8 -*-
"""CLO835 Week 14 lab v2 - kubeconfig and the Horizontal Pod Autoscaler, in ONE
workshop.

v1 had 3 workshops and 10 steps. The limit is now the size of the Week 03 and
Week 04 labs: at most Step 0 to Step 6. v2 keeps the line of the lecture
(week14/Week14_lecture_style_v11.pptx): the kubeconfig (users, contexts,
use-context, set-context), the Metrics Server, and an HPA that scales under load.
The optional IRSA workshop is left out.

The Metrics Server comes from the course repository (Week14/metrics-server.yaml):
the upstream v0.7.1 file with the maziar image and --kubelet-insecure-tls,
because a kubeadm kubelet serves a self-signed certificate.

Outputs: week14/Lab_week14_v2.pptx, week14/localMachine_v2.sh,
week14/Lab_week14_Blackboard_Submission_v2.md, ~/Documents/c/r/CLO835_Fall_2026/Week14/
Run from the project root. It is guarded, so importing it writes nothing.
"""
import os
import sys

import build_week07_lab_v2 as w07
import build_week14_lab_v1 as v1
import lab_kubeadm as L

F = L.FILE_MARK
MS_FILE = "metrics-server.yaml"
MS_URL = L.RAW + "Week14/" + MS_FILE

SLIDES = [
 ("title", "Workshop 1 – Kubeconfig and Autoscaling"),
 ("prereq",),
 ("cluster",),
 ("step2", "A second user: viewer", "bash", [
  "# kubectl reads ~/.kube/config: clusters, users, contexts.",
  "$ kubectl config get-contexts",
  " ",
  "# The cluster CA signs a certificate for viewer, and the",
  "# built-in ClusterRole view gives read-only access.",
  "$ openssl genrsa -out viewer.key 2048",
  "$ openssl req -new -key viewer.key -out viewer.csr -subj \"/CN=viewer/O=viewers\"",
  "$ cat > viewer-csr.yaml <<EOF",
  F,
  "EOF",
  "$ kubectl apply -f viewer-csr.yaml",
  "$ kubectl certificate approve viewer",
  "$ kubectl get csr viewer                    # Approved,Issued",
  "$ kubectl get csr viewer -o jsonpath='{.status.certificate}' | base64 -d > viewer.crt",
  "$ kubectl create clusterrolebinding viewer-view --clusterrole=view --user=viewer",
  ], "viewer-csr.yaml", "viewer-csr.yaml", v1.CSR),
 ("step", "A context, and switch to it", "bash", [
  "# A context = one cluster + one user + a namespace.",
  "$ kubectl config set-credentials viewer --client-certificate=viewer.crt --client-key=viewer.key --embed-certs=true",
  "$ kubectl create namespace dev",
  "$ kubectl config set-context context-1 --cluster=kubernetes --user=viewer --namespace=dev",
  " ",
  "# Switch: the cluster, the user AND the namespace change together.",
  "$ kubectl config use-context context-1",
  "$ kubectl config current-context                # context-1",
  "$ kubectl get pods                              # allowed: No resources found in dev",
  "$ kubectl create deployment web --image=maziar/kubia:v1     # Forbidden: view cannot create",
  " ",
  "# Back to the admin.",
  "$ kubectl config use-context kubernetes-admin@kubernetes",
  "$ kubectl config get-contexts",
  ]),
 ("step", "The Metrics Server", "bash", [
  "# The HPA reads the CPU use from the Metrics Server. Install it from the course repository.",
  "# This copy adds --kubelet-insecure-tls: a kubeadm kubelet serves a self-signed certificate.",
  "$ kubectl apply -f " + MS_URL,
  "$ kubectl -n kube-system rollout status deployment/metrics-server",
  "$ kubectl wait --for=condition=Available apiservice/v1beta1.metrics.k8s.io --timeout=180s",
  "$ kubectl get apiservice v1beta1.metrics.k8s.io           # AVAILABLE True",
  "$ sleep 30; kubectl top nodes",
  ]),
 ("step2", "A HorizontalPodAutoscaler", "bash", [
  "# A PHP page that burns CPU on every request.",
  "$ kubectl create deployment php-apache --image=maziar/hpa-example",
  "$ kubectl set resources deployment php-apache --requests=cpu=200m",
  "$ kubectl expose deployment php-apache --port=80",
  "$ kubectl rollout status deployment/php-apache",
  " ",
  "# Keep the average CPU at 50 % of the request.",
  "$ cat > hpa.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f hpa.yaml",
  "# Wait for the first CPU sample. Before it, TARGETS is <unknown>.",
  "$ kubectl wait --for=condition=ScalingActive hpa/php-apache --timeout=180s",
  "$ kubectl get hpa php-apache",
  "# TARGETS cpu: 0%/50%   REPLICAS 1",
  ], "hpa.yaml", "hpa.yaml", v1.HPA),
 ("step", "Generate load and watch the HPA scale", "bash", [
  "# A Pod that calls the application in a loop.",
  "$ kubectl run load-generator --image=busybox:1.36 --restart=Never -- /bin/sh -c \"while sleep 0.01; do wget -q -O- http://php-apache; done\"",
  " ",
  "# Read the HPA every 15 s for 3 minutes. REPLICAS climbs.",
  "$ for i in $(seq 12); do kubectl get hpa php-apache --no-headers; sleep 15; done",
  " ",
  "# desired replicas = ceil( current replicas x current CPU / target CPU )",
  "$ kubectl describe hpa php-apache | grep -A1 '^Metrics:'",
  "$ kubectl get pods -l app=php-apache",
  " ",
  "# Stop the load. After the 5-minute stabilization window, the HPA scales down.",
  "$ kubectl delete pod load-generator --now",
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
 ("end", "Workshop 1 – The End"),
]

SCRIPT_HEAD = """#!/bin/bash
# CLO835 - Week 14 - Kubeconfig and the Horizontal Pod Autoscaler.
# Run these ON THE MASTER NODE, section by section. Do NOT run the whole file.
#
# Terraform builds 3 machines: 1 control plane and 2 workers. The cluster forms
# itself at boot, the same way it did in Weeks 04 to 13.
#
# Each step matches one slide of Lab_week14_v2.pptx.
"""

CLEANUP = """kubectl config use-context kubernetes-admin@kubernetes 2>/dev/null
kubectl delete hpa php-apache 2>/dev/null
kubectl delete deployment php-apache 2>/dev/null
kubectl delete service php-apache 2>/dev/null
kubectl delete pod load-generator --now 2>/dev/null
kubectl delete namespace dev 2>/dev/null
kubectl delete clusterrolebinding viewer-view 2>/dev/null
kubectl delete csr viewer 2>/dev/null
kubectl config delete-context context-1 2>/dev/null
kubectl config delete-user viewer 2>/dev/null
kubectl -n kube-system delete deployment metrics-server 2>/dev/null
kubectl -n kube-system delete service metrics-server 2>/dev/null
kubectl delete apiservice v1beta1.metrics.k8s.io 2>/dev/null
kubectl -n kube-system delete serviceaccount metrics-server 2>/dev/null
kubectl -n kube-system delete rolebinding metrics-server-auth-reader 2>/dev/null
kubectl delete clusterrolebinding metrics-server:system:auth-delegator system:metrics-server 2>/dev/null
kubectl delete clusterrole system:aggregated-metrics-reader system:metrics-server 2>/dev/null
rm -f ./viewer.key ./viewer.csr ./viewer.crt ./viewer-csr.yaml ./hpa.yaml

kubectl get hpa,deployments,pods"""

BLACKBOARD = [
 ("Working with kubeconfig",
  "A kubeconfig holds clusters, users and contexts. A context joins one cluster, one user and a namespace.",
  ["Show the approved viewer certificate and the ClusterRoleBinding to the view role.",
   "Show use-context context-1: get pods allowed, create deployment Forbidden.",
   "Show get-contexts after you switch back to the admin.",
   "Explain what changes when you switch context."]),
 ("Horizontal Pod Autoscaling",
  "The HPA adjusts the replicas of php-apache to keep the average CPU at 50 %.",
  ["Show kubectl top nodes, and explain --kubelet-insecure-tls.",
   "Show kubectl get hpa before the load and while REPLICAS climbs.",
   "Show the Metrics section of kubectl describe hpa, and calculate the desired replicas from it.",
   "Show the clean-up and terraform destroy."]),
]


def ms_manifest():
    text = open(os.path.join(w07.MIRROR_DIR, "metrics-server/v0.7.1/components.yaml")).read()
    old = "        - --kubelet-use-node-status-port\n"
    assert text.count(old) == 1
    return text.replace(old, old + "        - --kubelet-insecure-tls\n")


if __name__ == "__main__":
    L.check_lines(SLIDES)
    L.make_lab("14", SLIDES, "week14/Lab_week14_v2.pptx", SCRIPT_HEAD, script_path="week14/localMachine_v2.sh")
    if "--no-repo" not in sys.argv:
        dst, files = L.make_repo_folder("14", "Kubeconfig and the Horizontal Pod Autoscaler", CLEANUP,
                                        "week14/localMachine_v2.sh", extra_files={MS_FILE: ms_manifest()})
        print("repo folder : %s (%d files)" % (dst, len(files)))
    L.blackboard_text("14", "The Terraform configuration in Week 14 creates the same three Ubuntu 26.04 EC2 "
                      "machines as Weeks 04 to 13.", BLACKBOARD, "week14/Lab_week14_Blackboard_Submission_v2.md")
    print("blackboard  : week14/Lab_week14_Blackboard_Submission_v2.md")
