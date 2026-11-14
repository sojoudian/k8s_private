# Report: Week 10 lecture and lab, standards audit

**Date**: 2026-10-31
**Sequence**: #07 for the day

## Summary
The answer is no. The lecture has 18 defects. The worst are removed volume types, 2 wrong
facts, a typing mistake in a title, and 11 third-party images. The lab runs and is on
GitHub, but it has 7 defects. The audit is read-only, so I changed no deck, no script and
no repository file. This is the class of 2026-11-04.

## Scope
- Lecture: `Week10/Week09_lecture_style_v7.pptx`, 28 slides, 3.59 MB.
- Lab: `Week10/Lab_week10_v2.pptx`, 10 slides, 0.07 MB.
- Code: `~/Documents/c/r/CLO835_Fall_2026/Week10`, in commit `1783b12`.

## What Changed
- Created this report and the memory file `project-week10-deck.md`.
- Temporary renders are in the session scratchpad.
- I created no cloud resource, so the lab did not run again.

## Lecture defects

| No | Slide | Defect | Rule |
|--:|--:|---|---|
| L1 | 3 | "Week 9: K8s- K8s- PVs & K8s in AKS": a doubled word, and AKS is the Azure product. | Section 14, outline |
| L2 | 3 | "Week 13: K8s – RBAC and AKS": the syllabus says Amazon EKS. | Section 14, outline |
| L3 | 3 | "Study Week" has no week number, and lecture Week 09 v6 says "Week 8: Study Week". | Section 14, outline |
| L4 | file | The file name says Week09, but the deck is Week 10. | Section 14, agreement |
| L5 | 8, 14 | `awsElasticBlockStore`: the current Kubernetes volumes page no longer lists this type. | Section 14, current API |
| L6 | 11, 16, 19 | `gcePersistentDisk` and `kubernetes.io/gce-pd`: the in-tree driver was removed in v1.28. The cluster runs v1.35, and the course uses AWS. | Section 14, current API |
| L7 | 15 | `image: mongo` is not a `maziar` image. | Section 6 |
| L8 | 24 | Wrong fact: a pet returns "with the same name, IP and data". A new Pod gets a new IP address. It keeps its name, DNS name and data. Slide 25 and the title of lab slide 8 show this. | Section 14, facts |
| L9 | 25 | Wrong fact: a headless Service "Points to only Master". Its DNS name returns the IP address of all the Pods. Only the name `mysql-0.mysql-h...` points to one Pod. | Section 14, facts |
| L10 | 24 | Typing mistakes: "Sttatefulsets" in the title, and "anew" in the bullet. | Section 14 |
| L11 | 5, 6, 10, 12, 16, 20, 23, 24, 25, 26, 28 | 11 third-party images, not native house diagrams. Slide 5 is a screenshot of a web page. Several add orange and green outside the palette. | Section 13, section 6 |
| L12 | deck | 3.59 MB. The rule is near 1 MB. Images are 3.56 MB of it. | Section 13 |
| L13 | 26, 28 | Images below 110 DPI: 108 and 106. | Section 13 |
| L14 | 23, 28 | Slide 23 image enters the title band (y 0.97) and crosses the footer line (y 7.07). Slide 28 image crosses the footer line (y 7.12). | Section 13 |
| L15 | 27 | The commands do not run as shown: `k` is not defined, `kubia-headless.yaml` is not shown, and `dig` is printed as a comment. | Section 14 |
| L16 | 7 | The manifest uses `type: Directory` with `/data`. The directory must exist, so the Pod does not start on a node without it. | Section 14 |
| L17 | 4, 5, 8, 13, 17, 18, 22, 24, 25, 26, 27, 28 | The bullets are not in ASD-STE100: "resurrected", "out-of-band", "maybe", "K8s agnostic". One object has 5 spellings: StatefulSet, Statefulset, Stateful Set, Stateful sets, statefulset. "pod" and "Pod" are both used. | Section 14, section 1 |
| L18 | 6, 10, 12, 16, 20, 21, 25, 26, 27, 28 | Title style differs: sizes 20 to 28 pt against 32 pt, lowercase on slide 21, and all capitals on slide 25. | Week 01 reference |

## Lab defects

| No | Slide | Defect | Rule |
|--:|--:|---|---|
| A1 | 2 | The title says "Lab 10". The cleanup headers say the same. | Section 14, agreement |
| A2 | 3 | The sample output says `v1.35.9`. The cluster now installs `v1.35.10`. | Section 15 |
| A3 | 5 | `busybox:1.36` is not a `maziar` image, and `maziar/busybox` does not exist. The helper in `local-path-storage.yaml` also uses `docker.io/library/busybox`, with no tag. | Section 6 |
| A4 | all | Lecture slides 27 and 28 (SRV records, peer discovery) have no practice. The lab runs `nslookup` on one Pod name only. | Section 15, every topic |
| A5 | repo | The folder has 9 files. `local-path-storage.yaml` is the extra file. The rule says 8. | Section 15 |
| A6 | Blackboard | `Lab_week10_Blackboard_Submission_v2.md` is the short form, and it has the pledge. It is not the form of your `Lab04` and `Lab05` items. | Section 15 |
| A7 | test | The live test of 2026-10-27 ran on v1.35.9, with a local copy of the provisioner file. The cluster version changed, and the raw GitHub URL has not run live. | Section 15 |

## What passes

**Both decks**
- Canvas 13.333 x 7.5 in, Calibri and Consolas only, 0 float coordinates, nothing off the canvas.
- Whale and footer on every slide, `N / 28` and `N / 10` in sequence.
- No duplicate title. No Consolas command has an EN DASH or a curly quotation mark.
- The cover says "Week 10 · Lecture", and the outline highlights Week 10.

**Lab**
- 10 slides, Step 0 to 6, 35 commands. Each script step names its slide.
- GitHub HEAD holds this lab, and `localMachine.sh` equals `localMachine_v2.sh`.
- `bash -n` and `terraform fmt -check` pass. `main.tf` differs from Week 09 by the week name only.
- The raw URL returns 200, and `local-path-storage.yaml` equals the tested file.
- The tags `kubia-pet:latest`, `alpine-curl:latest` and `local-path-provisioner:v0.0.37` exist.
- No `luksa`, `nano`, `/Users/`, `.ssh/` or user name in the folder.
- The lab ran 2 times on a live cluster on 2026-10-27, and the clean-up left nothing.

## Technical Details
- Rules: `~/.claude/PREFERENCES.md` sections 6, 13, 14 and 15.
- Deck checks: the audit script of report #02, then a render of every slide.
- Facts come from the kubernetes.io pages for volumes, Services and DNS. For L5, the page
  lists no `awsElasticBlockStore`. Its removal in v1.27 is my knowledge, not from that page.
- I viewed the slides as contact sheets, so I read the small text in images one time only.

## Issues / Notes
- A fix of L5 and L6 needs manifests with a CSI provisioner, for example `ebs.csi.aws.com`.
- A fix of L8 and L9 changes the text only.
- A7 needs a new live test on AWS, and this needs your clear approval.
- `build_week09.py` has no `__main__` guard, and it writes decks at import (section 13).
- The lecture v7 has no PDF.
- `maziar/kubia-pet` has `latest` only, so the lab names no tag.
- `apk update` on slide 27 is not tested on `maziar/alpine-curl`.
- The Blackboard name of this lab is your decision.
