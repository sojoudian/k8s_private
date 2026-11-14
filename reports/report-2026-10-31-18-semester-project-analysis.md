# Report: Semester Project Deep Analysis
**Date**: 2026-10-31
**Sequence**: #18 for the day

## Summary
The user said "analyze it 100% deep deep deep and understand it 100%". This pass is read-only. I read all 17 `_v2` project documents line by line. I then checked them against the Week 04 and Week 05 code, GitHub, Docker Hub, the syllabus, the decks, the labs, the 8 Summer grading reports and official documents.

**Result: 0. The project is not ready for release on Wednesday 2026-11-04.** The main facts:

- `sojoudian/clo835-mirrors` does not exist on GitHub. 10 of 16 projects fail at install.
- 0 of 16 projects have run on kubeadm. The Summer submissions all used kind.
- 3 sources give 3 different dates for the project.
- 13 defects make a rubric line false or impossible.
- 2 of 16 projects (11 and 14) have no blocker and no such defect.

## What Changed
- New: this report.
- New: memory `project-clo835-semester-project.md`, with a pointer in `MEMORY.md`.
- Changed: memory `project-no-eks-in-educate.md`, one correction line.
- No project file changed. No AWS resource. No commit. No push. No browser action.

## Technical Details

### 1. What the project is
The syllabus name is Final Project, weight 20%. A student must get 50% or better on it to pass the course, and must complete it. The documents call it Semester Project.

Each student builds one real system alone, on a personal Week 05 kubeadm cluster, and defends it live. The design resists AI help in 5 ways:

- The student ID goes into names and data.
- The live twist cannot be rehearsed exactly.
- The student states a prediction before each command, and the prediction gets marks.
- The professor asks individual oral questions.
- The git history shows the work over time.

**Life cycle of one project:**
1. The student claims a project by email or in class, first come, first served. No two students share a project.
2. The student may propose a new subject or a change. Approval comes first.
3. The student builds one GitHub repository: `manifests/`, `bootstrap.sh`, `runbook.md`, `evidence/`, `README.md`.
4. `bootstrap.sh` must go from a fresh Week 05 cluster to the full system in 15 minutes or less, with no manual step.
5. The student gives one commit hash. The repository is then frozen.
6. The student presents in person in the same session, from that commit: 10 minutes, no slides, one twist, then the oral questions.

**Rubric (the same in all 16 projects):**

| Part | Points |
|---|---|
| Implementation and runbook | 25 |
| `bootstrap.sh` in 15 minutes or less | 15 |
| Live demo, twist and prediction narration | 35 |
| Individual oral questions | 25 |

Each project also has 5 or 6 pass bars. One missed bar caps the grade at 60.

**Hard rules (all projects):** raw YAML and kubectl only. No Helm, no kustomize, no EKS, no managed AWS service. Images come from Docker Hub or GHCR. GitHub Actions may only build and push.

