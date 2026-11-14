# Report: Grade Assignment 1, recording review of pshrestha49

**Date**: 2026-10-30
**Sequence**: #06 for the day

## Summary
I read the recording of Pratham Shrestha (`pshrestha49`) on the screen, without sound.
The provisional grade changes from 75 to 90. The recording shows the pull and the name
test, so the student gets those 15 marks. Line H (10 marks) stays open, because an
explanation is spoken and I cannot hear the recording. The grade stays provisional.

## What Changed
- Created this report. It replaces the `pshrestha49` line in reports #02 and #03.
- Reports #02 and #03 stay as they are.
- Corrected the OneDrive line in the memory file `reference-grading-recordings.md`.
- No student file changed.

## Results (out of 100)

**Provisional, do not post**
- 90 (13.50) Pratham Shrestha (pshrestha49) — The shared port part: missing the explanation of port 8080.

The grade is 100 (15.00) with the text "full." if the audio has the explanation.

| Line | Max | Mark | Evidence |
|---|--:|--:|---|
| A Dockerfiles, images reach Docker Hub | 10 | 10 | Build at 2:02, push at 2:41, tags on Docker Hub |
| B GitHub, master protected, no credentials | 5 | 5 | GitHub gives `protected` true for master; the rule page is on screen |
| C Built with the CLI and published | 10 | 10 | Build at 2:02, push of both images at 2:41 and 3:26 |
| D Pulled from Docker Hub | 5 | 5 | `docker pull` of both images at 1:49 |
| E MySQL on a custom bridge, connection | 15 | 15 | `clo835-net` at 3:26, MySQL run at 3:46, query output at 4:42 |
| F Three containers on 8081 to 8083 | 20 | 20 | `docker ps` at 5:01; blue, pink and lime pages at 5:32, 5:36 and 5:46 |
| G Reach by name | 10 | 10 | `docker exec` ping at 6:13, 3 packets, 0 % loss |
| H Shared port 8080 explained | 10 | open | Not in the report; I cannot hear the recording |
| I Docker Compose | 15 | 15 | `compose up -d` at 8:00, `compose ps` and `compose down` at 9:06 |

The recording is 9:18, so it is within the limit of 15 minutes.

## Technical Details
- I used the OneDrive player in Chrome and did not click the Download button.
- The player stays at 426 x 240, also in the large view. The terminal text is blurred.
- I read the commands from zoomed frames. A word can be wrong, but the output of each
  step (pull status, table of rows, ping statistics, compose status) is clear.
- I sampled about 20 frames. I did not look at every frame.
- Docker Hub: `clo835-webapp` and `clo835-mysql` each have `latest` and `v1`.
- GitHub: master has a classic protection rule, and 1 pull request is merged.

## Issues / Notes
- The audio stream is present, because the player decodes it. I have no means to hear it.
- A transcript needs the file `assignment_1_clo_835.mp4` (OneDrive, about 400 MB). The
  download needs your clear approval.
- The browser extension lost its connection one time, and the same step worked again.
- `cokonkwo11` stays provisional. `dilewis` has no recording.
