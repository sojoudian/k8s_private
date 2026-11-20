# -*- coding: utf-8 -*-
"""Pass-or-fail gate for the Week 13 lab (v3: lab v6 after review round 1 of the Week 13 v10 loop, 2026-11-18;
the title of section 1 and the Explain item on the phases of a request follow the Blackboard text v6;
review round 2: the CSR item, "normal users", the title of section 4 and the view needle).

The original title: Pass-or-fail gate for the Week 13 lab (CLO835_STANDARDS.md v1.2, Parts A, B5, C, E3, F).

It runs deck_checks of gate_week12.py (by import, with ROOT week13/) on the lab deck, and the lab, Blackboard
and live checks of gate_week12.py, adapted to Week 13. It prints PASS or FAIL for each check, then GATE 1 when
every check passes, or GATE 0 when a check fails. It reads the files and changes nothing.

Run from the project root:
    INSTRUMENT=tools/instrument.py .venv/bin/python gate_week13_v2.py LAB_STEM BLACKBOARD_FILE [LIVE_FOLDER]
    INSTRUMENT=tools/instrument.py .venv/bin/python gate_week13_v3.py Lab_week13_v6 Lab_week13_Blackboard_Submission_v6.md

The arguments:
- LAB_STEM: the lab deck in week13/, with no .pptx. Its PDF (week13/LAB_STEM.pdf) must exist. The deck script
  is week13/localMachine_vN.sh for Lab_week13_vN.
- BLACKBOARD_FILE: the Blackboard text in week13/.
- LIVE_FOLDER (optional): the folder of a live test (E3) with run1.log, run2.log (the runner of
  "tools/instrument.py localMachine.sh https://none/" on two new clusters), out_public.log, out_public2.log,
  out_private.log, destroy1.log, destroy.log, pause1.log, lecture.log and run.sh (the tested runner).
  With no LIVE_FOLDER, the gate does no live check, and it says so.
- INSTRUMENT (environment): the path of tools/instrument.py.

F4 (a rubric line must be runnable): the table F4 below has one row for each item of the Blackboard text, with
the command, the comment or the lecture topic that earns it. The gate fails an item with no row, a row with no
item, and a needle that is not in its lab step.

Review round 5 (2026-11-11): "allow", not "let", for a permission (the F4 needles and the A1 patterns).

Review round 4 (2026-11-11): the section 4 items start with the verb; the script head of Week 12 round 10.

Review round 3 (2026-11-11): Step 6 of Week 12 v7 on slide 9 and in the script, the script head of Week 12
round 9, and the Blackboard item "Run terraform destroy in the Week13 directory ...".

Review round 2 (2026-11-11): the slide 2 and slide 3 texts of the current Week 12 v7 model; Step 0 of the
script equals the left panel of slide 3 (C2); the Week 13 repo text equals the Week 12 repo text, except the
week name and the topic (C5); more A1 patterns; one instruction in one Blackboard item; the new F4 rows.
"""
import os
import re
import subprocess
import sys

from pptx import Presentation

import gate_week12 as G
from gate_week12 import check, paragraphs

ROOT = G.ROOT = "week13/"
REPO = G.REPO = os.path.expanduser("~/Documents/c/r/CLO835_Fall_2026/Week13/")
REPO12 = os.path.expanduser("~/Documents/c/r/CLO835_Fall_2026/Week12/")
TOPIC12, TOPIC13 = "CLO835 - Week 12 - ConfigMaps and Secrets", "CLO835 - Week 13 - Authentication and RBAC"
LABELS = ["A Kubernetes cluster with kubeadm (3 nodes)", "A container image that the Kubernetes nodes can pull"]
SLIDE3_LEFT = ["# ON YOUR OWN MACHINE - get the repo. Then build 1 master and 2 workers.",
               "# If no clone exists: git clone https://github.com/sojoudian/CLO835_Fall_2026.git",
               "# git reset --hard replaces your changes with the files of GitHub.",
               "$ cd CLO835_Fall_2026 && git fetch && git reset --hard origin/master",
               "$ cd Week13 && terraform init",
               "$ terraform apply          # Terraform asks for key_name",
               "# These two commands show the public and the private addresses.",
               "$ terraform output public_ips", "$ terraform output private_ips",
               "# kubeadm forms the cluster at boot. Wait about 4 minutes.",
               "$ ssh -i <your-key>.pem ubuntu@<masternode-public-ip>",
               "# ON THE MASTER - check the three nodes", "$ kubectl get nodes -o wide", "$ kubectl get pods -n kube-system"]
