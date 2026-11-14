# Report: Week 07 and Week 10 lectures, the fixes of the audit 2026-11-09-02
**Date**: 2026-11-10
**Sequence**: #01 for the day

## Summary
The user asked to fix all the items of the audit `report-2026-11-09-02-week07-week10-lecture-audit.md`
(tables 1 to 5). Two new builders make the new lecture versions: Week 07 v7 (24 slides) and Week 10 v10
(37 slides). A third builder makes the Week 07 lab v3, its script and its long Blackboard text, and updates
the Week07 folder of the course repository (no commit, no push). All three decks pass the 32 deck checks of
`gate_week12.py` on PDFs that PowerPoint made. An independent reviewer checked the result (section "Review").
Nine items are open or are a decision of the user; they are in "Issues / Notes".

## What Changed
- Created `build_week07_lecture_v7.py`: the Week 07 lecture v7 and the slide kit that Week 10 imports.
- Created `build_week10_lecture_v10.py`: the whole Week 10 lecture in one builder, with `VERSION`.
- Created `build_week07_lab_v3.py` (from `build_week07_lab_v2.py`).
- Created `Week07/Lecture_week07_v7.pptx` and `.pdf`, `Week10/Lecture_week10_v10.pptx` and `.pdf`.
- Created `Week07/Lab_week07_v3.pptx` and `.pdf`, `Week07/localMachine_v3.sh`,
  `Week07/Lab_week07_Blackboard_Submission_v3.md`.
- Changed in `~/Documents/c/r/CLO835_Fall_2026/Week07/` (not committed): `localMachine.sh` (equal to
  `localMachine_v3.sh`), `cleanup_lab07.sh` and `master-init.sh.tftpl` (header "Lab Week 07"),
  `local-path-storage.yaml` (helper Pod image).
- No delivered file changed. v6, v9 and the lab v2 stay on disk.

## Technical Details

