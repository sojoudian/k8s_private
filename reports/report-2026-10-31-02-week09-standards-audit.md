# Report: Week 09 lecture and lab, standards audit

**Date**: 2026-10-31
**Sequence**: #02 for the day

## Summary
The answer is no. The lab is close: it has 2 defects, and all the build and repository
rules pass. The lecture is not final: it has 9 defects, and the worst are the wrong week
on the cover, a broken Course Outline, third-party images and 2 dead links. The audit
is read-only, so I changed no deck, no script and no repository file.

## Scope
I audited the folder `Week09`, which is the class of the week of 10/23:
- Lecture: `Week09/Week08_lecture_style_v5.pptx`, 11 slides, 0.45 MB.
- Lab: `Week09/Lab_week09_v2.pptx`, 10 slides, 0.07 MB.

`Week10/Week09_lecture_style_v7.pptx` has "Week09" in its name, but it belongs to the
class of 11/4. I did not audit it.

## What Changed
- Created this report. Nothing else changed.
- Temporary renders are in the session scratchpad.

## Lecture defects

| No | Slide | Defect | Rule |
|--:|--:|---|---|
| L1 | 1 | The cover says "Week 8 · Lecture". The deck is in `Week09`, and the outline says Week 8 is Study Week. The file name also says Week 08. | Section 14, outline |
| L2 | 2 | "Week 9: K8s- K8s- PVs & K8s in AKS": a doubled word, and AKS is the Azure product. The lecture and the syllabus say EKS. | Section 14, outline |
| L3 | 2 | "Week 13: K8s – RBAC and AKS": the syllabus says Amazon EKS. | Section 14, outline |
| L4 | 5, 7, 8 | The diagrams are third-party images (AWS style), not native house diagrams. Slides 5 and 8 add green and orange outside the palette. | Section 13, section 6 |
| L5 | 7 | The two images repeat the two bullet lists, step for step. | Section 14, one time |
| L6 | 11 | 2 of 6 links return 404: `docs.giantswarm.io/...` and `github.com/sojoudian/eksctl/tree/main/examples`. | Section 14, facts |
| L7 | 11 | 4 of 6 links are about volumes, and the lecture has no volume content. The syllabus gives 10/23 to "Persistent Volumes, EKS deployment", and the lecture has EKS only. | Section 14, outline |
| L8 | 3, 5, 6, 7, 9, 10 | The bullets are not in ASD-STE100: "Under the hood", "the hard parts", "wires kubectl", "actually", "Less cluster operations". Slide 5 says "Master nodes", and the other slides say "control plane". | Section 14, section 1 |
| L9 | 4, 5, 8 | The titles differ in style: "Cluster COST Estimate – Control Plane Only!", a double space on slide 5, and all capitals on slide 8. | Week 01 reference |

## Lab defects

| No | Slide | Defect | Rule |
|--:|--:|---|---|
| A1 | 2 | The title says "Lab 9". The syllabus has no lab on 10/23, and your Blackboard names differ from the week (Week 05 is `Lab03`). | Section 14, agreement |
| A2 | all | The lab does not practise the VPC CNI, IAM with RBAC, `eksctl` or the cost. These 4 lecture topics need EKS, and the students have no EKS. | Section 15, every topic |

A2 cannot reach 100 % on the kubeadm cluster. The lab already teaches the other topics
as "the jobs that EKS does for you".

## What passes

**Both decks**
- Canvas 13.333 x 7.5 in, Calibri and Consolas only, 0 float coordinates, nothing off the canvas.
- Whale and footer on every slide, `N / 11` and `N / 10` in sequence.
- No duplicate title, no bullet word for word on two slides, no image below 110 DPI, no WMF.

**Lab**
- 10 slides, Step 0 to 6, 31 commands. Each script step names its slide.
- No EN DASH, curly quotation mark or zero-width space in a Consolas command.
- The 8 repository files match the names of Week 04, with no README.
- `master-init.sh.tftpl` writes `cleanup_lab09.sh`, and the script calls only that file.
- `m5.large`, Ubuntu 26.04, Kubernetes v1.35, Flannel and MTU 1500 are in the code.
- `maziar/kubia:v1` exists. The folder has no `luksa`, `nano`, `/Users/`, `.ssh/` or home IP.
- GitHub HEAD `2dbeafc` holds this version, and `localMachine.sh` equals `localMachine_v2.sh`.
- The lab ran 2 times on a live cluster on 2026-10-27 (report 2026-10-27-14).
- Lecture and lab agree on the story: EKS runs these jobs, and here you run them.

## Technical Details
- Rules: `~/.claude/PREFERENCES.md` sections 6, 13, 14 and 15.
- Deck checks: a python-pptx script on `prs.slides`, then a render of every slide, because
  a text extract misses images.
- Links: HTTP status with `curl`. The render uses LibreOffice, so a font can differ a little.

## Results
- Lecture: 9 defects. Lab: 2 defects, and 1 of them cannot reach 100 %.
- I did not run Terraform or the lab again.

## Issues / Notes
- `build_week08.py` has no `__main__` guard (section 13). `dedup_lectures.py` made v5, and it has the guard.
- The lecture v5 has no PDF. The lab v2 has one.
- Slides 3, 6 and 10 have cards that are more than half empty. No rule covers this.
- `Lab_week09_Blackboard_Submission_v2.md` is the short form, not the longer form of `Lab03`.
