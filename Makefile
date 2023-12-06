generate_migration:
	poetry run alembic revision -m="$(NAME)" --autogenerate

migrate:
	poetry run alembic upgrade head