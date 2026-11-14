# Report: Repository analysis, run 8 (delta over run 7, 2026-10-08)
**Date**: 2026-10-27
**Sequence**: #04 for the day

## Summary
I analysed the full repository with read-only checks. The base is run 7
(`ARCHITECTURE/LATEST.md`, 2026-10-08) and the delta report of 2026-10-13. I
verified every file that changed after them. All new work is in three areas:
Week 06, the assignments, and the question pools. All 6 new builders and all 17
quiz text files rebuild exactly. No old defect is repaired in place. The most
important new finding is outside this folder: the verified Assignment 1 repair is
not on GitHub.

## What Changed
- Created `reports/report-2026-10-27-04-repo-analysis-run8.md` (this report).
- No other repository file changed. Every rebuild ran on copies in the session
  scratchpad.
- I did not change `ARCHITECTURE/`. This report holds the run 8 model.

## Technical Details

### 1. The repository in numbers

| Measure | 2026-10-13 | Now |
|---|--:|--:|
| Total size | 1.8 GB | 1.8 GB |
| Of which `.venv` | 198 MB | 198 MB |
| Of which `week02/terraform-vm` (provider cache) | 765 MB | 765 MB |
| Files, excluding `.venv` | 1 799 | 1 868 |
| PowerPoint decks | 171 | 175 |
| Decks on 16:9 / on 4:3 | — | 165 / 10 |
| Python files (first party) | — | 51, 24 972 lines |
| Of which at the root | 21 | 26, 19 591 lines |
| Of which in `quiz_pool_src/` | — | 21, 4 365 lines, plus 4 in `rejected_v1/` |
| Reports | 106 | 124 |

The folder is not a git repository. It has no remote and no history.

### 2. The five layers
1. **Specification.** `PROMPT.md` (rules R1 to R8), `DESIGN_LANGUAGE.md`,
   `CLAUDE.md`, `ARCHITECTURE_ANALYSIS_PROMPT.md`.
2. **Deck builders.** 26 root Python files. `build_week12.py` (2 371 lines) is the
   engine, and 7 modules import it: `build_lab01`, `build_week01`, `build_week02`,
   `build_week12_v3_lab`, `build_week13`, `build_week14`, `fix_week03`.
3. **Decks.** 175 `.pptx` files in week folders, `finalWork/`, `old/` and the root.
4. **Assessments.** `quiz_pool_src/` (pools, Blackboard files, QTI 2.1 packages),
   the final exam, Hard 20, two assignment handouts, Blackboard texts.
5. **Lab code.** `week05_practical_work/` and `week02/terraform-vm/`. The live lab
   code is in the public repository `CLO835_Fall_2026`, not here.

### 3. What changed since run 7

| Date | Area | New files |
|---|---|---|
| 2026-10-08 | Week 05 lab | `Lab_week05_v4.pptx` (18 slides), `build_week05_lab_v4.py` |
| 2026-10-14 | Week 06 lecture | `Week06_lecture_style_v6.pptx` (41) and `v7` (34), with PDFs; `build_week06_v6.py` (1 236 lines), `build_week06_v7.py` (312) |
| 2026-10-14 | Blackboard texts | `Week05/Lab_week05_Blackboard_Submission.md`, `Assignments/Assignment_2/Assignment2_Blackboard_Submission.md` |
| 2026-10-15 | Assignment 1 | `CLO835_Assignment1_v2.docx`, `fix_assignment1_docx.py` (134), the Blackboard text |
| 2026-10-15 and 16 | Week 06 lab | `Lab_week06_v1.pptx`, `Lab_week06_v2.pptx` (31 each), `build_week06_lab_v1.py` (785), `build_week06_lab_v2.py` (799), `localMachine_v1.sh`, two Blackboard texts |
| 2026-10-23 | Quiz 3 | a 100-question pool, its key, a QTI 2.1 package; `q3_quiz3.py`, `build3.py`, `audit3.py`, `build_qti3.py`, `audit_qti3.py` |
| 2026-10-26 and 27 | Easy 20 quizzes | W01-W02, W03-W04, W05-W06, each with a Blackboard file, a key and a QTI package; 9 Python files and `qti_pack.py` |

No report in `reports/` covers the Week 06 lab work of 2026-10-15 and 2026-10-16.
The docstring of `build_week06_lab_v2.py` is the only record of the v2 changes.

