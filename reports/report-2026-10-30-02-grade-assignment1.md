# Report: Grade Assignment 1 (15%), 13 submissions
**Date**: 2026-10-30
**Sequence**: #02 for the day

## Summary
I graded the 13 submissions in `a1/` against the 9 rubric lines, with generous
marking. Nine grades are final. Three grades are provisional, because I could not
read the recording. One submission has no recording. The final grades go from 93
to 100.

## What Changed
- Created this report.
- Added the memory file `reference-grading-recordings.md` and one line in `MEMORY.md`.
- No student file changed. Clones, frames and transcripts are in the session
  scratchpad only.

## Grades

| Line | Requirement | Max |
|---|---|--:|
| A | Dockerfiles build both images, images reach Docker Hub | 10 |
| B | GitHub repository, master protected, no credentials | 5 |
| C | Both images built with the CLI and published | 10 |
| D | Images pulled from Docker Hub | 5 |
| E | MySQL on a custom bridge network, connection | 15 |
| F | Three containers on 8081 to 8083, answer from the machine | 20 |
| G | Containers reach each other by name | 10 |
| H | Shared port 8080 explained | 10 |
| I | Docker Compose brings the stack up | 15 |

| Student | Login | A | B | C | D | E | F | G | H | I | /100 | /15 | State |
|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|---|
| Aaron King | apking1 | 10 | 5 | 10 | 5 | 15 | 20 | 10 | 10 | 15 | **100** | 15.00 | final |
| Daniel Araujo | daraujo2 | 10 | 5 | 10 | 5 | 15 | 20 | 10 | 10 | 15 | **100** | 15.00 | final |
| Mitesh Chand Thakur | mcthakur | 10 | 5 | 10 | 5 | 15 | 20 | 10 | 10 | 15 | **100** | 15.00 | final |
| Muskan | mmuskan24 | 10 | 5 | 10 | 5 | 15 | 20 | 10 | 10 | 15 | **100** | 15.00 | final |
| Xinmeng Yuan | xyuan29 | 10 | 5 | 10 | 5 | 15 | 20 | 10 | 10 | 15 | **100** | 15.00 | final |
| Halimat Aminu | hoaminu | 10 | 3 | 10 | 5 | 15 | 20 | 10 | 10 | 15 | **98** | 14.70 | final |
| Tirth Patel | tdpatel12 | 10 | 3 | 10 | 5 | 15 | 20 | 10 | 10 | 15 | **98** | 14.70 | final |
| Yiming Pan | ypan69 | 10 | 5 | 10 | 0 | 15 | 20 | 10 | 10 | 15 | **95** | 14.25 | final |
| Lassana Konneh | lgmkonneh | 10 | 3 | 10 | 5 | 15 | 20 | 5 | 10 | 15 | **93** | 13.95 | final |
| Aneeta Jijo | ajijo1 | 10 | 5 | 10 | 5 | 15 | 20 | 10 | 10 | 15 | **100** | 15.00 | provisional |
| Pratham Shrestha | pshrestha49 | 10 | 5 | 10 | 0 | 15 | 20 | 0 | 0 | 15 | **75** | 11.25 | provisional |
| Clement Okonkwo | cokonkwo11 | 10 | 3 | 10 | 0 | 15 | 20 | 10 | 0 | 0 | **68** | 10.20 | provisional |
| Daneilia Lewis | dilewis | 10 | 5 | 10 | 0 | 0 | 10 | 5 | 0 | 0 | **40** | 6.00 | no recording |

## Where the student lost marks (student-facing text)

| Student | Text |
|---|---|
| apking1 | — |
| daraujo2 | — |
| mcthakur | — |
| mmuskan24 | — |
| xyuan29 | — |
| hoaminu | The GitHub part: missing branch protection on master. |
| tdpatel12 | The GitHub part: missing branch protection on master. |
| ypan69 | The Docker Hub part: missing the docker pull of both images. |
| lgmkonneh | The GitHub part: missing branch protection on master. The container name part: missing the test of containers that reach each other by name. |
| dilewis | The recording: missing. The Docker pull, MySQL connection, shared port and Docker Compose parts: missing the demonstration. The three containers and container name parts: described in the report, missing the demonstration. |

Do not post the provisional grades. For these three students, the lost marks are
evidence that I could not see, so the text can change after the recording review:
- `ajijo1`: no loss so far.
- `pshrestha49`: pull, name test and shared port (20 marks) are not in the report.
- `cokonkwo11`: the master protection loss (2 marks) stands. Pull, shared port and
  Docker Compose (30 marks) are not in the report.

## For you, not the student

**Recordings**

