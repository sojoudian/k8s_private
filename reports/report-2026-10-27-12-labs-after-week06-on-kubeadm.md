# Report: Labs After Week 06 Rebuilt on the kubeadm Cluster
**Date**: 2026-10-27
**Sequence**: #12 for the day

## Summary
This work rebuilds the six labs after Week 06 (Weeks 07, 09, 10, 12, 13 and 14) on the kubeadm cluster of Weeks 04 to 06. Each lab now matches its lecture. Each lab uses the design and the engine of the Week 05 and Week 06 labs. Each lab has a deck, a PDF, a `localMachine.sh` file, a Blackboard submission file and an 8-file folder in the course repository. No lab uses EKS, Cloud9, IAM users, IAM roles or kind. No live AWS test was done. Nothing was committed or pushed.

## What Changed
New builders in `/Users/maziar/Downloads/k8s_week3/`:
- `lab_kubeadm.py`: the shared helper. `make_lab()` builds the deck and the script from one slide list. `make_repo_folder()` writes the 8 repository files from the tested `Week06` folder. `blackboard_text()` writes the submission file. `check_lines()` stops the build if a command holds a non-ASCII character.
- `build_week07_lab_v1.py`, `build_week09_lab_v1.py`, `build_week10_lab_v1.py`, `build_week12_lab_v1.py`, `build_week13_lab_v1.py`, `build_week14_lab_v1.py`. Each builder is guarded. Import writes nothing.

New lab files (decks, PDFs, scripts, submission files):

| Week | Deck | Slides | Steps | Workshops |
|---|---|---|---|---|
| 07 | `Week07/Lab_week07_v1.pptx` + `.pdf` | 22 | 10 | emptyDir, gitRepo replaced by an init container, hostPath, local-path StorageClass and PVC, NFS |
| 09 | `Week09/Lab_week09_v1.pptx` + `.pdf` | 19 | 11 | static Pods, etcdctl, stop the scheduler, kubeadm certs and upgrade plan, join token, drain, Flannel vs VPC CNI, private 6443, auth whoami, Terraform state |
| 10 | `Week10/Lab_week10_v1.pptx` + `.pdf` | 27 | 17 | mongo on hostPath, static PV and PVC (Retain), StorageClass `fast`, StatefulSet `maziar/kubia-pet`, headless Service, kubectl proxy, SRV records, `maziar/kubia-pet-peers` |
| 12 | `Week12/Lab_week12_v1.pptx` + `.pdf` | 25 | 15 | command and args, env, ConfigMaps (literal, file, declarative, envFrom, key, volume, dev and prod), Secrets (imperative, declarative, key, tmpfs volume, env risk, projected token, plain text in etcd) |
| 13 | `week13/Lab_week13_v1.pptx` + `.pdf` | 22 | 12 | certificate user `dev-user` by CSR, API groups, ServiceAccount token with curl, Role and RoleBinding, can-i, ClusterRole `pv-reader`, default roles, `super-admin.conf` |
| 14 | `week14/Lab_week14_v1.pptx` + `.pdf` | 18 | 10 | kubeconfig (view, get-contexts, current-context, set-credentials, set-context, use-context, `--current`, `--minify --flatten`, KUBECONFIG merge); HPA (metrics-server, `maziar/hpa-example`, autoscaling/v2, load generator, replica calculation); optional: a Pod gets LabRole from its node, which is why IRSA exists |

Each week folder also has `localMachine_v1.sh` and `Lab_weekNN_Blackboard_Submission.md`.

New folders in the course repository clone `~/Documents/c/r/CLO835_Fall_2026` (not committed):
- `Week07/`, `Week09/`, `Week10/`, `Week12/`, `Week13/`, `Week14/`. Each folder has `.gitignore`, `bootstrap.sh`, `cleanup_labNN.sh`, `localMachine.sh`, `main.tf`, `master-init.sh.tftpl`, `variables.tf` and `worker-join.sh.tftpl`.
- `Week07/master-init.sh.tftpl` installs `nfs-kernel-server` and exports `/srv/nfs`. `Week07/bootstrap.sh` adds `nfs-common` on every node.

