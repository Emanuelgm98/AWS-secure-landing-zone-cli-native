# Design decisions

## CloudFormation JSON

CloudFormation JSON keeps this AWS-only reference within AWS CLI and CloudFormation workflows without a second state engine. The trade-off is verbose syntax and no multi-cloud portability. cfn-lint, Checkov and reviewed change sets are required before deployment.

## Two Availability Zones

Templates parameterize two AZs, matching the implemented subnet and route-table count. A third AZ is an extension, not a current property.

## Cost and resilience split

Dev uses one NAT gateway and one Aurora writer. Prod uses a NAT gateway per AZ and can add an Aurora reader. This lowers baseline development cost while making production failure domains explicit; cost and recovery objectives still need service-owner approval.

## Staged account security controls

The audit stack is opt-in because CloudTrail, Config, GuardDuty and Security Hub affect account-level controls and may require management/delegated-administrator review. Production enablement needs a separate ownership, retention and cost decision.

## Threat model and limits

The intended boundary exposes HTTPS at the ALB and keeps ECS tasks and Aurora private. Security groups, Secrets Manager and KMS reduce network exposure and credential/data risk. Audit services support detection when enabled. These are template intentions, not deployed or independently scanner-verified properties. Risks still include application vulnerabilities, compromised authorized identities, IAM misconfiguration, region-wide outages, cost spikes, and missing workload-specific recovery objectives.
