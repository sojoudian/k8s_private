# -*- coding: utf-8 -*-
"""CLO835 Week 12 - ConfigMaps and Secrets, on the kubeadm cluster.

The lecture (Week12/Week12_v3.pptx) teaches command-line arguments (ENTRYPOINT
and CMD against command and args), environment variables, ConfigMaps (literal,
file and declarative; envFrom, a single key and a volume; one manifest for many
environments), Secrets (base64, envFrom, a single key, a volume in tmpfs, the
risk of environment variables, the service account token, and etcd without
encryption at rest). The earlier lab practised only one part. This lab practises
all of it.

Outputs: Week12/Lab_week12_v1.pptx, Week12/localMachine_v1.sh,
Week12/Lab_week12_Blackboard_Submission.md, ~/Documents/c/r/CLO835_Fall_2026/Week12/
Run from the project root. It is guarded, so importing it writes nothing.
"""
import sys

import lab_kubeadm as L

F = L.FILE_MARK
N = "-n week12"

ARGS_POD = """apiVersion: v1
kind: Pod
metadata:
  name: fortune-args
spec:
  containers:
  - image: maziar/fortune:args
    name: html-generator
    args: ["2"]""".split("\n")

SLEEPER = """apiVersion: v1
kind: Pod
metadata:
  name: ubuntu-sleeper-pod
spec:
  restartPolicy: Never
  containers:
  - name: ubuntu-sleeper
    image: ubuntu:24.04
    command: ["sleep"]
    args: ["10"]""".split("\n")

ENV_POD = """apiVersion: v1
kind: Pod
metadata:
  name: fortune-env
spec:
  containers:
  - image: maziar/fortune:env
    name: html-generator
    env:
    - name: INTERVAL
      value: "30\"""".split("\n")

CONFIG_MAP = """apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_COLOR: blue
  APP_MODE: prod""".split("\n")

CM_ENV_POD = """apiVersion: v1
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
          key: sleep-interval""".split("\n")

CM_VOL_POD = """apiVersion: v1
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
      name: app-config""".split("\n")

MODE_POD = """apiVersion: v1
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
        name: app-config""".split("\n")

SECRET = """apiVersion: v1
kind: Secret
metadata:
  name: app-secret
data:
  DB_Host: bXlzcWw=
  DB_User: cm9vdA==
  DB_Password: cGFzd3Jk""".split("\n")

SECRET_POD = """apiVersion: v1
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
      secretName: app-secret""".split("\n")

ETCD = [
  '$ ETCD="etcdctl --endpoints=https://127.0.0.1:2379 \\',
  '    --cacert=/etc/kubernetes/pki/etcd/ca.crt \\',
  '    --cert=/etc/kubernetes/pki/etcd/server.crt \\',
  '    --key=/etc/kubernetes/pki/etcd/server.key"',
]

