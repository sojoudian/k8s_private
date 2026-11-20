# Report: Repository analysis, run 15 (changes after run 14)
**Date**: 2026-11-18
**Sequence**: #01 for the day

## Summary
Run 15 is a read-only pass over `~/Documents/c/r/k8s_private`. It records the changes after run 14
(`report-2026-11-14-01-repo-analysis-run14.md`), and that report stays valid for all other parts. The most
important finding is about time: the mid-term exam is today, Wednesday 2026-11-18, 19:00 to 20:45. The
delivered exam files still hold the defects of review round 17, and Q37 has two defensible answers.

## What Changed
- Created this report.
- No project file changed. No builder ran. No git operation. No AWS call. No memory file changed.
- Network: anonymous reads of the GitHub API for the two public repos.

## Technical Details

### 1. What the project is (short form, the details are in run 14)
- The private work folder of the professor for CLO835 "Portable Technologies in Cloud", Seneca, Fall 2026.
- It holds the decks, the lab scripts, the quizzes, the exams, the assignments, the semester project
  specifications, the Python builders, the QA gates and 186 reports.
- The student material goes to the public course repo `github.com/sojoudian/CLO835_Fall_2026`.
- The lab cluster: kubeadm on EC2, 1 master and 2 workers, Kubernetes v1.35, local-path StorageClass
  `standard` with WaitForFirstConsumer.

### 2. Correction to the calendar of run 14
- Run 14 said that "the exam of 11/11 is over". That is not correct.
- On 2026-11-14 the user set the exam date: Wednesday 2026-11-18, 19:00 to 20:45, in the lecture time.
- At the time of this report (13:56 local), the exam starts in approximately 5 hours.
- The exam scope from the user: Weeks 01 to 06, 09 and 10. Week 07 and Week 08 (study week) are out.
  ConfigMaps, Secrets and all topics after Week 10 are out.

### 3. The mid-term exam `Exam_W11_Midterm40`
Files (all untracked in git):
- Source: `quiz_pool_src/q_midterm40.py` (2026-11-15 04:59).
- Builder and audit: `quiz_pool_src/build_midterm40.py`, `quiz_pool_src/audit_midterm40.py`.
- Delivered: `quiz_pool_src/Exam_W11_Midterm40/` with the Blackboard text, the answer key, the titles and
  the QTI 2.1 ZIP (all 2026-11-15 04:59). The delivered files agree with the source.

Checks run today (read-only):

| Check | Result |
|---|---|
| `audit_midterm40.py` | errors 0, answer leaks 0, question pairs at risk 0 |
| Guess by the most words | 8 of 40 |
| Guess by length | longest 9.0 of 40, shortest 9.8 of 40 |
| ZIP | 41 files, 40 items; 40 titles; 40 key records |
| `tools/quiz_cue_sim.py` | PASS, highest strategy "middle length" 10.83 of 40, limit 12.0 |

The source docstring records 17 review rounds (2026-11-15). The findings of review round 17 are NOT in the
source and NOT in the delivered files:

| Question | Defect | Class |
|---|---|---|
| Q37 A | "It stays Pending, and it binds after a change to storageClassName". The default class sets storageClassName on the old claim, and the claim stays Pending until a Pod uses it. So A is also true, and the question has two correct answers. | MUST-FIX |
| Q18 key | "The container of the Pod template to update". The other options end "of the Pods to update", so the key has the odd form. | SHOULD-FIX |
| Q4 A | "It stops, and Docker then ends its main process". A container stops because its main process ends, so the text contradicts itself and a student can remove it with no knowledge. | SHOULD-FIX |
| Q17 C | "one at a time" is an idiom (ASD-STE100). | SHOULD-FIX |
| Q10 IF B | The feedback says "+r adds the read permission for every user". With umask 077, `chmod +r` adds read for the owner only. The feedback is not correct; the key is correct. | SHOULD-FIX |

