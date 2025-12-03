#!/bin/bash
# Quick Start Script for Agentic Workflows

set -e

echo "🚀 Agentic Workflows - Quick Start"
echo "=================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created. Please review and update if needed."
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p storage logs plugins

# Start services
echo "🐳 Starting Docker services..."
docker-compose up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service health
echo "🏥 Checking service health..."
docker-compose ps

echo ""
echo "✅ All services are running!"
echo ""
echo "📍 Access Points:"
echo "   - API Documentation: http://localhost:8000/api/docs"
echo "   - API Health Check: http://localhost:8000/api/health"
echo "   - Flower (Task Monitor): http://localhost:5555"
echo "   - Prometheus Metrics: http://localhost:9090/metrics"
echo ""
echo "🎯 Quick Commands:"
echo "   - View logs: docker-compose logs -f"
echo "   - Stop services: docker-compose down"
echo "   - Restart services: docker-compose restart"
echo "   - Run workflow: agentic-workflows run --spec .kiro/specs/lazy_file_butler.yaml"
echo ""
echo "📚 Documentation:"
echo "   - README.md - Getting started"
echo "   - ARCHITECTURE.md - System design"
echo "   - IMPLEMENTATION_ROADMAP.md - Development plan"
echo ""
echo "🎉 Happy automating!"