SLIDE3_RIGHT = ["$ kubectl get nodes -o wide", "# Three real nodes form this cluster.",
                "# It uses no kind and no Docker in Docker.", "# Other columns show Ubuntu 26.04 and containerd 2.2.2."]
# A1 texts of the old lab decks (the review rounds of Week 12 and Week 13).
DECK_A1 = [r"\bRunning\b", r"accessible by", r"No clone yet", r"build 1 master \+ 2 workers", r"No kind\.",
           r"\bthe API knows\b", r"can ask this", r"\bconfirm\b", r"\bK8s\b", r"\blets?\b"]
TITLE = "# Lab Week 13: Authentication and RBAC"
ALSO = "# This also deletes every Kubernetes object and every file of the lab."
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
# An -ing form. RoleBinding, ClusterRoleBinding and Binding are names of Kubernetes objects, not verb forms.
ING = r"\b(?!\w*Binding\b)\w+ing\b"
# The objects of the lab, one name each (C3), and the command that creates each one.
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
# The planned denials: a comment predicts each one (C9). They exit 1, in this order.
STEP6 = ["# ON YOUR OWN MACHINE - destroy the three EC2 instances.", ALSO,
         "$ terraform destroy          # Terraform asks for key_name again",
         "# Destroy the cluster at the end of each lab. The Learner Lab budget is small."]
HEAD = ["# CLO835 - Week 13 - Authentication and RBAC.",
        "# Run the commands ON THE MASTER NODE, step by step, except the commands ON YOUR OWN MACHINE. Do NOT run the whole file.",
        "# Terraform builds 3 EC2 instances: 1 master and 2 workers. The cluster forms"]
DENIALS = [DEV + " get pods",
           DEV + " delete pod web                     # Forbidden",
           "kubectl auth can-i list services -n default " + SA + "   # no",
           "kubectl auth can-i list persistentvolumes -A " + SA + "   # no"]
# A1 words that must not be in the script, the repo files or the Blackboard text.
A1 = [r"\bK8s\b", r"\bprints?\b", r"\bfolders?\b", r"\b[Rr]efus", r"control-plane node", r"CONTROL PLANE node",
      r"\b[Tt]urn (on|off)\b", r"\b(turns|turned) (on|off)\b", r"\bcomes? back\b", r"\bputs? .{0,30}\bin\.",
      r"\bshut down\b", r"\bhand over\b", r"\bgo (out|past)\b", r"\bat once\b", r"\bcarry over\b", r"\bholds back\b",
      r"\bretrying\b", r"\bsticks\b", r"\bSSH in\b", r"\bis appended\b", r"\bis not blocked\b", r"\bis dropped\b",
      r"\bships one\b", r"\bUsed for SSH\b", r"\bLab only\b", r"\bchars\b", r"—", r"\br6i\b", r"\bwithout \w+ing\b",
      r"\bcleanup\b", r"\bclean[ -]up\b", r"\btee\b", r"\bgrants?\b", r"\bpods? network\b",
      # Review round 2 (Week 12 rounds 4 to 7): no idiom, a full sentence, one word for one meaning.
      r"\bNext try in\b", r"Prerequisites installed", r"by themselves", r"Give them a few minutes", r"\bright after\b",
      r"No clone yet", r"\bthe API knows\b", r"can ask this", r"initializes automatically", r"Authentication checks",
      r"does not run admission control", r"retries kubeadm join", r"\battached to the node\b", r"(?m)^# kubeconfig for",
      # Review round 3 (Week 12 rounds 8 and 9).
      r"section by section", r"Run these ON", r"(?<!Terraform )asks for key_name", r"Always destroy", r"From the Week13",
      r"x86_64", r"does not permit", r"Terraform builds 3 machines", r"next try starts", r"\bwould stop\b",
      # Review round 4 (Week 12 round 10): an item starts with its verb; one verb for an AWS object.
      r"(?m)^- As dev-user", r"Terraform creates no VPC", r"when this node is ready",
      # Review round 5, SHOULD-FIX 4: "allow", not "let", for a permission.
      r"\blets?\b"]

