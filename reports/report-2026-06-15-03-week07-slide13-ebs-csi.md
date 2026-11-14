# Report: Week 7 — Modernize deprecated EBS volume on slide 13 (v3)
**Date**: 2026-06-15
**Sequence**: #03 for the day

## Summary
Slide 13 used the deprecated in-tree `awsElasticBlockStore` volume. Per user request ("update slide
13 only"), replaced it with the modern **EBS CSI driver** pattern (StorageClass-backed PVC + Pod).
Produced `Week07/Week07_lab_style_v3.pptx` (v2 retained).

## What Changed
- **Edited** `build_week07.py` slide-13 block + bumped `VERSION` to `v3`.
- **Created** `Week07/Week07_lab_style_v3.pptx` + `.pdf`.

## Technical Details
- Manifest: was a single Pod with inline `awsElasticBlockStore: {volumeID, fsType}`. Now two docs in
  one terminal: a **PersistentVolumeClaim** (`storageClassName: ebs-sc`, `ReadWriteOnce`, `4Gi`) and a
  **Pod** whose volume is `persistentVolumeClaim: {claimName: my-ebs-claim}`.
- Bullets rewritten to the modern flow: EBS CSI driver provisions via a StorageClass
  (`ebs-sc → ebs.csi.aws.com`) → PVC requests storage → Pod mounts via the PVC.
- Fit fix: 27 YAML lines overflowed the dark panel at font 9.5; dropped to font 9 (matches slide 11's
  working config) — now fully contained. Rendered and verified.

## Results
- Slide 13 renders cleanly, modern CSI pattern, no overflow. Rest of deck unchanged.

## Issues / Notes
- Scope was slide 13 only. **Still deprecated (left per user):** slide 6 (Volume Types list includes
  gitRepo + in-tree gce/aws/azure disk types) and slide 10 (gitRepo diagram).
