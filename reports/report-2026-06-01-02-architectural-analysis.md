# Report: Comprehensive Architectural Analysis of k8s_week3
**Date**: 2026-06-01
**Sequence**: #02 for the day

## Summary

End-to-end architectural read of `/Users/maziar/Downloads/k8s_week3` (excluding `.pptx`/`.pdf` binaries per task scope). The project is a **content-engineering pipeline** for Professor Maziar's CLO835 (Cloud Architecture, Fall 2026) at Seneca Polytechnic ITAS. Its core artifact is a family of programmatically-generated PowerPoint decks built with `python-pptx` in a single shared visual language ("Lab02 design language") derived from a canonical source deck. Around that core sit four support concerns: a written design spec, a behavior contract for the AI deck-builder, a Terraform/kind lab harness for the student-facing workshop, and a per-week analysis archive of source `.pptx` decompressions used to drive content fidelity.

The architecture is essentially a **single-author craft pipeline** — no CI, no tests, no package boundaries, no application runtime. The code is procedural Python that emits one binary artifact. Engineering discipline lives in three layers: `DESIGN_LANGUAGE.md` (visual contract), `PROMPT.md` (behavioral contract for AI sessions), and `reports/*.md` (provenance trail per substantive change). The biggest production-engineering risks are (1) duplicated helper functions across the six build scripts with no shared module, (2) an OOXML float-coordinate bug that LibreOffice tolerates but PowerPoint/Keynote do not, and (3) heavy artifact accumulation (700 user files, ~30 MB of intermediate JPGs + XML) with no `.gitignore`-style cleanup discipline.

## What Changed
This is analysis-only. The only artifact written is this report at `reports/report-2026-06-01-02-architectural-analysis.md`.

## Technical Details

### 1. Inventory (700 user files, excluding `.pptx`/`.pdf`/`.venv`/`.git`)

| Category | Count | Notes |
|---|---:|---|
| `.jpg` | 386 | Per-slide renders for visual QA. Build artifacts. |
| `.xml` / `.rels` | 137 / 112 | Unzipped OOXML inside `analysis/*_xml/` — used as source-of-truth for palette/typography reverse-engineering. |
| `.md` | 19 | Spec (`DESIGN_LANGUAGE.md`), prompt template (`PROMPT.md`), per-session reports (9), source-text dumps (5), other (4). |
| `.png` | 16 | Asset library: whale, K8s logo, Docker logo, Python logo, old-assessment screenshots, source-slide screenshots. |
| `.py` | 6 | All build scripts. No tests, no `__init__`, no shared lib. |
| `.tf` | 8 | AWS+EC2+kind Terraform stack for student lab harness (duplicated 4 of 4 inside an extracted-zip subfolder). |
| `.yaml` | 4 | kind cluster config + `kubia` pod descriptor (each duplicated in the nested zip extract). |
| `.txt` | 3 | Lab commands ref, Blackboard quiz TSV, human-readable quiz answer key. |
| `.svg` | 2 | Python logo source (re-encoded to PNG via `cairosvg`). |
| `.sh` | 2 | `init_kind.sh` (duplicate of EC2 user-data inline). |
| `.html` | 1 | Lab 03 instructions, styled standalone — `<style>` block with web-safe fonts (Lato/Open Sans/Georgia), not the deck's Calibri/Consolas. |
| `.mp4` | 1 | 70 MB lab recording. Outside any build pipeline. |
| `.zip` | 1 | Source archive of `week5_code/` (already extracted into a duplicate dir). |
| Lock | 1 | `.claude/scheduled_tasks.lock` — Claude Code session control file. |

### 2. Top-level structure

