# Report: Test of the Week 10 lab in the course repository
**Date**: 2026-11-10
**Sequence**: #06 for the day

## Summary
The user asked to test the Week 10 lab of `~/Documents/c/r/CLO835_Fall_2026/Week10` and to confirm that it works 100 %. I could not run a new live test. The auto mode classifier denied `terraform apply` ("Protected-Scope IaC Apply"), so I created no AWS resource. All checks that need no new resource pass. The 40 master commands of the repo are byte-equal to the commands that passed live pass 3 today at 19:25 (40 of 40 exit 0). The boot files differ from the tested files by one comment line only. So a new live run is the only check that is not done.

## What Changed
- Created this report.
- No project file and no repo file changed.
- Sandbox only: a copy of the Week10 folder (`terraform init`, `validate`, `plan`), two clones of the public repository, and the runner scripts. Folder: `/private/tmp/claude-501/-Users-maziar-Downloads-k8s-week3/4607d34d-8f32-4600-8c64-da86808c91b9/scratchpad/w10live`.
- AWS: only read calls (`sts get-caller-identity`, `describe-instances`, `describe-security-groups`, and the data sources of `terraform plan`). No resource was created.

## Technical Details

### 1. The denied step
- Command: `(sleep 10; echo Maziar; sleep 40; echo yes) | terraform -chdir=<sandbox> apply`.
- Result: "Permission for this action was denied by the Claude Code auto mode classifier. Reason: [Protected-Scope IaC Apply]."
- I did not try a different way to create the cluster.
- Account state at the time: 3 running `m5.large` instances of a Week 12 cluster (`week12-k8s-*`), from session `4b692c4c`. I did not touch them.

### 2. Static checks of the repo folder (all pass)

| Check | Result |
|---|---|
| Files | 8: `.gitignore`, `bootstrap.sh`, `cleanup_lab10.sh`, `localMachine.sh`, `main.tf`, `master-init.sh.tftpl`, `variables.tf`, `worker-join.sh.tftpl` |
| `localMachine.sh` against `Week10/localMachine_v4.sh` | equal |
| Master commands (`tools/instrument.py`) | 40: Step 0 2, Step 1 5, Step 2 12, Step 3 3, Step 4 5, Step 5 11, Step 6 2 |
| `bash -n` on the 4 scripts | pass |
| `terraform fmt -check` | pass |
| `terraform validate` (sandbox) | "Success! The configuration is valid." |
| `master-init.sh.tftpl` writes `cleanup_lab10.sh` | yes, equal to the repo file |
| Message of the day | names Week 10 and `localMachine.sh` |
| `variables.tf` | `key_name` has no default; `lab_instance_profile` = `LabInstanceProfile` |
| Cleanup removes the lab files | `pv-pvc.yaml`, `writer.yaml`, `kubia-statefulset.yaml` |
| Private-data scan | 0 hits (`/Users/`, `.ssh/`, `mazSeneca`, the email, AWS keys, private keys) |
| Docker Hub tags | `maziar/alpine-curl:latest`, `maziar/kubia-pet:latest`, `maziar/local-path-provisioner:v0.0.37`: 200 |
| Flannel manifest URL | 200; images `ghcr.io/flannel-io/flannel:v0.28.10`, `flannel-cni-plugin:v1.9.1-flannel3` |

### 3. `terraform plan` (read-only)
- Exit 0. "Plan: 15 to add, 0 to change, 0 to destroy."
- AMI `ami-0547ecbf0e9b4aeb5`. This is the AMI of the live test of 18:56.
- All three instances use one subnet, `subnet-00d55b9eb7c9414aa`.

### 4. The live test of 18:56 to 20:42 today (session `4b692c4c`)
I read its logs in `/private/tmp/claude-501/-Users-maziar-Downloads-k8s-week3/4b692c4c-a5fe-4559-849f-f6432d702f32/scratchpad/w10lab/`.

