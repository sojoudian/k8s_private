# Report: Grade Lab 04 (2.5%) — 13 submissions

**Date**: 2026-07-28
**Sequence**: #04 for the day

## Summary
Graded all 13 Lab 04 ("Lab Week 10: Kubernetes cluster on AWS", kubeadm/Terraform + storage classes,
PV/PVC, StatefulSets, dashboard) reports against the 8-item rubric. Because this lab is
explanation-heavy (each item has a specific "explain why" with a correct answer), graders were given
the MODEL ANSWERS and scored explanation ACCURACY (~55% evidence + ~45% correct explanation per item).
All 13 scored 85-100. 2 of 15 students did not submit (etran12, ngraval).

## What Changed
- No student files modified (read-only grading).
- Staged 13 submissions with clean usernames + converted 1 docx (frsheikh) to PDF in scratchpad/lab04.
- Ran a background Workflow: 13 parallel graders + re-verify on flagged ones (15 agents; 2 red-flagged reports re-checked).
- Personally verified zjlee's item-5 conceptual-error call via pdftotext (confirmed "data lives in the pod" wording).
- Created this report.

## Technical Details
Each grader Read the full PDF (rendering screenshots), and for each of 8 items judged BOTH the demo
evidence (16 added, nodes Ready, gp2 SC, PVC Pending->Bound, <pending> EXTERNAL-IP, mongo cordon
find-empty, dashboard login/overview, fortune readOnly, headless SRV, clean destroy) AND whether the
"explain why" matched the model answer. Flagged/low submissions independently re-graded; reconciliation
kept the higher score.

## Results (out of 100, sorted)
- 100 Ayush Patel (apatel638) — flawless; cordon proof + WaitForFirstConsumer AZ rationale standout.
- 100 Huu Duc Huy Nguyen (hdhnguyen) — CORRECTED from 99: the "cluster-user" item was a one-word prose
  typo (binding command + explanation are correct), so the deduction was removed. Feedback rewritten
  student-facing after the professor flagged the original as unusable/nitpicky.
- 99 Leandro Delgado (ldelgado8) — item-8 PVC-deletion step not screenshotted.
- 98 Christian Emeka Onwuanaku (ceonwuanaku) — "16 added" in prose, not captured.
- 97 Faizan Razzakbhai Sheikh (frsheikh) — minor explanation gaps (dashboard danger, STS DNS).
- 96.5 Marjan Haghighi (mhaghighi6) — item-5 no cordon negative case; apply shot "3 added".
- 94.5 Selva Roshan Sivagnanasundaram Rexon (srsivagnanasundaram) — item-5 cordon case missing; no dashboard login.
- 94 Indah Cahyani Styoningrum (icstyoningrum) [re-verified] — illegible screenshots; honest AI-debug disclosure + redo, no penalty.
- 92 Joe-Smith Effiong Essang (jeessang) — item-5 negative case + item-8 teardown screenshots missing.
- 91.5 Olivier Moriceau (omoriceau) [re-verified] — item-8 teardown + item-5 cordon missing; cover mislabel "Amazon EKS" (cosmetic).
- 89.5 Zhuo Jue Lee (zjlee) — item-5 wrong explanation ("data lives in the pod"/failover framing) + no cordon contrast. CONFIRMED by me.
- 87 Chenyu Gao (cgao37) — evidence complete; second clause of explanations missing on items 2,5,7.
- 85 Tony Vu (tvu27) — item-5 negative case + item-8 teardown missing; minor evidence gaps.

## Issues / Notes
- Two class-wide loss patterns: (item 5) not using kubectl cordon to force the pod onto the OTHER
  worker to show empty find(); (item 8) explaining but not screenshotting PVC-delete-before-destroy.
  If explanation-alone is acceptable to the professor, several students rise a few points.
- icstyoningrum honestly disclosed using Claude/ChatGPT to debug then redid from her own records —
  treated as integrity-compliant (no deduction). Flagged for professor confirmation.
- zjlee: only genuine conceptual error (hostPath "lives in the pod") — worth a one-line correction.
- etran12 & ngraval: no Lab04 submission on file.
- Workflow artifacts: workflows/scripts/grade-lab04-wf_f65793e2-d7d.js (run wf_f65793e2-d7d).
