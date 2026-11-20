# Report: Week 13 to lecture v10 and lab v6, the running loop report
**Date**: 2026-11-18
**Sequence**: #08 for the day

## Summary
This is the state file of the `/loop` that brings Week 13 (Authentication, RBAC and EKS) to lecture v10 and
lab v6, 100 % to `CLO835_STANDARDS.md` v1.2. Each run does one phase and updates this report. Run 1 stopped
at the session check, because the old AWS Academy session had ended. Run 2 (new session) did phase 0.

## Loop state
| Item | Value |
|---|---|
| AWS session first seen | 2026-11-18 23:00 EST (the time of the new credentials file; role voclabs, us-east-1) |
| Stop the AWS work by | 2026-11-19 02:30 EST (3.5 h) |
| Phases done | 0, 1 (5 lecture, 2 lab, 4 quiz items; 0 MUST-FIX), 2 (all 9 SHOULD-FIX applied), 3 (all gates pass), 4 (pass 1: 0 unplanned non-zero exits; 20 of 20 keys proven) |
| Phase 5 | pass 2: 0 unplanned non-zero exits; gate with the live folder GATE 1 (156 PASS); 15 destroyed; 0 instances |
| Round 1 | lecture 6/8, lab 0/3, quiz 5/7 (MUST/SHOULD), all applied with P1 and P2 |
| Phase 3 after round 1 | all gates pass (lecture and lab FAILED: 0, lab gate v3 GATE 1 with the live folder, quiz audit 0 errors, cue PASS) |
| Probe run after round 1 | the new Q5 proven live (probe13b.log); 15 added, 15 destroyed; 0 instances |
| Round 2 | lecture 4/8, lab 0/4, quiz 1/5 (MUST/SHOULD), all applied; no command changed |
| Phase 3 after round 2 | all gates pass |
| Probe run after round 2 | Q16 proven with dev-user; a third full pass of the final commands (35 exit 0, 4 planned denials); 15 destroyed; 0 instances |
| Round 3 | lecture 3/7, lab 0/0, quiz 1/3 (MUST/SHOULD), all applied; no command changed; the phase 3 checks pass |
| Stop | 02:49 EST: the AWS session is 3 h 49 min old (limit 3.5 h); 0 instances; the user must restart the lab |
| Next phase | 6 (review round 4: three fresh independent reviewers), in a new lab session |
| After the stop | the user chose (2026-11-19, about 01:25 EST): finish the Week 13 loop first, then start the Week 14 loop |
| Open findings for the next fix | P1 (quiz, Q12 feedback), P2 (lecture samples): text only, no command changes |
| Clusters of this loop that run now | none |

## What Changed
Run 1 (22:52 EST): this report. No other change.

Run 2 (phase 0, 23:02 to 23:06 EST):
- Fixed the old path `/Users/maziar/Downloads/k8s_week3` to `/Users/maziar/Documents/c/r/k8s_private` in
  `quiz_pool_src/audit_easy20_w13.py` (1 line, line 12).
- No clone: `~/Documents/c/r/CLO835_Fall_2026` exists.
- AWS: no change (nothing of an old Week 13 test remains).

## Technical Details

### Run 1: the session check (22:52 EST)
- `aws sts get-caller-identity` gave exit 0, and the Arn was `assumed-role/voclabs`.
- The credentials file had the time 17:42 EST, so the session was 5 h 10 min old (limit 3.5 h).
- `ec2 describe-instances` and `ec2 describe-security-groups` gave `UnauthorizedOperation`, from an explicit
  deny of the policy `voc-cancel-cred`. The session had ended.
- The loop had no cluster, so there was nothing to destroy. The run stopped and asked for a new lab session.

### Run 2: phase 0 (preflight)
Session check:
- `aws sts get-caller-identity`: exit 0, Arn `assumed-role/voclabs`, region `us-east-1`.
- The credentials file has the time 23:00:48 EST, so the session is 2 min old.

The repo:
- `~/Documents/c/r/CLO835_Fall_2026`: HEAD `7c4d9b8` ("add week12"). The only change is
  ` M Week12/localMachine.sh` of the Week 12 loop (no commit).
- `Week13/` has 7 files (with `.gitignore`). `Week13/localMachine.sh` is byte-equal to
  `Week13/localMachine_v5.sh`.

The old path:
- Of the Week 13 chain, only `quiz_pool_src/audit_easy20_w13.py` named the old path (the folder of the
  upload files). `build_week13_lecture_v9.py`, `build_week13_lab_v5.py`, `build_easy20_w13.py`,
  `q_easy20_w13.py` and `tools/` have no old path. `tools/rungate.py` and `tools/deck_pipe.sh` are fixed
  since report #06.

AWS inventory (us-east-1):
- Instances in any state: 0.
- Security groups: only `default`.
- Elastic IP addresses: 0.
- So no old Week 13 test object remains, and nothing was terminated.

### Baseline (lecture v9, lab v5 and quiz v1, before any change)
The deck gate ran with `tools/rungate.py` only. `tools/deck_pipe.sh` was not used, because it exports the
PDF again and would overwrite the v9 and v5 PDF files.

| Check | Result |
|---|---|
| Deck gate `Lecture_week13_v9` (lecture) | FAILED: 0 |
| Deck gate `Lab_week13_v5` (lab) | FAILED: 0 |
| Quiz audit `Quiz_W13_Easy20` | errors 0; 20 rows; keys 5 A, 5 B, 5 C, 5 D; longest run of one letter 2; answer leaks 0; pairs at risk 0; 20 key records; ZIP 21 files (20 items); 20 titles |
| Quiz length guesses | longest 4 of 20, shortest 4 of 20, most words 3 of 20; with ties shared: longest 4.5, shortest 4.5 |
| Cue simulation | PASS; highest: middle length 5.50 of 20, most words 5.17 of 20 (limit 6.0) |

The other lines of the cue simulation: always A, B, C or D 5.00; convergence 3.67; convergence (stemmed)
3.33; fewest words 4.83; longest 4.50; odd one out 3.00; shortest 4.50; stem overlap 2.50.

Facts for the next phases:
- The current versions: `Lecture_week13_v9` (v8 also exists), `Lab_week13_v5`, `localMachine_v5.sh`,
  `Lab_week13_Blackboard_Submission_v5.md`, `quiz_pool_src/q_easy20_w13.py` and `Quiz_W13_Easy20/`.
- The syllabus row of 11/25: "Securing K8s API: introduction to RBAC in Kubernetes and Amazon EKS",
  Part 3, Chapter 12, Section 1 and part of Section 2, Optional Lab 10 (2.5%), Final Project due date (20%).
  The row has no quiz.
- The lab uses the kubeadm cluster of Terraform. EKS is a concept only, and the quiz has an EKS question.

### Phase 1: the audit (run 3, 23:05 to 23:30 EST, read-only)
Read:
- `Lecture_week13_v9.pptx` (32 slides) and `Lab_week13_v5.pptx` (10 slides), with `prs.slides`;
- `localMachine_v5.sh`, `Lab_week13_Blackboard_Submission_v5.md`, `Quiz_W13_Easy20` (20 questions) and
  `q_easy20_w13.py`;
