# syntax=docker/dockerfile-upstream:master-labs

FROM python:3.12-alpine AS build
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
WORKDIR /app
RUN --mount=type=cache,target=/var/cache/apk \
    --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=src,target=src \
    uv sync --no-editable --locked

FROM python:3.12.0-alpine AS base
COPY --parents --from=build /app/.venv /
WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=0

FROM base AS production
ENV BIND=0.0.0.0
ENTRYPOINT ["wirecraft-server"]
