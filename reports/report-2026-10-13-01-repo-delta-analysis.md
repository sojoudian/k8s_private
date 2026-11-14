# Report: Repository Analysis, Delta over 2026-10-08
**Date**: 2026-10-13
**Sequence**: #01 for the day

## Summary
Nothing changed in `k8s_week3` since my 2026-10-08 run, apart from the files that
run produced. The Week 05 work is in place and clean. Two things outside the
folder did move, and both matter: the public repository was relocated, and the
local clone at its new path is six commits behind GitHub and holds no Week 04 or
Week 05.

## The repository today
| Measure | 2026-10-08 | Now |
|---|--:|--:|
| Size | 1.8 GB | 1.8 GB |
| Files, excluding `.venv` | 1 788 | 1 799 |
| Decks | 170 | 171 |
| Reports | 101 | 106 |
| Root Python files | 20 | 21 |

The whole delta is the 2026-10-08 output: `Lab_week05_v4.pptx` and its PDF,
`build_week05_lab_v4.py`, five reports, the architecture report, and the updated
Week 05 lab code. No file was touched between 10-08 and today, apart from two
`.DS_Store` files that Finder wrote.

## What is correct now
| Item | State |
|---|---|
| `Week05/Lab_week05_v4.pptx` | 18 slides, footers `1 / 18` to `18 / 18`, 0 floats, Calibri and Consolas only |
| `Week05/lecture_week05_v3.pptx` | 30 slides, 0 floats, 0 bad characters in a Consolas run |
| `week03/Week03_lecture_style_v2.pptx` | 15 slides, the "lowest layer" error is corrected |
| The three question pools | 100 rows each, 0 problems, longest-option 25 to 27 % |
| `CLO835_Hard20_Blackboard.txt` | 20 rows, 0 problems |
| Week 05 lab shell files | `bash -n` passes, 0 non-ASCII bytes |

`FFBD2E` appears in the Week 05 decks and is NOT a defect. It is the amber dot of
the house terminal title bar, and Week 01, Week 02, Week 03 and Week 12 all use it.

## Two findings outside this folder

### 1. The public repository moved
It was at `~/Documents/c/r/Oct08/CLO835_Fall_2026`. That path is gone. The
repository is now at `~/Documents/c/r/CLO835_Fall_2026`.

### 2. That local clone is six commits behind GitHub
| Side | State |
|---|---|
| GitHub `origin/master` | `1b808f6`, holds Week02, Week03, **Week04**, **Week05** and `assignment-1` |
| The local clone | `27e247f`, holds Week01, Week02, Week03 only |

The six missing commits are `ef0c6cf`, `7ebaa39`, `7cb7050`, `0bce7bb`, `05014af`
and `1b808f6`.

**The risk.** GitHub holds the only copy of the tested Week 04 and Week 05 labs.
The local folder does not. A commit made in that folder and pushed could roll the
remote back.

**The fix.** Run `git pull` in `~/Documents/c/r/CLO835_Fall_2026` before any work.

### 3. Two Week 05 code sets exist, and they differ
| Set | Path | State |
|---|---|---|
| A | `k8s_week3/week05_practical_work/week5_code/` | An earlier draft. It has a `README.md`, an `ssh_cidr` variable, and `rs.yaml` and `sidecar.yaml` as files. **It does NOT write `cleanup_lab05.sh` to the master.** |
| B | GitHub `Week05/` | The student copy. It matches the Week 04 style and carries the cleanup fix. It ran on AWS three times. |

Set B is the one that works. Set A would fail at Step 13.

## Defects that are still open
Re-tested today, every one reproduces.

| Defect | State |
|---|---|
| `Week04/Week04_lab_style_v16.pptx` | 175 float coordinates, off-palette `556F88` |
| `Week04/FINAL/Week04.pptx` | 26 slides, footer `/38`, teaches kind on 7 slides |
| `Week04/FINAL/Lab_week04.pptx` | 13 slides, footer jumps from `1 / 38` to `27 / 38` |
| `Week06/Week06_lecture_style_v5.pptx` | 41 slides, footer `/71` |
| `finalWork/Week04.pptx` | 26 slides, footer `/38` |
| `finalWork/Week06_Part_A.pptx` and `_B` | footer `/71`, one slide each with no footer |
| `Week04/localMachine.sh` on GitHub | calls `./cleanup_lab04.sh`, which never reaches the master |
| `CLO835_Final_Exam_Blackboard.txt` | the correct option is the longest in 53 % of its MC rows |
| `week01/Week01_Quiz_Blackboard.txt` | Q14, Q15 and Q16 still need the slide |
| `build_week08.py`, `build_week09.py` | the folder names are off by one; the assets exist |
| `assemble_week13.py`, `assemble_week14.py` | point at a dead scratchpad path |

## Run safety, unchanged
Ten of the 21 root builders save a deck at import, with no `__main__` guard:
`build_lab.py`, `build_lab_guide.py`, `build_week3.py`, `build_week03.py`,
`build_week04.py`, `build_week05.py`, `build_week06.py`, `build_week07.py`,
`build_week08.py`, `build_week09.py`. Run them in a sandbox only.

`build_week05_lab_v4.py`, added on 10-08, is guarded.

## Waste, unchanged
| Item | Size |
|---|---|
| `week02/terraform-vm/.terraform` | 765 MB |
| `.venv` | 198 MB |
| Superseded `Week04_lab_style*` decks | 16 |
| Superseded `Week05_lab_style*` decks | 26 |
| Home IP in `week02/terraform-vm` | 2 files |

## Issues / Notes
No file was changed by this analysis.
