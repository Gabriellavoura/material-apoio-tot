FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /srv
ENV UV_COMPILE_BYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/srv/.venv/bin:$PATH"

COPY pyproject.toml uv.lock* ./
RUN uv sync --no-dev --frozen

COPY app app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]