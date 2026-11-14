# Report: Week 12, fix of all audit defects and live test

**Date**: 2026-10-31
**Sequence**: #10 for the day

## Summary
I fixed all 25 defects of report #09: 19 in the lecture and 6 in the lab. The lecture is now
v4 and the lab is now v3. The lab passes a new live test on AWS: 42 commands, 2 full passes,
and all 15 resources destroyed. The only non-zero exit is the final `grep`, which must find
nothing. The `Week12` folder in the clone is ready for your git step. GitHub still holds lab
v2 until you push.

## What Changed

**Created**
- `build_week12_lecture_v4.py`, `Week12/Lecture_week12_v4.pptx` and `.pdf`.
- `build_week12_lab_v3.py`, `Week12/Lab_week12_v3.pptx` and `.pdf`, `Week12/localMachine_v3.sh`.
- `Week12/Lab_week12_Blackboard_Submission_v3.md`, in the form of your `Lab04` item.
- `fix_outline_week15.py`, `Week09/Lecture_week09_v7.pptx` and `.pdf`,
  `Week10/Lecture_week10_v9.pptx` and `.pdf`. Their outlines now agree with Week 12.

**Changed**
- `build_week09.py` and `build_week08.py`: added the `__main__` guard.
- `lab_kubeadm.py`: added `prereq_title`, `node_version`, `lab_label` and a conditional `chown`.
- `~/Documents/c/r/CLO835_Fall_2026/Week12`, not committed: `localMachine.sh`,
  `cleanup_lab12.sh`, `master-init.sh.tftpl`.
- Memory: `project-week12-deck.md`, `project-week09-deck.md`, `project-week10-deck.md`,
  `project-short-labs-2026-10-27.md`, `clo835-course-schedule.md`, `MEMORY.md`.

Earlier versions stay as they are.

## Lecture fixes

| No | Fix |
|---|---|
| L1 | Slide 1: "Week 12 · Lecture" and "Week 12 feels like 100". |
| L2 | Slide 3: the outline is rebuilt. The red box is the Week 11 exam, and the blue box is Week 12. |
| L3 | Slide 3: "Week 9: K8s – PVs & K8s in EKS", "Week 13: K8s – RBAC and EKS", "Week 8: Study Week". |
| L4 | Slide 3: Week 15 is the project presentation, as you stated. Week 09 v7 and Week 10 v9 now agree. |
| L5 | Slide 7 uses `maziar/fortune:args`, `command: ["sleep"]` and `args: ["3600"]`. |
| L6 | Slides 11 and 15 use `maziar/kubia:v1`. |
| L7 | Slide 10: `--from-literal=APP_MODE=prod`. |
| L8 | Slide 14: the `\` is back, and the command runs. |
| L9 | Slides 13 and 18: the kubelet keeps a Secret in tmpfs on a worker node. etcd stores it on the control-plane disk. |
| L10 | Slides 16 and 17: since v1.24 no token Secret exists. Slide 17 shows the projected volume `kube-api-access`. |
| L11 | Slide 16: the default ServiceAccount has API discovery permissions only. |
| L12 | Slide 16: the output comes from `kubectl get secrets -n week12` and `ls` on the token folder. |
| L13 | Slide 18: the path is gone, and the command uses `kubectl` and the lab Pod `secret-pod`. The bullets have no `#`. |
| L14 | The 3 typing mistakes are gone. |
| L15 | Slides 9, 12, 17 and 20 are native diagrams in the palette. The deck has 0 third-party images. |
| L16 | Slide 21 has 6 links, and all 6 return 200 today. |
| L17 | The bullets are in ASD-STE100, with one spelling: Pod, ConfigMap, etcd. See the exception below. |
| L18 | All titles are 30 pt, on one line, in one style. |
| L19 | Each terminal title names the file or the content. `error_log` is no longer red. |

## Lab fixes

| No | Fix |
|---|---|
| A1 | "Lab Week 12 - Prerequisites", and the same label in the cleanup headers. |
| A2 | The sample says `v1.35.10`. |
| A3 | `maziar/alpine-curl` replaces `busybox:1.36`. No new image was needed. |
| A4 | The lab now practises `--from-file`, `configMapKeyRef`, the declarative `config-dev.yaml`, the second environment `week12-dev`, and the ServiceAccount token folder. |
| A5 | The Blackboard text has the long form, with 7 sections and no pledge. |
| A6 | New live test, below. |

