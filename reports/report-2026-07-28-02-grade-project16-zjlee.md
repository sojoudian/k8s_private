# Report: Grade Semester Project 16 — Zhuo Jue Lee (zjlee, 109920256)

**Date**: 2026-07-28
**Sequence**: #02 for the day

## Summary
Graded the two repository-assessable components of **Project 16 — Async job orchestration with
KEDA and native-API workers** for student Zhuo Jue Lee (Seneca ID 109920256), repo
`zhuojuelee/S26-CLO835-Project` @ frozen commit `d20f430`. This is a DIFFERENT project from the
PostgreSQL one (the course offers a menu of ~16 individual projects; this student chose #16).
Per the professor's instruction, the presentation (Live demo 35 + Oral 25 = 60) is taken as full.
Graded Implementation (16/25) + Bootstrap (8/15). **Raw total 84/100**, with a flagged pass-bar
cap decision that could reduce it to 60.

## What Changed
- No project files changed (read-only grading).
- Cloned + inspected the repo at the frozen commit in the scratchpad.
- Identified the correct spec (`project/Project_16_Async_job_orchestration_with_KEDA_and_native_API_workers.docx`).
- Ran a background grading Workflow (5 dimension graders + 44 adversarial verifications, 49 agents).
- Created this report.

## Technical Details
Method: inline scouting (bootstrap.sh, manifests, app code, runbook) + a Workflow that fanned out
5 dimension graders (manifests/RBAC/KEDA/quota; app-code; bootstrap; runbook/evidence;
hygiene/git) each returning structured findings, then adversarially verified every deduction and
pass-bar flag (38 CONFIRMED, 5 PARTIAL, 1 REFUTED).

Strengths (verified): genuinely working non-blocking design (main-server returns 202+jobId without
awaiting; nonblock.png shows 24 POSTs at 30-63ms during 24x30s jobs); both offload paths
(/queueJob->BullMQ, /spawnJob->native createNamespacedJob); P3 CONFIRMED (ephemeral Jobs created by
orchestrator's own namespace-scoped least-privilege SA via in-cluster token, not kubectl/cluster-
admin); controllable sleep tasks; BullMQ retry/stall handling; CI build+push only (Task 13);
clean layout; all 6 runbook procedures; 61-commit genuine history; no committed secrets.

Confirmed deductions:
- Implementation 16/25: minReplicaCount:1 not 0 (no scale-to-zero, Task 7/P2, MAJOR); KEDA not
  vendored, fetched from network URL (Task 6/P6, MAJOR); no ResourceQuota anywhere + requests/limits
  only on worker (Task 11, MODERATE); Redis Service named redis-service not redis-109920256
  (Task 2); maxReplicaCount 15 unjustified; /spawnJob not /ephemeralJob (Task 4); ephemeral Job
  name/labels carry UUID not student ID (Task 9); job output never prints 109920256 (P5 "in job
  output"); runbook (d) omits BullMQ/Redis mechanism naming + malformed -l selector + GUI-driven
  posting steps. REFUTED (not deducted): Role omitting pods get/list is correct least-privilege
  (orchestrator tracks status via Redis, never lists pods).
- Bootstrap 8/15: brings the system up (KEDA incl.) under 15 min (evidence 0-bootstrap), BUT is
  INTERACTIVE (four read prompts -> not unattended, P4) and NOT self-reproducing from the frozen
  commit (applies manifests from raw.githubusercontent .../refs/heads/main, i.e. main branch not
  d20f430); no ResourceQuota applied; hard-depends on EC2 IMDS.

Pass-bar tension (rubric caps total at 60 if any pass bar missing): frozen artifacts FAIL P2
(scaledObject min=1), P4 (interactive bootstrap), P6 (KEDA not vendored + optional managed-AWS ALB).
Professor already credited the demo full (waiving demo-based P1/P2/P3 live), so recommended 84 with
those failures reflected as deductions rather than double-penalized via the cap; strict enforcement
= 60. Left the decision to the professor and flagged the P2 manifest-vs-demo contradiction as the
one to reconcile.

## Results
Implementation 16 + Bootstrap 8 + Presentation 60 (full) = **84/100** raw; **60/100** if the pass-bar
cap is enforced strictly on the frozen artifacts. Delivered the breakdown to the professor with the
cap decision surfaced as their call.

## Issues / Notes
- Workflow artifacts: /Users/maziar/.claude/projects/-Users-maziar-Downloads-k8s-week3/4c65ef92-e3a8-40bf-9a8a-97634bbfb537/workflows/scripts/grade-project16-zjlee-wf_174d6b71-edf.js (run wf_174d6b71-edf).
- Single most important item for the professor: the frozen ScaledObject cannot scale to zero
  (min=1) yet the demo was credited full — reconcile whether scale-to-zero was actually shown.
- Student-facing fixes: set minReplicaCount 0; vendor keda-2.20.0.yaml under manifests/; add a
  ResourceQuota + requests/limits on all containers; make bootstrap non-interactive (flags/env) and
  apply LOCAL manifests (not main-branch URLs); name Redis service redis-<id>; stamp student ID into
  the ephemeral Job name/labels and job output.
