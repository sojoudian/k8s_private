# Report: Week12 Lab v3 — one simple, self-contained workshop

**Date**: 2026-07-15
**Sequence**: #13 for the day

## Summary
Read and fully mapped the Week12 lab v2 deck (17 slides, two workshops), then built a new
**v3 lab deck with a single, deliberately simple workshop** that teaches the whole subject —
ConfigMaps *and* Secrets — via the one simplest mechanism: inject a literal value into a Pod as
an **environment variable**. No ConfigMap volumes, no nginx, no openssl, no TLS/HTTPS. Ran a
4-dimension adversarial multi-agent QA pass over the rendered slides, fixed the one confirmed
defect, and delivered.

## What Changed
- **New** `build_week12_v3_lab.py` (repo root) — standalone builder that imports `build_week12`
  (guarded, so importing never rebuilds) and reuses its exact house-design helpers.
- **New** `Week12/Week12_lab_style_v3.pptx` — 10 slides.
- Reports/memory updated.

## Analysis of v2 (why a new workshop, not "keep one")
Lab v2 has two workshops, neither "super easy":
- **WS1 "Configure Applications with Environment Variables and ConfigMaps"** (slides 2–9):
  sprawls across five techniques — env from Pod manifest, env from ConfigMap, command-line args,
  create-from-file, and a **ConfigMap volume exposing an nginx config as files** (+ port-forward/curl).
- **WS2 "Working with K8s Secrets"** (slides 10–16): default serviceaccount secrets, a TLS Secret
  generated with **openssl**, an nginx **HTTPS/SSL** ConfigMap, deploy + verify HTTPS with curl.

So per the instruction ("if we don't have a super-simple one, create one"), I built a new one.

## v3 deck (10 slides)
1. Cover — ConfigMaps & Secrets · Week 10 · Lab
2. Workshop divider — *Inject Configuration into a Pod*
3. Goals
4. **Step 1 · Create a ConfigMap** (`--from-literal=sleep-interval=25 --from-literal=sky-color=blue`; `get cm -o yaml`)
5. **Step 2 · Inject the ConfigMap as an env var** (Pod YAML `configMapKeyRef` → `printenv INTERVAL` → 25)
6. **Step 3 · Create a Secret** (`create secret generic ... --from-literal=api-key=s3cr3t-value`; base64/Opaque)
7. **Step 4 · Inject the Secret as an env var** (Pod YAML `secretKeyRef` → `printenv API_KEY` → s3cr3t-value)
8. **ConfigMaps vs Secrets** (two-card comparison)
9. Workshop: the End
10. Cleanup (`kubectl delete namespace week10`)

Consistent pattern for the four step slides: title + one intro line + two content-fit terminals
(manifest/commands | stored-yaml/verify). base64("s3cr3t-value") = `czNjcjN0LXZhbHVl` (verified).

## Technical Details
- Reused imported helpers: `render_cover`, `divider`, `closing`, `title`, `bullets`, `auto_term`,
  `add_rounded_rect/rect/text`, `whale_and_footer`, `_sanitize_coords`, palette. Custom
  `two_terms()` sizes both terminals to the taller pane's content (font auto-shrinks 13→ until it
  fits `6.72 - y`), and a custom `_compare_card()` draws the two comparison cards.
- Built + rendered in the sandbox (`bx12/`, which symlinks assets); 0 float coordinates each build.

## QA (adversarial multi-agent workflow)
Ran `week12-labv3-qa`: 4 review dimensions (k8s-correctness, factual-claims, pedagogy,
design-layout) → each finding independently verify-agent'd. 10 findings raised, 3 confirmed:
- **CONFIRMED MAJOR (slide 8)** — the comparison's storage row was false/misleading for an
  env-var-only workshop: "Mounted via tmpfs (in-memory)" applies only to Secret *volumes* (never
  mounted here), and "Lives in etcd / on the node" implied Secrets don't persist to etcd. **Fixed:**
  both cards now say "Persisted in etcd", the Secret adds "encryption-at-rest is opt-in", and the
  tmpfs/volume claim is removed. (Corroborated by 3 independent verifiers.)
- **CONFIRMED NIT (slide 1)** — cover says "Week 10". Left as-is: standing cover-label item the
  user has not authorized changing; kept consistent with the v2 covers.
- **Rejected by verifiers**: sky-color orphan key (canonical example), apply→exec readiness wait
  (overstated), unexplained `luksa/fortune:env` (nit), terminal empty space (normal terminal look).

## Results
- Delivered `Week12/Week12_lab_style_v3.pptx` (10 slides) + `build_week12_v3_lab.py`. v1/v2 decks
  untouched. All slides render clean: bigger readable terminals, no void/overflow/overlap, footers
  "X / 10", 0 float coords, and the comparison slide is now technically correct.

## Issues / Notes
- Cover still reads "Week 10 · Lab" (matches v1/v2 covers) — the same standing label mismatch,
  untouched pending explicit OK to flip WEEK_LABEL.
- v3 intentionally drops volumes/nginx/openssl/TLS; if a "simple + one hands-on volume" variant is
  wanted later, that's a separate ask.
