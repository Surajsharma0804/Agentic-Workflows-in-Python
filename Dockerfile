# Multi-stage build for production-ready backend

# Stage 1: Build frontend
FROM node:18-slim AS frontend-builder
WORKDIR /frontend
COPY ui/package*.json ./
RUN npm ci
COPY ui/ ./
RUN npm run build

# Stage 2: Python dependencies
FROM python:3.11-slim AS python-builder
WORKDIR /build

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements-full.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --user -r requirements-full.txt

# Stage 3: Final production image
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
    useradd -r -g agentic --uid=1000 --home-dir=/app agentic

# Copy Python dependencies from builder
COPY --from=python-builder /root/.local /home/agentic/.local

# Copy frontend build
COPY --from=frontend-builder --chown=agentic:agentic /frontend/dist ./ui/dist

# Copy application code
COPY --chown=agentic:agentic . .

# Set environment variables
ENV PATH=/home/agentic/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=10000

# Switch to non-root user
USER agentic

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:${PORT}/api/health || exit 1

# Expose port
EXPOSE ${PORT}

# Run application
CMD ["sh", "-c", "uvicorn agentic_workflows.api.server:app --host 0.0.0.0 --port ${PORT}"]
