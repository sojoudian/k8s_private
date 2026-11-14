# Report: Combined two-workshop lab deck (Week08 + Week09)
**Date**: 2026-07-08
**Sequence**: #07 for the day

## Summary
Built one PowerPoint file, `CLO835_Workshops_Lab_v1.pptx` (45 slides), containing two lab demos: Workshop 1 from `Week08_lab_style_v3.pptx` (Amazon EKS setup + Kubernetes Dashboard, then Volume Lifecycle with NodePort/LoadBalancer) and Workshop 2 from `Week09_lab_style_v2.pptx` (hostPath, dynamic PV/PVC on EBS, StatefulSets). Each demo is trimmed to run in a ~70-minute lab while keeping all core learning material. The original hand-tuned slides (including YAML, terminal screenshots, and diagrams stored as images) are preserved by merging the actual slides, not rebuilding from the (stale) builders.

## What Changed
- New file `CLO835_Workshops_Lab_v1.pptx` at the repo root (45 slides, 16:9).
- Scratch tooling: `pptx_merge.py` (cross-file slide-copy with image-relationship remapping, plus delete/reorder), `build_workshops.py`, `analyze-lab-decks` workflow.

## Technical Details
- Analysis: a 2-agent workflow read all 60 rendered slides (images, not just text) and produced a per-slide type/timing map and a 70-minute keep-plan per deck.
- Workshop 1 (Week08): kept 23 of 30 slides (~64 min). Cut the two Cloud9 env-prep slides (disk resize, temp-credential disable) as pre-class setup, two empty placeholder slides, one duplicate Description, and the internal "End of Workshop 1".
- Workshop 2 (Week09): kept 22 of 31 slides (~70 min). Kept all three sub-labs end to end (hostPath, dynamic PV/PVC, StatefulSet identity/storage/peer-discovery); cut two hostPath tangents, the app.js code walkthrough, three redundant "The End" dividers, and folded three duplicate diagrams.
- Merge mechanics: start from Week08, append the kept Week09 slides first (fresh partnames), then delete unwanted Week08 slides with drop_rel so orphaned parts are not serialized. Images imported through the package image machinery (unique names + hash dedup) to avoid the classic duplicate-partname corruption.
- Labeling: the two opening slides now read "Workshop 1 · CLO835 Lab" and "Workshop 2 · CLO835 Lab"; the decks' internal "WORKSHOP N" sub-dividers were relabeled "PART N" to avoid nested-workshop confusion; Week08's closing slide was relabeled "End of Workshop 1"; all 45 footers renumbered "N / 45".

## Results
- Package valid: zip OK, 45 slide parts, 45 content-type overrides, 0 dangling; LibreOffice renders all 45 pages.
- Visually verified: both Workshop title slides (relabeled subtitles + logos), a PART divider (dark circle "PART/1"), the "End of Workshop 1" closer, and a StatefulSet YAML+terminal content slide (code blocks and screenshot images intact), footers correct.

## Issues / Notes
- Workshop 2 is right at ~70 minutes; it fits only if the EKS cluster (and ideally the aws-ebs-csi-driver addon) is pre-provisioned before class rather than created live. Workshop 1 has ~6 minutes of buffer.
- These are the EKS-based Academy Learner Lab labs; that is correct for the labs and is separate from the no-EKS semester-project rule.
- A couple of "Goals" body lines still say "Workshop N goals" while the divider now says "PART N"; cosmetic only. Can normalize in a v2 if wanted.
- Saved as v1; can add an overall title/agenda slide or trim further on request.
