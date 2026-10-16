# Phase 2 — environment configuration

- **Script:** `python scripts/phase_check.py 2`; `python scripts/validate.py` checks `config/environments/{dev,prod}.json` against security/cost invariants.
- **Prueba:** `python -m unittest discover -s tests -v`.
- **ADR:** keep immutable environment-specific inputs in JSON; optional CloudFront, WAF and interface endpoints default off.
- **Verificación:** `python scripts/phase_check.py 2`.
- **Checklist de evidencia:** [ ] distinct CIDRs; [ ] region `us-east-1`; [ ] dev NAT=1/prod NAT=AZ count; [ ] Aurora min=0.5; [ ] optional services off.
