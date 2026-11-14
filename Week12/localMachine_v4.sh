#!/bin/bash
# CLO835 - Week 12 - ConfigMaps and Secrets.
# Run these ON THE MASTER NODE, section by section. Do NOT run the whole file.
#
# Terraform builds 3 machines: 1 control plane and 2 workers. The cluster forms
# itself at boot, the same way it did in Weeks 04 to 10. The objects of the lab
# live in the namespaces week12 and week12-dev.
#
# Each step matches one slide of Lab_week12_v4.pptx.

########################################################
# Step 0 - check the cluster                    (slide 3)
########################################################
# All three nodes must reach Ready. The workers take a few minutes to join.
kubectl get nodes -o wide
kubectl get pods -n kube-system

########################################################
# Step 1 - args replace the CMD of the image    (slide 4)
########################################################
# One namespace for the whole lab.
kubectl create namespace week12

# The image: ENTRYPOINT ["/bin/fortuneloop.sh"], CMD ["10"].
# args replaces CMD, and command would replace
# ENTRYPOINT. This Pod writes a fortune every 2 s.
# tee writes the file and shows it.
tee fortune-args.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: fortune-args
spec:
  containers:
  - image: maziar/fortune:args
    name: html-generator
    args: ["2"]
EOF
kubectl apply -f fortune-args.yaml -n week12
kubectl wait --for=condition=Ready pod/fortune-args -n week12 --timeout=120s
sleep 6; kubectl logs fortune-args -n week12 --tail=4

########################################################
# Step 2 - Environment variables from a ConfigMap (slide 5)
########################################################
# The ConfigMap keeps the values out of the manifest.
kubectl create configmap app-config -n week12 \
    --from-literal=APP_COLOR=blue --from-literal=APP_MODE=prod

# --from-file makes one key from a file.
printf 'LOG_LEVEL=debug\n' > app.properties
kubectl create configmap app-file -n week12 --from-file=app.properties -o yaml

# env sets one value. configMapKeyRef reads one key.
# envFrom injects every key.
tee config-env.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: config-env
spec:
  containers:
  - name: app
    image: maziar/alpine-curl
    command: ["sleep", "3600"]
    env:
    - name: GREETING
      value: hello
    - name: COLOR
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: APP_COLOR
    envFrom:
    - configMapRef:
        name: app-config
EOF
kubectl apply -f config-env.yaml -n week12
kubectl wait --for=condition=Ready pod/config-env -n week12 --timeout=120s
kubectl exec config-env -n week12 -- printenv GREETING COLOR APP_COLOR APP_MODE

########################################################
# Step 3 - A ConfigMap as a volume              (slide 6)
########################################################
# Each key becomes a file in the mounted folder.
tee config-volume.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: config-volume
spec:
  containers:
  - name: app
    image: maziar/alpine-curl
    command: ["sleep", "3600"]
    volumeMounts:
    - name: app-config-volume
      mountPath: /etc/app-config
  volumes:
  - name: app-config-volume
    configMap:
      name: app-config
EOF
kubectl apply -f config-volume.yaml -n week12
kubectl wait --for=condition=Ready pod/config-volume -n week12 --timeout=120s
kubectl exec config-volume -n week12 -- ls /etc/app-config
kubectl exec config-volume -n week12 -- cat /etc/app-config/APP_COLOR; echo

# Change the ConfigMap. The file follows in about a
# minute. A variable never changes in a running Pod.
kubectl patch configmap app-config -n week12 -p '{"data":{"APP_COLOR":"green"}}'
sleep 90; kubectl exec config-volume -n week12 -- cat /etc/app-config/APP_COLOR; echo
kubectl exec config-env -n week12 -- printenv APP_COLOR     # still blue

########################################################
# Step 4 - A Secret as a variable and as a volume (slide 7)
########################################################
# --from-file makes one key from a file. The file name is the key.
printf 'paswrd' > DB_Password
kubectl create secret generic app-secret -n week12 \
    --from-literal=DB_Host=mysql --from-file=DB_Password
# base64 is an encoding, not encryption.
kubectl get secret app-secret -n week12 -o jsonpath='{.data.DB_Password}' | base64 -d; echo

# secretKeyRef reads one key. secretRef injects every key.
tee secret-pod.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: secret-pod
spec:
  containers:
  - name: app
    image: maziar/alpine-curl
    command: ["sleep", "3600"]
    env:
    - name: DB_Password
      valueFrom:
        secretKeyRef:
          name: app-secret
          key: DB_Password
    envFrom:
    - secretRef:
        name: app-secret
    volumeMounts:
    - name: app-secret-volume
      mountPath: /etc/secret-volume
      readOnly: true
  volumes:
  - name: app-secret-volume
    secret:
      secretName: app-secret
EOF
kubectl apply -f secret-pod.yaml -n week12
kubectl wait --for=condition=Ready pod/secret-pod -n week12 --timeout=120s
kubectl exec secret-pod -n week12 -- printenv DB_Password DB_Host
kubectl exec secret-pod -n week12 -- cat /etc/secret-volume/DB_Host; echo
# On the node, the volume is in memory (tmpfs), not on the disk.
kubectl exec secret-pod -n week12 -- mount | grep secret-volume

# The Pod also gets a ServiceAccount token as files. No Secret holds it.
kubectl exec secret-pod -n week12 -- ls /var/run/secrets/kubernetes.io/serviceaccount
kubectl get secrets -n week12     # app-secret only

########################################################
# Step 5 - A second environment, and a Secret in etcd (slide 8)
########################################################
# The same Pod manifest in a second namespace gets other values.
tee config-dev.yaml <<'EOF'
apiVersion: v1
kind: Namespace
metadata:
  name: week12-dev
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: week12-dev
data:
  APP_COLOR: red
  APP_MODE: dev
---
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
  namespace: week12-dev
data:
  DB_Password: ZGV2LXBhc3M=
EOF
kubectl apply -f config-dev.yaml
kubectl apply -f config-env.yaml -n week12-dev
kubectl wait --for=condition=Ready pod/config-env -n week12-dev --timeout=120s
kubectl exec config-env -n week12-dev -- printenv APP_COLOR APP_MODE   # red, dev
kubectl get secret app-secret -n week12-dev \
    -o jsonpath='{.data.DB_Password}' | base64 -d; echo

# By default etcd stores a Secret as plain bytes. Read it from etcd.
ETCD="etcdctl --endpoints=https://127.0.0.1:2379 \
    --cacert=/etc/kubernetes/pki/etcd/ca.crt \
    --cert=/etc/kubernetes/pki/etcd/server.crt \
    --key=/etc/kubernetes/pki/etcd/server.key"
kubectl -n kube-system exec etcd-masternode -- $ETCD \
    get /registry/secrets/week12/app-secret | grep -a -o paswrd
# paswrd: the password, in plain text, in the cluster database.
# Protect it: encryption at rest, RBAC, or an external secret store.

########################################################
# Step 6 - Clean up                             (slide 9)
########################################################
# ON THE MASTER - remove the Kubernetes objects.
bash cleanup_lab12.sh

# Confirm that nothing is left.
kubectl get namespaces | grep week12

# ON YOUR OWN MACHINE - remove the three EC2 machines.
# ON YOUR OWN MACHINE:  terraform destroy          # asks for key_name again

# Always destroy. The Learner Lab budget is small.
