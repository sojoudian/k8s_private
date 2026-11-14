# Report: Repository analysis, run 9 (delta over run 8, 2026-10-27)
**Date**: 2026-10-30
**Sequence**: #01 for the day

## Summary
I analysed the repository with read-only checks. The base is run 8
(`report-2026-10-27-04-repo-analysis-run8.md`) and the 10 reports after it. This
folder is the build system for the CLO835 Fall 2026 course. Python builders make
the decks, the quizzes and the lab scripts. The live lab code is in a separate
public GitHub repository. All 61 new outputs that I rebuilt in a sandbox are
exact copies of the stored files. The largest risk is outside this folder: the
lab of the next class (2026-11-04) is not on GitHub.

## What Changed
- Created this report.
- Updated 3 memory files and `MEMORY.md`: `project-clo835-arch-analysis`,
  `project-short-labs-2026-10-27`, `project-clo835-fall2026-repo`.
- No other file changed. All rebuilds ran on copies in the session scratchpad,
  with `HOME` set to a sandbox folder and `--no-repo` on each lab builder.
- I did not change `ARCHITECTURE/`. `ARCHITECTURE/LATEST.md` (2026-10-08) is now
  two runs old.

## Technical Details

### 1. What the repository is
The project produces the full teaching set of one course: lectures, labs, quizzes,
exams, assignments and the semester project.

| Layer | Content | Main files |
|---|---|---|
| Specification | Rules and design | `PROMPT.md`, `DESIGN_LANGUAGE.md`, `CLAUDE.md`, `~/.claude/PREFERENCES.md` |
| Deck builders | Python with python-pptx | `build_*.py`, `lab_kubeadm.py` |
| Repair scripts | Change a delivered file into its next version | `dedup_lectures.py`, `retarget_*.py`, `fix_*.py` |
| Decks | Delivered slides | Week folders, `finalWork/`, `old/` |
| Assessments | Pools, quizzes, exam, assignments, project | `quiz_pool_src/`, `Assignments/`, `project/`, root exam files |
| Lab code | Terraform and scripts | The public repository, not this folder |

### 2. The repository in numbers

| Measure | Run 8 | Now |
|---|--:|--:|
| Total size | 1.8 GB | 2.06 GB |
| Of which `week02/terraform-vm` (provider cache) | 765 MB | 765 MB |
| Of which `.venv` | 198 MB | 198 MB |
| Of which `a1.zip` (new) | 0 | 222 MB |
| Files, excluding `.venv` | 1 868 | 2 026 |
| PowerPoint decks | 175 | 211 |
| Decks at 16:9 / at 4:3 | 165 / 10 | 201 / 10 |
| Python files, first party | 51 | 71, 30 318 lines |
| Of which at the root | 26 | 46, 24 937 lines |
| Reports | 124 | 135 before this report |

The folder is not a git repository. It has no remote and no history.

### 3. The current deck of each week
The numbers come from a new audit of all 211 decks.

| Folder | Lecture | Slides | Footer | Lab | Slides |
|---|---|--:|---|---|--:|
| `week01` | `Week01_lecture_style_v6` | 38 | /38 | none | - |
| `week02` | none | - | - | `Lab01_v1` | 24 |
| `week03` | `Week03_lecture_style_v2` | 15 | /15 | `Lab03_lab_style_v1` | 8 |
| `Week04/FINAL` | `Week04_v2` | 26 | **/38 wrong** | `Lab_week04_v2` | 13, **/38 wrong** |
| `Week05` | `lecture_week05_v4` | 30, 1 hidden | /29 | `Lab_week05_v4` | 18 |
| `Week06` | `Week06_lecture_style_v7` | 34, 1 hidden | /34 | `Lab_week06_v4` | 10 |
| `Week07` | `Week07_lab_style_v5` | 12 | /12 | `Lab_week07_v2` | 10 |
| `Week09` | `Week08_lecture_style_v5` | 11 | /11 | `Lab_week09_v2` | 10 |
| `Week10` | `Week09_lecture_style_v7` | 28 | /28 | `Lab_week10_v2` | 10 |
| `Week12` | `Week12_v3` | 21 | /21 | `Lab_week12_v2` | 10 |
| `week13` | `Week13_lecture_style_v7` | 21 | /21 | `Lab_week13_v2` | 10 |
| `week14` | `Week14_lecture_style_v11` | 11 | /11 | `Lab_week14_v2` | 10 |

