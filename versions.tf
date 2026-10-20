terraform {
  required_version = ">= 1.5.0, < 2.0.0" # placeholder constraint; validate and pin an approved local version before adoption
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" } # placeholder; no provider version is asserted or installed
  }
}
