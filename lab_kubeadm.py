# -*- coding: utf-8 -*-
"""CLO835 - shared helpers for the labs on the kubeadm cluster (Weeks 07 to 14).

Two jobs:
1. make_lab()  builds a lab deck AND its localMachine.sh from ONE slide list, with
   the engine of build_week06_lab_v3.py (the design of the Week 05 and 06 labs).
2. make_repo_folder()  writes the 8-file folder of the course repository from the
   tested Week 06 folder: .gitignore, bootstrap.sh, cleanup_labNN.sh,
   localMachine.sh, main.tf, master-init.sh.tftpl, variables.tf,
   worker-join.sh.tftpl. Only the week name, the token, the message of the day,
   the cleanup script and the extras of the week change.

It is guarded, so importing it writes nothing.
"""
import os
import re
import subprocess

import build_week06_lab_v3 as eng

FILE_MARK = eng.FILE_MARK
REPO = os.path.expanduser("~/Documents/c/r/CLO835_Fall_2026")
TEMPLATE = os.path.join(REPO, "Week06")
MIRRORS = "https://raw.githubusercontent.com/sojoudian/clo835-mirrors/main/"
# v2: the course repository holds the extra manifests of a week, so a lab needs
# no other repository. The template is read from git HEAD, so the Week06 folder
# itself can be rebuilt.
RAW = "https://raw.githubusercontent.com/sojoudian/CLO835_Fall_2026/master/"


def _template(f):
    return subprocess.check_output(["git", "-C", REPO, "show", "HEAD:Week06/" + f]).decode("utf8")


def make_lab(nn, slides, out, script_head, step0=None, script_path=None, prereq_title=None,
             node_version="v1.35.9", cluster_edits=None):
    """nn: the week number as text, e.g. "07". Builds the deck; writes the script.

    cluster_edits (optional, 2026-11-10): more replacements for the cluster slide, applied after the
    default ones (a value replaces the default value of the same key). With no value, nothing changes."""
    eng.PREREQ_TITLE = prereq_title or "Lab %d - Prerequisites" % int(nn)
    eng.CLUSTER_EDITS = {
        # A clone from an earlier week has no folder for this week: pull first.
        "# ON YOUR MACHINE - build 1 master + 2 workers": "# ON YOUR MACHINE - pull the repo, build 1 master + 2 workers",
        "$ cd week5_code": "$ cd CLO835_Fall_2026 && git pull && cd Week%s" % nn,
        "# NodePort 30000-32767 is open on both workers.": "# NodePort 30000-32767 is open on all three nodes.",
        # The version that the live test of 2026-10-27 installed.
        "masternode    Ready    control-plane   4m    v1.35.0": "masternode    Ready    control-plane   4m    " + node_version,
        "workernode1   Ready    worker          3m    v1.35.0": "workernode1   Ready    worker          3m    " + node_version,
        "workernode2   Ready    worker          3m    v1.35.0": "workernode2   Ready    worker          3m    " + node_version,
    }
    if cluster_edits:
        eng.CLUSTER_EDITS.update(cluster_edits)
    # terraform destroy asks for key_name as well, because the variable has no default.
    slides = [item[:3] + ([l.replace("L$ terraform destroy", "L$ terraform destroy          # asks for key_name again")
                            if l == "L$ terraform destroy" else l for l in item[3]],) + item[4:]
              if item[0] in ("step", "step2") else item for item in slides]
    eng.SLIDES = slides
    eng.SCRIPT_HEAD = script_head
    if step0 is not None:
        eng.STEP0 = step0
    total = eng.build(out)
    if script_path:
        eng.write_script(script_path)
    return total


def _sub(text, old, new, count=1):
    if text.count(old) != count:
        raise SystemExit("template changed: %r found %d times" % (old[:50], text.count(old)))
    return text.replace(old, new)


