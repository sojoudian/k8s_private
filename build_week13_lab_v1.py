# -*- coding: utf-8 -*-
"""CLO835 Week 13 - Authentication and RBAC, on the kubeadm cluster.

The lecture (week13/Week13_lecture_style_v7.pptx) teaches authentication
plugins (X509 client certificates, tokens), users that Kubernetes does not
store, groups, ServiceAccounts and their tokens, the API groups, RBAC with
Roles, RoleBindings, ClusterRoles and ClusterRoleBindings, the default roles,
and the EKS mapping of IAM identities. The old lab created IAM users on EKS,
which the Learner Lab does not allow. Here a user is an X509 certificate that
the cluster CA signs: the kubeadm form of an external identity.

Outputs: week13/Lab_week13_v1.pptx, week13/localMachine_v1.sh,
week13/Lab_week13_Blackboard_Submission.md, ~/Documents/c/r/CLO835_Fall_2026/Week13/
Run from the project root. It is guarded, so importing it writes nothing.
"""
import sys

import lab_kubeadm as L

F = L.FILE_MARK
DEV = "kubectl --context=dev-user@kubernetes"

CSR = """apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: dev-user
spec:
  request: $(base64 -w0 < dev-user.csr)
  signerName: kubernetes.io/kube-apiserver-client
  expirationSeconds: 86400
  usages:
  - client auth""".split("\n")

CURL_SA = """apiVersion: v1
kind: Pod
metadata:
  name: curl-sa
spec:
  serviceAccountName: clo835
  containers:
  - name: main
    image: maziar/curl
    command: ["sleep", "3600"]""".split("\n")

SERVICE_READER = """apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: service-reader
rules:
- apiGroups: [""]
  resources: ["services"]
  verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: service-reader-binding
subjects:
- kind: ServiceAccount
  name: clo835
  namespace: week13
roleRef:
  kind: Role
  name: service-reader
  apiGroup: rbac.authorization.k8s.io""".split("\n")

DEVELOPER = """apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: developer
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["list", "get", "create", "update"]
- apiGroups: [""]
  resources: ["configmaps"]
  verbs: ["create"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: devuser-developer-binding
subjects:
- kind: User
  name: dev-user
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: developer
  apiGroup: rbac.authorization.k8s.io""".split("\n")

CALL = [
  "$ kubectl exec curl-sa -n week13 -- sh -c 'SA=/var/run/secrets/kubernetes.io/serviceaccount; \\",
  "    curl -s --cacert $SA/ca.crt -H \"Authorization: Bearer $(cat $SA/token)\" \\",
  "    https://kubernetes.default.svc/api/v1/namespaces/week13/services | head -12'",
]

