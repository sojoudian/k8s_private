# Report: Grade Semester Project 13 — Indah Cahyani Styoningrum (HPA under load)

**Date**: 2026-07-30
**Sequence**: #01 for the day

## Summary
Graded the two repository-assessable parts of Project 13 (HPA under load) for Indah Cahyani
Styoningrum (Seneca ID 115029258), repo `indahcs/hpaunderload` @ frozen commit `bb1b6de`.
Implementation 25/25 + Bootstrap 15/15; presentation (Live demo 35 + Oral 25 = 60) taken as full per
the professor's convention (flagged for confirmation). **Final: 100/100.** Strongest project repo of
the three graded this cycle (hdhnguyen 99, zjlee 84, Indah 100).

## What Changed
- No student files modified (read-only grading).
- Cloned + inspected the repo at the frozen commit in scratchpad/proj_indah (32 commits, 2026-07-21..07-26, all before due, via PRs).
- Created this report.

## Technical Details
Every task verified against the repo:
- T1 kind-config 1 control-plane + 2 workers; cluster 115029258-hpa in bootstrap.
- T2 metrics-server VENDORED (manifests/metrics-server.yaml) with --kubelet-insecure-tls + correct comment.
- T3 namespace 115029258-hpa.
- T4 Deployment 115029258-burn replicas:1, requests cpu 200m / limits 500m, Go app response "OK burn 115029258 ...".
- T5 ClusterIP Service on port 80. NOTE: named s115029258-burn-svc (leading 's') — this is CORRECT, not a
  fault: a K8s Service name is an RFC-1035 DNS label and cannot start with a digit, so the literal
  <id>-burn-svc is invalid. Handled properly (load job references the same s-prefixed name).
- T6 HPA autoscaling/v2, CPU Utilization 50%, min1/max10, scaleDown stabilizationWindowSeconds 60.
- T7 quota.yaml parameterized (${QUOTA_PODS}, ${QUOTA_CPU}); apply-quota.sh validates + envsubst; default
  6 pods / 1000m caps below maxReplicas → collision demonstrable.
- T8 load-job.yaml: 3 busybox wget pods with own CPU requests (50m/100m).
- T9 bootstrap.sh: clean host -> full system, blocks until kubectl top pods returns numbers, idempotent,
  waits nodes/rollouts/metrics/HPA, prints final state, leaves load job for demo. evidence/01 clean run.
- T10 raw YAML + kubectl in git; no GitHub Actions (optional); image on Docker Hub (icstyoningrum/115029258-burn:v1).
- Runbook (1354 lines): all required procedures + worked replica-prediction arithmetic + correct deep
  note that a requests.cpu quota forces temporary test pods to declare CPU requests.
- Secret scan clean. Evidence genuine: 08-replicaset-quota-collision shows real
  "forbidden: exceeded quota: 115029258-quota ... used: pods=6, limited: pods=6" + ReplicaFailure.

Pass bars: bootstrap-to-metrics <15min and student-ID stamping met from repo; live bars corroborated
by transcripts (05 prediction, 07 scale-out, 08 collision, 11-13 scale-down). No 60-cap triggered.

## Results
Implementation 25 + Bootstrap 15 + presentation 60 (full) = **100/100**. Nothing lost. Could not find
a defensible deduction.

## Issues / Notes
- Presentation assumed graded full (professor's convention this cycle); confirm if different.
- The s-prefixed Service name is a correct RFC-1035 workaround, explicitly NOT penalized.
