# Report: Assignment 2 analysed, updated and moved into the Fall 2026 repo
**Date**: 2026-10-14
**Sequence**: #03 for the day

## Summary
I compared the Summer 2026 Assignment 2 starter against the Fall 2026 labs. The
assignment targets a **kind** cluster. The Fall labs build a **real kubeadm
cluster on EC2**. No lab in the Fall repository uses kind. That one mismatch
breaks the whole deployment section. I found 8 defects in total, corrected them,
and put the result in the Fall repository as `assignment-2/`. I did not commit
and I did not push.

## What Changed
- Created `/Users/maziar/Documents/c/r/a2_test/CLO835_Fall_2026/assignment-2/`,
  19 files. The folder is untracked; `git status` shows `?? assignment-2/`.
- The source repository `CLO835_summer2026_assignment2` is **not** changed.
- Created `reports/report-2026-10-14-03-assignment2-fall-alignment.md`.

## Technical Details

### The comparison
| | Summer assignment | Fall labs |
|---|---|---|
| Cluster | kind, on the laptop | kubeadm, 1 control plane + 2 workers on EC2 |
| Kubernetes | not stated | v1.35, Flannel |
| Reach the app | port forward | NodePort 30000-32767, open to the internet |
| Image registry | Docker Hub | Docker Hub, taught in Week 02 Step 5 |
| Build platform | not stated | the nodes are x86_64 |

Evidence: `grep -rn "kind create\|kind load\|kindest" Week0* assignment-1`
returns nothing. `Week05/main.tf` opens 30000-32767 and outputs `nodeport_url`.
`Week05/bootstrap.sh` installs Kubernetes v1.35.

### The 8 defects
1. **The cluster is wrong.** The README said "deployed to your kind Kubernetes
   cluster" twice. Replaced with the Week 05 kubeadm cluster, and the Terraform
   commands that build it.
2. **No way to reach the app.** A kind cluster needs a port forward. The Fall
   cluster answers on a node port. The README now pins `nodePort: 30000` and
   tells the student to open all three public addresses, as Week 05 Step 12 does.
3. **The pipeline could not run.** GitHub names a new repository's first branch
   `main`. The workflow listened on `master` only. It now listens on both.
4. **The CPU trap was absent.** The nodes are x86_64, and a Mac with Apple
   Silicon builds arm64. Week 02 Step 5 teaches this. The README and the
   Dockerfile now carry the warning and the `--platform linux/amd64` flag.
5. **A dead link.** The README pointed at the Summer assignment 1 repository. It
   now points at `../assignment-1` in the same repository.
6. **The Rust starter had no probe paths.** The other five starters answer
   `/healthz` and `/readyz`, and the README offers bonus probes. The Rust file
   answered the message on every path. I added the two paths, and tested it.
7. **The report was mandatory but had no template.** Added `report.md`.
8. **A wrong path in `.gitignore`.** `/go/server` ignores nothing. Corrected to
   `apps/go/server`.

I also removed the version numbers from the language table and from the file
headers ("Python 3.14 starter", "Go 1.26 starter"). They go stale, and the
starters do not depend on them. I removed the "Star + Watch this repo" line,
because the folder is no longer a separate repository.

### A trap that the move creates
GitHub reads a workflow only from `.github/workflows/` at the **root** of a
repository. Inside `assignment-2/` the workflow is inert, which is safe for the
course repository. A student must copy the folder contents to the root of their
own repository. The README now says this, and the trouble table repeats it.

### What I did NOT change
The teaching design is correct for this course and is left alone:
- two versions, 0.2 and 0.3, with the student ID in 0.3;
- three replicas;
- `kubectl set image`, `rollout status`, `rollout history`, `rollout undo`;
- six languages, one choice;
- every answer left as a `TODO`.

Week 05 teaches rollout and rollback in the lab. Week 06 teaches Services and
Deployments in the lecture. Assignment 2 is released in Week 5 and is due in
Week 8, so every command it needs is taught before the due date.

## Results
I ran five of the six starters and called all three paths on each.

| Starter | `GET /` | `/healthz` | `/readyz` |
|---|---|---|---|
| Python 3.14.8 | correct | 200 | 200 |
| Node.js v26.10 | correct | 200 | 200 |
| Go 1.26.3 | correct | 200 | 200 |
| Java 27 | correct | 200 | 200 |
| Rust 1.96 (after my fix) | correct | 200 | 200 |

C# is not tested. The `dotnet` command is not on this machine.

Public-repository safety check on the new folder: no home path, no user name, no
`.ssh` path, no key, no password, no token, and no use of `nano`.

## Issues / Notes
- **Nothing is committed and nothing is pushed.** The folder is untracked.
- I did not write a grade breakdown. I do not have the official one, so the
  README points at the handout on Blackboard.
- The Summer repository keeps its own history. The copy carries no git history.