- A minimal fix set exists in the session scratchpad, `exam/trial/r17m6.json` (6 option edits, Q10 IF B not
  included). In the earlier trial it passed all cue harnesses except one (cues12 jaccard-out 12.08 of 40,
  limit 12.0). The scratchpad can be cleared at any time.
- The live proofs of standard D5 are not done (no AWS, the Docker daemon was off).

### 4. Git and GitHub
- `sojoudian/k8s_private`: public. Still 1 commit, `840e1c7` (2026-11-14 23:14 UTC). No push after that.
- `sojoudian/CLO835_Fall_2026`: public. HEAD `7c4d9b8` "add week12" (2026-11-13). No new commit after run 14.
- Untracked in the private repo: the 4 exam files, the 3 exam scripts, 7 `__pycache__` files and the run 14
  report. `.DS_Store` and one `.pyc` file are modified.
- The repo is public. A `git add .` and a push puts the exam answer key on the public internet.
- The exam files hold no `/Users/` path, no `.ssh/` path and no email. The only IP addresses are the
  examples 127.0.0.1 and 10.0.0.5 in the question text.

### 5. The semester project (from the student email of 2026-11-16)
- The email quotes `kind-config.yaml` and kind on one EC2 host. That is the v1 text (2026-07-08).
- The folder also holds v2 (2026-10-27), which moves every project to the Week 05 kubeadm cluster. Run 14
  recorded that no v2 project ran on kubeadm. The repo does not show which version the students have now.
- Project 1 (v1 and v2) says: "The instructor will provide a reference for the ordinal-aware init-container
  scripts". No such reference exists in the repo. A search for `server-id` finds only the two spec files.
- The overview v1 says "Do not commit any passwords or tokens". Project 1 requirement 7 says that the
  Secret values "may be dummy". The draft reply resolves this: `bootstrap.sh` generates the Secret.
- v2 Project 1 lists `README.md` two times in the repo layout (lines 87 and 91).
- The draft reply of 2026-11-16 is in the chat only. Its point 1 has a `[date]` placeholder.

### 6. Items of run 14 that did not change
- The local clone `~/Documents/c/r/CLO835_Fall_2026` does not exist, so the lab builders stop.
- The old path `/Users/maziar/Downloads/k8s_week3` is still in 13 files outside `reports/`, `ARCHITECTURE/`
  and `old*`: `tools/rungate.py`, `tools/deck_pipe.sh`, 7 `quiz_pool_src/audit_easy20*.py`,
  `quiz_pool_src/rejected_v1/build.py`, `CLO835_STANDARDS.md`, `CLAUDE.md`, `PROMPT.md`,
  `ARCHITECTURE_ANALYSIS_PROMPT.md` and `Week05/cl.md`.
- The memory folder of the new path is empty. The memory of the old path has 69 files.
- Week 12 lab v7 and Week 13 lab v5 are public and have no live test.
- The hand edits of 2026-11-11 in lecture 07 v8 and lecture 10 v12 are not in the builders.
- The 13 older decks that fail the deck gate, and the 6 current decks with no PDF.

## Results
Findings, ranked:
1. The exam is today at 19:00. Q37 of the delivered exam has two correct answers (MUST-FIX). Q18, Q4,
   Q17 C and Q10 IF B are SHOULD-FIX. The automatic gates pass, so they do not show these defects.
2. The exam answer key is untracked in a public repo. A commit and a push publishes it.
3. The init-container reference that Project 1 promises does not exist, and a student asks for it.
4. The students quote the v1 (kind) project text. The v2 (kubeadm) text is not tested live. The version
   in force is not recorded.
5. The items of run 14 in section 6 stay open.

No server started, so no port is used.

## Issues / Notes
- I did not run `build_midterm40.py` or `qti_pack.py`, because they write the delivered files.
- I did not check if the exam is already in Blackboard. A change to the files after an import needs a
  new import.
- This report is in a folder that the public repo tracks. It names no account number, no student and no
  private IP address.
