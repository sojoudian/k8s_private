# -*- coding: utf-8 -*-
"""CLO835 Week 12 lab v7 - lab v6 with no cleanup script (CLO835_STANDARDS.md v1.2, the user, 2026-11-11).

terraform destroy removes the three machines, and with them every Kubernetes object and every file of
the lab, so:
- Step 6 is "Destroy the cluster": only terraform destroy on your own machine (lab_destroy_only.ALSO).
- The repo folder has no cleanup_lab12.sh, and master-init writes no cleanup file
  (make_repo_folder(..., None, ...), standards C5 and H10).
- Section 7 of the Blackboard text is "Destroy the Cluster", with no cleanup item.
- The A1 words of v6 (repo_words) stay, except the two edits of the cleanup text.
After review round 3 of 2026-11-11 (scratchpad w12review/round3_decks.md):
- The kubelet updates a ConfigMap volume "within about two minutes" (sync period plus cache TTL, 1 minute
  each by default, kubernetes.io configure-pod-configmap); "has priority", not "wins" (one word for one
  meaning, as lecture slide 22); Step 5 says that a real project puts no Secret manifest in source control.
- Slide 3 shows the two git lines of the script, and kubectl get nodes -o wide (only -o wide shows the
  OS and containerd); the script header of Step 0 has the title of slide 3.
- The repo files get more A1 words: worker-join.sh.tftpl, the retry messages, variables.tf and main.tf.
After review round 4 (scratchpad w12review4/round4_decks.md): STEP0 holds the comment lines of slide 3
(C2), and both say "check the three nodes"; slide 2 says "A Kubernetes cluster with kubeadm"; the Step 5
comment is a full sentence; main.tf, master-init.sh.tftpl and bootstrap.sh get more A1 words.
After review round 5 (scratchpad w12review5/round5_decks.md): one instruction in one sentence in the first
line of slide 3 and in the Blackboard items; full sentences in the comments "If no clone exists", "Three
real nodes form this cluster" and "Create a namespace"; the message of the day says "Wait until all three
nodes are Ready"; the Blackboard text says "kubeadm forms the Kubernetes cluster at boot".
After review round 6: the two retry messages are full sentences ("The next try starts in N seconds.").
After review round 7: each prose comment of main.tf, variables.tf and master-init.sh.tftpl is a full
sentence with its articles; the unverified r6i claim goes (the Learner Lab allows r8i.large, standards E1).
After review round 8 (scratchpad w12review8/round8_decks.md): full sentences in variables.tf; amd64, "allow",
8 GiB and "the xlarge size" in main.tf; "the API server" and "repo" in main.tf; the NodePort comment; "can
stop" (no "would") in master-init; "tries ... again" (no noun "try") in the retry messages; "step by step"
and "3 EC2 instances" in the script head; "Destroy the cluster at the end of each lab." on slide 9; the
Blackboard item of section 7 starts with its verb.
After review round 9 (scratchpad w12review9/round9_decks.md): main.tf says "Terraform creates no VPC and no
subnet" (no unproven claim about the Learner Lab) and "AMI"; the script head says "Run the commands"; the
Blackboard text says "builds" for the EC2 instances; "the script tries the apply again" in master-init;
"Try kubeadm join again" in worker-join.
After review round 10 (scratchpad w12review10/round10_decks.md): the script head names the commands of
your own machine as the exception; "Terraform builds no VPC and no subnet" (one verb for Terraform); the
worker-join comment says "when this node starts kubeadm join" ("Ready" is a node condition).
All other content is v6 (imported, not copied).

Outputs: Week12/Lab_week12_v7.pptx, Week12/localMachine_v7.sh,
Week12/Lab_week12_Blackboard_Submission_v7.md, ~/Documents/c/r/CLO835_Fall_2026/Week12/
Run from the project root. It refuses to overwrite an output, unless you give --force.
--no-repo skips the repo folder. It is guarded, so importing it writes nothing.
"""
import os
import sys

from pptx import Presentation

import build_week12_lab_v6 as v6
import lab_destroy_only as D
import lab_kubeadm as L
from build_week12_lecture_v6 import finish

