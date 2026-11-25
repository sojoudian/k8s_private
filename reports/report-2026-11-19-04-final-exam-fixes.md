# Report: Fixes of 6 Questions in the Week 11 Final Exam (Blackboard and Local File)
**Date**: 2026-11-19
**Sequence**: #04 for the day

## Summary
I fixed the 6 questions of report #03 (Q1, Q4, Q6, Q11, Q17, Q28) in the Blackboard test "Week 11 - Final Exam
20%" and in the local upload file. The difficulty and the key letters did not change. A fresh-page check shows
that the 40 questions in Blackboard are equal to the fixed local file (40 of 40).

## What Changed
- Local: `summer_2026_CLO835_exam/Week11_Final_Exam_Blackboard_Ultra.txt`, edited in place (7 text
  replacements in 6 records). No copy and no other version of the file exists.
- Blackboard: the same 6 questions, edited in the question editor of the test and saved one at a time.
- Not changed: `CLO835_Summer2026_Final_Exam_MCQ_with_Answers.md` (the record of the exam as the Summer 2026
  students got it).

## Technical Details

| Q | Field | Old text | New text |
|--:|---|---|---|
| 1 | Option E (correct) | docker start resumes a stopped container with its filesystem intact. | docker start starts a stopped container again with its filesystem intact. |
| 4 | Stem, sentence 1 | ...launches the server with --port=18080, so the app listens on 18080 inside the container. | ...launches the server with --host=0.0.0.0 --port=18080, so the app listens on 18080 on all interfaces inside the container. |
| 6 | Option A (correct) | A prints goodbye and B prints hello goodbye | A fails to start, because the image has no program goodbye, and B prints hello goodbye |
| 6 | Option B | A prints hello goodbye and B prints goodbye | A prints hello goodbye, and B fails to start, because the image has no program goodbye |
| 11 | Stem | ...with its own MAC address and an IP handed out by the LAN's DHCP server, so... | ...with its own MAC address and its own IP address on the LAN subnet, so... |
| 11 | Option D (correct) | ...its own MAC on the physical network and can pull a real LAN IP | ...its own MAC on the physical network and its own IP address on the LAN subnet |
| 17 | Statement (key True) | In this course's deployment prerequisites, kubectl and the cluster may differ in MAJOR version, but they should run the same MINOR version. | According to the Kubernetes version skew policy, kubectl and the cluster must run the same MAJOR version, but kubectl may differ from the API server by one MINOR version, older or newer. |
| 28 | Option D (correct) | A ClusterIP service is also created automatically, and the externally... | The Service also gets a cluster IP, and the externally... |

- Difficulty: each question tests the same concept with the same number of options. Q6 keeps its stem and its
  distractors C and D; the new option B is the mirror of the key (the classic CMD/ENTRYPOINT mix-up). Q17 keeps
  the MAJOR/MINOR contrast and its key True.
- Local file checks: 40 records (26 MC, 9 MA, 5 TF), ASCII, CRLF, no line end after the last record. The 34
  unchanged records keep their checksums.
- Blackboard edits: for each field I put the cursor in the editor, checked the focus with a script, selected
  the text with Cmd+A, typed the new text, and saved. One first attempt (Q6 option B) lost the focus, and the
  text went to the page, not to an editor; the retry with the focus check worked. The final check shows no
  change outside the 6 questions.
- Final check (fresh page): a SHA-256 checksum of each question (stem, options, correct-answer marks) against
  the fixed local file: 40 of 40 equal.

## Results
- Blackboard: 40 questions, 2.5 points each, 100 points; 0 differences from the fixed file.
- The test stays "Hidden from students". The settings did not change: due Sun Nov 22, 2026, 11:59 PM (EST)
  (a date that the user set after report #02), late submissions prohibited, 75 minutes, 1 attempt, LockDown
  Browser required, grades posted by hand.

- Double check (on request, later the same day): I computed the checksums again from the local file on disk
  (22843 bytes, 40 records; the 6 fixed texts are present) and compared them with a fresh load of the test
  page: 40 of 40 equal, 2.5 points each, 100 points. The correct options of the 6 fixed questions: Q1 A, B, E,
  F; Q4 B; Q6 A; Q11 D; Q17 True; Q28 D. The settings did not change. The test now shows "Visible to
  students"; I did not change the visibility.

## Issues / Notes
- In the editor of Q4 (and Q6, Q11, Q28), the switch "Option Feedback" shows on, with empty feedback that is
  hidden from students. I did not change this switch; the upload set it.
- The announcement text of this session names Fri Nov 20 as the due date. The test now shows Sun Nov 22, 2026,
  11:59 PM (EST), and the start time for the full 75 minutes is 10:44 PM on that day.
- No server started, so no port is used.
