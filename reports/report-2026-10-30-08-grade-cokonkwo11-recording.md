# Report: Grade Assignment 1, recording review of cokonkwo11

**Date**: 2026-10-30
**Sequence**: #08 for the day

## Summary
I read the screen of the recording of Clement Okonkwo (`cokonkwo11`). The provisional
grade changes from 68 to 88. The recording shows the pull and Docker Compose, so the
student gets those 20 marks. Line H (10 marks) stays open, because the recording has no
captions and I cannot hear it. The grade stays provisional.

## What Changed
- Created this report. It replaces the `cokonkwo11` line in reports #02 and #03.
- Reports #02 and #03 stay as they are.
- No student file changed.

## Results (out of 100)

**Provisional, do not post**
- 88 (13.20) Clement Okonkwo (cokonkwo11) — The GitHub part: missing a protected master branch. The shared port part: missing the explanation of port 8080.

The grade is 98 (14.70), without the shared port text, if the audio has the explanation.

| Line | Max | Mark | Evidence |
|---|--:|--:|---|
| A Dockerfiles, images reach Docker Hub | 10 | 10 | Docker Hub page at 1:42, tags on Docker Hub, report images |
| B GitHub, master protected, no credentials | 5 | 3 | `main` branch only, GitHub gives `protected` false |
| C Built with the CLI and published | 10 | 10 | `docker tag` and `docker push` in the report images |
| D Pulled from Docker Hub | 5 | 5 | `docker pull` of both images at 2:50 |
| E MySQL on a custom bridge, connection | 15 | 15 | Report images: `clo835-net`, containers with `DBHOST=mysql` |
| F Three containers on 8081 to 8083 | 20 | 20 | `docker ps` at 4:40; blue, pink and lime pages at 5:40, 6:15 and 6:28 |
| G Reach by name | 10 | 10 | `docker exec`, then `ping pink` and `ping lime` at 8:40 to 10:00, 0 % loss |
| H Shared port 8080 explained | 10 | open | Not in the report; I cannot hear the recording |
| I Docker Compose | 15 | 15 | `compose up -d` and `compose ps` at 10:00 and 11:20, 4 of 4 up |

The recording is 13:23, so it is within the limit of 15 minutes.

## For you, not the student
- The stack is already up when the recording starts. `docker ps` shows "Up About an hour".
- The running containers use the local images `my_app` and `my_db`, not the Docker Hub
  images. The pull says "Image is up to date", and no `docker rmi` occurs before it.
- From 0:55 to 1:20 the browser shows `sojoudian/CLO835_Fall_2026`, not the repository of
  the student.
- All 21 commits in the repository of the student come from the course account.
- The Dockerfile in the repository has no `iputils-ping`, but ping works on the
  recording. The image on the recording does not match the repository.
- Build and push are not on the frames that I read. Credit comes from the report images.
- The checklist in the Word file on screen has no build, push or MySQL step.

**Generous decisions**
- Line D: 5 of 5 for the pull commands, although the images were already local.
- Line E: 15 of 15 from the report images. I saw no direct MySQL client connection.

## Technical Details
- You signed in to Seneca in Chrome. I did not sign in, and I did not download a file.
- The player gives 1920 x 1080. Stream shows no captions, so it has no transcript.
- I read about 25 frames, 30 s to 40 s apart. I did not look at every frame.
- At 12:00 to 13:00 the student talks to the camera on the 8081 page. The explanation
  can be there, but I cannot confirm it.
- GitHub: read the branches, rulesets, pull requests and commits.
- Docker Hub: `webapp` and `mysql-custom` each have `v1`.

## Issues / Notes
- A transcript needs `CLO835-Assignment1 video.mp4` (Seneca SharePoint, about 34 MB).
  The download needs your clear approval. I read the size from SharePoint.
- After this review, 11 of 13 grades are final. `cokonkwo11` is provisional, and
  `dilewis` has no recording.
