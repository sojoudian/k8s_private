# Report: Week 09 lab v3, full live test on AWS

**Date**: 2026-10-31
**Sequence**: #04 for the day

## Summary
Lab v3 passes on a real cluster. All 35 commands ran two times, and every result agrees
with the slide comments. The clean-up works, also after a stop half way. All 15 resources
are destroyed. One blocker stays: GitHub does not hold lab v3, so a student gets v2.
The test found 4 small text defects, and none of them stops a student.

## What Changed
- Created this report.
- Updated the memory files `project-week09-deck.md` and `project-short-labs-2026-10-27.md`.
- No deck, script or repository file changed. Nothing was committed or pushed.

## Blocker
**GitHub HEAD `1783b12` holds lab v2.** That commit was made before lab v3. In
`~/Documents/c/r/CLO835_Fall_2026`, v3 is 3 modified files: `localMachine.sh`,
`cleanup_lab09.sh` and `master-init.sh.tftpl`. `git ls-remote` and a fresh clone both
show 0 `auth whoami` lines. So I tested the v3 folder of your clone, in a sandbox copy.
A student who runs `git pull` gets commands that do not match the slides or the Blackboard text.

## Technical Details
- Account `499333804030`, role `voclabs`, region `us-east-1`. I used `~/.aws/credentials`
  and copied no key to a file.
- Key pair `Maziar` matches `~/.ssh/mazSeneca` (same fingerprint).
- I answered the Terraform prompts as a student does: `key_name` is `Maziar`, then `yes`.
- Pass 1 ran at full speed. Pass 2 ran on the same cluster after the clean-up, with 3 s
  between commands. `instrument.py` from the 2026-10-27 test gives each command an exit code.
- Recovery test: with the scheduler away, a node cordoned and Pods Pending, I ran the clean-up.

## Results

| Check | Result |
|---|---|
| `bash -n`, `terraform fmt -check`, `terraform validate` | Pass |
| `terraform apply`, student prompts | 15 added |
| 3 nodes Ready | 1 min 58 s after the apply started |
| Versions | Kubernetes v1.35.10, Ubuntu 26.04.1, containerd 2.2.2 |
| `cloud-init` | `done`, `errors: []` |
| Message of the day | Correct: Week 09 and `localMachine.sh` |
| `cleanup_lab09.sh` on the master | Same as the repository file |
| Pass 1 | 35 commands, 1 non-zero |
| Pass 2 | 35 commands, 1 non-zero |
| Recovery test | Scheduler back, node uncordoned, nothing left |
| `terraform destroy`, student prompts | 15 destroyed |
| After destroy | 0 instances, 0 `week09` security groups |

The 1 non-zero exit in each pass is the final `grep`, which must find nothing.

**The 5 new commands of v3**

| Command | Result | Slide comment |
|---|---|---|
| `kubectl auth whoami` | `kubernetes-admin`, `kubeadm:cluster-admins`, X509 credential | Correct |
| `kubectl auth can-i delete nodes` | `yes` | Correct |
| `kubectl get csidrivers,storageclass` | `No resources found` | Correct |
| `kubectl get nodes -o wide` | INTERNAL-IP `172.31.x.x`, Pods `10.244.x.x` | Correct |
| `terraform state list` | 25 lines | See finding 1 |

**The other slide comments, both passes**
- `Node` owner, `No resources found`, `Pending` with `<none>`, Running on a worker: correct.
- 2 Pods on each worker before the drain, then all 4 on `workernode1`: correct.
- `SchedulingDisabled` after the cordon, one etcd member, `key_name` asked two times: correct.
- Certificates 364 days. Deck, script and Blackboard commands agree in the offline check.

## Findings (not fixed)
1. Slide 9 says "Terraform created these objects", but `terraform state list` prints 25 lines:
   15 resources and 10 `data` sources. Terraform only reads the `data` lines. A student can
   report 25, and `Destroy complete!` says 15.
2. Slide 3 sample output says `v1.35.9`, and the cluster now runs `v1.35.10`. The text is in
   `lab_kubeadm.py`, so it affects all the labs.
3. Slide 7 says the certificates expire after one year. The 3 CA certificates expire after
   10 years. The other 11 expire after one year.
4. `kubectl auth can-i delete nodes` also prints `Warning: resource 'nodes' is not namespace
   scoped`. The result is correct, but a student can think it is an error.

**Notes**
- `kubeadm upgrade plan` shows no upgrade, because v1.35.10 is the latest v1.35 version.
  The command and the "it only reads" comment are correct.
- The drain also evicts a `kubeadm upgrade plan` health-check Pod in some runs. This is harmless.

## Issues / Notes
- The first run stopped before it created anything. Terraform reads stdin in blocks, so my
  harness lost the `yes`. A delay before each answer fixed the harness. This is not a lab defect.
- The AWS session keys are in this chat. They expire with the Learner Lab session. A scan of
  the reports, Week09, memory and test logs finds no key.
- The machines ran for about 6 minutes. No server started on this computer, so no port is used.
