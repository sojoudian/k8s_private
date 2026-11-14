# Report: Analyze the User's Week 6 v3 Changes (lecture/lab split)
**Date**: 2026-06-08
**Sequence**: #01 for the day

## Summary
The user updated my `Week06_lab_style_v2.pptx` and provided two v3 files
(`Week06_lab_style_v3.pptx`, `Week06_lecture_style_v3.pptx`). I deeply diffed v2 → v3
(metadata, per-slide text-with-levels, and slide-by-slide visual renders) to understand their
changes 100%. **No new pptx was generated** (per instruction). Findings recorded to memory.

## What Changed (v2 → v3) — purely structural
1. **Split one 71-slide deck into two**, mirroring the Week-5 lecture+lab pattern:
   - `Week06_lecture_style_v3.pptx` — **41 slides** — concepts only.
   - `Week06_lab_style_v3.pptx` — **31 slides** — workshops only.
2. **Exact partition by original 71-numbering** (complete, non-overlapping, union = 1–71):
   - LECTURE = {1–10, 16, 17, 22–49, 71}: cover, agenda, outline, Deployment-Rollouts theory,
     Labels theory, all Services theory (Service Types, Endpoints, Networking, Ingress),
     Additional Resources.
   - LAB = {11–15, 18–21, 50–70}: Workshop 1 (Rollouts), 2 (Labels), 3 (Services/Guestbook —
     keeps orig-58 Frontend↔MongoDB concept inline), 4 (DNS — keeps orig-65 endpoints + 66–68
     DNS concept inline).
3. **Footers keep the original master 71-numbering** (NOT renumbered per deck) → both decks have
   gaps and still read "/ 71".
4. **Lab deck slide 1 is BLANK** (no title/content); the lab deck has no cover of its own.
   The lecture deck keeps the full cover.
5. **Hidden slides preserved**: lecture hides slide 13 (= orig 22); lab hides slide 18 (= orig 57).
6. **Design, palette, fonts, layout, terminals, embedded figures, bullet hierarchy, dividers, and
   verbatim text are all UNCHANGED.** "lecture_style"/"lab_style" denote deck purpose, same visual
   system. No content edits found.

## Technical Details
- Metadata: v2_lab 71/hidden[22,57]; v3_lab 31/hidden[18]; v3_lecture 41/hidden[13]; all 16:9.
- Text dumped with indent levels to `/tmp/wk6_{v2_lab,v3_lab,v3_lecture}.txt`; rendered all three to
  `/tmp/wk6_{lab2,lab3,lec3}` for visual diff. Verified cover, LAB divider, deployment-YAML terminal,
  Labels Recap (both figures), Changing-MongoDB terminal (red error), Ingress (title-only) — all
  identical to v2.
- `build_week06.py` is NOT yet updated — it still emits the single combined 71-slide deck.

## Results
- Understanding captured; memory `project-week06-deck.md` updated with the v3 two-deck structure
  and the partition; `MEMORY.md` index updated. No pptx written.

## Issues / Notes — confirm before any regeneration
- Refactor `build_week06.py` to emit both decks in this split?
- Keep the master 71-footer-numbering (as the user did), or renumber per-deck (N / 41, N / 31)?
- Give the lab deck a proper cover instead of the blank slide 1?
