variable "bucket_name" { type = string }
variable "kms_key_arn" { type = string }
resource "aws_cloudtrail" "organization" {
  name = "organization-trail"
  s3_bucket_name = var.bucket_name
  is_multi_region_trail = true
  is_organization_trail = true
  enable_log_file_validation = true
  kms_key_id = var.kms_key_arn
  include_global_service_events = true
  lifecycle { prevent_destroy = true }
}
output "trail_arn" { value = aws_cloudtrail.organization.arn }
