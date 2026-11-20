# -*- coding: utf-8 -*-
"""CLO835 Week 12 lab v8 - lab v7 with the fixes of the audit of 2026-11-18 (loop report 2026-11-18-06).

The changes add no new command. The lab stays at 39 commands on the master (standards C1).
- B2: the priority of env over envFrom is now visible. The ConfigMap app-config also holds GREETING=hi,
  and env sets GREETING=hello, so printenv shows hello (Step 2). The Step 4 comment only says that env and
  envFrom give DB_Password the same value.
- L2 (syllabus, Part 2 Section 7): config-env.yaml sets MESSAGE to "$(GREETING) $(COLOR)", so the student
  sees a reference to earlier environment variables (Step 2).
- L3 (syllabus): config-volume.yaml sets defaultMode: 0440. Step 3 shows the permissions with ls -lL.
  The busybox ls of maziar/alpine-curl follows the symbolic links of the volume with -L.
- The Blackboard text asks for the new values and has three new Explain items.
- Review round 1 (2026-11-18):
  - R1-1 (A1 glossary): the Step 2 comment says "two earlier environment variables".
  - R1-2 (A1): the KUBERNETES_SERVICE_HOST comment moves next to the printenv command.
    No comment paragraph has more than 6 sentences.
  - R1-3 (C7): section 1 of the Blackboard text is "Build and Check the Cluster", the words of slide 3.
  - R1-4 (A1 glossary): this docstring says "does not overwrite", not "refuses".
- Review round 2 (R2-1, A1): the docstring has short sentences in the active voice.
- Review round 3 (R3-1): the docstring states what the guard checks, and what runs at import.
All other content is v7 (imported, not copied). The builder writes the repo folder as v7 does.

Outputs: Week12/Lab_week12_v8.pptx, Week12/localMachine_v8.sh,
Week12/Lab_week12_Blackboard_Submission_v8.md, ~/Documents/c/r/CLO835_Fall_2026/Week12/
Run from the project root. It does not overwrite the deck, the script or the Blackboard text,
unless you give --force. The guard does not check the repo folder (standards A5).
--no-repo skips the repo folder. The code that writes the outputs runs only under __main__,
so an import writes nothing.
"""
import os
import sys

from pptx import Presentation

import build_week12_lab_v6 as v6
import build_week12_lab_v7 as v7
import lab_kubeadm as L
from build_week12_lecture_v6 import finish

VERSION = "v8"
OUT = "Week12/Lab_week12_%s.pptx" % VERSION
SCRIPT = "Week12/localMachine_%s.sh" % VERSION
BLACKBOARD = "Week12/Lab_week12_Blackboard_Submission_%s.md" % VERSION
N = v6.N
D = v6.D

# Terminal lines: old line -> new lines, for each step title.
TERM_EDITS = {
    "Environment variables from a ConfigMap": {
        "    --from-file=LOG_LEVEL": ["    --from-literal=GREETING=hi --from-file=LOG_LEVEL"],
        "# envFrom injects every key.": [
            "# envFrom injects every key.",
            "# The ConfigMap also holds GREETING=hi. env has priority over envFrom.",
            "# $(GREETING) and $(COLOR) give the values of two earlier environment variables."],
        "# The kubelet injects KUBERNETES_SERVICE_HOST for the API server.": [],
        "# printenv shows one value for each name, in the order of the names.": [
            "# The kubelet injects KUBERNETES_SERVICE_HOST for the API server.",
            "# printenv shows one value for each name, in the order of the names."],
        "$ kubectl exec config-env " + N + " -- \\":
            ["$ kubectl exec config-env " + N + " -- printenv GREETING COLOR \\"],
        "    printenv GREETING COLOR APP_COLOR APP_MODE LOG_LEVEL KUBERNETES_SERVICE_HOST":
            ["    MESSAGE APP_COLOR APP_MODE LOG_LEVEL KUBERNETES_SERVICE_HOST"],
    },
    "A ConfigMap as a volume": {
        "# Each key becomes a file in the volume.": [
            "# Each key becomes a file in the volume.",
            "# defaultMode 0440 lets the owner and the group read each file."],
        "$ kubectl exec config-volume " + N + " -- ls /etc/app-config":
            ["$ kubectl exec config-volume " + N + " -- ls -lL /etc/app-config"],
    },
    "A Secret, and the ServiceAccount token": {
        "# When env and envFrom set the same name, the value of env has priority.":
            ["# env and envFrom both set DB_Password, with the same value."],
    },
}

