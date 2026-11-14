# Report: Repetition removed from the lectures after Week 06
**Date**: 2026-10-27
**Sequence**: #10 for the day

## Summary
The user asked for the Week 06 treatment on the rest of the semester, all the
lectures. I applied the same rule to the 6 lecture decks after Week 06: state a
point one time, a second time only when it is needed, and never three times; no
two slides with one title. The decks go from 117 slides to 104. I deleted 13
slides and changed the text of 29 slides; 6 of the 29 got a new title. Three of the deleted slides repeated a
slide of an earlier lecture word for word. Every input deck is unchanged.

## What Changed

### New decks
| Lecture | Input | Output | Slides |
|---|---|---|--:|
| Week 07 Volumes | `Week07/Week07_lab_style_v4.pptx` | `Week07/Week07_lab_style_v5.pptx` | 14 → 12 |
| Week 08 EKS | `Week09/Week08_lecture_style_v4.pptx` | `Week09/Week08_lecture_style_v5.pptx` | 13 → 11 |
| Week 09 PV/StatefulSets | `Week10/Week09_lecture_style_v6.pptx` | `Week10/Week09_lecture_style_v7.pptx` | 36 → 28 |
| Week 12 ConfigMaps/Secrets | `Week12/Week12_v2.pptx` | `Week12/Week12_v3.pptx` | 21 → 21 |
| Week 13 RBAC | `week13/Week13_lecture_style_v6.pptx` | `week13/Week13_lecture_style_v7.pptx` | 22 → 21 |
| Week 14 RBAC/HPA | `week14/Week14_lecture_style_v10.pptx` | `week14/Week14_lecture_style_v11.pptx` | 11 → 11 |

### New script
`dedup_lectures.py` (guarded). It holds every deletion, edit and retitle, with
the reason beside it. It reads each input and never writes it, and it stops if
one edit does not match exactly one text.

## Technical Details

Method: I dumped every slide in deck order (titles, bullets, terminals, tables,
notes), read the text inside 44 large images with macOS Vision OCR, and counted
each fact. Slide numbers below are the numbers of the input deck.

### Week 07 (Volumes)
| Fact | Before | After |
|---|---|---|
| A volume shares the lifecycle of the pod | slides 3, 9 | 9 |
| A volume is defined in the pod spec | 3, 5 | 5 |
| gitRepo | 6, 10, 11 | 6, 11 |
| A pod uses a PV through a PVC | 5, 7, 13 | 5, 7 |
- Deleted: 3 (its one new bullet, "filesystems are unique per container", moved to 4), 10 (the gitRepo diagram).
- Edited: 8 (emptyDir definition, already on 6), 13 (PVC bullet; the manifest shows `claimName`).

### Week 08 (EKS)
| Fact | Before | After |
|---|---|---|
| AWS manages the control plane | 3, 6, 8 | 3, 8 |
| Public or private API endpoint | 5, 10 | 10 |
| Worker node types | 3, 5, 7 | 3, 7 |
- Deleted: 6 (its one new fact, "No SSH", moved to the slide 3 card), 12 ("Volume Lifecycle", word for word Week 07 slide 9).
- Edited: 3 (added bullet), 5 (2 bullets).

### Week 09 (PV, PVC, StorageClass, StatefulSets)
| Fact | Before | After |
|---|---|---|
| Stable pod names | 24, 27, 30, 31 | 24, 31 |
| Stable network identity | 24, 27, 29, 30, 31 | 24, 31 |
| Per-pod storage | 24, 28, 30, 31, 34 | 24, 34 |
| Ordered operations | 24, 26, 27, 30 | 24 |
| Deployment pods change name and IP | 24, 26, 29, 31 | 24, 31 |
| Per-pod DNS name | 24, 32, 33 | 24, 32 |
| Challenges of a direct volume | 8, 10 | 8 |
- Deleted: 9 (the NFS slide, word for word Week 07 slide 14), 10 (its point moved to 8), 26, 27, 28, 29, 30, 33.
- Edited: 8 (added "locks the pod definition to a specific cluster"), 24 (card 1 takes the ordinal index of slide 27), 31 (the per-pod volume sentence), 32 (takes `clusterIP: None` of slide 33), 35 (takes the "every member must know every other member" point of slide 29).
- Retitled: 16 ("Using a PersistentVolumeClaim in a pod" was also the title of 17) → "A PersistentVolumeClaim and a Matching PersistentVolume".
- Kept on purpose: the binding flow on 12 (diagram) and 15 (text); the PV manifests on 13 and 16 (16 pairs a PV with a PVC to show the match); the 25 scenario picture.

