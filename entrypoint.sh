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
echo "DATABASE_URL: ${DATABASE_URL:0:30}..."
echo "============================================"

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."
max_attempts=30
attempt=0
until python -c "from agentic_workflows.db.database import engine; engine.connect()" 2>/dev/null; do
    attempt=$((attempt + 1))
    if [ $attempt -ge $max_attempts ]; then
        echo "ERROR: PostgreSQL not available after $max_attempts attempts"
        exit 1
    fi
    echo "PostgreSQL not ready yet (attempt $attempt/$max_attempts)..."
    sleep 2
done
echo "PostgreSQL is ready!"

# Initialize database
echo "Initializing database tables..."
python -c "
try:
    from agentic_workflows.db.database import init_db
    init_db()
    print('Database initialized successfully')
except Exception as e:
    print(f'Database init warning: {e}')
    print('Continuing anyway...')
"

# Start the application
echo "Starting uvicorn on 0.0.0.0:$PORT..."
exec uvicorn agentic_workflows.api.server:app \
    --host 0.0.0.0 \
    --port "$PORT" \
    --workers 1 \
    --log-level info \
    --timeout-keep-alive 120
