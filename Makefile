.PHONY: tests
include local.env
include .env
export

container_name=json-transformer

lint:
	@echo "/ -------------------------- pylint analysis starts -----------------------------"
	@poetry run pylint --rcfile=pylintrc.cfg --jobs 4 src
	@echo "-------------------------- pylint analysis ends ----------------------------- /"
	@echo ""

mypy:
	@echo "/ -------------------------- mypy analysis starts -----------------------------"
	@echo "Starting mypy analysis in src/ and tests/ folders."
	@poetry run mypy src
	@echo "-------------------------- mypy analysis ends ----------------------------- /"
	@echo ""

tests:
	@poetry run pytest --cov src --cov-report term-missing --cov-report html tests

quality: lint mypy tests

run:
	@rm profile.prof || true
	@poetry run python -m cProfile -o profile.prof -s time -m src.main


GIT_USER=santunioni
GIT_TOKEN=smiGDp_fhPz2Mck-zZ_u
docker-run:
	@docker rm -f $(container_name) || true
	@docker build --build-arg GIT_USER=$(GIT_USER) --build-arg GIT_TOKEN=$(GIT_TOKEN) -t decode/$(container_name):latest .
	@docker run -it --env-file=local.env --network host --name $(container_name) decode/$(container_name):latest

measure:
	@poetry run python -m tests.measure

view-profile:
	@poetry run snakeviz profile.prof -b firefox

infra-up:
	@docker-compose up --build
