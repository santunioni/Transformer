# This strategy for building the docker image will speed up compile-time by a lot, because
# the the-flash library requires several libraries to be installed with it. Therefore, the_flash
# has it's own container for building it, allowing using docker cache more efficiently when changing
# some other libraries.

FROM python:3.9 AS exporter
RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc
RUN pip install --upgrade pip && pip install --upgrade setuptools && pip install poetry
COPY poetry.lock pyproject.toml ./
RUN poetry export --without-hashes | grep flash > the_flash-req.txt
RUN poetry export --without-hashes | grep -v flash > not-the_flash-req.txt


FROM python:3.9 as build-image
# Install tools
RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc
RUN pip install --upgrade pip && pip install --upgrade setuptools && pip install poetry
# Manipulate authentification with git
ARG GIT_USERNAME
ARG GIT_ACCESS_TOKEN
RUN git config --global url."http://${GIT_USERNAME}:${GIT_ACCESS_TOKEN}@gitlab.".insteadOf "ssh://git@gitlab."
# Activating VENV
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install --upgrade pip && pip install --upgrade setuptools
# Install TheFlash deps in VENV
COPY --from=exporter the_flash-req.txt ./requirements.txt
RUN pip install -r requirements.txt
# Install other deps
COPY --from=exporter not-the_flash-req.txt ./requirements.txt
RUN pip install -r requirements.txt


# Use fresh image to run the app
FROM python:3.9-slim
# Copy VENV and assign it to PATH
ENV VIRTUAL_ENV=/opt/venv
COPY --from=build-image $VIRTUAL_ENV $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
# Copy app
WORKDIR /app
COPY src/ ./src
# Run it!
CMD ["python", "-m", "src.main"]
