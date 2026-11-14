# CLO835 - Week 02 - Manual "hard way" demonstration VM
# Terraform and provider versions are pinned on purpose.
# An unpinned version caused the Week 05 lab to fail.

terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = var.region

  default_tags {
    tags = {
      Course    = "CLO835"
      Week      = "02"
      Purpose   = "Manual-deploy-demo"
      ManagedBy = "Terraform"
      Owner     = "Maziar"
    }
  }
}