```
/Users/maziar/Downloads/k8s_week3/
├── DESIGN_LANGUAGE.md          # 39 KB — visual spec (14 sections)
├── PROMPT.md                   # 11 KB — AI behavior contract (9 hard rules + workflow)
├── Lab02_Announcement.md       # short student-facing announcement
├── Lab03_Instructions.md       # lab rubric
├── Lab03_Instructions.html     # same rubric, styled
│
├── build_lab.py                # 638 LoC → Week3_Hands_On_Lab.pptx (8 slides)
├── build_lab_guide.py          # 1062 LoC → Lab03_Guide.pptx (18 slides)
├── build_week3.py              # 961 LoC → Week3_lab_style.pptx (14 slides)
├── build_week03.py             # 1049 LoC → Week03_lab_style.pptx (14 slides, sibling to ↑)
├── build_week04.py             # 1389 LoC → Week04/Week04_lab_style_v{N}.pptx (38 slides)
├── build_week05.py             # 1106 LoC → Week05/Week05_lab_style_v{N}.pptx (39 slides)
│
├── whale.png, docker_logo.jpg  # extracted from Lab02.pptx/ppt/media/
│
├── analysis/                   # 18 MB — source-deck decompositions
│   ├── lab01/, lab02/, week03/, week3_src/, week3_new/, week03_new/, lab_new/, guide_new/, lab02_user/
│   │                           # → each contains slide-NN.jpg + text.md (markdown-ified source slides)
│   └── lab01_xml/, lab02_xml/, week03_xml/
│                               # → unzipped OOXML used to grep palette/font runs
│
├── Week04/                     # 17 PPTX versions (v2..v16) + per-slide PDFs + previews + assets
├── Week05/                     # 11 PPTX versions (v1..v11) + previews + v11_jpgs + src-preview
├── Week06/                     # empty (placeholder for next week)
│
├── week05_practical_work/      # Student-facing lab harness
│   ├── Week5 - Lab Reco.mp4    # 70 MB recording
│   ├── week5_code.zip          # source archive (8 KB)
│   └── week5_code/             # extracted; contains a NESTED week5_code/ that is its own duplicate
│
├── old_assessments/            # 4 PNG screenshots of prior course assessments
├── reports/                    # 9 markdown reports — provenance log per substantive change
└── .venv/                      # local virtualenv (excluded from analysis)
```

### 3. The build-script architecture

All six build scripts share the **same internal layout**:

1. **Module docstring** — names output file + scope.
2. **Palette block** — 24 `RGBColor` constants (BLUE, SLATE, BODY, MUTED, LIGHTBLUE, WHITE, CARD_BG, RULE_GRAY, GOAL_GREEN, ALERT_RED, TERMBG, TERM_RED/YEL/GRN/GRAY/CYAN/ORANGE/ERR, FOOTER_GRAY, etc.) plus a `STEPS = [...]` 6-element gradient and `FONT_SANS`/`FONT_MONO` literals. **Verbatim duplicated** across all 6 files.
3. **Helper block** — a stable core of 8 functions (`add_text`, `add_rich_text`, `add_rect`, `add_oval`, `add_line`, `whale_and_footer`, `title`, `terminal`), plus deck-specific extras (`add_hex`, `add_diamond`, `add_pentagon`, `add_triangle`, `add_arrow`, `add_doublearrow`, `add_dashed_line`, `goal_panel`, `bullet_list`, `capture_panel`, `step_block`, `meta_box`, `objective`, `pillar`, `takeaway`, ...). The core 8 are **verbatim duplicated** across all 6 files.
4. **`prs = Presentation()` setup** — always 13.333 × 7.5 in, layout 6 (Blank), `TOTAL = <slide count>`.
5. **Per-slide procedural blocks**, delimited by `# SLIDE N` comments. Each block opens `s = prs.slides.add_slide(blank)`, calls `title(s, ...)`, body construction, then `whale_and_footer(s, N, TOTAL)`.
6. **`prs.save(out)`** at the bottom.

Function count per script: 14 (`build_lab.py`) → 31 (`build_week04.py`). Total 6205 LoC across all six.

**Identifiable inheritance trail**: `build_week03.py` was first (a faithful Lab02-style port). `build_week3.py` cloned its helpers and added topic-specific components (`fact`, `cmd_row`, `model_card`, `fix_block`, `pillar`, `layer_box`, `wrap_box`). `build_lab.py` cloned again and added `goal_panel`/`step_block`/`meta_box`. `build_lab_guide.py` cloned again and added `capture_panel`/`reflection`. `build_week04.py` and `build_week05.py` are the most recent generation — they introduced shape-vocabulary primitives (`add_hex`, `add_diamond`, `add_pentagon`, `add_triangle`, `add_arrow`, `add_dashed_line`, `add_doublearrow`) plus a `new_slide()` helper. `build_week05.py` is the slimmest of the new generation (13 helpers), reflecting maturation: by week 5 the patterns are stable enough that fewer ad-hoc helpers are needed.

### 4. Output naming + versioning

