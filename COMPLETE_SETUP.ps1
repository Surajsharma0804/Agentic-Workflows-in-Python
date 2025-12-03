# Complete Setup Script - Run Everything

Write-Host "`n" -NoNewline
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   COMPLETE PROJECT SETUP" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$step = 1

# Step 1: Clean up documentation
Write-Host "[$step] Cleaning up documentation..." -ForegroundColor Yellow
$step++
if (Test-Path "cleanup-and-organize.ps1") {
    & .\cleanup-and-organize.ps1
} else {
    Write-Host "  Cleanup script not found, skipping..." -ForegroundColor Gray
}

# Step 2: Stop existing services
Write-Host "`n[$step] Stopping existing services..." -ForegroundColor Yellow
$step++
docker compose down 2>&1 | Out-Null

# Step 3: Remove old volumes
Write-Host "[$step] Removing old volumes..." -ForegroundColor Yellow
$step++
docker volume rm agentic-workflows_postgres_data -ErrorAction SilentlyContinue | Out-Null
docker volume rm agentic-workflows_redis_data -ErrorAction SilentlyContinue | Out-Null

# Step 4: Build images
Write-Host "[$step] Building Docker images..." -ForegroundColor Yellow
$step++
Write-Host "  This may take 2-3 minutes..." -ForegroundColor Gray
docker compose build --no-cache

# Step 5: Start services
Write-Host "`n[$step] Starting all services..." -ForegroundColor Yellow
$step++
docker compose up -d

# Step 6: Wait for services
Write-Host "[$step] Waiting for services to initialize..." -ForegroundColor Yellow
$step++
Write-Host "  Waiting 30 seconds..." -ForegroundColor Gray
Start-Sleep -Seconds 30

# Step 7: Check status
Write-Host "`n[$step] Checking service status..." -ForegroundColor Yellow
$step++
docker compose ps

# Step 8: Test API
Write-Host "`n[$step] Testing API health..." -ForegroundColor Yellow
$step++
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/health" -UseBasicParsing -ErrorAction Stop
    Write-Host "  [OK] API is healthy!" -ForegroundColor Green
} catch {
    Write-Host "  [WARN] API not responding yet, may need more time" -ForegroundColor Yellow
}

# Summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   SETUP COMPLETE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Services Status:" -ForegroundColor Yellow
docker compose ps

Write-Host "`nAccess Points:" -ForegroundColor Cyan
Write-Host "  API Documentation: http://localhost:8000/api/docs" -ForegroundColor White
Write-Host "  Health Check:      http://localhost:8000/api/health" -ForegroundColor White
Write-Host "  Flower Monitor:    http://localhost:5555" -ForegroundColor White
Write-Host "  UI Dashboard:      http://localhost:3000" -ForegroundColor White

Write-Host "`nUseful Commands:" -ForegroundColor Cyan
Write-Host "  View logs:    docker compose logs -f" -ForegroundColor White
Write-Host "  Stop all:     docker compose down" -ForegroundColor White
Write-Host "  Restart:      docker compose restart" -ForegroundColor White

Write-Host "`nDocumentation:" -ForegroundColor Cyan
Write-Host "  Quick Start:  QUICK_START.md" -ForegroundColor White
Write-Host "  Full Setup:   SETUP.md" -ForegroundColor White
Write-Host "  Deployment:   DEPLOYMENT_GUIDE.md" -ForegroundColor White
Write-Host "  Status:       PROJECT_STATUS.md" -ForegroundColor White

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "   YOUR PROJECT IS READY!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Open browser
Write-Host "Opening API documentation in browser..." -ForegroundColor Yellow
Start-Sleep -Seconds 2
Start-Process "http://localhost:8000/api/docs"

Write-Host "`nDone! Enjoy your agentic workflows platform! 🚀" -ForegroundColor Green
Write-Host ""
