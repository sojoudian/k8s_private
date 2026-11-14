# Report: Grade Semester Project 14 — Marjan Haghighi (Service-discovery failure clinic)

**Date**: 2026-07-30
**Sequence**: #04 for the day

## Summary
Graded the repository-assessable parts of Project 14 (Service-discovery failure clinic) for Marjan
Haghighi (Seneca ID 127878254), repo `MarjanHaghighi/CLO835-Project-Kubernetes-Service-Discovery-Clinic`.
No frozen commit hash was provided, so graded HEAD `2d90526`. Implementation 25/25 + Bootstrap 15/15;
presentation 60 taken as full per convention. **Total: 100/100.**

## Grade
| Component | Score |
|---|---|
| Implementation | 25/25 |
| Bootstrap | 15/15 |
| Presentation (Live demo + Oral) | 50/60 (−10) |
| Total | 90/100 |

Presentation deduction −10 (professor's call, live-observed):
- The live-demo part: the demo was not performed to standard.
- The oral part: incorrect answers to the questions asked during the presentation.

## Technical Details (verified against repo)
- namespace clinic-127878254; db-127878254 Deployment (1 replica, app=db/owner labels), mysql:8, seeded
  via db-seed-127878254 initdb ConfigMap (clinic_items, 5 rows each student_id=127878254); passwords
  from Secret db-secret-127878254 (created in bootstrap, NOT committed).
- db-svc-127878254 ClusterIP selector app=db,owner, port 3306; web references db only by DB_HOST DNS
  name (from app-config-127878254 ConfigMap) — no hardcoded IPs anywhere.
- web-127878254 Deployment (2 replicas), image marjanhaghighi/clo835-project-service-discovery-web:v1;
  web_app.py prints student_id + db_service + seeded row; fails LOUDLY (socket.gaierror -> 503 dns_error,
  mysql.connector.Error -> 503 database_error, never generic 500); /ready queries DB (goes unready when
  db unreachable); /live independent.
- web-svc-127878254 NodePort 30080; debug-127878254 busybox:1.36 sleep infinity.
- diagnosis-tree.md (593 lines): layered tree (confirm symptom -> Service exists -> Endpoints -> why
  empty: selector mismatch/pods down -> CoreDNS) with prediction, exact command, distinguishing output,
  layer, and repair per branch; coredns-known-good.yaml present for the Corefile fix.
- bootstrap.sh: kind cluster (config), apply namespace/configmap/seed, create db-secret from prompted
  password, apply db/web/debug, rollout waits, ends with curl against localhost:30080.
- CI (.github/workflows/docker-build-push.yml): build+push only to Docker Hub via secrets; no kubectl.
- Secret scan clean (only read -rsp prompts + env refs); commit history 7 commits 2026-07-26..27.

## Issues / Notes (for professor, not deductions)
- bootstrap.sh PROMPTS for DB_PASSWORD/MYSQL_ROOT_PASSWORD (read -rsp) if not exported — a
  security-correct choice (avoids committing a secret) but not fully unattended; export the vars first
  for a hands-off run. Not penalized.
- No frozen commit hash declared by the student/professor; graded HEAD 2d90526.
- terraform/ provisions the EC2 host only (allowed) — not an app-level managed-AWS use.
