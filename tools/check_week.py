# -*- coding: utf-8 -*-
"""CLO835 - one pass-or-fail checker for a week: the lecture deck, the lab deck, the lab repo folder, the
Blackboard lab text, the F4 table, the quiz and the logs of a live test.

It replaces gate_week12.py, gate_week13.py, gate_week13_v2.py, gate_week13_v3.py and tools/rungate.py. The
generic checks come from CLO835_STANDARDS.md. The values that only one week has (slide titles, section titles,
object names, planned denials, the F4 table) are in tools/week_specs/weekNN.py. With no spec file, the checks
that need a spec value show N/A.

Each check prints one line: PASS, FAIL or N/A, the rule of CLO835_STANDARDS.md, the name, and for a FAIL the
detail. Then the checker prints one line for each rule of the standards, and GATE 1 when no check fails, or
GATE 0. The exit code is 0 for GATE 1 and 1 for GATE 0.

The checker reads the files and changes nothing. It lists one directory level at a time with os.listdir, so
it never walks a directory tree and a directory link cannot make a loop. Each external command has a time limit.

Usage (from any directory; the paths are absolute):
    .venv/bin/python -I tools/check_week.py --week 13
    .venv/bin/python -I tools/check_week.py --week 12 --lecture Lecture_week12_v8 --lab Lab_week12_v8 \\
        --blackboard Lab_week12_Blackboard_Submission_v8.md --live <folder of a live test>
    .venv/bin/python -I tools/check_week.py --week 7 --deck Lecture_week07_v8 --kind lecture

The options:
    --week N        the week (required).
    --lecture STEM  the lecture deck in the week directory, with no .pptx. Default: the newest Lecture_weekNN_vN.
    --lab STEM      the lab deck. Default: the newest Lab_weekNN_vN.
    --blackboard F  the Blackboard lab text. Default: the newest Lab_weekNN_Blackboard_Submission_vN.md.
    --dir DIR       the week directory of the decks. Default: WeekNN or weekNN in the project root.
    --repo DIR      the repo folder of the week. Default: ~/Documents/c/r/CLO835_Fall_2026/WeekNN.
    --quiz DIR      the quiz folder. Default: the newest quiz_pool_src/Quiz_..._Easy20 folder of the week.
    --live DIR      the folder of a live test (E3): run1.log, run2.log, out_public.log, out_public2.log,
                    out_private.log, destroy1.log, destroy.log, pause1.log, lecture.log and run.sh.
    --deck STEM     run only the deck checks on one deck (the form of tools/rungate.py).
    --kind K        lecture or lab, with --deck. Default: lecture.
    --out FILE      also write the result as a Markdown file.
"""
import argparse
import collections
import io
import os
import re
import runpy
import subprocess
import sys
import zipfile

from PIL import Image
from pptx import Presentation

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(HERE)
COURSE_REPO = os.path.expanduser("~/Documents/c/r/CLO835_Fall_2026")
INSTRUMENT = os.path.join(HERE, "instrument.py")
CUE_SIM = os.path.join(HERE, "quiz_cue_sim.py")
SPECS = os.path.join(HERE, "week_specs")
QUIZ_ROOT = os.path.join(PROJECT, "quiz_pool_src")
TIMEOUT = 300
EMU = 914400.0

# ---------------------------------------------------------------------------------------------------------
# The rules of CLO835_STANDARDS.md. A rule with a reason gets N/A when no check of the checker covers it.
RULES = [
    ("A1", "Language: ASD-STE100", None, "the checks find listed words and long sentences; the rest needs a reader"),
    ("A2", "Scope and permission", "a rule for the work, not for a file"),
    ("A3", "The answer in the chat", "a rule for the chat, not for a file"),
    ("A4", "Reports", "a rule for the work, not for a file"),
    ("A5", "Files, versions and builders", None),
    ("A6", "The machine and the tools", "a rule for the work, not for a file"),
    ("A7", "Fixed, good, done: 0 or 1", "a rule for the work: this checker is step 2 of A7"),
    ("B1", "Canvas and chrome", None),
    ("B2", "Palette", None),
    ("B3", "Text sizes", None),
    ("B4", "Bullets", None),
    ("B5", "Terminals", None),
    ("B6", "Diagrams and images", None, "the drawing rules need a look at the PDF pages"),
    ("B7", "Content", None, "the facts for v1.35, the links (HTTP 200) and the repeated points need a reader"),
    ("B8", "The build and QA pipeline of a deck", None),
    ("C1", "Size and structure", None),
    ("C2", "One content list", None),
    ("C3", "Commands", None, "an exit 0 of each command needs --live"),
    ("C4", "Comments and sample output", None, "each comment against the live output needs --live and a reader"),
    ("C5", "The repo folder of a week", None),
    ("C6", "The cluster", None),
    ("C7", "The Blackboard lab text", None),
    ("C8", "Lecture and lab agree", None, "the content of the slide Lab Week NN at a Glance needs a reader"),
    ("C9", "The lab checks", None),
    ("D1", "The kinds of quiz", "a rule for the design of the quiz"),
    ("D2", "Each question", "the audit (D9) checks a part; the rest needs the review of D11"),
    ("D3", "The options", "the audit (D9) and the cue simulation (D10) check a part; the rest needs D11"),
    ("D4", "Across the quiz or the pool", "the audit (D9) checks the leaks; the rest needs D11"),
    ("D5", "Correctness and proof", "needs a live probe or the documentation"),
    ("D6", "Feedback", "needs the review of D11"),
    ("D7", "Platform rules", "the audit (D9) checks the letters and the runs"),
    ("D8", "The quiz builder", "the builder overwrites its outputs (A5), so the checker does not run it"),
    ("D9", "The audit", None),
    ("D10", "Cue simulations", None),
    ("D11", "The review loop", "a rule for the work, not for a file"),
    ("D12", "Blackboard delivery of a quiz", "a setting in Blackboard, not a file"),
    ("E1", "The environment", "a fact of the AWS account, not a file"),
    ("E2", "Permission", "a rule for the work, not for a file"),
    ("E3", "The live test protocol of a lab", None),
    ("F1", "The course repo", None),
    ("F2", "Accounts and images", None, "that each tag exists on Docker Hub needs a network check"),
    ("F3", "Security", None),
    ("F4", "A rubric line must be runnable", None),
    ("F5", "Git authorship", "the user does the git part (F1)"),
    ("G1", "Lab item names", "a name in Blackboard, not a file (the label rule of C1 has its own checks)"),
    ("G2", "Lab items", "a setting in Blackboard, not a file"),
    ("G3", "The schedule", "a fact of the course, not a file"),
    ("G4", "Grading text for students", "a rule for the grading text, not for a week file"),
]

PALETTE = {"1FA8E0", "37465A", "3F3F3F", "868686", "CFDBEE", "F4F7FB", "E0E0E0", "27AE60", "E74C3C", "2A2A2A",
           "2196A0", "1F8FCD", "1F7AB8", "2466A0", "3A3A3A", "FF5F56", "FFBD2E", "27C93F", "BABABA", "4EC9E0",
           "FFFFFF"}
# A1: the words that the deck gate bans outside Consolas text.
BANNED = [r"\boptions\b", r"\bparameters\b", r"\bkeeps?\b", r"\bways?\b", r"\bdescription\b", r"\bPODs?\b", r"K8s-",
          r"[Cc]ommand line\b(?! interface)", r"Config Map", r"ETCD", r"\bwe\b", r"\bOverrid", r"never on disk",
          r"\bcontrol-plane (node|disk)\b", r"\bbake\b", r"\bdumped\b", r"\bresource\b", r"\bentries\b",
          r"(?<![Ee]nvironment )\b[Vv]ariables?\b", r"secret volume", r"configMap volume", r"mounted (files|folder)"]
CONTRACTION = re.compile(r"\b\w+'(t|s|re|ve|ll|d)\b")
# An agenda line that names a slide title, and diagram labels (gate_week12.py). A spec can add more.
ALLOWED_REPEATS = set()                # gate_week12.py had 3 Week 12 phrases; they are in week_specs/week12.py

# The lab texts that every lab of the current form has (the Week 12 v7 model, gate_week13_v3.py).
LABELS = ["A Kubernetes cluster with kubeadm (3 nodes)", "A container image that the Kubernetes nodes can pull"]
SLIDE3_LEFT = ["# ON YOUR OWN MACHINE - get the repo. Then build 1 master and 2 workers.",
               "# If no clone exists: git clone https://github.com/sojoudian/CLO835_Fall_2026.git",
               "# git reset --hard replaces your changes with the files of GitHub.",
               "$ cd CLO835_Fall_2026 && git fetch && git reset --hard origin/master",
               "$ cd Week{NN} && terraform init",
               "$ terraform apply          # Terraform asks for key_name",
               "# These two commands show the public and the private addresses.",
               "$ terraform output public_ips", "$ terraform output private_ips",
               "# kubeadm forms the cluster at boot. Wait about 4 minutes.",
               "$ ssh -i <your-key>.pem ubuntu@<masternode-public-ip>",
               "# ON THE MASTER - check the three nodes", "$ kubectl get nodes -o wide", "$ kubectl get pods -n kube-system"]
SLIDE3_RIGHT = ["$ kubectl get nodes -o wide", "# Three real nodes form this cluster.",
                "# It uses no kind and no Docker in Docker.", "# Other columns show Ubuntu 26.04 and containerd 2.2.2."]
ALSO = "# This also deletes every Kubernetes object and every file of the lab."
STEP6 = ["# ON YOUR OWN MACHINE - destroy the three EC2 instances.", ALSO,
         "$ terraform destroy          # Terraform asks for key_name again",
         "# Destroy the cluster at the end of each lab. The Learner Lab budget is small."]
HEAD = ["# CLO835 - Week {NN} - {TOPIC}.",
        "# Run the commands ON THE MASTER NODE, step by step, except the commands ON YOUR OWN MACHINE. Do NOT run the whole file.",
        "# Terraform builds 3 EC2 instances: 1 master and 2 workers. The cluster forms"]
REPO_FILES = [".gitignore", "bootstrap.sh", "localMachine.sh", "main.tf", "master-init.sh.tftpl", "variables.tf",
              "worker-join.sh.tftpl"]
SAMPLE_VERSION = "v1.35.10"          # C4: the version that the cluster installs (2026-11-10)
FLANNEL_IMAGE = "maziar/flannel:v0.28.10"
RESOURCES = 15                       # C6: terraform apply adds 15 resources
# An -ing form. RoleBinding, ClusterRoleBinding and Binding are names of Kubernetes objects, not verb forms.
# Nouns are not -ing verb forms, and a phase name after "the" (the Running phase, the Pending claim) is not one.
ING = (r"\b(?!\w*Binding\b)(?!(?:[Ss]tring|[Nn]othing|[Ss]omething|[Aa]nything|[Ee]verything|[Tt]hings?|[Dd]uring|[Pp]ing"
       r"|[Rr]ing)\b)(?!(?<=the )(?:Pending|Running)\b)\w+ing\b")
