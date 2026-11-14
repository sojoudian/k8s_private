# -*- coding: utf-8 -*-
"""CLO835 Week 13 lab v4 - lab v3 with no cleanup script (the user, 2026-11-11).

terraform destroy removes the three machines, the kubeconfig entry of dev-user and every
object and file of the lab, so:
- Step 6 is "Destroy the cluster": only terraform destroy on your own machine.
- The repo folder has no cleanup_lab13.sh, and master-init writes no cleanup file. Of the wording
  fixes of v3, only the message of the day stays: the other three were in the cleanup text.
- The Blackboard text v4 comes from v3: section 7 has no cleanup items.
All other content is v3 (imported, not copied).

Outputs: week13/Lab_week13_v4.pptx, week13/localMachine_v4.sh,
week13/Lab_week13_Blackboard_Submission_v4.md, ~/Documents/c/r/CLO835_Fall_2026/Week13/
Run from the project root. It is guarded, so importing it writes nothing.
It refuses to overwrite an output, unless you give --force. --no-repo skips the repo folder.
"""
import os
import sys

from pptx import Presentation
from pptx.util import Inches

import build_week13_lab_v3 as v3
import lab_destroy_only as D
import lab_kubeadm as L
from build_week12_lab_v5 import own_flannel
from build_week12_lecture_v6 import finish

VERSION = "v4"
OUT = "week13/Lab_week13_%s.pptx" % VERSION
SCRIPT = "week13/localMachine_%s.sh" % VERSION
BLACKBOARD_SRC = "week13/Lab_week13_Blackboard_Submission_v3.md"
BLACKBOARD = "week13/Lab_week13_Blackboard_Submission_v4.md"

SLIDES = D.destroy_step(v3.SLIDES)


def blackboard_text():
    return D.destroy_section(
        open(BLACKBOARD_SRC, encoding="utf8").read(),
        "At the end of the lab, delete the Kubernetes objects and destroy all three EC2 instances.",
        ["- Run bash cleanup_lab13.sh on the master node, and show that only the kubernetes-admin context is left.",
         "- Explain why the deletion of the week13 namespace does not delete the CSR, the ClusterRole and "
         "the ClusterRoleBinding."])


def own_wording(dst):
    """The message of the day of the master says MASTER, as in v3."""
    path = os.path.join(dst, "master-init.sh.tftpl")
    text = open(path, encoding="utf8").read()
    old, new = "You are on the CONTROL PLANE node. kubectl is ready.", "You are on the MASTER node. kubectl is ready."
    assert text.count(old) == 1, text.count(old)
    open(path, "w", encoding="utf8").write(text.replace(old, new))


if __name__ == "__main__":
    for out in (OUT, SCRIPT, BLACKBOARD):
        if os.path.exists(out) and "--force" not in sys.argv:
            sys.exit("%s exists. Bump the version; never overwrite a delivered file." % out)
    L.check_lines(SLIDES)
    text = blackboard_text()
    L.make_lab("13", SLIDES, OUT, v3.SCRIPT_HEAD, script_path=SCRIPT, prereq_title="Lab Week 13 - Prerequisites",
               node_version="v1.35.10")
    prs = Presentation(OUT)
    # One name for the computer of the student, as on the last step slide.
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
        dst, files = L.make_repo_folder("13", "Authentication and RBAC", None, SCRIPT, lab_label="Lab Week 13")
        own_flannel(dst)
        own_wording(dst)
        print("repo folder : %s (%d files)" % (dst, len(files)))
    open(BLACKBOARD, "w", encoding="utf8").write(text)
    print("blackboard  : %s" % BLACKBOARD)
