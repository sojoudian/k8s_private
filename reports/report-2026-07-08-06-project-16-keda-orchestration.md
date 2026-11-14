# Report: Project 16 (student KEDA orchestration proposal) written up
**Date**: 2026-07-08
**Sequence**: #06 for the day

## Summary
Turned Zhuo Jue Lee's emailed project proposal into a full Project 16 spec, `project/Project_16_Async_job_orchestration_with_KEDA_and_native_API_workers.docx`, in the same format as the other 15. Every element from his diagram was preserved and extended with course-relevant depth and the universal project rules.

## What Changed
- New file `project/Project_16_Async_job_orchestration_with_KEDA_and_native_API_workers.docx` (folder now holds Project_00 + Project_01 ... Project_16).
- Scratch: `add_project16.js` appended the P16 entry to projects.json (now 16 projects); regenerated via gen_projects.js.

## Technical Details
- Preserved verbatim from the proposal: Client, Main Server, Job Orchestrator Server, POST /queueJob and POST /ephemeralJob, Redis queue, BullMQ workers (1/2/3), KEDA scaling the queue-based workers, the ephemeral long-running worker created via native K8s API, and the non-blocking goal.
- Extended with: namespace + student-ID stamping; Redis and BullMQ as in-cluster Pods (no managed services); KEDA installed from a pinned raw YAML bundle vendored in the repo (no Helm); a ScaledObject on Redis queue length with scale-to-zero and a justified max; a least-privilege ServiceAccount + Role/RoleBinding so the orchestrator can create Jobs only in its namespace; a ResourceQuota bounding the fan-out; an explicit non-blocking proof (latency probe vs job duration); bootstrap.sh clean-host bring-up in 15 minutes; GitHub-Actions-build-only rule.
- Full section set matching the other 15: Project Outline, Architecture and Environment, Learning Outcomes, Tasks (13 numbered rows), Runbook Requirements (6), Evaluation (100-pt rubric + 6 pass bars), Submission (freeze rule + KEDA-version + evidence + Plagiarism + Integrity Pledge), Presentation (10 minutes, already-running system, 8 demo steps with a two-part instructor twist, scale-to-zero and worker-kill), 5 oral questions.
- Times New Roman, no em dashes.

## Results
Validated OK. Rendered all 6 pages to PDF and visually verified: title/outline, architecture, tasks table, runbook, presentation, and orals all clean.

## Issues / Notes
- Project 16 is a custom, approved add-on for one student; the overview still says "15 projects" and its assignment table lists 1-15. Not auto-added there. Offered to add a "16. ..." row with the student's name if wanted.
- Approval conditions from the prior assessment (scope control, KEDA-via-raw-manifest, least-privilege RBAC, non-blocking proof) are baked into the Tasks and pass bars.
- Grade weight still not set (files say "refer to Blackboard").