- `CLO835_STANDARDS.md` Parts A to G, `~/.claude/PREFERENCES.md` (sections 6, 14, 15), the headings of
  `PROMPT.md` and `DESIGN_LANGUAGE.md`, and the syllabus row of 11/25;
- the reports of 2026-11-11 (#02, #03) on Week 13.

Tools (read-only):
- `gate_week13_v2.py Lab_week13_v5 Lab_week13_Blackboard_Submission_v5.md` (no live folder): GATE 1,
  0 failed. Its F4 table has one item that the lecture answers, not the lab: section 3, "the order of the
  three phases of a request".
- The 10 reference links of slide 32: all return HTTP 200.
- A word count over the 20 questions: no word is in 3 or more wrong options and in no key; no word is in 2
  or more keys and in no wrong option.

Facts checked on the documentation (v1-35.docs.kubernetes.io, docs.aws.amazon.com). All are true:
- the certificate revocation (none in v1.35), the minimum `expirationSeconds` of 600, no auto-approval
  for `kubernetes.io/kube-apiserver-client`;
- admission control does not act on a read; the authentication configuration file is stable in v1.34;
  `--authorization-config` is stable in v1.32;
- `--authorization-mode` "Defaults to AlwaysAllow if --authorization-config is not used";
  `--anonymous-auth` defaults to true;
- "The healthz endpoint is deprecated (since Kubernetes v1.16)";
- system:masters bypasses "any authorization restrictions imposed by the RBAC or Webhook mechanisms";
- the default roles of `system:authenticated`: `system:basic-user`, `system:discovery` and
  `system:public-info-viewer`;
- EKS: "EKS access entries are the best way to grant users access to the Kubernetes API"; "The aws-auth
  ConfigMap is deprecated"; "Once the access entry method is enabled, it cannot be disabled";
  `bootstrapClusterCreatorAdminPermissions` "The default value is true"; the creator in the mode
  `CONFIG_MAP` "doesn't appear in any visible configuration"; the token TTL is 15 minutes; two ways attach
  permissions to an access entry; the best-practices guide calls the removal of the creator access a best
  practice.

What passes:
- B1 to B6 by the gate (FAILED: 0 in phase 0).
- B7: the slide set (cover, agenda, Course Outline with Week 13 "RBAC and EKS", four parts, Summary,
  Optional Topics, Key Takeaways, "Lab Week 13 at a Glance", References). The facts above.
- The syllabus topics of Part 3, Chapter 12, Sections 1 and 2: users and groups, ServiceAccounts, their
  creation and their assignment to a Pod, the API call with the token, the RBAC plugin and its four
  objects, Roles and RoleBindings, ClusterRoles and ClusterRoleBindings (also for paths), the default
  ClusterRoles, least privilege, and Amazon EKS. The image pull Secrets of a ServiceAccount are in the
  Week 12 v8 lecture (slide 19).
- C1: 10 slides with the right titles; Steps 0 to 6; 39 commands on the master (limit 40).
- C3: the images `maziar/kubia:v1` and `maziar/alpine-curl` only; `kubectl wait` for curl-sa; each
  manifest with `<<'EOF'`, and the one exception (`<<EOF` for the CSR) has its reason in a comment.
- C5: 7 files; `localMachine.sh` = `localMachine_v5.sh`; the gate checks the repo text.
- C7: the title, "all 7 sections", the recording paragraph, sections 1 to 7, `You must:`, Explain items
  last, six Submission Requirements, the Important paragraph, no pledge, "master node",
  "control-plane Pods".
- C8: each terminal labeled "Lab Week 13, Step M" (slides 9, 11, 12, 16, 17, 22, 23) holds only commands
  of that step; the four manifests are identical to the lab files.
- D: keys 5 A, 5 B, 5 C, 5 D; the audit and the cue simulation pass; each key is correct in my reading.

Defects (the input of phase 2):

| ID | Part | Rule | Defect | Class |
|---|---|---|---|---|
| L1 | Lecture | B7 | Slide 5: "Each request to the API server has three phases" and "After the three phases, the API server stores the object in etcd". The same slide says that admission control acts only on a write, and only a write stores an object. | SHOULD-FIX |
| L2 | Lecture | B7 | Slide 20: "Outside kube-system, a new ServiceAccount has only the API discovery permissions". The documentation says: no permission beyond those of all authenticated users. These are `system:discovery`, `system:basic-user` (for example `auth whoami`) and `system:public-info-viewer`. The lab comment "Every authenticated user can run auth whoami" names a permission that is not discovery. | SHOULD-FIX |
| L3 | Lecture | B7, C8 | Slide 31 names topics that are not in the lab, but their slides have no "Concept only" label: slide 5 (the answer 401), slide 6 (the prefix `system:`), slide 8 (the minimum lifetime, the revocation), slide 15 (no deny rule; the verbs watch, patch, deletecollection; update; configmaps), slide 17 (nodes and paths in a ClusterRole), slide 18 (system:masters, kubeadm:cluster-admins, the health paths), slide 20 (another namespace, a change of `serviceAccountName`, the permissions of a new ServiceAccount). | SHOULD-FIX |
| L4 | Lecture | B7 | Slide 31 repeats "Also not in the lab:" in five paragraphs (the Week 12 defect L5). Make one list, with one line for each part. | SHOULD-FIX |
| L5 | Lecture | A5, C8 | `build_week13_lecture_v9.py` imports `build_week13_lab_v5`, and its paths are `week13/`. The v10 builder must import the v6 lab, and use `Week13/` (the A5 names). | SHOULD-FIX |
| L6 | Lecture | C4 | The sample outputs on slides 9, 11, 12, 16, 17, 22 and 23 come from the run of 2026-11-11 (for example `notAfter=Nov 12 05:27:22 2026 GMT`, the credential-id hash, `"resourceVersion": "670"`). Compare them with the output of phase 4. | check |
| B1 | Lab | C3, C4, C9, E3 | No live pass of lab v5 or of lecture v9 exists (report #03 of 2026-11-11: "The live tests are NOT done"). | phases 4 and 5 |
| B2 | Lab | A5 | The `build_week13_lab_v5.py` docstring says that it stops when an output exists, but the guard does not check the repo folder (the Week 12 finding R3-1). The v6 docstring must say so. | SHOULD-FIX |
| B3 | Lab | C1 | 39 of 40 commands. A new topic must fold into an existing command or manifest, or stay "Concept only". | constraint |
| Q1 | Quiz | D3 | Q11: the stem says "Nobody approves or denies it", so a student with no knowledge removes the option "Denied". | SHOULD-FIX |
| Q2 | Quiz | D3 | Q12: the stem names the field `expirationSeconds`, so a student with no knowledge removes "86400 hours" and "86400 days". | SHOULD-FIX |
| Q3 | Quiz | D2 | Short forms with no definition in the question: "RBAC" in Q4, Q7 and Q8 (the Week 12 v2 quiz writes "(RBAC)"); "IAM" in Q10; "TLS" and "HTTPS" in Q18. "EKS" stays, as in the Week 09 quiz. | SHOULD-FIX |
| Q4 | Quiz | D5 | No proof log exists yet: `probe_w13.sh` and its log are gone (an old scratchpad). Phase 4 needs a probe for Q1, Q2, Q3, Q5, Q6, Q7, Q8, Q9, Q11, Q16, Q17, Q18 and Q20 (B); the lab log for Q12, Q14, Q15, Q19 and Q20 (C); the documentation for Q4, Q10 and Q13. | phase 4 |
| N1 | Course | D1 | The syllabus row of 11/25 has no quiz. "Quiz 5 (2.0%)" is on 12/2. The quiz title says "Easy quiz", as in Weeks 01 to 12. | note for the user |

### Phase 2: the fix (run 4, 23:14 to 23:25 EST)
New builders (each has `VERSION`, a `__main__` guard and `--force`; each imports the version before it):
- `build_week13_lab_v6.py` takes each slide line, each manifest, the cluster slide, Step 0 and the Blackboard
  text from `build_week13_lab_v5` by import. It writes `Week13/Lab_week13_v6.pptx` (10 slides),
  `Week13/localMachine_v6.sh` (6 steps), `Week13/Lab_week13_Blackboard_Submission_v6.md` and the repo folder
  `~/Documents/c/r/CLO835_Fall_2026/Week13` (7 files).
- `build_week13_lecture_v10.py` imports `build_week13_lecture_v9` as V, sets the lab of v6 (`V.lab`, `V.LAB`,
  `V.FILES`), and replaces 8 slide builders in `V.SLIDES`. It writes `Week13/Lecture_week13_v10.pptx`
  (32 slides). It reads `Week13/Lecture_week13_v8.pptx` for the cover, the agenda and the outline.
- `quiz_pool_src/q_easy20_w13_v2.py` (22 exact text edits of v1, each found one time),
  `build_easy20_w13_v2.py` and `audit_easy20_w13_v2.py` (v1 with the names of v2;
  `Quiz_W13_Easy20_v2/`). GATE 10 also checks the pool `q_easy20_w12_v2`.

Lab v6 against lab v5:
- `localMachine_v6.sh`: only line 9 differs ("Each step matches one slide of Lab_week13_v6.pptx.").
- `Lab_week13_Blackboard_Submission_v6.md`: byte-equal to v5.
- The repo: ` M Week13/localMachine.sh` (the same one line), and ` M Week12/localMachine.sh` of the
  Week 12 loop. No commit.
- The command count stays at 39 (limit 40). No syllabus topic is missing (phase 1), so no command is new.

The fixes:

| ID | Fix |
|---|---|
| L1 | Slide 5: "A request to the API server passes two or three phases, in this order:" and "After admission control, the API server stores the new or changed object in etcd". |
| L2 | Slide 20: "Outside `kube-system`, a new ServiceAccount has only the permissions of every authenticated user, for example the path `/api` and `kubectl auth whoami`". |
| L3 | New or longer "Concept only" labels: slide 5 (the answer 401), 6 (the rule for the prefix `system:`), 8 (the minimum lifetime, the revocation), 15 (no lab command uses `watch`, `patch`, `update`, `deletecollection` or `configmaps`; no deny rule), 17 (nodes or a path in a ClusterRole), 18 (`system:masters`, `kubeadm:cluster-admins`, a health path), 20 (the default permissions, a change of `serviceAccountName`, another namespace). Slides 8, 15, 17 and 20 move a bullet box or the table to make room. |
| L4 | Slide 31: "Not in the lab:", then one line for each of Parts 1 to 4, and one line for slides 28 and 29. No "Also not in the lab". `check_note31()` of v9 passes, with two changed phrases in `QUAL31`. The map `MAP31` does not change. |
| L5 | The lecture imports lab v6; the paths are `Week13/`. |
| B2 | The lab v6 docstring: "The guard does not check the repo folder (standards A5): each run writes it again." |
| Q1 | Q11: "You run no other command, and no other user works on the cluster." in place of "Nobody approves or denies it." The feedback of Denied: "No controller denies this request." |
| Q2 | Q12: the wrong options "1 year", "Until an administrator deletes the CSR dev-user", "With no limit, because Kubernetes cannot revoke a certificate", with new feedback. |
| Q3 | Q2 "common name (CN)"; Q4 "RBAC means role-based access control."; Q7 "The cluster uses role-based access control (RBAC)."; Q8 option "Forbidden, because no binding now allows a request of the group system:masters" and RBAC defined in the WHY; Q10 "AWS Identity and Access Management (IAM)", the option "A RoleBinding that names ci-deployer, with no other change", "AWS command line interface (CLI)"; Q15 and Q16 define RBAC in the WHY; Q18 "no encryption", "enough for the connection", no HTTP; Q19 no JSON and no RBAC. |

The quiz build of v2 (the gates run in the builder): GATE 1 to 7 0 errors; GATE 10, 11, 12, 13 and 14
0 errors; GATE 9 longest 4, shortest 4; GATE 8 keys 5/5/5/5; GATE 8b longest run 2; GATE 8c pass;
13 questions keep a logical order.

New probes for phase 4 (D5), for the changed scenarios:
- Q11: a CSR with no approve and no deny shows Pending after two minutes.
- Q12: after `kubectl delete csr dev-user`, the certificate still works (`auth whoami`), and its end date
  stays 24 hours after the signature.

### Phase 3: the static gates (run 5, 23:24 to 23:35 EST)
First pipeline run of the lecture: FAILED: 0. My page read found two layout defects, which the gate does not
check. Both are fixed in `build_week13_lecture_v10.py`, and the deck is built again with `--force` (v10 is not
delivered yet, A5):
1. Slide 17: the new label overlapped the third bullet ("--as names the subject" wraps to two lines). The
   label is now one line at 3.42 in: "Concept only: the lab puts no nodes and no path in a ClusterRole."
2. Slide 31: the last note line touched the footer band. The line of Part 4 now also names slides 28 and 29,
   so the note has five lines.

| Check | Result |
|---|---|
| Deck gate `Lecture_week13_v10` (PowerPoint PDF, 32 pages), after the fix | FAILED: 0 |
| Deck gate `Lab_week13_v6` (PowerPoint PDF, 10 pages) | FAILED: 0 |
| PDF info | the titles "CLO835 Week 13 Lecture: Authentication, RBAC and EKS" and "CLO835 Week 13 Lab: Authentication and RBAC", the author Maziar Sojoudian |
| `pdffonts` | Calibri, Calibri-Bold, Calibri-Italic, Consolas, Consolas-Bold only (both PDFs) |
| Page read | all 32 lecture pages and all 10 lab pages; slides 17 and 31 again after the fix; no overlap, no text past a box, no wrapped terminal line |
| `gate_week13_v2.py Lab_week13_v6 Lab_week13_Blackboard_Submission_v6.md` | GATE 1, 115 PASS, 0 failed (no live folder) |
| C9: repo folder `Week13/` | 7 files (`.gitignore`, `bootstrap.sh`, `localMachine.sh`, `main.tf`, `master-init.sh.tftpl`, `variables.tf`, `worker-join.sh.tftpl`); no cleanup text; no state, `.terraform` or key file |
| C9: scripts | `bash -n` passes on the 4 scripts and templates; `terraform fmt -check` passes; `localMachine.sh` = `localMachine_v6.sh` |
| C9: images | `maziar/kubia:v1`, `maziar/alpine-curl` (only `latest` exists, F2), `maziar/flannel:v0.28.10`, `maziar/flannel-cni-plugin:v1.9.1-flannel3` |
| F3 scan of the repo folder | no `/Users/`, `.ssh/`, user name, email or AWS key; the only IP address is the EC2 metadata address 169.254.169.254 |
| Quiz build | GATE 1 to 14: 0 errors; GATE 9 longest 4, shortest 4; GATE 8 keys 5/5/5/5; GATE 8b run 2; GATE 8c pass |
| `qti_pack.py` | 20 questions, `Quiz_W13_Easy20_v2_QTI21.zip` (17602 bytes) |
| `audit_easy20_w13_v2.py` | errors 0; 20 rows; leaks 0; pairs at risk 0; 20 key records; ZIP 21 files (20 items); 20 titles; length guesses with ties shared: longest 4.5, shortest 4.5 |
| Cue simulation | PASS; highest: middle length 5.50 of 20, most words 5.25, fewest words 5.08 (limit 6.0) |
| Word check (D3) | no word in 3 or more wrong options and in no key; no word in 2 or more keys and in no wrong option |

The delivered keys of v2 equal those of v1: 1 A, 2 C, 3 B, 4 B, 5 A, 6 D, 7 D, 8 A, 9 C, 10 C, 11 D, 12 A,
13 B, 14 C, 15 A, 16 B, 17 D, 18 D, 19 B, 20 C.

### Phase 4: live pass 1 and the quiz probes (run 6, 23:28 to 23:40 EST)
The live folder for the gate is `scratchpad/w13live/gate/` (the file names of `gate_week13_v2.py`).

Setup (E3):
- Sandbox `w13live/p1`: a copy of the 7 repo files; `terraform init`; `terraform validate`: "Success! The
  configuration is valid."
- Instances before the apply: 0.
- Apply as a student (`(sleep 10; echo Maziar; sleep 40; echo yes) | terraform apply`): 23:28:36 to 23:29:55,
  "Apply complete! Resources: 15 added, 0 changed, 0 destroyed."
- SSH at the first try (23:30:43). `cloud-init status`: done. The 3 nodes were Ready at 04:31:10 UTC
  (v1.35.10, Ubuntu 26.04.1 LTS, kernel 7.0.0-1017-aws, containerd 2.2.2), about 2 min 35 s after the apply
  started.
- The message of the day names "CLO835 - Week 13 - Authentication and RBAC" and `localMachine.sh`. The home
  directory of the master holds no file, so no cleanup script. Week 13 has no extra file.
- The Flannel Pods run `maziar/flannel:v0.28.10` and `maziar/flannel-cni-plugin:v1.9.1-flannel3`; no
  `ghcr.io` image (`pause1.log`).

Pass 1 (the runner `run.sh` of `tools/instrument.py <repo localMachine.sh> https://none/`, DELAY 0, detached
on the master): 04:31:23 to 04:31:30 UTC.
- 39 commands, 39 `@@RC` lines: 35 with exit 0, 4 with exit 1.
- The 4 non-zero exits are the planned denials of C9 (a comment predicts each one), in the order of
  `DENIALS` of the gate: `get pods` as dev-user (Forbidden), `delete pod web` as dev-user (Forbidden),
  `can-i list services -n default` (no), `can-i list persistentvolumes -A` (no). Unplanned non-zero exits: 0.
- The `can-i` answers: no, no, yes.

Comments and samples against the live output (C4):

| Item | Live output | Slide or comment | Result |
|---|---|---|---|
| Step 0 | 3 nodes Ready, v1.35.10, Ubuntu 26.04.1, containerd 2.2.2; ROLES control-plane, worker, worker | lab slide 3 | equal (only AGE differs) |
| Step 1 | created, approved; `24h` `Approved,Issued`; `subject=O=developers, CN=dev-user`; `notAfter=Nov 20 04:26:24 2026 GMT` | lecture slide 9, lab comments | equal, except the run values AGE (0s, slide 1s) and the date |
| Step 2 | the version JSON with `"gitVersion": "v1.35.10"`; the 403 Status for system:anonymous; `Starting to serve on 127.0.0.1:8001` and the APIGroupList; whoami `dev-user`, `[developers system:authenticated]`; the Forbidden error for pods | lecture slides 11, 12 | equal, except the credential-id hash |
| Step 3 | the two created lines; `pod/web created`; the delete Forbidden; `developers-view created`; `No resources found in week13 namespace.` | lecture slide 16 | equal |
| Step 4 | created, created, condition met; the 403 Status that names `system:serviceaccount:week13:clo835` | lecture slide 22, lab comment | equal |
| Step 5 | the two created lines; the ServiceList with `"items": []`; no; the api-resources lines; no; yes | lecture slides 17, 23 | equal, except `"resourceVersion": "678"` (slide 23: "670") |

The `curl -k` lines show a progress meter in the log, because the runner sends the output to a file. A student
at a terminal does not see it.

The lecture commands (`lecture.log`): each of the 34 `$` lines of the terminals on slides 8, 9, 11, 12, 16,
17, 22 and 23 is a pass 1 command: 30 with exit 0, and 4 with exit 1 (the planned denials).

Probes (`w13live/probe13.sh` on the same cluster, 04:31 to 04:34:30 UTC, `probe13.log`). The table of
lecture slide 28, with each user (a delete as a server dry run): all 18 cells equal the slide.

The proof of each quiz key (D5):

| Q | Key | Proof |
|---|---|---|
| 1 | A | probe: ana (a real certificate, no binding): `pods is forbidden: User "ana" cannot create ... "shop"`; kubernetes-admin: `namespaces "shop" not found`. Docs: "admission control happens after authorization has completed" |
| 2 | C | probe: `error: the server doesn't have a resource type "users"` (exit 1) |
| 3 | B | probe: `pods is forbidden: User \"system:anonymous\" cannot list resource \"pods\" ...`, `"code": 403` |
| 4 | B | docs (authorization): "If any authorizer approves or denies a request, that decision is immediately returned and no other authorizer is consulted." The cluster: `--authorization-mode=Node,RBAC` |
| 5 | A | probe: ben can list pods in dev yes; default, kube-system, prod no |
| 6 | D | probe: lee reads configmaps, deployments and pods (exit 0); secrets Forbidden |
| 7 | D | probe: sam get, list, create, update, delete: yes (5 of 5) |
| 8 | A | probe: with no ClusterRoleBinding `cluster-admin` (0 bindings name system:masters): ops-lead alone Forbidden; ops-lead in system:masters `node "workernode2" deleted (server dry run)`. Docs: "bypassing any authorization restrictions imposed by the RBAC or Webhook mechanisms". The binding was created again from its saved YAML |
| 9 | C | probe: kim `Groups [ops audit system:authenticated]`; no type group |
| 10 | C | docs (access-entries): "EKS access entries are the best way to grant users access to the Kubernetes API." |
| 11 | D | probe: `qa-user 2m ... <none> Pending` |
| 12 | A | pass 1 `24h`; probe: notBefore Nov 19 04:26:24, notAfter Nov 20 04:26:24 (24 h); after `kubectl delete csr dev-user`, `auth whoami` still shows dev-user, and the end date does not change |
| 13 | B | probe: the decoded request field is byte-equal to `dev-user.csr`; 0 lines with "PRIVATE KEY" |
| 14 | C | pass 1: `User \"system:serviceaccount:week13:clo835\" cannot list resource \"services\"` |
| 15 | A | probe in sales: delete Forbidden; get pod web, get pods and `run api` (server dry run) exit 0 |
| 16 | B | probe: only the rule `[""]`, `["configmaps"]` allows the create; the other three are forbidden |
| 17 | D | probe: /api 403, /apis 403, /apis/apps 403, /version 200 |
| 18 | D | probe: `curl: (60) SSL certificate ... unable to get local issuer certificate`, exit 60 |
| 19 | B | pass 1: the ServiceList with `"items": []` |
| 20 | C | pass 1: `can-i` yes after the ClusterRoleBinding; probe: a ClusterRoleBinding with roleRef kind Role is rejected (`roleRef.kind: Unsupported value: "Role"`) |

Clean-up and destroy:
- The probe objects are deleted: the namespaces dev, prod, qa and sales; the CSRs probe13-ana, probe13-kim and
  qa-user; `/tmp/probe13`. After it: the namespaces default, kube-flannel, kube-node-lease, kube-public,
  kube-system and week13; only the 3 kubelet CSRs; the ClusterRoleBinding `cluster-admin` exists again.
- Destroy as a student (`(sleep 10; echo Maziar; sleep 40; echo yes) | terraform destroy`): "Destroy complete!
  Resources: 15 destroyed." (23:38:12 EST, `destroy1.log`).
- After it: 0 instances in any state; only the `default` security group.

Findings of phase 4, for the next fix (phase 6, then phase 3):
- P1 (quiz, D6): the signer starts the certificate 5 minutes before the signature (notBefore 04:26:24, approve
  at 04:31). The new Q12 feedback "This certificate expires 24 hours after the signature." is 5 minutes wrong.
  Write "This certificate is valid for 24 hours." The WHY "the certificate expires one day later" has the
  same gap: write "and the certificate is valid for 24 hours".
- P2 (lecture, C4): the run values of slides 9, 12 and 23 (AGE, notAfter, the hash, resourceVersion) come from
  2026-11-11. Take them from this pass 1 log, as the Week 12 v8 lecture did.

### Phase 5: live pass 2 (run 7, 23:40 to 23:50 EST)
- Instances before the apply: 0. The runner of the repo `localMachine.sh` is byte-equal to `gate/run.sh` of
  pass 1.
- Sandbox `w13live/p2`: a new copy of the 7 repo files; `terraform init`; `terraform validate`: "Success!".
- Apply as a student: 23:40:26 to 23:41:45, "Apply complete! Resources: 15 added, 0 changed, 0 destroyed." A new
  master address (the gate checks it). SSH at the first try; `cloud-init status`: done; 3 nodes Ready at
  04:42:48 UTC (v1.35.10); the message of the day names Week 13; the home directory holds no file.
- Pass 2 (the same runner, `DELAY=3`, detached): 04:42:59 to 04:45:00 UTC (2 min 1 s). 39 commands: 35 with exit
  0, and the same 4 planned denials with exit 1. Unplanned non-zero exits: 0. The `can-i` answers: no, no, yes.
- The outputs of pass 1 and pass 2 are equal after the run values (ages, addresses, the hash, the end date,
  resourceVersion, the Pod name suffixes). Only the speed numbers of the `curl` progress meter differ.
- Destroy as a student: "Destroy complete! Resources: 15 destroyed." (23:48:38 EST, `destroy.log`).
- After it: 6 instances in the state terminated (pass 1 and pass 2), 0 in pending, running, stopping or stopped;
  only the `default` security group (it cannot be deleted).

The gate with the live folder:
`gate_week13_v2.py Lab_week13_v6 Lab_week13_Blackboard_Submission_v6.md w13live/gate` gives GATE 1, 0 failed,
156 PASS (115 static and 41 live). The live checks include: each pass ran all 39 commands; each pass has only
the four planned denials as non-zero exits; 12 samples of C4 in each pass; pass 2 ran on a new cluster; both
destroys complete; the maziar Flannel image; no recovery test; the tested commands equal the final commands.

### Phase 6: review round 1 (run 8, 23:51 EST to 00:40 EST on 2026-11-19)
Three fresh independent subagents (one for each part) got the rules (`CLO835_STANDARDS.md` parts), the
files, the page images and the live logs, but no list of my findings. Their results are in
`scratchpad/w13review_r1/` (`lecture.md`, `lab.md`, `quiz.md`).

| Part | MUST-FIX | SHOULD-FIX |
|---|--:|--:|
| Lecture v10 | 6 | 8 |
| Lab v6 with its Blackboard text | 0 | 3 |
| Quiz v2 | 5 | 7 |

All 29 findings and the two phase 4 findings (P1, P2) are applied. I checked each finding against the rules,
the documentation and the logs before I applied it.

Lecture (`build_week13_lecture_v10.py`, built again with `--force`; v10 is not delivered):
- L-M1, slide 5: admission control acts on create, change, delete and connect (for example `kubectl exec`),
  not on a request that only reads. Docs: "Admission controllers act on requests that create, modify,
  delete, or connect to (proxy) an object." The diagram box says "Create, change, delete, connect".
- L-M2, slides 15 and 31: `kubectl wait` uses watch, `kubectl certificate approve` uses update, and `view`
  has watch. The label and the note now say "no rule of the lab has watch, patch or deletecollection" and
  "No command of dev-user uses update or configmaps".
- L-M3, slides 6, 17 and 31: the slide 6 label names no group `system:unauthenticated`; the note says
  "nodes or a path in a ClusterRole".
- L-M4, slide 20: the label no longer says that the lab uses no other namespace, and names no ServiceAccount
  default.
- L-M5, slide 17: the verdict boxes say "auth can-i: no" and "auth can-i: yes".
- L-M6, slide 20: the example of the last bullet is `kubectl auth whoami` only.
- L-S1 to L-S8: slide 8 (kube-controller-manager never approves a CSR for this signer), slides 10 and 31 ("the
  discovery path /api"), slide 14 ("The first authorizer that allows or denies the request decides"; the
  least-privilege bullet moves to the caption of slide 15), slide 21 ("ca.crt in the directory of the token"),
  slide 12 ("Extra shows a hash of the certificate"), slide 22 (GET of a collection: list; of one object: get),
  slide 10 (the value "" in apiGroups is the core group).
- P2: the run values of pass 1 of 2026-11-18 on slides 9, 12 and 23 (AGE 0s, notAfter Nov 20 04:26:24, the
  hash, resourceVersion 678).
- The builder now replaces 14 slide functions of v9. Slide 31 finds each slide by its function name.
  `QUAL31` has 9 phrases; `check_note31()` and the map `MAP31` pass.

Lab (`build_week13_lab_v6.py`, built again with `--force`; v6 is not delivered):
- B-S1: Blackboard section 1 is "## 1. Build and Check the Cluster" (the Week 12 v8 model).
- B-S2: the Explain item is "Explain the order of the phases of a request in the API server."
- B-S3: the Step 5 comment is "# The Role service-reader and its RoleBinding allow clo835 to get and list
  Services." It reaches the deck, `localMachine_v6.sh`, the repo `localMachine.sh` and lecture slide 23.
- Only a comment changed: the runner of the repo `localMachine.sh` is still byte-equal to the tested runner
  `w13live/gate/run.sh`. So phases 4 and 5 do not run again for the lab.
- `gate_week13_v3.py` (new, a copy of v2): the section 1 title and the F4 row of the section 3 Explain item
  follow the Blackboard text v6. v2 stays on disk.

Quiz (`q_easy20_w13_v2.py`, 18 exact text edits and one new record):
- Q-M1 = P1 (Q12): "the certificate is valid for 24 hours" in the WHY and in the IF of the last option.
- Q-M2 (Q9): "in the group ops only", "in the group audit only".
- Q-M3 (Q13): "Only the content of dev-user.csr" (the key) and "Only the content of dev-user.key".
- Q-M4: Q5 (the scope of a RoleBinding) tested the fact of Q20. Q5 is now "edit role": a RoleBinding binds
  `edit` to ben in dev; which command gets Forbidden (key: `kubectl get rolebindings -n dev`). This new
  scenario has no live proof yet (D5).
- Q-M5: "with no" was in 4 wrong options and in no key. New wrong options in Q9 ("in no group, because groups
  must be objects"), Q12 ("For an unlimited time, ...") and Q18 ("curl sends the request as plain text, and
  anyone can read the token").
- Q-S1 (Q8): "and the ClusterRole cluster-admin stays"; the option "Deleted, because the ClusterRole
  cluster-admin still allows each request" in place of super-admin.conf, with new feedback.
- Q-S2 (Q9): the stem defines the common name (CN) and organization (O) fields. Q-S3 (Q10): the options with
  mapRoles and RoleBinding also say "access". Q-S4 and Q-S5 (Q11), Q-S6 (Q6), Q-S7 (Q10): feedback texts.
- The builder gates: GATE 1 to 7 0 errors; GATE 10 to 14 0 errors; GATE 9 longest 4, shortest 4; GATE 8 keys
  5/5/5/5; GATE 8b longest run 3 (limit 3); GATE 8c pass (halves AABBBCCCDD / AAABBCCDDD).

The probe for the new Q5 (for the next live run, `--as=ben`, with a server dry run for the delete and the
scale): `get rolebindings` Forbidden; `get secrets`, `delete deployment web` and `scale deployment web
--replicas=3` allowed.

### Phase 3 again: the static gates after round 1 (run 9, 00:26 to 00:35 EST on 2026-11-19)
Correction: review round 1 ended at about 00:25 EST, not at 00:40.

| Check | Result |
|---|---|
| Deck gate `Lecture_week13_v10` (32 pages) | FAILED: 0 (two builds; see the page read) |
| Deck gate `Lab_week13_v6` (10 pages) | FAILED: 0 |
| `pdffonts` | Calibri and Consolas only (both PDFs) |
| Page read | the changed lecture pages 5, 6, 8 to 10, 12, 14, 15, 17, 20 to 23 and 31, and lab page 8. One defect: on slide 31 the code name `kubeadm:cluster-admins` broke over two lines. The Part 2 line now names the paths first and the groups last; the name is on one line (read again). |
| `gate_week13_v3.py Lab_week13_v6 Lab_week13_Blackboard_Submission_v6.md w13live/gate` | GATE 1, 0 failed, 156 PASS (with the 41 live checks; "the tested commands equal the final commands" passes, because only a comment changed) |
| C9 and F3 | 7 repo files; `bash -n` and `terraform fmt -check` pass; no cleanup text; the F3 scan is clean; the repo has only ` M Week12/localMachine.sh` and ` M Week13/localMachine.sh` |
| Quiz build | GATE 1 to 14: 0 errors; keys 5/5/5/5; GATE 8b longest run 3 (limit 3); GATE 9 longest 4, shortest 4 |
| `qti_pack.py` | 20 questions, 17620 bytes |
| Quiz audit | errors 0; leaks 0; pairs at risk 0; length guesses with ties shared: longest 4.5, shortest 4.3 |
| Cue simulation | PASS; highest: middle length 5.50, most words 5.42, fewest words 5.08 (limit 6.0) |
| Word check (D3) | no word only in keys; "rolebinding" is in 3 wrong options, and the key of Q5 has "rolebindings" (the audit folds plurals) |

The delivered keys: 1 A, 2 C, 3 B, 4 B, 5 B, 6 D, 7 D, 8 A, 9 C, 10 C, 11 D, 12 A, 13 B, 14 C, 15 A, 16 B,
17 D, 18 D, 19 A, 20 C.

### Phase 4 again, probes only (run 10, 01:28 to 01:36 EST on 2026-11-19)
No lab command changed in round 1, so no new lab pass runs. The new Q5 needs a live proof (D5).
- Instances before the apply: 0. Sandbox `w13live/p3` (the 7 repo files), `terraform validate`: "Success!".
- Apply as a student: "Apply complete! Resources: 15 added". SSH at the first try (01:29:57); cloud-init
  done; 3 nodes Ready (v1.35.10).
- `probe13b.sh` (the names of the stem):

| Q | Key | Proof |
|---|---|---|
| 5 | B (`kubectl get rolebindings -n dev`) | ben with the ClusterRole `edit` in dev: `rolebindings.rbac.authorization.k8s.io is forbidden: User "ben" cannot list resource "rolebindings"` (rc 1); `get secrets` shows `db` (rc 0); `delete deployment web` "deleted from dev namespace (server dry run)" (rc 0); `scale deployment web --replicas=3` "scaled (server dry run)" (rc 0) |

- The probe deleted the namespace dev; after it, only the 5 start namespaces stay.
- Destroy as a student: "Destroy complete! Resources: 15 destroyed." (01:35:40 EST). After it: 0 instances;
  only the `default` security group.
- The changed Q8 scenario ("the ClusterRole cluster-admin stays") has its proof in `probe13.log`: the probe
  deleted only the ClusterRoleBinding, so ops-lead alone got Forbidden while the ClusterRole existed.
- All 20 keys of the current quiz v2 now have a proof (19 live, Q10 by the EKS documentation; Q4 by the
  documentation and the live flag).

### Phase 6: review round 2 (run 11, 01:38 to 02:15 EST on 2026-11-19)
Three new fresh independent subagents, with the same kind of brief as round 1 (the rules, the files, the page
images and the live logs; no list of my findings). Their results are in `scratchpad/w13review_r2/`.

| Part | MUST-FIX | SHOULD-FIX |
|---|--:|--:|
| Lecture v10 | 4 | 8 |
| Lab v6 with its Blackboard text | 0 | 4 |
| Quiz v2 | 1 | 5 |

All 22 findings are applied. No command changed: the commands of the repo `localMachine.sh` equal the tested
runner `w13live/gate/run.sh` (two new comment lines move the line numbers of the later commands; the gate
compares the commands without the line numbers).

Lecture:
- L-M1, slide 6: "Kubernetes stores no normal users and no groups". The docs: "service accounts are users
  managed by the Kubernetes API". The same fix reaches the lab comment, the Blackboard text (section 2 and its
  Explain item) and the Q2 WHY of the quiz.
- L-M2, slide 15: "the lab does not write a rule with watch, patch or deletecollection" (the ClusterRole view
  that Step 3 binds has watch).
- L-M3, slide 17: "the lab does not put nodes or a path in a ClusterRole" (the form of B7).
- L-M4, slides 20 and 31: Step 4 shows that a new ServiceAccount gets Forbidden, so the label and the note name
  "kubectl auth whoami as a ServiceAccount".
- L-S1 to L-S8: "the rule for the prefix system:" in the note; no `cluster-admin` and no
  `kubeadm:cluster-admins` in the note and the slide 18 label (`kubernetes-admin` is in
  `kubeadm:cluster-admins`, which binds `cluster-admin`); the user name of slide 21 on one line; slide 23 "A
  subject can also be a ServiceAccount of another namespace" with a label; slide 22 the verbs of POST, PUT,
  PATCH and DELETE with the label "the lab does not send a PATCH request"; slide 27 "and you cannot remove it"
  (mode CONFIG_MAP); slides 7 and 30 "verifies" and "user"; slide 8 "The CertificateSigningRequest API (stable
  in v1.19)".
- The builder replaces 18 slide functions of v9. Its own `check_note31()` (a copy of v9) also allows a phrase
  with a RoleBinding to name a ServiceAccount of another namespace.

Lab and Blackboard text:
- B-S1: "Approve the dev-user CertificateSigningRequest (CSR) with kubectl certificate approve dev-user."
- B-S2: "## 4. Create a Role and a RoleBinding for dev-user, and a RoleBinding for the Group developers".
- B-S3: "# The group of the certificate gets the default ClusterRole view, in week13 only." (also lecture
  slide 16).
- B-S4: two new Step 1 comments: "# The signer sets the start date 5 minutes before the approval." and "# So
  notAfter, the end date, is about 23 h 55 min after the approval." (pass 1: approve 04:31:24, notAfter
  04:26:24 the next day; pass 2: 04:43:18 and 04:38:18).
