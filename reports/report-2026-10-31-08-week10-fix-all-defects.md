# Report: Week 10, fix of all audit defects and live test

**Date**: 2026-10-31
**Sequence**: #08 for the day

## Summary
I fixed all 25 defects of report #07: 18 in the lecture and 7 in the lab. The lecture is now
v8 and the lab is now v3. The lab passes a new live test on AWS: 37 commands, 2 full passes,
0 non-zero exits, and all 15 resources destroyed. One item is open: the fix is not pushed,
so GitHub still holds lab v2. The push needs your clear yes.

## What Changed

**Created**
- `build_week10_lecture_v8.py`, `Week10/Lecture_week10_v8.pptx` and `.pdf`.
- `build_week10_lab_v3.py`, `Week10/Lab_week10_v3.pptx` and `.pdf`, `Week10/localMachine_v3.sh`.
- `Week10/Lab_week10_Blackboard_Submission_v3.md`, in the form of your `Lab04` item.

**Changed**
- `build_week09.py`: added the `__main__` guard.
- `~/Documents/c/r/CLO835_Fall_2026/Week10`, not committed: `localMachine.sh`,
  `cleanup_lab10.sh`, `master-init.sh.tftpl`. `local-path-storage.yaml` is deleted.
- Memory: `project-week10-deck.md`, `project-short-labs-2026-10-27.md`, `MEMORY.md`.

Earlier versions stay as they are.

## Lecture fixes

| No | Fix |
|---|---|
| L1 | Slide 3: "Week 9: K8s – PVs & K8s in EKS". |
| L2 | Slide 3: "Week 13: K8s – RBAC and EKS". |
| L3 | Slide 3: "Week 8: Study Week". |
| L4 | The file is `Lecture_week10_v8.pptx`. |
| L5 | Slide 8 uses an `nfs` volume, and a new bullet says that EBS needs a PV and the CSI driver. Slide 14 uses a `csi` block with `ebs.csi.aws.com`. |
| L6 | Slides 11 and 19 use `ebs.csi.aws.com`. Slide 16 is a new diagram with no GCE. |
| L7 | Slide 15 uses `maziar/kubia:v1`. The names are now `kubia-pv`, `kubia-pvc` and `kubia-pod`. |
| L8 | Slide 24: the new Pod keeps its name, DNS name and data. Its IP address can change. |
| L9 | Slide 25: the name of a headless Service returns all the Pods. |
| L10 | Slide 24: "StatefulSets vs ReplicaSets", and "anew" is gone. |
| L11 | 10 native diagrams and 1 native warning card replace the 11 images. |
| L12 | 0.20 MB. |
| L13, L14 | The images are gone, so no image is below 110 DPI or in a band. |
| L15 | Slide 27 holds the tested lab commands, with `nslookup -type=SRV`. |
| L16 | Slide 7 uses `type: DirectoryOrCreate`. |
| L17 | 12 slides are in ASD-STE100, with one spelling: StatefulSet, Pod. |
| L18 | All titles are 32 pt, and dividers keep 40 pt. All have one style. |

## Lab fixes

| No | Fix |
|---|---|
| A1 | "Lab Week 10 - Prerequisites", and the same label in the cleanup headers. |
| A2 | The sample says `v1.35.10`. |
| A3 | `maziar/alpine-curl` replaces both `busybox` images. No new image was needed. |
| A4 | Step 5 adds 2 commands: the name of the Service, and `nslookup -type=SRV`. |
| A5 | The folder has 8 files. `master-init.sh.tftpl` writes the manifest to the master. |
| A6 | The Blackboard text has the long form, with 7 sections and no pledge. |
| A7 | New live test, below. |

## Live test
- Account `499333804030`, `us-east-1`, key pair `Maziar`. Student prompts for `key_name` and `yes`.
- `terraform apply`: 15 added. All 3 nodes Ready about 2 minutes after the start.
- Kubernetes v1.35.10. `cloud-init` shows `errors: []`.
- `cleanup_lab10.sh` on the master equals the repository file.
- The master holds `local-path-storage.yaml`, and the manifest has 2 `maziar` images.
- Pass 1 and pass 2: 37 commands each, 0 non-zero exits.
- `terraform destroy`: 15 destroyed. After it: 0 instances and 0 `week10` security groups.

**Results that prove the new text**
- After the delete, `kubia-0` kept its name and data, and its IP changed from 10.244.2.5 to 10.244.2.6.
- `nslookup` on the Service name returned both Pod addresses.
- `nslookup -type=SRV` returned `kubia-0.kubia...` and `kubia-1.kubia...`, port 8080.
- The helper Pods created and deleted the volumes with the new image.
- After each clean-up: no PV, PVC, StorageClass, provisioner namespace, ClusterRole or proxy.

**Lecture manifests**
- All 8 pass `kubectl apply --dry-run=server` on the cluster.
- `test-pd.yaml` ran for real, and the Pod reached Running with no `/data` on the node.
- The manifests with `ebs.csi.aws.com` did not create a volume, because the cluster has no EBS driver.

## Results

| Check | Lecture v8 | Lab v3 |
|---|---|---|
| Slides, footers | 28, `N / 28` | 10, `N / 10` |
| Size | 0.20 MB | 0.07 MB |
| Fonts | Calibri, Consolas | Calibri, Consolas |
| Float coordinates, shapes off the canvas | 0, 0 | 0, 0 |
| Duplicate titles | 0 | 0 |
| Images | Logo and whale only | Whale only |

- Every changed lecture slide was rendered and viewed.
- `bash -n` and `terraform fmt -check` pass. The scan for `/Users/`, `.ssh/`, the user name,
  `luksa`, `busybox` and an AWS key finds 0.
- No server started on this computer, so no port is used.

## Issues / Notes
- **Push: done by you.** Commit `dd284ce` (02:08) put lab v3 on GitHub. Later, I ran the slide 3
  command on a clone at `ff69e05`: `git pull` gave lab v3, with the same 8 files as the live test.
- **Recovery test: partial.** My harness took the wrong lines for the StatefulSet, so the
  half-way test ran with the provisioner and the Service only. The clean-up passed. Each pass
  also ran the clean-up with the pets up and the proxy on, so that state has a test.
- Slide 8 keeps your hand position (x = 0.01), so its bullets start at the slide edge.
- Slide 27 no longer shows `dig`, because `nslookup -type=SRV` needs no package.
- The Week 09 lecture outline still says "Storage classes & Statefulsets".
- Weeks 07 and 14 still name `busybox`. They are outside this work.
- The Blackboard name of this lab is your decision.
