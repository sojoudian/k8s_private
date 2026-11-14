# Report: The Week 05 and Week 06 preferences added to PREFERENCES.md
**Date**: 2026-10-27
**Sequence**: #08 for the day

## Summary
The user said "yes add them all". I added every preference of report #07 that
`~/.claude/PREFERENCES.md` did not hold, and I made the 3 partial ones explicit.
That is 37 new lines: 2 in section 6, 4 in section 12, and 3 new sections (13, 14
and 15). No old line changed. I also corrected a count in report #07: 33
preferences were missing, not 22.

## What Changed
- `~/.claude/PREFERENCES.md`: 135 lines to 202 lines, 12 sections to 15.
  - Header: one line that names the source of the new lines.
  - Section 6 (Course content): only `maziar` and `sojoudian`; check that a tag
    exists.
  - Section 12 (Work style): the Week 05 standard, audit first, fix all, no
    "mostly".
  - Section 13 (Decks: build, layout and images): 11 lines.
  - Section 14 (Decks: content): 10 lines.
  - Section 15 (Labs): 10 lines.
- `reports/report-2026-10-27-07-week06-preferences-deep-dive.md`: the counts
  changed from "22 missing, 5 partial" to "33 missing, 3 partial", with a note.
- A backup of the old file is in the session scratchpad
  (`PREFERENCES.md.before`).

## Technical Details
- The count error: report #07 said 22 of 44 were missing. A recount of its own
  tables gives 33 missing, 3 partial (A2, D6, D7) and 8 present. I told the user 22
  in the chat, so the chat number was wrong too.
- The 37 lines are the 33 missing items, the 3 partial items, and E9 in full
  ("run every command"), because section 10 held only "destroy".
- I did not resolve the 6 conflicts. One of them now sits inside the file: section
  15 names kubeadm, and section 10 says "Use kind on EC2". Section 15 marks it as an
  open conflict for the user.
- I did not change `PROMPT.md`, `CLAUDE.md` or the hooks.

## Results
- `diff` against the backup: 37 new `- ` lines, 0 removed lines.
- 15 section headings, in order 1 to 15.

## Issues / Notes
- Open conflicts for the user: `PROMPT.md` R1 (verbatim) against the repairs;
  `E74C3C` against `FF5F56`; the reference deck (Week 04 v02_02 or Week 01 v5);
  kind against kubeadm; two footer conventions; Week 8 "BREAK" and Week 9 "EKS"
  against the 2026-07-15 schedule.
