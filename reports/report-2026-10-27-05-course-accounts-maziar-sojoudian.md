# Report: Course material moved to the maziar and sojoudian accounts
**Date**: 2026-10-27
**Sequence**: #05 for the day

## Summary
The user asked for `maziar/kubia` in the Week 06 lab, and for no Docker Hub account
other than `maziar` and no GitHub account other than `sojoudian`. The user chose
"push both" and "Everything, tools too". The Week 06 lab, 10 canonical decks, the
public course repo copy and two quizzes now name only the two accounts. All Docker
Hub work is done and public. The GitHub forks and one new repository still need a
GitHub API login. Until then, 9 deck links and the Flannel URL point at repositories
that do not exist yet.

## What Changed

### Pushed (outward)
- `sojoudian/kubia`, commit `430135f`: an optional `VERSION` setting in `app.js`,
  `ARG`/`ENV VERSION` in `Dockerfile`, a README section. The CI run passed.
- Docker Hub `maziar/kubia:v1` and `maziar/kubia:v2`, built for amd64 and arm64.
- Docker Hub copies, all public:
  `maziar/fortune:env`, `maziar/fortune:args`, `maziar/alpine-git:latest`,
  `maziar/alpine-curl:latest`, `maziar/hpa-example:latest`, `maziar/aws-cli:latest`,
  `maziar/trivy:0.76.1`, `maziar/trivy:latest`, `maziar/gb-frontend:v5`,
  `maziar/flannel:v0.28.10`, `maziar/flannel-cni-plugin:v1.9.1-flannel3`,
  `maziar/metrics-server:v0.7.1`.

### Created in this folder
- `build_week06_lab_v3.py`, `Week06/Lab_week06_v3.pptx` (31 slides),
  `Week06/Lab_week06_Blackboard_Submission_v3.md`.
- `retarget_accounts.py` (guarded). It wrote the next version of 10 decks:
  `week01/Week01_lecture_style_v6.pptx`, `Week04/FINAL/Lab_week04_v2.pptx`,
  `Week05/lecture_week05_v4.pptx`, `Week07/Week07_lab_style_v4.pptx`,
  `Week09/Week08_lecture_style_v4.pptx`, `Week10/Week09_lecture_style_v5.pptx`,
  `Week12/Week12_v2.pptx`, `Week12/Week12_lab_v2.pptx`,
  `week14/Week14_lecture_style_v10.pptx`, `week14/Week14_lab_style_v11.pptx`.
- `quiz_pool_src/Week01_Pool_v2_Blackboard.txt` and its key,
  `week01/Week01_Pool_v2_Blackboard.txt`,
  `quiz_pool_src/Quiz_W01W02_Easy20/Quiz_W01W02_Easy20_v2_*` (txt, key, QTI 2.1 ZIP).

### Modified in this folder
- `quiz_pool_src/q2_w01.py`: 2 options, `jenkins/jenkins` to `maziar/kubia`.
- `quiz_pool_src/q_easy20.py`: 1 stem and 1 feedback line.
- `quiz_pool_src/build2.py`, `build_easy20.py`, `audit_easy20.py`: the W01 output
  names carry `_v2`, so no delivered quiz file is overwritten.
- `week03/cleanup_lab03.sh`: `aquasec/trivy` to `maziar/trivy`.

### Modified in the public repo copy, NOT committed
`~/Documents/c/r/CLO835_Fall_2026`:
- `Week06/localMachine.sh` (written by `build_week06_lab_v3.py --script`).
- `Week03/bootstrap.sh`, `Week03/localMachine.sh`, `Week03/cleanup_lab03.sh`: Trivy.
- `Week04`, `Week05`, `Week06` `master-init.sh.tftpl`: the Flannel URL.

### Prepared, NOT pushed
- `scratchpad/clo835-mirrors/`: a local git repository, commit `5156c38`. It holds
  `flannel/v0.28.10/kube-flannel.yml`, `metrics-server/v0.7.1/components.yaml`,
  `README.md` and the Apache 2.0 `LICENSE`.
- `gh` 2.103.3, installed with Homebrew. It is not logged in.

## Technical Details

### Why a text swap was not enough for the Week 06 lab
- `maziar/kubia` had only the tags `latest`, `0.1` and two commit SHAs. The lab
  rolls out `v1`, then `v2`, and shows `This is v2 running in pod ...`.
- The fix: with `VERSION` set, the app replies `This is <VERSION> running in pod
  <name>`. Without it, the reply stays `You've hit <name>`, so `latest` and `0.1`
  do not change. Tested: CI rebuilt `latest`, and it still replies `You've hit`.
- `maziar/kubia:v9` does not exist (HTTP 404). The failed-rollout step needs that.
- `maziar/kubia` is `node:24-alpine`. It has `wget`, but no `curl` and no `bash`.
  Two lab commands ran `curl` inside a kubia Pod. They now use `wget -qO-`.
