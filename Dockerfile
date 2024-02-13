FROM python:3.12.2-alpine AS builder
LABEL stage=builder

ENV PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.6.0

WORKDIR /app
COPY poetry.lock pyproject.toml ./

RUN python -m pip install --no-cache-dir poetry==$POETRY_VERSION \
    && poetry config virtualenvs.in-project true \
    && poetry install --without dev --no-interaction --no-ansi


FROM python:3.12.2-alpine

WORKDIR /app

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1

COPY --from=builder /app .
COPY . ./

RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    app
USER app

ENTRYPOINT ["/bin/sh", "docker-entrypoint.sh"]