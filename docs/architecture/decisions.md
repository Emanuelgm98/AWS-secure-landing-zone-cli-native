# Architecture decisions

- Terraform is an additive reference track; CloudFormation templates remain for compatibility.
- Root configurations are separated by account responsibility to permit reviewed state and approval boundaries.
- No remote backend, state bucket, organization ID, account ID, or credentials are embedded. Local state is sensitive and should not be created until a deployment design is approved.
- Provider and CLI constraints are documented placeholders because no approved local Terraform version was supplied. Workflow pins are illustrative only and must be reviewed.
- SCP examples are opt-in and require policy simulation/review. An SCP limits maximum permissions and does not grant access. Never claim root exclusion, universal coverage, or lockout prevention; policy inheritance, management account behavior, break-glass access and service exceptions need account-specific testing.
- The archive module enables public-access blocks, versioning, KMS encryption, and insecure-transport denial. Service delivery bucket policy, object lock, replication, lifecycle, and audit retention are intentionally unfinished prerequisites.
- OIDC trust is an inert JSON example with replacement values. It grants no access until separately provisioned and permission-scoped.
