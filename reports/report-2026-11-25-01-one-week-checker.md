# Report: One Week Checker for CLO835
**Date**: 2026-11-25
**Sequence**: #01 for the day

## Summary
The user asked for one Python application for CLO835 and accepted the recommendation: one week checker that replaces the gate scripts of single weeks. Claude wrote `tools/check_week.py` and 2 data files, `tools/week_specs/week12.py` and `tools/week_specs/week13.py`.

The checker gives PASS, FAIL or N/A for each check and for each rule of `CLO835_STANDARDS.md`. On the current files, it gives the same result as the old gates for each old check: 147 of 147 for Week 13 and 90 of 90 for Week 12. Three independent reviews found 20, 17 and 12 items. Claude fixed them, except the items in "Issues / Notes". The third round was not a clean round, and Claude ran no fourth round.

## What Changed
New files in `/Users/maziar/Documents/c/r/k8s_private` (Git does not track them yet; no commit):
- `tools/check_week.py` (1,382 lines): the checker.
- `tools/week_specs/week12.py` (16 lines): the values of Week 12, from `gate_week12.py`.
- `tools/week_specs/week13.py` (156 lines): the values of Week 13, from `gate_week13_v3.py`. The lists `SLIDE_TITLES`, `SECTIONS`, `OBJECTS`, `DENIALS` and `F4` are byte-for-byte copies.
- This report.

Claude changed no other file. The old gates (`gate_week12.py`, `gate_week13*.py`, `tools/rungate.py`) are still in the project. `tools/deck_pipe.sh` and `CLO835_STANDARDS.md` (B8, C9) still name them.

## Technical Details

### Use
Run the checker from any directory:
- `.venv/bin/python -I tools/check_week.py --week 13` checks the newest lecture deck, lab deck and Blackboard text of the week. It also checks the repo folder `~/Documents/c/r/CLO835_Fall_2026/Week13` and the newest quiz folder.
- `--lecture`, `--lab`, `--blackboard`, `--dir`, `--repo` and `--quiz` select other files or copies.
- `--live DIR` adds the checks of a live test (E3). The folder holds the 10 files of the old gates.
- `--deck STEM --kind lecture|lab` runs only the deck checks, in the form of `tools/rungate.py`.
- `--out FILE` also writes the result as a Markdown table.

The output has 3 parts:
1. One line for each check: PASS, FAIL or N/A, the rule ID, the name, and the detail of a FAIL.
2. One line for each of the 48 rules A1 to G4. A rule with only some checks shows "PASS ... not checked: ...".
3. `GATE 1` when no check fails, or `GATE 0`. The exit code is 0 or 1.

### Design
- Generic checks come from the standards and from the 2 newest gates. A week with no spec file gets the generic checks. A check that needs a spec value shows N/A.
- A spec file holds data only. For example: `TOPIC`, `SLIDE_TITLES`, `SECTIONS`, `OBJECTS`, `DENIALS`, `F4`, `REPO_BASE`, `EXTRA_REPO_FILES`, `MAZIAR_ONLY`, `ALLOWED_REPEATS` and the live samples.
- The checker reads files only. It lists one directory level with `os.listdir`, so a directory link cannot make a loop (the Q3 fault of COMP2130). It reads no link and no special file.
- Each external command has a time limit: 300 s, and 60 s for each page of `pdftotext`. `terraform fmt -check` runs with `CHECKPOINT_DISABLE=1`, so it does not call HashiCorp.
- Weeks 01 to 03 are Docker labs (G3). For them, the kubeadm lab checks show N/A, and the checker does only the repo scan, the images, `bash -n`, `terraform fmt` and the state files.

### New checks (not in the old gates)
- B4: no `a:buChar` bullet with the glyph of B4.
- B6: no connector with zero extent, and no horizontal or vertical arrow drawn as a connector.
- B7: the lecture has the slides Agenda, Course Outline, Optional Topics, Key Takeaways and "Lab Week NN at a Glance".
- C8: each command and each file in a lecture terminal labeled "Lab Week NN, Step M" is in that lab step. The check reads the repo script, the files of `master-init.sh.tftpl` and the extra repo files.
- C1 and G1: the label is "Lab Week NN", never "Lab NN".
- C5: no README, no `.terraform` directory, and each image of `master-init.sh.tftpl` and of the extra repo files is of `maziar`.
- A5: the builder of each deck exists and has a `VERSION` constant and a `__main__` guard.
- D9 and D10: the checker runs the audit script of the quiz folder and `tools/quiz_cue_sim.py`.
- The checks of `gate_week13_v3.py` with no Week 13 value now run for every week. Examples are the slide 3 panels, the script head, Step 6 and the Blackboard form.

## Results