VERSION = "v7"
OUT = "Week12/Lab_week12_%s.pptx" % VERSION
SCRIPT = "Week12/localMachine_%s.sh" % VERSION
BLACKBOARD = "Week12/Lab_week12_Blackboard_Submission_%s.md" % VERSION

V6_STEP6 = "Delete the objects, and destroy the cluster"
STEP6 = ("step", D.TITLE, "bash", [
    "# ON YOUR OWN MACHINE - destroy the three EC2 instances.",
    D.ALSO,
    "L$ terraform destroy          # Terraform asks for key_name again",
    " ",
    "# Destroy the cluster at the end of each lab. The Learner Lab budget is small.",
])


LINE_EDITS = {   # review round 3: old line -> new lines
    "# Change the ConfigMap. The kubelet updates the file within about one minute.":
        ["# Change the ConfigMap. The kubelet updates the file within about two minutes."],
    "# A namespace for the objects of the lab.": ["# Create a namespace for the objects of the lab."],
    "# When env and envFrom set the same name, the value of env wins.":
        ["# When env and envFrom set the same name, the value of env has priority."],
    "$ cat > config-dev.yaml <<'EOF'":
        ["# These values are for the lab only. Put no Secret manifest in source control.",
         "$ cat > config-dev.yaml <<'EOF'"],
}


def slides():
    out, n, done = [], 0, set()
    for s in v6.SLIDES:
        if s[0] == "step" and s[1] == V6_STEP6:
            out.append(STEP6)
            n += 1
        elif s[0] in ("step", "step2"):
            lines = []
            for line in s[3]:
                if line in LINE_EDITS:
                    lines += LINE_EDITS[line]
                    done.add(line)
                else:
                    lines.append(line)
            out.append(s[:3] + (lines,) + tuple(s[4:]))
        else:
            out.append(s)
    assert n == 1, n
    assert done == set(LINE_EDITS), set(LINE_EDITS) - done
    return out


SLIDES = slides()

GIT_RESET_OLD = "# git reset --hard replaces your local changes in the repo with the files of GitHub."
GIT_RESET = "# git reset --hard replaces your changes with the files of GitHub."
GIT_CLONE_OLD = "# No clone yet? git clone https://github.com/sojoudian/CLO835_Fall_2026.git"
GIT_CLONE = "# If no clone exists: git clone https://github.com/sojoudian/CLO835_Fall_2026.git"
FIRST_OLD = "# ON YOUR OWN MACHINE - get the repo, build 1 master + 2 workers"
FIRST = "# ON YOUR OWN MACHINE - get the repo. Then build 1 master and 2 workers."
assert v6.STEP0.count(GIT_RESET_OLD) == 1 and v6.STEP0.count(GIT_CLONE_OLD) == 1
MASTER_OLD = "# ON THE MASTER - all three nodes must reach Ready. The workers take a few minutes to join."
MASTER = "# ON THE MASTER - check the three nodes"


def step0():
    """Step 0 of the script holds the comment lines of slide 3, in the order of the slide (C2, round 4)."""
    out = []
    for line in v6.STEP0:
        if line == GIT_RESET_OLD:
            out.append(GIT_RESET)
        elif line == GIT_CLONE_OLD:
            out.append(GIT_CLONE)
        elif line == FIRST_OLD + " (slide 3).":
            out.append(FIRST)
        elif line == MASTER_OLD:
            out.append(MASTER)
        elif line == "# ON YOUR OWN MACHINE:  terraform output public_ips":
            out += ["# These two commands show the public and the private addresses.", line]
        elif line.startswith("# ON YOUR OWN MACHINE:  ssh "):
            out += ["# kubeadm forms the cluster at boot. Wait about 4 minutes.", line]
        else:
            out.append(line)
    assert len(out) == len(v6.STEP0) + 2 and all(x in out for x in (MASTER, GIT_RESET, GIT_CLONE, FIRST))
    return out


STEP0 = step0()

SCRIPT_HEAD = (v6.SCRIPT_HEAD.replace("Lab_week12_v6.pptx", "Lab_week12_%s.pptx" % VERSION)
               .replace("section by section.", "step by step.")
               .replace("# Run these ON THE MASTER NODE, step by step.",
                        "# Run the commands ON THE MASTER NODE, step by step, except the commands ON YOUR OWN MACHINE.")
               .replace("Terraform builds 3 machines:", "Terraform builds 3 EC2 instances:"))
