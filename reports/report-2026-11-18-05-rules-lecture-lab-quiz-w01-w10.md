# Report: The rules and standards for the lectures, labs and quizzes of Weeks 01 to 10
**Date**: 2026-11-18
**Sequence**: #05 for the day

## Summary
This is a read-only pass. I read `CLO835_STANDARDS.md` v1.2 (2026-11-11, Parts A to H), the memory index of
the old project path (69 files), and the quiz folders. This report collects the rules for the lectures, the
labs and the quizzes of Weeks 01 to 10. Week 11 (the exam) is not in it. Week 08 is the study week and has
no lecture, lab or quiz.

## What Changed
- Created this report. No other file changed.

## Technical Details

### 0. The rule sources and their order
1. `~/.claude/CLAUDE.md` and the project `CLAUDE.md`: ASD-STE100 first, scope second, 1 to 4 line answers
   third.
2. `CLO835_STANDARDS.md` v1.2. Where two sources do not agree, its newer rule wins.
3. `~/.claude/PREFERENCES.md` (15 sections, 2026-10-27).
4. `PROMPT.md` and `DESIGN_LANGUAGE.md` (the deck spec of 2026-05). The standards file replaces R1, R7, R8,
   the 44 pt cover, the `soffice` render, the reference deck `Week04_v02_02` and the colour F07178.
5. The feedback memories (for example the MCQ rules of 2026-10-26 and the quiz review lessons).

### 1. Rules for all material (Part A)
- Language: ASD-STE100 in every slide, lab comment, Blackboard text, stem, option and feedback.
  - Procedural sentence 20 words or fewer; descriptive sentence 25 words or fewer (the gate fails above 25).
  - Active voice, present tense, one instruction in one sentence, the verb first, the articles kept.
  - No contraction, no possessive `'s` in a deck, no slang, no idiom, no phrasal verb, no "we".
  - Paragraph of 6 sentences or fewer; a vertical list for complex data.
  - A word for the digits 2 to 9 before "step", "file", "method", "way", "entries", "section".
- One word for one meaning (the glossary of A1):
  - Kubernetes (not K8s), Pod (not pod), directory (not folder), create (not make);
  - master node in lab and Blackboard texts (not control-plane node);
  - claim or PersistentVolumeClaim (PVC), PersistentVolume (PV) at first use;
  - show (not print), reject (not refuse), setting or field or flag (not option or parameter);
  - environment variable (not variable alone), ConfigMap and etcd.
- Banned words in a deck outside Consolas: options, parameters, keep, keeps, way, ways, description, entries,
  resource, POD, K8s-, Config Map, ETCD, we, command line, control-plane node, variable (alone), and others.
- Files and versions (A5):
  - Never overwrite a delivered file. Bump the version for each rebuild after a delivery.
  - Each builder has `VERSION`, a `__main__` guard and `--force`. A builder never writes its input deck.
  - Names: `WeekNN/Lecture_weekNN_vN.pptx`, `WeekNN/Lab_weekNN_vN.pptx`, `WeekNN/localMachine_vN.sh`,
    `WeekNN/Lab_weekNN_Blackboard_Submission_vN.md`, `quiz_pool_src/Quiz_WNN_Easy20/`.
- Tools (A6): absolute paths, no `cd`; the editor is vi (never nano); deck PDFs come from PowerPoint, not
  LibreOffice.
- "Fixed" or "good" is 0 or 1 (A7): read all rule sources, run the gate, read every PDF page, get an
  independent review, fix and repeat, and state the scope of the claim.

### 2. Lecture decks (Part B)
Canvas and chrome (B1):
- 13.333 x 7.5 in (16:9), white, blank layout. Calibri and Consolas only, in the `.pptx` and in the PDF.
- The whale at (0.45, 6.85), 0.5 x 0.5 in, and the footer `CLO835, Fall 2026     N / TOTAL` on every slide.
- No shape in the title band (0.3 to 1.42 in) except the title, no shape in the footer band (below 6.705 in)
  except the chrome, no shape off the canvas, integer coordinates only.
