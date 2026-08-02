FROM python:3.13-slim

WORKDIR /app
RUN pip install --no-cache-dir uv
COPY pyproject.toml README.md ./
COPY src ./src
RUN uv sync --no-dev

EXPOSE 8000
CMD ["uv", "run", "fastapi", "run", "src/missioncloud_value_hub/main.py", "--host", "0.0.0.0", "--port", "8000"]
