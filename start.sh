#!/bin/bash
# Startup script for Render.com deployment

# Use PORT environment variable from Render, default to 8000
PORT=${PORT:-8000}

echo "Starting server on port $PORT..."

# Run uvicorn directly
exec uvicorn agentic_workflows.api.server:app \
    --host 0.0.0.0 \
    --port $PORT \
    --workers 1 \
    --log-level info
