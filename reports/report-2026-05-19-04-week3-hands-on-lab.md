# Report: Week 3 Hands-On Lab Deck
**Date**: 2026-05-19
**Sequence**: #04 for the day

## Summary
Built `Week3_Hands_On_Lab.pptx`: an 8-slide hands-on lab in the exact `new_Week3.pptx` (Lab02) design language. One integrated exercise — students stand up a MySQL + Adminer stack that exercises all three Week 3 topics: networking (user-defined bridge + DNS), storage (named volume), and security (image scan + non-root + cap-drop + secret file).

## What Changed
- **`Week3_Hands_On_Lab.pptx`** — new 8-slide deck (~92 KB).
- **`build_lab.py`** — generator script. Reuses every helper from `build_week3.py` so palette and layout primitives stay identical.
- **`reports/report-2026-05-19-04-week3-hands-on-lab.md`** — this report.

## Technical Details
**Scope decisions (confirmed with user before building):**
- Structure: **one integrated lab** — MySQL + Adminer stack exercises networking + storage + security together. Shows how the concepts compose.
- Slide count: **8 slides** (compact, ~25-min lab session).
- Solutions: **fully guided** — every command shown, expected output shown, only the 3 reflection questions on the closing slide are open-ended.

**Slide map:**
1. Title — "Hands-on Lab · Networking, Storage and Security in one stack"
2. What you'll build — 4 step blocks (Networking · Storage · Security · Verify) + 7 meta info rows (time, prereqs, images, network, volume, scanner, deliverable)
3. Step 1: Create a user-defined network — `docker network create --driver bridge --subnet 172.28.0.0/16 clo835-net` + inspect output + "why custom bridge?" callout
4. Step 2: MySQL on the network, backed by a volume — `docker volume create` + `docker run` with `--network` and `--mount type=volume` + seed one row + mini terminal showing `docker ps` + `docker volume ls` proof
5. Step 3: Connect Adminer by container name — `docker run` Adminer on the same network + `nslookup mysql-db` proof + browser config (Server: mysql-db, BY NAME) + mini architecture diagram showing both containers on `clo835-net` with DNS arrow
6. Step 4: Now harden it — `docker scout cves` scan + create secret file (chmod 600) + rebuild MySQL with `--mount` for secret, `MYSQL_ROOT_PASSWORD_FILE`, `--cap-drop=ALL`, `--cap-add` for required caps, `--security-opt=no-new-privileges` + 4-pillar checklist showing what each command does
7. Verify + Tear down — two side-by-side terminals: left verifies the stack is healthy + the row survived; right tears down containers, network, volume, and the local secret file
8. Closing — "Submit your lab notebook" + 3 reflection questions

**Design fidelity vs new_Week3.pptx:**
- ✅ Same palette: `#1FA8E0` blue, `#37465A` slate, `#3F3F3F` body, blue-gradient step blocks, `#2A2A2A` terminals
- ✅ Same fonts: Calibri + Consolas
- ✅ Same dimensions: 13.33" × 7.5" widescreen
- ✅ Same chrome: blue Calibri title top-left, cyan whale icon bottom-left, footer `CLO835, Fall 2026  N / 8` bottom-right
- ✅ Same lab-slide pattern as Week03_lab_style.pptx slides 9-11: GOAL panel with green left bar, terminal mockup left, Expected/Reflect column right
- ✅ Same security 2x2 grid pattern from new_Week3.pptx slide 12 (reduced to 4 small numbered pillars on slide 6)
- ✅ Same mini architecture diagram pattern from new_Week3.pptx slide 3 (host/network/containers, drawn with shapes)

**Content all from the new_Week3.pptx material:**
- Networking concepts (user-defined network for DNS) → slides 3, 5
- Storage concepts (named volume, `--mount` syntax) → slide 4
- Security four pillars (image/runtime/secrets/network) → slide 6 mapped 1:1

## Results
- 8-slide deck rendered cleanly via LibreOffice → PDF → JPG.
- Visual inspection: no overlapping elements, no text overflow, footer renders correctly on all 8 slides, mini-diagram on slide 5 reads clearly.
- File: `/Users/maziar/Downloads/k8s_week3/Week3_Hands_On_Lab.pptx` (~92 KB).

**Port allocation:** N/A — no dev server.

## Issues / Notes
- **Slide 6 GOAL text wraps to 2 lines.** The GOAL panel uses a fixed 0.55" height; the slide-6 goal text ("Apply the four pillars in order: scan the image, restart the MySQL container as non-root, drop capabilities, and stop passing the password through an env var.") is long enough to wrap and just barely fits. If you want it tighter, edit the goal-panel call on slide 6 in `build_lab.py` to either shorten the text or pass a taller height. Other slides' goal panels are one-liners and fit fine.
- **Adminer image** is pinned to `:latest` for brevity. In a real classroom you'd want a specific tag (e.g. `adminer:4.8.1`) so students get the same UI.
- **Security step uses BOTH a bind mount for the secret file AND a named volume for data.** Two `--mount` flags on one `docker run` is a deliberate teaching moment — it shows how multiple mounts compose. Mention this verbally during the lab.
- **No troubleshooting slide.** Per user choice of "compact, 7-9 slides". If students hit blockers, point them at the Week03_lab_style.pptx slide 12 (Troubleshooting) which already has the four most common errors documented.
- **Tear-down is on the same slide as Verify.** This keeps the deck tight but means students might miss the cleanup step. Emphasize during the live lab: every resource you create on slide 3-6 must be removed on slide 7.