- Size near 1 MB. File Title, Author "Maziar Sojoudian" and Last Modified By set in `.pptx` and PDF.
- No blank thumbnail, no speaker notes, no hidden slide unless the source hides it.
- Only two pictures: the whale and the Kubernetes logo. Everything else is a native shape.

Palette (B2): BLUE 1FA8E0, SLATE 37465A, BODY 3F3F3F, MUTED 868686, LIGHTBLUE CFDBEE, CARD_BG F4F7FB,
RULE_GRAY E0E0E0, GOAL_GREEN 27AE60, ALERT_RED E74C3C, TERMBG 2A2A2A, the six STEPS fills, the terminal
colours 3A3A3A, FF5F56, FFBD2E, 27C93F, BABABA, 4EC9E0, and white. No other colour.

Text (B3, B4):
- Cover title 34 pt. Content title 30 pt, bold, BLUE. Body at least 12 pt. Terminal text 9 to 14 pt.
- Consolas, bold SLATE, for a code name, a command, a file name, a path and an IP address in body text.
- Bullets: the glyph "▪" as a bold run plus a tab, with a hanging indent. Keep the bullet hierarchy.

Terminals (B5):
- Each command starts with `$` (master) or `L$` (own machine). A comment and a sample output start with `#`.
- No wrapped line and no text past the terminal box in the PowerPoint PDF. Only ASCII in Consolas.
- Each command runs on the course cluster with current syntax. A terminal labeled "Lab Week N, Step M" holds
  only commands of that lab step.

Diagrams (B6): native house diagrams; no third-party screenshot, watermark, WMF or image below 110 DPI; a
shape arrow (not a connector) for a horizontal or vertical arrow; labels 0.40 in past a logo ring.

Content (B7):
- Every fact correct for Kubernetes v1.35, checked on kubernetes.io or on the live cluster. Name the version
  when a feature became stable. Current API only; mark a deprecated feature.
- State a point one time (two times only when necessary, never three). No two slides with the same title, no
  bullet word for word on two slides, no fragment card. No two lectures hold the same slide.
- The slide order: cover, agenda, Course Outline (follows the schedule G3), part dividers, content, Optional
  Topics ("not in the lab or in the quiz"), Key Takeaways, "Lab Week NN at a Glance".
- "Lab Week NN at a Glance" maps each lab step to its slides and names, under "Not in the lab", each topic
  that the lab does not practise.
- The lecture uses the object names of the lab. A concept that the lab does not run gets "Concept only: the
  lab does not run X."
- Each reference link returns HTTP 200 and names no third-party account.
- The reference redesign is `week01/Week01_lecture_style_v5.pptx`.

Build and QA (B8): build, export through PowerPoint (`tools/deck_pipe.sh`), run the 32 deck checks of
`gate_week12.deck_checks` (`FAILED: 0`), read every PDF page, get an independent review, then repeat.

### 3. Labs (Part C)
Size and structure (C1):
- One workshop: Step 0 to Step 6, about 30 to 40 commands on the master, 90 minutes. Weeks 03 and 04 are the
  size model. The user rejected a lab of 21 steps.
- The deck has 10 slides: title "Workshop 1 – <topic>", "Lab Week NN - Prerequisites", the cluster slide
  (Step 0), five step slides (Steps 1 to 5), "Destroy the cluster" (Step 6, only `terraform destroy`), and
  "Workshop 1 – The End".
- One step on one terminal slide. A step with a manifest uses two panels: terminal left, file right.
- The label is "Lab Week NN", never "Lab NN".
- The lab practises every lecture topic within the size limit. The size limit wins.

One content list (C2): `SLIDES` in the builder makes the deck, `localMachine.sh`, the repo copy and the
Blackboard text. Each script step names its slide. `check_lines()` rejects non-ASCII.

