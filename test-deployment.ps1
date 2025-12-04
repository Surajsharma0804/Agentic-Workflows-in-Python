#!/usr/bin/env pwsh
# Test Render.com Deployment

$BASE_URL = "https://agentic-workflows.onrender.com"

Write-Host "`n=== Testing Agentic Workflows Deployment ===" -ForegroundColor Cyan
Write-Host "Base URL: $BASE_URL`n" -ForegroundColor Gray

# Test 1: Health Check
Write-Host "[1/4] Testing Health Check..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$BASE_URL/api/health" -Method Get -TimeoutSec 10
    Write-Host "✅ Health Check: PASSED" -ForegroundColor Green
    Write-Host "   Status: $($response.status)" -ForegroundColor Gray
} catch {
    Write-Host "❌ Health Check: FAILED" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Gray
}

# Test 2: Debug Filesystem
Write-Host "`n[2/4] Testing Debug Filesystem..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$BASE_URL/api/debug/filesystem" -Method Get -TimeoutSec 10
    Write-Host "✅ Debug Filesystem: PASSED" -ForegroundColor Green
    Write-Host "   UI Dist Exists: $($response.ui_dist_exists)" -ForegroundColor Gray
    Write-Host "   UI Dist Path: $($response.ui_dist_path)" -ForegroundColor Gray
    Write-Host "   Contents: $($response.ui_dist_contents -join ', ')" -ForegroundColor Gray
    
    if (-not $response.ui_dist_exists) {
        Write-Host "`n⚠️  WARNING: ui/dist folder not found!" -ForegroundColor Red
        Write-Host "   This means the frontend was not built or copied correctly." -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Debug Filesystem: FAILED" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Gray
}

# Test 3: Frontend Root
Write-Host "`n[3/4] Testing Frontend Root..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$BASE_URL/" -Method Get -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        $isHtml = $response.Content -match "<!DOCTYPE html>"
        if ($isHtml) {
            Write-Host "✅ Frontend Root: PASSED" -ForegroundColor Green
            Write-Host "   Status: $($response.StatusCode)" -ForegroundColor Gray
            Write-Host "   Content-Type: $($response.Headers['Content-Type'])" -ForegroundColor Gray
        } else {
            Write-Host "⚠️  Frontend Root: WARNING" -ForegroundColor Yellow
            Write-Host "   Status: $($response.StatusCode) but not HTML" -ForegroundColor Gray
        }
    }
} catch {
    Write-Host "❌ Frontend Root: FAILED" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Gray
    Write-Host "   Status: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Gray
}

# Test 4: API Docs
Write-Host "`n[4/4] Testing API Docs..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$BASE_URL/api/docs" -Method Get -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ API Docs: PASSED" -ForegroundColor Green
        Write-Host "   Status: $($response.StatusCode)" -ForegroundColor Gray
    }
} catch {
    Write-Host "❌ API Docs: FAILED" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Gray
}

# Summary
Write-Host "`n=== Summary ===" -ForegroundColor Cyan
Write-Host "If all tests passed, your deployment is working!" -ForegroundColor Green
Write-Host "If Frontend Root failed, check the Debug Filesystem output." -ForegroundColor Yellow
Write-Host "`nLive URL: $BASE_URL" -ForegroundColor Cyan
Write-Host "API Docs: $BASE_URL/api/docs" -ForegroundColor Cyan
Write-Host "`n"
