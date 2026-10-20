variable "permission_set_name" { type = string
  default = "ReadOnlyAudit" }
variable "session_duration" { type = string
  default = "PT1H" }
resource "aws_ssoadmin_permission_set" "readonly" {
  name = var.permission_set_name
  description = "Example read-only access
  identity store and assignments are managed outside this module."
  instance_arn = data.aws_ssoadmin_instances.current.arns[0]
  session_duration = var.session_duration
}
data "aws_ssoadmin_instances" "current" {}
resource "aws_ssoadmin_managed_policy_attachment" "readonly" {
  instance_arn = aws_ssoadmin_permission_set.readonly.instance_arn
  permission_set_arn = aws_ssoadmin_permission_set.readonly.arn
  managed_policy_arn = "arn:aws:iam::aws:policy/ReadOnlyAccess"
}
output "permission_set_arn" { value = aws_ssoadmin_permission_set.readonly.arn }
