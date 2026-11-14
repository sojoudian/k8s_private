#!/bin/bash
# CLO835 - Week 10 - PersistentVolumes, StorageClasses and StatefulSets.
# Run these ON THE MASTER NODE, section by section. Do NOT run the whole file.
#
# Terraform builds 3 machines: 1 control plane and 2 workers. The cluster forms
# itself at boot, the same way it did in Weeks 04 to 09. Workshop 3 installs the
# local-path provisioner from the course mirror, so the cluster gets a default
# StorageClass, as the EBS CSI driver gives one on EKS.
#
# Each step matches one slide of Lab_week10_v1.pptx.

########################################################
# Step 0 - check the cluster                    (slide 3)
########################################################
# All three nodes must reach Ready. The workers take a few minutes to join.
kubectl get nodes -o wide
kubectl get pods -n kube-system

########################################################
# Step 1 - MongoDB on a hostPath volume         (slide 4)
########################################################
# MongoDB keeps its files in /data/db: a folder of workernode1.
cat > mongodb-hostpath.yaml <<'EOF'
apiVersion: v1
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
      type: DirectoryOrCreate
EOF
kubectl apply -f mongodb-hostpath.yaml
kubectl wait --for=condition=Ready pod/mongodb --timeout=120s
sleep 5        # mongod needs a moment after the container starts

# Add a sample document to the database mystore.
kubectl exec mongodb -- mongosh mystore --quiet --eval 'db.foo.insertOne({name:"foo"})'
kubectl exec mongodb -- mongosh mystore --quiet --eval 'db.foo.find()'
kubectl get pod mongodb -o wide            # NODE workernode1

########################################################
# Step 2 - Delete the Pod: where is the data?   (slide 5)
########################################################
# Delete the Pod and create it again on the same node. The data persisted.
kubectl delete pod mongodb
kubectl apply -f mongodb-hostpath.yaml
kubectl wait --for=condition=Ready pod/mongodb --timeout=120s; sleep 5
kubectl exec mongodb -- mongosh mystore --quiet --eval 'db.foo.find()'

# What if the Pod is scheduled to a different node? Move it to workernode2.
kubectl delete pod mongodb
sed 's/workernode1/workernode2/' mongodb-hostpath.yaml | kubectl apply -f -
kubectl wait --for=condition=Ready pod/mongodb --timeout=120s; sleep 5
kubectl exec mongodb -- mongosh mystore --quiet --eval 'db.foo.find()'
# Nothing: the data stayed on workernode1. hostPath is not storage for a database.
kubectl delete pod mongodb

########################################################
# Step 3 - Why hostPath at all? System Pods use it (slide 6)
########################################################
# kube-proxy needs files of its node: the iptables lock and the kernel modules.
kubectl -n kube-system get pods -l k8s-app=kube-proxy -o wide
KP=$(kubectl -n kube-system get pods -l k8s-app=kube-proxy -o name | head -1)
kubectl -n kube-system get $KP -o jsonpath='{range .spec.volumes[*]}{.name}{"  "}{.hostPath.path}{"\n"}{end}'
# xtables-lock  /run/xtables.lock
# lib-modules   /lib/modules

########################################################
# Step 4 - An administrator creates a PersistentVolume (slide 9)
########################################################
# The admin makes the storage first, out of band, and posts a PV.
# 1 Gi, two access modes, and Retain after the claim goes.
cat > mongodb-pv.yaml <<'EOF'
apiVersion: v1
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
    type: DirectoryOrCreate
EOF
kubectl apply -f mongodb-pv.yaml
kubectl get pv mongodb-pv                  # STATUS Available

########################################################
# Step 5 - A user claims it: Pending, then Bound (slide 10)
########################################################
# The claim asks for 1 Gi, ReadWriteOnce. storageClassName ""
# means: bind to a PV that already exists, provision nothing.
cat > mongodb-pvc.yaml <<'EOF'
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mongodb-pvc
spec:
  resources:
    requests:
      storage: 1Gi
  accessModes:
  - ReadWriteOnce
  storageClassName: ""
