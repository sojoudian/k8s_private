# Report: Upload of the mid-term questions to the Blackboard test
**Date**: 2026-11-18
**Sequence**: #03 for the day

## Summary
I opened the test "CLO835 Exam" in Blackboard Ultra in the browser that the user selected. The test was empty.
After the upload, the test holds 40 questions, and Blackboard shows "Unsupported question types were removed".
All 40 questions match the upload file, so Blackboard removed no question.

## What Changed
- Blackboard: the test "CLO835 Exam" now holds 40 multiple-choice questions, 1 point each, 40 points.
- Local: no file changed.

## Technical Details
- Browser: the device that the user named. Page: the test link that the user gave.
- Before the upload: "Create your assessment", 0 maximum points, hidden from students.
- I selected "Upload questions from file". That item opens the file chooser of the operating system, and the
  file was selected in that chooser on the screen. I did not see the chooser, so I do not know which of the
  two files was selected. The two files hold the same 40 records, so the result is the same.
- I put a small script into the page to find the file input. It found no file input, and it changed nothing
  in Blackboard. I closed the tab after the check, so the script is gone.
- Check: for each question, I compared the stem, the 4 options and the correct answer on the page with the
  file `Week11_Exam/Exam_W11_Midterm40_Blackboard_Ultra.txt` (a hash of the text). 40 of 40 are equal.

## Results
- 40 questions are in the test. 0 questions differ from the file. 0 questions are missing.
- The message "Unsupported question types were removed" shows after the upload, also with the new file
  format. No question is removed, so the message has no effect on this test.

- Second check (on the request of the user): I opened the test again in a new tab. It has 40 questions,
  40 points, and it is hidden from students. Each question has 4 options and 1 correct answer. Its text and
  its correct answer are equal to the upload file and to `Exam_W11_Midterm40_AnswerKey.txt` (40 of 40).

## Issues / Notes
- The test settings show "Post grades automatically when assessment is graded". Standard D12 says to set
  auto post to off for an exam window.
- The due date is Thu Nov 19, 2026 11:59 PM (EST). The test is hidden from students.
- No server started, so no port is used.