- `gate_week13_v3.py`: the section 4 title, the CSR item, "normal users" and the view needle follow the text.

Quiz:
- Q-M1: Q15 "role verbs" is a new record with the lab names: dev-user creates the Pod web, then runs `delete pod
  web`; the key "Forbidden, because no rule of the Role has the verb delete". The old options B and C repeated
  the verbs of the stem. Proof: pass 1 L114 `pod/web created`, L115 the Forbidden of the delete.
- Q-S1 (Q3): option D "A PodList of default, because every client gets read access to default" (the stem of
  Q17 removed the old -k option), with new feedback.
- Q-S2 (Q10): the key "An access entry that names ci-deployer" (it was the only option with no "that" clause).
- Q-S3 (Q14, Q19): the stems name the token, not curl (with Q18, they supported a wrong option of Q18).
- Q-S4 (Q11): "kube-controller-manager never approves (denies) ...", because a custom controller can.
- Q-S5 (Q16): the probe must use dev-user and its context. It needs a new live cluster (open).
- My own addition (A1): the Q19 WHY says "allows", not "lets".
- The builder gates: GATE 1 to 14 0 errors; keys 5/5/5/5; GATE 9 longest 4, shortest 4; GATE 8b run 3.

### Phase 3 again: the static gates after round 2 (run 12, 02:11 to 02:13 EST on 2026-11-19)
- First lecture gate: FAILED: 1, "no shape in the footer band" (slide 22: the new PATCH label ended at 7.08 in).
  The page read then showed two more defects: on slide 22 the second bullet overlapped the label, and on slide
  31 the last note line reached the footer band. Fixes: slide 22 bullets at 13 pt and a one-line label of
  0.30 in at 6.38 in; slide 31 joins "Not in the lab." and the Part 1 line. Read again: both pages are clean.

