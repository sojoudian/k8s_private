# Report: Week 12 and Week 13 fix, state before the live tests
**Date**: 2026-11-11
**Sequence**: #03 for the day (it replaces the interim state of #02)

## Summary
The user asked to fix Week 12 and then Week 13 "100 %" to CLO835_STANDARDS.md (v1.2 since 2026-11-11: a lab
on AWS has no cleanup script, and pass 2 runs on a new cluster). All work that needs no AWS is done: the
builders, decks, PDFs, scripts, Blackboard texts, repo folders, gates and both quizzes, with independent
review rounds until the decks and the quiz texts reached 0 MUST-FIX and 0 SHOULD-FIX (the last fixes were the
exact texts that the last reviewers proposed and checked). The live tests are NOT done: the Learner Lab
session ended at about 01:39, and the AWS token is still expired at 06:45. So no claim of "fixed" or "done"
is made (A7 step 6). The old Week 12 cluster still exists (3 instances, see Issues).

## What Changed
Project root /Users/maziar/Downloads/k8s_week3:
- Week 12: build_week12_lab_v7.py (new); build_week12_lecture_v7.py (round 3 to 7 fixes, v7 never delivered,
  so --force); Week12/Lab_week12_v7.pptx/.pdf, Week12/localMachine_v7.sh,
  Week12/Lab_week12_Blackboard_Submission_v7.md, Week12/Lecture_week12_v7.pptx/.pdf; gate_week12.py (lab
  and live checks for v1.2; deck checks unchanged; old copy in scratchpad w12/gate_week12_before_v12rule.py).
- Week 12 quiz: quiz_pool_src/q_easy20_w12.py and Quiz_W12_Easy20/ (4 files): new Q20 (env and envFrom),
  rounds 3 to 10 of the source docstring.
- Week 13: build_week13_lab_v5.py, build_week13_lecture_v9.py, gate_week13_v2.py (new); week13/Lab_week13_v5,
  week13/localMachine_v5.sh, week13/Lab_week13_Blackboard_Submission_v5.md, week13/Lecture_week13_v9 (32
  slides); guards added to build_week13_lab_v1/v2/v3.py, build_week13_lecture_v8.py and build_week13.py.
- Week 13 quiz (new): quiz_pool_src/q_easy20_w13.py, build_easy20_w13.py, audit_easy20_w13.py,
  Quiz_W13_Easy20/ (Blackboard.txt, AnswerKey.txt, Titles.txt, QTI21.zip).
- tools/instrument.py: a line that ends with `<<EOF` (no quotes) now starts a heredoc block (Week 13 counted
  50 commands and Week 14 49 before, both wrong; now 39 and 38; Weeks 04 to 12 unchanged, the Week 12 runner
  is byte-equal).
- Course repo ~/Documents/c/r/CLO835_Fall_2026 (not committed; HEAD 5b97e4f): Week12 (7 files,
  cleanup_lab12.sh deleted) and Week13 (7 files). Week13 equals Week12 except the week name and the topic (C5).

## Technical Details
Review rounds (MUST/SHOULD), each by a fresh independent agent:
- Week 12 decks: 5/24, 6/22, 4/15, 1/11, 1/7, 0/4, 1/4, 0/12, 1/2, 0/3, 0/0 (round 11).
- Week 12 quiz: 13/18, 6/13, 5/11, 2/8, 1/5, 0/2, 0/1, 0/1, 0/1 (round 9: 0 in the quiz text; its one item was
  in probe4.sh and is applied).