All 22 decks are 16:9, hold 0 float coordinates and use Calibri and Consolas only.
These lists supersede the canonical table of run 8.

`Lab_week06_v4.pdf` and the other 6 short lab PDFs exist. These 10 current decks
have no PDF: Week 01 v6, Week 04 v2 (both), Week 05 lecture v4, Week 07 v5,
Week 08 v5, Week 09 v7, Week 12 v3, Week 13 v7, Week 14 v11.

### 4. The build system

**Run safety.** The 10 unguarded builders of run 8 are unchanged: `build_lab`,
`build_lab_guide`, `build_week3`, `build_week03`, `build_week04`, `build_week05`,
`build_week06`, `build_week07`, `build_week08`, `build_week09`. They save a deck at
import. Run them in a sandbox only. `lab_kubeadm.py` has no `__main__` guard, but
its module body writes nothing.

**Three engine families.**
1. `build_week12.py` (2 371 lines). Importers: `build_lab01`, `build_week01`,
   `build_week02`, `build_week12_v3_lab`, `build_week13`, `build_week14`, `fix_week03`.
2. Read one delivered deck and copy its design: `build_week05_lab_v4`,
   `build_week06_v6`, `build_week06_v7`, `build_week06_lab_v1` to `v3`.
3. New: the kubeadm lab family, below.

**The kubeadm lab family (2026-10-27).** One slide list makes the deck and
`localMachine.sh`, so the two cannot differ.

```
Week05/Lab_week05_v4.pptx  (design source, read only)
        |
build_week06_lab_v3.py     (engine)
        |
lab_kubeadm.py             (make_lab, make_repo_folder, blackboard_text, check_lines)
        |
build_week06_lab_v4, build_week07_lab_v2, build_week09_lab_v2, build_week10_lab_v2,
build_week12_lab_v2, build_week13_lab_v2, build_week14_lab_v2
```

Extra links between builders:
- `build_week10_lab_v2` and `build_week14_lab_v2` import `build_week07_lab_v2`.
- `build_week12_lab_v2`, `13` and `14` import their `_v1` builder for manifests.

A delete of `Week05/Lab_week05_v4.pptx` or of `build_week06_lab_v3.py` stops all 7
labs. The same is true of a `_v1` builder for its `_v2`.

**Each lab builder writes outside this folder.** Without `--no-repo`,
`make_repo_folder()` overwrites `~/Documents/c/r/CLO835_Fall_2026/WeekNN`.

**A trap in the Week 06 template.** `lab_kubeadm.py:32` reads the template from
git HEAD. `lab_kubeadm.py:104` requires the text
`chown ubuntu:ubuntu /home/ubuntu/.kube/config` exactly one time, or the build
stops with `template changed`. HEAD holds that text one time. The uncommitted
Week 06 change replaces it with `chown -R`, so the count is 0. After that commit,
every repo step of the 7 builders stops. `--no-repo` runs still work.

**Repair scripts.** `retarget_accounts.py`, `retarget_kind.py`, `dedup_lectures.py`
and `retarget_kind_docx.py` read an input and refuse to overwrite an output. Run
them from the project root, because their paths are relative.

### 5. Rebuild proof
Each comparison excludes `docProps/`.

| Group | Outputs | Differences |
|---|--:|--:|
| 7 short lab decks | 7 decks, 53 parts each | 0 |
| 7 `localMachine` scripts | 7 | 0 bytes |
| 7 Blackboard submission texts | 7 | 0 bytes |
| Decks of `retarget_accounts`, `retarget_kind`, `dedup_lectures` | 22 | 0 parts |
| Word files of `retarget_kind_docx` | 18 | 0 parts |
| Total | 61 | 0 |

Quiz results, on a copy of `quiz_pool_src/`:
- `build2`, `build3`, `build_easy20`, `build_easy20_w34` and `build_easy20_w56`
  exit 0. A recursive `diff` against the stored folder prints nothing.
- `audit3`, `audit_easy20`, `audit_easy20_w34`, `audit_easy20_w56` and `audit_qti3`
  report 0 errors. `audit_qti3` reads a relative path, so it needs its own folder
  as the working directory.

`build_week08.py`, `build_week09.py`, `assemble_week13.py`, `assemble_week14.py` and
`fix_week03.py` are unchanged, so the run 8 failures stand. I did not run them.

### 6. The public course repository
Path: `~/Documents/c/r/CLO835_Fall_2026`. The local HEAD equals `origin/master`:
`2dbeafc`, 2026-10-28.

