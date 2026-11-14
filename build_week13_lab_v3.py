# -*- coding: utf-8 -*-
"""CLO835 Week 13 lab v3 - Authentication and RBAC, in ONE workshop.

v3 fixes the lab defects of report 2026-10-31-15: the label is "Lab Week 13", the sample
version is v1.35.10, the lab now practises a group, a default ClusterRole, a ClusterRole
and a ClusterRoleBinding, tee writes each manifest and shows it, the clean-up deletes the
objects that have no namespace, and the master applies a Flannel manifest with the images
of the maziar account. The Blackboard text of v3 is the hand-written file
week13/Lab_week13_Blackboard_Submission_v3.md, in the long form.

v1 had 4 workshops and 12 steps. The limit is the size of the Week 03 and Week 04 labs:
at most Step 0 to Step 6. The lab keeps the line of the lecture
(week13/Lecture_week13_v8.pptx): a user is a certificate that the cluster CA signed,
authentication is not authorization, a Role and a RoleBinding for the user, and a
ServiceAccount that calls the API with its token.

Outputs: week13/Lab_week13_v3.pptx, week13/localMachine_v3.sh,
~/Documents/c/r/CLO835_Fall_2026/Week13/
Run from the project root. It is guarded, so importing it writes nothing.
"""
import os
import sys

from pptx import Presentation
from pptx.util import Inches

import build_week13_lab_v1 as v1
import lab_kubeadm as L
from build_week12_lab_v5 import own_flannel
from build_week12_lecture_v6 import finish

OUT = "week13/Lab_week13_v3.pptx"
SCRIPT = "week13/localMachine_v3.sh"
F = L.FILE_MARK
DEV = v1.DEV
SA = "--as=system:serviceaccount:week13:clo835"
# v1.CALL, with "; echo" so the prompt starts on a new line after the JSON.
CALL = v1.CALL[:2] + [v1.CALL[2].replace("| head -12'", "| head -12; echo'")]
assert CALL[2] != v1.CALL[2]

