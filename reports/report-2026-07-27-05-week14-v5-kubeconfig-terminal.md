# Report: Week14 v5 — inserted a kubectl-config terminal after the kubeconfig slide

**Date**: 2026-07-27
**Sequence**: #05 for the day

## Summary
Per the user: after lecture slide 4 (kubeconfig concept + diagram), insert a new slide using the
house dark-terminal mockup ("the old terminal we had in previous weeks") showing the kubeconfig
commands taught to students. Added a `kubectl config` terminal page and saved as v5. Lecture deck grows
8 → 9 slides; lab deck unchanged.

## What Changed
- `build_week14.py`: `VERSION="v5"`; added `_KUBECONFIG_TERMINAL` (a synthetic content slide with a bash
  code block) and inserted it in `build_all()`'s lecture list immediately after source slide 11 — so it
  renders as a full house terminal via the existing `_term_stack` path. (Same insertion technique as the
  Week13 "Role and RoleBinding" page.)
- New `week14/Week14_lecture_style_v5.pptx` (9 slides) + `week14/Week14_lab_style_v5.pptx` (23 slides;
  unchanged content, re-emitted for parity).

## The terminal added (canonical kubectl config workflow; uses the diagram's own names)
- `kubectl config view` — view the merged config (~/.kube/config)
- `kubectl config get-contexts` — list contexts (each = CLUSTER + USER + NAMESPACE)
- `kubectl config current-context` — which context is active now
- `kubectl config use-context context-1` — switch (changes cluster, user AND namespace together)
- `kubectl config set-context --current --namespace=dev` — pin a default namespace
- `kubectl config set-context context-1 --cluster=cluster-1 --user=user-1 --namespace=dev` — define a context
  (ties Context 1 → cluster-1 + user-1 + namespace dev, matching the concept diagram)

## Results
- Lecture slide 5 is now the kubeconfig terminal (house style: traffic-light bar, green comments, cyan
  commands); HPA moves to slide 6, footers renumber /9. Clean, no overflow, 0 float coords on both v5 decks.
- Delivered `Week14_lecture_style_v5.pptx` + `Week14_lab_style_v5.pptx`; v1–v4 retained; source untouched.

## Issues / Notes
- Chose the standard `kubectl config` command family (which operationalizes the concept diagram) over
  source slide 12's AWS/EKS-specific `aws eks update-kubeconfig` hands-on — that one is IAM-access
  focused and already lives in the lab deck. Say the word to swap in those commands instead.
