# Smart Pi Interactive Projection — common targets
# Use: make install, make test, make lint, make run, etc.

PYTHON ?= python3
PIP ?= $(PYTHON) -m pip
VENV ?= .venv
BIN = $(VENV)/bin

.PHONY: install install-dev test lint format run calibrate healthcheck clean lock

install:
	$(PIP) install -r requirements.txt

install-dev:
	$(PIP) install -r requirements.txt -r requirements-dev.txt
	$(PIP) install -e .

test:
	$(PYTHON) -m pytest tests/ -v

lint:
	ruff check src tests
	ruff format --check src tests
	mypy src

format:
	ruff format src tests
	black src tests

run:
	$(PYTHON) -m smartpi.cli run

calibrate:
	$(PYTHON) -m smartpi.cli calibrate

healthcheck:
	$(PYTHON) -m smartpi.cli healthcheck
	@-./scripts/healthcheck.sh 2>/dev/null || true

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage

# Reproducible install: generate requirements-lock.txt from current env (optional)
lock:
	$(PIP) install -r requirements.txt -r requirements-dev.txt -e . && $(PIP) freeze | grep -v "^#" > requirements-lock.txt
	@echo "Wrote requirements-lock.txt. Use: pip install -r requirements-lock.txt for a reproducible env."
