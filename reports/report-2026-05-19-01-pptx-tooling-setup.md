# Report: PPTX Redesign Tooling Setup
**Date**: 2026-05-19
**Sequence**: #01 for the day

## Summary
Installed the toolchain required to redesign `Week03_redesigned.pptx` so it matches the design language of `Lab01.pptx` and `Lab02.pptx`. Set up a Python 3.13 virtual environment with `python-pptx`, `markitdown`, and `Pillow`, and installed LibreOffice via Homebrew Cask for `.pptx → .pdf` rendering used in visual QA. Verified the full pipeline end-to-end on `Lab01.pptx`.

## What Changed
- `./.venv/` — created Python 3.13 virtual environment for this project (Python 3.14 was tried first but failed: `beautifulsoup4` has no 3.14 wheel yet).
- Python packages installed in the venv: `python-pptx 1.0.2`, `markitdown 0.1.5` (with pptx extras: `lxml`, `beautifulsoup4`, `markdownify`, `defusedxml`, etc.), `Pillow 12.2.0`, plus transitive deps (`onnxruntime`, `magika`, `numpy`, `XlsxWriter`).
- `/Applications/LibreOffice.app` — LibreOffice 26.2.3.2 installed via `brew install --cask libreoffice`. `soffice` symlinked at `/opt/homebrew/bin/soffice`.
- `./reports/` — created this directory and this report.

## Technical Details
**Skills already present** in `~/.claude/skills/` (no install needed): `pptx` (core PowerPoint editing), `ckm-design-system` (design-token synthesis), `theme-factory` (theme application), `ckm-slides` (HTML slides, not needed here).

**Dependency choices and reasoning:**
- Used **Python 3.13** rather than the system default 3.14 because several pptx-adjacent packages (notably `beautifulsoup4`) do not yet publish 3.14 wheels, and pip cannot resolve a working dependency tree under 3.14.
- Chose a **project-local `.venv`** over global pip per user request — keeps the toolchain scoped to this project and doesn't pollute system Python.
- LibreOffice install required **one retry** — the first `brew install --cask libreoffice` attempt failed when the download mirror dropped the connection mid-transfer (`curl: (18) transfer closed with 243561087 bytes remaining`). Retry succeeded.

**Pipeline established:**
1. `markitdown <file>.pptx` → text content extraction (for content QA).
2. `python-pptx` → programmatic editing of slide XML (layouts, shapes, fonts, colors).
3. `soffice --headless --convert-to pdf <file>.pptx` → render to PDF.
4. `pdftoppm -jpeg -r 150 <file>.pdf slide` → rasterize each PDF page to JPG (for visual QA against Lab01/Lab02).

## Results
**Smoke test:** `Lab01.pptx` → `Lab01.pdf` → `slide-01.jpg` succeeded with no errors.

**Versions confirmed:**
- python-pptx: **1.0.2**
- markitdown: **0.1.5**
- Pillow: **12.2.0**
- LibreOffice: **26.2.3.2**
- pdftoppm (Poppler): **26.04.0**

**Port allocation:** N/A — no dev server started this session.

## Issues / Notes
- **Python 3.14 incompatibility:** if the venv ever needs to be rebuilt, force Python 3.13 explicitly (`/opt/homebrew/bin/python3.13 -m venv .venv`). Calling `python3 -m venv` picks up 3.14 by default and breaks on `beautifulsoup4`.
- **LibreOffice download flakiness:** the documentfoundation.org mirror cut the first download. If retries also fail, fall back to `brew install --cask libreoffice-still` (older stable) or download the dmg manually.
- **Soffice cosmetic warning:** `Task policy set failed: 4 ((os/kern) invalid argument)` appears on first invocation under macOS 25 — harmless, slide rendering still works.
- The actual redesign of `Week03_redesigned.pptx` was **not started** in this session — only the tooling was set up. Next step: extract Lab01/Lab02 design language (palette, fonts, layouts, motifs), then apply to Week03.
