# Report: 50-question CLO835 final exam for Blackboard Ultra
**Date**: 2026-07-13
**Sequence**: #02 for the day

## Summary
Built a 50-question difficult final exam grounded strictly in the finalWork/ course slides and produced a Blackboard-Ultra-uploadable tab-delimited file plus a human-readable answer key. Questions were authored per-topic by agents that actually read the rendered slides, then every question and answer key was adversarially verified against the source slides before selection. Final mix: 36 multiple-choice, 9 multiple-answer (select all), 5 true/false, balanced across all 11 topic areas.

## What Changed
- `CLO835_Final_Exam_Blackboard.txt` (NEW) - the upload file: 50 tab-delimited rows (MC/MA/TF), CRLF, ASCII-only, HTML-escaped, no header.
- `CLO835_Final_Exam_AnswerKey.md` (NEW) - review copy: each question with options, correct answers marked, rationale, source slide, plus upload instructions.
- Scratch only: `exam_workflow.js` (22-agent author+verify workflow), `format_exam.py` (deterministic Blackboard formatter), `exam_questions.json` (verified question set).

## Technical Details
- Coverage buckets (11): Docker fundamentals, Dockerfile/images, Docker networking, Docker storage/security, K8s intro/arch, Pods/ReplicaSets, Deployments/rollouts, Services/Ingress, Volumes, EKS, PV/PVC/StorageClass/StatefulSets. Per-bucket caps summed to exactly 50.
- Workflow: pipeline(BUCKETS, author, verify). Authors read ~15-25 of their JPGs (from the 367-slide render) and wrote 6 hard questions each (66 raw); adversarial verifiers re-derived each answer from the slides and returned ACCEPT/REVISE/REJECT + groundedness + distractor + difficulty checks. Script kept only grounded survivors, applied any REVISE answer corrections, then culled to 50 by difficulty rank with per-bucket caps + backfill. 22 agents, 0 errors, 971K tokens, ~6 min.
- Blackboard format: `MC<TAB>q<TAB>opt<TAB>correct|incorrect...`, `MA` same with 2+ correct, `TF<TAB>q<TAB>true|false`. No header, CRLF line endings.
- Sanitizing: unicode punctuation -> ASCII (no em dashes/smart quotes), tabs/newlines stripped from fields, HTML-escaped (&,<,>) for the txt only since Blackboard renders answer text as HTML. Rephrased one option that contained <user>/<repo> to plain wording.

## Results
Structural validation passed: 50 lines, 36 MC / 9 MA / 5 TF, 0 empty fields, every MC exactly 1-correct-of-4, every MA 2+ correct with >=1 incorrect, every TF a valid true/false, no non-ASCII, no em dashes/smart quotes. Files written to the project root.

## Issues / Notes
- Points per question are NOT in the file (Blackboard has no points column in this format); set them in the upload dialog (e.g. 2 x 50 = 100).
- Answer key is for the instructor only - do not upload it.
- Questions are intentionally hard (scenario/analysis, close distractors); if any prove too hard for the cohort, individual items can be swapped from the surplus that was culled (resume the workflow from cache to regenerate).
