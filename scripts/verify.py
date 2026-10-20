#!/usr/bin/env python3
"""Future post-deployment verification entry point; no AWS API calls."""
import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--environment", required=True, choices=("dev", "prod"))
    parser.add_argument("--execute", action="store_true", help="reserved for a separately reviewed future implementation")
    parser.parse_args()
    print("BLOCKED: verify is not implemented. No AWS command was run. Use reviewed evidence procedures only after a future approved deployment.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
