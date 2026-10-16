#!/usr/bin/env python3
"""Local-only contract validation. Does not call AWS or execute templates."""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_json(path):
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def validate():
    errors = []
    envs = {}
    for name in ("dev", "prod"):
        path = ROOT / "config" / "environments" / f"{name}.json"
        try:
            config = load_json(path)
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
            continue
        envs[name] = config
        if config.get("Environment") != name:
            errors.append(f"{name}: Environment must equal filename")
        if config.get("Region") != "us-east-1":
            errors.append(f"{name}: Region must be us-east-1 per approved baseline")
        if config.get("AvailabilityZoneCount") < 2:
            errors.append(f"{name}: at least two AZs required")
        if config.get("NatGatewayCount") != (1 if name == "dev" else config.get("AvailabilityZoneCount")):
            errors.append(f"{name}: NAT count must be 1 for dev and one per AZ for prod")
        if config.get("AuroraMinACU") != 0.5:
            errors.append(f"{name}: Aurora minimum ACU must be 0.5")
        if config.get("TaskDesiredCount", 0) < (1 if name == "dev" else 2):
            errors.append(f"{name}: task count is below environment minimum")
        for key in ("EnableCloudFront", "EnableWaf", "EnableInterfaceEndpoints"):
            if config.get(key) is not False:
                errors.append(f"{name}: optional {key} must remain explicitly disabled")
        if config.get("EnableAuditStack") is not False:
            errors.append(f"{name}: optional audit stack must remain disabled by default")

    if set(envs) == {"dev", "prod"} and envs["dev"].get("VpcCidr") == envs["prod"].get("VpcCidr"):
        errors.append("dev and prod VPC CIDRs must be distinct")

    for path in sorted((ROOT / "templates").glob("*.json")):
        try:
            template = load_json(path)
            if template.get("AWSTemplateFormatVersion") != "2010-09-09":
                errors.append(f"{path.relative_to(ROOT)}: missing CloudFormation format version")
            if not isinstance(template.get("Resources"), dict) or not template["Resources"]:
                errors.append(f"{path.relative_to(ROOT)}: Resources must be a non-empty object")
            else:
                resource_names = set(template["Resources"])
                parameter_names = set(template.get("Parameters", {}))
                condition_names = set(template.get("Conditions", {}))
                pseudo_parameters = {"AWS::AccountId", "AWS::NotificationARNs", "AWS::NoValue", "AWS::Partition", "AWS::Region", "AWS::StackId", "AWS::StackName", "AWS::URLSuffix"}
                for resource_name, resource in template["Resources"].items():
                    condition = resource.get("Condition")
                    if condition and condition not in condition_names:
                        errors.append(f"{path.name}:{resource_name}: unknown Condition {condition}")
                    dependencies = resource.get("DependsOn", [])
                    if isinstance(dependencies, str):
                        dependencies = [dependencies]
                    for dependency in dependencies:
                        if dependency not in resource_names:
                            errors.append(f"{path.name}:{resource_name}: unknown DependsOn {dependency}")

                def check_intrinsics(value, location="template"):
                    if isinstance(value, dict):
                        if "Ref" in value:
                            reference = value["Ref"]
                            if reference not in resource_names | parameter_names | pseudo_parameters:
                                errors.append(f"{path.name}:{location}: unknown Ref {reference}")
                        if "Fn::GetAtt" in value:
                            target = value["Fn::GetAtt"][0]
                            if target not in resource_names:
                                errors.append(f"{path.name}:{location}: unknown GetAtt target {target}")
                        for key, child in value.items():
                            check_intrinsics(child, f"{location}.{key}")
                    elif isinstance(value, list):
                        for index, child in enumerate(value):
                            check_intrinsics(child, f"{location}[{index}]")
                check_intrinsics(template)
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")

    expected_templates = {"network.json", "registry.json", "data.json", "app.json", "audit.json"}
    found_templates = {path.name for path in (ROOT / "templates").glob("*.json")}
    if found_templates != expected_templates:
        errors.append(f"templates: expected {sorted(expected_templates)}, found {sorted(found_templates)}")

    try:
        network = load_json(ROOT / "templates" / "network.json")["Resources"]
        if network["NatB"].get("Condition") != "IsProd":
            errors.append("network: second NAT must be conditional on prod")
        if "AWS::EC2::Subnet" not in {r.get("Type") for r in network.values()}:
            errors.append("network: subnets are required")
        data = load_json(ROOT / "templates" / "data.json")["Resources"]
        cluster = data["Cluster"]["Properties"]
        if cluster.get("StorageEncrypted") is not True or "ServerlessV2ScalingConfiguration" not in cluster:
            errors.append("data: Aurora must use encryption and Serverless v2 scaling")
        app = load_json(ROOT / "templates" / "app.json")["Resources"]
        service = app["Service"]["Properties"]
        if service["NetworkConfiguration"]["AwsvpcConfiguration"].get("AssignPublicIp") != "DISABLED":
            errors.append("app: Fargate tasks must not receive public IPs")
        listeners = [r for r in app.values() if r.get("Type") == "AWS::ElasticLoadBalancingV2::Listener"]
        if not listeners or any(l["Properties"].get("Protocol") != "HTTPS" for l in listeners):
            errors.append("app: public listener must use HTTPS")
        network_template = load_json(ROOT / "templates" / "network.json")
        if "ApplicationSecurityGroupId" not in network_template.get("Outputs", {}):
            errors.append("network: application security group output is required for data/app stack wiring")
        if "ApplicationSecurityGroupId" not in load_json(ROOT / "templates" / "data.json").get("Parameters", {}):
            errors.append("data: application security group parameter is required")
        if "ApplicationSecurityGroupId" not in load_json(ROOT / "templates" / "app.json").get("Parameters", {}):
            errors.append("app: application security group parameter is required")
        if not any(r.get("Type") == "AWS::EC2::SecurityGroupIngress" for r in app.values()):
            errors.append("app: explicit ALB-to-task security group ingress is required")
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        errors.append(f"template invariant check failed: {exc}")

    for path in sorted((ROOT / "iam" / "policies").glob("*.json")):
        try:
            doc = load_json(path)
            if doc.get("Version") != "2012-10-17" or not doc.get("Statement"):
                errors.append(f"{path.relative_to(ROOT)}: invalid IAM policy document")
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")

    phase_notes = list((ROOT / "docs" / "phases").glob("phase-*.md"))
    if len(phase_notes) != 8:
        errors.append(f"expected 8 phase notes, found {len(phase_notes)}")
    for path in phase_notes:
        text = path.read_text(encoding="utf-8")
        for term in ("Script", "Prueba", "ADR", "Verificación", "Evidencia"):
            if term.lower() not in text.lower():
                errors.append(f"{path.relative_to(ROOT)}: missing {term} section")

    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        print("VALIDATION FAILED")
        print("\n".join(f"- {problem}" for problem in problems))
        sys.exit(1)
    print("VALIDATION PASSED (local-only; no AWS calls made)")
