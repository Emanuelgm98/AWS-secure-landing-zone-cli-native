# Troubleshooting

- Terraform absent: local checks still cover Python contracts/docs; no install/download is performed here.
- `fmt` fails: review formatting with the approved Terraform CLI when available; this environment did not run Terraform.
- `validate` needs provider schemas: do not run `terraform init` under the current development-only constraint; obtain a separately authorized validation environment.
- Organizations/Config/CloudTrail errors: check organization feature set, delegated-admin setup, service access, region, service-linked roles and bucket/KMS policy with an approved future operator procedure.
- SCP unexpected denial: stop rollout, use tested break-glass access and inspect inherited policies/permission boundaries; do not remove controls blindly.
- Archive delivery failure: verify CloudTrail/Config service principals, bucket policy prefixes, KMS key policy and regional settings without exposing account secrets in logs.
