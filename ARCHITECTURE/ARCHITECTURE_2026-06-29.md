# CLO835 Deck-Builder — Exhaustive Architectural Analysis
**Generated:** 2026-06-29 · **Method:** 15-agent workflow (10 domain readers → 4 cross-cutting analysts → 1 completeness critic) + firsthand binary-artifact audit of 16 shipped decks.
**Confidence:** High on code/convention/IaC/env (every file read); High on shipped-deck reality (binaries opened & scanned, not inferred).

---

## 0. What this project actually is

Not an application — a **single-author, batch, file-driven content-generation pipeline** that programmatically re-authors a university Kubernetes course's PowerPoint decks (Seneca Polytechnic, **CLO835, Fall 2026**, Prof. Maziar) into a consistent house visual language ("Lab02 design language") using the `python-pptx` library.

There is **no server, runtime, network surface, database, or shared library.** The "architecture" is a *convention*: a prose governance layer (3 Markdown specs) that **8 standalone, top-to-bottom imperative Python scripts** are each *supposed* to obey **by copy-paste**. The defining architectural property is **share-by-copy**: a ~200-line palette+helper "engine" is physically duplicated in all 8 builders, so the system has the *appearance* of a shared design system but the *mechanics* of 8 independent forks.

---

## 1. Project structure & organization

### File census (verified, excludes `.venv`)
| Type | Count | Role |
|---|---|---|
| `.jpg` | 520 | source-slide renders + per-version QA previews (throwaway) |
| `.png` | 87 | embedded figure crops + logos |
| `.pdf` | 84 | LibreOffice "proof" exports paired 1:1 with each `.pptx` |
| `.pptx` | 76 | **the actual deliverables** (least-inspected surface) |
| `.xml`/`.rels` | 137/112 | unzipped OOXML dumps under `analysis/*_xml/` |
| `.md` | 30 | 19 reports + 3 governance specs + lab/announcement content |
| `.tf` | 8 | Week-5 Terraform IaC (loose + nested duplicate) |
| `.py` | 8 | **the 8 builder scripts** (the entire codebase) |
| `.yaml`/`.txt`/`.sh`/`.svg` | 4/3/2/2 | kind/Pod manifests, quiz/runbook, init scripts, vector logos |
| `.zip`/`.mp4`/`.pyc`/`.lock` | 1/1/1/1 | lab bundle, 72MB recording, stale bytecode, dead scheduler lock |

### Layout
```
k8s_week3/
├── build_week{3,03,04,05,06,07}.py, build_lab.py, build_lab_guide.py   # 8 builders (root)
├── PROMPT.md, DESIGN_LANGUAGE.md, ARCHITECTURE_ANALYSIS_PROMPT.md       # governance "constitution"
├── whale.png, docker_logo.jpg                                          # shared brand assets
├── analysis/         # INPUT pipeline: <deck>/{slide-NN.jpg, text.md}, <deck>_xml/ (unzipped OOXML)
├── Week04..Week08/   # OUTPUT folders: WeekNN_<track>_style_vN.pptx + .pdf, assets/, preview/
├── week05_practical_work/week5_code/   # the only runnable code: Terraform + kind + shell
├── old_assessments/  # prior-semester Blackboard screenshots (PNG, reference-only)
├── reports/          # 19 auto-generated session reports (de-facto commit log)
└── .venv/            # Python 3.13.13 (homebrew, arm64); NO requirements.txt/pyproject/git
```

---

## 2. The design-system engine (architectural heart)

Each builder re-declares the same engine inline. Canonical reference: `build_week05.py`.

