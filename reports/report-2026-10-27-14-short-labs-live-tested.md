# Report: Labs of Weeks 06 to 14, Cut to Week 04 Size and Tested Live on AWS
**Date**: 2026-10-27
**Sequence**: #14 for the day

## Summary
The Week 06 lab had 4 workshops and 21 steps. That does not fit in one 90-minute lab. The user set a new limit: no lab is longer than the Week 03 and Week 04 labs. This work rebuilds the labs of Weeks 06, 07, 09, 10, 12, 13 and 14 to one workshop each, with Step 0 to Step 6. Each lab ran live on AWS (account 499333804030), two times on the same cluster. The tests found 21 defects. All 21 are fixed, and every lab passed again after the last fix. Nothing is committed or pushed.

## What Changed
New builders in `/Users/maziar/Downloads/k8s_week3/`:
- `build_week06_lab_v4.py`, `build_week07_lab_v2.py`, `build_week09_lab_v2.py`, `build_week10_lab_v2.py`, `build_week12_lab_v2.py`, `build_week13_lab_v2.py`, `build_week14_lab_v2.py`.
- `lab_kubeadm.py` (changed): reads the Week 06 template from git HEAD, writes the extra manifests of a week, sets `chown -R` on `~/.kube`, adds `git pull` to the cluster slide, and keeps the mode 644 of `bootstrap.sh`.

New lab files (the v1 files stay in place):

| Week | Deck and PDF | Slides | Script steps | Commands |
|---|---|---|---|---|
| 06 | `Week06/Lab_week06_v4.pptx` + `.pdf` | 10 | 0 to 6 | 36 |
| 07 | `Week07/Lab_week07_v2.pptx` + `.pdf` | 10 | 0 to 6 | 40 |
| 09 | `Week09/Lab_week09_v2.pptx` + `.pdf` | 10 | 0 to 6 | 31 |
| 10 | `Week10/Lab_week10_v2.pptx` + `.pdf` | 10 | 0 to 6 | 35 |
| 12 | `Week12/Lab_week12_v2.pptx` + `.pdf` | 10 | 0 to 6 | 33 |
| 13 | `week13/Lab_week13_v2.pptx` + `.pdf` | 10 | 0 to 6 | 36 |
| 14 | `week14/Lab_week14_v2.pptx` + `.pdf` | 10 | 0 to 6 | 40 |

For comparison: Week 03 has 6 steps and Week 04 has 7 steps (0 to 6). Each week folder also has `localMachine_vN.sh` and `Lab_weekNN_Blackboard_Submission_vN.md`.

Course repository `~/Documents/c/r/CLO835_Fall_2026` (the fresh clone at `acd8cdf`):
- `Week06/`: `localMachine.sh`, `cleanup_lab06.sh` and `master-init.sh.tftpl` changed.
- `Week07/`, `Week09/`, `Week10/`, `Week12/`, `Week13/`, `Week14/`: new. Each has the 8 files of the Week 06 pattern.
- `Week07/local-path-storage.yaml`, `Week10/local-path-storage.yaml`: the local-path provisioner v0.0.37 with the `maziar` image, StorageClass `standard` (default).
- `Week14/metrics-server.yaml`: metrics-server v0.7.1 with the `maziar` image and `--kubelet-insecure-tls`.

## Technical Details
Content of each lab (one workshop, 5 lesson steps and a clean-up):
- Week 06: a Deployment; roll out v2 and roll back; labels drive the ReplicaSet; a ClusterIP Service with its DNS name; a NodePort Service.
- Week 07: two containers share an emptyDir; the volume lifecycle; an init container clones a repository (replaces gitRepo); hostPath; a PVC with a StorageClass.
- Week 09: static Pods; etcd; stop and restore the scheduler; certificates, upgrade plan and join command; cordon and drain.
- Week 10: a static PV and a PVC; data that outlives the Pod; a StorageClass; a StatefulSet with a headless Service; a pet keeps its name, data and DNS name.
- Week 12: args; variables from a ConfigMap; a ConfigMap as a volume; a Secret as a variable and a volume; the Secret in etcd.
- Week 13: a user certificate by CSR; authenticated but not authorized; a Role for the user; a ServiceAccount token call; a Role for the ServiceAccount.
- Week 14: a second user and a context; use-context; the Metrics Server; an HPA; load and scale-out.

Removed to meet the limit: Week 06 failed rollout, Recreate, pause, LoadBalancer, Ingress, environment-variable discovery; Week 07 NFS; Week 09 networking, private API and Terraform state; Week 10 mongo, redis and the peers update; Week 12 the two-namespace pattern and the token Secret; Week 13 ClusterRoles and API groups; Week 14 the separate kubeconfig file and the optional IRSA workshop.

Test method (`scratchpad/labtest/`):
- `instrument.py` turns `localMachine.sh` into one bash script. Each command prints its line number and its exit code. Here-documents and continuation lines stay as one command.
- `labtest2.sh` copies the repo folder, runs `terraform apply`, waits for 3 Ready nodes, and checks that `cleanup_labNN.sh` on the master is the same as the repo file.
- Pass 1 runs every command at full speed. It stops before the clean-up, so the laptop checks run (Week 06: the NodePort on all 3 public IPs). Then the clean-up runs.
- Pass 2 runs the whole lab again on the SAME cluster, with 3 seconds between commands. It proves that the clean-up removes everything, and it simulates a slow student.
- After pass 2, a check lists every object that a lab can leave: namespaces, PVs, StorageClasses, CSRs, cluster roles, kube-system objects, contexts, users and home files.
- `terraform destroy` runs at the end.
- The course repo is not pushed, so the 3 manifest URLs return 404. The test copies the same files to the master and rewrites only those 3 URLs.

