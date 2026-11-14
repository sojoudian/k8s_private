# Report: Blackboard text for Lab Week 06

**Date**: 2026-10-31
**Sequence**: #01 for the day

## Summary
You pasted the Blackboard text of Lab Week 05, which is named `Lab03 - 2.5%` on your
Blackboard, and you asked for a new one based on Week 06. I wrote it in the same shape,
with 7 sections for the 7 steps of the short Week 06 lab.

## What Changed
- Created `Week06/Lab_week06_Blackboard_Submission_v5.md`. Versions v1 to v4 stay.
- Added the Blackboard name to the memory file `project-clo835-lab-numbering.md`.
- Nothing was committed, and nothing was pushed.

## Technical Details
The source is the short lab: `Week06/Lab_week06_v4.pdf` and `Week06/localMachine_v4.sh`.

| Section | Lab step | Slide |
|---|---|--:|
| 1 Build the cluster | Step 0 | 3 |
| 2 Deployment from a manifest | Step 1 | 4 |
| 3 Roll out and roll back | Step 2 | 5 |
| 4 Labels | Step 3 | 6 |
| 5 ClusterIP Service and DNS | Step 4 | 7 |
| 6 NodePort Service | Step 5 | 8 |
| 7 Clean up | Step 6 | 9 |

Each "run" line names a command in that step. The explanation questions come from the
comments in the lab or from `Week06_lecture_style_v7.pdf`: revisions, named `targetPort`,
the DNS name, the search list, EndpointSlices, kube-proxy and NodePort. The lab comments
are the only source for change cause and for a Pod with no owner.

## Results
- `maziar/kubia:v1`, `maziar/kubia:v2` and `maziar/alpine-curl:latest` exist on Docker Hub.
- I did not run the lab again. The lab has a live test on AWS from 2026-10-27.
- No server started, so no port is used.

## Issues / Notes
- **GitHub still holds the old Week 06.** HEAD has 22 steps (Step 0 to Step 21). The short
  lab is an uncommitted change in `~/Documents/c/r/CLO835_Fall_2026`. A student who runs
  `git pull` gets commands that do not match this text.
- The analysis in `report-2026-10-30-01-repo-analysis-run9.md` records a template trap for
  a Week 06 commit. Read that note before a push.
- A Blackboard name for this lab is your decision. `Lab04 - 2.5%` is the next number.
- One command of mine made a stray file, `~/Downloads/.tmp_w6`. I removed it.