assert "step by step, except the commands ON YOUR OWN MACHINE." in SCRIPT_HEAD and "3 EC2 instances:" in SCRIPT_HEAD


def blackboard_text():
    text = v6.BLACKBOARD_TEXT
    old_title = "## 7. Delete the Objects and Destroy the Cluster"
    assert text.count(old_title) == 1
    text = text.replace(old_title, D.SECTION_OLD)
    # Review round 3: lecture slide 27 lists these two topics as "Not in the lab", so the text says that the
    # lecture holds their answers.
    intro = "Each Pod also gets a ServiceAccount token.\n"
    assert text.count(intro) == 1
    text = text.replace(intro, "Each Pod also gets a ServiceAccount token. The last two Explain items ask about lecture "
                               "topics that the lab does not run.\n")
    # Review round 5: one instruction in one sentence (A1), and one word for one meaning ("forms").
    for old, new in (
            ("The Kubernetes cluster initializes automatically at boot.", "kubeadm forms the Kubernetes cluster at boot."),
            ("The Week 12 Terraform configuration creates three Ubuntu 26.04 EC2 instances",
             "The Week 12 Terraform configuration builds three Ubuntu 26.04 EC2 instances"),
            ("- Update the repo with git fetch and git reset --hard origin/master, then run terraform init and terraform apply.",
             "- Update the repo with git fetch and git reset --hard origin/master.\n- Run terraform init and terraform apply."),
            ("Copy the commands of each step from localMachine.sh, and run them on the master node.",
             "Copy the commands of each step from localMachine.sh. Run them on the master node."),
            ("- Create the LOG_LEVEL file, then create the app-config ConfigMap with --from-literal and --from-file.",
             "- Create the LOG_LEVEL file.\n- Create the app-config ConfigMap with --from-literal and --from-file."),
            ("- Create the DB_Password file, then create the app-secret Secret with --from-literal and --from-file.",
             "- Create the DB_Password file.\n- Create the app-secret Secret with --from-literal and --from-file."),
            ("- Apply config-env.yaml in the week12-dev namespace and wait until the Pod is Ready.",
             "- Apply config-env.yaml in the week12-dev namespace.\n- Run kubectl wait, and show that the Pod is Ready.")):
        assert text.count(old) == 1, old
        text = text.replace(old, new)
    old = "- From the Week12 directory on your own machine, run terraform destroy."
    assert text.count(old) == 1, old
    text = text.replace(old, "- Run terraform destroy in the Week12 directory on your own machine.")
    for pod in ("fortune-args", "config-env", "config-volume", "secret-pod"):
        old = "- Apply the manifest and wait until the %s Pod is Ready." % pod
        assert text.count(old) == 1, old
        text = text.replace(old, "- Apply the manifest.\n- Run kubectl wait, and show that the %s Pod is Ready." % pod)
    return D.destroy_section(
        text,
        "At the end of the lab, delete the Kubernetes objects and destroy all three EC2 instances.",
        ["- Run bash cleanup_lab12.sh on the master node, and show that both namespaces are deleted.",
         "- Explain why the deletion of a namespace deletes the Pods, ConfigMaps and Secrets in it."])


def step0_title(path):
    """The script header of Step 0 has the title of slide 3 (C2), at the same column for "(slide 3)"."""
    text = open(path, encoding="utf8").read()
    old = "# Step 0 - check the cluster                    (slide 3)"
    new = "# Step 0 - Build and check the cluster          (slide 3)"
    assert text.count(old) == 1 and len(old) == len(new)
    open(path, "w", encoding="utf8").write(text.replace(old, new))


