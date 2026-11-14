# Report: Assignment 1 — Repaired, End to End
**Date**: 2026-10-15
**Sequence**: #01 for the day

## Summary
A student, Yiming Pan, asked why the handout lists the Docker steps as Pull,
Build, Push, Pull. The student is correct, and the handout is wrong. The user
asked me to fix Assignment 1 and everything related to it. I found **eight**
defects across the handout, the repository and the Blackboard text. Two of them
make a graded requirement impossible. All eight are fixed.

## What Changed

### New files
- `fix_assignment1_docx.py` — the repair script for the handout. It is guarded,
  it reads the original, and it never writes it.
- `Assignments/Assignment_1/CLO835_Assignment1_v2.docx` — the repaired handout.
- `Assignments/Assignment_1/Assignment1_Blackboard_Submission.md` — the
  Blackboard text, corrected and matched to the handout.
- This report.

### Changed files, in the public repository
`~/Documents/c/r/a2_test/CLO835_Fall_2026/assignment-1/`
- `Dockerfile` — adds `iputils-ping`.
- `compose.yaml` — adds `build: .` to the `pink` and `lime` services.
- `README.md` — rewritten, 14 lines removed and 147 added.

### Unchanged
- `Assignments/Assignment_1/CLO835_Assignment1.docx` — 201 718 bytes, Sep 30.
- `app.py`, `mysql.sql`, `requirements.txt`, `templates/`.
- Nothing is committed, and nothing is pushed.

## Technical Details

### The eight defects

| # | Where | Defect | Marks at risk |
|---|---|---|---|
| 1 | handout | The Recording list starts with Pull, before Build and Push | — |
| 2 | handout | "This assignment has 3 main parts", but the grade table scores four | 15 |
| 3 | handout | No check that the two images differ, which is the mis-tag trap | 15 |
| 4 | `Dockerfile` | No `iputils-ping`. The Ubuntu base image holds no `ping` | 10 |
| 5 | `README.md` | No `docker login`, `tag`, `push` or `pull` at all | 25 |
| 6 | `README.md` | No MySQL connection test with a MySQL image | 15 |
| 7 | `README.md` | Creates a container named `blue` two times | — |
| 8 | `README.md` | No wait for MySQL, so the web container stops at once | — |

### Defect 1 — the student is right
The handout Recording list reads:
1. Pull the webapp and MySQL images from Docker Hub using `docker pull`.
2. Build the images locally after you merge into the master branch.
3. Push the images to Docker Hub.
4. Open a terminal and run `docker pull` to fetch the images.

Step 1 and step 4 are the same step. Step 1 is impossible, because the push in
step 3 creates the images. I deleted step 1. The Blackboard text never held the
error, so the two documents now agree.

### Defect 4 — a graded requirement is impossible
The rubric gives 10 marks for `ping pink` from inside the `blue` container. The
`Dockerfile` installs `python3`, `python3-venv`, `mysql-client` and
`ca-certificates`, with `--no-install-recommends`. The Ubuntu image holds no
`ping`, and `ping` comes from the `iputils-ping` package. Every student that
used the supplied `Dockerfile` met `ping: command not found`.

I could not run Docker on this machine to prove it, so I verified the fact by
web search. The fix adds `iputils-ping` to the apt list, with a comment that
names the reason.

### Defect 5 — the README skipped 25 marks of the rubric
The README built the images, ran them and ran Compose. It never showed
`docker login`, `docker tag`, `docker push` or `docker pull`. Those four
commands carry 25 of the 100 marks, and they are the subject of the student
question. The new README holds them as sections 3 and 4, in the correct order.

### Defect 3 and the student image list
The student image list shows:

| Repository | Tag | IMAGE ID | Size |
|---|---|---|---|
| ypan69/my_app | v2 | `506aa9262ed6` | 356.41 MB |
| ypan69/my_db | v2 | `506aa9262ed6` | 356.41 MB |

`ypan69/my_db:v2` carries the IMAGE ID of the web image. One wrong `docker tag`
command caused it. The handout now tells a student to run `docker images` and to
compare the IDs before the push. The README repeats the check at the build step
and at the push step, and the trouble table names the symptom.

### The repair method for the handout
`word/document.xml` holds 172 paragraphs. Each target paragraph holds one
`<w:t>` element, so a text replacement is safe. The script:
- deletes the paragraph of the misplaced pull;
- rewrites two paragraphs;
- clones the third outline item, strips `w14:paraId` and `w14:textId` from the
  clone, and sets the Compose text;
- rebuilds the ZIP, and copies every other part byte for byte.

## Results
- The repaired handout holds 172 paragraphs, the same count, because one
  paragraph goes and one arrives.
- The outline now reads "4 main parts", and the fourth is Docker Compose.
- The Recording list now reads Build, Push, Pull, in that order.
- LibreOffice converts the repaired handout to a 323 KB PDF, so the file is not
  corrupt.
- The safety grep on `assignment-1/` is clean: no home path, no user name, no
  `.ssh`, no key, no token, no `nano`.
- `git status` shows three modified files, and nothing else.

## Issues / Notes
- **I could not test the Docker commands.** The Docker daemon does not run on
  this machine. The `iputils-ping` fact comes from a web search, and the README
  commands come from the existing files. Run one full pass before class.
- The `compose.yaml` change adds `build: .` to `pink` and `lime`. Without it,
  Compose can try to pull `my_app` from Docker Hub. I did not reproduce that
  failure, so the change is a guard, not a proven fix.
- `app.py` holds the default password `passwors`, which is a typo. I did not
  change it, because a student always sets `DBPWD`. The README now says to set
  it every time.
- `mysql.sql` inserts two rows that both carry `emp_id` `1`. It is course data,
  and it breaks nothing. I did not change it.
- The user committed `assignment-2` as `39a43b1`. I did not push anything.
