# Report: Week 10 lab v4 and the Week 10 easy quiz, made the Week 09 way
**Date**: 2026-11-10
**Sequence**: #03 for the day

## Summary
The user asked for the Week 10 lab and quiz, made the same way as the Week 09 lab and quiz. I audited lab v3 against the user's standards and against lecture v10. Then I built lab v4, with 40 master commands. It passed 3 live passes and a recovery test on AWS. Two independent reviews checked it. Lab v4 shows the Released phase, so lecture v11 changes slide 37 only, to agree with the lab. The quiz has 20 easy questions, each with a live proof or a documentation proof. It passes all builder gates and the audit. 11 independent review rounds found 13, 9, 8, 7, 7, 6, 5, 3, 3, 2 and 0 defects. Round 11 checked only the two questions that changed after round 10. Terraform destroyed all AWS resources at the end.

## What Changed
Created:
- `build_week10_lab_v4.py`: the builder of the lab deck, the script, the repo files and the Blackboard text.
- `Week10/Lab_week10_v4.pptx` and `.pdf` (PowerPoint PDF, title and author set), 10 slides.
- `Week10/localMachine_v4.sh`: 40 master commands, Step 0 to 6.
- `Week10/Lab_week10_Blackboard_Submission_v4.md`: the long form of `Lab04`, 7 sections, no pledge.
- `build_week10_lecture_v11.py`, `Week10/Lecture_week10_v11.pptx` and `.pdf`: lecture v10 with slide 37 changed.
- `quiz_pool_src/q_easy20_w10.py`: the 20 questions with WHY and IF feedback.
- `quiz_pool_src/build_easy20_w10.py`: a copy of the Week 09 builder, with `q_easy20_w09` added to GATE 10. GATE 10b (the old EKS quiz) is removed.
- `quiz_pool_src/audit_easy20_w10.py`: a copy of the Week 09 audit. Since review round 2 the leak check counts words of 3 or more letters. A new check shares ties in the length guess (limit 6.0 of 20). Since round 3 a plural folds to its singular, and a trailing period is not part of a word.
- `quiz_pool_src/Quiz_W10_Easy20/`: `_Blackboard.txt` (20 rows), `_AnswerKey.txt`, `_Titles.txt`, `_QTI21.zip` (20 items and 1 manifest).

Changed:
- `~/Documents/c/r/CLO835_Fall_2026/Week10/`: `localMachine.sh` (= lab v4), `cleanup_lab10.sh` and `master-init.sh.tftpl` (one comment: "StatefulSet Pods" replaces "pets"). Not committed, not pushed.
- Memory: `project-week10-deck.md`, `project-clo835-question-pools.md`, `MEMORY.md`.

Not changed: lab v3, lecture v10, the Week 09 files, every other week.

## Technical Details

### Audit of lab v3 (the Week 09 step 1)
| No | Defect in lab v3 | Rule | Fix in v4 |
|---|---|---|---|
| A1 | The deck gate fails 4 checks: a LibreOffice PDF (Carlito and Linux Libertine fonts), the word "keeps" in a title, a blank thumbnail, and no file title | Pref 13, gate | PowerPoint PDF, new title, `finish()` |
| A2 | Lecture slide 16 shows `kubectl describe pvc data-pvc` as Lab Step 1; the lab does not have it | Lecture and lab agree | Added to Step 1 |
| A3 | Lecture slide 33 shows `kubectl delete pod dnstest` as Lab Step 5; the lab does not have it | Lecture and lab agree | Added to Step 5 |
| A4 | The lab does not practise the Released phase (lecture slides 13, 14 and takeaway 4) | Pref 15, every topic | Step 2 deletes the claim and shows Released |
| A5 | "pet", "folder", "makes" in the comments; the lecture says "Pod", "directory", "creates" | ASD-STE100, one word | Replaced |
| A6 | Step 2 title "The data outlives the Pod" is not the wording of the lecture | One word for one meaning | "The data stays after the Pod and the claim" |

The size limit stays: v3 had 37 master commands, and v4 has 40. To stay at 40, Step 4 shows `kubectl get pods,pvc,pv -o wide` in one table, and Step 5 drops the read after the POST, because the POST answer shows the write.

