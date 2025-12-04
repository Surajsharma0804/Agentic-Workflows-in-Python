#!/bin/bash
# Agentic Workflows - Complete Command Reference
# Run these commands to reproduce audit checks, tests, and deployment

set -e

echo "========================================="
echo "  Agentic Workflows - Command Reference"
echo "========================================="

# STEP 1: Install Dependencies
echo -e "\n[1/10] Installing dependencies..."
python -m pip install --upgrade pip
python -m pip install -r requirements-full.txt
python -m pip install pytest pytest-cov ruff mypy bandit safety pip-audit

# STEP 2: Security Scans
echo -e "\n[2/10] Running security scans..."
echo "  - Bandit (Python security issues)..."
bandit -r agentic_workflows -lll -f json -o audit/raw-outputs/bandit-report.json || true
bandit -r agentic_workflows -lll

echo "  - pip-audit (vulnerable dependencies)..."
pip-audit --desc --format json --output audit/raw-outputs/pip-audit-report.json || true
pip-audit --desc || true

echo "  - safety check..."
safety check --json --output audit/raw-outputs/safety-report.json || true
safety check || true

# STEP 3: Code Quality Checks
echo -e "\n[3/10] Running code quality checks..."
echo "  - Ruff linter..."
ruff check . --output-format=json > audit/raw-outputs/ruff-report.json || true
ruff check .

echo "  - MyPy type checker..."
mypy agentic_workflows --ignore-missing-imports --json-report audit/raw-outputs/mypy-report || true
mypy agentic_workflows --ignore-missing-imports || true

# STEP 4: Run Tests
echo -e "\n[4/10] Running tests..."
pytest -v --maxfail=1 --disable-warnings --tb=short \
  --cov=agentic_workflows \
  --cov-report=xml:audit/raw-outputs/coverage.xml \
  --cov-report=term \
  --cov-report=html:audit/raw-outputs/htmlcov

# STEP 5: License Audit
echo -e "\n[5/10] Auditing licenses..."
pip-licenses --format=csv --output-file=audit/raw-outputs/licenses.csv || true
pip-licenses

# STEP 6: Build Docker Image
echo -e "\n[6/10] Building Docker image..."
docker build -t agentic-workflows:local -f Dockerfile .

# STEP 7: Docker Security Scan
echo -e "\n[7/10] Scanning Docker image..."
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image --severity HIGH,CRITICAL \
  --format json --output audit/raw-outputs/trivy-report.json \
  agentic-workflows:local || echo "Trivy not available - skipping"

# STEP 8: Git Status
echo -e "\n[8/10] Checking git status..."
git status --porcelain > audit/raw-outputs/git-status.txt
git rev-parse --abbrev-ref HEAD > audit/raw-outputs/git-branch.txt
git log -1 --pretty=format:"%H %s" > audit/raw-outputs/git-commit.txt

# STEP 9: Run Demo (Dry-run)
echo -e "\n[9/10] Running workflow demo (dry-run)..."
python -m agentic_workflows.runner run \
  --spec ./.kiro/specs/lazy_file_butler.yaml \
  --dry-run \
  > audit/raw-outputs/demo-output.txt 2>&1 || echo "Demo failed - check logs"

# STEP 10: Start Server (Background)
echo -e "\n[10/10] Starting server for health check..."
export DATABASE_URL="sqlite:///./test.db"
export SECRET_KEY="test-secret-key-for-demo-only"
export PORT=8080

# Start server in background
uvicorn agentic_workflows.api.server:app --host 0.0.0.0 --port 8080 &
SERVER_PID=$!

# Wait for server to start
echo "Waiting for server to start..."
sleep 5

# Test health endpoint
echo "Testing health endpoint..."
curl -s http://localhost:8080/api/health | jq . > audit/raw-outputs/health-check.json || \
  curl -s http://localhost:8080/api/health > audit/raw-outputs/health-check.json

# Test API docs
echo "Testing API docs..."
curl -s http://localhost:8080/api/docs > audit/raw-outputs/api-docs.html || true

# Stop server
echo "Stopping server..."
kill $SERVER_PID || true

echo -e "\n========================================="
echo "  All checks complete!"
echo "========================================="
echo "Results saved to: audit/raw-outputs/"
echo ""
echo "Next steps:"
echo "1. Review audit/audit-report.md"
echo "2. Apply fixes from fixes/ directory"
echo "3. Run tests again to verify"
echo "4. Deploy using deploy/README.md"
echo ""