## Live test
- Account `499333804030`, `us-east-1`, key pair `Maziar`. Student prompts for `key_name` and `yes`.
- `terraform apply`: 15 added. All 3 nodes Ready about 2 minutes after the start.
- Kubernetes v1.35.10 on Ubuntu 26.04.1. `cloud-init` shows `errors: []`.
- `cleanup_lab12.sh` on the master equals the repository file.
- Pass 1 and pass 2: 42 commands each. The only non-zero exit is the final `grep week12`.
- `terraform destroy`: 15 destroyed. After it: 0 instances and 0 `week12` security groups.

**Results that prove the new text**
- `args` replaced the CMD: the fortune log wrote every 2 seconds.
- `printenv` gave `hello`, `blue`, `blue`, `prod` in `week12`, and `red`, `dev` in `week12-dev`.
- After the patch and 90 seconds, the file said `green` and the variable still said `blue`.
- `mount` showed `tmpfs on /etc/secret-volume`.
- The token folder holds `ca.crt`, `namespace` and `token`.
- `kubectl get secrets -n week12` showed `app-secret` only.
- The volume is projected from `serviceAccountToken`, the ConfigMap `kube-root-ca.crt`, and `downwardAPI`.
- `kubectl auth can-i` gave `no` for both tests with the default ServiceAccount.
- `etcdctl get` showed `paswrd` in the stored bytes.

**Lecture commands**
- The commands of slides 7, 8, 10, 11, 14, 15 and 16 ran on the cluster, with 0 failures.
- Slide 7 showed `sleep 3600`, slide 8 showed `30`, and slide 11 showed `blue` and `prod`.
- The sample output on slide 16 matches the live output.

**Recovery test**
- I stopped the lab half-way, with 2 namespaces and their objects in place.
- `bash cleanup_lab12.sh` returned 0, and no `week12` namespace stayed.
- After it, the home folder held only `cleanup_lab12.sh` and `run.sh`, which is my test file.

## Results

| Check | Lecture v4 | Lab v3 |
|---|---|---|
| Slides, footers | 21, `N / 21` | 10, `N / 10` |
| Size | 0.18 MB | 0.07 MB |
| Fonts | Calibri, Consolas | Calibri, Consolas |
| Float coordinates, shapes off the canvas | 0, 0 | 0, 0 |
| Duplicate titles | 0 | 0 |
| Images | Logo and whale only | Whale only |

- I viewed every slide of both PDFs as contact sheets, and slides 4, 11, 12, 14, 15 and 16 at full size.
- Slide 12 had `app-config` broken across 2 lines. I fixed the label and rebuilt the deck.
- `localMachine.sh` in the clone equals `Week12/localMachine_v3.sh`.
- `bash -n` and `terraform fmt -check` pass.
- The scan for `/Users/`, `.ssh/`, the user name, `luksa`, `busybox`, `nano` and an AWS key finds 0.
- The folder has 8 files and no Terraform state.
- No server started on this computer, so no port is used.

## Issues / Notes

**Not tested exactly as the slide shows**
- Slide 5, `docker run`: this needs Docker. The cluster nodes do not run it. The same image ran as a Pod.
- Slide 3, `terraform output public_ips` and `private_ips`: I ran `terraform output` and the `-json` form.
  The bare command printed both names.
- Slide 3, `git pull`: this gives lab v3 only after your push.
- The inject blocks of slides 11 and 15 ran in the lab forms, in `config-env.yaml`,
  `config-volume.yaml` and `secret-pod.yaml`. Slide 15 `secretKeyRef` ran in `secret-pod.yaml`.
- Slide 4 shows a sample `nginx.conf`. It holds no command, so I did not run it.

**Open**
- Slide 3 keeps "Week 5: K8s- PODs, ReplicaSets", the same label as Week 10 v9. This is the one place
  in the lecture with `PODs`. A change here alone makes the outlines disagree.
- The outlines of other lectures do not agree with Week 12 on Weeks 14 and 15:
  - Weeks 01, 02, 03: "Week 14 : Project presentation - Helm".
  - Week 06: "Week 14 / HPA & Final Project", "Week 15 / Final Project · Term End".
  - Weeks 13 and 14: "Week 14: Project presentation", and Week 13 also has "Week 14: K8s – HPA".
- The syllabus still says Helm on 12/9.
- Weeks 07 and 14 still name `busybox`. They are outside this work.
- The Blackboard name of this lab is your decision.
