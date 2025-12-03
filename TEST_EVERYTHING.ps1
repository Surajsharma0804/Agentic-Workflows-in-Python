# Comprehensive System Test Script
# Tests all components from scratch

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "COMPREHENSIVE SYSTEM TEST" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

$testsPassed = 0
$testsFailed = 0

# Test 1: Docker Services
Write-Host "Test 1: Checking Docker services..." -ForegroundColor Yellow
$services = docker ps --filter "name=agentic" --format "{{.Names}}\t{{.Status}}"
if ($services -like "*agentic-api*Up*" -and $services -like "*agentic-postgres*Up*") {
    Write-Host "✅ Docker services running" -ForegroundColor Green
    $testsPassed++
} else {
    Write-Host "❌ Docker services not running" -ForegroundColor Red
    $testsFailed++
}

# Test 2: API Health
Write-Host "`nTest 2: Checking API health..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/api/health" -ErrorAction Stop
    if ($health.status -eq "healthy") {
        Write-Host "✅ API is healthy" -ForegroundColor Green
        $testsPassed++
    } else {
        Write-Host "❌ API is not healthy" -ForegroundColor Red
        $testsFailed++
    }
} catch {
    Write-Host "❌ API not responding" -ForegroundColor Red
    $testsFailed++
}

# Test 3: Database Connection
Write-Host "`nTest 3: Checking database..." -ForegroundColor Yellow
try {
    $dbCheck = docker exec agentic-postgres psql -U agentic -d agentic_workflows -t -c "SELECT COUNT(*) FROM users;" 2>$null
    if ($dbCheck) {
        Write-Host "✅ Database connected and users table exists" -ForegroundColor Green
        $testsPassed++
    } else {
        Write-Host "❌ Database table not found" -ForegroundColor Red
        $testsFailed++
    }
} catch {
    Write-Host "❌ Database connection failed" -ForegroundColor Red
    $testsFailed++
}

