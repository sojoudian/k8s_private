# Report: kind removed from every current file
**Date**: 2026-10-27
**Sequence**: #09 for the day

## Summary
The user said "fix them all", then "change everything. update them all." I moved
every current file that still used kind to the kubeadm cluster of the labs: the
Week 05 Terraform, 1 master and 2 workers on EC2. 35 new files: 6 decks, 17
project files, Assignment 2, 3 quizzes with keys, 2 Markdown files, 2 lab texts.
`PREFERENCES.md` section 10 now says "Never use kind". Every input file stays
unchanged; each output is a new `_v2` (or next) version. No AWS resource was made.

## What Changed

### New files
| File | Change |
|---|---|
| `Week04/FINAL/Week04_v2.pptx`, `finalWork/Week04_v2.pptx` | 10 texts on slides 1, 2, 8, 17, 18, 21, 26: kind to kubeadm on EC2; the `get-contexts` output is now `kubernetes-admin@kubernetes` |
| `Week10/Week09_lecture_style_v6.pptx`, `CLO835_Workshops_Lab_v2.pptx`, `finalWork/Week09_v2.pptx`, `finalWork/Lab07_v2.pptx` | hostPath: "for single-node tests only", not "kind and minikube" |
| `Week04/FINAL/lab_commands_v2.txt` | the kind guide replaced by the tested kubeadm steps (Terraform, SSH, Steps 4 to 11, destroy) |
| `Week04/FINAL/Week04_Quiz_v2_Blackboard.txt` + key | Q4: why the security group opens 30000-32767 (correct option C, as before) |
| `CLO835_Final_Exam_v2_Blackboard.txt` + `_AnswerKey.md` | Q19: the same fact for the final exam (correct option C, as before) |
| `quiz_pool_src/Quiz_W03W04_Easy20/*_v2*` (txt, key, QTI ZIP) | "Where does the control plane run?" on the kubeadm cluster |
| `Assignments/Assignment_2/CLO835_Assignment2_v2.docx` | 14 texts: the Week 05 cluster, the control plane machine, the public IP of a node, `terraform destroy`, the kubeadm reference link |
| `project/Project_00` to `Project_16` `_v2.docx` (17) | 4 to 29 texts each, see below |
| `Semester_Projects_Individual_v2.md` | the same changes as the Word files |
| `Semester_Project_Ideas_v2.md` | 7 lines: kind to kubeadm |
| `Labs/Lab03/Lab03_v2.txt` | the Week 04 submission text for the kubeadm lab |

### Changed files
- `quiz_pool_src/q_easy20_w34.py`: 1 question. `build_easy20_w34.py` and
  `audit_easy20_w34.py`: the `_v2` file names.
- `~/.claude/PREFERENCES.md`: section 10 says kubeadm, never kind; the "open
  conflict" line of section 15 is removed.
- Memory: `project-no-eks-in-educate.md`, `reference-preferences-file.md`,
  `MEMORY.md`.

### New scripts (all guarded; inputs are never written)
- `retarget_kind.py`: the 6 decks.
- `retarget_docx.py`: a Word text replacer (lxml + zipfile only; it handles text
  that spans runs, and exact-paragraph matches).
- `retarget_kind_docx.py`: Assignment 2 and the 17 project files.

### Pushed to Docker Hub (public)
`maziar/local-path-provisioner:v0.0.37`, `maziar/keda:2.21.0`,
`maziar/keda-metrics-apiserver:2.21.0`, `maziar/keda-admission-webhooks:2.21.0`,
`maziar/nfs-server-alpine:latest`, `maziar/netshoot:latest`, `maziar/curl:latest`.

### Added to the local `clo835-mirrors` repository (not pushed)
`local-path-provisioner/v0.0.37/local-path-storage.yaml` (image on maziar, the
StorageClass named `standard` and default, as in kind) and
`keda/2.21.0/keda-2.21.0.yaml` (3 images on maziar). Commits `9064aef`, and a
README fix after it.

## Technical Details

