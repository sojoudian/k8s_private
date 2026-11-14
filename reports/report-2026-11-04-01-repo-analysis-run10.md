# Report: Repository analysis, run 10 (delta over run 9, 2026-10-30)
**Date**: 2026-11-04
**Sequence**: #01 for the day

## Summary
I analysed the repository with read-only checks. The base is run 9
(`report-2026-10-30-01-repo-analysis-run9.md`) and the 26 reports after it. No
file changed after 2026-10-31 23:19, except `.DS_Store`. All 21 builders that I
ran in a sandbox exit 0, and their 43 outputs equal the stored files. The course
repository on GitHub equals the local clone, and every lab folder equals the
script in this folder. Two new faults are serious. The mirror copy in
`/private/tmp` lost most of its files, so the KEDA bundle has no copy now. Also,
12 of the 16 current PDFs have substitute fonts.

## What Changed
- Created this report.
- Updated the memory files `project-clo835-arch-analysis.md` and
  `project-clo835-semester-project.md`, and their lines in `MEMORY.md`.
- No other file changed. All rebuilds ran on a copy in the session scratchpad
  (`run10/`), with `HOME` set to a sandbox folder.
- The real course clone had 0 changed files before and after the checks.
- I made no AWS call, no `git fetch`, no commit and no push.

## Technical Details

### 1. What changed after run 9
76 files are newer than the run 9 report. All of them are from 2026-10-30 and
2026-10-31.

| Type | Count | Files |
|---|--:|---|
| New builders and gates | 16 | `build_week09_lab_v3`, `v4`, `build_week09_lecture_v6`, `build_week10_lab_v3`, `build_week10_lecture_v8`, `build_week12_lab_v3` to `v5`, `build_week12_lecture_v4` to `v6`, `build_week13_lab_v3`, `build_week13_lecture_v8`, `fix_outline_week15`, `gate_week12`, `gate_week13` |
| Changed scripts | 3 | `build_week08.py` and `build_week09.py` (a `__main__` guard), `lab_kubeadm.py` (4 optional parameters) |
| Decks | 15 | Weeks 09, 10, 12 and 13 |
| PDFs | 15 | One for each new deck |
| `localMachine_vN.sh` | 7 | Weeks 09, 10, 12 and 13 |
| Blackboard texts | 8 | Week 06 v5, Week 09 v3 and v4, Week 10 v3, Week 12 v3 to v5, Week 13 v3 |
| Other | 12 | `Week12/assets/kube-flannel-v0.28.10.yml`, 10 `__pycache__` files, `.DS_Store` |

### 2. The repository in numbers

| Measure | Run 9 | Now |
|---|--:|--:|
| Total size | 2.06 GB | 2.3 GB |
| Files, excluding `.venv` | 2 026 | 2 158 |
| PowerPoint decks | 211 | 226 |
| Decks at 16:9 / at 4:3 | 201 / 10 | 216 / 10 |
| PDFs | - | 155 |
| Python files, first party | 71, 30 318 lines | 87, 34 961 lines |
| Of which at the root | 46, 24 937 lines | 62, 29 580 lines |
| Reports | 135 | 162 before this report |

The folder is still not a git repository.

### 3. The current deck of each week

