# Report: Repository analysis, run 14 (the new path k8s_private)
**Date**: 2026-11-14
**Sequence**: #01 for the day

## Summary
Run 14 is a read-only pass over the project after its move from `~/Downloads/k8s_week3` to
`~/Documents/c/r/k8s_private` (2026-11-14). I read the rule sources, the memory of the old path, the reports
after run 13, the chat records after 2026-11-11, the engines and the gate. I ran the deck gate on the current
decks of 12 weeks, the cue tool on the two newest quizzes, and compared the public course repo with the local
lab scripts. The new findings: the new repo `sojoudian/k8s_private` is public, the move broke the hard-coded
paths, the local clone of the course repo is gone, and the user hand-edited two delivered lectures on 11-11.

## What Changed
- Created this report.
- No project file changed. No git operation. No AWS call. No memory file changed.
- Scratch scripts only, in the session scratchpad: `prompts.py`, `answers.py`, `graph.py`, `gateall.py`,
  `pptx_vs_pdf.py`, and the folder `raw/` (copies of the public `localMachine.sh` files).
- Network: anonymous reads of public GitHub pages, the GitHub API, raw files and `git ls-remote`.

## Technical Details

### 1. What the project is
- The private work folder of the professor for CLO835 "Portable Technologies in Cloud", Seneca, Fall 2026,
  section NCE (class 6401). Hybrid: Wednesday 19:00 in person, Friday 17:10 online.
- It holds the lecture decks, the lab decks, the lab scripts, the quizzes, the exam, the assignments, the
  semester project specs, the Python builders that make them, the QA gates, and 184 reports.
- The student material goes to a second, public repo: `github.com/sojoudian/CLO835_Fall_2026`.
- Grading (syllabus): quizzes 10 %, labs 20 %, assignments 30 % (2 x 15 %), mid-term 20 %, project 20 %.
- Calendar position today (Saturday 2026-11-14): Week 11 (the exam of 11/11) is over. Week 12 ConfigMaps and
  Secrets starts 11/18. Lab06 (Lab Week 10) is due Saturday 11/21. Week 13 RBAC is 11/25, Week 14 HPA 12/2,
  Week 15 the project presentation 12/9.

### 2. The rule sources and their order
1. `~/.claude/CLAUDE.md` and the project `CLAUDE.md`: ASD-STE100 first, scope second, 1 to 4 line answers third.
2. `CLO835_STANDARDS.md` v1.2 (2026-11-11), Parts A to H. Where sources disagree, its newer rule wins.
3. `~/.claude/PREFERENCES.md` (15 sections, 2026-10-27). Section 15 still says that master-init writes
   `cleanup_labNN.sh`; standard C5 (2026-11-11) replaces that rule.
4. `PROMPT.md` and `DESIGN_LANGUAGE.md` (2026-05): the design spec. The standard replaces R1, R7, R8, the
   44 pt cover, the soffice render, the reference deck and the colour F07178.
5. The memory folder of the OLD path, 70 files (see section 3).

### 3. The move of 2026-11-14 and what it broke
- `git init`, then commit `840e1c7` "create the remote repo for the course" (18:14, author
  `BartyCrouch <sojodyan@gmail.com>`), pushed to `github.com/sojoudian/k8s_private`.
- The GitHub API says `"private": false, "visibility": "public"` (created 23:13 UTC). The page answers 200 to
  an anonymous request.
- The commit tracks 2258 files (the `.git` folder is 496 MB). The root has no `.gitignore`, so the commit
  also holds 49 `__pycache__` files, 9 `.DS_Store` files and 2 `.claude/` files. `.venv` is not tracked.
- The public tree holds 30 answer-key files: the mid-term exam keys (v1 and v2), the pools and the easy
  quizzes, also `Quiz_W12_Easy20` and `Quiz_W13_Easy20`, which students did not take yet.
- It holds 22 grading reports in `reports/` with student identifiers in the file names.
- `a1.zip` and `a1/` (standard F3) are not in the folder. A secret scan of the tracked text found no AWS key
  and no private key (3 hits are the text `aws_secret_access_key=...`).
- Hard-coded old path `/Users/maziar/Downloads/k8s_week3`, which does not exist now:
  - `tools/rungate.py` and `tools/deck_pipe.sh` (the deck pipeline of standard B8);
  - 7 quiz audits `quiz_pool_src/audit_easy20*.py` and `rejected_v1/build.py`;
  - `CLO835_STANDARDS.md` (A4, A5, A6, Appendix) and the Scope line of the project `CLAUDE.md`.
