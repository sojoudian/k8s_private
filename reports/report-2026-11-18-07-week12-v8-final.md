# Report: Week 12 v8, the final result of the loop
**Date**: 2026-11-18
**Sequence**: #07 for the day

## Summary
The `/loop` brought Week 12 (ConfigMaps and Secrets) to v8, to `CLO835_STANDARDS.md` v1.2. It ran from
17:50 to 20:15 EST, in 12 runs. All stop conditions are true. The running state of each run is in
`reports/report-2026-11-18-06-week12-v8-loop.md`.

## What Changed
New files in `/Users/maziar/Documents/c/r/k8s_private/` (no v7 file is overwritten):
- `build_week12_lecture_v8.py`: builds `Week12/Lecture_week12_v8.pptx` (29 slides) and its PDF.
- `build_week12_lab_v8.py`: builds `Week12/Lab_week12_v8.pptx` (10 slides) and its PDF,
  `Week12/localMachine_v8.sh` (39 commands on the master), `Week12/Lab_week12_Blackboard_Submission_v8.md`,
  and the repo folder.
- `quiz_pool_src/q_easy20_w12_v2.py`, `build_easy20_w12_v2.py`, `audit_easy20_w12_v2.py`, and the output
  folder `quiz_pool_src/Quiz_W12_Easy20_v2/` (the upload file, the QTI ZIP, the titles, the answer key).

Changed files:
- `tools/rungate.py`, `tools/deck_pipe.sh`, `quiz_pool_src/audit_easy20_w12.py`: the old path
  `/Users/maziar/Downloads/k8s_week3` is now `/Users/maziar/Documents/c/r/k8s_private`.
- `~/Documents/c/r/CLO835_Fall_2026/Week12/localMachine.sh`: byte-equal to `Week12/localMachine_v8.sh`.
  It is the only changed file of the repo. There is no commit and no push.

## Technical Details
The content changes (the defect IDs are in report #06):
- Lecture:
  - A new slide 19 "Image Pull Secrets" (a syllabus topic, concept only).
  - `$(NAME)` references, `defaultMode` and `items`, and the priority of env over envFrom.
  - "Concept only" labels on each topic that the lab does not run.
  - One "Not in the lab" list on slide 28, with each topic one time.
  - The live sample outputs of 2026-11-18, for example `size=7814528k` on slide 20.
- Lab:
  - Step 2 adds `GREETING` (env has priority over envFrom) and `MESSAGE` = `"$(GREETING) $(COLOR)"`.
  - Step 3 adds `defaultMode: 0440` and `ls -lL`.
  - The command count stays at 39 (limit 40). The Blackboard text has the new items.
- Quiz v2 changes: Q4 A; Q5 B and D, with their feedback; the Q8 stem, the key and option D; the Q17 stem;
  and the -ing forms of A1.

The review rounds (one fresh independent subagent for each part in each round):

| Round | Lecture (MUST/SHOULD) | Lab and Blackboard text | Quiz |
|---|--:|--:|--:|
| 1 | 2 / 5 | 0 / 4 | 1 / 4 |
| 2 | 1 / 4 | 0 / 1 | 1 / 1 |
| 3 | 0 / 5 | 0 / 1 | 0 / 2 |
| 4 | 0 / 2 (docstring only) | 0 / 0 | 0 / 0 |
| 5 | 0 / 1 (docstring only) | not needed (no change) | not needed (no change) |
| 6 | 0 / 0 | not needed (no change) | not needed (no change) |

All 42 findings are applied. Rounds 3 to 6 checked the changed parts and their effects (D11 step 5).

## Results
The stop conditions:

| Condition | Result |
|---|---|
| Phase 3 on the final files | lecture gate FAILED: 0 (29 pages); lab gate FAILED: 0 (10 pages); fonts Calibri and Consolas only; repo folder 7 files, no cleanup file, `bash -n` ok, `terraform fmt -check` ok; images `maziar/fortune:args`, `maziar/alpine-curl` (only `latest` exists), `maziar/flannel:v0.28.10`, `maziar/flannel-cni-plugin:v1.9.1-flannel3`; quiz GATE 1 to 14 with 0 errors, keys 5/5/5/5, audit errors 0, cue simulation PASS (highest: shortest 5.50 of 20, limit 6.0) |
| Pass 1 and pass 2 | 39 of 39 commands with exit 0 in each pass |
| Tested commands = final commands | the runner of the final `localMachine_v8.sh` is byte-equal to the runner of pass 2 (checked again at 20:14) |
| Proof of the 20 quiz keys | all 20, live (probe12.sh in pass 1, probe12b.sh for the new Q8 D and the Q17 premise) |
| Last review round | 0 MUST-FIX and 0 SHOULD-FIX for each part: lab and quiz in round 4, lecture in round 6 |
| AWS | 0 instances in any state; only the `default` security group (it cannot be deleted) |

The AWS use: 3 clusters of 3 `m5.large` instances each (pass 1, pass 2, the round 2 probe). Each one was
destroyed in the run that created it ("15 destroyed" each time). Also 3 old instances and 2 security groups
of the Week 12 test of 2026-11-11 were removed in phase 0.

## Issues / Notes
- The syllabus names this quiz "Quiz 4 (2.0%)" and the lab "Optional Lab 9 (2.5%)". The quiz title says
  "Easy quiz", as in Weeks 01 to 10 (`CLO835_STANDARDS.md` line 439).
- The lab builder writes the repo folder with no guard (standards A5). Its docstring now says so.
- The upload of the quiz to Blackboard, the git commit and the push are not done. They are for the user.
- No server started, so no port is used.