def slide3(prs):
    """Slide 3: the two git lines of Step 0 of the script, and kubectl get nodes -o wide (review round 3)."""
    import copy
    slide = prs.slides[2]
    boxes = [sh for sh in slide.shapes if sh.has_text_frame]

    def one(text):
        hit = [sh for sh in boxes if sh.text_frame.text == text]
        assert len(hit) == 1, (text, len(hit))
        return hit[0]

    first = one(FIRST_OLD)
    left = [sh for sh in boxes if sh.left == first.left and sh.top > first.top]
    last = max(left, key=lambda sh: sh.top)
    assert last.text_frame.text == " "          # the empty last line of the panel goes, to make room
    last._element.getparent().remove(last._element)
    left.remove(last)
    step = int(0.25 * 914400)
    for sh in left:
        sh.top = sh.top + 2 * step
    anchor = first._element
    ids = [int(e.get("id")) for e in slide.shapes._spTree.iter() if e.tag.endswith("}cNvPr")]
    for k, text in enumerate((GIT_CLONE, GIT_RESET)):
        new = copy.deepcopy(first._element)
        cnv = [e for e in new.iter() if e.tag.endswith("}cNvPr")][0]
        cnv.set("id", str(max(ids) + 1 + k))       # a unique shape id, or PowerPoint repairs the file
        cnv.set("name", "TextBox %d" % (max(ids) + 1 + k))
        anchor.addnext(new)
        anchor = new
    added = [sh for sh in slide.shapes if sh._element in (first._element.getnext(), first._element.getnext().getnext())]
    for k, (sh, text) in enumerate(zip(added, (GIT_CLONE, GIT_RESET))):
        sh.top = first.top + (k + 1) * step
        runs = sh.text_frame.paragraphs[0].runs
        runs[0].text = text
        for r in runs[1:]:
            r.text = ""
    bottom = max(sh.top + sh.height for sh in left)
    panel = [sh for sh in slide.shapes if sh.shape_type == 1 and sh.left < first.left and sh.height > 914400 * 3]
    assert len(panel) == 1 and bottom < panel[0].top + panel[0].height, "the left panel is too short"
    for old, new in (("# ON THE MASTER - confirm the three nodes", MASTER),
                     (FIRST_OLD, FIRST),
                     ("Running Kubernetes cluster - kubeadm (3 nodes)", "A Kubernetes cluster with kubeadm (3 nodes)"),
                     ("Running Container image accessible by Kubernetes nodes",
                      "A container image that the Kubernetes nodes can pull"),
                     ("kubectl get nodes", "kubectl get nodes -o wide"),
                     ("$ kubectl get nodes", "$ kubectl get nodes -o wide"),
                     ("# Each node runs Ubuntu 26.04 and containerd 2.2.2.",
                      "# Other columns show Ubuntu 26.04 and containerd 2.2.2."),
                     # Round 5: full sentences; the right panel gets one more line in its empty slot.
                     ("# Three real nodes. No kind. No Docker in Docker.", "# Three real nodes form this cluster."),
                     ("# Other columns show Ubuntu 26.04 and containerd 2.2.2.",
                      "# It uses no kind and no Docker in Docker."),
                     (" ", "# Other columns show Ubuntu 26.04 and containerd 2.2.2.")):
        if old.startswith("Running"):
            old = old.replace("Running Container", "Container")
            boxes2 = [b for b in prs.slides[1].shapes if b.has_text_frame and b.text_frame.text == old]
            assert len(boxes2) == 1, len(boxes2)
            runs = boxes2[0].text_frame.paragraphs[0].runs
            runs[0].text = new
            for r in runs[1:]:
                r.text = ""
            continue
        right = 0 if old in ("# ON THE MASTER - confirm the three nodes", FIRST_OLD) else 8 * 914400
        sh = [b for b in boxes if b.text_frame.text == old and b.left > right]
        if old == " ":          # the empty slot under the line "# It uses no kind ..."
            above = [b for b in boxes if b.text_frame.text == "# It uses no kind and no Docker in Docker."][0]
            sh = [b for b in sh if b.top == above.top + int(0.25 * 914400)]
            green = above.text_frame.paragraphs[0].runs[0].font.color.rgb
            sh[0].text_frame.paragraphs[0].runs[0].font.color.rgb = green
        assert len(sh) == 1, (old, len(sh))
        runs = sh[0].text_frame.paragraphs[0].runs
        whole = "".join(r.text for r in runs)
        assert whole == old
        runs[-1].text = runs[-1].text + new[len(old):] if new.startswith(old) else runs[-1].text
        if not new.startswith(old):
            runs[0].text = new
            for r in runs[1:]:
                r.text = ""
        assert sh[0].text_frame.text == new, sh[0].text_frame.text


