# Report: A Hand-Picked Set of 20 Harder Questions
**Date**: 2026-10-07
**Sequence**: #08 for the day

## Summary
Twenty questions are selected by hand from the three Week 01 to Week 03 pools.
Each one asks the student to apply a rule to a situation, to tell two similar
things apart, or to state a fact that runs against intuition. No question is
plain recall. The set passes the same gates as the pools.

## What Changed
| File | Purpose |
|------|---------|
| `CLO835_Hard20_Blackboard.txt` | 20 MCQ, tab-delimited, ready to upload |
| `CLO835_Hard20_AnswerKey.txt` | The key, with the source pool of each question |
| `quiz_pool_src/pick20.py` | The selection, by stem, with its checks |

## Technical Details

### How the 20 were chosen
| Kind | Examples |
|------|----------|
| Apply a rule to a situation | A developer edits line 2 of a ten line Dockerfile. Which layers rebuild? |
| Tell two similar things apart | ENTRYPOINT with CMD against CMD alone, when the user types a word |
| A fact that runs against intuition | A read is served by the HIGHEST layer; EXPOSE publishes nothing; an unpublished port is still reachable on the same network; Kubernetes isolation is OFF by default |
| Two steps in one question | A 512 MB cap and hidden host processes, in that order |

### Spread
| Source | Questions |
|--------|-----------|
| Week 01 | 7 |
| Week 02 | 7 |
| Week 03 | 6 |

### Checks
- 20 rows, 10 fields each, exactly one correct per row.
- 0 repeated options, 0 repeated stems, 0 banned phrases.
- No two of the twenty carry the same fact.
- Correct option is the longest in 6 of 20 and the shortest in 5 of 20.
- Key position: A 6, B 3, C 6, D 5.
- The option order differs from the pools, so a student cannot carry an order over.

## Results
The file uploads the same way as a pool file: open a test, select the plus sign,
then **Upload questions from file**. All 20 questions land in that test, so no
question pool is needed for a 20 question quiz.

## Issues / Notes
- Points arrive as 1 per question. Correct them with Bulk Edit Points.
- These 20 also remain inside the three pools. Do not draw a pool from a pool
  file and run this set in the same assessment.
