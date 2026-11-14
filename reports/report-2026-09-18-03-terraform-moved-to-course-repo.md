# Report: The Week 02 Terraform moved into the public course repository

**Date**: 2026-09-18
**Sequence**: #03 for the day

## Summary

The professor asked why the Terraform code was not in
`/Users/maziar/Documents/c/r/CLO835_Fall_2026/Week02`. The reason is simple: the
professor never named that directory, and my working directory is
`/Users/maziar/Downloads/k8s_week3`. That repository is **public**, and it pushes
to `github.com/sojoudian/CLO835_Fall_2026`. I copied the code there, and I
removed two personal values first.

## What Changed

Created `Week02/terraform/` in the course repository, with 10 files.

| File | Note |
|---|---|
| `versions.tf` | Removed the tag `Owner = "Maziar"`. |
| `variables.tf` | `ssh_cidr` default changed from the home address to `0.0.0.0/0`. Added `private_key_path`. |
| `main.tf` | No change. |
| `outputs.tf` | The 2 fixed paths `~/.ssh/mazSeneca` now use `var.private_key_path`. |
| `user_data.sh.tftpl` | No change. |
| `ips.sh` | Now reads the SSH command from the output, not from a fixed path. |
| `README.md` | Rewritten for the students. Added the two-port explanation and 4 discussion questions. |
| `terraform.tfvars.example` | New. Follows the pattern of the week11 repository. |
| `terraform.tfvars` | The professor's private values. Git ignores this file. |
| `.gitignore` | Copied from `sojoudian/CLO835_week11_lab`, unchanged. |

## Technical Details

### The two values that must not go public

1. `ssh_cidr` held `173.33.124.240/32`. This is the professor's home address.
   A public repository must not hold it. The new default is `0.0.0.0/0`, because
   each student connects from a different address. The README explains how to
   make the value narrow.
2. The outputs held `~/.ssh/mazSeneca`. No student has that file. A new variable
   `private_key_path` holds the path, and its default is a placeholder.

The professor keeps both real values in `terraform.tfvars`. The `.gitignore`
file excludes that file, so git never sees it. I verified this with
`git check-ignore`.

### Verification

| Command | Result |
|---|---|
| `grep -rn "mazSeneca\|173.33.124.240\|Maziar"` | No match in the 9 tracked files. |
| `git status --porcelain -uall` | 9 files, and `terraform.tfvars` is absent. |
| `git check-ignore -v ...terraform.tfvars` | Matched by rule 6 of `.gitignore`. |
| `terraform validate` | Success. |
| `terraform plan -var="key_name=Maziar"` | 6 to add, 0 to change, 0 to destroy. |

## Results

The code works from the new location. No commit ran, and no push ran.

## Issues / Notes

- **Two copies now exist.** The old copy stays at
  `/Users/maziar/Downloads/k8s_week3/week02/terraform-vm/`. It still holds the
  home address and the personal key path. The two copies will diverge. I
  recommend the deletion of the old copy, but I did not delete it.
- SSH now accepts every address by default. The Ubuntu image accepts a key only,
  and it refuses a password, so the risk stays low. The professor's own
  `terraform.tfvars` narrows the range to the home address.
- The repository `Week01` directory is still empty.
