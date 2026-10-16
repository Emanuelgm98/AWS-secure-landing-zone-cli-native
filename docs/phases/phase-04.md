# Phase 4 — network foundation

- **Script:** `python scripts/phase_check.py 4`; `python scripts/validate.py` parses `templates/network.json`; neither provisions resources.
- **Prueba:** `python -m unittest discover -s tests -v`.
- **ADR:** CloudFormation manages VPC/subnet/route dependencies; dev has one NAT for lower cost, prod one NAT per AZ.
- **Verificación:** local `python scripts/phase_check.py 4`. Future read-only API validation example: `aws cloudformation validate-template --template-body file://templates/network.json --region us-east-1` (not run).
- **Checklist de evidencia:** [ ] CIDR overlap checked against enterprise network; [ ] actual AZ choice approved; [ ] NAT cost accepted; [ ] template reviewed in AWS CloudFormation Guard/cfn-lint before any deployment.
