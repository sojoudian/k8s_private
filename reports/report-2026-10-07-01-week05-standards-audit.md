# Report: Week 05 Lecture and Lab — Standards Audit
**Date**: 2026-10-07
**Sequence**: #01 for the day

## Summary
The Week 05 lecture and lab do not meet the standard set by Week 01 to Week 04.
The audit finds 14 defects. Three of them stop a student: the footer numbering is
wrong on all 40 slides, `terraform init` fails, and three shell commands carry an
EN DASH instead of a hyphen. No file was changed.

## What Changed
Nothing. The audit is read-only. One scratch copy of the Terraform ran `init` and
`validate` in the session scratchpad.

## Technical Details

### Decks audited
- `Week05/lecture_week05.pptx` — 29 slides, 1 hidden
- `Week05/Lab_week05.pptx` — 11 slides
- `Week05/Week05_lab_style_v26.pptx` — 29 slides, identical audit result to the lecture
- `week05_practical_work/week5_code/` — the lab code

### What the decks PASS
- Canvas 13.333 in (16:9).
- Fonts: Calibri and Consolas only. No third typeface.
- Float coordinates: 0. The teleport bug is absent.
- Whale glyph and footer present on every slide.

### Defect list

**D1 — Footer numbering wrong on every slide (40 of 40).**
The lecture footers read `1 / 39` to `28 / 39` over 29 slides. The lab footers read
`29 / 39` to `39 / 39` over 11 slides. Both decks were split out of the 39-slide
master and kept the master numbering. The lecture must read `N / 29`. The lab must
read `N / 11`.

**D2 — `terraform init` fails. The lab cannot start.**
`sg.tf` calls `terraform-aws-modules/security-group/aws` with no `version`.
Terraform resolves 6.0.0, which removed `ingress_cidr_blocks`. Proven:
```
Error: Unsupported argument
  on sg.tf line 8, in module "dev_ssh_sg":
   8:   ingress_cidr_blocks = ["127.0.0.1/32"]
```

**D3 — EN DASH inside three shell commands.**
A student who copies these gets an error.
- `lecture` slide 19: `–image`
- `lecture` slide 19: `kubectl create –f kubia-descriptor.yaml`
- `lab` slide 7: `kubectl get all –n pingpong`

**D4 — `week5.pub` is missing.**
`ec2.tf` line 54 reads `public_key = file("${path.module}/week5.pub")`. The file does
not exist. `terraform apply` fails after D2 is fixed.

**D5 — Two security groups share the name `ec2_sg`.**
`sg.tf` names both `dev_ssh_sg` and `ec2_sg` as `ec2_sg`. AWS rejects the duplicate.

**D6 — The NodePort ports are not open.**
`kind.yaml` maps 30000 and 30001 to the host. The security groups open port 22 only.
A browser cannot reach the application.

**D7 — Two zero-width spaces in the code.**
`ec2.tf` line 33 and `kind.yaml` line 5 each end with U+200B. The `kind create
cluster` line and the node image digest both carry an invisible character.

**D8 — The lab still teaches kind.**
Week 04 now builds a real kubeadm cluster, 1 master and 2 workers. Week 05 builds a
single-node kind cluster on Amazon Linux 2. The two weeks contradict each other.

**D9 — Amazon Linux 2 and `yum`.**
`ec2.tf` selects `amzn2-ami-hvm-*-x86_64-ebs`. Amazon Linux 2 reached end of life on
30 June 2025. Weeks 02, 03 and 04 use Ubuntu.

**D10 — kind v0.11.0 and `kindest/node:v1.23.17`.**
Both date from 2021. The course teaches Kubernetes 1.35.

**D11 — The Terraform ignores the Week 02 to Week 04 pattern.**
- `instance_type = "t3.medium"`, not the proven `m5.large`.
- `key_name = "week5"` hardcoded, not prompted.
- No subnet selection by `aws_ec2_instance_type_offerings`.
- `output.tf` prints the public IP only. You asked for the public AND the private IP
  on every run.
- No `required_providers` block and no provider version.

**D12 — No `localMachine.sh`, no `cleanup_lab05.sh`, no `README.md`.**
Weeks 02, 03 and 04 all ship these three files.

**D13 — Off-palette colours in the lecture.**
- `E74C3C` on 6 slides (14, 17, 20, 22, 23, 24). The house red is `FF5F56`.
- `B8AB9A`, `8B7E6E`, `DED2C1`, `CFCFCF`, `6A8AB8` on slide 7. The three-tier diagram
  is beige and grey, not house blue.

**D14 — Four source screenshots remain as pictures.**
Lecture slides 3, 5, 9 and 18 hold PNG screenshots that cover 36 %, 58 %, 33 % and
39 % of the slide. PROMPT.md rule 4 asks for a native diagram.

### Housekeeping found, not a defect
- `Week05/` holds 29 `.pptx` files and 58 MB. `v1` to `v25` are superseded.
- `week05_practical_work/week5_code/week5_code/` is a nested duplicate.
- `init_kind.sh` duplicates the `user_data` block and nothing calls it.
- `Week04/` holds three stray Week 05 files.
- `~/Documents/c/r/CLO835_Fall_2026` now holds Week01, Week02 and Week03 only.
  Week 04 and Week 05 are not in the public repo.

## Results
Verdict: the Week 05 lecture and lab do NOT meet the standard. The design shell is
right. The content, the numbering and the lab code are not.

Verified in this session:
- `terraform init` failure reproduced with Terraform v1.16.4.
- Footer denominators read `['1','39']` on 29-slide and 11-slide decks.
- Non-ASCII bytes located by `grep -nP '[^\x00-\x7F]'`.
- Palette compared against the union of Week01 v5, Week02 v1 and Week03 v1.

## Issues / Notes
No file was changed and no AWS resource was created. The fixes wait for your word.
