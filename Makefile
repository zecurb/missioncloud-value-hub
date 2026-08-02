SHELL := /usr/bin/env bash

.PHONY: help api-install web-install api-dev web-dev test lint typecheck format docker-up docker-down

help:
	@printf '%s\n' \
	  'make api-install   Install API dependencies with uv' \
	  'make web-install   Install web dependencies with npm' \
	  'make api-dev       Run FastAPI development server' \
	  'make web-dev       Run Next.js development server' \
	  'make test          Run API tests' \
	  'make lint          Run Python and web lint checks' \
	  'make typecheck     Run Python and TypeScript type checks' \
	  'make format        Format Python code' \
	  'make docker-up     Start local containers' \
	  'make docker-down   Stop local containers'

api-install:
	cd services/api && uv sync --all-groups

web-install:
	cd apps/web && npm install

api-dev:
	cd services/api && uv run fastapi dev src/missioncloud_value_hub/main.py --host 0.0.0.0 --port 8000

web-dev:
	cd apps/web && npm run dev

test:
	cd services/api && uv run pytest

lint:
	cd services/api && ruff check .
	cd apps/web && npm run lint

typecheck:
	cd services/api && uv run mypy src
	cd apps/web && npm run typecheck

format:
	cd services/api && ruff format .

docker-up:
	docker compose up --build

docker-down:
	docker compose down
