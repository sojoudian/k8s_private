# Report: No cleanup script in the AWS labs
**Date**: 2026-11-11
**Sequence**: #01 for the day

## Summary
The user asked to delete the cleanup of the AWS labs in `CLO835_Fall_2026`, for all 10 weeks and the whole chain. `terraform destroy` removes the three machines and every object and file of a lab. The cleanup is now gone from 8 weeks: 04, 05, 06, 07, 09, 10, 13 and 14. I kept Week 03, because it runs Docker on the laptop of the student, where `terraform destroy` removes nothing. I did not change Week 12, because session `4b692c4c` was rebuilding it at the same time. A live test of the 7 weeks with a changed `master-init` passed, and all clusters are destroyed. The user then committed and pushed all of it as `5b97e4f`.

## What Changed

Engine and helpers:
- `lab_kubeadm.py`, `make_repo_folder()`:
  - It accepts `cleanup_body=None`, which gives no cleanup file and no cleanup block.
  - It works with a Week06 template with or without the cleanup block. Without the block, the anchor is `cat > /etc/motd`.
- `lab_destroy_only.py` (new):
  - `destroy_step()` turns the "Clean up" step into "Destroy the cluster".
  - `destroy_section()` turns section 7 of a Blackboard text into "Destroy the Cluster".

New builders. Each one imports the version before it and changes only the clean-up parts:

| Week | Builder | New outputs |
|---|---|---|
| 05 | `build_week05_lab_v5.py` | `Lab_week05_v5.pptx/.pdf`, `Lab_week05_Blackboard_Submission_v2.md`, repo Week05 |
| 06 | `build_week06_lab_v5.py` | `Lab_week06_v5.pptx/.pdf`, `localMachine_v5.sh`, `Lab_week06_Blackboard_Submission_v6.md`, repo Week06 |
| 07 | `build_week07_lab_v4.py` | `Lab_week07_v4.pptx/.pdf`, `localMachine_v4.sh`, `Lab_week07_Blackboard_Submission_v4.md`, repo Week07 |
| 09 | `build_week09_lab_v5.py` | `Lab_week09_v5.pptx/.pdf`, `localMachine_v5.sh`, `Lab_week09_Blackboard_Submission_v5.md`, repo Week09 |
| 10 | `build_week10_lab_v5.py` | `Lab_week10_v5.pptx/.pdf`, `localMachine_v5.sh`, `Lab_week10_Blackboard_Submission_v5.md`, repo Week10 |
| 13 | `build_week13_lab_v4.py` | `Lab_week13_v4.pptx/.pdf`, `localMachine_v4.sh`, `Lab_week13_Blackboard_Submission_v4.md`, repo Week13 |
| 14 | `build_week14_lab_v3.py` | `Lab_week14_v3.pptx/.pdf`, `localMachine_v3.sh`, `Lab_week14_Blackboard_Submission_v3.md`, repo Week14 |
| 04 | `remove_cleanup_week04.py` | repo Week04 only (the deck and the Blackboard text name no cleanup) |
| 07 | `build_week07_lecture_v8.py` | `Lecture_week07_v8.pptx/.pdf` (slide 18) |
| 10 | `build_week10_lecture_v12.py` | `Lecture_week10_v12.pptx/.pdf` (slides 23 and 37) |

Course repository, per week:
- `cleanup_labNN.sh` is deleted.
- `master-init.sh.tftpl` loses the block that wrote that file. This does not apply to Week 04, whose template never had the block.
- Step 6 of `localMachine.sh` (Step 13 for Week 05) is "Destroy the cluster", with only `terraform destroy`.

Rules and memory:
- `CLO835_STANDARDS.md` v1.2: C1, C5, C7, C9, E3, and H10 (Week 12 is open).
- Memory: `feedback-no-cleanup-script.md` (new), plus the week memories and `MEMORY.md`.

No delivered file was overwritten. All old versions stay.

## Technical Details

### What each change removes
- Deck: on the last step slide, the master part is removed: the cleanup script and the "nothing is left" check. The lines of your own machine stay, and a new comment follows them: "# This also deletes every Kubernetes object and every file of the lab." The slide title is now "Destroy the cluster".
- Blackboard text: the section title becomes "## 7. Destroy the Cluster" with a new intro. The `Run bash cleanup_labNN.sh` item and the "nothing is left" item are removed, and so is each Explain item about the cleanup:
  - Week 07 and Week 10: the order "claims before the provisioner".
  - Week 13: why the namespace deletion does not delete the CSR, the ClusterRole and the ClusterRoleBinding.
- Week 14 (short form): "Show the clean-up and terraform destroy." becomes "Show terraform destroy."
- Lectures:
  - W07 slide 18 drops the sentence "So the clean-up deletes the claim before the provisioner".
  - W10 slide 23 drops the bullet on the clean-up order.
  - W10 slide 37 maps Step 6 to "Destroy the cluster", with no lecture slide.

