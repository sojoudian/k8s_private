# Report: All 300 Questions Rewritten
**Date**: 2026-10-07
**Sequence**: #05 for the day

## Summary
The first 300 questions were not usable. They tested deck recall, not Docker. A
review found 75 questions that needed the slide, 13 with a wrong or a second
correct answer, and a length pattern that let a guesser pass. All 300 are
rewritten and all 300 now pass five gates. The defective files are moved out of
the week folders so that nobody uploads them by mistake.

## What Changed
| File | State |
|------|-------|
| `week01/Week01_Pool_Blackboard.txt` + `_AnswerKey.txt` | REPLACED, 100 new questions |
| `week02/Week02_Pool_Blackboard.txt` + `_AnswerKey.txt` | REPLACED, 100 new questions |
| `week03/Week03_Pool_Blackboard.txt` + `_AnswerKey.txt` | REPLACED, 100 new questions |
| `quiz_pool_src/build2.py` | The new builder, with five gates |
| `quiz_pool_src/q2_w01.py`, `q2_w02.py`, `q2_w03.py` | The new question sources |
| `quiz_pool_src/rejected_v1/` | The defective pools and their builder, kept but moved |

## Technical Details

### The cause of the first failure
The old builder proved that a question matched a line in the deck. It never
proved that a student could answer the question without the slide. So a question
such as "What is Step 3?" passed the check and failed the student.

### The five gates in the new builder
1. **Self-contained.** The build fails if a stem or an option names a deck, a
   slide, a table, an agenda, a numbered step, a numbered layer, or an earlier
   question. 46 banned phrases are checked.
2. **Fact.** The build fails if a correct answer repeats a statement that is
   wrong in 2026, even when a lecture slide makes that statement. Six such
   statements are blocked by name.
3. **No length giveaway.** The correct option may be the strictly longest in at
   most 30 of 100, and the strictly shortest in at most 30.
4. **No answer leak.** The build fails if the correct option shares two or more
   content words with the stem that no distractor shares.
5. **Structure.** Four options, one correct, no repeated option, no repeated
   stem, no TAB and no newline in any field.

### The facts that are now correct, against the lecture slides
| Topic | What a slide says | What the pool now says |
|-------|-------------------|------------------------|
| Copy-on-write read | The lowest layer that holds the file | The highest layer that holds the file |
| Layers | Each instruction creates a layer | Only RUN, COPY and ADD create a filesystem layer |
| FROM | FROM must be the first instruction | ARG may legally appear before FROM |
| Image scanning | docker scan | Scan with a current tool; docker scan was removed in 2023 |
| EXPOSE | Tells Docker which ports are published | EXPOSE documents a port; -p publishes it |
| Unpublished ports | Not reachable from outside | Other containers on the same network still reach it |
| Drivers | bridge, null and host | bridge, host, none, overlay and macvlan |

### Content of each pool
| Pool | Main areas |
|------|-----------|
| Week 01 | Containers and VMs, cgroups and namespaces, engine and API, images and layers, copy-on-write, registries and names, Dockerfile and build cache |
| Week 02 | Base and parent images, layers and cache, EXPOSE, publishing ports, CMD, ENTRYPOINT, environment variables, registries and tags, drivers and the default bridge |
| Week 03 | Networks and drivers, network commands, name resolution, CNM and CNI, layers and copy-on-write, ephemeral containers, volumes and bind mounts and tmpfs, mount syntax, security |

## Results

Every guessing strategy was simulated against the final files.

| Pool | Always longest | Always shortest | Always A | Always B | Always C | Always D |
|------|---------------|-----------------|----------|----------|----------|----------|
| Week 01 | 23% | 15% | 21% | 28% | 30% | 21% |
| Week 02 | 28% | 20% | 30% | 26% | 20% | 24% |
| Week 03 | 22% | 20% | 29% | 18% | 20% | 33% |

Chance is 25%. No strategy passes. In the old pools, "always longest" scored 53%,
55% and 54%.

Other checks on the final files:
- 100 rows each, 10 fields per row, exactly 1 correct per row.
- 0 repeated options, 0 repeated stems, 0 empty fields.
- 0 banned phrases in any stem.
- 0 uses of "lowest layer", 0 uses of "docker scan".

## Issues / Notes
- The defective pools are at `quiz_pool_src/rejected_v1/`. Do not upload them.
- Points still arrive as 1 per question. Correct them with Bulk Edit Points.
- Blackboard gives the same points to every question inside one pool.
- A question bank imports ZIP only. Upload each `.txt` into one source test, then
  draw the pool from that test.
