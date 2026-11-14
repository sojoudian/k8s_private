# CLO835 Repository — Deep Analysis (2026-10-08)

**Run:** 7. **Type:** full re-scan, not a delta.
**Supersedes:** `ARCHITECTURE_2026-09-16_11-51-47.md` (run 6).
**Method:** full tree scan; a 686 MB sandbox mirror; every builder executed in that
mirror; a ZIP-CRC reproducibility compare; a binary audit of all 170 decks; a gate
run over every MCQ file; a Terraform `init` and `validate`; a secret sweep.
**Repo files written by this run:** 3, and all three are byte-identical rebuilds
(`quiz_pool_src/Week0*_Pool_Blackboard.txt`, md5 unchanged).
**Confidence:** High. Every number below comes from a command this run executed.

---

## 0. The repository in one table

| Measure | Value |
|---|--:|
| Total size | 1.8 GB |
| Of which `.venv` | 198 MB |
| Of which one stale Terraform cache | 765 MB |
| Files, excluding `.venv` | 1 788 |
| PowerPoint decks | 170 |
| First-party Python files | 30 |
| First-party Python lines | 18 145 |
| Reports | 101, from 2026-05-19 to 2026-10-07 |
| Weeks with a deck | 12 |

---

## 1. What changed since run 6 (2026-09-16)

| Change | Detail |
|---|---|
| **Python grew by 13 files and 3 566 lines** | 17 files / 14 579 lines, now 30 / 18 145 |
| **A new subsystem appeared** | `quiz_pool_src/` — a question-pool builder with 7 gates |
| **Week 03 gained a second lecture version** | `Week03_lecture_style_v2.pptx`, one wrong fact corrected |
| **Week 05 gained v2 and v3 of both decks** | lecture 30 slides, lab 11 slides |
| **The Week 05 lab code was replaced** | kind, one node → kubeadm, 1 master and 2 workers |
| **Three of the ten open defects are now closed** | all three Week 05 Terraform defects |
| **Seven defects remain open, and five new ones are found** | see section 4 |

---

## 2. The build system

### 2.1 Shape

`build_week12.py` is the engine: 2 371 lines, the palette, the fonts, and the shared
renderers. Seven modules import it:

- `build_lab01.py`, `build_week01.py`, `build_week02.py`,
  `build_week12_v3_lab.py`, `build_week13.py`, `build_week14.py`, `fix_week03.py`.

`fix_week03.py` imports `build_week02` as well, so it is the only two-parent module.

### 2.2 Run safety

**Ten of the twenty root builders save a deck at import.** They carry no
`__main__` guard, so importing one writes a file:

```
build_lab.py  build_lab_guide.py  build_week3.py  build_week03.py
build_week04.py  build_week05.py  build_week06.py  build_week07.py
build_week08.py  build_week09.py
```

Run any of them in a sandbox only.

### 2.3 Which builders run

Every builder was executed in a full sandbox mirror.

| Result | Count | Which |
|---|--:|---|
| Runs clean | 15 | all the rest |
| Fails | 5 | `assemble_week13`, `assemble_week14`, `build_week08`, `build_week09`, `fix_week03` |

**Root cause of the `build_week08` and `build_week09` failures: the folder names
are off by one.** The repo stores the Week 08 deck in `Week09/` and the Week 09
deck in `Week10/`. The builders look in `Week08/assets` and `Week09/assets`.

Proof:

- `build_week08.py:59` reads `ASSETS_DIR = "Week08/assets"`. `Week08/` does not
  exist. The file it wants, `s05_1.png`, is at `Week09/assets/s05_1.png`.
- `build_week09.py:62` reads `ASSETS_DIR = "Week09/assets"`. The file it wants,
  `s05_1.jpg`, is at `Week10/assets/s05_1.jpg`.

Each one needs two path edits and a matching output path. That is the three-line
fix recorded in earlier runs, now with the exact cause.

`assemble_week13.py:8` and `assemble_week14.py:8` point at
`/private/tmp/.../4c65ef92-.../scratchpad`. That session directory is gone, so both
scripts are dead. `build_week13.py` and `build_week14.py` still run, because the
JSON they consume is committed.

`fix_week03.py` wants `Week03.pptx` at the repository root. The root holds
`Week3.pptx` and `new_Week3.pptx`, and `week03/Week03.pptx` holds the source.

### 2.4 Reproducibility

Thirteen decks were rewritten by the sandbox run and compared slide-part by
slide-part against the stored file.