| Folder | Lecture | Slides | Footer | Lab | Slides | Footer |
|---|---|--:|---|---|--:|---|
| `week01` | `Week01_lecture_style_v6` | 38 | /38 | none | - | - |
| `week02` | none | - | - | `Lab01_v1` | 24 | /24 |
| `week03` | `Week03_lecture_style_v2` | 15 | /15 | `Lab03_lab_style_v1` | 8 | /8 |
| `Week04/FINAL` | `Week04_v2` | 26 | **/38** | `Lab_week04_v2` | 13 | **/38** |
| `Week05` | `lecture_week05_v4` | 30, 1 hidden | /29 | `Lab_week05_v4` | 18 | /18 |
| `Week06` | `Week06_lecture_style_v7` | 34, 1 hidden | /34 | `Lab_week06_v4` | 10 | /10 |
| `Week07` | `Week07_lab_style_v5` | 12 | /12 | `Lab_week07_v2` | 10 | /10 |
| `Week09` | `Lecture_week09_v7` | 12 | /12 | `Lab_week09_v4` | 10 | /10 |
| `Week10` | `Lecture_week10_v9` | 28 | /28 | `Lab_week10_v3` | 10 | /10 |
| `Week12` | `Lecture_week12_v6` | 21 | /21 | `Lab_week12_v5` | 10 | /10 |
| `week13` | `Lecture_week13_v8` | 26 | /26 | `Lab_week13_v3` | 10 | /10 |
| `week14` | `Week14_lecture_style_v11` | 11 | /11 | `Lab_week14_v2` | 10 | /10 |

All 22 decks are 16:9, hold 0 float coordinates and use Calibri and Consolas only.
The newest deck in each folder is the deck in this table.

**Covers.** The covers of Weeks 01 to 13 give the correct week. The Week 14
cover still says "Week 12 · Lecture".

**Course Outline slides.** Weeks 09, 10, 12 and 13 give the same 15 weeks. Week 13
v8 is word for word equal to Week 12 v6. Weeks 09 and 10 differ in one line only
("K8s- PODs" for "K8s – Pods"). Week 06 v7 gives the same plan in other words.
These outlines still disagree:
- Week 01 v6: Week 8 PVs and EKS, Week 12 "RBAC and AKS", presentations in
  Weeks 13 and 14, and Helm.
- Week 03 v2: the same old plan, with Helm and AKS.
- Week 14 v11: "AKS" two times, the broken line "Configmaps & SecretsWeek",
  and presentations in Weeks 13 and 14.

### 4. The build system

**Four engine families now.**
1. `build_week12.py`, 7 importers. No change.
2. Read one delivered deck and copy its design. No change.
3. The kubeadm lab family: `Week05/Lab_week05_v4.pptx` -> `build_week06_lab_v3.py`
   -> `lab_kubeadm.py` -> 20 lab builders (6 `_v1`, 7 short `_v2`, 7 new).
4. New: the lecture-repair family. `build_week08.py` is the engine.

```
build_week08.py (engine, now guarded)
  build_week09_lecture_v6   reads Week09/Week08_lecture_style_v5.pptx
    build_week10_lecture_v8   reads Week10/Week09_lecture_style_v7.pptx
      build_week12_lecture_v4   reads Week12/Week12_v3.pptx
        build_week12_lecture_v5   reads Week12/Lecture_week12_v4.pptx
        build_week12_lecture_v6   reads Week12/Lecture_week12_v5.pptx
          build_week13_lecture_v8 reads Week12/Lecture_week12_v6.pptx
fix_outline_week15          Week09 v6 -> v7, Week10 v8 -> v9
```

Links between the families:
- `build_week12_lab_v5` imports `build_week12_lecture_v6`.
- `build_week13_lab_v3` imports `build_week12_lab_v5` and `build_week12_lecture_v6`.
- So a rebuild of the Week 13 lab needs the Week 12 lecture chain and its 4 input
  decks. A delete of one of these decks stops the rebuild.
- `gate_week13.py` imports `gate_week12.py` and reads the Week 12 v6 outline.

**Run safety.**
- 8 builders save at import: `build_lab`, `build_lab_guide`, `build_week3`,
  `build_week03`, `build_week04`, `build_week05`, `build_week06`, `build_week07`.
  `build_week08` and `build_week09` now have the guard.
- The 6 new lecture builders and `fix_outline_week15` call `prs.save(OUT)` with no
  check. A run in the project root overwrites a delivered deck.
- Each lab builder without `--no-repo` overwrites
  `~/Documents/c/r/CLO835_Fall_2026/WeekNN`. No change.

**The template trap of run 9 is closed.** Six lab builders ran their repository
step into the sandbox clone at `665768b`. The clone showed 0 changed files after
the runs. So the generated folders equal the GitHub folders.

