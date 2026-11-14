# Report: Grade Assignment 1, recording review of ajijo1

**Date**: 2026-10-30
**Sequence**: #04 for the day

## Summary
I read the recording of Aneeta Jijo (`ajijo1`), so this grade is now final. The grade
changes from a provisional 100 to a final 98. The student loses 2 marks on line B,
because the ruleset `protect-master` was never active. All other lines are correct.

## What Changed
- Created this report. It replaces the `ajijo1` line in reports #02 and #03.
- Reports #02 and #03 stay as they are.
- Added the method to the memory file `reference-grading-recordings.md`.
- No student file changed.

## Results (out of 100)
- 98 (14.70) Aneeta Jijo (ajijo1) — The GitHub part: missing branch protection on master. The ruleset `protect-master` is disabled.

| Line | Max | Mark | Evidence |
|---|--:|--:|---|
| A Dockerfiles, images reach Docker Hub | 10 | 10 | Build at 2:50, push at 4:22, tags on Docker Hub |
| B GitHub, master protected, no credentials | 5 | 3 | Ruleset disabled, see below |
| C Built with the CLI and published | 10 | 10 | Build at 2:50, push at 4:22 |
| D Pulled from Docker Hub | 5 | 5 | `docker rmi`, then `docker pull` of both images at 4:47 |
| E MySQL on a custom bridge, connection | 15 | 15 | `app-net` at 5:25, no published MySQL port, `mysql -h mysql` query at 6:30 |
| F Three containers on 8081 to 8083 | 20 | 20 | `docker ps` at 7:48, pages at 6:42, 6:52 and 7:03 |
| G Reach by name | 10 | 10 | `ping` from blue to pink and lime at 7:48, 0 % loss |
| H Shared port 8080 explained | 10 | 10 | Report section 4; the recording has no explanation |
| I Docker Compose | 15 | 15 | `compose up -d` and `compose ps` at 9:15, explanation at 10:07 |

The recording is 12:16, so it is within the limit of 15 minutes.

## For you, not the student
- At 1:08 the student says that master is protected.
- At 1:26 the ruleset page shows the enforcement status `Disabled`.
- At 1:27 the student selects `Active` in the list. The page shows `Active` until 1:58.
- GitHub gives `enforcement` as `disabled` today.
- GitHub gives the same created and updated time, 2026-10-15 23:34:38 UTC (19:34 EDT).
  The recording starts 3 hours later, so GitHub shows no save after the creation.
- Screenshot 1 in the report shows `Active` at the same page address. In report #02,
  I gave the 5 marks because of this screenshot.
- I do not know the intent of the student, and I make no statement about it.

**Decision on line B:** 3 of 5. The ruleset has the correct rules (deletion,
force push, pull request), and all 4 changes reached master through a pull request.
The rule did not protect master, so the loss is the same as for `hoaminu`, `tdpatel12`
and `lgmkonneh`.

**Not deducted**
- The pages at 8081 and 8082 show the heading "Employee Database v2" on tag `v1`. The
  student says that the update came first. Part 3 has no rubric line.
- Line H credit comes from the report, the same decision as for `lgmkonneh`.

## Technical Details
- You signed in to Seneca in Chrome. I did not sign in, and I did not download a file.
- I read the Stream transcript on the page, then I moved the player to the time of each
  rubric step and read the screen. I did not look at every frame.
- The player was muted. Each visit can add to the view count of the recording.
- GitHub: read the ruleset detail, the master commits and the pull requests.
- Docker Hub: `webapp` has `v1` and `v2`, and `mysql-db` has `v1`. The `v1` tags are
  dated 22:36 EDT on 10-15, which agrees with the push at 22:37 on the recording.

## Results of the check
- 10 of 13 grades are now final.
- `pshrestha49` and `cokonkwo11` stay provisional.
- `dilewis` has no recording.

## Issues / Notes
- The closing of the browser tab left the other sign-in tab of the group as it was.
- The GitHub time is the only proof that no save occurred, because the recording does
  not show the bottom of the ruleset page.