# F4: (section, item, source, needles). source "step": each needle is in a command line of the lab step of the
# section (section 1 and 7: in the step text, because the commands of your own machine are comments).
# "comment": each needle is in a comment line of that step. "lecture": the answer is a lecture topic
# (scratchpad w13review/round1.md, list 3); the needle names it, and the gate does not search for it.
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


def runner():
    return subprocess.run([sys.executable, "-I", os.environ["INSTRUMENT"], REPO + "localMachine.sh", "https://none/"],
                          capture_output=True, text=True).stdout


def steps(script):
    """{n: the text of Step n}, from the "# Step n - " headers of the script."""
    parts = re.split(r"^# Step (\d) - .*$", script, flags=re.M)
    return {int(parts[k]): parts[k + 1] for k in range(1, len(parts), 2)}


def command_lines(text):
    return [l for l in text.split("\n") if l.strip() and not l.lstrip().startswith("#")]


def comment_lines(text):
    return [l for l in text.split("\n") if l.lstrip().startswith("#")]


def heredocs(script):
    """{file name: body lines} of each cat > file <<EOF block."""
    return {m.group(1): m.group(2).split("\n")
            for m in re.finditer(r"^cat > (\S+) <<'?EOF'?\n(.*?)\nEOF$", script, re.M | re.S)}


def prose(body):
    """The text of a script or a Terraform file that a person reads: the comments, the description fields, the
    echo texts and the message of the day. The Flannel manifest of master-init is not prose."""
    body = re.sub(r"<<'MANIFEST'\n.*?\nMANIFEST\n", "", body, flags=re.S)
    out = [l.strip() for l in body.split("\n") if l.lstrip().startswith("#") and not l.startswith("#!")]
    out += re.findall(r'description\s*=\s*"([^"]*)"', body)
    out += re.findall(r'echo "([^"$]*)"', body)
    out += [m for m in re.findall(r"<<'MOTD'\n(.*?)\nMOTD", body, re.S)]
    return "\n".join(out)


