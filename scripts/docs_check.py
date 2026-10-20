#!/usr/bin/env python3
"""Local documentation presence/link smoke check; no network access."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ["README.md", "docs/architecture/overview.md", "docs/architecture/decisions.md", "docs/security/threat-model.md", "docs/security/iam-model.md", "docs/security/oidc-trust.md", "docs/deployment/prerequisites.md", "docs/deployment/manual-deployment.md", "docs/operations/recovery-destroy.md", "docs/troubleshooting.md", "docs/evidence/README.md", "docs/cost-estimate.md"]
missing = [item for item in REQUIRED if not (ROOT / item).is_file()]
if missing:
    raise SystemExit("Missing required docs: " + ", ".join(missing))
print(f"Documentation presence check passed ({len(REQUIRED)} files).")
