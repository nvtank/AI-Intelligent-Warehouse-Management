.PHONY: setup up down api web migrate lint test test-integration build types types-check check check-docker

PYTHON ?= python3.12
VENV_PYTHON := .venv/bin/python

setup:
	$(PYTHON) -m venv .venv
	$(VENV_PYTHON) -m pip install -c services/api/requirements.lock -r services/api/requirements-dev.txt
	npm ci

up:
	docker compose up --build -d --wait

down:
	docker compose down

api:
	@set -a; . ./.env; set +a; $(VENV_PYTHON) -m uvicorn app.main:app --app-dir services/api --reload --host 127.0.0.1 --port $${API_PORT:-8000}

web:
	npm run dev

migrate:
	@set -a; . ./.env; set +a; $(VENV_PYTHON) -m alembic -c services/api/alembic.ini upgrade head

lint:
	$(VENV_PYTHON) -m ruff check .
	$(VENV_PYTHON) -m ruff format --check .
	npm run lint

test:
	$(VENV_PYTHON) -m pytest -q
	npm test

test-integration:
	@set -a; . ./.env; set +a; $(VENV_PYTHON) -m pytest -q -m integration

build:
	npm run build

types:
	$(PYTHON) scripts/generate_web_types.py

types-check:
	$(PYTHON) scripts/generate_web_types.py --check

check: lint types-check test build

check-docker:
	docker compose --profile checks build api-checks
	docker compose --profile checks run --rm api-checks python -m ruff check .
	docker compose --profile checks run --rm api-checks python -m ruff format --check .
	docker compose --profile checks run --rm api-checks python scripts/generate_web_types.py --check
	docker compose --profile checks run --rm api-checks
	docker compose --profile checks run --rm api-checks python -m alembic -c services/api/alembic.ini upgrade head
	docker compose --profile checks run --rm api-checks python -m alembic -c services/api/alembic.ini check
	docker compose --profile checks run --rm api-checks python -m pytest -q -m integration -p no:cacheprovider
