# syntax=docker/dockerfile:1

FROM python:3.13-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# bubblewrap powers the per-session terminal. git/curl make the lessons and
# healthcheck work without mounting anything from the host.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        bash \
        bubblewrap \
        ca-certificates \
        curl \
        git \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --gid 10001 kernl \
    && useradd --uid 10001 --gid kernl --create-home --shell /bin/bash kernl

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Build-time static collection is intentional: the runtime container is
# read-only and must never mutate its own image.
RUN python manage.py collectstatic --noinput \
    && mkdir -p /app/data /app/var/terminal \
    && chown -R kernl:kernl /app

COPY docker/start-api.sh /usr/local/bin/start-api.sh
RUN chmod 0755 /usr/local/bin/start-api.sh

USER kernl
EXPOSE 8000

ENTRYPOINT ["/usr/local/bin/start-api.sh"]
