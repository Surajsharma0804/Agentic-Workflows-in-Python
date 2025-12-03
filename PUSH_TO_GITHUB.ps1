# Push to GitHub Script
# Repository: https://github.com/Surajsharma0804/Agentic-Workflows-in-Python.git

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "PUSHING TO GITHUB" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

$repoUrl = "https://github.com/Surajsharma0804/Agentic-Workflows-in-Python.git"

# Check if git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "Initializing Git repository..." -ForegroundColor Yellow
    git init
    Write-Host "✅ Git initialized" -ForegroundColor Green
} else {
    Write-Host "✅ Git already initialized" -ForegroundColor Green
}

# Check if .gitignore exists
if (-not (Test-Path ".gitignore")) {
    Write-Host "Creating .gitignore..." -ForegroundColor Yellow
    
    @"
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST
.pytest_cache/
.coverage
htmlcov/
*.log

# Virtual Environment
.venv/
venv/
ENV/
env/

# Environment Variables
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnpm-debug.log*

# Build
dist/
build/
*.tsbuildinfo

# Docker
*.log

# Database
*.db
*.sqlite
*.sqlite3

# Storage
storage/
logs/

# Temporary
*.tmp
*.temp
.cache/
"@ | Out-File -FilePath ".gitignore" -Encoding UTF8
    
    Write-Host "✅ .gitignore created" -ForegroundColor Green
} else {
    Write-Host "✅ .gitignore exists" -ForegroundColor Green
}

Write-Host ""
Write-Host "Adding files to Git..." -ForegroundColor Yellow
git add .

Write-Host ""
Write-Host "Creating commit..." -ForegroundColor Yellow
$commitMessage = "Initial commit: Agentic Workflows Platform with Authentication & Alert System"
git commit -m $commitMessage

Write-Host ""
Write-Host "Adding remote repository..." -ForegroundColor Yellow
try {
    git remote add origin $repoUrl 2>$null
    Write-Host "✅ Remote added" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Remote already exists, updating..." -ForegroundColor Yellow
    git remote set-url origin $repoUrl
    Write-Host "✅ Remote updated" -ForegroundColor Green
}

Write-Host ""
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
Write-Host "Repository: $repoUrl" -ForegroundColor Cyan
Write-Host ""

# Try to push
try {
    git push -u origin main
    Write-Host ""
    Write-Host "=========================================" -ForegroundColor Green
    Write-Host "✅ SUCCESSFULLY PUSHED TO GITHUB!" -ForegroundColor Green
    Write-Host "=========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Repository URL: $repoUrl" -ForegroundColor Cyan
    Write-Host ""
} catch {
    Write-Host ""
    Write-Host "⚠️  Push failed. Trying 'master' branch..." -ForegroundColor Yellow
    try {
        git branch -M main
        git push -u origin main --force
        Write-Host ""
        Write-Host "=========================================" -ForegroundColor Green
        Write-Host "✅ SUCCESSFULLY PUSHED TO GITHUB!" -ForegroundColor Green
        Write-Host "=========================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Repository URL: $repoUrl" -ForegroundColor Cyan
        Write-Host ""
    } catch {
        Write-Host ""
        Write-Host "=========================================" -ForegroundColor Red
        Write-Host "❌ PUSH FAILED" -ForegroundColor Red
        Write-Host "=========================================" -ForegroundColor Red
        Write-Host ""
        Write-Host "Please ensure:" -ForegroundColor Yellow
        Write-Host "  1. You're logged into GitHub" -ForegroundColor Gray
        Write-Host "  2. The repository exists: $repoUrl" -ForegroundColor Gray
        Write-Host "  3. You have write access to the repository" -ForegroundColor Gray
        Write-Host ""
        Write-Host "Manual push command:" -ForegroundColor Yellow
        Write-Host "  git push -u origin main" -ForegroundColor Gray
        Write-Host ""
    }
}

Write-Host "Next steps:" -ForegroundColor White
Write-Host "  1. Visit: https://github.com/Surajsharma0804/Agentic-Workflows-in-Python" -ForegroundColor Gray
Write-Host "  2. Verify all files are uploaded" -ForegroundColor Gray
Write-Host "  3. Check README.md displays correctly" -ForegroundColor Gray
Write-Host "  4. Add repository description and topics" -ForegroundColor Gray
Write-Host ""
