# -*- coding: utf-8 -*-
"""Pass-or-fail gate for the Week 13 lecture and lab.

It uses the deck checks of gate_week12.py, with the word list of this lecture, and adds the
checks of this week. The script prints PASS or FAIL for each check, then GATE 1 when every
check passes, or GATE 0 when any check fails. It reads the files and changes nothing.

Run from the project root:
    python gate_week13.py LECTURE_STEM LAB_STEM BLACKBOARD_FILE [LIVE_FOLDER]
    python gate_week13.py Lecture_week13_v8 Lab_week13_v3 Lab_week13_Blackboard_Submission_v3.md
"""
import os
import re
import subprocess
import sys

from pptx import Presentation

import gate_week12 as G
from gate_week12 import check, paragraphs, words_of_page

ROOT = G.ROOT = "week13/"
REPO = G.REPO = os.path.expanduser("~/Documents/c/r/CLO835_Fall_2026/Week13/")
OUTLINE_MODEL = "Week12/Lecture_week12_v6.pptx"
# "resource" is the RBAC word, and "access entries" is the AWS name. The other words of Week 12 stay.
G.BANNED = [b for b in G.BANNED if b not in (r"\bresource\b", r"\bentries\b")] + [
    r"(?<![:\w])[Ss]erviceaccount", r"Kuberntes", r"\bAKS\b", r"IRSA", r"irinag", r"\bAdmins deploying",
    r"\bDevs\b", r"\bSas\b", r"Curl ", r"–k", r"Withmultiple", r"Kube API", r"Amazon IAM", r"\b[Pp]lugin", r"[Mm]echanism",
    r"outside service", r"third party", r"\b[Rr]efus", r"\bLink the\b", r"Role Based", r"/logs", r"worker-2"]
# Labels of diagram boxes. None of these is a bullet on two slides.
G.ALLOWED_REPEATS = {"kubernetes api", "serviceaccount", "role-based access control (rbac)", "eks api server"}
# The lab shows these four refusals on purpose, in the order of the file.
EXPECTED_REFUSALS = ["get pods", "delete pod web", "auth can-i list services -n default", "auth can-i list persistentvolumes"]


def lecture_extra(stem):
    prs = Presentation(ROOT + stem + ".pptx")
    slides = list(prs.slides)
    by_slide = {}
    for no, sh, p, text in paragraphs(prs):
        by_slide.setdefault(no, []).append(text)
    check("lecture: cover says Week 13", "Week 13 · Lecture" in by_slide[1], by_slide[1])
    check("lecture: 26 slides", len(slides) == 26, len(slides))
    check("lecture: cover title", "Introduction to K8s RBAC" in by_slide[1], by_slide[1])
    model = Presentation(OUTLINE_MODEL).slides[2]
    tiles = {sh.text_frame.text for sh in model.shapes if sh.has_text_frame and sh.name != "TextBox 1"
             and sh.top < 6000000}
    ours = {sh.text_frame.text for sh in slides[2].shapes if sh.has_text_frame and sh.name != "TextBox 1"
            and sh.top < 6000000}
    check("lecture: outline equals the Week 12 outline", tiles == ours, tiles ^ ours)

    def fill_of(text):
        box = [sh for sh in slides[2].shapes if sh.has_text_frame and sh.text_frame.text == text][0]
        frame = [sh for sh in slides[2].shapes if sh.shape_type == 1 and sh.top == box.top
                 and abs(sh.left + 146304 - box.left) < 20000][0]
        return str(frame.fill.fore_color.rgb)
    check("lecture: Week 13 is the blue tile", fill_of("Week 13: K8s – RBAC and EKS") == "1FA8E0")
    check("lecture: Week 12 is a normal tile", fill_of("Week 12: K8s – ConfigMaps & Secrets") == "F4F7FB")
    check("lecture: the exam tile is red", fill_of("Week 11: Exam & Mock Exam week") == "E74C3C")
    titles = {no: lines[0] for no, lines in by_slide.items()}
    manifest = [no for no, title in titles.items() if title == "Role and RoleBinding"][0]
    agenda = {"authentication": "Authentication and Authorization Process", "ServiceAccounts": "ServiceAccounts",
              "RBAC": "RBAC Introduction", "Roles and RoleBindings": "Role and RoleBinding",
              "ClusterRoles and ClusterRoleBindings": "ClusterRoles and ClusterRoleBindings",
              "default roles": "Default ClusterRoles", "Amazon EKS": "Amazon EKS Authentication"}
    for word, title in agenda.items():
        said = any(word in line for line in by_slide[2])
        taught = any(t.startswith(title) for t in titles.values())
        check("lecture: agenda line '%s' has a slide" % word, said and taught)
    late = []
    for no in range(1, len(slides) + 1):
        for x0, y0, x1, y1, word in words_of_page(ROOT + stem + ".pdf", no):
            if 6.72 < y1 and y0 < 6.82:
                late.append((no, word))
    check("lecture: no text below 6.70 in in the rendered PDF", not late, late[:6])
    # Each outside picture is gone, so only the logo and the whale stay.
    pics = [(no, sh.name) for no, s in enumerate(slides, 1) for sh in s.shapes
            if sh.shape_type == 13 and sh.width > 914400 and no != 1]
    check("lecture: no picture but the logo and the whale", not pics, pics)
    lab = open(REPO + "localMachine.sh").read()
    role = re.search(r"tee developer-role.yaml <<'EOF'\n(.*?)\nEOF", lab, re.S).group(1)
    shown = [text for no, sh, para, text in paragraphs(prs) if no == manifest and G.is_mono(para)
             and not text.startswith(("#", "$"))]
    check("lecture: the manifest of the Role slide equals the lab manifest",
          sorted(l.strip() for l in role.split("\n")) == sorted(shown),
          set(l.strip() for l in role.split("\n")) ^ set(shown))


