# Report: Architecture Delta Analysis — the Week 01 Workstream
**Date**: 2026-09-16
**Sequence**: #01 for the day

## Summary
This run analyses the repository and updates the durable model. It is a delta over the
exhaustive run of 2026-09-07. One workstream was added in the nine days between the two
runs. No existing source file was edited, and no open defect was fixed.

## What Changed
- `ARCHITECTURE/ARCHITECTURE_2026-09-16_11-51-47.md` — new. The delta report.
- `ARCHITECTURE/LATEST.md` — replaced with the same content.
- `ARCHITECTURE/INDEX.md` — one dated line appended.
- `memory/project-week01-deck.md` — new. The Week 01 subsystem model.
- `memory/project-clo835-arch-analysis.md` — refreshed to the new counts.
- `memory/MEMORY.md` — two index lines refreshed or added.
- `reports/report-2026-09-16-01-architecture-delta-week01.md` — this file.

## Technical Details
The method was a mtime scan of the whole tree against the 2026-09-07 run. It found 32 new
files. All of them belong to one workstream: `build_week01.py` and the `week01/` folder.
The 16 older Python files carry mtimes of 2026-07-27 or earlier, so they are unchanged.

The run then executed `build_week01.py` in a symlink sandbox, never at the repo root,
because ten builders still save a deck at import time. A ZIP-CRC comparison shows the
builder reproduces its shipped v5 exactly. A binary audit re-tested every open defect.

## Results
- First-party Python: 17 files, 14 579 lines. Renderers: 15.
- Coordinate guard: 10 of 15 renderers (6 own copies, 4 by import).
- 14 of 15 renderers reproduce their stored deck content-identically.
- `build_week01.py` needs no scratchpad path, so it fixes the repo's top
  reproducibility risk by example.
- Every open defect reproduces. The lab `terraform init` still fails. The two
  zero-width spaces are present. `week5.pub` is still missing. `Week04_lab_style_v16.pptx`
  still holds 175 float coordinates. `build_week08.py` and `build_week09.py` still fail.
- Safety gate: this run wrote 0 files into the repository source.

## Issues / Notes
- The repository is not a git repository, so no history is available.
- The user has fixed none of the six priorities from the 2026-09-07 report.
- No local web service was started, so the port rule does not apply.
