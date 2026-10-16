# Phase 7 — operations and evidence

- **Script:** `python scripts/phase_check.py 7`; optional `scripts/aws-readonly-validate.ps1 -Environment dev` calls only STS identity and CloudFormation ValidateTemplate read/validation APIs.
- **Prueba:** `python -m unittest discover -s tests -v`.
- **ADR:** evidence collection uses AWS describe/get/list operations only and excludes secrets and sensitive payloads.
- **Verificación:** `python scripts/phase_check.py 7`. AWS validation remains optional and read-only; it was not run in this task.
- **Checklist de evidencia:** [ ] account identity confirmed; [ ] region confirmed; [ ] evidence redacted; [ ] logs and retention monitored; [ ] spend alarms planned.