### Method
1. Both lectures start from the cover, agenda and Course Outline of `Week12/Lecture_week12_v6.pptx`, as the
   Week 07 v6 did. So both decks have one outline design (W10 #42, #8, #41).
2. The kit in `build_week07_lecture_v7.py` gives: `new_slide`, `bullets`, `rich`, `term`, `card`,
   `cards`, `caution`, `grid` (a table of house rectangles), `concept`, `cover`, `outline`, `agenda`,
   `number_and_save` and `set_pdf_info`.
3. Text between backticks is code: Consolas, bold, slate (W07 #23, W10 #22).
4. Bullets: a glyph run that ends with a tab, and the hanging indent as the tab stop. A test deck through
   PowerPoint gave the same x (68.4 pt) for the first word and for each wrapped line (W07 #25).
   An `a:buChar` bullet with U+25AA did not show in the PowerPoint PDF, so the kit does not use it.
5. Terminals: YAML and output gray, comments green, `$` lines cyan, error lines red (W10 #28). 11 or 12 pt
   (W07 #24). Long manifests use line spacing 1.0.
6. The outline: "K8s" becomes "Kubernetes" (W07 #21, W10 #18, #41), the text is 12 pt (W10 #42), and the
   tiles move 0.08 in to the left, so they end at 12.83 in, with the footer rule (W10 #49).
7. PDF: PowerPoint (AppleScript) makes the PDF. Then an incremental PDF update adds Title and Author
   (W07 #32). The pages stay byte for byte. `pdffonts` shows Calibri and Consolas only (W10 #1).
8. Gate: `gate_week12.deck_checks` with `ROOT` set to the week folder: 32 of 32 for each deck.
9. Each page was checked by eye at 80 dpi. Layout fixes after that: a wrapped table cell, the timeline
   lines, a wrapped add-on name, two terminal gaps, a wrapped DNS name, the agenda code names.

### Week 07 v7, slide by slide
1 cover, 2 agenda (in deck order), 3 outline, 4 Volumes in Kubernetes (definition first), 5 What Volumes Are
For (+ Secret caution), 6 Volumes vs PersistentVolumes, 7 Volume Types, 8 Volume Types, Continued (gitRepo
since v1.33, CVE-2024-10220, the complete list of removed in-tree types), 9 comparison table, 10 fortune
diagram, 11 emptyDir manifest, 12 emptyDir and Mount Settings, 13 Volume Lifecycle (+ timeline),
14 Git diagram (init container left, steps 1 to 4), 15 Git manifest (+ ENTRYPOINT, `.git` and sidecar
cards), 16 hostPath (lab Step 4 manifest + Baseline caution), 17 NFS (example only), 18 claim and StorageClass
on the course cluster (lab Step 5), 19 Amazon EBS on EKS (ebs-sc + claim, add-on, IAM, Auto Mode),
20 Commands and Troubleshooting, 21 Configuration for Applications (with the answers), 22 Key Takeaways,
23 Lab Week 07 and the Next Lectures, 24 References.

### Week 10 v10, slide by slide
1 cover, 2 agenda, 3 outline, 4 Part 1 divider, 5 hostPath, 6 hostPath Concerns (+ red caution), 7 sharing
diagram, 8 test-pd example, 9 Volumes in the Pod Specification: the Limits (+ CSI card), 10 Part 2 divider,
11 PV and PVC process, 12 Access Modes, 13 PV manifest `data-pv` (lab Step 1), 14 PV Phases and Reclaim
Policies, 15 decoupling diagram, 16 How a PVC Binds to a PV (+ lab Step 1 commands), 17 `data-pvc` and the
writer Pod (lab Steps 1, 2), 18 benefits diagram, 19 StorageClass, 20 Using StorageClasses, 21 the
StorageClass `standard` (+ EKS card), 22 dynamic provisioning diagram, 23 Storage on the Course Cluster,
24 Troubleshooting a Pending Claim, 25 Part 3 divider, 26 Why StatefulSets?, 27 MySQL Replication without
Kubernetes (source, replica, `SOURCE_HOST`), 28 StatefulSets vs ReplicaSets, 29 Headless Service,
30 the StatefulSet manifest of lab Step 4, 31 Adding Volumes to StatefulSet Pods (`data-kubia-0`,
retention policy), 32 StatefulSet Updates and Ordinals, 33 Discovering Peers (+ SRV commands, delete
dnstest), 34 Peer Discovery through DNS, 35 Optional Topics, 36 Key Takeaways, 37 Lab Week 10 at a Glance.

### Table 5, the rule conflicts: the decision taken in the decks
The rule files are not changed.
1. ASD-STE100 and correct facts win over "keep the source text" (CLAUDE.md gives ASD-STE100 the first place).
2. Docker Official Images: `nginx:alpine` stays (the user's decision of 2026-10-27). `busybox` goes from the
   Week 07 lab, because the gate bans it. `maziar/alpine-curl` replaces it, as in the Week 10 lab.
3. Week 07 introduces hostPath, a claim and a StorageClass, because its lab practises them. Week 10 teaches
   them in detail. The labs do not move.
4. The outline keeps the text that the user set on 2026-10-31 (Week 11 "Exam & Mock Exam week", Week 14 and
   Week 15 "Project presentation", EKS in Weeks 9 and 13).
5. `E74C3C` (PROMPT, DESIGN and the gate).
6. Terminals at 11 or 12 pt: inside the gate range, near the Week 01 reference.
7. The rules stay as the engine draws them (not changed).
8. The lab limit of about 40 commands wins. The decks label each topic that is not in a lab.
9. Title Case, as in all decks. The W07 title "Managing configuration" became "Configuration for Applications".
10. ASD-STE100 and the 12 pt minimum win.
11. The Week 01 reference glyphs: blue `▪`, teal `–`, gray `•`.
12. The Week 01 reference wins (PREFERENCES is newer than PROMPT.md).

## Results
- `Week07/Lecture_week07_v7`: 24 slides, gate 32 of 32 (v6: 31 of 32).
- `Week10/Lecture_week10_v10`: 37 slides, gate 32 of 32 (v9: 22 of 32).
- `Week07/Lab_week07_v3`: 10 slides, gate 32 of 32 (v2 had 3 fails: "keeps", the file title, the thumbnail).
- All three PDFs: Quartz (PowerPoint), Calibri and Consolas only, the page count equals the slide count,
  Title and Author set.
- `localMachine.sh` in the course repository equals `Week07/localMachine_v3.sh`. `bash -n` passes. It has
  0 `busybox`.
- No server started, so no port is used.

## Review
One independent reviewer (a subagent, read-only) checked each row of tables 1 to 4 against the text dumps, the
rendered pages, the lab scripts and the Kubernetes v1.35, AWS and MySQL documents.

First result, before the second round of fixes:
- Table 1: 30 of 37 fixed. Table 2: 17 of 18. Table 3: 38 of 49. Table 4: 18 of 22.
- 15 new problems.

Fixed in the second round (all three decks rebuilt, gate 32 of 32 again, pages checked by eye):
- W10 slide 33 ran `kubectl create service` again after lab Step 4 (AlreadyExists). The command moved to
  slide 29 as lab Step 4. Slide 30 is now "The StatefulSet Manifest".
- W07 slide 18 waited for `pod-using-my-claim`, but showed only the claim. The terminal now says that the
  file holds the Pod too.
- W10 slide 32: "Updates stay in order" was false with `maxUnavailable`. Now: "when it scales".
- W10 slide 27: the MySQL order was wrong. `CHANGE REPLICATION SOURCE TO` now comes before the start of
  replication.
- W07 slide 19: the IAM policy name. The EKS user guide now uses `AmazonEBSCSIDriverPolicyV2` (verified by the
  reviewer). The slide now says "the AWS managed policy that the EKS user guide names".
- W10 slide 13: a PV with no class binds to a claim that asks for no class (not only `""`).
- W07 slide 22: "removed the in-tree drivers" became "removed their in-tree drivers" (cloud disks only).
  "stay in the cluster" became "stay after the Pod".
- W10 slide 29: "A Pod IP address can change" became "A new Pod gets a new IP address".
- W07 slide 13: the persistent bar no longer says "exists before the Pod" (false for a dynamic PV).
- W10 slide 31: two Pods, as `replicas: 2`. W10 slide 35: the quiz claim is gone.
- W10 slide 37: the lab map now names slides 14, 17 (Step 1) and 26, 29 (Step 5).
- Repeats: three sentences that were word for word in both lectures; WaitForFirstConsumer on five W10 slides
  (now three); "ends with the Pod" on W07 slides 7 and 9; "hides the old files" on W07 slide 10; the
  gitRepo date on W07 slide 20; "Pod names the claim" on W10 slide 17.
- Labels "not in the lab": W07 slide 12 and slide 20, W10 slides 32 and 37.
- Passive voice: W07 slides 7, 8 and 13, W10 slide 14.
- Code names in Consolas: W07 slides 10, 13, 23; W10 slide 34. W10 slide 29 box: no code in the box now.
- `publishNotReadyAddresses` on W10 slide 33 (T4#12). `volumeMode` on W10 slide 11 (T3#37).
- The cover title is 34 pt, as in the Week 01 reference (T3#29). The outline text is 12 pt (T3#42).
- The CSI card points to the list of removed in-tree types (T4#6).
- W07 Blackboard section 7: W07 slide 18 now gives the answer.
- Lab: "Kubernetes" replaces "K8s" on lab slide 2. The helper Pod of `Week07/local-path-storage.yaml` uses
  `docker.io/maziar/alpine-curl`, as the live-tested Week 10 manifest does (was `docker.io/library/busybox`).

Facts that the reviewer could not verify (from memory only): CVE-2024-10220 as the reason for gitRepo off;
the git ENTRYPOINT of `maziar/alpine-git`; Baseline forbids hostPath; awsElasticBlockStore and azureDisk removed
in v1.27, azureFile and vsphereVolume in v1.30, cinder in v1.26 (the v1.35 PV page still lists cinder and
vsphereVolume as deprecated); RWOP stable in v1.29; the port name `80-8080`; Retain as the default for a static
PV; the MySQL statements.

## Issues / Notes
1. Not live-tested: the Week 07 lab changes (alpine-curl for busybox in Steps 4 and 5 and in the helper Pod
   of the local-path manifest, the block YAML style, comments). The
   Docker daemon on this Mac is off, and an AWS test needs the user's approval.
2. W07 #28: `maziar/alpine-git` has only the tag `latest` on Docker Hub. A pinned tag needs a push to Docker
   Hub, which needs the user's yes. The `.git` risk has a card; the YAML style is fixed.
3. W07 additions 12 and 15, W10 addition 16: no cluster ran, so the decks show no new live output. They show
   the standard kubectl error text and the output lines that the Week 10 lab recorded in its comments.
4. W10 #14: the Week 10 lab is not changed. The deck labels NFS, MySQL replication and the peer data as not
   in the lab, and slide 37 maps each lab step to its slides. Retain/Released and a claim that names a class
   are in the lecture only.
5. W07 #33 and W10 #48: kept by the decisions 2 and 11 above.
6. W07 #17 and W10 #41: the schedule text is the text of the user (decision 4).
7. The Week 07 lab deck still says "Lab Week 07" because Blackboard has no known name for the Week 07 lab
   (Week 06 is `Lab04`, Week 09 is `Lab05`).
8. I used `cd` one time at the start of a build command, against the rule. The shell stayed in the project
   folder.
9. Open after the review, by decision or by a blocker:
   - T1#17, T3#41: Weeks 14 and 15 both say "Project presentation". This is the text of the user (2026-10-31).
   - T1#21, T3#18: "PV" and "PVC" stay as the defined short forms of PersistentVolume and PersistentVolumeClaim.
   - T1#33 (`nginx:alpine`), T3#48 (the teal en dash): decisions 2 and 11.
   - T3#47: one builder with VERSION, but it uses the `build_week08` engine, not the Week 01 engine.
   - T3#14: Retain/Released and a claim that names a class are in the lecture only (decision 8).
   - Images with no tag: `maziar/alpine-git`, `maziar/alpine-curl`, `maziar/kubia-pet` (only `latest` exists).
   - The takeaway slides repeat points on purpose.
10. The scratchpad holds the export and gate scripts (`w0710/export.sh`, `pipe.sh`, `rungate.py`). They are
   volatile.
