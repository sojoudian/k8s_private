# Report: Auto-compact window set to 800K tokens
**Date**: 2026-10-27
**Sequence**: #06 for the day

## Summary
The user asked for auto-compact at 800K tokens, not at the 1M window. I added the
top-level key `"autoCompactWindow": 800000` to `~/.claude/settings.json`. The file
is valid JSON, and all other keys stay the same.

## What Changed
- `~/.claude/settings.json`: one new line after `"effortLevel"`:
  `"autoCompactWindow": 800000,`

## Technical Details
- The settings schema defines `autoCompactWindow` as an integer, in tokens, from
  100000 to 1000000. The top-level key applies to all models.
- A `modelSettings.<model>.autoCompactWindow` value replaces the top-level key for
  that model. `modelSettings.claude-opus-5-5` holds only `effortLevel`, so the new
  key applies to Opus 5.5 too.
- `/autocompact` saves a per-model value. If you use it later, that value wins for
  that model.
- The `CLAUDE_CODE_AUTO_COMPACT_WINDOW` environment variable overrides this key. It
  is not set in the `env` block.

## Results
- `json.load` passes. `autoCompactWindow = 800000`. The file holds 18 top-level keys.

## Issues / Notes
- The documentation does not say whether a running session reloads this key. Start a
  new session to be sure, or type `/autocompact 800k` to apply it to this session now.
- The status line `used_percentage` measures against the full 1M window, so
  compaction starts at about 80 % on that scale.