- `luksa/kubia` ignored SIGTERM. `maziar/kubia` stops in 0.15 s. The slide 4
  comment now says so.

### The Week 06 lab v3
- 14 `luksa/kubia` lines, 2 `curl` commands, 2 comment lines, the docstring.
- 31 slides, footers 1/31 to 31/31, 0 floats, Calibri and Consolas only.
- The script output passes `bash -n`.
- Slides 4 and 18 were rendered with LibreOffice and read. The text fits.

### The image copies
- `docker buildx imagetools create` copies the layers on the registry side.
- Flannel, Trivy, metrics-server, aws-cli and the two alpine images keep their
  upstream digest. `fortune`, `hpa-example` and `gb-frontend` are single-platform
  sources, so the copy has a new index digest with the same layers.
- `registry.k8s.io/test-webserver:latest` is a Docker schema 1 image. It cannot be
  copied, and containerd 2 cannot pull it, so the Week 09 slide was already broken.
  Slide 7 of the Week 09 lecture now uses `maziar/kubia:0.1`.

### The decks
- `retarget_accounts.py` replaces text in runs, also across run borders, in shapes,
  groups, tables and notes. It reads each input and never writes it. The three
  input checksums that I recorded stay the same.
- Every replacement matched: 29 replacements in 10 decks.
- A text compare of each input with its output: only the expected paragraphs differ
  (1 to 5 per deck). Slide counts, footers and fonts do not change.
- The account scan of the new decks finds only `maziar` and `sojoudian`.
- The 114 images of the canonical decks were read with macOS Vision OCR. No image
  names another account.
- 16 changed slides were rendered and read. The longest URL, Week 14 lecture slide
  11, fits on one line.

### The quizzes
- `build2.py`: 0 cross-pool repeats, W01 0 errors, longest 26 %.
- `build_easy20.py`: gates 1 to 11 pass, key 5/5/5/5.
- `audit_easy20.py` on the v2 files: 0 errors, 0 leaks, 0 pairs at risk.
- The key positions do not change, because the shuffle seed uses the stem only.
- `build3.py`, `build_easy20_w34.py` and `build_easy20_w56.py` still pass, and their
  outputs stay byte-identical.

### The GitHub copies that are still to do
Forks keep the name of the author, so they also keep the credit:

| Fork to create | Used by |
|---|---|
| `sojoudian/flannel` | Week 04 lab v2, slides 3 and 13 |
| `sojoudian/container.training` | Week 04 lab v2, slide 13 |
| `sojoudian/kubernetes-in-action` | Week 04 lab v2 slide 13, Week 12 v2 slide 21 |
| `sojoudian/kubia-website-example` | Week 07 lab v4, slide 11 (the clone runs in the Pod) |
| `sojoudian/eksctl` (from `eksctl-io/eksctl`) | Week 08 lecture v4, slide 13 |
| `sojoudian/simple-webapp-mysql` | Week 12 v2, slide 21 |
| `sojoudian/mjarosie.github.io` | Week 14 lecture v10, slide 11 |
| `sojoudian/clo835-mirrors` (new repository) | Week 14 lab v11 slide 20; Weeks 04 to 06 `master-init.sh.tftpl` |

## Results
- Docker Hub: 14 new tags in 12 public repositories, all checked with
  `imagetools inspect`.
- `maziar/kubia:v1` and `v2` answer correctly on amd64 and on arm64, on port 18090.
- Week 06 lab v3 and 10 deck versions: 0 other accounts, 0 floats, footers
  unchanged.
- Public repo copy: 0 `luksa`, 0 `aquasec`, 0 `flannel-io`.
- Port 18090 was used for the image tests only. Every test container is stopped.

## Issues / Notes
- **Blocking:** the forks and `clo835-mirrors` need `gh auth login`. Until then,
  the 9 deck links and the Flannel URL return 404.
- The public repo changes are not committed and not pushed.
- `Lab_week06_v2.pptx` is open in PowerPoint (lock file). I did not touch it.
- Kept on purpose: Docker Official Images (`nginx`, `alpine`, `busybox`, `mysql`);
  the `registry.k8s.io` system images that kubeadm pulls; the apt repositories
  `pkgs.k8s.io` and `download.docker.com`; author names such as "(Luksa)" and
  "(J. Petazzoni)"; links that are not GitHub or Docker Hub (`eksctl.io`,
  `pycon2019.container.training`, `dev.to` and similar).
- Not changed: superseded deck versions, `old/`, `finalWork/`, the PDFs, the
  kind-era `Week04/FINAL/lab_commands.txt`, and the draft
  `week05_practical_work/week5_code/`.
- The Docker Hub copies do not update. The README of `clo835-mirrors` says how to
  move to a new release.
- The CI of `sojoudian/kubia` builds `latest` for amd64 only. `v1` and `v2` are
  multi-platform.
- I used `cd` once in a shell command, against the preference. I moved the session
  back to the project root.
