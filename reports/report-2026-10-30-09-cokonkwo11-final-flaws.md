# Report: Grade Assignment 1, final grade and flaws of cokonkwo11

**Date**: 2026-10-30
**Sequence**: #09 for the day

## Summary
You set the grade of Clement Okonkwo (`cokonkwo11`) at 88 and declined the download. The
grade is now final. This report lists all the flaws that I found. It replaces the
`cokonkwo11` line in report #08. With this grade, 12 of 13 grades are final, and
`dilewis` has no recording.

## What Changed
- Created this report. Report #08 stays as it is.
- No student file changed. I did not download the recording.

## Results (out of 100)
- 88 (13.20) Clement Okonkwo (cokonkwo11) — The GitHub part: missing a protected master branch. The shared port part: missing the explanation of port 8080.

## All flaws

**Marks lost**
1. The GitHub part: missing a protected master branch. The repository has `main` only, with no protection (2 marks).
2. The shared port part: missing the explanation of port 8080 (10 marks).

**No marks lost**
3. The GitHub part: missing commits by the student. All 21 commits come from the course account.
4. The Dockerfile part: missing `iputils-ping` in the repository, so the working ping image does not match the repository.
5. The Docker pull part: missing `docker rmi` before the pull. The pull says "Image is up to date".
6. The containers part: the running containers use the local images `my_app` and `my_db`, not the Docker Hub images.
7. The recording: the stack is already up at the start ("Up About an hour"), so the recording does not show the containers start.
8. The recording: the ping output shows the Compose network `assignment-1_default`, not the custom bridge `clo835-net`.
9. The recording: missing the build and the push. They are in the report images only.
10. The recording: from 0:55 to 1:20 the browser shows the course repository, not the repository of the student.
11. The MySQL part: missing a direct MySQL client connection.
12. The update part: missing a `v2` tag on Docker Hub.
13. The report: the recording entry is a local path (`C:\Users\onyek\...`), not a link. The submission field has the correct link.

## Technical Details
- Items 1, 3, 4, 12 and 13 come from GitHub, Docker Hub and the report text.
- Items 5 to 8 and 10 come from frames that I read on the recording.
- Items 9 and 11 come from about 25 sampled frames, so a short step can be missing from
  my sample.

## Issues / Notes
- Item 2 is confirmed for the report only. I did not hear the audio.
- Rule on feedback: items 3 to 13 cost no marks, so send them to the student only if you
  want that.
