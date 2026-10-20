variable "parent_id" { type = string }
variable "unit_names" { type = set(string)
  default = ["Security", "Workloads"] }
resource "aws_organizations_organizational_unit" "this" {
  for_each = var.unit_names
  name = each.value
  parent_id = var.parent_id
}
output "ou_ids" { value = { for name, ou in aws_organizations_organizational_unit.this : name => ou.id } }