| Check | Result |
|---|---|
| Deck gate `Lecture_week13_v10` (32 pages) | FAILED: 0 (after the fixes) |
| Deck gate `Lab_week13_v6` (10 pages) | FAILED: 0 |
| `pdffonts` | Calibri and Consolas only (both PDFs) |
| Page read | the changed lecture pages 5 to 8, 13 to 31, and lab pages 4 and 6 |
| `gate_week13_v3.py` with the live folder | GATE 1, 0 failed, 156 PASS ("the tested commands equal the final commands" passes) |
| C9 and F3 | 7 repo files; `bash -n` and `fmt` pass; no cleanup text; F3 clean; repo `localMachine.sh` = `localMachine_v6.sh` |
| Quiz build | GATE 1 to 14: 0 errors; keys 5/5/5/5 |
| `qti_pack.py` | 17685 bytes |
| Quiz audit | errors 0; leaks 0; pairs at risk 0; length guesses with ties shared: longest 4.5, shortest 4.3 |
| Cue simulation | PASS; highest: middle length 5.50 (limit 6.0) |

The delivered keys did not change: 1 A, 2 C, 3 B, 4 B, 5 B, 6 D, 7 D, 8 A, 9 C, 10 C, 11 D, 12 A, 13 B,
14 C, 15 A, 16 B, 17 D, 18 D, 19 A, 20 C.