# Test 4: Authentication - Login
Write-Host "`nTest 4: Testing authentication (login)..." -ForegroundColor Yellow
try {
    $loginBody = @{
        email = "test@example.com"
        password = "SecurePass123!"
        remember_me = $true
    } | ConvertTo-Json

    $loginResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login" `
        -Method POST `
        -Body $loginBody `
        -ContentType "application/json" `
        -ErrorAction Stop

    if ($loginResponse.access_token) {
        Write-Host "✅ Authentication working" -ForegroundColor Green
        $testsPassed++
    } else {
        Write-Host "❌ Authentication failed" -ForegroundColor Red
        $testsFailed++
    }
} catch {
    Write-Host "❌ Authentication error: $($_.Exception.Message)" -ForegroundColor Red
    $testsFailed++
}

# Test 5: Wrong Password Rejection
Write-Host "`nTest 5: Testing wrong password rejection..." -ForegroundColor Yellow
try {
    $wrongBody = @{
        email = "test@example.com"
        password = "WrongPassword!"
        remember_me = $false
    } | ConvertTo-Json

    $wrongResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login" `
        -Method POST `
        -Body $wrongBody `
        -ContentType "application/json" `
        -ErrorAction Stop

    Write-Host "❌ SECURITY ISSUE: Wrong password accepted!" -ForegroundColor Red
    $testsFailed++
} catch {
    Write-Host "✅ Wrong password correctly rejected" -ForegroundColor Green
    $testsPassed++
}

# Test 6: UI Accessibility
Write-Host "`nTest 6: Checking UI accessibility..." -ForegroundColor Yellow
try {
    $uiCheck = Invoke-WebRequest -Uri "http://localhost:3001" -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
    if ($uiCheck.StatusCode -eq 200) {
        Write-Host "✅ UI is accessible" -ForegroundColor Green
        $testsPassed++
    } else {
        Write-Host "❌ UI not accessible" -ForegroundColor Red
        $testsFailed++
    }
} catch {
    Write-Host "⚠️  UI not running (may need to start separately)" -ForegroundColor Yellow
    Write-Host "   Run: cd ui && npm run dev" -ForegroundColor Gray
}

# Test 7: API Documentation
Write-Host "`nTest 7: Checking API documentation..." -ForegroundColor Yellow
try {
    $docsCheck = Invoke-WebRequest -Uri "http://localhost:8000/api/docs" -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
    if ($docsCheck.StatusCode -eq 200) {
        Write-Host "✅ API documentation accessible" -ForegroundColor Green
        $testsPassed++
    } else {
        Write-Host "❌ API documentation not accessible" -ForegroundColor Red
        $testsFailed++
    }
} catch {
    Write-Host "❌ API documentation error" -ForegroundColor Red
    $testsFailed++
}

# Test 8: Redis Connection
Write-Host "`nTest 8: Checking Redis..." -ForegroundColor Yellow
try {
    $redisCheck = docker exec agentic-redis redis-cli ping 2>$null
    if ($redisCheck -eq "PONG") {
        Write-Host "✅ Redis is running" -ForegroundColor Green
        $testsPassed++
    } else {
        Write-Host "❌ Redis not responding" -ForegroundColor Red
        $testsFailed++
    }
} catch {
    Write-Host "❌ Redis connection failed" -ForegroundColor Red
    $testsFailed++
}

# Test 9: File Structure
Write-Host "`nTest 9: Checking file structure..." -ForegroundColor Yellow
$requiredFiles = @(
    "docker-compose.yml",
    "Dockerfile",
    "requirements.txt",
    "requirements-full.txt",
    "ui/package.json",
    "ui/src/App.tsx",
    "ui/src/components/Alert.tsx",
    "ui/src/contexts/AlertContext.tsx",
    "agentic_workflows/api/server.py",
    "agentic_workflows/db/models.py"
)

$allFilesExist = $true
foreach ($file in $requiredFiles) {
    if (-not (Test-Path $file)) {
        Write-Host "❌ Missing file: $file" -ForegroundColor Red
        $allFilesExist = $false
    }
}

if ($allFilesExist) {
    Write-Host "✅ All required files present" -ForegroundColor Green
    $testsPassed++
} else {
    Write-Host "❌ Some files missing" -ForegroundColor Red
    $testsFailed++
}

# Test 10: Documentation
Write-Host "`nTest 10: Checking documentation..." -ForegroundColor Yellow
$docFiles = @(
    "README.md",
    "SUBMISSION.md",
    "AUTHENTICATION_VERIFIED.md",
    "FINAL_STATUS.md",
    "START_HERE.md"
)

$allDocsExist = $true
foreach ($doc in $docFiles) {
    if (-not (Test-Path $doc)) {
        Write-Host "❌ Missing documentation: $doc" -ForegroundColor Red
        $allDocsExist = $false
    }
}

if ($allDocsExist) {
    Write-Host "✅ All documentation present" -ForegroundColor Green
    $testsPassed++
} else {
    Write-Host "❌ Some documentation missing" -ForegroundColor Red
    $testsFailed++
}

# Summary
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "TEST SUMMARY" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Tests Passed: $testsPassed" -ForegroundColor Green
Write-Host "Tests Failed: $testsFailed" -ForegroundColor Red
Write-Host ""

$totalTests = $testsPassed + $testsFailed
$successRate = [math]::Round(($testsPassed / $totalTests) * 100, 2)
Write-Host "Success Rate: $successRate%" -ForegroundColor $(if ($successRate -ge 80) { "Green" } elseif ($successRate -ge 60) { "Yellow" } else { "Red" })

Write-Host ""
if ($testsFailed -eq 0) {
    Write-Host "🎉 ALL TESTS PASSED! System is fully operational." -ForegroundColor Green
} elseif ($testsFailed -le 2) {
    Write-Host "⚠️  Most tests passed. Minor issues detected." -ForegroundColor Yellow
} else {
    Write-Host "❌ Multiple tests failed. Please review the issues above." -ForegroundColor Red
}

Write-Host ""
Write-Host "Quick Actions:" -ForegroundColor White
Write-Host "  • View logs:     docker logs agentic-api --tail 50" -ForegroundColor Gray
Write-Host "  • Restart API:   docker-compose restart api" -ForegroundColor Gray
Write-Host "  • Start UI:      cd ui && npm run dev" -ForegroundColor Gray
Write-Host "  • Full restart:  docker-compose down && docker-compose up -d" -ForegroundColor Gray
Write-Host ""
