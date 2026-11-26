# -*- coding: utf-8 -*-
"""The values of Week 13 (Authentication and RBAC) for tools/check_week.py.

The values come from gate_week13_v3.py (lab v6 and Blackboard text v6, review rounds 1 to 5 of 2026-11-11 and
2026-11-18). The lists SLIDE_TITLES, SECTIONS, OBJECTS, DENIALS and F4 are copies of that gate, byte for byte.
This file holds data only. check_week.py reads each name in capital letters.
"""
TOPIC = "Authentication and RBAC"
EXTRA_REPO_FILES = []                           # C5: the 7 files only, no extra file
REPO_BASE = (12, "ConfigMaps and Secrets")     # C5: the repo text equals the Week 12 repo text
HELPER_IMAGE = "maziar/alpine-curl"             # C3, M26
NO_FILE_PANEL = [5]                             # the lab slide of Step 2 has no file panel
# F3: the only GitHub name in the Week 13 repo is the course repo (gate_week13_v3.py).
SCAN_ACCOUNT = r"[Ss]ojoudian(?!/CLO835_Fall_2026\.git)"
PROXY = "kubectl proxy --port=8001 & sleep 2; curl -s http://localhost:8001/apis | head -8; kill %1"
DEV = "kubectl --context=dev-user@kubernetes"
SA = "--as=system:serviceaccount:week13:clo835"
SLIDE_TITLES = ["Workshop 1 – Authentication and RBAC", "Lab Week 13 - Prerequisites", "Build and check the cluster",
                "A new user is a signed certificate", "Authenticated, not authorized",
                "A Role and a RoleBinding for dev-user", "A Pod calls the API with its token",
                "A Role and a ClusterRole for the ServiceAccount", "Destroy the cluster", "Workshop 1 – The End"]
SECTIONS = ["Build and Check the Cluster", "Create a User with a Signed Certificate",
            "Show That dev-user Is Authenticated, Not Authorized", "Create a Role and a RoleBinding for dev-user, and a RoleBinding for the Group developers",
            "Call the API from a Pod with Its Token", "Give the ServiceAccount a Role and a ClusterRole", "Destroy the Cluster"]
OBJECTS = {"namespace week13": "kubectl create namespace week13",
           "user dev-user": "kubectl config set-credentials dev-user",
           "group developers": "/CN=dev-user/O=developers",
           "Role developer": "  name: developer\n",
           "RoleBinding devuser-developer-binding": "  name: devuser-developer-binding\n",
           "RoleBinding developers-view": "kubectl create rolebinding developers-view --clusterrole=view --group=developers",
           "ServiceAccount clo835": "kubectl create serviceaccount clo835 -n week13",
           "Pod curl-sa": "  name: curl-sa\n",
           "Role service-reader": "  name: service-reader\n",
           "RoleBinding service-reader-binding": "  name: service-reader-binding\n",
           "ClusterRole pv-reader": "kubectl create clusterrole pv-reader",
           "RoleBinding pv-test": "kubectl create rolebinding pv-test",
           "ClusterRoleBinding pv-test": "kubectl create clusterrolebinding pv-test"}
DENIALS = [DEV + " get pods",
           DEV + " delete pod web                     # Forbidden",
           "kubectl auth can-i list services -n default " + SA + "   # no",
           "kubectl auth can-i list persistentvolumes -A " + SA + "   # no"]
