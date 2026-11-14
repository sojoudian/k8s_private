# -*- coding: utf-8 -*-
"""Pass-or-fail gate for the Week 12 lecture and lab.

Each check maps to one written rule of PREFERENCES.md, PROMPT.md or DESIGN_LANGUAGE.md.
The script prints PASS or FAIL for each check, then GATE 1 when every check passes,
or GATE 0 when any check fails. It reads the files and changes nothing.

Run from the project root:
    python gate_week12.py LECTURE_STEM LAB_STEM BLACKBOARD_FILE [LIVE_FOLDER]
    python gate_week12.py Lecture_week12_v7 Lab_week12_v7 Lab_week12_Blackboard_Submission_v7.md

2026-11-11 (CLO835_STANDARDS.md v1.2): a lab on AWS has no cleanup script. The lab checks now want
7 repo files, no cleanup text, and a Step 6 with no command on the master. The live checks want pass 1
and pass 2 on two clusters (out_public.log and out_public2.log name two masters), a complete destroy of
each cluster (destroy1.log, destroy.log), and no recovery log. The deck checks did not change.
"""
import collections
import io
import os
import re
import subprocess
import sys
import zipfile
import xml.etree.ElementTree as ET

from PIL import Image
from pptx import Presentation

ROOT = "Week12/"
REPO = os.path.expanduser("~/Documents/c/r/CLO835_Fall_2026/Week12/")
EMU = 914400.0
PALETTE = {"1FA8E0", "37465A", "3F3F3F", "868686", "CFDBEE", "F4F7FB", "E0E0E0", "27AE60", "E74C3C", "2A2A2A",
           "2196A0", "1F8FCD", "1F7AB8", "2466A0", "3A3A3A", "FF5F56", "FFBD2E", "27C93F", "BABABA", "4EC9E0",
           "FFFFFF"}
# Words with a chosen replacement, from the check of one word for one meaning.
BANNED = [r"\boptions\b", r"\bparameters\b", r"\bkeeps?\b", r"\bways?\b", r"\bdescription\b", r"\bPODs?\b", r"K8s-",
          r"[Cc]ommand line\b(?! interface)", r"Config Map", r"ETCD", r"\bwe\b", r"\bOverrid", r"never on disk",
          r"\bcontrol-plane (node|disk)\b", r"\bbake\b", r"\bdumped\b", r"\bresource\b", r"\bentries\b",
          r"(?<![Ee]nvironment )\b[Vv]ariables?\b", r"secret volume", r"configMap volume", r"mounted (files|folder)"]
CONTRACTION = re.compile(r"\b\w+'(t|s|re|ve|ll|d)\b")
# An agenda line that names a slide title, and diagram labels. None of these is a bullet on two slides.
ALLOWED_REPEATS = {"configuring containerized applications", "configmap volume", "projected volume"}
FAILS = []


def check(name, ok, detail=""):
    print("%s  %s%s" % ("PASS" if ok else "FAIL", name, "" if ok else "  -> %s" % (detail,)))
    if not ok:
        FAILS.append(name)


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


def words_of_page(pdf, page):
    out = subprocess.run(["pdftotext", "-bbox", "-f", str(page), "-l", str(page), pdf, "-"],
                         capture_output=True, text=True).stdout
    found = re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>', out)
    return [(float(a) / 72, float(b) / 72, float(c) / 72, float(d) / 72, w) for a, b, c, d, w in found]