**Twelve rebuild content-identically. One diverges:**
`Week06/Week06_lab_style_v2.pptx`, 142 slide parts differ, because a person re-saved
it in PowerPoint.

---

## 3. The decks

### 3.1 The canonical deck of each week

| Week | Folder | Newest deck | Slides | Footer |
|---|---|---|--:|---|
| 01 | `week01` | `Week01_lecture_style_v5.pptx` | 38 | /38 correct |
| 02 | `week02` | `Lab01_v1.pptx` | 24 | /24 correct |
| 03 | `week03` | `Week03_lecture_style_v2.pptx` | 15 | /15 correct |
| 04 | `Week04` | `Week04.pptx` | 26 | **/38 WRONG** |
| 05 | `Week05` | `Lab_week05_v3.pptx` | 11 | /11 correct |
| 06 | `Week06` | `Week06.pptx` | 24 | **/71 WRONG** |
| 07 | `Week07` | `Week07_lab_style_v3.pptx` | 14 | /14 correct |
| 08 | `Week09` | `Week08_lecture_style_v3.pptx` | 13 | /13 correct |
| 09 | `Week10` | `Week09_lecture_style_v4.pptx` | 36 | /36 correct |
| 12 | `Week12` | `Week12_lab.pptx` | 10 | /10 correct |
| 13 | `week13` | `Week13_lab_style_v6.pptx` | 26 | /26 correct |
| 14 | `week14` | `Week14_lab_style_v10.pptx` | 23 | /23 correct |

### 3.2 The float-coordinate bug

**27 decks carry float coordinates.** Earlier runs named one. The full list:

- `Week04/Week04_lab_style*.pptx` — 16 decks, 69 to 181 floats each.
- `Week05/Week05_lab_style_v1..v11.pptx` — 11 decks, 30 to 53 floats each.

Every canonical deck and every `FINAL/` deck is clean. The bug lives only in the
superseded version chains of Week 04 and Week 05.

### 3.3 Footer denominators that do not match the slide count

Twenty-one decks. The ones that matter, because somebody may open them:

| Deck | Slides | Footer says |
|---|--:|---|
| `Week04/FINAL/Week04.pptx` | 26 | /38 |
| `Week04/FINAL/Lab_week04.pptx` | 13 | /38, and the sequence jumps 1 then 27 |
| `Week04/Week04.pptx` | 26 | /38 |
| `Week06/Week06.pptx` | 24 | /71 |
| `Week06/Week06_lecture_style_v5.pptx` | 41 | /71 |
| `finalWork/Week04.pptx` | 26 | /38 |
| `finalWork/Week06_Part_A.pptx` | 24 | /71, 1 slide has no footer |
| `finalWork/Week06_Part_B.pptx` | 24 | /71, 1 slide has no footer |
| `finalWork/Lab06.pptx` | 11 | /71 |

### 3.4 Decks still on the 4:3 canvas

Ten. All are source decks or the `finalWork` and `old` copies of them:
`Lab01.pptx`, `Week3.pptx`, `finalWork/Lab01.pptx`, `finalWork/Week01.pptx`,
`finalWork/Week02.pptx`, `old/Week01-03.pptx`, `week01/Week01.pptx`,
`week02/Week02.pptx`.

### 3.5 The Week 04 contradiction

`Week04/FINAL/Lab_week04.pptx` now teaches kubeadm correctly. Slide 5 reads
"No kind, no Docker-in-Docker."

`Week04/FINAL/Week04.pptx`, the lecture, still teaches kind on seven slides. Slide
26 reads: "In this course: we'll use kind locally for Week 4-7, then EKS for Week 8."

The lecture and the lab disagree.

`Week04/FINAL/Week04.pdf` is older than `Week04.pptx`, so the PDF is stale.

---

## 4. Defect status

### 4.1 Closed since run 6

| Defect | Evidence today |
|---|---|
| Week 05 lab `terraform init` fails | No registry module remains. `terraform init` and `validate` both pass. |
| Two zero-width spaces | 0 non-ASCII bytes in any `.tf`, `.sh`, `.tftpl`, `.yaml` under `week05_practical_work` |
| `week5.pub` missing | The `aws_key_pair` resource is gone; `var.key_name` prompts instead |

### 4.2 Still open

