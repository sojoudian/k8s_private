# Report: Add project-assignment sign-up table to the overview
**Date**: 2026-07-08
**Sequence**: #05 for the day

## Summary
Added a "Project assignment" section with a two-column table (Project | Student) to the end of `project/Project_00_Overview_and_Instructions.docx`. All 15 project titles are pre-filled; the Student column is blank for the professor to fill in as projects are claimed.

## What Changed
- `project/Project_00_Overview_and_Instructions.docx` regenerated with the new final section.
- Scratch `gen_overview.js`: added table imports, a `tcell()` helper, an `assignmentTable()` builder, and the "Project assignment" section after the Integrity Pledge.

## Technical Details
- Table: content width 9360 DXA, columns Project 6360 / Student 3000, single 999999 borders, header row shaded DDDDDD and bold, cell padding 80/120. Data rows use HeightRule.ATLEAST 360 so blank student cells are writable when printed.
- Titles pulled directly from projects.json (sorted by project number) so they match the 15 detail files exactly, prefixed with the project number (1..15) for easy mapping to Project_01 ... Project_15.
- Placed at the very end, after the Integrity Pledge, per the user's stated preference. Times New Roman, no em dashes.

## Results
Validated OK (docx validator). Rendered to PDF and visually verified: table shows all 15 titles filled and the Student column empty.

## Issues / Notes
- Grade weight still not set (files say "refer to Blackboard").
