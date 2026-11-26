# Report: Week 12 Check with check_week.py
**Date**: 2026-11-25
**Sequence**: #02 for the day

## Summary
The user asked Claude to run the new checker on Week 12 and to check everything. The output goes to the correct location in k8s_private. Claude ran all the checks of `tools/check_week.py` on the newest Week 12 files. The result is GATE 1: 0 failed, 160 passed and 6 not applicable.

## What Changed
- New directory `analysis/week12/`, with 2 files:
  - `check_week-2026-11-25.txt`: the full output of the checker (13,498 bytes).
  - `check_week-2026-11-25.md`: the same result as Markdown tables, written with `--out` (15,004 bytes).
- This report.

No other file changed. The checker reads files only.

## Technical Details
- Command, from the project root: `.venv/bin/python -B -I tools/check_week.py --week 12 --out analysis/week12/check_week-2026-11-25.md`.
- The checker selected these files:
  - lecture `Week12/Lecture_week12_v8.pptx` and its PDF;
  - lab `Week12/Lab_week12_v8.pptx`, its PDF and `Week12/localMachine_v8.sh`;
  - Blackboard text `Week12/Lab_week12_Blackboard_Submission_v8.md`;
  - repo folder `~/Documents/c/r/CLO835_Fall_2026/Week12`;
  - quiz folder `quiz_pool_src/Quiz_W12_Easy20_v2`, with `audit_easy20_w12_v2.py` and the cue simulation.
- Location: the project keeps the analysis files of a week in `analysis/weekNN/` (for example `analysis/week09/`). Earlier gate results were only in the text of the reports. So the output is in `analysis/week12/`, with the date in the file names, so that a later run does not overwrite it.

## Results
- GATE 1: 0 failed, 160 passed, 6 not applicable. Exit code 0.
- Rules of `CLO835_STANDARDS.md`: 23 PASS, 0 FAIL, 25 N/A. The N/A rules are rules for the work, the chat or Blackboard, or rules that need a reader, a review or a live test.
- The 6 checks with N/A:
  1. C3, each object keeps its name: no `OBJECTS` in `week_specs/week12.py`.
  2. C5, the repo text equals the repo text of the model week: no `REPO_BASE`.
  3. C1, the slide titles of the lab deck in order: no `SLIDE_TITLES`.
  4. C7, the section titles of the Blackboard text: no `SECTIONS`.
  5. F4, a row of the F4 table for each Blackboard item: no `F4` table.
  6. E3 and C9, the live checks: no live test folder.
- Checks 1 to 5 need Week 12 values that `gate_week12.py` also did not have. Check 6 needs a live test on AWS.

Claude ran no server and used no port.

## Issues / Notes
- The PASS of a rule covers only the checks of the checker. B7, C3, C4, C8, F2 and A1 also need a reader, a live test or a network check. The rule lines of the output say what each rule does not check.
- The Week 13 rule "allow, not let, for a permission" does not apply to Week 12. Week 12 has "defaultMode 0440 lets the owner" in `localMachine.sh` line 103 and on lab slide 6.
- `terraform fmt -check` ran with `CHECKPOINT_DISABLE=1`, so it made no network call.
