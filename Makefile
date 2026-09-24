PYTHON ?= .venv/bin/python
MKDOCS ?= .venv/bin/mkdocs

.PHONY: validate sync-vault finalize
validate:
	$(PYTHON) -m unittest discover -s tests -v
	$(PYTHON) scripts/check_harness.py
	$(PYTHON) scripts/check_handbook.py
	npm run check:mermaid
	$(MKDOCS) build --strict
	$(PYTHON) scripts/check_prompts.py
	$(PYTHON) scripts/check_site.py

sync-vault:
	$(PYTHON) scripts/sync_vault.py
	$(PYTHON) scripts/sync_vault.py --check

finalize: validate
	$(MAKE) sync-vault
