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

# Start the application immediately
# Database initialization happens in FastAPI startup event
echo "Starting uvicorn on 0.0.0.0:$PORT..."
exec uvicorn agentic_workflows.api.server:app \
    --host 0.0.0.0 \
    --port "$PORT" \
    --workers 1 \
    --log-level info \
    --timeout-keep-alive 120
