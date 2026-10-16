# AWS Secure Landing Zone CLI-native

CLI-first reference implementation for isolated `dev` and `prod` environments in `us-east-1`. Infrastructure is described with AWS CloudFormation JSON and can be inspected, validated and tested locally without AWS credentials.

> **Safety:** this repository intentionally does not execute infrastructure changes. `scripts/validate.py` and the test suite are local-only. CloudFormation templates can create billable AWS resources; deployment commands are documented for a separately approved future operation and were not run here.

## Quick start (local only)

```powershell
python scripts/validate.py
python -m unittest discover -s tests -v
python scripts/plan.py --environment dev
./scripts/run-local-checks.ps1
```

See [docs/PHASES.md](docs/PHASES.md), [architecture](docs/ARCHITECTURE.md), and [Phase 0 review](docs/phase-0-review.md). All eight implementation phases have a script, local proof, short ADR, verification command, and evidence checklist under `docs/phases/`.

`scripts/plan.py` is a local-only dry plan; it is not a CloudFormation change set. `scripts/aws-readonly-validate.ps1` is optional and calls only STS identity and CloudFormation `ValidateTemplate`. There is no deploy/update/delete helper in this repository.

## Proposed components

- Network: VPC, two AZs, public/private/data subnets, 1 NAT for dev and 1 per AZ for prod.
- App: ALB, ECS Fargate, ECR, private tasks, CloudWatch log group.
- Data: Aurora PostgreSQL Serverless v2 at min 0.5 ACU (one writer in dev; writer plus reader in prod).
- Security baseline: CloudTrail, AWS Config recorder/delivery channel, GuardDuty, Security Hub opt-in, KMS, and illustrative least-privilege IAM/SCP policy documents.
- Operations: local validation, cost inputs, environment parameter files, and read-only evidence commands.

Account-level services and SCPs need a management/delegated administrator account and organization-specific review. They are not auto-enabled by local validation.