# A1 texts of the old lab decks (the review rounds of Week 12 and Week 13).
# "Running" and "lets" of gate_week13_v3.py are in week_specs/week13.py (DECK_A1_EXTRA). "Running" is also a word
# of sample output (1/1 Running), so the generic check looks for it only in prose (DECK_A1_PROSE).
DECK_A1 = [r"accessible by", r"No clone yet", r"build 1 master \+ 2 workers", r"No kind\.",
           r"\bthe API knows\b", r"can ask this", r"\bconfirm\b", r"\bK8s\b"]
DECK_A1_PROSE = [r"\bRunning\b"]
# A1 words that must not be in the script, the repo files or the Blackboard text (gate_week13_v3.py, with
# "From the Week13" for each week). A spec adds the words of its week in A1_EXTRA.
A1 = [r"\bK8s\b", r"\bprints?\b", r"\bfolders?\b", r"\b[Rr]efus", r"control-plane node", r"CONTROL PLANE node",
      r"\b[Tt]urn (on|off)\b", r"\b(turns|turned) (on|off)\b", r"\bcomes? back\b", r"\bputs? .{0,30}\bin\.",
      r"\bshut down\b", r"\bhand over\b", r"\bgo (out|past)\b", r"\bat once\b", r"\bcarry over\b", r"\bholds back\b",
      r"\bretrying\b", r"\bsticks\b", r"\bSSH in\b", r"\bis appended\b", r"\bis not blocked\b", r"\bis dropped\b",
      r"\bships one\b", r"\bUsed for SSH\b", r"\bLab only\b", r"\bchars\b", r"—", r"\br6i\b", r"\bwithout \w+ing\b",
      r"\bcleanup\b", r"\bclean[ -]up\b", r"\btee\b", r"\bgrants?\b", r"\bpods? network\b",
      r"\bNext try in\b", r"Prerequisites installed", r"by themselves", r"Give them a few minutes", r"\bright after\b",
      r"No clone yet", r"\bthe API knows\b", r"can ask this", r"initializes automatically", r"Authentication checks",
      r"does not run admission control", r"retries kubeadm join", r"\battached to the node\b", r"(?m)^# kubeconfig for",
      r"section by section", r"Run these ON", r"(?<!Terraform )asks for key_name", r"Always destroy", r"From the Week\d+",
      r"x86_64", r"does not permit", r"Terraform builds 3 machines", r"next try starts", r"\bwould stop\b",
      r"Terraform creates no VPC", r"when this node is ready"]
# The names of the .gitignore of a week folder (C5). Git does not track them, so they are not repo text.
IGNORED = r"^\.DS_Store$|^\.terraform|\.tfstate|^terraform\.tfvars$|\.tfplan$|^crash\.log$|\.pem$|\.ppk$|^credentials$"
KUBEADM_FROM = 4                     # G3: Weeks 01 to 03 are Docker weeks; the kubeadm labs start in Week 04
# F3: the GitHub account may appear only in a GitHub URL (F2: the copies of other repos are forks of sojoudian).
ACCOUNT = r"(?<!github\.com/)(?<!githubusercontent\.com/)[Ss]ojoudian"
NUMBER = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine"}

RESULTS = []          # (status, rule, name, detail)


def emit(status, rule, name, detail=""):
    RESULTS.append((status, rule, name, detail))
    tail = ""
    if status == "FAIL":
        tail = "  -> %s" % (detail,)
    elif status == "N/A":
        tail = "  (%s)" % (detail,)
    print("%-4s  %-3s %s%s" % (status, rule, name, tail))


def check(rule, name, ok, detail=""):
    emit("PASS" if ok else "FAIL", rule, name, detail)
    return bool(ok)


def na(rule, name, reason):
    emit("N/A", rule, name, reason)


def info(text):
    print("INFO  %s" % text)


def run(args, **kw):
    """subprocess.run with a time limit. A timeout gives returncode -1 and an empty stdout."""
    try:
        return subprocess.run(args, capture_output=True, text=True, timeout=kw.pop("timeout", TIMEOUT), **kw)
    except subprocess.TimeoutExpired:
        info("timeout: %s" % " ".join(args)[:120])
        return subprocess.CompletedProcess(args, -1, "", "timeout")
    except FileNotFoundError as e:
        info("command not found: %s" % e)
        return subprocess.CompletedProcess(args, -1, "", str(e))


def read(path):
    with open(path, encoding="utf8", errors="replace") as f:
        return f.read()


# ---------------------------------------------------------------------------------------------------------
# Files of a week. Only os.listdir: one directory level, no walk.

def week_dir(parent, week):
    """The directory WeekNN or weekNN in parent (any case), or None."""
    want = "week%02d" % week
    try:
        names = os.listdir(parent)
    except OSError:
        return None
    for name in sorted(names):
        if name.lower() == want and os.path.isdir(os.path.join(parent, name)):
            return os.path.join(parent, name)
    return None


def newest(folder, regex):
    """The name with the highest version that matches regex (group 1 = the version, or None for no version)."""
    best = None
    for name in os.listdir(folder) if folder and os.path.isdir(folder) else []:
        m = re.fullmatch(regex, name)
        if m:
            v = int(m.group(1)) if m.group(1) else 0
            if best is None or v > best[0]:
                best = (v, name)
    return best[1] if best else None


def load_spec(week):
    path = os.path.join(SPECS, "week%02d.py" % week)
    if not os.path.exists(path):
        return {}, None
    spec = runpy.run_path(path)
    return {k: v for k, v in spec.items() if k.isupper()}, path


# ---------------------------------------------------------------------------------------------------------
# Deck checks (B1 to B8, A1). The logic of deck_checks in gate_week12.py, with a rule for each check.

def paragraphs(prs):
    for no, slide in enumerate(prs.slides, 1):
        for sh in slide.shapes:
            if sh.has_text_frame:
                for p in sh.text_frame.paragraphs:
                    text = "".join(r.text for r in p.runs).strip()
                    if text:
                        yield no, sh, p, text


def is_mono(p):
    runs = [r for r in p.runs if r.text.strip()]
    return bool(runs) and all(r.font.name == "Consolas" for r in runs)


def fill_rgb(sh):
    """The hex RGB of a solid fill, or None (no fill, or a theme color with no .rgb)."""
    try:
        return str(sh.fill.fore_color.rgb) if sh.fill.type == 1 else None
    except (AttributeError, TypeError, ValueError):
        return None


def is_dark(sh, min_height=0.0):
    return (sh.shape_type == 1 and sh.has_text_frame and not sh.text_frame.text.strip() and sh.height / EMU > min_height
            and fill_rgb(sh) == "2A2A2A")


def words_of_page(pdf, page):
    """The words of one PDF page with their boxes in inches, or None when pdftotext fails."""
    r = run(["pdftotext", "-bbox", "-f", str(page), "-l", str(page), pdf, "-"], timeout=60)
    if r.returncode != 0:
        return None
    out = r.stdout
    found = re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>', out)
    return [(float(a) / 72, float(b) / 72, float(c) / 72, float(d) / 72, w) for a, b, c, d, w in found]