def lab_deck_checks(lab, script):
    prs = Presentation(ROOT + lab + ".pptx")
    slides = list(prs.slides)
    check("lab deck: 10 slides", len(slides) == 10, len(slides))
    texts = [[t for no, sh, p, t in paragraphs(prs) if no == k] for k in range(1, len(slides) + 1)]
    check("lab deck: the slide titles of C1, in order",
          all(SLIDE_TITLES[k] in texts[k] for k in range(min(10, len(texts)))),
          [(k + 1, SLIDE_TITLES[k]) for k in range(min(10, len(texts))) if SLIDE_TITLES[k] not in texts[k]])
    titles = [t for t in SLIDE_TITLES if re.search(ING, t)]
    check("lab deck: no -ing form in a slide title", not titles, titles)
    every = [t for page in texts for t in page]
    check("lab deck: Kubernetes, not K8s", not [t for t in every if "K8s" in t], [t for t in every if "K8s" in t][:3])
    bad = [(k + 1, m.group(0)) for k, page in enumerate(texts) for x in page for b in DECK_A1 for m in [re.search(b, x)] if m]
    check("lab deck: A1 words of the review rounds (no -ing form, full sentences, Kubernetes)", not bad, bad[:5])
    check("lab deck: slide 2 labels (round 2, MUST-FIX 1)", all(x in texts[1] for x in LABELS), texts[1])
    s3 = slides[2]
    rows = sorted(((sh.top, sh.left, sh.text_frame.text) for sh in s3.shapes if sh.has_text_frame
                   and 1.8 * 914400 < sh.top < 6.5 * 914400 and sh.text_frame.text.strip()), key=lambda r: (r[1] > 8 * 914400, r[0]))
    left = [x for top, lft, x in rows if lft < 8 * 914400]
    right = [x for top, lft, x in rows if lft > 8 * 914400]
    check("lab deck: slide 3 left panel, line for line (M19 to M21; round 2 MUST-FIX 2, SHOULD-FIX 1)",
          left == SLIDE3_LEFT, [x for x in left if x not in SLIDE3_LEFT] + [x for x in SLIDE3_LEFT if x not in left])
    sample = [x for x in right if re.search(r"\b(NAME|masternode|workernode\d)\s{2,}", x)]
    check("lab deck: slide 3 right panel (round 2, SHOULD-FIX 1)", [x for x in right if x not in sample] == SLIDE3_RIGHT,
          [x for x in right if x not in sample])
    check("lab deck: slide 3 sample output is 4 comment lines with v1.35.10 (B5, C4)",
          len(sample) == 4 and all(x.startswith("# ") for x in sample) and sum("v1.35.10" in x for x in sample) == 3,
          sample)
    master = SLIDE3_LEFT.index("# ON THE MASTER - check the three nodes")
    want = [("# ON YOUR OWN MACHINE:  " + x[2:] if x.startswith("$ ") and k < master else x[2:] if x.startswith("$ ") else x)
            for k, x in enumerate(SLIDE3_LEFT)]
    got = [x for x in steps(script)[0].split("\n")[2:] if x.strip() and set(x) != {"#"}]
    check("lab: Step 0 of the script holds the lines of slide 3, in order (C2; round 2, MUST-FIX 3)", got == want,
          [x for x in got if x not in want] + [x for x in want if x not in got])
    s9 = [t for t in texts[8] if t != SLIDE_TITLES[8] and not t.startswith("CLO835")]
    check("lab deck: slide 9 is STEP6 of Week 12 v7: only terraform destroy and the comments (round 3, MUST-FIX 3)",
          [t for t in s9 if t != "bash"] == STEP6, s9)
    # C2: one content list. Each command of slides 4 to 8 is a line of the script, and back.
    deck = [t[2:] for page in texts[3:8] for t in page if t.startswith("$ ")]
    lines = set(script.split("\n"))
    check("lab deck: each command of slides 4 to 8 is in the script", all(c in lines for c in deck),
          [c for c in deck if c not in lines][:3])
    st = steps(script)
    first = [l for n in range(1, 6) for l in command_lines(st[n])
             if not l.startswith(" ") and l != "EOF" and not re.match(r"^[a-zA-Z]+:|^- |^---", l)]
    check("lab deck: each command of Steps 1 to 5 is on a slide", all(c in deck for c in first),
          [c for c in first if c not in deck][:3])
    # C3: the right panel shows the file, line for line.
    docs = heredocs(script)
    for no in range(4, 9):
        slide = slides[no - 1]
        right = [sh for sh in slide.shapes if sh.has_text_frame and sh.left > 8 * 914400
                 and 1.8 * 914400 < sh.top < 6.5 * 914400]
        body = [p.text for sh in right for p in sh.text_frame.paragraphs]
        bar = [sh.text_frame.text for sh in slide.shapes if sh.has_text_frame and sh.left > 8 * 914400
               and sh.top < 1.8 * 914400 and sh.text_frame.text.strip()]
        if no == 5:
            check("lab deck: slide 5 has no file panel", not right and not bar, bar)
            continue
        name = bar[0] if bar else None
        check("lab deck: slide %d shows %s as written by the script" % (no, name),
              name in docs and body == docs[name], (name, [x for x in body if x not in docs.get(name, [])][:3]))