### 4. The build system

**Run safety.** 10 of the 26 root builders save a deck at import. They have no
`__main__` guard: `build_lab`, `build_lab_guide`, `build_week3`, `build_week03`,
`build_week04`, `build_week05`, `build_week06`, `build_week07`, `build_week08`,
`build_week09`. Run them in a sandbox only. The other 16 are guarded, and that
includes all 6 new builders.

**A new pattern: derive from a delivered deck.** The new builders do not import
the engine. Each one reads one delivered deck, copies its house design, and never
writes it:

| Builder | Reads | Writes |
|---|---|---|
| `build_week05_lab_v4.py` | `Week05/Lab_week05_v3.pptx` | `Lab_week05_v4.pptx` |
| `build_week06_v6.py` | `Week06/Week06_lecture_style_v5.pptx` | `v6` |
| `build_week06_v7.py` | `Week06/Week06_lecture_style_v6.pptx` | `v7` |
| `build_week06_lab_v1.py`, `_v2.py` | `Week05/Lab_week05_v4.pptx` | `Lab_week06_v1`, `_v2` |
| `fix_assignment1_docx.py` | `CLO835_Assignment1.docx` | `CLO835_Assignment1_v2.docx` |

The result: the chain v5, v6, v7 must stay on disk. A delete of v5 or v6 stops
the rebuild of v7. A delete of `Lab_week05_v4.pptx` stops the Week 06 lab.

**One content list, two outputs.** `build_week06_lab_v2.py --script PATH` writes
the lab shell script from the same lines as the deck. Its output equals GitHub
`Week06/localMachine.sh` line for line. The local `Week06/localMachine_v1.sh` is
the v1 script. It differs from GitHub in about 10 places (change-cause
annotations, `--sort-by`, the pause step, the 35-second wait).

**Reproducibility of the new builders.** I ran each one on copies and compared the
output part by part with the stored file. `docProps/` is excluded.

| Output | Parts | Parts that differ |
|---|--:|--:|
| `Week05/Lab_week05_v4.pptx` | 69 | 0 |
| `Week06/Week06_lecture_style_v6.pptx` | 130 | 0 |
| `Week06/Week06_lecture_style_v7.pptx` | 112 | 0 |
| `Week06/Lab_week06_v1.pptx` | 95 | 0 |
| `Week06/Lab_week06_v2.pptx` | 95 | 0 |
| `Assignment_1/CLO835_Assignment1_v2.docx` | 32 | 0 |

`build_week06_v6.py` prints `TEXT NOT FOUND` for 2 strings. This is not a defect.
The builder lists each rewrite twice, once with a curved and once with a straight
apostrophe, and one form always misses.

**Builders that still do not run** (unchanged, the files are older than run 7):
- `build_week08.py:59` reads `Week08/assets`. `Week08/` does not exist. The
  assets are in `Week09/assets`.
- `build_week09.py:62` reads `Week09/assets`. The file `s05_1.jpg` is in
  `Week10/assets`.
- `assemble_week13.py:8` and `assemble_week14.py:8` point at a deleted
  scratchpad. `build_week13` and `build_week14` still run from the committed JSON.
- `fix_week03.py` wants `Week03.pptx` at the root. It is not there.

### 5. The canonical deck of each week

| Week | Folder | Lecture | Lab |
|---|---|---|---|
| 01 | `week01` | `Week01_lecture_style_v5` 38, /38 | — |
| 02 | `week02` | — | `Lab01_v1` 24, /24 |
| 03 | `week03` | `Week03_lecture_style_v2` 15, /15 | lab v1 8 |
| 04 | `Week04/FINAL` | `Week04` 26, **/38 wrong** | `Lab_week04` 13, **/38, 12 of 13 out of sequence** |
| 05 | `Week05` | `lecture_week05_v3` 30 (1 hidden), /29 | `Lab_week05_v4` 18, /18 |
| 06 | `Week06` | `Week06_lecture_style_v7` 34 (1 hidden), /34 | `Lab_week06_v2` 31, /31 |
| 07 | `Week07` | `Week07_lab_style_v3` 14 | (same deck) |
| 08 | `Week09` | `Week08_lecture_style_v3` 13 | — |
| 09 | `Week10` | `Week09_lecture_style_v4` 36 | — |
| 12 | `Week12` | `Week12` 21 | `Week12_lab` 10 |
| 13 | `week13` | `Week13_lecture_style_v6` 22 | `Week13_lab_style_v6` 26 (6 hidden) |
| 14 | `week14` | `Week14_lecture_style_v9` 11 | `Week14_lab_style_v10` 23 (2 hidden) |

