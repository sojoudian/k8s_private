# Change the values here. Do not change the code.

instance_type  = "r8i.large" # 2 vCPU, 16 GB, 3.9 GHz Intel Xeon 6
ubuntu_version = "22.04"     # matches the FROM line of the Dockerfile
# key_name has no default. Terraform asks for it at each plan and each apply.
# Remove the "#" below to stop the question.
# key_name = "Maziar"

# Set this to your current public address before each class.
# Find the address with this command:  curl -s https://checkip.amazonaws.com
ssh_cidr = "173.33.124.240/32"

# The students open the application from many addresses.
app_cidr = "0.0.0.0/0"
