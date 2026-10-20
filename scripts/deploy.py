#!/usr/bin/env python3
"""Future deployment entry point. Intentionally non-operational in this review."""
import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--environment", required=True, choices=("dev", "prod"))
    parser.add_argument("--execute", action="store_true", help="reserved for a separately reviewed future implementation")
    parser.parse_args()
    print("BLOCKED: deploy is not implemented. No AWS command was run. Complete the predeploy checklist and separately authorize a future deploy implementation.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
