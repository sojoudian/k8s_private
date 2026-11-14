# -*- coding: utf-8 -*-
"""CLO835 Week 13 lab v5 - lab v4 at the level of CLO835_STANDARDS.md v1.2 and of the model Week 12 lab v7.

Each change names the finding of the review round 1 of 2026-11-11 (scratchpad w13review/round1.md):

The cluster slide (slide 3) and Step 0 of the script:
- M19, F1: git fetch and git reset --hard origin/master replace git pull, so a clone made before the history
  rewrite of 2026-11-05 also works (CLUSTER_EDITS of build_week12_lab_v6, with Week13).
- M20: the title is "Build and check the cluster" (no -ing form).
- M21: "These two commands show the public and the private addresses." replaces "prints BOTH".
- M22, B5: the sample output of kubectl get nodes is a comment, with v1.35.10, in the comment color, and the
  sample command starts with "$" (cluster_comment_color of build_week12_lab_v6).
- S19: a fact of the live cluster replaces the NodePort line, because the lab has no Service.
- Slide 3 shows the two git comment lines of the script, and kubectl get nodes -o wide (slide3 of
  build_week12_lab_v7).
- S22, C2: Step 0 of the script lists each command of your own machine as a comment (STEP0 of
  build_week12_lab_v7, with Week13), and its header has the title of slide 3 (step0_title).

The prerequisite slide (slide 2):
- M23: "Kubernetes", not "K8s" (kubernetes_not_k8s of build_week12_lab_v6). The labels have the size and the
  place of the model, so each label breaks into two lines of near the same length.

The step slides and the script:
- M24, C3: each manifest is written with cat > file.yaml <<'EOF'. The CSR file uses cat > dev-user-csr.yaml
  <<EOF with no quotes, because the shell must write the base64 request into the file. A comment gives that
  reason. This is the one allowed exception to the quoted form. The comment "tee writes the file" is gone.
- M25: "# EOF has no quotes, so the shell writes the base64 request into the file." (no phrasal verb).
- M26, C3: the Pod curl-sa uses the helper image maziar/alpine-curl. Its curl command is the same.
- M27, C2: the script header names Lab_week13_v5.pptx (from VERSION).
- S6, C4: Step 1 shows the subject as a sample, and says that the certificate is valid for 24 hours.
- S20, S21, C4: the kubectl proxy line stays one line (it is tested). Comments explain [1], the process ID,
  "Starting to serve", [1]+ Terminated, and the output of auth whoami.
- A1: Step 5 uses "give", not "grant", and "an object with no namespace", not "a cluster-level resource".
  Its first comment is a full sentence.
- The objects keep their names: week13, dev-user, developers, developer, devuser-developer-binding,
  developers-view, clo835, curl-sa, service-reader, service-reader-binding, pv-reader, pv-test.
- The command count stays 39.

The Blackboard text v5 (BLACKBOARD_TEXT, written by this builder, C2):
- M28: "show the answer No resources found" replaces "no Forbidden error comes back" (no phrasal verb).
- M29: "directory", not "folder".
- M30, F4: section 1 starts with the item git fetch and git reset --hard origin/master.
- S24: "with", not "using"; "which shows the message Destroy complete!" replaces "showing Destroy complete!.".
- S25: "the user and the groups".
- S26, C7: the titles of sections 3, 5 and 6 use the words of the deck.
- M24: "display its contents" (the form of the model) in sections 2, 4, 5 and 6.
- Each Run item names a command of its lab step. Each Explain item has its answer in a lab comment or in the
  lecture (the table of F4 is in gate_week13_v2.py).

The repo folder ~/Documents/c/r/CLO835_Fall_2026/Week13/ (7 files, no cleanup script, C5):
- M31 to M36, S28 to S30: repo_words() of build_week12_lab_v7, called by import, so each later Week 12 fix
  also reaches Week 13. C5 wants one wording in every week, so the Week 13 repo text equals the Week 12 repo
  text, except the week name and the topic (gate_week13_v2.py checks it).

After review round 2 of 2026-11-11 (scratchpad w13review2/round2_decks.md):
- MUST-FIX 1 to 3, SHOULD-FIX 1: STEP0 and slide3() of the current build_week12_lab_v7. Slide 2 says "A
  Kubernetes cluster with kubeadm (3 nodes)" and "A container image that the Kubernetes nodes can pull".
  The first line of slide 3 gives one instruction in one sentence. Step 0 of the script holds the comment
  lines of slide 3. The right panel has full sentences. master_check() now only checks "check the three nodes".
- MUST-FIX 4 to 7, SHOULD-FIX 2 and 15: the repo text of the current Week 12 repo_words() (the message of
  the day, "for a short time", "The next try starts in N seconds.", "bootstrap.sh installed the prerequisites.",
  "tries kubeadm join again until the control plane answers", the full sentences of variables.tf and master-init).
- MUST-FIX 8: one instruction in one sentence in the Blackboard items and in the intro of section 2.
- MUST-FIX 11, SHOULD-FIX 5: the Explain item on the three phases of a request moves from section 1 to
  section 3, with its intro sentences. They say "The lab does not show admission control."
- SHOULD-FIX 3, 4, 12, 13: "kubeadm forms the Kubernetes cluster at boot."; "Authentication finds who you
  are."; the Step 2 comment "the API server knows who dev-user is ... can run auth whoami"; "Create
  dev-user-csr.yaml with the cat > command."; "the curl command for /apis".
- SHOULD-FIX 14: build_week13_lab_v2.py and build_week13_lecture_v8.py exit with a message when you run them.
- No command changes. The count stays 39.

After review round 3 of 2026-11-11 (scratchpad w13review3/round3_decks.md):
- MUST-FIX 1: a rebuild takes the current repo_words() of Week 12 (rounds 8 and 9), so the Week 13 repo text
  again equals the Week 12 repo text, except the week name and the topic.
- MUST-FIX 2: the script head of Week 12 round 9: "# Run the commands ON THE MASTER NODE, step by step."
- MUST-FIX 3: Step 6 is STEP6 of build_week12_lab_v7 (by import): "# Terraform asks for key_name again" and
  "# Destroy the cluster at the end of each lab. The Learner Lab budget is small."
- MUST-FIX 4: "- Run terraform destroy in the Week13 directory on your own machine."; section 1 says
  "builds" for the EC2 instances (Week 12 round 9).
- SHOULD-FIX 7: build_week13.py exits with a message when you run it.
- No command changes. The count stays 39.

After review round 4 of 2026-11-11 (scratchpad w13review4/round4_decks.md) and Week 12 round 10:
- MUST-FIX 2: the three Blackboard items of section 4 start with the verb ("- Run the kubectl run web command
  as dev-user, ...").
- The script head of Week 12 round 10: "... step by step, except the commands ON YOUR OWN MACHINE."
- The repo text of Week 12 round 10 (main.tf "Terraform builds no VPC and no subnet."; worker-join "when this
  node starts kubeadm join"), through the imported repo_words().
- No command changes. The count stays 39.

After review round 5 (scratchpad w13review5/round5_decks.md), SHOULD-FIX 4: "allow", not "lets", for a
permission in the comments of Steps 2, 4 and 5 (one word for one meaning). No command changes.

S27 (old builders can overwrite delivered files and the repo): build_week13_lab_v1.py and
build_week13_lab_v3.py now exit with a message when you run them. Importing them still works.

Outputs: week13/Lab_week13_v5.pptx, week13/localMachine_v5.sh,
week13/Lab_week13_Blackboard_Submission_v5.md, ~/Documents/c/r/CLO835_Fall_2026/Week13/ (7 files).
Run from the project root. It stops when an output exists, unless you give --force.
--no-repo does not write the repo folder. It is guarded, so importing it writes nothing.
"""
import os
import sys