| Folder | On GitHub | Local state | Equal to `localMachine_vN.sh` of this folder |
|---|---|---|---|
| Week02 to Week05 | yes | unchanged | - |
| Week06 | **old version, 4 workshops, `luksa/kubia`** | 3 modified files, not committed | yes (local) |
| Week07 | yes (`c5bc5e0`) | clean | yes |
| Week09 | yes (`2dbeafc`) | clean | yes |
| Week10 | **no** | untracked | yes (local) |
| Week12 | **no** | untracked | yes (local) |
| Week13 | **no** | untracked | yes (local) |
| Week14 | **no** | untracked | yes (local) |

The second clone `~/Documents/c/r/a2_test/CLO835_Fall_2026` is at `39a43b1`. It still
holds the verified Assignment 1 repair as uncommitted changes.

### 7. The calendar against the labs
Source: `CLO835_SYL/clo835-nce-6401_1790130855373.pdf`. Today is in the Study Week
(10/28 and 10/30).

| Date | Topic | Due | Folder of the lab | On GitHub |
|---|---|---|---|---|
| 11/4 | PV, PVC, StorageClasses, StatefulSets; Final Project release | Lab 7 | `Week10` | **no** |
| 11/11 | Mid-Term Exam | Exam, Lab 8 | none | - |
| 11/18 | ConfigMaps and Secrets | Quiz 4, Optional Lab 9 | `Week12` | **no** |
| 11/25 | RBAC and Amazon EKS | Optional Lab 10, Final Project | `Week13` | **no** |
| 12/2 | HPA | Quiz 5 | `Week14` | **no** |
| 12/9 | Helm | - | none | - |

The first slide of each short lab runs `cd CLO835_Fall_2026 && git pull && cd WeekNN`.
This line fails for these 4 weeks until the push. Also, the Week 10 and Week 14 labs
apply a manifest from a raw URL that returns 404 now.

The syllabus still lists Helm on 12/9. The memory schedule says "Helm dropped".

### 8. Links and image tags, tested today
- **Docker Hub tags that do not exist:** `maziar/kubia:1.0` and `maziar/kubia:2.0`.
  `Week06_lecture_style_v7` names them on slides 4, 9 and 20. The tags that exist:
  `0.1`, `latest`, `v1`, `v2` and 3 commit tags. A student who copies these commands
  gets a failed image pull. Every other tagged `maziar` image returns 200.
- **Dead GitHub links in current decks:** 9 links to 7 repositories that do not exist.

| Repository | Deck and slide |
|---|---|
| `sojoudian/flannel` | Lab Week 04 v2: 3, 13 |
| `sojoudian/container.training` | Lab Week 04 v2: 13 |
| `sojoudian/kubernetes-in-action` | Lab Week 04 v2: 13; Week 12 v3: 21 |
| `sojoudian/eksctl` | Week 08 v5: 11 |
| `sojoudian/kubia-website-example` | Week 07 v5: 9 |
| `sojoudian/simple-webapp-mysql` | Week 12 v3: 21 |
| `sojoudian/mjarosie.github.io` | Week 14 v11 |

`sojoudian/clo835-mirrors` also returns 404, but the short labs no longer need it.
`gh` is not logged in. The local copy of the mirror is in the scratchpad of session
`0b02113e`, and the operating system can delete that folder.

### 9. The rule "only maziar and sojoudian" on GitHub
Report 05 said the public repo copy held 0 `luksa`, 0 `aquasec` and 0 `flannel-io`.
That is no longer true. The user re-cloned the repository at `acd8cdf`, so those
uncommitted changes are gone. HEAD holds:
- `aquasec/trivy` in 3 files of `Week03`.
- `luksa/kubia` in 14 lines of `Week06/localMachine.sh`.
- `flannel-io` in `master-init.sh.tftpl` of Weeks 04, 05, 06, 07 and 09. The 4 new
  local folders hold it too.

### 10. Defects re-tested today

