# Open All Services - Quick Access Script

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "OPENING AGENTIC WORKFLOWS PLATFORM" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Check if services are running
Write-Host "Checking services..." -ForegroundColor Yellow
$apiStatus = docker ps --filter "name=agentic-api" --format "{{.Status}}"

if ($apiStatus -like "*Up*") {
    Write-Host "✅ Services are running!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Services not running. Starting..." -ForegroundColor Yellow
    docker-compose up -d
    Write-Host "Waiting for services to start..." -ForegroundColor Yellow
    Start-Sleep -Seconds 30
}

Write-Host ""
Write-Host "Opening all interfaces..." -ForegroundColor Yellow
Write-Host ""

# Open Web UI
Write-Host "🌐 Opening Web UI (http://localhost:3001)..." -ForegroundColor Cyan
Start-Process "http://localhost:3001"
Start-Sleep -Seconds 1

# Open API Docs
Write-Host "📚 Opening API Documentation (http://localhost:8000/api/docs)..." -ForegroundColor Cyan
Start-Process "http://localhost:8000/api/docs"
Start-Sleep -Seconds 1

# Open Flower
Write-Host "🌸 Opening Flower Monitoring (http://localhost:5555)..." -ForegroundColor Cyan
Start-Process "http://localhost:5555"

Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "ALL SERVICES OPENED!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Available Services:" -ForegroundColor White
Write-Host "  • Web UI:        http://localhost:3001" -ForegroundColor Gray
Write-Host "  • API:           http://localhost:8000" -ForegroundColor Gray
Write-Host "  • API Docs:      http://localhost:8000/api/docs" -ForegroundColor Gray
Write-Host "  • Flower:        http://localhost:5555" -ForegroundColor Gray
Write-Host ""
Write-Host "Test Credentials:" -ForegroundColor White
Write-Host "  • Email:    test@example.com" -ForegroundColor Gray
Write-Host "  • Password: SecurePass123!" -ForegroundColor Gray
Write-Host ""
Write-Host "Quick Commands:" -ForegroundColor White
Write-Host "  • Test Auth:     .\test-auth.ps1" -ForegroundColor Gray
Write-Host "  • Health Check:  .\health-check.ps1" -ForegroundColor Gray
Write-Host "  • View Logs:     docker logs agentic-api --tail 50" -ForegroundColor Gray
Write-Host "  • Stop All:      docker-compose down" -ForegroundColor Gray
Write-Host ""
Write-Host "📖 Documentation:" -ForegroundColor White
Write-Host "  • START_HERE.md" -ForegroundColor Gray
Write-Host "  • FINAL_STATUS.md" -ForegroundColor Gray
Write-Host "  • SUBMISSION.md" -ForegroundColor Gray
Write-Host ""
Write-Host "🎉 Ready to use!" -ForegroundColor Green