def lab_checks(lab, blackboard):
    run = runner()
    count = run.count('echo "@@CMD')
    check("lab: at most 40 commands on the master (%d)" % count, count <= 40, count)
    script = open(REPO + "localMachine.sh").read()
    check("lab: Step 0 to Step 6, and Step 6 has no command on the master",
          re.findall(r"@@STEP (\d)", run) == list("012345") and re.findall(r"^# Step (\d) - ", script, re.M) == list("0123456"),
          (re.findall(r"@@STEP (\d)", run), re.findall(r"^# Step (\d) - ", script, re.M)))
    step6 = script.split("# Step 6 - ")[1].split("\n")[3:]
    check("lab: Step 6 holds only terraform destroy and the C1 comment",
          [l for l in step6 if l.strip() and not l.startswith("#")] == [] and "terraform destroy" in "\n".join(step6)
          and ALSO in step6, step6)
    check("lab: each step names its slide", re.findall(r"# Step (\d) - .*\(slide (\d+)\)", script)
          == [(str(i), str(i + 3)) for i in range(7)])
    check("lab: Step 0 has the title of slide 3", "# Step 0 - Build and check the cluster          (slide 3)" in script)
    deck_script = ROOT + lab.replace("Lab_week13", "localMachine") + ".sh"
    check("lab: the repo script equals the deck script", script == open(deck_script).read(), deck_script)
    check("lab: the script header names the deck (M27)", "# Each step matches one slide of %s.pptx." % lab in script)
    check("lab: the script head of Week 12 round 9 (round 3, MUST-FIX 2)", script.split("\n")[1:3] == HEAD[:2]
          and HEAD[2] in script.split("\n")[:6], script.split("\n")[1:6])
    tail = [l for l in script.split("# Step 6 - ")[1].split("\n")[2:] if l.strip()]   # [0] title, [1] the rule line
    check("lab: Step 6 of the script is STEP6 of Week 12 v7 (C2; round 3, MUST-FIX 3)",
          tail == [STEP6[0], ALSO, "# ON YOUR OWN MACHINE:  " + STEP6[2][2:], STEP6[3]], tail)
    st = steps(script)
    check("lab: Step 0 has git fetch and git reset --hard origin/master (M19, S22)",
          "# ON YOUR OWN MACHINE:  cd CLO835_Fall_2026 && git fetch && git reset --hard origin/master" in st[0]
          and "# ON YOUR OWN MACHINE:  cd Week13 && terraform init" in st[0] and "git pull" not in script)
    names = sorted(x for x in os.listdir(REPO) if x != ".terraform")
    check("lab: 7 files", names == sorted([".gitignore", "bootstrap.sh", "localMachine.sh", "main.tf",
                                           "master-init.sh.tftpl", "variables.tf", "worker-join.sh.tftpl"]), names)
    check("lab: no state or key file", not [x for x in os.listdir(REPO) if re.search(r"tfstate|tfvars|\.pem|\.key$", x)])
    for f in ("localMachine.sh", "bootstrap.sh", "master-init.sh.tftpl", "worker-join.sh.tftpl"):
        check("lab: bash -n " + f, subprocess.run(["bash", "-n", REPO + f]).returncode == 0)
    check("lab: terraform fmt", subprocess.run(["terraform", "-chdir=" + REPO, "fmt", "-check"], capture_output=True).returncode == 0)
    text = "".join(open(REPO + x, errors="replace").read() for x in names)
    bad = re.findall(r"/Users/|\.ssh/|173\.33\.124\.240|sojodyan|[Ss]ojoudian(?!/CLO835_Fall_2026\.git)|@gmail|mazSeneca|"
                     r"AKIA[0-9A-Z]{12}|ASIA[0-9A-Z]{12}|luksa|busybox|\bnano\b|flannel-io|ghcr\.io|"
                     r"\b[Ww]eek ?(0[1-9]|1[0-24-9])\b", text)
    check("lab: repo scan (F3, other weeks)", not bad, bad[:5])
    master = open(REPO + "master-init.sh.tftpl").read()
    check("lab: no cleanup script or cleanup text in the repo folder",
          not re.search(r"cleanup|clean[ -]up", text, re.I))
    images = sorted(set(re.findall(r"(?:^\s*(?:- )?image:\s*|--image=)(\S+)", script, re.M)))
    check("lab: images of maziar only", images and all(i.startswith("maziar/") for i in images), images)
    check("lab: the helper image is maziar/alpine-curl (M26)", "maziar/alpine-curl" in images and "maziar/curl" not in images,
          images)
    flannel = re.findall(r"^\s*image:\s*(\S+)", master, re.M)
    check("lab: Flannel images of maziar only", len(flannel) == 3 and all(i.startswith("maziar/") for i in flannel), flannel)
    check("lab: the message of the day names Week 13, the MASTER node and localMachine.sh",
          "CLO835 - Week 13 - Authentication and RBAC" in master and "You are on the MASTER node." in master
          and "localMachine.sh" in master)
    variables = open(REPO + "variables.tf").read()
    key = re.search(r'variable "key_name" \{(.*?)\n\}', variables, re.S).group(1)
    profile = re.search(r'variable "lab_instance_profile" \{(.*?)\n\}', variables, re.S).group(1)
    check("lab: key_name has no default; lab_instance_profile defaults to LabInstanceProfile",
          "default" not in key and re.search(r'default\s*=\s*"LabInstanceProfile"', profile) is not None)
    heads = re.findall(r"^(\S.*<<'?EOF'?)$", script, re.M)
    want = ["cat > dev-user-csr.yaml <<EOF", "cat > developer-role.yaml <<'EOF'", "cat > curl-sa.yaml <<'EOF'",
            "cat > service-reader.yaml <<'EOF'"]
    check("lab: each manifest is written with cat > file <<'EOF'; only the CSR file has no quotes (C3, M24)",
          heads == want and not re.search(r"^tee ", script, re.M), heads)
    csr = script.split("cat > dev-user-csr.yaml <<EOF")[0].rstrip("\n").split("\n")[-1]
    check("lab: a comment gives the reason for the unquoted EOF (M25)",
          csr == "# EOF has no quotes, so the shell writes the base64 request into the file.", csr)
    check("lab: the kubectl proxy line is the tested line", PROXY in command_lines(st[2]))
    missing = [o for o, needle in OBJECTS.items() if needle not in script]
    check("lab: each object keeps its name", not missing, missing)
    texts = {x: prose(open(REPO + x, errors="replace").read()) for x in names}
    texts["Blackboard text"] = open(ROOT + blackboard).read()
    bad = [(name, b, m.group(0)) for name, body in texts.items() for b in A1 for m in [re.search(b, body)] if m]
    check("lab: A1 words in the comments of the script and the repo files, and in the Blackboard text", not bad, bad[:6])
    check("lab: the planned denials are lines of the script", all(d in script.split("\n") for d in DENIALS),
          [d for d in DENIALS if d not in script.split("\n")])
    check("lab: the sample version is v1.35.10", "v1.35.9" not in script and "v1.35.0" not in script)
    diffs = []
    for x in names:
        if x == "localMachine.sh":
            continue
        a = open(REPO12 + x, encoding="utf8").read()
        a = a.replace("  %s\n  %s\n" % (TOPIC12, "-" * len(TOPIC12)), "  %s\n  %s\n" % (TOPIC13, "-" * len(TOPIC13)))
        for w12, w13 in (("Week12", "Week13"), ("week12", "week13"), ("Week 12", "Week 13")):
            a = a.replace(w12, w13)
        b = open(REPO + x, encoding="utf8").read()
        if a != b:
            diffs.append((x, [l for l in b.split("\n") if l not in a.split("\n")][:2]))
    check("lab: the repo text equals the Week 12 repo text, except the week name and the topic (C5)", not diffs, diffs)
    lab_deck_checks(lab, script)