**Two builders read a volatile folder.** `build_week07_lab_v2.py:24` sets
`MIRROR_DIR` to the scratchpad of session `0b02113e` in `/private/tmp`.
`build_week14_lab_v2` imports it. Its repository step now stops with
`FileNotFoundError` for `metrics-server/v0.7.1/components.yaml`.

**The gates cannot run now.** `gate_week12.py` and `gate_week13.py` need the
`INSTRUMENT` file `scratchpad/w9t/instrument.py`. That file is gone. Their inputs
are unchanged since the GATE 1 results of 10-31, so those results still apply to
these files. A new run of the gates is not possible until the file is written again.

### 5. Rebuild proof
Each deck comparison excludes `docProps/`.

| Group | Builders | Outputs | Differences |
|---|--:|--:|--:|
| New lecture builders, `fix_outline_week15` | 7 | 8 decks | 0 parts |
| New lab builders | 7 | 7 decks, 7 scripts | 0 |
| The 7 short labs of run 9 (regression) | 7 | 7 decks, 7 scripts, 7 Blackboard texts | 0 |
| Total | 21 | 43 | 0 |

- All 21 builders exit 0 with `--no-repo` for the labs.
- The repository step: 6 of 7 current lab builders exit 0 and change 0 files.
  `build_week14_lab_v2` stops, see section 4.
- The Blackboard texts from Week 09 v3 to Week 13 v3 are hand-written. No builder
  makes them, so they have no rebuild proof.
- `quiz_pool_src/`, the exam files and the Word files did not change after run 9.
  The run 9 results for them stand. I did not run them again.

### 6. The public course repository
Path: `~/Documents/c/r/CLO835_Fall_2026`. `git ls-remote` gives `665768b` for
`master`, and the local HEAD is `665768b` (2026-10-31 20:35). `git status` shows 0
changed files.

| Folder | Last commit | Files | `localMachine.sh` equals |
|---|---|--:|---|
| Week06 | `1783b12` | 8 | `Week06/localMachine_v4.sh` |
| Week07 | `c5bc5e0` | 9 | `Week07/localMachine_v2.sh` |
| Week09 | `ff69e05` | 8 | `Week09/localMachine_v4.sh` |
| Week10 | `dd284ce` | 8 | `Week10/localMachine_v3.sh` |
| Week12 | `20e8dc9`, `665768b` | 8 | `Week12/localMachine_v5.sh` |
| Week13 | `665768b` | 8 | `week13/localMachine_v3.sh` |
| Week14 | `1783b12` | 9 | `week14/localMachine_v2.sh` |

All 7 lab folders after Week 05 are on GitHub and equal this folder. In run 9, 4 of
them were not on GitHub and Week 06 was the old version.

**Scan of the whole repository:**

| Text | Files |
|---|--:|
| Home IP, `/Users/`, `.ssh/`, the key name, `clo835-mirrors` | 0 |
| An AWS access key or secret key | 0 |
| `luksa`, `nano` | 0 |
| `flannel-io` | 7 (`master-init.sh.tftpl` of Weeks 04, 05, 06, 07, 09, 10, 14) |
| `aquasec` | 3 (Week 03) |
| `busybox` | 4 (Week 03, Week 07 two files, Week 14) |

Weeks 12 and 13 embed the Flannel manifest, so they do not use `flannel-io`. Week 07
and Week 14 have 9 files, against the rule of 8.

### 7. The calendar against the labs
Today is 2026-11-04.

| Date | Topic | Lab folder | On GitHub |
|---|---|---|---|
| 11/4 (today) | PV, PVC, StorageClasses, StatefulSets; Final Project release | `Week10`, lab v3 | yes |
| 11/11 | Mid-Term Exam | none | - |
| 11/18 | ConfigMaps and Secrets | `Week12`, lab v5 | yes |
| 11/25 | RBAC and EKS; Final Project due in the syllabus | `Week13`, lab v3 | yes |
| 12/2 | HPA | `Week14`, lab v2 | yes |
| 12/9 | Helm in the syllabus; project presentation in the decks | none | - |

