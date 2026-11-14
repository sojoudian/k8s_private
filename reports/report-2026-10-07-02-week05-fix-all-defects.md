# Report: Week 05 - All 14 Defects Fixed
**Date**: 2026-10-07
**Sequence**: #02 for the day

## Summary
The audit in report #01 found 14 defects in the Week 05 lecture, lab deck and lab
code. All 14 are fixed. The lab code now builds a kubeadm cluster of 1 master and
2 workers, the same pattern as Week 04. `terraform init` and `terraform validate`
both pass. The two decks are rebuilt as `_v2`, with correct footers, native
diagrams, a Course Outline slide and a palette with zero off-brand colours.

## What Changed

### Lab code - `week05_practical_work/week5_code/`
| File | Change |
|------|--------|
| `main.tf` | NEW. 1 master + 2 workers, pinned provider, subnet by instance-type offerings, NodePort rule, public AND private IP outputs |
| `variables.tf` | NEW. `key_name` with no default, `lab_instance_profile`, `ssh_cidr` |
| `bootstrap.sh` | NEW. Runs on every node: swap off, MTU 1500, containerd, kubeadm v1.35 |
| `master-init.sh.tftpl` | NEW. `kubeadm init` + Flannel, with a retry loop |
| `worker-join.sh.tftpl` | NEW. `kubeadm join`, with a retry loop |
| `localMachine.sh` | NEW. The lab, 9 steps |
| `cleanup_lab05.sh` | NEW. Removes the Kubernetes objects and names the destroy step |
| `README.md` | NEW. Build, run, clean up, and why each choice was made |
| `.gitignore` | NEW. State files and keys stay out of git |
| `legacy_kind/` | MOVED. `config.tf`, `ec2.tf`, `sg.tf`, `output.tf`, `init_kind.sh`, `kind.yaml` |

### Decks - `Week05/`
| File | Change |
|------|--------|
| `lecture_week05_v2.pptx` + `.pdf` | NEW. 30 slides (29 visible, 1 hidden) |
| `Lab_week05_v2.pptx` + `.pdf` | NEW. 11 slides |

The `v1` files are untouched (PROMPT.md R8).

## Technical Details

### D1 - Footer numbering
The lecture footers now read `1 / 29` to `29 / 29`. The lab footers read `1 / 11` to
`11 / 11`. The hidden slide repeats the number of its visible twin, which is the
convention the source deck already used.

### D2 - `terraform init` failure
`sg.tf` is gone. `main.tf` declares the security groups and the rules directly, so
no registry module is involved. `required_providers` pins `hashicorp/aws ~> 5.0`.
Proven with Terraform v1.16.4:
```
terraform init     -> success
terraform validate -> Success! The configuration is valid.
terraform fmt      -> clean
```

### D3 - EN DASH in commands
Three commands are corrected:
- lecture, `--image`
- lecture, `kubectl create -f kubia-descriptor.yaml`
- lab, `kubectl get all -n pingpong`

A second pass catches a pattern that straddles two runs. The final check finds
zero non-ASCII characters in any Consolas run, in either deck.

### D4 - Missing `week5.pub`
The `aws_key_pair` resource is removed. `var.key_name` has no default, so Terraform
asks for the name of a key pair that already exists in the Learner Lab. This is the
Week 02, 03 and 04 pattern.

### D5 - Duplicate security group name
The two groups are now `week05-k8s-master` and `week05-k8s-worker`.

### D6 - NodePort not open
`aws_security_group_rule.worker_nodeport` opens 30000-32767 on the workers. Step 8
of `localMachine.sh` publishes the nginx Pod on NodePort 30000 and proves it.

### D7 - Zero-width spaces
Removed from `ec2.tf` and `kind.yaml` in both copies. Zero non-ASCII bytes remain
in any `.tf`, `.sh`, `.tftpl`, `.yaml` or `.md` file under `week5_code/`.

### D8 - The lab taught kind
The lab deck slide 2 now reads `Running K8s cluster - kubeadm (3 nodes)`. Slide 3
shows the Terraform build on the left and `kubectl get nodes` with three Ready
nodes on the right. Each terminal line is coloured by its kind: a comment is green,
a command is cyan, output is grey.

### D9 - Amazon Linux 2 and `yum`
The AMI is `ubuntu-resolute-26.04-amd64-server-*`, the same release as Week 02 and
Week 03. Every `[ec2-user@ip-172-31-12-180 tmp]$` prompt in both decks is now
`ubuntu@masternode:~$`. `nodeName: kind-control-plane` is now `workernode1`.