def blackboard_checks(blackboard):
    b = open(ROOT + blackboard).read()
    check("blackboard: title", b.startswith(TITLE + "\n"))
    check("blackboard: 7 sections", len(re.findall(r"^## \d\. ", b, re.M)) == 7 and "all 7 sections" in b)
    found = re.findall(r"^## \d\. (.*)$", b, re.M)
    check("blackboard: the section titles use the words of the deck (S26)", found == SECTIONS, found)
    ing = [t for t in found if re.search(ING, t)]
    check("blackboard: no -ing form in a section title", not ing, ing)
    check("blackboard: no pledge", "pledge" not in b.lower())
    check("blackboard: ends with the Important paragraph", b.strip().split("\n")[-1].startswith("Important: Use your own"))
    check("blackboard: no control-plane node; master node", "control-plane node" not in b and "master node" in b)
    check("blackboard: section 7 is Destroy the Cluster, with no cleanup item",
          "## 7. Destroy the Cluster\n" in b and not re.search(r"clean[ -]?up", b, re.I))
    check("blackboard: directory, not folder (M29); the item starts with its verb (round 3, MUST-FIX 4)",
          "\n- Run terraform destroy in the Week13 directory on your own machine.\n" in b
          and "builds three Ubuntu 26.04 EC2 instances" in b
          and "folder" not in b.lower())
    check("blackboard: no 'using', 'showing' or '!.' (S24)", not re.search(r"\busing\b|\bshowing\b|!\.", b))
    check("blackboard: the user and the groups (S25)", "show the user and the groups." in b)
    check("blackboard: kubeadm forms the Kubernetes cluster at boot (round 2, SHOULD-FIX 3)",
          "kubeadm forms the Kubernetes cluster at boot." in b)
    check("blackboard: the lab does not show admission control, in section 3 (round 2, MUST-FIX 11, SHOULD-FIX 5)",
          "The lab does not show admission control." in b.split("## 3. ")[1].split("## 4. ")[0]
          and "admission" not in b.split("## 3. ")[0])
    two = [l for l in b.split("\n") if l.startswith("- ")
           and (re.search(r", then\b|\band wait\b|, and (approve|create|apply|wait)\b", l)
                or re.search(r"^- (Create|Apply|Update|Add|Write|Approve)\b.*, run\b", l))]
    two += [l for l in b.split("\n") if "from localMachine.sh, and run" in l]
    check("blackboard: one instruction in one item (round 2, MUST-FIX 8)", not two, two)
    req = b.split("## Submission Requirements")[1].split("Important:")[0]
    check("blackboard: Submission Requirements with six items", len(re.findall(r"^- ", req, re.M)) == 6)
    sections = re.split(r"^## \d\. ", b, flags=re.M)[1:]
    items = {}
    for k, sec in enumerate(sections, 1):
        body = sec.split("## Submission")[0]
        check("blackboard: 'You must:' in section %d" % k, "\nYou must:\n" in body)
        its = [l[2:] for l in body.split("\n") if l.startswith("- ")]
        kinds = [i.startswith("Explain") for i in its]
        check("blackboard: Explain items last in '%s'" % sec.split("\n")[0][:30], kinds == sorted(kinds))
        for i in its:
            items[(k, i)] = True
    return b, items


