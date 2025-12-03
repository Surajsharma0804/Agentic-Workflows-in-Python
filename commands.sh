#!/bin/bash
# Comprehensive Security Audit Commands
# Run these commands to reproduce all audit findings

set -e

echo "========================================="
echo "AGENTIC WORKFLOWS SECURITY AUDIT"
echo "Date: $(date)"
echo "========================================="

# Create audit results directory
mkdir -p audit-results

echo ""
echo "1. Installing audit tools..."
pip install -q ruff mypy pytest pytest-cov bandit safety pip-audit httpx

echo ""
echo "2. Running code linting (ruff)..."
ruff check . --output-format=json > audit-results/ruff.json 2>&1 || true
echo "   Results saved to: audit-results/ruff.json"

echo ""
echo "3. Running type checking (mypy)..."
mypy agentic_workflows --strict --no-error-summary 2>&1 | tee audit-results/mypy.txt || true
echo "   Results saved to: audit-results/mypy.txt"

echo ""
echo "4. Running security scan (bandit)..."
bandit -r agentic_workflows -f json -o audit-results/bandit.json 2>&1 || true
echo "   Results saved to: audit-results/bandit.json"

echo ""
echo "5. Checking for vulnerable dependencies (pip-audit)..."
pip-audit --format=json > audit-results/pip-audit.json 2>&1 || true
echo "   Results saved to: audit-results/pip-audit.json"

echo ""
echo "6. Checking for outdated dependencies (safety)..."
safety check --json > audit-results/safety.json 2>&1 || true
echo "   Results saved to: audit-results/safety.json"

echo ""
echo "7. Running tests with coverage..."
pytest -q --maxfail=1 --disable-warnings --cov=agentic_workflows --cov-report=html --cov-report=json 2>&1 | tee audit-results/pytest.txt || true
echo "   Results saved to: audit-results/pytest.txt"
echo "   Coverage report: htmlcov/index.html"

echo ""
echo "8. Building Docker image..."
docker build -t agentic-workflows:audit . > audit-results/docker-build.log 2>&1 || true
echo "   Build log saved to: audit-results/docker-build.log"

echo ""
echo "9. Scanning Docker image (trivy)..."
if command -v trivy &> /dev/null; then
    trivy image agentic-workflows:audit --format=json > audit-results/trivy.json 2>&1 || true
    echo "   Results saved to: audit-results/trivy.json"
else
    echo "   Trivy not installed. Install from: https://github.com/aquasecurity/trivy"
fi

echo ""
echo "10. Checking frontend dependencies..."
cd ui
npm audit --json > ../audit-results/npm-audit.json 2>&1 || true
cd ..
echo "   Results saved to: audit-results/npm-audit.json"

echo ""
echo "11. Checking for hard-coded secrets..."
grep -r "password\|secret\|api_key\|token" agentic_workflows --include="*.py" | grep -v "test" | grep -v ".pyc" > audit-results/secrets-scan.txt 2>&1 || true
echo "   Results saved to: audit-results/secrets-scan.txt"

echo ""
echo "12. Checking database connection..."
docker exec agentic-postgres psql -U agentic -d agentic_workflows -c "\dt" > audit-results/db-tables.txt 2>&1 || true
echo "   Results saved to: audit-results/db-tables.txt"

echo ""
echo "13. Checking API health..."
curl -s http://localhost:8000/api/health | jq . > audit-results/api-health.json 2>&1 || true
echo "   Results saved to: audit-results/api-health.json"

echo ""
echo "14. Checking Docker container status..."
docker ps -a --filter "name=agentic" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" > audit-results/docker-status.txt
echo "   Results saved to: audit-results/docker-status.txt"

echo ""
echo "========================================="
echo "AUDIT COMPLETE!"
echo "========================================="
echo ""
echo "Review results in the audit-results/ directory"
echo ""
echo "Critical findings to address:"
echo "  - Hard-coded secrets in auth.py"
echo "  - Missing database tables"
echo "  - SQL injection vulnerabilities"
echo "  - Shell command injection"
echo "  - Missing rate limiting"
echo "  - No HTTPS enforcement"
echo ""
echo "See audit-report.md for complete details and remediation steps."
