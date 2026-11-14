# -*- coding: utf-8 -*-
"""CLO835 - Week 15 is the project presentation (the user, 2026-10-31).

Makes the Course Outline of the Week 09 and Week 10 lectures agree with the Week 12
lecture v4. Each input is read and never written. The output is its next version.

Run from the project root. It is guarded, so importing it writes nothing.
"""
import copy

from pptx import Presentation

DECKS = {"Week09/Lecture_week09_v6.pptx": "Week09/Lecture_week09_v7.pptx",
         "Week10/Lecture_week10_v8.pptx": "Week10/Lecture_week10_v9.pptx"}
LINES = {"Week 15: Helm Charts & Deployment Automation": "Week 15: Project presentation",
         "Week 12: K8s- Configmaps & Secrets": "Week 12: K8s – ConfigMaps & Secrets",
         "Week 10: K8s: Storage classes & Statefulsets": "Week 10: K8s – StorageClasses & StatefulSets"}


def outline_slide(prs):
    found = [s for s in prs.slides if any(sh.has_text_frame and sh.text_frame.text.strip() == "Course Outline"
                                          for sh in s.shapes)]
    assert len(found) == 1, len(found)
    return found[0]


def set_line(para, text):
    """Some boxes hold one line in two runs. The first run keeps the format."""
    para.runs[0].text = text
    for extra in para.runs[1:]:
        extra._r.getparent().remove(extra._r)


def main():
    for src, out in DECKS.items():
        prs = Presentation(src)
        hits = 0
        for sh in outline_slide(prs).shapes:
            if not sh.has_text_frame:
                continue
            text = sh.text_frame.text.strip()
            if text in LINES:
                set_line(sh.text_frame.paragraphs[0], LINES[text])
                hits += 1
            elif text == "Week 14: K8s – HPA":
                sh.text_frame._txBody.append(copy.deepcopy(sh.text_frame.paragraphs[0]._p))
                set_line(sh.text_frame.paragraphs[1], "Project presentation")
                hits += 1
        assert hits >= 2, (src, hits)
        prs.save(out)
        print("wrote %s (%d lines)" % (out, hits))


if __name__ == "__main__":
    main()
