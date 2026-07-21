FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

RUN apt-get update  \
    && apt-get install -y --no-install-recommends postgresql-client  \
    && pip install --no-cache-dir uv  \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app


COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

COPY . .

EXPOSE 8000

RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]