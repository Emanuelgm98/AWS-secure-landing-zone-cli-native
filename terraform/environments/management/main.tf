module "organization" { source = "../../modules/organizations"
  organization_id = var.organization_id
  accounts = var.accounts }
module "security_ou" { source = "../../modules/organizational-units"
  parent_id = var.root_id
  unit_names = ["Security", "Workloads"] }
variable "organization_id" { type = string
  description = "Existing organization ID
  supplied only for a reviewed future deployment." }
variable "root_id" { type = string
  description = "Organization root ID." }
variable "accounts" { type = map(object({ name=string, email=string, ou_name=string }))
  default = {} }
output "organization_arn" { value = module.organization.organization_arn }
output "account_ids" { value = module.organization.account_ids }