- Week 13 decks: 37/33 (audit of v8/v4), 13/15, 6/7, 2/3, 0/4, 0/3, 0/3, 0/4, 0/4, 0/1, 0/1 (round 11; its
  one item, "a change of this field", is the reviewer's checked text, applied verbatim).
- Week 13 quiz: 1/15, 0/8, 0/2, 0/2, 0/1, 0/1 (round 6; its one item, a Q11 feedback text, is applied
  verbatim).
Decisions (with the reason):
- Week 12 lab v7, not a v6 rebuild: the v6 repo files were pushed by the user (5b97e4f).
- Rejected with evidence: "slide 21 has no kubernetes.io support" (the security checklist says "Pods needing
  secrets should have these automatically mounted through volumes"); the round 7 quiz stem "The Pod has no
  other reference to app-config" (it contradicts the lab file config-env.yaml).
- Week 13 slide 31: the map comes from one written table of 175 slide-and-step pairs
  (scratchpad w13/slide31_map.md); criterion D counts only the denial rule of slide 14 (the admin rule of
  slide 18 was removed, the narrower reading). The builder asserts that no note line names a topic that a
  listed pair uses.
- "allow" is the one word for a permission in Week 13 (the third-party STE dictionary prefers LET; the
  standards use "allow"; owner decision kept).
- The engine shows L$ lines as "$" (owner decision, unchanged).
Facts checked on kubernetes.io and docs.aws.amazon.com (quotes in the review reports): TokenRequest stable in
v1.20, bound token volume in v1.22; ConfigMap volume update within about two minutes; RBAC stable in v1.8;
auth whoami stable in v1.28; the authorizers checked in order; system:masters bypasses RBAC; kubeadm
admin.conf in kubeadm:cluster-admins (v1.29+); CSR minimum 600 s, kube-apiserver-client never auto-approved;
/healthz deprecated since v1.16; Endpoints deprecated in v1.33; EKS access entries recommended, aws-auth
deprecated; kubeadm lets system:unauthenticated read the ConfigMap cluster-info.

## Results
- Week 12: gate_week12.py GATE 1 (90 checks, 0 failed) without the live folder; deck gate FAILED: 0 for the
  lecture (28 slides) and the lab (10 slides); 39 commands; quiz: all gates, audit errors 0, cue tool PASS
  (highest 5.50 of 20; "The API server rejects" and some phrases at exactly 6.00).
- Week 13: deck gate FAILED: 0 for lecture v9 (32 slides) and lab v5 (10 slides); gate_week13_v2.py GATE 1
  (115 checks) without the live folder; 39 commands; quiz: all gates, audit errors 0, cue tool PASS (highest
  5.50; "an" at 6.00).
- Repo: F3 scan clean for Week12 and Week13; bash -n and terraform fmt -check pass.
- Live (old cluster, before the session ended): the earlier lecture commands of Week 12 23/23 exit 0;
  probe3 (command with no args ignores CMD; token exp - iat = 31536000 s; a new shell keeps the old value).

## Issues / Notes
- AWS: the Learner Lab session ended at about 01:39 (explicit deny voc-cancel-cred), and the token is
  expired. The old Week 12 cluster (sandbox scratchpad w12/tf2, master 44.192.86.168, 15 resources) is NOT
  destroyed (live2/destroy_old_cluster.log). The user must start the Learner Lab and refresh the local
  credentials. Then the first action is its destroy.
- Pending live work, in this order (E3):
  1. Destroy the old Week 12 cluster; check 0 instances and 0 week12 security groups.
  2. Week 12: live_tools/up.sh 12 1, pass 1 (live_tools/pass.sh 12 1 0), probe4.sh (Q20, Q8 B and D, Q18),
     the lecture runner w12/lecture_run4.sh with no cleanup call, destroy1.log; up.sh 12 2, pass 2 (DELAY 3),
     destroy.log; then the gate with the live folder.
  3. Week 13: the same with live_w13, probe_summary.sh (20 slide claims), then probe_w13.sh (quiz keys), the
     lecture commands, pass 2 on a new cluster, destroy.
  4. A comment or a key that the live output contradicts goes back through a review round.
- Open owner items: the commits 5b97e4f, 5f8a655 and ad93eb8 have the author "BartyCrouch
  <sojodyan@gmail.com>" (F5 names "maziar"); G1 has no Blackboard item name for Lab Week 13; the
  third-party STE dictionary list (allow, block, works, whole) against the standards file.
- Release order (G2): commit and push Week12 and Week13 before the Blackboard texts are posted.
