variable "bucket_name" { type = string }
resource "aws_kms_key" "archive" { description = "Organization log archive encryption"
  enable_key_rotation = true
  deletion_window_in_days = 30
  lifecycle { prevent_destroy = true } }
resource "aws_s3_bucket" "archive" { bucket = var.bucket_name
  force_destroy = false
  lifecycle { prevent_destroy = true } }
resource "aws_s3_bucket_versioning" "archive" { bucket = aws_s3_bucket.archive.id
  versioning_configuration { status = "Enabled" } }
resource "aws_s3_bucket_server_side_encryption_configuration" "archive" {
  bucket = aws_s3_bucket.archive.id
  rule { apply_server_side_encryption_by_default { sse_algorithm = "aws:kms"
  kms_master_key_id = aws_kms_key.archive.arn }
  bucket_key_enabled = true }
}
resource "aws_s3_bucket_public_access_block" "archive" { bucket = aws_s3_bucket.archive.id
  block_public_acls = true
  block_public_policy = true
  ignore_public_acls = true
  restrict_public_buckets = true }
resource "aws_s3_bucket_policy" "archive" {
  bucket = aws_s3_bucket.archive.id
  policy = jsonencode({ Version="2012-10-17", Statement=[{Sid="DenyInsecureTransport", Effect="Deny", Principal="*", Action="s3:*", Resource=[aws_s3_bucket.archive.arn, "${aws_s3_bucket.archive.arn}/*"], Condition={Bool={"aws:SecureTransport"="false"}}}] })
}
output "bucket_name" { value = aws_s3_bucket.archive.bucket }
output "kms_key_arn" { value = aws_kms_key.archive.arn }