The folder names for Week 08 and Week 09 are off by one. `Week11-Exam/` and
`untitled folder/` are empty.

**Two footer conventions.** The two newest canonical lectures count a hidden slide
in different ways:
- `lecture_week05_v3` counts visible slides only. Hidden slide 5 and slide 6 both
  read `5 / 29`. The slide show reads 1 to 29 with no gap.
- `Week06_lecture_style_v7` counts every slide. Hidden slide 12 reads `12 / 34`.
  The slide show goes from 11 to 13.

### 6. Health of all 175 decks
- **Float coordinates:** 27 decks, 2 205 floats in total. 16 are in `Week04/` and
  11 are in `Week05/`, all in superseded `*_lab_style*` chains.
  `Week04_lab_style_v16.pptx` still holds 175. Every canonical deck holds 0.
- **4:3 canvas:** 10 decks: `Lab01.pptx`, `Week3.pptx`, `finalWork/Lab01`,
  `finalWork/Week01`, `finalWork/Week02`, `old/Week01`, `old/Week02`,
  `old/Week03`, `week01/Week01`, `week02/Week02`.
- **Wrong footer denominators** in decks that a person can open: `Week04/FINAL/`
  two decks (/38), `Week04/Week04.pptx` (/38), `Week06/Week06.pptx` (/71),
  `Week06_lecture_style_v3` to `v5` (/71), `Week06_lab_style_v3` and `v4` (/71),
  `finalWork/Week04` (/38), `finalWork/Week06_Part_A` and `_B` (/71),
  `finalWork/Lab06` (/71).
- **The new decks** hold Calibri and Consolas only, and 0 floats.
- **A deck is open in PowerPoint now.** `Week06/~$Lab_week06_v2.pptx` is a lock
  file, written 2026-10-27 18:33, owner "Maziar Sojoudian". A save from
  PowerPoint makes the deck differ from its builder. That is what happened to
  `Week06_lab_style_v2.pptx` (142 parts differ).

### 7. The question pools

| File set | Questions | Gate errors | Key A/B/C/D | Correct option longest |
|---|--:|--:|---|--:|
| Week 01 pool | 100 | 0 | 18/29/31/22 | 26 % |
| Week 02 pool | 100 | 0 | 26/27/23/24 | 25 % |
| Week 03 pool | 100 | 0 | 29/22/19/30 | 27 % |
| Hard 20 | 20 | 0 | — | 30 % (run 7) |
| Quiz 3 pool | 100 | 0 | 25/25/25/25 | 26 % |
| Easy 20, W01-W02 | 20 | 0 | 5/5/5/5 | 5 of 20 |
| Easy 20, W03-W04 | 20 | 0 | 5/5/5/5 | 5 of 20 |
| Easy 20, W05-W06 | 20 | 0 | 5/5/5/5 | 6 of 20 |

- The gates grow by pool: `build2.py` has gates 1 to 7. `build3.py` adds 8, 8b, 9
  and 10. The Easy 20 builders add 11 (feedback). The W05-W06 builder adds 12
  (logical option order, 12 questions) and 13.
- Every audit script reports 0 errors, 0 answer leaks and 0 pairs at risk.
- All 17 text outputs rebuild byte-identical. All 4 QTI packages rebuild with 0
  entries that differ (101 and 21 entries).
- The copies in `week01/`, `week02/` and `week03/` equal the `quiz_pool_src/`
  pools.
- The W05-W06 facts held 20 of 20 on a live v1.35.9 cluster (report 10-27-03).

**Still open, files unchanged since run 7:**
- `CLO835_Final_Exam_Blackboard.txt`: 40 questions (26 MC, 9 MA, 5 TF). The
  correct option is the strictly longest in 14 of 26 MC rows, which is 54 %.
  Run 7 gave 53 % with a different tie rule.
- `week01/Week01_Quiz_Blackboard.txt`: Q14, Q15 and Q16 need the slide.
- `Week09/Week08_Quiz_Blackboard.txt`: 3 questions point at the lecture, and 1
  asks an AWS price.

