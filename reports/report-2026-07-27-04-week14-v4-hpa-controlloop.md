# Report: Week14 v4 — teachable control-loop walkthrough on the HPA slide

**Date**: 2026-07-27
**Sequence**: #04 for the day

## Summary
Improved lecture slide 5 (source slide 20, "HPA – Horizontal POD Autoscaling"). It already had the 3
verbatim source bullets + the HPA control-loop diagram, but the diagram's numbered steps (1→2→3→4)
were only tiny text inside the image. Kept the 3 source bullets verbatim and ADDED a step-by-step
walkthrough of the control loop that maps 1:1 to the diagram's numbers. Saved as v4 (builds on v3's
kubeconfig-slide text).

## What Changed
- `assemble_week14.py`: `OVERRIDES[20]` = the 3 verbatim source bullets + a "control loop, step by step
  (numbers match the diagram)" heading with 4 nested steps.
- `build_week14.py`: `VERSION="v4"` (adaptive bullet sizing from v3 already handles the denser text).
- New `week14/Week14_lecture_style_v4.pptx` (8 slides, now with BOTH the kubeconfig explanation from v3
  and the HPA walkthrough) + `week14/Week14_lab_style_v4.pptx` (23 slides, content = lab v2/v3,
  re-emitted for version parity).

## The walkthrough added (maps to the diagram's numbered arrows)
- **The control loop, step by step (numbers match the diagram):**
  1. Query the Metrics Server for each managed pod's current metric (e.g. CPU utilization)
  2. Calculate the replica count needed to bring the metric to (or near) the target value
  3. Update the replica count on the target's Scale sub-resource (Deployment → ReplicaSet)
  4. The ReplicaSet then adds or removes Pods to reach the desired number

The 3 original source bullets (HPA definition, HorizontalPodAutoscaler resource, 15-second poll of the
target resource) are preserved verbatim above it.

## Results
- Lecture slide 5 now teaches the numbered loop explicitly beside the diagram — clean layout, no
  overflow/overlap, footer 5/8. 0 float coords on both v4 decks.
- Delivered `Week14_lecture_style_v4.pptx` + `Week14_lab_style_v4.pptx`; v1/v2/v3 retained. Source
  `week14/Week12.pptx` untouched.

## Issues / Notes
- Addition (requested improvement), not a change to the source's verbatim bullets — those are kept.
- The replica-calculation MATH (desiredReplicas formula) is intentionally NOT duplicated here; the next
  slide (source 21, "Autoscaling process") already covers it with its own calc diagram.
