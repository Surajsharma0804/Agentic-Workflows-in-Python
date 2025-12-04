# Deployment Status Checker for Render.com
# Usage: .\check-deployment.ps1 YOUR-APP-NAME

param(
    [Parameter(Mandatory=$false)]
    [string]$AppName = "agentic-workflows-api"
)

$BaseUrl = "https://$AppName.onrender.com"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Agentic Workflows - Deployment Checker" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "App URL: $BaseUrl" -ForegroundColor Yellow
Write-Host ""

# Test 1: Health Check
Write-Host "[1/4] Testing Health Endpoint..." -ForegroundColor White
try {
    $response = Invoke-RestMethod -Uri "$BaseUrl/api/health" -Method Get -TimeoutSec 10
    Write-Host "  ✓ Health Check: PASSED" -ForegroundColor Green
    Write-Host "    Status: $($response.status)" -ForegroundColor Gray
    Write-Host "    Version: $($response.version)" -ForegroundColor Gray
    Write-Host "    Environment: $($response.environment)" -ForegroundColor Gray
} catch {
    Write-Host "  ✗ Health Check: FAILED" -ForegroundColor Red
    Write-Host "    Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Possible reasons:" -ForegroundColor Yellow
    Write-Host "  1. Deployment still in progress (wait 2-3 minutes)" -ForegroundColor Gray
    Write-Host "  2. App name incorrect (check Render dashboard)" -ForegroundColor Gray
    Write-Host "  3. Service not started yet" -ForegroundColor Gray
    exit 1
}

Write-Host ""

# Test 2: API Docs
Write-Host "[2/4] Testing API Documentation..." -ForegroundColor White
try {
    $response = Invoke-WebRequest -Uri "$BaseUrl/api/docs" -Method Get -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "  ✓ API Docs: ACCESSIBLE" -ForegroundColor Green
        Write-Host "    URL: $BaseUrl/api/docs" -ForegroundColor Gray
    }
} catch {
    Write-Host "  ✗ API Docs: NOT ACCESSIBLE" -ForegroundColor Red
}

Write-Host ""

# Test 3: OpenAPI Schema
Write-Host "[3/4] Testing OpenAPI Schema..." -ForegroundColor White
try {
    $response = Invoke-RestMethod -Uri "$BaseUrl/api/openapi.json" -Method Get -TimeoutSec 10
    Write-Host "  ✓ OpenAPI Schema: AVAILABLE" -ForegroundColor Green
    Write-Host "    Title: $($response.info.title)" -ForegroundColor Gray
    Write-Host "    Version: $($response.info.version)" -ForegroundColor Gray
} catch {
    Write-Host "  ✗ OpenAPI Schema: NOT AVAILABLE" -ForegroundColor Red
}

Write-Host ""

# Test 4: Plugins Endpoint
Write-Host "[4/4] Testing Plugins Endpoint..." -ForegroundColor White
try {
    $response = Invoke-RestMethod -Uri "$BaseUrl/api/plugins" -Method Get -TimeoutSec 10
    Write-Host "  ✓ Plugins Endpoint: WORKING" -ForegroundColor Green
    Write-Host "    Available Plugins: $($response.Count)" -ForegroundColor Gray
} catch {
    Write-Host "  ✗ Plugins Endpoint: ERROR" -ForegroundColor Red
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Deployment Status: LIVE ✓" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Visit API Docs: $BaseUrl/api/docs" -ForegroundColor Gray
Write-Host "  2. Register a user via /api/auth/register" -ForegroundColor Gray
Write-Host "  3. Test authentication and workflows" -ForegroundColor Gray
Write-Host ""
Write-Host "Dashboard: https://dashboard.render.com" -ForegroundColor Cyan
Write-Host ""