SLIDES = [
 ("title", "Workshop 1 – Command-line Arguments"),
 ("prereq",),
 ("cluster",),
 ("step2", "Override CMD with args", "bash", [
  "# One namespace for the whole lab, so cleanup is one command.",
  "$ kubectl create namespace week12",
  " ",
  "# The image: ENTRYPOINT [\"/bin/fortuneloop.sh\"], CMD [\"10\"].",
  "# args replaces CMD. The Pod writes a fortune every 2 s.",
  "$ cat > fortune-args.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f fortune-args.yaml " + N,
  "$ kubectl wait --for=condition=Ready pod/fortune-args " + N + " --timeout=120s",
  "$ sleep 6; kubectl logs fortune-args " + N + " --tail=4",
  "# Configured to generate new fortune every 2 seconds",
  ], "fortune-args.yaml", "fortune-args.yaml", ARGS_POD),
 ("step2", "Override ENTRYPOINT with command", "bash", [
  "# command replaces ENTRYPOINT, and args replaces CMD.",
  "# Docker ENTRYPOINT = Kubernetes command;",
  "# Docker CMD = Kubernetes args.",
  "$ cat > ubuntu-sleeper.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f ubuntu-sleeper.yaml " + N,
  "$ kubectl get pod ubuntu-sleeper-pod " + N + " -w   # Running, then Completed. Ctrl+C",
  "$ kubectl get pod ubuntu-sleeper-pod " + N + " -o yaml | grep -A3 'command:'",
  ], "ubuntu-sleeper.yaml", "ubuntu-sleeper.yaml", SLEEPER),
 ("end", "Workshop 1 – The End"),

 ("title", "Workshop 2 – Environment Variables"),
 ("step2", "An environment variable in the Pod manifest", "bash", [
  "# A variable is set per container, not per Pod.",
  "$ cat > fortune-env.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f fortune-env.yaml " + N,
  "$ kubectl wait --for=condition=Ready pod/fortune-env " + N + " --timeout=120s",
  "$ kubectl exec fortune-env " + N + " -- printenv INTERVAL",
  "$ kubectl logs fortune-env " + N + " --tail=2",
  " ",
  "# Kubernetes adds a variable for each Service as well.",
  "$ kubectl exec fortune-env " + N + " -- printenv | grep KUBERNETES_SERVICE",
  " ",
  "# The drawback: 30 is hard coded in the manifest. A",
  "# different value for prod means a different manifest.",
  ], "fortune-env.yaml", "fortune-env.yaml", ENV_POD),
 ("end", "Workshop 2 – The End"),

 ("title", "Workshop 3 – ConfigMaps"),
 ("step", "Create ConfigMaps: from a literal and from a file", "bash", [
  "# Imperative, from a literal:",
  "$ kubectl create configmap fortune-config --from-literal=sleep-interval=25 " + N,
  " ",
  "# Imperative, from a file: the file name becomes the key.",
  "$ printf 'APP_COLOR=blue\\nAPP_MODE=prod\\n' > app_config.properties",
  "$ kubectl create configmap app-config-file --from-file=app_config.properties " + N,
  " ",
  "$ kubectl get configmaps " + N,
  "$ kubectl get configmap app-config-file " + N + " -o yaml",
  ]),
 ("step2", "Create a ConfigMap: declarative", "bash", [
  "# The same key/value pairs, as a manifest you can commit.",
  "$ cat > config-map.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl create -f config-map.yaml " + N,
  "$ kubectl describe configmap app-config " + N,
  ], "config-map.yaml", "config-map.yaml", CONFIG_MAP),
 ("step2", "Inject a ConfigMap: envFrom and one key", "bash", [
  "# envFrom injects every key. configMapKeyRef injects one",
  "# key under a name you choose.",
  "$ cat > config-env.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f config-env.yaml " + N,
  "$ kubectl wait --for=condition=Ready pod/config-env " + N + " --timeout=60s",
  "$ kubectl exec config-env " + N + " -- printenv APP_COLOR APP_MODE INTERVAL",
  "# blue",
  "# prod",
  "# 25",
  ], "config-env.yaml", "config-env.yaml", CM_ENV_POD),
 ("step2", "Mount a ConfigMap as a volume", "bash", [
  "# Each key becomes a file in the mounted folder.",
  "$ cat > config-volume.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f config-volume.yaml " + N,
  "$ kubectl wait --for=condition=Ready pod/config-volume " + N + " --timeout=60s",
  "$ kubectl exec config-volume " + N + " -- ls /etc/app-config",
  "$ kubectl exec config-volume " + N + " -- cat /etc/app-config/APP_COLOR",
  " ",
  "# Change the ConfigMap. The file follows in about a minute;",
  "# an environment variable never changes in a running Pod.",
  "$ kubectl patch configmap app-config " + N + " -p '{\"data\":{\"APP_COLOR\":\"green\"}}'",
  "$ sleep 90; kubectl exec config-volume " + N + " -- cat /etc/app-config/APP_COLOR",
  "$ kubectl exec config-env " + N + " -- printenv APP_COLOR       # still blue",
  ], "config-volume.yaml", "config-volume.yaml", CM_VOL_POD),
 ("step2", "One Pod manifest, two environments", "bash", [
  "# The same manifest in two namespaces. Each namespace has",
  "# its own app-config with its own values.",
  "$ kubectl create namespace dev; kubectl create namespace prod",
  "$ kubectl create configmap app-config -n dev --from-literal=APP_MODE=development",
  "$ kubectl create configmap app-config -n prod --from-literal=APP_MODE=production",
  "$ cat > mode-pod.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f mode-pod.yaml -n dev; kubectl apply -f mode-pod.yaml -n prod",
  "$ kubectl wait --for=condition=Ready pod/mode -n dev --timeout=60s",
  "$ kubectl wait --for=condition=Ready pod/mode -n prod --timeout=60s",
  "$ kubectl exec mode -n dev -- printenv APP_MODE      # development",
  "$ kubectl exec mode -n prod -- printenv APP_MODE     # production",
  ], "mode-pod.yaml", "mode-pod.yaml", MODE_POD),
 ("end", "Workshop 3 – The End"),

 ("title", "Workshop 4 – Secrets"),
 ("step", "Create a Secret: imperative", "bash", [
  "$ kubectl create secret generic app-secret " + N + " \\",
  "    --from-literal=DB_Host=mysql --from-literal=DB_User=root --from-literal=DB_Password=paswrd",
  "$ kubectl get secret app-secret " + N + " -o yaml",
  " ",
  "# The values are base64. That is an encoding, not encryption: anyone can decode it.",
  "$ echo -n paswrd | base64            # cGFzd3Jk",
  "$ echo cGFzd3Jk | base64 -d; echo    # paswrd",
  ]),
 ("step2", "Create a Secret: declarative, with base64 values", "bash", [
  "# In a manifest you write the values already encoded.",
  "# Make the same Secret again from the file.",
  "$ kubectl delete secret app-secret " + N,
  "$ cat > secret-data.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl create -f secret-data.yaml " + N,
  "$ kubectl get secret app-secret " + N + " -o jsonpath='{.data.DB_Password}' | base64 -d; echo",
  " ",
  "# Never commit a file like this to Git: it holds the",
  "# password in a form that anyone can decode.",
  ], "secret-data.yaml", "secret-data.yaml", SECRET),
 ("step2", "Inject a Secret: one key and a volume", "bash", [
  "# secretKeyRef works like configMapKeyRef. A Secret volume",
  "# gives one file per key, decoded for the application.",
  "$ cat > secret-pod.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f secret-pod.yaml " + N,
  "$ kubectl wait --for=condition=Ready pod/secret-pod " + N + " --timeout=60s",
  "$ kubectl exec secret-pod " + N + " -- printenv DB_Password",
  "$ kubectl exec secret-pod " + N + " -- ls /etc/secret-volume",
  "$ kubectl exec secret-pod " + N + " -- cat /etc/secret-volume/DB_Host",
  " ",
  "# The Secret volume is in memory (tmpfs), never on disk.",
  "$ kubectl exec secret-pod " + N + " -- mount | grep secret-volume",
  ], "secret-pod.yaml", "secret-pod.yaml", SECRET_POD),
 ("step", "Why an environment variable is a risk for a Secret", "bash", [
  "# A child process inherits every environment variable of its parent:",
  "$ kubectl exec secret-pod " + N + " -- sh -c 'sh -c \"echo the child sees: \\$DB_Password\"'",
  " ",
  "# A program that logs or dumps its environment exposes the password:",
  "$ kubectl exec secret-pod " + N + " -- sh -c 'tr \"\\0\" \"\\n\" < /proc/1/environ | grep DB_'",
  " ",
  "# A file in a tmpfs volume goes to no log and to no child process. Prefer the volume.",
  ]),
 ("step", "The service account token in every Pod", "bash", [
  "# Every Pod gets a token, a CA certificate and its namespace, in a tmpfs volume.",
  "$ kubectl exec secret-pod " + N + " -- ls /var/run/secrets/kubernetes.io/serviceaccount",
  "# ca.crt  namespace  token",
  "$ kubectl exec secret-pod " + N + " -- mount | grep serviceaccount",
  " ",
  "# Since Kubernetes 1.24 the token is projected and expires. No Secret object holds it:",
  "$ kubectl get secrets " + N + "                      # only app-secret",
  "$ kubectl get pod secret-pod " + N + " -o jsonpath='{.spec.volumes[*].name}{\"\\n\"}'",
  "# app-secret-volume kube-api-access-xxxxx",
  ]),
 ("step", "Secrets in etcd are not encrypted", "bash", [
  "# By default etcd stores a Secret as plain bytes. Read it from etcd directly.",
  ] + ETCD + [
  "$ kubectl -n kube-system exec etcd-masternode -- $ETCD get /registry/secrets/week12/app-secret | grep -a -o paswrd",
  "# paswrd: the password, in plain text, in the cluster database.",
  " ",
  "# Protect it: turn on encryption at rest, limit who can read Secrets with RBAC,",
  "# or keep the value in an external secret store.",
  ]),
 ("step", "Clean up", "bash", [
  "# ON THE MASTER - remove the Kubernetes objects.",
  "$ bash cleanup_lab12.sh",
  " ",
  "# Confirm that nothing is left.",
  "$ kubectl get namespaces | grep -E 'week12|dev|prod'",
  " ",
  "# ON YOUR OWN MACHINE - remove the three EC2 machines.",
  "L$ terraform destroy",
  " ",
  "# Always destroy. The Learner Lab budget is small.",
  ]),
 ("end", "Workshop 4 – The End"),
]