F4 = [
 (1, "Update the repo with git fetch and git reset --hard origin/master.", "step",
  ["git fetch && git reset --hard origin/master"]),
 (1, "Run terraform init and terraform apply.", "step", ["terraform init", "terraform apply"]),
 (1, "Run terraform output public_ips and terraform output private_ips, and show the addresses of all three nodes.",
  "step", ["terraform output public_ips", "terraform output private_ips"]),
 (1, "Show an SSH session connected to the master node.", "step", ["ssh -i <your-key>.pem ubuntu@<masternode-public-ip>"]),
 (1, "Run kubectl get nodes -o wide and show all three nodes in the Ready state.", "step", ["kubectl get nodes -o wide"]),
 (1, "Run kubectl get pods -n kube-system and show the control-plane Pods in the Running state.", "step",
  ["kubectl get pods -n kube-system"]),
  (2, "Create dev-user.key and dev-user.csr with the openssl genrsa and openssl req commands.", "step",
  ["openssl genrsa -out dev-user.key 2048", "openssl req -new -key dev-user.key -out dev-user.csr"]),
 (2, "Create dev-user-csr.yaml with the cat > command.", "step", ["cat > dev-user-csr.yaml <<EOF"]),
 (2, "Apply the manifest.", "step", ["kubectl apply -f dev-user-csr.yaml"]),
 (2, "Approve the dev-user CertificateSigningRequest (CSR) with kubectl certificate approve dev-user.", "step",
  ["kubectl certificate approve dev-user"]),
 (2, "Run kubectl get csr dev-user and show Approved,Issued.", "step", ["kubectl get csr dev-user   "]),
 (2, "Write the certificate to dev-user.crt with the kubectl get csr command and base64 -d.", "step",
  ["kubectl get csr dev-user -o jsonpath='{.status.certificate}' | base64 -d > dev-user.crt"]),
 (2, "Run the openssl x509 command, and show the subject and the end date.", "step",
  ["openssl x509 -in dev-user.crt -noout -subject -enddate"]),
 (2, "Explain why Kubernetes does not store normal users.", "comment", ["Kubernetes stores no normal users."]),   # and lecture v10 slide 6
 (2, "Explain what the CN and O fields of the certificate mean.", "comment", ["CN is the user name. O is the group"]),
 (3, "Create the week13 namespace.", "step", ["kubectl create namespace week13"]),
 (3, "Add the dev-user credentials and the dev-user@kubernetes context with kubectl config set-credentials and "
     "kubectl config set-context.", "step",
  ["kubectl config set-credentials dev-user", "kubectl config set-context dev-user@kubernetes"]),
 (3, "Run the two curl commands on port 6443, and show the version and the 403 Forbidden answer.", "step",
  ["curl -k https://localhost:6443/version", "curl -k https://localhost:6443/apis"]),
 (3, "Run the kubectl proxy command, and show the first lines of the APIGroupList.", "step", [PROXY]),
 (3, "Run kubectl --context=dev-user@kubernetes auth whoami, and show the user and the groups.", "step",
  [DEV + " auth whoami"]),
 (3, "Run kubectl --context=dev-user@kubernetes get pods, and show the Forbidden error.", "step", [DEV + " get pods"]),
 (3, "Explain the order of the phases of a request in the API server.", "lecture",
  ["authentication, authorization and admission control (lecture v10 slide 5; round1 list 3, item 2)"]),
 (3, "Explain the difference between authentication and authorization.", "comment",
  ["Authentication: the API server knows who dev-user is.", "Authorization: no Role allows dev-user to list Pods yet."]),
 (3, "Explain why the curl command for /apis gets 403 Forbidden, and the kubectl proxy request passes.", "comment",
  ["With no credentials you are system:anonymous.", "kubectl proxy sends your credentials to the API server"]),
 (3, "Explain why the auth whoami command passes and the get pods command fails.", "comment",
  ["Every authenticated user can run auth whoami.", "no Role allows dev-user to list Pods yet."]),
 (4, "Create developer-role.yaml and display its contents.", "step", ["cat > developer-role.yaml <<'EOF'"]),
 (4, "Apply the manifest with kubectl apply -f developer-role.yaml -n week13.", "step",
  ["kubectl apply -f developer-role.yaml -n week13"]),
 (4, "Run the kubectl run web command as dev-user, and show the answer pod/web created.", "step",
  [DEV + " run web --image=maziar/kubia:v1"]),
 (4, "Run the kubectl delete pod web command as dev-user, and show the Forbidden error.", "step",
  [DEV + " delete pod web"]),
 (4, "Create the developers-view RoleBinding with the kubectl create rolebinding command.", "step",
  ["kubectl create rolebinding developers-view"]),
 (4, "Run the kubectl get services command as dev-user, and show the answer No resources found.", "step",
  [DEV + " get services"]),
 (4, "Explain the difference between a Role and a RoleBinding.", "comment", ["The Role says what. The RoleBinding says who."]),
 (4, "Explain why the Role names configmaps and not ConfigMap.", "comment",
  ["RBAC matches the name in the API path: configmaps, not ConfigMap."]),
 (4, "Explain how dev-user gets the permissions of the default ClusterRole view.", "comment",
  ["The group of the certificate gets the default ClusterRole view"]),
 (5, "Create the clo835 ServiceAccount.", "step", ["kubectl create serviceaccount clo835 -n week13"]),
 (5, "Create curl-sa.yaml and display its contents.", "step", ["cat > curl-sa.yaml <<'EOF'"]),
 (5, "Apply the manifest.", "step", ["kubectl apply -f curl-sa.yaml -n week13"]),
 (5, "Run kubectl wait, and show that the curl-sa Pod is Ready.", "step",
  ["kubectl wait --for=condition=Ready pod/curl-sa -n week13"]),
 (5, "Run the curl command in the Pod with kubectl exec, and show the Forbidden answer.", "step",
  ["kubectl exec curl-sa -n week13 -- sh -c"]),
 (5, "Explain how the Pod proves its identity to the API server.", "comment",
  ["A Pod runs as a ServiceAccount. Kubernetes mounts", "the token proves"]),
 (5, "Explain why the API server answers Forbidden.", "comment", ["No Role allows it to list Services yet."]),
 (6, "Create service-reader.yaml and display its contents.", "step", ["cat > service-reader.yaml <<'EOF'"]),
 (6, "Apply the manifest with kubectl apply -f service-reader.yaml -n week13.", "step",
  ["kubectl apply -f service-reader.yaml -n week13"]),
 (6, "Run the same curl command, and show the ServiceList.", "step", ["kubectl exec curl-sa -n week13 -- sh -c"]),
 (6, "Run kubectl auth can-i list services for the default namespace, and show no.", "step",
  ["kubectl auth can-i list services -n default"]),
 (6, "Run the kubectl api-resources command, and show that NAMESPACED is false for persistentvolumes.", "step",
  ["kubectl api-resources --sort-by name | grep -E 'NAMESPACED|persistentvolumes'"]),
 (6, "Create the pv-reader ClusterRole.", "step", ["kubectl create clusterrole pv-reader"]),
 (6, "Create the pv-test RoleBinding.", "step", ["kubectl create rolebinding pv-test"]),
 (6, "Run kubectl auth can-i list persistentvolumes, and show no.", "step",
  ["kubectl auth can-i list persistentvolumes -A " + SA + "   # no"]),
 (6, "Create the pv-test ClusterRoleBinding.", "step", ["kubectl create clusterrolebinding pv-test"]),
 (6, "Run the same kubectl auth can-i command, and show yes.", "step",
  ["kubectl auth can-i list persistentvolumes -A " + SA + "   # yes"]),
 (6, "Explain why the ServiceAccount gets the answer no in the default namespace.", "comment",
  ["A Role and its RoleBinding work in one namespace only."]),
 (6, "Explain why a PersistentVolume needs a ClusterRoleBinding and not a RoleBinding.", "comment",
  ["A PersistentVolume has no namespace", "A RoleBinding cannot give access to an object with no namespace."]),
 (7, "Run terraform destroy in the Week13 directory on your own machine.", "step", ["terraform destroy"]),
 (7, "Include the final Terraform output, which shows the message Destroy complete!", "step", ["terraform destroy"]),
 (7, "State the number of resources Terraform destroyed.", "step", ["terraform destroy"]),
]
HEREDOC_HEADS = ("each manifest is written with cat > file <<'EOF'; only the CSR file has no quotes (C3, M24)",
                 ["cat > dev-user-csr.yaml <<EOF", "cat > developer-role.yaml <<'EOF'", "cat > curl-sa.yaml <<'EOF'",
                  "cat > service-reader.yaml <<'EOF'"])