- **Palette** — 24 `UPPER_SNAKE` `RGBColor` tokens, hex-verified verbatim against `Lab02.pptx` OOXML: `BLUE #1FA8E0` (accent/titles), `SLATE #37465A`, `BODY #3F3F3F` ("never pure black"), `MUTED #868686`, `CARD_BG #F4F7FB`, terminal set (`TERMBG #2A2A2A`, traffic-light `TERM_RED/YEL/GRN`, `TERM_CYAN` commands, `TERM_ERR` errors), semantic `GOAL_GREEN`/`ALERT_RED`, and a 6-stop `STEPS[]` blue→slate ramp (`STEPS[0]==BLUE`, `STEPS[5]==SLATE`).
- **Typography** — exactly two faces, never a third: `FONT_SANS='Calibri'`, `FONT_MONO='Consolas'` (evidence: 459 Consolas + 447 Calibri runs across 18 Lab02 slides, no third typeface).
- **Canvas** — `13.333×7.5in` (16:9), blank layout `slide_layouts[6]`, every shape absolutely positioned (no placeholders). Fixed anchors: left margin `0.55`, title `y=0.40`, content guard `y≤6.70`, footer rule `y=7.05`, whale at `(0.45,6.85)`.
- **Coordinate-safety primitives** — the project's signature engineering artifact, born of a real bug:
  - `_i(v)` int-coerces any float at every shape-creation call site.
  - `_sanitize_coords(prs)` walks the `spTree` before save and integer-coerces any surviving non-integer `a:off/a:ext/chOff/chExt`.
  - **Why:** Python `/` yields a float; `python-pptx` serializes a float EMU as e.g. `"4288536.0"`; **PowerPoint & Keynote parse that as 0 and teleport the shape to (0,0)**. LibreOffice tolerates it — so the project's own QA renderer is *blind* to the bug.
- **Helper library** — thin wrappers over `python-pptx`: `add_text/add_rect/add_rounded_rect/add_oval/add_line`, `title()`, `whale_and_footer()`, `terminal()` (dark macOS-window code mockup with traffic-light dots + run-tuple body), plus generation-specific helpers (`bullets()` multi-level hierarchy, `embed()` aspect-fit letterbox, `auto_term()` heuristic syntax-color, `divider()` LAB section breaks).
- **Patterns:** design-token constants; run-tuple rich-text model (`list[paragraph[(text,color)]]`); per-slide local closures for bespoke diagrams; raw `lxml`/OOXML injection for what `python-pptx` lacks (`a:prstDash` dashes, `a:tailEnd` arrowheads, `marL/indent` bullet hierarchy, `show='0'` hide); `# SLIDE N` banner comments; hardcoded page numbers/`TOTAL`.

---

## 3. The builder fleet — generational lineage

8 builders, 8,044 LoC total, evolving by cloning-and-extending:

| Gen | Builders | Output | Coord guard | Adds |
|---|---|---|---|---|
| **1** | `build_week03 → build_week3 → build_lab → build_lab_guide` | unversioned root `.pptx` | ❌ | base engine, lab/guide helpers (`goal_panel`, `step_block`, `reflection`) |
| **2** | `build_week04` (1389 LoC) | `Week04/..vN.pptx` | ❌ | shape vocabulary (`add_hex/diamond/pentagon/triangle/arrow`), native diagrams |
| **2** | `build_week05` (1192 LoC) | `Week05/..vN.pptx` | ✅ (origin) | slimmed engine; **the `_i`/`_sanitize_coords` fix** |
| **3** | `build_week06` (1305 LoC) | `Week06/..vN.pptx` | ✅ | `bullets()` hierarchy, `embed()`, `auto_term()`, `divider()`, `hide()` |
| **3** | `build_week07` (448 LoC) | `Week07/..vN.pptx` | ✅ | `yaml_terminal()`, `annot_card()`; lightest builder |

**Fork hazards:** `build_week3.py` vs `build_week03.py` differ only by a zero-pad but cover different topics (Networking/Storage/Security vs Layers/CoW+lab) — `build_week3.py`'s `.pptx` isn't even in the repo (silent abandonment). `build_lab.py` vs `build_lab_guide.py` is a second fork pair. The "identical" engine has measurably **drifted** between copies: `add_rounded_rect` radius_ratio `0.06`(w05)/`0.10`(w06)/`0.05`(spec); `bullet_list()`(■) vs `bullets()`(▪/–/•); param `slide`→`s`; `total` required→defaulted.

