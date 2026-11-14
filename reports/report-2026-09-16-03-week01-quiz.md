# Report: Week 1 Quiz — 20 Difficult Questions for Blackboard Ultra
**Date**: 2026-09-16
**Sequence**: #03 for the day

## Summary
This task creates a 20-question multiple-choice quiz for Week 1. Every question comes
from `week01/Week01_lecture_style_v5.pptx`. The files follow the format of the earlier
Week 04 and Week 08 quizzes.

## What Changed
- `week01/Week01_Quiz_Blackboard.txt` — new. The tab-delimited upload file.
- `week01/Week01_Quiz_AnswerKey.txt` — new. The human-readable key.
- `reports/report-2026-09-16-02-week01-quiz.md` — this file.

## Technical Details
The format matches `Week04/Week04_Quiz_Blackboard.txt` exactly. Each row holds ten
tab-separated fields: `MC`, the question, then four option and flag pairs. The file is
UTF-8 and ends with a newline.

The questions test reasoning, not recall. Each one gives a situation, then asks the
student to apply a rule from the deck. The distractors state the opposite rule, or swap
two related terms, so a partial understanding does not pass.

## Results
- 20 questions, all validated: 10 fields per row, one `correct` flag per row.
- Position balance: A×5, B×5, C×5, D×5.
- The answer sequence is BDACDACBCADBBCADCADB. No letter repeats more than twice.
- No correct answer is the longest option, per PROMPT.md.
- No duplicate options inside a question.
- Every correct answer was traced back to a literal string in the deck. 0 unsupported.

## Issues / Notes
- POINTS GOTCHA: the Ultra upload has no points field, and it defaults to 1 point per
  question. Fix it after the import with Bulk Edit Points: Select All, enter the value,
  then Update.
- Set auto-post OFF before a timed exam window, then post all grades after it closes.
- No local web service was started, so the port rule does not apply.
