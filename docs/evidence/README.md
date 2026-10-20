# Validation evidence

This folder records local static validation only. No AWS credentials, network access, Terraform initialization, AWS API calls, deployment, or cost measurement are involved. `local-validation.md` belongs to the preserved CloudFormation reference track and should not be interpreted as Terraform validation. Record future evidence with command, tool version, timestamp, repository revision and redaction notes only after an approved run; never store credentials, state files or sensitive plan output here.

For this change, `python scripts/validate.py`, `python scripts/docs_check.py`, and `python -m unittest discover -s tests -v` completed locally; the suite reported 9 passing tests. Terraform CLI was unavailable, so Terraform formatting and provider-backed validation remain unverified. The workflow files and source were inspected statically only.
