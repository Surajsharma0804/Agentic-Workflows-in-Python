# Contest Requirements Verification Script
# Ensures all requirements are met for submission

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "CONTEST REQUIREMENTS VERIFICATION" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

$allPassed = $true

# Requirement 1: .kiro directory exists
Write-Host "1. Checking .kiro directory..." -ForegroundColor Yellow
if (Test-Path ".kiro") {
    Write-Host "   ✅ .kiro directory exists" -ForegroundColor Green
    
    # Check contents
    $kiroFiles = Get-ChildItem -Path ".kiro" -Recurse -File
    Write-Host "   ✅ Contains $($kiroFiles.Count) files" -ForegroundColor Green
    
    # List files
    Write-Host "   Files in .kiro:" -ForegroundColor Gray
    Get-ChildItem -Path ".kiro" -Recurse -File | ForEach-Object {
        Write-Host "      - $($_.FullName.Replace((Get-Location).Path + '\', ''))" -ForegroundColor Gray
    }
} else {
    Write-Host "   ❌ .kiro directory NOT FOUND" -ForegroundColor Red
    Write-Host "   ⚠️  CRITICAL: This will result in DISQUALIFICATION!" -ForegroundColor Red
    $allPassed = $false
}

Write-Host ""

# Requirement 2: .kiro NOT in .gitignore
Write-Host "2. Checking .gitignore..." -ForegroundColor Yellow
$gitignoreContent = Get-Content .gitignore -Raw
if ($gitignoreContent -match "\.kiro") {
    Write-Host "   ❌ .kiro is in .gitignore" -ForegroundColor Red
    Write-Host "   ⚠️  CRITICAL: Remove .kiro from .gitignore!" -ForegroundColor Red
    $allPassed = $false
} else {
    Write-Host "   ✅ .kiro is NOT in .gitignore" -ForegroundColor Green
}

Write-Host ""

# Requirement 3: .kiro is tracked by git
Write-Host "3. Checking if .kiro is tracked by git..." -ForegroundColor Yellow
$trackedFiles = git ls-files .kiro
if ($trackedFiles) {
    Write-Host "   ✅ .kiro directory is tracked by git" -ForegroundColor Green
    Write-Host "   Tracked files:" -ForegroundColor Gray
    $trackedFiles | ForEach-Object {
        Write-Host "      - $_" -ForegroundColor Gray
    }
} else {
    Write-Host "   ❌ .kiro directory is NOT tracked by git" -ForegroundColor Red
    Write-Host "   ⚠️  CRITICAL: .kiro must be committed to git!" -ForegroundColor Red
    $allPassed = $false
}

Write-Host ""

# Requirement 4: Repository is public
Write-Host "4. Checking repository visibility..." -ForegroundColor Yellow
Write-Host "   ⚠️  Please verify manually that your repository is PUBLIC" -ForegroundColor Yellow
Write-Host "   Repository: https://github.com/Surajsharma0804/Agentic-Workflows-in-Python" -ForegroundColor Cyan
Write-Host "   Steps to verify:" -ForegroundColor Gray
Write-Host "      1. Visit the repository URL" -ForegroundColor Gray
Write-Host "      2. Check if you can access it in incognito/private mode" -ForegroundColor Gray
Write-Host "      3. Settings > General > Danger Zone > Change visibility" -ForegroundColor Gray

Write-Host ""

# Requirement 5: Complete project code
Write-Host "5. Checking project completeness..." -ForegroundColor Yellow

$requiredDirs = @(
    "agentic_workflows",
    "ui",
    "tests",
    ".kiro",
    ".github"
)

$allDirsExist = $true
foreach ($dir in $requiredDirs) {
    if (Test-Path $dir) {
        Write-Host "   ✅ $dir directory exists" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $dir directory missing" -ForegroundColor Red
        $allDirsExist = $false
        $allPassed = $false
    }
}

Write-Host ""

# Requirement 6: Essential files
Write-Host "6. Checking essential files..." -ForegroundColor Yellow

$requiredFiles = @(
    "README.md",
    "docker-compose.yml",
    "Dockerfile",
    "requirements.txt",
    ".env.example"
)

$allFilesExist = $true
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "   ✅ $file exists" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $file missing" -ForegroundColor Red
        $allFilesExist = $false
        $allPassed = $false
    }
}

Write-Host ""

# Summary
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "VERIFICATION SUMMARY" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

if ($allPassed) {
    Write-Host "✅ ALL REQUIREMENTS MET!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your repository is ready for contest submission!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Final Checklist:" -ForegroundColor White
    Write-Host "  ✅ .kiro directory exists and is tracked" -ForegroundColor Green
    Write-Host "  ✅ .kiro is NOT in .gitignore" -ForegroundColor Green
    Write-Host "  ✅ Complete project code included" -ForegroundColor Green
    Write-Host "  ⚠️  Verify repository is PUBLIC (manual check)" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Repository URL:" -ForegroundColor White
    Write-Host "  https://github.com/Surajsharma0804/Agentic-Workflows-in-Python" -ForegroundColor Cyan
} else {
    Write-Host "❌ SOME REQUIREMENTS NOT MET!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please fix the issues above before submitting." -ForegroundColor Red
    Write-Host ""
}

Write-Host ""
Write-Host "Contest Requirements:" -ForegroundColor White
Write-Host "  ✔️ Complete project code" -ForegroundColor Gray
Write-Host "  ✔️ /.kiro directory at the root" -ForegroundColor Gray
Write-Host "  ✔️ .kiro NOT in .gitignore" -ForegroundColor Gray
Write-Host "  ✔️ Repository must be PUBLIC" -ForegroundColor Gray
Write-Host ""
