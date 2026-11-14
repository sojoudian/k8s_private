# Report: Live test of the Week 10 lab of the course repository
**Date**: 2026-11-10
**Sequence**: #09 for the day

## Summary
The user added the two Terraform permission rules and asked me to run the live test. I ran the Week 10 lab of `~/Documents/c/r/CLO835_Fall_2026/Week10` (commit `5f8a655`) on AWS, as a student does. Three passes of 40 master commands each gave 0 non-zero exits. The recovery test left nothing in the cluster. `terraform destroy` removed all 15 resources. One small item: the cleanup leaves `/tmp/data-pv/note.txt` on workernode1, and the destroy removes it.

## What Changed
- Created this report.
- Updated the memory file `project-week10-deck.md`.
- No project file and no repo file changed. The 3 changed files in the clone are in `Week12`, from session `4b692c4c`.
- AWS: 15 resources created at 23:07 and destroyed at about 23:23 (local time), in a sandbox copy of the repo folder.

## Technical Details

### Method (standard Part E3)
1. Sandbox: `/private/tmp/claude-501/-Users-maziar-Downloads-k8s-week3/4607d34d-8f32-4600-8c64-da86808c91b9/scratchpad/w10live/tf`, a copy of the repo folder (8 files, equal to the repo before the apply).
2. `(sleep 10; echo Maziar; sleep 40; echo yes) | terraform -chdir=<sandbox> apply`: Terraform asked for `var.key_name` and for the approval.
3. SSH: `ssh -i ~/.ssh/mazSeneca ubuntu@<master>`, with a known_hosts file in the scratchpad.
4. Runners from `tools/instrument.py`: pass 1 and pass 3 at full speed, pass 2 with 3 s between commands. The pass 3 runner is byte-equal to the runner of the repo `localMachine.sh`.
5. Recovery runner: Steps 0 to 4, then a running `kubectl proxy`, a `dnstest` Pod, a Pending `data-pvc` and a Pending `writer` Pod, then `bash cleanup_lab10.sh` and the checks.
6. Destroy with the same student answers.

### The laptop commands of lab slide 3 and 9

| Command | Result |
|---|---|
| `git pull` in a fresh clone and in a clone at `ad93eb8` | exit 0 (report 2026-11-10-06) |
| `terraform init` | exit 0 |
| `terraform apply` (key name and `yes` typed) | "Apply complete! Resources: 15 added, 0 changed, 0 destroyed." |
| `terraform output public_ips` | master 98.83.37.201, worker-1 98.93.78.62, worker-2 3.230.135.33 |
| `terraform output private_ips` | master 172.31.69.229, worker-1 172.31.66.236, worker-2 172.31.67.203 |
| `ssh -i <key> ubuntu@<master>` | hostname `masternode` |
| `terraform destroy` (key name and `yes` typed) | "Destroy complete! Resources: 15 destroyed." |

### The master and the workers
- `cloud-init status --wait`: done. The 3 nodes were Ready about 1.5 minutes after the apply ended.
- Nodes: Kubernetes v1.35.10, Ubuntu 26.04.1 LTS, kernel 7.0.0-1016-aws, containerd 2.2.2.
- `/home/ubuntu/cleanup_lab10.sh` = the repo file. `/home/ubuntu/local-path-storage.yaml` = the manifest in `master-init.sh.tftpl` (188 lines). `/etc/motd` = the text of the template (Week 10, `localMachine.sh`).
- The worker message of the day says "You are on a WORKER node".
- CoreDNS and the Flannel DaemonSet rolled out before pass 1.

### Results by run

| Run | Commands | Non-zero exits |
|---|--:|--:|
| Pass 1, full speed | 40 | 0 |
| Pass 2, 3 s between commands | 40 | 0 |
| Recovery: Steps 0 to 4 (27 commands), then the half-done state and the cleanup | 27 | 0 |
| Pass 3, full speed, runner = repo file | 40 | 0 |

Recovery checks after `bash cleanup_lab10.sh`:
- `kubectl get pods,pvc,pv,sc`: "No resources found".
- Namespace `local-path-storage`, ClusterRole, ClusterRoleBinding, Service `kubia`: not found (exit 1 each, as required).
- `kubectl proxy`: not running. `pv-pvc.yaml`, `writer.yaml`, `kubia-statefulset.yaml`: removed (3 of 3).
- Workers: `/opt/local-path-provisioner` is empty on both.
- Between the passes, only the system Pods ran, and port 8001 was free.

### The output against the comments of `localMachine.sh` (all 3 passes)
- Step 0: 3 nodes Ready; the control-plane Pods Running.
- Step 1: `data-pvc` Bound to `data-pv`. In pass 1, `describe pvc` showed an early `FailedBinding` event and Status Bound, as the comment says. In pass 3 the Events were empty, which the word "can" covers.
- Step 2: `writer` on workernode1 each time; the same date after a new Pod; `data-pv` Released after the claim delete.
- Step 3: `standard (default)`, `rancher.io/local-path`, Delete, WaitForFirstConsumer. The real output also has ALLOWVOLUMEEXPANSION and AGE; the comment shows 4 of the 6 columns.
- Step 4: `kubia-0` before `kubia-1`; `data-kubia-0` and `data-kubia-1` Bound; new PVs Delete, Bound; `data-pv` Retain, Released.
- Step 5: "Data stored on pod kubia-0"; after the delete, "Data stored on this pod: Hello kubia-0"; one A record for `kubia-0.kubia`, two for `kubia`; two SRV records on port 8080; `dnstest` deleted.
- Step 6: the cleanup ends with "done"; `kubectl get pods,pvc,pv` gives "No resources found".

### After the destroy
- Week 10 instances: 3, all `terminated`. Not terminated: 0.
- Security groups that start with `week10`: 0.
- Terraform state of the sandbox: 0 resources.
- Still running: the 3 Week 12 instances of session `4b692c4c`. I did not touch them.

## Results
- The Week 10 lab of the repo works on a new cluster: 3 passes of 40 commands with 0 non-zero exits, a clean recovery, and a complete destroy.
- The scope of this result: the commands, the manifests, the boot files and the cleanup of the repo folder, on 2026-11-10, with the images and the Flannel manifest of today.
- No local server ran, so no port is used.

## Issues / Notes
1. After the cleanup, `/tmp/data-pv/note.txt` stays on workernode1. This is the Retain behavior, and `terraform destroy` removes the disk. Standard C5 asks the cleanup to remove each file of the lab. A student who runs the lab again on the same cluster gets the old file, and Step 2 writes over it.
2. The StorageClass comment shows 4 of the 6 output columns (known, report 2026-11-10-03).
3. Not tested here: the Blackboard text v4 (its "control-plane node" words stay open), and clones made before 2026-11-05 20:55 (they fail at `git pull`, run 12).
4. The Flannel URL uses "latest", and `maziar/alpine-curl` and `maziar/kubia-pet` use `latest`. A later change of them can change the result.
5. The first proxy check matched its own command line. The check with the pattern `[k]ubectl proxy` gave the true result: no proxy.