### Phase 4 again, probes only (run 13, 02:15 to 02:23 EST on 2026-11-19)
- Instances before the apply: 0. Sandbox `w13live/p4` (the 7 repo files of round 2), `terraform validate`:
  "Success!". Apply as a student: "Apply complete! Resources: 15 added". SSH at the first try (02:16:54);
  cloud-init done; 3 nodes Ready (v1.35.10).
- The runner of the final repo script (`w13live/run_final.sh`) ran first, so that dev-user and its context
  exist (a third full pass, `run3.log`): 39 commands, 35 with exit 0, and the same 4 planned denials; the
  `can-i` answers no, no, yes. Its commands equal the tested runner `gate/run.sh` (line numbers aside).
- `probe13c.sh` (Q16, one rule at a time, with dev-user and `--context=dev-user@kubernetes` in the namespace
  dev, a server dry run):

| Rule | apiGroups | resources | Result |
|---|---|---|---|
| a | `[""]` | `["ConfigMap"]` | `configmaps is forbidden: User "dev-user" cannot create resource "configmaps"` (rc 1) |
| b (key) | `[""]` | `["configmaps"]` | `configmap/app-config created (server dry run)` (rc 0) |
| c | `[core]` | `["ConfigMap"]` | forbidden (rc 1) |
| d | `[core]` | `["configmaps"]` | forbidden (rc 1) |

