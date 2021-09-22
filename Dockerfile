FROM python:3.9 as builder
RUN pip install poetry
COPY poetry.lock pyproject.toml ./
RUN poetry export --without-hashes > requirements.txt



FROM python:3.9-alpine

RUN pip install --upgrade pip
RUN apk update && apk add --no-cache musl-dev python3-dev libffi-dev gcc g++ build-base git

ARG GIT_USERNAME
ARG GIT_ACCESS_TOKEN
RUN git config --global url."http://${GIT_USERNAME}:${GIT_ACCESS_TOKEN}@gitlab.".insteadOf "ssh://git@gitlab."

WORKDIR ~/app/
COPY --from=builder requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
ENTRYPOINT ["python", "-m", "src.main"]






# CONSIGO CLONAR O REPOSITORIO COM ESSA BUILD AQUI
#FROM ubuntu:20.04
#RUN apt-get update
#RUN apt-get install -y openssh-client pip git
#RUN pip install poetry
#
#RUN useradd -m user
#USER user
#RUN mkdir -p /home/user/.ssh && ln -s /run/secrets/id_rsa /home/user/.ssh/id_rsa && ln -s /run/secrets/id_rsa_pub /home/user/.ssh/id_rsa.pub
#RUN chown -R user:user /home/user/.ssh/*
#WORKDIR /home/user
#
#CMD ["bash"]