def deck_checks(folder, stem, kind, allowed_repeats=frozenset()):
    path, pdf = os.path.join(folder, stem + ".pptx"), os.path.join(folder, stem + ".pdf")
    label = kind + ": "
    if not os.path.exists(path):
        check("B8", label + "the deck exists", False, path)
        return None
    prs = Presentation(path)
    n = len(prs.slides)
    have_pdf = os.path.exists(pdf)
    check("B1", label + "canvas 13.333 x 7.5 in", round(prs.slide_width / EMU, 3) == 13.333 and prs.slide_height / EMU == 7.5)
    check("B1", label + "size near 1 MB", os.path.getsize(path) < 1500000)
    fonts = collections.Counter(r.font.name for s in prs.slides for sh in s.shapes if sh.has_text_frame
                                for p in sh.text_frame.paragraphs for r in p.runs if r.font.name)
    check("B1", label + ".pptx uses Calibri and Consolas only", set(fonts) <= {"Calibri", "Consolas"}, dict(fonts))
    if not have_pdf:
        check("B8", label + "the PDF exists", False, pdf)
    else:
        out = run(["pdffonts", pdf]).stdout.split("\n")[2:]
        used = {l.split()[0].split("+")[-1].split("-")[0] for l in out if l.strip()}
        check("B1", label + "PDF uses Calibri and Consolas only", used == {"Calibri", "Consolas"}, used)
        pages = re.search(r"Pages:\s+(\d+)", run(["pdfinfo", pdf]).stdout)
        check("B8", label + "PDF page count equals slide count", bool(pages) and pages.group(1) == str(n),
              pages and pages.group(1))
        check("B8", label + "PDF is newer than the .pptx", os.path.getmtime(pdf) >= os.path.getmtime(path))
    footer, whale, band, top, off, dpi, small, mono_size, hidden, notes = [], [], [], [], [], [], [], [], [], []
    for no, s in enumerate(prs.slides, 1):
        if s._element.get("show") == "0":
            hidden.append(no)
        if s.has_notes_slide:
            notes.append(no)
        marks = [sh.text_frame.text for sh in s.shapes if sh.has_text_frame and "CLO835, Fall 2026" in sh.text_frame.text]
        if marks != ["CLO835, Fall 2026     %d / %d" % (no, n)]:
            footer.append((no, marks))
        pics = [sh for sh in s.shapes if sh.shape_type == 13]
        if not [sh for sh in pics if abs(sh.width / EMU - 0.5) < 0.02 and abs(sh.top / EMU - 6.85) < 0.02]:
            whale.append(no)
        for sh in pics:
            image = Image.open(io.BytesIO(sh.image.blob))
            if image.size[0] / (sh.width / EMU) < 110:
                dpi.append(no)
        for sh in s.shapes:
            t, b = sh.top / EMU, (sh.top + sh.height) / EMU
            if sh.left < 0 or sh.top < 0 or sh.left + sh.width > prs.slide_width or sh.top + sh.height > prs.slide_height:
                off.append((no, sh.name))
            if b > 6.705 and t < 6.8 and sh.shape_type != 13:
                band.append((no, sh.name, round(b, 2)))
            if no > 1 and 0.3 < t < 1.42 and sh.name != "TextBox 1" and sh.shape_type != 9 and sh.height > 0:
                top.append((no, sh.name, round(t, 2)))
    for no, sh, p, text in paragraphs(prs):
        if sh.top / EMU > 6.8:
            continue
        sizes = [r.font.size.pt for r in p.runs if r.text.strip() and r.font.size]
        if is_mono(p):
            over_dark = any(d.shape_type == 1 and d.has_text_frame and not d.text_frame.text.strip() and d.top <= sh.top
                            and d.left <= sh.left and fill_rgb(d) == "2A2A2A"
                            for d in prs.slides[no - 1].shapes)
            mono_size += [(no, z) for z in sizes if over_dark and (z < 9 or z > 14)]
        elif sizes and min(sizes) < 12:
            bar = sh.height / EMU < 0.35 and min(sizes) == 10
            if not bar:                  # B3: the Course Outline slide uses 12 pt, so no 10.5 pt exemption
                small.append((no, min(sizes), text[:40]))
    check("B1", label + "footer N / TOTAL on every slide", not footer, footer[:3])
    check("B1", label + "whale on every slide", not whale, whale)
    check("B1", label + "no shape off the canvas", not off, off)
    check("B1", label + "no shape in the footer band", not band, band)
    check("B1", label + "no shape on the title band", not top, top)
    check("B6", label + "no image below 110 DPI", not dpi, dpi)
    check("B1", label + "no hidden slide (source has none)", not hidden, hidden)
    check("B1", label + "no speaker notes", not notes, notes)
    check("B3", label + "body text at least 12 pt", not small, small[:8])
    check("B3", label + "terminal text 9 to 14 pt", not mono_size, mono_size[:8])
    titles = collections.Counter(sh.text_frame.text for s in prs.slides for sh in s.shapes
                                 if sh.has_text_frame and sh.name == "TextBox 1")
    check("B7", label + "no duplicate title", max(titles.values()) == 1 if titles else True, titles.most_common(2))
    repeat = collections.defaultdict(set)
    for no, sh, p, text in paragraphs(prs):
        key = re.sub(r"^[▪–•\-]+\s*", "", text).strip().lower()
        bullet = text[0] in "▪–•"
        if not is_mono(p) and (bullet or len(key) > 12) and "clo835" not in key and sh.height / EMU >= 0.35:
            repeat[key].add(no)
    allowed = ALLOWED_REPEATS | set(allowed_repeats)
    same = {k: sorted(v) for k, v in repeat.items() if len(v) > 1 and k not in allowed}
    check("B7", label + "no bullet word for word on two slides", not same, same)
    bad = [(no, text[:50]) for no, sh, p, text in paragraphs(prs) if is_mono(p) and re.search(r"[^\x00-\x7f]", text)]
    check("B5", label + "no non-ASCII character in Consolas text", not bad, bad[:4])
    bad = [(no, b, text[:50]) for no, sh, p, text in paragraphs(prs) for b in BANNED if not is_mono(p) and re.search(b, text)]
    check("A1", label + "no replaced word in the text", not bad, bad[:6])
    bad = [(no, text[:50]) for no, sh, p, text in paragraphs(prs) if not is_mono(p) and CONTRACTION.search(text)]
    check("A1", label + "no contraction", not bad, bad[:4])
    bad = [(no, text[:50]) for no, sh, p, text in paragraphs(prs) if not is_mono(p)
           and re.search(r"\b[2-9][ -](methods?|steps?|files?|ways?|entries|sections?|step)\b", text)]
    check("A1", label + "small numbers in words", not bad, bad[:4])
    bad = [(no, text[:50]) for no, sh, p, text in paragraphs(prs) if is_mono(p) and text.startswith("kubectl ")]
    check("B5", label + "each command starts with $", not bad, bad[:4])
    bad = [(no, len(s.split()), s[:50]) for no, sh, p, text in paragraphs(prs) if not is_mono(p)
           for s in re.split(r"(?<=[.:])\s", text) if len(s.split()) > 25]
    check("A1", label + "no sentence above 25 words", not bad, bad[:4])
    bad = [(no, text[:50]) for no, sh, p, text in paragraphs(prs) if re.search(r"busybox|luksa|nano\b|/Users/|\.ssh/", text)]
    check("F2", label + "no banned image, editor or private path", not bad, bad[:4])
    zf = zipfile.ZipFile(path)
    floats, colors, media, buchar, zero = 0, collections.Counter(), [], [], []
    order = {}
    for k, s in enumerate(prs.slides, 1):
        order[s.part.partname.lstrip("/")] = k
    for name in zf.namelist():
        if re.match(r"ppt/slides/slide\d+\.xml", name):
            xml = zf.read(name).decode()
            floats += len(re.findall(r'(?:\bx|\by|cx|cy|marL|indent)="-?\d+\.\d+"', xml))
            colors.update(c.upper() for c in re.findall(r'srgbClr val="([0-9A-Fa-f]{6})"', xml))
            if re.search(r'<a:buChar char="▪"', xml):
                buchar.append(order.get(name, name))
            for cxn in re.findall(r"<p:cxnSp>.*?</p:cxnSp>", xml, re.S):
                arrow = re.search(r'<a:(?:head|tail)End type="(?!none)', cxn)
                flat = re.search(r'<a:ext cx="0"|<a:ext cx="\d+" cy="0"', cxn)
                if re.search(r'<a:ext cx="0" cy="0"/>', cxn) or (arrow and flat):
                    zero.append(order.get(name, name))
        if "/media/" in name:
            media.append(name)
    check("B1", label + "0 float coordinates", floats == 0, floats)
    check("B2", label + "palette only", set(colors) <= PALETTE, set(colors) - PALETTE)
    check("B1", label + "only the logo and the whale as images", len(media) <= 2, media)
    check("B1", label + "no blank thumbnail", "docProps/thumbnail.jpeg" not in zf.namelist())
    core = prs.core_properties
    check("B1", label + "file title and author set", bool(core.title) and core.author == "Maziar Sojoudian"
          and core.last_modified_by == "Maziar Sojoudian", (core.title, core.author, core.last_modified_by))
    check("B4", label + "no a:buChar bullet with the glyph of B4 (PowerPoint for Mac does not show it)", not buchar,
          sorted(set(buchar), key=str))
    check("B6", label + "no connector with zero extent, and no horizontal or vertical arrow drawn as a connector", not zero,
          sorted(set(zero), key=str))
    if have_pdf:
        # Terminals on the page that PowerPoint rendered: no wrapped line, no text past the dark box.
        wraps, past, failed = [], [], []
        for no, s in enumerate(prs.slides, 1):
            words = words_of_page(pdf, no)
            if words is None:
                failed.append(no)
                continue
            darks = [sh for sh in s.shapes if is_dark(sh, 0.5)]
            for d in darks:
                l, r, t, b = d.left / EMU, (d.left + d.width) / EMU, d.top / EMU, (d.top + d.height) / EMU
                boxes = [sh for sh in s.shapes if sh.has_text_frame and sh.text_frame.text.strip() and l <= sh.left / EMU
                         and (sh.left + sh.width) / EMU <= r + 0.01 and t <= sh.top / EMU <= b
                         and any(x.font.name == "Consolas" for p in sh.text_frame.paragraphs for x in p.runs)]
                expect = sum(1 for sh in boxes for p in sh.text_frame.paragraphs if p.text.strip())
                inside = [w for w in words if l <= w[0] < r and t + 0.33 <= (w[1] + w[3]) / 2 <= b + 0.12]
                rows = sorted({round((w[1] + w[3]) / 2, 1) for w in inside})
                if boxes and len(rows) > expect:
                    wraps.append((no, d.name, len(rows), expect))
                for w in inside:
                    if boxes and (w[3] > b or w[2] > r):
                        past.append((no, w[4]))
        why = "pdftotext failed on pages %s" % failed[:5]
        check("B5", label + "no wrapped terminal line in the rendered PDF", not wraps and not failed, wraps[:5] or why)
        check("B5", label + "no text past a terminal box in the rendered PDF", not past and not failed, past[:5] or why)
    return prs


# ---------------------------------------------------------------------------------------------------------
# Lecture checks (B7, C8)

def steps(script):
    """{n: the text of Step n}, from the "# Step n - " headers of the script."""
    parts = re.split(r"^# Step (\d+) - .*$", script, flags=re.M)
    return {int(parts[k]): parts[k + 1] for k in range(1, len(parts), 2)}


def command_lines(text):
    return [l for l in text.split("\n") if l.strip() and not l.lstrip().startswith("#")]


def comment_lines(text):
    return [l for l in text.split("\n") if l.lstrip().startswith("#")]


def heredocs(script):
    """{file name: body lines} of each cat > file <<EOF block."""
    return {m.group(1): m.group(2).split("\n")
            for m in re.finditer(r"^cat > (\S+) <<'?EOF'?\n(.*?)\nEOF$", script, re.M | re.S)}


def joined(lines):
    """Lines with each backslash continuation joined, in a normal form: one space, no end comment."""
    out, cur = [], ""
    for l in lines:
        part = l.strip()
        if cur:
            cur += " " + part
        else:
            cur = part
        if cur.endswith("\\"):
            cur = cur[:-1].rstrip()
            continue
        out.append(re.sub(r"\s+", " ", re.sub(r"\s+#\s.*$", "", cur)).strip())
        cur = ""
    if cur:
        out.append(re.sub(r"\s+", " ", cur).strip())
    return out


def terminals(slide):
    """(label, body lines) of each terminal of a slide: a dark 2A2A2A box, the text on its bar, the text in it."""
    shapes = list(slide.shapes)
    out = []
    for d in shapes:
        if not is_dark(d, 0.5):
            continue
        l, r, t, b = d.left / EMU, (d.left + d.width) / EMU, d.top / EMU, (d.top + d.height) / EMU
        label = [sh.text_frame.text for sh in shapes if sh.has_text_frame and sh.text_frame.text.strip()
                 and abs(sh.top / EMU - t) < 0.12 and l - 0.01 <= sh.left / EMU < r and sh.height / EMU <= 0.4]
        body = [p.text for sh in shapes if sh.has_text_frame and sh.text_frame.text.strip()
                and l - 0.01 <= sh.left / EMU and (sh.left + sh.width) / EMU <= r + 0.01 and t + 0.3 <= sh.top / EMU <= b
                for p in sh.text_frame.paragraphs]
        out.append((" ".join(label), body))
    return out


