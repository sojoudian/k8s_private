# Report: Week14 v10 — fix dead eksworkshop IRSA link

**Date**: 2026-07-27
**Sequence**: #10 for the day

## Summary
The user reported `https://www.eksworkshop.com/beginner/110_irsa/` no longer works. Verified (WebFetch):
the EKS Workshop site was restructured and `/beginner/*` paths now redirect to the homepage. The IRSA
content moved to `https://www.eksworkshop.com/docs/security/iam-roles-for-service-accounts/` (verified
live with IRSA content). Replaced the dead link in both places it appears and rebuilt as v10.

## What Changed
- `assemble_week14.py`: added a `LINK_FIXES` map (applied to all body bullets) swapping
  `.../beginner/110_irsa/` → `.../docs/security/iam-roles-for-service-accounts/`. Fixes both the
  "Optional Group Activity" slide (source 28) and the References slide (source 29).
- `build_week14.py`: `VERSION="v10"`.
- New `week14/Week14_lecture_style_v10.pptx` (11 slides) + `week14/Week14_lab_style_v10.pptx` (23).

## Results
- The IRSA link now resolves to live content in both slides. 0 float coords. Delivered v10; v1–v9
  retained; source untouched.

## Issues / Notes (flagged, NOT fixed — same dead pattern, user only reported 110_irsa)
Two more eksworkshop `/beginner/*` links on the References slide are also dead (same restructure):
- `https://www.eksworkshop.com/beginner/090_rbac/`
- `https://www.eksworkshop.com/beginner/080_scaling/`
Left them as-is pending the user's go-ahead; a one-line addition to `LINK_FIXES` fixes them once the
current replacement URLs are confirmed.