The blocker of run 9 is gone: each lab from today to 12/2 is on GitHub.

### 8. Links and image tags, tested today
I tested 48 public links in the 22 current decks.
- 39 return 200.
- 2 return 403: `medium.com` and `itnext.io`. These sites refuse scripts, so the
  result is not a proof of a dead link.
- 1 returns 404 but is correct: the base URL `.../CLO835_Fall_2026/master` on Lab
  Week 07 v2 slide 8. The slide adds the file path to it.
- 6 links return 404. They name 5 `sojoudian` repositories that do not exist:

| Repository | Deck and slide |
|---|---|
| `sojoudian/container.training` | Lab Week 04 v2: 13 |
| `sojoudian/flannel` | Lab Week 04 v2: 3, 13 |
| `sojoudian/kubernetes-in-action` | Lab Week 04 v2: 13 |
| `sojoudian/kubia-website-example` | Week 07 v5: 9 |
| `sojoudian/mjarosie.github.io` | Week 14 v11: 11 |

In run 9 the count was 7 repositories. The repairs of Weeks 09 and 12 removed
`sojoudian/eksctl` and `sojoudian/simple-webapp-mysql`.

**Docker Hub.** 11 `maziar` tags return 200: `kubia:0.1`, `v1`, `v2`, `latest`,
`kubia-pet`, `alpine-curl`, `alpine-git`, `curl`, `fortune:args`, `fortune:env`,
`hpa-example`.
`maziar/kubia:1.0` and `maziar/kubia:2.0` still return 404. Week 06 v7 names them
on slides 4, 9 and 20.

Week 14 v11 still links to 3 pages under `eksworkshop.com/beginner/`.

### 9. The PDFs
16 of the 22 current decks have a PDF. Each PDF has one page for each visible
slide, and each PDF is newer than its deck.

**12 of the 16 PDFs have substitute fonts.** They show Carlito for Calibri and Linux
Libertine for Consolas. Linux Libertine is a proportional serif font, so the
commands do not show in a fixed-width font. Only these 4 PDFs show Calibri and
Consolas: Week 12 v6 and lab v5, Week 13 v8 and lab v3. The memory file
`reference-pdf-from-powerpoint.md` records the cause: `soffice` replaces the two
fonts.

The 12 PDFs include today's class: `Week10/Lecture_week10_v9.pdf` and
`Week10/Lab_week10_v3.pdf`. The others: Week 02 lab, Week 03 lecture and lab,
Week 05 lab, Week 06 lecture and lab, Week 07 lab, Week 09 lecture and lab, Week 14
lab.

These 6 current decks have no PDF: Week 01 v6, Week 04 v2 (both), Week 05 lecture v4,
Week 07 v5, Week 14 v11. In run 9 the count was 10.

### 10. The mirror copy is gone
Report #18 of 10-31 named one local copy of `clo835-mirrors`, in the scratchpad of
session `0b02113e`. Today that folder holds 6 files:
- `local-path-provisioner/v0.0.37/local-path-storage.yaml` stays. It equals
  `Week07/local-path-storage.yaml` of the course repository.
- The folders `metrics-server/v0.7.1`, `flannel/v0.28.10` and `keda/2.21.0` are
  empty.
- `.git` has no `HEAD`, so `git log` fails with "not a git repository".

The operating system removes old files from `/private/tmp`. The same cleanup removed
`w9t/instrument.py` from this session.

Effect:
- `sojoudian/clo835-mirrors` is still not on GitHub, so the 10 project files that
  name it still fail at install.
- Metrics-server: `Week14/metrics-server.yaml` in the course repository is a public
  copy. Flannel: `Week12/assets/kube-flannel-v0.28.10.yml` in this folder is a local
  copy.
- KEDA 2.21.0: no copy exists on this computer. Project 16 needs it. Only the
  upstream release of `kedacore` has it.

