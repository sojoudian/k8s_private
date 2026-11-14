# Report: The preferences behind the Week 06 lecture and lab fixes
**Date**: 2026-10-27
**Sequence**: #07 for the day

## Summary
The user asked me to dig deeper into the Week 06 fixes and to list all the
preferences. I read the user prompts of every saved session (524 prompts, 2026-09-08
to 2026-10-27), the Week 05 and Week 06 audit and repair reports, `PROMPT.md`, the
two deck memories, the public repo memory and the lab builder docstrings. I list 44
preferences in 6 groups, with the source of each one. 33 of them are not in
`~/.claude/PREFERENCES.md`. I also found 6 conflicts between the sources. No file
changed, apart from this report.

## What Changed
- Created this report. No other file changed.

## Technical Details

### Sources read
- The user prompts, extracted from 7 transcripts in
  `~/.claude/projects/-Users-maziar-Downloads-k8s-week3/`. The key prompts:
  - 2026-10-14: "now tell me is week06 lecture is up to my standards? (like what
    we did for the week05)", then "fix all of these".
  - 2026-10-14: "we are repeating a lot of points and facts, right?", then "only
    repeat the point if needed, not more that two times. even in situations which
    one example or one time mentioning a point is enough, do it only one time."
  - 2026-10-27: "set up the cluster using the terafform of the lab week06 and
    test the codes and then destroy the infra".
  - 2026-10-27: "we had this rule to not using the luksa/kubia and using the
    maziar/kubia", and "not only that many locations in the pptpx and pdf and
    everything else too!".
  - 2026-10-27: "never we should use any other github account or dockerhub account
    rather than the maziar for docker and sojoudian for the github".
- Reports: 10-07-01 (Week 05 standards audit, 14 defects), 10-07-02, 10-08-02 to
  10-08-05 (Week 05 lab alignment, repo folder, live test), 10-14-01 (Week 06
  lecture audit, 14 defects), 10-14-02 (v6 repair), 10-14-04 (Blackboard text),
  10-14-06 and 10-14-07 (repetition), 10-27-03 (live quiz test), 10-27-05 (accounts).
- `PROMPT.md` (rules R1 to R9), memories `project-week05-deck`,
  `project-week06-deck`, `project-clo835-fall2026-repo`.
- Docstrings of `build_week06_lab_v1.py` and `build_week06_lab_v2.py`. No report
  covers the lab v1 and v2 work, and no transcript of that work is saved.

### A. Process
| # | Preference | Source | In PREFERENCES.md |
|---|---|---|---|
| A1 | "Up to my standards" means the same checks as the Week 05 audit. | prompt 10-14 | no |
| A2 | Audit first, read-only. Fix only after "fix all of these". | prompts 10-07, 10-14 | partly (scope) |
| A3 | Fix all the defects of the audit, not a selection. | prompt 10-14 | no |
| A4 | Bump the version. Never overwrite a delivered file. | R8, memory | yes |
| A5 | A builder is guarded. It reads its input deck and never writes it. | reports 10-14-02, 10-14-07 | no |
| A6 | Write a report after each action. | CLAUDE.md | yes |

### B. Lecture: mechanics
| # | Preference | Source | In PREFERENCES.md |
|---|---|---|---|
| B1 | Canvas 13.333 x 7.5 in, 16:9. | PROMPT.md, audits | no |
| B2 | Calibri and Consolas only. | PROMPT.md, audits | no |
| B3 | Integer coordinates only, 0 floats. | memory | yes |
| B4 | Whale and footer `CLO835, Fall 2026     N / TOTAL` on every slide. | PROMPT.md | no |
| B5 | The footer total is the slide count of THIS deck, in sequence (no `/39`, no `/71`). | audits D1, item 4 | no |
| B6 | A slide hidden in the source stays hidden. | audit item 5 | no |
| B7 | House palette only. | R6 | yes |
| B8 | A small file: about 1 MB, like Week 01 v5 (1.37 MB). Drop the image part of a removed picture. | audit item 11 | no |

### C. Lecture: images
| # | Preference | Source | In PREFERENCES.md |
|---|---|---|---|
| C1 | No third-party screenshot. Draw a native house diagram or a house terminal. | audits D14, item 6 | no |
| C2 | No watermark of another author. | audit item 7 | no |
| C3 | No image below 110 DPI, and no WMF file. | audit item 9 | no |
| C4 | No shape over the title band or the footer band. | audit item 8 | no |
| C5 | Read the images too. A text extract misses an image (the removed Ingress API was in a picture). | memory | yes |