### 2. History
| Date | Event |
|---|---|
| 2026-07-06 | `Semester_Project_Ideas.md`: 5 team projects on EKS and Cloud9. The user rejected EKS and Helm. |
| 2026-07-08 | 15 individual specifications on kind, the overview, the 10-minute alignment, then Project 16 from one student proposal. |
| 2026-07-28 to 30 | 8 Summer projects graded. All ran on kind. |
| 2026-10-27 | `_v2` of all 17 files moved to kubeadm by text replacement (report #09 of that day). Report #09 says "Not tested live". |
| 2026-10-31 | This analysis. |

**Summer grades, by project:**

| Project | Grade | Note |
|---|---|---|
| 3 | 99 | |
| 16 | 84 | 60 if the cap is enforced. The professor had the decision. |
| 13 | 100 | |
| 10 | 90 | The report summary still says 100. |
| 4 | 100 | |
| 14 | 90 | The report summary still says 100. |
| 12 | 100 | |
| 7 | 100 | |

The mean is 95.4. The professor gave full presentation marks, with minus 10 on 2 projects. These grades prove the kind design only. They prove nothing about kubeadm.

### 3. The 16 projects
| # | Project | Idea | Twist | Mirror file needed |
|---|---|---|---|---|
| 1 | MySQL StatefulSet failover | 3 pods, async replication, manual promotion | Professor deletes any pod during writes | local-path |
| 2 | MongoDB replica set | Automatic election, majority writes | Marker insert, then kill within seconds | local-path |
| 3 | PostgreSQL streaming | Primary and hot standby, LSN lag | Professor writes rows, then orders promotion | local-path |
| 4 | Redis with Sentinel | Quorum 2, automatic failover | Method of master kill, then a Sentinel kill | None |
| 5 | Backup and restore | CronJob, keep last 7, exact restore | Professor picks the backup, student predicts lost rows | local-path |
| 6 | Two-cluster migration | Freeze, dump, `kubectl cp`, restore, SHA256 | Professor inserts unknown marker rows | local-path |
| 7 | Zero-data-loss upgrade | Broken migration, rollback is not restore | 1 of 3 failure moments | local-path |
| 8 | Node maintenance drill | hostPath against NFS during a drain | Professor names the worker | None |
| 9 | NFS shared storage | RWX over an in-cluster NFS server | Writer kill, then scale to 2 writers | local-path |
| 10 | Mini multi-tenant | RBAC, ResourceQuota, LimitRange | 1 fault from a pool | None |
| 11 | RBAC personas, break-glass | 3 identities, test suite | 1 of 4 RBAC breaks | None |
| 12 | Secrets rotation | Rotate with 0 failed requests | Rollback, or forced v3 | local-path |
| 13 | HPA under load | Quota collides with HPA | Professor names the quota | metrics-server |
| 14 | Service-discovery clinic | Diagnosis tree | 1 break from a sealed list | None |
| 15 | Self-healing, probes | Probe arithmetic, restart loop | Professor sets delay and probe value | None |
| 16 | Async orchestration, KEDA | Queue, scale to 0, Jobs by API | Quota value, then a worker kill | KEDA |

### 4. Class A: stops the release
**A1. The mirror repository does not exist.** [tested]
- All 16 project files name `sojoudian/clo835-mirrors`, 21 times in total.
- The 3 URLs return 404. `git ls-remote` says "Repository not found", with the local git login.
- Report #09 of 10-27 listed this as "Still blocking". The issue is still open.
- 10 projects fail: 8 that need a PVC (1, 2, 3, 5, 6, 7, 9, 12), plus 13 and 16.
- The overview says that a project that does not come up from a clean clone "cannot be graded". The syllabus requires the project to pass the course.
- **The only copy is in `/private/tmp`**, in the scratchpad of session `0b02113e`: 3 commits, no remote. All 3 named files are there. A system clean-up can delete `/private/tmp`.
- 2 of the 3 files are already public in the course repository, and both URLs return 200:
  - `Week07/local-path-storage.yaml`. It is byte-identical to the mirror file.
  - `Week14/metrics-server.yaml`. It has `--kubelet-insecure-tls`, so Project 13 needs no patch for that flag.
- `keda-2.21.0.yaml` (782 KB) has no public copy.
- All required `maziar` images exist on Docker Hub with the named tags.

**A2. Three sources give three dates.** [read]

| Source | Release | Due or present |
|---|---|---|
| Syllabus | 11/4 | Due 11/25 (Week 13) |
| Week 09, 10, 12, 13 decks; the user on 10-31 | none | Present in Weeks 14 and 15 (12/2, 12/9) |
| `Week14_lecture_style_v11.pptx` slide 3 | none | Present in Weeks 13 and 14 |
| Overview and all project files | none | No date. They say "before the project due date". |

**A3. The list does not match the folder.** [read]
- The overview says 15 projects and "Project_01 through Project_15". The folder has 16 projects.
- Project 16 is the design of one Summer student. It refers to "the proposed design" and to "the diagram". The file has no diagram.
- The folder holds the v1 files too, and the v1 files say kind. A student who gets the whole folder sees 34 files.
- The claim table in the overview is empty.

**A4. Project 1 promises a file that does not exist.** [read]
The text says "The instructor will provide a reference" for the init-container scripts. I found no such file.

### 5. Class B: 13 defects in one project
Each item makes a rubric line, a pass bar or a demo step false or impossible.

| # | Project | Text | Fact | Evidence |
|---|---|---|---|---|
| 1 | 3 | Task 12 and the runbook require the `promote_trigger_file` method. The image is `postgres:16`. | PostgreSQL 16 removed this variable. `pg_promote()` stays. | document |
| 2 | 3 | Runbook: `kubectl exec ... -- pg_ctl promote` | `kubectl exec` is root in the official image, and `pg_ctl` refuses root. | knowledge, not run |
| 3 | 4 | Twist option: `redis-cli DEBUG SLEEP 60` | Redis 7 blocks DEBUG by default. No task enables it. | document |
| 4 | 5 | Pass bar: weekly dumps "spanning the term". The example is `week05-entry`. | A release on 11/4 leaves 4 or 5 weeks. A strict grader must cap each student at 60. | logic |
| 5 | 7 | Twist (b): kill the Job "partway through the copy" | The SQL ends in milliseconds, and the task has no delay. The Summer student added `SLEEP 15`. The Job also restarts the pod, because no task sets `backoffLimit: 0`. | Summer report, logic |
| 6 | 8 | "comes back empty on a new node"; "empty file if it lands on the labeled node" | The nodeSelector allows 1 node only. After uncordon the pod returns to the same disk, and the file is intact. Only Pending is possible. | logic |
| 7 | 8 | Pass bar: any worker drain keeps every row, and counts increase. Runbook: data is lost with ephemeral NFS storage. | The two lines conflict. Task 3 gives the server no storage rule. | logic |
| 8 | 8, 9 | `bootstrap.sh` installs `nfs-common` "over SSH with your Week 05 key" | The script runs on the master, and the master has no key. The clean run of the professor uses another key. | code |
| 9 | 10 | Tenant c is half of `pods=5, secrets=5` | Half of 5 is 2.5. The Summer student rounded to 3. | logic |
| 10 | 13 | Pass bar and runbook: quota proof shows `ScalingLimited` | That condition reports the HPA minimum or maximum only. A quota does not set it. The real proof is `FailedCreate` and `exceeded quota`. | document |
| 11 | 13 | Task 6 says 60-300 s. Demo step 7 says 15-30 s. | One frozen commit cannot do both. | read |
| 12 | 13 | Service `<studentID>-burn-svc` | A Service name cannot start with a digit, and Seneca IDs can be 9 digits. A Summer student used an `s` prefix. | Summer report |
| 13 | 15 | Runbook: the wedged pod "does NOT leave endpoints (liveness kills it first)" | By the numbers of the task, readiness fails in about 10 s and liveness in about 30 s. The pod leaves first. | logic |

### 6. Class C: rules that conflict across projects
1. **Time bars do not fit the demo.** The presentation is 10 minutes, but recovery bars allow 10 minutes (Projects 1, 6, 7, 11) and 15 minutes (Project 14).
2. **Project 15 does not fit.** 3 replicas with a 90 s boot need about 5 minutes for one rollout, because the default strategy replaces one pod at a time. The twist allows 300 s, which is about 15 minutes.
3. **A failed bootstrap has three results.** The overview says "cannot be graded". The pass bars say cap at 60. Project 3 says "if bootstrap fails live, that is the grade", but the presentation forbids a live bootstrap.
4. **The freeze date differs by slot.** Submission happens at the presentation, so a student on 12/9 has 7 more days than a student on 12/2.
5. **The AI rule conflicts.** The pledge says "all work will be my own". Project 7 says an AI-generated app "is fine". The overview has no AI rule. A Summer student declared AI use, and the question stayed open.
6. **Student ID has no definition.** The examples are user names (`jdoe12`). Summer students used both user names and 9-digit numbers.
7. **Password prompts were graded two ways.** Summer Project 14 prompted with no penalty. Project 16 prompted and lost marks. A general rule is missing: generate each password in `bootstrap.sh`.
8. **The overview omits key facts:** the 20% weight, the 50% pass rule, the place to submit, and the due date.
9. **Words:** "instructor" 171 times and "professor" 6 times; "workstation" 8 times and "laptop" 1 time; "Semester Project" in the documents and "Final Project" in the syllabus. `bootstrap.sh` also names a different file in the Week 05 folder.
10. **Language:** the documents are not in ASD-STE100. My script finds 208 of 3,027 sentences over 25 words, and the longest has 61.
11. **Leftovers from the move to kubeadm:**
    - Project 1 still says "the provisioner that kind uses". The "kind is gone" claim in report #09 of 10-27 is false for this line.
    - Project 6 outline still says "30 minutes before cutover".
    - The hard rule in Project 6 says one cluster, but the project uses two.
    - `Semester_Project_Ideas_v2.md` still says EKS, Cloud9, teams and Helm. It is internal, and it must not go to students.

### 7. Class D: risks
These items are not text errors. No test has proved them.

| Project | Risk |
|---|---|
| All | **0 of 16 have run on kubeadm.** The Summer speed of 87 to 123 s was on kind. |
| 1 | The bar demands zero lost rows on async replication. Physics does not guarantee this. Project 3 accepts loss and demands an exact count. |
| 4 | "Must contain exactly" conflicts with a DNS master name, because `sentinel resolve-hostnames yes` is off by default. |
| 4 | The drain twist can remove 2 of 3 Sentinels at once. A Summer run on 2 workers passed. |
| 6 | Both `admin.conf` files use the same cluster and user names, so a merge of the two loses one. |
| 8, 9 | The NFS image may need `modprobe nfsd` on the host. This is not tested on the Ubuntu 26.04 kernel. |
| 8, 9 | With 2 workers and a local-path disk, a drain of the NFS node stops the share until uncordon. In Project 9 the twist can drain the writer node. |
| 9 | The RWO demo teaches the wrong cause. The conflict pod is Pending from PV node affinity. RWO allows 2 pods on one node. |
| 10 | `kubectl apply` does not remove a key that someone added by edit, for example `services: "0"`. The documented repair fails for this fault. `kubectl replace` works. |
| 12 | `failed=0` with a pod kill needs a `preStop` delay. No task asks for it. One failed request caps the grade. |
| 16 | The KEDA list holds waiting jobs only (my inference, not checked in the BullMQ documents). Scale to 0 can then stop active jobs. The Summer student used a minimum of 1. |
| Base | Weeks 04 and 05 apply the latest Flannel from `flannel-io`, not pinned and outside the account rule. |
| Base | The join token is fixed and public, and port 6443 is open to the internet. Project clusters stay up longer than lab clusters. |

**Skills that the projects need and the course does not teach.** This is a text search of the decks and `localMachine.sh` files. It cannot see text inside images.

| Skill | Hits in decks and labs | Projects |
|---|---|---|
| Readiness, liveness, startup probes | 0 | 12, 14, 15 |
| ResourceQuota, LimitRange | 0 | 10, 13, 16 |
| `kubectl cp` | 0 | 6, 7 |
| `mysqldump` | 0 | 1, 5, 6, 7 |
| `kubectl create token` | 1, in an old lab only | 10, 11 |
| CronJob | 1 mention, no lab | 5 |
| Anti-affinity | 1 mention, no lab | 3, 9 |
| Database replication | text only, no lab | 1, 2, 3, 4 |

**Taught late against the first presentation on 12/2:** Secrets on 11/18, RBAC on 11/25, HPA on 12/2. Students must work ahead on Projects 10, 11, 12 and 13.

**Presentation capacity.** 13 students times 15 minutes (10 for the demo, and my assumption of 5 for the oral) is 195 minutes. The in-person Wednesdays 12/2 and 12/9 give 210 minutes. This leaves 15 minutes for the HPA lecture and all changeovers. The Friday class is online, and the overview says in person.

**Clean-run load for the professor.** The lab allows 3 clusters at once. One cycle takes at most 19 minutes: 2 to build, 15 for `bootstrap.sh`, 2 to destroy. 13 repositories need 5 rounds, so 95 minutes at most. The build and destroy times come from the Week 13 live log.

### 8. Facts confirmed as good
- Weeks 04 and 05 differ only in names, so 2 clusters can run together.
- The 6 machines of Project 6 are under the limit of 9. This closes the doubt in report #09.
- Port 6443, the NodePort range and the certificate SAN for the public IP are correct in `Week05/main.tf` and `master-init.sh.tftpl`.
- All official image tags in the documents exist on Docker Hub. The account rule keeps Docker Official Images.
- A Week 13 cluster built from `terraform apply` to 3 Ready nodes in about 2 minutes. `terraform apply` for cluster b during the Project 6 demo is therefore possible, but tight.
- The Markdown source holds Projects 1 to 15, and Project 16 is only in Word. The original generator (`gen_projects.js`, `projects.json`) is gone. `retarget_docx.py` and `retarget_kind_docx.py` remain.

### 9. Recommended order
This is a recommendation only. Nothing is done.

1. Copy the mirror folder out of `/private/tmp`.
2. Set the dates, the freeze rule and the slots.
3. Point Project files at the two public course files, in new `_v3` files. Decide whether Project 16 is offered. If it is, publish the KEDA file.
4. Apply the 13 Class B fixes and the Class C rules, in ASD-STE100.
5. Build one PVC project, one NFS project and Project 13 on a live cluster. These 3 test the highest risks.
6. Publish `_v3` only, with the instructor material of Projects 1, 6, 10 and 14 ready.

## Results
| Check | Result |
|---|---|
| Documents read line by line | 17 of 17 `_v2` |
| Mirror URLs | 3 of 3 return 404 |
| Projects that fail at install | 10 of 16 |
| Projects run on kubeadm | 0 of 16 |
| Class A items | 4 |
| Class B defects | 13 |
| Class C conflicts | 11 |
| Class D risks | 13 in the table, plus 4 course-level findings |
| Projects with no Class A or B item | 2 (Projects 11 and 14) |
| Local server port | None. No server ran. |

## Issues / Notes

**Evidence labels.** "tested" means a command ran today. "document" means an official source. "logic" means a result from the numbers in the specification. "knowledge" means no test and no source. "read" means the text itself.

**Limits of this pass:**
- No cluster ran. I used no AWS and no Docker. Each kubeadm behavior here is reasoned, not observed.
- I did not read Blackboard. I do not know what is posted, or whether students have already claimed a project.
- I compared v1 and v2 by line counts and the report of 10-27, not line by line.
- I matched `Semester_Projects_Individual_v2.md` to the Word files by script. I did not read all of it.
- I did not view the layout of the Word files.
- I did not read the Summer student repositories again. I used the grading reports.
- The skill table cannot see text inside images. Check it before you rely on a 0.
- `gh` has no login on this computer, so I could not look at private repositories with it. `git ls-remote` used the local git login and found nothing.

**Sources:**
- [PostgreSQL 16 release notes](https://www.postgresql.org/docs/release/16/)
- [Kubernetes HPA walkthrough](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/)
- [Redis Sentinel documentation](https://redis.io/docs/latest/operate/oss_and_stack/management/sentinel/)
- [Redis 7 DEBUG error report](https://github.com/redis/redis-rb/issues/1113)
- [Disable dangerous Redis commands](https://oneuptime.com/blog/post/2026-03-31-redis-disable-dangerous-commands-production/markdown)
- [KEDA Redis Lists scaler](https://keda.sh/docs/2.21/scalers/redis-lists/)
- [nfs-server-alpine on Docker Hub](https://hub.docker.com/r/itsthenetwork/nfs-server-alpine)
- [Fork of nfs-server-alpine with the modprobe note](https://hub.docker.com/r/d0whc3r/nfs-server-alpine)
