# Report: Week13 v6 — 2026 accuracy review + deprecation cleanup

**Date**: 2026-07-20
**Sequence**: #05 for the day

## Summary
Reviewed `Week13_lecture_style_v5.pptx` (RBAC + IRSA) for technical accuracy as of mid-2026 via a
web-verified, adversarially-checked fact-check workflow. Only ONE item is genuinely removed-from-the-
product (wrong to teach); the rest of the "old-looking" content is legacy-but-still-fully-supported.
Removed the genuinely-dead items in v6; flagged (did NOT delete) the legacy-but-valid ones.

## Removed in v6
1. **Slide 4 — "Static password file"** (HTTP basic auth, `--basic-auth-file`). Deprecated in K8s
   v1.16, **removed in v1.19** (2020, PR kubernetes/kubernetes#89069). No longer exists — teaching it
   as a current auth method is factually wrong. (Kept the still-valid "Static token file".)
2. **Slide 22 — the two `eksworkshop.com/beginner/090_rbac/` and `/110_irsa/` links**. Verified they
   now redirect to the workshop homepage (site restructured); they no longer reach the labs. Removed
   the 2 stale links; kept the other 6 references.

## Flagged but NOT removed (legacy but still fully supported / still taught)
The adversarial verification explicitly downgraded these from "remove" to "update" — removing them
would gut the deck's core topic and would be wrong, because they still function and are still taught:
- **aws-auth ConfigMap** (slides 18-19): officially deprecated by AWS (docs banner) and superseded by
  **EKS Access Entries** (GA Nov 2023), but still fully functional (mapRoles/mapUsers/mapAccounts).
- **Client-side aws-iam-authenticator** (slide 20): superseded by `aws eks update-kubeconfig` /
  `aws eks get-token`, but the binary still works and the authenticator still runs server-side.
- **IRSA** (deck topic): still supported; AWS added **EKS Pod Identity** (2023) as a newer option.
- **Creator → system:masters** (slide 17): still true; Access Entries change how this is managed.
Recommended follow-up (offered to user): ADD modern-alternative notes rather than delete.

## Verified correct (no change)
RBAC GA in 1.8; `rbac.authorization.k8s.io/v1`; RBAC default in EKS; Role/RoleBinding manifests;
Node Authorization/RBAC/Webhook/ABAC as authorization modes (ABAC is legacy but still a valid mode).

## Results
- Delivered `Week13_lecture_style_v6.pptx` (22 slides) + `Week13_lab_style_v6.pptx` (26). Slide 4 auth
  list 8→7 items (clean reflow, diagram intact); references 8→6. 0 float coords, footers N/22.

## Method
4-area fact-check workflow (k8s-auth, eks-iam, irsa, refs) with WebSearch/WebFetch against
kubernetes.io + docs.aws.amazon.com, each finding adversarially re-verified with the strict test
"removed vs legacy-but-supported". I re-confirmed the two dead reference links with WebFetch myself.