### Proof that nothing else changed
- Backward compatibility of the engine: with the new engine, the 6 old builders (W06 v4, W07 v3, W09 v4, W10 v4, W13 v3, W14 v2) rebuild 15 of 15 files equal to the stored files. The 5 repo folders that they write are equal too. W14 v2 stops in its repo step, because it reads a deleted scratchpad mirror; v3 reads `HEAD:Week14/metrics-server.yaml`.
- Fallback: in a sandbox clone, I committed a Week06 template with no block. With it, the old W07 v3 builder (with a cleanup) gives a `master-init` that is byte-equal to the real one. So the Week 12 v6 builder of the other session still works after the push.
- New decks against the old ones: only the last step slide differs (slide 17 for W05, slide 9 for the others). The lectures differ only on W07 slide 18 and W10 slides 23 and 37.
- Blackboard texts: only section 7 differs (W14: one item).
- Repo diff: in each week, `master-init.sh.tftpl` has 0 added lines. Only the cleanup block goes, and its size is the cleanup script plus 8 lines. `localMachine.sh` changes only in its last step. The 8 week folders have 0 "cleanup" references.
- The real outputs are equal to the sandbox outputs (9 decks and 8 repo folders).

### PDFs and the deck gate
- 9 PDFs through PowerPoint, with a private export folder, and each deck opened by its name. They hold only Calibri and Consolas, the page count equals the slide count, and Title and Author are set.
- Gate (`tools/rungate.py`), old against new:

| Deck | Old fails | New fails | Note |
|---|--:|--:|---|
| Lab W05 v5 | 6 | 5 | substitute PDF font fixed; 8 pt terminals, "we", commands with no `$`, thumbnail, file title stay |
| Lab W06 v5 | 3 | 2 | substitute PDF font fixed; thumbnail, file title stay |
| Lab W07 v4 | 0 | 0 | |
| Lab W09 v5 | 3 | 2 | substitute PDF font fixed; thumbnail, file title stay |
| Lab W10 v5 | 0 | 0 | |
| Lab W13 v4 | 0 | 0 | |
| Lab W14 v3 | 4 | 3 | substitute PDF font fixed; `busybox:1.36`, thumbnail, file title stay |
| Lecture W07 v8 | 0 | 0 | |
| Lecture W10 v12 | 0 | 0 | |

- No deck has a new failure. I looked at the 10 changed pages.

### Live test (AWS, sandbox copies of the repo folders)
Each test ran on a new cluster. The steps: apply, cloud-init done, 3 Ready nodes, the master holds no cleanup file, its user-data holds 0 "cleanup", one full pass of the repo `localMachine.sh`, then destroy. The runner keeps `\` continuations and both heredoc forms together; `tools/instrument.py` splits them. The runner runs detached on the master.

| Week | Commands | Non-zero exits | Destroy |
|---|--:|---|---|
| 05 | 65 | 6, all old and none from this change: [36] fails on purpose ("This FAILS, and that is the lesson"); [58] is the placeholder `<paste-one-pod-name-here>`; [22], [24]-[26] read logs before the container starts (no `kubectl wait` in the script, full speed) | 16 destroyed |
| 06 | 34 | 0 | 15 destroyed |
| 07 | 38 | 0 | 15 destroyed |
| 09 | 33 | 0 | 15 destroyed |
| 10 | 38 | 0 | 15 destroyed |
| 13 | 39 | 4, all planned denials of the RBAC lab ("Forbidden", "no"), as the comments say | 15 destroyed |
| 14 | 38 | 1, the planned "Forbidden: view cannot create" | 15 destroyed |

- The files of each tested sandbox are equal to the pushed commit `5b97e4f`.
- After the destroys: 0 instances and 0 security groups of these weeks. Only the Week 12 cluster of the other session ran.

## Results
- 8 weeks have no cleanup script, no cleanup block and no cleanup step. The commit `5b97e4f` (by the user) holds them.
- 7 live passes on new clusters: the only non-zero exits are planned ones or old Week 05 timing items.
- No server ran, so no port is used.

## Issues / Notes
1. Week 03: not changed, on purpose. It runs on the laptop of the student ("Run these ON YOUR OWN LAPTOP ... Docker must be running"). Its Docker teardown (`docker rm`, `docker network rm`, `docker volume rm`) is graded in the Lab02 text.
2. Week 12: not changed. Session `4b692c4c` rebuilt it at the same time (`build_week12_lab_v6.py`, 23:47). The commit `5b97e4f` still holds `cleanup_lab12.sh`. Its next version must use `make_repo_folder(..., None, ...)` and `lab_destroy_only.destroy_step()`. The lab checks of `gate_week12.py` still expect a cleanup script.
3. Blackboard: the new texts are W05 v2, W06 v6, W07 v4, W09 v5, W10 v5, W13 v4 and W14 v3. Labs that students already submitted keep their old text for grading (C7).
4. The classifier denied two calls: the first Week 05 apply (piped form) and one read-only command. The Week 05 apply then ran in the form of the allow rule (`apply -var key_name=Maziar -auto-approve`), so that test did not type the student answers.
5. The first Week 14 apply lost one worker ("Client.UserInitiatedShutdown"). I started it while the Week 10 and 13 clusters still counted, and the 9-instance limit shut the worker down. A second apply replaced the worker. This was my error. E3 of the standard now asks to count the instances before each apply.
6. The first Week 05 run lost its SSH connection (the Mac network dropped). The pass ran again on the same, still empty cluster.
7. The pass logs and runners are in the volatile scratchpad: `/private/tmp/claude-501/-Users-maziar-Downloads-k8s-week3/4607d34d-8f32-4600-8c64-da86808c91b9/scratchpad/live7`.
8. A lab with no cleanup cannot run pass 2 on the same cluster. Each week had one pass on a new cluster.