### 11. Defects re-tested today

| Defect | State |
|---|---|
| Assignment 1 repair not on GitHub (`iputils-ping` count 0, no `.dockerignore`) | open |
| `assignment-2/.github/workflows/docker.yml:25` is not valid YAML (a `: ` inside a plain scalar) | open, file unchanged since 10-14 |
| `Week02/README.md:64` recommends `r6i.large` | open |
| `Week04/localMachine.sh:82` calls `./cleanup_lab04.sh`, which `master-init` does not write | open |
| Port 6443 open to `0.0.0.0/0` in Weeks 04 and 05 `main.tf` (Week 06 and later: `self`) | open |
| Week 05 lab: 14 step headers, above the limit of Step 0 to 6 | open |
| Week 04 v2 decks: footers /38 | open |
| Week 05 lecture: footers /29 with 30 slides | open |
| Home IP in `week02/terraform-vm`, 6 reports and 2 `ARCHITECTURE/` files | open; not in the course repository |
| `week05_practical_work/week5_code/week5_code/` nested duplicate | open |
| Empty folder `Week11-Exam/` | open |
| Final exam v2: longest option correct in 50 % of MC rows; files say "Final Exam", the syllabus says Mid-Term on 11/11 | open, files unchanged |
| Week 06 v7: `maziar/kubia:1.0` and `:2.0` do not exist | open |
| Week 14 v11: cover "Week 12", AKS outline, `eksworkshop.com/beginner` links, no PDF | open |
| `ARCHITECTURE/LATEST.md` (2026-10-08) | three runs old |

Closed after run 9:
- 4 lab folders not on GitHub, and the old Week 06 on GitHub.
- The `lab_kubeadm.py` template trap.
- 2 of 7 dead repository links.
- The Course Outline conflict for Weeks 06, 09, 10, 12 and 13.
- The covers of Weeks 09, 12 and 13.
- The unguarded `build_week08` and `build_week09`.

### 12. Assessments
- **Final Project:** the 34 project files did not change after report #18. The
  state of that report stands, with one change: the mirror copy is now gone. A
  student email of this week says Project 8 is assigned and other topics are
  claimed. So students claim projects before the fixes of report #18.
- **Assignment 1:** 12 of 13 grades are final. The late recording of `dilewis` is
  your decision.
- **Mid-Term on 11/11:** see section 11.

### 13. Risks, ranked
1. The project files name a repository that does not exist, and the KEDA bundle has
   no copy now. Students already claim projects.
2. The exam of 11/11 has the length clue in 50 % of its MC rows.
3. 12 PDFs, including today's lecture and lab, show commands in a serif font.
4. The gates and 2 lab builders depend on files in `/private/tmp`. Two of these
   files are already gone.
5. The decks of Weeks 01, 03 and 14 give an old course plan.

## Results
- 21 of 21 builders exit 0. 43 of 43 outputs equal the stored files.
- The repository step: 6 of 7 lab builders change 0 files in a clone at `665768b`;
  1 stops on a deleted mirror file.
- GitHub `master` = local HEAD = `665768b`. 7 of 7 lab folders equal this folder.
- 22 current decks: 16:9, 0 floats, 2 fonts. 2 decks have wrong footers.
- 6 dead repository links, 2 missing image tags.
- 12 of 16 PDFs have substitute fonts.
- No server started, so no port is used.

## Issues / Notes
- I did not run the 8 unguarded builders. Their files are older than run 7.
- I did not run the gates, because their helper file is gone. I did not write a new
  helper, because a new file would make a different gate.
- I did not render any deck to an image. The scans read slide text, so they miss
  text inside a picture.
- I did not re-read `DESIGN_LANGUAGE.md`, `analysis/`, `old/` or `old_assessments/`.
  They did not change.
- I did not open the student files in `a1/` or `a1.zip`.
- The link test used HTTP requests only. A 200 result does not prove that the page
  content still agrees with the slide.
- This report names no home IP and no student name.