- Old scripts (`build_lab.py`, `build_lab_guide.py`, `build_week3.py`, `build_week03.py`) save **one** canonical filename — no version suffix. Iteration overwrites.
- New scripts (`build_week04.py`, `build_week05.py`) save `Week{NN}/Week{NN}_lab_style_v{VERSION}.pptx` with `VERSION` as a module-level constant. **Old versions are not deleted** — Week04 keeps v2..v16, Week05 keeps v1..v11 + a repaired pair. This is intentional per PROMPT.md R8 "Version every build". The accumulated PPTX count: 17 (Week 4) + 11 (Week 5) = 28 generated decks, each ~140-220 KB.

### 5. Data flow

```
                       ┌──────────────────────────────┐
                       │  Source Week{N}.pptx (prof)  │
                       └──────────────┬───────────────┘
                                      │
              ┌───────────────────────┼───────────────────────┐
              ▼                       ▼                       ▼
   text extraction via         soffice → pdftoppm        manual unzip via
   python-pptx                 (per-slide JPGs)          analysis/{N}_xml/
              │                       │                       │
              ▼                       ▼                       ▼
   analysis/{N}/text.md       analysis/{N}/slide-NN.jpg   grep <a:srgbClr>
   (verbatim bullets)         (visual fidelity check)     (palette source)
              │                       │                       │
              └───────────────────────┼───────────────────────┘
                                      ▼
                       ┌──────────────────────────────┐
                       │      DESIGN_LANGUAGE.md      │  ← derived once, then stable
                       │      PROMPT.md (behavior)    │  ← rules from past sessions
                       └──────────────┬───────────────┘
                                      ▼
                       ┌──────────────────────────────┐
                       │  build_week{NN}.py           │  ← procedural composition
                       │   (palette + helpers + per-  │
                       │    slide blocks)             │
                       └──────────────┬───────────────┘
                                      ▼
                       Week{NN}/Week{NN}_lab_style_v{N}.pptx
                                      │
                                      ▼
                  soffice --headless → PDF → pdftoppm → JPG QA
                                      │
                                      ▼
                              Visual inspection
                                      │
                                      ▼
                     User feedback → bump VERSION → rebuild
                                      │
                                      ▼
                           reports/report-YYYY-MM-DD-NN.md
                                  (provenance log)
```

### 6. Reports as provenance ledger

Nine reports under `reports/`. They are not architecture documents — they are **per-session change journals**, mandated by user's global `~/.claude/CLAUDE.md`:

| Date | # | Topic |
|------|---|---|
| 2026-05-19 | 01 | Tooling setup (Python 3.13 venv + python-pptx 1.0.2 + LibreOffice 26.2.3.2) |
| 2026-05-19 | 02 | Week03 redesign in Lab02 style — first principles |
| 2026-05-19 | 03 | Week3 networking/storage/security deck — extension to security topics |
| 2026-05-19 | 04 | Week3 hands-on lab deck — MySQL+Adminer scenario |
| 2026-05-19 | 05 | Lab 03 instructions rubric |
| 2026-05-19 | 06 | Lab 03 catch-up guide PDF |
| 2026-05-23 | 01 | `DESIGN_LANGUAGE.md` spec authored from XML reverse-engineering |
| 2026-05-23 | 02 | Week 04 redesign (38 slides, dual slide-24, 5 QA fixes batch) |
| 2026-06-01 | 01 | Week 05 v11 deep analysis — float-coord bug surfaced |

The 2026-05-19 cluster shows the system bootstrap: tooling → first deck → expansion → labs → spec extraction. After 2026-05-23 the cadence drops to per-deck reports. This is a **single-author workflow** with the report system acting as both audit log and external memory.

### 7. The lab harness (`week05_practical_work/week5_code/`)

A small Terraform module that stands up an AWS EC2 t3.medium running Amazon Linux 2, installs Docker + kind + kubectl via user-data, and provisions a single-node kind cluster from `kind.yaml`. This is **independent of the deck pipeline** — it is the runtime artifact students use for the workshop sections of the slides. Key files:

