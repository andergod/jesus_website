FROM python:3.11-slim

# Install system deps (Poetry sometimes needs build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Copy only dependency files first (better caching)
COPY pyproject.toml poetry.lock* ./

# Install dependencies without creating a virtualenv
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copy the rest of the application
COPY . .

EXPOSE 8050

CMD ["gunicorn", "app:server", "--workers", "4", "--bind", "0.0.0.0:8050"]