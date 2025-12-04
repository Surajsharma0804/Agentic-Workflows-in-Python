# Agentic Workflows - Automated Demo Script (Windows)
# For Competition Judges

$ErrorActionPreference = "Stop"

Write-Host "🚀 Agentic Workflows - Competition Demo Setup" -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host ""

# Check if running in correct directory
if (-not (Test-Path "pyproject.toml")) {
    Write-Host "Error: Please run this script from the agentic-workflows directory" -ForegroundColor Red
    exit 1
}

Write-Host "Step 1/5: Checking prerequisites..." -ForegroundColor Blue

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Python 3 is not installed. Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

# Check Node.js
try {
    $nodeVersion = node --version
    Write-Host "✓ Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "Node.js is not installed. Please install Node.js 18+" -ForegroundColor Red
    exit 1
}

# Check npm
try {
    $npmVersion = npm --version
    Write-Host "✓ npm found: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "npm is not installed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Step 2/5: Setting up Python backend..." -ForegroundColor Blue

# Create virtual environment if it doesn't exist
if (-not (Test-Path ".venv")) {
    Write-Host "Creating Python virtual environment..."
    python -m venv .venv
}

# Activate virtual environment
& .\.venv\Scripts\Activate.ps1

# Install Python dependencies
Write-Host "Installing Python dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements-full.txt

Write-Host "✓ Backend dependencies installed" -ForegroundColor Green

Write-Host ""
Write-Host "Step 3/5: Setting up React frontend..." -ForegroundColor Blue

Set-Location ui

# Install Node dependencies
Write-Host "Installing Node dependencies..."
npm install --silent

Write-Host "✓ Frontend dependencies installed" -ForegroundColor Green

Write-Host ""
Write-Host "Step 4/5: Running tests..." -ForegroundColor Blue

# Run type check
Write-Host "Type checking..."
npm run type-check

# Run unit tests
Write-Host "Running unit tests..."
npm run test -- --run

Write-Host "✓ All tests passed" -ForegroundColor Green

Write-Host ""
Write-Host "Step 5/5: Building application..." -ForegroundColor Blue

# Build frontend
Write-Host "Building frontend..."
npm run build

Write-Host "✓ Build successful" -ForegroundColor Green

Set-Location ..

Write-Host ""
Write-Host "==============================================" -ForegroundColor Green
Write-Host "✨ Setup Complete!" -ForegroundColor Green
Write-Host "==============================================" -ForegroundColor Green
Write-Host ""

Write-Host "📋 Next Steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Start the backend server:"
Write-Host "   python -m agentic_workflows.api.server" -ForegroundColor Blue
Write-Host ""
Write-Host "2. In a new terminal, start the frontend:"
Write-Host "   cd ui; npm run dev" -ForegroundColor Blue
Write-Host ""
Write-Host "3. Open your browser:"
Write-Host "   http://localhost:3000" -ForegroundColor Blue
Write-Host ""
Write-Host "🎬 Demo Flow:" -ForegroundColor Yellow
Write-Host "   1. Register a new account"
Write-Host "   2. Explore the dashboard"
Write-Host "   3. Run a workflow"
Write-Host "   4. View AI agents"
Write-Host "   5. Check audit logs"
Write-Host "   6. Visualize DAG"
Write-Host ""
Write-Host "📚 Documentation:" -ForegroundColor Yellow
Write-Host "   - README.md - Project overview"
Write-Host "   - SUBMISSION.md - Competition guide"
Write-Host "   - ARCHITECTURE.md - Technical details"
Write-Host ""
Write-Host "Good luck with the demo! 🚀" -ForegroundColor Green
Write-Host ""

# Optional: Start servers automatically
$response = Read-Host "Would you like to start the servers now? (y/n)"
if ($response -eq "y" -or $response -eq "Y") {
    Write-Host ""
    Write-Host "Starting backend server..." -ForegroundColor Blue
    Start-Process python -ArgumentList "-m", "agentic_workflows.api.server" -NoNewWindow
    
    Write-Host "Waiting for backend to start..." -ForegroundColor Blue
    Start-Sleep -Seconds 5
    
    Write-Host "Starting frontend server..." -ForegroundColor Blue
    Set-Location ui
    Start-Process npm -ArgumentList "run", "dev" -NoNewWindow
    
    Write-Host ""
    Write-Host "Servers started!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
    Write-Host ""
    
    # Keep script running
    while ($true) {
        Start-Sleep -Seconds 1
    }
}