def label_steps(label):
    """[(week, step), ...] of a label such as "Lab Week 10, Step 4", "Lab Week 10, Steps 4 and 5",
    "Steps 4-5", "Steps 4 to 6" or "Step 4 and Step 5". None for a "Lab Week" label with no step."""
    m = re.search(r"(?i)Lab Week (\d+)\s*[,\-–]?\s*(Steps?)\s+(\d[^)]*)", label)
    if not m:
        return None if re.search(r"(?i)Lab Week \d+", label) else []
    week, plural, rest = int(m.group(1)), m.group(2).lower() == "steps", m.group(3)
    if plural:
        r = re.match(r"\s*(\d+)\s*(?:-|–|to)\s*(\d+)\b", rest)
        if r:
            return [(week, x) for x in range(int(r.group(1)), int(r.group(2)) + 1)]
        nums = re.findall(r"(?:^|,|&|\band\b|\bor\b)\s*(\d+)\b", rest)
    else:
        nums = [re.match(r"\d+", rest).group(0)] + re.findall(r"(?i)(?:\band\b|&|\bor\b)\s+(?:step\s+)?(\d+)\b", rest)
    return [(week, int(x)) for x in nums]


def week_files(folder, script=True):
    """{file name: lines} of the files that a lab puts on the master: the heredocs of localMachine.sh (when
    script is True), the cat > /home/ubuntu/FILE blocks of master-init.sh.tftpl, and the extra files of the repo
    folder (C5). A link or an entry that is not a regular file is not read."""
    out = {}
    if not folder or not os.path.isdir(folder):
        return out
    path = os.path.join(folder, "localMachine.sh")
    if script and os.path.isfile(path):
        out.update(heredocs(read(path)))
    master = os.path.join(folder, "master-init.sh.tftpl")
    if os.path.exists(master):
        for m in re.finditer(r"^cat > /home/ubuntu/(\S+) <<'?(\w+)'?\n(.*?)\n\2$", read(master), re.M | re.S):
            out.setdefault(m.group(1), m.group(3).split("\n"))
    for name in os.listdir(folder):
        f = os.path.join(folder, name)
        if (name not in REPO_FILES and re.search(r"\.(ya?ml|json)$", name) and os.path.isfile(f)
                and not os.path.islink(f)):
            out.setdefault(name, read(f).rstrip("\n").split("\n"))
    return out


FILE_RE = r"([\w.-]+\.(?:ya?ml|json|conf))\b"


def part_of(body, doc):
    """True when the lines of body are a block of the lines of doc, line for line."""
    lines, doc = [x.rstrip() for x in body], [x.rstrip() for x in doc]
    return bool(doc) and bool(lines) and any(doc[k:k + len(lines)] == lines for k in range(len(doc) - len(lines) + 1))


def own_machine(text):
    """The commands of your own machine: the "# ON YOUR OWN MACHINE:  cmd" comment lines of a step."""
    return [l.split(":", 1)[1] for l in text.split("\n") if l.startswith("# ON YOUR OWN MACHINE:")]


def lecture_checks(prs, week, stem, repo=None):
    titles = [" ".join(sh.text_frame.text.split()) for s in prs.slides for sh in s.shapes
              if sh.has_text_frame and sh.name == "TextBox 1"]
    for want in ("Agenda", "Course Outline", "Optional Topics", "Key Takeaways", "Lab Week %02d at a Glance" % week):
        check("B7", "lecture: has the slide %s" % want, want in titles)
    scripts, extra, missing = {}, {}, []
    bad_cmd, bad_file, bad_step, nothing, no_step, labeled = [], [], [], [], [], 0
    own = week_files(repo)              # every file of this week: an unlabeled terminal can show one of them
    for no, s in enumerate(prs.slides, 1):
        terms = terminals(s)
        slide_files = [m.group(1) for label, _ in terms for m in [re.search(FILE_RE, label)] if m]
        for label, body in terms:
            pairs = label_steps(label)
            fm = re.search(FILE_RE, label)
            commands = _command_blocks(body)
            if pairs is None:
                no_step.append((no, label[:60]))
                continue
            if not pairs:
                if fm and fm.group(1) in own and not commands and not part_of(body, own[fm.group(1)]):
                    bad_file.append((no, fm.group(1)))
                continue
            labeled += 1
            allowed, docs, usable = set(), {}, True
            for w, m in pairs:
                if w not in scripts:
                    folder = repo if (w == week and repo) else week_dir(COURSE_REPO, w)
                    extra[w] = week_files(folder, script=False)
                    path = os.path.join(folder, "localMachine.sh") if folder else None
                    scripts[w] = read(path) if path and os.path.isfile(path) else None
                    if scripts[w] is None:
                        missing.append(w)
                if scripts[w] is None:
                    usable = False
                    continue
                st = steps(scripts[w])
                if m not in st:
                    bad_step.append((no, "Lab Week %02d, Step %d" % (w, m)))
                    continue
                allowed |= set(joined(command_lines(st[m]))) | set(joined(own_machine(st[m])))
                docs.update(extra[w])
                docs.update(heredocs(st[m]))     # only the files of the named step, not of the whole script
            if not usable:
                continue
            bad_cmd += [(no, c[:70]) for c in commands if c not in allowed]
            for fname, lines in terminal_heredocs(body):
                if not part_of(lines, docs.get(fname, [])) and lines:
                    bad_file.append((no, fname))
            name = fm.group(1) if fm else None
            if not name and not commands:
                # The second part of a file that the other terminal of the slide names ("lines 14 to 26").
                name = next((f for f in slide_files if f in docs), None)
            if commands:
                continue                         # a terminal with commands is compared by its commands
            if name:
                if not part_of(body, docs.get(name, [])):
                    bad_file.append((no, name))
            else:
                nothing.append((no, label[:50]))
    if no_step:
        info("C8: terminal labels that name Lab Week NN with no step, so nothing was compared: %s" % no_step[:6])
    if labeled == 0:
        na("C8", "lecture: each command of a terminal labeled Lab Week NN, Step M is in that lab step",
           "the lecture has no terminal with such a label")
        check("C8", "lecture: each file of a terminal is a part of the lab file, line for line", not bad_file, bad_file[:5])
        return
    check("C8", "lecture: the repo script of each week that a terminal label names exists", not missing, missing)
    check("C8", "lecture: each step that a terminal label names is a step of the lab script", not bad_step, bad_step[:5])
    check("C8", "lecture: each command of a terminal labeled Lab Week NN, Step M is in that lab step (%d terminals)"
          % labeled, not bad_cmd, bad_cmd[:5])
    check("C8", "lecture: each file of a terminal is a part of the lab file, line for line", not bad_file, bad_file[:5])
    check("C8", "lecture: each labeled terminal shows a command or a part of a lab file", not nothing, nothing[:5])

def terminal_heredocs(body):
    """[(file, lines)] of each "$ cat > FILE <<EOF" block of a terminal body, up to the EOF line or the end."""
    out, cur = [], None
    for x in body:
        m = re.match(r"^(?:L\$|\$) cat > (\S+) <<-?\s*['\"]?(\w+)['\"]?\s*$", x)
        if cur is None and m:
            cur = (m.group(1), m.group(2), [])
        elif cur is not None:
            if x.strip() == cur[1]:
                out.append((cur[0], cur[2]))
                cur = None
            else:
                cur[2].append(x)
    if cur is not None:
        out.append((cur[0], cur[2]))
    return out


def _command_blocks(body):
    """The commands of a terminal body: each "$ " line and its continuation lines."""
    out, cur = [], None
    for x in body:
        m = re.match(r"^(?:L\$|\$|[\w.-]+@[\w.-]+:\S*\$) (.*)$", x)
        if m:
            if cur is not None:
                out.append(cur)
            cur = [m.group(1)]
            if not x.rstrip().endswith("\\"):
                out.append(cur)
                cur = None
        elif cur is not None:
            cur.append(x)
            if not x.rstrip().endswith("\\"):
                out.append(cur)
                cur = None
    if cur is not None:
        out.append(cur)
    return [c for block in out for c in joined(block)]


# ---------------------------------------------------------------------------------------------------------
# Lab checks (C1 to C6, C9, F2, F3)

def runner(script_path):
    return run([sys.executable, "-I", INSTRUMENT, script_path, "https://none/"]).stdout


def prose(body):
    """The text of a script or a Terraform file that a person reads: the comments, the description fields, the
    echo texts and the message of the day. The Flannel manifest of master-init is not prose."""
    body = re.sub(r"<<'MANIFEST'\n.*?\nMANIFEST\n", "", body, flags=re.S)
    out = [l.strip() for l in body.split("\n") if l.lstrip().startswith("#") and not l.startswith("#!")]
    out += re.findall(r'description\s*=\s*"([^"]*)"', body)
    out += re.findall(r'echo "([^"$]*)"', body)
    out += [m for m in re.findall(r"<<'MOTD'\n(.*?)\nMOTD", body, re.S)]
    return "\n".join(out)


def allowed_image(image):
    """C3 and F2: an image of Docker Hub maziar, a Docker Official Image, or an image of registry.k8s.io."""
    name = re.sub(r"^docker\.io/", "", image)
    first = name.split("/")[0]
    if "/" in name and ("." in first or ":" in first or first == "localhost"):
        return first == "registry.k8s.io"            # another registry
    return name.startswith("maziar/") or name.startswith("library/") or "/" not in name


def docker_lab_checks(ctx):
    """Weeks 01 to 03 are Docker labs (G3). The kubeadm lab checks of C1 to C6 do not apply to them."""
    week, repo = ctx["week"], ctx["repo"]
    names = sorted(x for x in os.listdir(repo) if x not in (".terraform", ".DS_Store"))
    na("C1", "lab: the kubeadm lab checks of C1 to C6 and C9", "Week %02d is a Docker lab (G3), not a kubeadm lab" % week)
    check("C5", "lab: no .terraform directory in the repo folder (C5)", not os.path.exists(os.path.join(repo, ".terraform")))
    check("C5", "lab: no state or key file", not [x for x in names if re.search(r"tfstate|tfvars|\.pem|\.key$", x)])
    for f in names:
        if f.endswith(".sh"):
            check("C5", "lab: bash -n " + f, run(["bash", "-n", os.path.join(repo, f)]).returncode == 0)
    files = [x for x in names if os.path.isfile(os.path.join(repo, x))]
    text = "".join(read(os.path.join(repo, x)) for x in files)
    scan = (r"/Users/|\.ssh/|173\.33\.124\.240|sojodyan|" + ACCOUNT + r"|@gmail|mazSeneca|"
            r"AKIA|ASIA[0-9A-Z]{8}|luksa|busybox|\bnano\b")
    bad = [m.group(0) for m in re.finditer(scan, text)]
    check("F3", "lab: repo scan (F3)", not bad, bad[:5])
    images = sorted(set(i for x in files for i in docker_images(read(os.path.join(repo, x)))))
    check("F2", "lab: images of maziar or Docker Official Images only (C3, F2)",
          all(allowed_image(i) for i in images), [i for i in images if not allowed_image(i)] or images)
    if [x for x in files if x.endswith(".tf")]:
        check("C5", "lab: terraform fmt", run(["terraform", "-chdir=" + repo, "fmt", "-check"],
                                              env=dict(os.environ, CHECKPOINT_DISABLE="1")).returncode == 0)
    return None


