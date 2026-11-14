# -*- coding: utf-8 -*-
"""CLO835 Week 14 lab v3 - lab v2 with no cleanup script (the user, 2026-11-11).

terraform destroy removes the three machines, the viewer user and every object and file of
the lab, so:
- Step 6 is "Destroy the cluster": only terraform destroy on your own machine.
- The repo folder has no cleanup_lab14.sh, and master-init writes no cleanup file.
- The Blackboard text v3 (the short form of v2): "Show terraform destroy." replaces
  "Show the clean-up and terraform destroy."
- metrics-server.yaml comes from the course repository (HEAD:Week14), because v2 read it from a
  scratchpad mirror that no longer exists.
All other content is v2 (imported, not copied).

Outputs: week14/Lab_week14_v3.pptx, week14/localMachine_v3.sh,
week14/Lab_week14_Blackboard_Submission_v3.md, ~/Documents/c/r/CLO835_Fall_2026/Week14/
Run from the project root. It is guarded, so importing it writes nothing.
It refuses to overwrite an output, unless you give --force. --no-repo skips the repo folder.
"""
import copy
import os
import subprocess
import sys

import build_week14_lab_v2 as v2
import lab_destroy_only as D
import lab_kubeadm as L

VERSION = "v3"
DECK = "week14/Lab_week14_%s.pptx" % VERSION
SCRIPT = "week14/localMachine_%s.sh" % VERSION
BLACKBOARD_OUT = "week14/Lab_week14_Blackboard_Submission_%s.md" % VERSION

SLIDES = D.destroy_step(v2.SLIDES)

BLACKBOARD = copy.deepcopy(v2.BLACKBOARD)
_hits = 0
for _title, _intro, _items in BLACKBOARD:
    for _i, _item in enumerate(_items):
        if _item == "Show the clean-up and terraform destroy.":
            _items[_i] = "Show terraform destroy."
            _hits += 1
assert _hits == 1, _hits


def ms_manifest():
    """The metrics-server v0.7.1 manifest of the course repository, with --kubelet-insecure-tls."""
    text = subprocess.check_output(["git", "-C", L.REPO, "show", "HEAD:Week14/" + v2.MS_FILE]).decode("utf8")
    assert text.count("        - --kubelet-insecure-tls\n") == 1
    return text


if __name__ == "__main__":
    for out in (DECK, SCRIPT, BLACKBOARD_OUT):
        if os.path.exists(out) and "--force" not in sys.argv:
            sys.exit("%s exists. Bump the version; never overwrite a delivered file." % out)
    L.check_lines(SLIDES)
    L.make_lab("14", SLIDES, DECK, v2.SCRIPT_HEAD, script_path=SCRIPT)
    if "--no-repo" not in sys.argv:
        dst, files = L.make_repo_folder("14", "Kubeconfig and the Horizontal Pod Autoscaler", None, SCRIPT,
                                        extra_files={v2.MS_FILE: ms_manifest()})
        print("repo folder : %s (%d files)" % (dst, len(files)))
    L.blackboard_text("14", "The Terraform configuration in Week 14 creates the same three Ubuntu 26.04 EC2 "
                      "machines as Weeks 04 to 13.", BLACKBOARD, BLACKBOARD_OUT)
    print("blackboard  : %s" % BLACKBOARD_OUT)