## Results
Live test, final run of each lab (two passes each):

| Week | Pass 1 | Pass 2 | Non-zero exit codes | Leftovers | Destroy |
|---|---|---|---|---|---|
| 06 | 36 commands | 36 commands | 1: the final `grep` that must find nothing | none | 15 of 15 |
| 07 | 40 | 40 | 0 | none | 15 of 15 |
| 09 | 31 | 31 | 1: the final `grep` | none | 15 of 15 |
| 10 | 35 | 35 | 0 | none | 15 of 15 |
| 12 | 33 | 33 | 1: the final `grep` | none | 15 of 15 |
| 13 | 36 | 36 | 4: the 2 `Forbidden` and the 2 `can-i` "no" that the lab teaches | none | 15 of 15 |
| 14 | 40 | 40 | 1: the `Forbidden` create that the lab teaches | none | 15 of 15 |

Week 14 ran 3 times. Run 2 found defect 18. Run 3, with the fix, is the result above: the HPA showed `cpu: 0%/50%` after the wait in both passes, then scaled 1 to 4 to 8 to 9 replicas under load.

Every non-zero exit code is a result that the slide expects.

Timing on AWS: `terraform apply` takes about 40 s. The 3 nodes are Ready about 70 to 110 s later. Kubernetes v1.35.9, Ubuntu 26.04.1, containerd 2.2.2.

Defects found and fixed (21):
1. Week 06 v3: 4 workshops and 21 steps. All seven labs are now one workshop with Step 0 to Step 6.
2. All folders: `~/.kube` belonged to root, so `kubectl config set-credentials` failed with "config.lock: permission denied" (Weeks 13 and 14). Fix: `chown -R ubuntu:ubuntu /home/ubuntu/.kube` in `master-init.sh.tftpl`.
3. All labs: the cluster slide had no `git pull`. A clone from an earlier week has no new folder. Fix: `cd CLO835_Fall_2026 && git pull && cd WeekNN`.
4. All labs: the sample output said v1.35.0. The cluster runs v1.35.9.
5. All labs: `terraform destroy` asks for `key_name`, and no slide said so. Fix: a comment on the line.
6. Week 06: right after the relabel, the Service had 2 endpoints, not 3. Fix: `kubectl rollout status` after the relabel.
7. Week 07: the clean-up left a `Released` PV, because it deleted the provisioner first. Fix: wait until the PVs are gone.
8. Week 10: the same PV clean-up defect. Same fix.
9. Week 10: right after `apply`, the PVC was `Pending`, but the slide said `Bound`. Fix: `kubectl wait --for=jsonpath='{.status.phase}'=Bound`.
10. Week 10: `kubectl wait pod/kubia-0` could start before the new Pod exists. Fix: `sleep 5` first.
11. Week 09: a fixed `sleep 20` for the scheduler Pod to go. Fix: `kubectl wait --for=delete`, then a label query.
12. Week 12: `cat` of a ConfigMap file printed no newline. Fix: `; echo`.
13. Week 13: the JSON answer of the API printed no newline. Fix: `; echo`.
14. Weeks 13 and 14: the Blackboard text asks for the approved CSR, but no command showed it. Fix: `kubectl get csr`.
15. Week 14: 25 s after install, the APIService was `False (FailedDiscoveryCheck)`, but the slide said True. Fix: `kubectl wait --for=condition=Available`.
16. Week 14: `grep -A2 Metrics` also matched the event `FailedComputeMetricsReplicas`. Fix: `grep -A1 '^Metrics:'`.
17. Week 14: the clean-up left the metrics-server ServiceAccount, RoleBinding, 2 ClusterRoles and 2 ClusterRoleBindings. Fix: delete them by name.
18. Week 14: after `sleep 30`, the HPA showed `<unknown>/50%` in one run and `0%/50%` in another. Fix: `kubectl wait --for=condition=ScalingActive`.
19. Week 07: the fork `sojoudian/kubia-website-example` of the lecture does not exist. Fix: the init container clones `sojoudian/kubia`, which exists.
20. Weeks 07, 10 and 14: the mirror repository `sojoudian/clo835-mirrors` does not exist. Fix: the manifests are files of the course repository.
21. Week 06: the generator changed `bootstrap.sh` from mode 644 to 755. Fix: it keeps 644.

Static checks on the 7 repo folders: `bash -n` passes, `terraform fmt -check` and `validate` pass, both templates render with `templatefile()`, 0 non-ASCII characters, and 0 hits for private data. All decks: 10 slides, footers `n / 10`, 0 float coordinates.

## Issues / Notes
- **Push the course repo before the labs.** Weeks 07, 10 and 14 apply a manifest from `https://raw.githubusercontent.com/sojoudian/CLO835_Fall_2026/master/WeekNN/`. These URLs return 404 until the push.
- **The Learner Lab allows 9 running instances.** Above 9, it shuts the new ones down at once ("Client.UserInitiatedShutdown"). So one account can run 3 lab clusters at the same time. Two test builds failed for this reason; their partial resources were destroyed.
- Flannel still comes from `flannel-io/.../releases/latest`, as in the committed Weeks 04 to 06. A future Flannel release can change it.
- Week 05 still has 13 steps (0 to 13). It was not changed.
- Final AWS state (2026-10-28 00:09): 0 instances, 0 `week*` security groups, 0 available volumes, 0 Elastic IPs.
- Local test logs: `/private/tmp/claude-501/-Users-maziar-Downloads-k8s-week3/0b02113e-4049-4aa0-bece-9e5b05d8791f/scratchpad/labtest/deep/`.
