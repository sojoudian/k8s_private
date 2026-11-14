# Every apply prints these values.
# Read the addresses again at any time with this command:
#   terraform output
# The public address changes after each stop and start in the Learner Lab.
# Refresh the state first with the ./ips.sh script.

output "public_ip" {
  description = "The public address. You connect to this address."
  value       = aws_instance.vm.public_ip
}

output "private_ip" {
  description = "The private address inside the VPC."
  value       = aws_instance.vm.private_ip
}

output "public_dns" {
  description = "The public name of the machine."
  value       = aws_instance.vm.public_dns
}

output "ips" {
  description = "Both addresses together."
  value = {
    public  = aws_instance.vm.public_ip
    private = aws_instance.vm.private_ip
  }
}

output "machine" {
  description = "The full description of the machine."
  value = {
    instance_id       = aws_instance.vm.id
    instance_type     = aws_instance.vm.instance_type
    availability_zone = aws_instance.vm.availability_zone
    public_ip         = aws_instance.vm.public_ip
    private_ip        = aws_instance.vm.private_ip
    ami_id            = data.aws_ami.ubuntu.id
    ami_name          = data.aws_ami.ubuntu.name
    root_disk_gb      = var.root_volume_size
  }
}

output "ssh_command" {
  description = "The command that opens a session on the machine."
  value       = "ssh -i ~/.ssh/mazSeneca ubuntu@${aws_instance.vm.public_ip}"
}

output "url_manual_run" {
  description = "The address of the application after the manual run."
  value       = "http://${aws_instance.vm.public_ip}:${var.app_port_manual}/"
}

output "url_container_run" {
  description = "The address of the application after the container run."
  value       = "http://${aws_instance.vm.public_ip}:${var.app_port_docker}/"
}

output "next_step" {
  description = "The first command of the class."
  value       = "ssh -i ~/.ssh/mazSeneca ubuntu@${aws_instance.vm.public_ip}   # public ${aws_instance.vm.public_ip} | private ${aws_instance.vm.private_ip}"
}
