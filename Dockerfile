FROM python:3.9 as builder
RUN pip install poetry
COPY poetry.lock pyproject.toml ./
RUN poetry export --without-hashes > requirements.txt



FROM python:3.9
# Installing build dependencies
# RUN apk update && apk add --no-cache musl-dev python3-dev libffi-dev gcc g++ build-base git
RUN apt update && apt install --no-cache musl-dev python3-dev libffi-dev gcc g++ build-essentials git


# Setting up python virtual env for user
RUN adduser -S the_flash
USER the_flash
RUN mkdir -p /home/the_flash/app/venv
WORKDIR /home/the_flash/app
RUN python -m venv venv && venv/bin/pip install --upgrade pip && venv/bin/pip install --upgrade setuptools

# Installing dependencies from GitLab
ARG GIT_USERNAME
ARG GIT_ACCESS_TOKEN
RUN git config --global url."http://${GIT_USERNAME}:${GIT_ACCESS_TOKEN}@gitlab.".insteadOf "ssh://git@gitlab."
COPY --from=builder requirements.txt ./requirements.txt
RUN venv/bin/pip install --no-cache-dir -r requirements.txt

# Copying and running source code
COPY src ./src
ENTRYPOINT ["venv/bin/python", "-m", "src.main"]
