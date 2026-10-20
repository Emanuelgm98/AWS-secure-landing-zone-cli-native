variable "organization_id" { type = string
  description = "Existing AWS Organizations ID (provided during a future approved deployment)." }
variable "accounts" { type = map(object({ name = string, email = string, ou_name = string }))
  default = {} }
resource "aws_organizations_organization" "this" {
  aws_service_access_principals = ["cloudtrail.amazonaws.com", "config.amazonaws.com"]
  feature_set = "ALL"
}
resource "aws_organizations_account" "this" {
  for_each = var.accounts
  name = each.value.name
  email = each.value.email
  parent_id = var.organization_id
  close_on_deletion = false
  lifecycle { prevent_destroy = true }
}
output "organization_arn" { value = aws_organizations_organization.this.arn }
output "account_ids" { value = { for key, account in aws_organizations_account.this : key => account.id } }
