# Report: Disable Claude Attribution in Git Commits
**Date**: 2026-11-05
**Sequence**: #02 for the day

## Summary
The user pasted three steps from a session on the other MacBook. This report records what was done on this MacBook.
Step 1 is done. Step 2 was not done, because the "Git Authorship" section does not exist on this MacBook. The auto mode classifier stopped Step 3. The user must run Step 3.

## What Changed
- `/Users/maziar/.claude/settings.json`: added `"attribution": { "commit": "", "pr": "" }` and `"includeCoAuthoredBy": false` after `cleanupPeriodDays`. All other keys are the same.

## Technical Details
Search before the change:
- `~/.claude/CLAUDE.md`, the project `CLAUDE.md`, `~/.claude/PREFERENCES.md`, the memory files and `settings.json` had no rule about the git author.
- No system file `/Library/Application Support/ClaudeCode/CLAUDE.md` exists.
- No file in `~/.claude` has a "Git Authorship" section.
- `git config --global core.hooksPath` was not set. `~/.git-hooks` did not exist.
- No repository under `~/Documents`, `~/app` or `~/Downloads` (depth 5) has an active hook in `.git/hooks`. Thus a global `core.hooksPath` disables no hook.
- Course repo commit `ff69e05` (2026-10-31, "update w09") has the line `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

Test of the `sed` line of the hook, with `/bin/sh` and `/usr/bin/sed` (BSD):
- The test removed `Co-Authored-By: Claude ...`, the lower-case `co-authored-by: claude ...`, `Claude-Session: ...` and the `🤖 Generated with [Claude Code]` line.
- The test kept `Co-Authored-By: Real Person <a@b.c>`. Exit code 0.

## Results
- Step 1: done. `jq` reads the file and shows the two new keys.
- Step 2: not done. The section text is on the other MacBook only.
- Step 3: denied by the auto mode classifier ("Unauthorized Persistence"). Not done.
- The new settings apply to the next Claude Code session.

## Update: Step 2 done
- The user pasted the "Git Authorship" section from the other MacBook.
- `/Users/maziar/.claude/CLAUDE.md`: the section is now at the end of the file, word for word.
- The global git identity on this MacBook is `BartyCrouch <sojodyan@gmail.com>`. The section names `maziar <sojodyan@gmail.com>`. This report does not change the identity, because the section forbids that.

## Update: Step 3 done by the user, checked
- `/Users/maziar/.git-hooks/commit-msg` exists (135 bytes, mode `-rwxr-xr-x`), with the same 2 lines as the pasted step.
- `git config --global core.hooksPath` gives `/Users/maziar/.git-hooks`.
- A direct run on a sample message removed the 3 Claude lines and kept `Co-Authored-By: Real Person`. Exit code 0.
- In a new test repository, `git rev-parse --git-path hooks` gives `/Users/maziar/.git-hooks`.
- A test commit with a `Co-Authored-By: Claude` line got the stored message `commit test` only. The test repository was then deleted.

## Issues / Notes
- The user must run Step 3 in this session with the `!` prefix, or in a terminal.
- `core.hooksPath` applies to every repository. A repository with its own hooks in `.git/hooks` then does not run them.
- The settings do not change commit `ff69e05`. A change to that commit needs a history rewrite and a force push.
