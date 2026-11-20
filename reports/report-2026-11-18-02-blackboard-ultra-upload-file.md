# Report: New Blackboard Ultra upload file for the mid-term exam
**Date**: 2026-11-18
**Sequence**: #02 for the day

## Summary
Blackboard Ultra showed "Unsupported question types were removed" for the upload of
`Exam_W11_Midterm40_Blackboard.txt`. I created a new upload file with the same 40 questions in the format of
the official Blackboard sample file. The content of the questions did not change.

## What Changed
- Created `quiz_pool_src/Exam_W11_Midterm40/Exam_W11_Midterm40_Blackboard_Ultra.txt`.
- No change to `Exam_W11_Midterm40_Blackboard.txt` or to any other file.

## Technical Details
- The official sample file `sample_upload_questions_original.txt` (help.anthology.com) has:
  - ASCII text;
  - CRLF line ends;
  - no line end after the last record (8 records, 7 CRLF).
- The Blackboard page says: "Don't include blank lines between records. The blank line will be processed and
  return an error."
- The old file has LF line ends and a line end after record 40. A parser that splits at each line end can
  read an empty record 41. An empty record has no question type.
- The new file has CRLF line ends and no line end after record 40, as the sample file has.
- Check: the new file has 40 records, and each record is byte-equal to the record in the old file.

## Results
- The new file: 40 multiple-choice records, ASCII, CRLF, no final line end.
- I did not upload the file to Blackboard, so the Blackboard result is not known.

## Issues / Notes
- The help page does not name the cause of the message. The empty last record is the only difference from
  the sample format that I found.
- No server started, so no port is used.
