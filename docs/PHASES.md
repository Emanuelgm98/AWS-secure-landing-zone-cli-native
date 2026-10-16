# Delivery phases 0–8

| Phase | Outcome | Local script / verification |
|---|---|---|
| 0 | Scope, assumptions, architecture and cost model | `docs/phase-0-review.md`; `python scripts/validate.py` |
| 1 | Repository conventions and environment contracts | `scripts/validate.py`; `python -m unittest discover -s tests -v` |
| 2 | Parameter/config validation and cost inputs | `scripts/validate.py`; tests |
| 3 | IAM/SCP policy examples and lint contracts | `scripts/validate.py`; tests |
| 4 | VPC and NAT CloudFormation template | `scripts/validate.py`; AWS `cloudformation validate-template` is documented only, not run |
| 5 | Aurora, KMS and audit/security baseline templates | same |
| 6 | ECR registry bootstrap, then ECS/Fargate and ALB application template | `python scripts/plan.py --environment dev`; `python scripts/phase_check.py 6` |
| 7 | CLI operator runbooks and read-only evidence checks | `python scripts/phase_check.py 7`; optional `scripts/aws-readonly-validate.ps1 -Environment dev` |
| 8 | Release gate, evidence register and handoff | `python -m unittest discover -s tests -v` |

Every phase note under `docs/phases/` records its script, local proof, short ADR, verification command and evidence checklist. CloudFormation validation through the AWS API is read-only but was not invoked because this task was completed without AWS credentials or external AWS API calls. No deployment was performed.
