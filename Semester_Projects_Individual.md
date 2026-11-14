# CLO835 Individual Semester Projects - Fall 2026

Fifteen projects, one per student. Every project runs on kind on your own EC2/Cloud9 Linux host. Raw YAML manifests and kubectl only.

## Rules that apply to every project

1. No Helm, no kustomize. Deployment is kubectl apply -f manifests/ plus your bootstrap script.
2. No EKS and no managed AWS services. Everything runs inside kind on your single host. Multi-node clusters are built with a kind config file.
3. Images come from Docker Hub or GHCR. If you use GitHub Actions, it may only build and push images. It never talks to your cluster.
4. Your Seneca student ID must appear in your namespace and resource names AND inside the data itself (seeded rows, app output). Work without your ID stamped through it is not gradable.
5. AI use: allowed for writing YAML and scripts. Not allowed as a substitute for understanding. The grade lives in the live demo and the oral questions, where only operating experience helps.
6. bootstrap.sh is mandatory: from a clean host with only Docker, kind, and kubectl installed, it must build your whole project (cluster, manifests, seed data) in 15 minutes or less.
7. Evidence is live terminal output during your demo. Screenshots in the repo are supporting material only and prove nothing by themselves.

## Submission and presentation: how it works

The moment you finish implementation and submit, you present. There is no gap.

1. Submission = a single git commit hash you declare final. Push it, tell the instructor the hash, and the repo is frozen. No edits, no new commits, no fixes after that.
2. You then present in the same session, from your own host, running exactly that commit: clone it fresh, run bootstrap.sh, and drive the demo from your runbook.
3. During the demo the instructor performs one live twist (kills a pod of their choosing, picks the backup, breaks one object, sets a parameter). The twist is parameterized, so it cannot be rehearsed exactly. You are graded on how you handle it and how you narrate what you expect before each command.
4. Individual oral questions follow. They are asked against your own files, your own data, and your own cluster.

## Grading (100 points, same for every project)

- 25: implementation correct and complete per the build requirements, repo layout and runbook quality included.
- 15: bootstrap.sh brings the whole project up from a clean host within 15 minutes.
- 35: live demo, including the instructor twist and prediction-first narration.
- 25: oral questions.
- Pass bars listed in each project are non-negotiable: missing one caps the project grade at 60.

Four different databases across projects 1-4 and different topics elsewhere, so no two students share answers.

---

## Project 1 - MySQL StatefulSet failover

**Goal.** Build a 3-replica MySQL StatefulSet on a kind cluster where `mysql-0` is the async replication primary and `mysql-1`/`mysql-2` are read replicas that discover the primary through a headless service. In the live demo, the instructor kills a pod of their choosing - possibly the primary, possibly while rows are being inserted - and you prove, from the terminal, that you can promote a replica by following your own runbook and that no committed row was lost.

### What you will learn

- How StatefulSets provide stable pod names (`mysql-0`, `mysql-1`, `mysql-2`), stable DNS, and one PVC per pod via `volumeClaimTemplates`.
- How headless services and CoreDNS give each pod a resolvable identity (`mysql-0.mysql-h.<namespace>.svc.cluster.local`) that replication configuration can depend on.
- How MySQL async replication actually behaves when the primary dies: what is replicated, what can lag, and how to verify with `SHOW REPLICA STATUS`.
- How to write and execute a failover runbook under pressure, instead of improvising with a database at stake.
- Why storage outlives pods: what happens to a PVC when its pod is deleted, and when data survives versus when it does not.

### Environment

- kind cluster with 1 control-plane node and 2 worker nodes, defined in `kind-config.yaml` committed to your repo.
- Image: official `mysql:8.0` from Docker Hub. No custom images required; if you build a helper image it must be pushed to Docker Hub or GHCR and pulled by tag in your manifests.
- Storage: the kind built-in `standard` StorageClass (local-path). No other provisioner.
- Tooling: `kubectl` and the `mysql` client (run via `kubectl exec` into the pods - nothing to install on the host beyond kind, kubectl, and Docker).
- Namespace: `mysql-<studentID>` (e.g. `mysql-jdoe12`). Every resource lives in this namespace.
- The instructor will provide a reference for the ordinal-aware init-container scripts (server-id assignment and mysqldump clone). You may adapt it, but you are graded on operating the system, and you must be able to explain every line you use.

### Build requirements

1. Create namespace `mysql-<studentID>`. All objects below go in it.
2. Create a StatefulSet named `mysql` with `replicas: 3`, `serviceName: mysql-h`, using the official `mysql:8.0` image.
3. Use an init container that derives `server-id` from the pod ordinal (parsed from the pod hostname) and writes a per-pod MySQL config file. `mysql-0` must be configured as the primary; `mysql-1` and `mysql-2` as replicas.
4. On first start, each replica must clone the primary's data via `mysqldump` taken from `mysql-0.mysql-h`, then configure async replication pointing at `mysql-0.mysql-h`. This must be idempotent: a pod restart with existing data must NOT re-clone.
5. Create a headless service `mysql-h` (`clusterIP: None`) selecting all mysql pods, and a normal ClusterIP service `mysql-read` for read traffic across all pods.
6. Use `volumeClaimTemplates` to give each pod its own PVC named `data-mysql-N`, `storageClassName: standard`, at least 1Gi.
7. Store replication scripts and MySQL config in a ConfigMap; store the root and replication passwords in a Secret named `mysql-secrets-<studentID>` (values may be dummy, but must not be hard-coded in the StatefulSet spec).
8. Seed data: bootstrap must create database `clo835`, table `students`, and insert at least 5 rows where one column contains your literal Seneca ID (e.g. `INSERT ... VALUES ('jdoe12', ...)`). Prove replication by reading these rows from `mysql-2`.
9. Write `writer.sh` (committed to the repo): an infinite loop that inserts one timestamped, sequence-numbered row per second into the primary via `kubectl exec`, tagged with `<studentID>`. The demo twist happens while this runs.
10. Write `bootstrap.sh` that, from a clean host with only Docker/kind/kubectl installed, creates the kind cluster from `kind-config.yaml`, applies every manifest, waits for all 3 pods Ready, seeds the data, and verifies replication - end to end in under 15 minutes. It must take the student ID from a variable at the top of the script, and that variable must drive namespace and Secret names.
11. Parameterize nothing else by hand: `kubectl apply -f manifests/` (plus the bootstrap seeding step) must be the whole deployment. No Helm, no kustomize overlays required, no manual `kubectl edit` steps.
12. Everything in git: `kind-config.yaml`, all manifests, all scripts, `runbook.md`. If the instructor clones your repo at your submitted commit, `./bootstrap.sh` must work.

### Runbook you must write

`runbook.md` must contain exact copy-pasteable commands for each of these, tested end to end:

- How to verify replication health: `kubectl exec` into a replica and read `SHOW REPLICA STATUS\G` - which fields you check (`Replica_IO_Running`, `Replica_SQL_Running`, `Seconds_Behind_Source`) and what healthy looks like.
- How to start and stop the write loop (`./writer.sh`), and how to read the last committed sequence number from any pod.
- How to handle a dead replica (`mysql-1` or `mysql-2` killed): what the StatefulSet controller does automatically, how to confirm the pod reattached its PVC and resumed replication, and how to check it caught up.
- How to promote a replica when `mysql-0` dies: the full manual procedure - stop the write loop, pick the most caught-up replica, `STOP REPLICA`, `RESET REPLICA ALL`, disable read-only, repoint clients, and what you do about `mysql-0` when the StatefulSet recreates it.
- How to count rows and verify zero data loss: the exact query comparing the writer's last confirmed sequence number against `SELECT MAX(seq), COUNT(*)` on the surviving primary, and how to explain any gap (rows in flight vs rows committed).
- How to tear down and rebuild from scratch (`kind delete cluster` + `./bootstrap.sh`) in case the demo environment is damaged.

### Submission

- Repo layout:
 - `manifests/` - namespace, ConfigMap, Secret, headless + read Services, StatefulSet, in apply order.
 - `kind-config.yaml`
 - `bootstrap.sh` and `writer.sh` (executable)
 - `runbook.md`
 - `evidence/` - terminal transcripts (`script` or copy-paste) of one full rehearsal: bootstrap, replication check, a kill, a promotion, the row-count proof.
 - `README.md` - one page: what the project is and how to run `bootstrap.sh`.
- Submission = the final commit hash. You present immediately after submitting, in the same session, from exactly that commit on your own host. No edits, no new commits, no "one small fix" after the hash is frozen.

### Presentation (starts right after you submit)

1. On your host, `git clone` your own repo at the submitted commit into a fresh directory and run `./bootstrap.sh`. While it runs, walk the instructor through the StatefulSet manifest and the init-container logic.
2. Show all three pods Ready and one PVC per pod: `kubectl get pods,pvc -n mysql-<studentID>`. Show your seeded `<studentID>` rows exist on `mysql-0` AND on `mysql-2` (proving replication).
3. Show replication health on both replicas with `SHOW REPLICA STATUS\G`.
4. Start `./writer.sh`. Show rows accumulating on the primary and appearing on a replica.
5. **Instructor twist.** The instructor names a pod (`mysql-0`, `mysql-1`, or `mysql-2`) and a moment - possibly mid-write-loop - and you run `kubectl delete pod <their choice> -n mysql-<studentID>` (or they run it themselves). You cannot know in advance whether you are handling a replica loss or a primary loss.
6. Respond using your runbook, out loud: if a replica died, show it come back, reattach its PVC, and catch up; if the primary died, execute your promotion procedure step by step on the replica of your choosing, justifying the choice from replication status.
7. Prove zero committed-row loss: compare the writer's last confirmed sequence number against `MAX(seq)` and `COUNT(*)` on the current primary. Explain any in-flight (uncommitted) writes.
8. Show the recreated pod's fate: what `mysql-0` is now (if it was the victim), what data it has, and what you would do next to restore 3-way redundancy.

### Oral questions to be ready for

1. When the instructor deleted the pod, its PVC survived. Show where that data lives on the kind node and explain what would have happened instead if you had run `kubectl delete pvc` too.
2. Your replica cloned the primary with `mysqldump` on first start. Why doesn't it re-clone after the pod is restarted, and what exact condition in your init logic prevents it?
3. During your failover, `Seconds_Behind_Source` was non-zero on one replica. How did you choose which replica to promote, and what would you have lost if you had picked the other one?
4. Why must the replicas point at `mysql-0.mysql-h` and not at the `mysql-read` Service? What would actually break if you used `mysql-read` as the replication source?
5. After promotion, the StatefulSet recreated `mysql-0` with its old data and old primary config. Why is that dangerous, and what does your runbook do about it?

### Pass bars

- `bootstrap.sh` from a clean clone to 3 Ready pods with verified replication in 15 minutes or less, with `<studentID>` in the namespace name and in the seeded rows.
- Whichever pod the instructor kills, whenever they kill it, you recover using only commands that appear in your committed `runbook.md`.
- Zero committed rows lost after failover, demonstrated live with the sequence-number comparison - not asserted, shown.
- If the primary is the victim, promotion completes and writes succeed against the new primary within 10 minutes of the kill.
- You can explain every replication and init-container command you ran; running the reference scripts without being able to explain them is a fail.

---

## Project 2 - MongoDB replica set

**Goal.** Build a 3-member MongoDB replica set on kind using a StatefulSet and a headless Service, initialized with stable DNS names so members find each other after any restart. The live demo proves automatic failover: the instructor picks a member, inserts a marker document seconds before you kill it, and that document must be readable on the new primary after election - with zero data loss.

### What you will learn

- Why databases need StatefulSets (stable pod names, stable DNS, per-pod storage) instead of Deployments.
- How headless Services and per-pod DNS records (`<pod>.<svc>.<ns>.svc.cluster.local`) enable peer discovery.
- How MongoDB replica set elections work and how to read `rs.status()` under pressure.
- What `writeConcern: majority` guarantees, and what a `w: 1` write can lose during failover.
- How PVC-to-pod binding preserves data when a StatefulSet pod is deleted and recreated.

### Environment

- kind cluster with 1 control-plane and 2 workers, defined in `kind-config.yaml` in your repo, so the three mongo pods can spread across nodes.
- Image: official `mongo:7` from Docker Hub (pin the tag; no custom image required - if you build one for init scripts, push it to your own Docker Hub/GHCR account).
- Tooling: only what the course used - `kind`, `kubectl`, `docker`. All mongo commands run via `kubectl exec ... -- mongosh`.
- Namespace: `mongo-<studentID>` (e.g. `mongo-jsmith12`). Every resource lives in it.

### Build requirements

1. Create namespace `mongo-<studentID>`; all objects below go in it.
2. Create a headless Service named `mongo-h` (`clusterIP: None`) selecting the mongo pods, exposing port 27017. Also create a regular ClusterIP Service `mongo-read` for client access.
3. Create a StatefulSet named `mongo` with `serviceName: mongo-h`, 3 replicas, image `mongo:7`, started with `--replSet rs0 --bind_ip_all`.
4. Use `volumeClaimTemplates` so each pod gets its own PVC (`data-mongo-0/1/2`) from the kind `standard` StorageClass, at least 1Gi, mounted at `/data/db`.
5. Initialize the replica set with `rs.initiate()` listing the three stable DNS names exactly: `mongo-0.mongo-h.mongo-<studentID>.svc.cluster.local:27017`, and the same for `mongo-1` and `mongo-2`. This may be a script in `scripts/` invoked by bootstrap.sh, or a one-shot init Job - either way it must be in git and idempotent (safe to re-run).
6. Add liveness and readiness probes to the StatefulSet (a `mongosh --eval "db.adminCommand('ping')"` exec probe is acceptable).
7. Seed data: create database `clo835`, collection `students`, and insert at least 10 documents each containing your student ID, e.g. `{ sid: "<studentID>", seq: 1, note: "seed" }`. Seeding must use `writeConcern: { w: "majority" }` and run from bootstrap.sh.
8. Write a `scripts/insert.sh` helper that takes a message argument and inserts `{ sid: "<studentID>", marker: "<message>", ts: new Date() }` with `w: "majority"` into the current primary. The instructor will use this during the twist.
9. Parameterize your student ID: it must appear only once in bootstrap.sh (or a single vars file) and be substituted into the namespace and seed data - no hardcoding it in ten places.
10. `bootstrap.sh` must go from a clean host (no kind cluster) to a fully initialized, seeded, 3-member replica set with an elected primary in under 15 minutes, and finish by printing `rs.status()` member states.
11. Everything in git: `kind-config.yaml`, all manifests under `manifests/`, all scripts under `scripts/`, `bootstrap.sh`, `runbook.md`. No unmanaged `kubectl create` by hand.
12. Do not use Helm, operators, or anything beyond raw YAML + kubectl.

### Runbook you must write

- How to bootstrap from a clean host: `./bootstrap.sh` and what output confirms success.
- How to find the current primary: `kubectl exec` + `rs.status()` / `rs.hello()`, and how to read `stateStr`, `health`, and `optime` in the output.
- How to insert a marker document with majority write concern: `scripts/insert.sh "<message>"` and the underlying `mongosh` command.
- How to kill any named member: `kubectl delete pod mongo-N -n mongo-<studentID>` and how to watch the election (`kubectl get pods -w`, repeated `rs.status()` from a survivor).
- How to verify data survived: count seed documents and find the marker document on the new primary, plus verify it replicated to a secondary using `db.getMongo().setReadPref('secondary')` or `readPreference`.
- How to prove PVC reattachment: show `kubectl get pvc` before and after a pod kill and that the recreated pod reuses its claim.
- How to tear down and rebuild: `kind delete cluster` then re-bootstrap.

### Submission

- Repo layout: `manifests/` (namespace, services, statefulset), `scripts/` (init, seed, insert.sh), `kind-config.yaml`, `bootstrap.sh`, `runbook.md`, `evidence/` (optional pre-demo terminal captures; the demo itself is live).
- Submission = the final commit hash. You present immediately after submitting, in the same session, from exactly that commit - `git clone` or `git checkout` it on your host in front of the instructor. No edits, no un-committed files, no "one small fix".

### Presentation (starts right after you submit)

1. Clone/checkout the frozen commit on your EC2/Cloud9 host and run `./bootstrap.sh`. While it runs, walk through the StatefulSet and headless Service YAML and explain the three DNS names in `rs.initiate()`.
2. Show `rs.status()`: identify the primary, the two secondaries, and explain `stateStr`, `health`, and why member hostnames match `<pod>.mongo-h.<ns>.svc.cluster.local`.
3. Show the seed data: count the documents and show your student ID inside them.
4. **Twist.** The instructor names the victim pod (any of mongo-0/1/2 - often the current primary, but their choice) and dictates a marker string (e.g. their initials + time). You run `scripts/insert.sh "<their string>"` with majority write concern, then immediately `kubectl delete pod <victim>` - no more than a few seconds between insert and kill.
5. Watch live: `kubectl get pods -w` in one pane, repeated `rs.status()` from a surviving member in another. Narrate the election as it happens and identify the new primary.
6. On the new primary, find the instructor's marker document and show the full seed count is intact. Zero lost documents.
7. Show the killed pod come back, rejoin as a secondary, and catch up (`optime` converging); show its PVC was reused, not recreated.
8. Answer: what would have happened to the marker if it had been written with `w: 1`? Demonstrate or explain using this cluster.

### Oral questions to be ready for