DOCKER_VALUE_OPTIONS = {"-p", "--publish", "-e", "--env", "-v", "--volume", "--name", "--network", "--net", "-w", "--workdir",
                        "--entrypoint", "--mount", "-u", "--user", "--env-file", "--restart", "-h", "--hostname", "-l",
                        "--label", "--memory", "-m", "--cpus", "--platform", "--ip", "--dns", "--add-host", "--link"}


def docker_images(text):
    """The images of a Docker lab: docker pull IMAGE, docker run [options] IMAGE, FROM IMAGE and image: lines."""
    out = []
    for line in command_lines(text):
        words = line.strip().split()
        for k in range(len(words) - 1):
            if words[k] == "docker" and words[k + 1] in ("pull", "run"):
                rest, j = words[k + 2:], 0
                while j < len(rest) and rest[j].startswith("-"):
                    j += 2 if rest[j] in DOCKER_VALUE_OPTIONS else 1
                if j < len(rest) and re.fullmatch(r"[\w./:@-]+", rest[j]) and not rest[j].startswith("$"):
                    out.append(rest[j])
        m = re.match(r"^\s*FROM\s+(\S+)", line)
        if m and m.group(1) != "scratch":
            out.append(m.group(1))
        m = re.match(r"^\s*(?:- )?image:\s*['\"]?([^'\"\s]+)", line)
        if m:
            out.append(m.group(1))
    return out


def set_images(commands):
    """The images of each "kubectl set image TYPE/NAME name=image ..." or "TYPE NAME name=image ..." line."""
    out = []
    for line in commands.split("\n"):
        m = re.search(r"\bset image\s+(.*)$", line)
        if m:
            for word in re.sub(r"\s+#.*$", "", m.group(1)).split():
                if "=" in word and not word.startswith("-"):
                    out.append(word.split("=", 1)[1].strip("'\""))
    return out


def other_weeks(week):
    """A pattern for the name of each week 01 to 19 other than this week."""
    others = "|".join("%02d" % w for w in range(1, 20) if w != week)
    return r"(?<![A-Za-z])[Ww]eek ?(%s)\b" % others      # also week11 in Lab_week11.pptx


def lab_checks(ctx):
    week, spec, repo, wdir, lab = ctx["week"], ctx["spec"], ctx["repo"], ctx["wdir"], ctx["lab"]
    nn = "%02d" % week
    topic = spec.get("TOPIC")
    script_path = os.path.join(repo, "localMachine.sh")
    if week < KUBEADM_FROM:
        return docker_lab_checks(ctx)
    if not os.path.exists(script_path):
        check("C5", "lab: localMachine.sh in the repo folder", False, script_path)
        return None
    run_text = runner(script_path)
    count = run_text.count('echo "@@CMD')
    check("C1", "lab: at most 40 commands on the master (%d)" % count, count <= 40, count)
    script = read(script_path)
    check("C1", "lab: Step 0 to Step 6, and Step 6 has no command on the master",
          re.findall(r"@@STEP (\d)", run_text) == list("012345") and re.findall(r"^# Step (\d) - ", script, re.M) == list("0123456"),
          (re.findall(r"@@STEP (\d)", run_text), re.findall(r"^# Step (\d) - ", script, re.M)))
    st = steps(script)
    six = script.split("# Step 6 - ")[1].split("\n")[3:] if "# Step 6 - " in script else []
    check("C1", "lab: Step 6 holds only terraform destroy and the C1 comment",
          bool(six) and [l for l in six if l.strip() and not l.startswith("#")] == [] and "terraform destroy" in "\n".join(six)
          and ALSO in six, six)
    check("C2", "lab: each step names its slide", re.findall(r"# Step (\d) - .*\(slide (\d+)\)", script)
          == [(str(i), str(i + 3)) for i in range(7)])
    check("C2", "lab: Step 0 has the title of slide 3", "# Step 0 - Build and check the cluster          (slide 3)" in script)
    deck_script = os.path.join(wdir, lab.replace("Lab_week%s" % nn, "localMachine") + ".sh") if lab else None
    check("C2", "lab: the repo script equals the deck script", bool(deck_script) and os.path.exists(deck_script)
          and script == read(deck_script), deck_script)
    check("C2", "lab: the script header names the deck (M27)", bool(lab) and "# Each step matches one slide of %s.pptx." % lab in script)
    lines = script.split("\n")
    if topic:
        head = [h.replace("{NN}", nn).replace("{TOPIC}", topic) for h in HEAD]
        check("C2", "lab: the script head of Week 12 round 9 (round 3, MUST-FIX 2)", lines[1:3] == head[:2]
              and head[2] in lines[:6], lines[1:6])
    else:
        na("C2", "lab: the script head of Week 12 round 9 (round 3, MUST-FIX 2)", "no TOPIC in the spec")
    tail = [l for l in script.split("# Step 6 - ")[1].split("\n")[2:] if l.strip()] if "# Step 6 - " in script else []
    check("C2", "lab: Step 6 of the script is STEP6 of Week 12 v7 (C2; round 3, MUST-FIX 3)",
          tail == [STEP6[0], ALSO, "# ON YOUR OWN MACHINE:  " + STEP6[2][2:], STEP6[3]], tail)
    check("F1", "lab: Step 0 has git fetch and git reset --hard origin/master (M19, S22)",
          "# ON YOUR OWN MACHINE:  cd CLO835_Fall_2026 && git fetch && git reset --hard origin/master" in st.get(0, "")
          and "# ON YOUR OWN MACHINE:  cd Week%s && terraform init" % nn in st.get(0, "") and "git pull" not in script)
    names = sorted(x for x in os.listdir(repo) if x not in (".terraform", ".DS_Store"))   # .gitignore ignores both
    check("C5", "lab: no .terraform directory in the repo folder (C5)", not os.path.exists(os.path.join(repo, ".terraform")))
    extra = spec.get("EXTRA_REPO_FILES")
    found = [x for x in names if x not in REPO_FILES]
    if extra is not None:
        check("C5", "lab: 7 files and the extras %s" % list(extra) if extra else "lab: 7 files",
              names == sorted(REPO_FILES + list(extra)), names)
    elif not found:
        check("C5", "lab: 7 files", names == sorted(REPO_FILES), names)
    else:
        check("C5", "lab: the 7 files of C5 are in the repo folder", all(x in names for x in REPO_FILES),
              [x for x in REPO_FILES if x not in names])
        na("C5", "lab: the extra files of the week", "no EXTRA_REPO_FILES in the spec; the folder also holds %s" % found)
    check("C5", "lab: no state or key file", not [x for x in os.listdir(repo) if re.search(r"tfstate|tfvars|\.pem|\.key$", x)])
    check("C5", "lab: no README in the repo folder (C5)", not [x for x in names if x.lower().startswith("readme")],
          [x for x in names if x.lower().startswith("readme")])
    for f in ("localMachine.sh", "bootstrap.sh", "master-init.sh.tftpl", "worker-join.sh.tftpl"):
        if os.path.exists(os.path.join(repo, f)):
            check("C5", "lab: bash -n " + f, run(["bash", "-n", os.path.join(repo, f)]).returncode == 0)
        else:
            check("C5", "lab: bash -n " + f, False, "no file")
    check("C5", "lab: terraform fmt", run(["terraform", "-chdir=" + repo, "fmt", "-check"],
                                          env=dict(os.environ, CHECKPOINT_DISABLE="1")).returncode == 0)
    files = [x for x in names if os.path.isfile(os.path.join(repo, x))]
    text = "".join(read(os.path.join(repo, x)) for x in files)
    scan = (r"/Users/|\.ssh/|173\.33\.124\.240|sojodyan|" + spec.get("SCAN_ACCOUNT", ACCOUNT) + r"|@gmail|mazSeneca|"
            r"AKIA|ASIA[0-9A-Z]{8}|luksa|busybox|\bnano\b|flannel-io|ghcr\.io|" + spec.get("OTHER_WEEKS", other_weeks(week)))
    bad = [m.group(0) for m in re.finditer(scan, text)]
    check("F3", "lab: repo scan (F3, other weeks)", not bad, bad[:5])
    master = read(os.path.join(repo, "master-init.sh.tftpl")) if os.path.exists(os.path.join(repo, "master-init.sh.tftpl")) else ""
    check("C5", "lab: no cleanup script or cleanup text in the repo folder", not re.search(r"cleanup|clean[ -]up", text, re.I))
    commands = "\n".join(command_lines(script))
    images = sorted(set(i.strip("'\"") for i in re.findall(r"(?:^\s*(?:- )?image:\s*|--image=)(\S+)", script, re.M))
                    | set(i.strip("'\"") for i in re.findall(r"--image (\S+)", commands)) | set(set_images(commands)))
    if spec.get("MAZIAR_ONLY"):
        check("F2", "lab: images of maziar only", bool(images) and all(i.startswith("maziar/") for i in images), images)
    else:
        check("F2", "lab: images of maziar or Docker Official Images only (C3, F2)",
              bool(images) and all(allowed_image(i) for i in images), [i for i in images if not allowed_image(i)] or images)
    check("C3", "lab: no maziar/curl and no busybox helper image (C3)",
          "maziar/curl" not in images and not [i for i in images if "busybox" in i], images)
    if spec.get("HELPER_IMAGE"):
        check("C3", "lab: the helper image is %s (M26)" % spec["HELPER_IMAGE"], spec["HELPER_IMAGE"] in images and "maziar/curl" not in images,
              images)
    master_images = re.findall(r"^\s*image:\s*(\S+)", master, re.M)
    if spec.get("MAZIAR_ONLY"):
        # The exact form of gate_week12.py and gate_week13_v3.py: master-init holds 3 images, all of maziar.
        check("F2", "lab: Flannel images of maziar only", len(master_images) == 3 and all(i.startswith("maziar/") for i in master_images),
              master_images)
    else:
        flannel = [i for i in master_images if "flannel" in i]
        check("F2", "lab: Flannel images of maziar only", len(flannel) == 3 and all(i.startswith("maziar/") for i in flannel),
              flannel or "no Flannel image in master-init.sh.tftpl (the flannel-io manifest URL of H8?)")
    extra_images = [i for x in files if x not in REPO_FILES and re.search(r"\.(ya?ml|json)$", x)
                    for i in re.findall(r"^\s*(?:- )?image:\s*(\S+)", read(os.path.join(repo, x)), re.M)]
    others = [i for i in master_images + extra_images if not re.sub(r"^docker\.io/", "", i.strip("\"'")).startswith("maziar/")]
    check("F2", "lab: each image of master-init.sh.tftpl and of the extra repo files is of maziar (F2)", not others, others)
    if topic:
        check("C6", "lab: the message of the day names Week %s, the MASTER node and localMachine.sh" % nn,
              "CLO835 - Week %s - %s" % (nn, topic) in master and "You are on the MASTER node." in master
              and "localMachine.sh" in master)
    else:
        na("C6", "lab: the message of the day names the week, the MASTER node and localMachine.sh", "no TOPIC in the spec")
    variables = read(os.path.join(repo, "variables.tf")) if os.path.exists(os.path.join(repo, "variables.tf")) else ""
    key = re.search(r'variable "key_name" \{(.*?)\n\}', variables, re.S)
    profile = re.search(r'variable "lab_instance_profile" \{(.*?)\n\}', variables, re.S)
    check("C5", "lab: key_name has no default; lab_instance_profile defaults to LabInstanceProfile",
          bool(key) and bool(profile) and "default" not in key.group(1)
          and re.search(r'default\s*=\s*"LabInstanceProfile"', profile.group(1)) is not None)
    heads = re.findall(r"^(\S.*<<'?EOF'?)$", script, re.M)
    unquoted = spec.get("UNQUOTED_EOF", {})
    any_heads = [l for l in command_lines(script) if re.search(r"<<-?\s*['\"]?\w+", l)]
    wrong = [h for h in any_heads if not re.fullmatch(r"cat > \S+ <<'EOF'", h)
             and not any(h == "cat > %s <<EOF" % f for f in unquoted)]
    check("C3", "lab: each manifest is written with cat > file <<'EOF' (C3, M24)",
          not wrong and not re.search(r"^tee ", script, re.M), wrong)
    if "HEREDOC_HEADS" in spec:
        name, want = spec["HEREDOC_HEADS"]
        check("C3", "lab: " + name, heads == want and not re.search(r"^tee ", script, re.M), heads)
    for f, comment in unquoted.items():
        before = script.split("cat > %s <<EOF" % f)[0].rstrip("\n").split("\n")[-1]
        name = "lab: a comment gives the reason for the unquoted EOF (M25)"
        check("C3", name if len(unquoted) == 1 else name + " of " + f, before == comment, before)
    for name, k, line in spec.get("STEP_COMMANDS", []):
        check("C3", "lab: " + name, line in command_lines(st.get(k, "")))
    if "OBJECTS" in spec:
        missing = [o for o, needle in spec["OBJECTS"].items() if needle not in script]
        check("C3", "lab: each object keeps its name", not missing, missing)
    else:
        na("C3", "lab: each object keeps its name", "no OBJECTS in the spec")
    bb = ctx.get("blackboard_path")
    texts = {x: prose(read(os.path.join(repo, x))) for x in files}
    if bb and os.path.exists(bb):
        texts["Blackboard text"] = read(bb)
    a1 = A1 + list(spec.get("A1_EXTRA", []))
    bad = [(name, b, m.group(0)) for name, body in texts.items() for b in a1 for m in [re.search(b, body)] if m]
    check("A1", "lab: A1 words in the comments of the script and the repo files, and in the Blackboard text", not bad, bad[:6])
    if spec.get("DENIALS"):
        check("C9", "lab: the planned denials are lines of the script", all(d in script.split("\n") for d in spec["DENIALS"]),
              [d for d in spec["DENIALS"] if d not in script.split("\n")])
    versions = sorted(set(re.findall(r"v1\.35\.\d+", script)))
    check("C4", "lab: the sample version is %s" % SAMPLE_VERSION, versions in ([], [SAMPLE_VERSION]), versions)
    base = spec.get("REPO_BASE")
    if base:
        bweek, btopic = base
        bdir = week_dir(COURSE_REPO, bweek)
        diffs = []
        t_old, t_new = "CLO835 - Week %02d - %s" % (bweek, btopic), "CLO835 - Week %s - %s" % (nn, topic)
        base_files = [x for x in os.listdir(bdir) if os.path.isfile(os.path.join(bdir, x)) and not re.search(IGNORED, x)] if bdir else []
        for x in sorted(set(files) | set(base_files)):
            if x == "localMachine.sh":
                continue
            p = os.path.join(bdir, x) if bdir else ""
            if not os.path.exists(p):
                diffs.append((x, "not in Week %02d" % bweek))
                continue
            if not os.path.exists(os.path.join(repo, x)):
                diffs.append((x, "not in Week %s" % nn))
                continue
            a = read(p).replace("  %s\n  %s\n" % (t_old, "-" * len(t_old)), "  %s\n  %s\n" % (t_new, "-" * len(t_new)))
            for o, n in (("Week%02d" % bweek, "Week" + nn), ("week%02d" % bweek, "week" + nn), ("Week %02d" % bweek, "Week " + nn)):
                a = a.replace(o, n)
            b = read(os.path.join(repo, x))
            if a != b:
                diffs.append((x, [l for l in b.split("\n") if l not in a.split("\n")][:2]))
        check("C5", "lab: the repo text equals the Week %d repo text, except the week name and the topic (C5)" % bweek,
              not diffs, diffs)
    else:
        na("C5", "lab: the repo text equals the repo text of the model week, except the week name and the topic",
           "no REPO_BASE in the spec")
    return script


