# -*- coding: utf-8 -*-
"""CLO835 Week 06 lab v5 - lab v4 with no cleanup script (the user, 2026-11-11).

terraform destroy removes the three machines and every object and file of the lab, so:
- Step 6 is "Destroy the cluster": only terraform destroy on your own machine.
- The repo folder Week06 (also the template of the other weeks) has no cleanup_lab06.sh,
  and its master-init writes no cleanup file. lab_kubeadm.make_repo_folder() accepts a template
  with or without that block.
- The Blackboard text v6 comes from v5 (the long form of Lab04): section 7 asks only for
  terraform destroy.
All other content is v4 (imported, not copied).

Outputs: Week06/Lab_week06_v5.pptx, Week06/localMachine_v5.sh,
Week06/Lab_week06_Blackboard_Submission_v6.md, ~/Documents/c/r/CLO835_Fall_2026/Week06/
Run from the project root. It is guarded, so importing it writes nothing.
It refuses to overwrite an output, unless you give --force. --no-repo skips the repo folder.
"""
import os
import sys

import build_week06_lab_v4 as v4
import lab_destroy_only as D
import lab_kubeadm as L

VERSION = "v5"
DECK = "Week06/Lab_week06_%s.pptx" % VERSION
SCRIPT = "Week06/localMachine_%s.sh" % VERSION
BLACKBOARD_SRC = "Week06/Lab_week06_Blackboard_Submission_v5.md"
BLACKBOARD = "Week06/Lab_week06_Blackboard_Submission_v6.md"

SLIDES = D.destroy_step(v4.SLIDES)


def blackboard_text():
    return D.destroy_section(
        open(BLACKBOARD_SRC, encoding="utf8").read(),
        "At the end of the lab, remove the Kubernetes objects and destroy all three EC2 instances.",
        ["- Run bash cleanup_lab06.sh on the control-plane node.",
         "- Run kubectl get all | grep -E 'kubia|client' and show that nothing is left."])


if __name__ == "__main__":
    for out in (DECK, SCRIPT, BLACKBOARD):
        if os.path.exists(out) and "--force" not in sys.argv:
            sys.exit("%s exists. Bump the version; never overwrite a delivered file." % out)
    L.check_lines(SLIDES)
    text = blackboard_text()
    L.make_lab("06", SLIDES, DECK, v4.SCRIPT_HEAD, script_path=SCRIPT)
    if "--no-repo" not in sys.argv:
        dst, files = L.make_repo_folder("06", "Rollouts, Labels and Services", None, SCRIPT)
        print("repo folder : %s (%d files)" % (dst, len(files)))
    open(BLACKBOARD, "w", encoding="utf8").write(text)
    print("blackboard  : %s" % BLACKBOARD)
