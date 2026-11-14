"""Week03 — targeted repair of the two shipped decks. No redesign.

Both decks are already in the CLO835 house design (16:9, Calibri + Consolas,
house palette, whale + footer). This script fixes only the five defects that
the 2026-09-22 audit found, and adds the Course Outline page the deck lacks.

  1. Lab slide 6: the terminal text overflows its box onto the white slide.
  2. Both covers: the whale overlaps the instructor line.
  3. Week03 cover: does not follow the Week 1 / Week 2 title pattern.
  4. Two off-palette colours: E74C3C and 3A3A3A.
  5. Week03 has no Course Outline page.

Every word of the source text is preserved (PROMPT.md R1). Nothing else moves.
"""

import re, zipfile, shutil
from pptx import Presentation
from pptx.util import Inches, Pt
import build_week02 as b2
from build_week12 import (
    BLUE, SLATE, MUTED, FOOTER_GRAY, RIGHT,
    add_text, title, whale_and_footer,
)

VERSION = "v1"

# The 16 outline tiles, VERBATIM from Week02_lecture_style_v1.pptx slide 3.
OUTLINE = [
    "Week 1 : Docker Introduction",
    "Week 2 : Docker Image Management",
    "Week 3 : Docker Networking, Storage & Security",
    "Week 4 : K8s Introduction",
    "Week 5 :K8s- PODs,  ReplicaSets",
    "Week 6 : K8s – Services & Deployments",
    "Week 7 : K8s  –  Volumes",
    "Study Week",
    "Week 8 : K8s- K8s- PVs & K8s in AKS",
    "Week 9 : K8s: Storage classes &  Statefulsets",
    "Week 10 : K8s-  Configmaps  & Secrets",
    "Week 11 : Exam & Mock Exam week",
    "Week 12 : K8s – RBAC and AKS",
    "Week 13 : Project presentation  - K8s and HPA",
    "Week 14 : Project presentation - Helm",
    "Term End",
]
HIGHLIGHT = 2          # Week 3 is this deck


# ------------------------------------------------------------------ helpers
def find_text(slide, starts):
    for sh in slide.shapes:
        if sh.has_text_frame and sh.text_frame.text.startswith(starts):
            return sh
    return None


def set_runs(shape, size=None, color=None):
    for p in shape.text_frame.paragraphs:
        for r in p.runs:
            if size is not None:
                r.font.size = Pt(size)
            if color is not None:
                r.font.color.rgb = color


def renumber_footers(prs, total):
    """Rewrite every 'CLO835, Fall 2026   n / t' footer to the new total."""
    n = 0
    for i, s in enumerate(prs.slides, 1):
        for sh in s.shapes:
            if not sh.has_text_frame:
                continue
            t = sh.text_frame.text
            if "CLO835, Fall 2026" in t and "/" in t:
                for p in sh.text_frame.paragraphs:
                    for r in p.runs:
                        if "CLO835, Fall 2026" in r.text or re.search(r"\d+\s*/\s*\d+", r.text):
                            r.text = f"CLO835, Fall 2026     {i} / {total}"
                        elif r.text.strip():
                            r.text = ""
                n += 1
                break
    return n


def move_slide(prs, old_index, new_index):
    lst = prs.slides._sldIdLst
    ids = list(lst)
    lst.remove(ids[old_index])
    lst.insert(new_index, ids[old_index])


def fix_cover_whale(slide):
    """Lift the instructor block clear of the whale at y=6.85."""
    sh = find_text(slide, "Instructor:")
    if sh is None:
        return False
    sh.top = Inches(6.05)
    sh.height = Inches(0.60)
    return True


def recolor(path, pairs):
    """Swap off-palette hex values for their house equivalents, in place."""
    tmp = path + ".tmp"
    zin = zipfile.ZipFile(path)
    zout = zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED)
    hits = 0
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename.startswith("ppt/slides/") and item.filename.endswith(".xml"):
            t = data.decode("utf8")
            for old, new in pairs:
                hits += t.count(f'val="{old}"')
                t = t.replace(f'val="{old}"', f'val="{new}"')
            data = t.encode("utf8")
        zout.writestr(item, data)
    zout.close(); zin.close()
    shutil.move(tmp, path)
    return hits


