# Report: Repository analysis, run 11 (all builders, all folders, all rules)
**Date**: 2026-11-05
**Sequence**: #01 for the day

## Summary
Run 11 closes the gaps of run 10. I ran all 68 builders and scripts in a sandbox. I read
the text inside the pictures of the 22 current decks. I audited all 228 decks, and I ran
the deck gate on the 17 current decks that have a PDF. Three reviewer agents read the
folders and rule files that earlier runs did not read. Two new facts are serious. First,
the public course repository is not public now. Second, the Mac restarted at 01:09 today,
and the restart deleted all of `/private/tmp`, which held the mirror copy and the gate
helper files.

## What Changed
- Created this report.
- Updated the memory files `project-clo835-arch-analysis.md`,
  `project-clo835-fall2026-repo.md` and `MEMORY.md`.
- No project file changed. All runs used a sandbox copy in the session scratchpad, with
  `HOME` set to a sandbox folder. The real course clone had 0 changed files after the runs.
- I made no AWS call, no commit and no push.

## Technical Details

### 1. Changes after run 10
- Project: only my Week 07 work of 2026-11-04 (report #03) and `.DS_Store`.
- The Mac restarted at 2026-11-05 01:09 for macOS 27.2. The restart emptied
  `/private/tmp`. These items are gone:
  - the mirror copy of session `0b02113e` (it held the last local `local-path-storage.yaml`
    copy of the mirror; the course repository still has its own copy),
  - `w9t/instrument.py`, which `gate_week12.py` and `gate_week13.py` need for the lab checks,
  - the live logs of Weeks 09, 10, 12 and 13, which the gates use with a live folder,
  - the scratchpad of session `4c65ef92`, which `assemble_week13.py` and
    `assemble_week14.py` read.

### 2. The course repository is not public now
- Local clone `~/Documents/c/r/CLO835_Fall_2026`: HEAD `665768b`, 0 changed files.
- `git ls-remote origin` works with the stored credentials and gives `665768b`.
- Anonymous requests return 404 today for the repository page, the API and two raw
  files. On 2026-11-04 (run 10) the raw file `Week14/metrics-server.yaml` returned 200.
- The public list of the account `sojoudian` has 201 repositories. `CLO835_Fall_2026` is
  not in it.
- Effect on students: the first lab command `git pull` (or `git clone`) fails. The raw
  URLs of the Week 07 and Week 14 labs fail. The next lab class is 11/18 (Week 12).
- I do not know if this change is on purpose.

### 3. The repository in numbers

| Measure | Run 10 | Now |
|---|--:|--:|
| Decks | 226 | 228 (Week 07 v6 and `week7_old.pptx`) |
| Decks at 16:9 / 4:3 | 216 / 10 | 218 / 10 |
| Decks with float coordinates | 27 | 27 (2 205 floats, all in superseded decks) |
| Decks with a WMF or EMF picture | not counted | 14 |
| Python files, root and `quiz_pool_src/` | - | 84 |
| Reports | 162 | 165 before this report |

### 4. All builders, run in a sandbox
68 jobs: every root script except `lab_kubeadm.py` and the 2 gates, and the 8 quiz
builders. Lab builders ran with `--no-repo`. The runner records each file that a job
writes, and compares it with the stored file (decks without `docProps/`).

| Result | Count |
|---|--:|
| Jobs that exit 0 | 62 |
| Files written (without the temporary QTI folder) | 145 |
| Equal to the stored file | 126 |
| Equal to a stored file under another name | 4 |
| Different | 15 |

**The 4 renamed outputs.** The user moved or renamed these files after the build:
- `build_lab01.py` writes `Lab01_v1.pptx` in the root. It equals `week02/Lab01_v1.pptx`.
- `build_week12.py` writes `Week12/Week12_lecture_style_v2.pptx`. It equals `Week12/Week12.pptx`.
- `build_week12_v3_lab.py` writes `Week12/Week12_lab_style_v3.pptx`. It equals `Week12/Week12_lab.pptx`.
- `build_week3.py` writes `Week3_lab_style.pptx`. It equals `new_Week3.pptx`.

**The 15 different files have 3 causes.**
1. `build_week14.py` has `VERSION = "v10"`. `retarget_accounts.py` also writes
   `week14/Week14_lecture_style_v10.pptx`, from v9. The stored v10 is the retarget output.
   So a run of `build_week14.py` overwrites the delivered v10 with a different deck
   (slides 10 and 11 differ). The dedup output v11 differed only because it read that
   wrong v10. With the stored v10 as input, v11 is equal again (60 of 60 parts).
2. `build_week06.py` has `VERSION = "v2"`, but it changed after v2 (Jun 8, 15:11 against
   14:26). Its output differs from the stored `Week06_lab_style_v2.pptx` on all 71 slides.
   A run overwrites that delivered file.
3. The 6 `_lab_v1` builders of Weeks 07, 09, 10, 12, 13 and 14 now write one different
   comment line ("# asks for key_name again"). `lab_kubeadm.py` changed on 10-31, after
   these v1 files were made. 12 files differ: 6 decks and 6 scripts. A run overwrites the
   delivered v1 files.

**The 6 jobs that stop.**

| Script | Error | Cause |
|---|---|---|
| `assemble_week13.py`, `assemble_week14.py` | FileNotFoundError | They read the scratchpad of session `4c65ef92`, which is gone |
| `build_week08.py` | FileNotFoundError `Week08/assets/s05_1.png` | The folder `Week08/` does not exist |
| `build_week09.py` | KeyError `s05_1.jpg` | An asset name is missing from its table |
| `fix_week03.py` | PackageNotFoundError `Week03.pptx` | The source moved to `week03/` |
| `quiz_pool_src/qti_pack.py` | ValueError | A command tool that needs 4 arguments; not a builder |

`build_week07_lab_v2.py` still runs with `--no-repo`. Its repository step reads the mirror
folder in `/private/tmp`, so that step now fails.

**Quizzes.** All 8 quiz builders give equal files. The QTI zip has 101 of 101 equal parts.
The 5 audits report 0 errors: `audit3`, `audit_easy20`, `audit_easy20_w34`,
`audit_easy20_w56`, `audit_qti3`.

**Run safety.** 22 files have no `__main__` guard:
- 8 deck builders save a deck at import: `build_lab`, `build_lab_guide`, `build_week3`,
  `build_week03`, `build_week04`, `build_week05`, `build_week06`, `build_week07`.
- 5 quiz audits run at import. They only read files.
- `lab_kubeadm.py` and 8 quiz data files run no code at import.

### 5. The deck gate on the current decks
I ran the deck checks of `gate_week12.py` on the 17 current decks that have a PDF.

| Deck | Pass | Fail | Main failures |
|---|--:|--:|---|
| Lecture Week 07 v6, Lecture Week 12 v6, Lab Week 12 v5, Lab Week 13 v3 | 32 | 0 | - |
| Lecture Week 13 v8 | 30 | 2 | repeated bullet, replaced word (the Week 13 gate allows them) |
| Lab Week 06 v4, Lab Week 09 v4 | 29 | 3 | substitute PDF fonts, file properties |
| Lab Week 07 v2, Lab Week 10 v3, Lab Week 14 v2 | 27 to 28 | 4 to 5 | substitute PDF fonts, `busybox`, replaced words |
| Lab01 v1, Lab Week 05 v4 | 26 | 6 | PDF fonts, words, terminal sizes |
| Lecture Week 09 v7 | 24 | 8 | PDF fonts, title band, 11 pt text, palette |
| Lecture Week 03 v2, Lecture Week 10 v9 | 22 | 10 | PDF fonts, bands, small text, palette |
| Lab03 v1 | 20 | 12 | the oldest design |
| Lecture Week 06 v7 | 19 | 13 | hidden slide, notes, photos, small text |

Five decks have no PDF, so the gate cannot run on them: Week 01 v6, Week 04 v2 (lecture and
lab), Week 05 lecture v4, and Week 14 lecture v11.

### 6. Text inside the pictures of the current decks
The 22 current decks hold 33 different pictures. macOS Vision read the text of 32 of them.
The last one is a WMF file.
- No picture holds an account name, a key, a private path or a home address.
- Third-party figures:
  - Week 01 v6: slides 9 to 13, 17 to 21, 23 to 25, 27, 31 and 33. Slide 13 has the
    brand of another company ("SoftServe").
  - Week 04 v2: slides 20, 23 and 25. Slide 25 is a WMF picture.
  - Week 14 v11: slides 4, 8 and 9.
  - Week 05 lecture v4: slide 9.
- Stock photos of unknown license: Week 01 v6 slides 29 and 30, and Week 06 v7 slides 5
  and 15.
- Week 06 v7 slide 17 has 3 icons with colors outside the palette.
- PREFERENCES section 13 forbids third-party pictures. But the user calls Week 01 v5 the
  reference redesign, and v6 keeps its pictures. This is a conflict that only the user can
  close.

### 7. Folders that earlier runs did not read
**Root files and support folders** (reviewer A):
- `old/` holds the 6 lectures of 2022 that are the sources of Weeks 01, 02, 03, 05, 10
  and 12.
- `analysis/` holds 521 working files from May to July (renders, PDFs, XML).
- `ARCHITECTURE/` holds runs 1 to 7. Reports hold runs 8 to 11.
- `old_assessments/` holds 4 Blackboard screenshots with no student names.
- `CLO835_SYL/` has two syllabus PDFs. The 6-page file is the complete one.
- `Labs/`: `Lab01` covers Week 02, `Lab02` Week 03, `Lab03_v2` Week 04.
- `Lab03_Guide.*` has "Lab 02" on the cover.
- `mazSeneca.pub` is a public key with a personal email address in its comment.

**Course content folders** (reviewer B):
- The newest file of each chain matches section 3 of run 10.
- These heads have no PDF: Week 01 v6, Week 04 v2 (both), Week 05 lecture v4.
- `Week04/Week04.pdf` (05-24) is older than its deck (09-30).
- `Week05_lab_style_v26.pdf` has 39 pages, but its deck has 29 slides.
- The Assignment 2 handout (v1 and v2) names the repositories
  `sojoudian/CLO835_summer2026_assignment1` and `_assignment2`. Both are public. The
  Blackboard text names `CLO835_Fall_2026/assignment-2`, which is not public now.
- `a1/` holds 34 files of 13 Assignment 1 attempts. No script reads it.
- `week05_practical_work/` holds an old kind copy and a nested duplicate of `week5_code/`.
- Other accounts (`luksa`, `jpetazzo`, `kindest`, `weaveworks`, `alpine/*`, `k8s.gcr.io`)
  are only in superseded decks and in `finalWork/`. All current heads are clean.

**Syllabus** (6-page PDF): Quiz 10 %, Labs 20 %, Assignments 30 %, Mid-Term 20 %, Final
Project 20 %. A student needs 50 % on the Final Project to pass. The schedule puts the
Mid-Term on 11/11, the Final Project due date on 11/25, and Helm on 12/9.

### 8. Rule sources (reviewer C)
- The rules come from `PROMPT.md` (05-26), `DESIGN_LANGUAGE.md` (05-23), the two
  `CLAUDE.md` files, `PREFERENCES.md` (10-27) and 18 feedback memories.
- The reviewer found 26 conflicts and 4 smaller ones. The main ones:
  - `PROMPT.md` names the old reference deck. `PREFERENCES.md` names Week 01 v5.
  - `PROMPT.md` says "keep the text verbatim". `PREFERENCES.md` says "write in ASD-STE100".
  - `PROMPT.md` says the correct answer must not be the longest. `PREFERENCES.md` says
    "the longest in about 1 of 4".
  - `DESIGN_LANGUAGE.md` uses 9 to 11.5 pt text and a contraction style. The gate needs
    12 pt and forbids contractions.
  - `PREFERENCES.md` says "keep a hidden slide". The gate fails any hidden slide.
  - The gate bans `busybox`. A memory keeps `busybox` as a Docker Official Image.
- Of 23 deck rules, the gate checks 3 in full and 13 in part. It does not check 7, for
  example facts, the outline, verbatim text, version bumps and arrow shapes. It does not
  check quizzes.
- The gate has Week 12 values in its code (paths, titles, 7 sections). So it needs a change
  for each new week.
- `PROMPT.md` and `DESIGN_LANGUAGE.md` are out of date: EKS for students, Docker logo on the
  cover, QA with `soffice`, no lab rules, no ASD-STE100.

### 9. Open items, ranked
1. The course repository is not public. Students cannot pull the labs.
2. The KEDA bundle of Project 16 and the `clo835-mirrors` content have no copy. 10 project
   files name the mirror repository, which does not exist.
3. The only exam files, `CLO835_Final_Exam_v2`, have the length clue in 50 % of their MC
   rows (run 9). The syllabus calls the exam of 11/11 a Mid-Term.
4. 3 builders overwrite delivered files with different content: `build_week14.py`,
   `build_week06.py` and the 6 `_lab_v1` builders.
5. The gates cannot run their lab checks until `instrument.py` exists again.
6. 12 of 16 PDFs use substitute fonts, and 5 current decks have no PDF.
7. The rule sources conflict in 26 places.

## Results
- 68 jobs: 62 exit 0. 130 of 145 written files equal a stored file. The other 15 have 3
  known causes.
- 228 decks open. 33 pictures of the current decks read with OCR.
- 17 current decks gated: 4 pass all 32 checks.
- No server started, so no port is used.

## Issues / Notes
- The reviewers did not read the text in the pictures of `analysis/`, nor the video files.
- I did not open the student files in `a1/` or `a1.zip`.
- I did not test the links again. Run 10 tested them on 2026-11-04.
- The cause of the 404 is not known. A private repository and a deleted repository both
  give 404 to an anonymous request. `git ls-remote` with the stored credentials works, so the
  repository exists.
