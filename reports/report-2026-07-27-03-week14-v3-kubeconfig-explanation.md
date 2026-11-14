# Report: Week14 v3 — teachable text added to the kubeconfig slide

**Date**: 2026-07-27
**Sequence**: #03 for the day

## Summary
Per the user: the kubeconfig slide (lecture slide 4 = source slide 11, "Understanding Kubeconfig –
Working Withmultiple Clusters, Users and Namespaces") was a single diagram with NO text — hard to
teach and hard to understand. Added a clear, accurate, teachable explanation beside the diagram and
saved as v3.

## What Changed
- `assemble_week14.py`: `OVERRIDES[11]` adds 8 explanatory bullets (with hierarchy) to slide 11. This
  is an INTENTIONAL, user-requested ADDITION (the source slide had only the image) — not a change to
  existing source text.
- `build_week14.py`: `VERSION="v3"`; the bullets+figure layout now uses adaptive bullet sizing
  (12.5pt when >5 bullets) and a slightly smaller/repositioned figure box so a dense explanation fits
  cleanly beside the diagram.
- New `week14/Week14_lecture_style_v3.pptx` (8 slides) + `week14/Week14_lab_style_v3.pptx` (23 slides;
  content identical to lab v2 — the kubeconfig slide is lecture-only, re-emitted at v3 for version parity).

## The explanation added (accurate; also reads the diagram)
- kubeconfig is the file kubectl reads (default ~/.kube/config) to decide WHICH cluster, as WHICH user,
  in WHICH namespace.
- It stores three independent lists: **Clusters** (API-server address + CA cert = the "where"),
  **Users** (credentials: client cert / token / auth plugin = the "who"), **Contexts** (a named bundle
  of one Cluster + one User + an optional namespace).
- kubectl uses the current-context by default; switch with `kubectl config use-context <name>`
  (list with `kubectl config get-contexts`).
- Reading the diagram: each Context links a User to a Cluster — Context 1 = User 1 on Cluster 1
  (namespace dev); Contexts 2 & 3 both target Cluster 2. One file can define many; the same user/cluster
  can be reused; here Users 2 & 4 are defined but unused.

## Results
- Lecture slide 4 now shows the explanation (left) beside the diagram (right) — clean layout, no
  overflow/overlap, footer 4/8. Source title typo "Withmultiple" preserved. 0 float coords on both v3 decks.
- Delivered `Week14_lecture_style_v3.pptx` + `Week14_lab_style_v3.pptx`; v1/v2 retained. Source
  `week14/Week12.pptx` untouched.

## Issues / Notes
- Only the kubeconfig slide changed; the rest of the deck is identical to v2.
- Covers still self-label "Week 12" (source's own label) — unchanged.
