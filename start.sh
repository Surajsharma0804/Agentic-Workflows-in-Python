#!/bin/bash
# Startup script for Render.com - FREE TIER (No Redis)

# Use PORT environment variable from Render
PORT=${PORT:-10000}

echo "========================================="
echo "Agentic Workflows - FREE DEPLOYMENT"
echo "Port: $PORT"
echo "Environment: ${ENVIRONMENT:-production}"
echo "========================================="

# Wait for database
echo "Waiting for database to be ready..."
sleep 10

# Initialize database tables
echo "Initializing database..."
python -c "from agentic_workflows.db.database import init_db; init_db()" || echo "Database init skipped"

# Start FastAPI server (no Redis/Celery)
echo "Starting FastAPI server..."
exec uvicorn agentic_workflows.api.server:app \
    --host 0.0.0.0 \
    --port $PORT \
    --workers 1 \
    --log-level info
