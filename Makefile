dev:
	uv run uvicorn scriptorium.__main__:app --reload

test:
	uv run pytest

format:
	uv run ruff format .

check: check_ruff

db-migrate:
	uv run alembic upgrade head

db-destroy:
	uv run alembic downgrade base

db-generate-migration:
	uv run alembic revision --autogenerate -m "$(name)"

check_ruff:
	uv run ruff check .