# Manifest lines: old line -> new lines, for each step title.
FILE_EDITS = {
    "Environment variables from a ConfigMap": {
        "          key: APP_COLOR": ["          key: APP_COLOR",
                                     "    - name: MESSAGE",
                                     '      value: "$(GREETING) $(COLOR)"'],
    },
    "A ConfigMap as a volume": {
        "      name: app-config": ["      name: app-config", "      defaultMode: 0440"],
    },
}


def _edit(lines, edits, where):
    out, done = [], set()
    for line in lines:
        if line in edits:
            out += edits[line]
            done.add(line)
        else:
            out.append(line)
    assert done == set(edits), (where, set(edits) - done)
    return out


def slides():
    out, seen_t, seen_f = [], set(), set()
    for s in v7.SLIDES:
        if s[0] == "step2" and (s[1] in TERM_EDITS or s[1] in FILE_EDITS):
            term = _edit(s[3], TERM_EDITS.get(s[1], {}), s[1])
            body = _edit(s[6], FILE_EDITS.get(s[1], {}), s[1])
            seen_t.add(s[1])
            if s[1] in FILE_EDITS:
                seen_f.add(s[1])
            out.append(s[:3] + (term,) + s[4:6] + (body,))
        else:
            out.append(s)
    assert seen_t == set(TERM_EDITS) and seen_f == set(FILE_EDITS), (seen_t, seen_f)
    return out


SLIDES = slides()
STEP0 = v7.STEP0
SCRIPT_HEAD = v7.SCRIPT_HEAD.replace("Lab_week12_v7.pptx", "Lab_week12_%s.pptx" % VERSION)
assert "Lab_week12_v8.pptx" in SCRIPT_HEAD

# The manifests, for the lecture (C8: the lecture takes them from here).
CM_ENV_POD = SLIDES[4][6]
CM_VOL_POD = SLIDES[5][6]
SECRET_POD = SLIDES[6][6]
DEV = SLIDES[7][6]


def blackboard_text():
    text = v7.blackboard_text()
    for old, new in (
            # Review round 1 (R1-3, C7): the section title uses the words of slide 3.
            ("## 1. Build the Cluster and Verify Its Status", "## 1. Build and Check the Cluster"),
            ("- Run the printenv command for GREETING, COLOR, APP_COLOR, APP_MODE, LOG_LEVEL and "
             "KUBERNETES_SERVICE_HOST, and show the values.",
             "- Run the printenv command for GREETING, COLOR, MESSAGE, APP_COLOR, APP_MODE, LOG_LEVEL and "
             "KUBERNETES_SERVICE_HOST, and show the values."),
            ("- Explain the difference between env, configMapKeyRef and envFrom.\n",
             "- Explain the difference between env, configMapKeyRef and envFrom.\n"
             "- Explain why GREETING shows hello, but the ConfigMap holds GREETING=hi.\n"
             "- Explain how Kubernetes sets the value of MESSAGE.\n"),
            ("- Run the ls and cat commands on /etc/app-config, and show the value of APP_COLOR.",
             "- Run the ls -lL and cat commands on /etc/app-config.\n"
             "- Show the permissions of the files and the value of APP_COLOR."),
            ("- Explain why the file changes and the environment variable does not change.\n",
             "- Explain why the file changes and the environment variable does not change.\n"
             "- Explain which permissions defaultMode: 0440 gives to the files.\n")):
        assert text.count(old) == 1, old
        text = text.replace(old, new)
    return text


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
    v7.slide3(prs)
    finish(prs, "CLO835 Week 12 Lab: ConfigMaps and Secrets")
    prs.save(OUT)
    v7.step0_title(SCRIPT)
    if "--no-repo" not in sys.argv:
        dst, files = L.make_repo_folder("12", "ConfigMaps and Secrets", None, SCRIPT, lab_label="Lab Week 12")
        v6.own_flannel(dst)
        v7.repo_words(dst)
        low = "".join(open(os.path.join(dst, f), encoding="utf8").read().lower() for f in os.listdir(dst)
                      if os.path.isfile(os.path.join(dst, f)))
        assert "cleanup" not in low, "cleanup text is left in the repo folder"
        print("repo folder : %s (%d files)" % (dst, len(files)))
    open(BLACKBOARD, "w", encoding="utf8").write(text)
    print("blackboard  : %s" % BLACKBOARD)
