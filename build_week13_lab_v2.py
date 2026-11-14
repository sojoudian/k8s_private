# -*- coding: utf-8 -*-
"""CLO835 Week 13 lab v2 - Authentication and RBAC, in ONE workshop.

v1 had 4 workshops and 12 steps. The limit is now the size of the Week 03 and
Week 04 labs: at most Step 0 to Step 6. v2 keeps the line of the lecture
(week13/Week13_lecture_style_v7.pptx): a user is a certificate that the cluster
CA signed, authentication is not authorization, a Role and a RoleBinding for
the user, and a ServiceAccount that calls the API with its token.
Every object lives in the namespace week13.

Outputs: week13/Lab_week13_v2.pptx, week13/localMachine_v2.sh,
week13/Lab_week13_Blackboard_Submission_v2.md, ~/Documents/c/r/CLO835_Fall_2026/Week13/
Run from the project root. It is guarded, so importing it writes nothing.
"""
import sys

import build_week13_lab_v1 as v1
import lab_kubeadm as L

F = L.FILE_MARK
DEV = v1.DEV
# v1.CALL, with "; echo" so the prompt starts on a new line after the JSON.
CALL = v1.CALL[:2] + [v1.CALL[2].replace("| head -12'", "| head -12; echo'")]
assert CALL[2] != v1.CALL[2]

