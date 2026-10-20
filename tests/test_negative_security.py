"""Reproducible negative security regression for the local IaC validator."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class NegativeSecurityTests(unittest.TestCase):
    def test_public_unencrypted_bucket_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            copy = Path(temp) / "repo"
            shutil.copytree(ROOT / "templates", copy / "templates")
            shutil.copytree(ROOT / "config", copy / "config")
            shutil.copytree(ROOT / "iam", copy / "iam")
            shutil.copytree(ROOT / "docs" / "phases", copy / "docs" / "phases")
            template_path = copy / "templates" / "insecure.json"
            template_path.write_text(json.dumps({
                "AWSTemplateFormatVersion": "2010-09-09",
                "Resources": {"PublicBucket": {"Type": "AWS::S3::Bucket", "Properties": {
                    "PublicAccessBlockConfiguration": {"BlockPublicAcls": False, "BlockPublicPolicy": False}
                }}}
            }), encoding="utf-8")
            import sys
            sys.path.insert(0, str(ROOT / "scripts"))
            from validate import validate
            original_root = __import__("validate").ROOT
            try:
                __import__("validate").ROOT = copy
                errors = validate()
            finally:
                __import__("validate").ROOT = original_root
            self.assertTrue(any("S3 public access must be blocked" in error for error in errors), errors)
            self.assertTrue(any("S3 default encryption is required" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
