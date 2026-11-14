#!/usr/bin/env bash
# CLO835 Week 02 - print the current addresses of the machine.
#
# The Learner Lab stops the machine at the end of each session.
# The public address changes after each start.
# This script reads the real address from AWS, and it prints both addresses.
#
# Use:  ./ips.sh

set -euo pipefail
cd "$(dirname "$0")"

if [ ! -f terraform.tfstate ]; then
  echo "No state file. Run 'terraform apply' first."
  exit 1
fi

echo "Reading the current state from AWS ..."
terraform refresh -input=false >/dev/null

PUB=$(terraform output -raw public_ip)
PRIV=$(terraform output -raw private_ip)
ID=$(terraform output -json machine | python3 -c 'import json,sys;print(json.load(sys.stdin)["instance_id"])')
AZ=$(terraform output -json machine | python3 -c 'import json,sys;print(json.load(sys.stdin)["availability_zone"])')

cat <<TXT

  CLO835 - Week 02 - The manual demonstration machine
  ---------------------------------------------------
  Instance      $ID   ($AZ)
  Public IP     $PUB
  Private IP    $PRIV

  SSH           ssh -i ~/.ssh/mazSeneca ubuntu@$PUB
  Manual run    http://$PUB:8080/
  Container run http://$PUB:18080/

TXT
