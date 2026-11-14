# CLO835 — Week 02 — The manual demonstration machine

This Terraform code builds one Ubuntu machine on AWS.
The machine shows the students the manual method of an application deployment.
The students then see the same steps inside a Dockerfile.

## The machine

| Item | Value | Reason |
|---|---|---|
| Instance type | `r8i.large` | 2 vCPU, 16 GB, 3.9 GHz Intel Xeon 6. The Learner Lab blocks every larger size. |
| Image | Ubuntu 22.04 LTS | The Dockerfile starts with `FROM ubuntu:22.04`. |
| Disk | 30 GB gp3, 3000 IOPS | The maximum that the Learner Lab permits. |
| Key pair | You type it | Terraform asks for `key_name`. Type `Maziar`. The private key is `~/.ssh/mazSeneca`. |
| Open ports | 22, 8080, 18080 | SSH, the manual run, and the container run. |
| Docker | Not installed | The manual method must stay difficult. |

## Before each class

Perform these three steps.

1. Start the Learner Lab, and copy the new credentials into `~/.aws/credentials`.
   The credentials expire after 4 hours.
2. Find your public address.
   ```bash
   curl -s https://checkip.amazonaws.com
   ```
3. Put that address into `terraform.tfvars` as `ssh_cidr`, and add `/32`.
   Your address at the college is different from your address at home.

## Build the machine

```bash
cd week02/terraform-vm
terraform init
terraform apply
```

Terraform asks one question.

```
var.key_name
  The name of YOUR EC2 key pair...

  Enter a value: Maziar
```

Type `Maziar`, then press Enter. Two other methods skip the question.

```bash
terraform apply -var="key_name=Maziar"
```

Or remove the `#` from the `key_name` line in `terraform.tfvars`.

## The addresses

Every `terraform apply` ends with this block.

```
Outputs:

ips = {
  "private" = "172.31.x.x"
  "public"  = "54.x.x.x"
}
machine = {
  "ami_id"            = "ami-05a3e9423ae4d7a19"
  "availability_zone" = "us-east-1a"
  "instance_id"       = "i-0123456789abcdef0"
  "instance_type"     = "r8i.large"
  "private_ip"        = "172.31.x.x"
  "public_ip"         = "54.x.x.x"
  "root_disk_gb"      = 30
}
next_step = "ssh -i ~/.ssh/mazSeneca ubuntu@54.x.x.x   # public 54.x.x.x | private 172.31.x.x"
public_ip = "54.x.x.x"
private_ip = "172.31.x.x"
ssh_command = "ssh -i ~/.ssh/mazSeneca ubuntu@54.x.x.x"
url_manual_run = "http://54.x.x.x:8080/"
url_container_run = "http://54.x.x.x:18080/"
```

Read one value at any time.

```bash
terraform output -raw public_ip
terraform output -raw private_ip
```

The Learner Lab stops the machine at the end of each session, and the public
address changes after the next start. The state file then holds the old address.
Run this script to read the real addresses from AWS.

```bash
./ips.sh
```

## The class demonstration — part 1: the manual method

Open a session on the machine.

```bash
ssh -i ~/.ssh/mazSeneca ubuntu@<PUBLIC-IP>
```

Perform each step in front of the students.

| Step | Command | Time |
|---|---|---|
| 1. Clone | `git clone https://github.com/sojoudian/simple-webapp-flask` | fast |
| 2. Enter | `cd simple-webapp-flask` | fast |
| 3. Install Python | `sudo apt-get install -y python3 python3-pip` | slow |
| 4. Install Flask | `pip3 install flask` | slow |
| 5. Run | `python3 app.py` | fast |
| 6. Test | Open `http://<PUBLIC-IP>:8080/` | fast |

Show the students the problems of this method.

- You repeat every step on every new machine.
- You cannot move the result to another machine.
- The machine keeps the Python packages after you stop the application.
- A different Ubuntu version breaks step 4.

## The class demonstration — part 2: the container method

Perform these steps on your laptop, not on the machine.

| Step | Command |
|---|---|
| 1. Clone | `git clone https://github.com/sojoudian/simple-webapp-flask` |
| 2. Create | Open the `Dockerfile`. Show that lines 3 to 5 repeat steps 3 to 5 above. |
| 3. Build | `docker build -t simple-webapp-flask:v1 .` |
| 4. Test | `docker run -d -p 18080:18080 simple-webapp-flask:v1` |
| 5. Tag | `docker tag simple-webapp-flask:v1 <user>/simple-webapp-flask:v1` |
| 6. Publish | `docker push <user>/simple-webapp-flask:v1` |

## Stop the costs

Destroy the machine at the end of the class.

```bash
terraform destroy
```

The Learner Lab also stops the machine at the end of each session.
A stopped machine still pays for the 30 GB disk.

## Cost estimate

The Learner Lab blocks the AWS pricing API, so these numbers are estimates.

| Item | Rate | 4-hour class |
|---|---|---|
| `r8i.large` | approximately 0.14 USD each hour | 0.56 USD |
| 30 GB gp3 | approximately 0.0033 USD each hour | 0.01 USD |
| Public address | 0.005 USD each hour | 0.02 USD |
| **Total** | | **approximately 0.60 USD** |

The lab budget is 50 USD.

## The files

| File | Content |
|---|---|
| `versions.tf` | The Terraform version and the pinned AWS provider. |
| `variables.tf` | Every input, with a description. |
| `main.tf` | The image, the firewall, the machine, and the optional fixed address. |
| `outputs.tf` | The address, the SSH command, and the two web addresses. |
| `user_data.sh.tftpl` | The start script. It installs git only. |
| `terraform.tfvars` | The values that you change. |
| `ips.sh` | Prints the current public address and private address. |
