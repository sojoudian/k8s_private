#!/bin/bash
# CLO835 - Week 13 - Authentication and RBAC.
# Run these ON THE MASTER NODE, section by section. Do NOT run the whole file.
#
# Terraform builds 3 machines: 1 control plane and 2 workers. The cluster forms
# itself at boot, the same way it did in Weeks 04 to 12. A user of this lab is
# an X509 certificate that the cluster CA signs, the kubeadm form of the IAM
# user of the lecture. kubectl proxy of Workshop 1 keeps running until clean-up.
#
# Each step matches one slide of Lab_week13_v1.pptx.

########################################################
# Step 0 - check the cluster                    (slide 3)
########################################################
# All three nodes must reach Ready. The workers take a few minutes to join.
kubectl get nodes -o wide
kubectl get pods -n kube-system

########################################################
# Step 1 - The admin user is a client certificate (slide 4)
########################################################
# The X509 plugin reads the user name from CN and the groups from O of the certificate.
kubectl auth whoami
kubectl config view --raw -o jsonpath='{.users[0].user.client-certificate-data}' | base64 -d | openssl x509 -noout -subject
# subject=O = kubeadm:cluster-admins, CN = kubernetes-admin

# Kubernetes stores no users. It trusts any certificate that its own CA signed.
kubectl get users
# error: the server doesn't have a resource type "users"

########################################################
# Step 2 - The API groups                       (slide 5)
########################################################
kubectl get --raw /version
kubectl get --raw /healthz; echo
kubectl api-versions | head -12               # v1 (the core group) and the named groups

# With no credentials you are system:anonymous. Only a few paths, such as /version, are open.
curl -sk https://localhost:6443/version | head -4
curl -sk https://localhost:6443/api/v1/namespaces | head -8     # 403 Forbidden

# kubectl proxy listens on 8001 and adds your credentials to each request.
kubectl proxy --port=8001 >/dev/null 2>&1 &
curl -s localhost:8001/apis | head -12

########################################################
# Step 3 - A new user: a key and a signing request (slide 6)
########################################################
# EKS maps an IAM user to a Kubernetes user. Here the
# cluster CA signs a certificate: CN dev-user, O developers.
openssl genrsa -out dev-user.key 2048
openssl req -new -key dev-user.key -out dev-user.csr -subj "/CN=dev-user/O=developers"

# No quotes on EOF: the shell puts the request into the file.
cat > dev-user-csr.yaml <<EOF
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: dev-user
spec:
  request: $(base64 -w0 < dev-user.csr)
  signerName: kubernetes.io/kube-apiserver-client
  expirationSeconds: 86400
  usages:
  - client auth
EOF
kubectl apply -f dev-user-csr.yaml
kubectl get csr dev-user                      # Pending
kubectl certificate approve dev-user
kubectl get csr dev-user                      # Approved,Issued
kubectl get csr dev-user -o jsonpath='{.status.certificate}' | base64 -d > dev-user.crt
openssl x509 -in dev-user.crt -noout -subject -enddate

########################################################
# Step 4 - A context for the new user: authenticated, not authorized (slide 7)
########################################################
kubectl create namespace week13
kubectl config set-credentials dev-user --client-certificate=dev-user.crt --client-key=dev-user.key --embed-certs=true
kubectl config set-context dev-user@kubernetes --cluster=kubernetes --user=dev-user --namespace=week13
kubectl config get-contexts

# The groups come from the certificate. system:authenticated is added for every user.
kubectl --context=dev-user@kubernetes auth whoami

# The API knows who dev-user is, but RBAC allows nothing yet:
kubectl --context=dev-user@kubernetes get pods
# Error from server (Forbidden): pods is forbidden: User "dev-user" cannot list resource "pods" ...

########################################################
# Step 5 - Every namespace has a default ServiceAccount (slide 10)
########################################################
kubectl get serviceaccounts -n week13          # default
kubectl create serviceaccount clo835 -n week13
kubectl get serviceaccounts -n week13

# The token of a ServiceAccount is a JWT. Make one and read its payload.
TOKEN=$(kubectl create token clo835 -n week13)
echo $TOKEN | cut -d. -f2 | python3 -c "import sys,base64; s=sys.stdin.read().strip(); print(base64.urlsafe_b64decode(s+'==').decode())"
# ... "sub":"system:serviceaccount:week13:clo835" ...

# The API server checks the signature of the token with the public key of the cluster.

########################################################
# Step 6 - A Pod calls the API with its token   (slide 11)
########################################################
# The Pod runs as the ServiceAccount clo835. Its token
# is mounted at /var/run/secrets/kubernetes.io/serviceaccount.
cat > curl-sa.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: curl-sa
spec:
  serviceAccountName: clo835
  containers:
  - name: main
    image: maziar/curl
    command: ["sleep", "3600"]
