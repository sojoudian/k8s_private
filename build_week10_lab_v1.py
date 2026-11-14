# -*- coding: utf-8 -*-
"""CLO835 Week 10 - PV, PVC, StorageClass and StatefulSets, on the kubeadm cluster.

The lecture (Week10/Week09_lecture_style_v7.pptx) teaches hostPath, the
PersistentVolume and its claim, binding, StorageClasses and dynamic
provisioning, and StatefulSets: stable names, per-pod storage, the headless
Service and peer discovery with DNS SRV records. The old lab ran on Amazon EKS
with EBS; this one runs on the kubeadm cluster with hostPath and the
local-path provisioner of the course mirror.

Outputs: Week10/Lab_week10_v1.pptx, Week10/localMachine_v1.sh,
Week10/Lab_week10_Blackboard_Submission.md, ~/Documents/c/r/CLO835_Fall_2026/Week10/
Run from the project root. It is guarded, so importing it writes nothing.
"""
import sys

import lab_kubeadm as L

F = L.FILE_MARK
SC_URL = L.MIRRORS + "local-path-provisioner/v0.0.37/local-path-storage.yaml"
PROXY = "localhost:8001/api/v1/namespaces/default"
MONGO_PUT = "$ kubectl exec mongodb -- mongosh mystore --quiet --eval 'db.foo.insertOne({name:\"foo\"})'"
MONGO_GET = "$ kubectl exec mongodb -- mongosh mystore --quiet --eval 'db.foo.find()'"

MONGO_HOSTPATH = """apiVersion: v1
kind: Pod
metadata:
  name: mongodb
spec:
  nodeSelector:
    kubernetes.io/hostname: workernode1
  containers:
  - image: mongo:7
    name: mongodb
    volumeMounts:
    - name: mongodb-data
      mountPath: /data/db
    ports:
    - containerPort: 27017
  volumes:
  - name: mongodb-data
    hostPath:
      path: /tmp/mongodb
      type: DirectoryOrCreate""".split("\n")

MONGO_PV = """apiVersion: v1
kind: PersistentVolume
metadata:
  name: mongodb-pv
spec:
  capacity:
    storage: 1Gi
  accessModes:
  - ReadWriteOnce
  - ReadOnlyMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: ""
  hostPath:
    path: /tmp/mongodb-pv
    type: DirectoryOrCreate""".split("\n")

MONGO_PVC = """apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mongodb-pvc
spec:
  resources:
    requests:
      storage: 1Gi
  accessModes:
  - ReadWriteOnce
  storageClassName: \"\"""".split("\n")

MONGO_POD_PVC = """apiVersion: v1
kind: Pod
metadata:
  name: mongodb
spec:
  nodeSelector:
    kubernetes.io/hostname: workernode1
  containers:
  - image: mongo:7
    name: mongodb
    volumeMounts:
    - name: mongodb-data
      mountPath: /data/db
  volumes:
  - name: mongodb-data
    persistentVolumeClaim:
      claimName: mongodb-pvc""".split("\n")

SC_FAST = """apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast
provisioner: rancher.io/local-path
reclaimPolicy: Delete
volumeBindingMode: WaitForFirstConsumer
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: redis-data
spec:
  storageClassName: fast
  resources:
    requests:
      storage: 100Mi
  accessModes:
  - ReadWriteOnce""".split("\n")

REDIS = """apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
spec:
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:7
        args: ["--appendonly", "yes"]
        volumeMounts:
        - name: data
          mountPath: /data
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: redis-data""".split("\n")

HEADLESS = """apiVersion: v1
kind: Service
metadata:
  name: kubia
spec:
  clusterIP: None
  selector:
    app: kubia
  ports:
  - name: http
    port: 80
    targetPort: 8080""".split("\n")

STS = """apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: kubia
spec:
  serviceName: kubia
  replicas: 2
  selector:
    matchLabels: {app: kubia}
  template:
    metadata:
      labels: {app: kubia}
    spec:
      containers:
      - name: kubia
        image: maziar/kubia-pet
        ports:
        - {name: http, containerPort: 8080}
        volumeMounts:
        - {name: data, mountPath: /var/data}
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources: {requests: {storage: 1Mi}}""".split("\n")

