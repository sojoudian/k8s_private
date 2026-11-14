# Report: Grade Assignment 1 (15%), grades and feedback for 13 submissions

**Date**: 2026-10-30
**Sequence**: #03 for the day

## Summary
This report gives the grade and the student feedback for all 13 submissions. It uses
the format of the Lab 05 and Lab 08 reports: where the student lost marks, and nothing
else. Report #02 gave feedback text for 10 students only, so this report completes it.
The grades do not change. I checked each lost mark again before I wrote the text.

## What Changed
- Created this report. Report #02 stays as it is.
- Added one rule to the memory file `feedback-student-facing-grading.md`.
- No student file changed.

## Results (out of 100, sorted)

**Final**
- 100 (15.00) Aaron King (apking1) — full.
- 100 (15.00) Daniel Araujo (daraujo2) — full.
- 100 (15.00) Mitesh Chand Thakur (mcthakur) — full.
- 100 (15.00) Muskan (mmuskan24) — full.
- 100 (15.00) Xinmeng Yuan (xyuan29) — full.
- 98 (14.70) Halimat Aminu (hoaminu) — The GitHub part: missing branch protection on master.
- 98 (14.70) Tirth Patel (tdpatel12) — The GitHub part: missing branch protection on master.
- 95 (14.25) Yiming Pan (ypan69) — The Docker pull part: missing the docker pull of both images.
- 93 (13.95) Lassana Konneh (lgmkonneh) — The GitHub part: missing branch protection on master. The container name part: missing the test of containers that reach each other by name.

**Provisional, do not post**
- 100 (15.00) Aneeta Jijo (ajijo1) — full.
- 75 (11.25) Pratham Shrestha (pshrestha49) — The Docker pull part: missing the docker pull of both images. The container name part: missing the test of containers that reach each other by name. The shared port part: missing the explanation of port 8080.
- 68 (10.20) Clement Okonkwo (cokonkwo11) — The GitHub part: missing a protected master branch. The Docker pull part: missing the docker pull of both images. The shared port part: missing the explanation of port 8080. The Docker Compose part: missing the demonstration.

**No recording**
- 40 (6.00) Daneilia Lewis (dilewis) — The recording: missing. The Docker pull, MySQL connection, shared port and Docker Compose parts: missing the demonstration. The three containers and container name parts: described in the report, missing the demonstration.

## Technical Details
I checked each lost mark against the source on 2026-10-30.

- `hoaminu`: GitHub gives `protected` false for master and no ruleset. At 9:52 the
  recording says that master is protected, but no protection page appears on the screen.
- `tdpatel12`: GitHub gives `protected` false for master and no ruleset. No protection
  page appears in the recording.
- `lgmkonneh`: GitHub gives `protected` false for master and no ruleset. The word
  `ping` is not in the recording text, the report text or the report images.
- `ypan69`: The recording and the report have no `docker pull` and no pull output.
- `pshrestha49`: The report has no image pull, no ping between containers and no
  port 8080. "Pull" occurs only in "pull request". "Ping" occurs only in `mysqladmin ping`.
- `cokonkwo11`: The repository has `main` only, and GitHub gives `protected` false. The
  report and its images have no `docker pull`, no port explanation and no compose command.
- `dilewis`: The report describes the three containers and the ping. It has no MySQL
  connection, no port 8080 and no compose demonstration.

## Results of the check
All lost marks stand. One line changed from report #02. For `cokonkwo11`, the GitHub
text now says "a protected master branch", because the repository has no master branch.
The Docker pull text now has one part name for all students.

## Issues / Notes
- The 3 provisional lines come from the report and the repository only. The recordings
  can show the missing items, so each line can change.
- `ajijo1`, `pshrestha49` and `cokonkwo11` recordings are still not read.
- The GitHub state is the state on 2026-10-30, not the state on the due date.
- The notes for the professor stay in report #02, in the part "For you, not the student".
