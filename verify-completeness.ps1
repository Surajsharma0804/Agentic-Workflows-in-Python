# Verification Script for Agentic Workflows

Write-Host "Verifying Agentic Workflows Completeness..." -ForegroundColor Cyan
Write-Host ("=" * 60) -ForegroundColor Cyan
Write-Host ""

$errors = 0
$warnings = 0

# Check critical files
$criticalFiles = @(
    "pyproject.toml",
    "requirements.txt",
    "requirements-full.txt",
    "Dockerfile",
    "docker-compose.yml",
    ".env.example",
    "README.md",
    "LICENSE",
    "Makefile",
    "alembic.ini"
)

Write-Host "Checking Critical Files..." -ForegroundColor Yellow
foreach ($file in $criticalFiles) {
    if (Test-Path $file) {
        Write-Host "  [OK] $file" -ForegroundColor Green
    } else {
        Write-Host "  [MISSING] $file" -ForegroundColor Red
        $errors++
    }
}

# Check directories
$criticalDirs = @(
    "agentic_workflows/api",
    "agentic_workflows/core",
    "agentic_workflows/plugins",
    "agentic_workflows/db",
    "agentic_workflows/auth",
    "agentic_workflows/cache",
    "agentic_workflows/monitoring",
    "agentic_workflows/tasks",
    "tests",
    "k8s",
    "docs",
    ".github/workflows"
)

Write-Host "`nChecking Critical Directories..." -ForegroundColor Yellow
foreach ($dir in $criticalDirs) {
    if (Test-Path $dir) {
        Write-Host "  [OK] $dir" -ForegroundColor Green
    } else {
        Write-Host "  [MISSING] $dir" -ForegroundColor Red
        $errors++
    }
}

# Check plugins
$plugins = @(
    "agentic_workflows/plugins/file_organizer.py",
    "agentic_workflows/plugins/email_summarizer.py",
    "agentic_workflows/plugins/http_task.py",
    "agentic_workflows/plugins/ai/openai_plugin.py",
    "agentic_workflows/plugins/database/postgres_plugin.py",
    "agentic_workflows/plugins/cloud/aws_s3_plugin.py",
    "agentic_workflows/plugins/communication/slack_plugin.py",
    "agentic_workflows/plugins/communication/email_plugin.py",
    "agentic_workflows/plugins/devops/git_plugin.py"
)

Write-Host "`nChecking Plugins..." -ForegroundColor Yellow
foreach ($plugin in $plugins) {
    if (Test-Path $plugin) {
        Write-Host "  [OK] $(Split-Path $plugin -Leaf)" -ForegroundColor Green
    } else {
        Write-Host "  [MISSING] $(Split-Path $plugin -Leaf)" -ForegroundColor Red
        $errors++
    }
}

# Check tests
$tests = @(
    "tests/test_orchestrator.py",
    "tests/test_file_organizer.py",
    "tests/test_utils.py",
    "tests/test_api.py",
    "tests/test_plugins.py",
    "tests/test_config.py"
)

Write-Host "`nChecking Tests..." -ForegroundColor Yellow
foreach ($test in $tests) {
    if (Test-Path $test) {
        Write-Host "  [OK] $(Split-Path $test -Leaf)" -ForegroundColor Green
    } else {
        Write-Host "  [MISSING] $(Split-Path $test -Leaf)" -ForegroundColor Red
        $errors++
    }
}

# Check Kubernetes manifests
$k8sFiles = @(
    "k8s/namespace.yaml",
    "k8s/deployment.yaml",
    "k8s/service.yaml",
    "k8s/ingress.yaml",
    "k8s/hpa.yaml"
)

Write-Host "`nChecking Kubernetes Manifests..." -ForegroundColor Yellow
foreach ($file in $k8sFiles) {
    if (Test-Path $file) {
        Write-Host "  [OK] $(Split-Path $file -Leaf)" -ForegroundColor Green
    } else {
        Write-Host "  [MISSING] $(Split-Path $file -Leaf)" -ForegroundColor Red
        $errors++
    }
}

# Check documentation
$docs = @(
    "README.md",
    "ARCHITECTURE.md",
    "SETUP.md",
    "CONTRIBUTING.md",
    "IMPLEMENTATION_ROADMAP.md",
    "COMPLETE_FEATURE_LIST.md",
    "FINAL_SUMMARY.md",
    "docs/API.md",
    "docs/PLUGINS.md",
    "docs/DEPLOYMENT.md"
)

Write-Host "`nChecking Documentation..." -ForegroundColor Yellow
foreach ($doc in $docs) {
    if (Test-Path $doc) {
        Write-Host "  [OK] $(Split-Path $doc -Leaf)" -ForegroundColor Green
    } else {
        Write-Host "  [MISSING] $(Split-Path $doc -Leaf)" -ForegroundColor Red
        $warnings++
    }
}

# Count files
Write-Host "`nStatistics..." -ForegroundColor Yellow
$pythonFiles = (Get-ChildItem -Recurse -Filter "*.py" | Where-Object { $_.FullName -notmatch "\.venv|__pycache__|\.egg-info" }).Count
$yamlFiles = (Get-ChildItem -Recurse -Filter "*.yaml" -ErrorAction SilentlyContinue).Count + (Get-ChildItem -Recurse -Filter "*.yml" -ErrorAction SilentlyContinue).Count
$mdFiles = (Get-ChildItem -Recurse -Filter "*.md" -ErrorAction SilentlyContinue).Count

Write-Host "  Python files: $pythonFiles" -ForegroundColor Cyan
Write-Host "  YAML files: $yamlFiles" -ForegroundColor Cyan
Write-Host "  Markdown files: $mdFiles" -ForegroundColor Cyan

# Final summary
Write-Host "`n" + ("=" * 60) -ForegroundColor Cyan
if ($errors -eq 0 -and $warnings -eq 0) {
    Write-Host "ALL CHECKS PASSED!" -ForegroundColor Green
    Write-Host "Your project is 100% complete and ready!" -ForegroundColor Green
} elseif ($errors -eq 0) {
    Write-Host "$warnings warnings found (non-critical)" -ForegroundColor Yellow
    Write-Host "Project is functional and ready!" -ForegroundColor Green
} else {
    Write-Host "$errors critical errors found" -ForegroundColor Red
    Write-Host "$warnings warnings found" -ForegroundColor Yellow
    Write-Host "Please fix the errors above." -ForegroundColor Red
}

Write-Host "`nNext Steps:" -ForegroundColor Cyan
Write-Host "  1. Run: .\quick-start.ps1" -ForegroundColor White
Write-Host "  2. Visit: http://localhost:8000/api/docs" -ForegroundColor White
Write-Host "  3. Check: FINAL_SUMMARY.md for complete overview" -ForegroundColor White
Write-Host ""