UNQUOTED_EOF = {"dev-user-csr.yaml": "# EOF has no quotes, so the shell writes the base64 request into the file."}
STEP_COMMANDS = [("the kubectl proxy line is the tested line", 2, PROXY)]
# Review round 4: an item starts with its verb. Review round 5, SHOULD-FIX 4: "allow", not "let", for a permission.
A1_EXTRA = [r"(?m)^- As dev-user", r"\blets?\b"]
DECK_A1_EXTRA = [r"\bRunning\b", r"\blets?\b"]  # gate_week13_v3.py looks for both in all the text of the lab deck
MAZIAR_ONLY = True                              # exact form of gate_week13_v3.py: images of Docker Hub maziar only
BLACKBOARD_PHRASES = [("the user and the groups (S25)", "show the user and the groups.")]
BLACKBOARD_SECTION_PHRASES = [
    ("the lab does not show admission control, in section 3 (round 2, MUST-FIX 11, SHOULD-FIX 5)", 3,
     "The lab does not show admission control.", "admission"),
]
# Live test (E3, C4, C9)
CAN_I = ["no", "no", "yes"]
LIVE_SAMPLES = ["Approved,Issued", "subject=O=developers, CN=dev-user", '"reason": "Forbidden"',
                '"kind": "APIGroupList"', "Starting to serve on 127.0.0.1:8001", "[developers system:authenticated]",
                'User "dev-user" cannot list resource "pods"', "pod/web created",
                "No resources found in week13 namespace.", '"kind": "ServiceList"', '"items": []',
                "pod/curl-sa condition met"]
LIVE_REGEX = [("shows NAMESPACED false for persistentvolumes", r"persistentvolumes\s+pv\s+v1\s+false\s+PersistentVolume")]
# gate_week13_v3.py ran deck_checks of gate_week12.py, so these 3 phrases of Week 12 were allowed repeats for the
# Week 13 decks too (tools/rungate.py did the same for the lecture).
ALLOWED_REPEATS = {"configuring containerized applications", "configmap volume", "projected volume"}
