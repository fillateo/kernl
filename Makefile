SHELL := /bin/bash
PIP := backend/.venv/bin/pip

.DEFAULT_GOAL := help

.PHONY: help install setup dev backend frontend migrate seed test test-backend test-frontend lint format build e2e e2e-install docker-build docker-up docker-down docker-reset docker-logs docker-check docker-e2e clean

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
	@printf "  make docker-up     Build and start the Docker Compose stack\n"
	@printf "  make docker-down   Stop the Docker Compose stack\n"
	@printf "  make docker-check  Verify the sandbox inside the API container\n"
	@printf "  make docker-e2e    Run Playwright against the Compose stack\n"
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

docker-build:
	docker compose build

docker-up:
	docker compose up --build -d --wait --wait-timeout 180
	docker compose ps

docker-down:
	docker compose down

docker-reset:
	docker compose down -v

docker-logs:
	docker compose logs -f --tail=100

docker-check:
	docker compose exec -T api python manage.py check_terminal

docker-e2e:
	docker compose up -d --wait --wait-timeout 180
	cd frontend && PLAYWRIGHT_BASE_URL=http://localhost:3000 E2E_HEALTH_URL=http://127.0.0.1:8000/api/health/ npm run e2e

clean:
	docker compose down -v --remove-orphans 2>/dev/null || true
	rm -rf backend/db.sqlite3 backend/var backend/.pytest_cache backend/.ruff_cache
	find backend/staticfiles -mindepth 1 ! -name .gitkeep -delete
	rm -rf frontend/.next frontend/test-results frontend/playwright-report frontend/coverage
	find backend/apps backend/config backend/tests -type d -name __pycache__ -prune -exec rm -rf {} +