| Defect | State |
|---|---|
| Assignment 1 repair not on GitHub (`iputils-ping` count 0, no `.dockerignore`) | open |
| `assignment-2/.github/workflows/docker.yml:25` is not valid YAML | open, confirmed with a parser |
| `Week02/README.md:64` recommends `r6i.large`, which the Learner Lab stops | open |
| `Week04/localMachine.sh:82` calls `./cleanup_lab04.sh`, absent on the master | open |
| Port 6443 open to the internet in Weeks 04 and 05 `main.tf` | open |
| Week 05 lab: 14 steps, above the limit of Step 0 to 6 | open |
| Week 04 v2 decks and `finalWork/Week04`, `Week04_v2`: /38 | open |
| `finalWork/Week06_Part_A`, `Part_B`, `Lab06`: /71 | open |
| `Week04/Week04_lab_style_v16.pptx`: 175 floats (27 decks, 2 205 floats, all in superseded chains) | open |
| Two footer conventions (Week 05 /29, Week 06 /34) | open |
| Home IP in `week02/terraform-vm/variables.tf` and `terraform.tfvars` | open; also in 6 reports and 2 `ARCHITECTURE/` files |
| `week5_code/week5_code/` nested duplicate | open |
| Empty folder `Week11-Exam/` | open |

**New or changed findings:**
- Final exam: `CLO835_Final_Exam_v2_Blackboard.txt` has 40 questions. The correct
  option is the longest in 13 of 26 MC rows, which is 50 %. The earlier file is 54 %.
- The syllabus calls this exam a Mid-Term (20 %). The files say "Final Exam".
- `Week04/FINAL/Week04.pdf` and `Lab_week04.pdf` still show kind. No v2 PDF exists.
- `week02/Lab01_v1` slide 5 shows an AWS account number in a command output. It is
  not in the public repository.
- Week 14 v11 still links to `eksworkshop.com/beginner/...` on slides 10 and 11.
- Week 13 v7 slide 10 holds `–k`, with an EN DASH, in a `curl` command.

**The Course Outline slides do not agree:**

| Deck | Numbering |
|---|---|
| Week 01 v6 | Study Week, Week 8 PVs and EKS, Week 9 Statefulsets, Week 10 ConfigMaps, Week 11 Exam |
| Week 06 v7 | Week 8 Study Week, Week 9 PVs and EKS, Week 10 StorageClasses, Week 11 Mid-Term, Week 12 ConfigMaps |
| Week 12 v3 | Week 09 PVs and "AKS"; broken line "Week 12: K8s" |
| Week 14 v11 | Week 9 PVs and "AKS"; broken line "Configmaps & SecretsWeek" |
| Syllabus | PVs and EKS on 10/23, then the Study Week |

The covers also differ from the folders. Week 09 folder: "Week 8". Week 12: "Week
10". Week 13: "Week 11". Week 14: "Week 12". A relabel waits for the approval of the
user.

### 11. Source conflicts that stay open
1. `PROMPT.md` R1 (keep the text verbatim) against the repairs of Weeks 05 to 14.
2. `PROMPT.md` `ALERT_RED` E74C3C against the audit house red FF5F56.
3. `PROMPT.md` reference deck `Week04_v02_02` against `week01/Week01_lecture_style_v5`.
4. `PROMPT.md` "Week 9 = EKS" against the syllabus (10/23).

### 12. New input: `a1.zip`
- Added 2026-10-30 15:19, 222 MB. I listed it and did not extract it.
- It holds 13 Blackboard attempts for Assignment 1: 34 files (13 txt, 8 docx, 5 pdf,
  5 png, 2 zip, 1 mp4). The attempt dates are 2026-10-04 to 2026-10-15.
- The file names hold student names and logins. This report names no student.
- The folder is local and is not a repository. Do not copy this archive into the
  public repository.

## Results
- 61 of 61 new outputs reproduce with 0 differences.
- All quiz files rebuild byte-identical, and all audits report 0 errors.
- 211 decks audited. 22 current decks: 0 floats, 16:9, 2 typefaces.
- 2 of 6 weeks after Week 06 are on GitHub. Week 06 on GitHub is the old version.
- 2 image tags and 7 repositories named by current decks do not exist.
- No server started, so no port is used.

## Issues / Notes
- I used `cd` in my first shell commands, against `PREFERENCES.md` section 5. The
  session directory moved to `reports/`. I moved it back and used absolute paths
  after that. Subshell `cd` calls ran only inside the sandbox.
- I did not run the 10 unguarded builders. Their files are older than run 7.
- I did not render any deck to an image in this run. The content scan reads slide
  text only, so it misses text inside a picture.
- I ran no Terraform command and made no AWS call. I ran no `git fetch`. I used
  `git ls-remote`, plus HTTP checks to GitHub and Docker Hub.
- I did not re-read `DESIGN_LANGUAGE.md`, `analysis/`, `old/` or `old_assessments/`.
  These files are older than run 7, so the run 7 model holds.
- I did not open the student files in `a1.zip`.
