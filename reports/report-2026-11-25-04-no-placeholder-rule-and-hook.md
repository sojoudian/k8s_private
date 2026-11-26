# Report: Rule and Stop Hook for Drafts with No Placeholder
**Date**: 2026-11-25
**Sequence**: #04 for the day

## Summary
The user asked for two changes after a reply to a student had the placeholder `[date]` for a reference that
did not exist. Claude added a written rule to the global `CLAUDE.md` and a Stop hook that finds a placeholder
in the text of each answer.

## What Changed
- `~/.claude/CLAUDE.md`: a new section "Complete drafts: no placeholder (MANDATORY)", after the section
  "Answer length".
- `~/.claude/hooks/no-placeholder.py` (new, executable): the hook script.
- `~/.claude/settings.json`: a new `hooks.Stop` entry that runs
  `/opt/homebrew/bin/python3 -I /Users/maziar/.claude/hooks/no-placeholder.py` (timeout 10 s). The
  `UserPromptSubmit` and `SessionStart` hooks did not change.

## Technical Details
- The rule: check each promise and fact of a draft against the course files; make a missing item first; ask
  before the draft when only the user can decide; tell the user at the top of the answer what they must post
  or send; check "Can the user use this now, with no change?".
- The hook reads the session transcript (`transcript_path`) and takes all the assistant text after the last
  prompt of the user. It also reads `last_assistant_message` when the input has it.
- Placeholders found: a square-bracket word such as date, deadline, time, name, link, url, path, file,
  number, email, title, location, room, course, section or id; `[insert ...]`, `[add ...]`, `[fill in ...]`,
  `[enter ...]`, `[your ...]`; the words TBD, TODO and FIXME; "lorem ipsum".
- Not found, on purpose: text in inline backticks, Markdown links such as `[name](url)`, and angle-bracket
  forms such as `<your-key>.pem` and `mysql-<studentID>`, which the lab files use on purpose.
- First find in a turn: the hook gives `{"decision": "block", "reason": ...}`, so Claude continues and must
  correct the answer. A find after that (`stop_hook_active` true): the hook shows a warning to the user and
  lets the stop go, so it cannot start a loop.

## Results
- Pipe tests with 8 sample transcripts, all as expected: `[date]` blocks; a clean answer passes; a second
  try gives a warning only; `[date]` in backticks passes; Markdown links pass; the lab angle-bracket forms,
  `[1m]`, `[x]` and `[ref]` pass; "TBD" and "[Insert the Zoom link here]" block; a placeholder in an older
  turn is not checked.
- `jq -e` on `~/.claude/settings.json`: the file is valid, and the Stop command is in place.
- An empty input gives exit 0 and no output.

## Issues / Notes
- A Stop hook runs after the answer is on the screen. It cannot hide the text. It makes Claude write a
  corrected answer below it at once.
- A new hook can need `/hooks` (open it one time) or a restart before it runs in this session.
- No server started, so no port is used.
