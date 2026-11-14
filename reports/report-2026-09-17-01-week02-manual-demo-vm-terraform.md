# Report: Week 02 manual demonstration VM — Terraform

**Date**: 2026-09-17
**Sequence**: #01 for the day

## Summary

I wrote Terraform code that builds one Ubuntu EC2 machine in the AWS Academy
Learner Lab. The machine supports the Week 02 lecture. The professor deploys the
Flask application by hand on the machine, and the students see how much work the
manual method needs. The professor then shows the same steps inside a Dockerfile.
The code passes `terraform validate` and `terraform plan` against the live lab
account 629512658466.

## What Changed

Created the directory `week02/terraform-vm/`.

| File | Content |
|---|---|
| `versions.tf` | Terraform >= 1.5.0. The AWS provider is pinned to `~> 6.0`. |
| `variables.tf` | 13 inputs. Each input has a description. |
| `main.tf` | The image, the firewall, the machine, and the optional fixed address. |
| `outputs.tf` | 8 outputs, including the SSH command and the two web addresses. |
| `user_data.sh.tftpl` | The start script. It installs git only. |
| `terraform.tfvars` | The values that the professor changes before each class. |
| `README.md` | The class runbook, with both demonstration parts. |
| `.gitignore` | Excludes the state and the provider cache. |

## Technical Details

### The instance type

I tested 33 instance types with `run-instances --dry-run` against the live lab.
The lab blocks every size of `xlarge` and larger, so 2 vCPU is the hard ceiling.
The professor asked for 4 vCPU, which the lab does not permit.

I then compared the clock speed of every allowed type with 16 GB.

| Type | RAM | Clock | Core | EBS |
|---|--:|--:|---|--:|
| `r8i.large` | 16 GB | 3.9 GHz | Intel Xeon 6 | 10 Gbps |
| `r7iz.large` | 16 GB | 3.9 GHz | Sapphire Rapids | 10 Gbps |
| `z1d.large` | 16 GB | 4.0 GHz | Cascade Lake, 2019 | 3.2 Gbps |
| `r7a.large` | 16 GB | 3.7 GHz | AMD Genoa | 10 Gbps |
| `r7i.large` | 16 GB | 3.2 GHz | Sapphire Rapids | 10 Gbps |

I selected `r8i.large`. It has the newest core and the full disk bandwidth.
`z1d.large` shows a higher clock, but its core is 7 years old and it gives one
third of the disk bandwidth.

### The Ubuntu version

I read the Dockerfile in `sojoudian/simple-webapp-flask`. It starts with
`FROM ubuntu:22.04`. I set the machine to Ubuntu 22.04 for two reasons.

1. Each manual command matches one Dockerfile line, so the comparison is exact.
2. Ubuntu 24.04 blocks `pip3 install flask` with a PEP 668 error.

The `ubuntu_version` variable changes this to 24.04.

### The ports

The repository uses two different ports.

- `app.py` uses port 8080 when the user runs `python3 app.py`.
- The Dockerfile uses port 18080 with `flask run --port=18080`.

The firewall opens both ports, so both demonstrations work.

### Other decisions

- The start script installs git only. It does not install Docker, pip, or Flask.
  The professor performs those steps live.
- The code selects the subnet automatically. It reads
  `aws_ec2_instance_type_offerings` and it picks a zone that offers the type.
  A `precondition` stops the apply with a clear message if no zone offers it.
- The machine requires IMDSv2.
- The fixed public address is optional, and it defaults to off.
- The key pair `Maziar` already exists in the account. Its MD5 fingerprint
  matches `~/.ssh/mazSeneca.pub`, so no import is necessary.

## Results

| Command | Result |
|---|---|
| `terraform fmt -recursive` | Clean. |
| `terraform init` | AWS provider 6.65.0 installed. |
| `terraform validate` | Success. |
| `terraform plan` | 6 to add, 0 to change, 0 to destroy. |

The plan resolves these values.

- AMI `ami-05a3e9423ae4d7a19` (`ubuntu-jammy-22.04-amd64-server-20260904`)
- Instance type `r8i.large`
- Subnet `subnet-00cb06a3536f3a884`
- Key pair `Maziar`
- Root disk 30 GB gp3, 3000 IOPS, 125 MB/s
- `http_tokens = required`

No `apply` ran. The machine does not exist yet.

## Issues / Notes

- The lab blocks the AWS pricing API for the `voclabs` role, so the cost table in
  the README shows estimates. The estimate is approximately 0.60 USD for a
  4-hour class, against a 50 USD budget.
- The `ssh_cidr` value is `173.33.124.240/32`. This is the professor's address at
  home. The address at the college is different, and SSH fails until the
  professor updates the value.
- The lab credentials expire after 4 hours. Terraform fails after that time
  until the professor copies new credentials into `~/.aws/credentials`.
- The Learner Lab stops the machine at the end of each session. The public
  address changes after each start, unless `use_elastic_ip` is true.
