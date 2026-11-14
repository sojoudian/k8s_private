# -*- coding: utf-8 -*-
"""CLO835 - move Assignment 2 and the 17 semester project files from kind to
the kubeadm cluster of the labs (Week 05 Terraform: 1 master, 2 workers on EC2).

Each input file is read and never written. The output is the next version
(<name>_v2.docx) beside it. Only the named text changes.

Run from the project root:   python retarget_kind_docx.py
It is guarded, so importing it writes nothing.
"""
import glob
import os
import sys

from retarget_docx import retarget

SC_URL = ("https://raw.githubusercontent.com/sojoudian/clo835-mirrors/main/"
          "local-path-provisioner/v0.0.37/local-path-storage.yaml")
MS_URL = ("https://raw.githubusercontent.com/sojoudian/clo835-mirrors/main/"
          "metrics-server/v0.7.1/components.yaml")
KEDA_PATH = "keda/2.21.0/keda-2.21.0.yaml"
CLUSTER = "The Week 05 kubeadm cluster: 1 master and 2 workers on EC2"
REBUILD = "for a new cluster, terraform destroy and terraform apply in Week05"

# ----------------------------------------------------------------- Assignment 2
ASSIGNMENT2 = [
    ("The containerized application will run on the local Kubernetes cluster (kind) you created in the Week 4/5 lab. "
     "No cloud (EKS) resources are required for this assignment, so it has no impact on your AWS budget.",
     "The containerized application will run on the three-node kubeadm cluster (1 control plane and 2 workers on EC2) "
     "that you built in the Week 04 and Week 05 labs. Build it with the Week05 Terraform of the course repository. "
     "No EKS is required, but the three EC2 machines use your Learner Lab budget, so destroy the cluster when you "
     "finish for the day."),
    ("running three replicas of the application on your kind cluster,",
     "running three replicas of the application on your kubeadm cluster,"),
    ("kind (Kubernetes in Docker) to run a local Kubernetes cluster",
     "Terraform and kubeadm (the Week 05 lab) to build a three-node Kubernetes cluster on EC2"),
    ("On the kind cluster, a Deployment", "On the kubeadm cluster, a Deployment"),
    ("so it can be reached from the host.", "so it can be reached on the public IP of every node."),
    ("Apply them to your kind cluster with kubectl apply -f.",
     "Apply them on the control plane machine of your kubeadm cluster with kubectl apply -f."),
    ("On your kind cluster, apply the manifests",
     "On the control plane machine of your kubeadm cluster, apply the manifests"),
    ("(for example via curl to the NodePort)",
     "(for example via curl to the NodePort on the public IP of a node)"),
    ("Make sure your kind cluster from the Week 4/5 lab is running, Docker is running, and kubectl is installed "
     "at the same minor version as your cluster.",
     "Build the Week 05 kubeadm cluster (cd Week05, terraform init, terraform apply), connect to the control plane "
     "machine with ssh, and make sure that Docker runs on your local machine."),
    ("docker version, kubectl version, and kind get clusters should all succeed.",
     "docker version must succeed on your local machine, and kubectl get nodes must show three Ready nodes on the "
     "control plane machine."),
    ("Reach the application from the host and confirm the 0.2 message.",
     "Reach the application on the public IP of a node and confirm the 0.2 message."),
    ("When finished, you may delete the resources with kubectl delete -f and end your lab session.",
     "When finished, delete the resources with kubectl delete -f, run terraform destroy on your local machine, "
     "and end your lab session."),
    ("https://kind.sigs.k8s.io/docs/user/quick-start/",
     "https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/", "exact"),
    ("it is reachable from the host and serves", "it is reachable on the public IP of a node and serves"),
]

