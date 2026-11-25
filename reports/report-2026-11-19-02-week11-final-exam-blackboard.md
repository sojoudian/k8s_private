# Report: Questions and Settings of the Blackboard Test "Week 11 - Final Exam 20%"
**Date**: 2026-11-19
**Sequence**: #02 for the day

## Summary
The empty test "Week 11 - Final Exam 20%" (course CLO835023.MERGED.2267) now holds the 40 questions of the Summer
2026 final exam, 2.5 points each, 100 points. Its settings equal the settings of the test "CLO835 Mock Exam",
except the due date. A checksum of each question on the Blackboard page agrees with the source file: 40 of 40.

## What Changed
- Blackboard, test "Week 11 - Final Exam 20%":
  - 40 questions uploaded from a file (26 multiple choice with one correct option, 9 with more than one
    correct option, 5 True/False), in the order of the source file;
  - points: 2.5 for each question (Bulk edit points), 100 maximum points;
  - settings: see the table below;
  - Respondus: LockDown Browser required, with the advanced options of the Mock Exam.
- Blackboard, test "CLO835 Mock Exam": no change. Its settings panel and its LockDown panel were read and
  closed with Cancel. After the work, the LockDown dashboard still shows "Required" for it.
- Local: created `summer_2026_CLO835_exam/Week11_Final_Exam_Blackboard_Ultra.txt` (the upload file) and this
  report.

## Technical Details
- Browser: Claude in Chrome, on the device that the user named.
- Upload file: a script built it from
  `summer_2026_CLO835_exam/CLO835_Summer2026_Final_Exam_MCQ_with_Answers.md`. The script parsed the Markdown file
  and asserted that it equals the verified question data of report #01. Format: tab-delimited records MC, MA
  and TF; ASCII; CRLF line ends; no line end after the last record (the format of the upload on 2026-11-18).
- Upload: "Upload questions from file" opens the file chooser of the operating system. I cannot use that
  chooser. A script in the page tried to catch the file input, but Blackboard did not use a normal file input,
  so the script caught nothing. The user selected the file in the chooser. The first selection gave no
  upload. I reloaded the page (this removed my script), opened the chooser again, and the user selected the
  file again. Blackboard showed "40 questions uploaded successfully to the assessment".
- Points: the upload gave 1 point for each question. "More options for Test Content", then "Bulk edit
  points", "Select all", Points 2.5, Update. Blackboard showed "40 questions were successfully updated".
- Settings: read in the Mock Exam panel, set in the new panel, then saved.

| Setting | Mock Exam | Week 11 - Final Exam 20% |
|---|---|---|
| Due date | Wed Nov 18, 2026, 8:45 PM (EST) | Fri Nov 20, 2026, 11:59 PM (EST), not changed |
| Prohibit late submissions | On | On |
| Prohibit new attempts after due date | On | On |
| Display one question at a time | On | On |
| Prohibit backtracking | On | On |
| Randomize questions | On | On |
| Randomize answers | On | On |
| Randomize pages | Off | Off |
| Class conversations, formative assessment | Off | Off |
| Grade category | Test | Test |
| Attempts allowed | 1 | 1 |
| Grade using | Points (100) | Points (100) |
| Hide student names, delegated grading | Off | Off |
| Post assessment grades automatically | Off | Off |
| Submission view | Hidden from students | Hidden from students |
| Question feedback, question scores, correct answers | Off | Off |
| Access code | None | None |
| Time limit | 75 minutes, automatic submission | 75 minutes, automatic submission |
| SafeAssign | Off | Off |
| Description | Empty | Empty |
| LockDown Browser | Required | Required |
| Require LockDown Browser to view post-exam feedback and results | On | On |
| Lock students into the browser, external web domains, calculator, printing | Off | Off |
| Respondus Monitor | Not required | Not required |

## Results
- Fresh page check: 40 questions, 2.5 points each, 100 points, 0 differences from the source file (checksum of
  the stem, the options and the correct-answer marks of each question).
- The settings panel after a reload shows the values of the table. The test summary shows "Students need to
  use Respondus LockDown Browser to complete this assessment".
- The test stays "Hidden from students".

## Issues / Notes
- The due date was not copied: the Mock Exam date (Wed Nov 18, 2026, 8:45 PM) is in the past, and with
  "Prohibit late submissions" no student could start the test. The new test keeps the Blackboard default,
  Fri Nov 20, 2026, 11:59 PM (EST).
- The visibility was not copied: the Mock Exam is "Visible to students", and the new test stays hidden.
- No server started, so no port is used.
