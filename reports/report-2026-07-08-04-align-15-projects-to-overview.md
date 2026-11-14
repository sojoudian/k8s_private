# Report: Align 15 project files with the overview (10-minute presentation)
**Date**: 2026-07-08
**Sequence**: #04 for the day

## Summary
Edited all 15 project detail files so their Presentation sections match `project/Project_00_Overview_and_Instructions.docx`, which sets a 10-minute in-person presentation. The project subjects and scope were not changed; only the presentation framing and the demo scripts were reconciled to the 10-minute rule.

## What Changed
- `project/Project_01 ... Project_15` .docx (all 15 regenerated).
- Scratch: `patch_presentation.js` (rewrote demo scripts in projects.json), edit to `gen_projects.js` (Presentation heading + intro).

## Technical Details
- Presentation heading changed to "Presentation (10 minutes, right after you submit)".
- Presentation intro rewritten: 10 minutes, in person, live demo of the already-running system; run bootstrap.sh before the window (at submission), not during it; the 15-point bootstrap check is verified separately from evidence and a clean run; no slides; instructor twist; narration graded; individual Q&A after the 10 minutes.
- Step 1 of every demo script rewritten: it previously ran ./bootstrap.sh live ("while it runs, walk through ..."), which cannot fit a 10-minute demo. Now each step 1 states the cluster is already up, shows git log -1 for the frozen commit, proves the relevant pods are Ready, and keeps that project's specific manifest walkthrough.
- Two time-heavy demos fixed:
  - P6 (Two-cluster migration): the twist that said "happens ~30 minutes before your cutover" now happens immediately before cutover.
  - P13 (HPA under load): step 7 previously said "wait out" the 300s downscale stabilization window; now the student configures a short window (15-30s) so scale-down is observable inside 10 minutes, and explains the 0s and 300s defaults out loud.
- Regenerated from projects.json via gen_projects.js. No em dashes (Rule 4). Times New Roman throughout.

## Results
- All 15 files pass the docx validator.
- P13 rendered to PDF and visually verified (new heading, intro, step 1, and step 7 all correct).
- Automated scan confirms no remaining live-bootstrap or multi-minute-wait phrasing in any of the 15 demo scripts.
- Folder now holds 16 .docx (Project_00 overview + Project_01 ... Project_15).

## Issues / Notes
- Evaluation section unchanged: the 15-point "bootstrap in 15 minutes or less" criterion still stands, now explicitly verified outside the 10-minute demo window.
- Grade weight still not set (files say "refer to Blackboard").
