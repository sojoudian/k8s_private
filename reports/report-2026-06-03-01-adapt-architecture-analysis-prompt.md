# Report: Adapt Architectural-Analysis Prompt for k8s_week3
**Date**: 2026-06-03
**Sequence**: #01 for the day

## Summary
The user supplied a long, multi-project "exhaustive architectural analysis" prompt originally
written for three web-service roots under `~/Documents/c/neWeb/` and asked to retarget it to the
single project at `~/Downloads/k8s_week3`. I scouted the project, established that it is a Python
`python-pptx` slide-deck/lab-guide build system (CLO835 Kubernetes course) rather than a web
service, and rewrote the prompt to match its real structure, entry points, risks, and verification
surface. The rewritten prompt was saved to `ARCHITECTURE_ANALYSIS_PROMPT.md` in the project root.

## What Changed
- **Created** `/Users/maziar/Downloads/k8s_week3/ARCHITECTURE_ANALYSIS_PROMPT.md` — the retargeted
  prompt, preserving the original's phase discipline (Scope → Map/Triage → Decompose → Seams →
  Critical Paths → Verify → Coverage Gate → Deliver → Rules) but rewritten for this project.
- **Created** this report.

## Technical Details
Reconnaissance performed before rewriting (no assumptions):
- `tCloud` from the original prompt does **not** exist under `neWeb/` (only an empty
  `~/Documents/c/research/tCloud`) — irrelevant here; the new target is a single root.
- `~/Downloads/k8s_week3` is **not a git repo** → git-history-based verification marked unavailable.
- Inventory: 6 first-party Python builders (`build_week3.py`, `build_week03.py`, `build_week04.py`,
  `build_week05.py`, `build_lab.py`, `build_lab_guide.py`; 6,291 LOC total), ~21 `.md` (spec/design
  + auto-reports), 4 yaml/yml, plus Terraform/shell lab content under
  `week05_practical_work/week5_code/`. Generated/skip set: `.venv/`, 64 `.pptx`, 79 `.pdf`,
  527 `.png/.jpg`, `analysis/` XML+JPG dumps, preview dirs, `.mp4`, `.zip`.

Key re-mappings from the original prompt's concepts to this domain:
- "Multiple project roots, each with inventory + coverage gate" → **build targets** (each `build_*.py`).
- "Auth / billing / data-integrity / core-product critical paths" → (1) build pipeline
  spec→builder→`.pptx`→render; (2) design-system single-source-of-truth (palette/fonts/geometry);
  (3) coordinate-unit integrity (`_i()`/`_sanitize_coords` float-coord bug); (4) lab-content validity
  (terraform/kind/kubia YAML).
- "Detect forks, analyze one + report drift" → targeted at `build_week3.py` vs `build_week03.py`
  and `build_lab.py` vs `build_lab_guide.py`.
- "CI / container / IaC build files" → none exist for the build system; the `.tf`/`.yaml`/`.sh`
  are teaching content, explicitly reclassified as content not deploy.
- ARCHITECTURE output dir → `/Users/maziar/Downloads/k8s_week3/ARCHITECTURE`.

Verified structural facts woven into the prompt:
- No shared module — each builder copy-pastes its own palette constants (`BLUE`, `SLATE`, `STEPS[*]`
  at ~lines 11–36 of each). Confirmed divergence (e.g. `TERM_ORANGE` present in `build_week3.py`,
  absent in `build_lab.py`).
- `_i()` and `_sanitize_coords()` are defined **only** in `build_week05.py`; the other five builders
  lack the float-coordinate guard → flagged as a concrete risk in the prompt.
- `build_week3.py` vs `build_week03.py` confirmed near-forks (same Lab02 palette; `build_week03.py`
  adds `Emu`/`qn` imports and claims a "verbatim" Lab02 derivation).

## Results
- `ARCHITECTURE_ANALYSIS_PROMPT.md` written successfully (single root, deck-build framing, no-git
  caveat, re-mapped critical paths, build-target coverage gates, ARCHITECTURE/ deliverable layout).
- No analysis was executed — the task was to adapt the prompt, not run it. The rewritten prompt is
  ready to paste back as a follow-up instruction, or to run directly.

## Issues / Notes
- The original prompt's `tCloud` root is a dead reference; if a multi-project analysis is ever wanted,
  the real `tCloud` candidate is empty and would contribute nothing.
- The prompt instructs running each builder in a scratch/temp CWD because executing `build_*.py` in
  place will overwrite existing `.pptx` artifacts — worth honoring when the analysis is actually run.
- Rendering `.pptx` → `.pdf`/`.jpg` may need LibreOffice; the prompt already flags that as a possible
  "cannot run → mark unverified" case.