def repo_words(dst):
    """The A1 words of v6 in the repo files. The cleanup header and the cleanup block of master-init do
    not exist any more, so their two edits go."""
    edits = {
        "master-init.sh.tftpl": [
            ("# === Control-plane init. This is appended after bootstrap.sh and runs as root. ===",
             "# === Control-plane init. Terraform appends this to bootstrap.sh, and it runs as root. ==="),
            ('# when Flannel reconfigures the network. One failed kubectl under "set -e"\n'
             "# would kill this whole script, so the apply retries until it sticks.",
             '# when Flannel reconfigures the network. Under "set -e", one failed kubectl\n'
             "# command can stop this whole script, so the script tries the apply again until it works."),
            ("  You are on the CONTROL PLANE node. kubectl is ready.", "  You are on the MASTER node. kubectl is ready."),
            ('echo "Flannel apply failed; retrying in 10s..."', 'echo "The Flannel apply failed. The script tries the apply again in 10 seconds."'),
            ("  The two workers join by themselves. Give them a few minutes.",
             "  The two workers join the cluster at boot. Wait until all three nodes are Ready."),
            ("# The API server drops connections for a moment right after init, and again",
             "# The API server drops connections for a short time after init, and again"),
            ("# kubeconfig for the ubuntu user, so kubectl works right after you SSH in.",
             "# Give the ubuntu user a kubeconfig, so kubectl works when you connect with SSH."),
            ("# Flannel v0.28.10 (Apache License 2.0). The images are copies on the maziar account.",
             "# This manifest installs Flannel v0.28.10 (Apache License 2.0). The images are copies on the maziar account."),
            ("# Label the workers as they join. This runs in the background, so cloud-init\n"
             "# is not blocked while it waits.",
             "# Label the workers as they join. This runs in the background, so cloud-init\n"
             "# continues while it waits."),
        ],
        "bootstrap.sh": [
            ("# 1. Turn swap off. kubelet refuses to start while swap is on.",
             "# 1. Stop swap. The kubelet does not start while swap is on."),
            ("#    8951-byte overlay. A NodePort reply bigger than 1500 bytes is dropped on\n"
             "#    the way to a browser on the internet, so the page never loads while the\n"
             "#    headers arrive fine. 1500 here makes Flannel compute 1450.",
             "#    8951-byte overlay. The internet path drops a NodePort reply bigger than\n"
             "#    1500 bytes, so a browser gets the headers but never the page. With 1500\n"
             "#    here, Flannel uses 1450."),
            ("# 3. Kernel modules and sysctls for the pod network.", "# 3. Kernel modules and sysctls for the Pod network."),
            ('echo "Prerequisites installed."', 'echo "bootstrap.sh installed the prerequisites."'),
        ],
        "variables.tf": [("The AWS Academy Learner Lab ships one called LabInstanceProfile (LabRole); the Learner Lab "
                          "forbids creating IAM roles but allows passing this one.",
                          "The AWS Academy Learner Lab has the profile LabInstanceProfile (LabRole). The Learner Lab "
                          "blocks the creation of IAM roles, but it allows this profile."),
                         ("in the Learner Lab). Used for SSH.", "in the Learner Lab). SSH uses this key pair."),
                         ('description = "Name of YOUR EC2 key pair', 'description = "Enter the name of YOUR EC2 key pair'),
                         ("IAM instance profile attached to the node.",
                          "Terraform attaches this IAM instance profile to each node.")],
        ".gitignore": [("# Keys / secrets — never commit these", "# Keys and secrets: never commit these")],
        "main.tf": [('description = "Week12 Kubernetes control-plane node"', 'description = "Week12 Kubernetes master node"'),
                    ("  # kubeadm bootstrap token, shared by the master (--token) and the workers\n"
                     "  # (--token). The workers join without copying anything from the master.",
                     "  # The master (--token) and the workers (--token) share this kubeadm\n"
                     "  # bootstrap token. The workers copy nothing from the master to join."),
                    ("# Latest Ubuntu 26.04 LTS (Resolute Raccoon), x86_64, from Canonical.",
                     "# The lab uses the latest Ubuntu 26.04 LTS AMI (Resolute Raccoon, amd64) from Canonical."),
                    ("# Default VPC. The Learner Lab does not permit a new VPC.",
                     "# The lab uses the default VPC. Terraform builds no VPC and no subnet."),
                    ("  # m5.large: 2 vCPU / 8 GB. The Learner Lab blocks xlarge and larger, and it\n"
                     "  # stops newer generations such as r6i a few seconds after launch.\n",
                     "  # m5.large has 2 vCPU and 8 GiB of memory. The Learner Lab blocks the xlarge size and each larger size.\n"),
                    ("# This covers every component port without listing each one:",
                     "# These rules open each component port. The ports are:"),
                    ("# Flannel. Each worker retries kubeadm join until the API answers.",
                     "# Flannel. Each worker tries kubeadm join again until the control plane answers."),
                    ("#   API 6443 node to node, Flannel VXLAN 8472/UDP.", "#   API server 6443 node to node, Flannel VXLAN 8472/UDP."),
                    ("# command of this lab runs on the master, and the workers reach the API\n"
                     "# through the node-to-node rules above. The bootstrap token is in a public\n"
                     "# repository, so the API must not answer outside the cluster.",
                     "# command of this lab runs on the master, and the workers reach the API server\n"
                     "# through the node-to-node rules above. The bootstrap token is in a public\n"
                     "# repo, so the API server must not answer outside the cluster."),
                    ("# A NodePort Service opens its port on EVERY node, so open the range on both.",
                     "# A NodePort Service opens its port on EVERY node, so the two rules below open the NodePort range\n"
                     "# in both security groups."),
                    ('# Format: 6 chars "." 16 chars, lowercase letters and digits. Lab only.',
                     '# The token has 6 characters, ".", then 16 characters (lowercase letters and digits). Use it only in the lab.')],
        "worker-join.sh.tftpl": [
            ("# === Worker join. This is appended after bootstrap.sh and runs as root. ===",
             "# === Worker join. Terraform appends this to bootstrap.sh, and it runs as root. ==="),
            ("# Retry until the control plane answers. The master may still be running\n# kubeadm init when this node is ready.",
             "# Try kubeadm join again until the control plane answers. The master can\n# still run kubeadm init when this node starts kubeadm join."),
            ('echo "Control plane not reachable yet; retrying in 15s..."',
             'echo "The control plane does not answer. This node tries kubeadm join again in 15 seconds."')],
    }
    for name, pairs in edits.items():
        path = os.path.join(dst, name)
        text = open(path, encoding="utf8").read()
        for old, new in pairs:
            assert text.count(old) == 1, (name, old[:50])
            text = text.replace(old, new)
        open(path, "w", encoding="utf8").write(text)