SCRIPT_HEAD = """#!/bin/bash
# CLO835 - Week 12 - ConfigMaps and Secrets.
# Run these ON THE MASTER NODE, section by section. Do NOT run the whole file.
#
# Terraform builds 3 machines: 1 control plane and 2 workers. The cluster forms
# itself at boot, the same way it did in Weeks 04 to 10. Every object of the lab
# lives in the namespace week12, except the dev and prod namespaces of Workshop 3.
#
# Each step matches one slide of Lab_week12_v1.pptx.
"""

CLEANUP = """kubectl delete namespace week12 dev prod 2>/dev/null
rm -f ./fortune-args.yaml ./ubuntu-sleeper.yaml ./fortune-env.yaml ./app_config.properties ./config-map.yaml ./config-env.yaml ./config-volume.yaml ./mode-pod.yaml ./secret-data.yaml ./secret-pod.yaml

kubectl get namespaces | grep -E "week12|dev|prod\""""

BLACKBOARD = [
 ("Command-line Arguments",
  "ENTRYPOINT and CMD of Docker are command and args in Kubernetes.",
  ["Show the logs of fortune-args with \"every 2 seconds\".",
   "Show ubuntu-sleeper-pod going from Running to Completed, and its command and args.",
   "Explain which field replaces ENTRYPOINT and which replaces CMD."]),
 ("Environment Variables",
  "A variable is set per container in the Pod manifest.",
  ["Show printenv INTERVAL in fortune-env, and the KUBERNETES_SERVICE variables.",
   "Explain the drawback of a hard-coded value."]),
 ("ConfigMaps",
  "A ConfigMap holds key/value pairs, created three ways and consumed three ways.",
  ["Show the three ConfigMaps: from a literal, from a file and from a manifest.",
   "Show APP_COLOR, APP_MODE and INTERVAL in config-env.",
   "Show the files of the ConfigMap volume, and APP_COLOR changing to green in the file only.",
   "Show APP_MODE development in dev and production in prod, from one Pod manifest.",
   "Explain why a volume follows a change and an environment variable does not."]),
 ("Secrets",
  "A Secret is base64, not encrypted. A volume is safer than an environment variable.",
  ["Show the Secret made imperatively, then declaratively, and the decoded password.",
   "Show the Secret volume files and the tmpfs mount.",
   "Show the child process and /proc/1/environ seeing the password.",
   "Show the service account files, and that no Secret object holds the token.",
   "Show the password in plain text in etcd, and explain encryption at rest.",
   "Show the clean-up and terraform destroy."]),
]

if __name__ == "__main__":
    L.check_lines(SLIDES)
    L.make_lab("12", SLIDES, "Week12/Lab_week12_v1.pptx", SCRIPT_HEAD, script_path="Week12/localMachine_v1.sh")
    if "--no-repo" not in sys.argv:
        dst, files = L.make_repo_folder("12", "ConfigMaps and Secrets", CLEANUP, "Week12/localMachine_v1.sh")
        print("repo folder : %s (%d files)" % (dst, len(files)))
    L.blackboard_text("12", "The Terraform configuration in Week 12 creates the same three Ubuntu 26.04 EC2 "
                      "machines as Weeks 04 to 10.", BLACKBOARD, "Week12/Lab_week12_Blackboard_Submission.md")
    print("blackboard  : Week12/Lab_week12_Blackboard_Submission.md")
