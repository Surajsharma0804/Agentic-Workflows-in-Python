#!/usr/bin/env pwsh
# Deployment Verification Script for Render.com FREE Tier

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  Deployment Verification - FREE Tier" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

$errors = 0
$warnings = 0

# Check 1: Critical Files Exist
Write-Host "[1/10] Checking critical files..." -ForegroundColor Yellow
$criticalFiles = @(
    "render.yaml",
    "Dockerfile",
    "start.sh",
    "requirements.txt",
    "agentic_workflows/config.py",
    "agentic_workflows/api/server.py",
    "agentic_workflows/celery_app.py"
)

foreach ($file in $criticalFiles) {
    if (Test-Path $file) {
        Write-Host "  [OK] $file" -ForegroundColor Green
    } else {
        Write-Host "  [FAIL] $file MISSING" -ForegroundColor Red
        $errors++
    }
}

# Check 2: .kiro Directory
Write-Host "`n[2/10] Checking .kiro directory..." -ForegroundColor Yellow
if (Test-Path ".kiro") {
    $kiroFiles = Get-ChildItem -Path ".kiro" -Recurse -File
    Write-Host "  [OK] .kiro directory exists ($($kiroFiles.Count) files)" -ForegroundColor Green
    
    # Check if .kiro is in .gitignore
    $gitignoreContent = Get-Content ".gitignore" -Raw
    if ($gitignoreContent -match "\.kiro") {
        Write-Host "  [FAIL] .kiro is in .gitignore - CONTEST DISQUALIFICATION RISK!" -ForegroundColor Red
        $errors++
    } else {
        Write-Host "  [OK] .kiro is NOT in .gitignore" -ForegroundColor Green
    }
} else {
    Write-Host "  [FAIL] .kiro directory missing - CONTEST DISQUALIFICATION!" -ForegroundColor Red
    $errors++
}

# Check 3: PORT Configuration
Write-Host "`n[3/10] Checking PORT configuration..." -ForegroundColor Yellow
$configContent = Get-Content "agentic_workflows/config.py" -Raw
if ($configContent -match 'env="PORT"') {
    Write-Host "  [OK] config.py uses PORT environment variable" -ForegroundColor Green
} else {
    Write-Host "  [FAIL] config.py doesn't use PORT env var" -ForegroundColor Red
    $errors++
}

$startContent = Get-Content "start.sh" -Raw
if ($startContent -match '\$\{PORT') {
    Write-Host "  [OK] start.sh uses PORT environment variable" -ForegroundColor Green
} else {
    Write-Host "  [FAIL] start.sh doesn't use PORT env var" -ForegroundColor Red
    $errors++
}

# Check 4: Redis/Celery Handling
Write-Host "`n[4/10] Checking Redis/Celery handling..." -ForegroundColor Yellow
$celeryContent = Get-Content "agentic_workflows/celery_app.py" -Raw
if ($celeryContent -match "try:" -and $celeryContent -match "except") {
    Write-Host "  [OK] Celery wrapped in try-except for FREE tier" -ForegroundColor Green
} else {
    Write-Host "  [WARN] Celery not wrapped - may crash without Redis" -ForegroundColor Yellow
    $warnings++
}

# Check 5: render.yaml Configuration
Write-Host "`n[5/10] Checking render.yaml..." -ForegroundColor Yellow
$renderContent = Get-Content "render.yaml" -Raw
if ($renderContent -match "plan: free") {
    Write-Host "  [OK] Using FREE plan" -ForegroundColor Green
} else {
    Write-Host "  [WARN] Not using FREE plan" -ForegroundColor Yellow
    $warnings++
}

if ($renderContent -match "type: redis") {
    Write-Host "  [WARN] Redis configured (costs `$7/month)" -ForegroundColor Yellow
    $warnings++
} else {
    Write-Host "  [OK] No Redis (FREE tier)" -ForegroundColor Green
}

if ($renderContent -match "healthCheckPath") {
    Write-Host "  [OK] Health check configured" -ForegroundColor Green
} else {
    Write-Host "  [FAIL] Health check missing" -ForegroundColor Red
    $errors++
}