### D. Lecture: content
| # | Preference | Source | In PREFERENCES.md |
|---|---|---|---|
| D1 | Every command runs as shown. No EN DASH, curly quote or zero-width space in a Consolas command. | audits D3, D7, items 1 and 10 | no |
| D2 | Every command uses the current syntax (`kubectl exec POD -- cmd`) and a current API (`networking.k8s.io/v1`, not `extensions/v1beta1`). | audit items 1 to 3, v6 repair | no |
| D3 | One image everywhere: `maziar/kubia`. | prompt 10-27, audit item 13 | yes |
| D4 | No Docker Hub account but `maziar`, no GitHub account but `sojoudian`. | prompt 10-27 | no (memory only) |
| D5 | The Course Outline follows the schedule: Study Week 8, exam 11, ConfigMaps 12, HPA 14, project 15. | audit item 12 | no |
| D6 | Bullets in ASD-STE100: no "b/w", "fwding", "a bunch of". | v6 repair | partly (language) |
| D7 | Every fact is correct ("the API server creates a Service", not kube-proxy). | v6 repair | partly (verify) |
| D8 | A bullet describes what the slide shows, not the colours of an old image. | v6 repair | no |
| D9 | State a point one time. A second time only when needed. Never three times. | prompt 10-14 | no |
| D10 | No two slides with the same title, and no bullet word for word on two slides. | report 10-14-07 | no |
| D11 | No fragment card (a card that is a piece of another card). | audit item 14 | no |
| D12 | The lecture and the lab do not contradict each other (kind against kubeadm). | Week 04 finding | no |

### E. Lab
| # | Preference | Source | In PREFERENCES.md |
|---|---|---|---|
| E1 | The lab practises the lecture. Every lecture topic has a workshop step. | report 10-08-03 | no |
| E2 | The lab design copies the Week 05 lab: title, prerequisites, cluster and end slides. One step is one terminal slide. | lab v1 docstring | no |
| E3 | The deck and `localMachine.sh` come from one content list, so they cannot differ. Each script step names its slide. | lab v1 docstring, report 10-08-04 | no |
| E4 | The repo folder has the 8 files of Week 04, with the same names, order and wording. No README. | report 10-08-04 | no |
| E5 | `localMachine.sh` calls no script that the master does not have. `master-init` writes `cleanup_labNN.sh` to the master. | memory | no |
| E6 | kubeadm cluster on EC2: 1 master and 2 workers, Ubuntu 26.04, Kubernetes v1.35, Flannel, `m5.large`, NIC at MTU 1500. | memory | no (and conflicts, see below) |
| E7 | Check each step against the real kubeadm v1.35 behaviour (CoreDNS has no Service cache, so `sleep 2`). | lab v2 docstring | no |
| E8 | Record the change-cause after each `set image`. | lab v2 docstring | no |
| E9 | Test the whole lab live on AWS, run every command, then destroy the infrastructure. | prompts 10-08, 10-27 | yes (destroy) |
| E10 | Write a Blackboard submission text for each lab, in the "Lab02 - 2.5%" form. | prompt 10-14 | no |
| E11 | The image must have the tag that the lab needs (`v1`, `v2`; `v9` must not exist). | report 10-27-05 | no |

### F. Answers
| # | Preference | Source | In PREFERENCES.md |
|---|---|---|---|
| F1 | Answer short and 100 % correct. | prompts 10-27 | yes |
| F2 | "Mostly" is not acceptable. Meet the rule 100 %. | prompt 10-27 | no |

### Conflicts found
1. `PROMPT.md` R1 says keep the source text verbatim and never fix a typo. The Week
   05 and Week 06 repairs rewrote bullets and fixed commands, because you said "fix
   all of these". R1 is older.
2. `PROMPT.md` lists `ALERT_RED = E74C3C`. The Week 05 audit counts `E74C3C` as off
   palette and names `FF5F56` as the house red.
3. `PROMPT.md` names `Week04/Week04_v02_02.pptx` as the reference deck.
   `PREFERENCES.md` and memory name `week01/Week01_lecture_style_v5.pptx`.
4. `PREFERENCES.md` section 10 says "Use kind on EC2 for the course work". The
   Week 04, 05 and 06 labs use kubeadm on EC2.
5. `lecture_week05_v3` counts visible slides in the footer. `Week06_lecture_style_v7`
   counts every slide. A hidden slide makes the count go from 11 to 13.
6. `PROMPT.md` says "Week 8 is BREAK" and "Week 9 = EKS". The 2026-07-15 schedule
   says Study Week at 8, and memory says students have no EKS.

## Results
- 44 preferences found: 6 process, 8 mechanics, 5 images, 12 content, 11 lab, 2 answers.
- 33 of the 44 are not in `~/.claude/PREFERENCES.md`. 3 more are there only in part. (Corrected: the first version of this report said 22 and 5.)
- 6 conflicts between the sources.

## Issues / Notes
- No transcript and no report holds the Week 06 lab v1 and v2 sessions. E2, E3, E7
  and E8 come from the builder docstrings only.
- I did not change `PREFERENCES.md`, `PROMPT.md` or any memory file.