### D10 - kind v0.11.0 and node v1.23.17
Gone. `bootstrap.sh` installs kubeadm, kubelet and kubectl from the Kubernetes
v1.35 apt repository, then holds the three packages.

### D11 - Terraform ignored the house pattern
- `m5.large`, chosen in `locals`.
- Subnet picked from `aws_ec2_instance_type_offerings`, so `us-east-1e` cannot
  break the launch.
- `key_name` prompts.
- `iam_instance_profile = var.lab_instance_profile`, default `LabInstanceProfile`.
- IMDSv2 required, hop limit 2.
- Outputs `public_ips`, `private_ips` and `next_step`.

### D12 - Missing scripts
`localMachine.sh`, `cleanup_lab05.sh` and `README.md` are added. All three shell
files pass `bash -n`.

### D13 - Off-palette colours
Six colours are remapped in 22 places:

| Was | Now | Where |
|-----|-----|-------|
| `E74C3C` | `FF5F56` | 6 slides |
| `CFCFCF` | `E0E0E0` | three-tier diagram |
| `B8AB9A` | `CFDBEE` | database cylinder bands |
| `8B7E6E` | `37465A` | database cylinder body |
| `DED2C1` | `1FA8E0` | database cylinder top |
| `6A8AB8` | `2196A0` | stray square |

The final check finds zero colours outside the union of Week01 v5, Week02 v1 and
Week03 v1.

### D14 - Source screenshots
Four PNG screenshots on lecture slides 3, 5, 9 and 18 are replaced by native
shapes:

| Slide | New diagram |
|-------|-------------|
| 3 | Two node panels, five Pods, Pod 3 crossed out, with the rule "A Pod never spans two nodes." |
| 5 | One Pod box: three container cards (sidecar, main, init), CPU/RAM/filesystem chips, one network stack, one IP |
| 9 | Three panels (two wrong, one correct) plus the sidecar logging pattern |
| 18 | A 5 x 3 label matrix: `app=ui/as/pc/sc/os` against `rel=stable/beta/canary` |

Every vertical position was measured on a render, not guessed, so no diagram
touches the bullet text above it.

### Addition - Course Outline
The lecture gains a Course Outline slide at position 3, built to the same design as
Week 04 slide 3. Row 05 is `Today`. Rows 01 to 04 are `Done`. The last row is
numbered `08`; the Week 04 deck numbers the same row `09`, which is a typo I did
not copy.

## Results

Lecture `lecture_week05_v2.pptx`:
- 30 slides, 29 visible, canvas 13.333 in
- footers `1 / 29` to `29 / 29`, zero wrong
- fonts: Calibri and Consolas only
- off-palette colours: 0
- float coordinates: 0
- non-ASCII characters in Consolas runs: 0
- `kind` / `yum` / `ec2-user` leftovers: 0

Lab `Lab_week05_v2.pptx`:
- 11 slides, canvas 13.333 in
- footers `1 / 11` to `11 / 11`, zero wrong
- fonts: Calibri and Consolas only
- off-palette colours: 0
- float coordinates: 0
- non-ASCII characters in Consolas runs: 0
- `kind` / `yum` / `ec2-user` leftovers: 0

Lab code:
- `terraform init`, `validate` and `fmt` all pass
- `bash -n` passes on all three shell files
- zero non-ASCII bytes

## Issues / Notes

- **The lab is not launched on AWS.** No credentials are available in this session,
  so the three nodes are not built and the cluster is not proven end to end. The
  code validates, and it follows the Week 04 pattern that was proven on AWS.
- Ubuntu 26.04 is chosen to match Week 02 and Week 03. The Week 04 kubeadm
  reference repository uses Ubuntu 24.04. The Kubernetes packages come from
  `pkgs.k8s.io`, which is the same for both releases.
- Three things from the audit are NOT changed, because each one is a deletion and
  you did not ask for a deletion:
  1. `Week05/` still holds 29 `.pptx` files and 58 MB.
  2. `week5_code/week5_code/` is still a nested duplicate (its zero-width spaces
     are removed).
  3. `Week04/` still holds three stray Week 05 files.
- Week 05 is still absent from `~/Documents/c/r/CLO835_Fall_2026`, which now holds
  Week01, Week02 and Week03 only. Week 04 is absent as well.
