# Report: Week 12 lecture and lab, standards audit

**Date**: 2026-10-31
**Sequence**: #09 for the day

## Summary
The answer is no. The lecture has 19 defects. The worst are the wrong week on the cover, a
broken Course Outline, 3 wrong facts about Secrets, commands that do not run, and 2 dead
links. The lab runs and is on GitHub, but it has 6 defects. The audit is read-only, so I
changed no deck, no script and no repository file.

## Scope
- Lecture: `Week12/Week12_v3.pptx`, 21 slides, 0.73 MB.
- Lab: `Week12/Lab_week12_v2.pptx`, 10 slides, 0.07 MB.
- Code: `~/Documents/c/r/CLO835_Fall_2026/Week12`, in commit `1783b12`.

## What Changed
- Created this report and updated the memory file `project-week12-deck.md`.
- Temporary renders are in the session scratchpad.
- I created no cloud resource, so the lab did not run again.

## Lecture defects

| No | Slide | Defect | Rule |
|--:|--:|---|---|
| L1 | 1 | The cover says "Week 10 · Lecture" and "Week 10 feels like 100". This is Week 12. | Section 14, agreement |
| L2 | 3 | The outline is broken: the red exam box also says "K8s- Configmaps & Secrets", and the next box says only "Week 12: K8s". No box highlights Week 12. | Section 14, outline |
| L3 | 3 | "Week 09: K8s- K8s- PVs & K8s in AKS" and "Week 13: K8s – RBAC and AKS". AKS is the Azure product. "Study Week" has no number. | Section 14, outline |
| L4 | 3 | "Week 15: Project presentation" disagrees with "Week 15: Helm Charts" in the Week 09 and Week 10 outlines. The syllabus says Helm on 12/9. | Section 14, outline |
| L5 | 7 | `command:["sleep2.0"]` and `args:["10"]` have no space after the colon, so the YAML does not parse. `sleep2.0` is not a command in the image, and `image: ubuntu-sleeper` does not exist on `maziar`. | Section 14, section 6 |
| L6 | 11, 15 | `image: simple-webapp-color` is not a `maziar` image. `maziar/simple-webapp-color` does not exist. | Section 6 |
| L7 | 10 | `--from-literal=APP_MOD=prod`: the key must be `APP_MODE`, as in the manifest on the same slide. | Section 14 |
| L8 | 14 | The `kubectl create secret` command has no `\` after `DB_User=root`, so it fails as shown. | Section 14 |
| L9 | 13, 18 | Wrong fact: "Never stored on the disk of the underlying host" and "never written to the disk". The kubelet uses tmpfs, but etcd stores the Secret on the disk of the control plane. Step 5 of the lab shows this. | Section 14, facts, agreement |
| L10 | 16, 17 | Old fact: a default token Secret is created and mounted. Before v1.24 Kubernetes made these. Now the kubelet mounts a short-lived token as a projected volume. The cluster runs v1.35. | Section 14, facts |
| L11 | 16 | Wrong fact: the token gives "read-only permissions". The default ServiceAccount has API discovery permissions only. | Section 14, facts |
| L12 | 16 | The sample output is cut at the left edge ("tach-controller-token-mfkmj"). It uses `k`, which is not defined, and it shows tokens that v1.35 does not make. | Section 14 |
| L13 | 18 | `/ect/nginx/certs` is a typing mistake. `k exec fortune-https` uses an undefined `k` and a Pod that the lecture does not create. The bullets start with `#`. | Section 14 |
| L14 | 9, 16, 19 | Typing mistakes: "variables of files", "entiries", "log files those exposing". | Section 14 |
| L15 | 9, 12, 17, 20 | 4 third-party images, not native diagrams, with orange and green outside the palette. All are below 110 DPI: 91, 97, 73 and 97. | Section 13, section 6 |
| L16 | 21 | 2 of 6 links return 404: `sojoudian/simple-webapp-mysql` and `sojoudian/kubernetes-in-action/.../Chapter07`. | Section 14, facts |
| L17 | most | The bullets are not in ASD-STE100: "bake", "not a great idea", "dumped". Spellings differ: POD, pod, Pod; Config Map, configMap, ConfigMap; ETCD, etcd. | Section 14, section 1 |
| L18 | 5, 14, 15, 17 | Title style differs: 25 pt and 22 pt against 30 pt, "Secrets- Create", and a two-line title on slide 17. | Week 01 reference |
| L19 | 4, 7, 11 | The terminal title says `bash` above a configuration file or YAML. `error_log` on slide 4 is red, as if it were an error. | Section 14 |

## Lab defects

| No | Slide | Defect | Rule |
|--:|--:|---|---|
| A1 | 2 | The title says "Lab 12". The cleanup headers say the same. | Section 14, agreement |
| A2 | 3 | The sample output says `v1.35.9`. The cluster now installs `v1.35.10`. | Section 15 |
| A3 | 5, 6, 7 | `busybox:1.36` is not a `maziar` image, and `maziar/busybox` does not exist. | Section 6 |
| A4 | all | 5 lecture topics have no practice: `--from-file`, a declarative manifest for a ConfigMap and a Secret, `configMapKeyRef`, multiple environments (slide 12), and the ServiceAccount token folder (slide 16). | Section 15, every topic |
| A5 | Blackboard | `Lab_week12_Blackboard_Submission_v2.md` is the short form, and it has the pledge. It is not the form of your `Lab04` and `Lab05` items. | Section 15 |
| A6 | test | The live test of 2026-10-27 ran on v1.35.9. The cluster version changed. | Section 15 |

## What passes

**Both decks**
- Canvas 13.333 x 7.5 in, Calibri and Consolas only, 0 float coordinates, nothing off the canvas.
- Whale and footer on every slide, `N / 21` and `N / 10` in sequence.
- No duplicate title. No Consolas command has an EN DASH or a curly quotation mark.
- The deck size is near 1 MB. The Week 01 reference uses 30 pt titles, so 30 pt passes here.

**Lab**
- 10 slides, Step 0 to 6, 33 commands. Each script step names its slide.
- GitHub HEAD holds this lab, and `localMachine.sh` equals `localMachine_v2.sh`.
- The folder has the 8 files, `bash -n` and `terraform fmt -check` pass.
- `maziar/fortune:args` and `maziar/fortune:env` exist.
- No `luksa`, `nano`, `/Users/`, `.ssh/` or user name in the folder.
- The lab ran 2 times on a live cluster on 2026-10-27, and the clean-up left nothing.

## Technical Details
- Rules: `~/.claude/PREFERENCES.md` sections 6, 13, 14 and 15.
- Deck checks: the audit script of report #02, then a render of every slide.
- Facts come from the kubernetes.io pages for Secrets, ServiceAccounts and ServiceAccount
  administration. I viewed the slides as contact sheets.

## Issues / Notes
- L4 needs your decision: Helm or the project presentation in Week 15. Your Week 12 edit of
  2026-07-15 dropped Helm, but the syllabus and 2 later outlines keep it.
- A fix of L5 and L6 needs an image of the `maziar` account. `maziar/kubia` and `maziar/fortune` exist.
- A6 needs a new live test on AWS, and this needs your clear approval.
- `Week12_v3.pptx` has no PDF, and its name does not say "lecture". The folder also holds
  `Week12.pptx`, `Week12_lab.pptx` and `Week12_lab_v2.pptx`, which are old versions.
- In report #07, line L18 named 32 pt as the standard. The Week 01 reference is 30 pt.
- The Blackboard name of this lab is your decision.
