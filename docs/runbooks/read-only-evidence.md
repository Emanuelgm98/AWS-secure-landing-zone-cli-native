# Read-only AWS evidence collection

Run only after a separately authorized deployment, from the approved account and region. These commands inspect state and do not alter resources.

```powershell
aws sts get-caller-identity
aws cloudformation describe-stacks --stack-name <stack> --region us-east-1
aws ec2 describe-vpcs --filters Name=tag:Environment,Values=<dev|prod> --region us-east-1
aws rds describe-db-clusters --region us-east-1
aws ecs describe-services --cluster <cluster> --services <service> --region us-east-1
aws cloudtrail get-trail-status --name slz-audit --region us-east-1
aws guardduty list-detectors --region us-east-1
aws securityhub describe-hub --region us-east-1
```

Do not include credentials, secret values, private log payloads or personal data in evidence. Redact account identifiers before sharing outside the approved team.
