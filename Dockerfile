# Use official Python runtime as base image
FROM python:3.12.3-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLET_SERVER_IP="0.0.0.0"
ENV FLET_SERVER_PORT=8553

# Install system dependencies including libmpv for audio
RUN apt-get update && apt-get install -y \
    curl \
    libmpv2 \
    gcc \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire src directory (which includes assets)
COPY src/ ./src/

WORKDIR /app/src

EXPOSE 8553

# For FastAPI, use uvicorn directly
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8553"]