- `config.tf` — provider region `us-east-1`, `data.aws_vpc.default`.
- `ec2.tf` — `aws_instance.k8s`, `t3.medium`, 16 GB root, `iam_instance_profile = "LabInstanceProfile"` (AWS Academy Learner Lab pattern).
- `sg.tf` — two security groups (one private `127.0.0.1/32` SSH, one `0.0.0.0/0` SSH+egress). The duplicated SG names (`name = "ec2_sg"` for both modules) **will collide** if both create at once.
- `kind.yaml` — `kind.x-k8s.io/v1alpha4`, `v1.23.17` node image, port mappings 30000+30001 for NodePort.
- `kubia-manual.yaml` — Luksa "Kubernetes in Action" example pod.
- `init_kind.sh` — duplicate of EC2 user-data shell block.

The **zip + extracted-zip** at this layer creates an exact-duplicate tree at `week05_practical_work/week5_code/week5_code/`. `diff -q` confirms identity on `config.tf`. This is accidental — extracting the zip beside the source created the nesting.

Note: this Terraform targets `kind v0.11.0` and K8s `v1.23.17`. The Week04 `lab_commands.txt` references `kind v0.31.0` + K8s `v1.35.0` (Dec 2025 stable). The two harnesses are out of sync — one is the production lab, the other is reference material.

### 8. The `analysis/` archive (18 MB)

Twelve subdirectories, each capturing a different stage of source-deck inspection:

- `*_xml/` (3 dirs): unzipped OOXML used to verify palette/typography by grepping `<a:srgbClr>` and `<a:typeface>`. Decommissionable once `DESIGN_LANGUAGE.md` exists, but kept as evidence.
- `lab01/, lab02/, lab02_user/, week03/, week3_src/, week3_new/, week03_new/, lab_new/, guide_new/` (9 dirs): each holds `slide-NN.jpg` + `text.md` extracted from a specific source `.pptx`. The `text.md` files are the canonical "preserve verbatim" reference that `R1` of PROMPT.md requires — they exist so future builds can diff what was actually said in the source.

Multiple report bodies note this directory is "safe to delete". It survives because the deck-builder workflow continues to need source-comparison.

### 9. External dependencies & runtime assumptions

**Runtime stack (host):**
- macOS Darwin 25.5 (zsh).
- Python **3.13** (3.14 explicitly blocked per report 01 — beautifulsoup4 wheel availability).
- `.venv/` at project root; `which python` is overridden by the venv.

**Python packages (per report 01):**
- `python-pptx 1.0.2` — the entire output is bound to this library's shape vocabulary, OOXML serialization, and EMU conventions.
- `markitdown 0.1.5` — `.pptx` → markdown extraction for `analysis/*/text.md`.
- `Pillow 12.2.0` — declared but only used transitively.
- `lxml` — direct XML element manipulation for dashed lines, arrow heads, paragraph indentation (`marL`).
- `cairosvg` — SVG→PNG for the Python logo (mentioned in PROMPT.md, not pinned).

**Native tools:**
- **LibreOffice 26.2.3.2** (`/Applications/LibreOffice.app`, `soffice` on PATH). Used for `--headless --convert-to pdf`. **Note**: LibreOffice silently tolerates malformed OOXML (notably float coordinates inside `<a:off>` / `<a:ext>`). PowerPoint and Keynote do not. This is the dominant rendering-fidelity risk in the project — see report 2026-06-01-01.
- **Poppler / `pdftoppm`** — PDF → JPG rasterization for slide-by-slide QA.
- **Docker + kind + kubectl** — only on the EC2 lab box, not the dev machine.

**External services referenced (none called from code):**
- AWS (Terraform → EC2 + VPC + IAM via the AWS Academy Learner Lab credentials).
- Docker Hub (`luksa/kubia`, `nginx`, `mysql:8`, `postgres:16`, `alpine`).
- Blackboard Ultra (manual upload destination for `Week04_Quiz_Blackboard.txt`).
- GitHub references in source decks (`github.com/sojoudian/simple-webapp-flask`, etc.) — narrative only.

**Persistent state outside the project:**
- `~/.claude/projects/-Users-maziar-Downloads-k8s-week3/memory/*.md` — long-lived AI memory entries that capture feedback rules (palette discipline, axis-aligned connector quirk, etc.). The build behavior depends on these surviving across sessions; they are referenced from PROMPT.md by name.
- `~/.claude/CLAUDE.md` — global rules: auto-report after every substantive action; local dev ports start at 18090.

### 10. Naming conventions

