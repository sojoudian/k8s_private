# Report: Blackboard "Content Error" after the upload of the Week 09 quiz
**Date**: 2026-11-06
**Sequence**: #02 for the day

## Summary
Blackboard Ultra uploaded all 20 questions of `Quiz_W09_Easy20_Blackboard.txt`, but it showed "Content Error: The content may be corrupted and could not be displayed."
The cause was Q12. Two of its options held the text `<none>`. Blackboard reads the text of an upload file as HTML, so it took `<none>` as an unknown HTML tag.
The Q12 options now use plain words. A new builder gate rejects `<`, `>` and `&` in a stem or an option.

## What Changed
- `quiz_pool_src/q_easy20_w09.py`: Q12 options changed.
  - Before: "STATUS Pending and NODE <none>", "STATUS Running and NODE masternode", "STATUS ContainerCreating and NODE workernode1", "STATUS Error and NODE <none>".
  - After: "STATUS Pending, with no node" (key), "STATUS Running on masternode", "STATUS ContainerCreating on workernode1", "STATUS Error, with no node".
- `quiz_pool_src/build_easy20_w09.py`: new GATE 14 rejects `<`, `>` and `&` in a stem or an option.
- `quiz_pool_src/Quiz_W09_Easy20/`: the upload file, the answer key, the titles and the QTI package are built again.

## Technical Details
- A scan of the old upload file found `<` or `>` only in row 12. It found no `&`, no non-ASCII byte and no byte-order mark.
- The earlier upload files of Weeks 03 to 06 hold no `<` or `>`, so this error did not occur before.
- The QTI package was never affected, because `qti_pack.py` escapes the XML text.

## Results
- All gates pass: GATE 1-7, 10, 10b, 11, 12, 13 and 14 with 0 errors. The key holds A 5, B 5, C 5 and D 5.
- `audit_easy20_w09.py`: exit code 0. The key of Q12 is still A, so no other letter moved.
- The new upload file holds 0 `<`, `>` or `&` characters.

## Issues / Notes
- The 20 questions that Blackboard already uploaded into "Quiz-4 - 2%" still hold the broken Q12. Delete them, then upload the new file again.
- The user asked me to make the Blackboard fix. The Chrome browser that I control opened the Learn@Seneca login page, because it has no Blackboard session. I do not sign in, so I closed the tab and changed nothing in Blackboard.
- The reviewer did not check this text change. The meaning of every option of Q12 is the same as before.
