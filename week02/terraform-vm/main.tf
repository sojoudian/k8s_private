# ---------------------------------------------------------------------------
# Network data
# The Learner Lab does not permit a new VPC. The default VPC is the only option.
# ---------------------------------------------------------------------------

data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

data "aws_subnet" "each" {
  for_each = toset(data.aws_subnets.default.ids)
  id       = each.value
}

# Not every availability zone offers every instance type.
# This data source finds the zones that offer the selected type.
data "aws_ec2_instance_type_offerings" "for_type" {
  location_type = "availability-zone"

  filter {
    name   = "instance-type"
    values = [var.instance_type]
  }
}

locals {
  good_zones = toset(data.aws_ec2_instance_type_offerings.for_type.locations)

  usable_subnet_ids = sort([
    for s in data.aws_subnet.each : s.id
    if contains(local.good_zones, s.availability_zone)
  ])

  subnet_id = var.subnet_id != "" ? var.subnet_id : try(local.usable_subnet_ids[0], "")
}

# ---------------------------------------------------------------------------
# The Ubuntu image
# Canonical owns account 099720109477.
# ---------------------------------------------------------------------------

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd*/ubuntu-*-${var.ubuntu_version}-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  filter {
    name   = "state"
    values = ["available"]
  }
}

# ---------------------------------------------------------------------------
# The firewall
# ---------------------------------------------------------------------------

resource "aws_security_group" "vm" {
  name_prefix = "${var.name}-"
  description = "CLO835 Week 02 manual demonstration VM"
  vpc_id      = data.aws_vpc.default.id

  tags = {
    Name = "${var.name}-sg"
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_vpc_security_group_ingress_rule" "ssh" {
  security_group_id = aws_security_group.vm.id
  description       = "SSH from the instructor"
  cidr_ipv4         = var.ssh_cidr
  ip_protocol       = "tcp"
  from_port         = 22
  to_port           = 22
}

resource "aws_vpc_security_group_ingress_rule" "app_manual" {
  security_group_id = aws_security_group.vm.id
  description       = "The Flask application in the manual run"
  cidr_ipv4         = var.app_cidr
  ip_protocol       = "tcp"
  from_port         = var.app_port_manual
  to_port           = var.app_port_manual
}

resource "aws_vpc_security_group_ingress_rule" "app_docker" {
  security_group_id = aws_security_group.vm.id
  description       = "The Flask application in the container run"
  cidr_ipv4         = var.app_cidr
  ip_protocol       = "tcp"
  from_port         = var.app_port_docker
  to_port           = var.app_port_docker
}

resource "aws_vpc_security_group_egress_rule" "all" {
  security_group_id = aws_security_group.vm.id
  description       = "All outbound traffic"
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}

# ---------------------------------------------------------------------------
# The virtual machine
# ---------------------------------------------------------------------------

resource "aws_instance" "vm" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  subnet_id                   = local.subnet_id
  key_name                    = var.key_name
  vpc_security_group_ids      = [aws_security_group.vm.id]
  associate_public_ip_address = true

  root_block_device {
    volume_type           = "gp3"
    volume_size           = var.root_volume_size
    iops                  = 3000
    throughput            = 125
    delete_on_termination = true

    tags = {
      Name = "${var.name}-root"
    }
  }

  # IMDSv2 only. This blocks the classic metadata credential attack.
  metadata_options {
    http_tokens                 = "required"
    http_endpoint               = "enabled"
    http_put_response_hop_limit = 1
  }

  user_data = templatefile("${path.module}/user_data.sh.tftpl", {
    repo_url        = var.repo_url
    app_port_manual = var.app_port_manual
    app_port_docker = var.app_port_docker
  })

  # A change to the script does not destroy the machine.
  user_data_replace_on_change = false

  tags = {
    Name = var.name
  }

  lifecycle {
    precondition {
      condition     = local.subnet_id != ""
      error_message = "No default subnet offers ${var.instance_type}. Select another instance type."
    }
  }
}
