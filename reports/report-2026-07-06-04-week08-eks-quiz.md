# Report: Week 8 EKS quiz — 10 easy MCQs for Blackboard Ultra
**Date**: 2026-07-06
**Sequence**: #04 for the day

## Summary
Authored a 10-question easy multiple-choice quiz from `Week08/Week08_lecture_style_v3.pptx` in the Blackboard tab-delimited upload format, plus a human-readable answer key. Intended grading: 10 points per question = 100 total.

## What Changed
- `Week08/Week08_Quiz_Blackboard.txt` — upload file, 10 lines, `MC<TAB>question<TAB>option<TAB>correct|incorrect ×4` (same format as the Week04 quiz).
- `Week08/Week08_Quiz_AnswerKey.txt` — key with `*` on correct options + answer summary.

## Technical Details
Coverage maps 1:1 to lecture slides: managed vs self-managed split (Q1), control-plane cost $0.10/h ≈ $73/mo (Q2), no-SSH/kubectl-only control plane (Q3), worker-node options (Q4), etcd in the managed multi-AZ control plane (Q5), VPC CNI real VPC IPs (Q6), IAM authenticates / RBAC authorizes (Q7), `aws eks update-kubeconfig` (Q8), eksctl → CloudFormation (Q9), volume lifecycle tied to the pod (Q10). House quiz rules applied: correct-answer positions balanced (A×3, B×2, C×3, D×2), correct answer never the longest option, plausible distractors.

## Results
Both files written under Week08/. Ready to import via Blackboard Ultra test upload.

## Issues / Notes
- **Points**: the Blackboard upload format has no points field — after import, set each question to 10 points in Ultra (or set the test total to 100 with equal weighting). This is noted in the answer-key header.
