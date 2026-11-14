# Report: Week 12 lecture and lab, check against all preferences

**Date**: 2026-10-31
**Sequence**: #11 for the day

## Summary
The answer is no. I checked `Lecture_week12_v4` and `Lab_week12_v3` against each line of
`~/.claude/PREFERENCES.md`. The check found 12 defects and 1 open item. The check is read-only, so
I changed no deck, no script and no repository file. The defects are small against the 25 of
report #09, but your rule is 100 %, and "mostly" is not acceptable.

## Correction of report #10
Report #10 says that all 25 defects are fixed. This statement is too strong:
- L9 stays in one lab comment. See D9.
- L17 is not complete. See D3 and D4.
- Report #10 says that the slide 8 commands ran. My test added a header to that manifest. See D5.

The audit of report #09 also missed D1. My audit script printed these lines, but I cut the output
at 150 characters, so I did not read them.

## What Changed
- Created this report.
- Updated the memory file `project-week12-deck.md` and its line in `MEMORY.md`.

## Lecture defects

| No | Slide | Defect | Rule |
|--:|--:|---|---|
| D1 | 10, 11, 14, 15 | 3 bullets are word for word on two slides: "A 2-step process:" (10, 14), "Inject the ConfigMap into the Pod" (10, 11), "Inject the Secret into the Pod" (14, 15). | Section 14 |
| D2 | 13, 15, 18 | The etcd point is on three slides. Slides 13 and 15 both say "not encrypted". Slide 18 says it again that etcd stores the Secret. | Section 14, "never three times" |
| D3 | 2, 4, 5, 6, 8 | One meaning has more than one word: "command-line" and "command line"; "arguments", "options" and "parameters"; "executable" and "process"; "Pod manifest" and "Pod description". | Section 1 |
| D4 | 3 | "Week 5: K8s- PODs, ReplicaSets" has `PODs` and `K8s-`. The other boxes use `K8s –`. Week 10 v9 has the same label. | Section 1, L17 |
| D5 | 6, 8 | Each `pod.yaml` has no `apiVersion` and no `metadata`, so `kubectl apply` refuses it as shown. Slide 8 names a real image, and my test added the header. | Section 14, "run as shown" |
| D6 | 4, 5, 8 | Slide 4: no bullet says what `nginx.conf` shows. Slide 5: "Docker reminder" repeats the title. Slide 8: "Problems:" has 1 item, and "are difficult" is not clear. | Section 14 |
| D7 | 14 | "The manifest must hold base64 encoded data" is at the level of Imperative and Declarative. It applies to Declarative only, so it must be one level lower. | Section 6, hierarchy |
| D8 | PDFs | Both PDFs use Carlito and Linux Libertine G, not Calibri and Consolas. Linux Libertine G is a proportional serif, so terminal columns do not align (lecture slide 16, lab slide 3). The `.pptx` files are correct. | Section 13 |

## Lab defects

| No | Slide | Defect | Rule |
|--:|--:|---|---|
| D9 | 7 | The comment "The volume is in memory (tmpfs), never on disk." is the wrong form of L9. Slide 8 of the same lab reads the Secret from etcd. | Section 14, facts, agreement |
| D10 | 7 | 2 lecture items have no practice: `envFrom` with `secretRef` (lecture slide 15), and `kubectl create secret generic --from-file` (lecture slide 14). | Section 15, every topic |
| D11 | Blackboard | I did not build the rubric table before release. 5 lines say "display its contents", but the lab has only `cat > file`, so the cell for the command is empty. | Section 12, rubric table |
| D12 | 3, lecture 5 | 3 commands did not run as shown: `terraform output public_ips`, `terraform output private_ips` and the `docker run` of lecture slide 5. | Section 15, every command |

## Open item
- **GitHub holds lab v2 until you push.** Until then, `git pull` on lab slide 3 gives the old lab
  with `busybox` and "Lab 12". The lab is not final for students before that push.

## Outside these two decks
- The outlines of Weeks 01-03, 06, 13 and 14 disagree with Week 12 on Weeks 14 and 15.
- The syllabus row 12/9 says Helm. You stated that Week 15 is the project presentation.
- The Blackboard name of this lab is your decision.

## What passes

**Both decks**
- Canvas 13.333 x 7.5 in, Calibri and Consolas only in the `.pptx`, 0 float coordinates.
- Whale and footer on every slide, `N / 21` and `N / 10` in sequence.
- No hidden slide, because the source has none. No shape on the title band or the footer band.
- 0.18 MB and 0.07 MB. No third-party image, no watermark, no image below 110 DPI.
- No two slides have the same title.
- All builders have the `__main__` guard. `build_week12_lecture_v4.py` reads `Week12_v3.pptx` and does not write it.

**Facts and images**
- `maziar/fortune:args`, `maziar/fortune:env`, `maziar/kubia:v1` and `maziar/alpine-curl:latest` exist on Docker Hub.
- The registry shows `maziar/fortune:args` with Entrypoint `/bin/fortuneloop.sh` and Cmd `10`. Slides 5 and 7 and lab slide 4 agree.
- All 6 links of slide 21 return 200.

**Lab**
- 10 slides, Step 0 to 6, 42 commands, 1 workshop. Each script step names its slide.
- The deck and `localMachine.sh` come from one content list.
- 8 files, `m5.large`, Ubuntu 26.04, v1.35.10, MTU 1500, `cleanup_lab12.sh` on the master.
- 2 live passes, a recovery test and a full destroy. Report #10 has the detail.
- No `/Users/`, `.ssh/`, user name, `luksa`, `busybox`, `nano` or AWS key in the folder.

## Technical Details
- Rules: all 15 sections of `~/.claude/PREFERENCES.md`, read line by line.
- Deck text: read with `prs.slides`, with no output cut.
- PDF fonts: `pdffonts`. Registry: the Docker Hub tag API and the image config blob.
- Lab coverage: a search of `localMachine.sh` for each form that the lecture shows.
- I created no cloud resource for this check.

## Issues / Notes
- D8 also affects the PDFs of earlier weeks. I checked `Week10/Lab_week10_v3.pdf`, and it has the same fonts.
- D5 on slide 6 is a generic form with `some/image`. It is not meant to run, but the rule does not make an exception.
- D11 also applies to the Week 10 text, which has 3 such lines.
- The Docker daemon did not answer on this computer, so slide 5 stays untested.
