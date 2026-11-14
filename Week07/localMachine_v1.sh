#!/bin/bash
# CLO835 - Week 07 - Volumes: attaching disk storage to containers.
# Run these ON THE MASTER NODE, section by section. Do NOT run the whole file.
#
# Terraform builds 3 machines: 1 control plane and 2 workers. The cluster forms
# itself at boot, the same way it did in Weeks 04 to 06. The master also runs an
# NFS server (/srv/nfs) for Workshop 5, and every node has the NFS client.
#
# Each step matches one slide of Lab_week07_v1.pptx.

########################################################
# Step 0 - check the cluster                    (slide 3)
########################################################
# All three nodes must reach Ready. The workers take a few minutes to join.
kubectl get nodes -o wide
kubectl get pods -n kube-system

########################################################
# Step 1 - Two containers, one emptyDir volume  (slide 4)
########################################################
# The fortune Pod of the lecture: html-generator writes a new fortune
# every 10 seconds into an emptyDir, and nginx serves the same folder.
cat > fortune-pod.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: fortune
spec:
  containers:
  - image: maziar/fortune:env
    name: html-generator
    env:
    - name: INTERVAL
      value: "10"
    volumeMounts:
    - name: html
      mountPath: /var/htdocs
  - image: nginx:alpine
    name: web-server
    volumeMounts:
    - name: html
      mountPath: /usr/share/nginx/html
      readOnly: true
    ports:
    - containerPort: 80
  volumes:
  - name: html
    emptyDir: {}
EOF
kubectl apply -f fortune-pod.yaml
kubectl wait --for=condition=Ready pod/fortune --timeout=120s
kubectl get pod fortune -o wide

# The master reaches each Pod IP. Call nginx two times, 10 s apart.
POD_IP=$(kubectl get pod fortune -o jsonpath='{.status.podIP}')
curl -s http://$POD_IP; sleep 10; curl -s http://$POD_IP

# The writer and the reader are two containers. One volume joins them.
kubectl logs fortune -c html-generator --tail=3

########################################################
# Step 2 - The volume shadows the folder        (slide 5)
########################################################
# nginx:alpine ships index.html and 50x.html in /usr/share/nginx/html.
# The emptyDir is mounted over that folder, so only the fortune file is there.
kubectl exec fortune -c web-server -- ls -l /usr/share/nginx/html

# web-server mounts the volume read-only. Try to write a file.
kubectl exec fortune -c web-server -- sh -c 'echo hi > /usr/share/nginx/html/x.html'
# sh: can't create /usr/share/nginx/html/x.html: Read-only file system

# The emptyDir is a folder on the node that runs the Pod:
#   /var/lib/kubelet/pods/<pod-uid>/volumes/kubernetes.io~empty-dir/html
kubectl get pod fortune -o jsonpath='{.metadata.uid}{"\n"}'

########################################################
# Step 3 - The volume lives as long as the Pod  (slide 6)
########################################################
# A container restart keeps the volume. Stop nginx: the container exits,
# and the kubelet starts it again in the same Pod.
kubectl exec fortune -c web-server -- nginx -s stop
sleep 5; kubectl get pod fortune        # RESTARTS is now 1
curl -s http://$POD_IP                 # the fortune file is still there

# A new Pod gets a new, empty volume. Delete the Pod and create it again.
kubectl delete pod fortune
kubectl apply -f fortune-pod.yaml
kubectl wait --for=condition=Ready pod/fortune --timeout=120s
kubectl exec fortune -c web-server -- stat -c '%y' /usr/share/nginx/html/index.html
# The file is new: its time is the start of the new Pod.

########################################################
# Step 4 - gitRepo is deprecated: an init container clones (slide 9)
########################################################
# The gitRepo volume type is deprecated. explain says so.
kubectl explain pod.spec.volumes.gitRepo | head -8

# The pattern of the lecture: an init container clones the
# repository into an emptyDir, and nginx serves it.
cat > gitrepo-volume-pod.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: gitrepo-volume-pod
spec:
  initContainers:
  - name: git-clone
    image: maziar/alpine-git
    args:
    - clone
    - https://github.com/sojoudian/kubia-website-example
    - /repo
    volumeMounts:
    - name: html
      mountPath: /repo
  containers:
  - image: nginx:alpine
    name: web-server
    volumeMounts:
    - name: html
      mountPath: /usr/share/nginx/html
      readOnly: true
  volumes:
  - name: html
    emptyDir: {}
EOF
kubectl apply -f gitrepo-volume-pod.yaml
kubectl wait --for=condition=Ready pod/gitrepo-volume-pod --timeout=120s
kubectl get pod gitrepo-volume-pod   # STATUS Running, after Init:0/1
kubectl logs gitrepo-volume-pod -c git-clone

# nginx serves the files of the repository.
GIT_IP=$(kubectl get pod gitrepo-volume-pod -o jsonpath='{.status.podIP}')
curl -s http://$GIT_IP | head -5

########################################################
# Step 5 - hostPath keeps data on one node      (slide 12)
########################################################
# A hostPath volume is a folder of the node. It outlives the Pod.
cat > hostpath-pod.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: hostpath-pod
spec:
  nodeSelector:
    kubernetes.io/hostname: workernode1
  containers:
  - name: shell
    image: busybox:1.36
    command: ["sleep", "3600"]
    volumeMounts:
    - name: node-data
      mountPath: /data
  volumes:
  - name: node-data
    hostPath:
      path: /tmp/clo835-week07
      type: DirectoryOrCreate