if __name__ == "__main__":
    for out in (OUT, SCRIPT, BLACKBOARD):
        if os.path.exists(out) and "--force" not in sys.argv:
            sys.exit("%s exists. Bump the version; never overwrite a delivered file." % out)
    L.check_lines(SLIDES)
    text = blackboard_text()
    L.make_lab("12", SLIDES, OUT, SCRIPT_HEAD, step0=STEP0, script_path=SCRIPT,
               prereq_title="Lab Week 12 - Prerequisites", node_version="v1.35.10", cluster_edits=v6.CLUSTER_EDITS)
    prs = Presentation(OUT)
    v6.kubernetes_not_k8s(prs)
    v6.cluster_comment_color(prs)
    slide3(prs)
    finish(prs, "CLO835 Week 12 Lab: ConfigMaps and Secrets")
    prs.save(OUT)
    step0_title(SCRIPT)
    if "--no-repo" not in sys.argv:
        dst, files = L.make_repo_folder("12", "ConfigMaps and Secrets", None, SCRIPT, lab_label="Lab Week 12")
        v6.own_flannel(dst)
        repo_words(dst)
        low = "".join(open(os.path.join(dst, f), encoding="utf8").read().lower() for f in os.listdir(dst)
                      if os.path.isfile(os.path.join(dst, f)))
        assert "cleanup" not in low, "cleanup text is left in the repo folder"
        print("repo folder : %s (%d files)" % (dst, len(files)))
    open(BLACKBOARD, "w", encoding="utf8").write(text)
    print("blackboard  : %s" % BLACKBOARD)
