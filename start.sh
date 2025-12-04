#!/bin/sh
set -e

# Use PORT environment variable from Render (default 10000)
PORT="${PORT:-10000}"

echo "========================================="
echo "Agentic Workflows - FREE DEPLOYMENT"
echo "Port: $PORT"
echo "Host: 0.0.0.0"
echo "Environment: ${ENVIRONMENT:-production}"
echo "========================================="

# Wait for database
echo "Waiting for database to be ready..."
sleep 15

# Initialize database tables
echo "Initializing database..."
python -c "from agentic_workflows.db.database import init_db; init_db()" || echo "Database init skipped (may already exist)"

# Start FastAPI server
echo "Starting FastAPI server on 0.0.0.0:$PORT..."
exec uvicorn agentic_workflows.api.server:app \
    --host 0.0.0.0 \
    --port "$PORT" \
    --workers 1 \
    --log-level info \
    --no-access-log