PUBLIC = """apiVersion: v1
kind: Service
metadata:
  name: kubia-public
spec:
  selector:
    app: kubia
  ports:
  - port: 80
    targetPort: 8080""".split("\n")

SLIDES = [
 ("title", "Workshop 1 – Exploring hostPath"),
 ("prereq",),
 ("cluster",),
 ("step2", "MongoDB on a hostPath volume", "bash", [
  "# MongoDB keeps its files in /data/db: a folder of workernode1.",
  "$ cat > mongodb-hostpath.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f mongodb-hostpath.yaml",
  "$ kubectl wait --for=condition=Ready pod/mongodb --timeout=120s",
  "$ sleep 5        # mongod needs a moment after the container starts",
  " ",
  "# Add a sample document to the database mystore.",
  MONGO_PUT,
  MONGO_GET,
  "$ kubectl get pod mongodb -o wide            # NODE workernode1",
  ], "mongodb-hostpath.yaml", "mongodb-hostpath.yaml", MONGO_HOSTPATH),
 ("step", "Delete the Pod: where is the data?", "bash", [
  "# Delete the Pod and create it again on the same node. The data persisted.",
  "$ kubectl delete pod mongodb",
  "$ kubectl apply -f mongodb-hostpath.yaml",
  "$ kubectl wait --for=condition=Ready pod/mongodb --timeout=120s; sleep 5",
  MONGO_GET,
  " ",
  "# What if the Pod is scheduled to a different node? Move it to workernode2.",
  "$ kubectl delete pod mongodb",
  "$ sed 's/workernode1/workernode2/' mongodb-hostpath.yaml | kubectl apply -f -",
  "$ kubectl wait --for=condition=Ready pod/mongodb --timeout=120s; sleep 5",
  MONGO_GET,
  "# Nothing: the data stayed on workernode1. hostPath is not storage for a database.",
  "$ kubectl delete pod mongodb",
  ]),
 ("step", "Why hostPath at all? System Pods use it", "bash", [
  "# kube-proxy needs files of its node: the iptables lock and the kernel modules.",
  "$ kubectl -n kube-system get pods -l k8s-app=kube-proxy -o wide",
  "$ KP=$(kubectl -n kube-system get pods -l k8s-app=kube-proxy -o name | head -1)",
  "$ kubectl -n kube-system get $KP -o jsonpath='{range .spec.volumes[*]}{.name}{\"  \"}{.hostPath.path}{\"\\n\"}{end}'",
  "# xtables-lock  /run/xtables.lock",
  "# lib-modules   /lib/modules",
  ]),
 ("end", "Workshop 1 – The End"),

 ("title", "Workshop 2 – PersistentVolumes and Claims"),
 ("step2", "An administrator creates a PersistentVolume", "bash", [
  "# The admin makes the storage first, out of band, and posts a PV.",
  "# 1 Gi, two access modes, and Retain after the claim goes.",
  "$ cat > mongodb-pv.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f mongodb-pv.yaml",
  "$ kubectl get pv mongodb-pv                  # STATUS Available",
  ], "mongodb-pv.yaml", "mongodb-pv.yaml", MONGO_PV),
 ("step2", "A user claims it: Pending, then Bound", "bash", [
  "# The claim asks for 1 Gi, ReadWriteOnce. storageClassName \"\"",
  "# means: bind to a PV that already exists, provision nothing.",
  "$ cat > mongodb-pvc.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f mongodb-pvc.yaml",
  "$ kubectl get pvc mongodb-pvc                # Bound to mongodb-pv",
  "$ kubectl get pv mongodb-pv                  # Bound, CLAIM default/mongodb-pvc",
  ], "mongodb-pvc.yaml", "mongodb-pvc.yaml", MONGO_PVC),
 ("step2", "The Pod uses the claim, not the storage", "bash", [
  "# The Pod names only the claim. It knows nothing of the disk.",
  "$ cat > mongodb-pod-pvc.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f mongodb-pod-pvc.yaml",
  "$ kubectl wait --for=condition=Ready pod/mongodb --timeout=120s; sleep 5",
  MONGO_PUT,
  " ",
  "# A new Pod with the same claim finds the same data.",
  "$ kubectl delete pod mongodb",
  "$ kubectl apply -f mongodb-pod-pvc.yaml",
  "$ kubectl wait --for=condition=Ready pod/mongodb --timeout=120s; sleep 5",
  MONGO_GET,
  " ",
  "# Delete the claim: Retain keeps the PV, now Released.",
  "$ kubectl delete pod mongodb; kubectl delete pvc mongodb-pvc",
  "$ kubectl get pv mongodb-pv                  # STATUS Released",
  ], "mongodb-pod-pvc.yaml", "mongodb-pod-pvc.yaml", MONGO_POD_PVC),
 ("end", "Workshop 2 – The End"),

 ("title", "Workshop 3 – StorageClasses and Dynamic Provisioning"),
 ("step", "Install a provisioner and list the StorageClasses", "bash", [
  "# The lecture asks: do you have any StorageClass at the moment?",
  "$ kubectl get storageclasses                 # No resources found",
  " ",
  "# Install the local-path provisioner from the course mirror. Its class is standard (default).",
  "$ kubectl apply -f " + SC_URL,
  "$ kubectl -n local-path-storage rollout status deploy/local-path-provisioner",
  "$ kubectl get storageclasses",
  ]),
 ("step2", "A second class, and a claim that names it", "bash", [
  "# A StorageClass names a provisioner. The claim names",
  "# the class: \"use that storage system to make the volume\".",
  "$ cat > storageclass-fast.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f storageclass-fast.yaml",
  "$ kubectl get storageclass",
  " ",
  "# WaitForFirstConsumer: Pending until a Pod uses it.",
  "$ kubectl get pvc redis-data",
  ], "storageclass-fast.yaml", "storageclass-fast.yaml", SC_FAST),
 ("step2", "Redis on a dynamically provisioned volume", "bash", [
  "$ cat > redis.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f redis.yaml",
  "$ kubectl rollout status deployment/redis",
  "$ kubectl get pvc redis-data                 # Bound",
  "$ kubectl get pv                             # made by the provisioner",
  " ",
  "# Store a key, delete the Pod, read the key from the new Pod.",
  "$ kubectl exec deploy/redis -- redis-cli set foo bar",
  "$ kubectl delete pod -l app=redis",
  "$ kubectl rollout status deployment/redis",
  "$ kubectl exec deploy/redis -- redis-cli get foo        # \"bar\"",
  " ",
  "# A local-path PV belongs to one node, so the new Pod",
  "# returns to that node. An EBS volume can move in its AZ.",
  "$ kubectl get pods -l app=redis -o wide",
  ], "redis.yaml", "redis.yaml", REDIS),
 ("end", "Workshop 3 – The End"),

 ("title", "Workshop 4 – StatefulSets"),
 ("step2", "The governing headless Service", "bash", [
  "# clusterIP: None. The Service does not load balance;",
  "# it gives each pet its own DNS name.",
  "$ cat > kubia-headless.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f kubia-headless.yaml",
  "$ kubectl get service kubia                  # CLUSTER-IP None",
  ], "kubia-headless.yaml", "kubia-headless.yaml", HEADLESS),
 ("step2", "A StatefulSet with a volume claim template", "bash", [
  "# The app stores a POST body in /var/data/kubia.txt.",
  "# Each pet gets its own claim from the template.",
  "$ cat > kubia-statefulset.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f kubia-statefulset.yaml",
  " ",
  "# SECOND SSH SESSION - watch the pets start. Ctrl+C to stop.",
  "$ kubectl get pods -l app=kubia -w",
  "# kubia-0 first. kubia-1 starts only when kubia-0 is Ready.",
  " ",
  "$ kubectl get pvc                            # data-kubia-0, data-kubia-1",
  ], "kubia-statefulset.yaml", "kubia-statefulset.yaml", STS),
 ("step", "Talk to each pet through the API server proxy", "bash", [
  "# kubectl proxy listens on 8001 and adds your credentials to each request.",
  "$ kubectl proxy --port=8001 >/dev/null 2>&1 &",
  "$ curl -s " + PROXY + "/pods/kubia-0/proxy/",
  "# You've hit kubia-0",
  "# Data stored on this pod: No data posted yet",
  " ",
  "$ curl -s -X POST -d 'Hey there! This greeting was submitted to kubia-0.' " + PROXY + "/pods/kubia-0/proxy/",
  "$ curl -s " + PROXY + "/pods/kubia-0/proxy/",
  "$ curl -s " + PROXY + "/pods/kubia-1/proxy/      # kubia-1 has its own, empty data",
  ]),
 ("step", "A deleted pet returns with its name and its data", "bash", [
  "$ kubectl delete pod kubia-0",
  "$ kubectl get pods -l app=kubia                   # a new kubia-0 starts",
  "$ kubectl wait --for=condition=Ready pod/kubia-0 --timeout=120s",
  " ",
  "# Same name, same claim data-kubia-0, so the same data. The IP address may be new.",
  "$ curl -s " + PROXY + "/pods/kubia-0/proxy/",
  "$ kubectl get pod kubia-0 -o wide",
  ]),
 ("step2", "A regular ClusterIP Service in front of the pets", "bash", [
  "# One address for clients. It load balances, so each",
  "# call can reach a different pet.",
  "$ cat > kubia-public.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f kubia-public.yaml",
  "$ URL=" + PROXY + "/services/kubia-public/proxy/",
  "$ for i in 1 2 3 4; do curl -s $URL; done",
  ], "kubia-public.yaml", "kubia-public.yaml", PUBLIC),
 ("step", "Discovering peers in a StatefulSet", "bash", [
  "# Kubernetes makes DNS SRV records for the Pods behind a headless Service.",
  "$ kubectl run dnstest --image=maziar/alpine-curl --restart=Never --command -- sleep 3600",
  "$ kubectl wait --for=condition=Ready pod/dnstest --timeout=60s",
  "$ kubectl exec dnstest -- sh -c 'apk add --no-cache bind-tools >/dev/null && dig +short SRV kubia.default.svc.cluster.local'",
  "# 0 50 80 kubia-0.kubia.default.svc.cluster.local.",
  "# 0 50 80 kubia-1.kubia.default.svc.cluster.local.",
  " ",
  "# Each pet has a stable DNS name of its own:",
  "$ kubectl exec dnstest -- nslookup kubia-0.kubia.default.svc.cluster.local",
  ]),
 ("step", "Updating a StatefulSet: a clustered data store", "bash", [
  "# The peers version of the app asks DNS for all pets and collates their data.",
  "$ kubectl set image statefulset/kubia kubia=maziar/kubia-pet-peers",
  "$ kubectl rollout status statefulset/kubia        # kubia-1 first, then kubia-0",
  " ",
  "$ curl -s -X POST -d 'The sun is shining' " + PROXY + "/services/kubia-public/proxy/",
  "$ curl -s -X POST -d 'The rain is falling' " + PROXY + "/services/kubia-public/proxy/",
  "$ curl -s " + PROXY + "/services/kubia-public/proxy/",
  "# One GET returns the data of every pet: the pets found each other through DNS SRV.",
  ]),
 ("step", "Clean up", "bash", [
  "# ON THE MASTER - stop the proxy and remove the Kubernetes objects.",
  "$ bash cleanup_lab10.sh",
  " ",
  "# Confirm that nothing is left.",
  "$ kubectl get pods,pvc,pv,storageclass",
  " ",
  "# ON YOUR OWN MACHINE - remove the three EC2 machines.",
  "L$ terraform destroy",
  " ",
  "# Always destroy. The Learner Lab budget is small.",
  ]),
 ("end", "Workshop 4 – The End"),
]

