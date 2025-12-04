# Pre-Deployment Comprehensive Check Script
# Run this before deploying to catch any issues

$ErrorActionPreference = "Continue"
$passed = 0
$failed = 0
$warnings = 0

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  PRE-DEPLOYMENT COMPREHENSIVE CHECK" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

function Test-Check {
    param($name, $command, $path = ".")
    
    Write-Host "[$name]" -NoNewline -ForegroundColor Yellow
    Write-Host " Testing..." -NoNewline
    
    try {
        Push-Location $path
        $output = Invoke-Expression "$command 2>&1"
        $exitCode = $LASTEXITCODE
        Pop-Location
        
        if ($exitCode -eq 0) {
            Write-Host " ✅ PASS" -ForegroundColor Green
            $script:passed++
            return $true
        } else {
            Write-Host " ❌ FAIL" -ForegroundColor Red
            Write-Host "   Output: $output" -ForegroundColor Red
            $script:failed++
            return $false
        }
    } catch {
        Write-Host " ❌ ERROR" -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
        $script:failed++
        return $false
    }
}

function Test-FileExists {
    param($name, $path)
    
    Write-Host "[$name]" -NoNewline -ForegroundColor Yellow
    Write-Host " Checking..." -NoNewline
    
    if (Test-Path $path) {
        Write-Host " ✅ EXISTS" -ForegroundColor Green
        $script:passed++
        return $true
    } else {
        Write-Host " ❌ MISSING" -ForegroundColor Red
        $script:failed++
        return $false
    }
}

# 1. FRONTEND CHECKS
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "1. FRONTEND CHECKS" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

Test-FileExists "package.json" "ui/package.json"
Test-FileExists "vite.config.ts" "ui/vite.config.ts"
Test-FileExists "tsconfig.json" "ui/tsconfig.json"
Test-FileExists "index.html" "ui/index.html"
Test-FileExists "manifest.json" "ui/public/manifest.json"
Test-FileExists "service worker" "ui/public/sw.js"
Test-FileExists "robots.txt" "ui/public/robots.txt"

Write-Host ""
Test-Check "TypeScript compilation" "npm run type-check" "ui"
Test-Check "Frontend build" "npm run build" "ui"

if (Test-Path "ui/dist/index.html") {
    Write-Host "[Build output]" -NoNewline -ForegroundColor Yellow
    Write-Host " ✅ dist/index.html exists" -ForegroundColor Green
    $script:passed++
} else {
    Write-Host "[Build output]" -NoNewline -ForegroundColor Yellow
    Write-Host " ❌ dist/index.html missing" -ForegroundColor Red
    $script:failed++
}

# 2. BACKEND CHECKS
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "2. BACKEND CHECKS" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

Test-FileExists "config.py" "agentic_workflows/config.py"
Test-FileExists "server.py" "agentic_workflows/api/server.py"
Test-FileExists "health.py" "agentic_workflows/api/routes/health.py"
Test-FileExists "requirements" "requirements-full.txt"
Test-FileExists "pyproject.toml" "pyproject.toml"

Write-Host ""
Test-Check "Python syntax check" "python -m py_compile agentic_workflows/config.py" "."

# 3. DEPLOYMENT FILES
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "3. DEPLOYMENT FILES" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

Test-FileExists "Dockerfile" "Dockerfile"
Test-FileExists "render.yaml" "render.yaml"
Test-FileExists "entrypoint.sh" "entrypoint.sh"
Test-FileExists ".env.example" ".env.example"

# 4. DOCUMENTATION
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "4. DOCUMENTATION" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

Test-FileExists "README.md" "README.md"
Test-FileExists "DEPLOYMENT_CHECKLIST.md" "DEPLOYMENT_CHECKLIST.md"
Test-FileExists "SHARE.md" "SHARE.md"
Test-FileExists "FINAL_STATUS.md" "FINAL_STATUS.md"

# 5. GIT STATUS
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "5. GIT STATUS" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

