FROM python:3.9 as builder
RUN pip install poetry
COPY poetry.lock pyproject.toml ./
RUN poetry export > requirements.txt

FROM python:3.9-alpine
RUN pip install --upgrade pip
RUN apk update && apk add --no-cache musl-dev python3-dev libffi-dev gcc g++
WORKDIR app/
COPY --from=builder requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
ENTRYPOINT ["python", "-m", "src.main"]