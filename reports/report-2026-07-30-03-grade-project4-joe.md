# Report: Grade Semester Project 4 — Joe-Smith Effiong Essang (Redis with Sentinel)

**Date**: 2026-07-30
**Sequence**: #03 for the day

## Summary
Graded the two repository-assessable parts of Project 4 (Redis with Sentinel) for Joe-Smith Effiong
Essang (jeessang), repo `Joesmithessang/project-redis-with-sentinel` @ frozen commit `5a4dbc2`.
Implementation 25/25 + Bootstrap 15/15; presentation (35+25=60) taken as full per convention
(flagged for confirmation). **Final: 100/100.** Third flawless project repo this cycle (Indah 100,
Leandro 100-repo, Joe 100).

## What Changed
- No student files modified (read-only grading).
- Cloned + inspected the repo at the frozen commit (26 commits, 2026-07-25..26, all before due).
- Created this report.

## Technical Details
Every task verified:
- T1 namespace redis-jeessang (parameterized ${STUDENT_ID}).
- T2 StatefulSet redis-jeessang 3 replicas + headless redis-hl (clusterIP None, publishNotReadyAddresses,
  documented cold-boot NXDOMAIN reason); startup script decides master vs replica by ASKING SENTINEL
  (get-master-addr-by-name) with pod-0 cold-boot fallback — better than ordinal-only; config from ConfigMap.
- T3 Sentinel StatefulSet sentinel-jeessang 3 replicas (StatefulSet-over-Deployment justified for stable
  identity) + sentinel-svc ClusterIP:26379 (and headless sentinel-hl).
- T4 sentinel.conf = exactly monitor mymaster-jeessang ... 2 (quorum 2), down-after 5000, failover-timeout
  15000, parallel-syncs 1; copied ConfigMap -> writable emptyDir before start (read-only mount ->
  CrashLoop, documented). resolve/announce-hostnames yes.
- T5 seed job: owner=jeessang + 50 keys jeessang:seed:<n>, via Sentinel discovery (not hardcoded).
- T6 writer.sh: jeessang:live:<n> once/sec via Sentinel get-master-addr-by-name; lost-write counter +
  master rediscovery on failure.
- T7 replica-read-only yes; READONLY rejection shown in runbook.
- T8 single-var parameterization, envsubst into manifests/rendered/.
- T9 bootstrap.sh: clean host -> render -> kind (1cp+2w) -> apply -> rollout/wait (not sleep) -> seed job
  wait -> Sentinel master check. ~112-123s (5 logged runs). Pinned kind v0.31.0 / kubectl v1.35.0.
- T10 raw YAML + kubectl; no Helm/managed AWS; image redis:7-alpine (Docker Hub).
- Runbook (214 lines): all procedures (get-master, INFO replication, writer, watch failover
  +sdown->+odown->+vote->+switch-master, 3 trigger methods, verify data + lost=counter-keycount,
  ckquorum, recovery) + honest gotchas (writer cadence ~1.2-1.5s; split-brain danger).
- Evidence: multiple bootstrap logs (~2 min); real failover logs by method (kill/freeze/drain) showing
  automatic +switch-master and quorum votes; sentinel 2-then-3 quorum test. Secret scan clean (no auth
  configured, no committed secrets).

Pass bars all met: bootstrap <15min (~2min), automatic failover with writer resume (real +switch-master),
lost-write accounting documented, ckquorum + sentinel-death quorum test present, student ID in
namespace/mymaster/data. No 60-cap.

## Results
Implementation 25 + Bootstrap 15 + presentation 60 (full) = **100/100**. Nothing lost.

## Issues / Notes
- Presentation assumed graded full (professor's convention this cycle); confirm if different.
- Student ID is the username-style "jeessang" (matches the spec's own redis-mjafari3 example) — accepted.