# Check 6: Dockerfile
Write-Host "`n[6/10] Checking Dockerfile..." -ForegroundColor Yellow
$dockerContent = Get-Content "Dockerfile" -Raw
if ($dockerContent -match "start\.sh") {
    Write-Host "  [OK] Uses start.sh" -ForegroundColor Green
} else {
    Write-Host "  [FAIL] Doesn't use start.sh" -ForegroundColor Red
    $errors++
}

if ($dockerContent -match "HEALTHCHECK") {
    Write-Host "  [OK] Health check configured" -ForegroundColor Green
} else {
    Write-Host "  [WARN] No health check in Dockerfile" -ForegroundColor Yellow
    $warnings++
}

# Check 7: Python Syntax
Write-Host "`n[7/10] Checking Python syntax..." -ForegroundColor Yellow
$pythonFiles = Get-ChildItem -Path "agentic_workflows" -Filter "*.py" -Recurse
$syntaxErrors = 0
foreach ($file in $pythonFiles) {
    $result = python -m py_compile $file.FullName 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  [FAIL] Syntax error in $($file.Name)" -ForegroundColor Red
        $syntaxErrors++
    }
}
if ($syntaxErrors -eq 0) {
    $fileCount = $pythonFiles.Count
    Write-Host "  [OK] All Python files valid ($fileCount files)" -ForegroundColor Green
} else {
    Write-Host "  [FAIL] $syntaxErrors Python files have syntax errors" -ForegroundColor Red
    $errors += $syntaxErrors
}

# Check 8: Dependencies
Write-Host "`n[8/10] Checking dependencies..." -ForegroundColor Yellow
if (Test-Path "requirements-full.txt") {
    $reqContent = Get-Content "requirements-full.txt"
    $criticalDeps = @("fastapi", "uvicorn", "sqlalchemy", "psycopg2-binary", "pydantic")
    foreach ($dep in $criticalDeps) {
        if ($reqContent -match $dep) {
            Write-Host "  [OK] $dep" -ForegroundColor Green
        } else {
            Write-Host "  [FAIL] $dep missing" -ForegroundColor Red
            $errors++
        }
    }
} else {
    Write-Host "  [FAIL] requirements-full.txt missing" -ForegroundColor Red
    $errors++
}

# Check 9: Git Status
Write-Host "`n[9/10] Checking git status..." -ForegroundColor Yellow
$gitStatus = git status --porcelain 2>&1
if ($gitStatus) {
    Write-Host "  [WARN] Uncommitted changes:" -ForegroundColor Yellow
    Write-Host $gitStatus -ForegroundColor Gray
    $warnings++
} else {
    Write-Host "  [OK] All changes committed" -ForegroundColor Green
}

# Check 10: Documentation
Write-Host "`n[10/10] Checking documentation..." -ForegroundColor Yellow
$docs = @("README.md", "DEPLOY_FREE.md", "ARCHITECTURE.md", "CONTRIBUTING.md")
foreach ($doc in $docs) {
    if (Test-Path $doc) {
        Write-Host "  [OK] $doc" -ForegroundColor Green
    } else {
        Write-Host "  [WARN] $doc missing" -ForegroundColor Yellow
        $warnings++
    }
}

# Summary
Write-Host "`n=========================================" -ForegroundColor Cyan
Write-Host "  Verification Summary" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

if ($errors -eq 0 -and $warnings -eq 0) {
    Write-Host "[SUCCESS] PERFECT! Ready to deploy!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. git add ." -ForegroundColor White
    Write-Host "2. git commit -m 'Ready for FREE deployment'" -ForegroundColor White
    Write-Host "3. git push origin main" -ForegroundColor White
    Write-Host "4. Go to https://dashboard.render.com" -ForegroundColor White
    Write-Host "5. Click 'New +' -> 'Blueprint'" -ForegroundColor White
    Write-Host "6. Select your repository" -ForegroundColor White
    Write-Host "7. Click 'Apply'" -ForegroundColor White
    exit 0
} elseif ($errors -eq 0) {
    Write-Host "[WARNINGS] $warnings warnings found" -ForegroundColor Yellow
    Write-Host "You can deploy, but review warnings above." -ForegroundColor Yellow
    exit 0
} else {
    Write-Host "[FAILED] ERRORS: $errors | WARNINGS: $warnings" -ForegroundColor Red
    Write-Host "Fix errors before deploying!" -ForegroundColor Red
    exit 1
}
