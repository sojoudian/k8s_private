# Report: Semester project overview/instructions Word file
**Date**: 2026-07-08
**Sequence**: #03 for the day

## Summary
Created `project/Project_00_Overview_and_Instructions.docx`, a one-page student-facing overview that sits at the front of the `project/` folder and explains how the semester project works. Styled after the Blackboard lab instruction pages the user shared, Times New Roman throughout.

## What Changed
- New file `project/Project_00_Overview_and_Instructions.docx` (sorts before Project_01 ... Project_15).
- Scratch generator `gen_overview.js` only (outside the repo).

## Technical Details
- Sections: intro, "Pick your project", "Build it, version it on GitHub, and make it reproducible", "Present it in 10 minutes and answer questions", "Where the details are", "Integrity Pledge".
- Encodes exactly the user's requirements: pick one of the 15; no two students share a project (first-come, claimed off the list); assignment over email or in labs/lectures; may propose a new subject or modify one toward industry work, by email, approved before starting; everything versioned on GitHub and reproducible from a clean clone via bootstrap.sh so it can be graded; 10-minute in-person live demo; must answer individual questions about the project.
- Reused the Assignment-2-style docx-js config from gen_projects.js (Heading1/Heading2 in Times New Roman, bullet numbering, US Letter, 1-inch margins). No em dashes (Rule 4).

## Results
Validated OK (docx validator, all passed). Rendered to PDF and visually verified: one clean page, correct headings, bullets, and Integrity Pledge.

## Issues / Notes
- The 15 individual project files describe the live demo and oral questions but do not state the 10-minute cap; offered to add "10 minutes" to each if wanted.
- Grade weight still not set anywhere (individual files say "refer to Blackboard").
