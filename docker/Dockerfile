FROM python:3.10-slim-buster

ARG POETRY_HOME=/opt/poetry

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV POETRY_HOME=${POETRY_HOME}

ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apt-get update && apt-get upgrade -y \
  && apt-get install --no-install-recommends -y \
  curl \
  && curl -sSL https://install.python-poetry.org | python -

WORKDIR /home/project

COPY poetry.lock pyproject.toml ./

RUN poetry install

COPY . .
