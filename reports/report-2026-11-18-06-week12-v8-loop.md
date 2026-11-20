# Report: Week 12 to v8, the running loop report
**Date**: 2026-11-18
**Sequence**: #06 for the day

## Summary
This is the state file of the `/loop` that brings Week 12 (ConfigMaps and Secrets) to v8, 100 % to
`CLO835_STANDARDS.md` v1.2. Each run does one phase and updates this report. Run 1 did phase 0 (preflight).

## Loop state
| Item | Value |
|---|---|
| AWS session first seen | 2026-11-18 17:50 EST (role voclabs, us-east-1) |
| Stop the AWS work by | 2026-11-18 21:20 EST (3.5 h) |
| Phases done | 0, 1, 2, 3, 4, 5, 6 (round 1: 3 MUST-FIX, 13 SHOULD-FIX, all applied), 3 again |
| Round 2 | 2 MUST-FIX, 6 SHOULD-FIX, all applied; Q8 D and the Q17 premise proven live |
| Round 3 | 0 MUST-FIX, 8 SHOULD-FIX, all applied |
| Round 4 | lab 0/0, quiz 0/0, lecture 0/2 (docstring only), applied |
| Round 5 | lecture 0/1 (docstring only), applied |
| Round 6 | lecture 0/0 |
| Next phase | none: the stop condition is met (20:15 EST). The final report is #07. |
| Clusters of this loop that run now | none |

## What Changed
Run 1 (phase 0, 17:50 to 18:05 EST):
- Cloned `github.com/sojoudian/CLO835_Fall_2026` to `~/Documents/c/r/CLO835_Fall_2026` (HEAD `7c4d9b8`,
  "add week12"). The clone was missing since the move of 2026-11-14.
- Fixed the old path `/Users/maziar/Downloads/k8s_week3` to `/Users/maziar/Documents/c/r/k8s_private` in:
  - `tools/rungate.py` (2 lines);
  - `tools/deck_pipe.sh` (4 lines);
  - `quiz_pool_src/audit_easy20_w12.py` (1 line).
- AWS: terminated 3 instances and deleted 2 security groups of the old Week 12 test.

## Technical Details

### AWS inventory before the clean-up
- 3 instances in the state running, `m5.large`, key pair `Maziar`:
  `week12-k8s-master`, `week12-k8s-worker-1`, `week12-k8s-worker-2`.
- Their launch time was 2026-11-18 22:41 UTC, but their root volumes were created on 2026-11-11 04:58 UTC.
  So they are the old test cluster of 2026-11-11, whose destroy got 403. The Learner Lab started them
  again with the new session.
- Security groups: `default`, `week12-k8s-master`, `week12-k8s-worker`. No Elastic IP.
- The Terraform state of that cluster is gone, so I removed it with the AWS CLI:
  - `terminate-instances` for the 3 instances, then `wait instance-terminated`;
  - revoke of the ingress rules of the two groups (they refer to each other), then `delete-security-group`.
- After: 0 instances in pending, running, stopping or stopped; only the `default` security group.

### Baseline (v7, before any change)
| Check | Result |
|---|---|
| Deck gate `Lecture_week12_v7` | FAILED: 0 |
| Deck gate `Lab_week12_v7` | FAILED: 0 |
| Quiz audit `Quiz_W12_Easy20` | errors 0, leaks 0, pairs at risk 0, 20 key records, ZIP 21 files, 20 titles |
| Quiz length guesses | longest 4.0 of 20, shortest 5.5 of 20, most words 4 of 20 |
| Cue simulation | PASS; highest: shortest 5.50 of 20, middle length 5.33 of 20 (limit 6.0) |
| Repo `Week12/` | 7 files; `localMachine.sh` is byte-equal to `Week12/localMachine_v7.sh` |

### Phase 1: the audit (run 2, 17:56 to 18:20 EST, read-only)
Read: `Lecture_week12_v7.pptx` (28 slides), `Lab_week12_v7.pptx` (10 slides), `localMachine_v7.sh`,
`Lab_week12_Blackboard_Submission_v7.md`, `Quiz_W12_Easy20` (20 questions), the repo `Week12/` files,
the syllabus row of Week 12, and kubernetes.io (configmap, configure-pod-configmap, secret, Pod v1 API).