from pptx import Presentation

import build_week12_lab_v6 as w12v6
import build_week12_lab_v7 as w12v7
import build_week13_lab_v1 as v1
import build_week13_lab_v4 as v4
import lab_destroy_only as D
import lab_kubeadm as L
from build_week12_lab_v5 import own_flannel
from build_week12_lecture_v6 import finish

VERSION = "v5"
OUT = "week13/Lab_week13_%s.pptx" % VERSION
SCRIPT = "week13/localMachine_%s.sh" % VERSION
BLACKBOARD = "week13/Lab_week13_Blackboard_Submission_%s.md" % VERSION
TITLE = "CLO835 Week 13 Lab: Authentication and RBAC"
IMAGE = "maziar/alpine-curl"
DEV = v1.DEV
PROXY = "$ kubectl proxy --port=8001 & sleep 2; curl -s http://localhost:8001/apis | head -8; kill %1"

# old line -> new lines. Each old line occurs one time in the slide list of v4.
LINE_EDITS = {
    # Step 1 (M24, M25, S6)
    "# No quotes on EOF: the shell puts the request in.":
        ["# EOF has no quotes, so the shell writes the base64 request into the file."],
    "# tee writes the file and shows it.": [],
    "$ tee dev-user-csr.yaml <<EOF": ["$ cat > dev-user-csr.yaml <<EOF"],
    "$ openssl x509 -in dev-user.crt -noout -subject -enddate":
        ["$ openssl x509 -in dev-user.crt -noout -subject -enddate",
         "# subject=O=developers, CN=dev-user",
         "# The certificate is valid for 24 hours, because expirationSeconds is 86400."],
    # Step 2 (S20, S21)
    PROXY:
        [PROXY,
         "# The shell shows [1] and the process ID. The proxy shows Starting to serve on 127.0.0.1:8001.",
         "# kill %1 stops the proxy. Then the shell shows [1]+ Terminated."],
    # Round 2, SHOULD-FIX 4: "the API server" is the component; the comment names the request.
    "# Authentication: the API knows who dev-user is. Every authenticated user can ask this.":
        ["# Authentication: the API server knows who dev-user is. Every authenticated user can run auth whoami."],
    "$ " + DEV + " auth whoami":
        ["$ " + DEV + " auth whoami",
         "# auth whoami shows dev-user, the groups developers and system:authenticated, and a hash of the certificate."],
    # Steps 3 to 5 (M24)
    "$ tee developer-role.yaml <<'EOF'": ["$ cat > developer-role.yaml <<'EOF'"],
    "$ tee curl-sa.yaml <<'EOF'": ["$ cat > curl-sa.yaml <<'EOF'"],
    "$ tee service-reader.yaml <<'EOF'": ["$ cat > service-reader.yaml <<'EOF'"],
    # Step 5 (A1: a full sentence; "give", not "grant"; "object", not "resource")
    "# get and list Services, for the ServiceAccount clo835.":
        ["# The Role service-reader allows the ServiceAccount clo835 to get and list Services."],
    # Round 5, SHOULD-FIX 4: one word for one meaning. The decks use "allow" for a permission, not "let".
    "# Authorization: no Role lets dev-user list Pods yet.":
        ["# Authorization: no Role allows dev-user to list Pods yet."],
    "# who the Pod is. No Role lets it list Services yet.":
        ["# who the Pod is. No Role allows it to list Services yet."],
    "# A RoleBinding does not grant access to a cluster-level resource.":
        ["# A RoleBinding cannot give access to an object with no namespace."],
    "# A ClusterRoleBinding grants it.":
        ["# A ClusterRoleBinding gives this access in the whole cluster."],
}


