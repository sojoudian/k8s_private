# Report: Trim CLO835 exam from 50 to 40 (keep hardest 26 MC)
**Date**: 2026-07-13
**Sequence**: #03 for the day

## Summary
Reduced the exam from 50 to 40 questions by keeping only the 26 hardest multiple-choice questions and leaving the 9 multiple-answer and 5 true/false untouched (26 + 9 + 5 = 40). Difficulty was scored by a blind 3-judge panel rather than the coarse hard/very_hard flag, and the 10 lowest-difficulty MC were dropped. Regenerated the Blackboard upload file and answer key.

## What Changed
- `CLO835_Final_Exam_Blackboard.txt` (overwritten) - now 40 tab-delimited rows (26 MC / 9 MA / 5 TF).
- `CLO835_Final_Exam_AnswerKey.md` (overwritten) - matching 40-question review copy.
- Scratch only: `judge_mc.js` (3-judge difficulty panel), `mc_for_judging.json` (36 MC input), `mc_ranked.json` (panel output), `select_40.py` (selection), `exam_questions_40.json` (final set).

## Technical Details
- Panel: 3 independent judges each scored all 36 MC 1-10 for difficulty (cognitive level, distractor closeness, subtlety, required reasoning), blind to each other, effort=high. 3 agents, 0 errors, ~34s, 104K tokens. Inter-judge agreement was high (most spreads within 1 point).
- Selection: averaged the 3 scores per question; sorted hardest-first with tie-break (avg desc, then very_hard flag, then original n); kept top 26. Kept-MC difficulty band avg 7.33 (hardest) down to 5.00 (26th); dropped 10 ranged 5.00 down to 3.33.
- Dropped items were the more recall-oriented MC (e.g. Docker architecture diagram roles, namespaced-resource lookup, cloud-controller-manager naming, gitRepo volume fact, EKS Fargate definition) - genuinely easier, not lower quality.
- Recombined 26 MC + 9 MA + 5 TF, re-sorted by topic bucket then original order for coherent flow, renumbered 1-40, reran the deterministic Blackboard formatter.

## Results
Validation passed: 40 lines, 26 MC / 9 MA / 5 TF, 0 structural errors, no non-ASCII, HTML-safe. Topic coverage still balanced across all 11 areas (3-5 questions each; every topic represented). MA and TF sets unchanged as requested.

## Issues / Notes
- The 50-question source (`exam_questions.json`) and the full ranking are retained in scratch, so restoring any dropped MC or reverting to 50 is a one-command reselect.
- Points per question still set in the Blackboard upload dialog (e.g. 2.5 x 40 = 100).
