# Report: Quiz 3 question pool (100 questions)
**Date**: 2026-10-23
**Sequence**: #02 for the day

## Summary
I wrote a pool of 100 multiple-choice questions for Quiz 3 and the upload file for
Blackboard. Blackboard draws 20 questions at random, at 5 points each. The key holds
25 correct answers for each letter, because the upload format cannot turn on option
shuffling. The content comes from the three lectures after Quiz 2: Pods, ReplicaSets
and Deployments; Rollouts, Labels, Selectors and Services; Volumes. Ten gates and one
independent audit pass with 0 defects.

## What Changed
- `quiz_pool_src/q3_quiz3.py` — new. The 100 questions, grouped by topic.
- `quiz_pool_src/build3.py` — new. The builder. It imports the seven gates of
  `build2.py` and adds three gates of its own.
- `quiz_pool_src/audit3.py` — new. The independent audit. It reads the upload file
  only, and it imports no question source.
- `quiz_pool_src/Quiz03_Pool_Blackboard.txt` — new. The upload file, 100 rows.
- `quiz_pool_src/Quiz03_Pool_AnswerKey.txt` — new. The answer key for the instructor.

## Technical Details
Scope. Quiz 1 came at the end of the second week and Quiz 2 at the end of the fourth
week. Quiz 3 closes the seventh week, so the pool covers the three lectures between
them: `Week05/lecture_week05_v3.pptx`, `Week06/Week06_lecture_style_v7.pptx` and
`Week07/Week07_lab_style_v3.pptx`. I extracted the text of all 78 slides first.

Topic counts: Pods 16, Pod descriptor and kubectl 8, Labels and Namespaces 10,
ReplicaSets 11, Deployments and rollouts 17, Services and Ingress 22, Volumes and
storage 16.

Gates. `build2.py` supplies gate 1 (each question stands on its own), gate 2 (the
correct answer is true today), gate 3 (no length giveaway), gate 4 (the stem does not
repeat its own answer), gate 5 (structure), gate 6 (no two questions of one pool share
a fact) and gate 7 (no repeat across pools). `build3.py` adds:
- Gate 8: the key holds 25 A, 25 B, 25 C and 25 D.
- Gate 8b: no more than 4 equal letters together.
- Gate 9: the correct option is the strictly longest in 20 to 30 questions.
- Gate 10: no question repeats a fact of the three Docker pools.

Balanced key. The first build produced a clustered key. The cause: an md5 integer
holds about 38 decimal digits, so a hand made shuffle of 100 items runs out of digits
after some 25 swaps and leaves the tail in order. The builder now uses a seeded
generator, and gate 8b checks the result.

Facts that change with the Kubernetes version. I checked two against the
documentation. The `gitRepo` volume is permanently off from v1.36 and absent from
v1.37, so no correct answer says that it works; question 99 asks for the init container
and `emptyDir` pattern instead. The `Endpoints` API is deprecated from v1.33, so no
question names it.

No command output. The pool holds no printed output of a command, so a cluster is not
needed to prove an answer. Every answer is documented Kubernetes behaviour. No cluster
runs on this machine at the moment, and I started none.

## Results
- `build3.py`: 0 errors on gates 1 to 10. Correct option longest in 26, shortest in 24.
  Key: A 25, B 25, C 25, D 25. Longest run of one letter: 4.
- `audit3.py`: 100 rows, 10 fields each, exactly one correct option per row.
  Guessing by the longest option wins 27 of 100. Guessing by the shortest wins 29 of
  100. Guessing by the most words wins 27 of 100. Random guessing wins 25 of 100.
  Answer leaks 0. Pairs at risk 0.
- Chance that one draw of 20 from 100 holds both questions of a pair: 3.838%, one in
  26. With 0 pairs at risk, the joint risk is 0.
- Rewrites during the work: 3 twin questions replaced, 11 options tuned for length,
  5 answers corrected after a factual read, 1 answer leak repaired, 1 Pod name with
  digits removed.

## Issues / Notes
- The upload format carries no points field. Every question arrives at its default
  value. Set 5 points with Bulk Edit Points after the import.
- The files state no date, no time limit, no number of attempts and no password.
- Three questions with a near equal twin were cut: the second API version question,
  the second replica count question and the `port` question beside `targetPort`. Each
  pair let a student reason from one question to the other.
