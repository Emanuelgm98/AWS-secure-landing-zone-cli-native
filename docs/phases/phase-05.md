# Phase 5 — data, encryption and audit

- **Script:** `python scripts/phase_check.py 5`; `python scripts/validate.py` parses `templates/data.json`, `templates/audit.json`, and security policy documents.
- **Prueba:** `python -m unittest discover -s tests -v`.
- **ADR:** Aurora PostgreSQL Serverless v2 min 0.5 ACU; prod reader is explicit. Generate master credentials in Secrets Manager; protect DB storage with a rotating KMS key. Audit services are opt-in per approved account/region.
- **Verificación:** local `python scripts/phase_check.py 5`. Future read-only checks are listed in `docs/runbooks/read-only-evidence.md`.
- **Checklist de evidencia:** [ ] secret values absent from parameters/logs; [ ] backup/RPO/RTO reviewed; [ ] Config/CloudTrail retention and cost accepted; [ ] no account-level service enabled.
