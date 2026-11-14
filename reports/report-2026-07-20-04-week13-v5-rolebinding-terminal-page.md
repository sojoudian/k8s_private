# Report: Week13 v5 — new "Role and RoleBinding" terminal page

**Date**: 2026-07-20
**Sequence**: #04 for the day

## Summary
Per the user: the two YAML boxes (developer-role.yaml + devuser-developer-binding.yaml) baked into
slide 13's ("RBAC - Intro") embedded diagram were small/illegible. Created a NEW page rendering them
as house-style dark terminals, plus the kubectl command, and saved as v5. Slide 13 is unchanged.

## What Changed
- `build_week13.py`: added `render_yaml_pair` renderer + `yaml_pair` slide type; `_yaml_pair_slide()`
  builds the page from slide 19's stored code_blocks (Role YAML, RoleBinding YAML, command — matched
  by content, not order); `build_all()` inserts it right after source slide 19; `VERSION="v5"`.
- New page (lecture display slide 14, "Role and RoleBinding"): two terminals side by side —
  `developer-role.yaml` (Role manifest) | `devuser-developer-binding.yaml` (RoleBinding manifest) —
  content-fit, plus a bash terminal below with `$ kubectl create -f devuser-developer-binding.yaml`.
- Rebuilt + delivered `Week13_lecture_style_v5.pptx` (22 slides) and `Week13_lab_style_v5.pptx` (26;
  the lab has no source-19 slide, re-emitted at v5 for version parity).

## Results
- Slide 13 untouched (keeps the RBAC diagram; footer renumbered 13/22). New slide 14 shows the two
  manifests legibly in the project terminal design (traffic-lights + filename title bar + Consolas),
  command in cyan. YAML content is verbatim from the stored source (incl. the complete
  `verbs: ["list", "get", "create", "update"]` line the source figure had clipped). 0 float coords,
  footers "N / 22".

## Issues / Notes
- Title "Role and RoleBinding" chosen for the new page (descriptive; the two terminal title bars carry
  the filenames). Rename on request.
- Deck grew 21 -> 22 slides (lecture); lab unchanged at 26.
- Prior open item still stands: slide-3 outline has Wk11=ConfigMaps / Wk12=Exam (reverse of canonical
  schedule), carried forward unchanged.