def lab_deck_checks(ctx, script):
    week, spec, wdir, lab = ctx["week"], ctx["spec"], ctx["wdir"], ctx["lab"]
    path = os.path.join(wdir, lab + ".pptx")
    if not os.path.exists(path):
        return
    prs = Presentation(path)
    slides = list(prs.slides)
    check("C1", "lab deck: 10 slides", len(slides) == 10, len(slides))
    texts = [[t for no, sh, p, t in paragraphs(prs) if no == k] for k in range(1, len(slides) + 1)]
    titles = spec.get("SLIDE_TITLES")
    if titles:
        check("C1", "lab deck: the slide titles of C1, in order",
              all(titles[k] in texts[k] for k in range(min(10, len(texts)))),
              [(k + 1, titles[k]) for k in range(min(10, len(texts))) if titles[k] not in texts[k]])
        found = list(titles)
    else:
        found = [" ".join(sh.text_frame.text.split()) for s in slides for sh in s.shapes
                 if sh.has_text_frame and sh.name == "TextBox 1"]
        na("C1", "lab deck: the slide titles of C1, in order", "no SLIDE_TITLES in the spec")
    fixed = {0: "Workshop 1 – ", 1: "Lab Week %02d - Prerequisites" % week, 8: "Destroy the cluster", 9: "Workshop 1 – The End"}
    wrong = [(k + 1, want) for k, want in fixed.items() if k < len(texts) and not any(t.startswith(want) for t in texts[k])]
    check("C1", "lab deck: slides 1, 2, 9 and 10 have the fixed titles of C1", not wrong and len(texts) >= 10, wrong)
    ing = [t for t in found if re.search(ING, t)]
    check("A1", "lab deck: no -ing form in a slide title", not ing, ing)
    every = [t for page in texts for t in page]
    check("A1", "lab deck: Kubernetes, not K8s", not [t for t in every if "K8s" in t], [t for t in every if "K8s" in t][:3])
    deck_a1 = DECK_A1 + list(spec.get("DECK_A1_EXTRA", []))
    bad = [(k + 1, m.group(0)) for k, page in enumerate(texts) for x in page for b in deck_a1 for m in [re.search(b, x)] if m]
    bad += [(no, m.group(0)) for no, sh, p, x in paragraphs(prs) if not is_mono(p) for b in DECK_A1_PROSE
            for m in [re.search(b, x)] if m and (no, m.group(0)) not in bad]
    check("A1", "lab deck: A1 words of the review rounds (no -ing form, full sentences, Kubernetes)", not bad, bad[:5])
    check("C1", "lab deck: the label is Lab Week NN, never Lab NN (C1, G1)",
          not [t for t in every if re.search(r"\bLab ?\d\d\b", t)], [t for t in every if re.search(r"\bLab ?\d\d\b", t)][:3])
    if len(slides) < 10:
        return
    check("C1", "lab deck: slide 2 labels (round 2, MUST-FIX 1)", all(x in texts[1] for x in LABELS), texts[1])
    left3 = [x.replace("{NN}", "%02d" % week) for x in SLIDE3_LEFT]
    s3 = slides[2]
    rows = sorted(((sh.top, sh.left, sh.text_frame.text) for sh in s3.shapes if sh.has_text_frame
                   and 1.8 * 914400 < sh.top < 6.5 * 914400 and sh.text_frame.text.strip()), key=lambda r: (r[1] > 8 * 914400, r[0]))
    left = [x for top, lft, x in rows if lft < 8 * 914400]
    right = [x for top, lft, x in rows if lft > 8 * 914400]
    check("C2", "lab deck: slide 3 left panel, line for line (M19 to M21; round 2 MUST-FIX 2, SHOULD-FIX 1)",
          left == left3, [x for x in left if x not in left3] + [x for x in left3 if x not in left])
    sample = [x for x in right if re.search(r"\b(NAME|masternode|workernode\d)\s{2,}", x)]
    check("C4", "lab deck: slide 3 right panel (round 2, SHOULD-FIX 1)", [x for x in right if x not in sample] == SLIDE3_RIGHT,
          [x for x in right if x not in sample])
    check("C4", "lab deck: slide 3 sample output is 4 comment lines with %s (B5, C4)" % SAMPLE_VERSION,
          len(sample) == 4 and all(x.startswith("# ") for x in sample) and sum(SAMPLE_VERSION in x for x in sample) == 3,
          sample)
    if script is None:
        return
    master = left3.index("# ON THE MASTER - check the three nodes")
    want = [("# ON YOUR OWN MACHINE:  " + x[2:] if x.startswith("$ ") and k < master else x[2:] if x.startswith("$ ") else x)
            for k, x in enumerate(left3)]
    got = [x for x in steps(script).get(0, "").split("\n")[2:] if x.strip() and set(x) != {"#"}]
    check("C2", "lab: Step 0 of the script holds the lines of slide 3, in order (C2; round 2, MUST-FIX 3)", got == want,
          [x for x in got if x not in want] + [x for x in want if x not in got])
    s9 = [t for t in texts[8] if t != "Destroy the cluster" and not t.startswith("CLO835")]
    check("C1", "lab deck: slide 9 is STEP6 of Week 12 v7: only terraform destroy and the comments (round 3, MUST-FIX 3)",
          [t for t in s9 if t != "bash"] == STEP6, s9)
    deck = [t[2:] for page in texts[3:8] for t in page if t.startswith("$ ")]
    lines = set(script.split("\n"))
    check("C2", "lab deck: each command of slides 4 to 8 is in the script", all(c in lines for c in deck),
          [c for c in deck if c not in lines][:3])
    st = steps(script)
    first = [l for n in range(1, 6) for l in command_lines(st.get(n, ""))
             if not l.startswith(" ") and l != "EOF" and not re.match(r"^[a-zA-Z]+:|^- |^---", l)]
    check("C2", "lab deck: each command of Steps 1 to 5 is on a slide", all(c in deck for c in first),
          [c for c in first if c not in deck][:3])
    docs = heredocs(script)
    no_panel = spec.get("NO_FILE_PANEL")
    for no in range(4, 9):
        slide = slides[no - 1]
        step_docs = heredocs(st.get(no - 3, ""))
        right = [sh for sh in slide.shapes if sh.has_text_frame and sh.left > 8 * 914400
                 and 1.8 * 914400 < sh.top < 6.5 * 914400]
        body = [p.text for sh in right for p in sh.text_frame.paragraphs]
        bar = [sh.text_frame.text for sh in slide.shapes if sh.has_text_frame and sh.left > 8 * 914400
               and sh.top < 1.8 * 914400 and sh.text_frame.text.strip()]
        if no_panel is not None and no in no_panel:
            check("C3", "lab deck: slide %d has no file panel" % no, not right and not bar, bar)
            continue
        if not bar and not right and not step_docs:
            continue                     # a step with no file and a slide with no file panel
        name = bar[0] if bar else None
        check("C3", "lab deck: slide %d shows %s as written by the script" % (no, name or "the file of its step"),
              name in step_docs and body == step_docs[name], (name, [x for x in body if x not in step_docs.get(name, [])][:3]))