- `.venv`: `bin/python` works (Python 3.13.18, python-pptx 1.0.2). The scripts in `bin/` (pip and others)
  have the old path in their first line.
- Memory: the 70 memory files stay under `~/.claude/projects/-Users-maziar-Downloads-k8s-week3/memory/`.
  The memory folder of the new path is empty, so a new session here does not load them.
- The local clone `~/Documents/c/r/CLO835_Fall_2026` does not exist. 40 Python files read it
  (`lab_kubeadm.REPO`, `gate_week12.REPO`, the gates of Week 13 and every lab builder). `make_repo_folder()`
  reads the template with `git -C REPO show HEAD:Week06/...`, so each lab builder now stops. The only other
  clone is `~/Documents/c/r/a2_test/CLO835_Fall_2026`, from 2026-10-14 (HEAD `39a43b1`).

### 4. The folders
- Week folders: `week01`, `week02`, `week03`, `Week04` (and `Week04/FINAL`), `Week05`, `Week06`, `Week07`,
  `Week09` (PVs and EKS), `Week10` (StorageClasses and StatefulSets), `Week12`, `week13`, `week14`.
  `Week11-Exam` and `untitled folder` are empty. No `Week08` (study week).
- `quiz_pool_src/`: the quiz sources, builders, audits, the QTI packer and the delivered quiz folders.
- `tools/`: `export_pdf.sh`, `deck_pipe.sh`, `rungate.py`, `sheet.py`, `instrument.py`, `quiz_cue_sim.py`.
- `Assignments/` (1 and 2), `project/` (16 project specs, v1 and v2, `.docx`), `CLO835_SYL/` (2 syllabus PDFs).
- `finalWork/` (the assembled set of July), `old/`, `old_assessments/`, `analysis/` (renders of May to July),
  `ARCHITECTURE/` (runs 1 to 7), `Labs/` (the early Blackboard texts; `LabNN.txt` is Week NN+1).
- `reports/`: 183 reports before this one, 2026-05-19 to 2026-11-11.

### 5. The build system (96 Python files in the root, 38 in `quiz_pool_src`, 4 in `tools`)
Four generations:
1. May: `build_week3.py`, `build_week03.py`, `build_lab.py`, `build_lab_guide.py`, `build_week04.py` (v13),
   `build_week05.py` (v12), `build_week06.py`. No `__main__` guard; a run or an import writes the output.
2. June and July: `build_week07.py` (no guard), `build_week08.py` (the helpers `E` that later builders
   import), `build_week09.py`, and `build_week12.py` (2371 lines, the DECK engine). `build_week01.py`,
   `build_week02.py`, `build_lab01.py`, `fix_week03.py`, `build_week12_v3_lab.py`, `build_week13.py` and
   `build_week14.py` import that engine.
3. October: `dedup_lectures.py`, `retarget_accounts.py`, `retarget_kind.py`, `retarget_docx.py` (kind to
   kubeadm, other accounts to `maziar`), and the short labs on `lab_kubeadm.py`.
4. 2026-11-09 to 11-11: `build_week07_lecture_v7.py` is the slide kit (native slides, tab bullets,
   `set_pdf_info`). `build_week10_lecture_v10/v11`, `build_week12_lecture_v7` and `build_week13_lecture_v9`
   import it. Each new builder has `VERSION`, the guard and `--force`. A small builder imports the version
   before it and replaces only some slide functions (for example lecture 07 v8, lecture 10 v12).

The lab chain:
- `build_week06_lab_v3.py` is the lab engine. Its input is the template deck `Week05/Lab_week05_v4.pptx`.
  A slide list `SLIDES` of `("step", title, ..., lines)` and `("step2", ..., file lines)` makes the deck and
  `localMachine.sh`, so they cannot differ.
- `lab_kubeadm.py`: `make_lab()` (deck and script) and `make_repo_folder()` (the 7-file week folder from the
  Week06 template of the course repo, or 8 files with a cleanup script).
- `lab_destroy_only.py`: `destroy_step()` and `destroy_section()` give Step 6 "Destroy the cluster" and
  section 7 "Destroy the Cluster" (the rule of 2026-11-11).
- The newest lab builder of each week imports the one before it: W05 v5, W06 v5, W07 v4, W09 v5, W10 v5,
  W12 v7, W13 v5, W14 v3.

