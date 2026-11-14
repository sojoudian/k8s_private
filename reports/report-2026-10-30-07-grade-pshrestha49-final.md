# Report: Grade Assignment 1, final grade of pshrestha49

**Date**: 2026-10-30
**Sequence**: #07 for the day

## Summary
I read the full recording of Pratham Shrestha (`pshrestha49`) with sound. The student
explains the shared port 8080 from 6:13 to 7:28, so line H earns 10 of 10. The grade
changes from a provisional 90 to a final 100. No marks are lost.

## What Changed
- Created this report. It replaces the `pshrestha49` line in reports #02, #03 and #06.
- Reports #02, #03 and #06 stay as they are.
- No student file changed.

## Results (out of 100)
- 100 (15.00) Pratham Shrestha (pshrestha49) — full.

| Line | Max | Mark | Evidence |
|---|--:|--:|---|
| A Dockerfiles, images reach Docker Hub | 10 | 10 | Build at 2:00 and 2:10, push at 2:25 and 2:40 |
| B GitHub, master protected, no credentials | 5 | 5 | GitHub gives `protected` true for master; the rule is on screen |
| C Built with the CLI and published | 10 | 10 | `docker build` and `docker push` of both images |
| D Pulled from Docker Hub | 5 | 5 | `docker pull` of both images at 1:45, "Downloaded newer image" |
| E MySQL on a custom bridge, connection | 15 | 15 | `clo835-net` at 3:40, `docker exec` MySQL query at 4:00 |
| F Three containers on 8081 to 8083 | 20 | 20 | `docker run` at 4:40, `localhost` pages at 5:25, 5:35 and 5:40 |
| G Reach by name | 10 | 10 | `ping` from blue to pink and lime at 6:00, 0 % loss |
| H Shared port 8080 explained | 10 | 10 | Spoken at 6:13: network namespaces, then host port forwarding |
| I Docker Compose | 15 | 15 | Stack started after 7:28, status shown at 8:31, `compose down -v` at 9:05 |

The recording is 9:18, so it is within the limit of 15 minutes.

## Technical Details
- You put the file in `~/Downloads` before I clicked anything, so I did not download it.
  The file is 400 943 345 bytes and has the duration of the player, 558.1 s.
- I copied the file to the session scratchpad. The original stays in `~/Downloads`.
- I ran the same process as for the other recordings: 1 frame every 5 s, screen text
  with macOS Vision, and a Whisper `base.en` transcript.
- The full quality text confirms the commands that I read at 240p in report #06. The
  times in this report replace the times in report #06.

## Issues / Notes
- The transcript gives "NAT means network access traffic". Whisper can change words, so
  I did not deduct for this. The explanation of the mechanism is correct.
- 11 of 13 grades are now final. `cokonkwo11` stays provisional, and `dilewis` has no
  recording.
- `assignment_1_clo_835.mp4` in `~/Downloads` holds a student recording. I did not
  delete it.
