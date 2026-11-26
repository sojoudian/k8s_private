# Report: Live Test of All Week 12 Lab Commands
**Date**: 2026-11-25
**Sequence**: #03 for the day

## Summary
The user asked Claude to test all the commands of the Week 12 lab on AWS. Claude built the Week 12 cluster
as a student, ran all 39 commands of `localMachine.sh` v8 on the master, and destroyed the cluster. All 39
commands gave exit 0, and each output agrees with its comment. The public GitHub repository still has the v7
`localMachine.sh`, not v8.

## What Changed
- This report.
- No project file and no repository file changed. There is no commit and no push.
- AWS: 1 cluster (3 `m5.large` instances, 15 resources) was created and destroyed in this session.
- Scratchpad only: a copy of the repo folder (`w12live_1125/`), the runner and its log, and a clone of the
  public repository (`w12git_1125/`).

## Technical Details
- AWS check before the test: the role `assumed-role/voclabs`, region us-east-1, 0 instances, only the
  `default` security group. The local key `~/.ssh/mazSeneca` has the fingerprint of the key pair `Maziar`.
- Sandbox: a copy of `~/Documents/c/r/CLO835_Fall_2026/Week12` (7 files). Its `localMachine.sh` is
  byte-equal to `Week12/localMachine_v8.sh`.
- Step 0 on the own machine:
  - `terraform init` and `terraform validate`: "Success! The configuration is valid." (Terraform v1.17.2).
  - `terraform apply` with the key name at the prompt: 15:15:07 to 15:16:35 EST, "Apply complete!
    Resources: 15 added, 0 changed, 0 destroyed."
  - `terraform output public_ips` and `private_ips`: 3 addresses each.
  - `git clone`, `git fetch` and `git reset --hard origin/master`: done in a new clone in the scratchpad (not
    in the course repo of the user), exit 0, HEAD 7c4d9b8.
- On the master: `cloud-init status` done; the message of the day names Week 12 and `localMachine.sh`; the
  home directory holds no file. 3 nodes Ready (v1.35.11, Ubuntu 26.04.1 LTS, containerd 2.2.2).
- Runner: `tools/instrument.py` made a runner of 39 commands with 3 s between commands (step 0: 2, step 1: 5,
  step 2: 6, step 3: 8, step 4: 11, step 5: 7). It ran detached on the master, from 20:18:18 to 20:21:42 UTC.

## Results
- 39 of 39 commands gave exit 0. 0 commands gave another exit code.
- Output against the comments:

| Step | Live output | Comment or sample | Result |
|---|---|---|---|
| 0 | 3 nodes Ready; 9 kube-system Pods Running | check the three nodes | equal |
| 1 | "Configured to generate new fortune every 2 seconds", then a line every 2 s | "a fortune every 2 s" | equal |
| 2 | hello, blue, hello blue, blue, prod, debug, 10.96.0.1 | env has priority over envFrom; `$(GREETING) $(COLOR)` | equal |
| 3 | `-r--r-----` for APP_COLOR, APP_MODE, GREETING, LOG_LEVEL; blue; green after the patch; `printenv APP_COLOR` blue | "0440 lets the owner and the group read"; "# still blue" | equal |
| 4 | paswrd; paswrd, mysql; mysql; tmpfs; ca.crt, namespace, token; app-secret Opaque 2 | "base64 is an encoding"; "in memory (tmpfs)"; "# app-secret only" | equal |
| 5 | namespace, ConfigMap and Secret created; red, dev; dev-pass | "# red, dev"; "dev-pass: the password, in plain bytes" | equal |

- Step 6, `terraform destroy` with the key name at the prompt: "Destroy complete! Resources: 15 destroyed."
  (15:25:33 EST). After it: the 3 instances are `terminated`, and only the `default` security group remains.

## Issues / Notes
- GitHub is not at v8. The public repository (HEAD 7c4d9b8) has the v7 `Week12/localMachine.sh`. The local
  course repo has v8 as an uncommitted change. A student who runs `git reset --hard origin/master` gets v7.
  v7 has no `GREETING=hi` key, no `MESSAGE` variable and no `defaultMode: 0440`, but the v8 lab deck shows
  them. The other 6 files of the folder are equal to GitHub. The commit and the push are for the user.
- Two samples differ from the live values. The values depend on the patch release and the node memory:
  - Lab deck v8 shows `v1.35.10` (3 times). Live: `v1.35.11`.
  - Lecture v8 slide 20 shows `size=7814528k`. Live: `size=7814512k`.
- No server started on the local machine, so no port is used.
