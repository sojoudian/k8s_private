# Report: Grade Lab 06 (2.5%) — 14 submissions

**Date**: 2026-08-05
**Sequence**: #01 for the day

## Summary
Graded all 14 Lab 06 ("Lab Week 12 - Workshop 1: ServiceAccounts", kubeadm cluster + SA/token/JWT/
authn-vs-authz/ambassador-sidecar) reports against the 5-item rubric with model answers embedded
(~55% evidence + ~45% explanation-correctness). Feedback in the professor's locked where-lost-only
format ("The <part> part: missing <X>"). Ten 100s; range 95-100.

## What Changed
- No student files modified (read-only grading).
- Staged 14 submissions + converted 1 docx (frsheikh) to PDF in scratchpad/lab06.
- Ran a background Workflow: 14 parallel graders (none needed re-verify; all >=95, no red flags).
- Personally spot-checked zjlee (3 pages) — grade 98 confirmed (only the terraform "16 added" shot missing).
- Created this report.

## Results (out of 100)
- 100: Ayush Patel (apatel638), Christian Emeka Onwuanaku (ceonwuanaku), Faizan Razzakbhai Sheikh
  (frsheikh), Huu Duc Huy Nguyen (hdhnguyen), Indah Cahyani Styoningrum (icstyoningrum), Joe-Smith
  Effiong Essang (jeessang), Leandro Delgado (ldelgado8), Marjan Haghighi (mhaghighi6), Nrupad
  Ganeshkumar Raval (ngraval), Tony Vu (tvu27).
- 99 Selva Roshan Sivagnanasundaram Rexon (srsivagnanasundaram) — cluster-build explanation omits why
  worker join retries in a loop + the CA-cert-hash.
- 98 Chenyu Gao (cgao37) — JWT explanation doesn't distinguish sub (identity) from namespace (scope).
- 98 Zhuo Jue Lee (zjlee) — cluster-build missing the terraform "16 added" screenshot (verified; 3-page
  report otherwise complete and correct — nodes Ready, all 5 tasks + explanations present).
- 95 Olivier Moriceau (omoriceau) — cluster-build token-location explanation incomplete (join token +
  CA-cert-hash staged in worker user-data by Terraform, not just a kube-system Secret); pod-queries-API
  missing the no-token 403 as system:anonymous (that screenshot actually shows system:serviceaccount:
  week12:clo835).

## Issues / Notes
- Very strong cohort on this lab; ServiceAccounts material well understood.
- ngraval improved markedly (100) vs earlier labs where explanations were absent.
- Workflow artifacts: workflows/scripts/grade-lab06-wf_33b1fd20-538.js (run wf_33b1fd20-538).
