# Production Dockerfile for Agentic Workflows (FREE Tier Optimized)

# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements-full.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip==24.0 && \
    pip install --no-cache-dir -r requirements-full.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user
RUN groupadd -r agentic --gid=1000 && \
    useradd -r -g agentic --uid=1000 --home-dir=/app --shell=/bin/bash agentic && \
    chown -R agentic:agentic /app

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=agentic:agentic agentic_workflows/ ./agentic_workflows/
COPY --chown=agentic:agentic .kiro/ ./.kiro/
COPY --chown=agentic:agentic pyproject.toml ./
COPY --chown=agentic:agentic entrypoint.sh ./

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Install the package
RUN pip install --no-cache-dir -e .

# Switch to non-root user
USER agentic

# Set environment
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Expose port
EXPOSE 10000

# Start application
CMD ["/bin/sh", "/app/entrypoint.sh"]
