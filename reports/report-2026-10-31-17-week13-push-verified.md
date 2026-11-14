# Report: Week 13 Push Verified
**Date**: 2026-10-31
**Sequence**: #17 for the day

## Summary
The user pushed the Week 13 lab to GitHub. A read-only check compares the pushed files with the clone and with the files of the live test. All compared files are the same, byte for byte.

## What Changed
- No course file changes.
- Memory: `project-week13-deck.md`, `project-short-labs-2026-10-27.md`, `project-clo835-fall2026-repo.md`, `MEMORY.md` now show that Week 13 is on GitHub.

## Technical Details
- `git ls-remote` and the local `HEAD` both give `665768b`.
- The compare uses the raw GitHub URL at this commit, with `cmp`.
- The push changes 3 files: `cleanup_lab13.sh`, `localMachine.sh` and `master-init.sh.tftpl`.

## Results
- All 8 files of `Week13` on GitHub are the same as the clone.
- 7 files are the same as the copy that the live test ran. The eighth file, `.gitignore`, has no effect on the lab.
- GitHub `localMachine.sh` is the same as `week13/localMachine_v3.sh`.
- `master-init.sh.tftpl` on GitHub has 3 lines with `maziar/flannel`, and 0 lines with `flannel-io` or `ghcr.io`.
- `git status` shows no changed file.
- `gate_week13.py` with the live logs: GATE 1, 132 of 132.

## Issues / Notes
- The commit message says "update week 12", but the commit changes `Week13`. This has no effect on students.
- I did not run the lab again from a fresh `git pull`. The live test used files that are the same as the files on GitHub.
- The decks and the Blackboard text are not in the repository. You upload them yourself.
- I did not view the decks in Keynote.

## Second Check
The user asked for a second check. This check does not use the results of the first check.

- Local HEAD and GitHub `master` are the same commit: `665768b`.
- `git status` shows no change, and the branch is the same as `origin/master`.
- The check hashes all 8 `Week13` files from `raw.githubusercontent.com` at commit `665768b`.
- All 8 files return HTTP 200, and all 8 are the same as the clone.
- All 8 files are the same as the live-tested copy. This now includes `.gitignore`.
- `localMachine.sh` is the same as `week13/localMachine_v3.sh`.
- `master-init.sh.tftpl` has 3 `maziar/flannel` lines and 0 `flannel-io` or `ghcr.io` lines.
- A search of `Week13` finds 0 AWS key patterns, 0 `/Users/` paths, 0 private key paths and 0 email addresses.
- `gh` has no login on this computer, so the check uses the public raw URLs.
- `gate_week13.py` with the live logs gives GATE 1, 132 of 132. The output is the same as the earlier gate output.
- The first gate run in this check stopped with an error, because the check gave the wrong arguments. The gate needs file stems and the `INSTRUMENT` environment value. The error is in the check, not in the files.
