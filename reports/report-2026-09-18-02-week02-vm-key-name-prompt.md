# Report: Week 02 VM — the key pair now asks, like the week11 repository

**Date**: 2026-09-18
**Sequence**: #02 for the day

## Summary

The professor asked me to handle the key pair in the same way as the repository
`sojoudian/CLO835_week11_lab`. That repository declares `key_name` with no
default value, so Terraform stops and asks for it. I removed the default from my
`key_name` variable. I changed nothing else, because the professor said "only the
key part".

## What Changed

| File | Change |
|---|---|
| `variables.tf` | Removed `default = "Maziar"` from `key_name`. Rewrote the description to match the week11 wording. |
| `terraform.tfvars` | Commented out the `key_name` line. A value there would stop the question. |
| `README.md` | The machine table now says "You type it". The build section shows the question and two methods that skip it. |

## Technical Details

A Terraform variable with no default is a required variable. Terraform asks for
the value at each plan and at each apply. The week11 repository uses this pattern
because each student has a different key pair.

A value in `terraform.tfvars` also satisfies a required variable. So the removal
of the default alone was not enough. I also commented out the `key_name` line in
`terraform.tfvars`.

## Results

| Test | Command | Result |
|---|---|---|
| The question appears | `terraform plan -input=false` | `Error: No value for required variable` |
| The value works | `terraform plan -input=false -var="key_name=Maziar"` | `Plan: 6 to add, 0 to change, 0 to destroy.` |
| The code is valid | `terraform validate` | Success. |

Test 1 proves the question. With `-input=false` Terraform cannot ask, so it
fails. In a normal run Terraform asks instead.

## Issues / Notes

- The `ssh_command` output and the `ips.sh` script still hold the fixed path
  `~/.ssh/mazSeneca`. This is the private key file, not the key pair name. I did
  not change it, because the professor limited the change to the key part. A
  student needs a different path.
- The professor now types `Maziar` at each plan and each apply. To stop the
  question, remove the `#` from the `key_name` line in `terraform.tfvars`.