EOF
kubectl apply -f mongodb-pvc.yaml
kubectl get pvc mongodb-pvc                # Bound to mongodb-pv
kubectl get pv mongodb-pv                  # Bound, CLAIM default/mongodb-pvc

########################################################
# Step 6 - The Pod uses the claim, not the storage (slide 11)
########################################################
# The Pod names only the claim. It knows nothing of the disk.
cat > mongodb-pod-pvc.yaml <<'EOF'
apiVersion: v1
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
      claimName: mongodb-pvc
EOF
kubectl apply -f mongodb-pod-pvc.yaml
kubectl wait --for=condition=Ready pod/mongodb --timeout=120s; sleep 5
kubectl exec mongodb -- mongosh mystore --quiet --eval 'db.foo.insertOne({name:"foo"})'

# A new Pod with the same claim finds the same data.
kubectl delete pod mongodb
kubectl apply -f mongodb-pod-pvc.yaml
kubectl wait --for=condition=Ready pod/mongodb --timeout=120s; sleep 5
kubectl exec mongodb -- mongosh mystore --quiet --eval 'db.foo.find()'

# Delete the claim: Retain keeps the PV, now Released.
kubectl delete pod mongodb; kubectl delete pvc mongodb-pvc
kubectl get pv mongodb-pv                  # STATUS Released

########################################################
# Step 7 - Install a provisioner and list the StorageClasses (slide 14)
########################################################
# The lecture asks: do you have any StorageClass at the moment?
kubectl get storageclasses                 # No resources found

# Install the local-path provisioner from the course mirror. Its class is standard (default).
kubectl apply -f https://raw.githubusercontent.com/sojoudian/clo835-mirrors/main/local-path-provisioner/v0.0.37/local-path-storage.yaml
kubectl -n local-path-storage rollout status deploy/local-path-provisioner
kubectl get storageclasses

########################################################
# Step 8 - A second class, and a claim that names it (slide 15)
########################################################
# A StorageClass names a provisioner. The claim names
# the class: "use that storage system to make the volume".
cat > storageclass-fast.yaml <<'EOF'
apiVersion: storage.k8s.io/v1
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
  - ReadWriteOnce
EOF
kubectl apply -f storageclass-fast.yaml
kubectl get storageclass

# WaitForFirstConsumer: Pending until a Pod uses it.
kubectl get pvc redis-data

########################################################
# Step 9 - Redis on a dynamically provisioned volume (slide 16)
########################################################
cat > redis.yaml <<'EOF'
apiVersion: apps/v1
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
          claimName: redis-data
EOF
kubectl apply -f redis.yaml
kubectl rollout status deployment/redis
kubectl get pvc redis-data                 # Bound
kubectl get pv                             # made by the provisioner

# Store a key, delete the Pod, read the key from the new Pod.
kubectl exec deploy/redis -- redis-cli set foo bar
kubectl delete pod -l app=redis
kubectl rollout status deployment/redis
kubectl exec deploy/redis -- redis-cli get foo        # "bar"

# A local-path PV belongs to one node, so the new Pod
# returns to that node. An EBS volume can move in its AZ.
kubectl get pods -l app=redis -o wide

########################################################
# Step 10 - The governing headless Service      (slide 19)
########################################################
# clusterIP: None. The Service does not load balance;
# it gives each pet its own DNS name.
cat > kubia-headless.yaml <<'EOF'
apiVersion: v1
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
    targetPort: 8080
EOF
kubectl apply -f kubia-headless.yaml
kubectl get service kubia                  # CLUSTER-IP None

########################################################
# Step 11 - A StatefulSet with a volume claim template (slide 20)
########################################################
# The app stores a POST body in /var/data/kubia.txt.
# Each pet gets its own claim from the template.
cat > kubia-statefulset.yaml <<'EOF'
apiVersion: apps/v1
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
      resources: {requests: {storage: 1Mi}}
EOF
kubectl apply -f kubia-statefulset.yaml

