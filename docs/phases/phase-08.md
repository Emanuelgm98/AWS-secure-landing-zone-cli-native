# Phase 8 — final review and handoff

- **Script:** `python scripts/phase_check.py 8`, `python scripts/validate.py` and `python -m unittest discover -s tests -v`.
- **Prueba:** local contract suite; no AWS calls.
- **ADR:** release is a reviewed source artifact, not a deployed environment. A future deployment needs a separate explicit operational authorization.
- **Verificación:** clean Git status, inspect final diff, run all three local commands.
- **Checklist de evidencia:** [ ] architecture accepted; [ ] Calculator exports attached; [ ] policies reviewed; [ ] all optional resources accounted for; [ ] validation output saved; [ ] no deployment performed; [ ] handoff and limitations acknowledged.

- **Estado de autorización:** instrucción posterior del usuario autorizó fases 1–8; no autoriza despliegues en AWS.
