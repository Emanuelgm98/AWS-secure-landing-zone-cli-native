# Phase 1 — repository foundation

- **Script:** `python scripts/phase_check.py 1` plus `python scripts/validate.py` (local contracts only).
- **Prueba:** `python -m unittest discover -s tests -v`.
- **ADR:** use JSON for environment inputs and CloudFormation templates so Python's standard library can parse them without third-party packages.
- **Verificación:** `python scripts/phase_check.py 1`.
- **Checklist de evidencia:** [ ] clean diff reviewed; [ ] configs parse; [ ] repository is local-only; [ ] no AWS request issued.
