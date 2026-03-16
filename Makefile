PYTHON ?= python
MANAGE ?= $(PYTHON) examples/demo_project/manage.py

.PHONY: install install-dev lint format check-dist test migrate demo-migrate

install:
	$(PYTHON) -m pip install -e .

install-dev:
	$(PYTHON) -m pip install -e ".[dev,celery,temporal]"

lint:
	ruff check .

format:
	ruff format .

check-dist:
	$(PYTHON) -m build
	$(PYTHON) -m twine check dist/*

test:
	pytest

migrate:
	$(PYTHON) -m pytest tests/test_migrations.py

demo-migrate:
	$(MANAGE) migrate
