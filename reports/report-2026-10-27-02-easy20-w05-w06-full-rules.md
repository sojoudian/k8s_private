# Report: The Week 05 and Week 06 easy quiz against every design rule

**Date**: 2026-10-27
**Sequence**: #02 for the day

## Summary

The quiz now meets every design rule that a file can carry. Two rules were
open: the question titles and the option order. Both are closed. The builder
has two new gates, and the independent audit tests the titles. Three rules stay
with the instructor, because a file cannot hold them.

## What Changed

- `quiz_pool_src/q_easy20_w56.py` — 12 questions carry a new `fix` field. The
  field holds the four options in their logical order.
- `quiz_pool_src/build_easy20_w56.py` — rewritten. It adds GATE 12 and GATE 13,
  and it balances the letters around the fixed orders.
- `quiz_pool_src/qti_pack.py` — it takes an optional title file. Without the
  file it works as before, so the two earlier quizzes stay as they are.
- `quiz_pool_src/audit_easy20_w56.py` — it tests the titles.
- `Quiz_W05W06_Easy20/Quiz_W05W06_Easy20_Titles.txt` — new. It holds one
  neutral title for each question.
- The upload file, the answer key and the QTI package are built again.

## Technical Details

### The title rule

The rule: "Use neutral question titles, only an ID and a topic. A title must
not show the answer."

Before, the QTI title held the first 60 characters of the stem. Now each title
has the form `clo835-e56-001 pods`. GATE 13 tests the form, and it rejects a
title that holds an option. The audit tests the same facts from the ZIP file.

### The order rule

The rule: "Put numbers and names in a logical order, for example small to
large." A second rule asks for the same number of correct answers at A, B, C
and D.

The two rules meet when the builder moves the correct option to a target
letter. The solution: 12 questions hold a number list, a time list or a name
list, and they keep that order. Their letters follow from the order. The other
8 questions take the letters that are left, so the count stays 5 for each
letter.

The 12 fixed orders:

- Q1 one node, two nodes, three nodes, any node
- Q3 and Q18 the commands in alphabetical order
- Q4 apps/v1, apps/v1beta1, deployment/v1, v1
- Q7 metadata, replicas, selector, template
- Q8 and Q19 the object names in alphabetical order
- Q9 before, at the same moment, after one Pod, after every Pod
- Q10 the strategy names in alphabetical order
- Q12 containerPort, nodePort, port, targetPort
- Q13 ClusterIP, NodePort, LoadBalancer, ExternalName, from the smallest reach
  to the largest
- Q14 the component names in alphabetical order

## Results

`build_easy20_w56.py`:

- GATE 1 to 7: 0 errors
- GATE 10: 0 repeats of an earlier pool
- GATE 11: 0 feedback errors
- GATE 12: 0 errors, 12 questions keep a logical order
- GATE 13: 0 errors
- GATE 9: longest 6, shortest 6
- GATE 8: A 5, B 5, C 5, D 5
- GATE 8b: longest run 2

`audit_easy20_w56.py`, exit code 0:

- rows: 20; letters A 5, B 5, C 5, D 5
- guess by the longest option 6, by the shortest 6, by the most words 2
- answer leaks 0; question pairs at risk 0
- records in the key 20; files in the ZIP 21
- titles in the title file 20; errors 0

## Issues / Notes

Three rules stay open, and a file cannot close them:

1. "Get an independent reviewer to check each question before the quiz."
   Only the gates and the audit checked the questions. A person must read
   them.
2. "Run all the code." No cluster and no Docker daemon run on this machine.
   No question prints command output, but a live cluster can prove the
   behavior claims.
3. "Show students only the grade until all students finish the quiz." That is
   a Blackboard setting, not a part of the file.

The rule about the question statistics applies after the quiz.