### Lab v4 by step
- Step 0: the cluster slide (unchanged design).
- Step 1: PV `data-pv` and claim `data-pvc`, wait for Bound, `get pv,pvc`, `describe pvc` (5 commands).
- Step 2: the writer Pod, the same data after a new Pod, then delete the Pod and the claim: `data-pv` is Released (12 commands).
- Step 3: the local-path provisioner and the StorageClass `standard` (3 commands).
- Step 4: the headless Service and the StatefulSet `kubia`; one table shows Retain/Released against Delete/Bound (5 commands).
- Step 5: POST, delete `kubia-0`, read the same data, DNS A and SRV lookups, delete `dnstest` (11 commands).
- Step 6: `cleanup_lab10.sh`, `get pods,pvc,pv`, `terraform destroy` (2 master commands).

### Live test on AWS
- Account 499333804030, role voclabs, us-east-1. The user approved AWS use in the prompt. The credentials came from the local AWS configuration; no key was copied.
- `terraform apply` in a sandbox copy of the repo folder, with the student answers `Maziar` and `yes`: 15 resources.
- Nodes: Kubernetes v1.35.10, Ubuntu 26.04.1, containerd 2.2.2, the same as the slide samples.
- The message of the day and `cleanup_lab10.sh` on the master agreed with the repo.
- The harness `instrument.py` turns `localMachine.sh` into a script that prints each command and its exit code.

### Quiz design
- 20 questions: 1 to 10 from the lecture, 11 to 20 from the lab.
- Each key has a proof. The scratchpad folder `w10lab` holds the logs:
  - `pass1.log`: the lab output (Q5, Q12 to Q18).
  - `probe.log` P0 to P11: hostPath on two nodes, RWO with two Pods on one node, a 2Gi claim on a 5Gi PV, an empty class name, WaitForFirstConsumer, a smaller request, the DNS name in another namespace, a partition, a scale down, no provisioner, and a new IP address.
  - `probe2.log` P12: a PV pinned to a cordoned node (Q11).
  - `probe3.log` P13: a write through a hostPath mount with no readOnly field (Q1).
- No question repeats an earlier pool (GATE 10, 8 pools, including Quiz 3 Q85 to Q100 on volumes).
- I removed a question on two StorageClasses before review, because it gave away the empty class name question.

## Results

### Lab
| Run | Commands | Non-zero exits | Note |
|---|---|---|---|
| Pass 1, full speed | 40 | 0 | All comments agree with the output |
| Pass 2, 3 s between commands | 40 | 0 | Same results |
| Recovery: stop half way, then `cleanup_lab10.sh` | 16 + clean-up | 0 | No Pod, claim, PV, class, provisioner namespace or proxy is left |
| Pass 3, the final repo `localMachine.sh` and `cleanup_lab10.sh` | 40 | 0 | After I removed the probe objects; the first try of pass 3 failed on a probe Pod named `dnstest` |

- Deck gate (`gate_week12.deck_checks`, PowerPoint PDF): lab v4 0 failures, lecture v11 0 failures. I viewed every changed page.
- The commands of the last builds are identical to the pass 3 commands (only comments and titles changed).

### Quiz
- Builder: GATE 1-7, 8, 8b, 9, 10, 11, 12, 13 and 14 pass. The key holds A 5, B 5, C 5, D 5. The longest run of one letter is 2.
- Audit: exit 0, 0 leaks, 0 pairs at risk. A guess by the longest option gets 4.8 of 20, and by the shortest 4.5 of 20 (ties shared).
- GATE 8c: each letter is the key 2 or 3 times in each half; no alternation of 5, no ABCD run, no repeated block of 3.
- The cue scripts of the reviewers (rounds 5, 7 and 8) give 4.0 to 5.7 of 20 for every strategy.
- Upload: the `.txt` file goes into a test through "Upload questions from file"; the QTI 2.1 package goes into a question bank.

### AWS
- `terraform destroy` with the student answers: 15 resources destroyed, exit 0.
- After the destroy: 0 instances in any state, and 0 `week10` security groups. The Terraform state files are only in the scratchpad sandbox, not in the repo.