### 6. The cluster and the lab
- kubeadm on EC2: 1 master and 2 workers, `m5.large`, Ubuntu 26.04, Kubernetes v1.35 (v1.35.10 measured),
  containerd, Flannel, MTU 1500. `terraform apply` adds 15 resources. No kind, no EKS, no Helm.
- Storage: the local-path provisioner `maziar/local-path-provisioner:v0.0.37`, StorageClass `standard`,
  WaitForFirstConsumer, reclaimPolicy Delete.
- The week folder: `.gitignore`, `bootstrap.sh`, `localMachine.sh`, `main.tf`, `master-init.sh.tftpl`,
  `variables.tf`, `worker-join.sh.tftpl`, plus the extras of the week. Only Week 03 keeps a cleanup script.
- A lab: Step 0 to Step 6, at most 40 commands, a 10-slide deck, the long Blackboard text with 7 sections.

### 7. The QA tools
- `gate_week12.deck_checks()` holds the 32 deck checks. It reads files only. Its lab, Blackboard and live
  checks hold Week 12 names. `gate_week13_v2.py` imports it for Week 13.
- `tools/instrument.py` turns `localMachine.sh` into a runner with exit codes; it splits heredocs and `\`.
- `tools/quiz_cue_sim.py`: 13 guess strategies, FAIL above 6.0 of 20.
- `tools/export_pdf.sh` makes the PDF through PowerPoint with AppleScript (real Calibri and Consolas).

### 8. The deck gate on the current decks (run today, read-only, with `ROOT` set to the new path)

| Week | Deck | Fails | Main causes |
|---|---|--:|---|
| 01 | `Week01_lecture_style_v5` | 13 | substitute PDF fonts, 6 images below 110 DPI, title band, duplicate titles, K8s/POD, author |
| 01 | `Week01_lecture_style_v6` | - | no PDF |
| 02 | `Week02_lecture_style_v1` | 13 | size, PDF fonts, DPI, 11.5 pt, contractions, curly quote in Consolas |
| 02 | `Lab01_v1` | 6 | PDF fonts, colour F07178, a wrapped terminal line, author |
| 03 | `Week03_lecture_style_v2` | 10 | PDF fonts, bands, 10.5 pt, contractions, colour FF6B6B |
| 03 | `Lab03_lab_style_v1` | 12 | PDF fonts, 8 pt terminals, non-ASCII in Consolas, text past a terminal |
| 04 | `FINAL/Week04_v2`, `FINAL/Lab_week04_v2` | - | no PDF |
| 05 | `lecture_week05_v4` | - | no PDF |
| 05 | `Lab_week05_v5` | 5 | 8 pt terminals, "we", commands with no `$`, thumbnail, file title |
| 06 | `Week06_lecture_style_v7` | 13 | PDF fonts, page count, hidden slide 12, notes on slide 18, a wrapped line |
| 06 | `Lab_week06_v5` | 2 | thumbnail, file title |
| 07 | `Lecture_week07_v8` | 1 | the PDF is older than the `.pptx` (section 10) |
| 07 | `Lab_week07_v4` | 0 | |
| 09 | `Lecture_week09_v7` | 8 | PDF fonts, title band, notes, 11.5 pt, K8s/POD, colour FF6B6B |
| 09 | `Lab_week09_v5` | 2 | thumbnail, file title |
| 10 | `Lecture_week10_v12` | 1 | the PDF is older than the `.pptx` (section 10) |
| 10 | `Lab_week10_v5` | 0 | |
| 12 | `Lecture_week12_v7`, `Lab_week12_v7` | 0, 0 | |
| 13 | `Lecture_week13_v9`, `Lab_week13_v5` | 0, 0 | |
| 14 | `Week14_lecture_style_v11` | - | no PDF |
| 14 | `Lab_week14_v3` | 3 | `busybox:1.36`, thumbnail, file title |

### 9. The course repo on GitHub
- Commits: `ad93eb8` (11-05, the rewritten history), `5f8a655` (11-10), `5b97e4f` (11-11, no cleanup in 8
  weeks), `7c4d9b8` (2026-11-13 13:50, "add week12"). All by `BartyCrouch`.
- `7c4d9b8` changes Week12 (cleanup script deleted, lab v7) and Week13 (lab v5).
- The public `localMachine.sh` equals the newest local script for Weeks 06 (v5), 07 (v4), 09 (v5),
  10 (v5), 12 (v7), 13 (v5) and 14 (v3). Week 05 has no local `localMachine_vN.sh`.
- Week 12 lab v7 and Week 13 lab v5 had no live test (report 2026-11-11-03: the AWS session ended).
- Clones made before 2026-11-05 still stop at `git pull` (exit 128, open item H1).

### 10. Hand edits of the user, 2026-11-11, in PowerPoint
Both decks were saved by "Microsoft Macintosh PowerPoint" after their PDFs (00:09):
- `Week07/Lecture_week07_v8.pptx` (15:44):
  - slide 6: the bullet "Weeks 9 and 10 teach PersistentVolumes in detail" is gone;
  - slide 7: "The Week 10 lecture teaches claims" is gone;
  - slide 11: the bullet "Lab Week 07, Step 1 uses this manifest" is gone;
  - slide 18: the text is now "The provisioner creates a PersistentVolume: a PersistentVolume backed by a
    directory on the node of the Pod." (the chat of 20:42 UTC proposed "backed by").
- `Week10/Lecture_week10_v12.pptx` (18:37): slide 9 loses "(Week 7)" after "for example nfs".
- The builders `build_week07_lecture_v8.py` and `build_week10_lecture_v12.py` do not hold these edits.
  A run with `--force` gives the old text. The PDFs show the old text.
- The pattern of the edits: the user removes references to other weeks and lab steps from lecture text.

### 11. The chat records after run 13
- Session `4b692c4c`, 11-11 06:38 local: "fix the Week 13 100 %". Result: report 2026-11-11-03 (all work
  that needs no AWS; live tests not done).
- Session `4607d34d`, 11-11: "do I have maziar/fortune" (on Docker Hub, tags `args` and `env`, not local);
  the question on the provisioner slide (section 10); 11-13: "do a pwd".
- The old Week 12 test cluster: its destroy got 403 (`voc-cancel-cred`) at 11-11 07:50 UTC. Its Terraform
  state was in a scratchpad folder that is empty now. So `terraform destroy` cannot remove it. I made no AWS
  call, so its state in AWS is not known.

### 12. The quizzes
- Pipeline: `q_easy20_wNN.py` (records t, q, a, fix, why, mis) -> `build_easy20_wNN.py` (GATE 1 to 14)
  -> `qti_pack.py` -> `audit_easy20_wNN.py` -> `tools/quiz_cue_sim.py`.
- Today: the cue tool passes `Quiz_W12_Easy20` and `Quiz_W13_Easy20` (20 rows each).
- Proofs still pending: Week 12 Q8, Q18, Q20 (`probe4.sh`), and the Week 13 probe keys (`probe_w13.sh`).
- Run 13 results stand: the cue tool fails W09, W03W04, W05W06 and the exam v2.

## Results
Findings, ranked:
1. `sojoudian/k8s_private` is public. It holds 30 answer-key files (also the keys of the Week 12 and Week 13
   quizzes and the exam) and 22 grading reports with student identifiers in the file names.
2. The local clone `~/Documents/c/r/CLO835_Fall_2026` is gone, so every lab builder and the lab checks of the
   gates stop.
3. 10 scripts and the standards file name the old path `/Users/maziar/Downloads/k8s_week3`. The deck
   pipeline (`rungate.py`, `deck_pipe.sh`) and 7 quiz audits fail.
4. The memory of the project is under the old path. The memory folder of the new path is empty.
5. Week 12 lab v7 and Week 13 lab v5 are public but have no live test. Week 12 starts 11/18.
6. The old Week 12 test cluster has no Terraform state now; its AWS state is not known.
7. The hand edits of 11-11 in lecture 07 v8 and lecture 10 v12 are not in the builders, and the PDFs are old.
8. "control-plane node" stays 3 times each in the Blackboard texts W06 v6, W09 v5 and W10 v5 (C7). W05 v2
   and W14 v3 are the old short form with a pledge.
9. The deck gate fails 13 older decks (section 8). 6 current decks have no PDF.
10. Open items of run 13 that did not change: H3 ("makes a directory" in lecture 10 v11/v12 builders),
    the cue results of older quizzes and the exam, the project overview (it says 15 projects; 16 exist),
    the commit identity `BartyCrouch`.

No server started, so no port is used.

## Issues / Notes
- I did not run any builder, because they write into the project or the course repo.
- I did not open a deck in PowerPoint and made no new PDF.
- I did not run the lab or live checks of the gates (no clone, no AWS).
- The chat records hold Learner Lab credentials of 10-31; my scripts masked them and this report holds none.
- This report is in a folder that the public repo tracks. It names no account number, no IP address and no
  student.