| Run | Commands | Non-zero exits |
|---|--:|--:|
| `apply.log` | - | "Apply complete! Resources: 15 added" |
| Pass 1, full speed | 40 | 0 |
| Pass 2, 3 s between commands | 40 | 0 |
| Recovery: stop half way, then `cleanup_lab10.sh` | - | the 3 "nothing left" checks (namespace, cluster role, proxy) return 1, as they must |
| Pass 3 | 40 | 0 |
| `destroy.log` | - | "Destroy complete! Resources: 15 destroyed." |

The comparison with the current repo:
- The runner that I made from the current `localMachine.sh` is byte-equal to `pass3.sh` and to `pass4.sh`. The pass 1 and pass 3 runners have the same command list. So all three passes ran the 40 commands of the current repo, with the same manifests.
- The tested Terraform folder is a copy of 18:54. Against the current repo:
  - `main.tf`, `variables.tf`, `bootstrap.sh`, `worker-join.sh.tftpl`, `.gitignore`: equal.
  - `cleanup_lab10.sh` and `master-init.sh.tftpl`: one comment line differs ("the pets" became "the StatefulSet Pods").
  - `localMachine.sh`: it was v3 on disk. The passes ran the v4 commands from the runner, so this does not change the result.

Pass 3 output against the comments of the script:
- Nodes: v1.35.10, Ubuntu 26.04.1 LTS, containerd 2.2.2, all Ready.
- `data-pvc` Bound to `data-pv`; `writer` on `workernode1`; the same date after a new Pod; `data-pv` Released after the delete of the claim.
- StorageClass `standard (default)`, `rancher.io/local-path`, Delete, WaitForFirstConsumer.
- `kubia-0` before `kubia-1`; `data-kubia-0` and `data-kubia-1` Bound; new PVs Delete, Bound; `data-pv` Retain, Released.
- POST answer "Data stored on pod kubia-0"; after the delete, "Data stored on this pod: Hello kubia-0".
- DNS: one A record for `kubia-0.kubia`, two for `kubia`, two SRV records (port 8080).
- Cleanup: "No resources found", "done".
- One small difference: the StorageClass sample comment shows 4 columns. The real output also has ALLOWVOLUMEEXPANSION and AGE. The values agree. Report 2026-11-10-03 kept this on purpose.

### 5. GitHub and `git pull`
- The user pushed commit `5f8a655` at 22:49 ("update with week10 and week07"), on top of `ad93eb8`. It changes 7 files in Week07 and Week10.
- A fresh clone: `git pull` exit 0. Its `Week10` folder is equal to the local folder (`diff -rq`: no difference). Its `Week07` folder is also equal.
- A clone set to `ad93eb8`: `git pull` exit 0 (fast-forward to `5f8a655`).
- A clone made before 2026-11-05 20:55 still fails at `git pull` (exit 128, tested in run 12).
- The commit author is `BartyCrouch <sojodyan@gmail.com>`. It has no Claude trailer.

### 6. The Blackboard text v4 against the commands (standard F4)
- Each `Run` and `Show` item of sections 1 to 7 has a command in the script or on lab slide 3 or 9.
- Three items say "display its contents" (`pv-pvc.yaml`, `writer.yaml`, `kubia-statefulset.yaml`). No script command does this. The student must run `cat <file>`. The model texts use the same words.
- The text says "control-plane node" on lines 11, 17, 55 and 104, and "control-plane pods" on line 19 (known defect).

## Results
- Static checks: all pass. `terraform plan`: 15 to add, exit 0.
- The current commands are byte-equal to the commands that passed 3 live passes today. The boot files differ by one comment line.
- GitHub now holds the tested Week 10 lab v4.
- Not done: a new live run on the final files, because `terraform apply` was denied.
- No local server ran, so no port is used.

## Issues / Notes
1. To get a new live test, the user must allow `terraform apply` for this session, or run it with `! <command>`.
2. The Flannel URL uses "latest", and the images `maziar/alpine-curl` and `maziar/kubia-pet` use `latest`. A later change of one of them can change the result of the live test of today.
3. Students with a clone from before 2026-11-05 20:55 stop at `git pull`.
4. The live test of today used the v3 boot file copy. The difference is one comment line, so the boot is the same.
