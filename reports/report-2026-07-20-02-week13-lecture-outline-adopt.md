# Report: Adopt user's Week13 lecture Course-Outline edit

**Date**: 2026-07-20
**Sequence**: #02 for the day

## Summary
The user hand-edited the delivered `week13/Week13_lecture_style_v2.pptx` and asked me to adopt it.
They said "slide 13", but a full semantic diff (my pristine build vs their file, all 21 slides in
display order) showed the ONLY real content change is on **display slide 3 (Course Outline)** —
slide 13 (RBAC-Intro) had only PowerPoint re-save noise (attribute reordering, quote style, empty
`<a:xfrm>`, `endParaRPr`), no content change. Adopted the slide-3 outline edit into the builder and
redelivered.

## What Changed
- `assemble_week13.py` OUTLINE + `week13/week13_deck.json` slide-3 body: weeks 8–13 renumbered +1 and
  the last tile changed:
  - Week 8→**9** PVs & K8s in AKS; Week 9→**10** Storage classes & Statefulsets;
    Week 10→**11** Configmaps & Secrets; Week 11→**12** Exam & Mock Exam week;
    Week 12→**13** RBAC and AKS; Week 13→**14** HPA;
    "Week 14: Helm Charts & Deployment Automation" → **"Week 14: Project presentation"**.
  - Weeks 1–7, Study Week, Term End unchanged; Week 1 still highlighted.
- Rebuilt + redelivered `Week13_lecture_style_v2.pptx` (21) and `Week13_lab_style_v2.pptx` (26, the
  lab has no outline slide so it is unchanged in content).

## Technical Details
- Diff method: python-pptx per-slide signature (shape type + geometry + every run's text/size/bold/
  italic/color), pristine bx13 build vs the user's file. Unambiguous: slide 3 tiles (7 changed) +
  slide-3 footer.
- The user's file showed slide-3 footer "3 / 46" (a paste/edit artifact from a 46-slide source); my
  rebuild restores the correct "3 / 21". I did NOT carry the "/46" footer over.
- Adopted the tile text VERBATIM (en-dashes, "K8s-" hyphens, "Configmaps", "Statefulsets" kept).
- Did NOT rebuild the v1 combined deck (user has `~$Week13_lab_style_v1.pptx` open); its outline is
  the old numbering — can update on request.

## Results
- Lecture v2 slide 3 matches the user's edit exactly, footer "3 / 21". 0 float coords on both v2 decks.

## Issues / Notes (flagged to user)
1. Change was on slide **3**, not 13 (13 had no real change) — confirmed via semantic diff.
2. The new outline places **Week 11 = Configmaps & Secrets, Week 12 = Exam**, which is the reverse of
   the previously-recorded canonical schedule (Wk11 EXAM, Wk12 ConfigMaps — see
   memory `clo835-course-schedule.md`, and the Week12 deck's own outline). The two course-outline
   slides now disagree. Adopted verbatim as edited; flagged for the user to reconcile — not silently
   "corrected".
