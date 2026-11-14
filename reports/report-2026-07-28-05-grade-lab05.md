# Report: Grade Lab 05 (2.5%) — 13 submissions

**Date**: 2026-07-28
**Sequence**: #05 for the day

## Summary
Graded all 13 Lab 05 ("Lab Week 11: ConfigMaps & Secrets", kubeadm v1.31 cluster + ConfigMap/Secret
injection) reports against the 7-item rubric with model answers embedded (~55% evidence + ~45%
explanation-correctness). Feedback delivered in the professor's required format: ONLY where the
student lost grade, "The <part> part: missing <X>" descriptive style, "—" for full marks. Scores
88–100 mostly; range 85–100. 1 of 14 did not submit (etran12).

## What Changed
- No student files modified (read-only grading).
- Staged 13 submissions with clean usernames + converted 1 docx (frsheikh) to PDF in scratchpad/lab05.
- Ran a background Workflow: 13 parallel graders (none needed re-verify; all >=85, no red flags).
- Personally spot-checked zjlee (4 pages) to confirm the item-1 NotReady/evidence call — grader correct.
- Created this report.

## Results (out of 100, sorted)
- 100 Ayush Patel (apatel638) — full.
- 100 Huu Duc Huy Nguyen (hdhnguyen) — full.
- 100 Leandro Delgado (ldelgado8) — full.
- 100 Marjan Haghighi (mhaghighi6) — full.
- 100 Nrupad Ganeshkumar Raval (ngraval) — full.
- 99 Indah Cahyani Styoningrum (icstyoningrum) — cluster-build worker-join explanation only partial.
- 98 Chenyu Gao (cgao37) — Secret part: explanation omits why base64 is encoding not encryption.
- 98 Joe-Smith Effiong Essang (jeessang) — Secret part: missing base64 -d decode screenshot.
- 97 Tony Vu (tvu27) — Compare: missing "consumed same way" explanation; Teardown: missing cascade explanation.
- 91 Faizan Razzakbhai Sheikh (frsheikh) — cluster-build: missing worker auto-join explanation; Teardown: missing "16 destroyed".
- 89 Zhuo Jue Lee (zjlee) — cluster-build: missing "16 added" + ls ~/week11, nodes NotReady; Teardown: missing cascade explanation. (spot-checked)
- 87.5 Selva Roshan Sivagnanasundaram Rexon (srsivagnanasundaram) — Compare: missing get cm,secret + "same way"; Secret: missing base64 -d + wrongly says plain text; ConfigMap: imprecise "why baking bad".
- 85 Olivier Moriceau (omoriceau) — cluster-build: missing 16-added/nodes/ls; Secret: missing base64 -d; Teardown: missing 16-destroyed.

## Issues / Notes
- Feedback format per [[feedback-student-facing-grading]]: where-lost only, "The <part> part: missing
  <X>." style, no praise/tips.
- zjlee nodes captured NotReady early but later pages show pods Running — cluster did work; only the
  item-1 capture and item-7 explanation cost points. Verified personally.
- srsivagnanasundaram has one factual-error deduction (says Secret stored "plain text"; it's base64).
- etran12: no Lab05 submission on file.
- Workflow artifacts: workflows/scripts/grade-lab05-wf_a85bdd9a-535.js (run wf_a85bdd9a-535).
