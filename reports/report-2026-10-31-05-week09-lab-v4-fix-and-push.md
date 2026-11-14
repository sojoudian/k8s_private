# Report: Week 09 lab v4, 4 text fixes and the push

**Date**: 2026-10-31
**Sequence**: #05 for the day

## Summary
I fixed the 4 text defects of report #04 in lab v4 and pushed Week 09 to GitHub as commit
`ff69e05`. A fresh clone now holds lab v4. No command changed, so the live test of lab v3
stays valid for lab v4. No item of the Week 09 audit or the live test is open.

## What Changed
- Created `build_week09_lab_v4.py`, `Week09/Lab_week09_v4.pptx` and `.pdf`, `Week09/localMachine_v4.sh`.
- Changed `lab_kubeadm.py`: added the optional `node_version`. The default stays `v1.35.9`.
- Pushed `Week09/localMachine.sh`, `cleanup_lab09.sh` and `master-init.sh.tftpl` to `master`.
- Updated the memory files of Week 09 and the short labs.
- The Blackboard text stays `Lab_week09_Blackboard_Submission_v3.md`. It needs no change.

## Fixes

| No | Slide | Fix |
|--:|--:|---|
| 1 | 9 | The comment now says that Terraform created 15 resources, and that a `data` line is a read. |
| 2 | 3 | The sample output says `v1.35.10`. |
| 3 | 7 | The comment says one year for each certificate and 10 years for each CA. |
| 4 | 7 | The `can-i` line says "yes. Ignore the namespace warning." |

## Technical Details
- With comments removed, all 39 lines of `localMachine.sh` are the same in v3 and v4.
- The push goes directly to `master`, because students run `git pull` on that branch and all
  your commits are on it. A separate branch leaves GitHub on v2.
- Before the push: `bash -n`, `terraform fmt -check`, and a scan for `/Users/`, `.ssh/`, the
  user name, a home IP address and an AWS key. All pass.

## Results
- `git ls-remote` and the clone both give `ff69e05`. The clone has no local change.
- A fresh clone has 8 files in `Week09`, 1 `auth whoami` line, and the same script as lab v4.
- The deck has 10 slides, `N / 10` footers, 0 float coordinates and 2 fonts.
- I viewed slides 3 and 7 after the change.
- No server started, so no port is used.

## Issues / Notes
- The other lab decks still show `v1.35.9`, and the cluster now installs `v1.35.10`. This is
  outside Week 09.
- COMP2130 Lab Test 1 grading has not started. You stopped that request with a new question.
