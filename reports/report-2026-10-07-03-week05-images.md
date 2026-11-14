# Report: Week 05 - One Kubia Image, Working Guestbook Tag
**Date**: 2026-10-07
**Sequence**: #03 for the day

## Summary
The lecture taught `maziar/kubia`, but the lab told the student to run
`luksa/kubia`. The lecture also used `gcr.io/google_samples/gb-frontend:v3`, which
the registry no longer publishes. Both decks and the lab code now use
`maziar/kubia`, and the guestbook tag moves to `v5`. The decks are rebuilt as `v3`.

## What Changed

### Decks - `Week05/`
| File | Note |
|------|------|
| `lecture_week05_v3.pptx` + `.pdf` | NEW. 30 slides, 29 visible |
| `Lab_week05_v3.pptx` + `.pdf` | NEW. 11 slides |

The `v1` and `v2` files stay in place (PROMPT.md R8).

Edits:
- Lab slide 5, command: `k run kubia --image luksa/kubia` -> `--image maziar/kubia`
- Lab slide 5, manifest: `- image: luksa/kubia` -> `- image: maziar/kubia`
- Lecture slide 23: `gcr.io/google_samples/gb-frontend:v3` -> `:v5`

### Lab code - `week05_practical_work/week5_code/`
- `localMachine.sh` line 48: `--image luksa/kubia` -> `--image maziar/kubia`
- `kubia-manual.yaml` line 9: `- image: luksa/kubia` -> `- image: maziar/kubia`

## Technical Details

Why the guestbook tag changed, and not the image. The registry answers:

```
https://gcr.io/v2/google_samples/gb-frontend/tags/list
  -> ["sample-public-image-v5-5be2e51", "v5"]
```

`v3` returns HTTP 404. `v5` is the only usable tag, so the slide keeps the same
example and the same teaching, with a tag that pulls.

Why `maziar/kubia` and not `luksa/kubia`. `maziar/kubia` is your own repository.
It is public, it has 275 pulls, and the last push was 2026-06-03. The lecture
already taught it on four slides. One image across the lecture, the lab deck and
the lab code removes the contradiction.

## Results

Image list after the change:

| Deck | Slide | Image |
|------|-------|-------|
| lecture | 11, 12, 13, 14 | `maziar/kubia` |
| lecture | 15, 25, 29 | `alpine:3.15` |
| lecture | 21, 28 | `nginx` |
| lecture | 23 | `gcr.io/google_samples/gb-frontend:v5` |
| lab | 4 | `nginx` |
| lab | 5 | `maziar/kubia` |
| lab | 6 | `alpine` |
| lab | 7 | `alpine:3.14` |

Checks:
- `luksa` leftovers: 0 in both decks and in the lab code
- `gb-frontend:v3` leftovers: 0
- `maziar/kubia:latest` on Docker Hub: HTTP 200
- `gcr.io/google_samples/gb-frontend` tag `v5`: present
- footers wrong: 0 | Consolas bad characters: 0 | off-palette: 0 | floats: 0
- fonts: Calibri and Consolas only
- `bash -n localMachine.sh`: passes

## Issues / Notes
- `maziar/kubia` publishes `amd64` only. The lab nodes are `m5.large`, so the lab
  works. A student on an Apple Silicon laptop needs emulation to run it locally.
- There is no git repository reference in either deck. Neither deck contains a URL.
- The lab is still not launched on AWS. No credentials are available.