- The probe deleted the namespace dev and each Role and RoleBinding q16.
- Destroy as a student: "Destroy complete! Resources: 15 destroyed." (02:23:13 EST). After it: 0 instances;
  only the `default` security group.
- All 20 keys of the current quiz have a proof with the names of the stems (18 live, Q4 by the documentation
  and the live flag, Q10 by the EKS documentation). The new Q15 has its proof in pass 1 (L114, L115).

### Phase 6: review round 3 (run 14, from 02:25 EST on 2026-11-19)
- The session check at 02:25:04: Arn assumed-role/voclabs, 0 instances, session age 3 h 24 min.
- Three new fresh independent subagents, with the same kind of brief as rounds 1 and 2. Their results are in
  `scratchpad/w13review_r3/`.

| Part | MUST-FIX | SHOULD-FIX |
|---|--:|--:|
| Lecture v10 | 3 | 7 |
| Lab v6 with its Blackboard text | 0 | 0 |
| Quiz v2 | 1 | 3 |

Lab (0/0): the reviewer found the 112 command lines of `run_final.sh` equal to the script, the 4 manifests of
the lecture equal to the lab files, and each comment true against run1, run2, run3 and `probe13c.log`. Notes
with no finding: B5 (`$` in place of `L$` on slides 3 and 9, also in the Week 12 v8 model; a fix belongs in the
standards file), G2 (the local repo has the v6 comments and GitHub has v5; git is the task of the user), and the
job messages of slide 5 (only an interactive shell shows them).

