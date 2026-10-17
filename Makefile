PYTHON ?= .venv/bin/python
MKDOCS ?= .venv/bin/mkdocs

.PHONY: validate slides sync-vault finalize
slides:
	npm run build:slides-renderer
	$(PYTHON) scripts/interactive_slides.py build --bundle _workspace/slides-renderer/renderer.js

validate:
	$(PYTHON) -m unittest discover -s tests -v
	$(PYTHON) scripts/check_harness.py
	$(PYTHON) scripts/check_handbook.py
	$(PYTHON) scripts/check_source_preservation.py
	$(PYTHON) scripts/english_study.py --check
	npm run check:mermaid
	$(MAKE) slides
	$(MKDOCS) build --strict
	$(PYTHON) scripts/interactive_slides.py publish
	$(PYTHON) scripts/check_prompts.py
	$(PYTHON) scripts/check_site.py
	npm run test:slides-browser

sync-vault:
	$(PYTHON) scripts/sync_vault.py
	$(PYTHON) scripts/sync_vault.py --check

finalize: validate
	$(MAKE) sync-vault
