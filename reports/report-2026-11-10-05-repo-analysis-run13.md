# Report: Repository analysis, run 13 (the changes of 2026-11-09 and 2026-11-10)
**Date**: 2026-11-10
**Sequence**: #05 for the day

## Summary
Run 13 checks all changes after run 12 (2026-11-09 23:13). The new work is the Week 07 lecture v7 and lab v3, the Week 10 lecture v10 and v11, the Week 10 lab v4 and quiz, `CLO835_STANDARDS.md` and `tools/`. I ran the 5 new deck builders and the Week 10 quiz builder in a sandbox. All 13 outputs are equal to the stored files, and the 5 new decks pass the 32 deck checks. A new finding: the cue tool of the standard fails the delivered Week 09 quiz and the exam of 11/11. On the exam, the strategy "pick the option with the most words" gets 15.8 of 26 MC rows.

## What Changed
- Created this report.
- Updated the memory files `project-clo835-arch-analysis.md`, `reference-chat-log-4b692c4c.md` and `MEMORY.md`.
- No project file changed. No file in `~/Documents/c/r/CLO835_Fall_2026` changed.
- All builds ran in the scratchpad sandbox `run13/`, with `HOME` set to a sandbox folder that holds a copy of the course repo.
- I made no AWS call, no commit and no push. The only network requests were anonymous HTTP reads of public pages.

## Technical Details

### 1. Changes after run 12
- New builders: `build_week07_lecture_v7.py`, `build_week07_lab_v3.py`, `build_week10_lecture_v10.py`, `build_week10_lecture_v11.py`, `build_week10_lab_v4.py`.
- New quiz files: `quiz_pool_src/q_easy20_w10.py`, `build_easy20_w10.py`, `audit_easy20_w10.py`, and the folder `Quiz_W10_Easy20/` (4 files).
- New decks and PDFs: `Week07/Lecture_week07_v7`, `Week07/Lab_week07_v3`, `Week10/Lecture_week10_v10`, `Week10/Lecture_week10_v11`, `Week10/Lab_week10_v4`.
- New lab files: `Week07/localMachine_v3.sh`, `Week07/Lab_week07_Blackboard_Submission_v3.md`, `Week10/localMachine_v4.sh`, `Week10/Lab_week10_Blackboard_Submission_v4.md`.
- New standard: `CLO835_STANDARDS.md`. It is version 1.1 now (44.6 KB, 22:31), with the 20 fixes of an independent review.
- New folder `tools/`: `export_pdf.sh`, `deck_pipe.sh`, `rungate.py`, `sheet.py`, `instrument.py`, `quiz_cue_sim.py`.
- 5 new reports: 2026-11-09-02 and 2026-11-10-01 to 04.
- 22 old `.pptx` files of `Week07` and `Week10` are in the macOS Trash (report 2026-11-10-02). `Week10/Lab_week10_v3.pptx` stays.
- Two extra copies of the Week 07 lecture PDF exist: `Lecture_week07_v7.pdf` in the project root and `Week07/Lecture_week07_final.pdf`. Both are equal to `Week07/Lecture_week07_v7.pdf`.

### 2. The repository in numbers

| Measure | Run 11 | Now |
|---|--:|--:|
| Decks (`.pptx`, without `.venv`) | 228 | 211 (228 - 22 in the Trash + 5 new) |
| Python files, root and `quiz_pool_src/` | 84 | 95 |
| Reports | 165 | 175 before this report |

### 3. The new builders, run in a sandbox

| Job | Exit | Output | Result |
|---|---|---|---|
| `build_week07_lecture_v7.py --force` | 0 | 24 slides | equal, 83 of 83 parts |
| `build_week10_lecture_v10.py --force` | 0 | 37 slides | equal, 109 of 109 parts |
| `build_week10_lecture_v11.py --force` | 0 | 37 slides | equal, 109 of 109 parts |
| `build_week07_lab_v3.py --force` | 0 | deck, script, Blackboard text, repo folder | 3 files equal (53 parts) |
| `build_week10_lab_v4.py --force` | 0 | deck, script, Blackboard text, repo folder | 3 files equal (53 parts) |
| `build_easy20_w10.py` | 0 | upload, key, titles | 3 files equal |
| `qti_pack.py` | 0 | QTI 2.1 ZIP | 21 of 21 parts equal |

- The parts of `docProps/` are not compared, because they hold the save time.
- The repo folders `Week07` and `Week10` that the lab builders wrote in the sandbox are equal to the working tree of the real clone.
- The lab builders need `Week05/Lab_week05_v4.pptx`, because `lab_kubeadm.py` uses it as the template.
- Lecture v11 differs from v10 on slide 37 only.
- `build_week10_lab_v4.py` reads `HEAD:Week07/local-path-storage.yaml`. It accepts the committed form (busybox) and the Week 07 v3 form (alpine-curl). `build_week07_lab_v3.py` reads the working-tree file.
- `build_week07_lab_v3.py` has no `VERSION` constant. Standard A5 asks for one in each builder.