1. During your failover, roughly how long did the election take, and which timeout in the replica set config governs when an election starts?
2. If the instructor had picked a secondary as the victim instead of the primary, what would `rs.status()` have shown and would any election have occurred? What did you actually observe when you tested that?
3. Your `rs.initiate()` used full DNS names through `mongo-h`. What breaks if you initiate with pod IPs instead, and when exactly would you find out?
4. The marker was written with `w: "majority"`. Walk through where that write physically was (which pods' disks) at the moment the primary died.
5. mongo-1 comes back after the kill and shows `STARTUP2` then `SECONDARY`. What is it doing in that window, and where is the data coming from?

### Pass bars

- `bootstrap.sh` produces a healthy 3-member replica set with an elected primary from a clean host in 15 minutes or less.
- The instructor's marker document, inserted seconds before the kill, is readable on the new primary - along with all seed documents. Zero lost writes.
- Election completes and the student identifies the new primary from `rs.status()` without help.
- The killed pod rejoins as a secondary with its original PVC; the student proves the claim was reused.
- Student ID appears in the namespace name and inside the stored documents shown live.

---

## Project 3 - PostgreSQL streaming replication

**Goal.** Build a two-instance PostgreSQL cluster in kind - a primary and a hot standby - wired together with streaming replication. The standby is seeded from the primary with `pg_basebackup` and follows the WAL stream via `primary_conninfo`. In the live demo you prove the standby is replicating (and measure how far behind it is), then promote it to a full read-write primary while the instructor is actively writing rows, and account for exactly which rows survived the promotion window and why.

### What you will learn

- How PostgreSQL streaming replication actually works: WAL shipping, `primary_conninfo`, replication slots, and the difference between a standby that replays WAL and a primary that generates it.
- How to run stateful, non-identical database roles on Kubernetes using StatefulSets, headless services, and stable pod DNS names.
- How to measure replication lag with `pg_stat_replication` (on the primary) and `pg_last_wal_replay_lsn()` (on the standby), and what an LSN is.
- What promotion does (`pg_ctl promote`), why it is one-way, and what happens to in-flight writes during a failover.
- Why "the standby is up" and "the standby has your data" are different claims, and how to prove the second one.

### Environment

- kind cluster with 1 control-plane + 2 workers, defined in `kind-config.yaml` (checked into git). Primary and standby must land on different worker nodes - use pod anti-affinity or `nodeSelector` on node labels you apply in `bootstrap.sh`.
- Image: official `postgres:16` from Docker Hub (or a derived image you build and push to your own Docker Hub/GHCR repo if you bake in config - no other images).
- Storage: the kind default `standard` StorageClass (local-path) via `volumeClaimTemplates`. One PVC per pod.
- No extra tooling beyond `kubectl`, `psql` inside the pods (`kubectl exec`), and `watch`. No operators, no Helm.
- Namespace: `pg-<studentID>` (e.g. `pg-jsmith12`). Every resource lives in it.

### Build requirements

1. Create namespace `pg-<studentID>`. All object names below carry your student ID where shown.
2. Create a StatefulSet `pg-primary-<studentID>` (replicas: 1) and a StatefulSet `pg-standby-<studentID>` (replicas: 1). Two single-replica StatefulSets, not one two-replica set - the roles are asymmetric and you must be able to promote the standby without touching the primary.
3. Create two headless Services, `pg-primary-hs` and `pg-standby-hs`, so each pod has a stable DNS name (e.g. `pg-primary-<studentID>-0.pg-primary-hs.pg-<studentID>.svc.cluster.local`). Also create a ClusterIP Service `pg-write` selecting the primary - this is what "clients" connect to.
4. Configure the primary for replication: `wal_level = replica`, `max_wal_senders >= 3`, a replication role `repl` (password from a Secret, see req. 8), and a `pg_hba.conf` entry permitting replication connections from the pod network. Configuration must come from a ConfigMap, not be typed into a running pod.
5. Seed the standby with `pg_basebackup`. Use an initContainer on the standby pod that runs `pg_basebackup -h pg-primary-<studentID>-0.pg-primary-hs... -U repl -D /var/lib/postgresql/data/pgdata -R -X stream` when the data directory is empty (the `-R` flag writes `standby.signal` and `primary_conninfo` for you). The initContainer must be idempotent: skip the copy if `pgdata` already exists.
6. Seed the primary with data stamped with your ID: a database `clo835`, a table `events_<studentID>(id serial, tag text, created_at timestamptz default now())`, and at least 20 rows whose `tag` values contain `<studentID>`. Seeding runs from `bootstrap.sh` via `kubectl exec` or a one-shot Job `pg-seed-<studentID>` - either way it must be in git.
7. Prove replication is streaming: after bootstrap, `SELECT state, sync_state, replay_lsn FROM pg_stat_replication;` on the primary must show one `streaming` standby.
8. Store the postgres superuser password and the `repl` password in a Secret `pg-creds-<studentID>`. No passwords in manifests or in the repo history.
9. Parameterize the student ID: `bootstrap.sh` takes it as `$1` (or reads `STUDENT_ID`) and substitutes it into namespace, object names, and seed rows (e.g. `sed` over manifest templates). Grading uses a fresh ID-stamped run, so hardcoding fails.
10. Everything in git: `kind-config.yaml`, all manifests under `manifests/`, `bootstrap.sh`, `runbook.md`. `bootstrap.sh` must go from a clean host (no cluster) to "replication streaming + rows seeded" in under 15 minutes with zero manual steps.
11. Write a script or documented one-liner `lag-check` in the runbook that prints, side by side: primary `pg_current_wal_lsn()`, standby `pg_last_wal_replay_lsn()`, and the byte difference via `pg_wal_lsn_diff()`.
12. Promotion must work two ways and both must be in the runbook: `pg_ctl promote` executed inside the standby pod, and the trigger-file alternative (`promote_trigger_file` / `pg_promote()`). You demo one; be ready to explain the other.

### Runbook you must write

- How to bootstrap from nothing: `./bootstrap.sh <studentID>` and what "healthy" looks like afterward (`kubectl get pods,pvc -n pg-<studentID>`, the `pg_stat_replication` check).
- How to check replication lag: the exact `psql` queries on both pods (`pg_current_wal_lsn()`, `pg_last_wal_replay_lsn()`, `pg_wal_lsn_diff()`, `pg_stat_replication.replay_lsn`) and how to read the output.
- How to generate write load on the primary: a loop that inserts timestamped rows into `events_<studentID>` (e.g. `kubectl exec ... -- psql -c "INSERT ..."` in a `while` loop) so lag becomes visible.
- How to verify the standby is read-only: attempt an `INSERT` on the standby and show the `cannot execute INSERT in a read-only transaction` error.
- How to promote the standby: `kubectl exec pg-standby-<studentID>-0 -- pg_ctl promote -D <pgdata>`, how to confirm with `SELECT pg_is_in_recovery();` (must flip to `f`), and the trigger-file alternative.
- How to repoint clients: patch the `pg-write` Service selector to the standby's labels (`kubectl patch svc pg-write ...`) and prove writes land on the new primary.
- How to count and reconcile rows after promotion: `SELECT count(*), max(id) FROM events_<studentID>;` on both instances and how to identify rows that never reached the standby.
- How to tear down and rebuild: `kind delete cluster` + re-run bootstrap.

### Submission

- Repo layout:
 - `manifests/` - all YAML (namespace, ConfigMaps, Secret template, headless Services, `pg-write` Service, both StatefulSets, seed Job)
 - `kind-config.yaml`
 - `bootstrap.sh`
 - `runbook.md`
 - `evidence/` - terminal transcripts from your own dry runs (bootstrap timing, lag check, a practice promotion)
- Submission = the final commit hash. You present immediately after submitting, in the same session, from exactly that commit. No edits, no "one small fix" - if bootstrap fails live, that is the grade.

### Presentation (starts right after you submit)

1. On a clean host, run `./bootstrap.sh <yourID>` and narrate while it builds. When it finishes, show `kubectl get pods -n pg-<studentID> -o wide` (pods on different workers) and the `pg_stat_replication` query showing `streaming`.
2. Show the seeded data on the primary, including your ID inside the rows: `SELECT * FROM events_<studentID> LIMIT 5;`. Run the same query on the standby to prove it replicated.
3. Prove the standby is read-only (failed `INSERT`), then run your lag check while your write loop hammers the primary - show the LSN gap moving.
4. **Instructor twist.** The instructor takes your keyboard (or dictates) and starts their own insert loop with a tag *they* choose on the spot (e.g. `tag = 'prof-<word>-<n>'`) at a rate they choose. While their rows are flowing, they tell you *when* to promote - possibly with the primary still up, possibly after they kill the primary pod (`kubectl delete pod pg-primary-<studentID>-0`); their call, live. You cannot rehearse the tag, the timing, or the failure mode.
5. Promote the standby (`pg_ctl promote`), confirm `pg_is_in_recovery()` returns `f`, and repoint the `pg-write` Service to it.
6. Reconcile: count the instructor's rows on the promoted node vs. what their loop reported sending (or vs. the old primary's table if it still exists). State exactly how many made it and how many were lost.
7. Explain why: asynchronous replication means rows committed on the old primary but not yet replayed on the standby at promotion time are gone from the new timeline - walk through it using the last LSN numbers from your lag check.
8. Insert a new row tagged `<studentID>-post-promo` on the promoted node to prove it accepts writes, then answer oral questions.

### Oral questions to be ready for

1. Your lag check showed a nonzero LSN gap even when no one was writing - what causes that, and what did the gap look like in bytes during the instructor's write burst?
2. The old primary pod is still running after you promoted the standby. What happens if a client writes to it now, and how would you prevent that split-brain in this setup?
3. Why did you use an initContainer with `pg_basebackup` instead of just letting the standby's postgres start with an empty data directory? What happens on standby pod restart - does it re-copy?
4. If you set `synchronous_commit = on` with a synchronous standby, which of the instructor's rows would have been lost instead, and what would the instructor's insert loop have experienced?
5. Your standby's PVC survived the pod being deleted. Show or explain how you verified it re-attached, and what would have gone wrong if the initContainer weren't idempotent.

### Pass bars

- `bootstrap.sh` reaches "replication streaming, seed rows visible on the standby" from a clean host in under 15 minutes, unattended.
- Replication lag is demonstrated with real LSN numbers from `pg_stat_replication` and `pg_wal_lsn_diff()`, under write load - not just "it says streaming".
- Promotion succeeds live: `pg_is_in_recovery()` flips to `f`, and the promoted node accepts a write within 2 minutes of the instructor's signal.
- The accounting of the instructor's rows is exact - a stated number that made it, a stated number that did not, and a correct explanation tied to WAL replay position. "Some rows were lost" without numbers fails.
- Student ID appears in the namespace, the StatefulSet names, the table name, and the row data, generated by the parameterized bootstrap - not hand-edited.

---

## Project 4 - Redis with Sentinel

**Goal.** Build a self-healing Redis deployment in kind: one master, two replicas, and three Sentinel processes that watch the master and automatically promote a replica when the master dies. The live demo proves that a client writing data through Sentinel discovery survives the master being killed mid-write, that the takeover happens automatically within your tuned failover window, and that you can explain exactly why quorum math changes when a Sentinel itself dies.

### What you will learn

