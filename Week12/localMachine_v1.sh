#!/bin/bash
# CLO835 - Week 12 - ConfigMaps and Secrets.
# Run these ON THE MASTER NODE, section by section. Do NOT run the whole file.
#
# Terraform builds 3 machines: 1 control plane and 2 workers. The cluster forms
# itself at boot, the same way it did in Weeks 04 to 10. Every object of the lab
# lives in the namespace week12, except the dev and prod namespaces of Workshop 3.
#
# Each step matches one slide of Lab_week12_v1.pptx.

########################################################
# Step 0 - check the cluster                    (slide 3)
########################################################
# All three nodes must reach Ready. The workers take a few minutes to join.
kubectl get nodes -o wide
kubectl get pods -n kube-system

########################################################
# Step 1 - Override CMD with args               (slide 4)
########################################################
# One namespace for the whole lab, so cleanup is one command.
kubectl create namespace week12

# The image: ENTRYPOINT ["/bin/fortuneloop.sh"], CMD ["10"].
# args replaces CMD. The Pod writes a fortune every 2 s.
cat > fortune-args.yaml <<'EOF'
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
# Configured to generate new fortune every 2 seconds

########################################################
# Step 2 - Override ENTRYPOINT with command     (slide 5)
########################################################
# command replaces ENTRYPOINT, and args replaces CMD.
# Docker ENTRYPOINT = Kubernetes command;
# Docker CMD = Kubernetes args.
cat > ubuntu-sleeper.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: ubuntu-sleeper-pod
spec:
  restartPolicy: Never
  containers:
  - name: ubuntu-sleeper
    image: ubuntu:24.04
    command: ["sleep"]
    args: ["10"]
EOF
kubectl apply -f ubuntu-sleeper.yaml -n week12
kubectl get pod ubuntu-sleeper-pod -n week12 -w   # Running, then Completed. Ctrl+C
kubectl get pod ubuntu-sleeper-pod -n week12 -o yaml | grep -A3 'command:'

########################################################
# Step 3 - An environment variable in the Pod manifest (slide 8)
########################################################
# A variable is set per container, not per Pod.
cat > fortune-env.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: fortune-env
spec:
  containers:
  - image: maziar/fortune:env
    name: html-generator
    env:
    - name: INTERVAL
      value: "30"
EOF
kubectl apply -f fortune-env.yaml -n week12
kubectl wait --for=condition=Ready pod/fortune-env -n week12 --timeout=120s
kubectl exec fortune-env -n week12 -- printenv INTERVAL
kubectl logs fortune-env -n week12 --tail=2

# Kubernetes adds a variable for each Service as well.
kubectl exec fortune-env -n week12 -- printenv | grep KUBERNETES_SERVICE

# The drawback: 30 is hard coded in the manifest. A
# different value for prod means a different manifest.

########################################################
# Step 4 - Create ConfigMaps: from a literal and from a file (slide 11)
########################################################
# Imperative, from a literal:
kubectl create configmap fortune-config --from-literal=sleep-interval=25 -n week12

# Imperative, from a file: the file name becomes the key.
printf 'APP_COLOR=blue\nAPP_MODE=prod\n' > app_config.properties
kubectl create configmap app-config-file --from-file=app_config.properties -n week12

kubectl get configmaps -n week12
kubectl get configmap app-config-file -n week12 -o yaml

########################################################
# Step 5 - Create a ConfigMap: declarative      (slide 12)
########################################################
# The same key/value pairs, as a manifest you can commit.
cat > config-map.yaml <<'EOF'
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_COLOR: blue
  APP_MODE: prod
EOF
kubectl create -f config-map.yaml -n week12
kubectl describe configmap app-config -n week12

########################################################
# Step 6 - Inject a ConfigMap: envFrom and one key (slide 13)
########################################################
# envFrom injects every key. configMapKeyRef injects one
# key under a name you choose.
cat > config-env.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: config-env
spec:
  containers:
  - name: app
    image: busybox:1.36
    command: ["sleep", "3600"]
    envFrom:
    - configMapRef:
        name: app-config
    env:
    - name: INTERVAL
      valueFrom:
        configMapKeyRef:
          name: fortune-config
          key: sleep-interval
EOF
kubectl apply -f config-env.yaml -n week12
kubectl wait --for=condition=Ready pod/config-env -n week12 --timeout=60s
kubectl exec config-env -n week12 -- printenv APP_COLOR APP_MODE INTERVAL
# blue
# prod
# 25

########################################################
# Step 7 - Mount a ConfigMap as a volume        (slide 14)
########################################################
# Each key becomes a file in the mounted folder.
cat > config-volume.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: config-volume
spec:
  containers:
  - name: app
    image: busybox:1.36
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
kubectl wait --for=condition=Ready pod/config-volume -n week12 --timeout=60s
kubectl exec config-volume -n week12 -- ls /etc/app-config
kubectl exec config-volume -n week12 -- cat /etc/app-config/APP_COLOR

# Change the ConfigMap. The file follows in about a minute;
# an environment variable never changes in a running Pod.
kubectl patch configmap app-config -n week12 -p '{"data":{"APP_COLOR":"green"}}'
sleep 90; kubectl exec config-volume -n week12 -- cat /etc/app-config/APP_COLOR
kubectl exec config-env -n week12 -- printenv APP_COLOR       # still blue