### 4. The deck gate and the PDFs
- `tools/rungate.py` (the `deck_checks` of `gate_week12.py`): `FAILED: 0` for Lecture Week 07 v7, Lab Week 07 v3, Lecture Week 10 v10, Lecture Week 10 v11 and Lab Week 10 v4.
- The PDFs of Lecture 07 v7, Lab 07 v3, Lecture 10 v11 and Lab 10 v4 hold only Calibri and Consolas. Each has a Title, the Author "Maziar Sojoudian" and a page count equal to the slide count.
- The reference links of the two lectures: 10 of 10 pages return 200 (kubernetes.io, docs.aws.amazon.com, github.com). Four 404 results are label keys in YAML (for example `kubernetes.io/hostname`), not links.

### 5. The quizzes and the exam, with the cue tool of the standard
`tools/quiz_cue_sim.py` (13 strategies, limit 30 %) ran on the MC rows of each upload file. The Week 10 quiz audit also ran: exit 0, 0 errors, longest 4.8 and shortest 4.5 of 20.

| File | MC rows | Result (strategies above 30 %) |
|---|--:|---|
| `Quiz_W10_Easy20` | 20 | PASS (highest: middle length 5.5) |
| `Quiz_W01W02_Easy20` and `_v2` | 20 | PASS |
| `Quiz_W09_Easy20` (delivered as "Quiz-4 - 2%") | 20 | FAIL: stem overlap 7.25, convergence 6.50, convergence stemmed 6.83 |
| `Quiz_W03W04_Easy20` | 20 | FAIL: stem overlap 8.08, odd one out 7.00 |
| `Quiz_W03W04_Easy20_v2` | 20 | FAIL: stem overlap 7.83, odd one out 7.00 |
| `Quiz_W05W06_Easy20` | 20 | FAIL: fewest words 6.92, longest 6.33 |
| `week01/Week01_Pool` | 100 | FAIL by a small margin: most words 33.3, longest 31.2, always C 31.0 |
| `week02/Week02_Pool` | 100 | FAIL by a small margin: shortest 30.9, longest 30.6 |
| `week03/Week03_Pool` | 100 | FAIL by a small margin: longest 32.0, stem overlap 30.9 |
| `CLO835_Final_Exam_v2` (26 MC, 9 MA, 5 TF) | 26 | FAIL: most words 15.83, longest 14.50, convergence 13.83, always C 10.00 |
| `CLO835_Final_Exam` (v1) | 26 | FAIL: most words 15.83, longest 15.00 |
| `CLO835_Hard20` | 20 | FAIL: longest 7.00, most words 6.67 |

- These files, except the Week 10 quiz, are older than the cue rule (D10 of the standard, 2026-11-10).
- The Blackboard draw of a pool is random, so the pool results are near the limit, not a clear failure.
- The exam result agrees with run 12 (the key is the strictly longest option in 13 of 26 MC rows).

### 6. The course repository
- `git ls-remote`: `ad93eb8` for HEAD and `master`. The repository page returns 200.
- The clone has 7 changed files, not committed: Week07 (`cleanup_lab07.sh`, `local-path-storage.yaml`, `localMachine.sh`, `master-init.sh.tftpl`) and Week10 (`cleanup_lab10.sh`, `localMachine.sh`, `master-init.sh.tftpl`).
- `HEAD:Week07/localMachine.sh` is lab v2. `HEAD:Week10/localMachine.sh` and the public raw file are lab v3.
- The working tree: `Week07/localMachine.sh` = v3, `Week10/localMachine.sh` = v4.
- A scan of the changed folders found 0 hits for `/Users/`, `.ssh/`, `mazSeneca`, the email, AWS keys and private keys. The only IP addresses are 0.0.0.0, 10.244.0.0, 127.0.0.1 and 169.254.169.254.
- `bash -n` passes on each script. `terraform fmt -check` passes on the sandbox copies of Week07 and Week10.
- `sojoudian/clo835-mirrors` still returns 404.

### 7. The old builders after the delete of 2026-11-10
Report 2026-11-10-02 says that 11 old builders "now fail". This is true for 6 of them, which read a deck in the Trash: `build_week07_lecture_v6.py` (`week7_old.pptx`), `build_week10_lecture_v8.py` (`Week09_lecture_style_v7.pptx`), `dedup_lectures.py`, `retarget_accounts.py`, `retarget_kind.py` and `fix_outline_week15.py`. The other 5 do not fail:
- `build_week07_lab_v1.py`, `build_week07_lab_v2.py`, `build_week10_lab_v1.py` and `build_week10_lab_v2.py` read only the Week 05 template. The deleted deck is their output, so the overwrite guard does not stop them.
- Without `--no-repo`, each of these 4 writes its old lab into the course repo folder `Week07` or `Week10`. This replaces the v3 and v4 lab files there.
- `build_week07.py` has no `__main__` guard. An import writes `Week07/Week07_lab_style_v1.pptx` again.