Commands (C3):
- Each command runs as shown on the live cluster and exits 0.
- `kubectl wait` in place of a long `sleep`. Manifests with `cat > file.yaml <<'EOF'`.
- Images of Docker Hub `maziar` only (plus Docker Official Images and the kubeadm images), with a tag that
  exists. Helper image `maziar/alpine-curl`, never `busybox`. Never `luksa/kubia`; use `maziar/kubia`.
- Record the change-cause after each `kubectl set image`. One name for each object in the lab and lecture.

Comments and sample output (C4): they agree with the live output and the current versions (v1.35.10). They
explain an output that can confuse a student, in the words of the lecture.

The repo folder of a week (C5):
- The 7 files of Week 04 (`.gitignore`, `bootstrap.sh`, `localMachine.sh`, `main.tf`,
  `master-init.sh.tftpl`, `variables.tf`, `worker-join.sh.tftpl`) plus the extras. No README.
- `key_name` has no default. `lab_instance_profile` defaults to `LabInstanceProfile`.
- No cleanup script since 2026-11-11: Step 6 is only `terraform destroy`. Exception: Week 03 (Docker on the
  laptop) keeps `cleanup_lab03.sh`.
- No Terraform state, `.terraform`, `.pem` or key file in the repo. Scan (F3), `bash -n`,
  `terraform fmt -check`, and `terraform validate` in a sandbox copy.

The cluster (C6): kubeadm on EC2, 1 master and 2 workers, `m5.large`, Ubuntu 26.04, Kubernetes v1.35,
containerd, Flannel, MTU 1500. Never kind, no EKS for students, no Helm. Storage: local-path provisioner
`maziar/local-path-provisioner:v0.0.37`, StorageClass `standard`, WaitForFirstConsumer, reclaimPolicy Delete.

The Blackboard lab text (C7):
- The model is `Lab04 - 2.5%` (Lab Week 06). Start with `# Lab Week NN: <Topic>` and
  `## Submission Instructions` ("all 7 sections", the recording paragraph).
- One section for each step, `## 1.` to `## 7.` ("Destroy the Cluster"). Each has an intro, `You must:`,
  `Run ...` and `Show ...` items, and the `Explain ...` items last.
- End with `## Submission Requirements` (six items) and the "Important: Use your own screenshots ..."
  paragraph. No Academic Integrity Pledge. "master node", "control-plane Pods".
- Each `Run` item names a command of that step; each `Explain` item has its answer in the lecture or a lab
  comment (the runnable table of F4).

Lecture and lab agree (C8): each command of a "Lab Week NN, Step M" terminal is in that step; each manifest
is identical; "Lab Week NN at a Glance" stays true when the lab changes.

Lab checks and live test (C9, E3): the 7 files, at most 40 commands, Step 0 to 6, `bash -n`, `terraform
fmt`, no cleanup script, repo script equals deck script, `maziar` images only. Live: a sandbox copy, two full
passes on two new clusters with 0 non-zero exits, all probe objects deleted, a final pass with the final
files, and "Destroy complete! Resources: 15 destroyed." with 0 instances left.

Blackboard lab items (G1, G2): Lab Week 05 = `Lab03`, Week 06 = `Lab04`, Week 09 = `Lab05`, Week 10 =
`Lab06`. An item is "File upload and Text entry", 100 points, 1 attempt, grades posted by hand.

### 4. Quizzes (Part D)
Kinds (D1):
- Weeks 01 to 03: a pool of 100 questions for each lecture (`weekNN/WeekNN_Pool_Blackboard.txt`).
- Easy quizzes of 20 questions (10 lecture, 10 lab), every student gets all 20: `Quiz_W01W02_Easy20`,
  `Quiz_W03W04_Easy20`, `Quiz_W05W06_Easy20`, `Quiz_W09_Easy20`, `Quiz_W10_Easy20`. Week 07 has no quiz
  folder.

Each question (D2, the rules of 2026-10-26):
- One important concept, not a small detail. The question stands alone (no slide, picture, step or table).
- Only content that the course teaches. Knowledge true in any good source. No slide, page or week named.
- Prefer an application question with one clear result. A prepared student answers in 1 to 2 minutes.
- No negative stem ("not" fails the audit). A short form defined at first use, for example
  "PersistentVolume (PV)".
