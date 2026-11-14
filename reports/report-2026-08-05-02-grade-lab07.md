# Report: Grade Lab 07 (2.5%) — 14 submissions

**Date**: 2026-08-05
**Sequence**: #02 for the day

## Summary
Graded all 14 Lab 07 ("Lab Week 12 - Workshop 2: Roles, RoleBindings & ClusterRoles") reports against
the 7-item rubric with model answers embedded (~55% evidence + ~45% explanation-correctness). Feedback
in the professor's locked where-lost-only format. Nine 100s; range 91-100.

## What Changed
- No student files modified (read-only grading).
- Staged 14 submissions + converted 1 docx (frsheikh) to PDF in scratchpad/lab07grade.
- Ran a background Workflow: 14 parallel graders + re-verify (mhaghighi6 red-flagged for AI affirmation,
  cleared to 100 — screenshots are own cluster, consistent 2026-07-23 timestamps).
- Created this report.

## Results (out of 100)
- 100: apatel638, ceonwuanaku, cgao37, frsheikh, hdhnguyen, icstyoningrum, mhaghighi6, ngraval, tvu27.
- 97 Selva Roshan Sivagnanasundaram Rexon (srsivagnanasundaram) — cross-namespace: missing post-edit
  curls (week12-2 SA lists week12-1 services 200, own 403).
- 96 Joe-Smith Effiong Essang (jeessang) — cross-namespace: missing the week12-2 pod curls (200/403);
  only the edited RoleBinding subjects list shown.
- 96 Leandro Delgado (ldelgado8) — ClusterRole: missing the persistentvolumes 403(RoleBinding)/
  200(ClusterRoleBinding) curls (Fig 11 shows leftover week12-2 services 403).
- 95 Olivier Moriceau (omoriceau) — cluster-staging explanation partly misses token location (user-data,
  not kube-system Secret); two-namespaces: missing SA/proxy-pod creation + get pods -n week12-1 shot.
- 91 Zhuo Jue Lee (zjlee) — cross-namespace: missing the verification curls + the "subjects can name a
  SA from any namespace while the binding grants access only in its own namespace" explanation.

## Issues / Notes
- Strong cohort; cross-namespace-subject (item 5) and ClusterRole-scope (item 6) verification curls were
  the most common gap among the sub-100s.
- mhaghighi6 AI-use affirmation reviewed and cleared (own cluster evidence) — no penalty.
- No etran12 submission on file (14 students).
- Workflow artifacts: workflows/scripts/grade-lab07-wf_26847fa6-652.js (run wf_26847fa6-652).
