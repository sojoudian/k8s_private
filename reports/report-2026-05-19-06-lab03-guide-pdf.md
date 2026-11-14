# Report: Lab 03 Step-by-Step Guide PDF
**Date**: 2026-05-19
**Sequence**: #06 for the day

## Summary
Built `Lab03_Guide.pdf` — an 18-slide catch-up walkthrough so a student who missed the class can complete every part of Lab 03 (the rubric in `Lab03_Instructions.html`) on their own. Exact same design language as `Week3_Hands_On_Lab.pptx` (now `new_Week3.pptx`): Lab02 palette, Calibri/Consolas, terminal mockups with traffic-light dots, goal panels with green left bar, cyan whale + footer chrome.

## What Changed
- **`Lab03_Guide.pdf`** — 549 KB, 18 pages, the primary deliverable.
- **`Lab03_Guide.pptx`** — 121 KB, source PPTX (exported to the PDF).
- **`build_lab_guide.py`** — generator script (~700 lines). Reuses every helper from `build_lab.py`.

## Technical Details
**Slide map (18 slides):**
1. Title — "Lab 03 · Catch-up Guide / A step-by-step walkthrough"
2. What you'll build (and submit) — 5 step blocks + 6-item report checklist
3. Before you begin — 5 prereq items + terminal verifying `docker --version` and `pwd`
4. **Step 1**: Create the network — full `docker network create` + `inspect` terminal + capture checklist
5. **Step 2a**: MySQL with volume — `docker volume create` + `docker run` with `--mount type=volume` + `docker ps` verify
6. **Step 2b**: Insert + verify — wait-for-ready, CREATE DB + INSERT, SELECT showing Puffball
7. **Step 3a**: Adminer + DNS — `docker run` adminer + `nslookup` proof with annotated `Server: 127.0.0.11` and `Address: 172.28.0.2`
8. **Step 3b**: Browser login — mock Adminer login form with `Server: mysql-db` highlighted, "← BY NAME, not IP" annotation
9. **Step 4a**: Scan + secret file — `docker scout cves` + `chmod 600 db_password.txt` + `ls -l` showing `-rw-------`
10. **Step 4b**: Rebuild MySQL hardened — single `docker run` with secret mount, `--cap-drop=ALL`, selective adds, `--security-opt=no-new-privileges`
11. **Step 4c**: Verify hardening — `docker inspect --format` extracting CapDrop/CapAdd/SecurityOpt JSON + bonus env-grep proof
12. **Step 5**: Survive + tear down — SELECT after restart + cleanup commands + clean-state verification (three "no rows" greps)
13. **Reflection 1** — default bridge / DNS · with side-by-side terminal proof (NXDOMAIN on default vs resolution on user-defined)
14. **Reflection 2** — named volume vs bind mount · with `docker volume inspect` output
15. **Reflection 3** — how DNS works on user-defined networks · two-piece evidence breakdown
16. **Reflection 4** — caps + no-new-privileges · with default-vs-hardened CapAdd comparison
17. **Reflection 5** — data survival + early `volume rm` · with safe export-first sequence
18. Report + Integrity Pledge — 8-item submission checklist + sign-and-date pledge card

**Design fidelity** (vs `Week3_Hands_On_Lab.pptx`):
- ✅ Same Lab02 palette (`#1FA8E0` blue, `#37465A` slate, `#3F3F3F` body, `#868686` muted, blue gradient step blocks, `#2A2A2A` terminals)
- ✅ Same fonts (Calibri for body/titles, Consolas for code and terminal mockups)
- ✅ Same dimensions (13.33" × 7.5" widescreen)
- ✅ Same chrome (blue Calibri title top-left, cyan whale icon bottom-left, footer `CLO835, Fall 2026  N / 18` bottom-right)
- ✅ Same patterns (Goal panel with green bar, terminal mockups with traffic-light dots and title bar, Capture/Expected checklist column on the right, slate-circle numbered blocks)
- ✅ Same reflection-card pattern as the dark Q&A card from the original Week03 deck — but with the light-card variant from Copy-on-Write since we agreed Lab02 has no dark content panels

**Build pipeline:** `python build_lab_guide.py` → `Lab03_Guide.pptx` → `soffice --headless --convert-to pdf` → `Lab03_Guide.pdf` → `pdftoppm` for visual QA.

**One QA fix during the build:** Reflection 5's answer text was long enough that its 3 paragraphs overlapped when each got a fixed 1" textbox. Switched the reflection helper to use one combined textbox with paragraph spacers, so long answers reflow naturally. Verified slide 17 now renders cleanly.

## Results
- All 18 slides render correctly via LibreOffice → PDF → JPG; no overlapping elements, no text overflow, footer renders correctly on every page (`N / 18`).
- Mock browser window on slide 8 has correct chrome (traffic-light dots, address bar) and highlights the `mysql-db` field with a blue border + "← BY NAME, not IP" annotation.
- All 5 reflection answers include both a written explanation and (where helpful) a terminal-mockup proof.
- File: `/Users/maziar/Downloads/k8s_week3/Lab03_Guide.pdf` (549 KB).

**Port allocation:** N/A — no dev server.

## Issues / Notes
- **Mock browser screenshot on slide 8** is a simulated Adminer login form drawn with shapes, not a real screenshot. If you want a real one, run the lab once and substitute a real screenshot. The simulated version is good enough for a guide PDF where the student takes their own screenshots.
- **Pillars per step** mapping is explicit in slides 9-11 (Pillar 1 = Image, Pillar 3 = Secrets, then the rebuild combines 2/3/4 in one `docker run`). If you want pillar 2 (Network) called out as a separate item, note that it's actually already in place from step 1 (the user-defined network is the network-pillar baseline).
- **Reflection 4** uses `jq` syntax in the proof terminal. If your students don't have jq, mention they can also use the `--format` filter on docker inspect (shown in slide 11).
- **Scout vs Trivy** — the slide shows `docker scout cves` as the primary command. If students don't have Docker Scout (Windows / older Docker Desktop), trivy works equivalently. Both are mentioned.
- **No real screenshots embedded** — the guide tells students *what to capture* but doesn't include reference screenshots. If you want reference shots for grading, run the lab once and save the JPGs to the `analysis/` folder, then update `build_lab_guide.py` to embed them.
