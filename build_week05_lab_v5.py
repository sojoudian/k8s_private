# -*- coding: utf-8 -*-
"""CLO835 Week 05 lab v5 - lab v4 with no cleanup script (the user, 2026-11-11).

terraform destroy removes the three machines and every object and file of the lab, so:
- Deck: slide 17 "Clean up" becomes "Destroy the cluster". Its terminal keeps only the lines of
  your own machine (terraform destroy). Every other slide is v4, byte for byte.
- Blackboard text v2: section 10 has no cleanup item.
- Course repository Week05 (not written by a builder before): localMachine.sh Step 13 holds only
  terraform destroy, master-init writes no cleanup file, and cleanup_lab05.sh is deleted.

Inputs : Week05/Lab_week05_v4.pptx, Week05/Lab_week05_Blackboard_Submission.md (never written)
Outputs: Week05/Lab_week05_v5.pptx, Week05/Lab_week05_Blackboard_Submission_v2.md,
         ~/Documents/c/r/CLO835_Fall_2026/Week05/
Run from the project root. It is guarded, so importing it writes nothing.
It refuses to overwrite an output, unless you give --force. --no-repo skips the repo folder.
"""
import copy
import os
import sys

from pptx import Presentation

import lab_destroy_only as D
import lab_kubeadm as L

VERSION = "v5"
SRC = "Week05/Lab_week05_v4.pptx"
DECK = "Week05/Lab_week05_%s.pptx" % VERSION
BB_SRC = "Week05/Lab_week05_Blackboard_Submission.md"
BB = "Week05/Lab_week05_Blackboard_Submission_v2.md"
REPO_WEEK = os.path.join(L.REPO, "Week05")

MASTER_LINES = ["# ON THE MASTER - remove the Kubernetes objects.", "$ bash cleanup_lab05.sh", " ",
                "# Confirm that nothing is left.",
                "$ kubectl get all --all-namespaces | grep -E 'nginx|kubia|pingpong'", " "]
OWN = "# ON YOUR OWN MACHINE - remove the three EC2 machines."

SCRIPT_OLD = ("# Step 13 - clean up                            (slide 17)\n"
              "########################################################\n"
              "./cleanup_lab05.sh\n")
SCRIPT_NEW = ("# Step 13 - Destroy the cluster                 (slide 17)\n"
              "########################################################\n"
              "%s\n%s\n"
              "# ON YOUR OWN MACHINE:  terraform destroy\n"
              "#\n"
              "# Always destroy. The Learner Lab budget is small.\n") % (OWN, D.ALSO)
BLOCK_START = "# Step 13 of localMachine.sh calls ./cleanup_lab05.sh."
BLOCK_END = "chown ubuntu:ubuntu /home/ubuntu/cleanup_lab05.sh\n\n"
BB_ITEM = "- Run ./cleanup_lab05.sh on the control-plane machine, and show the cluster is empty.\n"


def deck():
    prs = Presentation(SRC)
    slide = prs.slides[16]
    shapes = {sh.name: sh for sh in slide.shapes}
    title = shapes["TextBox 1"].text_frame.paragraphs[0].runs[0]
    assert title.text == "Clean up", title.text
    title.text = D.TITLE
    body = shapes["TextBox 8"].text_frame
    paras = list(body.paragraphs)
    assert [p.text for p in paras[:len(MASTER_LINES)]] == MASTER_LINES, [p.text for p in paras]
    assert paras[len(MASTER_LINES)].text == OWN
    for p in paras[:len(MASTER_LINES)]:
        p._p.getparent().remove(p._p)
    own = paras[len(MASTER_LINES)]._p
    also = copy.deepcopy(own)
    own.addnext(also)
    runs = also.findall("{http://schemas.openxmlformats.org/drawingml/2006/main}r")
    assert len(runs) == 1
    runs[0].find("{http://schemas.openxmlformats.org/drawingml/2006/main}t").text = D.ALSO
    lines = [p.text for p in body.paragraphs]
    assert not any("clean" in l.lower() for l in lines) and "$ terraform destroy" in lines, lines
    prs.save(DECK)
    return lines


def blackboard():
    text = open(BB_SRC, encoding="utf8").read()
    assert text.count(BB_ITEM) == 1
    text = text.replace(BB_ITEM, "")
    assert "cleanup" not in text.lower()
    open(BB, "w", encoding="utf8").write(text)


def repo():
    path = os.path.join(REPO_WEEK, "localMachine.sh")
    text = open(path, encoding="utf8").read()
    assert text.count(SCRIPT_OLD) == 1 and text.endswith(SCRIPT_OLD)
    open(path, "w", encoding="utf8").write(text.replace(SCRIPT_OLD, SCRIPT_NEW))
    path = os.path.join(REPO_WEEK, "master-init.sh.tftpl")
    text = open(path, encoding="utf8").read()
    assert text.count(BLOCK_START) == 1 and text.count(BLOCK_END) == 1
    start, end = text.index(BLOCK_START), text.index(BLOCK_END) + len(BLOCK_END)
    text = text[:start] + text[end:]
    assert "cleanup" not in text
    open(path, "w", encoding="utf8").write(text)
    old = os.path.join(REPO_WEEK, "cleanup_lab05.sh")
    if os.path.exists(old):
        os.remove(old)


if __name__ == "__main__":
    for out in (DECK, BB):
        if os.path.exists(out) and "--force" not in sys.argv:
            sys.exit("%s exists. Bump the version; never overwrite a delivered file." % out)
    print("deck        : %s, slide 17: %s" % (DECK, " | ".join(deck())))
    blackboard()
    print("blackboard  : %s" % BB)
    if "--no-repo" not in sys.argv:
        repo()
        print("repo folder : %s (%d files)" % (REPO_WEEK, len(os.listdir(REPO_WEEK))))
