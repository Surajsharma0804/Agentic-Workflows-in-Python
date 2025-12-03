# Cleanup and Organize Project

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   PROJECT CLEANUP & ORGANIZATION" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Create archive directory
Write-Host "Creating archive directory..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "archive/planning" | Out-Null

# Files to archive (planning/temporary docs)
$archiveFiles = @(
    "IMPLEMENTATION_ROADMAP.md",
    "TRANSFORMATION_SUMMARY.md",
    "START_ELITE_BUILD.md",
    "ELITE_UPGRADE_PLAN.md",
    "ELITE_FEATURES_ADDED.md"
)

Write-Host "Archiving planning documents..." -ForegroundColor Yellow
foreach ($file in $archiveFiles) {
    if (Test-Path $file) {
        Move-Item $file "archive/planning/" -Force
        Write-Host "  [ARCHIVED] $file" -ForegroundColor Gray
    }
}

# Files to remove (redundant/temporary)
$removeFiles = @(
    "COMPLETE_FEATURE_LIST.md",
    "COMPLETION_REPORT.md",
    "ERRORS_FIXED.md",
    "FINAL_STATUS.md",
    "FINAL_SUMMARY.md",
    "FULL_SETUP_GUIDE.md",
    "INSTALL_DOCKER_NOW.md",
    "ISSUES_RESOLVED.md",
    "NEXT_STEPS_NOW.md",
    "PROJECT_COMPLETE.md",
    "RUN_WITHOUT_DOCKER.md",
    "SIMPLE_START.md",
    "START_HERE.md",
    "STATUS.md",
    "SUCCESS_REPORT.md",
    "UI_SETUP_REQUIRED.md",
    "WHAT_TO_DO_NOW.md",
    "CLEANUP_PLAN.md",
    "start-backend-simple.ps1"
)

Write-Host "`nRemoving redundant files..." -ForegroundColor Yellow
foreach ($file in $removeFiles) {
    if (Test-Path $file) {
        Remove-Item $file -Force
        Write-Host "  [REMOVED] $file" -ForegroundColor Red
    }
}

# Clean up UI documentation
Write-Host "`nCleaning UI documentation..." -ForegroundColor Yellow
$uiRemoveFiles = @(
    "ui/TYPESCRIPT_ERRORS_EXPLAINED.md",
    "ui/fix-typescript-errors.ps1"
)

foreach ($file in $uiRemoveFiles) {
    if (Test-Path $file) {
        Remove-Item $file -Force
        Write-Host "  [REMOVED] $file" -ForegroundColor Red
    }
}

# Remove temporary scripts
Write-Host "`nRemoving temporary scripts..." -ForegroundColor Yellow
$tempScripts = @(
    "cleanup-unwanted-files.ps1",
    "start-backend.ps1"
)

foreach ($file in $tempScripts) {
    if (Test-Path $file) {
        Remove-Item $file -Force
        Write-Host "  [REMOVED] $file" -ForegroundColor Red
    }
}

# Summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   CLEANUP COMPLETE" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Essential Documentation (Root):" -ForegroundColor Yellow
$essentialDocs = @(
    "README.md",
    "QUICK_START.md",
    "SETUP.md",
    "ARCHITECTURE.md",
    "DEPLOYMENT_GUIDE.md",
    "CONTRIBUTING.md",
    "PROJECT_STATUS.md"
)

foreach ($doc in $essentialDocs) {
    if (Test-Path $doc) {
        Write-Host "  [OK] $doc" -ForegroundColor Green
    } else {
        Write-Host "  [MISSING] $doc" -ForegroundColor Red
    }
}

Write-Host "`nArchived:" -ForegroundColor Yellow
Write-Host "  archive/planning/ - Planning documents" -ForegroundColor Gray

Write-Host "`nProject is now clean and organized!" -ForegroundColor Green
Write-Host ""