$gitStatus = git status --porcelain
if ($gitStatus) {
    Write-Host "[Git status]" -NoNewline -ForegroundColor Yellow
    Write-Host " ⚠️  UNCOMMITTED CHANGES" -ForegroundColor Yellow
    Write-Host "   Files:" -ForegroundColor Yellow
    $gitStatus | ForEach-Object { Write-Host "   $_" -ForegroundColor Yellow }
    $script:warnings++
} else {
    Write-Host "[Git status]" -NoNewline -ForegroundColor Yellow
    Write-Host " ✅ CLEAN" -ForegroundColor Green
    $script:passed++
}

$currentBranch = git branch --show-current
Write-Host "[Git branch]" -NoNewline -ForegroundColor Yellow
Write-Host " $currentBranch" -ForegroundColor Cyan

# 6. CONFIGURATION VALIDATION
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "6. CONFIGURATION VALIDATION" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

# Check render.yaml
$renderYaml = Get-Content "render.yaml" -Raw
if ($renderYaml -match "healthCheckPath: /api/health") {
    Write-Host "[Health check path]" -NoNewline -ForegroundColor Yellow
    Write-Host " ✅ CORRECT (/api/health)" -ForegroundColor Green
    $script:passed++
} else {
    Write-Host "[Health check path]" -NoNewline -ForegroundColor Yellow
    Write-Host " ❌ INCORRECT" -ForegroundColor Red
    $script:failed++
}

if ($renderYaml -match "region: oregon") {
    Write-Host "[Region]" -NoNewline -ForegroundColor Yellow
    Write-Host " ✅ SET (oregon)" -ForegroundColor Green
    $script:passed++
} else {
    Write-Host "[Region]" -NoNewline -ForegroundColor Yellow
    Write-Host " ❌ MISSING" -ForegroundColor Red
    $script:failed++
}

if ($renderYaml -match "branch: main") {
    Write-Host "[Branch]" -NoNewline -ForegroundColor Yellow
    Write-Host " ✅ SET (main)" -ForegroundColor Green
    $script:passed++
} else {
    Write-Host "[Branch]" -NoNewline -ForegroundColor Yellow
    Write-Host " ❌ MISSING" -ForegroundColor Red
    $script:failed++
}

# Check config.py for PORT env variable
$configPy = Get-Content "agentic_workflows/config.py" -Raw
if ($configPy -match 'env="PORT"') {
    Write-Host "[PORT env variable]" -NoNewline -ForegroundColor Yellow
    Write-Host " ✅ CORRECT" -ForegroundColor Green
    $script:passed++
} else {
    Write-Host "[PORT env variable]" -NoNewline -ForegroundColor Yellow
    Write-Host " ❌ INCORRECT" -ForegroundColor Red
    $script:failed++
}

# SUMMARY
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  SUMMARY" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ Passed:   $passed" -ForegroundColor Green
Write-Host "❌ Failed:   $failed" -ForegroundColor $(if ($failed -gt 0) { "Red" } else { "Green" })
Write-Host "⚠️  Warnings: $warnings" -ForegroundColor Yellow
Write-Host ""

$total = $passed + $failed
$percentage = if ($total -gt 0) { [math]::Round(($passed / $total) * 100, 1) } else { 0 }

Write-Host "Success Rate: $percentage%" -ForegroundColor $(if ($percentage -ge 90) { "Green" } elseif ($percentage -ge 70) { "Yellow" } else { "Red" })
Write-Host ""

if ($failed -eq 0) {
    Write-Host "🎉 ALL CHECKS PASSED! Ready to deploy!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. git add -A" -ForegroundColor White
    Write-Host "  2. git commit -m 'your message'" -ForegroundColor White
    Write-Host "  3. git push origin main" -ForegroundColor White
    Write-Host ""
    exit 0
} else {
    Write-Host "⚠️  SOME CHECKS FAILED! Please fix issues before deploying." -ForegroundColor Red
    Write-Host ""
    exit 1
}
