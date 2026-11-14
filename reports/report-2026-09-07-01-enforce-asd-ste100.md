# Report: Enforce the ASD-STE100 Language Rule
**Date**: 2026-09-07
**Sequence**: #01 for the day

## Summary
The user requires all output in ASD-STE100 Simplified Technical English. The rule was
absent from every configuration file. This task adds the rule in five places. Two hooks
put the rule into the model context at each session start and at each user prompt.

## What Changed
- `~/.claude/hooks/asd-ste100.sh` — new. The hook script prints the rule as JSON.
- `~/.claude/settings.json` — modified. Two hook entries were added: `UserPromptSubmit`
  and `SessionStart`. The backup is `settings.json.bak-ste100`.
- `/Users/maziar/Downloads/k8s_week3/.claude/settings.local.json` — modified. The same
  two hook entries were added. The backup is `settings.local.json.bak-ste100`.
- `~/.claude/CLAUDE.md` — modified. A new first section holds the rule. The backup is
  `CLAUDE.md.bak-ste100`.
- `/Users/maziar/Downloads/k8s_week3/CLAUDE.md` — new. The file holds the same rule.
- `~/.claude/projects/-Users-maziar-Downloads-k8s-week3/memory/feedback-write-in-asd-ste100.md`
  — new memory file.
- `.../memory/MEMORY.md` — modified. One index line points to the new memory file.

## Technical Details
The hook script reads the hook input on standard input. It reads the field
`hook_event_name` with `jq`. It then prints one JSON object. The object holds
`hookSpecificOutput.additionalContext`. Claude Code puts that text into the model
context. The field `suppressOutput` is `true`, so the text stays out of the transcript.

The script defaults to `UserPromptSubmit` if the event name is absent. This keeps the
output valid for any caller.

The hook command uses the absolute path `/Users/maziar/.claude/hooks/asd-ste100.sh`.
An absolute path removes all doubt about shell variable expansion.

The `jq` merge preserves all existing keys in both settings files. The merge also
removes any earlier copy of this same hook. This prevents duplicate entries.

## Results
- The script exits 0 for three test inputs: `UserPromptSubmit`, `SessionStart`, and `{}`.
- The event name in the output matches the event name in the input.
- `jq -e` confirms the hook path in both settings files.
- Both settings files are valid JSON.
- The hooks fire in a new session. This session started before the change, so the hooks
  are not yet active here.

## Issues / Notes
- Open the `/hooks` menu once, or restart the session. This makes Claude Code reload the
  configuration. The hooks are correct on disk.
- The script needs `jq`. The binary is at `/opt/homebrew/bin/jq`.
- Five backup files carry the suffix `.bak-ste100`. Delete them when you are satisfied.
