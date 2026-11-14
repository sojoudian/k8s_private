# Report: Grade Lab 03 (2.5%) — 15 submissions

**Date**: 2026-07-28
**Sequence**: #03 for the day

## Summary
Graded all 15 Lab 03 ("Intro to Kubernetes with kind") report submissions against the 7-step rubric
(EC2 launch, tooling/versions, kind cluster, nginx pod, NodePort service+curl, deployment scale,
rolling update+undo) plus the optional Dashboard bonus. Marked out of 100 with ~60% screenshot
evidence + ~40% required explanation per step; bonus +5 capped at 100. Produced a per-student table
of grade + where-lost + short feedback for the professor.

## What Changed
- No student files modified (read-only grading).
- Staged all 15 submissions with clean usernames + converted 2 docx (etran12, frsheikh) to PDF in scratchpad.
- Ran a background Workflow: 15 parallel graders (one per PDF) + a re-verify pass on the 5 low/flagged ones (20 agents).
- Personally spot-checked etran12 (empty file, unpacked docx) and cgao37 (read all 6 pages) to confirm the two most contestable grades.
- Created this report.

## Technical Details
Method: each grader Read the full PDF (rendering screenshots) and scored each step for BOTH evidence
(screenshot with the expected output — kind-kind context, 1/1 Running, NodePort 80:3xxxx, curl
"Welcome to nginx" HTML, 5 pods, rollout undo) AND the required conceptual explanation. Low/flagged
submissions (<80 or red-flagged) were independently re-graded; reconciliation took the higher score
to protect students from a grader page-miss. I personally confirmed etran12 (empty) and cgao37 (54).

## Results (out of 100, sorted)
- 100 Christian Emeka Onwuanaku (ceonwuanaku) — flawless 7 steps; skipped optional bonus.
- 100 Faizan Razzakbhai Sheikh (frsheikh) — exemplary + full HTTPS Dashboard bonus.
- 100 Indah Cahyani Styoningrum (icstyoningrum) — complete + bonus; nit: created at replicas=5 (scale no-op).
- 100 Leandro Delgado (ldelgado8) — complete + bonus; same create-at-5 nit.
- 96 Joe-Smith Effiong Essang (jeessang) — no EC2-console shot; describe truncated; missing why-Deployment explanation.
- 96 Tony Vu (tvu27) — create-at-5 (no 3->5); terse Service/rolling explanations; SG-port mismatch; bonus unfinished.
- 94 Selva Roshan Sivagnanasundaram Rexon (srsivagnanasundaram) — generic Events explanation; scale-to-5 not clearly shown; port typo.
- 92 Ayush Patel (apatel638) — missing Service-types explanation (step5); thin step3; describe truncated.
- 92 Zhuo Jue Lee (zjlee) — missing rollout undo output; 3->5 not shown; loose NodePort/kindnet; no name labels.
- 85 Marjan Haghighi (mhaghighi6) — explanations weak/missing across steps; no EC2-console shot; 25GB not 32; rolling mislabeled blue-green.
- 71 Olivier Moriceau (omoriceau) [re-verified] — most graded explanations absent; rollout undo not run; bonus login failed.
- 70 Huu Duc Huy Nguyen (hdhnguyen) [re-verified] — used Cloud9 not EC2 (no step-1 console); missing docker version; explanations partial.
- 54 Chenyu Gao (cgao37) [re-verified, I confirmed] — complete name-labeled screenshots but ZERO written explanations (-40%/step); no EC2 step-1; Cloud9.
- 48 Nrupad Ganeshkumar Raval (ngraval) [re-verified] — no conceptual explanations; no curl HTML/Events/EC2 console; some pods mid-ContainerCreating.
- 0 Elvis Tran (etran12) [re-verified, I confirmed] — empty/corrupted file (blank PDF; docx has no media or text). Recommend re-submission.

## Issues / Notes
- etran12: submission is genuinely empty (unpacked docx = no media, no body text). Likely a bad
  upload; recommended requesting a re-submission before finalizing a 0.
- cgao37 (54) & ngraval (48): did the technical work correctly but wrote no explanations; ~40%/step
  lost. If the professor weights explanations lighter, these two rise. Flagged the rubric lever.
- hdhnguyen & cgao37 used Cloud9 instead of the EC2 kind-lab instance, so step-1 "capture the running
  instance in the EC2 console" cannot be met that way. Flagged for the professor to allow-or-not.
- Workflow artifacts: workflows/scripts/grade-lab03-wf_17a4343b-75f.js (run wf_17a4343b-75f).
