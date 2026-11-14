# -*- coding: utf-8 -*-
"""CLO835 Week 07 lab v4 - lab v3 with no cleanup script (the user, 2026-11-11).

terraform destroy removes the three machines and every object and file of the lab, so:
- Step 6 is "Destroy the cluster": only terraform destroy on your own machine.
- The repo folder has no cleanup_lab07.sh, and master-init writes no cleanup file.
- The Blackboard text v4: section 7 asks only for terraform destroy.
All other content is v3 (imported, not copied).

Outputs: Week07/Lab_week07_v4.pptx, Week07/localMachine_v4.sh,
Week07/Lab_week07_Blackboard_Submission_v4.md, ~/Documents/c/r/CLO835_Fall_2026/Week07/
Run from the project root. It is guarded, so importing it writes nothing.
It refuses to overwrite an output, unless you give --force. --no-repo skips the repo folder.
"""
import os
import sys

from pptx import Presentation

import build_week07_lab_v3 as v3
import lab_destroy_only as D
import lab_kubeadm as L
from build_week12_lecture_v6 import finish

VERSION = "v4"
DECK = "Week07/Lab_week07_%s.pptx" % VERSION
SCRIPT = "Week07/localMachine_%s.sh" % VERSION
BLACKBOARD = "Week07/Lab_week07_Blackboard_Submission_%s.md" % VERSION

SLIDES = D.destroy_step(v3.SLIDES)

BLACKBOARD_TEXT = D.destroy_section(
    v3.BLACKBOARD_TEXT,
    "At the end of the lab, remove the Kubernetes objects and destroy all three EC2 instances.",
    ["- Run bash cleanup_lab07.sh on the master node.",
     "- Run kubectl get pods,pvc,pv and show that nothing is left.",
     "- Explain why the clean-up deletes the claim before it deletes the provisioner."])


if __name__ == "__main__":
    for out in (DECK, SCRIPT, BLACKBOARD):
        if os.path.exists(out) and "--force" not in sys.argv:
            sys.exit("%s exists. Bump the version; never overwrite a delivered file." % out)
    L.check_lines(SLIDES)
    sc = v3.sc_manifest()
    L.make_lab("07", SLIDES, DECK, v3.SCRIPT_HEAD, script_path=SCRIPT, prereq_title="Lab Week 07 - Prerequisites")
    deck = Presentation(DECK)
    finish(deck, "CLO835 Week 7 Lab: Volumes")          # file title and author, no blank thumbnail
    for slide in deck.slides:                           # one word for one meaning: Kubernetes, not K8s
        for sh in slide.shapes:
            if sh.has_text_frame:
                for p in sh.text_frame.paragraphs:
                    for r in p.runs:
                        r.text = r.text.replace("K8s", "Kubernetes")
    deck.save(DECK)
    if "--no-repo" not in sys.argv:
        dst, files = L.make_repo_folder("07", "Volumes", None, SCRIPT, extra_files={v3.SC_FILE: sc},
                                        lab_label="Lab Week 07")
        print("repo folder : %s (%d files)" % (dst, len(files)))
    open(BLACKBOARD, "w", encoding="utf8").write(BLACKBOARD_TEXT)
    print("blackboard  : %s" % BLACKBOARD)
