#!/usr/bin/env pwsh
# Agentic Workflows - Complete Command Reference (PowerShell)
# Run these commands to reproduce audit checks, tests, and deployment

$ErrorActionPreference = "Continue"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  Agentic Workflows - Command Reference" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# STEP 1: Install Dependencies
Write-Host "`n[1/10] Installing dependencies..." -ForegroundColor Yellow
python -m pip install --upgrade pip
python -m pip install -r requirements-full.txt
python -m pip install pytest pytest-cov ruff mypy bandit safety pip-audit

# STEP 2: Security Scans
Write-Host "`n[2/10] Running security scans..." -ForegroundColor Yellow
Write-Host "  - Bandit (Python security issues)..."
bandit -r agentic_workflows -lll -f json -o audit/raw-outputs/bandit-report.json
bandit -r agentic_workflows -lll

Write-Host "  - pip-audit (vulnerable dependencies)..."
pip-audit --desc --format json --output audit/raw-outputs/pip-audit-report.json
pip-audit --desc

Write-Host "  - safety check..."
safety check --json --output audit/raw-outputs/safety-report.json
safety check

# STEP 3: Code Quality Checks
Write-Host "`n[3/10] Running code quality checks..." -ForegroundColor Yellow
Write-Host "  - Ruff linter..."
ruff check . --output-format=json | Out-File audit/raw-outputs/ruff-report.json
ruff check .

Write-Host "  - MyPy type checker..."
mypy agentic_workflows --ignore-missing-imports

# STEP 4: Run Tests
Write-Host "`n[4/10] Running tests..." -ForegroundColor Yellow
pytest -v --maxfail=1 --disable-warnings --tb=short `
  --cov=agentic_workflows `
  --cov-report=xml:audit/raw-outputs/coverage.xml `
  --cov-report=term `
  --cov-report=html:audit/raw-outputs/htmlcov

# STEP 5: License Audit
Write-Host "`n[5/10] Auditing licenses..." -ForegroundColor Yellow
pip-licenses --format=csv --output-file=audit/raw-outputs/licenses.csv
pip-licenses

# STEP 6: Build Docker Image
Write-Host "`n[6/10] Building Docker image..." -ForegroundColor Yellow
docker build -t agentic-workflows:local -f Dockerfile .

# STEP 7: Docker Security Scan
Write-Host "`n[7/10] Scanning Docker image..." -ForegroundColor Yellow
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock `
  aquasec/trivy image --severity HIGH,CRITICAL `
  --format json --output audit/raw-outputs/trivy-report.json `
  agentic-workflows:local

# STEP 8: Git Status
Write-Host "`n[8/10] Checking git status..." -ForegroundColor Yellow
git status --porcelain | Out-File audit/raw-outputs/git-status.txt
git rev-parse --abbrev-ref HEAD | Out-File audit/raw-outputs/git-branch.txt
git log -1 --pretty=format:"%H %s" | Out-File audit/raw-outputs/git-commit.txt

# STEP 9: Run Demo (Dry-run)
Write-Host "`n[9/10] Running workflow demo (dry-run)..." -ForegroundColor Yellow
python -m agentic_workflows.runner run `
  --spec ./.kiro/specs/lazy_file_butler.yaml `
  --dry-run `
  | Out-File audit/raw-outputs/demo-output.txt

# STEP 10: Start Server (Background)
Write-Host "`n[10/10] Starting server for health check..." -ForegroundColor Yellow
$env:DATABASE_URL = "sqlite:///./test.db"
$env:SECRET_KEY = "test-secret-key-for-demo-only"
$env:PORT = "8080"

# Start server in background
$serverJob = Start-Job -ScriptBlock {
    param($port)
    uvicorn agentic_workflows.api.server:app --host 0.0.0.0 --port $port
} -ArgumentList 8080

# Wait for server to start
Write-Host "Waiting for server to start..."
Start-Sleep -Seconds 5

# Test health endpoint
Write-Host "Testing health endpoint..."
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8080/api/health" -UseBasicParsing
    $response.Content | Out-File audit/raw-outputs/health-check.json
    Write-Host "Health check: OK" -ForegroundColor Green
} catch {
    Write-Host "Health check failed: $_" -ForegroundColor Red
}

# Test API docs
Write-Host "Testing API docs..."
try {
    Invoke-WebRequest -Uri "http://localhost:8080/api/docs" -OutFile audit/raw-outputs/api-docs.html
} catch {
    Write-Host "API docs check failed: $_" -ForegroundColor Yellow
}

# Stop server
Write-Host "Stopping server..."
Stop-Job -Job $serverJob
Remove-Job -Job $serverJob

Write-Host "`n=========================================" -ForegroundColor Cyan
Write-Host "  All checks complete!" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Results saved to: audit/raw-outputs/" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Review audit/audit-report.md"
Write-Host "2. Apply fixes from fixes/ directory"
Write-Host "3. Run tests again to verify"
Write-Host "4. Deploy using deploy/README.md"
Write-Host ""
