# Report: Assignment 2 Blackboard Submission Text
**Date**: 2026-10-14
**Sequence**: #05 for the day

## Summary
The user asked for the same kind of Blackboard text for Assignment 2 as the one
written for the Week 05 lab, and asked to include the repository address. I wrote
it and saved it to `Assignments/Assignment_2/Assignment2_Blackboard_Submission.md`.

## What Changed
- **Created** `Assignments/Assignment_2/Assignment2_Blackboard_Submission.md` —
  142 lines. It holds the intro, the version table, the repository address,
  11 numbered sections, the Submission Requirements block, and the Integrity
  Pledge block.
- No other file was changed. No command with a side effect ran. Nothing was
  committed, and nothing was pushed.

## Technical Details
Facts came from the starter folder
`~/Documents/c/r/a2_test/CLO835_Fall_2026/assignment-2`:
- `README.md` — the two versions 0.2 and 0.3, port 8080, the six languages, the
  CPU trap, the NodePort 30000, and the Week 05 cluster.
- `Dockerfile`, `.github/workflows/docker.yml`, `k8s/deployment.yaml`,
  `k8s/service.yaml` — the four graded placeholder files, each with TODO only.
- `report.md` — the report template.
- `git remote -v` — the repository address
  `https://github.com/sojoudian/CLO835_Fall_2026`.

The text keeps the shape of the Week 04 and Week 05 items:
- a title, `Assignment 2 Submission`;
- a short intro;
- numbered sections, each with one or two sentences and a `You must:` list;
- every bullet starts with `Show`, `Run`, `Give`, `State`, `Create`, `Change`,
  `Choose`, `Copy`, `Open`, `Add`, `List` or `Explain`;
- the two standard blocks at the end, verbatim.

The 11 sections follow the order of the work:

| Section | Subject |
|---|---|
| 1. Your Own Repository | the copy to the root, the git log |
| 2. Choose One Language and Make Version 0.2 | the MESSAGE constant, the local test |
| 3. The Dockerfile | the first graded file, linux/amd64 |
| 4. The GitHub Actions Pipeline | the second graded file, the two secrets |
| 5. The Kubernetes Cluster | the Week 05 Terraform cluster |
| 6. Deploy Version 0.2 | the third and fourth graded files |
| 7. Reach the Application from Every Node | the three public addresses |
| 8. Release Version 0.3 | the student ID, set image, rollout status |
| 9. Roll Back | rollout history, rollout undo |
| 10. The Report | report.md |
| 11. Destroy the Cluster | terraform destroy |

Every section names a real file or a real command of the starter. Each section
carries at least one `Explain` bullet, the same way the Week 04 and Week 05 items
do. The `Explain` bullets cover:
- why a workflow in a sub-folder never runs;
- why the image must be linux/amd64, and what `exec format error` means;
- why a token is a secret, and what the commit SHA tag adds;
- why the Service selector must match the pod labels;
- why a node that runs no pod still serves the page;
- why the pods change one at a time during a rolling update;
- why a rollback does not need a new image build.

## Results
The file is at
`/Users/maziar/Downloads/k8s_week3/Assignments/Assignment_2/Assignment2_Blackboard_Submission.md`.
The text is ready to paste into the Blackboard instruction editor.

## Issues / Notes
- **The repository address is not live yet.** The text sends students to
  `https://github.com/sojoudian/CLO835_Fall_2026`, folder `assignment-2`. That
  folder is still untracked in the local clone. It is not committed, and it is
  not pushed. Push it before the item becomes visible to the students.
- The text does not name a weight, a due date, or a grade breakdown, because the
  user did not supply them. The Week 04 item carries 2.5% and 100 points.
- The starter `README.md` points at the Blackboard handout for the grade
  breakdown. If this text becomes the handout, add the breakdown here.
