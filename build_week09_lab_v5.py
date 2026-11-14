# -*- coding: utf-8 -*-
"""CLO835 Week 09 lab v5 - lab v4 with no cleanup script (the user, 2026-11-11).

terraform destroy removes the three machines and every object and file of the lab, so:
- Step 6 is "Destroy the cluster": terraform state list and terraform destroy on your own machine.
- The repo folder has no cleanup_lab09.sh, and master-init writes no cleanup file.
- The Blackboard text v5 comes from v4: section 7 has no cleanup items.
All other content is v4 (imported, not copied).

Outputs: Week09/Lab_week09_v5.pptx, Week09/localMachine_v5.sh,
Week09/Lab_week09_Blackboard_Submission_v5.md, ~/Documents/c/r/CLO835_Fall_2026/Week09/
Run from the project root. It is guarded, so importing it writes nothing.
It refuses to overwrite an output, unless you give --force. --no-repo skips the repo folder.
"""
import os
import sys

import build_week09_lab_v4 as v4
import lab_destroy_only as D
import lab_kubeadm as L

VERSION = "v5"
DECK = "Week09/Lab_week09_%s.pptx" % VERSION
SCRIPT = "Week09/localMachine_%s.sh" % VERSION
BLACKBOARD_SRC = "Week09/Lab_week09_Blackboard_Submission_v4.md"
BLACKBOARD = "Week09/Lab_week09_Blackboard_Submission_v5.md"

SLIDES = D.destroy_step(v4.SLIDES)


def blackboard_text():
    return D.destroy_section(
        open(BLACKBOARD_SRC, encoding="utf8").read(),
        "At the end of the lab, remove the Kubernetes objects and destroy all three EC2 instances.",
        ["- Run bash cleanup_lab09.sh on the control-plane node.",
         "- Run kubectl get pods,deployments | grep -E 'kubia|no-scheduler' and show that nothing is left."])


if __name__ == "__main__":
    for out in (DECK, SCRIPT, BLACKBOARD):
        if os.path.exists(out) and "--force" not in sys.argv:
            sys.exit("%s exists. Bump the version; never overwrite a delivered file." % out)
    L.check_lines(SLIDES)
    text = blackboard_text()
    L.make_lab("09", SLIDES, DECK, v4.SCRIPT_HEAD, script_path=SCRIPT,
               prereq_title="Lab Week 09 - Prerequisites", node_version="v1.35.10")
    if "--no-repo" not in sys.argv:
        dst, files = L.make_repo_folder("09", "Managed vs Self-managed Kubernetes", None, SCRIPT,
                                        lab_label="Lab Week 09")
        print("repo folder : %s (%d files)" % (dst, len(files)))
    open(BLACKBOARD, "w", encoding="utf8").write(text)
    print("blackboard  : %s" % BLACKBOARD)
