#!/usr/bin/env python3
"""Safe local preflight. Never initializes or contacts AWS."""
import argparse
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--environment", choices=("dev", "prod"), default="dev")
    parser.add_argument("--strict-scanners", action="store_true", help="fail if cfn-lint or Checkov is unavailable")
    args = parser.parse_args()

    commands = [
        [sys.executable, "scripts/validate.py"],
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        [sys.executable, "scripts/plan.py", "--environment", args.environment],
    ]
    for command in commands:
        result = subprocess.run(command, cwd=ROOT)
        if result.returncode:
            return result.returncode

    missing = []
    for tool, command in (("cfn-lint", ["cfn-lint", "templates"]), ("Checkov", ["checkov", "-d", "templates", "--framework", "cloudformation"])):
        executable = shutil.which(command[0])
        if not executable:
            print(f"SKIPPED: {tool} is not installed locally.")
            missing.append(tool)
            continue
        result = subprocess.run(command, cwd=ROOT)
        if result.returncode:
            return result.returncode
    if missing and args.strict_scanners:
        print("Preflight incomplete: install missing scanners or rerun without --strict-scanners.")
        return 2
    print("LOCAL PREFLIGHT PASSED. No AWS commands, credentials, or network calls were used.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
