#!/usr/bin/env python3
"""Local evidence gate for one implementation phase; never calls AWS."""
import argparse
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PHASE_FILES = {
    1: ["README.md", "docs/PHASES.md", "tests/test_contracts.py"],
    2: ["config/environments/dev.json", "config/environments/prod.json", "scripts/validate.py"],
    3: ["iam/policies/audit-readonly.json", "iam/policies/deny-audit-tampering-scp.example.json"],
    4: ["templates/network.json"],
    5: ["templates/data.json", "templates/audit.json"],
    6: ["templates/registry.json", "templates/app.json", "scripts/plan.py"],
    7: ["docs/runbooks/read-only-evidence.md", "scripts/aws-readonly-validate.ps1"],
    8: ["docs/ARCHITECTURE.md", "docs/phase-0-review.md", "docs/phases/phase-08.md", "scripts/run-local-checks.ps1"],
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", type=int, choices=sorted(PHASE_FILES))
    args = parser.parse_args()
    missing = [item for item in PHASE_FILES[args.phase] if not (ROOT / item).is_file()]
    if missing:
        print("PHASE EVIDENCE INCOMPLETE")
        print("\n".join(f"- missing: {item}" for item in missing))
        return 1
    print(f"PHASE {args.phase} LOCAL EVIDENCE PRESENT (no AWS calls made)")
    for item in PHASE_FILES[args.phase]:
        print(f"- {item}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