| Surface | Convention | Compliance |
|---|---|---|
| Build scripts | `build_<deck>.py` | ✅ |
| Output decks (old) | `<DescriptiveName>.pptx` (`Week3_lab_style.pptx`) | ✅ |
| Output decks (new) | `Week{NN}/Week{NN}_lab_style_v{N}.pptx` | ✅ |
| Render artifacts | `analysis/<deckname>/slide-NN.jpg` | partial — also lives at `Week04/preview/`, `Week05/preview/`, `Week05/v11_jpgs/`, `Week05/src-preview/`. Convention drifted. |
| Reports | `reports/report-YYYY-MM-DD-NN-<slug>.md` | ✅ |
| Color tokens | UPPER_SNAKE; verbatim hex matches Lab02 XML | ✅ |
| Helper functions | `add_<shape>(slide, x, y, w, h, …)` | ✅ |
| Per-slide markers | `# ==…\n# SLIDE N — Title\n# ==…` | ✅ |
| Course code in user-facing text | `CLO835` (no space, no hyphen) | ✅ |
| Footer | `CLO835, Fall 2026     N / TOTAL` (5 spaces) | ✅ (encoded literally in every `whale_and_footer`) |

### 11. Design patterns

- **Shared-by-copy library**: helpers are duplicated verbatim across 6 scripts rather than imported. This is a deliberate choice ("portable, self-contained" — see DESIGN_LANGUAGE.md §10). Trade-off: any cross-cutting fix (e.g., the float-coordinate bug) must be applied 6 times.
- **Declarative-in-procedural-clothing**: each slide is essentially a literal-data construction (rectangles at fixed `Inches(...)` positions, text runs with explicit fonts/colors). There is no layout engine — every offset is hand-computed. Layout grid invariants are documented in DESIGN_LANGUAGE.md §4 and enforced by convention.
- **Two-phase visual contract**: `DESIGN_LANGUAGE.md` is the *visual* contract; `PROMPT.md` is the *behavioral* contract for the AI session that does the building. The PROMPT explicitly cross-references the DESIGN spec.
- **Verbatim preservation (R1)**: source content is sacred. The build is purely a re-skin. The `analysis/*/text.md` dumps exist so the spec can be checked against the source.
- **Native diagram rendering**: source diagrams stored as images in `.pptx` are intentionally not pulled forward as images — they are redrawn using shape primitives (`add_rect`, `add_oval`, `add_hex`, `add_diamond`, `add_pentagon`). This guarantees palette compliance but is the largest source of work per deck.
- **Terminal mockup as motif**: the dark `TERMBG` rectangle + 3 traffic-light dots + title bar + Consolas body is used 12+ times per deck. It is the visual signature alongside the whale icon.
- **Version-and-keep**: `VERSION = "v11"` constant changes per session. Old versions are kept on disk so the user can roll back. This is why Week04/ has 17 `.pptx` and Week05/ has 11.

### 12. Technical debt, inconsistencies, and risks

