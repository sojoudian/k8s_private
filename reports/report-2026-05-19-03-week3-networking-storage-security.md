# Report: Week 3 — Networking, Storage & Security Deck
**Date**: 2026-05-19
**Sequence**: #03 for the day

## Summary
Built `Week3_lab_style.pptx`: a 14-slide teaching deck for "Docker Networking, Storage & Security", using the **exact** Lab02 design language already nailed down in `Week03_lab_style.pptx`. Networking + Storage content was pulled from the existing `Week3.pptx` (41 slides) and condensed; Security content was added from scratch since the source deck barely touched it. ECR/GitHub Actions was dropped per scope.

## What Changed
- **`Week3_lab_style.pptx`** — new 14-slide deck (~107 KB).
- **`build_week3.py`** — generator script (~600 lines). Reuses every helper from `build_week03.py` (whale_and_footer, terminal, title, add_rect, add_oval, etc.) so palette and layout primitives stay identical.
- **`reports/report-2026-05-19-03-week3-networking-storage-security.md`** — this report.

## Technical Details
**Scope decisions (confirmed with user before building):**
- Slide count: **tight**, 14 slides (the 15-18 target was a guideline; landed at 14).
- ECR/GitHub Actions section from source deck: **dropped** (not Networking/Storage/Security).
- Security topics: all four pillars (image / runtime / secrets / network), but condensed into one slide as requested.
- Labs: **concepts only** — no hands-on lab slides this deck.

**Slide map:**
1. Title — Week 3, Networking + Storage + Security subtitle, Docker logo in light-blue ring
2. Agenda — four numbered objectives (3 topics + a "decision frameworks" rollup)
3. What is a Docker network? — virtual-switch concept + diagram of a host with bridge network and three containers, hand-drawn with python-pptx shapes
4. Network drivers — bridge/host/overlay/macvlan/none comparison table
5. Working with networks — command list (ls/create/inspect/connect/disconnect/rm) + terminal mockup
6. Service discovery — DNS-on-user-defined-networks explanation + multi-container terminal + "gotcha" call-out for the default bridge
7. CNM vs CNI — side-by-side Docker vs Kubernetes model cards
8. Layers + Copy-on-Write — reused layout from Week03_lab_style with adjusted text
9. Ephemeral by default — scenario/fix two-column with blue-gradient option blocks
10. Volumes vs bind mounts vs tmpfs — comparison table (reused exactly)
11. -v vs --mount — legacy/modern terminals + comparison table
12. Four pillars of security — 2x2 grid with risk + practice for each pillar
13. Key takeaways — four numbered points
14. Closing — "Questions? / See you next week. / Good luck, Professor Maziar"

**Content provenance:**
- **Networking** (slides 3-7): condensed from Week3.pptx slides 4-13 (Lab 1 — Docker Networks). Kept the virtual-switch concept, command examples, multi-container service discovery, and CNM vs CNI comparison. Dropped the per-container ping/inspect detail since this is a teaching deck not a lab.
- **Storage** (slides 8-11): reused four layouts from Week03_lab_style nearly verbatim (the user already approved them).
- **Security** (slide 12): added from scratch. Source deck had no security content. Pulled the four pillars from standard Docker hardening practices (Trivy scanning, USER non-root, BuildKit secrets, daemon TLS).
- **Closing** (slide 14): matches the original closing intent from Week03 (Questions? / See you next week / Good luck Professor Maziar) — restored after I had replaced it with a Lab02 wrap-up template in the previous deck.

**Design fidelity vs Week03_lab_style.pptx:**
- ✅ Same palette: `#1FA8E0` blue, `#37465A` slate, `#3F3F3F` body, `#868686` muted, blue-gradient step blocks, `#2A2A2A` terminals
- ✅ Same fonts: Calibri (titles + body), Consolas (code + terminals)
- ✅ Same dimensions: 13.33" × 7.5" widescreen
- ✅ Same chrome: blue Calibri title 32pt top-left, cyan whale icon bottom-left, footer `CLO835, Fall 2026  N / 14` bottom-right with subtle separator line
- ✅ Same layouts: dark-slate numbered circles, terminal mockups with traffic-light dots, comparison tables with slate header + alternating bands, two-column cards
- ✅ No design changes were made — the only edits were content swaps inside existing patterns plus one new pattern (the host-bridge-containers diagram on slide 3, drawn with rectangles and ovals).

## Results
- 14-slide deck rendered successfully end-to-end (PowerPoint → PDF → JPG).
- Visual inspection of all 14 slides: no overlapping elements, no text overflow, no wrapping issues on the footer, no design-language deviations from Week03_lab_style.
- File: `/Users/maziar/Downloads/k8s_week3/Week3_lab_style.pptx` (~107 KB).

**Port allocation:** N/A — no dev server.

## Issues / Notes
- **Security pillar slide (slide 12)** uses small 10.5pt body text to fit four pillars in 2x2. Per user direction (all four in one slide), some compression was unavoidable. If you want to expand later, splitting into two slides (image+runtime / secrets+network) would give breathing room.
- **Diagram on slide 3** is hand-drawn with shapes (host box, bridge network sub-box, three container rectangles). If you want a more polished diagram, swapping in a real image would work — just substitute `s.shapes.add_picture(...)` for that block.
- **Slide 6 "Gotcha" box** uses the same red-left-bar card style as the Week03_lab_style troubleshooting slide — it's intentionally re-used to keep the visual vocabulary tight.
- **No labs**: per user direction. If you later want a hands-on lab slide for each topic, the Week03_lab_style script has full-terminal lab slide templates ready to adapt.
- **41 → 14 compression**: original Week3.pptx was 41 slides (Networking + Storage + ECR + Architecture). This deck is 14 slides covering only Networking + Storage + Security. Cleaner scope, same lecture-length target.
