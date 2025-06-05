FROM python:3.12-alpine
COPY --from=ghcr.io/astral-sh/uv:0.7.11 /uv /uvx /bin/

RUN apk add --no-cache \
    git \
    libpq-dev \
    build-base \

COPY . /app

WORKDIR /app