def deck_checks(stem, kind):
    path, pdf = ROOT + stem + ".pptx", ROOT + stem + ".pdf"
    prs = Presentation(path)
    n = len(prs.slides)
    label = kind + ": "
    check(label + "canvas 13.333 x 7.5 in", round(prs.slide_width / EMU, 3) == 13.333 and prs.slide_height / EMU == 7.5)
    check(label + "size near 1 MB", os.path.getsize(path) < 1500000)
    fonts = collections.Counter(r.font.name for s in prs.slides for sh in s.shapes if sh.has_text_frame
                                for p in sh.text_frame.paragraphs for r in p.runs if r.font.name)
    check(label + ".pptx uses Calibri and Consolas only", set(fonts) <= {"Calibri", "Consolas"}, dict(fonts))
    out = subprocess.run(["pdffonts", pdf], capture_output=True, text=True).stdout.split("\n")[2:]
    used = {l.split()[0].split("+")[-1].split("-")[0] for l in out if l.strip()}
    check(label + "PDF uses Calibri and Consolas only", used == {"Calibri", "Consolas"}, used)
    pages = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
    check(label + "PDF page count equals slide count", re.search(r"Pages:\s+(\d+)", pages).group(1) == str(n))
    check(label + "PDF is newer than the .pptx", os.path.getmtime(pdf) >= os.path.getmtime(path))
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
                            and d.left <= sh.left and d.fill.type == 1 and str(d.fill.fore_color.rgb) == "2A2A2A"
                            for d in prs.slides[no - 1].shapes)
            mono_size += [(no, z) for z in sizes if over_dark and (z < 9 or z > 14)]
        elif sizes and min(sizes) < 12:
            bar = sh.height / EMU < 0.35 and min(sizes) == 10
            outline = kind == "lecture" and no == 3 and min(sizes) == 10.5
            if not bar and not outline:
                small.append((no, min(sizes), text[:40]))
    check(label + "footer N / TOTAL on every slide", not footer, footer[:3])
    check(label + "whale on every slide", not whale, whale)
    check(label + "no shape off the canvas", not off, off)
    check(label + "no shape in the footer band", not band, band)
    check(label + "no shape on the title band", not top, top)
    check(label + "no image below 110 DPI", not dpi, dpi)
    check(label + "no hidden slide (source has none)", not hidden, hidden)
    check(label + "no speaker notes", not notes, notes)
    check(label + "body text at least 12 pt", not small, small[:8])
    check(label + "terminal text 9 to 14 pt", not mono_size, mono_size[:8])
    titles = collections.Counter(sh.text_frame.text for s in prs.slides for sh in s.shapes
                                 if sh.has_text_frame and sh.name == "TextBox 1")
    check(label + "no duplicate title", max(titles.values()) == 1 if titles else True, titles.most_common(2))
    repeat = collections.defaultdict(set)
    for no, sh, p, text in paragraphs(prs):
        key = re.sub(r"^[▪–•\-]+\s*", "", text).strip().lower()
        bullet = text[0] in "▪–•"
        if not is_mono(p) and (bullet or len(key) > 12) and "clo835" not in key and sh.height / EMU >= 0.35:
            repeat[key].add(no)
    same = {k: sorted(v) for k, v in repeat.items() if len(v) > 1 and k not in ALLOWED_REPEATS}
    check(label + "no bullet word for word on two slides", not same, same)
    bad = [(no, text[:50]) for no, sh, p, text in paragraphs(prs) if is_mono(p) and re.search(r"[^\x00-\x7f]", text)]
    check(label + "no non-ASCII character in Consolas text", not bad, bad[:4])
    bad = [(no, b, text[:50]) for no, sh, p, text in paragraphs(prs) for b in BANNED if not is_mono(p) and re.search(b, text)]
    check(label + "no replaced word in the text", not bad, bad[:6])
    bad = [(no, text[:50]) for no, sh, p, text in paragraphs(prs) if not is_mono(p) and CONTRACTION.search(text)]
    check(label + "no contraction", not bad, bad[:4])
    bad = [(no, text[:50]) for no, sh, p, text in paragraphs(prs) if not is_mono(p)
           and re.search(r"\b[2-9][ -](methods?|steps?|files?|ways?|entries|sections?|step)\b", text)]
    check(label + "small numbers in words", not bad, bad[:4])
    bad = [(no, text[:50]) for no, sh, p, text in paragraphs(prs) if is_mono(p) and text.startswith("kubectl ")]
    check(label + "each command starts with $", not bad, bad[:4])
    bad = [(no, len(s.split()), s[:50]) for no, sh, p, text in paragraphs(prs) if not is_mono(p)
           for s in re.split(r"(?<=[.:])\s", text) if len(s.split()) > 25]
    check(label + "no sentence above 25 words", not bad, bad[:4])
    bad = [(no, text[:50]) for no, sh, p, text in paragraphs(prs) if re.search(r"busybox|luksa|nano\b|/Users/|\.ssh/", text)]
    check(label + "no banned image, editor or private path", not bad, bad[:4])
    zf = zipfile.ZipFile(path)
    floats, colors, media = 0, collections.Counter(), []
    for name in zf.namelist():
        if re.match(r"ppt/slides/slide\d+\.xml", name):
            xml = zf.read(name).decode()
            floats += len(re.findall(r'(?:\bx|\by|cx|cy|marL|indent)="-?\d+\.\d+"', xml))
            colors.update(c.upper() for c in re.findall(r'srgbClr val="([0-9A-Fa-f]{6})"', xml))
        if "/media/" in name:
            media.append(name)
    check(label + "0 float coordinates", floats == 0, floats)
    check(label + "palette only", set(colors) <= PALETTE, set(colors) - PALETTE)
    check(label + "only the logo and the whale as images", len(media) <= 2, media)
    check(label + "no blank thumbnail", "docProps/thumbnail.jpeg" not in zf.namelist())
    core = prs.core_properties
    check(label + "file title and author set", bool(core.title) and core.author == "Maziar Sojoudian"
          and core.last_modified_by == "Maziar Sojoudian", (core.title, core.author, core.last_modified_by))
    # Terminals on the page that PowerPoint rendered: no wrapped line, no text past the dark box.
    wraps, past = [], []
    for no, s in enumerate(prs.slides, 1):
        words = words_of_page(pdf, no)
        darks = [sh for sh in s.shapes if sh.shape_type == 1 and sh.has_text_frame and not sh.text_frame.text.strip()
                 and sh.height / EMU > 0.5 and sh.fill.type == 1 and str(sh.fill.fore_color.rgb) == "2A2A2A"]
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
    check(label + "no wrapped terminal line in the rendered PDF", not wraps, wraps[:5])
    check(label + "no text past a terminal box in the rendered PDF", not past, past[:5])