EOF
kubectl apply -f curl-sa.yaml -n week13
kubectl wait --for=condition=Ready pod/curl-sa -n week13 --timeout=60s

# Ask the API server for the Services of week13.
kubectl exec curl-sa -n week13 -- sh -c 'SA=/var/run/secrets/kubernetes.io/serviceaccount; \
    curl -s --cacert $SA/ca.crt -H "Authorization: Bearer $(cat $SA/token)" \
    https://kubernetes.default.svc/api/v1/namespaces/week13/services | head -12'
# services is forbidden: User
# system:serviceaccount:week13:clo835 cannot list ...
# Authenticated as the ServiceAccount, not authorized.

########################################################
# Step 7 - A Role and a RoleBinding for the ServiceAccount (slide 14)
########################################################
# The Role says what: get and list Services. The
# RoleBinding says who: the ServiceAccount clo835.
cat > service-reader.yaml <<'EOF'
apiVersion: rbac.authorization.k8s.io/v1
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
  apiGroup: rbac.authorization.k8s.io
EOF
kubectl apply -f service-reader.yaml -n week13

# The same call now returns a ServiceList.
kubectl exec curl-sa -n week13 -- sh -c 'SA=/var/run/secrets/kubernetes.io/serviceaccount; \
    curl -s --cacert $SA/ca.crt -H "Authorization: Bearer $(cat $SA/token)" \
    https://kubernetes.default.svc/api/v1/namespaces/week13/services | head -12'

########################################################
# Step 8 - The developer Role of the lecture, for dev-user (slide 15)
########################################################
# RBAC needs the lower-case plural name of a resource:
# configmaps, not ConfigMap.
cat > developer-role.yaml <<'EOF'
apiVersion: rbac.authorization.k8s.io/v1
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
  apiGroup: rbac.authorization.k8s.io
EOF
kubectl apply -f developer-role.yaml -n week13

kubectl --context=dev-user@kubernetes run web --image=maziar/kubia:v1     # create pods: yes
kubectl --context=dev-user@kubernetes get pods                            # list pods: yes
kubectl --context=dev-user@kubernetes delete pod web                      # Forbidden
kubectl --context=dev-user@kubernetes create configmap demo --from-literal=a=b   # yes
kubectl --context=dev-user@kubernetes get configmaps                      # Forbidden

########################################################
# Step 9 - Check permissions with kubectl auth can-i (slide 16)
########################################################
# An admin can ask on behalf of any user, without its credentials.
kubectl auth can-i list services -n week13 --as=system:serviceaccount:week13:clo835     # yes
kubectl auth can-i list services -n default --as=system:serviceaccount:week13:clo835    # no
# A Role and its RoleBinding work in one namespace only.

kubectl auth can-i delete pods -n week13 --as=dev-user                                  # no
kubectl auth can-i --list -n week13 --as=dev-user

########################################################
# Step 10 - A RoleBinding cannot grant cluster resources (slide 19)
########################################################
# A PersistentVolume belongs to no namespace.
kubectl create clusterrole pv-reader --verb=get,list --resource=persistentvolumes
kubectl create rolebinding pv-test --clusterrole=pv-reader --user=dev-user -n week13
kubectl --context=dev-user@kubernetes get persistentvolumes
# Forbidden: ... cannot list resource "persistentvolumes" ... at the cluster scope

# To grant a cluster-level resource, use a ClusterRoleBinding.
kubectl delete rolebinding pv-test -n week13
kubectl create clusterrolebinding pv-test --clusterrole=pv-reader --user=dev-user
kubectl --context=dev-user@kubernetes get persistentvolumes             # No resources found: allowed

########################################################
# Step 11 - The default roles and bindings      (slide 20)
########################################################
kubectl get clusterroles | grep -E '^(cluster-admin|admin|edit|view) '
kubectl get clusterrolebinding cluster-admin -o wide           # GROUPS system:masters
kubectl get clusterrolebinding kubeadm:cluster-admins -o wide  # the group of our admin

# system:discovery lets every authenticated user read the paths of the API.
kubectl get clusterrole system:discovery -o yaml | grep -A8 nonResourceURLs

# On EKS the creator of the cluster is in system:masters, and no ConfigMap shows it.
# kubeadm keeps the same break-glass identity in super-admin.conf. RBAC cannot lock it out.
sudo ls /etc/kubernetes/*.conf

########################################################
# Step 12 - Clean up                            (slide 21)
########################################################
# ON THE MASTER - stop the proxy and remove the Kubernetes objects and the user.
bash cleanup_lab13.sh

# Confirm that nothing is left.
kubectl config get-contexts

# ON YOUR OWN MACHINE - remove the three EC2 machines.
# ON YOUR OWN MACHINE:  terraform destroy

# Always destroy. The Learner Lab budget is small.