## Technical Details
- The six labs use the engine of `build_week06_lab_v3.py`. The prerequisites slide says "Lab N - Prerequisites". The cluster slide says `cd CLO835_Fall_2026/WeekNN`.
- One slide list makes the deck AND `localMachine.sh`. Thus the slides and the script cannot differ.
- Every repository folder comes from the tested `Week06` folder. Only the week name, the token `weekNN.0123456789abcdef`, the message of the day, the cleanup script and the extras of the week change. `main.tf` keeps port 6443 closed to the internet.
- The students have no EKS. Each EKS topic of a lecture becomes its kubeadm equivalent:
  - Managed control plane: static Pods, etcd, the scheduler, kubeadm certs and upgrades (Week 09).
  - Managed node group: join token, cordon and drain (Week 09).
  - IAM users and aws-auth: certificate users by CSR and RBAC (Weeks 13 and 14).
  - IRSA: an optional workshop shows that every Pod gets LabRole from IMDS (Week 14). It needs no IAM change.
  - EBS StorageClass: the local-path provisioner from the course mirror (Weeks 07 and 10).
- Week 14 patches metrics-server with `--kubelet-insecure-tls`, because a kubeadm kubelet serves a self-signed certificate.
- Week 14 Workshop 3 works because `main.tf` sets `iam_instance_profile = var.lab_instance_profile` and an IMDS hop limit of 2.
- Week 13 uses the lecture developer Role with the correct resource `configmaps`.

## Results
Checks (all on the files above):
- Deck audit: 6 of 6 decks are 16:9, 0 hidden slides, 0 float coordinates, all footers `n / total`, 2 typefaces (Calibri, Consolas).
- Render: Week 14 rendered to PNG and read slide by slide. No overflow. The other 5 decks were rendered the same way when they were built.
- PDFs: 22, 19, 27, 25, 22 and 18 pages. The page counts agree with the slide counts.
- Accounts: only Docker Hub `maziar` and GitHub `sojoudian`, plus Docker official images (nginx, mongo, redis, busybox, ubuntu).
- Image tags: 14 of 14 `maziar/*` tags return HTTP 200 on Docker Hub, including `aws-cli`, `hpa-example`, `kubia-pet`, `kubia-pet-peers` and `metrics-server:v0.7.1`.
- kind: 0 uses. The only hit is the inherited cluster-slide line "No kind. No Docker in Docker."
- `bash -n`: all scripts in the 6 folders pass.
- Non-ASCII characters in the 6 folders: 0.
- YAML: 30 here-doc manifests parse, and each has `apiVersion` and `kind`.
- Terraform: `fmt -check` and `validate` pass in scratch copies of all 6 folders.
- Templates: `master-init.sh.tftpl` and `worker-join.sh.tftpl` render with `templatefile()` in all 6 folders. The only template variable in `master-init` is `${k8s_token}`.
- Private data: 0 hits for the home IP, `/Users/`, `.ssh/`, the key name or the e-mail address in the 6 folders, in Weeks 03 to 06 and in the 6 decks.
- No local port was used. No AWS resource was created.

## Issues / Notes
- **The labs do not work until two GitHub items exist.** Both URLs return HTTP 404 now:
  - `sojoudian/clo835-mirrors`: the Flannel, metrics-server, local-path and KEDA files. The local repository is ready in the scratchpad. `gh` is not logged in.
  - The fork `sojoudian/kubia-website-example` (Week 07 init container).
- **Not live-tested.** The checks are static. Only Weeks 04 to 06 ran on AWS.
- **Do not commit `Week06/apply.log`.** It is untracked, it is not git-ignored, and it holds 8 IP addresses from the test of today. The test infrastructure is destroyed: the state holds 0 resources.
- The course repository changes are not committed and not pushed. The verified Assignment 1 repair is still only in the `a2_test` clone.
- Labels: the lab prerequisites use the course week (Lab 7, 9, 10, 12, 13, 14). Some lecture covers still say Week 8, 10, 11 or 12. A relabel needs the approval of the user.
- Lecture defects found and not changed:
  - Week 12 lecture slides 16 and 17 show the old ServiceAccount token Secret. Since Kubernetes 1.24, the token is projected. The lab teaches the projected token.
  - The Week 13 lecture developer Role writes `ConfigMap`. RBAC needs the plural `configmaps`.
  - Week 07 lecture slide 12 holds a stray item.
- The old lab decks (for example `week14/Week14_lab_style_v11.pptx`) stay in place. The new decks do not overwrite them.
