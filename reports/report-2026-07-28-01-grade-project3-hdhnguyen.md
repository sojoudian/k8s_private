# Report: Grade Semester Project 3 — Huu Duc Huy Nguyen (hdhnguyen)

**Date**: 2026-07-28
**Sequence**: #01 for the day

## Summary
Graded the two repository-assessable components of Project 3 (PostgreSQL streaming
replication on kind) for student `hdhnguyen` — Implementation (25) and Bootstrap (15) —
against the Project_03 rubric. Per the professor's instruction ("grade everything except
the presentation, that part I graded full only for the presentation part"), the Live demo
(35) and Oral (25) were taken as full. **Final grade: 99/100.**

## What Changed
- No project files changed (read-only grading).
- Cloned + inspected `github.com/jaydenhnguyen/postgresql-streaming-replication-k8s` @ frozen
  commit `70c78db` in the scratchpad.
- Created this report.

## Technical Details
Evidence-based grading against all 12 Tasks + runbook + evidence transcripts + full-history
secret scan:
- **Bootstrap 15/15**: `src/bootstrap.sh` — parameterized student ID (`$1`/`STUDENT_ID`),
  `envsubst` templating (no secrets to git), random-password fallback (zero manual steps),
  `rollout status`/`wait` gates, idempotent, wall-clock timing. Evidence `01-bootstrap.txt`:
  `real 86.98s` clean-host → primary/standby on **different workers**, PVCs Bound 5Gi,
  `streaming | async`, 20 seed rows.
- **Implementation 24/25**: every task verified in-repo — namespace `pg-<id>`; two
  single-replica StatefulSets; two headless Services + `pg-write` ClusterIP; ConfigMap-driven
  `wal_level=replica`/`max_wal_senders=10`/`scram-sha-256`; idempotent `pg_basebackup -R -X
  stream -C -S <slot>` initContainer; seed `events_hdhnguyen` 20 rows tagged
  `student-hdhnguyen`; Secret `pg-creds-<id>` templated; full ID parameterization; runbook
  covers all 8 procedures with a `pg_wal_replay_pause()` lag/row-loss window and exact
  `sent/made_it/lost` accounting; both promotion methods documented. Lag evidence LSN math
  verified (`0x3447EA0−0x3446F38 = 3944` = reported `lag_bytes`).
- **−1 pt**: one literal committed password `POSTGRES_PASSWORD: p@sswoord123` in the peripheral
  `postgres-learning/docker-compose.yaml` (self-study folder, not the K8s deliverable) — small
  but defensible against the "no passwords committed" rule.
- **Noted, not further penalized**: deliverables under `src/` rather than repo root (documented
  in runbook, not a functional break); `postgres:18` vs spec's `postgres:16` (still official
  Docker Hub, works).
- **Pass bars**: all met — no 60-cap. 53 commits, all before due; real PR/branch workflow.

## Results
Final grade **99/100** = Implementation 24 + Bootstrap 15 + Live demo 35 (full) + Oral 25 (full).
Strongest Project 3 submission reviewed to date. Delivered the breakdown to the professor.

## Issues / Notes
- Presentation (60 pts) not independently re-verified — graded full at the professor's explicit
  direction; the runbook methodology corroborates the demo/accounting pass bars.
- The committed throwaway password is the single actionable feedback item for the student.
