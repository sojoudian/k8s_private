# Report: Verify CLO835 exam file against official Blackboard Ultra upload spec
**Date**: 2026-07-13
**Sequence**: #04 for the day

## Summary
Verified that `CLO835_Final_Exam_Blackboard.txt` is 100% conformant with Blackboard Ultra's tab-delimited "Upload Questions" format. Rather than trust memory, I confirmed the authoritative format from primary Anthology documentation via three independent researchers, ran an independent line-by-line audit of the actual file against that spec, and did my own byte-level check. Result: PASS, zero blockers.

## What Changed
- No exam files changed (verification only; the file was already correct).
- Scratch only: `verify_bb_format.js` (4-agent verification workflow), byte-level inspection commands.
- This report.

## Technical Details
- Workflow (4 agents, 0 errors): 3 parallel spec researchers pulled the format from the official Anthology Ultra "Upload or Import Questions" page + the Original Course View page, cross-checked against Ulster University, UT-LV ScreenSteps, and Ole Miss FTDC reproductions; then 1 audit agent read the file and checked it against the reconciled spec.
- Confirmed authoritative formats:
  - MC: `MC TAB question TAB (answer TAB correct|incorrect)...`, max 100 answers.
  - MA: same structure, 2+ answers marked correct.
  - TF (highest-risk): `TF TAB question TAB true|false` - exactly THREE fields, a bare true/false value, NO correct/incorrect markers and NO second answer field. All three researchers agreed (high confidence).
  - Rules: no header row; no blank lines between records (a blank line throws an import error); single-tab delimiter; correctness keywords in English; Ultra records-per-file recommendation 250 (Original says 500); encoding and line endings not specified by the docs.
  - Ultra-supported upload types: MC, MA, TF, ESS, MAT, FIB, FIB_PLUS, NUM.
- Byte-level check of the file: no BOM, CRLF endings (40 CRLF, 0 lone LF), no trailing blank line, 40 non-empty records.

## Results
Audit verdict: conforms=true, 0 issues. Per-type: MC 26 (each exactly 1 correct of 4), MA 9 (each 2+ correct and >=1 incorrect), TF 5 (all short 3-field true/false form). Only Ultra-supported types used. 40 records is well under the 250 Ultra cap. File is safe to upload as-is.

## Issues / Notes
- Docs do not formally specify encoding/line endings; the file uses ASCII + CRLF, the de-facto Excel-tested path, so no risk.
- Minor source discrepancies handled: Ultra page recommends 250 records/file vs Original page 500 (used 250 as the safe Ultra number); one Ole Miss Excel screenshot showed a two-column TF layout that contradicts the single-field spec in the same doc and the official table - treated as an error, single true|false field is authoritative.
- Post-upload, Ultra previews uploaded questions but does not allow editing them until they are copied into the assessment (normal Ultra behavior).
