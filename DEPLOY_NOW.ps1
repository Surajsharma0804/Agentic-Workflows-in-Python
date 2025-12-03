# Deploy to Render.com - Quick Setup Script
# This script helps you prepare for Render deployment

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  DEPLOY TO RENDER.COM" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is available
Write-Host "1. Checking Git..." -ForegroundColor Yellow
if (Get-Command git -ErrorAction SilentlyContinue) {
    Write-Host "   ✅ Git is installed" -ForegroundColor Green
} else {
    Write-Host "   ❌ Git not found. Please install Git first." -ForegroundColor Red
    exit 1
}

# Check if we're in a git repository
Write-Host ""
Write-Host "2. Checking Git Repository..." -ForegroundColor Yellow
if (Test-Path .git) {
    Write-Host "   ✅ Git repository found" -ForegroundColor Green
} else {
    Write-Host "   ❌ Not a git repository" -ForegroundColor Red
    exit 1
}

# Check if render.yaml exists
Write-Host ""
Write-Host "3. Checking Render Configuration..." -ForegroundColor Yellow
if (Test-Path render.yaml) {
    Write-Host "   ✅ render.yaml found" -ForegroundColor Green
} else {
    Write-Host "   ❌ render.yaml not found" -ForegroundColor Red
    exit 1
}

# Check if Dockerfile exists
Write-Host ""
Write-Host "4. Checking Docker Configuration..." -ForegroundColor Yellow
if (Test-Path Dockerfile) {
    Write-Host "   ✅ Dockerfile found" -ForegroundColor Green
} else {
    Write-Host "   ❌ Dockerfile not found" -ForegroundColor Red
    exit 1
}

# Check if .kiro directory exists
Write-Host ""
Write-Host "5. Checking .kiro Directory..." -ForegroundColor Yellow
if (Test-Path .kiro) {
    Write-Host "   ✅ .kiro directory found" -ForegroundColor Green
    $kiroFiles = (Get-ChildItem .kiro -Recurse -File).Count
    Write-Host "   ✅ Contains $kiroFiles files" -ForegroundColor Green
} else {
    Write-Host "   ❌ .kiro directory not found" -ForegroundColor Red
    exit 1
}

# Check if changes need to be committed
Write-Host ""
Write-Host "6. Checking Git Status..." -ForegroundColor Yellow
$gitStatus = git status --porcelain
if ($gitStatus) {
    Write-Host "   ⚠️  You have uncommitted changes" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "   Would you like to commit and push now? (Y/N)" -ForegroundColor Cyan
    $response = Read-Host
    
    if ($response -eq "Y" -or $response -eq "y") {
        Write-Host ""
        Write-Host "   Adding files..." -ForegroundColor Yellow
        git add .
        
        Write-Host "   Committing..." -ForegroundColor Yellow
        git commit -m "Prepare for Render deployment"
        
        Write-Host "   Pushing to GitHub..." -ForegroundColor Yellow
        git push origin main
        
        Write-Host "   ✅ Changes pushed to GitHub" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Please commit and push manually before deploying" -ForegroundColor Yellow
    }
} else {
    Write-Host "   ✅ No uncommitted changes" -ForegroundColor Green
}

# Generate SECRET_KEY
Write-Host ""
Write-Host "7. Generating SECRET_KEY..." -ForegroundColor Yellow
$secretKey = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | ForEach-Object {[char]$_})
Write-Host "   ✅ SECRET_KEY generated" -ForegroundColor Green
Write-Host ""
Write-Host "   Copy this for Render environment variables:" -ForegroundColor Cyan
Write-Host "   $secretKey" -ForegroundColor White
Write-Host ""

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  READY TO DEPLOY!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Go to: https://dashboard.render.com" -ForegroundColor White
Write-Host "2. Sign up with GitHub (free)" -ForegroundColor White
Write-Host "3. Click 'New +' → 'Blueprint'" -ForegroundColor White
Write-Host "4. Select repository: Agentic-Workflows-in-Python" -ForegroundColor White
Write-Host "5. Click 'Apply'" -ForegroundColor White
Write-Host "6. Wait 5-10 minutes for deployment" -ForegroundColor White
Write-Host "7. Get your URL and share with friends!" -ForegroundColor White
Write-Host ""
Write-Host "OR use Manual Setup:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Create PostgreSQL database" -ForegroundColor White
Write-Host "2. Create Redis instance" -ForegroundColor White
Write-Host "3. Create Web Service" -ForegroundColor White
Write-Host "4. Add environment variables (including SECRET_KEY above)" -ForegroundColor White
Write-Host "5. Deploy!" -ForegroundColor White
Write-Host ""
Write-Host "📚 Full Guide: DEPLOY_TO_RENDER.md" -ForegroundColor Cyan
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Open browser
Write-Host "Would you like to open Render.com now? (Y/N)" -ForegroundColor Cyan
$openBrowser = Read-Host

if ($openBrowser -eq "Y" -or $openBrowser -eq "y") {
    Start-Process "https://dashboard.render.com"
    Write-Host "✅ Opening Render.com..." -ForegroundColor Green
}

Write-Host ""
Write-Host "Good luck with your deployment!" -ForegroundColor Green
Write-Host ""
