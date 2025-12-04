#!/bin/bash
# Startup script for Render.com deployment - FULL FUNCTIONALITY

# Use PORT environment variable from Render, default to 8000
PORT=${PORT:-8000}

echo "========================================="
echo "Starting Agentic Workflows - FULL MODE"
echo "Port: $PORT"
echo "Environment: ${ENVIRONMENT:-production}"
echo "========================================="

# Wait for database to be ready
echo "Waiting for database..."
sleep 5

# Run database migrations
echo "Running database migrations..."
alembic upgrade head || echo "Migration skipped (may not be needed)"

# Start the full FastAPI server with all features
echo "Starting FastAPI server with all features..."
exec uvicorn agentic_workflows.api.server:app \
    --host 0.0.0.0 \
    --port $PORT \
    --workers 1 \
    --log-level info \
    --access-log