# ---------------------------------------------------------------------------------------------------------
# Blackboard checks (C7) and F4

def blackboard_checks(ctx):
    week, spec, path = ctx["week"], ctx["spec"], ctx.get("blackboard_path")
    if not path or not os.path.exists(path):
        check("C7", "blackboard: the Blackboard lab text exists", False, path)
        return {}
    b = read(path)
    topic = spec.get("TOPIC")
    title = "# Lab Week %02d: " % week + (topic or "")
    check("C7", "blackboard: title", b.startswith(title + "\n") if topic else b.startswith(title), title)
    check("C7", "blackboard: Submission Instructions with all 7 sections", "\n## Submission Instructions\n" in b
          and "all 7 sections" in b)
    check("C7", "blackboard: 7 sections", len(re.findall(r"^## \d\. ", b, re.M)) == 7 and "all 7 sections" in b)
    found = re.findall(r"^## \d\. (.*)$", b, re.M)
    if spec.get("SECTIONS"):
        check("C7", "blackboard: the section titles use the words of the deck (S26)", found == spec["SECTIONS"], found)
    else:
        na("C7", "blackboard: the section titles use the words of the deck (S26)", "no SECTIONS in the spec")
    ing = [t for t in found if re.search(ING, t)]
    check("C7", "blackboard: no -ing form in a section title", not ing, ing)
    check("C7", "blackboard: no pledge", "pledge" not in b.lower())
    check("C7", "blackboard: ends with the Important paragraph", b.strip().split("\n")[-1].startswith("Important: Use your own"))
    check("C7", "blackboard: no control-plane node; master node", "control-plane node" not in b and "master node" in b)
    check("C7", "blackboard: section 7 is Destroy the Cluster, with no cleanup item",
          "## 7. Destroy the Cluster\n" in b and not re.search(r"clean[ -]?up", b, re.I))
    check("C7", "blackboard: directory, not folder (M29); the item starts with its verb (round 3, MUST-FIX 4)",
          "\n- Run terraform destroy in the Week%02d directory on your own machine.\n" % week in b
          and "builds three Ubuntu 26.04 EC2 instances" in b
          and "folder" not in b.lower())
    check("C7", "blackboard: no 'using', 'showing' or '!.' (S24)", not re.search(r"\busing\b|\bshowing\b|!\.", b))
    check("C7", "blackboard: kubeadm forms the Kubernetes cluster at boot (round 2, SHOULD-FIX 3)",
          "kubeadm forms the Kubernetes cluster at boot." in b)
    for name, phrase in spec.get("BLACKBOARD_PHRASES", []):
        check("C7", "blackboard: " + name, phrase in b)
    for name, k, phrase, absent in spec.get("BLACKBOARD_SECTION_PHRASES", []):
        part = b.split("## %d. " % k)
        check("C7", "blackboard: " + name, len(part) > 1 and phrase in part[1].split("## %d. " % (k + 1))[0]
              and (absent is None or absent not in part[0]))
    two = [l for l in b.split("\n") if l.startswith("- ")
           and (re.search(r", then\b|\band wait\b|, and (approve|create|apply|wait)\b", l)
                or re.search(r"^- (Create|Apply|Update|Add|Write|Approve)\b.*, run\b", l))]
    two += [l for l in b.split("\n") if "from localMachine.sh, and run" in l]
    check("C7", "blackboard: one instruction in one item (round 2, MUST-FIX 8)", not two, two)
    req = b.split("## Submission Requirements")
    check("C7", "blackboard: Submission Requirements with six items",
          len(req) > 1 and len(re.findall(r"^- ", req[1].split("Important:")[0], re.M)) == 6)
    labels = [l for l in b.split("\n") if re.search(r"\bLab ?\d\d\b", l)]
    check("C1", "blackboard: the label is Lab Week NN, never Lab NN (C1, G1)", not labels, labels[:3])
    sections = re.split(r"^## \d\. ", b, flags=re.M)[1:]
    items = {}
    for k, sec in enumerate(sections, 1):
        body = sec.split("## Submission")[0]
        check("C7", "blackboard: 'You must:' in section %d" % k, "\nYou must:\n" in body)
        its = [l[2:] for l in body.split("\n") if l.startswith("- ")]
        kinds = [i.startswith("Explain") for i in its]
        check("C7", "blackboard: Explain items last in '%s'" % sec.split("\n")[0][:30], kinds == sorted(kinds))
        for i in its:
            items[(k, i)] = True
    return items


def f4_checks(ctx, items, script):
    spec = ctx["spec"]
    if "F4" not in spec:
        na("F4", "F4: each Blackboard item has a row of the F4 table", "no F4 table in the spec")
        return
    if script is None:
        check("F4", "F4: the lab script exists", False)
        return
    st = steps(script)
    rows = {(k, i): (src, needles) for k, i, src, needles in spec["F4"]}
    check("F4", "F4: each Blackboard item has a row", not set(items) - set(rows), sorted(set(items) - set(rows))[:4])
    check("F4", "F4: each row has a Blackboard item", not set(rows) - set(items), sorted(set(rows) - set(items))[:4])
    runs = [(k, i) for (k, i) in items if i.startswith("Run ")]
    check("F4", "F4: each Run item has a command of its step", all(rows.get(r, ("",))[0] == "step" for r in runs),
          [r for r in runs if rows.get(r, ("",))[0] != "step"])
    misses = []
    for (k, i), (src, needles) in rows.items():
        step = st.get(k - 1, "")
        if src == "step":
            where = step if k in (1, 7) else "\n".join(command_lines(step))
        elif src == "comment":
            where = " ".join(l.lstrip("# ").strip() for l in comment_lines(step))
        else:
            continue
        misses += [(k, n) for n in needles if n not in where]
    check("F4", "F4: each needle is in its lab step", not misses, misses[:5])
    lecture = [(k, i[:50]) for (k, i), (src, _) in rows.items() if src == "lecture"]
    info("F4 rows answered by the lecture, not by the lab: %s" % lecture)


# ---------------------------------------------------------------------------------------------------------
# Live checks (E3, C9)

LIVE_FILES = ["run1.log", "run2.log", "out_public.log", "out_public2.log", "out_private.log", "destroy1.log",
              "destroy.log", "pause1.log", "lecture.log", "run.sh"]


def live_checks(ctx, folder):
    spec, repo = ctx["spec"], ctx["repo"]

    def get(name):
        p = os.path.join(folder, name)
        return read(p) if os.path.isfile(p) else ""
    if not repo or not os.path.isfile(os.path.join(repo, "localMachine.sh")):
        check("E3", "live: the repo folder with localMachine.sh exists", False, repo)
        return
    absent = [f for f in LIVE_FILES if not os.path.isfile(os.path.join(folder, f))]
    check("E3", "live: the live folder holds the %d files of a live test" % len(LIVE_FILES), not absent, absent)
    final = runner(os.path.join(repo, "localMachine.sh"))
    count = final.count('echo "@@CMD')
    denials = spec.get("DENIALS", [])
    for no in (1, 2):
        log = get("run%d.log" % no)
        check("E3", "live: pass %d ran all %d commands" % (no, count), log.count("@@CMD") == count, log.count("@@CMD"))
        if denials:
            failed = re.findall(r"@@CMD L\d+: ([^\n]*)\n(?:(?!@@CMD).*\n)*?@@RC [1-9]", log)
            check("C9", "live: pass %d has only the %s planned denials as non-zero exits (C9)" % (no, NUMBER.get(len(denials), len(denials))),
                  failed == denials, failed)
        else:
            check("C9", "live: pass %d has 0 non-zero exits" % no, not re.search(r"^@@RC [1-9]", log, re.M))
        if spec.get("CAN_I"):
            answers = [x.strip() for x in log.split("\n") if x.strip() in ("no", "yes")]
            check("C4", "live: pass %d can-i answers are %s" % (no, ", ".join(spec["CAN_I"])), answers == spec["CAN_I"], answers)
        for sample in spec.get("LIVE_SAMPLES", []):
            check("C4", "live: pass %d shows the sample '%s' (C4)" % (no, sample[:40]), sample in log)
        for name, regex in spec.get("LIVE_REGEX", []):
            check("C4", "live: pass %d %s" % (no, name), re.search(regex, log) is not None)
    check("E3", "live: terraform output public_ips", "master" in get("out_public.log"))
    check("E3", "live: terraform output private_ips", "master" in get("out_private.log"))
    lecture = get("lecture.log")
    bad = spec.get("LECTURE_LOG_BAD", r"(?i)^error: |invalid|unable to|unknown (flag|command)")
    nonempty = spec.get("LECTURE_LOG_NONEMPTY", True)
    check("E3", "live: lecture commands have no error", (lecture.strip() != "" or not nonempty)
          and not re.search(bad, lecture, re.M))
    masters = [re.search(r'"master"\s*=\s*"([\d.]+)"', get(f)) for f in ("out_public.log", "out_public2.log")]
    check("E3", "live: pass 2 ran on a new cluster (two master addresses)", all(masters) and masters[0].group(1) != masters[1].group(1),
          [m and m.group(1) for m in masters])
    for f in ("destroy1.log", "destroy.log"):
        check("E3", "live: destroy complete (%s)" % f, "Destroy complete! Resources: %d destroyed." % RESOURCES in get(f))
    pause = get("pause1.log")
    check("F2", "live: cluster runs the maziar Flannel image", FLANNEL_IMAGE in pause and "ghcr.io" not in pause)
    check("E3", "live: no recovery test (terraform destroy is the recovery)", not os.path.exists(os.path.join(folder, "recovery.log")))
    tested = re.sub(r"@@CMD L\d+:", "@@CMD", get("run.sh"))
    check("E3", "live: the tested commands equal the final commands", tested.strip() == re.sub(r"@@CMD L\d+:", "@@CMD", final).strip())