SLIDES = [
 ("title", "Workshop 1 – Authentication: Who Are You?"),
 ("prereq",),
 ("cluster",),
 ("step", "The admin user is a client certificate", "bash", [
  "# The X509 plugin reads the user name from CN and the groups from O of the certificate.",
  "$ kubectl auth whoami",
  "$ kubectl config view --raw -o jsonpath='{.users[0].user.client-certificate-data}' | base64 -d | openssl x509 -noout -subject",
  "# subject=O = kubeadm:cluster-admins, CN = kubernetes-admin",
  " ",
  "# Kubernetes stores no users. It trusts any certificate that its own CA signed.",
  "$ kubectl get users",
  "# error: the server doesn't have a resource type \"users\"",
  ]),
 ("step", "The API groups", "bash", [
  "$ kubectl get --raw /version",
  "$ kubectl get --raw /healthz; echo",
  "$ kubectl api-versions | head -12               # v1 (the core group) and the named groups",
  " ",
  "# With no credentials you are system:anonymous. Only a few paths, such as /version, are open.",
  "$ curl -sk https://localhost:6443/version | head -4",
  "$ curl -sk https://localhost:6443/api/v1/namespaces | head -8     # 403 Forbidden",
  " ",
  "# kubectl proxy listens on 8001 and adds your credentials to each request.",
  "$ kubectl proxy --port=8001 >/dev/null 2>&1 &",
  "$ curl -s localhost:8001/apis | head -12",
  ]),
 ("step2", "A new user: a key and a signing request", "bash", [
  "# EKS maps an IAM user to a Kubernetes user. Here the",
  "# cluster CA signs a certificate: CN dev-user, O developers.",
  "$ openssl genrsa -out dev-user.key 2048",
  "$ openssl req -new -key dev-user.key -out dev-user.csr -subj \"/CN=dev-user/O=developers\"",
  " ",
  "# No quotes on EOF: the shell puts the request into the file.",
  "$ cat > dev-user-csr.yaml <<EOF",
  F,
  "EOF",
  "$ kubectl apply -f dev-user-csr.yaml",
  "$ kubectl get csr dev-user                      # Pending",
  "$ kubectl certificate approve dev-user",
  "$ kubectl get csr dev-user                      # Approved,Issued",
  "$ kubectl get csr dev-user -o jsonpath='{.status.certificate}' | base64 -d > dev-user.crt",
  "$ openssl x509 -in dev-user.crt -noout -subject -enddate",
  ], "dev-user-csr.yaml", "dev-user-csr.yaml", CSR),
 ("step", "A context for the new user: authenticated, not authorized", "bash", [
  "$ kubectl create namespace week13",
  "$ kubectl config set-credentials dev-user --client-certificate=dev-user.crt --client-key=dev-user.key --embed-certs=true",
  "$ kubectl config set-context dev-user@kubernetes --cluster=kubernetes --user=dev-user --namespace=week13",
  "$ kubectl config get-contexts",
  " ",
  "# The groups come from the certificate. system:authenticated is added for every user.",
  "$ " + DEV + " auth whoami",
  " ",
  "# The API knows who dev-user is, but RBAC allows nothing yet:",
  "$ " + DEV + " get pods",
  "# Error from server (Forbidden): pods is forbidden: User \"dev-user\" cannot list resource \"pods\" ...",
  ]),
 ("end", "Workshop 1 – The End"),

 ("title", "Workshop 2 – ServiceAccounts"),
 ("step", "Every namespace has a default ServiceAccount", "bash", [
  "$ kubectl get serviceaccounts -n week13          # default",
  "$ kubectl create serviceaccount clo835 -n week13",
  "$ kubectl get serviceaccounts -n week13",
  " ",
  "# The token of a ServiceAccount is a JWT. Make one and read its payload.",
  "$ TOKEN=$(kubectl create token clo835 -n week13)",
  "$ echo $TOKEN | cut -d. -f2 | python3 -c \"import sys,base64; s=sys.stdin.read().strip(); print(base64.urlsafe_b64decode(s+'==').decode())\"",
  "# ... \"sub\":\"system:serviceaccount:week13:clo835\" ...",
  " ",
  "# The API server checks the signature of the token with the public key of the cluster.",
  ]),
 ("step2", "A Pod calls the API with its token", "bash", [
  "# The Pod runs as the ServiceAccount clo835. Its token",
  "# is mounted at /var/run/secrets/kubernetes.io/serviceaccount.",
  "$ cat > curl-sa.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f curl-sa.yaml -n week13",
  "$ kubectl wait --for=condition=Ready pod/curl-sa -n week13 --timeout=60s",
  " ",
  "# Ask the API server for the Services of week13.",
  ] + CALL + [
  "# services is forbidden: User",
  "# system:serviceaccount:week13:clo835 cannot list ...",
  "# Authenticated as the ServiceAccount, not authorized.",
  ], "curl-sa.yaml", "curl-sa.yaml", CURL_SA),
 ("end", "Workshop 2 – The End"),

 ("title", "Workshop 3 – Roles and RoleBindings"),
 ("step2", "A Role and a RoleBinding for the ServiceAccount", "bash", [
  "# The Role says what: get and list Services. The",
  "# RoleBinding says who: the ServiceAccount clo835.",
  "$ cat > service-reader.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f service-reader.yaml -n week13",
  " ",
  "# The same call now returns a ServiceList.",
  ] + CALL + [
  ], "service-reader.yaml", "service-reader.yaml", SERVICE_READER),
 ("step2", "The developer Role of the lecture, for dev-user", "bash", [
  "# RBAC needs the lower-case plural name of a resource:",
  "# configmaps, not ConfigMap.",
  "$ cat > developer-role.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f developer-role.yaml -n week13",
  " ",
  "$ " + DEV + " run web --image=maziar/kubia:v1     # create pods: yes",
  "$ " + DEV + " get pods                            # list pods: yes",
  "$ " + DEV + " delete pod web                      # Forbidden",
  "$ " + DEV + " create configmap demo --from-literal=a=b   # yes",
  "$ " + DEV + " get configmaps                      # Forbidden",
  ], "developer-role.yaml", "developer-role.yaml", DEVELOPER),
 ("step", "Check permissions with kubectl auth can-i", "bash", [
  "# An admin can ask on behalf of any user, without its credentials.",
  "$ kubectl auth can-i list services -n week13 --as=system:serviceaccount:week13:clo835     # yes",
  "$ kubectl auth can-i list services -n default --as=system:serviceaccount:week13:clo835    # no",
  "# A Role and its RoleBinding work in one namespace only.",
  " ",
  "$ kubectl auth can-i delete pods -n week13 --as=dev-user                                  # no",
  "$ kubectl auth can-i --list -n week13 --as=dev-user",
  ]),
 ("end", "Workshop 3 – The End"),

 ("title", "Workshop 4 – ClusterRoles and ClusterRoleBindings"),
 ("step", "A RoleBinding cannot grant cluster resources", "bash", [
  "# A PersistentVolume belongs to no namespace.",
  "$ kubectl create clusterrole pv-reader --verb=get,list --resource=persistentvolumes",
  "$ kubectl create rolebinding pv-test --clusterrole=pv-reader --user=dev-user -n week13",
  "$ " + DEV + " get persistentvolumes",
  "# Forbidden: ... cannot list resource \"persistentvolumes\" ... at the cluster scope",
  " ",
  "# To grant a cluster-level resource, use a ClusterRoleBinding.",
  "$ kubectl delete rolebinding pv-test -n week13",
  "$ kubectl create clusterrolebinding pv-test --clusterrole=pv-reader --user=dev-user",
  "$ " + DEV + " get persistentvolumes             # No resources found: allowed",
  ]),
 ("step", "The default roles and bindings", "bash", [
  "$ kubectl get clusterroles | grep -E '^(cluster-admin|admin|edit|view) '",
  "$ kubectl get clusterrolebinding cluster-admin -o wide           # GROUPS system:masters",
  "$ kubectl get clusterrolebinding kubeadm:cluster-admins -o wide  # the group of our admin",
  " ",
  "# system:discovery lets every authenticated user read the paths of the API.",
  "$ kubectl get clusterrole system:discovery -o yaml | grep -A8 nonResourceURLs",
  " ",
  "# On EKS the creator of the cluster is in system:masters, and no ConfigMap shows it.",
  "# kubeadm keeps the same break-glass identity in super-admin.conf. RBAC cannot lock it out.",
  "$ sudo ls /etc/kubernetes/*.conf",
  ]),
 ("step", "Clean up", "bash", [
  "# ON THE MASTER - stop the proxy and remove the Kubernetes objects and the user.",
  "$ bash cleanup_lab13.sh",
  " ",
  "# Confirm that nothing is left.",
  "$ kubectl config get-contexts",
  " ",
  "# ON YOUR OWN MACHINE - remove the three EC2 machines.",
  "L$ terraform destroy",
  " ",
  "# Always destroy. The Learner Lab budget is small.",
  ]),
 ("end", "Workshop 4 – The End"),
]

