FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /srv
ENV UV_COMPILE_BYTECODE=1 PYTHONUNBUFFERED=1
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY app app
ENV PATH="/srv/.venv/bin:$PATH"

CMD ["uv", "run", "fastapi", "run", "app/main.py", "--port", "8000", "--host", "0.0.0.0"]