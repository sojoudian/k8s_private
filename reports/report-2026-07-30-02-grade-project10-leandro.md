# Report: Grade Semester Project 10 — Leandro Delgado (Mini multi-tenant cluster)

**Date**: 2026-07-30
**Sequence**: #02 for the day

## Summary
Graded the two repository-assessable parts of Project 10 (Mini multi-tenant cluster) for Leandro
Delgado (Seneca ID 114416241). The submitted PDF is a 2-page cover declaring the repo + frozen commit;
graded the repo `leandg5/multitenant-114416241` @ `f4c6090`. Implementation 25/25 + Bootstrap 15/15;
presentation (35+25=60) taken as full per convention (flagged for confirmation). **Final: 100/100.**
Second flawless project repo this cycle (alongside Indah's Project 13 = 100).

## What Changed
- No student files modified (read-only grading).
- Copied the cover PDF to scratchpad; cloned + inspected the repo at the frozen commit (4 commits, 2026-07-19..21, all before due).
- Created this report.

## Technical Details
Every task verified:
- T1 namespaces tenant-114416241-{a,b,c} with owner + tenant labels; STUDENT_ID single source in vars.sh, targeted envsubst.
- T2 ServiceAccounts dev-{a,b,c} per namespace.
- T3 Roles tenant-dev (namespace-scoped) with exactly get/list/watch/create/delete on pods/services/configmaps/deployments + get/list on secrets; per-tenant RoleBindings to only that SA; NO ClusterRoleBindings.
- T4 mint-kubeconfig.sh: create token --duration=2h, assembles standalone kubeconfig (embedded CA + server + token + context) that works with no flags.
- T5 quotas base(a)/2x(b)/half(c) exact on cpu/mem; pods/secrets 5/10/3 with a documented 5/2->3 rounding for tenant c so its 2-replica app fits AND leaves headroom for the CPU-based over-quota demo.
- T6 LimitRanges defaultRequest 100m/64Mi, default 200m/128Mi; fit under every quota.
- T7 Secrets secret-114416241-<t> stringData owner=114416241-tenant-<t>; Deployments web-114416241 nginx:1.27 2 replicas, no resources (LimitRange fills).
- T8 authz-matrix.sh 3x3 can-i get secrets via --as; evidence authz-matrix.txt shows clean diagonal.
- T9 overquota-pod.yaml requests cpu "2" exceeds quota-c 250m; no numeric prefix so bootstrap skips it.
- T10 all raw YAML + kubectl, numbered; no Helm/kustomize.
- T11 bootstrap.sh clean host -> render -> apply in order -> wait rollouts -> mint 3 kubeconfigs -> node allocatable -> denial matrix. bootstrap-timing.log: DONE in 84s.
- Runbook (229 lines): quota-vs-node-allocatable arithmetic incl. "legal quota, still unschedulable" (3.5 CPU limits vs 2 CPU/worker).
- .gitignore excludes kubeconfigs/ + *.kubeconfig + manifests/rendered/; no committed tokens/kubeconfigs/creds (scan clean).

Pass bars all met from repo/evidence: bootstrap <15min (84s), cross-tenant denial proven, no
ClusterRoleBindings, no committed creds, student ID stamped through namespace/names/secret data.
No 60-cap.

## Results
Implementation 25 + Bootstrap 15 + presentation 50 (−10, see below) = **90/100**.

Presentation deduction −10 (professor's call, live-observed):
- The live-demo part: the demo was not performed to standard.
- The oral part: incorrect answers to the questions asked during the presentation.

## Issues / Notes
- Repo parts remain 40/40 (Implementation 25 + Bootstrap 15); the −10 is entirely on the
  live-observed presentation (demo + oral), per the professor.
- Commits authored as "EC2 Default User <ec2-user@...>" (committed from the EC2 host, git identity
  not set to his GitHub account) — not a deduction; repo ownership is declared in the PDF cover.
- Only 4 commits — thin history but all before due and the work is coherent/self-consistent.