### The old gates against the new checker
- On the current files: Week 13 gives GATE 1 (0 failed, 175 passed, 1 N/A), and Week 12 gives GATE 1 (0 failed, 160 passed, 6 N/A). The 147 checks of `gate_week13_v3.py` and `tools/rungate.py` (Week 13) have the same names and results. The 90 checks of `gate_week12.py` (Week 12) also have the same names and results.
- The `--deck` mode gives the same 32 results as `tools/rungate.py` on 4 decks: Lecture_week07_v8, Lab_week10_v5, Lecture_week13_v10 and Lab_week12_v8.
- Fault test (`cw-mut.py` in the scratchpad): 21 copies, each with one known fault, through the old gate and the new checker.
  - The faults are in the Blackboard text, Step 6, the repo folder (a state file, a ghcr.io Flannel image) and the decks.
  - Other faults are a missing Explain item, a lab slide title and a lecture contraction.
  - The live cases are a pass, a non-planned failure, a missing sample and an incomplete destroy. Made-up logs stand in for the live logs, because no live log exists on this Mac.
  - 20 of 21 cases give 0 differences. In the last case, `gate_week13_v3.py` stops with `FileNotFoundError` on the state file, and the new checker reports the fault.
- The checker found the faults that the reviewers made in copies. Examples:
  - a rancher image, `Lab_week11` and a short `AKIA` key in the repo;
  - a `.terraform` directory and a missing `lecture.log`;
  - a missing file panel and a missing `pdftotext`.

### The other weeks
No week crashes the checker. The results are GATE 0 for Weeks 01 to 10 and 14:

| Week | Failed | Passed | N/A |
|---|---|---|---|
| 14 | 35 | 64 | 12 |
| 10 | 21 | 135 | 8 |
| 09 | 38 | 111 | 9 |
| 07 | 21 | 134 | 11 |
| 06 | 30 | 82 | 9 |
| 05 | 50 | 66 | 9 |
| 04 | 13 | 20 | 10 |
| 03 | 7 | 7 | 6 |
| 02 | 3 | 11 | 6 |
| 01 | 2 | 3 | 7 |

Most of these FAIL lines show that these weeks do not have the form of the Week 12 v7 model. Examples:
- `git pull` in place of `git fetch` (open item H1).
- The `flannel-io` manifest URL (H8), and v1.35.9 samples (C4).
- "K8s", "Lab 14 - Prerequisites", and `busybox`.
- Old deck names (A5): Weeks 01 to 03 have no `Lecture_weekNN_vN.pptx` file.
- An old Blackboard form, and missing deck title properties.

Week 11 has no week directory (only `Week11_Exam` and `Week11-Exam`), so the checker stops with a message.

### Reviews (A7, steps 4 and 5)
- Round 1: 5 MUST-FIX and 15 SHOULD-FIX. Claude fixed 18. Items 13 and 19 are design decisions (see the notes).
- Round 2: 5 MUST-FIX and 12 SHOULD-FIX. Claude fixed all 17.
- Round 3: 1 MUST-FIX and 11 SHOULD-FIX. Claude fixed 11, and accepted item 12 (see the notes).
- After each round, Claude ran the full test set again: the real files, the name comparison, the 21 fault cases and Weeks 01 to 14.

Claude ran no server and used no port.

## Issues / Notes
- No review round was clean: round 3 still had 1 MUST-FIX, and Claude did not run a round 4. So this report does not say "fixed" or "good" (A7).
- Accepted changes for Week 12. The real Week 12 files pass all of them:
  - Four checks of `gate_week12.py` now have the Week 13 name and form:
    - "at most 40 commands";
    - "Step 6 holds only terraform destroy", now with the C1 comment;
    - "repo scan", now wider;
    - "no control-plane node", now also "master node".
  - "images of maziar only" now fails a script with no image.
  - The 10.5 pt exemption of lecture slide 3 is gone, because B3 says that the Course Outline uses 12 pt. No current lecture has 10.5 pt on slide 3.
- Design decisions:
  - B6 allows a plain horizontal connector, because each title line is one.
  - The Step 0 check wants `git fetch && git reset --hard origin/master`, but F1 and H1 of the standards still say `git pull`. The standard needs an update.
  - A terminal label "Lab Week NN" with no step gives an INFO line, not a FAIL.
- `"lets"` (A1, "allow", not "let", for a permission) is a Week 13 rule in `week13.py`. Week 12 has "defaultMode 0440 lets the owner" in `localMachine.sh` line 103 and on lab slide 6. If the rule is for all weeks, add it to A1 of the standards and to the generic list.
- The generic A1 list still holds some phrases of the Week 12 and Week 13 review rounds, for example "does not run admission control".
- The audits of Weeks 01 to 10 read `/Users/maziar/Downloads/k8s_week3/...`, which does not exist, so D9 gives FAIL for these weeks. The cue simulation fails both upload files of `Quiz_W03W04_Easy20` (stem overlap 8.08 and 7.83 of 20).
- The old gates ran `terraform fmt` with no `CHECKPOINT_DISABLE`. So a test run updated `~/.terraform.d/checkpoint_cache` (312 bytes, 13:37) through a call to HashiCorp. The folder existed since 3 June 2026.
- A `python -m py_compile` call wrote `tools/__pycache__/check_week.cpython-313.pyc`. Claude deleted that file.
- The test scripts and the copies are in the session scratchpad, which a reboot can clear: `cw-mut.py`, `cw-compare.py`, `cw-base/`, `cw-new/`, `review1/` to `review3/`.
- The standards name `/Users/maziar/Downloads/k8s_week3` for the reports and the tools (A4, A5, A6), but that folder does not exist. This report is in `k8s_private/reports/`.
