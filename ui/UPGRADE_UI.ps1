# UI Upgrade Script - Install dependencies and start

Write-Host "`n" -NoNewline
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   UI UPGRADE & START" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$step = 1

# Step 1: Check if we're in the UI directory
Write-Host "[$step] Checking directory..." -ForegroundColor Yellow
$step++
if (-not (Test-Path "package.json")) {
    Write-Host "  [ERROR] Not in UI directory!" -ForegroundColor Red
    Write-Host "  Please run this from the ui/ directory" -ForegroundColor Red
    exit 1
}
Write-Host "  [OK] In UI directory" -ForegroundColor Green

# Step 2: Clean install
Write-Host "`n[$step] Cleaning old dependencies..." -ForegroundColor Yellow
$step++
if (Test-Path "node_modules") {
    Remove-Item -Recurse -Force node_modules
    Write-Host "  [OK] Removed node_modules" -ForegroundColor Green
}
if (Test-Path "package-lock.json") {
    Remove-Item -Force package-lock.json
    Write-Host "  [OK] Removed package-lock.json" -ForegroundColor Green
}

# Step 3: Install dependencies
Write-Host "`n[$step] Installing dependencies..." -ForegroundColor Yellow
$step++
Write-Host "  This may take 2-3 minutes..." -ForegroundColor Gray
npm install

if ($LASTEXITCODE -eq 0) {
    Write-Host "  [OK] Dependencies installed successfully!" -ForegroundColor Green
} else {
    Write-Host "  [ERROR] Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Step 4: Start dev server
Write-Host "`n[$step] Starting development server..." -ForegroundColor Yellow
$step++

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   UI READY!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "The UI will start on: http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "Features:" -ForegroundColor Cyan
Write-Host "  ✨ Professional animations with Framer Motion" -ForegroundColor White
Write-Host "  🎨 Modern glassmorphism design" -ForegroundColor White
Write-Host "  📊 Interactive charts and visualizations" -ForegroundColor White
Write-Host "  🚀 Smooth page transitions" -ForegroundColor White
Write-Host "  💫 Loading states and skeletons" -ForegroundColor White
Write-Host "  🎯 Fully functional workflow execution" -ForegroundColor White
Write-Host ""
Write-Host "Starting server..." -ForegroundColor Yellow
Write-Host ""

npm run dev
