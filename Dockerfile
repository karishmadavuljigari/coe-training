# syntax=docker/dockerfile:1
#
# Dockerfile: the recipe that turns this repository into a container image.
# Read it from top to bottom. Each block has a comment that says what it does and why.
#
# Base images are pinned to verified tags and SHA-256 digests.

# ---------------------------------------------------------------- stage 1: build
# A "multi-stage" build keeps build tools out of the final image (CTR-01).
FROM python:3.13-slim@sha256:b3575dcf816cdacc5292df77a6e3e59b8941631078373a045efa2ac1e9c5c3b2 AS builder

# Copy the uv program from its official image instead of installing it with pip.
COPY --from=ghcr.io/astral-sh/uv:0.10.3@sha256:7a88d4c4e6f44200575000638453a5a381db0ae31ad5c3a51b14f8687c9d93a3 /uv /bin/uv

WORKDIR /build

# Copy only the dependency files first. Docker caches this step, so a code change does not
# re-install every package. uv.lock must exist: run `uv lock` once and commit it (README, Quick start).
COPY pyproject.toml uv.lock ./

# --locked: use exactly the versions in uv.lock. --no-dev: leave out test tools.
# --no-install-project: install libraries only; the app code is copied in the next stage.
RUN uv sync --locked --no-dev --no-install-project

# ---------------------------------------------------------------- stage 2: run
FROM python:3.13-slim@sha256:b3575dcf816cdacc5292df77a6e3e59b8941631078373a045efa2ac1e9c5c3b2 AS runtime

# Run as a normal user with a fixed ID, never as root (CTR-02).
RUN useradd --create-home --uid 1000 --shell /bin/sh appuser

WORKDIR /app

# Bring the installed libraries from stage 1.
COPY --from=builder /build/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Copy the application code and give it to the normal user.
COPY --chown=appuser:appuser app/ ./app/

USER appuser
EXPOSE 8000

# The container reports its own health. Slim images have no curl, so we use a tiny Python call.
# It asks /health/ready, which also checks dependencies (CTR-06).
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request, sys; r = urllib.request.urlopen('http://localhost:8000/health/ready', timeout=8); sys.exit(0 if r.status == 200 else 1)"

# `exec` makes uvicorn the main process, so it receives the stop signal (SIGTERM) and can
# finish current requests before exiting (CTR-07, ARC-08).
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --proxy-headers --forwarded-allow-ips=\"${FORWARDED_ALLOW_IPS:-127.0.0.1}\" --no-access-log"]
