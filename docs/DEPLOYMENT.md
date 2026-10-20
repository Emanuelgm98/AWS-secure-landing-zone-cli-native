# Preparation and future deployment guide

## Local and AWS boundary

Local commands (`validate.py`, `plan.py`, tests, `preflight.py`, cfn-lint and Checkov) read repository files only. They do not need AWS CLI, credentials, or network access. The deploy, verify and destroy entry points intentionally return a clear `BLOCKED` status without invoking any AWS command. No AWS operation has been performed as part of this preparation.

Do not pass credentials into local checks. This guide does not instruct operators to configure credentials. A real deployment workflow, account binding, IAM role, change-set review, and approval process must be designed and approved separately before the blocked scripts are ever implemented.

## Local installation and checks

Requirements: Python 3.10 or later; Git for source control. Optional scanners:

```sh
python -m pip install cfn-lint checkov
python scripts/preflight.py --environment dev --strict-scanners
python scripts/preflight.py --environment prod --strict-scanners
```

Without scanners, run `python scripts/preflight.py --environment dev` (and `prod`); it reports unavailable scanners as skipped. The workflow installs/runs scanner actions in GitHub-hosted CI. The repository has no web application or local web server. It contains only IaC templates, local scripts, tests and documentation; no endpoint or browser verification applies.

## Exact future prerequisites

Before designing an approved deploy implementation, owners must provide and review:

1. Separate approved AWS accounts or documented isolation boundaries for dev/prod; account IDs, region `us-east-1`, owner, contact and budget owner.
2. Approved identity and least-privilege IAM design. For CI, OIDC trust constrained to exact GitHub organization/repository/ref or protected environment; no static keys. This repository has no role ARN or OIDC trust policy.
3. Account quota/service availability review and CIDR overlap review with connected networks. Current templates require two usable AZs and non-overlapping VPC CIDRs (`10.20.0.0/16`, `10.30.0.0/16`).
4. An issued ACM certificate ARN in `us-east-1` matching the intended DNS name, plus approved DNS ownership/routing. DNS resources are not implemented.
5. An application source/build definition, tested health endpoint on port 8080 at `/health`, immutable ECR image digest, runtime architecture, resource sizing and database migration/recovery procedure. No application image/build exists here.
6. Reviewed parameter values, Aurora engine/version support and Serverless v2 availability, backup/PITR and deletion protection expectations, KMS/secret access, log/audit ownership, alert contacts and incident runbooks.
7. Dated AWS Pricing Calculator exports for dev and prod and written approval of monthly and variable-cost ceilings.
8. Approved predeploy, rollback, evidence retention and cleanup owners. Current `plan.py` is not a CloudFormation change set.

The environment JSON currently fixes region, CIDRs, task sizing, Aurora ACU and optional service flags. Validate any future change locally and review its security and cost impact. There are no generated dynamic references between stacks today: the informational plan shows output placeholders that an eventual orchestration layer must resolve and validate.

## Cost inputs and retention

Use 730 hours/month as the baseline, then price each environment separately. Include NAT hourly charges and processed bytes; public IPv4 and internet/inter-AZ transfer; ALB hours and LCU; Fargate vCPU/memory hours and architecture; Aurora minimum/peak ACU for writer and reader, storage, I/O and backup; KMS keys/requests; Secrets Manager secrets/API calls; CloudWatch ingestion, storage, queries and alarms; ECR storage/transfer; and optional account-level audit services. WAF, CloudFront and interface endpoints are disabled and excluded. Add workload-specific traffic and growth scenarios. No current quote is asserted by this repository.

Template retention defaults: application CloudWatch log group 30 days; Aurora automated backup retention 7 days; ECR lifecycle keeps 30 images; optional audit S3 bucket enables versioning and expires current objects after 2,555 days. Audit bucket uses AES-256 server-side encryption, not KMS. Noncurrent S3 versions do not currently have an expiration rule. Review legal hold, regulatory rules, backup copy and restore testing before production approval. Do not enable the optional audit stack until account ownership, global service behavior, bucket naming, KMS requirements and costs are reviewed.

## Predeploy checklist

- [ ] `python scripts/preflight.py --environment dev --strict-scanners` and prod pass in an approved review environment.
- [ ] CloudFormation template validation by an approved method is recorded separately; local checks do not prove AWS service/property compatibility.
- [ ] Account, region, AZ capacity, quotas, CIDR routes and environment isolation are approved.
- [ ] ACM/DNS, application image digest, `/health`, ports and database migration are ready.
- [ ] IAM/OIDC trust, permissions boundary, SCP interaction and CloudFormation execution permissions receive security review.
- [ ] Cost Calculator exports, variable traffic assumptions and budget alarms are approved.
- [ ] Backup/PITR, restore test, deletion protection, retention, evidence ownership and rollback are agreed.
- [ ] Proposed stack parameters, dependency/output mapping, change sets and security findings receive human approval.

## Postdeploy checklist (future; not performed)

- [ ] Record stack IDs, template digest, approved parameter set, image digest and change-set approval.
- [ ] Verify ALB TLS certificate/health, expected public exposure, private task addressing and security-group paths.
- [ ] Verify ECS steady state, runtime health, secret retrieval and database connectivity without exposing secret values.
- [ ] Verify Aurora encryption, backup policy and restore procedure; test alarms/log routing and retention.
- [ ] Verify cost/budget alerts, resource tags, audit controls and evidence collection permissions.
- [ ] Capture timestamped evidence in an approved protected location; redact account-sensitive values.
- [ ] Record drift, findings, owner and remediation; no evidence is pre-created by this repository.

## Controlled cleanup checklist (future; not performed)

- [ ] Confirm environment, exact stack names, owner approval and maintenance/traffic window.
- [ ] Export and preserve required audit evidence and database snapshots; verify restore and retention requirements.
- [ ] Stop/redirect traffic; remove app stack first, then data only after data-owner approval, then registry and network in dependency order.
- [ ] For prod, explicitly review Aurora deletion protection and final snapshot requirements; never bypass protection automatically.
- [ ] Review retained snapshots, ECR images, log groups, KMS keys, secrets, EIPs and audit objects for cost and retention obligations.
- [ ] Verify no resources remain using an approved future read-only procedure; record owner/date and evidence.

`python scripts/destroy.py` is not a cleanup procedure. It fails closed until a separately reviewed implementation and explicit authorization exist.
