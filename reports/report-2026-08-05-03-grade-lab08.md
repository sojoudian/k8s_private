# Report: Grade Lab 08 (2.5%) — 14 submissions

**Date**: 2026-08-05
**Sequence**: #03 for the day

## Summary
Graded all 14 Lab 08 ("Lab Week 12 - Workshop 3: Client-certificate user & RBAC") reports against the
5-item rubric with model answers embedded (~55% evidence + ~45% explanation-correctness). Feedback in
the professor's locked where-lost-only format. Eleven 100s; range 91-100.

## What Changed
- No student files modified (read-only grading).
- Staged 14 submissions + converted 1 docx (frsheikh) to PDF in scratchpad/lab08grade.
- Ran a background Workflow: 14 parallel graders (none <75; none re-verified).
- Personally spot-checked zjlee (3 pages, lowest with an "explanation incorrect" claim) — confirmed the
  terraform-destroy screenshot is genuinely missing; softened the wording (his teardown explanation is
  valid but omits the specific no-PVC/EBS reason, not "incorrect"). 93 stands on the missing screenshot.
- Created this report.

## Results (out of 100)
- 100: apatel638, ceonwuanaku, cgao37, frsheikh, hdhnguyen, icstyoningrum, jeessang, ldelgado8, ngraval,
  srsivagnanasundaram, tvu27.
- 93 Zhuo Jue Lee (zjlee) — teardown: missing terraform destroy "16 destroyed" screenshot; explanation
  omits the asked reason (no PVCs/EBS volumes for destroy to miss). [spot-checked]
- 92 Marjan Haghighi (mhaghighi6) — cluster-staging: missing the worker auto-join explanation.
- 91 Olivier Moriceau (omoriceau) — client-cert: missing openssl key+CSR /CN screenshot; Role part:
  missing get pods -n kube-system denied shot (mislabeled image shows get deploy -n rbac-test succeeding);
  cluster: token-location explanation off (user-data, not a kube-system Secret).

## Issues / Notes
- Very strong cohort; client-cert/RBAC material well understood. 11 perfect scores.
- omoriceau's recurring token-location inaccuracy (says kube-system Secret; it's Terraform user-data).
- No etran12 submission on file (14 students).
- Workflow artifacts: workflows/scripts/grade-lab08-wf_fd52803b-3d3.js (run wf_fd52803b-3d3).