# ------------------------------------------------- semester projects: every file
COMMON = [
    ("on your own kind cluster from raw Kubernetes manifests",
     "on your own kubeadm cluster from raw Kubernetes manifests"),
    ("(everything runs inside kind on your own EC2/Cloud9 host)",
     "(everything runs on your own Week 05 kubeadm cluster: 1 master and 2 workers on EC2; a project that uses a "
     "PVC installs the standard StorageClass in bootstrap.sh with kubectl apply -f " + SC_URL + ")"),
    ("brings the entire project up from a clean host (Docker, kind, kubectl only) in 15 minutes or less",
     "brings the entire project up on a fresh Week 05 cluster in 15 minutes or less"),
    ("Everything in git: kind-config.yaml, ", "Everything in git: "),
    ("kind-config.yaml, bootstrap.sh", "bootstrap.sh"),
    ("How to bootstrap from a clean host", "How to bootstrap on a fresh Week 05 cluster"),
    ("from a clean host (no kind cluster)", "from a fresh Week 05 cluster"),
    ("from a clean host (no cluster)", "from a fresh Week 05 cluster"),
    ("go from a clean host", "go from a fresh Week 05 cluster"),
    ("from a clean host in", "on a fresh Week 05 cluster in"),
    ("on a clean host in", "on a fresh Week 05 cluster in"),
    ("from a clean host", "on a fresh Week 05 cluster"),
    ("the kind standard StorageClass", "the standard StorageClass"),
    ("kind standard StorageClass", "standard StorageClass"),
    ("produces a working cluster, ", "produces "),
    ("live from your own host", "live from your own Week 05 cluster"),
    ("on your own host", "on your own Week 05 cluster"),
    ("git clone or git checkout it on your host", "git clone or git checkout it on the master of your Week 05 cluster"),
]

