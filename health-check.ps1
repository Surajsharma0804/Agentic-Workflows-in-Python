# Comprehensive Health Check Script for Agentic Workflows

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   AGENTIC WORKFLOWS HEALTH CHECK" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$errors = 0
$warnings = 0
$passed = 0

# Function to test Python import
function Test-PythonImport {
    param($module, $description)
    
    $result = python -c "import $module; print('OK')" 2>&1
    if ($LASTEXITCODE -eq 0 -and $result -match "OK") {
        Write-Host "  [PASS] $description" -ForegroundColor Green
        return $true
    } else {
        Write-Host "  [FAIL] $description" -ForegroundColor Red
        return $false
    }
}

# 1. Python Environment Check
Write-Host "1. Python Environment" -ForegroundColor Yellow
Write-Host "   Checking Python version..." -ForegroundColor Gray
$pythonVersion = python --version 2>&1
Write-Host "   $pythonVersion" -ForegroundColor Cyan

if (Test-Path ".venv") {
    Write-Host "  [PASS] Virtual environment exists" -ForegroundColor Green
    $passed++
} else {
    Write-Host "  [WARN] Virtual environment not found" -ForegroundColor Yellow
    $warnings++
}

# 2. Core Module Imports
Write-Host "`n2. Core Module Imports" -ForegroundColor Yellow
if (Test-PythonImport "agentic_workflows" "Core package") { $passed++ } else { $errors++ }
if (Test-PythonImport "agentic_workflows.core.spec" "Spec module") { $passed++ } else { $errors++ }
if (Test-PythonImport "agentic_workflows.core.orchestrator" "Orchestrator") { $passed++ } else { $errors++ }
if (Test-PythonImport "agentic_workflows.core.agents" "Agents") { $passed++ } else { $errors++ }
if (Test-PythonImport "agentic_workflows.runner" "CLI Runner") { $passed++ } else { $errors++ }

# 3. Plugin Imports
Write-Host "`n3. Plugin Imports" -ForegroundColor Yellow
if (Test-PythonImport "agentic_workflows.plugins.base" "Plugin base") { $passed++ } else { $errors++ }
if (Test-PythonImport "agentic_workflows.plugins.file_organizer" "File Organizer") { $passed++ } else { $errors++ }
if (Test-PythonImport "agentic_workflows.plugins.email_summarizer" "Email Summarizer") { $passed++ } else { $errors++ }
if (Test-PythonImport "agentic_workflows.plugins.http_task" "HTTP Task") { $passed++ } else { $errors++ }

# 4. File Structure Check
Write-Host "`n4. File Structure" -ForegroundColor Yellow
$criticalFiles = @(
    "pyproject.toml",
    "requirements.txt",
    "requirements-full.txt",
    "README.md",
    "LICENSE",
    "Dockerfile",
    "docker-compose.yml",
    ".env.example"
)

foreach ($file in $criticalFiles) {
    if (Test-Path $file) {
        Write-Host "  [PASS] $file" -ForegroundColor Green
        $passed++
    } else {
        Write-Host "  [FAIL] $file missing" -ForegroundColor Red
        $errors++
    }
}

# 5. Directory Structure Check
Write-Host "`n5. Directory Structure" -ForegroundColor Yellow
$criticalDirs = @(
    "agentic_workflows/core",
    "agentic_workflows/plugins",
    "agentic_workflows/api",
    "agentic_workflows/agents",
    "tests",
    "k8s",
    "docs",
    "ui"
)

foreach ($dir in $criticalDirs) {
    if (Test-Path $dir) {
        Write-Host "  [PASS] $dir/" -ForegroundColor Green
        $passed++
    } else {
        Write-Host "  [FAIL] $dir/ missing" -ForegroundColor Red
        $errors++
    }
}

# 6. YAML Spec Validation
Write-Host "`n6. YAML Spec Files" -ForegroundColor Yellow
$specFiles = Get-ChildItem -Path ".kiro/specs" -Filter "*.yaml" -ErrorAction SilentlyContinue

