# Cleanup Script - Remove unnecessary files and organize project

Write-Host "🧹 Cleaning up project..." -ForegroundColor Cyan

# Remove old deployment markdown files (already archived)
$oldDocs = @(
    "check-render-status.md",
    "check-deployment.ps1",
    "pre-deploy-check.ps1",
    "test-deployment.ps1",
    "verify-deployment.ps1",
    "demo.ps1",
    "demo.sh"
)

foreach ($file in $oldDocs) {
    if (Test-Path $file) {
        Remove-Item $file -Force
        Write-Host "✓ Removed $file" -ForegroundColor Green
    }
}

# Clean up node_modules and build artifacts if requested
$response = Read-Host "Clean node_modules and build artifacts? (y/N)"
if ($response -eq 'y' -or $response -eq 'Y') {
    if (Test-Path "ui/node_modules") {
        Remove-Item "ui/node_modules" -Recurse -Force
        Write-Host "✓ Removed ui/node_modules" -ForegroundColor Green
    }
    if (Test-Path "ui/dist") {
        Remove-Item "ui/dist" -Recurse -Force
        Write-Host "✓ Removed ui/dist" -ForegroundColor Green
    }
}

# Clean Python cache
Get-ChildItem -Path . -Include __pycache__,*.pyc -Recurse -Force | Remove-Item -Recurse -Force
Write-Host "✓ Removed Python cache files" -ForegroundColor Green

# Clean test artifacts
if (Test-Path "tests/playwright/test-results") {
    Remove-Item "tests/playwright/test-results" -Recurse -Force
    Write-Host "✓ Removed test results" -ForegroundColor Green
}

Write-Host "`n✅ Cleanup complete!" -ForegroundColor Green
Write-Host "Run 'npm install' in ui/ folder to reinstall dependencies" -ForegroundColor Yellow