def make_repo_folder(nn, topic, cleanup_body, script_src, extra_packages="", master_extra="", extra_files=None,
                     lab_label=None):
    """Write CLO835_Fall_2026/WeekNN from the Week 06 folder.

    cleanup_body  : the lines of cleanup_labNN.sh after its header, or None (2026-11-10): then the
                    folder has no cleanup script and the master gets none, because terraform destroy
                    removes the three machines. The folder then has 7 files.
    script_src    : the localMachine.sh that make_lab() wrote
    extra_packages: apt packages that every node needs (added to bootstrap.sh)
    master_extra  : shell lines for the master, run before the cleanup file is
                    written. A Terraform template: write $${ for a literal ${.
    lab_label     : the lab name in the cleanup header (default "Lab N")
    """
    dst = os.path.join(REPO, "Week%s" % nn)
    os.makedirs(dst, exist_ok=True)
    read = _template
    week = "Week %s" % nn
    title = "CLO835 - %s - %s" % (week, topic)
    rule = "-" * len(title)

    main = read("main.tf")
    main = _sub(main, 'k8s_token = "week06.0123456789abcdef"', 'k8s_token = "week%s.0123456789abcdef"' % nn)
    main = _sub(main, "week06-k8s-", "week%s-k8s-" % nn, 4)
    main = _sub(main, "Week06 Kubernetes", "Week%s Kubernetes" % nn, 2)

    boot = read("bootstrap.sh")
    boot = _sub(boot, "# CLO835 Week 06 - kubeadm node prerequisites.", "# CLO835 %s - kubeadm node prerequisites." % week)
    if extra_packages:
        boot = _sub(boot, "conntrack socat ethtool\n", "conntrack socat ethtool %s\n" % extra_packages)

    cleanup = None
    if cleanup_body is not None:
        cleanup = ("#!/bin/bash\n"
                   "# CLO835 - %s - remove everything the lab creates inside the cluster.\n"
                   "# The three machines are removed by \"terraform destroy\" on your own laptop.\n"
                   "set -uo pipefail\n\n" % (lab_label or "Lab %d" % int(nn))) + cleanup_body.strip("\n") + "\n\necho \"done\"\n"
        if "${" in cleanup or "%{" in cleanup:
            raise SystemExit("the cleanup script must not hold ${ or %{ (Terraform template)")

    master = read("master-init.sh.tftpl")
    # kubectl config set-credentials / set-context / use-context write a lock file
    # next to the config, so ubuntu must own the whole folder (live test, Week 13).
    # Week06 HEAD has this line since commit 1783b12, so the change can be a no-op.
    master = master.replace("chown ubuntu:ubuntu /home/ubuntu/.kube/config\n",
                            "chown -R ubuntu:ubuntu /home/ubuntu/.kube\n")
    old_block = "# The last step of localMachine.sh calls ./cleanup_lab06.sh."
    if old_block in master:          # the template still writes cleanup_lab06.sh: replace that block
        start = master.index(old_block)
        end = master.index("chown ubuntu:ubuntu /home/ubuntu/cleanup_lab06.sh\n") + len(
            "chown ubuntu:ubuntu /home/ubuntu/cleanup_lab06.sh\n")
    else:                            # a template with no cleanup block: the block goes before the motd
        start = end = master.index("cat > /etc/motd <<'MOTD'\n")
    parts = []
    if master_extra:
        parts.append(master_extra.strip("\n") + "\n")
    if cleanup is not None:
        parts.append(("# The last step of localMachine.sh calls ./cleanup_lab%s.sh. The student runs\n"
                      "# terraform on their own laptop, so that file never reaches this node. Write it\n"
                      "# here, so the last step of the lab works with no copying.\n"
                      "cat > /home/ubuntu/cleanup_lab%s.sh <<'CLEANUP'\n%sCLEANUP\n"
                      "chmod +x /home/ubuntu/cleanup_lab%s.sh\n"
                      "chown ubuntu:ubuntu /home/ubuntu/cleanup_lab%s.sh\n") % (nn, nn, cleanup, nn, nn))
    block = "\n".join(parts)
    if start == end:                 # keep one empty line between the block and the motd
        block = block + "\n" if block else ""
    elif not block and master[end:end + 1] == "\n":
        end += 1                     # no block: do not leave two empty lines
    master = master[:start] + block + master[end:]
    master = _sub(master, "  CLO835 - Week 06 - Rollouts, Labels and Services\n"
                          "  ------------------------------------------------\n",
                  "  %s\n  %s\n" % (title, rule))

    worker = read("worker-join.sh.tftpl")
    worker = _sub(worker, "  CLO835 - Week 06 - Rollouts, Labels and Services\n"
                          "  ------------------------------------------------\n",
                  "  %s\n  %s\n" % (title, rule))

    files = {
        ".gitignore": read(".gitignore"),
        "bootstrap.sh": boot,
        "localMachine.sh": open(script_src, encoding="utf8").read(),
        "main.tf": main,
        "master-init.sh.tftpl": master,
        "variables.tf": read("variables.tf"),
        "worker-join.sh.tftpl": worker,
    }
    if cleanup is not None:
        files["cleanup_lab%s.sh" % nn] = cleanup
    else:                            # no cleanup script: remove an old copy from the folder
        old = os.path.join(dst, "cleanup_lab%s.sh" % nn)
        if os.path.exists(old):
            os.remove(old)
    files.update(extra_files or {})
    for name, text in files.items():
        path = os.path.join(dst, name)
        open(path, "w", encoding="utf8").write(text)
        if name.endswith(".sh"):
            # bootstrap.sh keeps the mode of the template (git 100644); Terraform only reads it.
            os.chmod(path, 0o644 if name == "bootstrap.sh" else 0o755)
    return dst, sorted(files)


def blackboard_text(nn, intro, sections, out):
    """The Blackboard submission text, in the form of Lab_week06_Blackboard_Submission."""
    lines = ["# Lab Week %s Submission" % nn, "",
             "Please submit a report that demonstrates all the main points of Lab Week %s." % nn,
             "The lab recording demonstrates every step required for this assignment. You may watch "
             "the recording and follow it directly, step by step, to complete the lab. Make sure your "
             "submission includes your own screenshots, command outputs, and explanations as described below.",
             ""]
    if intro:
        lines += [intro, ""]
    for k, (title, text, musts) in enumerate(sections, 1):
        lines += ["## %d. %s" % (k, title), "", text, "You must:"]
        lines += ["- " + m for m in musts]
        lines.append("")
    lines += ["## Submission should include", "",
              "- Name label on every screenshot",
              "- Detailed explanation of commands being executed",
              "- Highlight the output of commands executed", "",
              "## Integrity Pledge", "",
              "By submitting this assignment you affirm that you will not plagiarize, give or receive "
              "illegitimate help on assignments, papers or examinations. You will uphold fairness and honesty "
              "in your work and the work of others. Please read Seneca Academic Integrity policy for more details."]
    open(out, "w", encoding="utf8").write("\n".join(lines) + "\n")


def check_lines(slides):
    """Refuse a non-ASCII character in any command line or file line."""
    bad = []
    for item in slides:
        groups = []
        if item[0] in ("step", "step2"):
            groups.append(item[3])
        if item[0] == "step2":
            groups.append(item[6])
        for g in groups:
            for l in g:
                if l == FILE_MARK:
                    continue
                if re.search(r"[^\x00-\x7f]", l):
                    bad.append(l)
    if bad:
        raise SystemExit("non-ASCII in a command line: %r" % bad[:3])