def f4_checks(items):
    script = open(REPO + "localMachine.sh").read()
    st = steps(script)
    rows = {(k, i): (src, needles) for k, i, src, needles in F4}
    check("F4: each Blackboard item has a row", not set(items) - set(rows), sorted(set(items) - set(rows))[:4])
    check("F4: each row has a Blackboard item", not set(rows) - set(items), sorted(set(rows) - set(items))[:4])
    runs = [(k, i) for (k, i) in items if i.startswith("Run ")]
    check("F4: each Run item has a command of its step", all(rows.get(r, ("",))[0] == "step" for r in runs),
          [r for r in runs if rows.get(r, ("",))[0] != "step"])
    misses = []
    for (k, i), (src, needles) in rows.items():
        step = st[k - 1]
        if src == "step":
            where = step if k in (1, 7) else "\n".join(command_lines(step))
        elif src == "comment":
            where = " ".join(l.lstrip("# ").strip() for l in comment_lines(step))
        else:
            continue
        misses += [(k, n) for n in needles if n not in where]
    check("F4: each needle is in its lab step", not misses, misses[:5])
    lecture = [(k, i[:50]) for (k, i), (src, _) in rows.items() if src == "lecture"]
    print("INFO  F4 rows answered by the lecture, not by the lab: %s" % lecture)


