# Report: Question Pools for Lectures 1, 2 and 3
**Date**: 2026-10-07
**Sequence**: #04 for the day

## Summary
Three Blackboard question pools are built, 100 multiple-choice questions each, 300
in total. Every question comes from the text of its lecture deck. A verifier
proves that the line each question rests on really exists on the slide it names.
No question comes from a chart or from a picture.

## What Changed
| File | Purpose |
|------|---------|
| `week01/Week01_Pool_Blackboard.txt` | 100 MCQ, tab-delimited, ready to upload |
| `week01/Week01_Pool_AnswerKey.txt` | The key, with the slide number of each question |
| `week02/Week02_Pool_Blackboard.txt` | 100 MCQ |
| `week02/Week02_Pool_AnswerKey.txt` | The key |
| `week03/Week03_Pool_Blackboard.txt` | 100 MCQ |
| `week03/Week03_Pool_AnswerKey.txt` | The key |
| `quiz_pool_src/build.py` | The builder and the verifier |
| `quiz_pool_src/q_w01.py`, `q_w02.py`, `q_w03.py` | The question sources |

## Technical Details

### Source decks
| Pool | Deck | Slides |
|------|------|--------|
| Week 01 | `week01/Week01_lecture_style_v5.pptx` | 38 |
| Week 02 | `week02/Week02_lecture_style_v1.pptx` | 27 |
| Week 03 | `week03/Week03_lecture_style_v1.pptx` | 15 |

### How a repeat of the Week 01 quiz failure is prevented
The earlier Week 01 quiz shipped two questions a student could not answer. Both
asked about numbers inside a survey chart. The builder now blocks that class of
error:

1. Every question carries a `src` field. The builder normalises the text and
   proves that `src` appears on the slide the question names. If it does not, the
   build FAILS and nothing is written.
2. No question is taken from a slide whose content is only a picture.
3. Every question has exactly 4 options and exactly 1 correct answer.
4. No option is repeated inside a question. No question stem is repeated.
5. No TAB and no newline sits inside any field, so the upload cannot break.

All 300 questions pass. The build exits with an error if even one fails.

### Spread
Each pool keeps the slide spread of the deck. A slide that carries more teaching
text gets more questions.

| Pool | Slides covered | Questions per slide |
|------|---------------|---------------------|
| Week 01 | 20 | 2 to 9 |
| Week 02 | 16 | 3 to 11 |
| Week 03 | 12 | 4 to 11 |

### Correct-answer position
The builder shuffles the options with a fixed seed per question, so the output is
reproducible and the correct answer is not always in the same place.

| Pool | A | B | C | D |
|------|---|---|---|---|
| Week 01 | 25 | 22 | 23 | 30 |
| Week 02 | 30 | 20 | 28 | 22 |
| Week 03 | 22 | 26 | 27 | 25 |

### File format
Tab-delimited, one question per line:

```
MC <TAB> question <TAB> answer1 <TAB> correct|incorrect <TAB> ... (4 answers)
```

## Results
- 300 questions, 0 verifier errors.
- 100 rows in each file, 10 fields in every row, exactly 1 `correct` per row.
- 0 repeated options, 0 repeated stems.
- 15 answers were also read by eye against the deck line they cite. All 15 match.

## Issues / Notes
- **Points.** The Blackboard Ultra upload has no points field. Every question
  arrives worth 1 point. Correct it with Bulk Edit Points: Select All, enter the
  value, then Update.
- **One point value per pool.** Blackboard gives the same points to every question
  inside one question pool. You cannot set points per question inside a pool.
- **A bank imports ZIP only.** Upload each `.txt` into one source test, then draw
  the pool from that test with Add question pool.
- The questions test the deck as it is written. Week 01 slides 29 and 30 are
  duplicates in the deck, so only slide 29 is used.
