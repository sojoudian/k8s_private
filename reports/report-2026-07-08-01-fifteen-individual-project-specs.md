# Report: 15 individual semester project specs (full handout)
**Date**: 2026-07-08
**Sequence**: #01 for the day

## Summary
Authored the complete student handout for the 15 individual semester projects (one per student) and wrote it to `Semester_Projects_Individual.md`. Each project has a deep spec: goal, learning outcomes, environment, numbered build requirements, mandatory runbook contents, submission rules, a live-demo script with the instructor twist, 5 oral questions, and pass bars. The submit-then-present protocol is explicit: submission freezes a commit hash and the student presents immediately, same session, from that exact commit.

## What Changed
- `Semester_Projects_Individual.md` (new, ~151 KB, 15 project sections + common rules header).
- `reports/report-2026-07-08-01-fifteen-individual-project-specs.md` (this report).

## Technical Details
- 15 specs authored in parallel (one agent per project) against a fixed template and hard constraints: kind on EC2/Cloud9 only, raw YAML + kubectl, no Helm, no EKS/managed AWS, images via Docker Hub/GHCR, GitHub Actions build-only.
- Universal mechanics baked into every spec: student-ID stamping in names AND data; bootstrap.sh clean-host bring-up in <=15 min; runbook.md with copy-pasteable procedures; live-terminal evidence; one parameterized instructor twist per demo.
- Common header adds the submit-then-present protocol and a shared 100-point rubric (25 implementation / 15 bootstrap / 35 live demo / 25 orals; pass bars cap at 60).
- User formatting rules applied: all em/en dashes stripped (verified 0 remaining), concise direct language.
- Consistency scan: no Helm/eksctl/LoadBalancer references anywhere; "EKS" appears only in the prohibition rule.

## Results
File verified: 15 `## Project N` sections, all named per the approved list, projects 1-4 use four different databases (MySQL, MongoDB, PostgreSQL, Redis).

## Issues / Notes
- Project 1 states the instructor provides a reference for the MySQL replication init scripts (per the feasibility review) - that reference implementation still needs to be produced before term start.
