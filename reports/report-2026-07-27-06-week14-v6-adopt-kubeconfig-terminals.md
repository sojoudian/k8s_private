# Report: Week14 v6 — adopt user's split kubeconfig terminals (with real output)

**Date**: 2026-07-27
**Sequence**: #06 for the day

## Summary
The user hand-edited `Week14_lecture_style_v5.pptx` and asked me to adopt + understand the changes.
Diagnosed via a python-pptx semantic diff (my v5 build vs their file): they **split my single
`kubectl config` terminal (lecture slide 5) into THREE teaching terminals**, and added the **real
captured command output** from their own `k3d-kabana-dev` cluster. Baked their edit into the builder
and rebuilt as v6. Lecture deck grows 9 → 11 slides.

## What the user changed (understood)
My v5 slide 5 was one terminal listing all 6 `kubectl config` commands. Their edit turns it into three
slides (all titled "Working with Kubeconfig – Kubectl Config"), pairing each command with its real
output so students see what it produces:
- **Slide 5** — `kubectl config view` + the actual merged kubeconfig YAML (apiVersion v1; cluster
  `k3d-kabana-dev` at `https://0.0.0.0:59478`, `certificate-authority-data: DATA+OMITTED`; context/user
  `admin@k3d-kabana-dev`; `current-context: k3d-kabana-dev`; `kind: Config`).
- **Slide 6** — `kubectl config get-contexts` + the real table (`CURRENT NAME CLUSTER AUTHINFO
  NAMESPACE` / `* k3d-kabana-dev k3d-kabana-dev admin@k3d-kabana-dev`).
- **Slide 7** — the four context-mutation commands (current-context / use-context / set-context
  --namespace / set-context define).

## What Changed (adopted)
- `build_week14.py`: replaced `_KUBECONFIG_TERMINAL` (single) with `_KUBECONFIG_TERMINALS` (list of 3);
  `build_all()` now `extend`s all three after source slide 11. `VERSION="v6"`. The user's captured
  output is stored VERBATIM (k3d-kabana-dev, DATA+OMITTED, server URL, and the get-contexts column
  alignment — Consolas preserves it).
- New `week14/Week14_lecture_style_v6.pptx` (11 slides) + `week14/Week14_lab_style_v6.pptx` (23, unchanged).

## Results
- Slides 5-7 render as house terminals: command (cyan) + comment (green) + output (gray), indentation
  and table columns preserved. HPA moves to slide 8; footers renumber /11. 0 float coords on both v6 decks.
- Delivered v6; v1-v5 and the user's edited v5 retained; source untouched.

## Why it's a good change (pedagogy)
Showing real command output (the kubeconfig YAML and the contexts table) makes the abstract concept
concrete — students see the clusters/users/contexts/current-context they just learned about in an
actual file. Splitting across 3 slides keeps each terminal readable instead of one dense block.