| State | Students |
|---|---|
| Read (9) | apking1, daraujo2, hoaminu, lgmkonneh, mcthakur (2 clips, 9:47 total), mmuskan24, tdpatel12, xyuan29, ypan69 |
| Seneca sign-in needed (2) | ajijo1, cokonkwo11. The links stop at the Microsoft sign-in page. I did not sign in. |
| Opens, but not readable (1) | pshrestha49, `assignment_1_clo_835.mp4`, 9:18, OneDrive. The player gave me 426 px wide video and no audio. |
| None (1) | dilewis |

All 9 recordings are 15 minutes or less. The longest is `tdpatel12`, at 14:17.

**Each submission**
- `dilewis`: at 23:54 on 10-15, the Blackboard note says the recording failed to
  save, and the screenshot shows a Microsoft Stream error. The note says a redo might
  miss the deadline. The zip holds one attempt only. Docker Hub received both images
  at 20:16 EDT on 10-15. The decision to accept a late recording is yours.
- `ajijo1`: GitHub shows the ruleset `protect-master` as `disabled` today. The report
  screenshot shows it Active, so I gave the 5 marks.
- `hoaminu` and `tdpatel12`: each report says master is protected. GitHub shows no
  ruleset and no protection today. Each repository does show merged pull requests.
- `lgmkonneh`: the recording says the computer is too slow to run commands live, so
  it walks through earlier terminal output. I gave credit for that output. The
  Dockerfile on GitHub has no `iputils-ping`, and no ping appears in the recording or
  the report. The repository has one commit by the student, a README edit.
- `cokonkwo11`: the repository has a `main` branch only. All 21 commits come from the
  course account, so the student added no commit. The Dockerfile has no
  `iputils-ping`, but the report screenshots show ping working.
- `ypan69`: I found no `docker pull` in the recording, the report or the README. The
  report has 91 words, which I accepted.

**Generous decisions**
- `lgmkonneh` line G: 5 of 10, because `DBHOST=mysql-db` shows a name lookup.
- `lgmkonneh` line H: 10 of 10 from the report, because the recording has no explanation.
- `ypan69` line E: 15 of 15, because data that one web container wrote appears in
  another. The recording has no direct MySQL client connection.
- `dilewis` lines F and G: half marks from the report text.
- `ajijo1` lines D and E: credit from the report text, until the recording review.
- `pshrestha49` lines E, F and I: credit from the report text and the repository.
- `cokonkwo11` line E: credit from the report text and the screenshots.

**Rules that I did not apply**
- Part 3 (update and redeploy) has no rubric line, so I deducted nothing. No `v2`
  tag on Docker Hub: `cokonkwo11`, `dilewis`, `lgmkonneh`, `pshrestha49`, `xyuan29`.
- The handout says the due date is the week of September 25. All attempts are dated
  10-04 to 10-15, and the last commit of any student is 10-15 23:30 EDT. I took 10-15
  as the due date. I applied no late penalty and no commit date penalty.

**Integrity check**
- Report text overlap is low. The highest overlap of 6-word runs is 3.3 %
  (`hoaminu`, `tdpatel12`). I do not see a sign of copying.
- No repository holds a token or a password file. The `aws_secret_access_key=...`
  match in 3 repositories is the placeholder from the course repository.

## Technical Details
- GitHub: cloned all 13 repositories. I read each Dockerfile and compose file, and I
  searched the full history for tokens. The REST API gave the `protected` flag of
  each branch and the rulesets.
- Docker Hub: read the tags, dates and sizes of all 26 repositories.
- Recordings: 1 frame every 5 s, macOS Vision text extraction on each frame, and a
  Whisper `base.en` transcript. A scan gave the first time of each rubric command.
- I did not look at every frame with my eyes. I used the extracted text and the
  transcript, and I read one contact sheet (`lgmkonneh`).
- Whisper changes names and terms, so I took no fact from a name in a transcript.
- Report images: text extraction on all 9 reports that hold images.

## Results
- 9 final grades: 93 to 100, 5 of them 100.
- 3 provisional grades: 68, 75 and 100.
- 1 submission with no recording: 40.
- No server started, so no port is used.

## Issues / Notes
- GitHub protection is the state on 2026-10-30, not the state on the due date. Except
  for `ajijo1`, I have no screenshot of an earlier state.
- I opened the two Seneca links in a Chrome tab, reached the sign-in page and closed
  the tab. I entered nothing.
- I did not use the Download button of the OneDrive player, because a download needs
  your approval.
- The scratchpad holds student recordings with faces and voices. The operating system
  removes that folder. Nothing went to a public location.