SLIDES = [
 ("title", "Workshop 1 – Authentication and RBAC"),
 ("prereq",),
 ("cluster",),
 ("step2", "A new user is a signed certificate", "bash", [
  "# The cluster CA signs a certificate for dev-user. Kubernetes stores no users.",
  "# CN is the user name. O is the group: developers.",
  "$ openssl genrsa -out dev-user.key 2048",
  "$ openssl req -new -key dev-user.key -out dev-user.csr -subj \"/CN=dev-user/O=developers\"",
  "# No quotes on EOF: the shell puts the request in.",
  "# tee writes the file and shows it.",
  "$ tee dev-user-csr.yaml <<EOF",
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
  " ",
  "# With no credentials you are system:anonymous. Every client can read /version.",
  "$ curl -k https://localhost:6443/version",
  "$ curl -k https://localhost:6443/apis                # 403 Forbidden",
  " ",
  "# kubectl proxy sends your credentials to the API server, so this request passes.",
  "$ kubectl proxy --port=8001 & sleep 2; curl -s http://localhost:8001/apis | head -8; kill %1",
  " ",
  "# Authentication: the API knows who dev-user is. Every authenticated user can ask this.",
  "$ " + DEV + " auth whoami",
  " ",
  "# Authorization: no Role lets dev-user list Pods yet.",
  "$ " + DEV + " get pods",
  "# Error from server (Forbidden): pods is forbidden: User \"dev-user\" cannot list resource \"pods\" ...",
  ]),
 ("step2", "A Role and a RoleBinding for dev-user", "bash", [
  "# The Role says what. The RoleBinding says who.",
  "# RBAC matches the name in the API path: configmaps, not ConfigMap.",
  "$ tee developer-role.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f developer-role.yaml -n week13",
  " ",
  "$ " + DEV + " run web --image=maziar/kubia:v1    # pod/web created",
  "$ " + DEV + " delete pod web                     # Forbidden",
  " ",
  "# The group of the certificate gets the default ClusterRole view.",
  "$ kubectl create rolebinding developers-view --clusterrole=view --group=developers -n week13",
  "$ " + DEV + " get services      # No resources found: allowed",
  ], "developer-role.yaml", "developer-role.yaml", v1.DEVELOPER),
 ("step2", "A Pod calls the API with its token", "bash", [
  "# A Pod runs as a ServiceAccount. Kubernetes mounts",
  "# its token in the Pod.",
  "$ kubectl create serviceaccount clo835 -n week13",
  "$ tee curl-sa.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f curl-sa.yaml -n week13",
  "$ kubectl wait --for=condition=Ready pod/curl-sa -n week13 --timeout=120s",
  " ",
  "# Ask the API server for the Services of week13.",
  ] + CALL + [
  "# \"reason\": \"Forbidden\": the token proves",
  "# who the Pod is. No Role lets it list Services yet.",
  ], "curl-sa.yaml", "curl-sa.yaml", v1.CURL_SA),
 ("step2", "A Role and a ClusterRole for the ServiceAccount", "bash", [
  "# get and list Services, for the ServiceAccount clo835.",
  "$ tee service-reader.yaml <<'EOF'",
  F,
  "EOF",
  "$ kubectl apply -f service-reader.yaml -n week13",
  " ",
  "# The same call now returns a ServiceList. week13 has no Service, so items is empty.",
  ] + CALL + [
  " ",
  "# A Role and its RoleBinding work in one namespace only.",
  "$ kubectl auth can-i list services -n default " + SA + "   # no",
  " ",
  "# A PersistentVolume has no namespace: NAMESPACED is false.",
  "$ kubectl api-resources --sort-by name | grep -E 'NAMESPACED|persistentvolumes'",
  "$ kubectl create clusterrole pv-reader --verb=get,list --resource=persistentvolumes",
  "# A RoleBinding does not grant access to a cluster-level resource.",
  "$ kubectl create rolebinding pv-test --clusterrole=pv-reader --serviceaccount=week13:clo835 -n week13",
  "$ kubectl auth can-i list persistentvolumes -A " + SA + "   # no",
  "# A ClusterRoleBinding grants it.",
  "$ kubectl create clusterrolebinding pv-test --clusterrole=pv-reader --serviceaccount=week13:clo835",
  "$ kubectl auth can-i list persistentvolumes -A " + SA + "   # yes",
  ], "service-reader.yaml", "service-reader.yaml", v1.SERVICE_READER),
 ("step", "Clean up", "bash", [
  "# ON THE MASTER - delete the Kubernetes objects and the kubeconfig entry of dev-user.",
  "# A CSR, a ClusterRole and a ClusterRoleBinding have no namespace,",
  "# so the deletion of week13 does not delete them. The script deletes them one by one.",
  "# The output must show the context kubernetes-admin@kubernetes only.",
  "# This step takes about 40 seconds.",
  "$ bash cleanup_lab13.sh",
  " ",
  "# ON YOUR OWN MACHINE - destroy the three EC2 instances.",
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
# Terraform builds 3 EC2 instances: 1 master and 2 workers. The cluster forms
# itself at boot, the same way it did in Weeks 04 to 12. The objects that have a
# namespace are in the namespace week13.
#
# Each step matches one slide of Lab_week13_v3.pptx.
"""

CLEANUP = """kubectl delete namespace week13 2>/dev/null
kubectl delete csr dev-user 2>/dev/null
kubectl delete clusterrolebinding pv-test 2>/dev/null
kubectl delete clusterrole pv-reader 2>/dev/null
kubectl config delete-context dev-user@kubernetes 2>/dev/null
kubectl config delete-user dev-user 2>/dev/null
rm -f ./dev-user.key ./dev-user.csr ./dev-user.crt ./dev-user-csr.yaml
rm -f ./developer-role.yaml ./curl-sa.yaml ./service-reader.yaml

kubectl config get-contexts"""


def own_wording(dst):
    """One word for one meaning, and the active voice, in the shared lines of the repository files."""
    pairs = [("remove everything the lab creates inside the cluster", "delete everything that the lab creates inside the cluster"),
             ('# The three machines are removed by "terraform destroy" on your own laptop.',
              '# On your own machine, "terraform destroy" destroys the three EC2 instances.'),
             ("calls ./cleanup_lab13.sh. The student runs\n# terraform on their own laptop,",
              "runs bash cleanup_lab13.sh. The student runs\n# terraform on their own machine,"),
             ("You are on the CONTROL PLANE node. kubectl is ready.", "You are on the MASTER node. kubectl is ready.")]
    for name, count in (("cleanup_lab13.sh", 2), ("master-init.sh.tftpl", 4)):
        path = os.path.join(dst, name)
        text = open(path, encoding="utf8").read()
        hits = sum(1 for old, _ in pairs if old in text)
        assert hits == count, (name, hits)
        for old, new in pairs:
            text = text.replace(old, new)
        open(path, "w", encoding="utf8").write(text)


if __name__ == "__main__":
    # S27 of review round 1 (2026-11-11): this old builder wrote delivered files and the repo folder with a
    # cleanup script. Use build_week13_lab_v5.py. Importing this file still works.
    sys.exit("build_week13_lab_v3.py is an old version. Use build_week13_lab_v5.py.")
    L.check_lines(SLIDES)
    L.make_lab("13", SLIDES, OUT, SCRIPT_HEAD, script_path=SCRIPT, prereq_title="Lab Week 13 - Prerequisites",
               node_version="v1.35.10")
    prs = Presentation(OUT)
    # One name for the computer of the student, as on the Clean up slide.
    runs = [r for sh in prs.slides[2].shapes if sh.has_text_frame for p in sh.text_frame.paragraphs for r in p.runs
            if r.text.startswith("# ON YOUR MACHINE")]
    assert len(runs) == 1, len(runs)
    runs[0].text = runs[0].text.replace("ON YOUR MACHINE", "ON YOUR OWN MACHINE")
    runs = [r for sh in prs.slides[2].shapes if sh.has_text_frame for p in sh.text_frame.paragraphs for r in p.runs
            if r.text == "# ON THE MASTER - confirm the three nodes"]
    assert len(runs) == 1, len(runs)
    runs[0].text = "# ON THE MASTER - check the three nodes"
    # Wider labels, so that no word stands alone on a second line.
    for sh in prs.slides[1].shapes:
        if sh.name in ("TextBox 7", "TextBox 10"):
            sh.left, sh.width = Inches(2.55 if sh.name == "TextBox 7" else 6.80), Inches(4.0)
    finish(prs, "CLO835 Week 13 Lab: Authentication and RBAC")
    prs.save(OUT)
    if "--no-repo" not in sys.argv:
        dst, files = L.make_repo_folder("13", "Authentication and RBAC", CLEANUP, SCRIPT, lab_label="Lab Week 13")
        own_flannel(dst)
        own_wording(dst)
        print("repo folder : %s (%d files)" % (dst, len(files)))