- The stem names every object that an option names, and closes each gap of the scenario.

Options (D3):
- 4 options, exactly 1 correct. Each wrong option is a real student mistake.
- No trick option, no "all/none of the above", no "both A and B", no option that starts with "Both".
- Each option fits the grammar of the stem. Numbers, times and names in logical order.
- The key is strictly longest in about 1 of 4 questions and strictly shortest in about 1 of 4 (GATE 9).
- No option implies another, contradicts itself or contradicts the stem.
- No word or form only in wrong options or only in keys across the quiz. The key is not the only option of
  its form and not the convergence centre. The key repeats no stem word that no wrong option repeats.

Across the quiz (D4): each fact one time; no question gives the answer to another; no repeat of an earlier
pool (GATE 10); the same difficulty; no copy of a practice question with new names.

Correctness and proof (D5): each key has a proof (live lab log, probe run, or the Kubernetes documentation),
listed in the report. A wrong lecture slide gets fixed in the deck too.

Feedback (D6): WHY for the key; one IF for each wrong option in the order of `a[1:]`; no slide, week or deck
named; correct also for edge cases.

Platform (D7): keys balanced 5 A, 5 B, 5 C, 5 D; no run above 3 equal letters; each letter 2 or 3 times in
each half; no alternation over 5, no ABCD or DCBA run, no repeated block of 3; neutral titles
`clo835-eNN-001 topic`; no `<`, `>` or `&`.

Tools (D8 to D10): the builder `build_easy20_wNN.py` (GATE 1 to 14, writes nothing on a failure),
`qti_pack.py`, the audit `audit_easy20_wNN.py`, and `tools/quiz_cue_sim.py` (FAIL above 6.0 of 20 for any
guess strategy, ties shared).

Review loop (D11): build, audit and simulate; a fresh independent reviewer each round with MUST-FIX and
SHOULD-FIX lists; apply all; prove new scenarios live; stop at 0 and 0. Week 09 took 6 rounds, Week 10 took
11.

Delivery (D12): a test uses "Upload questions from file" with the `.txt`; a question bank imports the QTI 2.1
ZIP; set the points with Bulk Edit Points; show only the grade until all students finish; auto post off for
an exam window; review a question below 30 % or above 95 % correct, or with low discrimination.

### 5. Week notes for Weeks 01 to 10
| Week | Topic | Notes |
|---|---|---|
| 01 | Docker Introduction | The lecture `Week01_lecture_style_v5` is the reference redesign. Pool of 100. |
| 02 | Docker Image Management | Pool of 100. Easy quiz W01W02. |
| 03 | Docker Networking, Storage and Security | Lab on the laptop Docker, keeps `cleanup_lab03.sh`. Pool of 100. |
| 04 | Kubernetes Introduction | The lab size model with Week 03. The 7 repo files are the template. Easy quiz W03W04. |
| 05 | Pods and ReplicaSets | Lab Week 05 = `Lab03`. Open item: the lab has Step 0 to Step 13. |
| 06 | Services and Deployments | Lab Week 06 = `Lab04`, the model of the Blackboard text. Easy quiz W05W06. |
| 07 | Volumes | No quiz folder. |
| 08 | Study Week | No material. |
| 09 | PVs and Kubernetes in EKS | Lab Week 09 = `Lab05`. Students have no EKS, so EKS is concept only. Easy quiz W09. |
| 10 | StorageClasses and StatefulSets | Lab Week 10 = `Lab06`. Easy quiz W10. |

## Results
- The rule set for Weeks 01 to 10 is in sections 1 to 5. The source is `CLO835_STANDARDS.md` v1.2 and the
  feedback memories.

## Issues / Notes
- Some files still name the old path `/Users/maziar/Downloads/k8s_week3` (report #01 of today).
- This report names no account number, no key fingerprint, no student and no private IP address.
- No server started, so no port is used.