def lab_checks(lab, blackboard):
    run = subprocess.run([sys.executable, "-I", os.environ["INSTRUMENT"], REPO + "localMachine.sh", "https://none/"],
                         capture_output=True, text=True).stdout
    count = run.count('echo "@@CMD')
    check("lab: at most 40 commands", count <= 40, count)
    script = open(REPO + "localMachine.sh").read()
    check("lab: Step 0 to Step 6, and Step 6 has no command on the master",
          re.findall(r"@@STEP (\d)", run) == list("012345") and re.findall(r"^# Step (\d) - ", script, re.M) == list("0123456"),
          (re.findall(r"@@STEP (\d)", run), re.findall(r"^# Step (\d) - ", script, re.M)))
    step6 = script.split("# Step 6 - ")[1].split("\n")[3:]
    check("lab: Step 6 holds only terraform destroy", [l for l in step6 if l.strip() and not l.startswith("#")] == []
          and "terraform destroy" in "\n".join(step6), step6)
    check("lab: each step names its slide", re.findall(r"# Step (\d) - .*\(slide (\d+)\)", script)
          == [(str(i), str(i + 3)) for i in range(7)])
    check("lab: the repo script equals the deck script", script == open(ROOT + lab.replace("Lab_week12", "localMachine") + ".sh").read())
    names = sorted(x for x in os.listdir(REPO) if x != ".terraform")
    check("lab: 7 files", names == sorted([".gitignore", "bootstrap.sh", "localMachine.sh", "main.tf",
                                           "master-init.sh.tftpl", "variables.tf", "worker-join.sh.tftpl"]), names)
    check("lab: no state or key file", not [x for x in os.listdir(REPO) if re.search(r"tfstate|tfvars|\.pem", x)])
    check("lab: bash -n localMachine.sh", subprocess.run(["bash", "-n", REPO + "localMachine.sh"]).returncode == 0)
    check("lab: terraform fmt", subprocess.run(["terraform", "-chdir=" + REPO, "fmt", "-check"], capture_output=True).returncode == 0)
    text = "".join(open(REPO + x, errors="replace").read() for x in names)
    bad = re.findall(r"/Users/|\.ssh/|sojodyan|AKIA|ASIA[0-9A-Z]{8}|luksa|busybox|\bnano\b|Week 1[0-1]\b|week1[01]\b|flannel-io|ghcr\.io", text)
    check("lab: repo scan", not bad, bad[:5])
    master = open(REPO + "master-init.sh.tftpl").read()
    check("lab: no cleanup script or cleanup text in the repo folder", "cleanup" not in text.lower())
    images = sorted(set(re.findall(r"^\s*(?:- )?image:\s*(\S+)", script, re.M)))
    check("lab: images of maziar only", all(i.startswith("maziar/") for i in images), images)
    flannel = re.findall(r"^\s*image:\s*(\S+)", master, re.M)
    check("lab: Flannel images of maziar only", len(flannel) == 3 and all(i.startswith("maziar/") for i in flannel), flannel)
    b = open(ROOT + blackboard).read()
    check("blackboard: title", b.startswith("# Lab Week 12: ConfigMaps and Secrets"))
    check("blackboard: 7 sections", len(re.findall(r"^## \d\. ", b, re.M)) == 7 and "all 7 sections" in b)
    check("blackboard: no pledge", "pledge" not in b.lower())
    check("blackboard: ends with the Important paragraph", b.strip().split("\n")[-1].startswith("Important: Use your own"))
    check("blackboard: no control-plane node", "control-plane node" not in b)
    check("blackboard: section 7 is Destroy the Cluster, with no cleanup item",
          "## 7. Destroy the Cluster\n" in b and "cleanup" not in b.lower() and "clean up" not in b.lower())
    for sec in re.split(r"^## \d\. ", b, flags=re.M)[1:]:
        items = [l for l in sec.split("## Submission")[0].split("\n") if l.startswith("- ")]
        kinds = [i.startswith("- Explain") for i in items]
        check("blackboard: Explain items last in '%s'" % sec.split("\n")[0][:30], kinds == sorted(kinds))