SLIDES = [
 ("title", "Workshop 1 – Authentication and RBAC"),
 ("prereq",),
 ("cluster",),
 ("step2", "A new user is a signed certificate", "bash", [
  "# You are kubernetes-admin: a certificate with O = kubeadm:cluster-admins.",
  "$ kubectl auth whoami",
  " ",
  "# The cluster CA signs a certificate for dev-user,",
  "# group developers. Kubernetes stores no users.",
  "$ openssl genrsa -out dev-user.key 2048",
  "$ openssl req -new -key dev-user.key -out dev-user.csr -subj \"/CN=dev-user/O=developers\"",
  "# No quotes on EOF: the shell puts the request in.",
  "$ cat > dev-user-csr.yaml <<EOF",
  F,
  "EOF",
  "$ kubectl apply -f dev-user-csr.yaml",
  "$ kubectl certificate approve dev-user",
  "$ kubectl get csr dev-user                    # Approved,Issued",
  "$ kubectl get csr dev-user -o jsonpath='{.status.certificate}' | base64 -d > dev-user.crt",
  "$ openssl x509 -in dev-user.crt -noout -subject -enddate",
  ], "dev-user-csr.yaml", "dev-user-csr.yaml", v1.CSR),
 ("step", "Authenticated, not authorized", "bash", [
  "$ kubectl create namespace week13",
  "$ kubectl config set-credentials dev-user --client-certificate=dev-user.crt --client-key=dev-user.key --embed-certs=true",
  "$ kubectl config set-context dev-user@kubernetes --cluster=kubernetes --user=dev-user --namespace=week13",
  "$ kubectl config get-contexts",
  " ",
  "# The API knows who dev-user is:",
  "$ " + DEV + " auth whoami",
  " ",
  "# ... but RBAC allows nothing yet:",
  "$ " + DEV + " get pods",
  "# Error from server (Forbidden): pods is forbidden: User \"dev-user\" cannot list resource \"pods\" ...",
  ]),
 ("step2", "A Role and a RoleBinding for dev-user", "bash", [
  "# The Role says what. The RoleBinding says who.",
  "# RBAC needs the plural name: configmaps.",
  "$ cat > developer-role.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f developer-role.yaml -n week13",
  " ",
  "$ " + DEV + " run web --image=maziar/kubia:v1    # yes",
  "$ " + DEV + " get pods                           # yes",
  "$ " + DEV + " delete pod web                     # Forbidden",
  " ",
  "# An admin can ask on behalf of any user:",
  "$ kubectl auth can-i delete pods -n week13 --as=dev-user",
  "$ kubectl auth can-i --list -n week13 --as=dev-user",
  ], "developer-role.yaml", "developer-role.yaml", v1.DEVELOPER),
 ("step2", "A Pod calls the API with its token", "bash", [
  "# A Pod runs as a ServiceAccount. Its token is",
  "# mounted in the Pod.",
  "$ kubectl create serviceaccount clo835 -n week13",
  "$ cat > curl-sa.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f curl-sa.yaml -n week13",
  "$ kubectl wait --for=condition=Ready pod/curl-sa -n week13 --timeout=120s",
  " ",
  "# Ask the API server for the Services of week13.",
  ] + CALL + [
  "# \"reason\": \"Forbidden\": the token proves",
  "# who the Pod is. RBAC allows nothing yet.",
  ], "curl-sa.yaml", "curl-sa.yaml", v1.CURL_SA),
 ("step2", "A Role for the ServiceAccount", "bash", [
  "# get and list Services, for the ServiceAccount clo835.",
  "$ cat > service-reader.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f service-reader.yaml -n week13",
  " ",
  "# The same call now returns a ServiceList.",
  ] + CALL + [
  " ",
  "# A Role and its RoleBinding work in one namespace only.",
  "$ kubectl auth can-i list services -n week13 --as=system:serviceaccount:week13:clo835",
  "$ kubectl auth can-i list services -n default --as=system:serviceaccount:week13:clo835",
  ], "service-reader.yaml", "service-reader.yaml", v1.SERVICE_READER),
 ("step", "Clean up", "bash", [
  "# ON THE MASTER - remove the Kubernetes objects and the user.",
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
 ("end", "Workshop 1 – The End"),
]

SCRIPT_HEAD = """#!/bin/bash
# CLO835 - Week 13 - Authentication and RBAC.
# Run these ON THE MASTER NODE, section by section. Do NOT run the whole file.
#
# Terraform builds 3 machines: 1 control plane and 2 workers. The cluster forms
# itself at boot, the same way it did in Weeks 04 to 12. Every object of the lab
# lives in the namespace week13.
#
# Each step matches one slide of Lab_week13_v2.pptx.
"""

CLEANUP = """kubectl delete namespace week13 2>/dev/null
kubectl delete csr dev-user 2>/dev/null
kubectl config delete-context dev-user@kubernetes 2>/dev/null
kubectl config delete-user dev-user 2>/dev/null
rm -f ./dev-user.key ./dev-user.csr ./dev-user.crt ./dev-user-csr.yaml ./developer-role.yaml ./curl-sa.yaml ./service-reader.yaml

kubectl config get-contexts"""

BLACKBOARD = [
 ("Users and authentication", "A Kubernetes user is a certificate that the cluster CA signed.",
  ["Show kubectl auth whoami as kubernetes-admin.",
   "Show the approved CSR and the subject of dev-user.crt.",
   "Show kubectl auth whoami and the Forbidden error for dev-user, and explain the difference between authentication and authorization."]),
 ("Roles and ServiceAccounts", "A RoleBinding gives the rules of a Role to a user or a ServiceAccount, in one namespace.",
  ["Show what dev-user can and cannot do after the developer Role, and kubectl auth can-i --list.",
   "Show the Forbidden answer of the API to the Pod, then the ServiceList after the service-reader Role.",
   "Show the two can-i answers for week13 and default, and explain them.",
   "Show the clean-up and terraform destroy."]),
]

if __name__ == "__main__":
    # SHOULD-FIX 14 of review round 2 (2026-11-11): this old builder overwrote delivered files and wrote the repo folder with a cleanup script.
    # Use build_week13_lab_v5.py. Importing this file still works.
    sys.exit("build_week13_lab_v2.py is an old version. Use build_week13_lab_v5.py.")
    L.check_lines(SLIDES)
    L.make_lab("13", SLIDES, "week13/Lab_week13_v2.pptx", SCRIPT_HEAD, script_path="week13/localMachine_v2.sh")
    if "--no-repo" not in sys.argv:
        dst, files = L.make_repo_folder("13", "Authentication and RBAC", CLEANUP, "week13/localMachine_v2.sh")
        print("repo folder : %s (%d files)" % (dst, len(files)))
    L.blackboard_text("13", "The Terraform configuration in Week 13 creates the same three Ubuntu 26.04 EC2 "
                      "machines as Weeks 04 to 12.", BLACKBOARD, "week13/Lab_week13_Blackboard_Submission_v2.md")
    print("blackboard  : week13/Lab_week13_Blackboard_Submission_v2.md")