def live_checks(folder):
    def read(name):
        return open(os.path.join(folder, name), errors="replace").read()
    final = runner()
    count = final.count('echo "@@CMD')
    for no in (1, 2):
        log = read("run%d.log" % no)
        check("live: pass %d ran all %d commands" % (no, count), log.count("@@CMD") == count, log.count("@@CMD"))
        failed = re.findall(r"@@CMD L\d+: ([^\n]*)\n(?:(?!@@CMD).*\n)*?@@RC [1-9]", log)
        check("live: pass %d has only the four planned denials as non-zero exits (C9)" % no, failed == DENIALS, failed)
        answers = [x.strip() for x in log.split("\n") if x.strip() in ("no", "yes")]
        check("live: pass %d can-i answers are no, no, yes" % no, answers == ["no", "no", "yes"], answers)
        for sample in ("Approved,Issued", "subject=O=developers, CN=dev-user", '"reason": "Forbidden"',
                       '"kind": "APIGroupList"', "Starting to serve on 127.0.0.1:8001", "[developers system:authenticated]",
                       'User "dev-user" cannot list resource "pods"', "pod/web created",
                       "No resources found in week13 namespace.", '"kind": "ServiceList"', '"items": []',
                       "pod/curl-sa condition met"):
            check("live: pass %d shows the sample '%s' (C4)" % (no, sample[:40]), sample in log)
        nsd = re.search(r"persistentvolumes\s+pv\s+v1\s+false\s+PersistentVolume", log)
        check("live: pass %d shows NAMESPACED false for persistentvolumes" % no, nsd is not None)
    check("live: terraform output public_ips", "master" in read("out_public.log"))
    check("live: terraform output private_ips", "master" in read("out_private.log"))
    lecture = read("lecture.log")
    check("live: lecture commands have no error", lecture.strip() != ""
          and not re.search(r"(?i)^error: |invalid|unable to|unknown (flag|command)", lecture, re.M))
    masters = [re.search(r'"master"\s*=\s*"([\d.]+)"', read(f)) for f in ("out_public.log", "out_public2.log")]
    check("live: pass 2 ran on a new cluster (two master addresses)", all(masters) and masters[0].group(1) != masters[1].group(1),
          [m and m.group(1) for m in masters])
    for f in ("destroy1.log", "destroy.log"):
        check("live: destroy complete (%s)" % f, "Destroy complete! Resources: 15 destroyed." in read(f))
    pause = read("pause1.log")
    check("live: cluster runs the maziar Flannel image", "maziar/flannel:v0.28.10" in pause and "ghcr.io" not in pause)
    check("live: no recovery test (terraform destroy is the recovery)", not os.path.exists(os.path.join(folder, "recovery.log")))
    tested = re.sub(r"@@CMD L\d+:", "@@CMD", read("run.sh"))
    check("live: the tested commands equal the final commands", tested.strip() == re.sub(r"@@CMD L\d+:", "@@CMD", final).strip())


def main():
    if len(sys.argv) < 3 or "INSTRUMENT" not in os.environ:
        sys.exit(__doc__)
    lab, blackboard = sys.argv[1:3]
    G.deck_checks(lab, "lab")
    lab_checks(lab, blackboard)
    _, items = blackboard_checks(blackboard)
    f4_checks(items)
    if len(sys.argv) > 3:
        live_checks(sys.argv[3])
    else:
        print("INFO  no LIVE_FOLDER: the gate did no live check (E3, C9).")
    print("\nGATE %d  (%d failed)" % (0 if G.FAILS else 1, len(G.FAILS)))
    sys.exit(1 if G.FAILS else 0)


if __name__ == "__main__":
    main()
