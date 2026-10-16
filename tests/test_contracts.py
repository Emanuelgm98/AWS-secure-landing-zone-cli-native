import sys
import unittest
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate import validate
from phase_check import PHASE_FILES
from plan import build_plan


class ContractTests(unittest.TestCase):
    def test_repository_contracts_are_valid(self):
        self.assertEqual(validate(), [])

    def test_environment_nat_and_optional_defaults(self):
        dev = json.loads((ROOT / "config/environments/dev.json").read_text())
        prod = json.loads((ROOT / "config/environments/prod.json").read_text())
        self.assertEqual(dev["NatGatewayCount"], 1)
        self.assertEqual(prod["NatGatewayCount"], prod["AvailabilityZoneCount"])
        for config in (dev, prod):
            self.assertFalse(config["EnableCloudFront"])
            self.assertFalse(config["EnableWaf"])
            self.assertFalse(config["EnableInterfaceEndpoints"])

    def test_database_minimum_and_encryption(self):
        template = json.loads((ROOT / "templates/data.json").read_text())
        cluster = template["Resources"]["Cluster"]["Properties"]
        self.assertTrue(cluster["StorageEncrypted"])
        self.assertEqual(template["Parameters"]["MinACU"]["Default"], 0.5)

    def test_application_has_https_and_private_tasks(self):
        template = json.loads((ROOT / "templates/app.json").read_text())
        listener = template["Resources"]["HttpsListener"]["Properties"]
        self.assertEqual(listener["Protocol"], "HTTPS")
        net = template["Resources"]["Service"]["Properties"]["NetworkConfiguration"]["AwsvpcConfiguration"]
        self.assertEqual(net["AssignPublicIp"], "DISABLED")

    def test_each_phase_has_local_evidence_inputs(self):
        self.assertEqual(set(PHASE_FILES), set(range(1, 9)))
        for phase, files in PHASE_FILES.items():
            with self.subTest(phase=phase):
                self.assertTrue(all((ROOT / item).is_file() for item in files))

    def test_local_plan_is_non_mutating_and_orders_dependencies(self):
        plan = build_plan("dev")
        self.assertFalse(plan["aws_calls"])
        self.assertEqual(plan["mode"], "LOCAL_PLAN_ONLY")
        self.assertEqual(
            [stack["name"] for stack in plan["stacks"]],
            ["slz-dev-network", "slz-dev-registry", "slz-dev-data", "slz-dev-app"],
        )
        self.assertFalse(plan["optional_audit_stack_enabled"])

    def test_audit_stack_is_opt_in(self):
        for env in ("dev", "prod"):
            plan = build_plan(env)
            self.assertNotIn(f"slz-{env}-audit", [stack["name"] for stack in plan["stacks"]])

    def test_scripts_contain_no_aws_mutation_commands(self):
        forbidden = (
            "cloudformation deploy",
            "cloudformation create-stack",
            "cloudformation update-stack",
            "cloudformation delete-stack",
            "cloudformation create-change-set",
            "cloudformation execute-change-set",
        )
        script_dir = ROOT / "scripts"
        for path in script_dir.rglob("*"):
            if path.suffix.lower() not in (".py", ".ps1"):
                continue
            content = path.read_text(encoding="utf-8").lower()
            for term in forbidden:
                with self.subTest(file=path.name, term=term):
                    self.assertNotIn(term, content)


if __name__ == "__main__":
    unittest.main()
