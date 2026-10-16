# Phase 3 — identity and guardrails

- **Script:** `python scripts/phase_check.py 3`; `python scripts/validate.py` validates IAM policy document structure.
- **Prueba:** `python -m unittest discover -s tests -v`.
- **ADR:** store a sample read-only inventory policy and an explicitly marked example SCP. SCP attachment is organization-wide and requires security/management-account approval.
- **Verificación:** `python scripts/phase_check.py 3`.
- **Checklist de evidencia:** [ ] policy JSON parses; [ ] SCP marked example only; [ ] role trust and least privilege reviewed for real CI identity; [ ] no policy attached.