EOF
# Run the Pod on workernode1 and write a file into the volume.
kubectl apply -f hostpath-pod.yaml
kubectl wait --for=condition=Ready pod/hostpath-pod --timeout=60s
kubectl exec hostpath-pod -- sh -c 'date > /data/written-by-pod.txt'

# Delete the Pod, start it again on the same node: the file is there.
kubectl delete pod hostpath-pod --now
kubectl apply -f hostpath-pod.yaml
kubectl wait --for=condition=Ready pod/hostpath-pod --timeout=60s
kubectl exec hostpath-pod -- cat /data/written-by-pod.txt

# Move the Pod to workernode2: the folder there is empty.
kubectl delete pod hostpath-pod --now
sed 's/workernode1/workernode2/' hostpath-pod.yaml | kubectl apply -f -
kubectl wait --for=condition=Ready pod/hostpath-pod --timeout=60s
kubectl exec hostpath-pod -- ls -l /data
# Empty: the data stayed on workernode1.

########################################################
# Step 6 - A StorageClass for the cluster       (slide 15)
########################################################
# On EKS, the EBS CSI driver provisions a disk for each claim. This cluster has no cloud
# driver, so we install the local-path provisioner from the course mirror.
kubectl apply -f https://raw.githubusercontent.com/sojoudian/clo835-mirrors/main/local-path-provisioner/v0.0.37/local-path-storage.yaml
kubectl -n local-path-storage rollout status deploy/local-path-provisioner

# One StorageClass, the default. A claim with no class gets it.
kubectl get storageclass
# NAME                 PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE
# standard (default)   rancher.io/local-path   Delete          WaitForFirstConsumer

# A PersistentVolume is an API resource. A plain volume is not.
kubectl api-resources | grep -i persistentvolume

########################################################
# Step 7 - A PersistentVolumeClaim requests the storage (slide 16)
########################################################
# The claim asks for 1 Gi of the standard class.
cat > my-claim.yaml <<'EOF'
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-claim
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: standard
  resources:
    requests:
      storage: 1Gi
EOF
kubectl apply -f my-claim.yaml

# WaitForFirstConsumer: no PV is made until a Pod
# uses the claim, so the claim stays Pending.
kubectl get pvc my-claim
kubectl describe pvc my-claim | tail -3
kubectl get pv

########################################################
# Step 8 - The Pod mounts the volume through the claim (slide 17)
########################################################
cat > pod-using-my-claim.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: pod-using-my-claim
spec:
  containers:
  - name: shell
    image: busybox:1.36
    command: ["sleep", "3600"]
    volumeMounts:
    - mountPath: /my-data
      name: my-volume
  volumes:
  - name: my-volume
    persistentVolumeClaim:
      claimName: my-claim
EOF
kubectl apply -f pod-using-my-claim.yaml
kubectl wait --for=condition=Ready pod/pod-using-my-claim --timeout=120s
kubectl get pvc,pv                 # Bound, and a new PV

# Write data, delete the Pod, mount the same claim again.
kubectl exec pod-using-my-claim -- sh -c 'echo kept > /my-data/note.txt'
kubectl delete pod pod-using-my-claim --now
kubectl apply -f pod-using-my-claim.yaml
kubectl wait --for=condition=Ready pod/pod-using-my-claim --timeout=120s
kubectl exec pod-using-my-claim -- cat /my-data/note.txt

# 'kept': the claim outlives the Pod. This PV is a folder of
# one node, so the Pod returns to that node:
kubectl describe pv | grep -A3 'Node Affinity'

########################################################
# Step 9 - One NFS share, two Pods on two nodes (slide 20)
########################################################
# Terraform made an NFS server on the master: /srv/nfs. Every
# node has the NFS client (nfs-common) from bootstrap.sh.
sudo exportfs -v
NFS_IP=$(kubectl get node masternode -o jsonpath='{.status.addresses[0].address}')
echo $NFS_IP                  # the private IP of the master

# No quotes on EOF: the shell writes the address into the file.
cat > nfs-pod.yaml <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: NAME
spec:
  nodeSelector:
    kubernetes.io/hostname: NODE
  containers:
  - name: shell
    image: busybox:1.36
    command: ["sleep", "3600"]
    volumeMounts:
    - name: my-nfs-volume
      mountPath: /my-nfs
  volumes:
  - name: my-nfs-volume
    nfs:
      server: $NFS_IP
      path: /srv/nfs
EOF
for n in 1 2; do sed "s/NAME/nfs-pod-$n/;s/NODE/workernode$n/" nfs-pod.yaml | kubectl apply -f -; done
kubectl wait --for=condition=Ready pod/nfs-pod-1 pod/nfs-pod-2 --timeout=120s
kubectl get pods nfs-pod-1 nfs-pod-2 -o wide

# Write on workernode1, read on workernode2.
kubectl exec nfs-pod-1 -- sh -c 'date > /my-nfs/hello.txt'
kubectl exec nfs-pod-2 -- cat /my-nfs/hello.txt
# One share for two nodes: an NFS volume is not tied to a node.

########################################################
# Step 10 - Clean up                            (slide 21)
########################################################
# ON THE MASTER - remove the Kubernetes objects.
bash cleanup_lab07.sh

# Confirm that nothing is left.
kubectl get pods,pvc,pv

# ON YOUR OWN MACHINE - remove the three EC2 machines.
# ON YOUR OWN MACHINE:  terraform destroy

# Always destroy. The Learner Lab budget is small.
