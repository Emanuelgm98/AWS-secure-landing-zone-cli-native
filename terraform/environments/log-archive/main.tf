variable "bucket_name" { type = string }
module "archive" { source = "../../modules/log-archive"
  bucket_name = var.bucket_name }
output "bucket_name" { value = module.archive.bucket_name }