### 8. The assignments
- **Assignment 1.** `CLO835_Assignment1_v2.docx` rebuilds exactly from
  `fix_assignment1_docx.py`. It holds 4 repairs: the early Pull is deleted, "3
  main parts" becomes 4, the Compose part is added, and a tag check is added.
- **Assignment 2.** `CLO835_Assignment2.docx` is the summer file (2026-07-06).
  The Fall version is the `assignment-2/` folder of the public repository. This
  folder holds only its Blackboard text.

### 9. The public course repository (outside this folder)
Two local clones exist.

| Clone | HEAD | State |
|---|---|---|
| `~/Documents/c/r/CLO835_Fall_2026` | `acd8cdf` 2026-10-16 "update w06" | Equal to `origin/master` after a fetch. Holds Week02 to Week06, `assignment-1`, `assignment-2`. Untracked: `Week06/apply.log`, `Week06/destroy.log`. `terraform.tfstate` is ignored. |
| `~/Documents/c/r/a2_test/CLO835_Fall_2026` | `39a43b1` 2026-10-14 | One commit behind `origin`. Holds the 2026-10-15 Assignment 1 repair as **uncommitted** changes: 5 modified files and `assignment-1/.dockerignore`. |

Findings:
1. **The verified Assignment 1 repair is not on GitHub.** The main clone and
   `origin` hold a `Dockerfile` with 0 `iputils-ping` lines and no
   `.dockerignore`. Students who clone GitHub get the version with the 11 defects.
2. **The 2026-10-23 analysis read the stale clone.** It reports "no week after
   05". GitHub holds `Week06` since 2026-10-16.
3. **Three defects of 2026-10-23 are still on GitHub:**
   `assignment-2/.github/workflows/docker.yml:25` is not valid YAML;
   `assignment-2/README.md:145` and `:186` omit the `k8s/` prefix;
   `Week02/README.md:64` still recommends `r6i.large`.

### 10. Secrets and private data
- The home IP `173.33.124.240` is in `week02/terraform-vm/variables.tf:57`,
  `week02/terraform-vm/terraform.tfvars:11`, 5 reports and 2 `ARCHITECTURE/`
  files.
- No AWS access key, no private key, no `.pem`, no `.ppk` and no `.tfstate` file
  is in this folder.
- `mazSeneca.pub` is at the root. It is a public key.

### 11. Defects re-tested today

| Defect | State |
|---|---|
| `Week04_lab_style_v16.pptx`, 175 floats | open |
| `Week04/FINAL/Week04.pptx`, /38, teaches kind | open |
| `Week04/FINAL/Lab_week04.pptx`, /38, sequence 1 then 27 | open |
| `finalWork` footers (Week04, Week06 A and B, Lab06) | open |
| `build_week08.py`, `build_week09.py` | open |
| `assemble_week13.py`, `assemble_week14.py` | open |
| `fix_week03.py` input path | open |
| Final exam length giveaway, 54 % | open |
| `week01` quiz Q14 to Q16, `Week08` quiz | open |
| Home IP in `week02/terraform-vm` | open |
| `week5_code/week5_code/` nested duplicate, 7 files | open |
| `Week06_lecture_style_v5`, /71 | superseded by v7 (/34 correct); v5 is still on disk |
| Week 06 lab deck not audited (`Week06_lab_style_v4`) | superseded by `Lab_week06_v2`, a new build |

## Results
- Read-only run. 0 repository files changed, apart from this report.
- 6 of 6 new builders reproduce their stored file with 0 differing parts.
- 17 of 17 quiz text files rebuild byte-identical. 4 of 4 QTI packages rebuild
  with 0 differing entries.
- 0 old defects repaired in place. 2 are superseded by new decks.
- 6 new findings: the Assignment 1 repair is not on GitHub; the 10-23 analysis
  read a stale clone; a deck is open in PowerPoint; two footer conventions; no
  report for the Week 06 lab; the new builders depend on the version chain.
- No server started, so no port is used.

## Issues / Notes
- I did not run the 10 unguarded builders again. Their files are older than run
  7, so the run 7 results hold.
- I did not render the new decks to images. The visual checks come from the
  reports of 2026-10-14.
- I ran no Terraform command and made no AWS call.
- I ran `git fetch` in the main public clone. It changed no working file.
- The run 7 file `ARCHITECTURE/LATEST.md` is now out of date for sections 1, 3.1
  and 4.
