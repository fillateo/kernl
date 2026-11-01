SHELL := /bin/bash
PIP := backend/.venv/bin/pip

.DEFAULT_GOAL := help

.PHONY: help install setup dev backend frontend migrate seed test test-backend test-frontend lint format build e2e e2e-install clean

help:
	@printf "\nKernl — local-first terminal courses\n\n"
	@printf "  make install      Install backend and frontend dependencies\n"
	@printf "  make setup        Install, migrate, and seed the catalog\n"
	@printf "  make dev          Run Django (8000) and Next.js (3000)\n"
	@printf "  make test         Run backend and frontend test suites\n"
	@printf "  make lint         Ruff, ESLint, and typecheck\n"
	@printf "  make format       Format Python and TypeScript\n"
	@printf "  make build        Build the production Next.js bundle\n"
	@printf "  make e2e-install  Install Chromium for Playwright\n"
	@printf "  make e2e          Run the Playwright browser tests\n"
	@printf "  make clean        Remove local databases, builds, and caches\n\n"

install:
	python3 -m venv backend/.venv
	$(PIP) install --upgrade pip
	$(PIP) install -r backend/requirements-dev.txt
	cd frontend && npm ci

setup: install migrate seed

dev:
	./scripts/dev.sh

backend:
	cd backend && .venv/bin/daphne -b 127.0.0.1 -p 8000 config.asgi:application

frontend:
	cd frontend && npm run dev

migrate:
	cd backend && .venv/bin/python manage.py migrate

seed:
	cd backend && .venv/bin/python manage.py seed_catalog --prune

test: test-backend test-frontend

test-backend:
	cd backend && .venv/bin/pytest --cov=apps --cov=config --cov-report=term-missing

test-frontend:
	cd frontend && npm test

lint:
	cd backend && .venv/bin/ruff check . && .venv/bin/ruff format --check .
	cd frontend && npm run lint && npm run typecheck && npm run format:check

format:
	cd backend && .venv/bin/ruff format . && .venv/bin/ruff check --fix .
	cd frontend && npm run format

build:
	cd frontend && npm run build

e2e-install:
	cd frontend && npx playwright install chromium

e2e:
	cd frontend && npm run e2e

clean:
	rm -rf backend/db.sqlite3 backend/var backend/.pytest_cache backend/.ruff_cache
	find backend/staticfiles -mindepth 1 ! -name .gitkeep -delete
	rm -rf frontend/.next frontend/test-results frontend/playwright-report frontend/coverage
	find backend/apps backend/config backend/tests -type d -name __pycache__ -prune -exec rm -rf {} +
