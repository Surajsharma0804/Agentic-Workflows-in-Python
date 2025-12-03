# Test Authentication Flow
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "TESTING AUTHENTICATION SYSTEM" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Register a new user
Write-Host "Test 1: Register new user..." -ForegroundColor Yellow
$registerBody = @{
    name = "Test User"
    email = "test@example.com"
    password = "SecurePass123!"
    company = "Test Company"
} | ConvertTo-Json

try {
    $registerResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/auth/register" `
        -Method POST `
        -Body $registerBody `
        -ContentType "application/json"
    
    Write-Host "✅ Registration successful!" -ForegroundColor Green
    Write-Host "User ID: $($registerResponse.user.id)" -ForegroundColor Green
    Write-Host "Email: $($registerResponse.user.email)" -ForegroundColor Green
    Write-Host "Token: $($registerResponse.access_token.Substring(0, 20))..." -ForegroundColor Green
    $token = $registerResponse.access_token
} catch {
    Write-Host "❌ Registration failed: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.ErrorDetails.Message) {
        Write-Host "Details: $($_.ErrorDetails.Message)" -ForegroundColor Red
    }
}

Write-Host ""

# Test 2: Try to register with same email (should fail)
Write-Host "Test 2: Try duplicate email (should fail)..." -ForegroundColor Yellow
try {
    $duplicateResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/auth/register" `
        -Method POST `
        -Body $registerBody `
        -ContentType "application/json"
    
    Write-Host "❌ SECURITY ISSUE: Duplicate email was accepted!" -ForegroundColor Red
} catch {
    Write-Host "✅ Correctly rejected duplicate email" -ForegroundColor Green
    Write-Host "Error: $($_.ErrorDetails.Message)" -ForegroundColor Gray
}

Write-Host ""

# Test 3: Login with correct credentials
Write-Host "Test 3: Login with correct credentials..." -ForegroundColor Yellow
$loginBody = @{
    email = "test@example.com"
    password = "SecurePass123!"
    remember_me = $true
} | ConvertTo-Json

try {
    $loginResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login" `
        -Method POST `
        -Body $loginBody `
        -ContentType "application/json"
    
    Write-Host "✅ Login successful!" -ForegroundColor Green
    Write-Host "User: $($loginResponse.user.name)" -ForegroundColor Green
    Write-Host "Token: $($loginResponse.access_token.Substring(0, 20))..." -ForegroundColor Green
} catch {
    Write-Host "❌ Login failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Test 4: Login with wrong password (should fail)
Write-Host "Test 4: Login with wrong password (should fail)..." -ForegroundColor Yellow
$wrongPasswordBody = @{
    email = "test@example.com"
    password = "WrongPassword123!"
    remember_me = $false
} | ConvertTo-Json

try {
    $wrongResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login" `
        -Method POST `
        -Body $wrongPasswordBody `
        -ContentType "application/json"
    
    Write-Host "❌ SECURITY ISSUE: Wrong password was accepted!" -ForegroundColor Red
} catch {
    Write-Host "✅ Correctly rejected wrong password" -ForegroundColor Green
    Write-Host "Error: $($_.ErrorDetails.Message)" -ForegroundColor Gray
}

Write-Host ""

# Test 5: Login with non-existent email (should fail)
Write-Host "Test 5: Login with non-existent email (should fail)..." -ForegroundColor Yellow
$nonExistentBody = @{
    email = "nonexistent@example.com"
    password = "SomePassword123!"
    remember_me = $false
} | ConvertTo-Json

try {
    $nonExistentResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login" `
        -Method POST `
        -Body $nonExistentBody `
        -ContentType "application/json"
    
    Write-Host "❌ SECURITY ISSUE: Non-existent email was accepted!" -ForegroundColor Red
} catch {
    Write-Host "✅ Correctly rejected non-existent email" -ForegroundColor Green
    Write-Host "Error: $($_.ErrorDetails.Message)" -ForegroundColor Gray
}

Write-Host ""

# Test 6: Verify database entry
Write-Host "Test 6: Verify user in database..." -ForegroundColor Yellow
try {
    $dbCheck = docker exec agentic-postgres psql -U agentic -d agentic_workflows -t -c "SELECT email, name, is_active FROM users WHERE email='test@example.com';"
    if ($dbCheck) {
        Write-Host "✅ User found in database:" -ForegroundColor Green
        Write-Host $dbCheck -ForegroundColor Gray
    } else {
        Write-Host "❌ User not found in database" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Database check failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "AUTHENTICATION TESTS COMPLETE" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
