# Report: Week 12 and Week 13 fix to CLO835_STANDARDS.md v1.2 (interim state)
**Date**: 2026-11-11
**Sequence**: #02 for the day

## Summary
The user asked: "FIX THE WEEK12 100%" and then "FIX THE WEEK13 100%", based on CLO835_STANDARDS.md, with no
partial work. For Week 13 the user answered: "Yes, make the quiz" and "Yes, use AWS". The standards changed to
v1.2 during the work (another session, 2026-11-11): a lab on AWS has no cleanup script, and pass 2 needs a new
cluster. This report records the state at 04:08. The work is NOT complete: the live tests of both weeks wait
for a new Learner Lab session, and the review loops still run. A final report follows.

## What Changed
Week 12 (project root /Users/maziar/Downloads/k8s_week3):
- New build_week12_lab_v7.py: Week12/Lab_week12_v7.pptx and .pdf, Week12/localMachine_v7.sh,
  Week12/Lab_week12_Blackboard_Submission_v7.md, and the repo folder
  ~/Documents/c/r/CLO835_Fall_2026/Week12 (7 files, cleanup_lab12.sh deleted, not committed).
- build_week12_lecture_v7.py: rebuilt Week12/Lecture_week12_v7.pptx and .pdf (28 slides; v7 was never
  delivered in an answer, so --force).
- gate_week12.py: lab and live checks for v1.2 (7 files, no cleanup text, Step 6 with no command on the
  master, section 7 "Destroy the Cluster", pass 2 on a new cluster, no recovery log). The deck checks did not
  change. A copy of the old gate: scratchpad w12/gate_week12_before_v12rule.py.
- quiz_pool_src/q_easy20_w12.py and Quiz_W12_Easy20/ (rebuilt): Q20 is new ("env and envfrom"), because
  the lab no longer deletes a namespace; review rounds 3 to 5 applied.
Week 13:
- New build_week13_lab_v5.py (worker): week13/Lab_week13_v5.pptx and .pdf, week13/localMachine_v5.sh,
  week13/Lab_week13_Blackboard_Submission_v5.md, repo folder Week13 (7 files, not committed), and
  gate_week13_v2.py.
- New build_week13_lecture_v9.py (worker): week13/Lecture_week13_v9.pptx and .pdf (32 slides).
- New quiz: quiz_pool_src/q_easy20_w13.py, build_easy20_w13.py, audit_easy20_w13.py, Quiz_W13_Easy20/.
- tools/instrument.py (worker): a line that ends with `<<EOF` (no quotes) now starts a heredoc block.
  Before, Week 13 counted 50 commands and Week 14 49 (both wrong); now 39 and 38. Weeks 04 to 12 do not
  change (checked: the Week 12 runner is byte-equal).

## Technical Details
- Week 12 review rounds (MUST/SHOULD): decks 5/24, 6/22, 4/15, 1/11, 1/7, 0/4, 1/4 (round 8 runs); quiz
  13/18, 6/13, 5/11, 2/8, 1/5 (round 6 runs). Each finding was applied or rejected with evidence.
- Rejected with evidence: round 3 "slide 21 has no kubernetes.io support" (the security checklist says
  "Pods needing secrets should have these automatically mounted through volumes" and "the environment variable
  method might be more prone to leakage"); round 6 text "the access to Secrets through a new Pod" (false:
  secret-pod is a new Pod that reads app-secret).
- Facts checked: TokenRequest is stable in v1.20, the bound token volume in v1.22 (slide 22 now says
  "Since v1.22, the kubelet gets the token from the TokenRequest API"); a ConfigMap volume updates within
  about two minutes (sync period plus cache TTL, 1 minute each by default).
- Week 13 audit (round 1): 37 MUST-FIX and 33 SHOULD-FIX on lecture v8, lab v4, Blackboard v4 and the repo.
  Lecture v9 and lab v5 fix them (worker tables); review round 2 runs now.
- Week 13 quiz round 1: 20 questions, all gates pass, cue tool 5.50 of 20; review round 1 runs now.

## Results
- Week 12: gate_week12.py GATE 1 (0 failed, 90 checks) without the live folder; deck gate FAILED: 0 for both
  decks; 39 commands; the lecture runner has 26 commands (25 run, 1 docker skip).
- Week 13: deck gate FAILED: 0 for lecture v9 and lab v5; gate_week13_v2.py GATE 1 (114 PASS) without the live
  folder; 39 commands.
- Live, done before the session ended: Week 12 lecture commands 23 of 23 exit 0 (live2/lecture.log of the
  earlier lecture form), probe3 (command with no args ignores CMD; the token of a Pod has exp - iat =
  31536000 s with expirationSeconds 3607; a new shell shows the old value of an environment variable).

## Issues / Notes
- AWS: the Learner Lab session ended at about 01:39 (explicit deny voc-cancel-cred). The three instances of
  the old Week 12 cluster (sandbox scratchpad w12/tf2, master 44.192.86.168) are NOT destroyed; the destroy
  failed with 403 (live2/destroy_old_cluster.log). The user must start the lab again; then the destroy runs.
- Pending live work: Week 12 v7 pass 1 and pass 2 on two new clusters, probe4 (Q20, Q8 options B and D), the
  lecture runner lecture_run4.sh; Week 13 v5 pass 1 and pass 2, probe_w13.sh, probe_summary.sh (slide 28),
  the lecture commands; each destroy with "Destroy complete! Resources: 15 destroyed.".
- The repo commits 5b97e4f, 5f8a655 and ad93eb8 have the author "BartyCrouch <sojodyan@gmail.com>". F5 names
  "maziar". Nothing was rewritten.
- Release order (G2): commit and push Week12 and Week13 before the Blackboard texts are posted.
- The worker reports could not be written to reports/ (harness rule); this report holds their numbers.
