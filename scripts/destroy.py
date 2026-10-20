#!/usr/bin/env python3
"""Future controlled cleanup entry point; never deletes resources in this implementation."""
import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--environment", required=True, choices=("dev", "prod"))
    parser.add_argument("--confirm-stack-prefix", help="reserved for explicit future stack-prefix confirmation")
    parser.add_argument("--execute", action="store_true", help="reserved for a separately reviewed future implementation")
    parser.parse_args()
    print("BLOCKED: destroy is not implemented. No AWS command was run. Preserve backups/evidence and complete the cleanup checklist before any separately approved future cleanup tooling.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
