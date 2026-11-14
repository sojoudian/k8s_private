# Report: Exhaustive architectural analysis (delta run)
**Date**: 2026-07-12
**Sequence**: #01 for the day

## Summary
Executed the `ARCHITECTURE_ANALYSIS_PROMPT.md` against the whole project. Produced a durable current-state model persisted to `ARCHITECTURE/`, closing the prior run's one gap by safely executing all 10 builders. Confirmed the 2026-06-29 model still holds, added the two new builders, and re-verified every prior live defect (all still unfixed) plus new findings.

## What Changed
- `ARCHITECTURE/ARCHITECTURE_2026-07-12_18-30-37.md` (new full report) + `ARCHITECTURE/LATEST.md` (overwritten) + `ARCHITECTURE/INDEX.md` (appended).
- Memory: new `project-clo835-arch-analysis.md` + MEMORY.md index line (run-safety gotcha + pointer to LATEST.md).
- Scratch tooling only: `audit_decks.py` (binary defect scan), `run_builders.py` (safe sandbox runner), `clo835-arch-analysis` workflow.

## Technical Details
- Scope: 10 builders now (prompt said 6, prior report 8); build_week08/09 are new, both coord-guarded, using a new `build()` function that emits a lecture+lab pair with dynamic `total=len(deck)`.
- Method: 5-agent reader workflow (deep-read week08/09, drift-check the 8 known, spec-staleness, IaC re-verify) + my own deterministic verification.
- Run-harness: ran all 10 builders in a symlink sandbox (read-only asset symlinks, real temp output dirs, cwd=sandbox). All exit 0; `build_week04` live-emits 105 floats; guarded builders emit 0. **0 canonical files modified** (asserted via mtime check) — critical because builders have no `__main__` guard and save cwd-relative.
- Binary audit of 16 shipped decks: re-confirmed Week04 v16 = 175 floats, Week05 `/39` footer on 29 slides, Week06 v5 slide-13 un-hide; found new Week06 `/71` footers and the Week09 lecture-"Week 10" vs lab-"Week 9" cover conflict.
- Generator↔artifact divergence refined per builder: week04/05/06 emit older versions than canonical (re-running regresses); week07/08/09 in sync.
- IaC: all Week-5 defects still live (SSH 0.0.0.0/0, SG name collision, U+200B, missing kind.yaml/week5.pub); nested duplicate still ships.
- Governance specs stale (say 6/4 builders and "only week05 guarded"; reality 10 builders, 5/10 guarded).

## Results
Report validated by construction (all claims backed by a command or file:line). Coverage: all 10 builders read/drift-verified, all 10 executed, 16 decks binary-audited, 3 specs + 7 IaC files re-verified. Corrected one wording error (Week09 identity) after checking the shipped covers directly.

## Issues / Notes
- Highest-leverage open recommendation unchanged: extract a shared `clo835_design/` package + back-fill the coord guard + add a `validate.py` footer/float/hidden gate before authoring Week 10.
- The `project/` docx system and `CLO835_Workshops_Lab_v1.pptx` are new subsystems whose generators live outside the repo (session scratchpad), so the repo holds only their outputs.