PER = {
    "00": [
        ("present one real Kubernetes system on your own kind cluster.",
         "present one real Kubernetes system on your own kubeadm cluster (the Week 05 cluster: 1 master and 2 "
         "workers on EC2)."),
        ("in weight and depth: kind, raw manifests,", "in weight and depth: kubeadm, raw manifests,"),
        ("run your bootstrap.sh on a clean host (Docker, kind, and kubectl only), and get",
         "run your bootstrap.sh on a fresh Week 05 cluster, and get"),
        ("Everything runs inside kind on your own EC2 or Cloud9 host, from raw Kubernetes YAML",
         "Everything runs on your own Week 05 kubeadm cluster on EC2 (1 master and 2 workers, built with the "
         "Week 05 Terraform), from raw Kubernetes YAML"),
    ],
    "01": [
        ("MySQL StatefulSet on a kind cluster where", "MySQL StatefulSet on a kubeadm cluster where"),
        ("kind cluster with 1 control-plane node and 2 worker nodes, defined in kind-config.yaml committed to your repo.",
         CLUSTER + ", built with the Week 05 Terraform of the course repository."),
        ("Storage: the kind built-in standard StorageClass (local-path). No other provisioner.",
         "Storage: the standard StorageClass (local-path), the course copy of the provisioner that kind uses. "
         "bootstrap.sh installs it with kubectl apply -f " + SC_URL + ". No other provisioner."),
        ("nothing to install on the host beyond kind, kubectl, and Docker)", "nothing to install beyond kubectl on the master)"),
        ("(kind delete cluster + ./bootstrap.sh)",
         "(kubectl delete namespace mysql-<studentID> + ./bootstrap.sh; " + REBUILD + ")"),
        ("kind-config.yaml", "README.md: how to build the Week 05 cluster (terraform apply)", "exact"),
        ("Show where that data lives on the kind node",
         "Show where that data lives on the worker node (under /opt/local-path-provisioner)"),
        ("from a clean host with only Docker/kind/kubectl installed, creates the kind cluster from kind-config.yaml, "
         "applies every manifest,",
         "on the master of a fresh Week 05 cluster, installs the standard StorageClass, applies every manifest,"),
    ],
    "02": [
        ("MongoDB replica set on kind using", "MongoDB replica set on a kubeadm cluster using"),
        ("kind cluster with 1 control-plane and 2 workers, defined in kind-config.yaml in your repo, so the three "
         "mongo pods can spread across nodes.",
         CLUSTER + ", so the three mongo pods can spread across nodes."),
        ("Tooling: only what the course used - kind, kubectl, docker.",
         "Tooling: only what the course used - kubectl on the master."),
        ("How to tear down and rebuild: kind delete cluster then re-bootstrap.",
         "How to tear down and rebuild: kubectl delete namespace mongo-<studentID> then re-bootstrap; " + REBUILD + "."),
    ],
    "03": [
        ("PostgreSQL cluster in kind -", "PostgreSQL cluster in a kubeadm cluster -"),
        ("kind cluster with 1 control-plane + 2 workers, defined in kind-config.yaml (checked into git). Primary and standby",
         CLUSTER + ". Primary and standby"),
        ("Storage: the kind default standard StorageClass (local-path) via volumeClaimTemplates.",
         "Storage: the standard StorageClass (local-path) via volumeClaimTemplates."),
        ("How to tear down and rebuild: kind delete cluster + re-run bootstrap.",
         "How to tear down and rebuild: kubectl delete namespace pg-<studentID> + re-run bootstrap; " + REBUILD + "."),
        ("kind-config.yaml", "README.md: how to build the Week 05 cluster (terraform apply)", "exact"),
    ],
    "04": [
        ("self-healing Redis deployment in kind:", "self-healing Redis deployment in a kubeadm cluster:"),
        ("kind cluster with 1 control-plane + 2 worker nodes, defined in kind-config.yaml committed to your repo.",
         CLUSTER + "."),
        ("Tooling: kubectl, kind, docker only. redis-cli runs inside the pods - do not install it on the host.",
         "Tooling: kubectl only. redis-cli runs inside the pods - do not install it on the master."),
        ("manifests/ (all YAML + kind-config.yaml)", "manifests/ (all YAML)"),
        ("bootstrap.sh must, from a clean host: create the kind cluster from kind-config.yaml, apply all manifests,",
         "bootstrap.sh must, on a fresh Week 05 cluster: apply all manifests,"),
    ],
    "05": [
        ("Build a MySQL database in kind whose", "Build a MySQL database in a kubeadm cluster whose"),
        ("kind cluster from a committed config file: 1 control-plane + 1 worker (kind-config.yaml in the repo). "
         "Cluster name backup-<studentID>.",
         CLUSTER + " (this project needs one worker). The cluster keeps its default kubeadm name; your student ID "
         "goes into the namespace and resource names."),
        ("Storage: kind's built-in standard StorageClass (local-path). No NFS needed.",
         "Storage: the standard StorageClass (local-path). No NFS needed."),
        ("Tooling on the host: docker, kind, kubectl, git. Nothing else.",
         "Tooling on the master: kubectl and git. Nothing else."),
        ("kind delete cluster --name backup-<studentID> && ./bootstrap.sh.",
         "kubectl delete namespace proj5-<studentID> && ./bootstrap.sh; " + REBUILD + "."),
        ("kind-config.yaml, README.md", "README.md (how to build the Week 05 cluster)", "exact"),
        ("stands up everything from a clean host: creates the kind cluster from kind-config.yaml, applies all manifests in order,",
         "stands up everything on a fresh Week 05 cluster: installs the standard StorageClass, applies all manifests in order,"),
    ],
    "06": [
        ("on kind cluster a, then migrate the data live to a freshly created kind cluster b on the same host - "
         "freeze writes, dump with a Kubernetes Job, transfer the dump through the host filesystem,",
         "on kubeadm cluster a, then migrate the data live to a freshly created kubeadm cluster b - freeze writes, "
         "dump with a Kubernetes Job, copy the dump through your workstation with kubectl cp,"),
        ("Two kind clusters on your single EC2/Cloud9 host: kind create cluster --name a and kind create cluster "
         "--name b (single-node each is fine; contexts kind-a and kind-b).",
         "Two kubeadm clusters on EC2: cluster a from the Week 05 Terraform and cluster b from the Week 04 "
         "Terraform of the course repository (their resource names differ, so both run at the same time: 6 "
         "machines). On your workstation (the laptop that runs Terraform), copy /etc/kubernetes/admin.conf from "
         "each master, set its server to https://<master-public-ip>:6443, and name the contexts a and b."),
        ("Cluster b may be created during the demo - bootstrap timing includes it.",
         "Cluster b may be created during the demo with terraform apply in Week04 - bootstrap timing includes it."),
        ("Extra tooling on the host: only sha256sum, curl, docker, kind, kubectl - all already taught or preinstalled.",
         "Extra tooling on your workstation: only sha256sum, curl, kubectl and terraform - all already taught or "
         "preinstalled."),
        ("Operating two independent kind clusters on one host and switching between them with kubectl contexts "
         "(kind-a, kind-b).",
         "Operating two independent kubeadm clusters from one workstation and switching between them with kubectl "
         "contexts (a, b)."),
        ("How to create and prepare cluster b: kind create cluster --name b, kubectl --context kind-b apply -f manifests/b/.",
         "How to create and prepare cluster b: terraform apply in Week04, add its kubeconfig as context b, "
         "install the standard StorageClass on it (kubectl --context b apply -f " + SC_URL + "), then "
         "kubectl --context b apply -f manifests/b/."),
        ("and where the dump lands on the host.", "and how you copy the dump to your workstation with kubectl cp."),
        ("bootstrap.sh brought cluster a from clean host to seeded, serving app",
         "bootstrap.sh brought cluster a from a fresh Week 05 cluster to a seeded, serving app"),
        ("Create/confirm cluster b: kind create cluster --name b (or show it pre-created), apply manifests/b/,",
         "Create/confirm cluster b: terraform apply in Week04 (or show it pre-created), apply manifests/b/ with "
         "--context b,"),
        ("(and optionally pre-create cluster b) from a clean host in under 15 minutes",
         "(and optionally pre-create cluster b) on a fresh Week 05 cluster in under 15 minutes"),
        ("--context kind-a", "--context a"),
        ("verify.sh kind-a", "verify.sh a"),
        ("verify.sh kind-b", "verify.sh b"),
        ("(kind standard StorageClass)", "(standard StorageClass)"),
        ("a NodePort Service app-<studentID> reachable from the host.",
         "a NodePort Service app-<studentID> reachable on the public IP of each node of cluster a."),
        ("and writes it to a hostPath-mounted directory so the file lands on the host (e.g. /tmp/migrate-<studentID>/dump.sql).",
         "and writes it to a PVC dump-<studentID>. Copy the file to your workstation with kubectl --context a cp "
         "from a helper pod that mounts that PVC (e.g. to /tmp/migrate-<studentID>/dump.sql)."),
        ("a Job on cluster b that mounts the same host directory via hostPath and restores dump.sql into the empty DB.",
         "a Job on cluster b that mounts a PVC dump-<studentID>, into which you copied dump.sql with kubectl "
         "--context b cp, and restores it into the empty DB."),
        ("All names, namespaces, and host paths must derive", "All names, namespaces, and file paths must derive"),
        ("live from your own host", "live from your own workstation"),
        ("./scripts/probe.sh http://<host>:<nodePortA>/", "./scripts/probe.sh http://<node-public-ip-of-a>:<nodePortA>/"),
        ("Your restore Job uses hostPath. Why does that work here, and why would this exact transfer design fail if "
         "clusters a and b were on different hosts?",
         "Your dump moves from cluster a to cluster b through your workstation with kubectl cp. Why can a hostPath "
         "volume not carry it, now that clusters a and b run on different machines?"),
    ],
    "07": [
        ("both running in kind, where", "both running in a kubeadm cluster, where"),
        ("kind cluster from a committed config file kind-config.yaml: 1 control-plane + 1 worker (multi-node so "
         "MySQL and the app land on the worker via a nodeSelector - keeps the demo honest about scheduling).",
         CLUSTER + ". bootstrap.sh labels one worker, and MySQL and the app land on it via a nodeSelector - keeps "
         "the demo honest about scheduling."),
        ("Extra tooling: none beyond kind, kubectl, docker, and the mysql client",
         "Extra tooling: none beyond kubectl and the mysql client"),
        ("reachable from the host (map the NodePort in kind-config.yaml with extraPortMappings).",
         "reachable at http://<node-public-ip>:<nodePort> (the Week 05 security group opens 30000-32767)."),
        ("bootstrap.sh: from a clean host, creates the kind cluster from kind-config.yaml, applies all manifests in order,",
         "bootstrap.sh: on a fresh Week 05 cluster, installs the standard StorageClass, labels the worker, applies "
         "all manifests in order,"),
        ("idempotent enough to re-run after kind delete cluster.",
         "idempotent enough to re-run after kubectl delete -f manifests/."),
        ("streamed to the host via kubectl exec/kubectl cp", "streamed to the master via kubectl exec/kubectl cp"),
        ("nothing to install on the host).", "nothing to install on the master)."),
    ],
    "08": [
        ("Build a 4-node kind cluster (1 control-plane + 3 workers) running two identical web apps",
         "Use the 3-node Week 05 kubeadm cluster (1 master + 2 workers) to run two identical web apps"),
        ("kind cluster from a checked-in config file kind-config.yaml: 1 control-plane + 3 workers. Name the cluster "
         "maint-<studentID>.",
         CLUSTER + " (workernode1 and workernode2). The cluster keeps its default kubeadm name; your student ID "
         "goes into the namespace maint-<studentID>."),
        ("plus a public NFS server image (e.g. itsthenetwork/nfs-server-alpine or equivalent). No other tooling "
         "beyond kind, kubectl, and docker.",
         "plus the NFS server image maziar/nfs-server-alpine. No other tooling beyond kubectl. The Week 05 Ubuntu "
         "nodes have no NFS client: bootstrap.sh installs nfs-common on both workers before it creates the NFS PV "
         "(for example over SSH with your Week 05 key), and the runbook shows how you verified it."),
        ("How to tear down: kind delete cluster --name maint-<studentID>.",
         "How to tear down: kubectl delete namespace maint-<studentID>, then kubectl delete pv pv-nfs-<studentID>."),
        ("Bootstrap from a clean host to both apps", "Bootstrap from a fresh Week 05 cluster to both apps"),
        ("walk through kind-config.yaml and the two volume designs", "walk through the node labels and the two volume designs"),
        ("Tear down with kind delete cluster --name maint-<studentID> if time allows.",
         "Tear down with kubectl delete namespace maint-<studentID> if time allows."),
        ("Commit kind-config.yaml defining 1 control-plane and 3 workers. Workers must be identifiable in kubectl "
         "get nodes output (default names maint-<studentID>-worker, -worker2, -worker3 are fine).",
         "Use the Week 05 cluster: 1 master and 2 workers. Workers must be identifiable in kubectl get nodes output "
         "(the Week 05 names workernode1 and workernode2 are fine)."),
        ("bootstrap.sh must: create the kind cluster from kind-config.yaml, label the worker,",
         "bootstrap.sh must: install nfs-common on the workers, label the worker,"),
        ("Clean host to fully running in under 15 minutes.", "Fresh Week 05 cluster to fully running in under 15 minutes."),
    ],
    "09": [
        ("kind cluster with 1 control-plane + 2 workers, defined in kind-config.yaml (workers so you can show pods "
         "on different nodes mounting the same share).",
         CLUSTER + " (workers so you can show pods on different nodes mounting the same share)."),
        ("NFS client utilities must be present on the kind nodes - document in the runbook whether your kind node "
         "image already includes them (the standard kindest/node image does) and how you verified.",
         "NFS client utilities must be present on the nodes. The Week 05 Ubuntu nodes do not include them: "
         "bootstrap.sh installs nfs-common on every node (for example over SSH with your Week 05 key), and the "
         "runbook documents how you verified it."),
        ("Runs entirely on your single EC2/Cloud9 host. No Helm, no cloud storage.",
         "Runs entirely on your Week 05 cluster. No Helm, no cloud storage."),
        ("(kind's local-path StorageClass)", "(the local-path standard StorageClass)"),
        ("How to tear down: kind delete cluster.",
         "How to tear down: kubectl delete namespace nfs-<studentID>, then kubectl delete pv pv-nfs-<studentID>."),
        ("Tear down with kind delete cluster.",
         "Tear down with kubectl delete namespace nfs-<studentID> and kubectl delete pv pv-nfs-<studentID>."),
        ("via kind's local-path provisioner.", "via the local-path provisioner."),
        ("stand up everything from a clean host: create the kind cluster from kind-config.yaml, apply all manifests in order,",
         "stand up everything on a fresh Week 05 cluster: install the standard StorageClass and nfs-common, apply "
         "all manifests in order,"),
        ("Images: itsthenetwork/nfs-server-alpine:latest (or k8s-ganesha) for the server;",
         "Images: maziar/nfs-server-alpine:latest for the server;"),
        ("using itsthenetwork/nfs-server-alpine (or ganesha), exporting", "using maziar/nfs-server-alpine, exporting"),
    ],
    "10": [
        ("Build a single kind cluster that safely hosts", "Set up the Week 05 kubeadm cluster so that it safely hosts"),
        ("kind cluster with 1 control-plane and 2 workers, defined in kind-config.yaml in your repo. Cluster name "
         "multitenant-<studentID>.",
         CLUSTER + ". The cluster keeps its default kubeadm name; your student ID goes into the namespace names."),
        ("Repo layout: kind-config.yaml, manifests/", "Repo layout: manifests/"),
        ("Tooling: kubectl and kind only.", "Tooling: kubectl only."),
    ],
    "11": [
        ("Build a kind cluster with three least-privilege identities",
         "On the Week 05 kubeadm cluster, build three least-privilege identities"),
        ("kind cluster from a committed config file kind-config.yaml: 1 control-plane + 1 worker (RBAC needs no "
         "special topology; the worker proves your manifests do not assume a single node).",
         CLUSTER + " (RBAC needs no special topology; the workers prove your manifests do not assume a single node)."),
        ("Tooling: kubectl, kind, jq", "Tooling: kubectl, jq"),
        ("export KUBECONFIG=$(kind get kubeconfig-path 2>/dev/null || echo ~/.kube/config) with the admin context",
         "export KUBECONFIG=~/.kube/config (the copy of /etc/kubernetes/admin.conf on the master) with the "
         "kubernetes-admin context"),
        ("Commit kind-config.yaml and a bootstrap.sh that creates the cluster, the namespace rbac-<studentID>,",
         "Commit a bootstrap.sh that creates the namespace rbac-<studentID>,"),
        ("the kind-generated admin kubeconfig (kind get kubeconfig) or the kubernetes-admin context.",
         "the kubeadm admin kubeconfig (/etc/kubernetes/admin.conf, copied to ~/.kube/config on the master) with "
         "the kubernetes-admin context."),
    ],
    "12": [
        ("Build a two-tier app in kind - a small web app", "Build a two-tier app in a kubeadm cluster - a small web app"),
        ("kind cluster from a config file committed to the repo: 1 control-plane + 2 workers (kind-config.yaml), "
         "cluster name clo835-<studentID>.",
         CLUSTER + ". The cluster keeps its default kubeadm name; your student ID goes into the resource names."),
        ("manifests/ (all YAML including kind-config.yaml and the env-var variant)",
         "manifests/ (all YAML including the env-var variant)"),
        ("NodePort Service webapp-<studentID> exposing the app, with the port mapped in kind-config.yaml via "
         "extraPortMappings so curl http://localhost:<port>/ works from the host.",
         "NodePort Service webapp-<studentID> exposing the app, so curl http://localhost:<nodePort>/ works on the "
         "master and http://<node-public-ip>:<nodePort>/ works from a browser."),
        ("bootstrap.sh stands up everything - kind cluster, namespace,",
         "bootstrap.sh stands up everything - the standard StorageClass, namespace,"),
        ("curl http://localhost:<port>/ - show the seeded row", "curl http://localhost:<nodePort>/ on the master - show the seeded row"),
    ],
    "13": [
        ("Build a CPU-bound web app on a kind cluster,", "Build a CPU-bound web app on a kubeadm cluster,"),
        ("kind cluster from a config file checked into git: 1 control-plane + 2 workers, cluster name <studentID>-hpa.",
         CLUSTER + ". The cluster keeps its default kubeadm name; the namespace is <studentID>-hpa."),
        ("Why metrics-server does not work out of the box on kind,", "Why metrics-server does not work out of the box on kubeadm,"),
        ("runbook.md, kind-config.yaml, evidence/", "runbook.md, evidence/"),
        ("why the --kubelet-insecure-tls patch is required on kind and what",
         "why the --kubelet-insecure-tls patch is required on kubeadm and what"),
        ("Write kind-config.yaml (1 control-plane, 2 workers) and create the cluster as <studentID>-hpa in bootstrap.sh.",
         "Build the Week 05 cluster (1 master, 2 workers) with terraform apply, and create the namespace "
         "<studentID>-hpa in bootstrap.sh."),
        ("bootstrap.sh stands up everything from a clean host - kind cluster, metrics-server,",
         "bootstrap.sh stands up everything on a fresh Week 05 cluster - metrics-server,"),
        ("The stock registry.k8s.io/hpa-example is also acceptable.", "The course image maziar/hpa-example is also acceptable."),
        ("metrics-server installed from its upstream manifest, patched in your repo",
         "metrics-server installed from the course copy of its manifest (" + MS_URL + ", image maziar/metrics-server), "
         "patched in your repo"),
        ("or the hey binary on the host.", "or the hey binary on the master."),
        ("why kind needs it (kubelet serving certs", "why kubeadm needs it (kubelet serving certs"),
    ],
    "14": [
        ("kind cluster from a config file committed to git: 1 control-plane + 2 workers, cluster name clinic-<studentID>.",
         CLUSTER + ". The cluster keeps its default kubeadm name; the namespace is clinic-<studentID>."),
        ("Tooling: kubectl, docker, kind, nslookup/dig inside the debug pod.",
         "Tooling: kubectl, and nslookup/dig inside the debug pod."),
        ("How to bootstrap the whole project from a clean host (./bootstrap.sh)",
         "How to bootstrap the whole project on a fresh Week 05 cluster (./bootstrap.sh)"),
        ("bootstrap.sh: from a clean host, creates the kind cluster from the config file, builds nothing at demo time",
         "bootstrap.sh: on a fresh Week 05 cluster, builds nothing at demo time"),
        ("busybox:1.36 or nicolaka/netshoot for the debug pod", "busybox:1.36 or maziar/netshoot for the debug pod"),
        ("type NodePort, reachable with curl from the host.", "type NodePort, reachable with curl on the public IP of a node."),
        ("Everything in git: kind config, all manifests", "Everything in git: all manifests"),
        ("manifests/ (kind config, all YAML including", "manifests/ (all YAML including"),
    ],
    "15": [
        ("kind cluster named probe-<studentID> with 1 control-plane + 2 workers, defined in kind-config.yaml "
         "(committed to the repo).",
         CLUSTER + ". The cluster keeps its default kubeadm name; your student ID goes into the namespace "
         "probes-<studentID>."),
        ("bootstrap.sh at repo root: creates the kind cluster from kind-config.yaml, applies all manifests in order, "
         "waits for rollout, and finishes with all 3 pods Ready in under 15 minutes from a clean host.",
         "bootstrap.sh at repo root: applies all manifests in order, waits for rollout, and finishes with all 3 "
         "pods Ready in under 15 minutes on a fresh Week 05 cluster."),
        ("Dockerfile, app source, kind-config.yaml, all manifests", "Dockerfile, app source, all manifests"),
        ("A curl client pod (curlimages/curl)", "A curl client pod (maziar/curl)"),
    ],
    "16": [
        ("observable on a single kind cluster.", "observable on a single kubeadm cluster."),
        ("One kind cluster on your EC2 or Cloud9 host.", "One kubeadm cluster: the Week 05 cluster on EC2 (1 master and 2 workers)."),
        ("bootstrap.sh brings the whole system up on a clean host (Docker, kind, kubectl only) in 15 minutes or less",
         "bootstrap.sh brings the whole system up on a fresh Week 05 cluster in 15 minutes or less"),
        ("so a clean host with only Docker, kind, and kubectl comes up to a fully working orchestrator (cluster, KEDA,",
         "so a fresh Week 05 cluster comes up to a fully working orchestrator (KEDA,"),
        ("KEDA: installed from its official pinned YAML bundle vendored into your repo",
         "KEDA: installed from the pinned course copy of its YAML bundle (" + KEDA_PATH + " in sojoudian/clo835-mirrors, "
         "images on maziar), vendored into your repo"),
        ("Install KEDA from its official pinned release manifest (kubectl apply -f keda-<version>.yaml), vendored into "
         "your repo under manifests/.",
         "Install KEDA from the course copy of its pinned release manifest (" + KEDA_PATH + " in "
         "sojoudian/clo835-mirrors, applied with kubectl apply --server-side -f), vendored into your repo under manifests/."),
    ],
}


def jobs():
    yield ("Assignments/Assignment_2/CLO835_Assignment2.docx",
           "Assignments/Assignment_2/CLO835_Assignment2_v2.docx", ASSIGNMENT2)
    for src in sorted(glob.glob("project/Project_*.docx")):
        if src.endswith("_v2.docx"):
            continue
        tag = os.path.basename(src)[8:10]
        yield (src, src[:-5] + "_v2.docx", PER.get(tag, []) + COMMON)


if __name__ == "__main__":
    bad = 0
    for src, out, pairs in jobs():
        if os.path.exists(out):
            sys.exit("refusing to overwrite " + out)
        done, missed = retarget(src, out, pairs)
        print("%-62s %3d replacements" % (out, sum(done.values())))
        own = [m for m in missed if m in {p[0] for p in pairs[:len(pairs) - len(COMMON)]}] if src.startswith("project") else missed
        if own:
            bad += 1
            for m in own:
                print("    NOT FOUND:", m[:90])
    sys.exit(1 if bad else 0)
