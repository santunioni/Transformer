.PHONY: tests


formatters:
	poetry run autoflake .
	poetry run isort --atomic .
	poetry run black .

linters:
	poetry run flake8 --max-line-length 120

mypy:
	poetry run mypy transformer tests

tests:
	poetry run pytest --cov transformer tests

quality: formatters linters mypy tests