What passes:
- B1 to B6 by the gate (FAILED: 0), with the title and author set.
- B7: the slide set (cover, agenda, Course Outline, three parts, Optional Topics, Key Takeaways, "Lab Week 12
  at a Glance", References). All 8 reference links return HTTP 200.
- B7 facts checked: command and args, the 1 MiB limit, optional: true, the update delay (kubelet sync period
  1 min + cache TTL 1 min = "about two minutes"), subPath, base64, tmpfs, RBAC and Pod creation, the token
  since v1.22 and v1.24, the discovery permissions, immutable (v1.21), KMS v2 (v1.29).
- C1: 10 slides with the right titles; Steps 0 to 6; 39 commands on the master (limit 40).
- C3: images `maziar/fortune:args` and `maziar/alpine-curl` only; Flannel from `maziar`.
- C5: 7 files, no cleanup script, `key_name` with no default, `LabInstanceProfile`, the message of the day
  names Week 12 and `localMachine.sh`.
- C7: the title, "all 7 sections", the recording paragraph, sections 1 to 7, `You must:`, Explain items
  last, six Submission Requirements, the Important paragraph, no pledge, "master node".
- C8: each terminal labeled "Lab Week 12, Step M" holds only commands of that step; the manifests match.
- D: keys 5 A, 5 B, 5 C, 5 D; the audit and the cue simulation pass; each key is correct in my reading.
  The Pod v1 API reference proves Q20: "Values defined by an Env with a duplicate key will take
  precedence".

Defects (the input of phase 2):

| ID | Part | Rule | Defect | Class |
|---|---|---|---|---|
| L1 | Lecture | syllabus | Image pull Secrets (`kubectl create secret docker-registry`, `imagePullSecrets`) are not taught. Slide 16 names only the type `kubernetes.io/dockerconfigjson`. | MUST-FIX |
| L2 | Lecture | syllabus | `$(VAR_NAME)` references in an env value and in command or args are not taught. | SHOULD-FIX |
| L3 | Lecture | syllabus | The `items` field (only some keys as files) and `defaultMode` (file permissions) of a ConfigMap volume are not taught. | SHOULD-FIX |
| L4 | Lecture | D2, C8 | "env has priority over envFrom" is only in a lab comment (Step 4), but quiz Q20 tests it. No slide states it. | SHOULD-FIX |
| L5 | Lecture | B7 | Slide 27 repeats "Also not in the lab:" in five paragraphs. Make one list. | SHOULD-FIX |
| L6 | Lecture | A5, C8 | `build_week12_lecture_v7.py` imports `build_week12_lab_v6`. The v8 lecture must import the v8 lab. | SHOULD-FIX |
| L7 | Lecture | C4 | The sample outputs on slides 7, 12 to 14, 16, 18 to 20 and 22 come from the run of 2026-11-11. Compare them with the output of phase 4. | check |
| B1 | Lab | C3, C4, C9, E3 | No live pass of v7. | phases 4 and 5 |
| B2 | Lab | C3 | The Step 4 comment says that env has priority over envFrom, but `secret-pod` sets the same value in env and in secretRef, so the output does not show the priority. | SHOULD-FIX |
| B3 | Lab | C1 | 39 of 40 commands. A new syllabus topic must fold into an existing command or manifest, or stay "Concept only" in the lecture. | constraint |
| Q1 | Quiz | D5 | No live proof yet for the keys of Q8 (options B and D), Q13, Q18 and Q6 (the reject message of an invalid base64 value). | phase 4 |
| N1 | Course | D1 | The syllabus names this quiz "Quiz 4 (2.0%)" and the lab "Optional Lab 9 (2.5%)". The quiz title says "Easy quiz". | note for the user |

### Phase 2: the fix (run 3, 18:01 to 18:35 EST)
New builders (each has `VERSION`, a `__main__` guard and `--force`; each imports the version before it):
- `build_week12_lab_v8.py` writes `Week12/Lab_week12_v8.pptx` (10 slides), `Week12/localMachine_v8.sh`
  (6 steps), `Week12/Lab_week12_Blackboard_Submission_v8.md`, and the repo folder
  `~/Documents/c/r/CLO835_Fall_2026/Week12` (7 files; only `localMachine.sh` differs from HEAD `7c4d9b8`).
- `build_week12_lecture_v8.py` writes `Week12/Lecture_week12_v8.pptx` (29 slides). It takes each lab
  command and manifest from `build_week12_lab_v8` (L6).
- `quiz_pool_src/q_easy20_w12_v2.py`, `build_easy20_w12_v2.py`, `audit_easy20_w12_v2.py`: copies of v1
  with the names of v2 (`Quiz_W12_Easy20_v2/`). The questions do not change, because phase 1 found no
  quiz defect. Phase 6 can change them.

The fixes:

| ID | Fix |
|---|---|
| L1 | New slide 19 "Image Pull Secrets" (concept only): the type `kubernetes.io/dockerconfigjson`, `kubectl create secret docker-registry`, `imagePullSecrets` in a Pod and in a ServiceAccount, the namespace rule. The account and the image are placeholders (`<your-account>`), so the slide names no third-party account (F2). |
| L2 | Slide 8: "`$(NAME)` in a value, in command or in args gives the value of an environment variable. In env, the variable must come earlier in the list." Lab Step 2: `MESSAGE` = `"$(GREETING) $(COLOR)"`. |
| L3 | Slide 13: `defaultMode` and `items` ("Concept only: the lab does not run items."). Lab Step 3: `defaultMode: 0440` and `ls -lL`. |
| L4, B2 | Lab Step 2: the ConfigMap also holds `GREETING=hi`, and env sets `GREETING=hello`, so printenv shows `hello`. Slide 12 states the priority. The Step 4 comment says that env and envFrom give DB_Password the same value. |
| L5 | Slide 28: one list, one line for each part, no repeated "Also not in the lab". |
| L6 | The lecture imports lab v8. |
| Numbers | The slides after 18 move by one. Slide 28 maps Step 4 to 16, 18, 20, 23, 24 and Step 5 to 11, 14, 17, 21. Slides 10 and 14 show `GREETING`. The agenda names image pull Secrets. |
| Blackboard | Section 3: printenv with MESSAGE; two new Explain items (GREETING, MESSAGE). Section 4: `ls -lL`, the permissions; a new Explain item (defaultMode 0440). |

- The lab still has 39 commands on the master (no new command).
- The expected Step 2 output on slide 12: hello, blue, hello blue, blue, prod, debug, 10.96.0.1. Phase 4
  checks it, and the `ls -lL` output, on the live cluster (L7).

### Phase 3: the static gates (run 4, 18:08 to 18:40 EST)
First gate run on the lecture: 5 FAILs, all fixed, then a rebuild of the lab and the lecture:
1. Body text below 12 pt (slide 14, the ConfigMap boxes at 11 pt): 12 pt, and the boxes have more room.
2. A bullet word for word on two slides ("Image pull Secrets", agenda and slide 19): the agenda now says
   "A Secret for the pull of a private image".
3. "variable" without "environment" (slides 8 and 28): "environment variable".
4. and 5. A wrapped terminal line and text past the terminal box (slide 12): the printenv command of
   Step 2 is now two lines in the lab (`... -- printenv GREETING COLOR \` and
   `MESSAGE APP_COLOR APP_MODE LOG_LEVEL KUBERNETES_SERVICE_HOST`). It is still one command.
After my page read: slide 13 terminal moved up (an empty gap), slide 14 boxes got more room, slide 28 line 4
is shorter (it wrapped inside `kube-api-access-<id>`).

| Check | Result |
|---|---|
| Deck gate `Lecture_week12_v8` (32 checks, PowerPoint PDF, 29 pages) | FAILED: 0 |
| Deck gate `Lab_week12_v8` (PowerPoint PDF, 10 pages) | FAILED: 0 |
| PDF Title and Author | set in both PDFs ("Maziar Sojoudian") |
| `pdffonts` | Calibri, Calibri-Bold, Calibri-Italic, Consolas, Consolas-Bold only |
| Page read | all 29 lecture pages and all 10 lab pages read; the three layout defects above fixed and read again |
| Repo folder | 7 files, no cleanup text, `localMachine.sh` byte-equal to `Week12/localMachine_v8.sh` |
| `bash -n` | ok for `bootstrap.sh`, `localMachine.sh`, `master-init.sh.tftpl`, `worker-join.sh.tftpl` |
| `terraform fmt -check` | ok |
| Images (Docker Hub API, HTTP 200) | `maziar/alpine-curl:latest`, `maziar/fortune:args`, `maziar/flannel:v0.28.10`, `maziar/flannel-cni-plugin:v1.9.1-flannel3` |
| Commands on the master | 39 (limit 40) |
| Blackboard text v8 | 7 sections, no "control-plane node", Explain items last |
| Quiz v2 build | GATE 1-7, 8, 8b, 8c, 9, 10, 11, 12, 13, 14: 0 errors; keys 5/5/5/5; longest 4, shortest 5 |
| Quiz v2 pack and audit | ZIP 21 files (20 items), 20 titles, 20 key records, leaks 0, pairs at risk 0, errors 0 |
| Quiz v2 cue simulation | PASS, highest: shortest 5.50 of 20 (limit 6.0) |
| Quiz v2 upload file | byte-equal to v1 (no question changed yet) |

### Phase 4: live pass 1 (run 5, 18:13 to 18:25 EST)
- Sandbox: a copy of the repo folder `Week12/` (7 files) in the scratchpad; `terraform init` and
  `terraform validate` ("Success! The configuration is valid.").
- Apply as a student (`(sleep 10; echo Maziar; sleep 40; echo yes) | terraform apply`): 18:13:41 to 18:15:00,
  "Apply complete! Resources: 15 added, 0 changed, 0 destroyed."
- `cloud-init status`: done. The message of the day names Week 12 and `localMachine.sh`. The master holds no
  cleanup file. The 3 nodes were Ready at 18:16 (v1.35.10, Ubuntu 26.04.1 LTS, containerd 2.2.2).
- Pass 1 (`tools/instrument.py`, delay 0, detached on the master): 23:16:17 to 23:16:41 UTC,
  39 commands, 39 with exit 0, 0 with another exit code.

Comments and samples against the live output (C4):

| Item | Live output | Slide or comment | Result |
|---|---|---|---|
| Step 1 logs | "Configured to generate new fortune every 2 seconds", then a line every 2 s | slide 7 | equal (only the dates differ) |
| Step 2 printenv | hello, blue, hello blue, blue, prod, debug, 10.96.0.1 | slide 12 | equal |
| Step 3 `ls -lL` | `-r--r-----` for APP_COLOR, APP_MODE, GREETING, LOG_LEVEL | lab comment "0440 lets the owner and the group read each file" | equal |
| Step 3 until loop | green, then `printenv APP_COLOR` blue | slide 13, "# still blue" | equal |
| Step 4 | paswrd; paswrd, mysql; mysql; tmpfs; ca.crt, namespace, token; app-secret Opaque 2 | slides 16, 18, 20, 23 | equal, except the tmpfs size: live `size=7814528k`, slide 20 `size=7814532k` (11-11) |
| Step 5 | the three created lines, red, dev, dev-pass | slides 14, 21 | equal |

Probes on the same cluster (`probe12.sh`, all objects in the namespace `probe12`, and one ConfigMap in
`default` for Q18). The proof of each key:

| Q | Key | Live proof |
|---|---|---|
| 1 | D | `printenv KUBERNETES_SERVICE_HOST` 10.96.0.1 = cluster IP of the Service kubernetes 10.96.0.1 |
| 2 | C | apply exit 0; state `CreateContainerConfigError` "configmap "missing-config" not found"; no ConfigMap created |
| 3 | B | "ConfigMap "big" is invalid: []: Too long: may not be more than 1048576 bytes"; exit 1; nothing stored |
| 4 | B | pass 1 Step 3: the file shows green without a restart |
| 5 | C | `base64 -d` of cGFzc3dvcmQ= gives password |
| 6 | A | "BadRequest ... illegal base64 data at input byte 4"; exit 1; no Secret q6 |
| 7 | B | `kubectl exec` reads the value; `kubectl describe pod` shows it 0 times; the volume is tmpfs |
| 8 | A | the log holds the password with secretKeyRef (1), with stringData (1), as non-root (1); with a Secret volume (0) |
| 9 | D | "ls: /var/run/secrets/kubernetes.io/serviceaccount: No such file or directory", exit code 1 |
| 10 | C | 403 Forbidden: "system:serviceaccount:probe12:default cannot list resource pods" |
| 11 | A | pass 1 Step 1: "every 2 seconds" |
| 12 | D | pass 1 Step 2: LOG_LEVEL debug |
| 13 | B | `printenv APP_COLOR` exit code 1, no value; COLOR blue |
| 14 | C | after apply again: blue; in a new shell: blue; after delete and create: green |
| 15 | D | pass 1 Step 4: TYPE Opaque |
| 16 | C | pass 1 Step 4: mysql |
| 17 | D | pass 1 Step 4: app-secret only |
| 18 | A | with app-config green in default: the Pod in week12-dev shows red |
| 19 | A | pass 1 Step 5: dev-pass from etcd |
| 20 | B | env APP_COLOR=blue and envFrom red: printenv shows blue (also the Pod v1 API reference) |

- Slide 19 (concept only): `kubectl create secret docker-registry regcred --docker-username=... --docker-password=...`
  works; TYPE `kubernetes.io/dockerconfigjson`, DATA 1; the default server is `"https://index.docker.io/v1/"`.
- Clean-up: the namespace `probe12` and the ConfigMap `app-config` of `default` deleted; the probe files in
  `/tmp` deleted. Only `week12` and `week12-dev` of the lab stay, and the destroy removes them.
- Destroy as a student: "Destroy complete! Resources: 15 destroyed." (18:23 EST). After: 0 instances in any
  state, and only the `default` security group.
- Open from phase 4: slide 20 shows `size=7814532k` (11-11); live is `size=7814528k`. The size depends on the
  memory of the node, so phase 6 sets the slide to the value of the final pass.

### Phase 5: live pass 2 (run 6, 18:25 to 18:35 EST)
- A new sandbox copy of the repo folder; `localMachine.sh` byte-equal to `Week12/localMachine_v8.sh`;
  `terraform validate` ok.
- Apply as a student: 18:25:38, "Apply complete! Resources: 15 added, 0 changed, 0 destroyed."
  `cloud-init status`: done; 3 nodes Ready; no cleanup file on the master.
- Pass 2 (`tools/instrument.py`, 3 s between commands): 23:28:12 to 23:31:22 UTC, 39 commands, 39 with
  exit 0, 0 with another exit code.
- The outputs equal pass 1: Step 2 hello, blue, hello blue, blue, prod, debug, 10.96.0.1; Step 3
  `-r--r-----` for the four files; Step 4 tmpfs `size=7814528k` (the same as pass 1); Step 5 red, dev,
  dev-pass.
- Destroy as a student: "Destroy complete! Resources: 15 destroyed." (18:35 EST). After: 0 instances in any
  state, and only the `default` security group.

### Phase 6: review round 1 (run 7, 18:37 to 18:58 EST)
Three fresh independent subagents, each with the rules, the files, the course content and the live logs
(not my conclusion). Findings in the scratchpad `w12review_r1/lecture.md`, `lab.md`, `quiz.md`.

| Part | MUST-FIX | SHOULD-FIX |
|---|--:|--:|
| Lecture | 2 | 5 |
| Lab and Blackboard text | 0 | 4 |
| Quiz | 1 | 4 |

All 16 findings are applied:
- Lecture M1 (C4): slide 20 shows `size=7814528k`, the value of pass 1, pass 2 and the probes.
- Lecture M2 (B7): takeaway 6 is "By default, each Pod gets a ServiceAccount token in a projected volume.
  The kubelet renews it, and no Secret holds it" (`automountServiceAccountToken: false` is the exception).
- Lecture S1, S2 (B7): "Concept only" labels on slides 7, 8, 12, 13 (`items` or `subPath`), 17
  (`stringData` or base64), 21, 23 and 24.
- Lecture S3, S4 (B7, no point three times): takeaway 3 states only the change at run time; slide 8 drops
  "A ConfigMap prevents this".
- Lecture S5 (B3): "The ServiceAccount `default`", with the name in Consolas.
- Lab R1-1 (A1 glossary): "two earlier environment variables".
- Lab R1-2 (A1, 6 sentences in a paragraph): the KUBERNETES_SERVICE_HOST comment moves next to printenv.
- Lab R1-3 (C7): Blackboard section 1 is "Build and Check the Cluster" (the words of slide 3).
- Lab R1-4 (A1 glossary): the builder docstrings say "does not overwrite", not "refuses".
- Quiz F1 (D4, MUST-FIX): Q4 A is "The old value, because the files of the volume are read-only"; the old
  option ("only a new container reads the new value") gave the key of Q14.
- Quiz F2 (D2): the Q17 stem names kube-root-ca.crt. The proof: in pass 1, Step 4, the token volume of
  secret-pod in week12 holds ca.crt, which the projected volume takes from the ConfigMap kube-root-ca.crt of
  the same namespace (kubernetes.io, service-accounts-admin).
- Quiz F3 (D3): Q5 B is "Nothing, because cGFzc3dvcmQ= is the password" (probe Q5: the decode gives password).
- Quiz F4 (A1): Q5 D is "The encryption key of the cluster".
- Quiz F5 (A1, -ing forms): the Q8 stem ("so the log holds the password. Which change prevents this?"),
  the Q4 WHY and the Q14 IF D.
- The quiz docstring now names the live proofs of 2026-11-18.

No lab command changed. The runner made from the final `localMachine_v8.sh` is byte-equal to the runner of
pass 2, so the tested commands equal the final commands, and phases 4 and 5 stay valid.

Phase 3 again, on the final files:

| Check | Result |
|---|---|
| Deck gate lecture v8 (29 pages) and lab v8 (10 pages) | FAILED: 0 and FAILED: 0 |
| Fonts | Calibri, Calibri-Bold, Calibri-Italic, Consolas, Consolas-Bold only |
| Page read | the changed pages 5 to 8, 10 to 24 and 27 of the lecture, and pages 5 to 8 of the lab |
| Repo folder | 7 files; `localMachine.sh` = `localMachine_v8.sh`; `bash -n` and `terraform fmt -check` ok |
| Quiz v2 | GATE 1 to 14: 0 errors; keys 5/5/5/5; longest 4, shortest 5; audit errors 0; cue simulation PASS (highest 5.50 of 20) |
| Quiz feedback letters | Q4, Q5, Q8 and Q17: each IF matches its delivered letter |

### Phase 6: review round 2 (run 8, 19:00 to 19:30 EST)
Three new fresh subagents; findings in the scratchpad `w12review_r2/`.

| Part | MUST-FIX | SHOULD-FIX |
|---|--:|--:|
| Lecture | 1 | 4 |
| Lab and Blackboard text | 0 | 1 |
| Quiz | 1 | 1 |

All 8 findings are applied:
- Lecture M1 (B7, a fact): takeaway 3 is "The files of a ConfigMap volume change at run time. An environment
  variable does not change" ("Only" was false: the files of a Secret volume and the token file also change).
- Lecture S1 (B7): labels on slide 10 (the limit of 1 MiB) and slide 16 (the types and the limit).
- Lecture S2 (B7): the slide 23 label also names the renewal of the token and the permissions of `default`.
- Lecture S3 (C8): slide 28 line 5 names the risks of slide 22 (a log file, a child process); the lab does
  put a Secret in an environment variable.
- Lecture S4 (B7): the slide 19 label is "Concept only: the lab does not create a pull Secret, because it
  pulls only public images."
- Lab R2-1 (A1): the builder docstrings have short sentences in the active voice. I also rewrote the
  docstring of the lecture builder in the same way. The outputs of the builders do not change.
- Quiz F1 (D3, MUST-FIX): Q8 key "Mount the Secret as a volume for the password, in place of secretKeyRef";
  Q8 D "Give the password through secretRef, in place of secretKeyRef in env" (the non-root option kept
  "the same secretKeyRef", so a student could remove it with no knowledge).
- Quiz F2 (D3, D4): Q5 D "The base64 encryption key of the cluster".

Phase 3 again: the lecture gate shows FAILED: 0 (29 pages; pages 10, 16, 19, 23, 27 and 28 read); the quiz
build shows 0 errors in all gates, keys 5/5/5/5, longest 4, shortest 5; audit errors 0; cue simulation PASS
(highest: shortest 5.50 of 20; convergence 3.92, odd one out 1.75). The new Q8 D needs a live probe (D5),
so a short probe cluster runs `probe12b.sh`: Q8 with `envFrom: secretRef` and with a Secret volume, and the
Q17 premise (the ConfigMap kube-root-ca.crt in a new namespace).

The probe cluster (19:23 to 19:29 EST): apply "15 added", 3 nodes Ready, then `probe12b.sh`:
- Q17: the new namespace `week12` holds the ConfigMap `kube-root-ca.crt` (DATA 1) after 5 s, and
  `kubectl get secrets` shows "No resources found". The stem premise and the key D are true.
- Q8 D: with `envFrom: secretRef`, the log holds the password (1 line), so D is a wrong option.
- Q8 key: with a Secret volume, the log holds the password 0 times, and the file holds it.
- Clean-up: the namespace deleted. Destroy "15 destroyed"; after it, 0 instances and only `default`.

### Phase 6: review round 3 (run 9, 19:31 to 19:50 EST, the changes of round 2 and their effects, D11 step 5)
Findings in the scratchpad `w12review_r3/`.

| Part | MUST-FIX | SHOULD-FIX |
|---|--:|--:|
| Lecture | 0 | 5 |
| Lab and Blackboard text | 0 | 1 |
| Quiz | 0 | 2 |

All 8 findings are applied:
- Lecture S1, S2 (B7, A1): the labels of slides 10 and 16 name the size limit of a ConfigMap and of a
  Secret; the slide 16 label names only `kubernetes.io/tls`, and bullet 5 points to slide 19 for
  `kubernetes.io/dockerconfigjson`; slide 28 names each topic one time.
- Lecture S3 (B7): the slide 21 label also names the risk of the permission to create Pods.
- Lecture S4, S5 (A1, a fact): the docstring of the lecture builder.
- Lab R3-1 (a fact): the docstrings of both builders state that the guard does not check the repo folder,
  and that only the code that writes the outputs runs under `__main__`.
- Quiz F1 (D3): Q8 D is "Give the password through secretRef, in place of secretKeyRef" (no "in env").
- Quiz F2 (D6): Q5 IF D is "No key of the cluster protects the base64 text in this manifest."

Phase 3 again: lecture gate FAILED: 0 (pages 10, 16, 21 and 28 read); quiz GATE 1 to 14 with 0 errors,
keys 5/5/5/5, longest 4, shortest 5; audit errors 0; cue simulation PASS. The upload file is byte-equal to
the copy that the round 3 reviewer checked. No lab output changed.

### Phase 6: review round 4 (run 10, 19:45 to 20:00 EST, the changes of round 3 and their effects)
Findings in the scratchpad `w12review_r4/`.

| Part | MUST-FIX | SHOULD-FIX |
|---|--:|--:|
| Lecture (deck: no defect; builder docstring only) | 0 | 2 |
| Lab and Blackboard text | 0 | 0 |
| Quiz | 0 | 0 |

- The lab part and the quiz part meet the stop condition (0 and 0).
- The lecture reviewer found no defect in the deck. The two findings are facts in the docstring of
  `build_week12_lecture_v8.py`: the `labeled()` note (slides 7, 21 and 24), and the module docstring
  (slides 10 and 14 and the agenda are v8; the input gives the agenda too; "only the type"; the
  `--force` exception). Both are applied. The deck, the PDF and the other outputs did not change.

### Phase 6: review round 5 (run 11, 19:55 to 20:05 EST, the lecture builder docstring only)
Findings in the scratchpad `w12review_r5/lecture.md`: 0 MUST-FIX, 1 SHOULD-FIX. The deck has no defect,
and the deck and its PDF did not change after round 4.
- S1 (a fact): docstring line L6 said that each manifest and each terminal come from lab v8. Slide 7 is
  the exception: its `kubectl wait` lines are in the v7 function `s_args`, and `fortune-args.yaml` comes
  from lab v1. Both agree with Step 1 of lab v8, so C8 holds. The docstring now names the exception.

### Phase 6: review round 6 (run 12, 20:07 to 20:13 EST, the L6 item of the lecture builder docstring)
Findings in the scratchpad `w12review_r6/lecture.md`: 0 MUST-FIX, 0 SHOULD-FIX. The reviewer checked all
16 labeled boxes of the deck (10 terminals, 6 manifests): slide 7 is the only exception, as L6 says.

The last review of each part is 0 and 0: the lab and the quiz in round 4, the lecture in round 6. No part
changed after its last review. The final report is `reports/report-2026-11-18-07-week12-v8-final.md`.

## Results
- Phase 0 is complete.
- Phase 1 is complete: 1 MUST-FIX, 7 SHOULD-FIX, 1 check, 1 note. The live work waits for phases 4 and 5. The tools for Week 12 run from the new path.
- The account has no instance now, so the 9-instance limit allows the live passes.

## Issues / Notes
- Other tools still name the old path (report #01 of today); they are not in the Week 12 chain.
- No server started, so no port is used.
