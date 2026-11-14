# Report: Grade Semester Project 12 — Olivier Moriceau (Secrets rotation with zero downtime)

**Date**: 2026-07-30
**Sequence**: #05 for the day

## Summary
Graded the repository-assessable parts of Project 12 (Secrets rotation with zero downtime) for Olivier
Moriceau (ID omoriceau), repo `omoriceau/clo835-project12-secrets-rotation` @ frozen commit `b0b02c6`.
Implementation 25/25 + Bootstrap 15/15; presentation 60 taken as full per convention. **Total: 100/100.**

## Grade
| Component | Score |
|---|---|
| Implementation | 25/25 |
| Bootstrap | 15/15 |
| Live demo | 35/35 (professor) |
| Oral | 25/25 (professor) |
| Total | 100/100 |

Where lost: —

## Technical Details (verified against repo)
- namespace rotation-omoriceau; MySQL single-replica StatefulSet + PVC (volumeClaimTemplates, standard SC),
  headless Service mysql-omoriceau (clusterIP:None, documented as the headless variant satisfying "ClusterIP
  Service mysql-<id>"); root password from imperatively-created Secret mysql-root-omoriceau (not committed).
- webapp-omoriceau Deployment, 2 replicas, RollingUpdate maxUnavailable:0/maxSurge:1; creds MOUNTED AS FILES
  from Secret db-cred-omoriceau at /etc/dbcred (read at connection time, not cached — app.py read_credentials());
  readiness /healthz runs SELECT 1. Image ghcr.io/omoriceau/clo835p12-webapp.
- app.py: / returns owner=<id> connected_as=<CURRENT_USER()> + seeded row; reads creds fresh per request.
- 35-webapp-envvar-variant.yaml (Task 5): secretKeyRef variant with an excellent comment on why env vars
  can't observe a live rotation (injected once at start) and why they still rollout restart (deterministic
  cutover, re-auth, kubelet sync-race).
- NodePort webapp-omoriceau 30080 -> hostPort 8080 via kind extraPortMappings (1 cp + 2 workers).
- monitor.sh: 1 req/sec, total/failed counters, any non-200/curl-error increments failed.
- rotate.sh: ./rotate.sh v2|v1|v3; create appuser_<ver>_omoriceau (openssl rand, GRANT SELECT, CREATE IF NOT
  EXISTS + ALTER resync) -> update Secret (dry-run|apply) -> rollout restart+status -> verify connected_as=
  (retry for endpoint propagation) -> MANDATORY pause (read -p) -> drop old user. Order documented; handles
  rollback to a fresh v1/v3.
- bootstrap.sh: clean host -> kind -> mysql-root secret (openssl) -> seed demo_data (3 rows, student_id=
  omoriceau, idempotent) + appuser_v1 -> db-cred v1 Secret -> webapp -> smoke curl. <15min.
- CI (.github/workflows/build-push.yml): build+push to GHCR only; comment + content confirm no kubectl.
- Secret hygiene: all passwords openssl-generated; none committed; .gitignore excludes .env + secrets/*.
- Evidence: monitor-during-rotation.txt failed=0 throughout; dead-credential-proof.txt "Access denied for
  user 'appuser_v2_omoriceau'" (old credential revoked); rotation-v1/v2 logs.

## Issues / Notes (for professor, not deductions)
- AI disclosure in the integrity pledge: student states AI was used for documentation, the 2-tier webapp code,
  and consultation — NOT to perform the K8s work. Graded substance (manifests, rotate.sh, bootstrap.sh) shows
  genuine understanding. Whether AI-authored webapp code is "unauthorized help" is the professor's integrity
  call; not penalized here.
- 9 commits (2026-07-25..26) via PRs, all before due.
