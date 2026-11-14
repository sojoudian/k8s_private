# Report: Week 05 Lab Revised Against the Lecture
**Date**: 2026-10-08
**Sequence**: #03 for the day

## Summary
The Week 05 lab now covers the Week 05 lecture. Seven slides are added and one is
extended, so the deck grows from 11 slides to 18. The lab script grows from 9
steps to 14, and each step names the slide it belongs to. Two manifests are added.
Every `kubectl` verb that appears on a slide now exists in the script.

## What Changed

### Deck
| File | Note |
|------|------|
| `Week05/Lab_week05_v4.pptx` + `.pdf` | NEW. 18 slides. |

`Lab_week05_v2.pptx` and `v3.pptx` are untouched.

### Lab code - `week05_practical_work/week5_code/`
| File | Change |
|------|--------|
| `localMachine.sh` | Rewritten. 14 steps, each one naming its slide. |
| `sidecar.yaml` | NEW. The two-container Pod. |
| `rs.yaml` | NEW. The ReplicaSet written by hand. |
| `cleanup_lab05.sh` | Removes `kubia-rs`, `web-with-sidecar` and `nginx-http` as well. |
| `README.md` | The step table now maps each step to a slide. |

### Builder
| File | Purpose |
|------|---------|
| `build_week05_lab_v4.py` | Guarded. Reads v3, writes v4. |

## Technical Details

### The gaps that are now closed

| Gap | Lecture slides | New lab slide |
|---|---|---|
| Sidecar, a multi-container Pod | 7, 9, 10 | 6, "Two containers in one Pod" |
| Label selectors | 18, 19, 22, 23 | 8, "Labels and selectors" |
| Writing a ReplicaSet manifest | 21, 22, 23, 25 | 10, "Creating a ReplicaSet from a descriptor" |
| `kubectl explain` | 11 | 5, extended with two lines |
| Rollout commands | 27 | 12, "Rolling out a new version" |
| Rollback | 27 | 14, "Rollback - history and undo" |
| NodePort, reaching the Pod | — | 16, "Reach the Pod from your browser" |
| Cleaning up | — | 17, "Clean up" |

Slide 9 of v3 showed the rollout OUTPUT with no command. It is now slide 13 and is
retitled "Rollout in progress - two ReplicaSets". The commands sit on slide 12.

### The new slide order

| # | Slide | State |
|--:|---|---|
| 1 | LAB | kept |
| 2 | Deployment of K8s Pod - Prerequisites | kept |
| 3 | Preparing the cluster | kept |
| 4 | Niginx pod deployment | kept |
| 5 | Create pod manifest | **extended** with `kubectl explain` |
| 6 | Two containers in one Pod | **new** |
| 7 | Retrieving logs - Pingpong | kept |
| 8 | Labels and selectors | **new** |
| 9 | Can we scale the pod? | kept |
| 10 | Creating a ReplicaSet from a descriptor | **new** |
| 11 | Scaling | kept |
| 12 | Rolling out a new version | **new** |
| 13 | Rollout in progress - two ReplicaSets | **retitled** |
| 14 | Rollback - history and undo | **new** |
| 15 | Maintaining the desired state - Resilience | kept |
| 16 | Reach the Pod from your browser | **new** |
| 17 | Clean up | **new** |
| 18 | Workshop 1 - The End | kept |

### One design decision
`rs.yaml` selects `app: kubia-rs`, not `app: kubia`. Step 5 labels the existing
`kubia` pod with `app=kubia`. A ReplicaSet with the same selector would adopt
that pod and start only two more. The distinct label keeps the two steps
independent.

### Layout
A rendered terminal line is about 0.212 in tall at 11 pt with 1.15 line spacing,
and the frame leaves 4.58 in. The builder drops to 9 pt when a block runs longer
than 21 lines, so no block overflows its frame. This was measured on a render,
not assumed.

## Results

Deck `Lab_week05_v4.pptx`:
- 18 slides, all visible, canvas 13.333 in
- footers `1 / 18` to `18 / 18`, none missing
- fonts: Calibri and Consolas only
- off-palette colours: 0
- float coordinates: 0
- non-ASCII characters in a Consolas run: 0
- renders to 18 PDF pages

Lab code:
- `bash -n` passes on all three shell files
- 0 non-ASCII bytes
- `terraform init` and `validate` pass
- Every `kubectl` verb on a slide exists in `localMachine.sh`:
  `apply, create, delete, explain, expose, get, label, logs, patch,
  port-forward, rollout, run, scale, set`

## Issues / Notes
- The lab was not launched on AWS. No credentials are available.
- `Lab_week05_v3.pptx` stays on disk. v4 is the one to use.