Lecture (all 10 applied; no fact was wrong):
- L-M1 (B7, three times), slide 16: the bullet is now "`dev-user` is in the group `developers`. The RoleBinding
  `developers-view` gives this group the ClusterRole `view`, so `dev-user` can list the Services" (slide 17 and
  the lab comment state the namespace scope).
- L-M2 (B7, C8), slide 31: "a PATCH request" moves to the Part 3 line (slide 22 is in Part 3).
- L-M3 (B7, four times), slide 30: bullet 3 is "A Pod proves its identity with the token of its ServiceAccount".
- L-S1, slide 5: a no-break space keeps `kubectl exec` on one line.
- L-S2 (C4), slide 11: the sample has the live line `"details": {},` (run1 L84); the empty line before
  `kubectl proxy` is removed, so the terminal stays above the footer band.
- L-S3 (A1), slide 31: the Part 1 sentence of 27 words is now two sentences.
- L-S4, slide 8: "`expirationSeconds: 86400` (stable in v1.24)" (feature gate CSRDuration, GA 1.24).
- L-S5, slide 15: "The request verbs: ..." (slide 29 names more verbs).
- L-S6 (syllabus 12.2.4), slide 17: "Use them for nodes, PersistentVolumes, paths such as `/readyz`, and the Pods
  of all namespaces", with the label "Concept only: the lab does not put nodes or a path in a ClusterRole, or
  bind a ClusterRole for the Pods of all namespaces." (one line at the full width), and the Part 2 line of
  slide 31. Bullet 3 is now one line: "`kubectl auth can-i` asks if a subject (`--as`) can do an action".
