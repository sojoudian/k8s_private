# Report: project/ folder with 15 MS Word project specs
**Date**: 2026-07-08
**Sequence**: #02 for the day

## Summary
Created `/Users/maziar/Downloads/k8s_week3/project/` containing 15 .docx files, one per individual semester project, formatted after `Assignments/Assignment_2/CLO835_Assignment2.docx`. Content adapted from `Semester_Projects_Individual.md`.

## What Changed
- New folder `project/` with `Project_01_MySQL_StatefulSet_failover.docx` through `Project_15_Self_healing_and_probe_tuning.docx` (~15 KB each).
- Scratch tooling only (parser + docx-js generator) outside the repo.

## Technical Details
- Extracted Assignment 2's exact structure (Heading1 title; Heading2 sections: Outline, Architecture, Evaluation, Submission with Plagiarism + Integrity Pledge, Learning Outcomes, Tasks table, Recording/Presentation, Appendix) and mirrored it per project: Project Outline, Architecture and Environment, Learning Outcomes Covered in Project, Tasks (numbered table, full requirement text per row), Runbook Requirements, Evaluation (100-pt rubric + pass bars capping at 60), Submission (freeze rule: submission = final commit hash, presentation immediately after in the same session from that exact commit; ID-stamping; no committed credentials; plagiarism + integrity pledge in A2 wording), Presentation (numbered live-demo script with the instructor twist + 5 oral questions).
- Generated with docx-js per the docx skill; US Letter, 1-inch margins, Times New Roman throughout (user's Word-doc rule; A2 itself is Arial), proper list numbering, bordered tables with DXA widths.
- Parsed the 15 specs from Semester_Projects_Individual.md (all 8 subsections present in each).
- First render showed the Tasks column auto-split breaking sentences (e.g. at "clusterIP: None"); fixed by switching to numbered rows with full requirement text.

## Results
All 15 files pass the docx skill validator; Project 1 rendered to PDF and visually checked (pages 1-2 clean).

## Issues / Notes
- Project weight line reads "Refer to Blackboard for its weight in your final grade" (weight not stated anywhere in the course materials for the semester project).
- `Semester_Projects_Individual.md` remains as the source document.