---

## 4. Data flow & logic flow (end-to-end)

```
Source WeekNN.pptx (professor)
  │  ── markitdown ───────────► analysis/<deck>/text.md   (verbatim text = R1 "source of truth")
  │  ── soffice + pdftoppm ───► analysis/<deck>/slide-NN.jpg   (catches image/SmartArt content text-extract misses)
  │  ── unzip ────────────────► analysis/<deck>_xml/   (exact palette/font/position XML)
  ▼
GOVERNANCE: PROMPT.md (behavior R1–R9) + DESIGN_LANGUAGE.md (visual contract)
  ▼
build_weekNN.py  — author transcribes verbatim text into Python string literals;
                   composes slides via the copy-pasted engine; _i() guards coords
  ▼
prs.save() ──► WeekNN/WeekNN_<track>_style_vN.pptx   (+ paired .pdf proof, out-of-band)
  ▼
QA: soffice --headless --convert-to pdf → pdftoppm -jpeg → fresh-eyes subagent review (1→6 agents)
  ▼
feedback → fix IN THE SCRIPT → bump VERSION → re-save vN+1 → reports/report-YYYY-MM-DD-NN.md + AI memory
```

Every stage is a **hand-run shell command** — no Makefile, no orchestration, no `__main__`/argparse. The "real" artifact (`.pptx`, in-venv) and the "proof" artifact (`.pdf/.jpg`, out-of-venv LibreOffice/Poppler) come from two entirely separate toolchains a human keeps in sync.

---

## 5. Governance layer ("constitution")

- **PROMPT.md** — behavioral contract pasted at session start. 9 non-negotiable rules: **R1 preserve original text verbatim** (no rephrasing/invented content; typos like "Hierachy" kept), R2 recolor-only reference matching, R3 targeted changes only, R4 ask-before-guessing, **R5 connector zero-extent quirk** (use `MSO_SHAPE` arrows for axis-aligned, connectors only for diagonals), R6 stay-in-palette, R7 pod-icon = Python logo, **R8 version every build**, R9 visual QA in the user's real viewer.
- **DESIGN_LANGUAGE.md** (~39KB) — the visual system: canvas, palette, typography, 17 reusable components, 22 slide templates each mapped to a precedent `file:slide`, voice/tone, and §13 **explicit anti-patterns** ("tried and walked back": mono-caps kickers, dark content panels, 4:3, >2 fonts).
- **ARCHITECTURE_ANALYSIS_PROMPT.md** — the meta-prompt driving analyses like this one.
- **Circular authority:** the spec says it is "the single source of truth" but also "the build_*.py files are the ground truth — read them," and "when code disagrees with docs, code wins." Both specs are **already stale**: ARCHITECTURE_ANALYSIS_PROMPT.md asserts only `build_week05.py` has the coord guard (reality: 3 builders); DESIGN_LANGUAGE.md §0 says it derives from "the four build_*.py generators" (there are now 8).

---

## 6. External integrations, dependencies & runtime