# ------------------------------------------------------------------ lecture
def fix_lecture(src, out):
    prs = Presentation(src)
    cover = prs.slides[0]

    # DEFECT 3 — the house cover pattern (Week 1 / Week 2).
    # Every word is kept. Only the order and the styling change.
    t1 = find_text(cover, "CLO835 — Week 3")
    t2 = find_text(cover, "Docker Networking")
    t3 = find_text(cover, "Three things")
    t1.text_frame.paragraphs[0].runs[0].text = "CLO835 – Portable Technologies In Cloud"
    set_runs(t1, size=34, color=BLUE)
    t2.text_frame.paragraphs[0].runs[0].text = "Week 3 · Lecture"
    set_runs(t2, size=22, color=SLATE)
    t2.top = Inches(4.28)
    t3.text_frame.paragraphs[0].runs[0].text = "Docker Networking, Storage and Security"
    set_runs(t3, size=15, color=MUTED)
    t3.top = Inches(4.96)
    t1.top = Inches(2.25)

    # The tagline and the instructor line move to the foot, clear of the whale.
    ins = find_text(cover, "Instructor:")
    ins.top = Inches(5.95)
    ins.height = Inches(0.75)
    p = ins.text_frame.add_paragraph()
    r = p.add_run()
    r.text = "Three things every container engineer ships with."
    r.font.size = Pt(11); r.font.italic = True; r.font.color.rgb = MUTED
    r.font.name = "Calibri"

    # DEFECT 5 — add the Course Outline page, then move it to position 2.
    s = prs.slides.add_slide(prs.slide_layouts[6])
    title(s, "Course Outline")
    b2.course_outline_flow(s, OUTLINE, {HIGHLIGHT: BLUE})
    whale_and_footer(s, 2, len(prs.slides))
    move_slide(prs, len(prs.slides) - 1, 1)

    n = renumber_footers(prs, len(prs.slides))
    b2.bw._sanitize_coords(prs)
    prs.save(out)
    print(f"  {out}: {len(prs.slides)} slides, {n} footers renumbered")


# ------------------------------------------------------------------ lab
def fix_lab(src, out):
    prs = Presentation(src)

    # DEFECT 2 — the whale overlaps the instructor line on the cover.
    fix_cover_whale(prs.slides[0])

    # DEFECT 1 — slide 6 terminal text overflows its box.
    # 25 lines at 9 pt need 4.75 in; the body box is 3.93 in.
    # Grow the terminal to the footer rule, then set 8 pt: 25 x 8 x 1.52 / 72 = 4.22 in.
    s = prs.slides[5]
    body = find_text(s, "# 1. IMAGE")
    for sh in s.shapes:
        if sh.shape_type is not None and not sh.has_text_frame:
            continue
    # the terminal shell is the tall AUTO_SHAPE that starts at y=2.05
    for sh in s.shapes:
        if sh.height is None:
            continue
        top_in = sh.top / 914400.0
        h_in = sh.height / 914400.0
        if abs(top_in - 2.05) < 0.01 and h_in > 4.0:
            sh.height = Inches(4.85)          # bottom 6.90, clears the rule at 7.05
    body.height = Inches(4.35)
    set_runs(body, size=8)

    n = renumber_footers(prs, len(prs.slides))
    b2.bw._sanitize_coords(prs)
    prs.save(out)
    print(f"  {out}: {len(prs.slides)} slides, {n} footers renumbered")


PALETTE_FIX = [("E74C3C", "FF6B6B"), ("3A3A3A", "2A2A2A")]

if __name__ == "__main__":
    print("Week03 repair", VERSION)
    fix_lecture("Week03.pptx", f"Week03_lecture_style_{VERSION}.pptx")
    fix_lab("Lab03_week03.pptx", f"Lab03_lab_style_{VERSION}.pptx")
    for f in (f"Week03_lecture_style_{VERSION}.pptx", f"Lab03_lab_style_{VERSION}.pptx"):
        print(f"  {f}: {recolor(f, PALETTE_FIX)} off-palette colours replaced")