SCRIPT_HEAD = """#!/bin/bash
# CLO835 - Week 13 - Authentication and RBAC.
# Run these ON THE MASTER NODE, section by section. Do NOT run the whole file.
#
# Terraform builds 3 machines: 1 control plane and 2 workers. The cluster forms
# itself at boot, the same way it did in Weeks 04 to 12. A user of this lab is
# an X509 certificate that the cluster CA signs, the kubeadm form of the IAM
# user of the lecture. kubectl proxy of Workshop 1 keeps running until clean-up.
#
# Each step matches one slide of Lab_week13_v1.pptx.
"""

CLEANUP = """pkill -f "kubectl proxy" 2>/dev/null
kubectl delete namespace week13 2>/dev/null
kubectl delete csr dev-user 2>/dev/null
kubectl delete clusterrolebinding pv-test 2>/dev/null
kubectl delete clusterrole pv-reader 2>/dev/null
kubectl config delete-context dev-user@kubernetes 2>/dev/null
kubectl config delete-user dev-user 2>/dev/null
rm -f ./dev-user.key ./dev-user.csr ./dev-user.crt ./dev-user-csr.yaml ./curl-sa.yaml ./service-reader.yaml ./developer-role.yaml

kubectl get csr,clusterrolebinding | grep -E "dev-user|pv-test\""""