def lab_extra(lab, blackboard):
    run = subprocess.run([sys.executable, "-I", os.environ["INSTRUMENT"], REPO + "localMachine.sh", "https://none/"],
                         capture_output=True, text=True).stdout
    count = run.count('echo "@@CMD')
    check("lab: at most 40 commands", count <= 40, count)
    check("lab: Step 0 to Step 6", re.findall(r"@@STEP (\d)", run) == list("0123456"), re.findall(r"@@STEP (\d)", run))
    script = open(REPO + "localMachine.sh").read()
    check("lab: each step names its slide", re.findall(r"# Step (\d) - .*\(slide (\d+)\)", script)
          == [(str(i), str(i + 3)) for i in range(7)])
    check("lab: the repo script equals the deck script",
          script == open(ROOT + lab.replace("Lab_week13", "localMachine") + ".sh").read())
    names = sorted(x for x in os.listdir(REPO) if x != ".terraform")
    check("lab: 8 files", names == sorted([".gitignore", "bootstrap.sh", "cleanup_lab13.sh", "localMachine.sh", "main.tf",
                                           "master-init.sh.tftpl", "variables.tf", "worker-join.sh.tftpl"]), names)
    check("lab: no state or key file", not [x for x in os.listdir(REPO) if re.search(r"tfstate|tfvars|\.pem", x)])
    for f in ("localMachine.sh", "cleanup_lab13.sh"):
        check("lab: bash -n " + f, subprocess.run(["bash", "-n", REPO + f]).returncode == 0)
    check("lab: terraform fmt", subprocess.run(["terraform", "-chdir=" + REPO, "fmt", "-check"], capture_output=True).returncode == 0)
    text = "".join(open(REPO + x, errors="replace").read() for x in names)
    bad = re.findall(r"/Users/|\.ssh/|sojodyan|AKIA|ASIA[0-9A-Z]{8}|luksa|busybox|\bnano\b|flannel-io|ghcr\.io|[Ww]eek ?12", text)
    check("lab: repo scan", not bad, bad[:5])
    master = open(REPO + "master-init.sh.tftpl").read()
    cleanup = open(REPO + "cleanup_lab13.sh").read()
    check("lab: master-init writes the same cleanup script", cleanup.strip() in master.replace("$$", "$"))
    check("lab: cleanup removes each file and each object with no namespace", all(f in cleanup for f in (
        "dev-user.key", "dev-user.csr", "dev-user.crt", "dev-user-csr.yaml", "developer-role.yaml", "curl-sa.yaml",
        "service-reader.yaml", "clusterrolebinding pv-test", "clusterrole pv-reader", "csr dev-user",
        "delete-context dev-user@kubernetes", "delete-user dev-user")))
    images = sorted(set(re.findall(r"(?:^\s*(?:- )?image:\s*|--image=)(\S+)", script, re.M)))
    check("lab: images of maziar only", images and all(i.startswith("maziar/") for i in images), images)
    flannel = re.findall(r"^\s*image:\s*(\S+)", master, re.M)
    check("lab: Flannel images of maziar only", len(flannel) == 3 and all(i.startswith("maziar/") for i in flannel), flannel)
    for topic, needle in (("a group", "--group=developers"), ("a default ClusterRole", "--clusterrole=view"),
                          ("a ClusterRole", "create clusterrole pv-reader"),
                          ("a ClusterRoleBinding", "create clusterrolebinding pv-test"), ("tee", "tee curl-sa.yaml"),
                          ("a RoleBinding that fails", "create rolebinding pv-test"), ("/version", "6443/version"),
                          ("the anonymous 403", "6443/apis"), ("kubectl proxy", "kubectl proxy --port=8001")):
        check("lab: practises " + topic, needle in script)
    check("lab: no manifest written with cat", "cat >" not in script)
    prs = Presentation(ROOT + lab + ".pptx")
    all_text = [p for _, _, _, p in paragraphs(prs)]
    check("lab: label is Lab Week 13", "Lab Week 13 - Prerequisites" in all_text)
    check("lab: sample version is v1.35.10", any("v1.35.10" in t for t in all_text) and not any("v1.35.9" in t for t in all_text))
    b = open(ROOT + blackboard).read()
    check("blackboard: title", b.startswith("# Lab Week 13: Authentication and RBAC"))
    check("blackboard: 7 sections", len(re.findall(r"^## \d\. ", b, re.M)) == 7 and "all 7 sections" in b)
    check("blackboard: no pledge", "pledge" not in b.lower())
    check("blackboard: ends with the Important paragraph", b.strip().split("\n")[-1].startswith("Important: Use your own"))
    check("blackboard: no control-plane node", "control-plane node" not in b)
    for sec in re.split(r"^## \d\. ", b, flags=re.M)[1:]:
        items = [l for l in sec.split("## Submission")[0].split("\n") if l.startswith("- ")]
        kinds = [i.startswith("- Explain") for i in items]
        check("blackboard: Explain items last in '%s'" % sec.split("\n")[0][:30], kinds == sorted(kinds))


