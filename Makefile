.PHONY: fmt validate lint security test docs-check
fmt:
	terraform fmt -check -recursive terraform
validate:
	@echo "Static-only placeholder: terraform validate requires initialized providers; init is prohibited in this repository workflow."
lint:
	@python scripts/validate.py
security:
	@python -m unittest discover -s tests -p "test_negative_security.py" -v
test:
	@python -m unittest discover -s tests -v
docs-check:
	@python scripts/docs_check.py
