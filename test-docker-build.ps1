#!/usr/bin/env pwsh
# Test Docker build locally

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  Testing Docker Build" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# Build the image
Write-Host "`n[1/3] Building Docker image..." -ForegroundColor Yellow
docker build -t agentic-workflows-test .

if ($LASTEXITCODE -ne 0) {
    Write-Host "[FAIL] Docker build failed!" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Docker build successful!" -ForegroundColor Green

# Test with environment variables
Write-Host "`n[2/3] Testing container startup..." -ForegroundColor Yellow
$containerId = docker run -d `
    -e PORT=8080 `
    -e ENVIRONMENT=test `
    -e DATABASE_URL="sqlite:///./test.db" `
    -e SECRET_KEY="test-secret-key-12345" `
    -p 8080:8080 `
    agentic-workflows-test

if ($LASTEXITCODE -ne 0) {
    Write-Host "[FAIL] Container failed to start!" -ForegroundColor Red
    exit 1
}

Write-Host "[OK] Container started: $containerId" -ForegroundColor Green

# Wait for startup
Write-Host "`n[3/3] Waiting for application to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check logs
Write-Host "`nContainer logs:" -ForegroundColor Cyan
docker logs $containerId

# Test health endpoint
Write-Host "`nTesting health endpoint..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8080/api/health" -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "[OK] Health check passed!" -ForegroundColor Green
        Write-Host "Response: $($response.Content)" -ForegroundColor Gray
    } else {
        Write-Host "[FAIL] Health check returned status $($response.StatusCode)" -ForegroundColor Red
    }
} catch {
    Write-Host "[FAIL] Health check failed: $_" -ForegroundColor Red
}

# Cleanup
Write-Host "`nCleaning up..." -ForegroundColor Yellow
docker stop $containerId
docker rm $containerId

Write-Host "`n=========================================" -ForegroundColor Cyan
Write-Host "  Test Complete" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
