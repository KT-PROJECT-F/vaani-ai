.PHONY: up down api test lint format evals seed migrate web

up:
	docker compose up -d db redis

down:
	docker compose down

api:
	cd backend && uvicorn app.main:app --reload

test:
	cd backend && pytest

lint:
	cd backend && ruff check . && ruff format --check . && mypy app

format:
	cd backend && ruff format . && ruff check --fix .

evals:
	cd backend && python ../evals/run_evals.py

seed:
	cd backend && python ../scripts/seed_providers.py

migrate:
	cd backend && alembic upgrade head

web:
	cd frontend && npm run dev
