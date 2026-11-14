#!/bin/bash
# CLO835 - Week 09 - Managed vs Self-managed Kubernetes.
# Run these ON THE MASTER NODE, section by section. Do NOT run the whole file.
#
# Terraform builds 3 machines: 1 control plane and 2 workers. The cluster forms
# itself at boot, the same way it did in Weeks 04 to 07. The lecture teaches
# what Amazon EKS runs for you. This lab does those jobs by hand.
#
# Each step matches one slide of Lab_week09_v1.pptx.

########################################################
# Step 0 - check the cluster                    (slide 3)
########################################################
# All three nodes must reach Ready. The workers take a few minutes to join.
kubectl get nodes -o wide
kubectl get pods -n kube-system

########################################################
# Step 1 - The control plane runs as static Pods (slide 4)
########################################################
# On EKS, AWS runs the control plane, and you never see it. Here the master runs it.
# The kubelet of the master starts every file of this folder as a static Pod.
sudo ls /etc/kubernetes/manifests
# etcd.yaml  kube-apiserver.yaml  kube-controller-manager.yaml  kube-scheduler.yaml

kubectl get pods -n kube-system -o wide | grep masternode

# No Deployment owns these Pods. Their owner is the node itself.
kubectl get pod kube-scheduler-masternode -n kube-system -o jsonpath='{.metadata.ownerReferences[0].kind}{"\n"}'
# Node

########################################################
# Step 2 - etcd: the cluster database           (slide 5)
########################################################
# Every object of the cluster is a key in etcd. EKS runs etcd for you on three Availability Zones.
# Here it is one Pod on one machine. Ask it directly, with its own certificates.
ETCD="etcdctl --endpoints=https://127.0.0.1:2379 \
    --cacert=/etc/kubernetes/pki/etcd/ca.crt \
    --cert=/etc/kubernetes/pki/etcd/server.crt \
    --key=/etc/kubernetes/pki/etcd/server.key"
kubectl -n kube-system exec etcd-masternode -- $ETCD endpoint health
kubectl -n kube-system exec etcd-masternode -- $ETCD member list -w table

# The namespaces of the cluster, as etcd keys:
kubectl -n kube-system exec etcd-masternode -- $ETCD get /registry/namespaces --prefix --keys-only

# One member: no high availability. If this machine fails, the cluster stops.

########################################################
# Step 3 - You operate the control plane: stop the scheduler (slide 6)
########################################################
# On EKS you never touch the scheduler. Here it is a file. Move the file away.
sudo mv /etc/kubernetes/manifests/kube-scheduler.yaml /tmp/
sleep 20; kubectl get pods -n kube-system | grep scheduler     # nothing: it is gone

# With no scheduler, a new Pod waits for a node.
kubectl run no-scheduler --image=maziar/kubia:v1
sleep 5; kubectl get pod no-scheduler -o wide                  # Pending, NODE <none>

# Put the file back. The scheduler starts, and it places the Pod.
sudo mv /tmp/kube-scheduler.yaml /etc/kubernetes/manifests/
sleep 40; kubectl get pod no-scheduler -o wide                 # Running on a worker
kubectl delete pod no-scheduler --now

########################################################
# Step 4 - Certificates and upgrades are your job (slide 7)
########################################################
# kubeadm made the certificates of the cluster. They expire one year after kubeadm init.
sudo kubeadm certs check-expiration

# EKS upgrades and patches the control plane for you. Here you plan the upgrade yourself.
sudo kubeadm upgrade plan 2>&1 | tail -15
# It only reads. It changes nothing.

########################################################
# Step 5 - How a self-managed worker joins      (slide 10)
########################################################
# A managed node group joins by itself. Our workers joined with a bootstrap token.
sudo kubeadm token list

# The command that a new EC2 worker would run to join the cluster:
sudo kubeadm token create --print-join-command
# kubeadm join 172.31.x.x:6443 --token ... --discovery-token-ca-cert-hash sha256:...

kubectl get nodes -o wide

########################################################
# Step 6 - Drain a node, as AWS does for a managed node group (slide 11)
########################################################
kubectl create deployment kubia --image=maziar/kubia:v1 --replicas=4
kubectl rollout status deployment/kubia
kubectl get pods -l app=kubia -o wide             # spread over both workers

# Maintenance on workernode2: stop new Pods there, then move its Pods away.
kubectl cordon workernode2
kubectl drain workernode2 --ignore-daemonsets --delete-emptydir-data
kubectl get pods -l app=kubia -o wide             # all four on workernode1
kubectl get nodes                                 # workernode2 SchedulingDisabled

# The maintenance is done. Let the node take Pods again.
kubectl uncordon workernode2
kubectl get nodes

########################################################
# Step 7 - Pod addresses: an overlay, not VPC addresses (slide 14)
########################################################
# The VPC CNI of EKS gives every Pod a real VPC address. Flannel gives an overlay network.
kubectl get nodes -o wide                         # INTERNAL-IP 172.31.x.x: the VPC
kubectl get pods -l app=kubia -o wide             # IP 10.244.x.x: the overlay
kubectl get pods -n kube-flannel -o wide          # one Flannel Pod per node

# The VXLAN device that carries Pod traffic between the nodes:
ip -4 addr show flannel.1

########################################################
# Step 8 - The API endpoint is private          (slide 15)
########################################################
# The security group of this week does not open 6443 to the internet.
kubectl cluster-info                              # https://172.31.x.x:6443, a private address

# ON YOUR OWN MACHINE: the public address of the master does not answer.
# ON YOUR OWN MACHINE:  curl -sk --max-time 5 https://<MASTER-PUBLIC-IP>:6443/version; echo "exit $?"
# exit 28 is a time-out. Like an EKS private endpoint, the API answers only inside the VPC.

# ON THE MASTER: the same call works.
curl -sk https://localhost:6443/version

########################################################
# Step 9 - Who are you? Authentication and authorization (slide 16)
########################################################
# EKS maps your IAM identity to a Kubernetes user. kubeadm gave us a client certificate.
kubectl auth whoami
# Username kubernetes-admin, Groups [kubeadm:cluster-admins system:authenticated]

# The kubeconfig holds the API address, the certificate and the context.
kubectl config view --minify

# RBAC decides what the user can do. This group is bound to cluster-admin.
kubectl get clusterrolebinding kubeadm:cluster-admins -o wide
kubectl auth can-i '*' '*' --all-namespaces       # yes

########################################################
# Step 10 - Infrastructure as code: Terraform, not CloudFormation (slide 17)
########################################################
# eksctl writes CloudFormation stacks. Our cluster is Terraform state on your laptop.
# ON YOUR OWN MACHINE:  terraform state list
# ON YOUR OWN MACHINE:  terraform output public_ips

# On EKS the control plane costs 0.10 USD per hour, and the workers are billed as well.
# Here you pay only for the three EC2 machines, and you run everything yourself.

########################################################
# Step 11 - Clean up                            (slide 18)
########################################################
# ON THE MASTER - remove the Kubernetes objects.
bash cleanup_lab09.sh

# Confirm that nothing is left.
kubectl get pods,deployments | grep -E 'kubia|no-scheduler'

# ON YOUR OWN MACHINE - remove the three EC2 machines.
# ON YOUR OWN MACHINE:  terraform destroy

# Always destroy. The Learner Lab budget is small.
