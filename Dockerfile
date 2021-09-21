FROM python:3.9 as builder
RUN pip install poetry
COPY poetry.lock pyproject.toml ./
RUN poetry export --without-hashes > requirements.txt

FROM python:3.9-alpine
RUN pip install --upgrade pip
RUN apk update && apk add --no-cache musl-dev python3-dev libffi-dev gcc g++ build-base git openssh
WORKDIR app/
COPY --from=builder requirements.txt ./requirements.txt
COPY .ssh/id_rsa .
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
ENTRYPOINT ["python", "-m", "src.main"]
