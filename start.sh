#!/bin/bash
# Startup script for Render.com deployment

# Use PORT environment variable from Render, default to 8000
PORT=${PORT:-8000}

echo "Starting server on port $PORT..."

# Run minimal server for testing
exec python minimal_server.py
