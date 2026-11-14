# Report: Week 02 audit against the week11 reference repository

**Date**: 2026-09-18
**Sequence**: #04 for the day

## Summary

The professor asked why two personal values reached a public repository, and
asked me to audit `CLO835_Fall_2026/Week02` for other problems. I read the whole
reference repository `sojoudian/CLO835_week11_lab`, and I compared every pattern.
I found 7 more differences, and I fixed all of them.

## The cause of the two mistakes

I built the code as a private demonstration in a scratch directory. My own IP
address and my own key path were correct there. The professor then gave the
reference repository with the words "only the key part", so I changed one
variable. I treated the reference as a style note about that variable. It is the
model for the whole deliverable. The moment the target became a public,
student-facing repository, every pattern of the reference applied.

## The 7 further issues, and the fixes

| # | Issue | Fix |
|---|---|---|
| 1 | No IAM instance profile. The reference attaches `LabInstanceProfile` to every node. | Added the `lab_instance_profile` variable, with the reference default, and attached it. |
| 2 | No `commands.sh`. The reference holds the lab commands in one file, run section by section. | Wrote `commands.sh`: Part 1 on the machine (6 steps), Part 2 on the laptop (6 steps). |
| 3 | The README had no numbered structure and no Prerequisites. | Rewrote it in the reference structure: Prerequisites, 1. credentials, 2. apply, 3. addresses, 4. the lab, 5. destroy. |
| 4 | The README never said `chmod 400` for the key file. | Added it to section 2. |
| 5 | `ips.sh` called `python3` to read the outputs. A student may not have `python3` on the laptop. | Added the `instance_id` and `availability_zone` outputs, and rewrote `ips.sh` with `terraform output -raw` only. |
| 6 | `user_data.sh.tftpl` said "The instructor performs each step". | Changed to student wording. |
| 7 | `terraform.tfvars.example` did not mention the instance profile. | Added the commented line, in the reference style. |

## Results

| Check | Result |
|---|---|
| `terraform fmt -recursive` | Clean. |
| `terraform validate` | Success. |
| `terraform plan -var="key_name=Maziar"` | 6 to add, 0 to change, 0 to destroy. The plan shows `iam_instance_profile = "LabInstanceProfile"`. |
| Personal-data scan | No match for `mazSeneca`, `173.33.124.240`, `Maziar`, the email, or `/Users/maziar` in any tracked file. |
| `git status -uall` | 10 tracked files. `terraform.tfvars` stays hidden. |

## Issues / Notes

- No commit ran, and no push ran.
- The old copy still exists at
  `/Users/maziar/Downloads/k8s_week3/week02/terraform-vm/`, and it still holds
  the home address and the personal key path. I recommend the deletion of that
  copy.
- The repository `Week01` directory is still empty, and the root `README.md`
  holds 19 bytes.
- I saved the lesson as the memory `feedback-reference-repo-is-the-whole-model`.
