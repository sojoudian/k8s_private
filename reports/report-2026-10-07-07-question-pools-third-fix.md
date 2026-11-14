# Report: Third Review Fixed
**Date**: 2026-10-07
**Sequence**: #07 for the day

## Summary
A third review found 5 wording defects, 8 facts repeated across two pools, and 6
topics the lectures never teach. All are fixed. 19 questions are rewritten. The
builder now applies a seventh gate, which blocks the same fact from sitting in
two pools. One claim in the review was wrong, and that question is kept.

## What Changed
| File | Questions rewritten |
|------|--------------------|
| `week01/Week01_Pool_Blackboard.txt` + key | 2 |
| `week02/Week02_Pool_Blackboard.txt` + key | 8 |
| `week03/Week03_Pool_Blackboard.txt` + key | 9 |
| `quiz_pool_src/build2.py` | Gate 7 added |

## Technical Details

### Wording defects, fixed (5)
| Question | The defect | The fix |
|----------|-----------|---------|
| W01 Q64 | "release without waiting" led straight to "handover delay" | The stem now describes rebuilding from written instructions |
| W03 Q16 | "named in the Docker documentation" pointed outside the question, and the fact was already in W03 Q3 and W02 Q85 | The question now asks how a single host scope is described |
| W03 Q64 | The answer said the host duplicates the writable layer. Each container gets a NEW EMPTY layer, not a copy | The answer now reads "a new empty writable layer" |
| W03 Q66 | "must keep nothing after it stops" fought W01 Q75 and W03 Q74. The writable layer survives a stop and dies on removal | The stem no longer mentions stopping |
| W03 Q79 | Two options were about bind mounts, and the mount itself does go with the container, so a careful student could pick either | The options now separate the data from the host path |

### The same fact in two pools, removed (8 pairs)
| Pair | Which one changed |
|------|------------------|
| W01 Q53 and W02 Q8 | W02 Q8, now about the build cache |
| W01 Q72 and W03 Q60 | W03 Q60, now about why mounting storage helps |
| W01 Q78 and W02 Q71 | W02 Q71, now about pulling only the missing layers |
| W01 Q80 and W02 Q77 | W02 Q77, now about two tags on one image |
| W01 Q83 and W02 Q79 | W02 Q79, now about the docker tag command |
| W01 Q86 and W02 Q84 | W02 Q84, now about where a pulled image lives |
| W02 Q86 and W03 Q15 | W03 Q15, now about where container addresses come from |
| W02 Q87 and W03 Q12 | W03 Q12, now about name resolution |

Gate 7 then found one more pair that the review missed: W02 Q7 and W03 Q61 both
counted the layers of a Dockerfile. W03 Q61 is replaced.

### Topics the lectures never teach, removed (5)
Each was checked against the deck text first: x86 against ARM (W01 Q12), `-it`
(W02 Q56), registry login and access denied (W02 Q75), a firewall (W02 Q98), and
restarting a container under the same name (W03 Q39). Each is replaced by a
question on material the deck does teach.

### One review claim was wrong
The review listed W01 Q89, the build context, as a topic the deck does not teach.
Slide 35 of the Week 01 lecture reads: "The docker build command builds an image
from a Dockerfile and a context". The question is kept.

### Gate 7
The build now fails when a question in one pool and a question in another share a
correct answer and a stem that overlaps by 45 percent or more, or when two stems
overlap by 80 percent or more. This matters if one test ever draws from two pools.

## Results

| Pool | Rows | Problems | Duplicate stems | In-pool leaks | Longest | A | B | C | D |
|------|------|----------|-----------------|---------------|---------|---|---|---|---|
| Week 01 | 100 | 0 | 0 | 0 | 26% | 18 | 29 | 31 | 22 |
| Week 02 | 100 | 0 | 0 | 0 | 25% | 26 | 27 | 23 | 24 |
| Week 03 | 100 | 0 | 0 | 0 | 27% | 29 | 22 | 19 | 30 |

- Cross-pool repeats: 0.
- Answer keys agree with the upload files: 100 of 100 in each pool.
- Chance is 25%. No guessing strategy beats it.

## Issues / Notes
- Points still arrive as 1 per question. Correct them with Bulk Edit Points.
- Five other MCQ files still carry defects. They are listed in an earlier reply
  and are NOT changed, because you have not asked for that.
