# Phase 6 — application runtime

- **Script:** `python scripts/plan.py --environment dev` renders a local, non-mutating stack order; `python scripts/phase_check.py 6` checks the artifacts.
- **Prueba:** `python -m unittest discover -s tests -v`.
- **ADR:** ECR is a separate bootstrap stack so an image can be pushed before the ECS service is created. ECS Fargate was chosen over EKS because workload scale and Kubernetes requirements are unknown; immutable image tags, private tasks and TLS-only ALB ingress are defaults.
- **Verificación:** `python scripts/plan.py --environment prod`; optional future read-only service checks in `docs/runbooks/read-only-evidence.md`.
- **Checklist de evidencia:** [ ] image URI pinned to digest; [ ] ACM certificate/domain approved; [ ] health endpoint exists; [ ] task permissions reviewed; [ ] app egress constrained after dependency inventory.