def live_checks(folder):
    def read(name):
        return open(os.path.join(folder, name), errors="replace").read()
    final = subprocess.run([sys.executable, "-I", os.environ["INSTRUMENT"], REPO + "localMachine.sh", "https://none/"],
                           capture_output=True, text=True).stdout
    count = final.count('echo "@@CMD')
    for no in (1, 2):
        log = read("run%d.log" % no)
        check("live: pass %d ran all %d commands" % (no, count), log.count("@@CMD") == count, log.count("@@CMD"))
        check("live: pass %d has 0 non-zero exits" % no, not re.search(r"^@@RC [1-9]", log, re.M))
    check("live: terraform output public_ips", "master" in read("out_public.log"))
    check("live: terraform output private_ips", "master" in read("out_private.log"))
    lecture = read("lecture.log")
    check("live: lecture commands have no error", not re.search(r"(?i)^error|invalid|unable|forbidden", lecture, re.M))
    masters = [re.search(r'"master"\s*=\s*"([\d.]+)"', read(f)) for f in ("out_public.log", "out_public2.log")]
    check("live: pass 2 ran on a new cluster (two master addresses)", all(masters) and masters[0].group(1) != masters[1].group(1),
          [m and m.group(1) for m in masters])
    for f in ("destroy1.log", "destroy.log"):
        check("live: destroy complete (%s)" % f, "Destroy complete! Resources: 15 destroyed." in read(f))
    pause = read("pause1.log")
    check("live: cluster runs the maziar Flannel image", "maziar/flannel:v0.28.10" in pause and "ghcr.io" not in pause)
    check("live: no recovery test (terraform destroy is the recovery)", not os.path.exists(os.path.join(folder, "recovery.log")))
    tested = re.sub(r"@@CMD L\d+:", "@@CMD", read("run.sh"))
    check("live: the tested commands equal the final commands", tested.strip() == re.sub(r"@@CMD L\d+:", "@@CMD", final).strip())


def main():
    lecture, lab, blackboard = sys.argv[1:4]
    deck_checks(lecture, "lecture")
    deck_checks(lab, "lab")
    lab_checks(lab, blackboard)
    if len(sys.argv) > 4:
        live_checks(sys.argv[4])
    print("\nGATE %d  (%d failed)" % (0 if FAILS else 1, len(FAILS)))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
