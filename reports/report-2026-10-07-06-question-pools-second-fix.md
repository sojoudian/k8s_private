# Report: Second Review Fixed, and the Week 03 Deck Corrected
**Date**: 2026-10-07
**Sequence**: #06 for the day

## Summary
A second review found 5 wrong answers, 6 questions with no context, 4 unclear
answers, 12 topics that the lecture never teaches, repeated questions inside and
across the pools, and one error in the Week 03 lecture deck itself. Every item is
fixed. 53 questions are rewritten. The builder now applies a sixth gate. The
Week 03 deck is corrected and saved as v2.

## What Changed

### Question pools, replaced in place
| File | Questions rewritten |
|------|--------------------|
| `week01/Week01_Pool_Blackboard.txt` + key | 8 |
| `week02/Week02_Pool_Blackboard.txt` + key | 27 |
| `week03/Week03_Pool_Blackboard.txt` + key | 18 |

### Lecture deck
| File | Change |
|------|--------|
| `week03/Week03_lecture_style_v2.pptx` + `.pdf` | NEW. Slide 9 now reads "highest layer" |

`Week03_lecture_style_v1.pptx` is untouched.

### Builder
| File | Change |
|------|--------|
| `quiz_pool_src/build2.py` | 8 more banned phrases, and a sixth gate |
| `quiz_pool_src/qedit.py` | NEW. Replaces one question entry, found by its stem |

## Technical Details

### Wrong answers, fixed (5)
| Question | The defect | The fix |
|----------|-----------|---------|
| W03 Q25 | `docker network list` was a distractor, but it is a real alias. Confirmed on Docker 29.8.1: "Aliases: docker network ls, docker network list" | The distractors are now `show`, `status` and `get` |
| W03 Q70 | The answer "Three" fought Q79, because tmpfs does not survive removal | The question now asks which options keep data: volumes and bind mounts |
| W03 Q2 | "Every network has its own name resolution" fought Q9, Q36 and Q43, and the `none` network has no address range | The question is now scoped to a container joining a bridge network |
| W02 Q75 | The stem assumed a push is rejected when no registry is named. A bare name goes to Docker Hub | The question now asks about an access denied message |
| W02 Q42 | The stem said the Ubuntu image has no CMD, which is false, and a second option was also correct | The question now asks what happens with a shell and no terminal attached |

### Questions with no context, fixed (6)
W01 Q43, Q44 and Q46, W02 Q59, and W03 Q79 and Q80 said "in this model", "this
split", "the two instructions" or "which of the three". A pool shows its
questions in random order, so there was nothing to point at. Each stem now
carries its own situation. The eight phrases are added to gate 1, so the build
fails if one appears again.

### Unclear or self-contradicting answers, fixed (4)
- W01 Q16: the stem said the container escaped a limit while the answer said the
  limit was missing. The stem now describes a container starving the others.
- W01 Q60: "one layer per build step" fought Q55, which states that FROM adds no
  layer. The question now asks about separate RUN and COPY lines.
- W02 Q37 and Q54: "anywhere in the file" was wrong, because CMD and ENTRYPOINT
  must follow FROM. One now reads "anywhere after the FROM line", and the other
  is replaced.
- W02 Q97: "very close to the same mechanism" was vague. The question now asks
  what the engine sets up on a Linux host.

### Topics the lecture never teaches, removed (12)
Each one was checked against the deck text before it was removed: image digests,
the delete marker, PID 1 and signals, the `--entrypoint` flag, the `latest` tag,
publishing to 127.0.0.1, renaming a container, and combining RUN lines. Each is
replaced by a question on material the deck does teach. The build context was
also named by the review, but the Week 01 deck does teach it, so that question
stays.

### Repeated questions, removed
- **Across pools.** One stem appeared in two pools. Identical stems across the
  three pools: now 0.
- **Inside one pool.** 11 questions shared a correct answer with a near-identical
  stem, so one gave away the other. All are replaced.
- `-p` and `-P` differed only by one capital letter. The options now carry
  distinct text instead.

### The sixth gate
The build now fails when two questions in one pool share the same correct answer
AND their stems overlap by half or more of their words.

### The deck error
Slide 9 of the Week 03 lecture said a read is served by the "lowest layer that
has the file". A read is served by the highest layer. The quiz was correct and
the slide was wrong, so a student who studied the slide would have lost the mark.
The slide now reads "highest layer" in `Week03_lecture_style_v2.pptx`.

## Results

| Pool | Rows | Problems | Duplicate stems | In-pool leaks | Longest | A | B | C | D |
|------|------|----------|-----------------|---------------|---------|---|---|---|---|
| Week 01 | 100 | 0 | 0 | 0 | 25% | 17 | 30 | 31 | 22 |
| Week 02 | 100 | 0 | 0 | 0 | 26% | 25 | 29 | 24 | 22 |
| Week 03 | 100 | 0 | 0 | 0 | 25% | 31 | 19 | 17 | 33 |

- Identical stems across the three pools: 0.
- Answer keys agree with the upload files: 100 of 100 in each pool.
- Chance is 25%. No guessing strategy beats it.

## Issues / Notes
- Points still arrive as 1 per question. Correct them with Bulk Edit Points.
- One Blackboard pool gives the same points to every question inside it.
- `quiz_pool_src/rejected_v1/` still holds the first, defective 300. Do not
  upload them.
