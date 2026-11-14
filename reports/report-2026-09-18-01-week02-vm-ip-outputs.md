# Report: Week 02 VM — address outputs, and the Elastic IP removal

**Date**: 2026-09-18
**Sequence**: #01 for the day

## Summary

The professor does not need a fixed public address. I removed the Elastic IP
from the Terraform code. The professor wants every run to print the public
address and the private address. I rewrote the outputs in the style of the
professor's own repository `sojoudian/CLO835_week11_lab`, which uses
`public_ips`, `private_ips`, and `next_step`. I also added a small script that
reads the real addresses from AWS after a stop and a start.

## What Changed

| File | Change |
|---|---|
| `main.tf` | Removed `aws_eip` and `aws_eip_association`. 190 lines to 171 lines. |
| `variables.tf` | Removed the `use_elastic_ip` variable. |
| `outputs.tf` | Rewritten. 8 outputs to 10 outputs. Added `private_ip`, `public_dns`, `ips`, `machine`, and `next_step`. |
| `terraform.tfvars` | Removed the `use_elastic_ip` line. |
| `ips.sh` | New. Refreshes the state, then prints both addresses. |
| `README.md` | New section "The addresses", with the example output block. |

## Technical Details

### The style of the old repository

I read `sojoudian/CLO835_week11_lab`. Its `main.tf` ends with three outputs.

- `public_ips` — a map of the node name to the public address.
- `private_ips` — a map of the node name to the private address.
- `next_step` — one line that holds the SSH command.

This machine is a single machine, so a map of nodes has no value. I kept the
pattern, and I made the outputs flat.

| Output | Content |
|---|---|
| `public_ip` | The public address alone. |
| `private_ip` | The private address alone. |
| `public_dns` | The public name. |
| `ips` | Both addresses in one object. |
| `machine` | The full description: identifier, type, zone, both addresses, image, disk. |
| `ssh_command` | The SSH command. |
| `url_manual_run` | The web address on port 8080. |
| `url_container_run` | The web address on port 18080. |
| `next_step` | The SSH command with both addresses in a comment. |

### The reason for ips.sh

Terraform prints the outputs at the end of each apply. It reads those values
from the state file. The Learner Lab stops the machine at the end of each
session, and AWS gives a new public address at the next start. The state file
then holds the old address, and `terraform output` prints a wrong value.

The `ips.sh` script runs `terraform refresh` first, so it always prints the real
address.

## Results

| Command | Result |
|---|---|
| `terraform fmt -recursive` | Clean. |
| `terraform validate` | Success. |
| `terraform plan` | 6 to add, 0 to change, 0 to destroy. |

The plan shows all 10 outputs. The `machine` output already resolves the image
name, the instance type, and the disk size before the apply.

No `apply` ran. The machine does not exist yet.

## Issues / Notes

- The removal of the Elastic IP is a direct answer to the professor's statement:
  "I do not mind the IP changes." The professor can add it again later.
- AWS charges approximately 0.005 USD each hour for the public address. This
  charge applies with or without an Elastic IP.
- The `ssh_cidr` value is still the home address `173.33.124.240/32`. The
  professor must update it at the college.
