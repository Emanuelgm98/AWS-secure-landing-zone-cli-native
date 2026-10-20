variable "target_id" { type = string }
variable "policy_name" { type = string
  default = "DenyAuditControlPlaneTampering" }
resource "aws_organizations_policy" "this" {
  name = var.policy_name
  type = "SERVICE_CONTROL_POLICY"
  description = "Example defense in depth for audit controls
  requires compatibility review before attachment."
  content = file("${path.module}/../../../policies/scp/deny-audit-tampering.json")
}
resource "aws_organizations_policy_attachment" "this" { policy_id = aws_organizations_policy.this.id
  target_id = var.target_id }
output "policy_id" { value = aws_organizations_policy.this.id }