def live_checks(folder):
    def read(name):
        return open(os.path.join(folder, name), errors="replace").read()
    for no in (1, 2):
        log = read("run%d.log" % no)
        check("live: pass %d ran 40 commands" % no, log.count("@@CMD") == 40, log.count("@@CMD"))
        failed = re.findall(r"@@CMD L\d+: ([^\n]*)\n(?:(?!@@CMD).*\n)*?@@RC [1-9]", log)
        hits = [all(e not in f for e in EXPECTED_REFUSALS) for f in failed]
        check("live: pass %d has only the four refusals" % no, len(failed) == 4 and not any(hits), failed)
        lines = log.split("\n")
        check("live: pass %d first can-i persistentvolumes says no, the second says yes" % no,
              [x for x in lines if x in ("no", "yes")][-3:] == ["no", "no", "yes"], [x for x in lines if x in ("no", "yes")])
    check("live: terraform output public_ips", "master" in read("out_public.log"))
    check("live: terraform output private_ips", "master" in read("out_private.log"))
    check("live: lecture commands match the slides", "@@LECTURE OK" in read("lecture.log"))
    check("live: destroy complete", "Destroy complete! Resources: 15 destroyed." in read("destroy.log"))
    pause = read("pause1.log")
    check("live: cluster runs the maziar Flannel image", "maziar/flannel:v0.28.10" in pause and "ghcr.io" not in pause)
    recovery = read("recovery.log")
    check("live: recovery clean-up returns 0", re.search(r"rc=0 seconds=\d+\n", recovery) is not None)
    tested = re.sub(r"@@CMD L\d+:", "@@CMD", read("run.sh"))
    final = subprocess.run([sys.executable, "-I", os.environ["INSTRUMENT"], REPO + "localMachine.sh", "https://none/"],
                           capture_output=True, text=True).stdout
    check("live: the tested commands equal the final commands", tested.strip() == re.sub(r"@@CMD L\d+:", "@@CMD", final).strip())


def main():
    lecture, lab, blackboard = sys.argv[1:4]
    G.deck_checks(lecture, "lecture")
    lecture_extra(lecture)
    G.deck_checks(lab, "lab")
    lab_extra(lab, blackboard)
    if len(sys.argv) > 4:
        live_checks(sys.argv[4])
    print("\nGATE %d  (%d failed)" % (0 if G.FAILS else 1, len(G.FAILS)))
    sys.exit(1 if G.FAILS else 0)


if __name__ == "__main__":
    main()
