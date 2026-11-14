variable "region" {
  description = "The AWS region. The AWS Academy Learner Lab allows us-east-1 only."
  type        = string
  default     = "us-east-1"
}

variable "name" {
  description = "The name prefix for all resources."
  type        = string
  default     = "clo835-week02-manual"
}

variable "instance_type" {
  description = <<-EOT
    The EC2 instance type.
    The Learner Lab blocks every size of xlarge and larger.
    The maximum is 2 vCPU. r8i.large gives 2 vCPU, 16 GB, and a 3.9 GHz Intel Xeon 6 core.
    If the capacity is not available, use r7iz.large, r7a.large, or r7i.large.
  EOT
  type        = string
  default     = "r8i.large"
}

variable "ubuntu_version" {
  description = <<-EOT
    The Ubuntu LTS version.
    Use 22.04 to match the FROM line of the Dockerfile in the application repository.
    Version 24.04 blocks "pip3 install flask" with a PEP 668 error.
  EOT
  type        = string
  default     = "22.04"

  validation {
    condition     = contains(["22.04", "24.04"], var.ubuntu_version)
    error_message = "Set the ubuntu_version to 22.04 or to 24.04."
  }
}

variable "key_name" {
  description = "The name of YOUR EC2 key pair. Find it in the AWS Console, at EC2 > Key Pairs, in the Learner Lab. SSH uses this key pair. This variable has no default, so Terraform asks for it."
  type        = string
}

variable "root_volume_size" {
  description = "The size of the root disk in GB. The Learner Lab allows 30 GB."
  type        = number
  default     = 30
}

variable "ssh_cidr" {
  description = <<-EOT
    The source address range for SSH.
    Set this to your current public address with a /32 mask.
    Your address changes when you move from your home to the college.
  EOT
  type        = string
  default     = "173.33.124.240/32"
}

variable "app_cidr" {
  description = "The source address range for the web application ports. Students connect from many addresses."
  type        = string
  default     = "0.0.0.0/0"
}

variable "app_port_manual" {
  description = "The port of the manual run. The app.py file uses this port."
  type        = number
  default     = 8080
}

variable "app_port_docker" {
  description = "The port of the container run. The Dockerfile uses this port."
  type        = number
  default     = 18080
}

variable "repo_url" {
  description = "The Git address of the Flask application."
  type        = string
  default     = "https://github.com/sojoudian/simple-webapp-flask"
}

variable "subnet_id" {
  description = "An optional subnet. Leave this empty to let Terraform select a subnet that offers the instance type."
  type        = string
  default     = ""
}
