.PHONY: tests migrations
include local.env
include .env
export

container_name=field-translator

lint:
	@poetry run autopep8 --jobs 4 -r --aggressive --aggressive --in-place src tests
	@echo "/ -------------------------- pylint analysis starts -----------------------------"
	@poetry run pylint --rcfile=pylintrc.cfg --jobs 4 src
	@echo "-------------------------- pylint analysis ends ----------------------------- /"
	@echo ""

mypy:
	@echo "/ -------------------------- mypy analysis starts -----------------------------"
	@echo "Starting mypy analysis in src/ and tests/ folders."
	@poetry run mypy src tests
	@echo "-------------------------- mypy analysis ends ----------------------------- /"
	@echo ""

tests:
	@poetry run pytest --cov src --cov-report term-missing --cov-report html tests

quality: lint mypy tests

run:
	@rm profile.prof || true
	@poetry run python -m cProfile -o profile.prof -s time -m src.main

docker-run:
	@docker rm -f $(container_name) || true
	@docker build . -t decode/$(container_name):latest
	@docker run -it --env-file=local.env --network host --name $(container_name) decode/$(container_name):latest

measure:
	@poetry run python -m tests.measure

main:
	@poetry run python -m src.main

view-profile:
	@poetry run snakeviz profile.prof -b firefox

infra-up:
	@docker-compose up --build -d

infra-down:
	@docker-compose down --remove-orphans

infra-logs:
	@docker-compose logs -f

volume-prune:
	@docker volume prune -f

infra-refresh: infra-down volume-prune infra-up infra-logs
