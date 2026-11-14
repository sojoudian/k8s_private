# Report: Week 13, live test and final gate

**Date**: 2026-10-31
**Sequence**: #16 for the day

## Summary
The result is 1 for the scope below. `gate_week13.py` with the live logs gives GATE 1, 132 of 132. The lab passed 2 live passes of 40 commands each. The only 4 non-zero exits are the 4 planned refusals. All 22 lecture commands ran from the deck in slide order. All 15 AWS resources are destroyed. This report replaces the result 0 of report #15. Its audit, change lists, reviewer items and rubric table stay valid.

## What Changed
- `reports/report-2026-10-31-16-week13-live-test.md`, this report.
- Memory: `project-week13-deck.md`, `project-short-labs-2026-10-27.md`, `MEMORY.md`.
- No lecture, lab, script, Blackboard or repository file changed after the test. The test found no defect in them. The gate proves that the tested commands equal the final commands.

## Technical Details
- Account `499333804030`, `us-east-1`, key pair `Maziar`. Terraform got the student prompts for `key_name` and `yes`.
- The driver copied `~/Documents/c/r/CLO835_Fall_2026/Week13` and ran each file as it is.
- The lecture commands came from `Lecture_week13_v8.pptx`, with a check of each expected result.
- The recovery test stopped a lab half way, then ran the clean-up.

## Results

| Check | Result |
|---|---|
| `terraform apply` | 15 added |
| `terraform output public_ips`, `private_ips` | Both ran as shown |
| Nodes Ready | 3 of 3, 2 minutes after the start of the apply |
| Kubernetes | v1.35.10, Ubuntu 26.04.1, containerd 2.2.2 |
| Flannel | `maziar/flannel:v0.28.10`, no `ghcr.io` image |
| `cleanup_lab13.sh` on the master | Equals the repository file |
| Pass 1 | 40 commands, 4 planned refusals |
| Pass 2, 3 seconds between commands | 40 commands, 4 planned refusals |
| Lecture commands | 22 commands, `@@LECTURE OK`, 0 `@@BAD` |
| Recovery | Return code 0 in 6 seconds, 0 objects left |
| `terraform destroy` | 15 destroyed |
| After destroy | 0 instances, 0 `week13` security groups |
| `gate_week13.py` with the live folder | GATE 1, 132 of 132 |

**The 4 planned refusals**
- `kubectl --context=dev-user@kubernetes get pods`: Forbidden.
- `kubectl --context=dev-user@kubernetes delete pod web`: Forbidden.
- `kubectl auth can-i list services -n default ...`: no.
- The first `kubectl auth can-i list persistentvolumes -A ...`: no.

**Real output that proves the text**
- `/version` gave `v1.35.10`. `/apis` gave 403 for `system:anonymous`. `kubectl proxy` gave `APIGroupList`.
- `kubectl auth whoami` gave the user `dev-user` and the groups `developers` and `system:authenticated`.
- `openssl x509` gave `O=developers, CN=dev-user`.
- `get services` gave "No resources found in week13 namespace."
- The Pod got 403 first, then a `ServiceList` with `"items": []`.
- `api-resources` showed the header and `false` for `persistentvolumes`.
- After the RoleBinding the answer was no. After the ClusterRoleBinding the answer was yes.
- The clean-up left the context `kubernetes-admin@kubernetes` only.
- `--authorization-mode=Node,RBAC` is on the master, and `/logs/` returns NotFound. These 2 results prove the lecture changes.
- `kubeadm:cluster-admins` is a ClusterRoleBinding to `cluster-admin`. `describe clusterrole cluster-admin` equals slide 23.

## Issues / Notes

**Limits of this result**
- Lab v3 reaches students only after your push of the 3 changed files in `Week13`. Until then, `git pull` on lab slide 3 gives lab v2.
- The student order of `git pull` is not tested, for that reason.
- I did not view the decks in Keynote, because this computer has only PowerPoint.
- No reviewer re-read the fixes of the second pass. The gate, the live test and my page check cover them.
- "This step takes about 40 seconds" is an estimate from the length of pass 1 (62 seconds). I did not time this step alone.
- In the test, `curl` showed a progress table, because its output went to a pipe. A student at a terminal does not see this table.
- Commands on Amazon EKS are not in the deck, and the EKS facts come from the AWS documents. Students have no EKS, so these slides have no lab step.

**Your decision**
- The Blackboard name of this lab.

**Other weeks, not changed**
- The Week 14 cover says "Week 12 · Lecture".