- How Redis replication (master/replica) works and how Sentinel monitors it, detects failure, and elects a new master.
- Why quorum exists, what `sentinel monitor ... 2` means with 3 Sentinels, and what breaks when Sentinels die.
- How clients are supposed to find the current master (ask Sentinel, never hardcode the master's address).
- How StatefulSets, headless services, and stable DNS names make peer discovery possible in Kubernetes.
- How to tune `down-after-milliseconds` and `failover-timeout` and measure real failover time.

### Environment

- kind cluster with 1 control-plane + 2 worker nodes, defined in `kind-config.yaml` committed to your repo.
- Images: `redis:7-alpine` (or another pinned redis:7 tag) from Docker Hub for both Redis and Sentinel - Sentinel is the same image started with `redis-sentinel`. No custom images required; if you build one (e.g., for the writer client), push it to Docker Hub or GHCR from GitHub Actions.
- Tooling: `kubectl`, `kind`, `docker` only. `redis-cli` runs inside the pods - do not install it on the host.
- Namespace: `redis-<studentID>` (e.g., `redis-mjafari3`). Every resource lives in it.

### Build requirements

1. Create namespace `redis-<studentID>`. All object names below live in it.
2. Create a StatefulSet `redis-<studentID>` with 3 replicas (pods `redis-<studentID>-0/-1/-2`) and a headless Service `redis-hl` so each pod has a stable DNS name (`redis-<studentID>-0.redis-hl.redis-<studentID>.svc.cluster.local`). Pod `-0` starts as master; `-1` and `-2` start with `replicaof` pointing at `-0`'s DNS name. Use an initContainer or startup script (mounted from a ConfigMap) to decide master vs replica by pod ordinal - no hand-editing after `kubectl apply`.
3. Create a separate StatefulSet (or Deployment - pick one and justify it in the runbook) `sentinel-<studentID>` with 3 replicas running `redis-sentinel /etc/sentinel/sentinel.conf`, plus a Service `sentinel-svc` on port 26379.
4. Sentinel configuration must come from a ConfigMap `sentinel-config-<studentID>` and must contain exactly: `sentinel monitor mymaster-<studentID> <master-dns-or-ip> 6379 2` (quorum 2), a tuned `sentinel down-after-milliseconds mymaster-<studentID> 5000`, `sentinel failover-timeout mymaster-<studentID> 15000`, and `sentinel parallel-syncs mymaster-<studentID> 1`. Sentinel rewrites its own config file, so copy it from the ConfigMap mount to a writable `emptyDir` at startup - a read-only mount will fail. Show this in the manifest.
5. Seed data at bootstrap: a Job or script writes at least 50 keys of the form `<studentID>:seed:<n>` into the master, plus a key `owner` whose value is `<studentID>`. `GET owner` on any replica must return your ID.
6. Provide a writer: a small pod or `kubectl exec` loop (`writer.sh` in the repo) that writes `<studentID>:live:<counter>` once per second and prints each write with a timestamp. It must discover the master by asking Sentinel (`SENTINEL get-master-addr-by-name mymaster-<studentID>`), not by hardcoding `redis-<studentID>-0`.
7. Set replica read-only (default) and prove writes to a replica are rejected (`READONLY You can't write against a read only replica`).
8. Parameterize student ID: `<studentID>` must not be hand-typed in 12 places. Use a single variable in `bootstrap.sh` that generates or substitutes into the manifests (e.g., `envsubst` or `sed` into a `manifests/rendered/` directory).
9. `bootstrap.sh` must, from a clean host: create the kind cluster from `kind-config.yaml`, apply all manifests, wait for readiness (`kubectl rollout status` / `kubectl wait`), run the seed Job, and finish in under 15 minutes.
10. Everything in git: `kind-config.yaml`, all YAML manifests, ConfigMaps, `bootstrap.sh`, `writer.sh`, `runbook.md`. GitHub Actions (if you build any image) only builds and pushes - it never touches the cluster.

### Runbook you must write

- How to bootstrap from nothing: `./bootstrap.sh <studentID>` and the `kubectl get pods -n redis-<studentID> -w` output that indicates success.
- How to identify the current master: `kubectl exec` into a sentinel pod and run `redis-cli -p 26379 SENTINEL get-master-addr-by-name mymaster-<studentID>`, and the cross-check `redis-cli INFO replication` on a redis pod.
- How to start the write loop: `./writer.sh` (or the writer pod logs) and how to read its output.
- How to watch a failover live: `kubectl logs -f` on a sentinel pod, and which log lines to point at (`+sdown`, `+odown`, `+vote-for-leader`, `+switch-master`).
- How to verify data after failover: count `<studentID>:live:*` keys on the new master, compare against the writer's last printed counter, and explain any gap.
- How to check Sentinel quorum health: `SENTINEL ckquorum mymaster-<studentID>` and `SENTINEL master mymaster-<studentID>` (fields `num-other-sentinels`, `quorum`, `flags`).
- How to recover the killed pod and confirm it rejoins as a replica of the NEW master, not as a second master.

### Submission

- Repo layout: `manifests/` (all YAML + `kind-config.yaml`), `bootstrap.sh`, `writer.sh`, `runbook.md`, `evidence/` (bootstrap timing log and one full failover log capture from a practice run).
- Submission = the final commit hash. You present immediately after submitting, in the same session, from a fresh clone of exactly that commit on your own host. No edits, no `git pull`, no "one small fix".
- The repo must contain no secrets and no hardcoded IPs that only exist on your machine.

### Presentation (starts right after you submit)

1. Fresh clone of the frozen commit; run `./bootstrap.sh <studentID>`. While it runs, walk through your Sentinel ConfigMap and explain quorum 2 and your `down-after-milliseconds` choice.
2. Show the topology: `kubectl get pods -o wide -n redis-<studentID>`, then `SENTINEL get-master-addr-by-name` to name the current master. Show `GET owner` returns your student ID from a replica.
3. Prove a replica rejects writes (attempt a `SET` on a replica, show the READONLY error).
4. Start the write loop (`./writer.sh`) in one terminal; in a second terminal, `kubectl logs -f` a sentinel pod.
5. **Twist part 1:** the instructor picks the moment and the method - `kubectl delete pod <current-master> --grace-period=0 --force`, or `kubectl exec ... redis-cli DEBUG SLEEP 60`, or draining the node the master runs on. You do not know which. Narrate the sentinel log lines live: `+sdown` → `+odown` → leader election → `+switch-master`.
6. Show the writer recovering: it re-queries Sentinel, resumes writing to the new master. Count `<studentID>:live:*` keys, compare to the writer's counter, and state exactly how many writes (if any) were lost in the failover window and why.
7. Show the old master's pod come back and rejoin as a replica of the new master (`INFO replication` on it).
8. **Twist part 2:** the instructor picks ONE sentinel pod and deletes it (their choice of which, and whether the controller is allowed to restart it - they may scale your sentinel workload to 2). Answer live: what is quorum now, can `+odown` still be declared, can a failover still be *authorized* (majority of the original Sentinel count), and prove your answer with `SENTINEL ckquorum mymaster-<studentID>`.

### Oral questions to be ready for

1. Your writer lost N rows during the failover - walk through the exact timeline (down-after-milliseconds, election, +switch-master) and say which of those milliseconds each lost write fell into.
2. With 3 Sentinels and quorum 2, one Sentinel just died. Quorum for `+odown` still needs 2 - but why does failover *authorization* care about majority of all known Sentinels rather than the quorum number, and what happens if a second Sentinel dies?
3. Why did you copy sentinel.conf from the ConfigMap into an emptyDir instead of mounting it directly, and what did you observe when you tried the direct mount?
4. The old master came back - what stops it from accepting writes as a second master, and where in Sentinel's log or config is that recorded?
5. If your writer had hardcoded `redis-<studentID>-0` instead of asking Sentinel, exactly what would the demo have shown after the twist, and why doesn't a ClusterIP Service in front of all three redis pods solve it?

### Pass bars

- `bootstrap.sh` from a clean clone to seeded, sentinel-monitored cluster in under 15 minutes, unattended.
- Failover completes automatically (no kubectl or redis-cli intervention on your part) and the writer resumes within 30 seconds of the master being killed.
- You can name the number of lost writes and account for the failover window; "I don't know if data was lost" is a fail.
- After twist part 2 you correctly state the new quorum situation and prove it with `SENTINEL ckquorum` before being told the answer.
- Student ID present in the namespace, the master name (`mymaster-<studentID>`), and the stored data (`owner` key and key prefixes), verified live.

---

## Project 5 - Backup and restore lifecycle

**Goal.** Build a MySQL database in kind whose contents grow all semester with dated seed rows, protected by a CronJob that takes timestamped compressed dumps to a PVC and keeps only the last 7. On demo day the instructor picks one of your backups (not the newest one) and you must state - before running the restore - exactly which rows will be missing afterward. The live demo proves you understand that a backup is a point in time, not a safety blanket: you can reason about what any given backup contains, restore it correctly, and show the predicted data loss and nothing else.

### What you will learn

- How Kubernetes CronJobs schedule, run, and clean up batch work, and how `kubectl create job --from=cronjob/...` triggers a run on demand.
- How to share a PVC between a database workload and backup/restore Jobs, and why access modes and mount paths matter.
- How `mysqldump` and `mysql` restore behave inside containers: piping through `gzip`, exit codes, and idempotent restores with `--databases`/`DROP TABLE`.
- Retention logic in shell (`ls -1t | tail -n +8 | xargs rm`) and why "keep last 7" is a policy you must prove, not assume.
- Point-in-time reasoning: mapping a backup's timestamp to the exact set of rows it does and does not contain.

### Environment

- kind cluster from a committed config file: 1 control-plane + 1 worker (`kind-config.yaml` in the repo). Cluster name `backup-<studentID>`.
- Namespace: `proj5-<studentID>`. Every resource name carries `<studentID>` where noted below.
- Images: `mysql:8.0` from Docker Hub for the database, CronJob, and restore Job (the mysql image already contains `mysqldump`, `mysql`, `gzip`, and a shell - no custom image required, but you may build and push your own to Docker Hub/GHCR if you prefer).
- Storage: kind's built-in `standard` StorageClass (local-path). No NFS needed.
- Tooling on the host: docker, kind, kubectl, git. Nothing else.

### Build requirements

1. Create namespace `proj5-<studentID>`. All objects live in it.
2. Deploy MySQL as a single-replica Deployment (or single-pod StatefulSet) named `mysql-<studentID>`, with a PVC `mysql-data-<studentID>` (`standard` StorageClass, 1Gi) mounted at `/var/lib/mysql`. Root password comes from a Secret `mysql-secret-<studentID>` - never hard-coded in the pod spec.
3. Expose MySQL inside the cluster with a ClusterIP Service named `mysql-<studentID>` on port 3306. Backup and restore Jobs must reach the database by this Service DNS name, not by pod IP.
4. Create a second PVC `backup-<studentID>` (1Gi) that holds only backups. The CronJob and the restore Job both mount it at `/backups`. The database pod does NOT mount it - a backup on the same volume as the data it protects is worthless.
5. Seed schema and data via a ConfigMap `seed-sql-<studentID>` applied by an initContainer or a one-shot seed Job: database `clo835db`, table `records(id INT AUTO_INCREMENT PRIMARY KEY, student_id VARCHAR(20), note VARCHAR(100), added_on DATE)`. Every row's `student_id` column contains your actual `<studentID>`.
6. Across the term, insert at least one dated row per week (`note` like `week05-entry`, `added_on` = real date). Each week, run a manual dump and commit it to `evidence/weekly-dumps/` in git. The git commit dates on those files are your proof the data grew over time - a table seeded the night before the demo fails this requirement.
7. Create a CronJob `backup-<studentID>` with `schedule: "*/5 * * * *"`. Each run executes: `mysqldump -h mysql-<studentID> ... clo835db | gzip > /backups/mysql-<studentID>-$(date +%Y%m%d-%H%M%S).sql.gz`, then rotation: `cd /backups && ls -1t mysql-<studentID>-*.sql.gz | tail -n +8 | xargs -r rm --`. A failed dump must not delete anything (`set -e` before rotation, or check the dump's exit code).
8. Set `successfulJobsHistoryLimit: 3` and `failedJobsHistoryLimit: 3` on the CronJob so `kubectl get jobs` stays readable during the demo.
9. Write a restore Job manifest `manifests/restore-job.yaml` parameterized by backup filename - the filename appears exactly once, as an env var `BACKUP_FILE`, so it can be swapped with `sed` or an env edit in seconds. The Job runs `gunzip -c /backups/$BACKUP_FILE | mysql -h mysql-<studentID> ... clo835db` after dropping/recreating the table so the restore is exact, not a merge.
10. `bootstrap.sh` at repo root stands up everything from a clean host: creates the kind cluster from `kind-config.yaml`, applies all manifests in order, waits for MySQL readiness (`kubectl wait` or a readiness loop), loads the seed data including your committed historical rows, and triggers one immediate backup with `kubectl create job --from=cronjob/backup-<studentID>`. Total wall time under 15 minutes.
11. Everything is raw YAML in `manifests/`, applied with `kubectl apply`. No Helm, no kustomize overlays required, no operators.
12. All manifests, `bootstrap.sh`, `runbook.md`, seed SQL, and weekly dump evidence are committed to your GitHub repo.

### Runbook you must write

- How to bootstrap from nothing: `./bootstrap.sh`, plus the verification commands that prove the cluster, MySQL, and CronJob are healthy (`kubectl get pods,pvc,cronjob -n proj5-<studentID>`).
- How to list current backups newest-first with timestamps: the exact one-liner using a helper pod or `kubectl exec` / `kubectl run` mounting `backup-<studentID>` and running `ls -1t /backups`.
- How to trigger an immediate backup: `kubectl create job --from=cronjob/backup-<studentID> manual-backup-1 -n proj5-<studentID>` and how to watch it complete (`kubectl logs job/manual-backup-1`).
- How to inspect what rows a given backup contains WITHOUT restoring it: `gunzip -c` the file and grep the INSERT lines (this is what powers your prediction).
- How to insert a new dated row into the live database: the `kubectl exec ... mysql -e "INSERT ..."` command.
- How to run the restore Job against a named backup: edit/`sed` `BACKUP_FILE` in `restore-job.yaml`, `kubectl apply`, watch logs, then verify with a `SELECT`.
- How to prove rotation: the command sequence showing 7 files before a backup run, 7 files after (oldest gone, newest added).
- How to tear down and rebuild if something goes wrong mid-demo: `kind delete cluster --name backup-<studentID> && ./bootstrap.sh`.

### Submission

- Repo layout:
 - `manifests/` - all YAML (namespace, secret, PVCs, MySQL deployment + service, seed ConfigMap/Job, CronJob, restore Job template)
 - `bootstrap.sh` - full stand-up from a clean host, executable, idempotent enough to re-run
 - `runbook.md` - every procedure above with exact commands
 - `evidence/weekly-dumps/` - one committed `.sql` or `.sql.gz` per week of the term, real commit dates
 - `kind-config.yaml`, `README.md`
- Submission = the final commit hash. You present immediately after submitting, in the same session, from a checkout of exactly that commit on your own host. No edits, no "one small fix" after the hash is frozen. If the demo needs a file, it is already in the repo.

### Presentation (starts right after you submit)

1. Clone your frozen commit into a fresh directory, run `./bootstrap.sh`, and narrate while it builds. Show `git log --oneline evidence/weekly-dumps/` to prove the semester-long data timeline.
2. Show the running system: `kubectl get pods,pvc,cronjob,svc -n proj5-<studentID>`, then `SELECT * FROM records ORDER BY added_on` to display all dated rows containing your `<studentID>`.
3. Build backup history live: insert a new row (`note='demo-row-1'`), trigger a manual backup; insert `demo-row-2`, trigger another; let the CronJob fire or trigger a third. List `/backups` - at least 7 files exist (bootstrap + term dumps loaded + demo runs); prove rotation by showing the count stays at 7 and the oldest file disappeared after the newest run.
4. **TWIST - instructor's choice.** The instructor looks at your `ls -1t /backups` output and names ONE backup file to restore - the brief says N-2, but they may pick any of the seven, so nothing can be rehearsed exactly. They may also insert one extra row of their choosing first.
5. **Prediction first.** Before touching the restore Job, state out loud and type into a file (`evidence/prediction.txt`) exactly which rows will be ABSENT after the restore - by `note` value - reasoning only from the backup file's timestamp versus each row's insertion time. You may inspect the dump with `gunzip -c | grep INSERT` to confirm, but the prediction must be committed to the terminal before the restore runs.
6. Run the restore: set `BACKUP_FILE` to the instructor's chosen file, apply `restore-job.yaml`, show the Job logs completing cleanly.
7. Verify: `SELECT * FROM records ORDER BY added_on`. Walk the instructor through the output row by row against your prediction. Every predicted-missing row is gone; every predicted-present row survives; zero surprises.
8. Close the loop: trigger one more backup of the restored state, show it lands in `/backups`, and show rotation still holds at 7 files.

### Oral questions to be ready for

1. Your CronJob fires every 5 minutes. During your demo a backup Job was still running when you triggered a manual one - what happens, and what does `concurrencyPolicy` do about it in your spec?
2. The rotation line is `ls -1t | tail -n +8 | xargs rm`. Walk through exactly what each stage outputs when there are 9 files. What happens if the dump command fails *before* rotation runs, and how does your script prevent deleting good backups after a failed dump?
3. Why does your backup PVC have to be a different PVC from the MySQL data PVC? Demonstrate the failure mode you'd get on demo day if it weren't - what happens to your backups when the MySQL PVC is deleted?
4. Your restore drops the table before loading the dump. What would the `records` table look like after the restore if you skipped the drop and just piped the dump in? Show the specific duplicate/conflict behavior with your schema.
5. The instructor picked backup N-2, but between N-2 and now the CronJob ran twice more. After your restore, what do the NEWER backup files N-1 and N contain - the restored state or the pre-restore state? How would you get back to the pre-restore data if the instructor asked you to right now?

### Pass bars

- `bootstrap.sh` produces a working cluster, seeded database, and first backup from a clean host in under 15 minutes, from the frozen commit, with no manual fixes.
- Rotation provably holds: never more than 7 backup files on the PVC, demonstrated live with a before/after listing.
- Prediction is exact: the post-restore `SELECT` matches your stated missing-row list with zero discrepancies - one unpredicted missing or surviving row is a fail on the twist.
- The restore Job completes and the database is queryable in under 5 minutes from the instructor naming the file.
- Semester timeline is real: weekly dumps in `evidence/weekly-dumps/` with authentic git commit dates spanning the term, and every data row carries your `<studentID>`.

---

## Project 6 - Two-cluster data migration

**Goal.** Build a seeded MySQL (or PostgreSQL) database with a small web app in front of it on kind cluster `a`, then migrate the data live to a freshly created kind cluster `b` on the same host - freeze writes, dump with a Kubernetes Job, transfer the dump through the host filesystem, restore with a Job on cluster `b`, and cut the app over. The live demo proves zero data loss (row counts and SHA256 checksums match on both sides), that surprise rows the instructor inserts 30 minutes before cutover survive the migration, and that measured downtime stays within your declared window.

### What you will learn

- Operating two independent kind clusters on one host and switching between them with kubectl contexts (`kind-a`, `kind-b`).
- Designing a write-freeze: why you must stop writes before dumping, and how to do it with `kubectl scale` (or an SQL `REVOKE`).
- Using Kubernetes Jobs for one-shot operational work (dump, restore) instead of `kubectl exec` improvisation.
- Verifying data integrity with deterministic, ordered dumps and SHA256 checksums instead of "it looks fine".
- Measuring real downtime with a probe loop rather than guessing.

### Environment

- Two kind clusters on your single EC2/Cloud9 host: `kind create cluster --name a` and `kind create cluster --name b` (single-node each is fine; contexts `kind-a` and `kind-b`). Cluster `b` may be created during the demo - bootstrap timing includes it.
- Database: official `mysql:8` or `postgres:16` image from Docker Hub. App: a small HTTP app (your own image on Docker Hub/GHCR, or a scripted `nginx`/`httpd` variant) that reads from the DB and serves a page including a row count and your student ID.
- Namespace on both clusters: `migrate-<studentID>`.
- Extra tooling on the host: only `sha256sum`, `curl`, `docker`, `kind`, `kubectl` - all already taught or preinstalled.

### Build requirements

1. Write `manifests/a/` containing, for cluster `a`: namespace `migrate-<studentID>`, a Secret `db-credentials-<studentID>` for DB passwords, a ConfigMap holding the schema + seed SQL, a DB Deployment `db-<studentID>` (1 replica) with a PVC `db-data-<studentID>` (kind `standard` StorageClass), a ClusterIP Service `db-<studentID>`, an app Deployment `app-<studentID>` (2 replicas), and a NodePort Service `app-<studentID>` reachable from the host.
2. Seed the database at bootstrap with a table `records` containing at least 500 rows; every row's payload column must embed `<studentID>` (e.g. `seed-<studentID>-000123`). Seeding must happen automatically (init Job or entrypoint SQL from the ConfigMap), not by hand.
3. Write `manifests/b/` for cluster `b`: same namespace, Secret, DB Deployment/PVC/Service, app Deployment/Service - but no seed data. Cluster `b` starts empty.
4. Write `manifests/jobs/dump-job.yaml`: a Job on cluster `a` that runs the DB client image, executes a deterministic dump ordered by primary key (e.g. `mysqldump --skip-dump-date --order-by-primary` or `pg_dump` piped through ordered `COPY`), and writes it to a hostPath-mounted directory so the file lands on the host (e.g. `/tmp/migrate-<studentID>/dump.sql`).
5. Write `manifests/jobs/restore-job.yaml`: a Job on cluster `b` that mounts the same host directory via hostPath and restores `dump.sql` into the empty DB.
6. Write `scripts/freeze.sh`: scales `app-<studentID>` on cluster `a` to 0 replicas (or runs a `REVOKE INSERT, UPDATE, DELETE` statement) and verifies no writers remain. Write `scripts/unfreeze-b.sh` that points traffic at cluster `b`'s app.
7. Write `scripts/verify.sh`: run against a named context, it prints `SELECT COUNT(*) FROM records;` and the SHA256 of the ordered dump. It must accept the context as an argument (`./scripts/verify.sh kind-a`).
8. Write `scripts/probe.sh`: a `curl` loop against the serving app URL, one request per second, timestamping each success/failure to `evidence/probe.log`, so downtime = the failure window in the log. It must take the target URL as an argument.
9. Maintain `ledger.md` in git: one row per rehearsal with date, row count on `a`, SHA256 of the ordered dump, row count on `b` after restore, SHA256 on `b`, and measured downtime. At least three rehearsal entries committed before submission.
10. `bootstrap.sh` must stand up cluster `a` fully seeded (and optionally pre-create cluster `b`) from a clean host in under 15 minutes, taking `<studentID>` as a parameter or variable at the top.
11. All names, namespaces, and host paths must derive from a single `STUDENT_ID` variable - no hardcoded IDs scattered through files.
12. Everything above lives in the git repo; no manual steps outside `bootstrap.sh`, the scripts, and `kubectl` commands documented in the runbook.

### Runbook you must write

- How to bootstrap cluster `a` from nothing: `./bootstrap.sh <studentID>` and the verification commands that prove seeding worked.
- How to create and prepare cluster `b`: `kind create cluster --name b`, `kubectl --context kind-b apply -f manifests/b/`.
- How to freeze writes on `a`: `./scripts/freeze.sh` and how to prove the app is down to 0 replicas (`kubectl --context kind-a get deploy app-<studentID>`).
- How to run the dump Job and confirm completion: `kubectl --context kind-a apply -f manifests/jobs/dump-job.yaml`, `kubectl --context kind-a wait --for=condition=complete job/dump-<studentID>`, and where the dump lands on the host.
- How to compute and record the checksum: `sha256sum /tmp/migrate-<studentID>/dump.sql` and the `verify.sh` invocation for each side.
- How to restore on `b` and verify: apply the restore Job, wait for completion, run `./scripts/verify.sh kind-b`, compare counts and checksums.
- How to cut over and measure downtime: start `./scripts/probe.sh <url>` before the freeze, switch it to cluster `b`'s NodePort after restore, and read the failure window out of `evidence/probe.log`.
- How to roll back if the restore fails: unfreeze cluster `a` (scale app back up) and abandon the cutover.

### Submission

- Repo layout: `manifests/a/`, `manifests/b/`, `manifests/jobs/`, `scripts/`, `bootstrap.sh`, `runbook.md`, `ledger.md`, `evidence/` (probe logs and checksum outputs from rehearsals).
- GitHub Actions, if you build your own app image, may only build and push the image to Docker Hub/GHCR - never touch either cluster.
- Submission = the final commit hash. You present immediately after submitting, in the same session, from exactly that commit, live from your own host. No edits after submission - the runbook you froze is the runbook you follow.

### Presentation (starts right after you submit)

1. `git log -1` to show the frozen commit, then `./bootstrap.sh <studentID>` (or show cluster `a` already up from a clean bootstrap started at the top of the session). Prove seed data: `./scripts/verify.sh kind-a` shows the row count and rows containing your student ID.
2. **Twist (happens here, ~30 minutes before your cutover step):** the instructor runs their own insert script against your cluster `a` database. It inserts an instructor-chosen number of marker rows with an instructor-chosen marker string (e.g. `TWIST-<random>`) - you learn the string only when they run it. You cannot rehearse the exact rows; your pipeline must carry whatever is in the table. Continue the demo while these rows sit in `a`.
3. Start the downtime probe: `./scripts/probe.sh http://<host>:<nodePortA>/` in a second terminal, visibly logging one line per second.
4. Create/confirm cluster `b`: `kind create cluster --name b` (or show it pre-created), apply `manifests/b/`, show its `records` table is empty.
5. Freeze writes on `a` (`./scripts/freeze.sh`), run the dump Job, and run `sha256sum` on the ordered dump. Read the checksum aloud and show the row count - it must include the instructor's marker rows.
6. Run the restore Job on `b`, wait for completion, then `./scripts/verify.sh kind-b`: row count and SHA256 must match cluster `a` exactly.
7. Query the instructor's marker rows on `b`: `SELECT * FROM records WHERE payload LIKE '%<instructor-marker>%';` - the instructor confirms the rows they inserted are all present.
8. Point the probe at cluster `b`'s NodePort, stop it, and read the downtime window out of `evidence/probe.log`. Append the final row to `ledger.md` on screen and compare against your rehearsal entries.

### Oral questions to be ready for

1. Your dump is ordered by primary key. What specifically would break the SHA256 comparison if you dropped the ordering flag, even with identical data?
2. What happens to the instructor's marker rows if they run the insert script *after* your freeze but *before* your dump Job starts - and how does your freeze prevent that window from existing?
3. Your restore Job uses hostPath. Why does that work here, and why would this exact transfer design fail if clusters `a` and `b` were on different hosts?
4. Walk through your probe log from a rehearsal: which specific step of the cutover accounts for most of the downtime, and what did you change to shrink it?
5. During a rehearsal the restore Job completed but the checksums differed. What did you check first, and why can a "successful" restore still produce a mismatched dump?

### Pass bars

- Row counts and SHA256 checksums of the ordered dumps match exactly between clusters `a` and `b`, live on screen.
- Every instructor-inserted marker row is queryable on cluster `b` - zero lost rows, including rows you never saw before the demo.
- Measured downtime from the probe log is under 10 minutes, freeze to cutover.
- `ledger.md` contains at least three pre-submission rehearsal entries whose checksums were reproduced by the live run's method.
- `bootstrap.sh` brought cluster `a` from clean host to seeded, serving app in under 15 minutes without manual intervention.

---

## Project 7 - Zero-data-loss app upgrade

**Goal.** Build a small web app backed by MySQL, both running in kind, where every app version change runs a schema migration Job before the new pods roll out. Version 2 ships with a deliberately destructive, broken migration that corrupts data in a way `kubectl rollout undo` cannot repair. The live demo proves you understand the difference between rolling back *code* and recovering *data*: you take a real backup before upgrading, watch the v2 migration destroy data, correctly diagnose why rollback is not enough, and restore the database from your backup with zero lost rows.

### What you will learn

- Why `kubectl rollout undo` reverses Deployments but never reverses database schema or data changes.
- How to run schema migrations as a Kubernetes Job (or initContainer) gated by a `schema_version` table.
- How to take and verify a MySQL logical backup (`mysqldump`) from inside a cluster, and how to restore it under pressure.
- How Deployment rollouts, Jobs, and stateful data interact during an upgrade - and where the point of no return is.
- How to write and follow a runbook when something is genuinely broken and the audience is watching.

### Environment

- kind cluster from a committed config file `kind-config.yaml`: 1 control-plane + 1 worker (multi-node so MySQL and the app land on the worker via a nodeSelector - keeps the demo honest about scheduling).
- Namespace: `upgrade-<studentID>` (e.g. `upgrade-jsmith12`). Every resource lives in it.
- Images: your own app images `docker.io/<dockerhubuser>/notes-app:v1` and `:v2` (small provided/AI-generated web app is fine - Flask/Express/Go, one table, list + add rows). MySQL: official `mysql:8.0` from Docker Hub.
- Migrations: plain `.sql` files baked into a tiny migration image (or mounted from a ConfigMap) and executed by a Job running the `mysql` client image. No migration frameworks required.
- Extra tooling: none beyond `kind`, `kubectl`, `docker`, and the `mysql` client (run it inside a pod - nothing to install on the host).

### Build requirements

1. **MySQL**: a single-replica Deployment (or StatefulSet) `mysql`, a PVC `mysql-data-<studentID>` on the kind `standard` StorageClass, a ClusterIP Service `mysql`, root/app credentials in a Secret `mysql-creds-<studentID>`, and DB config (database name `notesdb`) in a ConfigMap.
2. **App v1**: Deployment `notes-app` with 2 replicas running `:v1`, exposed via NodePort Service `notes-app-svc` reachable from the host (map the NodePort in `kind-config.yaml` with `extraPortMappings`). v1 serves a page/endpoint listing all rows from a table `notes(id, author, body, created_at)`.
3. **Student ID stamping**: the seed data must contain at least 20 rows where `author = '<studentID>'`, and the app must print `Served by <studentID> - app vX - schema vY` on every page (version read live from the DB's `schema_version` table, not hardcoded).
4. **Migration mechanism**: each version has a numbered migration (`migrations/001_init.sql`, `migrations/002_v2.sql`). A Kubernetes Job `migrate-v1` / `migrate-v2` applies its migration only if `schema_version` is lower than the target, then updates `schema_version`. The app's v2 pods must refuse to become Ready (readiness probe or startup check) unless `schema_version = 2` - this forces the Job-before-rollout ordering.
5. **The broken v2 migration (by design)**: `002_v2.sql` renames `body` to `content` by creating the new column, copying only rows `WHERE id <= 10` (a "partial copy" bug), then `DROP COLUMN body`. Result: schema says v2, app v2 works, but every note past id 10 has NULL content. This exact failure mode must be committed to git as-is - do not fix the SQL; the fix is operational.
6. **Backup and restore**: a manifest `backup-job.yaml` (Job running `mysql:8.0`, executing `mysqldump --databases notesdb` to a dedicated PVC `backup-<studentID>` AND streamed to the host via `kubectl exec`/`kubectl cp` in the runbook), and `restore-job.yaml` that replays the dump. Both parameterized so the dump filename includes a timestamp.
7. **bootstrap.sh**: from a clean host, creates the kind cluster from `kind-config.yaml`, applies all manifests in order, runs `migrate-v1`, seeds the 20+ rows (seed SQL in git, containing `<studentID>` literals), and waits until the v1 app answers over the NodePort. Must finish in under 15 minutes; idempotent enough to re-run after `kind delete cluster`.
8. **Parameterization**: student ID, Docker Hub user, and namespace appear once (top of `bootstrap.sh` or a `params.env`), not scattered through YAML - use `sed`/`envsubst` in the script if needed. Grader will check that changing the ID in one place propagates everywhere.
9. **Row-count proof command**: a documented one-liner that prints total rows and count of non-NULL `body`/`content` rows - this is the before/after evidence for zero data loss.
10. **Everything in git**: manifests, both app versions' source + Dockerfiles, migration SQL (including the broken one), seed SQL, `bootstrap.sh`, `runbook.md`. Images pushed to Docker Hub/GHCR before submission. GitHub Actions may build/push the images only - no kubectl in CI.

### Runbook you must write

- **How to stand up everything** - `./bootstrap.sh` plus the verification commands (`kubectl get all -n upgrade-<studentID>`, `curl` the NodePort, the row-count one-liner).
- **How to take a pre-upgrade backup** - apply `backup-job.yaml`, wait with `kubectl wait --for=condition=complete job/backup-...`, verify the dump exists and contains the expected row count (e.g. `grep -c INSERT` or restore-to-scratch check), and copy it off with `kubectl cp`.
- **How to upgrade v1 → v2** - apply `migrate-v2` Job, wait for completion, then `kubectl set image deployment/notes-app app=<user>/notes-app:v2` and `kubectl rollout status`.
- **How to detect the data damage** - the row-count one-liner and a `SELECT` showing NULL content past id 10; compare against the pre-upgrade counts.
- **How to roll back the app image** - `kubectl rollout undo deployment/notes-app` (and why the v2 readiness gate means you must also handle `schema_version` - document the exact steps).
- **How to restore from backup** - scale the app to 0 (`kubectl scale deployment/notes-app --replicas=0`), run `restore-job.yaml` against the dump, reset `schema_version` to 1, scale v1 back up, re-verify counts match the pre-upgrade numbers exactly.
- **How to decide rollback vs restore** - a short decision table: migration Job not yet run / Job interrupted mid-copy / Job completed. State for each whether `rollout undo` alone is safe and why.

### Submission

- Repo layout: `manifests/` (all YAML, numbered for apply order), `app/` (v1 and v2 source + Dockerfiles), `migrations/`, `bootstrap.sh`, `runbook.md`, `evidence/` (pre-submission dry-run terminal logs only - demo evidence is live, not screenshots).
- Submission = the final commit hash. You present immediately after submitting, in the same session, from exactly that commit on your own host. No edits, no new commits, no "one small fix" - if the runbook is wrong, you improvise live and it costs marks.

### Presentation (starts right after you submit)

1. Clone your frozen commit to a clean directory, run `./bootstrap.sh`, and while it runs, walk the instructor through the migration design and the broken SQL in `002_v2.sql`.
2. Show v1 healthy: `curl` the app, run the row-count one-liner, show `schema_version = 1` and 20+ rows authored by `<studentID>`.
3. Instructor adds 3-5 rows of their own choosing through the app (content you cannot pre-seed). Re-run the row count - this is now the number you must not lose.
4. Take the pre-upgrade backup per your runbook and prove the dump contains the instructor's rows.
5. **Twist (instructor's live choice):** the instructor picks one of: (a) let `migrate-v2` run to completion, then roll out v2; or (b) kill the migration Job pod mid-run (`kubectl delete pod`) partway through the copy; or (c) let migration complete but interrupt the Deployment rollout halfway. You do not know which until this moment.
6. **Before touching anything**, state out loud which recovery is correct for the scenario you got - `rollout undo`, restore from backup, or both - and why. Then check the actual state (`schema_version`, row counts, rollout status) and confirm or revise your call. Marks for reasoning, not luck.
7. Execute the recovery from your runbook. Finish with the row-count one-liner matching step 3 exactly - including the instructor's rows - and the app serving pages again with the correct `Served by <studentID>` banner.
8. Show `kubectl rollout history deployment/notes-app` and explain what it does and does not tell you about the state of the data.

### Oral questions to be ready for

1. Your v2 migration Job completed and reported success - the damage happened with exit code 0. What signal, if any, could have caught this before users did, and where would you add it?
2. In the mid-migration-kill scenario, what exactly determines whether your database is at schema v1, v2, or something in between? Walk me through what `002_v2.sql` had and had not done at the moment the pod died.
3. Why does your v2 pod's readiness gate check `schema_version`, and what would have gone wrong during the rollout without it?
4. Your backup Job ran while the app was still accepting writes. Is your dump consistent? What rows could it miss, and what would you change to guarantee a clean cut?
5. You reset `schema_version` back to 1 during restore. What happens on the next `migrate-v2` run, and how would you make the migration safe to re-run - or safe at all?

### Pass bars

- `bootstrap.sh` produces a working v1 app with seeded, ID-stamped data on a clean host in under 15 minutes, from the frozen commit, with no manual fixes.
- The pre-upgrade backup demonstrably contains the instructor's live-added rows before the twist happens.
- Correct rollback-vs-restore call stated *before* acting, with a reason grounded in the actual `schema_version`/row state - a wrong call corrected after inspection passes; acting first and explaining after does not.
- Post-recovery row count exactly matches the pre-upgrade count, instructor's rows included: zero lost rows.
- Full recovery (decision to healthy app) completes in under 10 minutes using only commands from the runbook.

---

## Project 8 - Node maintenance drill

**Goal.** Build a 4-node kind cluster (1 control-plane + 3 workers) running two identical web apps that write timestamped rows to a data file: one backed by a hostPath volume pinned to a specific worker, one backed by an NFS PV served from inside the cluster. In the live demo you cordon and drain a worker like a real maintenance window, watch pods reschedule, and prove with terminal output why the hostPath app comes back empty on a new node while the NFS app keeps every row. Then you uncordon and drain a different node to show the drill is repeatable.

### What you will learn
- How `kubectl cordon`, `drain`, and `uncordon` actually behave - what gets evicted, what blocks eviction, and why `--ignore-daemonsets` and `--delete-emptydir-data` exist.
- Why hostPath data is node-local: the pod moves, the data does not.
- How an NFS-backed PV survives pod rescheduling because the storage lives outside any one consumer pod.
- How `nodeSelector` and node labels pin workloads, and what happens when the pinned node is cordoned.
- The blast radius of draining a node that hosts shared infrastructure (the NFS server itself).

### Environment
- kind cluster from a checked-in config file `kind-config.yaml`: 1 control-plane + 3 workers. Name the cluster `maint-<studentID>`.
- Namespace: `maint-<studentID>`. Every resource name carries your ID where shown below.
- Images: any small public image you control on Docker Hub or GHCR for the writer app (a shell loop appending lines with `busybox` is fine), plus a public NFS server image (e.g. `itsthenetwork/nfs-server-alpine` or equivalent). No other tooling beyond `kind`, `kubectl`, and `docker`.
- No Helm, no cloud services. Raw YAML + kubectl only.

### Build requirements
1. Commit `kind-config.yaml` defining 1 control-plane and 3 workers. Workers must be identifiable in `kubectl get nodes` output (default names `maint-<studentID>-worker`, `-worker2`, `-worker3` are fine).
2. Label one worker `disk=local-<studentID>` in `bootstrap.sh`. This is the hostPath node.
3. Deploy an in-cluster NFS server as a Deployment `nfs-server-<studentID>` (1 replica) with a ClusterIP Service `nfs-svc-<studentID>` exporting a share. Note which node it lands on - you must be able to find it live with `kubectl get pod -o wide`.
4. Create a PV `pv-nfs-<studentID>` pointing at the NFS service export and a PVC `pvc-nfs-<studentID>` bound to it (static binding, `storageClassName: ""`). Prove the bind in bootstrap output.
5. Deploy app A: Deployment `app-hostpath-<studentID>` (1 replica), `nodeSelector: disk=local-<studentID>`, hostPath volume at `/data` on the node. The container appends a line `"<studentID> $(date) hostpath"` to `/data/log.txt` every 5 seconds.
6. Deploy app B: Deployment `app-nfs-<studentID>` (1 replica), no node pinning, mounts `pvc-nfs-<studentID>` at `/data`, appends `"<studentID> $(date) nfs"` to `/data/log.txt` every 5 seconds.
7. Both apps must seed an initial marker row containing your student ID at container start, so an empty-after-drain hostPath file is unambiguous.
8. `bootstrap.sh` must: create the kind cluster from `kind-config.yaml`, label the worker, apply all manifests in order, wait for readiness (`kubectl wait`/`rollout status`), and print row counts from both apps. Clean host to fully running in under 15 minutes.
9. Parameterize the student ID in one place (a variable at the top of `bootstrap.sh` that stamps names via `sed`/`envsubst`, or clearly documented manifests). Grading checks that your ID appears in the namespace, resource names, AND the data rows.
10. Everything in git: manifests, config, scripts, runbook. No image builds required at demo time - images must already be pushed to Docker Hub/GHCR.

### Runbook you must write
- How to bootstrap from a clean host: `./bootstrap.sh` and what healthy output looks like.
- How to show pod placement: `kubectl get pods -n maint-<studentID> -o wide` and `kubectl get nodes --show-labels`.
- How to read current data from both apps: `kubectl exec ... -- wc -l /data/log.txt` and `tail -3 /data/log.txt` for each.
- How to drain any named worker: `kubectl cordon <node>` then `kubectl drain <node> --ignore-daemonsets --delete-emptydir-data`, including what error appears without those flags and why.
- How to verify rescheduling and re-check data on both apps after the drain, including the expected Pending state of the hostPath pod (its pinned node is unschedulable) or its empty file if it lands on the labeled node after uncordon - state exactly which behavior your design produces and why.
- How to uncordon: `kubectl uncordon <node>` and confirm the node returns to `Ready,SchedulingDisabled` → `Ready`.
- How to recover if the drained node hosted the NFS server: what breaks (app B's mount / new pod stuck ContainerCreating), how to watch it (`kubectl get events`, `kubectl describe pod`), and how service comes back once the NFS server pod reschedules - including whether data survives (it does not if the NFS server itself uses ephemeral storage; say so explicitly and defend the design).
- How to tear down: `kind delete cluster --name maint-<studentID>`.

### Submission
- Repo layout: `manifests/` (all YAML, numbered for apply order), `kind-config.yaml`, `bootstrap.sh`, `runbook.md`, `evidence/` (terminal transcripts from your own rehearsals - for practice tracking only; demo evidence is live).
- Submission = the final commit hash. You present immediately after submitting, in the same session, from exactly that commit on your own host. No edits, no new commits, no local uncommitted files.

### Presentation (starts right after you submit)
1. `git clone` your repo at the frozen commit onto your host (or `git checkout <hash>` in a clean copy) and run `./bootstrap.sh`. While it runs, walk through `kind-config.yaml` and the two volume designs.
2. Show placement: `kubectl get pods -n maint-<studentID> -o wide`. Point out which worker holds the hostPath app, the NFS app, and the NFS server pod.
3. Show live data accumulating: row counts and `tail` from both apps. Note the counts aloud - they are your baseline.
4. **TWIST: the instructor names the worker node to drain.** It may be the hostPath node, the NFS app's node, or the node running the NFS server pod. You run `kubectl cordon` + `kubectl drain --ignore-daemonsets` on whatever node they pick and narrate what you expect before pressing Enter.
5. Watch rescheduling with `kubectl get pods -o wide -w`. Explain every state you see (Evicted, Pending, ContainerCreating). If the NFS server node was picked, explain the blast radius live: app B stalls until the NFS server reschedules, and state clearly what happens to its data given your NFS server's own storage.
6. Re-run the data checks on both apps. Show the hostPath consequence (Pending pod or empty file) versus the NFS app's intact row count including pre-drain rows.
7. `kubectl uncordon` the drained node, confirm it is schedulable, then drain a *different* worker of the instructor's choice and repeat the data check to show the behavior is systematic, not luck.
8. Tear down with `kind delete cluster --name maint-<studentID>` if time allows.

### Oral questions to be ready for
1. When you drained the hostPath node, the pod went Pending instead of rescheduling - walk me through exactly which two mechanisms combined to cause that, and what single change would let it reschedule (and what data it would then see).
2. What did `kubectl drain` refuse to do the first time you ran it without flags, and what specifically does `--ignore-daemonsets` leave running on the node?
3. If I drain the node running your NFS server pod, what is the failure timeline for app B, second by second, and where would its in-flight writes go?
4. Your NFS PV survived the drain - but does the *data* survive a drain of the NFS server's node in your design? Prove your answer from what we just saw, and describe what you would change to make it survive.
5. What is the difference between cordon and drain, and give one real maintenance scenario from this drill where you would cordon but deliberately not drain?

### Pass bars
- Bootstrap from a clean host to both apps writing rows completes in under 15 minutes, entirely from the frozen commit.
- After draining any instructor-chosen worker, the NFS-backed app retains every pre-drain row (counts strictly increase across the drain), demonstrated live.
- The hostPath consequence (Pending pod or data loss) is demonstrated and correctly explained, not just asserted.
- The NFS-server blast radius question is answered correctly with live evidence, whether or not the instructor picks that node.
- Student ID appears in the namespace, all resource names above, and every data row shown on screen.

---

## Project 9 - NFS shared storage

**Goal.** Build an in-cluster NFS server that exports a shared filesystem, then mount that share ReadWriteMany into one writer pod and two reader pods. The live demo proves that shared storage decouples data from pod lifecycle: the instructor kills the writer mid-append, a replacement pod mounts the same share and continues the same files with no data loss visible to the readers - and you can explain what happens when two writers share one file.

### What you will learn

- How to run an NFS server inside Kubernetes as a Deployment fronted by a Service, backed by a PVC.
- The difference between ReadWriteOnce (kind's local-path StorageClass) and ReadWriteMany access modes, and why NFS enables RWX where local-path cannot.
- How static PV/PVC binding works when you declare `nfs:` volumes by hand instead of using a StorageClass.
- Why the NFS PV must reference the Service's ClusterIP rather than its DNS name, and what that tells you about where volume mounts happen (kubelet on the node, outside pod DNS).
- The risks of concurrent writers on shared storage: interleaving, last-write-wins, and why NFS gives you shared files but not coordination.

### Environment

- kind cluster with 1 control-plane + 2 workers, defined in `kind-config.yaml` (workers so you can show pods on different nodes mounting the same share).
- Images: `itsthenetwork/nfs-server-alpine:latest` (or `k8s-ganesha`) for the server; `busybox` or `alpine` for writer/reader pods.
- NFS client utilities must be present on the kind nodes - document in the runbook whether your kind node image already includes them (the standard kindest/node image does) and how you verified.
- Namespace: `nfs-<studentID>` (e.g. `nfs-jsmith12`). All resources live in it except the PV, which is cluster-scoped and must be named `pv-nfs-<studentID>`.
- Runs entirely on your single EC2/Cloud9 host. No Helm, no cloud storage.

### Build requirements

1. Create namespace `nfs-<studentID>`. Every namespaced object below goes in it.
2. Create a PVC `nfs-backend-<studentID>` (1Gi, ReadWriteOnce, StorageClass `standard`) that provides the NFS server's backing disk via kind's local-path provisioner. This PVC demonstrates RWO: it belongs to the server pod alone.
3. Deploy the NFS server as a Deployment `nfs-server-<studentID>` (replicas: 1) using `itsthenetwork/nfs-server-alpine` (or ganesha), exporting `/nfsshare`, mounting the backing PVC at the export path. Set the required `SHARED_DIRECTORY` env var and `privileged: true` security context (required by the image - note this in the runbook).
4. Create a ClusterIP Service `nfs-svc-<studentID>` exposing ports 2049 (and 111 if using ganesha).
5. Create a static PV `pv-nfs-<studentID>`: `accessModes: [ReadWriteMany]`, `nfs.server:` set to the Service's **ClusterIP** (not the DNS name), `nfs.path: /`, `storageClassName: ""`, `persistentVolumeReclaimPolicy: Retain`. Because the ClusterIP is only known after the Service exists, the PV manifest must be a template (e.g. `pv-nfs.yaml.tpl` with a `__NFS_IP__` placeholder) that `bootstrap.sh` fills in with `kubectl get svc -o jsonpath='{.spec.clusterIP}'` and applies. Be ready to explain why DNS does not work here.
6. Create a PVC `pvc-shared-<studentID>` with ReadWriteMany that binds to that PV by name (`volumeName`), `storageClassName: ""`.
7. Create a writer Deployment `writer-<studentID>` (replicas: 1) that mounts the shared PVC at `/data` and runs a loop appending a line every 2 seconds to `/data/log-<studentID>.txt`, each line containing your student ID, the pod name (`$HOSTNAME`), and a timestamp: e.g. `echo "<studentID> $HOSTNAME $(date +%T) seq=$i" >> /data/log-<studentID>.txt`.
8. Create two reader pods (a Deployment `reader-<studentID>` with replicas: 2, or two named pods) that mount the same PVC read-only and run `tail -f /data/log-<studentID>.txt`. Use pod anti-affinity or `nodeSelector` so the readers land on different worker nodes.
9. Add a demonstration manifest `rwo-conflict.yaml`: a second pod that tries to mount the RWO backing PVC directly. It must stay Pending/ContainerCreating on the other node - you will use it to show RWO vs RWX live.
10. `bootstrap.sh` must stand up everything from a clean host: create the kind cluster from `kind-config.yaml`, apply all manifests in order, render the PV template with the live ClusterIP, wait for the writer to produce at least 5 lines, and print `kubectl get pv,pvc,pods -n nfs-<studentID>`. Target: under 15 minutes end to end.
11. Everything in git: `kind-config.yaml`, all manifests (including the PV template), `bootstrap.sh`, `runbook.md`. No generated files with hardcoded IPs committed - the rendered PV is produced at bootstrap time.
12. Parameterize your student ID in one place (a variable at the top of `bootstrap.sh` or an `envsubst`-style template) so the grader can see it flows into namespace, resource names, and file contents.

### Runbook you must write

- How to bootstrap from a clean host: `./bootstrap.sh`, expected duration, expected final output.
- How to verify the share is live: `kubectl exec` into a reader and `tail /data/log-<studentID>.txt`; compare against `kubectl exec` into the writer.
- How to show which node each pod is on: `kubectl get pods -o wide -n nfs-<studentID>`.
- How to demonstrate RWO vs RWX: apply `rwo-conflict.yaml`, show the Pending pod with `kubectl describe pod`, contrast with both readers Running on different nodes against the RWX PVC.
- How to kill the writer and prove continuity: `kubectl delete pod <writer-pod> -n nfs-<studentID>`, watch the replacement with `kubectl get pods -w`, then show the log file contains lines from both the old and new pod names with no truncation (`grep -c`, `tail -20`).
- How to scale writers and observe concurrent-write behavior: `kubectl scale deployment writer-<studentID> --replicas=2`, then `tail -f` the file and point out interleaved lines from two hostnames.
- How to re-render the PV if the Service ClusterIP changes (cluster rebuild): the exact `kubectl get svc` jsonpath command and re-apply steps.
- How to tear down: `kind delete cluster`.

### Submission

- Repo layout:
 - `manifests/` - all YAML (namespace, backing PVC, NFS server Deployment + Service, PV template, shared PVC, writer, readers, rwo-conflict)
 - `bootstrap.sh` - executable, stands up everything from nothing
 - `runbook.md` - every procedure above with exact commands
 - `evidence/` - terminal transcripts from your own dry run (e.g. `script` output), not screenshots
- GitHub Actions, if you use it, may only build and push images - it must never touch the cluster.
- Freeze rule: submission = your final commit hash. You present immediately after submitting, in the same session, from exactly that commit on your own host. No edits, no new commits, no "one small fix" after submission.

### Presentation (starts right after you submit)

1. `git clone` (or `git checkout <submitted-hash>`) on your host, run `./bootstrap.sh`, and narrate what it creates while it runs. Cluster and all pods must be up within 15 minutes.
2. Show the topology: `kubectl get pods -o wide -n nfs-<studentID>` - point out writer and both readers on different nodes, all mounting one PVC. Show `kubectl get pv pv-nfs-<studentID> -o yaml` and explain the ClusterIP in `nfs.server` and why DNS would fail there.
3. Prove shared reads: `kubectl exec` into each reader and `tail /data/log-<studentID>.txt` - same file, same content, growing live, lines stamped with your student ID.
4. Prove RWO vs RWX: apply `rwo-conflict.yaml`, show it stuck, read the `describe` event aloud, delete it.
5. **Twist part 1 - instructor deletes the writer.** The instructor (not you) picks the moment and runs the delete - they may delete the pod, kill the container process via `kubectl exec`, or drain the writer's node; you get told which only as it happens. Show the replacement pod starting, then prove continuity: `tail -30` shows lines from the old pod name followed by lines from the new pod name, with sequence numbers letting you argue exactly how many seconds of writes (if any) were lost.
6. **Twist part 2 - instructor scales writers to 2.** The instructor runs (or dictates) `kubectl scale deployment writer-<studentID> --replicas=2 -n nfs-<studentID>`. Show interleaved output from two hostnames in the shared file, then answer live: what could go wrong with two concurrent writers, and what would you change if this were a real application?
7. Kill the NFS server pod yourself, show reader I/O stalling (`tail -f` freezes), show it resuming when the Deployment replaces the server, and explain why the data survived (backing PVC + Retain).
8. Tear down with `kind delete cluster`.

### Oral questions to be ready for

1. Your PV uses the Service's ClusterIP instead of `nfs-svc-<studentID>.nfs-<studentID>.svc.cluster.local`. What component actually performs the NFS mount, and why can't it resolve that DNS name?
2. When the instructor deleted your writer mid-append, exactly how many lines were lost, and what in your log format let you prove that number instead of guessing?
3. The backing PVC is RWO but three pods read and write the shared data at once. Explain how both statements are true at the same time.
4. With two writers appending to the same file over NFS, what failure modes are possible even if you never saw a garbled line during the demo? What would you use instead of a shared file if writes had to be safe?
5. Your NFS server is a Deployment with one replica. What happens to in-flight writes while it restarts, and why is setting `replicas: 2` on the NFS server itself a bad idea here?

### Pass bars

- `bootstrap.sh` brings up the full stack (cluster, NFS server, PV/PVC bound, writer + 2 readers writing/reading live) from a clean host in under 15 minutes, from the frozen commit, with no manual fixes.
- Both readers on different nodes show the same live-growing file; the RWO conflict pod demonstrably cannot schedule the same way.
- After the instructor's writer kill, the replacement pod appends to the same file and you quantify the gap (if any) using your sequence numbers - an unexplained truncation or restart-from-empty file is a fail.
- You correctly explain the ClusterIP-not-DNS requirement in terms of where the mount happens (kubelet on the node), not just "DNS didn't work".
- During the scale-to-2 twist, you identify at least one concrete concurrent-write risk and one realistic mitigation without prompting.

---

## Project 10 - Mini multi-tenant cluster

**Goal.** Build a single kind cluster that safely hosts three isolated "tenants", each in its own namespace with its own ServiceAccount, RBAC rules, ResourceQuota, and LimitRange. In the live demo you prove the isolation actually works - tenant A's credentials cannot read tenant B's Secrets, quota rejects over-limit workloads, and LimitRange fills in sane defaults - then the instructor breaks one tenant's policy objects and you diagnose and fix it live using only kubectl.

### What you will learn

- How namespaces, RBAC, ResourceQuota, and LimitRange combine to fake multi-tenancy on one cluster.
- How to mint and use scoped credentials with `kubectl create token` and a hand-built kubeconfig.
- How to test authorization without guessing, using `kubectl auth can-i --as` and real API calls.
- How quota math relates to node allocatable capacity - why a quota can be "legal" but unschedulable.
- How to debug policy failures (Forbidden errors, quota rejections, admission failures) from the messages Kubernetes actually gives you.

### Environment

- kind cluster with 1 control-plane and 2 workers, defined in `kind-config.yaml` in your repo. Cluster name `multitenant-<studentID>`.
- Workload images: `nginx:1.27` and `busybox:1.36` from Docker Hub (or mirrored to your own Docker Hub/GHCR account). No app code required - this project is about policy, not applications.
- Tooling: kubectl and kind only. No Helm, no external auth systems.
- Namespaces: `tenant-<studentID>-a`, `tenant-<studentID>-b`, `tenant-<studentID>-c`.

### Build requirements

1. Create the three namespaces `tenant-<studentID>-a`, `tenant-<studentID>-b`, `tenant-<studentID>-c`, each labeled `owner=<studentID>` and `tenant=a|b|c`. All namespace and tenant names must be parameterized in `bootstrap.sh` via a `STUDENT_ID` variable at the top of the script - no hardcoded IDs anywhere else.
2. In each namespace create a ServiceAccount named `dev-<tenant>` (e.g. `dev-a` in the a-namespace). This is the identity a "tenant developer" uses.
3. In each namespace create a Role `tenant-dev` granting get/list/watch/create/delete on pods, deployments, services, and configmaps, and get/list on secrets - **within that namespace only**. Bind it with a RoleBinding `tenant-dev-binding` to that tenant's ServiceAccount. No ClusterRoleBindings for tenant identities, ever.
4. Write a script `mint-kubeconfig.sh <tenant>` that runs `kubectl create token dev-<tenant> -n tenant-<studentID>-<tenant> --duration=2h`, then assembles a standalone kubeconfig file `kubeconfigs/tenant-<tenant>.kubeconfig` (cluster CA + server URL + the token). `kubectl --kubeconfig kubeconfigs/tenant-a.kubeconfig get pods` must work with no other flags.
5. Apply a ResourceQuota `quota-<tenant>` in each namespace. Tenant a: `requests.cpu=500m, requests.memory=512Mi, limits.cpu=1, limits.memory=1Gi, pods=5, secrets=5`. Tenant b: double tenant a. Tenant c: half tenant a. Document in `runbook.md` the arithmetic showing the sum of all three tenants' CPU/memory limits against your workers' `kubectl describe node` allocatable values.
6. Apply a LimitRange `limits-<tenant>` in each namespace with `defaultRequest` (cpu 100m, memory 64Mi) and `default` limits (cpu 200m, memory 128Mi) for containers. Defaults must fit under the tenant's quota so a bare `kubectl run` pod is admitted.
7. Seed each namespace with: a Secret named `secret-<studentID>-<tenant>` whose data contains the key `owner` with value `<studentID>-tenant-<tenant>`, and a Deployment `web-<studentID>` (nginx, 2 replicas, no explicit resources - the LimitRange must fill them in).
8. Include a "denial matrix" script `scripts/authz-matrix.sh` that loops over all three ServiceAccount identities × all three namespaces and prints the result of `kubectl auth can-i get secrets -n <ns> --as=system:serviceaccount:<ns2>:dev-<t>` as a 3×3 table. Expected result: yes on the diagonal, no everywhere else.
9. Include a deliberately over-quota manifest `manifests/overquota-pod.yaml` (requests exceeding the tenant-c quota) used in the demo to show a live quota rejection.
10. Everything in git: `kind-config.yaml`, all manifests under `manifests/` (numbered so `kubectl apply -f manifests/` in order works), `mint-kubeconfig.sh`, `scripts/authz-matrix.sh`, `bootstrap.sh`, `runbook.md`. Kubeconfig files and tokens must NOT be committed - add `kubeconfigs/` to `.gitignore`.
11. `bootstrap.sh` must go from a clean host (no kind cluster) to fully seeded three-tenant cluster, including minting all three kubeconfigs, in under 15 minutes, ending with the authz-matrix output printed.

### Runbook you must write

- How to bootstrap from scratch: `./bootstrap.sh` and what output confirms success.
- How to mint a fresh tenant kubeconfig: `./mint-kubeconfig.sh <tenant>` and how to verify it with `kubectl --kubeconfig ... auth whoami`.
- How to run the denial matrix: `scripts/authz-matrix.sh` and how to interpret the table.
- How to prove cross-tenant denial with a real API call, not just can-i: `kubectl --kubeconfig kubeconfigs/tenant-a.kubeconfig get secret secret-<studentID>-b -n tenant-<studentID>-b` and the exact Forbidden error expected.
- How to show quota consumption and headroom: `kubectl describe resourcequota -n <ns>` and `kubectl get resourcequota -A`.
- How to demonstrate LimitRange defaulting: `kubectl run test --image=nginx -n <ns>` then `kubectl get pod test -o jsonpath='{.spec.containers[0].resources}'`.
- How to diagnose a broken tenant, in order: `kubectl auth can-i --list --as=...`, `kubectl describe role/rolebinding -n <ns>`, `kubectl describe resourcequota -n <ns>`, `kubectl describe limitrange -n <ns>`, `kubectl get events -n <ns> --sort-by=.lastTimestamp`, and how to tell which of the three policy objects is at fault from the error text.
- How to repair: re-apply the known-good manifest with `kubectl apply -f manifests/<file>` and re-verify.
- How to show quota math vs node capacity: `kubectl describe node <worker> | grep -A8 Allocatable` alongside the sum of all quotas.

### Submission

- Repo layout: `kind-config.yaml`, `manifests/` (numbered YAML), `scripts/` (`authz-matrix.sh`), `mint-kubeconfig.sh`, `bootstrap.sh`, `runbook.md`, `evidence/` (bootstrap timing log and one full authz-matrix run captured with `script` or `tee` - terminal text, not screenshots), `.gitignore` excluding `kubeconfigs/`.
- Submission = the final commit hash. You present immediately after submitting, in the same session, from exactly that commit on your own host. No edits, no extra commits, no "fixed one thing" - the frozen commit is what runs.

### Presentation (starts right after you submit)

1. Clone your frozen commit into a fresh directory on your host and run `./bootstrap.sh`. While it builds, walk the instructor through the quota math against node allocatable.
2. When bootstrap finishes, show all three namespaces populated: `kubectl get deploy,secret,resourcequota,limitrange -A | grep <studentID>`.
3. Run the denial matrix (`scripts/authz-matrix.sh`) and explain the diagonal.
4. Prove denial for real: using `kubeconfigs/tenant-a.kubeconfig`, attempt to read tenant b's Secret and show the Forbidden error; then read tenant a's own Secret and show the `<studentID>` value inside it.
5. Show LimitRange defaulting (`kubectl run` a bare pod, inspect its resources) and quota rejection (`kubectl apply -f manifests/overquota-pod.yaml` in tenant c, show the error message naming the exceeded resource).
6. **Twist.** The instructor picks one tenant (a, b, or c - their choice) and injects one fault from an unpublished pool while you look away, e.g.: edits the Role's verbs so the tenant loses `list` on pods; adds a quota constraint on an unexpected resource (e.g. `services=0` or `configmaps=1`); or raises the LimitRange default above the quota so no new pod can be admitted. They then tell you only: "tenant <x> developers say things are broken."
7. Diagnose live following your runbook's diagnosis order: reproduce the failure as the tenant identity, read the error, inspect Role/RoleBinding, ResourceQuota, and LimitRange, and state out loud which object is wrong and why.
8. Repair by re-applying the known-good manifest from your repo, then re-run the failing command and the denial matrix to prove the tenant is healthy and isolation is still intact.

### Oral questions to be ready for

1. Your Role grants `get` and `list` on secrets - why does `kubectl auth can-i get secrets --as=...` say yes for the tenant's own namespace but the same identity gets Forbidden in another namespace, when the Role objects are identical in both?
2. During the twist, how did you decide whether the failure was RBAC, quota, or LimitRange before looking at any manifests? What in the error message told you?
3. Your three quotas sum to more CPU than one worker's allocatable. Is that a problem? What actually happens when tenants try to use all of it at once?
4. The token from `kubectl create token` expired mid-demo. What exactly stops working, what still works, and how do you recover without touching any manifests?
5. A pod created with no resources block gets requests/limits anyway - walk through exactly which object injected them, at what point in the API request path, and what would have happened to the same pod if the LimitRange were deleted.

### Pass bars

- `bootstrap.sh` produces the full three-tenant cluster from a clean host in under 15 minutes, ending with a correct denial matrix (yes on diagonal, no elsewhere).
- Cross-tenant Secret read fails with a live Forbidden error using a minted tenant kubeconfig, and the same identity reads its own `<studentID>`-stamped Secret successfully.
- The over-quota pod is rejected with an error naming the exceeded resource, and a bare pod receives LimitRange defaults visible in its spec.
- The instructor's injected fault is correctly identified (which object, which field) and repaired using only kubectl and manifests from the frozen commit, with the denial matrix clean afterward.
- No ClusterRoleBindings for tenant identities and no credentials committed to git.

---

## Project 11 - RBAC personas and break-glass
**Goal.** Build a kind cluster with three least-privilege identities - a deployer, a read-only auditor, and a CI pusher - each with its own ServiceAccount, Role/RoleBinding set, and kubeconfig, plus a scripted permission test suite that proves exactly what each persona can and cannot do. The live demo proves you can operate least-privilege access like an SRE: when the instructor silently breaks one piece of your RBAC, you diagnose it from the persona's symptoms alone (failing commands, `auth can-i` output) and repair it using your documented break-glass path - without being told what was changed.

### What you will learn
- How Kubernetes authorizes requests: ServiceAccounts, Roles, ClusterRoles, RoleBindings, and how verbs/resources/apiGroups combine.
- How to mint a kubeconfig for a ServiceAccount using a token and use it with `kubectl --kubeconfig`.
- How to test permissions systematically with `kubectl auth can-i` instead of guessing.
- How to diagnose an authorization failure from symptoms (Forbidden errors) and trace it back to the exact broken object.
- Why a break-glass admin path must exist, be documented, and be used sparingly.

### Environment
- kind cluster from a committed config file `kind-config.yaml`: 1 control-plane + 1 worker (RBAC needs no special topology; the worker proves your manifests do not assume a single node).
- Images: any small public image from Docker Hub - use `nginx:1.27-alpine` as the demo workload. Your CI persona demo also uses an image you built and pushed to Docker Hub/GHCR in an earlier week (`<dockerhubuser>/clo835-app:<tag>`).
- Tooling: `kubectl`, `kind`, `jq` (all already installed/trivially installable). No Helm, no external auth providers.
- Namespace: everything lives in `rbac-<studentID>` (e.g. `rbac-jsmith12`). The break-glass kubeconfig is the only identity allowed outside it.

### Build requirements
1. Commit `kind-config.yaml` and a `bootstrap.sh` that creates the cluster, the namespace `rbac-<studentID>`, all RBAC objects, the demo workload, the three kubeconfigs, and runs the permission test suite once - all from a clean host in under 15 minutes.
2. Create three ServiceAccounts in `rbac-<studentID>`: `deployer-<studentID>`, `readonly-<studentID>`, `ci-<studentID>`. Your student ID must appear in the SA names AND in a label `owner=<studentID>` on every RBAC object.
3. Deployer persona: a Role `deployer-role-<studentID>` allowing get/list/watch/create/update/patch/delete on deployments, replicasets, pods, services, configmaps in the namespace - and nothing else (no secrets, no RBAC objects, no other namespaces). Bound by RoleBinding `deployer-binding-<studentID>`.
4. Read-only persona: Role `readonly-role-<studentID>` allowing only get/list/watch on pods, deployments, services, configmaps, events. It must NOT be able to read secrets - you will prove this live.
5. CI persona: Role `ci-role-<studentID>` allowing ONLY `patch` and `get` on deployments (the minimum for `kubectl set image` plus verifying it landed). It must not be able to list pods, read logs, or delete anything. This models "CI can roll a new image, nothing more."
6. Generate a kubeconfig per persona (`kubeconfigs/deployer.kubeconfig`, `readonly.kubeconfig`, `ci.kubeconfig`) in `bootstrap.sh` using `kubectl create token <sa>` (bounded duration is fine; regenerate at bootstrap). The generation script is committed; the generated kubeconfig files are NOT committed (add to `.gitignore`).
7. Demo workload: Deployment `web-<studentID>` (nginx, 2 replicas), Service `web-<studentID>` (ClusterIP), a ConfigMap `app-config-<studentID>` whose data contains the line `owner: <studentID>`, and a Secret `db-creds-<studentID>` (any dummy values) - the secret exists specifically so read-only can be denied access to it.
8. Permission test suite: a committed script `tests/rbac-test.sh` that runs a fixed list of `kubectl auth can-i <verb> <resource> -n rbac-<studentID>` checks against each persona's kubeconfig (minimum 8 checks per persona, mixing expected-yes and expected-no), compares actual output to a committed expectations file `tests/expected.txt`, prints a per-check PASS/FAIL line, and exits nonzero on any mismatch.
9. Break-glass: document (in `runbook.md`) and script (`break-glass.sh`) the admin path - the kind-generated admin kubeconfig (`kind get kubeconfig`) or the `kubernetes-admin` context. The runbook must justify in 3-5 sentences when break-glass is permitted and why the personas must never be given cluster-admin.
10. Parameterize the student ID and Docker Hub user once at the top of `bootstrap.sh` (e.g. `SID=jsmith12`); every manifest either uses `envsubst`/`sed` templating from that variable or is generated by the script. Grading will check that changing `SID` changes every name.
11. All manifests live in `manifests/`, split into `manifests/rbac/` and `manifests/workload/`. No `kubectl create role` imperative-only objects - everything that defines the desired state is YAML in git.

### Runbook you must write
- How to bootstrap from a clean host: `./bootstrap.sh` and what "healthy" looks like (`kubectl get all,sa,role,rolebinding -n rbac-<studentID>`).
- How to run the permission test suite and read its output: `./tests/rbac-test.sh`, what a PASS/FAIL line means, exit codes.
- How to act as each persona: the exact `kubectl --kubeconfig kubeconfigs/<persona>.kubeconfig ...` invocations for each persona's normal job (deployer: `apply`/`rollout`; readonly: `get`/`describe`; ci: `set image deployment/web-<studentID>`).
- How to diagnose an authorization failure: read the Forbidden message (user, verb, resource, namespace), confirm with `kubectl auth can-i --list --kubeconfig ...`, then inspect with break-glass: `kubectl get role,rolebinding -n rbac-<studentID> -o yaml`, checking (in order) binding exists → binding's subject name/namespace → binding's roleRef → role's verbs/resources.
- How to invoke break-glass: when it is justified, `./break-glass.sh` or `export KUBECONFIG=$(kind get kubeconfig-path 2>/dev/null || echo ~/.kube/config)` with the admin context, and how to exit back to a persona afterward.
- How to repair: reapply the canonical manifests (`kubectl apply -f manifests/rbac/`) and re-run the test suite to prove recovery.
- How to regenerate a persona kubeconfig if its token expired mid-demo.

### Submission
- Repo layout: `manifests/` (rbac/ and workload/ YAML), `kind-config.yaml`, `bootstrap.sh`, `break-glass.sh`, `tests/rbac-test.sh` + `tests/expected.txt`, `runbook.md`, `evidence/` (one saved terminal transcript of a full bootstrap + green test run, produced with `script` or `tee`), `.gitignore` excluding `kubeconfigs/`.
- GitHub Actions (if you include CI) may only build and push your image to Docker Hub/GHCR - it must never contact the cluster.
- Freeze rule: your submission is a final commit hash. You present immediately after submitting, in the same session, from exactly that commit (`git checkout <hash>`). No edits, no new commits, no uncommitted files during the demo.

### Presentation (starts right after you submit)
1. Clean start: show `git log -1` matches the submitted hash, then run `./bootstrap.sh` (or show the cluster it just built if time-boxed by the instructor) and `kubectl get all,role,rolebinding,sa -n rbac-<studentID>` - point out your student ID in names and in `app-config-<studentID>` data.
2. Run `./tests/rbac-test.sh` - all checks green. Explain two interesting expected-no lines (e.g. readonly cannot get secrets, ci cannot delete deployments).
3. Persona walkthrough: as deployer, scale `web-<studentID>` to 3; as readonly, `kubectl get pods` succeeds but `kubectl get secret db-creds-<studentID>` is Forbidden; as ci, `kubectl set image` succeeds but `kubectl get pods` is Forbidden.
4. **Twist - you leave the room or turn away.** The instructor, using the admin kubeconfig, breaks exactly ONE of: (a) delete one RoleBinding, (b) edit a Role's verbs (e.g. remove `list`), (c) point a binding's subject at the wrong ServiceAccount name, (d) recreate a binding in the wrong namespace. Which one, and against which persona, is the instructor's choice at demo time. You may not look at shell history, audit logs, or ask what was done.
5. Diagnose: rerun `./tests/rbac-test.sh`, identify the failing persona from the red lines, use `auth can-i --list` and Forbidden messages to name the broken object and the exact nature of the break OUT LOUD before touching it.
6. Break-glass: state why admin access is now justified, run `./break-glass.sh`, show the broken object (`kubectl get ... -o yaml`) confirming your diagnosis.
7. Recover: `kubectl apply -f manifests/rbac/`, drop back out of break-glass, rerun `./tests/rbac-test.sh` - all green again.
8. Close: show the persona from step 5 doing its normal job successfully, and show `git status` still clean at the frozen commit.

### Oral questions to be ready for
1. Your test suite went red on the readonly persona but the RoleBinding was intact - walk me through how you distinguished "role verbs edited" from "wrong subject in the binding" using only persona-side commands.
2. Why does `kubectl set image` need `patch` on deployments but not on pods or replicasets? What actually receives the patch, and who updates the pods?
3. Your CI persona's token is a ServiceAccount token you generated at bootstrap. If GitHub Actions had that kubeconfig, why would deploying from CI still violate this course's rules - and what is the security argument beyond the rule?
4. The instructor recreated your binding in the `default` namespace instead of `rbac-<studentID>`. Why did the persona's `auth can-i` in your namespace say no, even though the Role and the binding both "exist" in the cluster?
5. If you gave the deployer persona `create` on rolebindings in its namespace, how could it escalate its own privileges, and what stops that escalation in your current design?

### Pass bars
- `bootstrap.sh` produces a working cluster, all three personas, and a fully green `tests/rbac-test.sh` from a clean host in under 15 minutes, with no manual steps.
- Every persona's expected-no checks actually fail with Forbidden when run live - least privilege is demonstrated, not asserted.
- During the twist you name the broken object AND the specific break (which of the four it was) correctly before opening break-glass, using only persona symptoms and `auth can-i`.
- Recovery completes in under 10 minutes: reapply manifests, exit break-glass, test suite fully green.
- Student ID appears in the namespace, every RBAC object name, and the ConfigMap data; the presented session runs from the exact frozen commit with a clean `git status`.

---

## Project 12 - Secrets rotation with zero downtime
**Goal.** Build a two-tier app in kind - a small web app backed by MySQL - where the app authenticates to the database using credentials stored in a Kubernetes Secret. Then rotate that password live: create a new DB user, update the Secret, roll the Deployment, verify, and revoke the old user, all while a 1-request-per-second curl loop hammers the app. The live demo proves you can rotate a production credential end-to-end with **zero failed requests**, and reverse the whole rotation on command when the instructor declares the new credential compromised.

### What you will learn
- How Pods consume Secrets as env vars versus mounted files, and why env vars require a Pod restart to pick up changes while file mounts update in place (with kubelet sync delay).
- Rotation choreography: why the order is *add new credential → switch consumers → revoke old credential*, and what breaks if you revoke first.
- How a rolling update (`maxUnavailable: 0`, readiness probes) keeps a service answering while every Pod is replaced.
- How to prove availability with evidence (a request loop with a failure counter) instead of asserting it.
- How to reverse a rotation safely when the *new* credential is the one that must die.

### Environment
- kind cluster from a config file committed to the repo: 1 control-plane + 2 workers (`kind-config.yaml`), cluster name `clo835-<studentID>`.
- Namespace: `rotation-<studentID>`. Your Seneca ID must also appear in seeded data (see build requirements).
- Images: `mysql:8.0` from Docker Hub, plus your own web app image (Flask/PHP/Node - anything taught) pushed to Docker Hub or GHCR by GitHub Actions. No other tooling beyond `kubectl`, `curl`, and `docker`.
- MySQL runs as a single-replica Deployment (or StatefulSet) with a PVC on the kind `standard` StorageClass so data survives a Pod restart.

### Build requirements
1. Web app Deployment `webapp-<studentID>`, **2 replicas**, with a readiness probe that only passes when the app can actually run `SELECT 1` against MySQL (an HTTP `/healthz` endpoint that touches the DB). Rolling update strategy must set `maxUnavailable: 0`, `maxSurge: 1`.
2. The app serves one endpoint `/` that runs a query against MySQL and returns a row containing your student ID and the DB username it connected as (e.g. `owner=<studentID> connected_as=appuser_v1`). Returning the connected username is required - it is how the instructor sees which credential is live.
3. MySQL Deployment/StatefulSet `mysql-<studentID>` with a PVC (`standard` StorageClass), a ClusterIP Service `mysql-<studentID>`, and an init job or seed script that creates database `app_<studentID>`, a table seeded with at least 3 rows containing your student ID, and DB user `appuser_v1_<studentID>`.
4. App credentials come from Secret `db-cred-<studentID>` with keys `username` and `password`. The app must read them **as a mounted file** (`/etc/dbcred/username`, `/etc/dbcred/password`), read at connection time, not cached at startup.
5. A second, clearly commented variant manifest `webapp-envvar-variant.yaml` in git showing the same Deployment consuming the Secret via `env.valueFrom.secretKeyRef`. It is not deployed; you must explain in the runbook and orally why this variant *cannot* pick up a Secret change without a restart, while the file mount can (and why you still roll the Deployment anyway: connection re-auth, kubelet sync lag, and deterministic cutover).
6. NodePort Service `webapp-<studentID>` exposing the app, with the port mapped in `kind-config.yaml` via `extraPortMappings` so `curl http://localhost:<port>/` works from the host.
7. A monitor script `monitor.sh` in git: infinite loop, 1 request/second to `/`, printing a running line like `total=412 failed=0 last=owner=<studentID> connected_as=appuser_v1`. Any non-200 or connection error increments `failed`. This is the pass/fail instrument - it must be trivially readable.
8. A rotation script `rotate.sh` (parameterized: `./rotate.sh v2` and `./rotate.sh v1` for rollback) that performs, in order: create DB user `appuser_<version>_<studentID>` with a new password and identical grants; update the Secret (`kubectl create secret ... --dry-run=client -o yaml | kubectl apply -f -`); `kubectl rollout restart deployment/webapp-<studentID>`; `kubectl rollout status`; verify `/` reports the new username; then **pause and prompt** before dropping the old user. The pause is mandatory - the twist happens there.
9. `bootstrap.sh` stands up everything - kind cluster, namespace, MySQL, seed data, Secret (v1), web app, NodePort - from a clean host in under 15 minutes, ending with a smoke test `curl` that prints the seeded row.
10. All manifests are raw YAML under `manifests/`, applied by `bootstrap.sh` with `kubectl apply`. No Helm, no kustomize overlays beyond plain files. GitHub Actions workflow builds and pushes the app image only - the workflow must contain no `kubectl`.
11. Passwords for v1 and v2 must differ and must not be committed in plaintext manifests; generate them in `bootstrap.sh`/`rotate.sh` (e.g. `openssl rand -hex 12`) and write them only into the live Secret and the DB.

### Runbook you must write
- How to bootstrap from a clean host: `./bootstrap.sh`, expected end state, expected duration.
- How to start and read the monitor: `./monitor.sh`, what a failure looks like, where the counter is.
- How to rotate to v2: `./rotate.sh v2` step by step - the exact `mysql` statement creating the user, the `kubectl apply` of the Secret, `kubectl rollout restart` / `rollout status`, the verification `curl`, and the final `DROP USER` command at the pause prompt.
- How to prove the old credential is dead: `kubectl run mysql-client --rm -it --image=mysql:8.0 -- mysql -h mysql-<studentID> -u appuser_v1_<studentID> -p...` showing `Access denied`.
- How to roll back a rotation (v2 declared compromised): re-point the Secret to v1 (or a fresh v3 if v1 was already dropped - cover both cases), roll the Deployment, verify, then drop v2.
- How to inspect what a running Pod actually sees: `kubectl exec ... -- cat /etc/dbcred/username` and how to compare against `kubectl get secret ... -o jsonpath`.
- How to explain env var vs file mount, with the commands that demonstrate the difference (`kubectl exec ... -- env` on the variant vs `cat` on the mount after a Secret change).

### Submission
- Repo layout: `manifests/` (all YAML including `kind-config.yaml` and the env-var variant), `app/` (web app source + Dockerfile), `bootstrap.sh`, `rotate.sh`, `monitor.sh`, `runbook.md`, `evidence/` (terminal transcripts from your own rehearsals - `script` or copy-paste, not screenshots), `.github/workflows/` (build+push only).
- Submission = the final commit hash. You present immediately after submitting, in the same session, from exactly that commit on your own host. No edits, no hotfixes, no "one sec while I change this".

### Presentation (starts right after you submit)
1. Fresh clone of the frozen commit; run `./bootstrap.sh`. While it runs, walk the instructor through the rotation order and why revoke comes last.
2. `curl http://localhost:<port>/` - show the seeded row with your student ID and `connected_as=appuser_v1_<studentID>`.
3. Start `./monitor.sh` in a dedicated visible terminal. It stays on screen for the rest of the demo. Let it accumulate ~20 requests, `failed=0`.
4. Run `./rotate.sh v2`: user v2 created, Secret updated, rolling restart completes, `curl` now shows `connected_as=appuser_v2_<studentID>`. Monitor still shows `failed=0`. The script is now paused at the "drop v1?" prompt.
5. **Twist (here, at the pause):** the instructor makes a live call the student cannot rehearse exactly - either (a) "v2 is compromised, roll back now," or (b) "proceed, drop v1" and *then*, after v1 is gone, "v2 is compromised, get off it" (forcing a fresh v3 rotation instead of a simple revert). The instructor may additionally kill one webapp Pod mid-rollback (`kubectl delete pod` of their choosing). Which branch, and which Pod, is the instructor's decision in the moment.
6. Execute the demanded reversal using the runbook: repoint Secret, roll, verify `connected_as` changed, drop v2. Monitor terminal: still `failed=0`.
7. Prove the compromised credential is dead: mysql-client Pod login as v2 → `Access denied`. Show the surviving user works.
8. Stop the monitor; read out the final line (`total=N failed=0`). Answer oral questions.

### Oral questions to be ready for
1. Your monitor showed zero failures - walk me through the exact moment a Pod with the old credential answered its last request. What guaranteed a v1 Pod and a v2 Pod could both talk to MySQL at that instant?
2. If you had dropped user v1 *before* the rollout finished, what exactly would have failed first, and what would the monitor have shown?
3. Your app reads the Secret from a file mount, and mounted Secrets update automatically - so why does your rotation still do a `rollout restart` instead of just waiting?
4. During your rollback, what would have happened if the instructor's `kubectl delete pod` had hit the last remaining old-credential Pod? Which setting in your Deployment protected the request loop?
5. The kubelet syncs mounted Secrets on a delay. If two Pods briefly disagree about the password file's contents, why doesn't your design produce failed requests during that window?

### Pass bars
- `bootstrap.sh` from a clean host to a working `curl` response in under 15 minutes, on the frozen commit.
- The monitor runs continuously from before the rotation until after the twist is resolved and reports **failed=0** at the end. One failed request = no pass on this bar.
- Forward rotation completes: `/` reports the v2 username and user v1 is provably revoked (`Access denied` shown live).
- The instructor's twist is resolved live using only runbook procedures: the compromised credential ends up revoked, the app ends on a valid credential, still zero failures.
- Student ID appears in the namespace, every major object name, and the seeded data returned by `/`.

---

## Project 13 - HPA under load

**Goal.** Build a CPU-bound web app on a kind cluster, wire it to a HorizontalPodAutoscaler backed by metrics-server, and drive live load against it so the class watches replicas scale out in real time. Then prove you understand the failure mode nobody reads about: a ResourceQuota set below the HPA's maxReplicas, so the autoscaler wants more pods than the namespace will allow. The live demo proves you can predict, observe, and explain exactly where scaling stalls - with a quota number the instructor picks on the spot.

### What you will learn

- Why metrics-server does not work out of the box on kind, and what `--kubelet-insecure-tls` actually disables.
- How HPA v2 computes desired replicas from CPU requests (not limits) and target utilization.
- How a ResourceQuota silently caps an HPA, and where the evidence appears (events, HPA conditions, ReplicaSet events).
- How the scale-in stabilization window prevents replica flapping after load stops.
- How to size CPU requests so autoscaling behaves predictably instead of randomly.

### Environment

- kind cluster from a config file checked into git: 1 control-plane + 2 workers, cluster name `<studentID>-hpa`.
- App image: any small CPU-burnable HTTP server you build yourself (e.g. a PHP, Python, or Go handler that does a tight loop per request) pushed to Docker Hub or GHCR as `<yourhandle>/<studentID>-burn:v1`. The stock `registry.k8s.io/hpa-example` is also acceptable.
- metrics-server installed from its upstream manifest, patched in your repo (not patched live) with `--kubelet-insecure-tls`.
- Load generator: `busybox` running a `wget` loop inside the cluster (a Job), or the `hey` binary on the host. No extra tooling beyond that.
- Namespace: `<studentID>-hpa`. Everything lives in it except metrics-server.

### Build requirements

1. Write `kind-config.yaml` (1 control-plane, 2 workers) and create the cluster as `<studentID>-hpa` in `bootstrap.sh`.
2. Vendor the metrics-server manifest into `manifests/metrics-server.yaml` with the `--kubelet-insecure-tls` flag already added to the Deployment args. Add a comment in the file explaining in one or two sentences why kind needs it (kubelet serving certs are self-signed and lack SANs metrics-server will trust).
3. Create namespace `<studentID>-hpa` in `manifests/00-namespace.yaml`.
4. Deploy the app as Deployment `<studentID>-burn` with exactly: `replicas: 1`, CPU `requests: 200m`, `limits: 500m`. The app's HTTP response body must include your student ID (e.g. `OK burn <studentID>`), so load-test output stamps your ID live.
5. Expose it with a ClusterIP Service `<studentID>-burn-svc` on port 80.
6. Create HPA `<studentID>-burn-hpa` using `autoscaling/v2`: CPU target utilization 50%, `minReplicas: 1`, `maxReplicas: 10`, and a `behavior.scaleDown.stabilizationWindowSeconds` you choose and can defend (60-300s).
7. Create `manifests/quota.yaml` as a ResourceQuota named `<studentID>-quota` in the namespace. The pod-count / CPU-request numbers must be **parameterized**: the file contains a placeholder (e.g. `pods: "${QUOTA_PODS}"`) and a helper script `apply-quota.sh <number>` renders and applies it with `envsubst` or `sed`. Your rehearsed default must cap the namespace below `maxReplicas` (e.g. `pods: "6"` and `requests.cpu` sized to match) so the collision is demonstrable.
8. Write `manifests/load-job.yaml`: a Job named `<studentID>-load` running 2-4 parallel busybox pods in a `wget -q -O- http://<studentID>-burn-svc` loop. Load pods must have their own small CPU request - you must account for them in your quota math.
9. `bootstrap.sh` stands up everything from a clean host - kind cluster, metrics-server, namespace, app, service, HPA, default quota - and blocks until `kubectl top pods -n <studentID>-hpa` returns numbers. Under 15 minutes total.
10. Everything above is raw YAML + kubectl in git. No Helm, no kustomize overlays required. If you use GitHub Actions, it may only build and push the app image.

### Runbook you must write

- How to bootstrap from a clean host: `./bootstrap.sh`, and how to verify metrics-server is serving (`kubectl top nodes`, `kubectl get apiservice v1beta1.metrics.k8s.io`).
- How to apply a quota with an arbitrary number: `./apply-quota.sh <N>` and how to verify with `kubectl describe quota <studentID>-quota -n <studentID>-hpa`.
- How to compute max achievable replicas for a given quota: the arithmetic (pod count cap vs `requests.cpu` cap vs load-Job pods, whichever bites first), written as a worked example.
- How to start and stop load: `kubectl apply -f manifests/load-job.yaml` and `kubectl delete job <studentID>-load -n <studentID>-hpa`.
- How to watch scaling: `kubectl get hpa -n <studentID>-hpa -w`, `kubectl top pods -n <studentID>-hpa`, `kubectl get events -n <studentID>-hpa --sort-by=.lastTimestamp`.
- How to find quota-collision evidence: `kubectl describe rs` (FailedCreate, `exceeded quota`), `kubectl describe hpa` (ScalingLimited / AbleToScale conditions).
- How to observe scale-in: what to run after killing load, what the stabilization window makes you wait for, and how to read `ScaleDownStabilized` in HPA conditions.

### Submission

- Repo layout: `manifests/` (numbered YAML incl. metrics-server, quota template, load job), `apply-quota.sh`, `bootstrap.sh`, `runbook.md`, `kind-config.yaml`, `evidence/` (terminal transcripts from your own rehearsal - the demo itself is live).
- Submission = final commit hash. The hash is frozen at submit time.
- You present immediately after submitting, same session, from that exact commit on your own host. No edits, no amend, no "one small fix".

### Presentation (starts right after you submit)

1. `git log -1` to show the frozen commit, then `./bootstrap.sh` on a clean host (or show the timestamped bootstrap you ran minutes earlier from this commit). Show `kubectl top nodes` works and explain, in one minute, why the `--kubelet-insecure-tls` patch is required on kind and what the production alternative is.
2. Show the app: `kubectl get all -n <studentID>-hpa`; curl the service via a temporary pod and show your student ID in the response body.
3. **Twist:** the instructor now names a quota number - any pod count and/or `requests.cpu` value, e.g. "pods: 4" or "requests.cpu: 1200m". Before touching anything, state out loud your prediction of the maximum replicas the HPA will actually reach under that quota, showing the arithmetic (app pod requests + load-Job pods vs the cap). Write the prediction on the board or in a comment in the terminal.
4. Apply it: `./apply-quota.sh <instructor's number>`, confirm with `kubectl describe quota`.
5. Start load (`kubectl apply -f manifests/load-job.yaml`) and run `kubectl get hpa -w` in one pane, `kubectl get pods -w` in another. Narrate as replicas climb.
6. When scaling stalls, prove why: `kubectl describe hpa <studentID>-burn-hpa` (conditions) and `kubectl describe rs` / events showing `exceeded quota`. Compare the stall point to your step-3 prediction. If you predicted wrong, explain exactly which term in your arithmetic was off.
7. Delete the load Job. Point at the HPA staying scaled out, name your stabilization window, and wait it out (talk through what would happen with a 0-second window). Show replicas drop back to 1.
8. Close with the events timeline: `kubectl get events -n <studentID>-hpa --sort-by=.lastTimestamp` - walk the class through the full story it tells, from SuccessfulRescale to FailedCreate to ScaleDown.

### Oral questions to be ready for

1. Your pods have CPU `limits: 500m` but `requests: 200m` - which number does the HPA's 50% target apply to, and what would change if you deleted the requests entirely?
2. During your demo the HPA showed `<unknown>/50%` for the first minute. What was happening, and what two things would you check if it never resolved?
3. The quota blocked the ReplicaSet, but `kubectl get hpa` still showed a desired replica count above the running count. Which controller actually got refused, and where did the refusal surface?
4. Your load-Job pods count against the same quota as the app pods. How did you account for that in your prediction, and how could you restructure the project so they didn't?
5. If the instructor had set the quota's `requests.cpu` to 900m instead of capping pods, walk through the exact arithmetic for how many app replicas fit - and which event proves the cap was CPU, not pod count.

### Pass bars

- `bootstrap.sh` from a clean host to working `kubectl top pods` in 15 minutes or less, from the frozen commit.
- Live scale-out from 1 to multiple replicas under load, observed in `kubectl get hpa -w` during the demo - no pre-scaled cluster.
- Prediction for the instructor's quota number stated **before** load starts, and the observed stall point matches it (or the discrepancy is correctly explained on the spot from live evidence).
- Quota collision proven from live events/conditions (`exceeded quota`, ScalingLimited), not asserted from memory.
- Scale-in observed live and the stabilization window's role explained; student ID visible in namespace, resource names, and app output throughout.

---

## Project 14 - Service-discovery failure clinic

**Goal.** Build a two-tier app where a web front end reaches a database only by its Service DNS name, then prove you can diagnose and repair name-resolution failures under pressure. You will first demonstrate the healthy path with hard evidence (DNS lookups, Endpoints, resolv.conf), then run a live failure clinic: the instructor breaks one thing from a sealed list, and you diagnose it out loud - predicting what each command will show before you run it - using a written diagnosis tree you authored.

### What you will learn
- How Kubernetes Service DNS actually works: CoreDNS, `/etc/resolv.conf`, search domains, `ndots`, and the four FQDN forms (`db`, `db.<ns>`, `db.<ns>.svc`, `db.<ns>.svc.cluster.local`).
- How a Service maps to Pods via selectors and the Endpoints object, and what "the Service exists but has no Endpoints" looks like.
- How to localize a discovery failure to the correct layer: name, Service, selector, Endpoints, or CoreDNS itself.
- How to diagnose from `kubectl get events`, pod logs, and a debug pod instead of guessing and restarting things.
- How to repair CoreDNS by fixing its ConfigMap and confirming the fix propagates.

### Environment
- kind cluster from a config file committed to git: 1 control-plane + 2 workers, cluster name `clinic-<studentID>`.
- Namespace: `clinic-<studentID>`. All app objects live there. Do not touch `kube-system` except during diagnosis/repair of CoreDNS.
- Images from Docker Hub or GHCR only: a small web image you build and push (any language taught in the course; it must query the db on every request), plus stock `mysql:8` or `postgres:16` for the db, and `busybox:1.36` or `nicolaka/netshoot` for the debug pod.
- Tooling: `kubectl`, `docker`, `kind`, `nslookup`/`dig` inside the debug pod. Nothing else.

### Build requirements
1. Deployment `db-<studentID>` (1 replica) running the database, with labels `app=db, owner=<studentID>`. Seed it via an initContainer or startup script with a table containing at least 5 rows, each row including your `<studentID>` as a column value.
2. Service `db-svc-<studentID>`, type ClusterIP, selecting `app=db, owner=<studentID>`, port 3306 (or 5432). The web tier must reference the db **only** by this DNS name - no IP addresses anywhere in manifests or app code.
3. Deployment `web-<studentID>` (2 replicas) running your image. Each HTTP response must print: your `<studentID>`, the db Service name it connected to, and at least one seeded row. The db hostname must come from a ConfigMap key (`DB_HOST`), not be hard-coded in the image.
4. Service `web-svc-<studentID>`, type NodePort, reachable with `curl` from the host.
5. The web app must fail loudly and informatively: when the db name does not resolve or the connection fails, the HTTP response and pod logs must show the actual resolver/connection error, not a generic 500. Readiness probe must go unready when the db is unreachable.
6. A debug pod manifest `manifests/debug-pod.yaml` (busybox or netshoot, `sleep infinity`) in your namespace, deployed by bootstrap - you will not have time to write it during the clinic.
7. `diagnosis-tree.md` in the repo root: a written decision tree starting from the symptom "web cannot reach db". Each branch must name the exact command to run, what output distinguishes the branches, and which layer it implicates. It must cover at minimum: Service missing/renamed, selector-label mismatch, Endpoints empty (pods down or unready), CoreDNS Corefile corrupted, and "none of the above / network layer". This file is graded.
8. `bootstrap.sh`: from a clean host, creates the kind cluster from the config file, builds nothing at demo time (images already pushed), applies all manifests, waits for readiness, and finishes with a passing `curl` against the NodePort - all in under 15 minutes.
9. Everything in git: kind config, all manifests (raw YAML only), Dockerfile + app source for the web image, `bootstrap.sh`, `runbook.md`, `diagnosis-tree.md`. No Helm, no kustomize overlays required.
10. GitHub Actions workflow that builds and pushes the web image on push to main. The workflow must never contact the cluster.

### Runbook you must write
- How to bootstrap the whole project from a clean host (`./bootstrap.sh`) and verify success (`kubectl get all -n clinic-<studentID>`, `curl` the NodePort).
- How to prove healthy DNS from the debug pod: `kubectl exec` into it, `cat /etc/resolv.conf` (explain each line including `ndots:5`), `nslookup db-svc-<studentID>` plus all three longer FQDN forms, and why the short name works.
- How to inspect the Service-to-Pod chain: `kubectl get svc,endpoints db-svc-<studentID> -n clinic-<studentID> -o wide`, `kubectl describe svc`, `kubectl get pods --show-labels`, and how to compare selector vs labels.
- How to inspect CoreDNS: `kubectl -n kube-system get pods -l k8s-app=kube-dns`, `kubectl -n kube-system get configmap coredns -o yaml`, `kubectl -n kube-system logs -l k8s-app=kube-dns`, and what a healthy Corefile looks like.
- How to repair each failure class in the diagnosis tree: recreate/rename a Service (`kubectl apply -f`), fix a selector or label (`kubectl patch` or edit + apply), restore the Corefile (`kubectl -n kube-system apply` of a known-good ConfigMap kept in `manifests/coredns-known-good.yaml`, then `kubectl -n kube-system rollout restart deployment coredns`), and how to confirm recovery end to end (`nslookup` from debug pod, then `curl` the web NodePort).
- How to read events and logs during diagnosis: `kubectl get events -n clinic-<studentID> --sort-by=.lastTimestamp`, `kubectl logs deploy/web-<studentID>`.

### Submission
- Repo layout: `manifests/` (kind config, all YAML including `debug-pod.yaml` and `coredns-known-good.yaml`), `web/` (Dockerfile + source), `bootstrap.sh`, `runbook.md`, `diagnosis-tree.md`, `evidence/` (healthy-path terminal transcripts captured with `script` or copy-paste, dated).
- Submission = the final commit hash. You present immediately after submitting, in the same session, from exactly that commit on your own host. No edits, no additional commits, no files outside the repo.

### Presentation (starts right after you submit)
1. Clone your frozen commit into a fresh directory and run `./bootstrap.sh`. While it runs, walk the instructor through `diagnosis-tree.md`.
2. Healthy-path evidence: `curl` the web NodePort and show your `<studentID>` and a seeded row. From the debug pod, show `/etc/resolv.conf` and explain `search` + `ndots:5`; run `nslookup` on the short name and the full FQDN; show `kubectl get endpoints db-svc-<studentID>` with populated addresses.
3. Hand the instructor the keyboard, then look away. The instructor breaks exactly ONE item from the sealed list, with randomized parameters, for example: rename `db-svc-<studentID>` to a random string; change the Service selector to a random label value; scale the db Deployment to 0 or break its readiness probe; corrupt the CoreDNS Corefile (e.g. change `forward`, break the `kubernetes` plugin zone, or introduce a syntax error); or delete the Endpoints-producing labels from the db pod template. You do not know which, and the injected names/values differ every time.
4. Take the keyboard back. Confirm the symptom with one command (`curl` the NodePort, or web pod logs) - do not skip this step.
5. Diagnose using your tree, prediction-first: before every command, state out loud what you expect to see if your current hypothesis is right, then run it, then say whether the output confirms or eliminates that branch. Silent typing scores zero for this phase.
6. Repair using only commands documented in your runbook. If the Corefile was corrupted, restore from `manifests/coredns-known-good.yaml` and restart CoreDNS.
7. Prove full recovery: `nslookup` from the debug pod succeeds, Endpoints are populated, and `curl` returns your `<studentID>` and seeded data again.
8. Instructor asks two oral questions from the list below.

### Oral questions to be ready for
1. Your debug pod resolved `db-svc-<studentID>` with the short name, no namespace. Walk through exactly which search-domain suffixes the resolver tried, in what order, and how `ndots:5` decided that.
2. During your clinic, `kubectl get svc` showed the Service present but `kubectl get endpoints` was empty. Name two distinct root causes that produce exactly that pair of outputs, and the single command that tells them apart.
3. If the instructor had corrupted the Corefile instead of what actually broke, what would `nslookup db-svc-<studentID>` from your debug pod have shown, and how would that differ from the renamed-Service symptom?
4. Why did you restart the CoreDNS Deployment after re-applying the ConfigMap - what happens if you fix the ConfigMap but skip the restart, and how long might the broken state persist?
5. Your web pods went unready during the outage. Trace what that did to `web-svc-<studentID>`'s Endpoints and what a client curling the NodePort experienced - and explain why that behavior is what you want.

### Pass bars
- `bootstrap.sh` completes from a clean host in under 15 minutes, ending with a successful `curl` showing `<studentID>` and seeded data.
- Healthy-path DNS evidence is shown live and correctly explained (resolv.conf, ndots, all FQDN forms, populated Endpoints) - reading it without explanation fails.
- The instructor's break is correctly localized to its layer using the diagnosis tree, with prediction-first narration on every diagnostic command.
- The fault is repaired using only runbook-documented commands, and end-to-end recovery (debug-pod nslookup + working curl) is demonstrated within 15 minutes of the break.
- No IP addresses, Helm, or cluster-touching CI anywhere in the repo; all names carry `<studentID>`.

---

## Project 15 - Self-healing and probe tuning

**Goal.** Build a deliberately flaky web app whose boot time and health state you control at runtime, deploy it with a correctly tuned set of startup, readiness, and liveness probes, and prove live that Kubernetes heals it: slow boots are tolerated, wedged pods are restarted, and unready pods receive no traffic. Then run the anti-demo - retune one liveness parameter too tight and show the same, perfectly healthy app driven into a restart loop - and explain exactly why from `kubectl describe` events.

### What you will learn

- What startup, readiness, and liveness probes each actually do, and which failure each one is for.
- How `initialDelaySeconds`, `periodSeconds`, `timeoutSeconds`, and `failureThreshold` combine into a "time to declared dead" budget, and how to compute it.
- How readiness gates Service endpoints so unready pods get zero traffic without being killed.
- How a mis-tuned liveness probe produces CrashLoopBackOff on a healthy app, and how to diagnose that purely from events and restart counts.
- How to predict probe behavior from numbers before applying a manifest - not by trial and error.

### Environment

- kind cluster named `probe-<studentID>` with 1 control-plane + 2 workers, defined in `kind-config.yaml` (committed to the repo).
- Namespace `probes-<studentID>` for everything.
- Your own flaky app image, built from a Dockerfile in the repo and pushed to Docker Hub or GHCR as `<registry>/<user>/flaky-<studentID>:v1`. A small Python (Flask) or Go HTTP server is fine - this is an OPS course, keep the app under ~100 lines.
- A `curl` client pod (`curlimages/curl`) for in-cluster traffic tests.
- GitHub Actions workflow that builds and pushes the image on push to `main`. The workflow never touches the cluster.

### Build requirements

1. **The flaky app.** One HTTP server with these behaviors, all in your repo with the Dockerfile:
 - On boot it sleeps for `STARTUP_DELAY_SECONDS` (env var) before serving anything, simulating a slow start.
 - `GET /healthz` returns 200 with body `ok <studentID>` when healthy; each response also includes the pod hostname.
 - `GET /` returns 200 with body `hello from <studentID> pod=<hostname>`.
 - `POST /wedge` (or `GET /wedge` if simpler) puts the app into a wedged state: `/healthz` now returns 500 (or hangs for `WEDGE_HANG_SECONDS` if set) until the process restarts. The wedge must survive only in process memory - a container restart cures it.
 - `GET /slow-healthz-ms` behavior: `/healthz` takes `HEALTHZ_LATENCY_MS` milliseconds (env var, default 0) to respond, so a tight `timeoutSeconds` can be demonstrated against a healthy app.
2. **ConfigMap** `flaky-config-<studentID>` supplying `STARTUP_DELAY_SECONDS` and `HEALTHZ_LATENCY_MS`. The Deployment must read both from this ConfigMap via `envFrom` or `valueFrom` - no hardcoded values in the pod spec.
3. **Deployment** `flaky-<studentID>`, 3 replicas, with the correct probe set:
 - `startupProbe` on `/healthz`: `periodSeconds: 5`, `failureThreshold` sized so the app survives a boot of at least 120 seconds (show the arithmetic in a comment in the YAML).
 - `readinessProbe` on `/healthz`: `periodSeconds: 5`, `failureThreshold: 2`.
 - `livenessProbe` on `/healthz`: `periodSeconds: 10`, `timeoutSeconds: 3`, `failureThreshold: 3`.
4. **Service** `flaky-svc-<studentID>` (ClusterIP) selecting the Deployment, so readiness-gated traffic can be proven with the curl pod.
5. **The bad manifest.** A second file `manifests/90-bad-liveness.yaml` - the same Deployment with only the liveness probe changed to something indefensibly tight (e.g. `periodSeconds: 1`, `timeoutSeconds: 1`, `failureThreshold: 1`, no startup probe) that will kill healthy pods once `HEALTHZ_LATENCY_MS` or startup delay is nontrivial. Every changed line carries a YAML comment saying what is wrong with it.
6. **Prediction worksheet** `predictions.md` in the repo: a short table you fill in live - columns for startup delay, probe parameter values, computed time-to-kill, and your predicted outcome (Ready / restart loop / never Ready).
7. **Student ID stamping**: `<studentID>` appears in the namespace, every object name, the image tag, and inside every HTTP response body.
8. **bootstrap.sh** at repo root: creates the kind cluster from `kind-config.yaml`, applies all manifests in order, waits for rollout, and finishes with all 3 pods Ready in under 15 minutes from a clean host. It must not apply `90-bad-liveness.yaml`.
9. Everything in git: `Dockerfile`, app source, `kind-config.yaml`, all manifests numbered in apply order under `manifests/`, the workflow under `.github/workflows/`.

### Runbook you must write

- How to bootstrap from a clean host: `./bootstrap.sh`, then `kubectl get pods -n probes-<studentID> -w` until 3/3 Ready.
- How to prove readiness gates traffic: run the curl pod in a loop against `flaky-svc-<studentID>`, wedge one pod, and show with `kubectl get endpoints` / `kubectl get endpointslices` that... it does NOT leave endpoints on wedge (liveness kills it first) versus what happens when you raise `HEALTHZ_LATENCY_MS` - document both observed paths.
- How to wedge a pod: `kubectl exec` or `kubectl port-forward` + `curl -X POST /wedge`, then watch liveness restart it - `kubectl get pods -w`, `kubectl describe pod` (the `Liveness probe failed` and `Killing` events), `kubectl get pod -o jsonpath='{.status.containerStatuses[0].restartCount}'`.
- How to change the startup delay: `kubectl create configmap ... --dry-run=client -o yaml | kubectl apply -f -` (or edit + apply), then `kubectl rollout restart deployment/flaky-<studentID>` and `kubectl rollout status`.
- How to compute time-to-kill from any probe parameter set: the formula (`initialDelay + failureThreshold × periodSeconds`, plus how `timeoutSeconds` interacts with a slow endpoint) with one worked example.
- How to run the anti-demo: apply `manifests/90-bad-liveness.yaml`, watch CrashLoopBackOff develop, and read the cause from `kubectl describe pod` and `kubectl get events -n probes-<studentID> --sort-by=.lastTimestamp`.
- How to recover: `kubectl apply -f manifests/30-deployment.yaml` (the good spec) and confirm rollout returns to 3/3 Ready.

### Submission

- Repo layout: `app/` (source + Dockerfile), `manifests/` (numbered YAML, including `90-bad-liveness.yaml`), `kind-config.yaml`, `bootstrap.sh`, `runbook.md`, `predictions.md`, `.github/workflows/build.yml`, `evidence/` (terminal transcripts from your own dry runs - `script` or copy-paste, not screenshots).
- Submission = the final commit hash. You present immediately after submitting, in the same session, from exactly that commit on your own host. No edits, no additional commits, no "one-second fix" after the hash is frozen.

### Presentation (starts right after you submit)

1. `git clone` your repo at the frozen commit onto your host (or `git checkout <hash>` in a clean directory) and run `./bootstrap.sh`. While it runs, walk through the three probes in your Deployment YAML and state each one's job in one sentence.
2. Show all 3 pods Ready, then start the curl loop from the client pod and show responses containing `<studentID>` and rotating pod hostnames.
3. **Self-healing demo**: wedge one pod via `/wedge`. Narrate the events as liveness fails 3 times, the container is killed and restarted, restart count increments by exactly 1, and the pod returns to Ready. Show the curl loop never returned an error.
4. **Slow-start demo**: set `STARTUP_DELAY_SECONDS=90` in the ConfigMap, rollout restart, and show the startup probe holding fire - pods stay `Running 0/1` with zero restarts until boot completes, and old pods keep serving (readiness gating) throughout.
5. **The twist**: the instructor now dictates two numbers - a new `STARTUP_DELAY_SECONDS` (anywhere 0-300) and one probe parameter change (e.g. "liveness `timeoutSeconds: 1` with `HEALTHZ_LATENCY_MS=2000`", or "remove the startup probe with delay 180", or "readiness `failureThreshold: 1`"). Before applying anything, fill in a row of `predictions.md` live: compute the time-to-kill and state the predicted outcome out loud (Ready in N seconds / CrashLoopBackOff / never Ready but never killed).
6. Apply the instructor's values and watch. Compare observed behavior against your prediction; if they differ, explain why from the events.
7. **Anti-demo**: reset to sane config, confirm 3/3 Ready and the app answering, then apply `90-bad-liveness.yaml`. Show a healthy app entering CrashLoopBackOff, and prove the cause from `kubectl describe pod` events - point at the exact `Liveness probe failed` lines and the growing backoff.
8. Recover by re-applying the good Deployment, show 3/3 Ready, and state in one sentence the rule of thumb for sizing a liveness probe against worst-case response time.

### Oral questions to be ready for

1. In your wedge demo, why did the wedged pod get restarted rather than just removed from the Service endpoints - and what one change to your probe config would flip that outcome?
2. Your app takes 90 seconds to boot. Walk me through the exact arithmetic that proves your startup probe tolerates it, and what would happen second-by-second if you deleted the startup probe but kept your current liveness probe.
3. During the anti-demo the pods showed CrashLoopBackOff even though `/` returned 200 the whole time. Which specific event lines told you the probe, not the app, was at fault?
4. Why must the wedge state live only in process memory? What would break in your self-healing demo if the wedge were written to a file on an emptyDir volume - and if it were on a hostPath?
5. When you changed `STARTUP_DELAY_SECONDS` in the ConfigMap, why did you need `kubectl rollout restart` - why didn't the running pods pick up the new value?

### Pass bars

- `bootstrap.sh` reaches 3/3 Ready pods on a clean host in under 15 minutes, with no manual intervention.
- Wedging a pod produces exactly one container restart, full recovery to Ready, and zero failed requests in the concurrent curl loop.
- With a 90+ second startup delay, pods reach Ready with restart count 0 - any startup-phase restart is a fail.
- The anti-demo drives a demonstrably healthy app into CrashLoopBackOff, and the student identifies the cause from live events without consulting notes.
- The twist prediction is committed out loud (with the arithmetic) before applying, and any mismatch with observed behavior is correctly explained from events.