- L-S7 (A1), slide 27: "admin permissions" in place of "admin access" (the word of slides 15, 20 and 26).
- The builder now replaces 20 slide functions of v9 (new: `s_anonymous`, `s_role_lab`).
- The first page read after the build found two layout defects: `dev-user` broke over two lines on slide 16, and
  bullet 3 of slide 17 touched the label. Both are fixed, and the second page read shows clean pages.
- Deck gate `Lecture_week13_v10`: FAILED: 0 (32 pages); `pdffonts`: Calibri and Consolas only.
- `gate_week13_v3.py` with the live folder: GATE 1, 0 failed, 156 PASS (02:47).

Quiz (all 4 applied; the reviewer found each of the 20 keys correct, with a proof, and 0 differences between
the source and the delivered files):
- Q-M1 (D3), Q9 "certificate subject": the key was the only option with no reason. New options: key C "The user
  kim in the groups ops and audit, from the O fields"; A "... ops only, from the first O field of the subject";
  B "... audit only, from the last O field of the subject"; D "The user kim in no group, because each group must
  be an object". The key stays the strictly shortest option (59 against 62 to 74 characters).
- Q-S1 (D2, D6), Q10 "eks identities": the IAM role eks-admin creates the cluster, and ci-deployer "must also run
  kubectl commands". So IF A is true also in the mode CONFIG_MAP (the creator is in `system:masters`).
- Q-S2 (D2, D6), Q12 "certificate lifetime": "A kubeadm cluster runs with the default settings." The WHY names
  the maximum of the signer (`--cluster-signing-duration`, 1 year by default).
- Q-S3 (D2, D6), Q2 "users": "a kubeadm cluster with the default settings" (a CRD with the plural users can add
  a type users).
- Builder: GATE 1 to 14, 0 errors; keys 5/5/5/5; GATE 9 longest 4, shortest 4; GATE 8b run 3.
- `qti_pack.py`: 17757 bytes, 21 files (20 items). Audit: errors 0, leaks 0, pairs at risk 0; length guesses
  with ties shared: longest 4.5, shortest 4.3. Cue simulation: PASS; highest "fewest words" 5.58 (limit 6.0).
- The delivered keys do not change: 1 A, 2 C, 3 B, 4 B, 5 B, 6 D, 7 D, 8 A, 9 C, 10 C, 11 D, 12 A, 13 B,
  14 C, 15 A, 16 B, 17 D, 18 D, 19 A, 20 C.

No command changed in round 3, so phases 4 and 5 stay valid. The phase 3 checks of the changed files ran after
the fixes (above); the lab files did not change.

### The session limit (02:49 EST on 2026-11-19)
- `aws sts get-caller-identity`: assumed-role/voclabs. The credentials date from 23:00:48 EST, so the session
  is 3 h 49 min old, more than the limit of 3.5 h (02:30:48 EST).
- No cluster of the loop exists: 0 instances; only the `default` security group. Nothing to destroy.
- The loop stops here, as its rule says. Restart the lab, then start the loop again.

## Results
- Phase 0 is complete. All baseline checks pass.
- Phase 1 is complete: 0 MUST-FIX, 9 SHOULD-FIX (L1 to L5, B2, Q1 to Q3), 1 check (L6), 2 live items (B1,
  Q4), 1 constraint (B3), 1 note (N1).
- Phase 2 is complete: all 9 SHOULD-FIX are applied. Lab v6 (10 slides, 39 commands), lecture v10
  (32 slides) and quiz v2 (all builder gates pass) are built. The PDFs and the gates come in phase 3.
- Phase 3 is complete: both deck gates FAILED: 0 after two layout fixes from the page read; the lab gate
  GATE 1; C9 and F3 pass; the quiz gates, the audit and the cue simulation pass.
- Phase 4 is complete: 15 added, pass 1 with 39 commands (35 exit 0, the 4 planned denials, 0 unplanned),
  all comments and samples checked, 20 of 20 quiz keys proven (18 live; Q4 by the documentation and the live
  flag; Q10 by the EKS documentation), probe objects deleted, 15 destroyed, 0 instances, only the `default`
  group. Two text findings (P1, P2) wait for the next fix.
- Phase 5 is complete: pass 2 on a new cluster with 0 unplanned non-zero exits, the full gate GATE 1 with
  the live folder (156 PASS), 15 destroyed.
- AWS at 23:48 EST: 0 instances in pending, running, stopping or stopped (6 terminated); only the `default`
  security group.
- Phase 6, round 1: 11 MUST-FIX and 18 SHOULD-FIX, all applied. No command changed. The new Q5 needs a live
  probe before the stop condition "all 20 quiz keys have a proof" is true again.

## Issues / Notes
- The quiz has at least one EKS question. Phase 4 proves an EKS key with a `docs.aws.amazon.com` page,
  because the loop creates no EKS cluster.
