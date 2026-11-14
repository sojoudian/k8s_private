#!/bin/bash
# CLO835 - Week 14 - Kubeconfig and the Horizontal Pod Autoscaler.
# Run these ON THE MASTER NODE, section by section. Do NOT run the whole file.
#
# Terraform builds 3 machines: 1 control plane and 2 workers. The cluster forms
# itself at boot, the same way it did in Weeks 04 to 13. Workshop 2 installs the
# Metrics Server from the course mirror. Workshop 3 is optional.
#
# Each step matches one slide of Lab_week14_v1.pptx.

########################################################
# Step 0 - check the cluster                    (slide 3)
########################################################
# All three nodes must reach Ready. The workers take a few minutes to join.
kubectl get nodes -o wide
kubectl get pods -n kube-system

########################################################
# Step 1 - Read the kubeconfig                  (slide 4)
########################################################
# kubectl reads ~/.kube/config: clusters (where), users (who) and contexts (one of each).
kubectl config view
kubectl config get-contexts
kubectl config current-context                # kubernetes-admin@kubernetes

########################################################
# Step 2 - A second user: viewer                (slide 5)
########################################################
# The cluster CA signs a certificate for viewer, and the
# built-in ClusterRole view gives read-only access.
openssl genrsa -out viewer.key 2048
openssl req -new -key viewer.key -out viewer.csr -subj "/CN=viewer/O=viewers"
cat > viewer-csr.yaml <<EOF
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: viewer
spec:
  request: $(base64 -w0 < viewer.csr)
  signerName: kubernetes.io/kube-apiserver-client
  expirationSeconds: 86400
  usages:
  - client auth
EOF
kubectl apply -f viewer-csr.yaml
kubectl certificate approve viewer
kubectl get csr viewer -o jsonpath='{.status.certificate}' | base64 -d > viewer.crt
kubectl create clusterrolebinding viewer-view --clusterrole=view --user=viewer

########################################################
# Step 3 - Define a context and switch to it    (slide 6)
########################################################
# A context = one cluster + one user + a namespace.
kubectl config set-credentials viewer --client-certificate=viewer.crt --client-key=viewer.key --embed-certs=true
kubectl config set-context context-1 --cluster=kubernetes --user=viewer --namespace=dev
kubectl create namespace dev
kubectl config get-contexts

# Switch context: the cluster, the user AND the namespace change together.
kubectl config use-context context-1
kubectl config current-context                # context-1
kubectl get pods                              # as viewer, in dev: allowed
kubectl create deployment web --image=maziar/kubia:v1     # Forbidden: view cannot create

# Back to the admin. Pin a default namespace on the current context.
kubectl config use-context kubernetes-admin@kubernetes
kubectl config set-context --current --namespace=dev
kubectl config get-contexts                   # NAMESPACE dev
kubectl config set-context --current --namespace=default

########################################################
# Step 4 - A kubeconfig file of its own         (slide 7)
########################################################
# Give a colleague one file with one context in it.
kubectl config view --minify --flatten --context=context-1 > viewer.kubeconfig
kubectl --kubeconfig=viewer.kubeconfig config get-contexts
kubectl --kubeconfig=viewer.kubeconfig get pods -A | head -5

# KUBECONFIG can merge several files into one view.
KUBECONFIG=~/.kube/config:viewer.kubeconfig kubectl config get-contexts

########################################################
# Step 5 - Deploy the Metrics Server            (slide 10)
########################################################
# The HPA reads CPU use from the Metrics Server. Install it from the course mirror.
kubectl apply -f https://raw.githubusercontent.com/sojoudian/clo835-mirrors/main/metrics-server/v0.7.1/components.yaml

# A kubeadm kubelet serves a self-signed certificate. Let metrics-server accept it.
kubectl -n kube-system patch deployment metrics-server --type=json -p '[{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"}]'
kubectl -n kube-system rollout status deployment/metrics-server
kubectl get apiservice v1beta1.metrics.k8s.io           # AVAILABLE True
sleep 30; kubectl top nodes

########################################################
# Step 6 - The sample application               (slide 11)
########################################################
# A PHP page that burns CPU on every request.
kubectl create deployment php-apache --image=maziar/hpa-example
kubectl set resources deployment php-apache --requests=cpu=200m
kubectl expose deployment php-apache --port=80
kubectl rollout status deployment/php-apache
kubectl get pods -l app=php-apache

########################################################
# Step 7 - A HorizontalPodAutoscaler resource   (slide 12)
########################################################
# Keep the average CPU at 50 % of the request, with
# 1 to 10 replicas.
cat > hpa.yaml <<'EOF'
apiVersion: autoscaling/v2
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
        averageUtilization: 50
EOF
kubectl apply -f hpa.yaml
sleep 30; kubectl get hpa php-apache
# TARGETS cpu: 0%/50%   REPLICAS 1

# The HPA controller polls the Metrics Server every 15 s.

########################################################
# Step 8 - Generate load and watch the HPA scale (slide 13)
########################################################
# SECOND SSH SESSION - watch the HPA. Ctrl+C to stop.
kubectl get hpa php-apache -w

# FIRST SSH SESSION - a Pod that calls the application in a loop.
kubectl run load-generator --image=busybox:1.36 --restart=Never -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://php-apache; done"

# In a minute or two, REPLICAS climbs. The calculation of the lecture:
#   desired replicas = ceil( current replicas x current CPU / target CPU )
kubectl describe hpa php-apache | grep -A3 Metrics

# Stop the load. After the 5-minute stabilization window, the HPA scales down.
kubectl delete pod load-generator --now

########################################################
# Step 9 - Every Pod has the role of its node   (slide 16)
########################################################
# On EKS, IRSA gives one ServiceAccount its own IAM role. Without it, a Pod gets the role of its node.
kubectl run awscli --image=maziar/aws-cli --restart=Never --env=AWS_DEFAULT_REGION=us-east-1 --command -- sleep 3600
kubectl wait --for=condition=Ready pod/awscli --timeout=120s
kubectl exec awscli -- aws sts get-caller-identity
# "Arn": "arn:aws:sts::<account>:assumed-role/LabRole/i-..."  : the role of the node

# Every Pod on these nodes can act as LabRole. IRSA, or one role per workload, prevents that.
kubectl delete pod awscli --now

########################################################
# Step 10 - Clean up                            (slide 17)
########################################################
# ON THE MASTER - remove the Kubernetes objects and the viewer user.
bash cleanup_lab14.sh

# Confirm that nothing is left.
kubectl get hpa,deployments,pods

# ON YOUR OWN MACHINE - remove the three EC2 machines.
# ON YOUR OWN MACHINE:  terraform destroy

# Always destroy. The Learner Lab budget is small.
