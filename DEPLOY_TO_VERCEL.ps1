# Deploy UI to Vercel Script

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "DEPLOY TO VERCEL (UI ONLY)" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "⚠️  IMPORTANT NOTE:" -ForegroundColor Yellow
Write-Host "Vercel can only deploy the FRONTEND (React UI)." -ForegroundColor Yellow
Write-Host "The BACKEND (FastAPI + Database) needs a different platform." -ForegroundColor Yellow
Write-Host ""
Write-Host "Recommended: Deploy backend to Render.com (free)" -ForegroundColor Cyan
Write-Host "See VERCEL_DEPLOYMENT.md for full instructions" -ForegroundColor Cyan
Write-Host ""

$continue = Read-Host "Continue with UI-only deployment? (Y/N)"
if ($continue -ne "Y" -and $continue -ne "y") {
    Write-Host "Deployment cancelled." -ForegroundColor Yellow
    exit
}

Write-Host ""
Write-Host "Checking Vercel CLI..." -ForegroundColor Yellow

# Check if Vercel CLI is installed
try {
    $vercelVersion = vercel --version 2>$null
    Write-Host "✅ Vercel CLI installed: $vercelVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Vercel CLI not installed" -ForegroundColor Red
    Write-Host ""
    Write-Host "Installing Vercel CLI..." -ForegroundColor Yellow
    npm install -g vercel
    Write-Host "✅ Vercel CLI installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "Navigating to UI directory..." -ForegroundColor Yellow
cd ui

Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
npm install

Write-Host ""
Write-Host "Building project..." -ForegroundColor Yellow
npm run build

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Build successful" -ForegroundColor Green
} else {
    Write-Host "❌ Build failed" -ForegroundColor Red
    Write-Host "Please fix build errors and try again" -ForegroundColor Red
    cd ..
    exit 1
}

Write-Host ""
Write-Host "Deploying to Vercel..." -ForegroundColor Yellow
Write-Host ""

vercel --prod

Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your UI is now live on Vercel!" -ForegroundColor Green
Write-Host ""
Write-Host "⚠️  IMPORTANT:" -ForegroundColor Yellow
Write-Host "The UI is deployed but the backend is NOT." -ForegroundColor Yellow
Write-Host ""
Write-Host "To make it fully functional:" -ForegroundColor White
Write-Host "  1. Deploy backend to Render.com" -ForegroundColor Gray
Write-Host "  2. Get your backend URL" -ForegroundColor Gray
Write-Host "  3. Add VITE_API_URL to Vercel environment variables" -ForegroundColor Gray
Write-Host "  4. Redeploy" -ForegroundColor Gray
Write-Host ""
Write-Host "See VERCEL_DEPLOYMENT.md for detailed instructions" -ForegroundColor Cyan
Write-Host ""

cd ..