BLACKBOARD = [
 ("Authentication",
  "A user is an X509 certificate that the cluster CA signs. Kubernetes stores no users.",
  ["Show kubectl auth whoami and the subject of the admin certificate.",
   "Show the error of kubectl get users, and explain it.",
   "Show /version answering without credentials and /api/v1/namespaces answering 403.",
   "Show the CertificateSigningRequest Pending, then Approved,Issued, and the subject of dev-user.crt.",
   "Show dev-user authenticated (auth whoami) but Forbidden to list pods.",
   "Explain how this maps to an IAM user on EKS."]),
 ("ServiceAccounts",
  "A Pod authenticates with the token of its ServiceAccount.",
  ["Show the default and clo835 ServiceAccounts, and the decoded payload of the token.",
   "Show the 403 answer when curl-sa lists the Services with its token."]),
 ("Roles and RoleBindings",
  "A Role says what. A RoleBinding says who.",
  ["Show the ServiceList after the service-reader Role and RoleBinding.",
   "Show what dev-user can and cannot do with the developer Role.",
   "Show kubectl auth can-i for both identities, and explain why a Role works in one namespace."]),
 ("ClusterRoles and ClusterRoleBindings",
  "A cluster-level resource needs a ClusterRoleBinding.",
  ["Show the Forbidden answer with the RoleBinding, and the allowed answer with the ClusterRoleBinding.",
   "Show the default cluster roles and the binding of system:masters.",
   "Explain the role of super-admin.conf, and compare it with the creator of an EKS cluster.",
   "Show the clean-up and terraform destroy."]),
]

if __name__ == "__main__":
    # S27 of review round 1 (2026-11-11): this old builder wrote delivered files and the repo folder with a
    # cleanup script. Use build_week13_lab_v5.py. Importing this file still works.
    sys.exit("build_week13_lab_v1.py is an old version. Use build_week13_lab_v5.py.")
    L.check_lines(SLIDES)
    L.make_lab("13", SLIDES, "week13/Lab_week13_v1.pptx", SCRIPT_HEAD, script_path="week13/localMachine_v1.sh")
    if "--no-repo" not in sys.argv:
        dst, files = L.make_repo_folder("13", "Authentication and RBAC", CLEANUP, "week13/localMachine_v1.sh")
        print("repo folder : %s (%d files)" % (dst, len(files)))
    L.blackboard_text("13", "The Terraform configuration in Week 13 creates the same three Ubuntu 26.04 EC2 "
                      "machines as Weeks 04 to 12.", BLACKBOARD, "week13/Lab_week13_Blackboard_Submission.md")
    print("blackboard  : week13/Lab_week13_Blackboard_Submission.md")
