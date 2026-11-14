# Report: Grade Semester Project 7 — Elvis Tran (Zero-data-loss app upgrade)

**Date**: 2026-07-30
**Sequence**: #06 for the day

## Summary
Graded the repository-assessable parts of Project 7 (Zero-data-loss app upgrade) for Elvis Tran
(etran12), repo `elvis-tran/zero-data-loss-upgrade` @ frozen commit `d7eb266`. Implementation 25/25 +
Bootstrap 15/15; presentation 60 taken as full per convention. **Total: 100/100.**

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
- params.env single source: STUDENT_ID=etran12, NAMESPACE=upgrade-etran12, images docker.io/elvistrann7/notes-app:v1|v2.
- MySQL (Task 1): PVC mysql-data-etran12 (standard SC), Service mysql (ClusterIP), ConfigMap mysql-config
  (MYSQL_DATABASE=notesdb), Secret mysql-creds-etran12 (root/user/password). Single-replica Deployment.
- notes-app v1 Deployment 2 replicas (${APP_IMAGE_V1}) + NodePort notes-app-svc 30080->8080; app renders
  student_id + app_version + schema_version (read live from schema_version table).
- Seed: 20 rows author=${STUDENT_ID} (notes 18-20 labeled "will be damaged by migration v2").
- Migrations: 001_init.sql (schema_version 0->1, notes table); 002_v2.sql INTENTIONALLY BROKEN per Task 5
  (ADD content, UPDATE ... WHERE id<=10, SLEEP 15, DROP body, schema_version=2) -> rows>10 NULL content.
  Correct by design, not a fault.
- v2 readiness gate: app /ready returns 503 unless schema_version == EXPECTED_SCHEMA_VERSION(2) -> forces
  migrate-before-rollout (Task 4). create_note also gates on schema.
- Backup/restore (Task 6): take-backup.sh renders 13-backup-job.yaml with a timestamp; mysqldump --databases
  notesdb; restore-backup.sh + 16-restore-job replay. Streamed to host per runbook.
- Row-count one-liner (Task 9): scripts/k8s-row-count.sh detects body(v1)/content(v2) column, prints
  total_rows + COUNT(note_column) non-null.
- bootstrap.sh: params.env -> envsubst -> kind -> apply in order -> migrate-v1 (delete+apply+wait) -> seed
  job -> wait v1 over NodePort (wait/wait_for_http, not sleep). Idempotent. <15 min.
- Secret scan clean (creds from Secret mysql-creds-etran12, none committed). 14 commits 2026-07-24..26.

## Issues / Notes (for professor, not deductions)
- 002_v2.sql "broken" SQL is required by the spec (destructive migration committed as-is; fix is
  operational). Not penalized.
- No GitHub Actions in repo (optional per Task 10); images pushed manually to Docker Hub.
- (Aside) etran12 had an empty Lab03 file and did not submit Lab04/Lab05 earlier; this project repo is
  complete and correct.
