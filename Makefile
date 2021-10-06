.PHONY: tests


formaters:
	poetry run autoflake .
	poetry run isort --atomic .
	poetry run black .

linters:
	poetry run flake8 --max-line-length 120

checkers:
	poetry run mypy transformer tests

tests:
	poetry run pytest --cov transformer tests

quality: formaters linters checkers tests