def slides():
    """The slide list of v4 with LINE_EDITS, the helper image maziar/alpine-curl in curl-sa.yaml (M26), and
    STEP6 of Week 12 v7 for Step 6 (round 3, MUST-FIX 3)."""
    out, done, images, step6 = [], [], 0, 0
    for s in v4.SLIDES:
        if s[0] == "step" and s[1] == D.TITLE:
            assert w12v7.STEP6[1] == D.TITLE
            out.append(w12v7.STEP6)
            step6 += 1
            continue
        if s[0] not in ("step", "step2"):
            out.append(s)
            continue
        lines = []
        for line in s[3]:
            if line in LINE_EDITS:
                lines += LINE_EDITS[line]
                done.append(line)
            else:
                lines.append(line)
        if s[0] == "step":
            out.append(s[:3] + (lines,))
            continue
        body = list(s[6])
        if body == v1.CURL_SA:
            body = [l.replace("image: maziar/curl", "image: " + IMAGE) for l in body]
            images += 1
        out.append(s[:3] + (lines, s[4], s[5], body))
    assert sorted(done) == sorted(LINE_EDITS), set(LINE_EDITS) - set(done)
    assert images == 1 and step6 == 1, (images, step6)
    return out


SLIDES = slides()

# The cluster slide of the model, with Week13 (M19 to M22, S19).
CLUSTER_EDITS = {k: v.replace("Week12", "Week13") for k, v in w12v6.CLUSTER_EDITS.items()}
assert sum(1 for k in CLUSTER_EDITS if CLUSTER_EDITS[k] != w12v6.CLUSTER_EDITS[k]) == 1
assert CLUSTER_EDITS["$ terraform init"] == "$ cd Week13 && terraform init"

# Step 0 of the script: the commands of slide 3 (S22).
STEP0 = [l.replace("cd Week12 ", "cd Week13 ") for l in w12v7.STEP0]
assert sum(1 for a, b in zip(STEP0, w12v7.STEP0) if a != b) == 1
assert not any("eek12" in l for l in STEP0)

