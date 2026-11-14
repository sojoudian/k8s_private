# Report: How to make all 40 Ultra questions worth 2.5 (=100) — points mechanism
**Date**: 2026-07-13
**Sequence**: #06 for the day

## Summary
Answered the instructor's concern that a prior upload gave every question only 1 point. Verified via official Anthology docs + university Ultra guides that Blackboard Ultra's file-upload flow has NO points field and defaults uploaded questions to 1 point each; the tab-delimited format cannot carry points. The fix is Ultra's Bulk Edit Points tool (Select All -> 2.5 -> Update -> total auto = 100). Corrected my earlier (Original-view) advice that told the user to set points in the upload dialog.

## What Changed
- No exam files changed (the .txt is correct as-is; points are a post-upload UI action).
- Scratch only: `ultra_points.js` (4-agent research workflow).
- This report.

## Technical Details
- Workflow (4 agents, 0 errors, high confidence): researched the Ultra upload dialog, how to set points after upload, community "1 point each" reports, and whether QTI preserves points.
- Findings:
  - Ultra "Upload questions from file" flow (test > + > Upload questions from file > Browse > Submit > OK) has NO "Points per question" field. Original Course View DOES - the source of my earlier incorrect advice.
  - Uploaded questions default to 1 point each in Ultra (Blackboard lowered the default from 10 to 1). Matches the user's observed 40x1=40.
  - Tab-delimited format has no points column, so points can never be embedded in the file.
  - FIX - Bulk Edit Points: test canvas > ellipsis (...) upper-right > Bulk Edit Points > Select All > enter 2.5 > Update. Test total recalculates to 100 automatically (total = sum of per-question points; no separate total field).
  - QTI/Common Cartridge does NOT solve it: QTI imports into Ultra as a question bank/pool without point values. Ruled out as an alternative.
- Sources: Anthology Ultra "Upload or Import Questions"; Baylor College of Medicine Ultra guide (default point = 1); UNLV/UTLV ScreenSteps "Bulk Point Editing"; UConn KB; Teesside University.

## Results
Definitive, sourced answer delivered: upload the .txt as-is, then Bulk Edit Points -> Select All -> 2.5 -> Update = 100 total. Owned and corrected the earlier upload-dialog advice (valid for Original, not Ultra).

## Issues / Notes
- One of four agents claimed the Ultra upload dialog has a points field; the other three (high confidence) plus the Baylor Ultra screenshot guide plus the user's real-world 1-point result contradict it - treated as a conflation with Original Course View.
- No file regeneration needed; the fix is purely the post-upload Bulk Edit Points action.
