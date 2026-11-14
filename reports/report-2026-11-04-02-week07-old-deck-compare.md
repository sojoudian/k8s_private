# Report: Week 07 old deck compared with the current lecture
**Date**: 2026-11-04
**Sequence**: #02 for the day

## Summary
You asked if `Week07/week7_old.pptx` is the same as the Week 07 lecture that we have.
The old deck is the source of the lecture series. `Week07_lab_style_v1.pptx` has the
same content as the old deck. The current lecture `Week07_lab_style_v5.pptx` is not the
same. It has 12 slides, against 14, and 5 slides have changes.

## What Changed
- Created this report.
- No deck changed. The text dumps and the extracted pictures are in the session
  scratchpad (`w7cmp/`).

## Technical Details
**The old deck.** `Week07/week7_old.pptx`, 1.8 MB, 14 slides, 16:9, dated 2026-11-04
18:36. Ten slides hold text. Four slides hold a picture:
- Slide 10: the gitRepo diagram (User, Pod, Container, gitRepo volume, Repository).
- Slide 11: the gitRepo Pod manifest with 4 notes. It clones
  `github.com/luksa/kubia-website-example.git`.
- Slide 13: an EBS Pod manifest with `awsElasticBlockStore` and a `volumeID`.
- Slide 14: an NFS Pod manifest, server `192.168.0.55`, path `/exports/assets`.

**Old deck against v1.** The text of 11 slides is the same. Slides 11, 13 and 14 show
the same YAML and notes as text in a terminal, not as a picture. Slide 10 keeps the
diagram. So v1 is the old deck in the house design.

**Old deck against v5 (current).**

| Old slide | v5 slide | Result |
|---|---|---|
| 1 Cover, 2 Agenda | 1, 2 | Same text |
| 3 K8s Volumes | 3 | Merged into "Volumes". 6 of 7 bullets removed |
| 4 Volumes | 3 | Same text, now on the merged slide |
| 5 to 7, 9 | 4 to 6, 8 | Same text |
| 8 Volume Type: emptyDir | 7 | "(an empty directory)" removed |
| 10 Using GitRepo Volume | none | Slide removed, with its diagram |
| 11 Pod Manifest with GitRepo | 9 | New manifest: an `initContainer` with `maziar/alpine-git` and an `emptyDir` |
| 12 Managing configuration | 10 | Same text |
| 13 Persistent Volumes: Amazon EBS | 11 | New bullets and manifest: EBS CSI driver, StorageClass, PVC |
| 14 Using NFS Volume | 12 | Same YAML, now as text |

The 6 bullets that old slide 3 has and v5 does not have:
- Used to persist data between container invocations.
- Can be shared by containers in a pod.
- Defined as part of the pod spec.
- Share pod's lifecycle.
- Initiated when pod starts.
- Terminated when a pod is terminated.

**When the changes occurred.**
- v2 to v4 replaced the gitRepo and EBS manifests, because Kubernetes deprecates
  the `gitRepo` volume and the in-tree `awsElasticBlockStore` volume.
- v5 (2026-10-27, `dedup_lectures.py`) merged old slides 3 and 4 and removed slide 10.

## Results
- Old deck = v1 in content: yes.
- Old deck = v5 (current): no. 9 slides keep the same text, 5 slides changed, 2 slides
  are gone.
- The new v5 slide 9 clones `github.com/sojoudian/kubia-website-example.git`. That
  repository returns 404 (run 10, report #01).

## Issues / Notes
- The text comparison ignores bullet signs and line breaks.
- I viewed the 4 old pictures. I did not render the v5 slides to images.
- No server started, so no port is used.