SCRIPT_HEAD = """#!/bin/bash
# CLO835 - Week 10 - PersistentVolumes, StorageClasses and StatefulSets.
# Run these ON THE MASTER NODE, section by section. Do NOT run the whole file.
#
# Terraform builds 3 machines: 1 control plane and 2 workers. The cluster forms
# itself at boot, the same way it did in Weeks 04 to 09. Workshop 3 installs the
# local-path provisioner from the course mirror, so the cluster gets a default
# StorageClass, as the EBS CSI driver gives one on EKS.
#
# Each step matches one slide of Lab_week10_v1.pptx.
"""

CLEANUP = """pkill -f "kubectl proxy" 2>/dev/null
kubectl delete pod mongodb dnstest --now 2>/dev/null
kubectl delete statefulset kubia 2>/dev/null
kubectl delete service kubia kubia-public 2>/dev/null
kubectl delete deployment redis 2>/dev/null
kubectl delete pvc mongodb-pvc redis-data data-kubia-0 data-kubia-1 2>/dev/null
kubectl delete pv mongodb-pv 2>/dev/null
kubectl delete storageclass fast 2>/dev/null
kubectl delete -f """ + SC_URL + """ 2>/dev/null
rm -f ./mongodb-hostpath.yaml ./mongodb-pv.yaml ./mongodb-pvc.yaml ./mongodb-pod-pvc.yaml ./storageclass-fast.yaml ./redis.yaml ./kubia-headless.yaml ./kubia-statefulset.yaml ./kubia-public.yaml

kubectl get pods,pvc,pv"""