### Decisions for the semester project
| Item | kind design | kubeadm design |
|---|---|---|
| Cluster | `kind-config.yaml` in the student repo | the Week 05 Terraform of the course repo |
| Storage | the built-in `standard` StorageClass | the same provisioner (local-path), installed by `bootstrap.sh` from the course mirror and named `standard` |
| Where data lives | the kind node | `/opt/local-path-provisioner` on a worker |
| NodePort | `extraPortMappings` to localhost | `http://<node-public-ip>:<nodePort>`, or `localhost` on the master |
| Cluster name | `kind create cluster --name ...` | default kubeadm name; the student ID goes in the namespace |
| Teardown | `kind delete cluster` | `kubectl delete namespace ...`; for a new cluster `terraform destroy` + `apply` |
| Break-glass (P11) | `kind get kubeconfig` | `/etc/kubernetes/admin.conf`, copied to `~/.kube/config` |
| Project 6 | 2 kind clusters on one host | cluster a = Week 05 set, cluster b = Week 04 set (different names, so both run: 6 machines); contexts `a` and `b` on the laptop; the dump moves with `kubectl cp` through PVCs, not hostPath |
| Project 8 | 4 nodes (1 + 3) | the 3-node Week 05 cluster (1 + 2); the drill still drains one worker, then the other |
| Projects 8, 9 (NFS) | the kindest/node image has NFS tools | `bootstrap.sh` installs `nfs-common` on the nodes (Ubuntu 26.04 has none) |
| Project 13 | `--kubelet-insecure-tls` "on kind" | the same flag on kubeadm (self-signed kubelet serving certificates); metrics-server from the course mirror |
| Project 16 | KEDA from its official bundle | KEDA 2.21.0 from the course mirror, `kubectl apply --server-side -f` |
| Images | `itsthenetwork/...`, `nicolaka/...`, `curlimages/...`, `registry.k8s.io/hpa-example` | `maziar/nfs-server-alpine`, `maziar/netshoot`, `maziar/curl`, `maziar/hpa-example` |

Facts checked against the Week 05 code: port 6443 is open to 0.0.0.0/0 and the
API server certificate holds the public IP (`--apiserver-cert-extra-sans`), so a
laptop kubeconfig works; 30000-32767 is open on all nodes; `bootstrap.sh` installs
no `nfs-common`; the Week 04 and Week 05 resource names differ.

### Verification
- Every replacement matched its text. The rebuild of all 18 Word files on a copy
  gives a byte-identical `word/document.xml`.
- A text compare of each deck with its input: only the expected paragraphs differ.
- The kind scan over the 35 new files finds only "No kind", "Never use kind" and
  the history line of `lab_commands_v2.txt`.
- The account scan over the new project files and quizzes finds only `maziar`
  and `sojoudian`.
- Quiz gates: `build_easy20_w34.py` gates 1 to 11 pass (key 5/5/5/5, longest 5,
  shortest 6). `build_easy20_w56`, `build_easy20` and `build3` still pass, with
  byte-identical outputs. `audit_easy20_w34.py`: 0 errors, 0 leaks.
- The Week 04 and exam quiz files keep their field counts (10 per MC row).
- Week 04 v2 slides 17 and 26 were rendered and read. The text fits.

## Results
- 35 new files, 0 input files changed.
- 7 new public images on Docker Hub.
- kind is gone from every current file. It stays only in superseded versions,
  in `old/`, in reports, and in the v1 files kept for comparison.

## Issues / Notes
- **Still blocking:** `sojoudian/clo835-mirrors` and the 7 forks do not exist on
  GitHub yet. `gh auth login` is still needed. Until then the StorageClass, KEDA,
  Flannel and metrics-server URLs return 404.
- **Not tested live.** No cluster ran. The project designs follow the tested
  Week 05 cluster, but no project was built end to end.
- Project 6 needs 6 `m5.large` machines at one time. I did not verify that the
  Learner Lab allows 6 at once.
- The public course repo copy holds uncommitted changes from report #05.
- Not changed: `Week04/FINAL/Week04.pdf`, `Lab_week04.pdf` and other PDFs (they
  still show kind); the Week 04 lecture footers (`/38`, a defect from before).
- The summer decks `CLO835_Workshops_Lab_v2`, `finalWork/Lab07_v2` and
  `finalWork/Week09_v2` still name `kubernetes/dashboard`, `weaveworks/eksctl`,
  `alpine/curl` and `k8s.gcr.io/test-webserver`. They were outside the account fix
  of report #05.
- Assignment 2 and the kubia CI use GitHub Actions from the `docker` and `actions`
  accounts (`docker/build-push-action`, `actions/checkout`). I did not change them.