## Review
| Round | Reviewer | MUST-FIX | SHOULD-FIX | Main findings |
|---|---|---|---|---|
| Lab 1 | independent | 2 | 7 | Lecture slide 37 said "Not in the lab: the Released phase"; `git pull` in an old clone; comments on FailedBinding, Released and serviceName; "pets" |
| Lab 2 | independent | 0 | 3 | Two comments with no verb or a vague "it"; the Step 2 title |
| Quiz 1 | independent | 5 | 8 | IF texts rotated in Q7; Q5 needed "the provisioner still runs"; give-aways between Q5, Q9, Q12, Q15, Q16 and Q17 |
| Quiz 2 | independent | 3 | 6 | Q3 had a second correct option under WaitForFirstConsumer; Q1 key repeated the stem; "always shortest" got 35 % |
| Quiz 3 | independent | 2 | 6 | Q1 key restated the stem; Q3 used a fact the course does not teach (the capacity of the claim) |
| Quiz 4 | independent | 1 | 6 | Q3 stem conflicted with the troubleshooting table; letter pattern by halves (new GATE 8c) |
| Quiz 5 | independent | 2 | 5 | Two options with one result in Q11; an option in Q3 that implied the key; ABCD runs (GATE 8c extended) |
| Quiz 6 | independent | 1 | 5 | Q9 key was the only option without "Kubernetes"; "but" only in wrong options; Q18 option A implied D |
| Quiz 7 | independent | 1 | 4 | Q18 option D removable from the stem; Q13 time order; idioms in the feedback |
| Quiz 8 | independent | 1 | 2 | Q18 option B implied D; a convergence cue in Q1, Q6 and Q17 |
| Quiz 9 | independent | 0 | 3 | Q18 option D repeated a Week 09 distractor; "Ready" only in keys; "print" and "removed" |
| Quiz 10 | independent | 0 | 2 | Q10 option A contradicted itself; Q18 option D was literally true for a certificate |
| Quiz 11 | independent | 0 | 0 | A full check of Q10 and Q18 (the only questions changed after round 10), and of their give-aways with the other 18 questions and the Week 09 pool |

After round 9, I also changed Q5 D and Q10 A, because the round 5 cue script gave 6.4 of 20 for the convergence strategy. After that change, every cue script gives 5.7 of 20 or less.

Live proofs added during the review: P12 (cordoned node, Q11), P13 (write through a hostPath mount, Q1), P14 and P15 (a 5Gi PV of the class fast for a 2Gi claim, Q3; a second claim stays Pending).

## Issues / Notes
1. OPEN, the user decides: lab slide 3 says `cd CLO835_Fall_2026 && git pull && cd Week10`. The repo history was rewritten on 2026-11-05, so `git pull` fails in a clone made before that date. The line comes from the shared engine `lab_kubeadm.py` and is in every lab. I did not change it.
2. NOT DONE, by the design of the Week 09 model: the terminal captions show no step number; the storageclass sample shows 4 columns, the same as lecture slide 23.
3. Lecture topics that lab v4 does not practise, because of the 40-command limit: a Pending claim with WaitForFirstConsumer, the claim retention policy, the scale down in reverse order, access modes other than ReadWriteOnce, and the SRV name form. Lecture slide 37 labels the update settings and the optional topics as not in the lab. The quiz tests some of these topics (Q9, Q10, Q2) with live proofs.
4. Lecture slides 21 and 23 say that the provisioner "makes" a directory; the lab says "creates". I changed only slide 37 of the lecture.
5. GitHub still has lab v3. The user does the commit and the push.
6. Images with only the tag `latest`: `maziar/alpine-curl`, `maziar/kubia-pet` (a known item).
7. The probe left objects on the cluster before the first pass 3. I removed them, and pass 3 ran again on a clean cluster. A first patch script of the quiz stopped on one text match and wrote nothing; the second run applied all changes.
8. Blackboard: the upload file cannot shuffle options, and Ultra sets 1 point for each question. Use Bulk Edit Points. Show only the grade until all students finish. After the quiz, read the statistics of each question.
9. No local server ran, so no port is used.