BLACKBOARD = [
 ("hostPath",
  "MongoDB keeps its data in a hostPath folder of workernode1.",
  ["Show the document in mystore after the Pod is deleted and created again on workernode1.",
   "Show the empty result after the Pod moves to workernode2.",
   "Show the hostPath volumes of a kube-proxy Pod.",
   "Explain why hostPath is not suitable for database storage in a multi-node cluster."]),
 ("PersistentVolumes and Claims",
  "An administrator posts a PV. A user claims it. A Pod uses the claim.",
  ["Show the PV Available, then Bound to mongodb-pvc.",
   "Show the document that survives a new Pod with the same claim.",
   "Show the PV Released after the claim is deleted, and explain the Retain policy.",
   "Explain how a claim decouples the Pod from the storage technology."]),
 ("StorageClasses and Dynamic Provisioning",
  "The local-path provisioner makes a PV for each claim.",
  ["Show kubectl get storageclasses before and after the install.",
   "Show the claim redis-data Pending, then Bound, and the PV that the provisioner made.",
   "Show the key foo still present after the Redis Pod is deleted.",
   "Explain WaitForFirstConsumer, and why a local-path PV keeps the Pod on one node."]),
 ("StatefulSets",
  "The kubia StatefulSet runs two pets with stable names, stable DNS names and their own storage.",
  ["Show the pets start in order, and the two claims data-kubia-0 and data-kubia-1.",
   "Show the greeting POSTed to kubia-0, and kubia-0 still holding it after it is deleted.",
   "Show the dig SRV answer of the headless Service.",
   "Show the collated data of all pets after the update to maziar/kubia-pet-peers.",
   "Explain why a Deployment cannot give these guarantees.",
   "Show the clean-up and terraform destroy."]),
]

if __name__ == "__main__":
    L.check_lines(SLIDES)
    L.make_lab("10", SLIDES, "Week10/Lab_week10_v1.pptx", SCRIPT_HEAD, script_path="Week10/localMachine_v1.sh")
    if "--no-repo" not in sys.argv:
        dst, files = L.make_repo_folder("10", "PersistentVolumes, StorageClasses and StatefulSets", CLEANUP,
                                        "Week10/localMachine_v1.sh")
        print("repo folder : %s (%d files)" % (dst, len(files)))
    L.blackboard_text("10", "The Terraform configuration in Week 10 creates the same three Ubuntu 26.04 EC2 "
                      "machines as Weeks 04 to 09.", BLACKBOARD, "Week10/Lab_week10_Blackboard_Submission.md")
    print("blackboard  : Week10/Lab_week10_Blackboard_Submission.md")