| Defect | State today |
|---|---|
| `Week04_lab_style_v16.pptx` | 175 floats, off-palette `556F88` |
| `Week06_lecture_style_v5.pptx` | 41 slides, footer /71 |
| `finalWork/Week04.pptx` | 26 slides, footer /38 |
| `finalWork/Week06_Part_A/B.pptx` | both /71, one slide each with no footer |
| `build_week08.py` | cannot find `Week08/assets` |
| `build_week09.py` | `KeyError: 's05_1.jpg'` |
| `assemble_week13/14.py` | point at a dead scratchpad path |
| `Week05_lab_style_v26.pptx` | 29 slides, /39 — superseded by `lecture_week05_v3` |

### 4.3 New, found by this run

1. **27 decks carry float coordinates**, not one.
2. **`Week04/FINAL/Lab_week04.pptx` has a broken footer sequence**: slide 1 says
   1/38, slide 2 says 27/38.
3. **The final exam is guessable.** `CLO835_Final_Exam_Blackboard.txt` holds 40
   questions. The correct option is the longest in **53%** of the multiple-choice
   rows. Ten questions point at a slide, a lecture or a table.
4. **`Week09/Week08_Quiz_Blackboard.txt`** has three questions that point at the
   lecture, and one that asks an AWS price.
5. **`week01/Week01_Quiz_Blackboard.txt`** still holds Q14 and Q15, which ask for
   numbers inside a chart, and Q16, which asks for "Step 3".

---

## 5. The question-pool subsystem

New since run 6. `quiz_pool_src/` holds `build2.py` (the builder and seven gates),
`q2_w01.py`, `q2_w02.py`, `q2_w03.py` (the questions), `qedit.py` and `pick20.py`.

The seven gates: self-contained stem, correct answer true in 2026, no length
giveaway, no answer leak, structure, no in-pool repeat, no cross-pool repeat.

Current state, re-run during this analysis:

| Pool | Questions | Gate errors | Longest-option |
|---|--:|--:|--:|
| Week 01 | 100 | 0 | 26% |
| Week 02 | 100 | 0 | 25% |
| Week 03 | 100 | 0 | 27% |
| Hard 20 | 20 | 0 | 30% |

`quiz_pool_src/rejected_v1/` keeps the first attempt: 110 gate failures across the
three files, and 45 to 49% longest-option. It must never be uploaded.

---

## 6. Infrastructure code

| Location | State |
|---|---|
| `week05_practical_work/week5_code/` | kubeadm, 1 master and 2 workers. `terraform validate` passes. |
| `week05_practical_work/week5_code/legacy_kind/` | the old kind set, kept and unused |
| `week05_practical_work/week5_code/week5_code/` | a nested duplicate, 7 files, still broken |
| `week02/terraform-vm/` | the Week 02 demo VM. **Holds the home IP in two files.** |
| `week03/cleanup_lab03.sh` | the Week 03 cleanup script |

---

## 7. Secrets

- No AWS access key, no `.pem`, no `.ppk`. The two `aws_session_token` hits are
  slide text, not credentials.
- `week02/terraform-vm/variables.tf:57` and `terraform.tfvars:11` hold
  `173.33.124.240/32`, the home IP. Four reports repeat it.
- `mazSeneca.pub` sits at the repository root.
- The repository is **not** under git, so nothing has been pushed from here.

---

## 8. Waste

| Item | Size or count |
|---|---|
| `week02/terraform-vm/.terraform` | **765 MB**, a provider cache |
| `.venv` | 198 MB |
| Superseded `Week04_lab_style*` decks | 16 |
| Superseded `Week05_lab_style*` decks | 26 |
| Nested duplicate `week5_code/week5_code/` | 7 files |
| Stray Week 05 files inside `Week04/` | 3 |
| `.bak`, `.DS_Store` and similar | 14 |
| Empty folders | `Week11-Exam`, `untitled folder` |
| `__pycache__` written through the import seam | 2 folders |

Removing the Terraform cache alone reclaims 765 MB of the 1.8 GB.

---

## 9. Priorities

1. **Fix the Week 04 lecture.** It teaches kind on seven slides while the lab
   teaches kubeadm. A student reads both.
2. **Fix the `Week04/FINAL` footers.** The lab sequence jumps from 1 to 27.
3. **Fix the final exam.** A student who always picks the longest option scores
   53%.
4. **Apply the off-by-one path fix** to `build_week08.py` and `build_week09.py`.
   The assets exist; only the folder names are wrong.
5. **Repair the `finalWork` footers** and the two slides with no footer.
6. **Delete `week02/terraform-vm/.terraform`** and scrub the home IP.
7. **Add the coordinate guard to `build_week04.py`**, then re-save the Week 04
   version chain.
8. **Write `validate.py`.** It would catch items 2, 5 and 7 automatically.