SCRIPT_HEAD = """#!/bin/bash
# CLO835 - Week 13 - Authentication and RBAC.
# Run the commands ON THE MASTER NODE, step by step, except the commands ON YOUR OWN MACHINE. Do NOT run the whole file.
#
# Terraform builds 3 EC2 instances: 1 master and 2 workers. The cluster forms
# itself at boot, as in Weeks 04 to 12. The objects that have a namespace are
# in the namespace week13.
#
# Each step matches one slide of Lab_week13_%s.pptx.
""" % VERSION

BLACKBOARD_TEXT = """# Lab Week 13: Authentication and RBAC

## Submission Instructions

Submit a report demonstrating your completion and understanding of all 7 sections of Lab Week 13.

The lab recording demonstrates the steps required to complete this assignment. You may follow the recording step by step. However, your submission must include your own screenshots, actual command outputs, and explanations for all required tasks.

## 1. Build the Cluster and Verify Its Status

The Week 13 Terraform configuration builds three Ubuntu 26.04 EC2 instances, as in Weeks 04 to 12: one master node and two worker nodes. kubeadm forms the Kubernetes cluster at boot.

You must:

- Update the repo with git fetch and git reset --hard origin/master.
- Run terraform init and terraform apply.
- Run terraform output public_ips and terraform output private_ips, and show the addresses of all three nodes.
- Show an SSH session connected to the master node.
- Run kubectl get nodes -o wide and show all three nodes in the Ready state.
- Run kubectl get pods -n kube-system and show the control-plane Pods in the Running state.

## 2. Create a User with a Signed Certificate

Kubernetes stores no users. The cluster CA signs a certificate, and the certificate names the user and the group. Copy the commands of each step from localMachine.sh. Run them on the master node.

You must:

- Create dev-user.key and dev-user.csr with the openssl genrsa and openssl req commands.
- Create dev-user-csr.yaml with the cat > command.
- Apply the manifest.
- Approve the dev-user request with kubectl certificate approve dev-user.
- Run kubectl get csr dev-user and show Approved,Issued.
- Write the certificate to dev-user.crt with the kubectl get csr command and base64 -d.
- Run the openssl x509 command, and show the subject and the end date.
- Explain why Kubernetes does not store users.
- Explain what the CN and O fields of the certificate mean.

## 3. Show That dev-user Is Authenticated, Not Authorized

Authentication finds who you are. Authorization decides what you can do. The first Explain item asks about a lecture topic. The lab does not show admission control.

You must:

- Create the week13 namespace.
- Add the dev-user credentials and the dev-user@kubernetes context with kubectl config set-credentials and kubectl config set-context.
- Run the two curl commands on port 6443, and show the version and the 403 Forbidden answer.
- Run the kubectl proxy command, and show the first lines of the APIGroupList.
- Run kubectl --context=dev-user@kubernetes auth whoami, and show the user and the groups.
- Run kubectl --context=dev-user@kubernetes get pods, and show the Forbidden error.
- Explain the order of the three phases of a request in the API server.
- Explain the difference between authentication and authorization.
- Explain why the curl command for /apis gets 403 Forbidden, and the kubectl proxy request passes.
- Explain why the auth whoami command passes and the get pods command fails.

## 4. Create a Role, a RoleBinding and a Binding for a Group

The Role says what. The RoleBinding says who.

You must:

- Create developer-role.yaml and display its contents.
- Apply the manifest with kubectl apply -f developer-role.yaml -n week13.
- Run the kubectl run web command as dev-user, and show the answer pod/web created.
- Run the kubectl delete pod web command as dev-user, and show the Forbidden error.
- Create the developers-view RoleBinding with the kubectl create rolebinding command.
- Run the kubectl get services command as dev-user, and show the answer No resources found.
- Explain the difference between a Role and a RoleBinding.
- Explain why the Role names configmaps and not ConfigMap.
- Explain how dev-user gets the permissions of the default ClusterRole view.

## 5. Call the API from a Pod with Its Token

A Pod runs as a ServiceAccount, and Kubernetes mounts its token in the Pod.

You must:

- Create the clo835 ServiceAccount.
- Create curl-sa.yaml and display its contents.
- Apply the manifest.
- Run kubectl wait, and show that the curl-sa Pod is Ready.
- Run the curl command in the Pod with kubectl exec, and show the Forbidden answer.
- Explain how the Pod proves its identity to the API server.
- Explain why the API server answers Forbidden.

## 6. Give the ServiceAccount a Role and a ClusterRole

A Role and its RoleBinding work in one namespace. An object with no namespace, such as a PersistentVolume, needs a ClusterRole and a ClusterRoleBinding.

You must:

- Create service-reader.yaml and display its contents.
- Apply the manifest with kubectl apply -f service-reader.yaml -n week13.
- Run the same curl command, and show the ServiceList.
- Run kubectl auth can-i list services for the default namespace, and show no.
- Run the kubectl api-resources command, and show that NAMESPACED is false for persistentvolumes.
- Create the pv-reader ClusterRole.
- Create the pv-test RoleBinding.
- Run kubectl auth can-i list persistentvolumes, and show no.
- Create the pv-test ClusterRoleBinding.
- Run the same kubectl auth can-i command, and show yes.
- Explain why the ServiceAccount gets the answer no in the default namespace.
- Explain why a PersistentVolume needs a ClusterRoleBinding and not a RoleBinding.

## 7. Destroy the Cluster

At the end of the lab, destroy all three EC2 instances. This also deletes every Kubernetes object and every file of the lab.

You must:

- Run terraform destroy in the Week13 directory on your own machine.
- Include the final Terraform output, which shows the message Destroy complete!
- State the number of resources Terraform destroyed.

## Submission Requirements

Your report must include all of the following:

- Your name clearly visible in every screenshot.
- Screenshots demonstrating the required commands and results in all 7 sections.
- Actual output from the commands you executed.
- Clear, detailed explanations of the commands, their purpose, and the results.
- Highlighted or clearly visible output where appropriate.
- Answers to every explanation question specified in the lab.

Important: Use your own screenshots and outputs from your lab environment. Screenshots or outputs copied from the recording or another student's submission do not demonstrate your own work.
"""
assert D.SECTION_NEW + "\n" in BLACKBOARD_TEXT and D.INTRO_NEW in BLACKBOARD_TEXT