| Severity | Item | Where | Suggested action |
|----------|------|-------|------------------|
| **HIGH** | Float-coordinate bug — `(int + int) / 2` produces floats; python-pptx writes them as `"4288536.0"` into `<a:off>`/`<a:ext>`. LibreOffice tolerates; PowerPoint/Keynote silently mis-position to (0,0). Confirmed on Week05 slides 6, 17, 21 — slide 21 has 16 affected connectors. | All build scripts; `add_arrow`, `add_line` after arithmetic. | Patch `add_arrow`/`add_line` to coerce coordinates with `int()`; replace axis-aligned connectors with MSO_SHAPE arrows or thin filled rectangles per memory `feedback-axis-aligned-arrows`. |
| **HIGH** | 41 zero-extent connectors (footer rule on every slide) — latent failure mode in Keynote/PPT, currently rendering OK. | All `whale_and_footer` calls. | Replace `add_line` footer with a thin filled rectangle. |
| **HIGH** | `build_week3.py` and `build_week03.py` coexist with subtly different content but near-identical helpers. Confusing for future contributors. | Project root. | Rename or merge. The "3 vs 03" distinction (Networking/Storage/Security vs Layers/Copy-on-Write) is meaningful but not signposted. |
| **HIGH** | Six near-identical helper sets means any semantic bug (e.g., the float bug above) must be applied six times. | All build scripts. | Extract `clo835_design/` package with `palette.py`, `shapes.py`, `chrome.py`, `terminal.py`. Build scripts import from it. |
| MED | `week05_practical_work/week5_code/` contains its own duplicate `week5_code/` from extracting the zip beside the source. | Lab harness. | Delete the nested dir or the zip; pick one as source of truth. |
| MED | Two security groups both named `"ec2_sg"` in `sg.tf` — `dev_ssh_sg` and `ec2_sg` modules both pass `name = "ec2_sg"`. AWS will refuse the second create. | `week05_practical_work/week5_code/sg.tf`. | Set `name = "dev_ssh_sg"` on the first module. |
| MED | `init_kind.sh` is a verbatim copy of the EC2 `user_data` heredoc. Drift risk. | `week05_practical_work/week5_code/`. | Either move the script to a file and reference via `templatefile()` in `ec2.tf`, or delete the standalone script. |
| MED | kind/kubectl version mismatch between `Week04/lab_commands.txt` (kind v0.31.0, K8s v1.35.0) and `week5_code/ec2.tf` (kind v0.11.0, K8s v1.23.17). | EC2 user_data. | Pick the current versions for the live lab. |
| MED | No `.gitignore`, no source control marker. Build artifacts (386 JPGs, 28 PPTX, intermediate PDFs) accumulate alongside source. | Project root. | Add `.gitignore` listing `*.pptx`, `*.pdf`, `analysis/`, `Week*/preview/`, `Week*/v*_jpgs/`, `Week*/src-preview/`, `*.mp4`, `.venv/`. |
| MED | `Week06/` is empty — placeholder. No problem now, but means structure is per-week. The "place a new build script at root, generate into `Week{NN}/`" convention is implicit. | `Week06/`. | Document the bootstrap step in DESIGN_LANGUAGE.md §11 or add a `build_template.py`. |
| MED | `DESIGN_LANGUAGE.md` claims `analysis/` is "safe to delete" twice (reports 02 and 23-01). It has not been deleted. Reports referencing other reports should be authoritative. | `reports/`. | Either delete `analysis/` and prune the warnings, or remove the "safe to delete" claim. |
| LOW | 70 MB `Week5 - Lab Reco.mp4` in `week05_practical_work/` is outside any build pipeline and exceeds the size of the rest of the project combined. | `week05_practical_work/`. | Move to external storage or document why it's checked in. |
| LOW | `Lab03_Instructions.html` and `Lab03_Instructions.md` are content-equivalent. The `.html` uses Lato/Open Sans/Georgia (off-brand). | Root. | Either make HTML use Calibri/Consolas to match the deck system, or delete it. |
| LOW | Output JPGs live in 4 different places (`Week04/preview/`, `Week05/preview/`, `Week05/v11_jpgs/`, `Week05/src-preview/`). Convention drift. | All weeks. | Standardize on `Week{NN}/preview/v{N}-slide{NN}.jpg` per DESIGN_LANGUAGE.md §12. |
| LOW | `analysis/lab02_user/` overlaps `analysis/lab02/` — same source different extractions. Unclear which is canonical. | `analysis/`. | Pick one and delete the other. |
| LOW | No unit / integration tests. The only "test" is opening the PDF render and looking at it. Quiz balancing is hand-checked. | Whole project. | The work is artist-rendered; a snapshot test of an entire PPTX is brittle. A useful minimum is a smoke test that runs every `build_*.py` and asserts the output file exists at expected size ± 20%. |
| LOW | The "Cover" slide is reimplemented inline in every build script rather than using a `cover()` helper. ~30 LoC duplicated 5 times. | All build scripts. | Extract a `cover_slide(prs, title, subtitle, logo_path, ring=True)` helper. |
| LOW | The `.claude/scheduled_tasks.lock` is committed-style (it's in the project tree). Acquired by PID 75031 on Wed May 20 — likely stale. | `.claude/`. | Add to `.gitignore`; or delete if no Claude session is using scheduled wakeups. |

### 13. Scalability & long-term considerations

- **Per-week growth pattern**: every week the user builds a 30-40 slide deck via a ~1000-1400 LoC `build_week{NN}.py`. Without shared library extraction, by Week 12 the project will hold ~12,000 LoC of mostly-duplicated helpers.
- **Format-drift risk**: as `python-pptx` evolves, the project depends on `1.0.2`-specific behavior in 6 places. Pinning in a `requirements.txt` (currently undeclared) would prevent silent regression.
- **Viewer-fidelity risk**: the project's primary visual QA path (`soffice → pdftoppm → JPG`) does not catch the float-coordinate class of bug. A second QA pass using a real PowerPoint or Keynote install would catch them, but the user is on macOS without Microsoft Office. The pragmatic mitigation is to fix the bug class at the helper level (int-cast every coordinate write).
- **Single-author throughput ceiling**: the workflow is highly bespoke per deck. The PROMPT contract assumes 1 user + 1 AI session. Adding a second contributor would require codifying the design system as a library, not 6 copies.
- **Course-schedule coupling**: `TOTAL` and `VERSION` are constants in each build script. Per-deck pagination (`page_num` arg to `whale_and_footer`) is hand-passed. Adding/removing a slide currently requires editing both `TOTAL` and every subsequent `whale_and_footer` call. A `paginate(prs)` post-pass would be a small safety improvement.

### 14. What is *not* in the project (notable absences)

- No `requirements.txt` / `pyproject.toml` / `setup.cfg`. Dependency resolution is via the report's prose description.
- No `Makefile` or task runner. Builds are invoked with `.venv/bin/python build_week{NN}.py`.
- No `.gitignore`, no `.git/` (per `Is a git repository: false` in the env). The project is not in source control. All "rollback" is filesystem version suffixes (`v1.pptx`, `v2.pptx`, …).
- No CI configuration.
- No tests of any kind (`tests/`, `test_*.py`, `*_test.py` — none).
- No `__init__.py` — Python files at root are scripts, not modules.
- No `README.md` at root. `DESIGN_LANGUAGE.md` + `PROMPT.md` together serve that role.
- No environment file. Secrets (AWS keys, etc.) come from the Learner Lab's vended `aws_access_key_id`/`aws_secret_access_key`/`aws_session_token`, not stored.
- No application runtime — nothing in this project serves traffic. It is a build pipeline that emits binary documents.

## Results

A complete mental model of the system has been built across all 7 surface areas requested:

1. **Structure & organization** — single-author Python build pipeline; one script per deck; reports as journal; weekly per-deck output dirs.
2. **Design patterns & decisions** — share-by-copy helpers (deliberate); declarative-in-procedural construction; verbatim-preserving content contract; visual contract in markdown.
3. **Data flow** — source `.pptx` → text + JPG extraction → spec-driven Python build → `.pptx` → PDF → JPG QA → user feedback → next version.
4. **External integrations** — none from code. AWS via Terraform (lab box only). Blackboard via manual TSV upload. Docker Hub referenced as content. No API calls.
5. **Build system** — bare `python build_week{NN}.py`; LibreOffice `soffice --headless` for PDF; Poppler `pdftoppm` for JPG.
6. **Runtime assumptions** — macOS, Python 3.13 venv, LibreOffice on PATH, `whale.png` + asset library co-located with build scripts, `~/.claude/` memory survives across sessions.
7. **Naming & coding standards** — fully encoded in `DESIGN_LANGUAGE.md` §12. High compliance except JPG output location.
8. **Technical debt, inconsistencies, risks** — 19 items enumerated above. Three HIGH (float bug, zero-extent connectors, week3-vs-week03 collision) and the helper-duplication architectural debt.

**Port allocation:** N/A — no dev server.

## Issues / Notes

- The project's most load-bearing artifacts are not the build scripts but `DESIGN_LANGUAGE.md` and `PROMPT.md` together. They are the system's true source of truth. The Python scripts are derived from them.
- The float-coordinate bug surfaced in this morning's earlier deep-analysis (report 2026-06-01-01) is symptomatic of the share-by-copy helper pattern: a fix to `add_arrow` in `build_week05.py` does not fix `build_week04.py`. Extracting a library would remove a whole class of latent bugs.
- The `analysis/` directory has been marked "safe to delete" twice across prior reports but remains. It survives because the workflow continues to need source-verbatim diffing per R1 of the PROMPT contract. The "safe to delete" claim is wrong as a long-term position; it should be revised to "rebuild on demand".
- The lab harness Terraform is small but has two real bugs (duplicate SG name, K8s/kind version drift vs `lab_commands.txt`) that will bite the first student who runs it. Worth a single one-off PR.
- The project has no source-control protection. A `git init` + first commit would cost nothing and let `reports/` become the actual commit messages rather than parallel files. Given the user's `MEMORY.md` discipline, source control is the natural next step.
