# Report: CLO835 standards file and the memory update
**Date**: 2026-11-10
**Sequence**: #04 for the day

## Summary
The user asked for two things. First, update the memory with all the fixes of this work. Second, write a deep and detailed standard for the lectures, the labs, the quizzes and the practical work in the AWS Learner Lab. I wrote `CLO835_STANDARDS.md` (version 1.1, Parts A to H and an appendix of commands) from all the rule sources and from the work of 2026-11-09 and 2026-11-10. I verified the environment facts with read-only and dry-run AWS commands, and the image tags on Docker Hub. I created no AWS resource. I copied the tools that the standard needs from the volatile scratchpad into `tools/`. An independent reviewer checked the standards file (see Review).

## What Changed
Created:
- `CLO835_STANDARDS.md`: the standard, version 1.
- `tools/export_pdf.sh`: the PowerPoint PDF export (container folder `clo835export`).
- `tools/deck_pipe.sh`: export, PDF info, deck gate and page sheets. It needs `SHEETS=<folder>`.
- `tools/rungate.py`, `tools/sheet.py`: the gate runner and the page sheets.
- `tools/instrument.py`: the lab runner that prints each command and its exit code.
- `tools/quiz_cue_sim.py`: a new cue simulation with 13 strategies and a pass-or-fail limit of 30 % (it replaces the copy of the round 5 script).
- Memory: `reference-clo835-standards.md`, `feedback-quiz-review-lessons.md`, `feedback-live-test-protocol.md`.

Changed (memory):
- `project-week07-deck.md`: the old decks in the Trash; lab v3 has no live test.
- `project-week10-deck.md`: Blackboard item `Lab06 - 2.5%`, the defect in the v4 Blackboard text, the review counts, the destroy, the old decks in the Trash.
- `project-clo835-question-pools.md`: the 11 review rounds, GATE 8c, the final cue scores.
- `project-learner-lab-ec2-limits.md`: the dry-run results of 2026-11-10.
- `project-clo835-lab-numbering.md`: Lab Week 10 = `Lab06 - 2.5%`.
- `reference-preferences-file.md`: a pointer to the standards file.
- `MEMORY.md`: 4 new index lines, and the Week 10 line.

Not changed: every deck, lab, quiz and repo file.

## Technical Details

### Sources read
CLAUDE.md (global and project), PREFERENCES.md (15 sections), PROMPT.md (2026-05; its soffice render and its old file names are superseded), the memory index and the memory files on decks, labs, quizzes, AWS, repos and Blackboard, `gate_week12.py` (32 deck checks, the BANNED list, the PALETTE, the lab, Blackboard and live checks), `build2.py` (GATE 1 to 7), `build_easy20_w10.py` (GATE 8 to 14 with 8b and 8c), `audit_easy20_w10.py`, and the reports of 2026-11-10.

### AWS checks (no resource created)
| Check | Result |
|---|---|
| Key pairs | `Maziar` (6e:c1:64:a7:ab:56:de:c9:00:3f:f9:56:7e:d0:92:57) and `vockey` |
| `~/.ssh/mazSeneca.pub` MD5 fingerprint | 6e:c1:64:a7:ab:56:de:c9:00:3f:f9:56:7e:d0:92:57 (a match) |
| AMI | `ami-0547ecbf0e9b4aeb5`, ubuntu-resolute-26.04-amd64-server-20261104.1 |
| Dry-run t3.medium, m5.large, r8i.large, c7i.large | DryRunOperation (allowed) |
| Dry-run m5.xlarge, t3.xlarge, r8i.xlarge | UnauthorizedOperation (blocked) |
| `max-instances` attribute | 20 (the lab limit of 9 running instances from 2026-10-27 stays) |
| `aws eks list-clusters` | allowed, no cluster |

### Other checks
- Docker Hub: all 11 `maziar/*` images that the course repo names exist with the named tags (table in Part F2).
- GitHub: `git ls-remote` gives `ad93eb8` for HEAD and master. The local clone has uncommitted changes in Week07 (4 files) and Week10 (3 files).

### Defect found during this work
`Week10/Lab_week10_Blackboard_Submission_v4.md` says "control-plane node" 4 times and "control-plane pods" one time. The Week 12 v5 text and the gate (`blackboard: no control-plane node`, and the BANNED word list) ask for "master node" and "control-plane Pods". I gave the user the v4 text earlier today. I did not change it, because this prompt did not ask for it. It is open item 2 of Part H.

## Results
- `CLO835_STANDARDS.md`: Parts A (how to work), B (lectures), C (labs), D (quizzes), E (AWS practical work), F (repos, accounts, security), G (Blackboard and the schedule), H (open items), and the appendix.
- The tools pass `bash -n` and `py_compile`.

## Review
An independent reviewer checked version 1 against its sources. It found 10 MUST-FIX and 10 SHOULD-FIX items. Version 1.1 fixes all 20:

| No | Finding | Fix in v1.1 |
|---|---|---|
| 1 | C3 allowed a non-zero exit of a final grep; the live gate allows none | Each command exits 0 |
| 2 | The lab, Blackboard and live checks of `gate_week12.py` are hard-coded for Week 12 | C9 says so, and lists the checks to do by hand |
| 3 | GATE 7 of build2 is not called by the easy-quiz builder | D8 says GATE 1-6, and GATE 10 does the job of GATE 7 |
| 4 | `quiz_cue_sim.py` did not compute most or fewest words, and had no limit | New tool: 13 strategies, exit 1 above 30 %; Week 10 quiz passes (max 5.5 of 20) |
| 5 | "NOT in bold" is impossible in the upload file | D2: no negative stem |
| 6 | "Small numbers in words" was wider than the gate | A1 states the scope of the gate |
| 7 | The appendix rebuilt delivered files; quiz tools have no guard | A5 lists the unguarded tools; the appendix is a template for a new version with `--no-repo` |
| 8 | `terraform validate` in the repo writes `.terraform/` | Run it in the sandbox |
| 9 | The rule to keep a hidden source slide was missing | B1 |
| 10 | H8 named the wrong Flannel weeks | Weeks 04, 05, 06, 07, 09, 10, 14 (checked with grep) |
| 11 | The replaced PROMPT.md rules were not named | A list in the header, and the reference deck week01 v5 |
| 12 | Omissions | A2, A3, A7, B1, B3, D12, G4 (newer grading form) |
| 13 | Two numbers had no source | Ready time from report 2026-10-31-04; line height marked as measured |
| 14 | D7 run limit | `run_limit=3` |
| 15 | C5 cleanup end | The check differs by week (examples) |
| 16 | F1 "never push" | Push only when a prompt names it |
| 17 | Part H omissions | H9 to H11 |
| 18 | The appendix runner wrote to the project root | It writes to the sandbox |
| 19 | Two scan lists | One list in F3 |
| 20 | Language | Long sentences split into lists; phrasal verbs and "prints", "refuses" replaced |

After the fixes, a sentence check finds no sentence above 25 words (the banned-word list is a list).

## Issues / Notes
1. The Blackboard v4 text defect above.
2. The Week 07 lab v3 still has no live test. The AWS lab is up, but the prompt asked for standards and memory, not for this test.
3. The tools in `tools/` are copies; the originals in the scratchpad are volatile.
4. No local server ran.
