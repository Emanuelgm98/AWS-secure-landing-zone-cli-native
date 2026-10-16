#!/usr/bin/env python3
"""Render a local deployment sequence; this is not a CloudFormation change set."""
import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def build_plan(environment):
    path = ROOT / "config" / "environments" / f"{environment}.json"
    config = json.loads(path.read_text(encoding="utf-8"))
    stacks = [
        {
            "name": f"slz-{environment}-network",
            "template": "templates/network.json",
            "parameters": {"Environment": environment, "VpcCidr": config["VpcCidr"]},
            "requires": [],
        },
        {
            "name": f"slz-{environment}-registry",
            "template": "templates/registry.json",
            "parameters": {"Environment": environment},
            "requires": [],
        },
        {
            "name": f"slz-{environment}-data",
            "template": "templates/data.json",
            "parameters": {
                "Environment": environment,
                "MinACU": config["AuroraMinACU"],
                "MaxACU": config["AuroraMaxACU"],
                "ReaderCount": config["AuroraReaderCount"],
                "VpcId": "<network output: VpcId>",
                "DataSubnetIds": "<network output: DataSubnetIds>",
                "ApplicationSecurityGroupId": "<network output: ApplicationSecurityGroupId>",
            },
            "requires": [f"slz-{environment}-network"],
        },
        {
            "name": f"slz-{environment}-app",
            "template": "templates/app.json",
            "parameters": {
                "Environment": environment,
                "DesiredCount": config["TaskDesiredCount"],
                "TaskCpu": str(config["TaskCpu"]),
                "TaskMemory": str(config["TaskMemory"]),
                "VpcId": "<network output: VpcId>",
                "PublicSubnetIds": "<network output: PublicSubnetIds>",
                "AppSubnetIds": "<network output: AppSubnetIds>",
                "ApplicationSecurityGroupId": "<network output: ApplicationSecurityGroupId>",
                "DatabaseHost": "<data output: ClusterEndpoint>",
                "DatabaseSecretArn": "<data output: SecretArn>",
                "ImageUri": "<immutable ECR image URI, pushed before app stack>",
                "CertificateArn": "<approved ACM certificate ARN>",
            },
            "requires": [f"slz-{environment}-network", f"slz-{environment}-registry", f"slz-{environment}-data", "image build and push"],
        },
    ]
    if config.get("EnableAuditStack"):
        stacks.append({
            "name": f"slz-{environment}-audit",
            "template": "templates/audit.json",
            "parameters": {},
            "requires": [],
            "note": "Account-level services; review ownership, organization strategy, retention and cost before enabling.",
        })
    return {
        "mode": "LOCAL_PLAN_ONLY",
        "aws_calls": False,
        "environment": environment,
        "region": config["Region"],
        "monthly_hours_assumption": 730,
        "optional_audit_stack_enabled": config.get("EnableAuditStack", False),
        "notes": [
            "No CloudFormation change set is created by this plan.",
            "Stack outputs must be passed explicitly; this repository does not deploy stacks.",
            "Audit stack is omitted unless EnableAuditStack is explicitly true and separately reviewed.",
        ],
        "stacks": stacks,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--environment", required=True, choices=("dev", "prod"))
    parser.add_argument("--format", choices=("json", "text"), default="text")
    args = parser.parse_args(argv)
    plan = build_plan(args.environment)
    if args.format == "json":
        print(json.dumps(plan, indent=2))
    else:
        print(f"LOCAL PLAN ONLY | {plan['environment']} | {plan['region']} | AWS calls: no")
        for index, stack in enumerate(plan["stacks"], 1):
            print(f"{index}. {stack['name']} <- {stack['template']}")
            for requirement in stack["requires"]:
                print(f"   requires: {requirement}")
        for note in plan["notes"]:
            print(f"NOTE: {note}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
