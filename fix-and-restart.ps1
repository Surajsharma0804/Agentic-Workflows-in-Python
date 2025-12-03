# Fix and Restart Script

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   Fixing and Restarting Services" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Stop all services
Write-Host "Stopping all services..." -ForegroundColor Yellow
docker compose down

# Remove volumes to start fresh
Write-Host "Removing old volumes..." -ForegroundColor Yellow
docker volume rm agentic-workflows_postgres_data -ErrorAction SilentlyContinue
docker volume rm agentic-workflows_redis_data -ErrorAction SilentlyContinue

# Rebuild images
Write-Host "Rebuilding images..." -ForegroundColor Yellow
docker compose build --no-cache

# Start services
Write-Host "Starting services..." -ForegroundColor Green
docker compose up -d

# Wait for services
Write-Host "Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Check status
Write-Host "`nChecking service status..." -ForegroundColor Cyan
docker compose ps

# Check logs
Write-Host "`nRecent logs:" -ForegroundColor Cyan
docker compose logs --tail=20

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "   Services Restarted!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Green

Write-Host "Access points:" -ForegroundColor Cyan
Write-Host "  - API: http://localhost:8000/api/docs" -ForegroundColor White
Write-Host "  - Flower: http://localhost:5555" -ForegroundColor White
Write-Host "  - UI: http://localhost:3000" -ForegroundColor White
Write-Host ""