- **Interpreter:** homebrew CPython **3.13.13** (arm64). Python 3.14 fails (no `beautifulsoup4` 3.14 wheel) — an undocumented landmine.
- **Imported by builders:** only `python-pptx 1.0.2` + `lxml 6.1.1` + stdlib `os/re/random`. Everything else is CLI-only.
- **CLI tools (out-of-band):** `markitdown 0.1.5` (deck→md extraction, drags in a ~50MB ML stack: `magika` 27MB arm64 binary + `onnxruntime`/`numpy`/`protobuf`), `cairosvg` (SVG→PNG logos/icons), `Pillow 12.2.0`.
- **System binaries (undocumented in-repo):** LibreOffice `soffice` 26.2.3.2, Poppler `pdftoppm` 26.04.0, Cairo, `unzip`.
- **Target platforms:** Blackboard Ultra LMS (deck/quiz/announcement uploads), Keynote/PowerPoint (author's viewers), AWS (Week-5 lab).

---

## 7. Build / deployment / reproduction posture

- **No dependency manifest** (no `requirements.txt`/`pyproject`/lockfile anywhere) — environment reproducible only by tribal prose in one report; transitive versions unpinned.
- **No version control** (no `.git`) — de-facto VCS is a monotonic `vN` filename chain (Week05 → v26, Week04 → v16), each paired with a `.pdf`, never pruned, plus 19 prose reports as commit messages. "Canonical = highest N" is the only (fragile) marker.
- **Machine lock-in:** `.venv` shebangs hardcode `/Users/maziar/Downloads/k8s_week3/.venv/bin/python`; all asset paths are bare relative strings (cwd must = repo root); no `__file__` anchoring, no `os.makedirs`; Weeks 05/06/07 reach cross-folder into `Week04/` for the K8s logo.

---

## 8. The IaC lab subsystem (`week05_practical_work/week5_code`)

The only runnable code: Terraform provisions one AWS EC2 `t3.medium` (Amazon Linux 2, default VPC, `us-east-1`), cloud-init installs Docker + kind v0.11.0 + kubectl, then `kind create cluster` and a sample `kubia` Pod. **Real defects (verified):**
- **SSH open to `0.0.0.0/0`** (the `127.0.0.1/32` SG is pointless since both attach and SG rules are additive).
- **Both SG modules named `"ec2_sg"`** → AWS name collision.
- **Invisible U+200B zero-width space** trailing `ec2.tf:33` and `kind.yaml:5` → breaks `--config kind.yaml` and the `kindest/node` image digest.
- **`kind.yaml` never delivered to the host**, yet cloud-init runs `kind create cluster --config kind.yaml` → fails.
- **`week5.pub` referenced but absent** → `terraform apply` fails out of the box.
- **kind/K8s version drift:** ec2.tf v0.11.0/v1.23.17 vs nested copy v1.19.11 vs `lab_commands.txt` v0.31.0/v1.35.0. Triplicated (loose + zip + nested).
- ✅ No hardcoded cloud secrets (auth delegated to `LabInstanceProfile`).

**Assessment content:** `Lab03_Instructions.md/.html` (a MySQL+Adminer hardening lab; the `.html` has silently diverged from the `.md`), Blackboard quiz as a fragile header-less tab-delimited TSV + asterisk answer key, `lab_commands.txt` runbook with time-rotting facts, and `old_assessments/*.png` revealing the full course arc (Docker → Dockerfile/EC2 → kind → EKS).

---

## 9. EMPIRICAL BINARY AUDIT — generator vs shipped reality (firsthand, the corrective layer)

The code-only analysis made claims about the decks that opening the binaries **partially refutes**. Verified by scanning 16 shipped `.pptx`:

| Deck | Slides | Float EMU | Hidden | Dim | Finding |
|---|---|---|---|---|---|
| `Week04_lab_style_v16` (canonical lab) | 38 | **175 / 5480** | — | 16:9 | **Float bug LIVE & shipped** (diagram-heavy) |
| `new_Week3` / `Week3_Hands_On_Lab` / `Lab03_Guide` / `Week03_lab_style` | 14/8/18/14 | **0** | — | 16:9 | **Gen-1 unguarded outputs are CLEAN** |
| `Week05_lab_style_v26` (canonical) | **29** | 0 | — | 16:9 | builder emits **v12/39 slides** → divergent |
| `lecture_week05` (canonical) | **29** | 0 | [4] | 16:9 | hand-tuned, not script-generated |
| `Week06_lecture_style_v3` | 41 | 0 | **[13]** | 16:9 | slide 13 correctly hidden |
| `Week06_lecture_style_v5` (canonical) | 41 | 0 | **[]** | 16:9 | **slide-13 un-hide regression CONFIRMED live** |
| `Week06_lab_style_v4` (canonical) | 31 | 0 | [18] | 16:9 | correct |
| `Week08 — EKS` (raw source) | 33 | 0 | [2] | **16:9** | source is **already 16:9**, not 4:3 |
| `Week04_v02_02` == `Week04_v02_01` | 38 | 0 | — | 16:9 | **byte-identical** (md5 `c698cbaf…`); image-based reference, **not** builder-reproducible |
| `Week3.pptx` (original source) | 43 | 0 | [26,27] | **10×7.5 (4:3)** | source aspect ratio is per-week, not uniform |

**Three corrections to the multi-agent findings:**
1. ❌ "All 5 unguarded builders ship broken decks" is **false**. Only `Week04` actually ships floats (175); the 4 gen-1 outputs are empirically clean. Risk is real but **localized to diagram-heavy decks**.
2. ✅ **NEW live defect:** every footer in the 29-slide canonical Week05 decks reads **"N / 39"** (denominator from the 39-slide builder era) — a visible, shipped error invisible to code-only analysis.
3. ✅ The MEMORY-only **slide-13 un-hide regression is confirmed real** in the shipped canonical `Week06_lecture_style_v5`.
4. ✅ Correction to a *risk* claim: the `ASPECT` dicts (flagged as silent-distortion risk) are **currently accurate** — 0 mismatches across 53+1 entries vs real pixel dims.

---

## 10. Technical debt, inconsistencies & risks (ranked)

**HIGH**
1. **Share-by-copy engine** duplicated across 8 builders (no shared module) — root cause of #2–#4; a `clo835_design/` package was recommended in 2026-06-01 and never built.
2. **Coordinate-safety guard in only 3 of 8 builders** — the v12 fix couldn't propagate; `Week04` lab deck demonstrably ships 175 floats.
3. **Generator–artifact divergence:** `build_week06.py` is STALE (emits old 71-slide combined deck; hand-split v5/v4 are canonical and would be destroyed by re-running); `Week04_v02_02` (reference) and `lecture_week05` are not script-reproducible. "The script is the source of truth" is broken.
4. **QA loop structurally blind** to the two defect classes that actually occur: float-EMU teleport (LibreOffice tolerates) and slide-visibility `show='0'` regressions.
5. **No git, no manifest, no tests, no CI**; machine/cwd lock-in.
6. **IaC defects** (§8): world-open SSH, SG name collision, U+200B corruption, missing `kind.yaml`/`week5.pub`.
7. **Week05 footer `/39`-on-29-slides** live content bug (newly found).

**MEDIUM** — version sprawl with no canonical marker (Week05 v1–v26; Week06 tracks version-misaligned v3 vs v1); fork pairs; helper-API drift; hardcoded relative paths; kind/K8s version drift; stale governance docs; `Lab03` md/html desync; mixed coord-unit contract in `build_week07` (`yaml_terminal`/`annot_card` take bare inches).

**LOW** — committed `.pyc`, 5× `.DS_Store`, empty "untitled folder", misplaced Week05 "Repaired" decks + an 883KB unrelated AI-video frame inside `Week04/`, dead imports/constants (`Emu`, `qn`, `BLACK`, `GOAL_GREEN`, `DOCKER_LOGO`), `TERM_ORANGE` defined via walrus-in-literal, typo'd filenames, stale `.claude/scheduled_tasks.lock`.

---

## 11. Naming conventions & coding standards

**Rigorously consistent:** `UPPER_SNAKE` palette tokens (byte-identical across builders), `lower_snake` helpers, `_underscore` privates, `Inches()/Pt()` everywhere, keyword-only styling args, module docstrings, `# SLIDE N` banners, and the flawlessly-followed `report-YYYY-MM-DD-NN-slug.md` auto-report mandate.

**Drifts:** `build_week3` vs `build_week03` filename collision; zero-padding inconsistent at every layer (`WeekN` source vs `WeekNN` output; `slide-7` vs `slide-07`); gen-1 writes unversioned root files vs gen-2/3 versioned per-week dirs; banner style hyphen→em-dash (older builders violate the spec's own em-dash rule); **no linter/formatter/type-checker/git/CI** — every convention is author-discipline only.

---

## 12. Scalability & long-term considerations

The pipeline **scales by cloning, not abstraction** — each new week is a linear multiplier of ~200 duplicated engine lines + accreted version artifacts (projected ~12k LoC by Week 12). **Week08 EKS** is the inflection point: a raw 33-slide source with no builder; under the current pattern it becomes the 9th fork of `build_week07.py`. The single-author/single-machine assumptions (hardcoded `/Users/maziar` paths, local `.venv`, arm64 `magika`, `.DS_Store`) mean a second author cannot reproduce the pipeline, and the original author increasingly cannot safely *regenerate* canonical decks (which are now hand-edited).

---

## 13. Prioritized recommendations

1. **Extract `clo835_design/`** (`theme.py`/`shapes.py`/`chrome.py`/`terminal.py`/`coord.py`) and `import` it everywhere — kills duplication and back-fills the coord guard to all builders in one move. Do this **before** Week08/09.
2. **Re-save `Week04_lab_style_v16` through `_sanitize_coords`** to fix the 175 shipped floats; fix the **Week05 `/39` footer**; apply the pending **Week06 slide-13 re-hide**.
3. **`git init` + `.gitignore`** (`.venv/`, `__pycache__/`, `.DS_Store`, render PDFs/JPGs, `.mp4`); **add `requirements.txt`** pinning python-pptx/lxml/Pillow/cairosvg/markitdown + the Python-3.13 + system-binary notes.
4. **Add a `validate.py` QA gate** the JPG loop can't provide: assert `slide_count == TOTAL`, zero non-integer EMU, footer denominator == `len(slides)`, and a `show='0'` snapshot diff. Wrap the 4-stage pipeline in a `Makefile`/CLI.
5. **De-machine builders:** `BASE_DIR = Path(__file__).resolve().parent`, `os.makedirs(..., exist_ok=True)`, single shared `assets/` dir.
6. **Record a per-week `CANONICAL.md`** (which artifact is source-of-truth; freeze or reconcile stale builders); resolve the two fork pairs; delete dead code/cruft.
7. **Fix the Week-5 IaC** (strip U+200B, restrict SSH CIDR, distinct SG names, write `kind.yaml` in user_data, add `week5.pub`/`ssh-keygen` note, converge versions).
8. **Refresh stale docs** (ARCHITECTURE_ANALYSIS_PROMPT.md "only week05 guarded" → 3; DESIGN_LANGUAGE.md "four generators" → 8); generate `Lab03_Instructions.html` from the `.md`.
9. **Longer-term:** migrate to a **data-driven deck spec** (per-week YAML: title + verbatim bullets + treatment) consumed by one renderer that auto-numbers footers — separating R1-protected content from rendering. Build Week08/09 on the new package as the proof case.

---

## 14. Coverage & confidence

- **Read in full:** all 8 builders, all 3 governance specs, all 19 reports, all 7 IaC files, all lab/assessment/instruction content, `.venv` manifest, full directory tree.
- **Verified firsthand (binary):** 16 shipped `.pptx` (slide counts, float-EMU scan, hidden-slide state, dimensions, footer denominators, byte-identity, ASPECT-dict accuracy).
- **Not done (deliberate):** did **not** execute any builder (would overwrite the user's canonical `WeekNN/` outputs) — reproducibility is asserted from code, not a live smoke-run. Did not OCR `old_assessments` PNGs or parse the 72MB lab video.