if ($specFiles) {
    foreach ($spec in $specFiles) {
        $relativePath = $spec.FullName.Replace((Get-Location).Path + "\", "").Replace("\", "/")
        $result = python -c "import yaml; yaml.safe_load(open(r'$($spec.FullName)')); print('OK')" 2>&1
        if ($LASTEXITCODE -eq 0 -and $result -match "OK") {
            Write-Host "  [PASS] $($spec.Name)" -ForegroundColor Green
            $passed++
        } else {
            Write-Host "  [FAIL] $($spec.Name) - Invalid YAML" -ForegroundColor Red
            $errors++
        }
    }
} else {
    Write-Host "  [WARN] No spec files found" -ForegroundColor Yellow
    $warnings++
}

# 7. Test Execution
Write-Host "`n7. Running Tests" -ForegroundColor Yellow
Write-Host "   Running basic tests..." -ForegroundColor Gray
$testResult = python -m pytest tests/test_orchestrator.py -v --tb=short 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  [PASS] Basic tests passed" -ForegroundColor Green
    $passed++
} else {
    Write-Host "  [FAIL] Tests failed" -ForegroundColor Red
    Write-Host "   $testResult" -ForegroundColor Gray
    $errors++
}

# 8. Documentation Check
Write-Host "`n8. Documentation" -ForegroundColor Yellow
$docFiles = @(
    "README.md",
    "ARCHITECTURE.md",
    "SETUP.md",
    "CONTRIBUTING.md",
    "docs/API.md",
    "docs/PLUGINS.md",
    "docs/DEPLOYMENT.md"
)

foreach ($doc in $docFiles) {
    if (Test-Path $doc) {
        Write-Host "  [PASS] $doc" -ForegroundColor Green
        $passed++
    } else {
        Write-Host "  [WARN] $doc missing" -ForegroundColor Yellow
        $warnings++
    }
}

# 9. UI Check
Write-Host "`n9. Frontend UI" -ForegroundColor Yellow
if (Test-Path "ui/package.json") {
    Write-Host "  [PASS] UI package.json exists" -ForegroundColor Green
    $passed++
    
    if (Test-Path "ui/src") {
        Write-Host "  [PASS] UI source directory exists" -ForegroundColor Green
        $passed++
    }
    
    $uiPages = Get-ChildItem -Path "ui/src/pages" -Filter "*.tsx" -ErrorAction SilentlyContinue
    if ($uiPages) {
        Write-Host "  [PASS] Found $($uiPages.Count) UI pages" -ForegroundColor Green
        $passed++
    }
} else {
    Write-Host "  [WARN] UI not initialized" -ForegroundColor Yellow
    $warnings++
}

# 10. DevOps Files
Write-Host "`n10. DevOps Configuration" -ForegroundColor Yellow
if (Test-Path "Dockerfile") {
    Write-Host "  [PASS] Dockerfile exists" -ForegroundColor Green
    $passed++
}
if (Test-Path "docker-compose.yml") {
    Write-Host "  [PASS] docker-compose.yml exists" -ForegroundColor Green
    $passed++
}
if (Test-Path "k8s") {
    $k8sFiles = Get-ChildItem -Path "k8s" -Filter "*.yaml" -ErrorAction SilentlyContinue
    if ($k8sFiles) {
        Write-Host "  [PASS] Found $($k8sFiles.Count) Kubernetes manifests" -ForegroundColor Green
        $passed++
    }
}
if (Test-Path ".github/workflows") {
    $workflows = Get-ChildItem -Path ".github/workflows" -Filter "*.yml" -ErrorAction SilentlyContinue
    if ($workflows) {
        Write-Host "  [PASS] Found $($workflows.Count) CI/CD workflows" -ForegroundColor Green
        $passed++
    }
}

# Summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   HEALTH CHECK SUMMARY" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Passed:   $passed" -ForegroundColor Green
Write-Host "  Warnings: $warnings" -ForegroundColor Yellow
Write-Host "  Errors:   $errors" -ForegroundColor Red
Write-Host ""

if ($errors -eq 0 -and $warnings -eq 0) {
    Write-Host "  STATUS: EXCELLENT - All checks passed!" -ForegroundColor Green
    Write-Host "  Your project is 100% healthy and ready!" -ForegroundColor Green
} elseif ($errors -eq 0) {
    Write-Host "  STATUS: GOOD - No critical errors" -ForegroundColor Green
    Write-Host "  Some optional components missing (warnings)" -ForegroundColor Yellow
} elseif ($errors -le 3) {
    Write-Host "  STATUS: FAIR - Minor issues detected" -ForegroundColor Yellow
    Write-Host "  Please review and fix the errors above" -ForegroundColor Yellow
} else {
    Write-Host "  STATUS: NEEDS ATTENTION - Multiple errors" -ForegroundColor Red
    Write-Host "  Please fix the errors before proceeding" -ForegroundColor Red
}

Write-Host "`n========================================`n" -ForegroundColor Cyan

# Return exit code based on errors
if ($errors -gt 0) {
    exit 1
} else {
    exit 0
}
