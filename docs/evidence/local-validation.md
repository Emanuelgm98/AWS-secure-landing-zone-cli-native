# Local validation evidence register

## Scope

This file records only checks actually run during the current local preparation. It does not claim AWS, CloudFormation service, deployment, runtime, account, pricing, or scanner evidence. No AWS commands or credential inspection were performed.

## Verified in this preparation

- `python scripts/validate.py`: passed; local JSON/reference/dependency/S3 checks only.
- `python -m unittest discover -s tests -v`: 9 tests passed, including the negative public/unencrypted S3 regression.
- `python scripts/plan.py --environment dev` and `prod`: both printed `LOCAL PLAN ONLY`, with no AWS calls.
- `python scripts/preflight.py --environment dev` and `prod`: passed local checks and reported both scanners unavailable.
- `python scripts/deploy.py --environment dev`, `verify.py --environment dev`, and `destroy.py --environment dev`: each returned exit 2 with `BLOCKED`; no AWS command was run.
- `git diff --check`: passed (Git emitted only line-ending conversion warnings for the two README files).
- Workflow reviewed locally: CI has `contents: read`; no deploy job or OIDC token permission.
- Repository inspection found no web application or local web server, so browser/endpoint verification does not apply.

## Still pending

- cfn-lint and Checkov results, unless locally installed and actually run.
- AWS CloudFormation service schema/property validation. The local validator cannot prove service acceptance. In particular, the optional audit template defines an AWS Config recorder and delivery channel but no recorder start operation; verify and complete that lifecycle in a future approved design.
- The future stack orchestration must explicitly map network/data outputs and check conditional resource behavior. `plan.py` contains placeholders, not a resolved deployment graph.
- AWS quotas, IAM permissions, account isolation, OIDC trust and region/service availability.
- Pricing Calculator exports and approval for each environment.
- Application image/build, DNS/certificate, live health, backup restore, monitoring and runtime security verification.
- Any deploy, postdeploy verification, cleanup, AWS resource state or cloud evidence.

No fabricated evidence or deployment artifacts are stored here.
