# -*- coding: utf-8 -*-
"""CLO835 Week 13 lab v6 - lab v5 with the version names of v6 (the Week 13 v10 loop of 2026-11-18).

Phase 1 of the loop (report 2026-11-18-08) found no defect in the lab content. So v6 takes each slide line,
each manifest, the cluster slide, Step 0 and the Blackboard text from build_week13_lab_v5 by import. The
changes:
- VERSION is v6, and the outputs are in Week13/ (the names of CLO835_STANDARDS.md A5).
- The script header names Lab_week13_v6.pptx.
- B2 (the Week 12 finding R3-1): this docstring says what the guard checks. See "Outputs" below.
- Review round 1 (B-S1 to B-S3): the Step 5 comment names the Role and its RoleBinding; the title of
  Blackboard section 1 is "Build and Check the Cluster"; the Explain item of section 3 names no number of
  phases. No command changes, so the tested commands stay valid.
- Review round 2 (B-S1 to B-S4, and the lecture finding L-M1): "Kubernetes stores no normal users"; two
  comment lines on the start date and the end date of the certificate; the view comment says "in week13 only";
  the Blackboard text names the CSR and a RoleBinding for the group developers. No command changes.

Outputs: Week13/Lab_week13_v6.pptx, Week13/localMachine_v6.sh,
Week13/Lab_week13_Blackboard_Submission_v6.md, and the repo folder ~/Documents/c/r/CLO835_Fall_2026/Week13/
(7 files). Run from the project root. The builder does not overwrite the deck, the script or the Blackboard
text, unless you give --force. The guard does not check the repo folder (standards A5): each run writes it
again. --no-repo skips the repo folder. The code that writes the outputs runs only under __main__, so an import
writes nothing.
"""
import copy
import os
import sys

from pptx import Presentation

import build_week12_lab_v6 as w12v6
import build_week12_lab_v7 as w12v7
import build_week13_lab_v5 as V
import lab_kubeadm as L
from build_week12_lab_v5 import own_flannel
from build_week12_lecture_v6 import finish

VERSION = "v6"
OUT = "Week13/Lab_week13_%s.pptx" % VERSION
SCRIPT = "Week13/localMachine_%s.sh" % VERSION
BLACKBOARD = "Week13/Lab_week13_Blackboard_Submission_%s.md" % VERSION
TITLE = V.TITLE
CLUSTER_EDITS = V.CLUSTER_EDITS
STEP0 = V.STEP0

# The comment edits of the review rounds of the loop, applied to the content of v5: old line -> new lines.
# Each old line occurs one time in the slide lines. No command changes.
LINE_EDITS = {
    # Round 1, B-S3 (C4, C8): a Role names no subject, so the Step 5 comment names the Role and its RoleBinding.
    "# The Role service-reader allows the ServiceAccount clo835 to get and list Services.":
        ["# The Role service-reader and its RoleBinding allow clo835 to get and list Services."],
    # Round 2, lecture L-M1 (B7): Kubernetes stores ServiceAccounts, so the comment says "normal users".
    "# The cluster CA signs a certificate for dev-user. Kubernetes stores no users.":
        ["# The cluster CA signs a certificate for dev-user. Kubernetes stores no normal users."],
    # Round 2, B-S4 (C4): the end date is about 23 h 55 min after the approval, and this can confuse.
    "# The certificate is valid for 24 hours, because expirationSeconds is 86400.":
        ["# The certificate is valid for 24 hours, because expirationSeconds is 86400.",
         "# The signer sets the start date 5 minutes before the approval.",
         "# So notAfter, the end date, is about 23 h 55 min after the approval."],
    # Round 2, B-S3 (C4, C8): the RoleBinding developers-view gives view in week13 only.
    "# The group of the certificate gets the default ClusterRole view.":
        ["# The group of the certificate gets the default ClusterRole view, in week13 only."]}
SLIDES = copy.deepcopy(V.SLIDES)
for old in LINE_EDITS:
    assert sum(l == old for s in SLIDES if len(s) > 3 for l in s[3]) == 1, old
SLIDES = [s[:3] + ([n for l in s[3] for n in LINE_EDITS.get(l, [l])],) + s[4:] if len(s) > 3 else s
          for s in SLIDES]
BLACKBOARD_EDITS = (
    # Round 1, B-S1 (C7): the title of section 1 uses the words of slide 3, as the Week 12 v8 model does.
    ("## 1. Build the Cluster and Verify Its Status", "## 1. Build and Check the Cluster"),
    # Round 1, B-S2 (C7, lecture finding L1): a read passes two phases, so the Explain item names no number.
    ("- Explain the order of the three phases of a request in the API server.",
     "- Explain the order of the phases of a request in the API server."),
    # Round 2, lecture L-M1: "normal users".
    ("Kubernetes stores no users. The cluster CA signs a certificate",
     "Kubernetes stores no normal users. The cluster CA signs a certificate"),
    ("- Explain why Kubernetes does not store users.", "- Explain why Kubernetes does not store normal users."),
    # Round 2, B-S1 (A1): "request" has one meaning (an API request); the CSR has its name.
    ("- Approve the dev-user request with kubectl certificate approve dev-user.",
     "- Approve the dev-user CertificateSigningRequest (CSR) with kubectl certificate approve dev-user."),
    # Round 2, B-S2 (C7, A1): "Binding" alone is another kind; the object for the group is a RoleBinding.
    ("## 4. Create a Role, a RoleBinding and a Binding for a Group",
     "## 4. Create a Role and a RoleBinding for dev-user, and a RoleBinding for the Group developers"))
BLACKBOARD_TEXT = V.BLACKBOARD_TEXT
for old, new in BLACKBOARD_EDITS:
    assert BLACKBOARD_TEXT.count(old) == 1, old
    BLACKBOARD_TEXT = BLACKBOARD_TEXT.replace(old, new)

# The script header of v5, with the deck name of v6. No other line changes.
SCRIPT_HEAD = V.SCRIPT_HEAD.replace("Lab_week13_%s.pptx" % V.VERSION, "Lab_week13_%s.pptx" % VERSION)
assert SCRIPT_HEAD != V.SCRIPT_HEAD and SCRIPT_HEAD.count("Lab_week13_v6.pptx") == 1


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
    V.master_check(prs)
    finish(prs, TITLE)
    prs.save(OUT)
    w12v7.step0_title(SCRIPT)
    if "--no-repo" not in sys.argv:
        dst, files = L.make_repo_folder("13", "Authentication and RBAC", None, SCRIPT, lab_label="Lab Week 13")
        own_flannel(dst)
        V.repo_words(dst)
        assert len(files) == 7, files
        low = "".join(open(os.path.join(dst, f), encoding="utf8").read().lower() for f in os.listdir(dst)
                      if os.path.isfile(os.path.join(dst, f)))
        assert "cleanup" not in low and "clean up" not in low, "cleanup text is left in the repo folder"
        print("repo folder : %s (%d files)" % (dst, len(files)))
    open(BLACKBOARD, "w", encoding="utf8").write(BLACKBOARD_TEXT)
    print("blackboard  : %s" % BLACKBOARD)
