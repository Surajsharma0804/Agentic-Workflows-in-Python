# Quick Start Script for Agentic Workflows (PowerShell)

Write-Host "Starting Agentic Workflows - Quick Start" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is installed
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "Docker is not installed. Please install Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Check if Docker Compose is available
if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    Write-Host "Docker Compose is not installed. Please install Docker Compose first." -ForegroundColor Red
    exit 1
}

# Create .env if it doesn't exist
if (-not (Test-Path .env)) {
    Write-Host "Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host ".env file created. Please review and update if needed." -ForegroundColor Green
}

# Create necessary directories
Write-Host "Creating directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path storage, logs, plugins | Out-Null

# Start services
Write-Host "Starting Docker services..." -ForegroundColor Yellow
docker-compose up -d

# Wait for services to be ready
Write-Host "Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check service health
Write-Host "Checking service health..." -ForegroundColor Yellow
docker-compose ps

Write-Host ""
Write-Host "All services are running!" -ForegroundColor Green
Write-Host ""
Write-Host "Access Points:" -ForegroundColor Cyan
Write-Host "   - API Documentation: http://localhost:8000/api/docs"
Write-Host "   - API Health Check: http://localhost:8000/api/health"
Write-Host "   - Flower (Task Monitor): http://localhost:5555"
Write-Host "   - Prometheus Metrics: http://localhost:9090/metrics"
Write-Host ""
Write-Host "Quick Commands:" -ForegroundColor Cyan
Write-Host "   - View logs: docker-compose logs -f"
Write-Host "   - Stop services: docker-compose down"
Write-Host "   - Restart services: docker-compose restart"
Write-Host "   - Run workflow: agentic-workflows run --spec .kiro/specs/lazy_file_butler.yaml"
Write-Host ""
Write-Host "Documentation:" -ForegroundColor Cyan
Write-Host "   - README.md - Getting started"
Write-Host "   - ARCHITECTURE.md - System design"
Write-Host "   - DEPLOYMENT_GUIDE.md - Deployment options"
Write-Host ""
Write-Host "Happy automating!" -ForegroundColor Green

# Open browser
Write-Host ""
Write-Host "Opening API documentation in browser..." -ForegroundColor Yellow
Start-Process "http://localhost:8000/api/docs"
