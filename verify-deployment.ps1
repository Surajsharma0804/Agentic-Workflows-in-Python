# Deployment Verification Script
# Run this to check if your deployment is live

Write-Host "🔍 Verifying Agentic Workflows Deployment..." -ForegroundColor Cyan
Write-Host ""

$baseUrl = "https://agentic-workflows.onrender.com"

# Function to test endpoint
function Test-Endpoint {
    param($url, $name)
    
    Write-Host "Testing $name..." -NoNewline
    try {
        $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 30
        if ($response.StatusCode -eq 200) {
            Write-Host " ✅ OK (Status: $($response.StatusCode))" -ForegroundColor Green
            return $true
        } else {
            Write-Host " ⚠️  Status: $($response.StatusCode)" -ForegroundColor Yellow
            return $false
        }
    } catch {
        Write-Host " ❌ FAILED" -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Test endpoints
Write-Host "📡 Testing Endpoints:" -ForegroundColor Yellow
Write-Host ""

$results = @{
    "Main App" = Test-Endpoint "$baseUrl/" "Main App"
    "Health Check" = Test-Endpoint "$baseUrl/health" "Health Check"
    "API Docs" = Test-Endpoint "$baseUrl/docs" "API Docs"
}

Write-Host ""
Write-Host "📊 Results Summary:" -ForegroundColor Yellow
Write-Host ""

$passed = ($results.Values | Where-Object { $_ -eq $true }).Count
$total = $results.Count

Write-Host "Passed: $passed / $total" -ForegroundColor $(if ($passed -eq $total) { "Green" } else { "Yellow" })

if ($passed -eq $total) {
    Write-Host ""
    Write-Host "🎉 All checks passed! Your deployment is LIVE!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 Share this link: $baseUrl" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "⚠️  Some checks failed. Deployment might still be building..." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "💡 Tips:" -ForegroundColor Cyan
    Write-Host "   1. Check Render.com dashboard for build status"
    Write-Host "   2. Wait 5-10 minutes for initial deployment"
    Write-Host "   3. Check logs: render logs -s agentic-workflows"
    Write-Host "   4. Verify environment variables are set"
}

Write-Host ""
Write-Host "📚 Documentation:" -ForegroundColor Yellow
Write-Host "   - README.md"
Write-Host "   - DEPLOYMENT_CHECKLIST.md"
Write-Host "   - SHARE.md"
Write-Host "   - FINAL_STATUS.md"
Write-Host ""
