# Report: Is the Week 05 Lab Aligned with the Week 05 Lecture?
**Date**: 2026-10-08
**Sequence**: #02 for the day

## Summary
Mostly yes. The lab practises the core of the lecture, and there is no
contradiction of the kind that Week 04 carries. Five topics are taught and never
practised, and three steps are in the lab CODE but on no lab SLIDE. Nothing was
changed.

## Files compared
| File | Slides |
|---|--:|
| `Week05/lecture_week05_v3.pptx` | 30 (29 visible) |
| `Week05/Lab_week05_v3.pptx` | 11 |
| `week05_practical_work/week5_code/localMachine.sh` | 9 steps |

## What is aligned

| Item | Evidence |
|---|---|
| Subject | Both run Pods, then ReplicaSets, then Deployments |
| The lecture agenda promises the lab | Slide 2: "Create pods, deployments, scale them, observe self-healing, and roll forward / back" |
| Images | Both use `maziar/kubia`, `nginx` and `alpine`. One kubia image everywhere. |
| Platform | The lecture terminal prompts read `ubuntu@masternode`. The lab builds that exact cluster. |
| No kind contradiction | The 13 hits of "kind" in the lecture are the YAML key `kind:`, never the tool. The lab says "No kind. No Docker in Docker." |
| Namespaces | Lecture slide 30 teaches them. The lab uses `kubectl create ns` and `-n pingpong`. |
| A Pod does not scale | Lecture slides 16, 20 and 24 state it. The lab proves it: `kubectl scale pod` fails, then a Deployment works. |
| Rolling update | Lecture slide 27 explains the new ReplicaSet scaling up while the old one scales down. Lab slide 9 shows exactly that output. |

## Taught in the lecture, never practised in the lab

| Topic | Lecture slides | In the lab |
|---|---|---|
| Label selectors | 18, 19, 22, 23 | The lab never writes a selector and never uses `-l` |
| Sidecar, a multi-container Pod | 7, 9, 10 | Every Pod in the lab holds one container |
| Writing a ReplicaSet manifest | 21, 22, 23, 25 | The lab only observes the ReplicaSet a Deployment makes |
| `kubectl explain` | 11 | Never used |
| `kubectl create -f` | 13 | The lab uses `kubectl apply -f` instead |

## In the lab CODE, on no lab SLIDE

`localMachine.sh` has 9 steps. The deck has 8 content slides.

| Step in the code | On a slide? |
|---|---|
| Step 6, `kubectl set image`, `rollout status`, `rollout history`, `rollout undo` | **No.** Slide 9 is titled "Rolling out a new version" and shows only the OUTPUT. It shows no command. |
| Step 8, `kubectl expose` plus `kubectl patch` to pin NodePort 30000 | **No slide at all.** This is the step that proves the security group rule and the MTU fix. |
| Step 1 verification, `kubectl wait` and `curl localhost:8080` | **No.** The slide shows `port-forward` but not the check. |

The deck contains zero occurrences of `expose`, `set image`, `rollout` and `patch`.

## Verdict
The lab does not contradict the lecture. It under-covers it. A student who
follows the slides alone cannot roll out a new version, because the command is
missing, and never reaches the application from a browser.

## Issues / Notes
No file was changed. The fix, if you want it, is three slides: a rollout command
slide, a NodePort slide, and a label selector exercise.