# SECOND SSH SESSION - watch the pets start. Ctrl+C to stop.
kubectl get pods -l app=kubia -w
# kubia-0 first. kubia-1 starts only when kubia-0 is Ready.

kubectl get pvc                            # data-kubia-0, data-kubia-1

########################################################
# Step 12 - Talk to each pet through the API server proxy (slide 21)
########################################################
# kubectl proxy listens on 8001 and adds your credentials to each request.
kubectl proxy --port=8001 >/dev/null 2>&1 &
curl -s localhost:8001/api/v1/namespaces/default/pods/kubia-0/proxy/
# You've hit kubia-0
# Data stored on this pod: No data posted yet

curl -s -X POST -d 'Hey there! This greeting was submitted to kubia-0.' localhost:8001/api/v1/namespaces/default/pods/kubia-0/proxy/
curl -s localhost:8001/api/v1/namespaces/default/pods/kubia-0/proxy/
curl -s localhost:8001/api/v1/namespaces/default/pods/kubia-1/proxy/      # kubia-1 has its own, empty data

########################################################
# Step 13 - A deleted pet returns with its name and its data (slide 22)
########################################################
kubectl delete pod kubia-0
kubectl get pods -l app=kubia                   # a new kubia-0 starts
kubectl wait --for=condition=Ready pod/kubia-0 --timeout=120s

# Same name, same claim data-kubia-0, so the same data. The IP address may be new.
curl -s localhost:8001/api/v1/namespaces/default/pods/kubia-0/proxy/
kubectl get pod kubia-0 -o wide

########################################################
# Step 14 - A regular ClusterIP Service in front of the pets (slide 23)
########################################################
# One address for clients. It load balances, so each
# call can reach a different pet.
cat > kubia-public.yaml <<'EOF'
apiVersion: v1
kind: Service
metadata:
  name: kubia-public
spec:
  selector:
    app: kubia
  ports:
  - port: 80
    targetPort: 8080
EOF
kubectl apply -f kubia-public.yaml
URL=localhost:8001/api/v1/namespaces/default/services/kubia-public/proxy/
for i in 1 2 3 4; do curl -s $URL; done

########################################################
# Step 15 - Discovering peers in a StatefulSet  (slide 24)
########################################################
# Kubernetes makes DNS SRV records for the Pods behind a headless Service.
kubectl run dnstest --image=maziar/alpine-curl --restart=Never --command -- sleep 3600
kubectl wait --for=condition=Ready pod/dnstest --timeout=60s
kubectl exec dnstest -- sh -c 'apk add --no-cache bind-tools >/dev/null && dig +short SRV kubia.default.svc.cluster.local'
# 0 50 80 kubia-0.kubia.default.svc.cluster.local.
# 0 50 80 kubia-1.kubia.default.svc.cluster.local.

# Each pet has a stable DNS name of its own:
kubectl exec dnstest -- nslookup kubia-0.kubia.default.svc.cluster.local

########################################################
# Step 16 - Updating a StatefulSet: a clustered data store (slide 25)
########################################################
# The peers version of the app asks DNS for all pets and collates their data.
kubectl set image statefulset/kubia kubia=maziar/kubia-pet-peers
kubectl rollout status statefulset/kubia        # kubia-1 first, then kubia-0

curl -s -X POST -d 'The sun is shining' localhost:8001/api/v1/namespaces/default/services/kubia-public/proxy/
curl -s -X POST -d 'The rain is falling' localhost:8001/api/v1/namespaces/default/services/kubia-public/proxy/
curl -s localhost:8001/api/v1/namespaces/default/services/kubia-public/proxy/
# One GET returns the data of every pet: the pets found each other through DNS SRV.

########################################################
# Step 17 - Clean up                            (slide 26)
########################################################
# ON THE MASTER - stop the proxy and remove the Kubernetes objects.
bash cleanup_lab10.sh

# Confirm that nothing is left.
kubectl get pods,pvc,pv,storageclass

# ON YOUR OWN MACHINE - remove the three EC2 machines.
# ON YOUR OWN MACHINE:  terraform destroy

# Always destroy. The Learner Lab budget is small.
