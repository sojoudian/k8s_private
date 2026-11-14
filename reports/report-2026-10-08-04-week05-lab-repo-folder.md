# Report: Week 05 Lab Folder, Built in the Week 04 Style
**Date**: 2026-10-08
**Sequence**: #04 for the day

## Summary
`CLO835_Fall_2026/Week05/` is created. It holds the same eight files as
`Week04/`, with the same names, the same order and the same wording. Only the
week number and the lab content differ. The 14 steps of `localMachine.sh` match
the 14 lab slides of `Lab_week05_v4.pptx`. Nothing is committed or pushed.

## What Changed

### New folder: `~/Documents/c/r/Oct08/CLO835_Fall_2026/Week05/`
| File | How it was made |
|------|-----------------|
| `.gitignore` | Copied from Week 04, byte-identical |
| `variables.tf` | Copied from Week 04, byte-identical |
| `main.tf` | Copied from Week 04. Only `week04` becomes `week05` in the two security group names, the two tag names and the kubeadm token. |
| `bootstrap.sh` | Copied from Week 04. Only the header line names Week 05. |
| `master-init.sh.tftpl` | Copied from Week 04. The MOTD names Week 05 and points at `localMachine.sh`. |
| `worker-join.sh.tftpl` | Copied from Week 04. The MOTD names Week 05. |
| `localMachine.sh` | NEW. 14 steps, written in the Week 04 banner style. |
| `cleanup_lab05.sh` | NEW. Same shape as `cleanup_lab04.sh`, with the Week 05 objects. |

No README is added, because Week 04 has none.

## Technical Details

### The style that was copied
- The same eight file names, with `04` replaced by `05`.
- The same section banner: a row of hashes, `# Step N - lower case title`, a row
  of hashes.
- The same comment voice: say WHY, not only what.
- The same ending: `localMachine.sh` finishes by calling the cleanup script.
- `variables.tf` carries `key_name` and `lab_instance_profile` only. Week 04 has
  no `ssh_cidr`, so Week 05 has none either.
- The infrastructure is unchanged: Ubuntu 26.04, `m5.large`, one subnet in a zone
  that offers it, 1 master and 2 workers, the MTU 1500 fix, Kubernetes v1.35,
  Flannel, and NodePort 30000-32767 open on both security groups.

### The lab content, from the Week 05 lecture
Each step names the slide it belongs to.

| Step | Slide | Subject |
|---|---|---|
| 0 | 3 | Check the cluster |
| 1 | 4 | Your first Pod, and a port forward |
| 2 | 5 | A Pod from a manifest, and `kubectl explain` |
| 3 | 6 | Two containers in one Pod |
| 4 | 7 | Logs, and `-c` to pick a container |
| 5 | 8 | Labels and selectors |
| 6 | 9 | A Pod does not scale, a Deployment does |
| 7 | 10 | A ReplicaSet from a descriptor |
| 8 | 11 | Scaling |
| 9 | 12, 13 | Roll forward |
| 10 | 14 | Roll back |
| 11 | 15 | Resilience |
| 12 | 16 | Reach a Pod from your browser on NodePort 30000 |
| 13 | 17 | Clean up |

`sidecar.yaml` and `rs.yaml` are written by a heredoc inside the script, exactly
as the slides show. No extra file is shipped, so the folder keeps the Week 04
shape.

## Results
- The file set is identical to Week 04, apart from the week number.
- `terraform init`, `terraform validate` and `terraform fmt -check` all pass.
- `bash -n` passes on all three shell files.
- 0 non-ASCII bytes in any `.sh`, `.tf` or `.tftpl` file.
- No home IP, no `~/.ssh` path, no AWS key.
- Every `kubectl` verb that appears on a slide exists in `localMachine.sh`:
  `apply, create, delete, explain, expose, get, label, logs, patch,
  port-forward, rollout, run, scale, set`.
- `git status` shows `?? Week05/`. Nothing is staged, committed or pushed.

## Issues / Notes
- The lab was not launched on AWS. No credentials are available.
- The deck that goes with this folder is
  `~/Downloads/k8s_week3/Week05/Lab_week05_v4.pptx`.
