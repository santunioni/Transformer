FROM python:3.9-slim AS build-image
RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc git

# Manipulate authentification with git
ARG GIT_USERNAME
ARG GIT_ACCESS_TOKEN
RUN git config --global url."http://${GIT_USERNAME}:${GIT_ACCESS_TOKEN}@gitlab.".insteadOf "ssh://git@gitlab."

# Activating VENV
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Export requirements.txt from poetry
RUN pip install poetry
COPY poetry.lock pyproject.toml ./
RUN poetry export --without-hashes > requirements.txt
# Install all
RUN pip install --upgrade pip && pip install --upgrade setuptools
RUN pip install -r requirements.txt


FROM python:3.9-slim
# Copy VENV and use it!
ENV VIRTUAL_ENV=/opt/venv
COPY --from=build-image $VIRTUAL_ENV $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
# Copy app
WORKDIR /app
COPY src/ ./src
# Run it!
CMD ["python", "-m", "src.main"]
