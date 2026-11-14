# Report: Week 09, fix of all audit defects

**Date**: 2026-10-31
**Sequence**: #03 for the day

## Summary
I fixed all 11 defects of report #02 and the 4 notes of that report. The lecture is now
v6 with 12 slides, and the lab is now v3 with 10 slides. All deck and repository checks
pass. One rule stays open: the 5 new lab commands have no live test, because a live test
creates EC2 machines and needs your approval. Nothing is committed or pushed.

## What Changed

**Created**
- `build_week09_lecture_v6.py`, `Week09/Lecture_week09_v6.pptx` and `.pdf`.
- `build_week09_lab_v3.py`, `Week09/Lab_week09_v3.pptx` and `.pdf`, `Week09/localMachine_v3.sh`.
- `Week09/Lab_week09_Blackboard_Submission_v3.md`, in the long form of `Lab03`.

**Changed**
- `build_week08.py`: added the `__main__` guard.
- `lab_kubeadm.py`: added the optional `prereq_title` and `lab_label`, and made the `chown`
  step conditional. The defaults of the other labs stay the same.
- `~/Documents/c/r/CLO835_Fall_2026/Week09`: `localMachine.sh`, `cleanup_lab09.sh` and
  `master-init.sh.tftpl`. These 3 changes are not committed.
- Memory: `project-week09-deck.md`, `project-short-labs-2026-10-27.md`, `MEMORY.md`.

Earlier versions stay as they are.

## Defects

| No | Fix |
|---|---|
| L1 | Cover says "Week 9 · Lecture". The new file name has no "Week08". |
| L2 | "Week 9: K8s – PVs & K8s in EKS". |
| L3 | "Week 13: K8s – RBAC and EKS". |
| L4 | Slides 5, 7 and 8 are native diagrams in the palette. All 4 images and their parts are gone. |
| L5 | Slide 7 states each step one time, in a flow. The bullet lists are gone. |
| L6 | The 2 dead links are replaced. All 6 links return 200. |
| L7 | New slide 10, "Persistent Volumes on EKS". The reading list now agrees with the lecture. |
| L8 | The bullets are in ASD-STE100. "Master nodes" is now "control plane", and "pod" is now "Pod". |
| L9 | The titles have one style and one size. |
| A1 | Slide 2 says "Lab Week 09 - Prerequisites". The cleanup headers say "Lab Week 09". |
| A2 | The lab now covers the 4 topics and storage, inside Step 0 to Step 6. See the table below. |

| Lecture topic | Lab step | Command |
|---|---|---|
| IAM and RBAC | 4 | `kubectl auth whoami`, `kubectl auth can-i delete nodes` |
| PersistentVolumes on EKS | 4 | `kubectl get csidrivers,storageclass` |
| VPC CNI | 5 | `kubectl get nodes -o wide`, compared with the Pod IP addresses |
| `eksctl` | 6 | `terraform state list` |
| Cost | 6 | A comment line, because no command shows a price |

**Notes of report #02**
- `build_week08.py` has the guard. The import of the module now writes nothing.
- The lecture has a PDF.
- The cards of slides 3, 6 and 11 hold larger text.
- The Blackboard text is in the long form.

## Technical Details
- Facts of slide 10 come from the AWS pages `ebs-csi.html` and `efs-csi.html`: no EBS on
  Fargate, IAM permissions for each driver, the EKS add-on, and EFS on Fargate with no
  driver installation. Week 07 slide 11 keeps the general EBS CSI fact.
- `eksctl` link: I used the `eksctl.io` page. A copy of the repository to `sojoudian` is an
  outward action that you did not ask for.
- The lab adds 5 commands and stays at 10 slides, with 34 commands on the master.

## Results

| Check | Lecture v6 | Lab v3 |
|---|---|---|
| Slides, footers | 12, `N / 12` | 10, `N / 10` |
| Size | 0.17 MB | 0.07 MB |
| Fonts | Calibri, Consolas | Calibri, Consolas |
| Float coordinates, shapes off the canvas | 0, 0 | 0, 0 |
| Duplicate titles or bullets | 0 | 0 |
| Images | Logo and whale only | Whale only |
| Non-ASCII in a command | not applicable | 0 |

- Every slide was rendered and viewed. The render found 2 layout defects, and I fixed them.
- `bash -n` passes on `localMachine.sh`, and the repository file equals `localMachine_v3.sh`.
- The 8 repository files stay, with no README. The scan for `/Users/`, `.ssh/` and the user name finds 0.
- No server started, so no port is used.

## Issues / Notes
- **Live test: not done.** `kubectl auth whoami`, `kubectl auth can-i delete nodes`,
  `kubectl get csidrivers,storageclass`, `kubectl get nodes -o wide` and
  `terraform state list` did not run on the cluster. The comment "No resources found"
  and the address `10.244.x.x` come from the code, not from a run. PREFERENCES section 15 needs this test.
- **Push: not done.** GitHub still holds lab v2 for Week 09.
- You pushed commit `1783b12` at 00:36 on 2026-10-31. It holds Week06 v4 and Weeks 10 to 14.
  So the GitHub warning in report #01 of today no longer applies.
- That commit changed the template, so the repository step stopped one time, as report run 9
  predicted. It wrote nothing before it stopped. The conditional step fixes this.
- The cost in the lab is a comment. The lab cannot show a price, because the pricing API
  is denied in the Learner Lab.
- `Week10/Week09_lecture_style_v7.pptx` is outside this work.