### Week 12 (ConfigMaps and Secrets)
| Fact | Before | After |
|---|---|---|
| The 3 ways to configure an app | 4 (twice) | 4 |
| `docker run ... fortune:args 15` | 5 (bullet and terminal) | 5 (terminal) |
| The ConfigMap manifest | 10, 11 | 10 |
| `envFrom: configMapRef` | 11 (twice) | 11 |
| The Secret manifest | 14, 15 | 14 |
| `envFrom: secretRef` | 15 (twice) | 15 |
| Base64 encoding | 13, 14 (twice), 15 | 13, 14 |
| The `mount | grep certs` command | 18 (bullet and terminal) | 18 (terminal) |
- Retitled: 7 ("Passing Command Line Arguments in Kubernetes" was also the title of 6) → "Example: Overriding ENTRYPOINT and CMD".
- Corrected: slide 13 said "Stored in etcd and are encrypted"; slide 15 says etcd does not encrypt a Secret without encryption at rest. Slide 13 now says "Stored in etcd".
- The removed `envFrom` block of slide 15 also carried a defect: `secretRef: name: app-config`.

### Week 13 (RBAC)
| Fact | Before | After |
|---|---|---|
| The auth plugin returns the groups | 4, 6 | 4 |
| EKS uses RBAC | 9, 16 | 16 |
| Webhook authorization | 9, 11, 12 | 11, 12 |
| ABAC | 9, 11 | 11 |
| Create a role, then bind it | 12, 13, 15 | 13, 15 |
| K8s stores no users | 5, 16 | 5, 16 (16 keeps the IdP line) |
- Deleted: 21 (the kubeconfig picture, with the same title and picture as Week 14 slide 4, which teaches it in full).
- Edited: 6, 9 (5 bullets), 12 (2 bullets), 16 (1 bullet).
- Kept on purpose: the Role manifest as a picture on 13 and as a terminal on 14 (you added 14 because the picture text is too small).

### Week 14 (RBAC continued, HPA)
| Fact | Before | After |
|---|---|---|
| A context = cluster + user + namespace | 4, 6, 7 (twice) | 4, 7 |
| `use-context` and `get-contexts` | 4, 6, 7 | 6, 7 |
| The 3 steps of the control loop | 8 (twice), 9 | 8 |
- Retitled: 5, 6, 7 (all three were "Working with Kubeconfig – Kubectl Config") and 9.
- Edited: 4, 5, 6, 7 (comments), 8 (bullet 3), 9 (its 3 repeated steps became the calculation that its picture shows: (60 + 90 + 50) / 50 = 4, and max(4, 3) = 4).

### Verification
- Every edit matched exactly one text; the script stops otherwise.
- Footers are `1 / N` to `N / N` in sequence in all 6 decks. 0 floats. Calibri and Consolas only.
- 0 duplicate titles in any deck.
- A text compare of each input with its output: text changed only on the slides named above (3, 2, 6, 8, 4 and 6 slides).
- 10 changed slides were rendered with LibreOffice and read. All text fits.

## Results
- 117 slides → 104 slides. 13 deleted, 29 changed (6 of them retitled).
- No fact is lost: each deleted slide either repeated other slides, or its one new point moved to the slide named above.

## Issues / Notes
Found during the read, NOT changed (not repetition):
- Week 12 slide 16 describes auto-created token Secrets. Since Kubernetes 1.24 a
  pod gets a projected service account token, not a Secret.
- The Course Outline slides of Weeks 08, 09, 12, 13 and 14 do not agree with
  each other, and the Week 12 and Week 14 ones hold broken lines ("Week 12: K8s",
  "Configmaps & SecretsWeek").
- Week 07 slide 5 says PVs "won't be discussed further in this section", but
  slide 13 (now 11) shows a PV with EBS.
- Week 07 slide 12 "Managing configuration" is Week 12 content inside the Volumes lecture.
- Week 09 uses the in-tree `awsElasticBlockStore` and `gcePersistentDisk` volumes.
- Week 14 links to `eksworkshop.com/beginner/...`, which no longer exists.
- The cover labels still read "Week 10 · Lecture" (Week 09 deck), "Week 11"
  (Week 13) and "Week 12" (Week 14).
- Weeks 01 to 05 were not part of this request.
