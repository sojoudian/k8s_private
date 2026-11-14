# -*- coding: utf-8 -*-
"""CLO835 Week 10 lab v5 - lab v4 with no cleanup script (the user, 2026-11-11).

terraform destroy removes the three machines and every object and file of the lab, so:
- Step 6 is "Destroy the cluster": only terraform destroy on your own machine (38 master commands).
- The repo folder has 7 files: no cleanup_lab10.sh, and master-init writes no cleanup file.
- The Blackboard text v5: section 7 asks only for terraform destroy.
All other content is v4 (imported, not copied).

Outputs: Week10/Lab_week10_v5.pptx, Week10/localMachine_v5.sh,
Week10/Lab_week10_Blackboard_Submission_v5.md, ~/Documents/c/r/CLO835_Fall_2026/Week10/
Run from the project root. It is guarded, so importing it writes nothing.
It refuses to overwrite an output, unless you give --force. --no-repo skips the repo folder.
"""
import os
import sys

from pptx import Presentation

import build_week10_lab_v4 as v4
import lab_destroy_only as D
import lab_kubeadm as L
from build_week12_lecture_v6 import finish

VERSION = "v5"
DECK = "Week10/Lab_week10_%s.pptx" % VERSION
SCRIPT = "Week10/localMachine_%s.sh" % VERSION
BLACKBOARD = "Week10/Lab_week10_Blackboard_Submission_%s.md" % VERSION

SLIDES = D.destroy_step(v4.SLIDES)
assert v4.SCRIPT_HEAD.count("Lab_week10_v4.pptx") == 1
SCRIPT_HEAD = v4.SCRIPT_HEAD.replace("Lab_week10_v4.pptx", "Lab_week10_%s.pptx" % VERSION)

BLACKBOARD_TEXT = D.destroy_section(
    v4.BLACKBOARD_TEXT,
    "At the end of the lab, remove the Kubernetes objects and destroy all three EC2 instances.",
    ["- Run bash cleanup_lab10.sh on the control-plane node.",
     "- Run kubectl get pods,pvc,pv and show that nothing is left.",
     "- Explain why the clean-up deletes the claims before it deletes the provisioner."])


if __name__ == "__main__":
    for out in (DECK, SCRIPT, BLACKBOARD):
        if os.path.exists(out) and "--force" not in sys.argv:
            sys.exit("%s exists. Bump the version; never overwrite a delivered file." % out)
    L.check_lines(SLIDES)
    L.make_lab("10", SLIDES, DECK, SCRIPT_HEAD, script_path=SCRIPT,
               prereq_title="Lab Week 10 - Prerequisites", node_version=v4.NODE_VERSION)
    deck = Presentation(DECK)
    finish(deck, "CLO835 Week 10 Lab: Persistent Storage and StatefulSets")
    for slide in deck.slides:                   # one word for one meaning: Kubernetes, not K8s
        for sh in slide.shapes:
            if sh.has_text_frame:
                for p in sh.text_frame.paragraphs:
                    for r in p.runs:
                        r.text = r.text.replace("K8s", "Kubernetes")
    deck.save(DECK)
    if "--no-repo" not in sys.argv:
        dst, files = L.make_repo_folder("10", "PersistentVolumes, StorageClasses and StatefulSets", None,
                                        SCRIPT, master_extra=v4.master_extra(), lab_label="Lab Week 10")
        old_file = os.path.join(dst, v4.SC_FILE)
        if os.path.exists(old_file):
            os.remove(old_file)
        print("repo folder : %s (%d files)" % (dst, len(files)))
    open(BLACKBOARD, "w", encoding="utf8").write(BLACKBOARD_TEXT)
    print("blackboard  : %s" % BLACKBOARD)
