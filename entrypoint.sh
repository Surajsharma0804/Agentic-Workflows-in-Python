#!/bin/sh
set -e

# Render.com sets PORT environment variable
PORT="${PORT:-10000}"

echo "============================================"
echo "  Agentic Workflows - Starting"
echo "============================================"
echo "PORT: $PORT"
echo "HOST: 0.0.0.0"
echo "ENVIRONMENT: ${ENVIRONMENT:-production}"
echo "============================================"

# Run database migrations
echo "Running database migrations..."
alembic upgrade head || echo "Warning: Migrations failed, continuing anyway..."

# Start the application
echo "Starting uvicorn on 0.0.0.0:$PORT..."
exec uvicorn agentic_workflows.api.server:app \
    --host 0.0.0.0 \
    --port "$PORT" \
    --workers 1 \
    --log-level info \
    --timeout-keep-alive 30 \
    --timeout-graceful-shutdown 10