### 8. The record of the chat after run 12
Chat `4b692c4c` continues. Its record is now 199.7 MB and 11 228 lines (22:28). It was compressed two more times (11-10 00:41 and 16:44). The prompt of 22:12 holds Learner Lab identity text; this report does not repeat it.

| Local time | Prompt | Result | Report |
|---|---|---|---|
| 11-09 23:12 | Analyze and remember everything | Run 12 | 11-09-01 |
| 11-09 23:26 | Check the Week 07 and Week 10 lectures against my preferences; ASCII tables | 37 and 49 defects, 18 and 22 additions, 12 conflicts | 11-09-02 |
| 11-10 15:06 | Fix all of the tables | Lecture 07 v7, lecture 10 v10, lab 07 v3; gate 32 of 32 | 11-10-01 |
| 11-10 18:33 | Delete the old versions of the decks | 22 `.pptx` files to the Trash | 11-10-02 |
| 11-10 18:42 | Do you remember the Week 09 lab and quiz process? | Answer only | - |
| 11-10 18:49 | Make the Week 10 lab and quiz the same way | Lab v4 (40 commands, 3 live passes), lecture v11, quiz (11 review rounds), destroy | 11-10-03 |
| 11-10 21:55 | Tell me the issues and the fixes in a few paragraphs | Answer only | - |
| 11-10 21:56 | What do I update on Blackboard Ultra? Which repo is the commit? | Answer only | - |
| 11-10 21:59 | Do we change the Lab06 text? Give the full updated version | The v4 text given | - |
| 11-10 22:05 | Is the Week 10 quiz good? | Answer only | - |
| 11-10 22:12 | Update the memory; write deep standards; AWS is up | `CLO835_STANDARDS.md` v1, then v1.1; `tools/` | 11-10-04 |
| 11-10 22:18 | (this session `4607d34d`) Analyze and remember everything | Run 13 | 11-10-05 |

## Results
- 7 sandbox jobs exit 0. 13 of 13 outputs are equal to the stored files. The repo folders are equal to the working tree.
- 5 of 5 new decks: deck gate `FAILED: 0`.
- Week 10 quiz: all builder gates pass, the audit has 0 errors, and the cue tool passes.
- No server started, so no port is used.

### Open items, ranked
1. The exam of 11/11 (`CLO835_Final_Exam_v2`): "most words" gets 15.8 of 26 MC rows, and "longest" gets 14.5.
2. Lab Week 10 v4 is not on GitHub (the public raw file is v3). The user has the v4 Blackboard text for `Lab06 - 2.5%`. Standard G2: paste the text only after the push.
3. The v4 Blackboard text says "control-plane node" on lines 11, 17, 55 and 104, and "control-plane pods" on line 19.
4. Clones made before 2026-11-05 20:55 stop at `git pull` (exit 128). This affects Lab Week 10 now, and Weeks 12 to 14.
5. The delivered Week 09 quiz fails 3 cue strategies. The Week 03-04 and Week 05-06 quizzes also fail.
6. The Week 07 lab v3 has no live test.
7. Lecture v11 uses "make" for "create" on slides 8, 21 (two times) and 23. Standard H3 names only slides 21 and 23.
8. The 4 old lab builders of section 7 can write old labs into the course repo. `build_week07.py` writes a deck at import.
9. `build_week07_lab_v3.py` has no `VERSION` constant.
10. Items of run 11 and run 12 that did not change: no copy of `clo835-mirrors` and KEDA 2.21.0; `build_week14.py`, `build_week06.py` and the 6 `_lab_v1` builders overwrite delivered files; 12 of 16 older PDFs use substitute fonts; the commit identity `BartyCrouch`.

## Issues / Notes
- Session `4b692c4c` worked at the same time as this run. It changed `CLO835_STANDARDS.md`, report 2026-11-10-04 and `reference-clo835-standards.md` at 22:31. I read the new versions before I wrote this report.
- I ran the gate only on the PDFs that exist. I made no new PDF, because an export opens PowerPoint.
- I did not run the lab, Blackboard and live checks of `gate_week12.py`. They hold Week 12 paths.
- I did not open the decks in PowerPoint and did not look at the pages. The run 13 deck check is the gate only.
- The cue tool reads MC rows only. The 9 MA and 5 TF rows of the exam are not in its result.
- I did not run the builders of run 11 again, because they did not change after run 11.
