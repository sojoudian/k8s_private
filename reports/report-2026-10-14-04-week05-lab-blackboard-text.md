# Report: Week 05 Lab Blackboard Submission Text
**Date**: 2026-10-14
**Sequence**: #04 for the day

## Summary
The user supplied three screenshots of the Blackboard item `Lab02 - 2.5%`, which
holds the `Lab Week 04 Submission` instructions. The user asked for the same kind
of text for the Week 05 lab. I wrote it and saved it to
`Week05/Lab_week05_Blackboard_Submission.md`.

## What Changed
- **Created** `Week05/Lab_week05_Blackboard_Submission.md` — 123 lines. It holds
  the full student-facing text: the intro, 10 numbered sections, the Submission
  Requirements block, and the Integrity Pledge block.
- No other file was changed. No command with a side effect ran.

## Technical Details
Facts came from two sources:
1. `~/Documents/c/r/a2_test/CLO835_Fall_2026/Week05/localMachine.sh` — the lab
   script, 13 steps, Step 0 to Step 13.
2. `Week05/Lab_week05_v4.pptx` — 18 slides. Each step of the script names its
   slide, so the mapping is exact.

The Week 04 text uses this shape, and the new text copies it:
- a title, `Lab Week NN Submission`;
- a two-sentence intro that names the lab recording;
- numbered sections, each with one or two sentences and a `You must:` list;
- every bullet starts with `Show`, `Run`, `State` or `Explain`;
- the `Submission Requirements` and `Integrity Pledge` blocks, verbatim.

The 13 script steps group into 10 sections:

| Section | Script steps |
|---|---|
| 1. Build the Cluster and Check It | 0 |
| 2. Your First Pod | 1 |
| 3. A Pod from a Manifest | 2 |
| 4. Two Containers in One Pod | 3 and 4 |
| 5. Labels and Selectors | 5 |
| 6. Pods, ReplicaSets and Deployments | 6 and 7 |
| 7. Scale, Roll Forward and Roll Back | 8, 9 and 10 |
| 8. Maintaining the Desired State | 11 |
| 9. Reach the Pod from Your Browser | 12 |
| 10. Destroy the Cluster | 13 |

Every command in a bullet is a real command of `localMachine.sh`. Examples:
`kubectl run kubia --image maziar/kubia --dry-run=client -o yaml`,
`kubectl get pods -l 'rel in (stable,beta)'`,
`kubectl set image deployment/pingpong alpine=alpine:3.15 -n pingpong`,
`./cleanup_lab05.sh`.

Each section carries at least one `Explain` bullet, because the Week 04 text does.
These bullets separate a student who understands from a student who pastes:
- why the port forward works with no Service;
- why the ReplicaSet selector must match the template labels;
- why the Deployment keeps the old ReplicaSet;
- which object replaces a deleted Pod, and which does not;
- why the two nodes that do not run the Pod still serve the page.

Section 10 names `cleanup_lab05.sh`. The Week 05 `master-init.sh.tftpl` writes
that file to `/home/ubuntu` at boot, so the command works. The same bullet in the
Week 04 text names `cleanup_lab04.sh`, which the Week 04 master does not hold.

## Results
The file is at `/Users/maziar/Downloads/k8s_week3/Week05/Lab_week05_Blackboard_Submission.md`.
The text is ready to paste into the Blackboard instruction editor.
No report of a local dev server applies; no server ran.

## Issues / Notes
- The Week 04 item is worth 2.5% and 100 points, with the due date
  Sun Oct 11, 2026. The new text does not name a weight or a due date, because
  the user did not supply them for Week 05.
- The Week 04 item attaches `Lab_week04.pdf`. The matching Week 05 file is
  `Week05/Lab_week05_v4.pdf`.
- **Known defect, not fixed here.** Section 10 of the Week 04 text tells a student
  to run `./cleanup_lab04.sh` on the master. That file is absent on the Week 04
  master, because `master-init.sh.tftpl` of Week 04 never writes it. Week 05 does
  not have the defect.