# ---------------------------------------------------------------------------------------------------------
# Quiz checks (D9, D10) and builders (A5)

def quiz_folder(week):
    best = None
    for name in os.listdir(QUIZ_ROOT) if os.path.isdir(QUIZ_ROOT) else []:
        m = re.fullmatch(r"Quiz_((?:W\d\d)+)_Easy20(?:_v(\d+))?", name)
        if m and ("W%02d" % week) in re.findall(r"W\d\d", m.group(1)):
            v = int(m.group(2) or 1)
            if best is None or v > best[0]:
                best = (v, name)
    return os.path.join(QUIZ_ROOT, best[1]) if best else None


def quiz_checks(ctx):
    week, folder = ctx["week"], ctx.get("quiz")
    if folder and not os.path.isdir(folder):
        check("D9", "quiz: the quiz folder exists", False, folder)
        return
    if not folder:
        na("D9", "quiz: the audit of the quiz", "no quiz_pool_src/Quiz_..._Easy20 folder names W%02d" % week)
        na("D10", "quiz: the cue simulation", "no quiz folder for the week")
        return
    want = os.path.normpath(folder)
    audits, stale = [], []
    for name in sorted(os.listdir(QUIZ_ROOT)):
        if re.fullmatch(r"audit_easy20(_w\d+)?(_v\d+)?\.py", name):
            m = re.search(r'^D = "([^"]+)"', read(os.path.join(QUIZ_ROOT, name)), re.M)
            if m and os.path.normpath(m.group(1)) == want:
                audits.append(name)
            elif m and os.path.basename(os.path.normpath(m.group(1))) == os.path.basename(want):
                stale.append((name, m.group(1)))
    if audits:
        for a in audits:
            r = run([sys.executable, "-I", os.path.join(QUIZ_ROOT, a)])
            last = [l for l in r.stdout.split("\n") if l.strip()][-3:]
            check("D9", "quiz: %s on %s" % (a, os.path.basename(folder)), r.returncode == 0, last)
    elif stale and not os.path.exists(stale[0][1]):
        check("D9", "quiz: the audit of %s can run" % os.path.basename(folder), False,
              "%s reads %s, which does not exist" % stale[0])
    elif stale:
        na("D9", "quiz: the audit of %s" % os.path.basename(folder),
           "%s reads %s, not this folder" % stale[0])
    else:
        na("D9", "quiz: the audit of %s" % os.path.basename(folder), "no audit_easy20 script reads this folder")
    uploads = sorted(x for x in os.listdir(folder) if x.endswith("_Blackboard.txt"))
    if uploads:
        for u in uploads:
            r = run([sys.executable, "-I", CUE_SIM, os.path.join(folder, u)])
            last = [l for l in r.stdout.split("\n") if l.strip()][-2:]
            check("D10", "quiz: cue simulation of %s (no strategy above 6.0 of 20)" % u, r.returncode == 0, last)
    else:
        na("D10", "quiz: cue simulation", "no _Blackboard.txt upload file in %s" % folder)


def builder_checks(ctx):
    week = ctx["week"]
    for kind, stem in (("lecture", ctx.get("lecture")), ("lab", ctx.get("lab"))):
        m = re.fullmatch(r"(Lecture|Lab)_week(\d\d)_v(\d+)", stem or "")
        if not m:
            na("A5", "%s: the builder of the deck" % kind, "the deck name is not of the form of A5")
            continue
        name = "build_week%s_%s_v%s.py" % (m.group(2), kind, m.group(3))
        path = os.path.join(PROJECT, name)
        if not os.path.exists(path):
            check("A5", "%s: the builder %s exists" % (kind, name), False)
            continue
        body = read(path)
        check("A5", "%s: %s has a VERSION constant and a __main__ guard" % (kind, name),
              re.search(r"^VERSION\s*=", body, re.M) is not None and re.search(r"^if __name__ == .__main__.:", body, re.M) is not None)


# ---------------------------------------------------------------------------------------------------------

def summary(out=None):
    by = collections.defaultdict(list)
    for status, rule, name, detail in RESULTS:
        by[rule].append(status)
    lines = []
    print("\nRULES OF CLO835_STANDARDS.md")
    for entry in RULES:
        rule, title, reason = entry[:3]
        part = entry[3] if len(entry) > 3 else None
        st = by.get(rule, [])
        fails, passes = st.count("FAIL"), st.count("PASS")
        if fails:
            s, why = "FAIL", "%d of %d checks failed" % (fails, fails + passes)
        elif passes:
            s, why = "PASS", "%d checks" % passes + ("; not checked: %s" % part if part else "")
        else:
            s, why = "N/A", reason or "no check ran for this week (see the N/A lines)"
        print("%-4s  %-3s %s: %s" % (s, rule, title, why))
        lines.append((s, rule, title, why))
    fails = sum(1 for r in RESULTS if r[0] == "FAIL")
    passes = sum(1 for r in RESULTS if r[0] == "PASS")
    nas = sum(1 for r in RESULTS if r[0] == "N/A")
    gate = "GATE %d  (%d failed, %d passed, %d not applicable)" % (0 if fails else 1, fails, passes, nas)
    print("\n" + gate)
    if out:
        with open(out, "w", encoding="utf8") as f:
            f.write("# check_week.py result\n\n%s\n\n## Checks\n\n| Result | Rule | Check | Detail |\n|---|---|---|---|\n" % gate)
            for status, rule, name, detail in RESULTS:
                f.write("| %s | %s | %s | %s |\n" % (status, rule, name.replace("|", "\\|"),
                                                       str(detail if status != "PASS" else "").replace("|", "\\|")[:300]))
            f.write("\n## Rules\n\n| Result | Rule | Title | Reason |\n|---|---|---|---|\n")
            for s, rule, title, why in lines:
                f.write("| %s | %s | %s | %s |\n" % (s, rule, title, why))
    return fails


def main():
    ap = argparse.ArgumentParser(description="CLO835 week checker (see the module text).")
    ap.add_argument("--week", type=int, required=True)
    ap.add_argument("--lecture")
    ap.add_argument("--lab")
    ap.add_argument("--blackboard")
    ap.add_argument("--dir")
    ap.add_argument("--repo")
    ap.add_argument("--quiz")
    ap.add_argument("--live")
    ap.add_argument("--deck")
    ap.add_argument("--kind", default="lecture", choices=["lecture", "lab"])
    ap.add_argument("--out")
    a = ap.parse_args()
    week = a.week
    nn = "%02d" % week
    wdir = a.dir or week_dir(PROJECT, week)
    if a.dir and not os.path.isdir(a.dir):
        sys.exit("--dir %s is not a directory" % a.dir)
    spec, spec_path = load_spec(week)
    if not wdir:
        sys.exit("no directory Week%s or week%s in %s" % (nn, nn, PROJECT))
    info("week %s: directory %s; spec %s" % (nn, wdir, spec_path or "none"))
    if a.deck:
        deck_checks(wdir, a.deck, a.kind, spec.get("ALLOWED_REPEATS", ()))
        sys.exit(1 if summary(a.out) else 0)
    lecture = a.lecture or (newest(wdir, r"Lecture_week%s_v(\d+)\.pptx" % nn) or "")[:-5] or None
    lab = a.lab or (newest(wdir, r"Lab_week%s_v(\d+)\.pptx" % nn) or "")[:-5] or None
    bb = a.blackboard or newest(wdir, r"Lab_week%s_Blackboard_Submission(?:_v(\d+))?\.md" % nn)
    repo = a.repo or week_dir(COURSE_REPO, week)
    quiz = a.quiz or quiz_folder(week)
    ctx = {"week": week, "spec": spec, "wdir": wdir, "lecture": lecture, "lab": lab, "repo": repo, "quiz": quiz,
           "blackboard_path": os.path.join(wdir, bb) if bb else None}
    info("lecture %s; lab %s; Blackboard %s; repo %s; quiz %s; live %s" % (lecture, lab, bb, repo, quiz, a.live))
    check("F1", "the course repo exists at %s" % COURSE_REPO, os.path.isdir(COURSE_REPO))
    decks = sorted(x for x in os.listdir(wdir) if x.endswith(".pptx"))
    if lecture:
        prs = deck_checks(wdir, lecture, "lecture", spec.get("ALLOWED_REPEATS", ()))
        if prs is not None:
            lecture_checks(prs, week, lecture, repo)
    elif [x for x in decks if "lecture" in x.lower()]:
        check("A5", "lecture: a deck with the name Lecture_week%s_vN.pptx (A5)" % nn, False,
              "the lecture decks have other names: %s" % [x for x in decks if "lecture" in x.lower()][:4])
    else:
        na("B8", "lecture: the deck checks", "no lecture deck in %s" % wdir)
    if lab:
        deck_checks(wdir, lab, "lab", spec.get("ALLOWED_REPEATS", ()))
    elif [x for x in decks if "lab" in x.lower()]:
        check("A5", "lab: a deck with the name Lab_week%s_vN.pptx (A5)" % nn, False,
              "the lab decks have other names: %s" % [x for x in decks if "lab" in x.lower()][:4])
    else:
        na("B8", "lab: the deck checks", "no lab deck in %s" % wdir)
    builder_checks(ctx)
    script = None
    if repo and os.path.isdir(repo):
        script = lab_checks(ctx)
        if lab and week >= KUBEADM_FROM:
            lab_deck_checks(ctx, script)
    elif lab:
        check("C5", "lab: the repo folder of the week exists", False, "no Week%s directory in %s" % (nn, COURSE_REPO))
    else:
        na("C5", "lab: the repo folder checks", "no Week%s directory in %s" % (nn, COURSE_REPO))
    if not bb and not lab:
        na("C7", "blackboard: the checks of the Blackboard lab text", "no lab deck and no Blackboard text in %s" % wdir)
        items = {}
    else:
        items = blackboard_checks(ctx)
    f4_checks(ctx, items, script)
    quiz_checks(ctx)
    if a.live:
        live_checks(ctx, a.live)
    else:
        na("E3", "live: the checks of a live test", "no --live folder: the checker did no live check (E3, C9)")
    sys.exit(1 if summary(a.out) else 0)


if __name__ == "__main__":
    main()