def master_check(prs):
    """Slide 3 says "check the three nodes" one time (slide3() of Week 12 v7 writes it), and no "confirm"."""
    texts = [sh.text_frame.text for sh in prs.slides[2].shapes if sh.has_text_frame]
    assert texts.count(w12v7.MASTER) == 1 and not any("confirm" in x for x in texts), texts


def repo_words(dst):
    """repo_words() of build_week12_lab_v7, by import, so that each later Week 12 fix also reaches Week 13 (C5).
    One edit of that function names Week12 (the descriptions of the security groups in main.tf). So the two
    descriptions get the name Week12 for the call, and Week13 again after it."""
    path = os.path.join(dst, "main.tf")
    w13, w12 = 'description = "Week13 Kubernetes ', 'description = "Week12 Kubernetes '
    text = open(path, encoding="utf8").read()
    assert text.count(w13) == 2 and w12 not in text, text.count(w13)
    open(path, "w", encoding="utf8").write(text.replace(w13, w12))
    w12v7.repo_words(dst)
    text = open(path, encoding="utf8").read()
    assert text.count(w12) == 2 and w13 not in text, text.count(w12)
    open(path, "w", encoding="utf8").write(text.replace(w12, w13))


if __name__ == "__main__":
    for out in (OUT, SCRIPT, BLACKBOARD):
        if os.path.exists(out) and "--force" not in sys.argv:
            sys.exit("%s exists. Bump the version; never overwrite a delivered file." % out)
    L.check_lines(SLIDES)
    L.make_lab("13", SLIDES, OUT, SCRIPT_HEAD, step0=STEP0, script_path=SCRIPT,
               prereq_title="Lab Week 13 - Prerequisites", node_version="v1.35.10", cluster_edits=CLUSTER_EDITS)
    prs = Presentation(OUT)
    w12v6.kubernetes_not_k8s(prs)
    w12v6.cluster_comment_color(prs)
    w12v7.slide3(prs)
    master_check(prs)
    finish(prs, TITLE)
    prs.save(OUT)
    w12v7.step0_title(SCRIPT)
    if "--no-repo" not in sys.argv:
        dst, files = L.make_repo_folder("13", "Authentication and RBAC", None, SCRIPT, lab_label="Lab Week 13")
        own_flannel(dst)
        repo_words(dst)
        assert len(files) == 7, files
        low = "".join(open(os.path.join(dst, f), encoding="utf8").read().lower() for f in os.listdir(dst)
                      if os.path.isfile(os.path.join(dst, f)))
        assert "cleanup" not in low and "clean up" not in low, "cleanup text is left in the repo folder"
        print("repo folder : %s (%d files)" % (dst, len(files)))
    open(BLACKBOARD, "w", encoding="utf8").write(BLACKBOARD_TEXT)
    print("blackboard  : %s" % BLACKBOARD)
