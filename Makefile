dev:
	uvicorn scriptorium.__main__:app --reload

test:
	pytest

format:
	black .

check: check_black check_ruff

db_migrate:
	echo "hello multiline";\
	alembic upgrade head

db_destroy:
	alembic downgrade base

db_generate_migration:
	alembic revision --autogenerate -m "$(name)"

check_ruff:
	ruff check .

check_black:
	black . --check