########################################################
# Step 8 - One Pod manifest, two environments   (slide 15)
########################################################
# The same manifest in two namespaces. Each namespace has
# its own app-config with its own values.
kubectl create namespace dev; kubectl create namespace prod
kubectl create configmap app-config -n dev --from-literal=APP_MODE=development
kubectl create configmap app-config -n prod --from-literal=APP_MODE=production
cat > mode-pod.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: mode
spec:
  containers:
  - name: app
    image: busybox:1.36
    command: ["sleep", "3600"]
    envFrom:
    - configMapRef:
        name: app-config
EOF
kubectl apply -f mode-pod.yaml -n dev; kubectl apply -f mode-pod.yaml -n prod
kubectl wait --for=condition=Ready pod/mode -n dev --timeout=60s
kubectl wait --for=condition=Ready pod/mode -n prod --timeout=60s
kubectl exec mode -n dev -- printenv APP_MODE      # development
kubectl exec mode -n prod -- printenv APP_MODE     # production

########################################################
# Step 9 - Create a Secret: imperative          (slide 18)
########################################################
kubectl create secret generic app-secret -n week12 \
    --from-literal=DB_Host=mysql --from-literal=DB_User=root --from-literal=DB_Password=paswrd
kubectl get secret app-secret -n week12 -o yaml

# The values are base64. That is an encoding, not encryption: anyone can decode it.
echo -n paswrd | base64            # cGFzd3Jk
echo cGFzd3Jk | base64 -d; echo    # paswrd

########################################################
# Step 10 - Create a Secret: declarative, with base64 values (slide 19)
########################################################
# In a manifest you write the values already encoded.
# Make the same Secret again from the file.
kubectl delete secret app-secret -n week12
cat > secret-data.yaml <<'EOF'
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
data:
  DB_Host: bXlzcWw=
  DB_User: cm9vdA==
  DB_Password: cGFzd3Jk
EOF
kubectl create -f secret-data.yaml -n week12
kubectl get secret app-secret -n week12 -o jsonpath='{.data.DB_Password}' | base64 -d; echo

# Never commit a file like this to Git: it holds the
# password in a form that anyone can decode.

########################################################
# Step 11 - Inject a Secret: one key and a volume (slide 20)
########################################################
# secretKeyRef works like configMapKeyRef. A Secret volume
# gives one file per key, decoded for the application.
cat > secret-pod.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: secret-pod
spec:
  containers:
  - name: app
    image: busybox:1.36
    command: ["sleep", "3600"]
    env:
    - name: DB_Password
      valueFrom:
        secretKeyRef:
          name: app-secret
          key: DB_Password
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
kubectl wait --for=condition=Ready pod/secret-pod -n week12 --timeout=60s
kubectl exec secret-pod -n week12 -- printenv DB_Password
kubectl exec secret-pod -n week12 -- ls /etc/secret-volume
kubectl exec secret-pod -n week12 -- cat /etc/secret-volume/DB_Host

# The Secret volume is in memory (tmpfs), never on disk.
kubectl exec secret-pod -n week12 -- mount | grep secret-volume

########################################################
# Step 12 - Why an environment variable is a risk for a Secret (slide 21)
########################################################
# A child process inherits every environment variable of its parent:
kubectl exec secret-pod -n week12 -- sh -c 'sh -c "echo the child sees: \$DB_Password"'

# A program that logs or dumps its environment exposes the password:
kubectl exec secret-pod -n week12 -- sh -c 'tr "\0" "\n" < /proc/1/environ | grep DB_'

# A file in a tmpfs volume goes to no log and to no child process. Prefer the volume.

########################################################
# Step 13 - The service account token in every Pod (slide 22)
########################################################
# Every Pod gets a token, a CA certificate and its namespace, in a tmpfs volume.
kubectl exec secret-pod -n week12 -- ls /var/run/secrets/kubernetes.io/serviceaccount
# ca.crt  namespace  token
kubectl exec secret-pod -n week12 -- mount | grep serviceaccount

# Since Kubernetes 1.24 the token is projected and expires. No Secret object holds it:
kubectl get secrets -n week12                      # only app-secret
kubectl get pod secret-pod -n week12 -o jsonpath='{.spec.volumes[*].name}{"\n"}'
# app-secret-volume kube-api-access-xxxxx

########################################################
# Step 14 - Secrets in etcd are not encrypted   (slide 23)
########################################################
# By default etcd stores a Secret as plain bytes. Read it from etcd directly.
ETCD="etcdctl --endpoints=https://127.0.0.1:2379 \
    --cacert=/etc/kubernetes/pki/etcd/ca.crt \
    --cert=/etc/kubernetes/pki/etcd/server.crt \
    --key=/etc/kubernetes/pki/etcd/server.key"
kubectl -n kube-system exec etcd-masternode -- $ETCD get /registry/secrets/week12/app-secret | grep -a -o paswrd
# paswrd: the password, in plain text, in the cluster database.

# Protect it: turn on encryption at rest, limit who can read Secrets with RBAC,
# or keep the value in an external secret store.

########################################################
# Step 15 - Clean up                            (slide 24)
########################################################
# ON THE MASTER - remove the Kubernetes objects.
bash cleanup_lab12.sh

# Confirm that nothing is left.
kubectl get namespaces | grep -E 'week12|dev|prod'

# ON YOUR OWN MACHINE - remove the three EC2 machines.
# ON YOUR OWN MACHINE:  terraform destroy

# Always destroy. The Learner Lab budget is small.
