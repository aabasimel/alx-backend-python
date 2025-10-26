FROM python:3.10-slim

# Create app directory
RUN mkdir -p /app
WORKDIR /app

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBUG=True \
    SECRET_KEY=django-insecure-ci-testing-key-change-in-production \
    DJANGO_ALLOWED_HOSTS="localhost 127.0.0.1 [::1]" \
    DATABASE_URL=postgresql://postgres:postgres@db:5432/messaging \
    CELERY_BROKER_URL=redis://redis:6379/0 \
    REDIS_URL=redis://redis:6379/0

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-tk \
    tk8.6 \
    git \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements first for caching
COPY requirements.txt /app/

# Copy .env file if it exists, otherwise create a default one
RUN touch /app/.env

# Create virtual environment and install dependencies
RUN python -m venv /venv \
    && /venv/bin/pip install --upgrade pip \
    && /venv/bin/pip install -r requirements.txt

# Copy rest of the app
COPY . /app/

# Make entrypoint executable
COPY entrypoint /app/entrypoint
RUN chmod +x /app/entrypoint

COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Use virtualenv in PATH
ENV PATH="/venv/bin:$PATH"


ENTRYPOINT [ "/app/entrypoint" ]
